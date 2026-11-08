#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Body Self-Check：三个探针的判定与 fail-closed 行为。

规范：spec/body-selfcheck.md
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import body_selfcheck as bsc  # noqa: E402


class _NoRss(bsc.FakeBody):
    def snapshot(self):
        snap = super().snapshot()
        snap.pop("rss_kb", None)
        return snap


class _NoFrame(bsc.FakeBody):
    def snapshot(self):
        snap = super().snapshot()
        snap.pop("frame_hash", None)
        return snap


class _Boom(bsc.FakeBody):
    def snapshot(self):
        raise RuntimeError("body gone")


class ProbeTest(unittest.TestCase):
    def test_healthy_body_passes_all(self):
        report = bsc.run(bsc.FakeBody(), rounds=3)
        self.assertTrue(report["ok"], report)
        self.assertEqual([c["id"] for c in report["checks"]],
                         ["input.liveness", "resource.growth", "render.variance"])

    def test_input_probe_fails_when_action_leaves_no_trace(self):
        check = bsc.probe_input(bsc.BrokenBody("input"))
        self.assertFalse(check.ok)
        self.assertFalse(check.detail["echoed"])
        self.assertIn("probe-", check.detail["token"])

    def test_growth_probe_fails_on_leak(self):
        check = bsc.probe_growth(bsc.BrokenBody("leak"), rounds=5, limit_kb=2048)
        self.assertFalse(check.ok)
        self.assertGreater(check.detail["rss_growth_kb"], 2048)

    def test_growth_probe_passes_on_stable_body(self):
        check = bsc.probe_growth(bsc.FakeBody(), rounds=5, limit_kb=2048)
        self.assertTrue(check.ok)
        self.assertLessEqual(check.detail["rss_growth_kb"], 2048)

    def test_render_probe_fails_on_blank_output(self):
        check = bsc.probe_render(bsc.BrokenBody("blank"))
        self.assertFalse(check.ok)
        self.assertEqual(check.detail["distinct"], 1)

    def test_render_probe_passes_on_distinct_states(self):
        check = bsc.probe_render(bsc.FakeBody())
        self.assertTrue(check.ok)
        self.assertGreaterEqual(check.detail["distinct"], 2)


class FailClosedTest(unittest.TestCase):
    def test_missing_rss_is_a_failure_not_a_skip(self):
        check = bsc.probe_growth(_NoRss(), rounds=3, limit_kb=2048)
        self.assertFalse(check.ok)
        self.assertIn("rss_kb", check.detail["error"])

    def test_missing_frame_hash_is_a_failure(self):
        check = bsc.probe_render(_NoFrame())
        self.assertFalse(check.ok)
        self.assertIn("frame_hash", check.detail["error"])

    def test_exception_is_a_failure_with_reason(self):
        check = bsc.probe_input(_Boom())
        self.assertFalse(check.ok)
        self.assertIn("RuntimeError", check.detail["error"])

    def test_degraded_body_is_not_ok(self):
        report = bsc.run(bsc.BrokenBody("degraded"), rounds=3)
        self.assertTrue(report["degraded"])
        self.assertFalse(report["ok"])
        self.assertIn("renderer", report["degraded_reason"])


class ReportTest(unittest.TestCase):
    def test_report_is_json_serialisable_and_versioned(self):
        report = bsc.run(bsc.FakeBody(), rounds=3)
        self.assertEqual(report["spec"], bsc.SPEC)
        self.assertIn("generated_at", report)
        json.dumps(report, ensure_ascii=False)

    def test_broken_input_is_not_ok(self):
        report = bsc.run(bsc.BrokenBody("input"), rounds=3)
        self.assertFalse(report["ok"])
        failed = [c["id"] for c in report["checks"] if not c["ok"]]
        self.assertIn("input.liveness", failed)


if __name__ == "__main__":
    unittest.main()
