#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A tiny fake Voyager bridge for adapter/CBAP tests.

This is not Minecraft and not Voyager. It implements only the HTTP surface
used by agents/voyager/adapter/adapter.mjs so the adapter can be tested
without a Java server, Node dependencies, or a live bot.
"""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class State:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.x = 0.0
        self.y = 64.0
        self.z = 0.0
        self.stopped = False
        self.chat: list[str] = []
        self.step_calls = 0

    def observe(self) -> list:
        with self.lock:
            return [[
                "observe",
                {
                    "status": {
                        "position": {"x": self.x, "y": self.y, "z": self.z},
                        "health": 20,
                        "food": 20,
                        "onGround": True,
                        "name": "fake-voyager",
                        "equipment": [None, None, None, None, None],
                    },
                    "inventory": {},
                },
            ]]

    def step(self, code: str) -> list:
        with self.lock:
            self.step_calls += 1
            if "setControlState('forward'" in code:
                self.z += 0.2
            if "bot.chat(" in code:
                # Keep this deliberately small; the adapter only needs status.
                self.chat.append(code[:200])
        return []


class Handler(BaseHTTPRequestHandler):
    state: State

    def log_message(self, fmt: str, *args) -> None:
        pass

    def _json(self, data, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/state":
            self._json(self.state.observe())
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        n = int(self.headers.get("content-length", "0") or "0")
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            payload = {}
        if self.path == "/step":
            self._json(self.state.step(str(payload.get("code", ""))))
        elif self.path == "/stop":
            with self.state.lock:
                self.state.stopped = True
            self._json({"ok": True})
        elif self.path == "/start":
            self._json({"ok": True})
        else:
            self._json({"error": "not found"}, 404)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    state = State()
    Handler.state = state
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    port = srv.server_address[1]
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump({"port": port}, f)
    print(f"fake-voyager http://{args.host}:{port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
