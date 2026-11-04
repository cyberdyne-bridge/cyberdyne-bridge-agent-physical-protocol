#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Order-stability checks for tools/list.

The definition digest normalizes tool order, so it cannot see a server that
rotates its list.  This module keeps the two properties separate:

    definition digest  -> is the set/content stable?
    order stability    -> is the wire order stable across calls?
"""
from __future__ import annotations

import itertools
import unittest

from drivers.mcp_device.definition import order_stability, tool_order

NAMES = ["alpha", "bravo", "charlie", "delta"]


class ToolOrderTest(unittest.TestCase):
    def test_tool_order_preserves_wire_order(self):
        tools = [{"name": "b"}, {"name": "a"}, {"name": "c"}]
        self.assertEqual(tool_order(tools), ("b", "a", "c"))

    def test_tool_order_skips_non_dicts(self):
        tools = [{"name": "a"}, "junk", {"name": "b"}]
        self.assertEqual(tool_order(tools), ("a", "b"))


class OrderStabilityTest(unittest.TestCase):
    def test_all_24_permutations_are_stable_when_repeated(self):
        # Any fixed order is allowed; only changes across calls are a warning.
        for perm in itertools.permutations(NAMES):
            result = order_stability([perm, perm, perm])
            self.assertEqual(result["status"], "pass", perm)
            self.assertTrue(result["stable"])
            self.assertEqual(len(result["distinct"]), 1)

    def test_rotation_is_warning(self):
        rotations = [tuple(NAMES[i:] + NAMES[:i]) for i in range(4)]
        result = order_stability(rotations)
        self.assertEqual(result["status"], "warning")
        self.assertFalse(result["stable"])
        self.assertEqual(len(result["distinct"]), 4)

    def test_content_change_with_same_order_is_not_an_order_warning(self):
        before = [{"name": "a", "description": "old"},
                  {"name": "b", "description": "old"}]
        after = [{"name": "a", "description": "new"},
                 {"name": "b", "description": "new"}]
        result = order_stability([tool_order(before), tool_order(after)])
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["stable"])

    def test_tool_set_change_is_info_not_warning(self):
        result = order_stability([("a", "b"), ("a", "b", "c")])
        self.assertEqual(result["status"], "info")
        self.assertIsNone(result["stable"])

    def test_one_tool_is_info(self):
        result = order_stability([("only",), ("only",), ("only",)])
        self.assertEqual(result["status"], "info")
        self.assertTrue(result["stable"])

    def test_one_probe_is_info(self):
        result = order_stability([("a", "b")])
        self.assertEqual(result["status"], "info")
        self.assertIsNone(result["stable"])

    def test_empty_is_info(self):
        result = order_stability([])
        self.assertEqual(result["status"], "info")
        self.assertIsNone(result["stable"])


if __name__ == "__main__":
    unittest.main()
