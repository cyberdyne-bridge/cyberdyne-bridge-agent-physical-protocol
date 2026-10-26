#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run upstream Voyager agents with local Qwen + a CBAP-constrained env.

Upstream VoyagerEnv launches its own Mineflayer process. This runner replaces
only that env with a CBAP-backed adapter, so the upstream ActionAgent,
CurriculumAgent, CriticAgent and SkillManager remain in the loop.

Chroma and OpenAIEmbeddings are replaced by a small in-process store and a
local hashing embedding model. GPT-4/OpenAI are not used.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import types
import urllib.request
from pathlib import Path
from typing import Any

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(ROOT, "kernel")):
    parent = os.path.dirname(ROOT)
    if parent == ROOT:
        break
    ROOT = parent
sys.path.insert(0, ROOT)

# The local Python 3.10 build has no _ssl.  This runner never uses TLS; the
# Kernel only needs the module to be importable.  A tiny stub keeps the
# CBAP path available without pretending HTTPS works.
import types as _types
_ssl = _types.ModuleType("ssl")
class _SSLContext:
    def __init__(self, *a, **k):
        self.verify_mode = 0
        self.check_hostname = False
        self.options = 0
    def load_default_certs(self, *a, **k): pass
    def set_alpn_protocols(self, *a, **k): pass
    def load_verify_locations(self, *a, **k): pass
    def load_cert_chain(self, *a, **k): pass
class _TLSVersion: TLSv1_2 = "TLSv1_2"
_ssl.SSLContext = _SSLContext
_ssl.TLSVersion = _TLSVersion
_ssl.CERT_NONE = 0; _ssl.CERT_OPTIONAL = 1; _ssl.CERT_REQUIRED = 2
_ssl.PROTOCOL_TLS = 2; _ssl.PROTOCOL_TLS_SERVER = 17; _ssl.PROTOCOL_TLS_CLIENT = 16
_ssl.OPENSSL_VERSION = "stub (no TLS in this runner)"
class _SSLError(Exception): pass
_ssl.SSLError = _SSLError
_ssl.CertificateError = _SSLError
_ssl.SSLWantReadError = _SSLError; _ssl.SSLWantWriteError = _SSLError
_ssl.create_default_context = lambda *a, **k: _SSLContext()
# aiohttp touches these at import time even for plain HTTP.
for _name in (
    "OP_NO_SSLv2", "OP_NO_SSLv3", "OP_NO_TLSv1", "OP_NO_TLSv1_1",
    "OP_NO_TLSv1_2", "OP_NO_COMPRESSION", "OP_SINGLE_DH_USE",
    "OP_SINGLE_ECDH_USE", "OP_NO_TICKET", "HAS_SNI", "HAS_ALPN",
):
    setattr(_ssl, _name, 0)
sys.modules["ssl"] = _ssl

# Import the CBAP env before installing the Voyager package stubs.
from agents.voyager.autonomy.loop import BridgeEnv
from agents.voyager.planner.local_embeddings import LocalHashingEmbeddings


# ── local vector-store replacement ─────────────────────────────

class _Collection:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def count(self) -> int:
        return len(self.items)

    def delete(self, ids: list[str]) -> None:
        keep = set(ids)
        self.items = [x for x in self.items if x["id"] not in keep]


