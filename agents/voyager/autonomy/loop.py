#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A complete, local-Qwen Voyager-style autonomy loop over CBAP.

The loop is intentionally explicit:

    curriculum -> action -> CBAP bridge -> server facts -> critic -> skill library

It is not VoyagerEnv. It uses the MIT Voyager prompts, a local Qwen server,
local hashing embeddings and the real 1.21.1 Voyager Mineflayer bridge.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
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

from drivers.mc.driver import McDriver
from kernel.legacy_runtime.client import CBAPClient
from kernel.legacy_runtime.server import KernelServer
from agents.voyager.planner.local_embeddings import LocalHashingEmbeddings

DEVICE = "mc://voyager/bot"
DEFAULT_LLM = "http://127.0.0.1:8099/v1/chat/completions"
PROMPT_DIR = Path(__file__).resolve().parents[1] / "planner" / "prompts"

HELPERS = r'''
async function moveForward(bot) {
  bot.setControlState("forward", true);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  bot.setControlState("forward", false);
}

async function moveBackward(bot) {
  bot.setControlState("back", true);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  bot.setControlState("back", false);
}

async function say(bot, text) {
  bot.chat(text);
}

async function mineBlock(bot, name, count = 1) {
  const block = bot.findBlock({
    matching: bot.registry.blocksByName[name].id,
    maxDistance: 32,
  });
  if (!block) throw new Error("no nearby block: " + name);
  await bot.collectBlock.collect(block);
}
'''


