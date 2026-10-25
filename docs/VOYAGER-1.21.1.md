# Voyager bridge on Minecraft 1.21.1

**Date:** 2026-10-25
**Result:** real 1.21.1 bridge, CBAP 8/8 through `mc://voyager/bot`
**Scope:** Mineflayer bridge only; not VoyagerEnv, curriculum, skill library, or GPT-4.

---

## What was tested

```text
Minecraft 1.21.1 server   existing local runtime, port 25565
Node.js                  22.14.0
mineflayer               4.39.0
minecraft-data           3.117.0
Adapter                  agents/voyager/adapter/adapter.mjs
Kernel                   explicit read/write/lease/estop test policy
```

Result:

```text
OK  Voyager device visible
OK  read state             [11.7, 64, -41.3]
OK  lease
OK  forward under lease
OK  position changed       z -41.3 -> -42.7
OK  say under lease
OK  estop
OK  offline after estop
```

The forward test first faces +Z (`bot.look(0, 0, true)`) so a blocked spawn
heading does not produce a false negative.

## Compatibility changes

The upstream bridge was written for Minecraft 1.19 / old Mineflayer. For 1.21.1:

1. Upgrade `mineflayer` / `minecraft-data`.
2. Apply `agents/voyager/adapter/patches/voyager-state.patch` (`/state`).
3. Apply `agents/voyager/adapter/patches/voyager-1.21.1.patch`:
   - optional plugins fail soft instead of killing the bridge;
   - remove setup `/gamerule` chat commands;
   - disable `returnItems()` command chatter.
4. Start with `reset: "none"`; do not send `/clear`, `/kill`, or `/give` from
   the bridge on a non-op vanilla server.
5. The adapter forward pulse uses a wall-clock 1000 ms delay rather than
   `bot.waitForTicks(20)`, which can reject after server pauses.

Without these changes the vanilla server kicks the bot for `disconnect.spam`
after the setup/gamerule/return-items command burst.

## Reproduction shape

```bash
# 1. Start a 1.21.1 server (the repository's runtime is one option).
# 2. Prepare a Voyager source checkout and install current bridge deps.
cd /path/to/Voyager/voyager/env/mineflayer
npm install mineflayer@4.39.0 minecraft-data@3.117.0

# 3. Apply both patches from this repository.
patch -p1 < .../voyager-state.patch
patch -p1 < .../voyager-1.21.1.patch

# 4. Start the bridge and one bot.
node index.js 3000
curl -X POST localhost:3000/start -H 'content-type: application/json' \
  -d '{"port":25565,"reset":"none","inventory":{},"waitTicks":10}'

# 5. Start the CBAP adapter, then the probe.
node .../agents/voyager/adapter/adapter.mjs \
  --bridge http://127.0.0.1:3000 --socket /tmp/voyager-cbap.sock
CBAP_TEST_MODE=1 python3 .../agents/voyager/tools/voyager_cbap.py
```

## What this does not prove

```text
VoyagerEnv
automatic curriculum
skill library
critic
GPT-4 planning
full 1.21.1 action coverage (mining/crafting/furnace/pathfinder)
```

It proves the **body bridge** and the CBAP lease/facts/estop path work on
1.21.1. It does not prove the Voyager autonomous agent works on 1.21.1.
