#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manifest signature validity window: expiry, future issue, key id."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from drivers.mcp_device import manifest_sig
from drivers.mcp_device.driver import MCPDeviceDriver

ROOT = Path(__file__).resolve().parents[2]
FAKE = ROOT / "tests/cbap/fake_mcp_hardware.py"
KEY = "test-manifest-key"
KEY_ID = "test-key-1"


def _base_manifest() -> dict:
    return {
        "device_id": "mcp://lab/light-01",
        "display_name": "Fake light",
        "transport": {
            "type": "stdio",
            "command": [sys.executable, str(FAKE), "--device", "light"],
            "cwd": str(ROOT),
        },
        "tools": {
            "turn_on": {"tool": "turn_on"},
            "turn_off": {"tool": "turn_off"},
        },
        "facts": {"source": "tool", "tool": "get_state"},
        "estop": {"tool": "turn_off", "expect": {"on": False}},
        "poll_interval": 0.05,
    }


class ManifestWindowTest(unittest.TestCase):
    def setUp(self):
        self._env = {k: os.environ.get(k) for k in
                     ("CBAP_MANIFEST_KEY", "CBAP_MANIFEST_KEY_ID",
                      "CBAP_REQUIRE_SIGNED_MANIFEST")}
        os.environ["CBAP_MANIFEST_KEY"] = KEY

    def tearDown(self):
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def _write(self, manifest: dict) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="mcp-sig-"))
        path = tmp / "device.json"
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        return path

    def _signed(self, *, days: int = 15, key_id: str | None = KEY_ID,
                now: datetime | None = None) -> dict:
        manifest = _base_manifest()
        manifest_sig.stamp(manifest, key_id=key_id, days=days, now=now)
        manifest["signature"] = manifest_sig.sign_manifest(manifest, KEY)
        return manifest

    def test_valid_window_accepted(self):
        path = self._write(self._signed())
        MCPDeviceDriver(path).close()

    def test_expired_rejected(self):
        old = datetime.now(timezone.utc) - timedelta(days=30)
        path = self._write(self._signed(now=old))
        with self.assertRaises(Exception) as ctx:
            MCPDeviceDriver(path)
        self.assertIn("expired", str(ctx.exception))

    def test_future_issued_rejected(self):
        future = datetime.now(timezone.utc) + timedelta(days=1)
        path = self._write(self._signed(now=future))
        with self.assertRaises(Exception) as ctx:
            MCPDeviceDriver(path)
        self.assertIn("future", str(ctx.exception))

    def test_key_id_mismatch_rejected(self):
        os.environ["CBAP_MANIFEST_KEY_ID"] = "other-key"
        path = self._write(self._signed(key_id=KEY_ID))
        with self.assertRaises(Exception) as ctx:
            MCPDeviceDriver(path)
        self.assertIn("key_id", str(ctx.exception))

    def test_tampered_expiry_rejected(self):
        manifest = self._signed()
        manifest["expires_at"] = manifest_sig.format_ts(
            datetime.now(timezone.utc) + timedelta(days=365))
        path = self._write(manifest)
        with self.assertRaises(Exception) as ctx:
            MCPDeviceDriver(path)
        self.assertIn("signature mismatch", str(ctx.exception))

    def test_legacy_without_expiry(self):
        manifest = _base_manifest()
        manifest["signature"] = manifest_sig.sign_manifest(manifest, KEY)
        path = self._write(manifest)
        MCPDeviceDriver(path).close()          # legacy allowed by default
        os.environ["CBAP_REQUIRE_SIGNED_MANIFEST"] = "1"
        with self.assertRaises(Exception) as ctx:
            MCPDeviceDriver(path)
        self.assertIn("expires_at", str(ctx.exception))

    def test_window_capped(self):
        with self.assertRaises(ValueError):
            manifest_sig.stamp(_base_manifest(), days=365)


if __name__ == "__main__":
    unittest.main()
