#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JCS / definition digest profile tests for the #3452 fixture."""
from __future__ import annotations

import json
import re
import unittest

import jcs
from poc.mcp_auth_fixture import digest, four_field_digest


class JCSTest(unittest.TestCase):
    def test_rfc8785_example_vector(self):
        raw = r'''{
          "numbers": [333333333.33333329, 1E30, 4.50,
                      2e-3, 0.000000000000000000000000001],
          "string": "\u20ac$\u000F\u000aA'\u0042\u0022\u005c\\\"\/",
          "literals": [null, true, false]
        }'''
        obj = json.loads(raw)
        expected = (
            '{"literals":[null,true,false],'
            '"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],'
            '"string":"€$\\u000f\\nA\'B\\"\\\\\\\\\\"/"}'
        )
        self.assertEqual(jcs.dumps(obj), expected)

    def test_number_edge_cases(self):
        self.assertEqual(jcs.dumps(0.0), "0")
        self.assertEqual(jcs.dumps(-0.0), "0")
        self.assertEqual(jcs.dumps(1.0), "1")
        self.assertEqual(jcs.dumps(1e-6), "0.000001")
        self.assertEqual(jcs.dumps(1e-7), "1e-7")
        self.assertEqual(jcs.dumps(1e21), "1e+21")
        self.assertEqual(jcs.dumps(4.50), "4.5")
        self.assertEqual(jcs.dumps(2e-3), "0.002")

    def test_jcs_rejects_non_json_numbers(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                jcs.dumps(value)


class DefinitionProfileTest(unittest.TestCase):
    def _snap(self, **overrides):
        snap = {
            "serverInfo": {"name": "fixture", "version": "1.0.0",
                           "title": "Fixture"},
            "instructions": "helpful",
            "tools": [
                {"name": "a", "title": "A", "description": "A tool",
                 "inputSchema": {"type": "object"}, "annotations": {}},
                {"name": "b", "title": "B", "description": "B tool",
                 "inputSchema": {"type": "object"}, "annotations": {}},
            ],
        }
        snap.update(overrides)
        return snap

    def test_digest_format(self):
        d = digest(self._snap())
        self.assertRegex(d, r"^sha256:[0-9a-f]{64}$")

    def test_tool_order_is_normalized(self):
        a = self._snap()
        b = self._snap(tools=list(reversed(a["tools"])))
        self.assertEqual(digest(a), digest(b))

    def test_server_title_is_not_part_of_definition_digest(self):
        a = self._snap()
        b = self._snap(serverInfo={"name": "fixture", "version": "1.0.0",
                                   "title": "Renamed"})
        self.assertEqual(digest(a), digest(b))

    def test_absent_and_empty_instructions_are_equivalent(self):
        a = self._snap(instructions="")
        b = dict(self._snap())
        b.pop("instructions")
        self.assertEqual(digest(a), digest(b))

    def test_tool_title_change_is_detected(self):
        a = self._snap()
        b = self._snap()
        b["tools"] = [dict(t) for t in a["tools"]]
        b["tools"][0]["title"] = "Changed"
        self.assertNotEqual(digest(a), digest(b))

    def test_instructions_change_is_detected_by_full_profile(self):
        a = self._snap()
        b = self._snap(instructions="different")
        self.assertNotEqual(digest(a), digest(b))
        self.assertEqual(four_field_digest(a["tools"]),
                         four_field_digest(b["tools"]))

    def test_server_version_change_is_detected(self):
        a = self._snap()
        b = self._snap(serverInfo={"name": "fixture", "version": "1.0.1",
                                   "title": "Fixture"})
        self.assertNotEqual(digest(a), digest(b))


if __name__ == "__main__":
    unittest.main()
