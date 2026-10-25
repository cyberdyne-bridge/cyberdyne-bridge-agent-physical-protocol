#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEP #3452: authenticated HTTP MCP scope-integrity tests.

The controlled fixture is deliberately small.  These tests do not claim that a
real MCP implementation is vulnerable; they pin down the distinctions the SEP
thread needs:

    same scope, different sessions -> definitions must match
    different scopes               -> per-scope differences are legitimate
    same scope, forked view        -> full-digest comparison detects it
    instructions only              -> four-field digest misses it
"""
from __future__ import annotations

import unittest

from poc.mcp_auth_fixture import (
    MCPHTTPClient, MCPHTTPFixture, digest, four_field_digest, snapshot,
)


class ScopeIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.server = MCPHTTPFixture().start()

    def tearDown(self):
        self.server.stop()

    def _snapshot(self, token: str) -> dict:
        client = MCPHTTPClient(self.server.url, token)
        return snapshot(client)

    def test_same_scope_is_stable_across_sessions(self):
        a = self._snapshot("reader-a")
        b = self._snapshot("reader-b")
        self.assertEqual(
            [t["name"] for t in a["tools"]],
            [t["name"] for t in b["tools"]],
        )
        self.assertEqual(digest(a), digest(b))
        self.assertEqual(a["instructions"], b["instructions"])

    def test_different_scopes_may_legitimately_differ(self):
        read = self._snapshot("reader-a")
        admin = self._snapshot("admin")
        read_tools = {t["name"] for t in read["tools"]}
        admin_tools = {t["name"] for t in admin["tools"]}
        self.assertIn("read_file", read_tools)
        self.assertNotIn("delete_file", read_tools)
        self.assertIn("delete_file", admin_tools)
        # Different authorization scopes are allowed to differ; this must not
        # be reported as a fork by a naive "all clients must match" rule.
        self.assertNotEqual(digest(read), digest(admin))

    def test_same_scope_fork_is_detected_by_full_digest(self):
        self.server.state.mode = "fork_same_scope"
        a = self._snapshot("reader-a")
        b = self._snapshot("reader-b")
        self.assertEqual({t["name"] for t in a["tools"]},
                         {"read_file", "list_dir"})
        self.assertIn("exfiltrate", {t["name"] for t in b["tools"]})
        self.assertNotEqual(digest(a), digest(b))

    def test_instructions_only_change_is_missed_by_four_field_digest(self):
        # First read: benign. Then flip only the instructions, not the tools.
        self.server.state.mode = "normal"
        a = self._snapshot("reader-a")
        self.server.state.mode = "instructions"
        b = self._snapshot("reader-b")
        self.assertEqual(a["tools"], b["tools"])
        self.assertNotEqual(a["instructions"], b["instructions"])
        self.assertEqual(four_field_digest(a["tools"]),
                         four_field_digest(b["tools"]))
        self.assertNotEqual(digest(a), digest(b))

    def test_missing_bearer_token_is_rejected(self):
        client = MCPHTTPClient(self.server.url, None)
        with self.assertRaises(RuntimeError) as cm:
            client.initialize()
        self.assertIn("HTTP 401", str(cm.exception))

    def test_unknown_token_is_rejected(self):
        client = MCPHTTPClient(self.server.url, "not-a-real-token")
        with self.assertRaises(RuntimeError) as cm:
            client.initialize()
        self.assertIn("HTTP 401", str(cm.exception))

    def test_reader_session_cannot_swap_to_admin_token(self):
        client = MCPHTTPClient(self.server.url, "reader-a")
        client.initialize()
        client.token = "admin"
        with self.assertRaises(RuntimeError) as cm:
            client.tools()
        self.assertIn("HTTP 403", str(cm.exception))

    def test_admin_session_cannot_be_replayed_with_reader_token(self):
        client = MCPHTTPClient(self.server.url, "admin")
        client.initialize()
        client.token = "reader-b"
        with self.assertRaises(RuntimeError) as cm:
            client.tools()
        self.assertIn("HTTP 403", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
