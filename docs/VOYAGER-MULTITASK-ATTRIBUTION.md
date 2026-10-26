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
