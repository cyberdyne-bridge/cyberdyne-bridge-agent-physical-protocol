#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercise the Voyager adapter against a fake bridge, then CBAP end to end.

This proves the adapter/CBAP plumbing without claiming a real Minecraft run.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

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

DEVICE = "mc://voyager/bot"


def wait_http(url: str, timeout: float = 8.0) -> None:
    end = time.time() + timeout
    last = None
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status == 200:
                    return
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(0.1)
    raise RuntimeError(f"bridge did not start: {last}")


def wait_socket(path: str, proc: subprocess.Popen, timeout: float = 8.0) -> None:
    end = time.time() + timeout
    while time.time() < end:
        if os.path.exists(path):
            return
        if proc.poll() is not None:
            out = proc.stdout.read() if proc.stdout else ""
            err = proc.stderr.read() if proc.stderr else ""
            raise RuntimeError(f"adapter exited {proc.returncode}: {out} {err}")
        time.sleep(0.1)
    raise RuntimeError("adapter socket did not appear")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", default=os.environ.get("NODE", "node"))
    ap.add_argument("--out", default=os.path.join(ROOT, "logs", "voyager-fake.json"))
    args = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="cbap-voyager-fake-")
    bridge_out = os.path.join(tmp, "bridge-port.json")
    adapter_sock = os.path.join(tmp, "adapter.sock")
    kernel_sock = os.path.join(tmp, "kernel.sock")
    bridge_log = open(os.path.join(tmp, "bridge.log"), "w+", encoding="utf-8")
    adapter_log = open(os.path.join(tmp, "adapter.log"), "w+", encoding="utf-8")
    bridge = adapter = kernel = driver = client = None
    report = {"ok": False, "mode": "fake-bridge", "steps": []}
    try:
        bridge = subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "agents/voyager/tools/fake_voyager_bridge.py"),
             "--out", bridge_out],
            stdout=bridge_log, stderr=subprocess.STDOUT,
        )
        wait_http_once = time.time() + 8
        while not os.path.exists(bridge_out):
            if time.time() > wait_http_once:
                raise RuntimeError("fake bridge did not publish a port")
            time.sleep(0.05)
        with open(bridge_out, encoding="utf-8") as f:
            port = json.load(f)["port"]
        base = f"http://127.0.0.1:{port}"
        wait_http(base + "/state")

        adapter = subprocess.Popen(
            [args.node, os.path.join(ROOT, "agents/voyager/adapter/adapter.mjs"),
             "--bridge", base, "--socket", adapter_sock],
            stdout=adapter_log, stderr=subprocess.STDOUT,
        )
        wait_socket(adapter_sock, adapter)

        driver = McDriver(
            adapter_sock,
            device_path=os.path.join(ROOT, "agents/voyager/adapter/device.json"),
            mapping_path=os.path.join(ROOT, "agents/voyager/adapter/mapping.json"),
            connect_timeout=5, reconnect=True,
        )
        driver.connect()
        policy = {"default": {"devices": ["*"],
                              "capabilities": ["read", "write", "lease", "estop"]},
                  "agents": {}}
        kernel = KernelServer(drivers=[driver], socket_path=kernel_sock,
                              audit_path=os.path.join(tmp, "audit.jsonl"),
                              policy=policy)
        if not kernel.start():
            raise RuntimeError("kernel did not start")
        client = CBAPClient(kernel_sock, agent_id="voyager-fake-probe")
        client.connect()
        client.hello()

        def step(name: str, ok: bool, detail=None) -> None:
            report["steps"].append({"name": name, "ok": bool(ok), "detail": detail})
            print(("OK  " if ok else "FAIL") + " " + name +
                  ("" if detail is None else " :: " + str(detail)[:300]), flush=True)

        devices = client.device_list()["payload"]["devices"]
        step("Voyager device visible", devices and devices[0]["device_id"] == DEVICE, devices)
        opened = client.open(DEVICE)
        fd = opened["payload"]["fd"]
        r = client.read(fd, "body", 3000)
        before = ((r.get("payload") or {}).get("frame") or {}).get("body", {}).get("pos")
        step("read synthetic state", bool(before), before)
        step("lease", client.lease(fd).get("ok"))

        _, _, rf = client.write(fd, {"channel": "body", "op": "forward", "args": {}},
                                deadline_ms=30000, timeout=30)
        step("forward under lease", rf.get("ok"), rf.get("payload") or rf.get("error"))

        after = None
        end = time.time() + 5
        while time.time() < end:
            r = client.read(fd, "body", 2000)
            after = ((r.get("payload") or {}).get("frame") or {}).get("body", {}).get("pos")
            if before and after and before != after:
                break
            time.sleep(0.2)
        step("synthetic position changed", bool(before and after and before != after),
             {"before": before, "after": after})

        _, _, rs = client.write(fd, {"channel": "chat", "op": "say",
                                     "args": {"text": "voyager fake bridge works"}},
                                deadline_ms=30000, timeout=30)
        step("say under lease", rs.get("ok"), rs.get("payload") or rs.get("error"))
        est = client.estop(fd, reason="voyager-fake-probe")
        step("estop", est.get("ok"), est.get("payload") or est.get("error"))
        end = time.time() + 3
        while time.time() < end and adapter.poll() is None:
            time.sleep(0.1)
        step("adapter exited after estop", adapter.poll() is not None,
             {"returncode": adapter.poll()})
        report["ok"] = all(s["ok"] for s in report["steps"])
    except Exception as e:
        report["error"] = str(e)
        print("FAIL exception ::", e, flush=True)
    finally:
        for p in (client, kernel, driver):
            try:
                if p:
                    p.close()
            except Exception:
                pass
        for p in (adapter, bridge):
            try:
                if p and p.poll() is None:
                    p.terminate()
                    p.wait(timeout=3)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        for f in (bridge_log, adapter_log):
            try:
                f.close()
            except Exception:
                pass
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps({"ok": report["ok"], "mode": report["mode"],
                          "steps": len(report["steps"]),
                          "out": args.out,
                          "failed": [s for s in report["steps"] if not s["ok"]],
                          "error": report.get("error")}, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
