# Voyager bugs / minimal reproductions / PoCs

**Date:** 2026-10-25  
**Upstream:** MineDojo/Voyager `55e45a880755d0c8c66ca7fb5fe7962ac8974f89` (2023-07-27)  
**Tested with:** Node 22.14, Mineflayer 4.39, Minecraft 1.21.1, Python 3.10  
**Status:** reliability / compatibility report, not a security advisory  
**Not legal advice.**

---

## Summary

| ID | Severity | Component | Issue | Confidence |
|---|---|---|---|---|
| VY-01 | P1 | `voyager/utils/record_utils.py` | `EventRecorder` assumes every event has `status`/`inventory`; `onChat` does not, so recording a chat action crashes with `KeyError: 'status'` | confirmed |
| VY-02 | P1 | `voyager/agents/action.py` | `process_ai_message` requires `@babel/core` and `@babel/generator`, but they are not in the bridge package; parsing fails on a clean install | confirmed |
| VY-03 | P1/P2 | `voyager/env/mineflayer/index.js` | optional `minecrafthawkeye` export is an object, but upstream passes it directly to `bot.loadPlugin()`; this throws `plugin needs to be a function` | confirmed |
| VY-04 | P2 | `voyager/env/mineflayer/index.js` | setup / `returnItems()` sends multiple `/gamerule`, `/setblock`, `/give` commands per step; observed `disconnect.spam` on a non-op vanilla 1.21.1 body | observed, server-config dependent |
| VY-05 | P2 | `voyager/env/mineflayer/mineflayer-collectblock` | `npm install` alone does not produce `lib/index.js`; the bridge crashes on startup unless `npx tsc` is run | confirmed setup footgun |
| VY-06 | P3 | bridge `/step` | `bot.waitForTicks()` can reject after a paused/slow-tick or kicked body; the bridge then exits on an uncaught timeout | observed, operational |

---

## VY-01 — EventRecorder crashes on `onChat`

**Affected:** `voyager/utils/record_utils.py`, `EventRecorder.record()` / `update_items()`

**Symptom:**

```text
KeyError: 'status'
```

`Voyager.step()` calls `self.recorder.record(events, task)` for every action.
The bridge emits an `onChat` event shaped as:

```json
["onChat", {"onChat": "hello"}]
```

`update_items(event)` unconditionally reads:

```python
inventory = event["inventory"]
elapsed_time = event["status"]["elapsedTime"]
```

So a chat action crashes the recorder before the critic/skill step.

**Minimal repro:**

```bash
VOYAGER_SRC=/path/to/Voyager \
python3 poc/voyager/poc_record_onchat.py
```

The PoC feeds:

```python
[
  ["onChat", {"onChat": "hello"}],
  ["observe", {"status": {...}, "inventory": {}, "blockRecords": []}],
]
```

**Actual:**

```text
REPRODUCED: KeyError 'status' (onChat event has no status/inventory)
```

**Expected:** recording should ignore non-observation events for inventory
bookkeeping, or the bridge should attach the last observation snapshot to every
event.

**PoC:** [`poc/voyager/poc_record_onchat.py`](../poc/voyager/poc_record_onchat.py)

**Workaround / fix:**

```python
for event_type, event in events:
    if event_type != "observe":
        continue
    self.update_items(event)
    self.update_elapsed_time(event)
```

Our CBAP adapter also attaches the full observation to `onChat`, which is why
the upstream runner can proceed.

---

## VY-02 — ActionAgent has an undeclared Babel dependency

**Affected:** `voyager/agents/action.py`, `ActionAgent.process_ai_message()`

**Symptom:**

```text
Cannot find module '@babel/core'
```

`process_ai_message` does:

```python
babel = require("@babel/core")
babel_generator = require("@babel/generator").default
```

But the bridge `package.json` does not list either package. The Python
`javascript` package runs Node but does not install Babel.

**Minimal repro:**

```bash
VOYAGER_SRC=/path/to/Voyager \
PATH=/path/to/node/bin:$PATH \
bash poc/voyager/poc_babel_missing.sh
```

**Actual:**

```text
REPRODUCED: @babel/core is missing from the bridge package
REPRODUCED: @babel/generator is also missing
```

**Expected:** the package should declare/install Babel, or the parser should not
depend on it.

**PoC:** [`poc/voyager/poc_babel_missing.sh`](../poc/voyager/poc_babel_missing.sh)

**Workaround:** install `@babel/core` and `@babel/generator` in the bridge
package, or replace `process_ai_message` with a small code-fence parser.

```javascript
// package.json (workaround)
"@babel/core": "^7.24.0",
"@babel/generator": "^7.24.0"
```

---

