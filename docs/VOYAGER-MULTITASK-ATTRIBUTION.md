# Voyager multi-task attribution — 2026-10-26

**Question:** is the 5-task craft failure a Minecraft/CBAP body problem, an
upstream Voyager problem, or our runner/skill-state problem?

**Environment:** Minecraft 1.21.1, local Mineflayer bridge, CBAP adapter,
upstream Voyager agents, local Qwen 4B. Fake inventory setup; local only.

---

## A. Fresh Voyager instance per task

Two separate runner invocations, same body and adapter:

```text
A1  Mine 1 spruce_log      -> success
    before: {oak_log: 8, crafting_table: 1}
    after:  {oak_log: 8, crafting_table: 1, spruce_log: 2}

A2  Craft 4 oak_planks     -> success
    before: {oak_log: 8, crafting_table: 1, spruce_log: 2}
    after:  {oak_log: 4, oak_planks: 16, crafting_table: 1, spruce_log: 2}
```

Result: **2/2**.

## B. Same Voyager instance, two craft tasks

One runner invocation, same inventory setup:

```text
B1  Craft 4 oak_planks     -> success
    before: {oak_log: 8, crafting_table: 1}
    after:  {oak_log: 4, oak_planks: 16, crafting_table: 1,
             spruce_sapling: 2, spruce_log: 11}

B2  Craft 4 oak_planks     -> failure
    before: {oak_log: 4, oak_planks: 16, crafting_table: 1,
             spruce_sapling: 2, spruce_log: 11}
    after:  same
    fact:   oak_planks did not increase (16 -> 16)
```

Result: **1/2**, second task fails even though the body still has oak logs and
the verified craft skill is available.

## Earlier C

The same pattern appeared in the five-task run:

```text
Mine OK
Craft 4 oak_planks  failed
Craft 1 table       failed
Craft 1 pickaxe     failed
Say OK
```

## Interpretation

```text
Not the body:       direct craft and A2 succeed
Not the primitive:  craftItem works in A2
Not proof of an upstream Voyager bug
```

The failure appears when the **same Voyager instance performs more than one
task**. The second task receives no inventory-changing program, so the strict
fact critic rejects it.

Current attribution:

```text
Our multi-task runner / skill-state reuse is the first suspect.
```

Possible mechanisms, in order:

```text
1. ActionAgent / SkillManager state is not clean between tasks.
2. The seeded-skill routing is not actually applied on the second task.
3. The second action is generated but the skill code is not in env programs.
4. Voyager instance reuse semantics differ from what our runner assumes.
```

## Four isolation experiments — results

Script: `agents/voyager/upstream_bench/isolation.py`

| Experiment | Isolation | Result |
|---|---|---|
| A | same CBAP env, two direct craft steps; no ActionAgent/Qwen | **2/2** |
| B | same Voyager instance, two chat tasks | **2/2** |
| C | same ActionAgent, fresh SkillManager for second craft | **2/2** |
| D | same SkillManager, fresh ActionAgent for second craft | **2/2** |

### A — direct env

```text
before: oak_log 8
first:  oak_log 7, oak_planks 4
second: oak_log 6, oak_planks 8
```

### B — two chat tasks

```text
say isolation one  -> success
say isolation two  -> success
```

### C — fresh SkillManager

```text
first:  oak_planks 0 -> 16
second: oak_planks 16 -> 32
```

### D — fresh ActionAgent

```text
first:  oak_planks 0 -> 16
second: oak_planks 16 -> 28
```

## Revised attribution

All four isolations pass. The failure was **not reproduced** by:

```text
direct env reuse
same-Voyager chat reuse
fresh SkillManager
fresh ActionAgent
```

Therefore the current evidence points to the **runner's seeded-skill routing
and task-wrapper state**, not to:

```text
Minecraft / CBAP body
craft primitive
Voyager SkillManager alone
Voyager ActionAgent alone
GPT-era OpenAI API
```

The next step is to instrument the runner's second craft task:

```text
current_skill
routed_process return value
SkillManager.programs contains craftOakPlanks
env.step programs argument
```

The isolation script itself is a diagnostic, not the production runner.

## Next experiment



Before changing the architecture:

```text
1. Add a fresh Voyager instance per task and rerun A -> B.
2. If that passes, implement a clean per-task instance boundary.
3. If it still fails, inspect ActionAgent messages, current_skill,
   SkillManager.programs and env.step arguments on the second task.
```

## Non-claims

```text
No upstream Voyager issue
No claim that the body is broken
No claim that the 5-task suite passed
```
