#!/usr/bin/env python3
"""Four isolation experiments for Voyager multi-task state.

A: same CBAP env, two direct craft steps (no ActionAgent/Qwen)
B: same Voyager instance, two chat tasks
C: same Voyager/ActionAgent, fresh SkillManager for the second craft
D: same Voyager/SkillManager, fresh ActionAgent for the second craft
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(ROOT, "kernel")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)

from agents.voyager.upstream_bench.run import (  # noqa: E402
    BridgeEnv, load_voyager_class,
)
from langchain.schema import AIMessage  # noqa: E402

CRAFT = '''async function craftPlanks(bot) {
  const item = bot.registry.itemsByName["oak_planks"];
  const recipes = bot.recipesFor(item.id, null, 1, null);
  if (!recipes.length) throw new Error("no oak_planks recipe");
  await bot.craft(recipes[0], 1, null);
}
await craftPlanks(bot);
'''

SKILL = '''async function craftOakPlanks(bot) {
    await craftItem(bot, "oak_planks", 4);
}'''


def make_voyager(adapter: str, log: str):
    Voyager = load_voyager_class(adapter, log)
    return Voyager(
        mc_port=25565, openai_api_key="local", max_iterations=1,
        action_agent_model_name="gpt-3.5-turbo",
        curriculum_agent_model_name="gpt-3.5-turbo",
        curriculum_agent_qa_model_name="gpt-3.5-turbo",
        critic_agent_model_name="gpt-3.5-turbo",
        skill_manager_model_name="gpt-3.5-turbo",
        ckpt_dir="/tmp/voyager-isolation-ckpt",
        skill_library_dir=None, resume=False,
    )


def add_skill(sm):
    sm.add_new_skill({
        "task": "Craft 4 oak_planks",
        "program_name": "craftOakPlanks",
        "program_code": SKILL,
    })


def route_craft(v):
    def process(message=None, **kwargs):
        return {
            "program_code": "async function useSeededCraft(bot) {\n"
                            "    await craftOakPlanks(bot);\n}",
            "program_name": "useSeededCraft",
            "exec_code": "await useSeededCraft(bot);",
            "programs": [],
        }
    v.action_agent.process_ai_message = process
    # ActionAgent.render_system_message reads this attribute.
    if not hasattr(v.action_agent.llm, "model_name"):
        v.action_agent.llm = type("LLM", (), {"model_name": "local",
            "__call__": lambda self, messages: AIMessage(content="")})()
    else:
        v.action_agent.llm.model_name = getattr(v.action_agent.llm, "model_name", "local")


def craft_once(v):
    before = v.env.inner.state().get("items") or {}
    msgs, _, done, info = v.rollout(
        task="Craft 4 oak_planks with the wood you have.",
        context="Use the verified craftOakPlanks skill.",
    )
    return {"success": bool(info.get("success")),
            "program": info.get("program_name"),
            "before": before,
            "after": v.env.inner.state().get("items") or {},
            "done": done}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", choices=list("abcd"))
    ap.add_argument("--adapter", default="/tmp/voyager-cbap.sock")
    ap.add_argument("--server-log", default="")
    ap.add_argument("--out", default="/tmp/voyager-isolation.json")
    a = ap.parse_args()
    os.environ["OPENAI_API_KEY"] = "local"
    os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:8099/v1"
    out = {"experiment": a.experiment}
    if a.experiment == "a":
        env = BridgeEnv(a.adapter, server_log=a.server_log)
        try:
            env.step("")
            before = env.state().get("items") or {}
            env.step(CRAFT)
            first = env.state().get("items") or {}
            env.step(CRAFT)
            second = env.state().get("items") or {}
            out.update({"before": before, "first": first, "second": second,
                        "ok": first.get("oak_planks", 0) > 0 and
                              second.get("oak_planks", 0) > first.get("oak_planks", 0)})
        finally:
            env.close()
    elif a.experiment == "b":
        v = make_voyager(a.adapter, a.server_log)
        try:
            results = []
            for text in ("say isolation one", "say isolation two"):
                _, _, done, info = v.rollout(task=f"Say '{text}' in chat.", context="")
                results.append({"task": text, "success": bool(info.get("success")),
                                "program": info.get("program_name"), "done": done})
            out.update({"results": results, "ok": all(r["success"] for r in results)})
        finally:
            v.close()
    else:
        v = make_voyager(a.adapter, a.server_log)
        try:
            add_skill(v.skill_manager)
            route_craft(v)
            first = craft_once(v)
            # Capture state before second; craft_once captures after only.
            before2 = v.env.inner.state().get("items") or {}
            if a.experiment == "c":
                from voyager.agents import SkillManager
                v.skill_manager = SkillManager(
                    model_name="gpt-3.5-turbo",
                    ckpt_dir="/tmp/voyager-isolation-skill2",
                    resume=False,
                )
                add_skill(v.skill_manager)
            else:
                from voyager.agents import ActionAgent
                v.action_agent = ActionAgent(
                    model_name="gpt-3.5-turbo",
                    ckpt_dir="/tmp/voyager-isolation-action2",
                    resume=False,
                )
                route_craft(v)
            second = craft_once(v)
            second["before"] = before2
            out.update({"first": first, "second": second,
                        "ok": first["success"] and second["success"]})
        finally:
            v.close()
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
