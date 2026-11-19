#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sign an MCP device manifest with HMAC-SHA256 and a validity window.

Usage:
  CBAP_MANIFEST_KEY=... python3 tools/sign_mcp_manifest.py manifest.json
  python3 tools/sign_mcp_manifest.py manifest.json --key ... --write

The signature covers the manifest without `signature` and `_manifest_path`.
Signing stamps `issued_at`, `expires_at` (default 15 days) and, when given,
`key_id`; all three are covered by the signature.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from drivers.mcp_device import manifest_sig  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--key", default=os.environ.get("CBAP_MANIFEST_KEY", ""))
    ap.add_argument("--key-id", default=os.environ.get("CBAP_MANIFEST_KEY_ID", ""))
    ap.add_argument("--days", type=int, default=manifest_sig.DEFAULT_DAYS,
                    help=f"validity window in days (default "
                         f"{manifest_sig.DEFAULT_DAYS}, max "
                         f"{manifest_sig.MAX_WINDOW_DAYS})")
    ap.add_argument("--write", action="store_true",
                    help="write signature into the manifest atomically")
    a = ap.parse_args()
    if not a.key:
        print("CBAP_MANIFEST_KEY or --key is required", file=sys.stderr)
        return 2
    p = Path(a.manifest)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("manifest must be a JSON object", file=sys.stderr)
        return 2
    try:
        manifest_sig.stamp(data, key_id=a.key_id or None, days=a.days)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    data["signature"] = manifest_sig.sign_manifest(data, a.key)
    if not a.write:
        print(data["signature"])
        return 0
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, p)
    print(data["signature"])
    print(f"expires_at={data['expires_at']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
