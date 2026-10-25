#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP tool-definition digest profile used by the CBAP MCP device driver.

This is the same profile as the #3452 fixture:

    serverInfo.name + serverInfo.version
    instructions (absent -> "")
    complete tool objects, sorted by name
    RFC 8785 JCS
    SHA-256, lowercase hex, domain separated
"""
from __future__ import annotations

import hashlib
from typing import Any

import jcs

DIGEST_VERSION = "mcp-tool-definition/v1"
_DOMAIN = b"mcp-tool-definition/v1\x00"


def definition_payload(server_info: dict | None,
                       tools: list[dict] | None) -> dict:
    server = server_info or {}
    normalized = []
    for tool in tools or []:
        if not isinstance(tool, dict):
            continue
        normalized.append(tool)
    normalized.sort(key=lambda t: str(t.get("name") or ""))
    names = [str(t.get("name") or "") for t in normalized]
    if any(not n for n in names):
        raise ValueError("tool definition has an empty name")
    if len(names) != len(set(names)):
        raise ValueError("duplicate tool names in definition")
    return {
        "digestVersion": DIGEST_VERSION,
        "server": {
            "name": str(server.get("name") or ""),
            "version": str(server.get("version") or ""),
        },
        "instructions": str(server.get("instructions") or ""),
        "tools": normalized,
    }


def definition_sha256(server_info: dict | None,
                      tools: list[dict] | None) -> str:
    body = jcs.dumps(definition_payload(server_info, tools)).encode("utf-8")
    return hashlib.sha256(_DOMAIN + body).hexdigest()


def definition_digest(server_info: dict | None,
                      tools: list[dict] | None) -> str:
    return "sha256:" + definition_sha256(server_info, tools)


def instructions_sha256(server_info: dict | None) -> str:
    text = str((server_info or {}).get("instructions") or "")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
