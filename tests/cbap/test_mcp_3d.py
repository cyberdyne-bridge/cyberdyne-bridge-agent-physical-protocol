#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D execution-authority residual tests for the CBAP MCP device driver.

These tests deliberately distinguish what CBAP enforces from what it cannot
prove.  They are not vulnerability claims about a real MCP server.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from drivers.mcp_device.driver import MCPDeviceDriver

ROOT = Path(__file__).resolve().parents[2]
FAKE = ROOT / "tests/cbap/fake_mcp_hardware.py"


def manifest(extra=()):
    tmp = Path(tempfile.mkdtemp(prefix="mcp-3d-"))
    cmd = [sys.executable, str(FAKE), "--device", "light", *extra]
    data = {
        "device_id": "mcp://lab/light-3d",
        "transport": {"type": "stdio", "command": cmd, "cwd": str(ROOT)},
        "tools": {"turn_on": {"tool": "turn_on"},
                  "turn_off": {"tool": "turn_off"}},
        "facts": {"source": "tool", "tool": "get_state"},
        "estop": {"tool": "turn_off", "expect": {"on": False}},
        "poll_interval": 0.05,
    }
    path = tmp / "device.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


class ExecutionAuthorityResidualTest(unittest.TestCase):
    def test_annotation_is_a_hint_not_an_enforcement(self):
        # The server advertises readOnlyHint but writes state. CBAP does not
        # treat annotations as authorization; this test records that boundary.
        driver = MCPDeviceDriver(manifest(["--annotation-lie"]))
        try:
            self.assertTrue(driver.connect())
            self.assertTrue(driver.send({"op": "turn_on",
                                         "expect": {"on": True}}))
            self.assertEqual(driver.latest_state["on"], True)
        finally:
            driver.close()

    def test_same_definition_behavior_drift_is_caught_by_facts(self):
        # First call behaves; later calls return ok but do not change state.
        # The definition is stable, so only facts can catch this.
        driver = MCPDeviceDriver(manifest(["--liar-after"]))
        try:
            self.assertTrue(driver.connect())
            self.assertTrue(driver.send({"op": "turn_on",
                                         "expect": {"on": True}}))
            self.assertTrue(driver.send({"op": "turn_off",
                                         "expect": {"on": False}}))
            self.assertFalse(driver.send({"op": "turn_on",
                                          "expect": {"on": True}}))
            self.assertEqual(driver.last_verification()["status"], "mismatch")
        finally:
            driver.close()

    def test_behavior_drift_without_expect_is_only_observed(self):
        # Without a declared postcondition, CBAP cannot call a tool receipt
        # "verified". This is the 3D boundary, not a successful security check.
        driver = MCPDeviceDriver(manifest(["--liar-after"]))
        try:
            self.assertTrue(driver.connect())
            self.assertTrue(driver.send({"op": "turn_on",
                                         "expect": {"on": True}}))
            self.assertTrue(driver.send({"op": "turn_off",
                                         "expect": {"on": False}}))
            self.assertTrue(driver.send({"op": "turn_on"}))
            self.assertEqual(driver.last_verification()["status"], "observed")
        finally:
            driver.close()


if __name__ == "__main__":
    unittest.main()
