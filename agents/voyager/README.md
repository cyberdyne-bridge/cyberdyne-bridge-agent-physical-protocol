# Voyager bridge

Status: **active / external, bridge only**

```text
upstream:  external/Voyager
adapter:   agents/voyager/adapter/adapter.mjs
device:    mc://voyager/bot
transport: HTTP bridge -> line JSON
control:   state / exec / forward / say / stop
```

This is **not** Voyager's autonomous Python agent. It is the Mineflayer bridge
only. The Voyager planner, curriculum, skill library, and critic are not wired.

This adapter lives directly under `agents/voyager/adapter/`; there is no
`drivers/voyager` shim.
The state endpoint patch is kept at `adapter/patches/voyager-state.patch`.

Local smoke: `python3 agents/voyager/smoke.py`
Tools: `agents/voyager/tools/`.

**2026-10-25 audit:** bridge-only; upstream Voyager agent/curriculum/skill
library are not wired. Current smoke is structural, not an end-to-end MC test.
The historical 1.19.2 8/8 result is not reproducible from this checkout
because `external/Voyager` and the 1.19.2 server are absent. Do not treat this
as a 1.21.1 brain until the bridge is revalidated. See
[`docs/VOYAGER-STATUS.md`](../../docs/VOYAGER-STATUS.md).