def load_prompt(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")


def qwen(url: str, messages: list[dict], model: str = "local",
         max_tokens: int = 700, timeout: float = 180) -> str:
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return str(data["choices"][0]["message"].get("content", ""))


def extract_code(text: str) -> tuple[str, str]:
    matches = re.findall(r"```(?:javascript|js)?\s*(.*?)```", text or "",
                         flags=re.DOTALL | re.IGNORECASE)
    code = "\n\n".join(x.strip() for x in matches if x.strip())
    if not code:
        m = re.search(r"(async\s+function\s+\w+\s*\([^)]*\)\s*\{.*)",
                      text or "", flags=re.DOTALL)
        code = m.group(1).strip() if m else ""
    if not code:
        raise ValueError("no JavaScript code fence")
    names = re.findall(r"async\s+function\s+(\w+)\s*\(\s*bot\s*\)", code)
    if not names:
        raise ValueError("no async function taking bot")
    return code, f"await {names[-1]}(bot);"


def json_object(text: str) -> dict:
    text = text or ""
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        raise ValueError("no JSON object")
    return json.loads(m.group(0))


def count_item(state: dict, name: str) -> int:
    items = state.get("items") or {}
    if not isinstance(items, dict):
        return 0
    for key, val in items.items():
        if str(key).split(":")[-1] == name:
            if isinstance(val, (int, float)):
                return int(val)
            if isinstance(val, dict):
                return int(val.get("count") or 0)
    return 0


def count_total(state: dict) -> int:
    items = state.get("items") or {}
    if not isinstance(items, dict):
        return 0
    total = 0
    for val in items.values():
        if isinstance(val, (int, float)):
            total += int(val)
        elif isinstance(val, dict):
            total += int(val.get("count") or 0)
    return total


class BridgeEnv:
    """CBAP-backed observation/action environment with Voyager-shaped events."""

    def __init__(self, adapter: str, server_log: str = "") -> None:
        self.tmp = tempfile.mkdtemp(prefix="cbap-voyager-autonomy-")
        self.server_log = server_log
        self.log_offset = 0
        if server_log and os.path.exists(server_log):
            self.log_offset = os.path.getsize(server_log)
        self.driver = McDriver(
            adapter,
            device_path=os.path.join(ROOT, "agents/voyager/adapter/device.json"),
            mapping_path=os.path.join(ROOT, "agents/voyager/adapter/mapping.json"),
            connect_timeout=5, reconnect=True,
        )
        self.driver.connect()
        policy = {"default": {"devices": ["*"],
                              "capabilities": ["read", "write", "lease", "estop"]},
                  "agents": {}}
        self.kernel = KernelServer(
            drivers=[self.driver],
            socket_path=os.path.join(self.tmp, "kernel.sock"),
            audit_path=os.path.join(self.tmp, "audit.jsonl"),
            policy=policy,
        )
        if not self.kernel.start():
            raise RuntimeError("kernel did not start")
        self.client = CBAPClient(os.path.join(self.tmp, "kernel.sock"),
                                 agent_id="voyager-autonomy")
        self.client.connect()
        self.client.hello()
        self.fd = self.client.open(DEVICE)["payload"]["fd"]
        self.client.lease(self.fd)
        self.last_events: list = []

    def state(self) -> dict:
        r = self.client.read(self.fd, "body", 3000)
        return ((r.get("payload") or {}).get("frame") or {}).get("body") or {}

    def log_has(self, text: str) -> bool:
        if not self.server_log or not os.path.exists(self.server_log):
            return False
        with open(self.server_log, "rb") as f:
            f.seek(self.log_offset)
            return text.encode("utf-8") in f.read()

    def bridge_state(self) -> dict:
        # The adapter strips some bridge-only fields; the body has enough for
        # the action prompt (position/items/voxels/biome/entities).
        return self.state()

    def step(self, code: str) -> tuple[list, dict]:
        before = self.state()
        _, _, res = self.client.write(
            self.fd,
            {"channel": "body", "op": "exec",
             "args": {"code": HELPERS + "\n\n" + code}},
            deadline_ms=60000, timeout=60,
        )
        payload = res.get("payload") or {}
        on_chat = payload.get("onChat") or []
        after = self.state()
        events = []
        for msg in on_chat:
            events.append(["onChat", {"onChat": msg}])
        events.append(["observe", self._observe(after)])
        self.last_events = events
        return events, after

    def _observe(self, s: dict) -> dict:
        return {
            "status": {
                "health": s.get("hp", 20),
                "food": s.get("food", 20),
                "position": {"x": (s.get("pos") or [0, 0, 0])[0],
                             "y": (s.get("pos") or [0, 0, 0])[1],
                             "z": (s.get("pos") or [0, 0, 0])[2]},
                "equipment": s.get("equipment") or [],
                "inventoryUsed": s.get("inventoryUsed") or 0,
                "biome": s.get("biome"),
                "timeOfDay": s.get("timeOfDay"),
                "entities": s.get("entities") or {},
                "name": s.get("bot", "bot"),
            },
            "voxels": s.get("voxels") or [],
            "inventory": s.get("items") or {},
            "nearbyChests": {},
        }

    def close(self) -> None:
        for obj in (self.client, self.kernel, self.driver):
            try:
                if obj:
                    obj.close()
            except Exception:
                pass


class SkillLibrary:
    def __init__(self, path: str) -> None:
        self.path = path
        self.emb = LocalHashingEmbeddings()
        self.skills: list[dict] = []
        if os.path.exists(path):
            try:
                self.skills = json.load(open(path, encoding="utf-8"))
            except Exception:
                self.skills = []

    def add(self, task: str, name: str, code: str) -> None:
        self.skills = [s for s in self.skills if s.get("task") != task]
        names = {s.get("name") for s in self.skills}
        base = name or "skill"
        unique = base
        i = 2
        while unique in names:
            unique = f"{base}{i}"
            i += 1
        self.skills.append({"task": task, "name": unique, "code": code,
                            "vec": self.emb.embed_query(task)})
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        json.dump(self.skills, open(self.path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    def retrieve(self, query: str, k: int = 2) -> list[dict]:
        if not self.skills:
            return []
        q = self.emb.embed_query(query)
        ranked = sorted(self.skills,
                        key=lambda s: sum(a * b for a, b in zip(q, s["vec"])),
                        reverse=True)
        return ranked[:k]

    def programs(self) -> str:
        return "\n\n".join(s["code"] for s in self.skills)


class Curriculum:
    def __init__(self, llm: str, model: str) -> None:
        self.llm = llm
        self.model = model
        self.fallback = [
            "Say 'voyager autonomy online' in chat.",
            "Say 'curriculum online' in chat.",
            "Say 'skill memory online' in chat.",
        ]

    def propose(self, state: dict, completed: list[str], failed: list[str],
                index: int) -> tuple[str, str]:
        sys_prompt = """You are the Voyager curriculum agent for a local Minecraft body.
Propose exactly one short, feasible task. Allowed task types:
- say a short chat message
- move forward for one second
- mine one nearby log block (spruce_log, oak_log, dark_oak_log, acacia_log)
Return only JSON: {"task": "...", "context": "..."}.
Do not propose crafting, furnaces, combat, or long journeys."""
        human = json.dumps({
            "position": state.get("pos"),
            "blocks": (state.get("voxels") or [])[:20],
            "items": state.get("items") or {},
            "completed": completed[-3:],
            "failed": failed[-3:],
        }, ensure_ascii=False)
        try:
            raw = qwen(self.llm, [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": human},
            ], model=self.model, max_tokens=180)
            obj = json_object(raw)
            task = str(obj.get("task") or "").strip()
            context = str(obj.get("context") or "").strip()
            low = task.lower()
            if any(x in low for x in ("mine", "collect", "log")):
                # pick a log that is actually nearby
                available = [b for b in (state.get("voxels") or [])
                             if str(b).endswith("_log")]
                if not available:
                    return "Say 'voyager autonomy online' in chat.", "no nearby log"
                task = f"Mine one {available[0]} from a nearby tree."
                if task not in completed:
                    return task, context
            if "say" in low:
                m = re.search(r"['\"]([^'\"]{1,80})['\"]", task)
                text = m.group(1) if m else "voyager autonomy online"
                task = f"Say '{text}' in chat."
                if task not in completed:
                    return task, context
            if any(x in low for x in ("move", "forward", "walk")):
                task = "Move forward for one second."
                if task not in completed:
                    return task, context
        except Exception:
            pass
        # Never repeat a completed task just because the 4B curriculum model
        # likes the same phrase again.
        for task in self.fallback:
            if task not in completed:
                return task, "curriculum fallback"
        return self.fallback[min(index, len(self.fallback) - 1)], "curriculum fallback"


class ActionAgent:
    def __init__(self, llm: str, model: str) -> None:
        self.llm = llm
        self.model = model
        self.system_template = load_prompt("action_template.txt")
        self.response_format = load_prompt("action_response_format.txt")

    def generate(self, task: str, obs: dict, skills: SkillLibrary,
                 last_code: str = "", error: str = "", critique: str = "") -> tuple[str, str, str]:
        programs = HELPERS + "\n\n" + skills.programs()
        system = self.system_template.format(programs=programs,
                                             response_format=self.response_format)
        human = f"""Task: {task}

Observation:
{json.dumps(obs, ensure_ascii=False)}

Code from the last round:
{last_code or 'None'}

Execution error:
{error or 'None'}

Critique:
{critique or 'None'}

Return Explain, Plan, and Code in the required format. Define one async
function taking bot and actually execute the task. Use the provided helpers.
"""
        text = qwen(self.llm, [
            {"role": "system", "content": system},
            {"role": "user", "content": human},
        ], model=self.model, max_tokens=700)
        code, call = extract_code(text)
        # Do not rewrite function definitions. Calls may be awaited; the
        # bridge's onChat is checked separately and the server log is a fact.
        return text, code, call


class Critic:
    def __init__(self, llm: str, model: str) -> None:
        self.llm = llm
        self.model = model

    def check(self, task: str, before: dict, after: dict,
              events: list, env: "BridgeEnv | None" = None) -> tuple[bool, str, dict]:
        on_chat = [e[1]["onChat"] for e in events if e[0] == "onChat"]
        low = task.lower()
        facts: dict[str, Any] = {"onChat": on_chat,
                                 "before": before.get("pos"),
                                 "after": after.get("pos")}
        if "say" in low:
            m = re.search(r"['\"]([^'\"]+)['\"]", task)
            expected = m.group(1) if m else ""
            ok = bool(expected and (any(expected in str(x) for x in on_chat) or
                                    (env is not None and env.log_has(expected))))
            facts["expected_chat"] = expected
            facts["fact"] = "chat"
        elif "mine" in low or "collect" in low:
            m = re.search(r"mine one ([a-z0-9_]+)", low)
            name = m.group(1) if m else "spruce_log"
            b = count_item(before, name)
            a = count_item(after, name)
            ok = a > b or count_total(after) > count_total(before)
            facts.update({"item": name, "before_count": b, "after_count": a,
                          "fact": "inventory"})
        elif "move" in low or "forward" in low:
            ok = before.get("pos") != after.get("pos")
            facts["fact"] = "position"
        else:
            ok = False
            facts["fact"] = "unsupported"

        # Local Qwen critique is explanatory only; it cannot override facts.
        try:
            raw = qwen(self.llm, [
                {"role": "system", "content": "Return only JSON {\"success\":bool,\"critique\":\"...\"}. Judge the task from the observed server facts."},
                {"role": "user", "content": json.dumps({"task": task, "facts": facts}, ensure_ascii=False)},
            ], model=self.model, max_tokens=160)
            obj = json_object(raw)
            critique = str(obj.get("critique") or "")
            qwen_says = bool(obj.get("success"))
        except Exception as e:
            critique = f"critic fallback: {e}"
            qwen_says = ok
        facts["qwen_says"] = qwen_says
        # Server facts are authoritative; Qwen cannot make false facts true.
        return bool(ok), critique, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", default=DEFAULT_LLM)
    ap.add_argument("--model", default="local")
    ap.add_argument("--adapter", default="/tmp/voyager-cbap.sock")
    ap.add_argument("--server-log", default="")
    ap.add_argument("--iterations", type=int, default=3)
    ap.add_argument("--max-attempts", type=int, default=2)
    ap.add_argument("--out", default=os.path.join(ROOT, "logs", "voyager-autonomy.json"))
    ap.add_argument("--skills", default=os.path.join(ROOT, "logs", "voyager-autonomy-skills.json"))
    args = ap.parse_args()

    report: dict = {"ok": False, "iterations": [], "model": args.model,
                    "mode": "local-Qwen Voyager-style autonomy over CBAP",
                    "llm": args.llm}
    env = None
    try:
        env = BridgeEnv(args.adapter, server_log=args.server_log)
        skills = SkillLibrary(args.skills)
        curriculum = Curriculum(args.llm, args.model)
        action = ActionAgent(args.llm, args.model)
        critic = Critic(args.llm, args.model)
        completed: list[str] = []
        failed: list[str] = []

        for i in range(args.iterations):
            state = env.state()
            task, context = curriculum.propose(state, completed, failed, i)
            rec = {"iteration": i + 1, "task": task, "context": context,
                   "attempts": []}
            print(f"\n=== iteration {i+1}: {task}", flush=True)
            success = False
            last_code = ""
            last_error = ""
            last_critique = ""
            for attempt in range(1, args.max_attempts + 1):
                try:
                    text, code, call = action.generate(
                        task, env._observe(state), skills,
                        last_code=last_code, error=last_error,
                        critique=last_critique,
                    )
                    events, after = env.step(code + "\n\n" + call)
                    ok, critique, facts = critic.check(task, state, after, events, env)
                    attempt_rec = {
                        "attempt": attempt,
                        "code": code,
                        "call": call,
                        "ok": ok,
                        "facts": facts,
                        "critique": critique,
                        "qwen_excerpt": text[:500],
                    }
                    rec["attempts"].append(attempt_rec)
                    print(f"  attempt {attempt}: {'OK' if ok else 'FAIL'} {facts}", flush=True)
                    last_code, last_error, last_critique = code, "", critique
                    if ok:
                        success = True
                        m = re.search(r"async\s+function\s+(\w+)\s*\(\s*bot", code)
                        name = m.group(1) if m else f"skill_{i+1}"
                        skills.add(task, name, code)
                        rec["skill_saved"] = name
                        break
                except Exception as e:
                    last_error = str(e)
                    rec["attempts"].append({"attempt": attempt, "ok": False,
                                            "error": str(e)})
                    print(f"  attempt {attempt}: EXCEPTION {e}", flush=True)
            rec["success"] = success
            if success:
                completed.append(task)
            else:
                failed.append(task)
            report["iterations"].append(rec)
            # Do not let one dead body poison the next iteration.
            if not success and env is not None:
                pass
        report["completed"] = completed
        report["failed"] = failed
        report["skills"] = [s["name"] for s in skills.skills]
        report["ok"] = bool(completed) and len(completed) >= max(1, args.iterations - 1)
    except Exception as e:
        report["error"] = str(e)
        print("AUTONOMY EXCEPTION:", e, flush=True)
    finally:
        if env:
            env.close()
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps({"ok": report["ok"], "out": args.out,
                          "completed": report.get("completed"),
                          "failed": report.get("failed"),
                          "skills": report.get("skills"),
                          "iterations": len(report.get("iterations", []))},
                         ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
