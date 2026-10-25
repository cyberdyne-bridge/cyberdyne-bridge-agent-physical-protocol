#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local-Qwen, Voyager-prompt action planner over the Voyager CBAP body.

This is not VoyagerEnv and does not run the upstream curriculum. It reuses
Voyager's action prompt/response contract, local skill retrieval and a local
OpenAI-compatible Qwen server. No GPT-4 or OpenAI embeddings are used.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(ROOT, "kernel")):
    parent = os.path.dirname(ROOT)
    if parent == ROOT:
        break
    ROOT = parent
sys.path.insert(0, ROOT)

from drivers.mc.driver import McDriver
from kernel.legacy_runtime.client import CBAPClient
from kernel.legacy_runtime.server import KernelServer
from agents.voyager.planner.local_embeddings import LocalHashingEmbeddings, SkillMemory

DEVICE = "mc://voyager/bot"
DEFAULT_LLM = "http://127.0.0.1:8099/v1/chat/completions"
DEFAULT_TASK = "Say exactly 'qwen voyager 121', then stop."

HELPERS = r'''
async function moveForward(bot) {
  bot.setControlState("forward", true);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  bot.setControlState("forward", false);
}

async function say(bot, text) {
  bot.chat(text);
}
'''


def load_prompt(name: str) -> str:
    path = Path(__file__).resolve().parent / "prompts" / name
    return path.read_text(encoding="utf-8")


def qwen_chat(url: str, messages: list[dict], model: str = "local",
              timeout: float = 180, max_tokens: int = 700) -> str:
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return str(data["choices"][0]["message"].get("content", ""))


def extract_code(text: str) -> tuple[str, str]:
    matches = re.findall(r"```(?:javascript|js)?\s*(.*?)```", text or "",
                         flags=re.DOTALL | re.IGNORECASE)
    code = "\n\n".join(x.strip() for x in matches if x.strip())
    if not code:
        # Some local models omit fences.  Keep from the first async function.
        m = re.search(r"(async\s+function\s+\w+\s*\([^)]*\)\s*\{.*)",
                      text or "", flags=re.DOTALL)
        code = m.group(1).strip() if m else ""
    if not code:
        raise ValueError("Qwen response contains no JavaScript code fence")
    names = re.findall(r"async\s+function\s+(\w+)\s*\(\s*bot\s*\)", code)
    if not names:
        raise ValueError("Qwen code has no async function taking bot")
    return code, f"await {names[-1]}(bot);"


