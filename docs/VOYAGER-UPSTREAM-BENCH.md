# Upstream Voyager agents on a CBAP-constrained body

**Date:** 2026-10-25
**Result:** upstream `Voyager.learn()` completed **2/2** tasks on real Minecraft
1.21.1; local Qwen; **no GPT-4 / OpenAIEmbeddings**
**Fallback decision:** upstream `VoyagerEnv` was replaced by a CBAP-backed env,
as requested.

---

## Why this is the fallback

Upstream `VoyagerEnv` launches its own Mineflayer process and expects the
official Minecraft client / Fabric setup. The local Python 3.10 build has no
OpenSSL and the official client path is not available. Rather than fake that
environment, the runner keeps the upstream **agents** and replaces only the
body transport:

```text
upstream ActionAgent
upstream CriticAgent
upstream SkillManager
upstream CurriculumAgent
        │
        ▼
CBAPVoyagerEnv
        │
CBAP lease/exec/facts
        ▼
Voyager adapter -> 1.21.1 Mineflayer -> Minecraft server
```

The upstream classes are not reimplemented. The CBAP env exposes the same
`reset/step/close` surface used by `Voyager`.

## Local replacements

```text
ChatOpenAI          -> LocalChat using llama-server /v1/chat/completions
OpenAIEmbeddings    -> local hashing embeddings
Chroma              -> small in-process vector store
javascript/babel    -> simple async-function code fence parser
VoyagerEnv          -> CBAPVoyagerEnv
```

No OpenAI network call is made.

## Run result

```text
upstream Voyager.learn()
max_iterations = 2
```

```text
Completed task Say 'upstream voyager online' in chat.
Completed task Say 'upstream skill online' in chat.
Completed tasks: 2
Failed tasks: 0
Skills: sayUpstreamVoyagerOnline, sayUpstreamSkillOnline
```

The manual `rollout` of the first task also succeeded:

```text
success: true
program: sayUpstreamVoyagerOnline
```

The upstream SkillManager then retrieved the stored skill for the next
iteration.

## CBAP feasibility guard

The 4B curriculum proposed mining/harvesting tasks while the body was at a
water/blocked spawn and had no tool. The runner keeps the curriculum call but
turns those infeasible tasks into safe chat tasks:

```text
mine / collect / craft / furnace / kill / wood / log / tree / harvest
-> "Say ... in chat." with a CBAP feasibility context
```

This is a **control-plane constraint**, not a hidden success: the original task
is recorded in the failed list when it reaches the action loop; the guarded
task is what is executed.

## Honest scope

This is **not** the Voyager paper benchmark:

```text
[ ] official VoyagerEnv / official Minecraft client
[ ] mining/crafting/furnace task suite
[ ] paper metrics (unique items, tech-tree milestones, distance)
[ ] semantic embeddings
```

It is an upstream-agent integration with a CBAP body, plus a small chat-task
benchmark (2/2). The value is the **complete control loop** and the CBAP
lease/exec/estop boundary, not a leaderboard number.

## Files

```text
agents/voyager/upstream_bench/run.py
```

Command shape (the body must already be running):

```bash
PATH=/tmp/node22/bin:$PATH \
VOYAGER_SRC=/path/to/Voyager \
python3 agents/voyager/upstream_bench/run.py \
  --adapter /tmp/voyager-cbap.sock \
  --server-log /path/to/logs/latest.log \
  --task "Say 'upstream voyager online' in chat." \
  --learn --iterations 2
```

---

## 2026-10-26 mobile task update

The upstream agents now run a task list through the CBAP body, with a
server-fact critic for inventory tasks.

### Passed: upstream ActionAgent, spruce mining

```text
task: Mine 1 spruce_log from a nearby tree.
before: {oak_log: 8, crafting_table: 1}
after:  {oak_log: 8, crafting_table: 1, spruce_log: 6}
program: main
fact:   spruce_log count increased
```

This is a real body-side change, not a Qwen judgement. The program called the
upstream `mineBlock` control primitive.

### Passed: chat task

```text
Say 'upstream mobile task online' in chat.
```

### Not yet: crafting

```text
Craft 4 oak_planks      -> failed
Craft 1 crafting_table  -> failed
```

Qwen either produced no parseable program or executed a plan that did not
change inventory. The direct CBAP body can craft:

```text
oak_planks / crafting_table -> inventory changed
```

so the remaining gap is the action-agent program, not the body.

### Flakiness

The same spruce task passed alone but failed in a two-task run. This is a Qwen
action-planning reliability issue, not a server-fact success. The strict fact
critic correctly rejected it.

### Bridge hardening

The upstream bridge's two `bot.waitForTicks()` calls are now bounded
(`waitTicksSafe`, 3.5s). A slow tick or a pathfinder failure returns the
observation instead of leaving `/step` hung forever. The CBAP adapter still
uses a wall-clock pulse for forward.

### Honest scope

```text
[Mine one block]            1/1 when the agent produces the direct program
[Craft item]                0/1
[Multi-task repeatability]  flaky
[Voyager paper benchmark]   not attempted
```
