#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small dependency-free secret scanner for tracked source files.

This is intentionally narrower than a full entropy scanner: it catches the
high-signal credential shapes we actually use, without flagging test fixtures
or documentation prose.  Runtime data, logs, node_modules and .git are out of
scope.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "node_modules", "runtime", "logs", "__pycache__"}
PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{32,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
]


def tracked_files() -> list[Path]:
    # CI always has git.  Let a missing git fail loudly instead of silently
    # falling back to a partial scan.
    raw = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT, stderr=subprocess.DEVNULL
    )
    names = raw.decode("utf-8", "replace").split("\0")
    if names:
        return [ROOT / n for n in names if n]
    return [p for p in ROOT.rglob("*") if p.is_file()
            and not (set(p.parts) & SKIP_PARTS)]


def main() -> int:
    findings = []
    for path in tracked_files():
        rel = path.relative_to(ROOT)
        if set(rel.parts) & SKIP_PARTS or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, rx in PATTERNS:
                if rx.search(line):
                    findings.append((str(rel), lineno, name))
    if findings:
        for rel, lineno, name in findings:
            print(f"{rel}:{lineno}: possible {name}", file=sys.stderr)
        print(f"secret scan failed: {len(findings)} finding(s)", file=sys.stderr)
        return 1
    print(f"secret scan passed: {len(tracked_files())} tracked files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