## VY-03 — Optional hawkeye plugin is an object, not a function

**Affected:** `voyager/env/mineflayer/index.js`, spawn handler

**Symptom:**

```text
AssertionError [ERR_ASSERTION]: plugin needs to be a function
```

Upstream does:

```javascript
const minecraftHawkEye = require("minecrafthawkeye");
bot.loadPlugin(minecraftHawkEye);
```

The installed export is an object:

```text
typeof minecrafthawkeye = object
keys = ['default', 'Vec2', 'Weapons', ...]
```

`bot.loadPlugin()` requires a function.

**Minimal repro:**

```bash
VOYAGER_SRC=/path/to/Voyager \
PATH=/path/to/node/bin:$PATH \
node poc/voyager/poc_hawkeye_plugin.js
```

**Actual:**

```text
require("minecrafthawkeye") typeof = object
REPRODUCED: upstream calls bot.loadPlugin(minecraftHawkEye) with an object
```

**Expected:** guard on type or use the actual plugin function.

```javascript
if (typeof minecraftHawkEye === "function") {
  bot.loadPlugin(minecraftHawkEye);
} else if (typeof minecraftHawkEye?.default === "function") {
  bot.loadPlugin(minecraftHawkEye.default);
}
```

**PoC:** [`poc/voyager/poc_hawkeye_plugin.js`](../poc/voyager/poc_hawkeye_plugin.js)

---

## VY-04 — Setup / returnItems command chatter can trip `disconnect.spam`

**Affected:** `voyager/env/mineflayer/index.js`

**Symptom observed in the real 1.21.1 bridge:**

```text
[Not Secure] <bot> voyager cbap works
bot lost connection: Kicked for spamming
```

The bridge sends, without an op check:

```javascript
bot.chat("/gamerule keepInventory true");
bot.chat("/gamerule doDaylightCycle false");

// after each /step:
function returnItems() {
  bot.chat("/gamerule doTileDrops false");
  ...
  bot.chat("/give @s crafting_table");
  ...
  bot.chat("/gamerule doTileDrops true");
}
```

On a vanilla server with a non-op bot, this is a burst of chat/command packets.
The exact kick threshold is server-configuration dependent; a minimal 3-command
probe did not kick, so this is reported as an **observed compatibility issue**,
not a deterministic upstream repro.

**Repro context:** apply `voyager-1.21.1.patch`? The patch removes these
commands; remove those hunks to restore the behavior, start the bridge and run
one action. The observed bridge log is above.

**Workaround:** default `returnItems()` to no-op; send setup commands only with
an explicit `setupCommands: true` and an op/allowlist check. This is what the
1.21.1 patch does.

**Confidence:** observed; not a universal guaranteed kick.

---

## VY-05 — `mineflayer-collectblock` has no built `lib/`

**Affected:** `voyager/env/mineflayer/mineflayer-collectblock`

**Symptom:**

```text
Error: Cannot find module '.../node_modules/mineflayer-collectblock/lib/index.js'
```

A plain `npm install` does not build the local TypeScript package. The upstream
installation docs do say `cd mineflayer-collectblock && npx tsc`, but the bridge
otherwise crashes during startup.

**Minimal repro:**

```bash
cd /path/to/Voyager/voyager/env/mineflayer
npm install
node -e "require('mineflayer-collectblock')"
```

**Expected:** `npm install` should build the local package, or the package should
ship `lib/`.

**Workaround:**

```bash
cd mineflayer-collectblock
npx tsc
```

**Confidence:** confirmed; this is a setup footgun rather than a runtime logic
bug.

---

## VY-06 — `waitForTicks` after a paused/slow/kicked body

**Affected:** bridge `/step`, `bot.waitForTicks(bot.waitTicks)`

**Symptom observed:**

```text
Error: Timeout waiting for 10 ticks after 5500ms
```

When the server is paused, slow, or the bot has been kicked, the bridge's
`waitForTicks` rejects and the process exits via an uncaught exception. This is
an operational hardening issue; it is not reported as a universal code bug.

**Workaround used by CBAP:** use a wall-clock pulse for short moves, and fail the
CBAP action instead of leaving an uncaught Node exception.

---

## PoC index

```text
poc/voyager/poc_record_onchat.py
poc/voyager/poc_babel_missing.sh
poc/voyager/poc_hawkeye_plugin.js
```

Run from the repository root with `VOYAGER_SRC` pointing at a Voyager checkout
and Node on `PATH`.

## What is not claimed

- No CVE or remote exploit.
- No claim that every 1.21.1 server kicks at the same threshold.
- No claim that upstream Voyager is unmaintained or malicious.
- These are reliability/compatibility findings from a local CBAP integration.