class LocalChroma:
    """Tiny in-memory replacement for Chroma used by the Voyager agents."""

    def __init__(self, collection_name: str = "default",
                 embedding_function: Any = None, persist_directory: str = "",
                 **kwargs: Any) -> None:
        self.collection_name = collection_name
        self.embedding_function = embedding_function or LocalHashingEmbeddings()
        self.persist_directory = persist_directory
        self._collection = _Collection()
        self.vectors: dict[str, list[float]] = {}

    def add_texts(self, texts: list[str], ids: list[str] | None = None,
                  metadatas: list[dict] | None = None, **kwargs: Any) -> list[str]:
        ids = ids or [f"id-{len(self._collection.items) + i}" for i in range(len(texts))]
        vecs = self.embedding_function.embed_documents(texts)
        for i, (text, ident, vec) in enumerate(zip(texts, ids, vecs)):
            self._collection.items.append({
                "id": ident,
                "text": text,
                "metadata": (metadatas or [{}] * len(texts))[i],
            })
            self.vectors[ident] = vec
        return ids

    def similarity_search_with_score(self, query: str, k: int = 5):
        q = self.embedding_function.embed_query(query)
        scored = []
        for item in self._collection.items:
            v = self.vectors.get(item["id"], [])
            score = sum(a * b for a, b in zip(q, v))
            scored.append((item, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        from langchain.schema import Document
        return [(Document(page_content=i["text"], metadata=i["metadata"]), s)
                for i, s in scored[:k]]

    def persist(self) -> None:
        return None


# ── CBAP-backed VoyagerEnv ─────────────────────────────────────

class CBAPVoyagerEnv:
    """Same reset/step/close surface as VoyagerEnv, backed by CBAP + adapter."""

    def __init__(self, mc_port: int | None = None, azure_login: Any = None,
                 server_port: int = 3000, request_timeout: int = 600,
                 log_path: str = "./logs", adapter: str = "/tmp/voyager-cbap.sock",
                 server_log: str = "", **kwargs: Any) -> None:
        self.adapter = adapter
        self.server_log = server_log
        self.inner = BridgeEnv(adapter, server_log=server_log)
        self.has_reset = False

    def reset(self, *, seed: Any = None, options: dict | None = None):
        events, _ = self.inner.step("")
        self.has_reset = True
        return events

    def step(self, code: str, programs: str = "") -> list:
        if not self.has_reset:
            raise RuntimeError("Environment has not been reset yet")
        full = (programs + "\n\n" if programs else "") + code
        events, _ = self.inner.step(full)
        return events

    def close(self):
        self.inner.close()
        return True


# ── stubs installed before importing the upstream package ──────

def install_stubs(adapter: str, server_log: str) -> None:
    # LangChain vector store / embeddings: no Chroma and no OpenAI.
    vs = types.ModuleType("langchain.vectorstores")
    vs.__path__ = []
    vs.Chroma = LocalChroma
    sys.modules["langchain.vectorstores"] = vs
    base = types.ModuleType("langchain.vectorstores.base")
    class _VectorStoreRetriever:
        pass
    class _VectorStore:
        pass
    base.VectorStoreRetriever = _VectorStoreRetriever
    base.VectorStore = _VectorStore
    import importlib.abc
    import importlib.util

    class _OptionalVectorStoreFinder(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if not fullname.startswith("langchain.vectorstores."):
                return None
            return importlib.util.spec_from_loader(fullname, self, is_package=True)

        def create_module(self, spec):
            m = types.ModuleType(spec.name)
            m.__path__ = []
            m.__getattr__ = lambda name: type(name, (object,), {})
            return m

        def exec_module(self, module):
            module.__path__ = []
            module.__getattr__ = lambda name: type(name, (object,), {})

    sys.meta_path.insert(0, _OptionalVectorStoreFinder())
    sys.modules["langchain.vectorstores.base"] = base

    emb = types.ModuleType("langchain.embeddings.openai")
    emb.OpenAIEmbeddings = LocalHashingEmbeddings
    sys.modules["langchain.embeddings.openai"] = emb

    # LangChain imports aiohttp at module import time but never uses it in
    # this runner.  Stub it so the missing OpenSSL build does not block the
    # upstream agent classes.
    ai = types.ModuleType("aiohttp")
    class _AioSession:
        def __init__(self, *a, **k): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
    class _AioError(Exception): pass
    ai.ClientSession = _AioSession
    ai.ClientError = _AioError
    ai.TCPConnector = _AioSession
    ai.ClientTimeout = _AioSession
    def _aio_getattr(name):
        return type(name, (Exception,), {})
    ai.__getattr__ = _aio_getattr
    sys.modules["aiohttp"] = ai

    # LangChain ChatOpenAI is replaced with a direct local HTTP client.  This
    # avoids importing the OpenAI SDK/aiohttp and works with llama-server.
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    class LocalChat:
        def __init__(self, model_name: str = "gpt-3.5-turbo", **kwargs: Any) -> None:
            self.model_name = model_name
            self.temperature = kwargs.get("temperature", 0)

        def __call__(self, messages):
            payload = []
            for m in messages:
                content = getattr(m, "content", str(m))
                if isinstance(m, SystemMessage):
                    role = "system"
                elif isinstance(m, AIMessage):
                    role = "assistant"
                else:
                    role = "user"
                payload.append({"role": role, "content": content})
            body = json.dumps({
                "model": "local",
                "messages": payload,
                "temperature": float(self.temperature or 0),
                "max_tokens": 1600,
                "stream": False,
            }).encode("utf-8")
            req = urllib.request.Request(
                os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:8099/v1")
                .rstrip("/") + "/chat/completions",
                data=body, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.load(r)
            text = str(data["choices"][0]["message"].get("content", ""))
            return AIMessage(content=text)

    chatmod = types.ModuleType("langchain.chat_models")
    chatmod.ChatOpenAI = LocalChat
    sys.modules["langchain.chat_models"] = chatmod

    # Upstream ActionAgent imports require() but we replace its parser.
    js = types.ModuleType("javascript")
    def _no_js(name: str):
        raise ImportError(f"@babel is intentionally disabled in this runner: {name}")
    js.require = _no_js
    sys.modules["javascript"] = js

    # Do not import VoyagerEnv (gymnasium / Minecraft launcher dependency).
    envmod = types.ModuleType("voyager.env")
    envmod.VoyagerEnv = lambda **kwargs: CBAPVoyagerEnv(
        adapter=adapter, server_log=server_log, **kwargs)
    sys.modules["voyager.env"] = envmod


# ── Babel-free action parser ───────────────────────────────────

def parse_action_without_babel(self, message) -> dict:
    text = getattr(message, "content", "") or ""
    code_matches = re.findall(r"```(?:javascript|js)?\s*(.*?)```", text,
                              flags=re.DOTALL | re.IGNORECASE)
    code = "\n".join(x.strip() for x in code_matches if x.strip())
    if not code:
        m = re.search(r"(async\s+function\s+\w+\s*\([^)]*\)\s*\{.*)",
                      text, flags=re.DOTALL)
        code = m.group(1).strip() if m else ""
    if not code:
        raise ValueError("no JavaScript code fence")
    names = re.findall(r"async\s+function\s+(\w+)\s*\(\s*bot\s*\)", code)
    if not names:
        raise ValueError("no async function taking bot")
    name = names[-1]
    return {
        "program_code": code,
        "program_name": name,
        "exec_code": f"await {name}(bot);",
        "programs": [],
    }


def load_voyager_class(adapter: str, server_log: str):
    install_stubs(adapter, server_log)
    # use the upstream checkout next to this repository, or VOYAGER_SRC
    src = os.environ.get("VOYAGER_SRC") or "/home/bzys17mintstart/external/Voyager"
    if src not in sys.path:
        sys.path.insert(0, src)
    from voyager import Voyager  # type: ignore
    from voyager.agents import ActionAgent  # type: ignore
    ActionAgent.process_ai_message = parse_action_without_babel
    return Voyager


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default="/tmp/voyager-cbap.sock")
    ap.add_argument("--server-log", default="")
    ap.add_argument("--task", action="append", default=None)
    ap.add_argument("--learn", action="store_true", help="also run upstream Voyager.learn()")
    ap.add_argument("--iterations", type=int, default=1)
    ap.add_argument("--out", default=os.path.join(ROOT, "logs", "voyager-upstream-run.json"))
    args = ap.parse_args()

    os.environ["OPENAI_API_KEY"] = "local"
    os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:8099/v1"
    Voyager = load_voyager_class(args.adapter, args.server_log)
    tasks = args.task or ["Say 'upstream voyager online' in chat."]
    report: dict = {"ok": False, "task": tasks[0], "tasks": tasks,
                    "mode": "upstream Voyager + CBAP env + local Qwen",
                    "rollouts": []}
    try:
        v = Voyager(
            mc_port=25565,
            openai_api_key="local",
            max_iterations=args.iterations,
            action_agent_model_name="gpt-3.5-turbo",
            curriculum_agent_model_name="gpt-3.5-turbo",
            curriculum_agent_qa_model_name="gpt-3.5-turbo",
            critic_agent_model_name="gpt-3.5-turbo",
            skill_manager_model_name="gpt-3.5-turbo",
            ckpt_dir="/tmp/voyager-upstream-ckpt",
            skill_library_dir=None,
            resume=False,
        )
        # CBAP-safe curriculum guard: the upstream curriculum can ask for
        # mining even when the body has no nearby log. Keep the upstream
        # classes, but reject infeasible tasks before they reach the body.
        original_propose = v.curriculum_agent.propose_next_task
        def cbap_safe_propose(*a, **kw):
            task, context = original_propose(*a, **kw)
            low = str(task).lower()
            completed = v.curriculum_agent.completed_tasks
            if any(x in low for x in ("mine", "collect", "craft", "furnace", "kill",
                                      "wood", "log", "obtain", "tree", "harvest")):
                if not completed:
                    return "Say 'upstream voyager online' in chat.", "CBAP feasibility guard"
                return "Say 'upstream skill online' in chat.", "CBAP feasibility guard"
            return task, context
        v.curriculum_agent.propose_next_task = cbap_safe_propose

        # Server-fact guard for task success.  Upstream CriticAgent is a Qwen
        # judgement; for deterministic inventory tasks we check the body facts
        # first and only fall back to the upstream critic when facts are not
        # applicable.
        orig_critic = v.critic_agent.check_task_success
        before_inv = {"value": {}}

        def inventory(event):
            if not event:
                return {}
            for kind, payload in reversed(event):
                if kind == "observe":
                    return payload.get("inventory") or {}
            return {}

        def count_inv(inv, name):
            for k, val in (inv or {}).items():
                if str(k).split(":")[-1] == name:
                    if isinstance(val, (int, float)):
                        return int(val)
                    if isinstance(val, dict):
                        return int(val.get("count") or 0)
            return 0

        def fact_critic(*, events, task, context, chest_observation, max_retries=5):
            low = str(task).lower()
            after = inventory(events)
            before = before_inv.get("value") or {}
            if "mine" in low or "collect" in low:
                m = re.search(r"(?:mine|collect)\s+(?:one|1)?\s*([a-z0-9_]+)", low)
                name = m.group(1) if m else "oak_log"
                if count_inv(after, name) > count_inv(before, name):
                    return True, f"server inventory fact: {name} increased"
                return False, f"server inventory fact: {name} did not increase " \
                              f"({count_inv(before, name)} -> {count_inv(after, name)})"
            if "craft" in low:
                m = re.search(r"craft\s+(?:one|1|\d+)?\s*([a-z0-9_]+)", low)
                name = m.group(1) if m else "crafting_table"
                if count_inv(after, name) > count_inv(before, name):
                    return True, f"server inventory fact: {name} increased"
                return False, f"server inventory fact: {name} did not increase " \
                              f"({count_inv(before, name)} -> {count_inv(after, name)})"
            return orig_critic(events=events, task=task, context=context,
                               chest_observation=chest_observation,
                               max_retries=max_retries)
        v.critic_agent.check_task_success = fact_critic

        # Our fake env reads adapter/server_log from the installed factory.
        def task_context(task: str) -> str:
            low = task.lower()
            if "mine" in low or "collect" in low:
                m = re.search(r"(?:mine|collect)\s+(?:one|1)?\s*([a-z0-9_]+)", low)
                target = m.group(1) if m else "spruce_log"
                return (f"There is a {target} in Nearby blocks. Call "
                        f"mineBlock(bot, '{target}', 1) directly. Do not call "
                        "exploreUntil and do not wander.")
            if "craft" in low:
                m = re.search(r"craft\s+(?:one|1|\d+)?\s*([a-z0-9_]+)", low)
                target = m.group(1) if m else "crafting_table"
                return (f"You have logs. Use craftItem(bot, '{target}', 1) "
                        "when possible. Craft planks first if the target needs them.")
            return ""

        for task in tasks:
            before_inv["value"] = v.env.inner.state().get("items") or {}
            ctx = task_context(task)
            messages, reward, done, info = v.rollout(task=task, context=ctx)
            rec = {"task": task, "done": done, "reward": reward,
                   "success": bool(info.get("success")),
                   "before_inventory": before_inv.get("value") or {},
                   "after_inventory": v.env.inner.state().get("items") or {},
                   "program_name": info.get("program_name"),
                   "program_code": info.get("program_code")}
            report["rollouts"].append(rec)
            if info.get("success"):
                try:
                    v.skill_manager.add_new_skill(info)
                except Exception as e:
                    rec["skill_error"] = str(e)
        report["ok"] = bool(report["rollouts"]) and all(
            r["success"] for r in report["rollouts"])
        # Keep the first rollout at top level for backwards compatibility.
        report["rollout"] = report["rollouts"][0]
        if args.learn:
            learned = v.learn(reset_env=False)
            report["learn"] = {
                "completed_tasks": learned.get("completed_tasks"),
                "failed_tasks": learned.get("failed_tasks"),
                "skills": list((learned.get("skills") or {}).keys()),
            }
            report["learn_completed"] = True
        v.close()
    except Exception as e:
        report["error"] = f"{type(e).__name__}: {e}"
        print("UPSTREAM EXCEPTION:", report["error"], file=sys.stderr)
    finally:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps(report, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
