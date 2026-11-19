# Native Cyberdyne random-world stone-pickaxe acceptance

- Date: 2026-11-19
- Result: **PASS**, based on server inventory facts, not `result.ok`.
- Path: native brain (`agents/cyberdyne/plugins/车钩.py` in legacy mode) -> native task stack -> native hand (`hand/node/server.js`) -> Minecraft 1.21.1.

## Run setup

```text
Server: mc-server.service, 127.0.0.1:25565, RCON disabled
Hand:   mc-hand.service
Brain:  mc-brain.service with CYBERDYNE_LEGACY=1
Memory: m7.memory_enable=false (reproduction mode)
Inventory: /clear DeepSeek; /give DeepSeek cooked_beef 64
Location: /spreadplayers 0 0 100 800 false DeepSeek
          -> settled at [104, 77, 773] (not the fixed spawn)
Task: chat "做个石镐" from mintstart
```

## Server-authoritative inventory

Queried with:

```text
/data get entity DeepSeek Inventory
```

Observed:

```text
dark_oak_log 5
dark_oak_planks 3
wooden_pickaxe 1 (damage 4)
dirt 6
cooked_beef 64
stone_pickaxe 1
```

## Native task evidence

```text
[22:29] 干完了：常识：stone_pickaxe。
```

## Fix required for this run

`proto_body.js` previously returned immediately when the requested placement
cell was occupied (e.g. dark-oak leaves). The plan then retried the same spot
until the task stalled. The hand now:

1. searches ±2 for an empty cell with a solid block below;
2. places there if found;
3. otherwise returns structured `先挖` / `挡着` fields so obstacle self-heal can
   remove the blocker and retry.

This is the difference between “the table is in a tree canopy” and a task that
can finish.

## Honest limits

- This is the native/legacy path, not the CBAP main chain.
- It started from a cleared inventory and supplied food, matching the historical
  native test conditions; it is not a fresh-world run.
- P1-D silent-exception baseline is still non-zero (see the enterprise review);
  this acceptance proves the functional tech tree, not every audit item.
