"""CBAP adapter must not turn a retry of the same in-flight step into E_BUSY."""
from __future__ import annotations

import os
import sys
import time
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from kernel.legacy_runtime.brain_adapter import CBAPHandAdapter  # noqa: E402


class FakeClient:
    def __init__(self):
        self.calls = 0

    def request(self, op, args, deadline_ms=5000):
        self.calls += 1
        return f"r-{self.calls}"

    def lease(self, fd, ttl_ms=30000, timeout=3.0):
        return {"ok": True}


class CBAPAdapterTest(unittest.TestCase):
    def test_identical_inflight_command_is_not_resent(self):
        a = CBAPHandAdapter(cbap_socket="/tmp/unused.sock")
        a.client = FakeClient()
        a.fd = "fd-1"
        a.lease_until = time.monotonic() + 60
        obj = {"cmd": "dig", "p": [1, 2, 3], "允许挖脚下": True}
        self.assertTrue(a.发(obj))
        self.assertTrue(a.发(dict(obj)))
        self.assertEqual(a.client.calls, 1)


if __name__ == "__main__":
    unittest.main()
