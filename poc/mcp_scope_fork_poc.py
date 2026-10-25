#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEP #3452 PoC: authenticated HTTP MCP scope / fork visibility.

This is a controlled fixture, not a production server and not a claim about a
specific MCP implementation.  It demonstrates four things:

1. two sessions with the same read scope get the same definitions;
2. read vs admin scope legitimately differ;
3. a same-scope fork is visible only when the full digest is compared;
4. an instructions-only change is invisible to a four-field tool digest.

Run:
    python3 poc/mcp_scope_fork_poc.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from poc.mcp_auth_fixture import (  # noqa: E402
    MCPHTTPClient, MCPHTTPFixture, digest, four_field_digest, snapshot,
)


def snap(server: MCPHTTPFixture, token: str) -> dict:
    client = MCPHTTPClient(server.url, token)
    data = snapshot(client)
    return {
        "client": token,
        "tools": [t["name"] for t in data["tools"]],
        "instructions": data["instructions"],
        "full": digest(data),
        "four_field": four_field_digest(data["tools"]),
        "snapshot": data,
    }


def show(label: str, a: dict, b: dict) -> None:
    print(f"\n=== {label} ===")
    for row in (a, b):
        print(f"client       : {row['client']}")
        print(f"tools        : {row['tools']}")
        print(f"instructions : {row['instructions'][:88]!r}")
        print(f"full digest  : {row['full']}")
        print(f"4-field      : {row['four_field']}")
    print(f"tools equal  : {a['tools'] == b['tools']}")
    print(f"full equal   : {a['full'] == b['full']}")
    print(f"4-field equal: {a['four_field'] == b['four_field']}")


def main() -> int:
    server = MCPHTTPFixture().start()
    try:
        print("controlled authenticated HTTP MCP fixture")
        print(f"endpoint: {server.url}")
        print("tokens: reader-a/read, reader-b/read, admin/admin")

        # 1. Same scope, two sessions: should match.
        server.state.reset()
        a = snap(server, "reader-a")
        b = snap(server, "reader-b")
        show("1. same read scope, two sessions", a, b)
        assert a["full"] == b["full"], "same scope must be stable"

        # 2. Different scopes: legitimate difference.
        server.state.reset()
        read = snap(server, "reader-a")
        admin = snap(server, "admin")
        show("2. read vs admin scope (legitimate difference)", read, admin)
        assert "delete_file" not in read["tools"]
        assert "delete_file" in admin["tools"]
        assert read["full"] != admin["full"]

        # 3. Same scope, forked view: full digest detects it.
        server.state.reset()
        server.state.mode = "fork_same_scope"
        benign = snap(server, "reader-a")
        forked = snap(server, "reader-b")
        show("3. same read scope, forked view", benign, forked)
        assert "exfiltrate" not in benign["tools"]
        assert "exfiltrate" in forked["tools"]
        assert benign["full"] != forked["full"], "fork should be detected"

        # 4. Instructions-only change: four-field digest misses it.
        server.state.reset()
        normal = snap(server, "reader-a")
        server.state.mode = "instructions"
        changed = snap(server, "reader-b")
        show("4. instructions-only change", normal, changed)
        assert normal["tools"] == changed["tools"]
        assert normal["four_field"] == changed["four_field"]
        assert normal["full"] != changed["full"], "full digest must catch it"

        print("\nPoC PASS: same-scope fork and instructions-only drift are visible"
              " to a full digest; legitimate scope differences are preserved.")
        print("This is a controlled fixture, not a vulnerability claim about a"
              " specific MCP server.")
        return 0
    finally:
        server.stop()


if __name__ == "__main__":
    raise SystemExit(main())
