#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Body Self-Check：三个探针，回答「身体还在不在」。

协议 conformance 证明命令发得对；这里证明身体没坏透——
帧率正常、内存正常、日志没有 error，画面却是空的，是这一层要抓的故障。

用法：
  python3 tools/body_selfcheck.py --target fake
  python3 tools/body_selfcheck.py --target broken --mode blank
  python3 tools/body_selfcheck.py --body mypkg:make_body --rounds 8 --json

规范：spec/body-selfcheck.md
退出码：0 全过；1 有失败；2 用法/加载错误
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import random
import string
import sys
import time
from dataclasses import dataclass
from typing import Any, Protocol

SPEC = "body-selfcheck/0.1"
DEFAULT_ROUNDS = 5
DEFAULT_GROWTH_KB = 2048
RENDER_STATES = ("thinking", "working", "error")


class Body(Protocol):
    """探针需要的最小身体接口。"""

    def send(self, action: str, args: dict[str, Any]) -> dict[str, Any]:
        ...

    def snapshot(self) -> dict[str, Any]:
        ...


@dataclass
class Check:
    id: str
    ok: bool
    detail: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "ok": self.ok, "detail": self.detail}


class FakeBody:
    """健康的假身体：状态会变，指纹跟着变，资源不涨。"""

    def __init__(self) -> None:
        self.state = "idle"
        self.turns = 0
        self.degraded = False
        self.degraded_reason: str | None = None

    def send(self, action: str, args: dict[str, Any]) -> dict[str, Any]:
        self.turns += 1
        if action == "say":
            self.state = str(args.get("text", self.state))
        elif action == "state":
            self.state = str(args.get("state", self.state))
        return {"ok": True, "state": self.state}

    def snapshot(self) -> dict[str, Any]:
        return {
            "frame_hash": f"h-{self.state}",
            "rss_kb": 120_000 + (self.turns % 3),   # 有小幅抖动，但不上涨
            "fds": 12,
            "degraded": self.degraded,
            "degraded_reason": self.degraded_reason,
        }


class BrokenBody(FakeBody):
    """演示用：按 mode 分别弄坏一个探针。"""

    MODES = ("input", "leak", "blank", "degraded")

    def __init__(self, mode: str = "input") -> None:
        if mode not in self.MODES:
            raise ValueError(f"unknown mode: {mode!r}")
        super().__init__()
        self.mode = mode
        self._rss = 120_000

    def send(self, action: str, args: dict[str, Any]) -> dict[str, Any]:
        self.turns += 1
        if self.mode == "input":
            return {"ok": True}                  # 回 ok，但什么都不落地
        if self.mode == "leak":
            self._rss += 900                     # 每轮涨 900 KB
        if action == "say":
            self.state = str(args.get("text", self.state))
        elif action == "state":
            self.state = str(args.get("state", self.state))
        return {"ok": True}

    def snapshot(self) -> dict[str, Any]:
        if self.mode == "blank":
            return {"frame_hash": "h-blank", "rss_kb": self._rss, "fds": 12,
                    "degraded": False, "degraded_reason": None}
        if self.mode == "degraded":
            return {"frame_hash": f"h-{self.state}", "rss_kb": self._rss, "fds": 12,
                    "degraded": True, "degraded_reason": "software renderer fallback"}
        return {"frame_hash": f"h-{self.state}", "rss_kb": self._rss, "fds": 12,
                "degraded": False, "degraded_reason": None}


# --------------------------------------------------------------------------
# 探针


def probe_input(body: Body) -> Check:
    """写下去的动作，真的到达了目标表面吗？"""
    token = "probe-" + "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    try:
        body.send("say", {"text": token})
        snap = body.snapshot()
    except Exception as exc:                      # fail-closed
        return Check("input.liveness", False, {"error": f"{type(exc).__name__}: {exc}"})
    blob = json.dumps(snap, ensure_ascii=False, default=str)
    ok = token in blob
    return Check("input.liveness", ok, {
        "token": token,
        "echoed": ok,
        "hint": None if ok else "动作返回了 ok，但身体没有任何可观测痕迹",
    })


