# Voyager-style autonomy loop

**Date:** 2026-10-25
**Result:** 3/3 iterations completed on real Minecraft 1.21.1 through CBAP
**Model:** local Qwen3-4B, no GPT-4 / paid API
**Boundary:** this is a complete autonomy control loop, not the upstream
`VoyagerEnv` benchmark and not mining/crafting autonomy.

---

## The loop

```text
CurriculumAgent (local Qwen + validated fallback)
        │  task
        ▼
ActionAgent (Voyager action prompt + local Qwen)
        │  JavaScript
        ▼
BridgeEnv (CBAP lease -> Voyager adapter -> 1.21.1 Mineflayer)
        │  observation + chat + execution error
        ▼
Critic (server facts first, Qwen critique second)
        │  success / critique
        ▼
SkillLibrary (local hashing embeddings + JSON)
        └────────────► next ActionAgent prompt
```

This is the same control cycle as Voyager at the component level:

```text
propose -> act -> verify -> store skill -> propose again
```

It is implemented in:

```text
agents/voyager/autonomy/loop.py
agents/voyager/planner/local_embeddings.py
agents/voyager/planner/prompts/
```

---

## Real run

```text
Minecraft       1.21.1
Node            22.14.0
mineflayer      4.39.0
Qwen            Qwen3-4B-Instruct-2507-Q4_K_M.gguf
LLM endpoint    http://127.0.0.1:8099/v1
Transport       CBAP-U -> Kernel -> McDriver -> Voyager adapter -> bridge
```

Result:

```text
3/3
```

```text
[1] Say 'voyager autonomy online' in chat.   OK
[2] Say 'curriculum online' in chat.         OK
[3] Say 'skill memory online' in chat.       OK
```

Skill library:

```text
sayVoyagerAutonomy
sayCurriculumOnline
saySkillMemoryOnline
```

The server log confirmed the chat facts. In one iteration `onChat` was empty
but the server log contained the message; the critic used the server log as
the authoritative fact.

Command shape:

```bash
python3 agents/voyager/autonomy/loop.py \
  --llm http://127.0.0.1:8099/v1/chat/completions \
  --adapter /tmp/voyager-cbap.sock \
  --server-log /path/to/minecraft/logs/latest.log \
  --iterations 3
```

---

## What is complete

```text
[x] curriculum proposes tasks
[x] action agent writes JavaScript
[x] JavaScript executes on a real 1.21.1 body
[x] server facts decide success
[x] critic returns a critique
[x] successful skills persist and are retrievable
[x] next iteration uses the updated prompt/skills
```

## What is not complete

```text
[ ] upstream VoyagerEnv / official Minecraft client
[ ] upstream CurriculumAgent class
[ ] upstream CriticAgent class
[ ] full mining / crafting / furnace benchmark
[ ] semantic embeddings (local hashing fallback is used)
```

The local 4B curriculum fell back to safe chat tasks after the body was at a
blocked/water spawn. That is an environment/task-feasibility limit, not a
hidden success: the loop records `failed` tasks and moves on.

This document does **not** claim a Voyager paper benchmark. It claims the
end-to-end autonomy cycle runs over a real 1.21.1 body with local models and
server-fact verification.
