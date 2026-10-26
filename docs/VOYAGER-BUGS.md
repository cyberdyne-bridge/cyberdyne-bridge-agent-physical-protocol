# Voyager bugs / minimal reproductions / PoCs

**Date:** 2026-10-26 (revised; VY-01 retracted)
**Upstream:** MineDojo/Voyager `55e45a880755d0c8c66ca7fb5fe7962ac8974f89` (2023-07-27)
**Tested with:** Node 22.14, Mineflayer 4.39, Minecraft 1.21.1, Python 3.10
**Status:** reliability / compatibility report, not a security advisory
**Not legal advice.**

> GPT-era legacy issues must first be checked for an OpenAI/LangChain upstream
> fix and recorded under
> [`VOYAGER-LEGACY-GPT-TRIAGE.md`](VOYAGER-LEGACY-GPT-TRIAGE.md).

---

## Summary

| ID | Severity | Component | Issue | Confidence |
|---|---|---|---|---|
| VY-01 | — | CBAP adapter | **RETRACTED as an upstream bug.** The upstream `bot.event()` includes every non-`on*` observation in an `onChat` event; our CBAP adapter omitted them. The adapter was fixed. | not upstream |
| VY-02 | P1 | `voyager/agents/action.py` | `process_ai_message` requires `@babel/core` and `@babel/generator`, but they are not in the bridge package; parsing fails on a clean install | confirmed |
| VY-03 | P1/P2 | `voyager/env/mineflayer/index.js` | optional `minecrafthawkeye` export is an object, but upstream passes it directly to `bot.loadPlugin()`; this throws `plugin needs to be a function` | confirmed |
| VY-04 | P2 | `voyager/env/mineflayer/index.js` | setup / `returnItems()` sends multiple `/gamerule`, `/setblock`, `/give` commands per step; observed `disconnect.spam` on a non-op vanilla 1.21.1 body | observed, server-config dependent |
| VY-05 | info | `voyager/env/mineflayer/mineflayer-collectblock` | `npm install` alone does not produce `lib/index.js`, but the upstream README already says `npx tsc` | documented setup, not a bug |
| VY-06 | P3 | bridge `/step` | `bot.waitForTicks()` can reject after a paused/slow-tick or kicked body; the bridge then exits on an uncaught timeout | observed, operational |

---

## Revision 2026-10-26

```text
VY-01  retracted: CBAP adapter emitted incomplete onChat; upstream includes
       non-on observations in bot.event()
VY-03  clarified: 1.3.6 function -> 1.3.7+ object default; upstream ^1.3.6
       now resolves 1.3.9
VY-04  removed editorial question; observed compatibility only
VY-05  downgraded: upstream README already says npx tsc
```

---

## VY-01 — RETRACTED: this was a CBAP adapter bug, not Voyager

**Affected:** our CBAP adapter, not `voyager/utils/record_utils.py`

**Correction:** The upstream bridge does include `status`, `inventory`, `voxels`,
and the other non-`on*` observations in every `onChat` event. In
`voyager/env/mineflayer/lib/observation/base.js`:

```javascript
bot.event = function (event_name) {
    let result = {};
    bot.obsList.forEach((obs) => {
        if (obs.name.startsWith("on") && obs.name !== event_name) return;
        result[obs.name] = obs.observe();
    });
    bot.cumulativeObs.push([event_name, result]);
};
```

Only other `on*` observations are skipped. `status`, `inventory`, `voxels`,
etc. are still included.

Our CBAP adapter originally forwarded only:

```json
["onChat", {"onChat": "hello"}]
```

That made the upstream recorder crash. We changed the adapter to attach the full
observation snapshot to `onChat`. The PoC now demonstrates the **adapter
contract**, not an upstream bug:

```bash
VOYAGER_SRC=/path/to/Voyager \
python3 poc/voyager/poc_cbap_onchat_contract.py
```

Expected:

```text
REPRODUCED (CBAP adapter contract): KeyError 'status'
```

This is retained as a regression test for our adapter. It must not be reported
to Voyager.

**PoC:** [`poc/voyager/poc_cbap_onchat_contract.py`](../poc/voyager/poc_cbap_onchat_contract.py)

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

**Version note:** the upstream range is `^1.3.6`. `minecrafthawkeye@1.3.6`
ended with `module.exports = inject` (a function); `1.3.7` and later export an
object with a `default` key. A fresh install today resolves `1.3.9`, so the
failure is a version-drift bug, not a property of 1.3.6.

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

**Repro context:** remove the setup/`returnItems` hunks from the 1.21.1
compatibility patch, start the bridge, and run one action. The observed bridge
log is above.

**Workaround:** default `returnItems()` to no-op; send setup commands only with
an explicit `setupCommands: true` and an op/allowlist check. This is what the
1.21.1 patch does.

**Confidence:** observed; not a universal guaranteed kick.

---

## VY-05 — Documented setup step: `mineflayer-collectblock` needs `npx tsc`

**Affected:** `voyager/env/mineflayer/mineflayer-collectblock`

**Status:** not an upstream bug. The upstream README already documents the
build step at lines 56–57.

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

**Expected:** follow the documented build step.

**Workaround:**

```bash
cd mineflayer-collectblock
npx tsc
```

**Confidence:** documented setup; downgraded from P2 to informational.

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
poc/voyager/poc_cbap_onchat_contract.py
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
