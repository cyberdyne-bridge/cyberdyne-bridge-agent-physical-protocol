#!/usr/bin/env python3
"""CBAP adapter contract regression: incomplete onChat event breaks recorder.

This is NOT an upstream Voyager reproduction: upstream bot.event() attaches
all non-on observations to onChat. It reproduces the shape our adapter used to
emit and guards that we keep attaching the full snapshot.
"""
import os
import sys
import tempfile
import types

src = os.environ.get("VOYAGER_SRC", "/tmp/voyager-audit")
root = os.path.join(src, "voyager")
pkg = types.ModuleType("voyager")
pkg.__path__ = [root]
sys.modules["voyager"] = pkg
utils = types.ModuleType("voyager.utils")
utils.__path__ = [os.path.join(root, "utils")]
sys.modules["voyager.utils"] = utils

from voyager.utils.record_utils import EventRecorder  # noqa: E402

rec = EventRecorder(ckpt_dir=tempfile.mkdtemp(prefix="voyager-rec-"))
events = [
    ["onChat", {"onChat": "hello"}],
    ["observe", {
        "status": {"elapsedTime": 1, "position": {"x": 0, "z": 0},
                   "biome": "plains"},
        "inventory": {},
        "blockRecords": [],
    }],
]
try:
    rec.record(events, "say hello")
except KeyError as e:
    print(f"REPRODUCED (CBAP adapter contract): KeyError {e} (onChat lacks status/inventory)")
    raise SystemExit(0)
print("NOT REPRODUCED")
raise SystemExit(1)