def observations(body: dict) -> str:
    return json.dumps({
        "position": body.get("pos"),
        "health": body.get("hp"),
        "food": body.get("food"),
        "acting": body.get("acting"),
        "inventory": body.get("items"),
        "chat": body.get("chat"),
    }, ensure_ascii=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", default=DEFAULT_LLM)
    ap.add_argument("--model", default="local")
    ap.add_argument("--adapter", default="/tmp/voyager-cbap.sock")
    ap.add_argument("--task", default=DEFAULT_TASK)
    ap.add_argument("--tries", type=int, default=3)
    ap.add_argument("--server-log", default="")
    ap.add_argument("--out", default=os.path.join(ROOT, "logs", "voyager-local-qwen.json"))
    args = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="cbap-voyager-qwen-")
    report: dict = {"ok": False, "task": args.task, "model": args.model,
                    "mode": "local-qwen + Voyager prompt + CBAP",
                    "llm": args.llm, "steps": []}
    client = kernel = driver = None
    skill = SkillMemory()
    skill.add(
        "moveForward",
        "Move the bot forward for one second using Mineflayer control state.",
        "async function moveForward(bot) {\n"
        "  bot.setControlState('forward', true);\n"
        "  await new Promise(r => setTimeout(r, 1000));\n"
        "  bot.setControlState('forward', false);\n"
        "}",
    )
    skill.add(
        "say",
        "Send a chat message from the bot.",
        "async function say(bot, text) { bot.chat(text); }",
    )
    retrieved = skill.retrieve(args.task, k=2)
    programs = HELPERS + "\n\n" + "\n\n".join(x["code"] for x in retrieved)
    template = load_prompt("action_template.txt")
    response_format = load_prompt("action_response_format.txt")
    system = template.format(programs=programs, response_format=response_format)

    log_offset = 0
    if args.server_log and os.path.exists(args.server_log):
        log_offset = os.path.getsize(args.server_log)

    def log_has(text: str) -> bool:
        if not args.server_log or not os.path.exists(args.server_log):
            return False
        with open(args.server_log, "rb") as f:
            f.seek(log_offset)
            return text.encode("utf-8") in f.read()

    def step(name: str, ok: bool, detail=None) -> None:
        report["steps"].append({"name": name, "ok": bool(ok), "detail": detail})
        print(("OK  " if ok else "FAIL") + " " + name +
              ("" if detail is None else " :: " + str(detail)[:500]), flush=True)

    try:
        driver = McDriver(
            args.adapter,
            device_path=os.path.join(ROOT, "agents/voyager/adapter/device.json"),
            mapping_path=os.path.join(ROOT, "agents/voyager/adapter/mapping.json"),
            connect_timeout=5, reconnect=True,
        )
        driver.connect()
        policy = {"default": {"devices": ["*"],
                              "capabilities": ["read", "write", "lease", "estop"]},
                  "agents": {}}
        kernel = KernelServer(drivers=[driver], socket_path=os.path.join(tmp, "kernel.sock"),
                              audit_path=os.path.join(tmp, "audit.jsonl"),
                              policy=policy)
        if not kernel.start():
            raise RuntimeError("kernel did not start")
        client = CBAPClient(os.path.join(tmp, "kernel.sock"), agent_id="qwen-voyager")
        client.connect(); client.hello()
        devices = client.device_list()["payload"]["devices"]
        step("device visible", devices and devices[0]["device_id"] == DEVICE, devices)
        fd = client.open(DEVICE)["payload"]["fd"]
        step("lease", client.lease(fd).get("ok"))
        r = client.read(fd, "body", 3000)
        before_body = ((r.get("payload") or {}).get("frame") or {}).get("body") or {}
        before = before_body.get("pos")
        step("initial state", bool(before), before)

        history: list[dict] = []
        got_movement = False
        got_chat = False
        for attempt in range(1, args.tries + 1):
            human = f"""Task: {args.task}

Current observation:
{observations(before_body)}

Previous attempt:
{json.dumps(history[-1], ensure_ascii=False) if history else 'None'}

Return Explain, Plan, and Code in the required format. The main code must
define one async function taking bot, and the function should actually perform
the task. Use moveForward(bot) and say(bot, text) where useful.
"""
            try:
                text = qwen_chat(args.llm, [
                    {"role": "system", "content": system},
                    {"role": "user", "content": human},
                ], model=args.model)
                code, call = extract_code(text)
                # Do not rewrite function definitions. Calls may be awaited;
                # the bridge's onChat and the server log are checked separately.
                step(f"Qwen code attempt {attempt}", True, text[:500])
                _, _, res = client.write(
                    fd,
                    {"channel": "body", "op": "exec",
                     "args": {"code": HELPERS + "\n\n" + code + "\n\n" + call}},
                    deadline_ms=60000, timeout=60,
                )
                payload = res.get("payload") or {}
                on_chat = payload.get("onChat") or []
                step(f"exec attempt {attempt}", bool(res.get("ok")),
                     {"onChat": on_chat, "error": res.get("error")})
                time.sleep(0.5)
                r2 = client.read(fd, "body", 3000)
                after_body = ((r2.get("payload") or {}).get("frame") or {}).get("body") or {}
                after = after_body.get("pos")
                moved = bool(before and after and before != after)
                chatted = (bool(on_chat) or
                           "qwen voyager 121" in json.dumps(after_body) or
                           log_has("qwen voyager 121"))
                got_movement = got_movement or moved
                got_chat = got_chat or chatted
                history.append({"attempt": attempt, "code": code, "call": call,
                                "ok": bool(res.get("ok")), "moved": moved,
                                "on_chat": on_chat, "error": res.get("error")})
                step(f"attempt {attempt} observed", moved or chatted,
                     {"before": before, "after": after, "moved": moved,
                      "chat": chatted})
                if moved and chatted:
                    break
            except Exception as e:  # noqa: BLE001
                history.append({"attempt": attempt, "error": str(e)})
                step(f"attempt {attempt} exception", False, str(e))
        step("movement observed (optional)", got_movement, {"before": before,
                                                            "after": history[-1].get("after") if history else None})
        step("chat observed", got_chat, {"history": history[-1] if history else None,
                                          "server_log": bool(args.server_log)})
        report["before"] = before
        report["history"] = history
        report["skills_retrieved"] = [x["name"] for x in retrieved]
        report["ok"] = bool(got_chat and history and
                            all(x.get("ok") for x in history[-1:] if "ok" in x))
    except Exception as e:
        report["error"] = str(e)
        step("exception", False, str(e))
    finally:
        for obj in (client, kernel, driver):
            try:
                if obj:
                    obj.close()
            except Exception:
                pass
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps({"ok": report["ok"], "out": args.out,
                          "steps": len(report["steps"]),
                          "before": report.get("before"),
                          "skills": report.get("skills_retrieved"),
                          "errors": [x for x in report["steps"] if not x["ok"]]},
                         ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
