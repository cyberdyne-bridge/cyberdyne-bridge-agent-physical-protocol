#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe an MCP HTTP endpoint for tool-order and definition stability.

Order and definition are separate properties:

    definition  full tool object + instructions + serverInfo (order-normalized)
    order       the wire order of tool names across repeated tools/list calls

Usage:
    python3 tools/mcp_order_probe.py --url http://127.0.0.1:3018/mcp
    python3 tools/mcp_order_probe.py --url ... --probes 5 --json
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from drivers.mcp_device.definition import (  # noqa: E402
    definition_digest, order_stability, tool_order,
)

META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {"name": "mcp-order-probe", "version": "1.0"},
    "io.modelcontextprotocol/clientCapabilities": {},
}
INIT = {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {"name": "mcp-order-probe", "version": "1.0"},
}


def post(url: str, method: str, params: dict, session: str | None = None):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                       "params": params}).encode()
    headers = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream"}
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", "replace")
            hdrs = dict(resp.headers)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        hdrs = dict(exc.headers)
    if not raw.strip():
        return {}, hdrs
    if raw.lstrip().startswith("event:") or "\ndata:" in raw:
        data = [line[5:].strip() for line in raw.splitlines()
                if line.startswith("data:")]
        raw = "\n".join(data) or "{}"
    return json.loads(raw), hdrs


def probe(url: str, probes: int) -> dict:
    discover, _ = post(url, "server/discover", {"_meta": META})
    if "result" in discover:
        era = "modern"
        result = discover["result"]
        server = dict(result.get("serverInfo") or {})
        server["instructions"] = result.get("instructions") or ""
        params = {"_meta": META}
        session = None
    else:
        init, headers = post(url, "initialize", INIT)
        era = "legacy"
        session = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
        result = init.get("result") or {}
        server = dict(result.get("serverInfo") or {})
        server["instructions"] = result.get("instructions") or ""
        post(url, "notifications/initialized", {}, session)
        params = {}

    calls = []
    for _ in range(max(1, probes)):
        response, _ = post(url, "tools/list", params, session)
        calls.append((response.get("result") or {}).get("tools") or [])

    orders = [tool_order(tools) for tools in calls]
    digests = [definition_digest(server, tools) for tools in calls]
    order = order_stability(orders)
    definition_stable = len(set(digests)) == 1
    return {
        "url": url,
        "era": era,
        "server": server,
        "tools_count": len(calls[0]) if calls else 0,
        "order": order,
        "definition_stable": definition_stable,
        "definition_digests": digests,
        "sequences": [list(o) for o in orders],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--probes", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on order warning or definition change")
    a = ap.parse_args(argv)

    result = probe(a.url, a.probes)
    order = result["order"]
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"URL:        {result['url']}")
        print(f"era:        {result['era']}")
        print(f"server:     {result['server'].get('name')} "
              f"{result['server'].get('version')}")
        print(f"tools:      {result['tools_count']}")
        print(f"order:      {order['status'].upper()} — {order['reason']}")
        for seq in order["distinct"]:
            print(f"            {','.join(seq)}")
        print(f"definition: {'STABLE' if result['definition_stable'] else 'CHANGED'}")
        print(f"            {result['definition_digests'][0]} -> "
              f"{result['definition_digests'][-1]}")

    if a.strict and (order["status"] == "warning"
                     or not result["definition_stable"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
