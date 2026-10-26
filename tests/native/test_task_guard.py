"""Native task-stack guards: air steps and stale coordinates must fail closed."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "agents", "cyberdyne", "brain"))

import bridge  # noqa: E402


class TaskGuardTest(unittest.TestCase):
    def _stack(self):
        return bridge.任务栈(
            {"task_enable": True},
            lambda *a, **k: None,
            lambda obj: None,
            tempfile.mkdtemp(prefix="task-guard-"),
        )

    def test_air_step_is_skipped_at_accept(self):
        t = self._stack()
        state = {
            "pos": [844.2, 64, -2.0],
            "scan": {"t": 1, "可交互": [], "方块": []},
            "blocks": [
                {"p": [844, 61, -2], "name": "air"},
                {"p": [844, 63, -2], "name": "stone"},
            ],
            "items": {"wooden_pickaxe": 1},
        }
        steps = [
            {"动作": "挖", "p": [844, 61, -2]},
            {"动作": "挖", "p": [844, 63, -2], "允许挖脚下": True},
        ]
        self.assertTrue(t.接("guard", steps, state))
        self.assertTrue(steps[0].get("跳过"))
        self.assertIsNone(steps[1].get("跳过"))

    def test_stale_step_fails_task_and_does_not_retry(self):
        t = self._stack()
        state = {
            "pos": [844.2, 64, -2.0],
            "scan": {"t": 1, "可交互": [], "方块": []},
            "blocks": [{"p": [844, 63, -2], "name": "stone"}],
            "items": {"wooden_pickaxe": 1},
        }
        steps = [{"动作": "挖", "p": [844, 63, -2], "允许挖脚下": True}]
        self.assertTrue(t.接("guard", steps, state))
        steps[0]["_陈坐标"] = True
        self.assertFalse(t.跑(state))
        self.assertEqual(t.任务.get("状态"), "败")
        self.assertEqual(t.任务.get("failure_code"), "stale_coordinate")

    def test_task_without_any_dig_cannot_complete(self):
        t = self._stack()
        state = {
            "pos": [844.2, 64, -2.0],
            "scan": {"t": 1, "可交互": [], "方块": []},
            "blocks": [{"p": [844, 63, -2], "name": "air"}],
            "items": {},
        }
        self.assertTrue(t.接("demo", [{"动作": "挖", "p": [844, 63, -2]}], state))
        self.assertFalse(t.跑(state))
        self.assertEqual(t.任务.get("状态"), "败")
        self.assertEqual(t.任务.get("failure_code"), "no_dig")

    def test_stale_failure_invokes_replanner_once(self):
        t = self._stack()
        state = {
            "pos": [844.2, 64, -2.0],
            "scan": {"t": 1, "可交互": [], "方块": []},
            "blocks": [{"p": [844, 63, -2], "name": "stone"}],
            "items": {"wooden_pickaxe": 1},
        }
        steps = [{"动作": "挖", "p": [844, 63, -2], "允许挖脚下": True}]
        self.assertTrue(t.接("guard", steps, state))
        calls = []
        t.重规划 = lambda stack, s: calls.append((stack, s))
        steps[0]["_陈坐标"] = True
        self.assertFalse(t.跑(state))
        self.assertEqual(len(calls), 1)
        self.assertEqual(t.任务.get("重规划次数"), 1)


if __name__ == "__main__":
    unittest.main()
