#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dependency-free local embeddings for Voyager-style skill retrieval.

This is deliberately small and deterministic. It replaces OpenAIEmbeddings
for the local-Qwen profile; it is *not* a semantic embedding model and its
retrieval quality is below a real text embedding model.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable

DIM = 256
_TOKEN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


def _features(text: str) -> Iterable[str]:
    text = (text or "").lower()
    words = _TOKEN.findall(text)
    for w in words:
        yield "w:" + w
    for a, b in zip(words, words[1:]):
        yield "b:" + a + "_" + b
    compact = " ".join(words)
    for i in range(max(0, len(compact) - 2)):
        yield "c:" + compact[i:i + 3]


def embed(text: str) -> list[float]:
    vec = [0.0] * DIM
    for feat in _features(text):
        h = hashlib.sha256(feat.encode("utf-8")).digest()
        idx = int.from_bytes(h[:4], "big") % DIM
        sign = 1.0 if h[4] & 1 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class LocalHashingEmbeddings:
    """Minimal LangChain-shaped embeddings object, without LangChain."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return embed(text)


class SkillMemory:
    def __init__(self) -> None:
        self.entries: list[dict] = []

    def add(self, name: str, description: str, code: str) -> None:
        self.entries.append({
            "name": name,
            "description": description,
            "code": code,
            "vec": embed(description + "\n" + code),
        })

    def retrieve(self, query: str, k: int = 2) -> list[dict]:
        q = embed(query)
        ranked = sorted(self.entries, key=lambda e: cosine(q, e["vec"]),
                        reverse=True)
        return ranked[:max(0, k)]
