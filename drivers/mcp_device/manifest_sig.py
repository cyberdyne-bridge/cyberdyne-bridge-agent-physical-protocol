#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manifest signature profile: HMAC-SHA256 with a validity window.

The signature covers the manifest without ``signature`` and
``_manifest_path``.  Optional fields ``issued_at``, ``expires_at`` and
``key_id`` are part of the signed payload, so they cannot be edited
without invalidating the signature.

Time is UTC, second precision, ``YYYY-MM-DDTHH:MM:SSZ``.  A signature
without a validity window is accepted only when ``require_expiry`` is
false (legacy manifests); production deployments should set
``CBAP_REQUIRE_SIGNED_MANIFEST=1``, which also rejects legacy manifests.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

SIG_VERSION = "mcp-manifest/v2"
DEFAULT_DAYS = 15
MAX_WINDOW_DAYS = 90
CLOCK_SKEW_SECONDS = 300
_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class ManifestSigError(ValueError):
    """A manifest signature failed validation."""


def canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def payload(manifest: dict) -> dict:
    return {k: v for k, v in manifest.items()
            if k not in ("signature", "_manifest_path")}


def sign_manifest(manifest: dict, key: str) -> str:
    body = canonical(payload(manifest)).encode("utf-8")
    return hmac.new(key.encode("utf-8"), body, hashlib.sha256).hexdigest()


def format_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime(_TS_FORMAT)


def parse_ts(value: str) -> datetime:
    try:
        return datetime.strptime(str(value), _TS_FORMAT).replace(
            tzinfo=timezone.utc)
    except (TypeError, ValueError) as exc:
        raise ManifestSigError(
            "E_AUTH", f"invalid manifest timestamp: {value!r}") from exc


def stamp(manifest: dict, key_id: str | None = None,
          days: int = DEFAULT_DAYS, now: datetime | None = None) -> dict:
    """Write issued_at / expires_at / key_id before signing (in place)."""
    if days <= 0 or days > MAX_WINDOW_DAYS:
        raise ValueError(f"days must be in 1..{MAX_WINDOW_DAYS}")
    issued = now or datetime.now(timezone.utc)
    manifest["issued_at"] = format_ts(issued)
    manifest["expires_at"] = format_ts(issued + timedelta(days=days))
    if key_id:
        manifest["key_id"] = key_id
    return manifest


def check(manifest: dict, key: str, *, require_expiry: bool = False,
          expected_key_id: str | None = None,
          now: datetime | None = None,
          max_window_days: int = MAX_WINDOW_DAYS) -> None:
    """Validate HMAC, key id and validity window.  Raise ManifestSigError."""
    sig = manifest.get("signature")
    if not sig:
        raise ManifestSigError("E_AUTH", "manifest is not signed")
    want = sign_manifest(manifest, key)
    if not hmac.compare_digest(str(sig), want):
        raise ManifestSigError("E_AUTH", "manifest signature mismatch")

    if expected_key_id and manifest.get("key_id"):
        if str(manifest["key_id"]) != str(expected_key_id):
            raise ManifestSigError(
                "E_AUTH",
                f"manifest key_id {manifest['key_id']!r} does not match "
                f"expected {expected_key_id!r}")

    expires_raw = manifest.get("expires_at")
    if not expires_raw:
        if require_expiry:
            raise ManifestSigError(
                "E_AUTH", "manifest signature lacks expires_at")
        return

    current = now or datetime.now(timezone.utc)
    expires = parse_ts(expires_raw)
    if current > expires:
        raise ManifestSigError(
            "E_AUTH", f"manifest signature expired at {expires_raw}")

    issued_raw = manifest.get("issued_at")
    if issued_raw:
        issued = parse_ts(issued_raw)
        if current + timedelta(seconds=CLOCK_SKEW_SECONDS) < issued:
            raise ManifestSigError(
                "E_AUTH", f"manifest issued in the future: {issued_raw}")
        if expires <= issued:
            raise ManifestSigError(
                "E_AUTH", "manifest validity window is empty")
        if expires - issued > timedelta(days=max_window_days):
            raise ManifestSigError(
                "E_AUTH",
                f"manifest validity window exceeds {max_window_days} days")