def probe_growth(body: Body, rounds: int, limit_kb: int) -> Check:
    """同一动作重复 N 次，资源会不会越长越胖？"""
    samples: list[int] = []
    try:
        body.send("state", {"state": "working"})      # 预热，丢掉首轮分配
        body.snapshot()
        for _ in range(max(2, rounds)):
            body.send("state", {"state": "working"})
            snap = body.snapshot()
            rss = snap.get("rss_kb")
            if not isinstance(rss, (int, float)):
                return Check("resource.growth", False, {
                    "error": "snapshot() 没有 rss_kb", "got": type(rss).__name__,
                })
            samples.append(int(rss))
    except Exception as exc:
        return Check("resource.growth", False, {"error": f"{type(exc).__name__}: {exc}"})

    growth = max(samples) - min(samples)
    ok = growth <= limit_kb
    return Check("resource.growth", ok, {
        "rss_growth_kb": growth,
        "limit_kb": limit_kb,
        "samples": len(samples),
        "min_kb": min(samples),
        "max_kb": max(samples),
    })


def probe_render(body: Body) -> Check:
    """不同的状态，画出来是不是真的不一样？"""
    hashes: list[str] = []
    try:
        for state in RENDER_STATES:
            body.send("state", {"state": state})
            snap = body.snapshot()
            h = snap.get("frame_hash")
            if not isinstance(h, str) or not h:
                return Check("render.variance", False, {
                    "error": "snapshot() 没有 frame_hash", "state": state,
                })
            hashes.append(h)
    except Exception as exc:
        return Check("render.variance", False, {"error": f"{type(exc).__name__}: {exc}"})

    distinct = len(set(hashes))
    ok = distinct >= 2
    return Check("render.variance", ok, {
        "distinct": distinct,
        "samples": len(hashes),
        "hashes": hashes,
        "hint": None if ok else "不同状态输出同一指纹：画面可能卡死或为空",
    })


# --------------------------------------------------------------------------
# 编排


def run(body: Body, *, rounds: int = DEFAULT_ROUNDS,
        growth_limit_kb: int = DEFAULT_GROWTH_KB,
        target: str = "custom") -> dict[str, Any]:
    checks = [
        probe_input(body),
        probe_growth(body, rounds, growth_limit_kb),
        probe_render(body),
    ]

    degraded = False
    reason = None
    try:
        snap = body.snapshot() or {}
        degraded = bool(snap.get("degraded"))
        reason = snap.get("degraded_reason")
    except Exception:
        degraded = True
        reason = reason or "snapshot() 不可用"

    ok = all(c.ok for c in checks) and not degraded
    return {
        "spec": SPEC,
        "target": target,
        "rounds": rounds,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "degraded": degraded,
        "degraded_reason": reason,
        "ok": ok,
        "checks": [c.as_dict() for c in checks],
    }


def load_body(spec: str) -> Body:
    """--body module:factory，factory 返回一个 Body。"""
    if ":" not in spec:
        raise ValueError("--body 需要 module:factory 形式")
    module_name, factory_name = spec.split(":", 1)
    module = importlib.import_module(module_name)
    factory = getattr(module, factory_name)
    body = factory() if callable(factory) else factory
    for method in ("send", "snapshot"):
        if not hasattr(body, method):
            raise TypeError(f"{spec} 返回的对象缺少 {method}()")
    return body


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="body_selfcheck",
        description="Body Self-Check：输入区 / 资源增长 / 渲染输出 三探针",
    )
    p.add_argument("--target", default="fake", choices=["fake", "broken"],
                   help="内置目标（真实身体请用 --body）")
    p.add_argument("--mode", default="input", choices=list(BrokenBody.MODES),
                   help="--target broken 时弄坏哪一项")
    p.add_argument("--body", default=None, help="外部身体：module:factory")
    p.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS)
    p.add_argument("--growth-limit-kb", type=int, default=DEFAULT_GROWTH_KB)
    p.add_argument("--json", action="store_true", help="只输出 JSON")
    args = p.parse_args(argv)

    try:
        if args.body:
            body = load_body(args.body)
            target = args.body
        elif args.target == "broken":
            body = BrokenBody(args.mode)
            target = f"broken:{args.mode}"
        else:
            body = FakeBody()
            target = "fake"
    except Exception as exc:
        print(f"[body_selfcheck] 加载失败: {exc}", file=sys.stderr)
        return 2

    report = run(body, rounds=args.rounds,
                 growth_limit_kb=args.growth_limit_kb, target=target)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Body Self-Check {SPEC} · target={target} · rounds={args.rounds}")
        for c in report["checks"]:
            print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['id']:<18} "
                  f"{json.dumps(c['detail'], ensure_ascii=False)}")
        if report["degraded"]:
            print(f"  [WARN] degraded: {report['degraded_reason']}")
        print(f"\n结果：{'全部通过' if report['ok'] else '有失败项'}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
