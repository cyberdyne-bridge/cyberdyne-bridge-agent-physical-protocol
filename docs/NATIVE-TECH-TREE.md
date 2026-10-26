# Native Cyberdyne tech tree — 2026-10-26

**Result: passed.** The native Cyberdyne brain/task stack/hand built a stone
pickaxe from an empty inventory on the local Minecraft 1.21.1 server.

This is the native path, not Voyager.

## Setup

```text
Minecraft 1.21.1, local server
bot: DeepSeek
native hand: agents/cyberdyne/hand/node/server.js
native brain: plugins/车钩.py + brain/bridge.py
native task stack: brain/bridge.py 任务栈
native solver: plugins/常识/求解器.py
```

The body was cleared, then given only food:

```text
/clear DeepSeek
/give DeepSeek cooked_beef 64
/tp DeepSeek 473 69 -131
```

The command was one chat line from `mintstar`:

```text
做个石镐
```

## Solver plan

The native solver produced a 24-step materialized plan:

```text
walk to birch_log -> mine birch_log -> collect birch_log
-> craft birch_planks -> craft crafting_table -> place crafting_table
-> mine/collect more logs -> craft sticks -> craft wooden_pickaxe
-> walk to stone -> mine stone -> collect cobblestone
-> craft stone_pickaxe
```

The task stack accepted the plan and executed it.

## Server-authoritative result

RCON inventory after completion:

```text
birch_log 4
birch_planks 7
dirt 11
wooden_pickaxe 1 (damage 4)
cooked_beef 64
stone_pickaxe 1
```

Native task log:

```text
[21:20] 「craft」成了（合成=stone_pickaxe）。
[21:21] 干完了：常识：stone_pickaxe。
```

The decisive fact is the server inventory containing `stone_pickaxe`, not a
Qwen critic sentence.

## What this proves

```text
native solver -> task stack -> hand -> server facts
```

works end-to-end for the small tech tree on 1.21.1.

## What this does not prove

```text
- It is not the CBAP main chain; this run used the legacy native brain/hand path.
- It is not a generality claim for other Minecraft versions or other agents.
- The run supplied food and started from a cleared inventory, matching the
  historical native test conditions; it did not start from a fresh world.
```

## Setup quirks fixed for this run

```text
- native config must be read from agents/cyberdyne/config.json
- native brain and hand must share agents/cyberdyne/cyberdyne.sock
- native minecraft-data is under hand/node/node_modules
- native plugins expect 外挂/ and 常识库/ next to the agent; compatibility
  links are committed
```

## Next

The next architectural step is not to move this entire task stack into CBAP.
It is to keep this brain as an external Agent and expose the body through a
CBAP adapter, so the control plane can lease/stop/audit it without absorbing
the planner.
