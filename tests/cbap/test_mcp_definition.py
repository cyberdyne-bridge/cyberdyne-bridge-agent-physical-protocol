#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CBAP MCP definition-digest profile tests."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from drivers.mcp_device.definition import (
    definition_digest, definition_payload, definition_sha256,
)
from drivers.mcp_device.driver import MCPDeviceDriver

ROOT = Path(__file__).resolve().parents[2]
FAKE = ROOT / "tests/cbap/fake_mcp_hardware.py"


class DefinitionProfileTest(unittest.TestCase):
    def _snapshot(self, **overrides):
        snap = {
            "serverInfo": {"name": "fixture", "version": "1.0.0",
                           "title": "Fixture",
                           "instructions": "helpful"},
            "tools": [
                {"name": "b", "title": "B", "description": "B tool",
                 "inputSchema": {"type": "object"}},
                {"name": "a", "title": "A", "description": "A tool",
                 "inputSchema": {"type": "object"},
                 "outputSchema": {"type": "object"}},
            ],
        }
        snap.update(overrides)
        return snap

    def test_profile_covers_title_and_output_schema(self):
        a = self._snapshot()
        b = json.loads(json.dumps(a))
        b["tools"][0]["title"] = "changed"
        self.assertNotEqual(definition_sha256(a["serverInfo"], a["tools"]),
                            definition_sha256(b["serverInfo"], b["tools"]))
        c = json.loads(json.dumps(a))
        c["tools"][1]["outputSchema"] = {"type": "string"}
        self.assertNotEqual(definition_sha256(a["serverInfo"], a["tools"]),
                            definition_sha256(c["serverInfo"], c["tools"]))

    def test_tool_order_is_normalized(self):
        a = self._snapshot()
        b = self._snapshot(tools=list(reversed(a["tools"])))
        self.assertEqual(definition_sha256(a["serverInfo"], a["tools"]),
                         definition_sha256(b["serverInfo"], b["tools"]))

    def test_server_title_is_not_definition(self):
        a = self._snapshot()
        b = self._snapshot(serverInfo={"name": "fixture", "version": "1.0.0",
                                       "title": "Renamed",
                                       "instructions": "helpful"})
        self.assertEqual(definition_sha256(a["serverInfo"], a["tools"]),
                         definition_sha256(b["serverInfo"], b["tools"]))

    def test_absent_and_empty_instructions_are_equivalent(self):
        a = self._snapshot(serverInfo={"name": "fixture", "version": "1.0.0",
                                       "title": "Fixture", "instructions": ""})
        b = self._snapshot(serverInfo={"name": "fixture", "version": "1.0.0",
                                       "title": "Fixture"})
        self.assertEqual(definition_sha256(a["serverInfo"], a["tools"]),
                         definition_sha256(b["serverInfo"], b["tools"]))

    def test_instructions_change_is_detected(self):
        a = self._snapshot()
        b = self._snapshot(serverInfo={"name": "fixture", "version": "1.0.0",
                                       "title": "Fixture",
                                       "instructions": "different"})
        self.assertNotEqual(definition_sha256(a["serverInfo"], a["tools"]),
                            definition_sha256(b["serverInfo"], b["tools"]))

    def test_digest_format_and_payload(self):
        s = self._snapshot()
        d = definition_digest(s["serverInfo"], s["tools"])
        self.assertRegex(d, r"^sha256:[0-9a-f]{64}$")
        payload = definition_payload(s["serverInfo"], s["tools"])
        self.assertEqual(payload["digestVersion"], "mcp-tool-definition/v1")
        self.assertEqual(payload["server"]["version"], "1.0.0")
        self.assertEqual([t["name"] for t in payload["tools"]], ["a", "b"])


class MCPDefinitionPinTest(unittest.TestCase):
    def _manifest(self, extra=()):
        tmp = Path(tempfile.mkdtemp(prefix="mcp-def-"))
        cmd = [sys.executable, str(FAKE), "--device", "light", *extra]
        manifest = {
            "device_id": "mcp://lab/light-def",
            "transport": {"type": "stdio", "command": cmd, "cwd": str(ROOT)},
            "tools": {"turn_on": {"tool": "turn_on"},
                      "turn_off": {"tool": "turn_off"}},
            "facts": {"source": "tool", "tool": "get_state"},
            "estop": {"tool": "turn_off", "expect": {"on": False}},
            "poll_interval": 0.05,
        }
        path = tmp / "device.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def test_legacy_pin_fails_closed(self):
        path = self._manifest()
        m = json.loads(path.read_text(encoding="utf-8"))
        m["pin_tools"] = {"tools_sha256": "0" * 64}
        path.write_text(json.dumps(m), encoding="utf-8")
        with self.assertRaises(Exception) as cm:
            MCPDeviceDriver(path).connect()
        self.assertIn("legacy", str(cm.exception).lower())

    def test_same_connection_title_drift_is_rejected(self):
        path = self._manifest(["--drift-title"])
        driver = MCPDeviceDriver(path)
        try:
            self.assertTrue(driver.connect())
            self.assertFalse(driver.send({"op": "turn_on"}))
            self.assertIn("changed", (driver._last_error or "").lower())
        finally:
            driver.close()


if __name__ == "__main__":
    unittest.main()
