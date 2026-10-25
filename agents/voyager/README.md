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

**2026-10-25 audit:** bridge-only. A real **1.21.1** bridge test now passes
CBAP 8/8, and a local-Qwen Voyager-prompt action test executes through the
bridge. It still does not include VoyagerEnv, curriculum, skill library,
critic, GPT-4, or full 1.21.1 action coverage. See
[`docs/VOYAGER-1.21.1.md`](../../docs/VOYAGER-1.21.1.md) and
[`docs/VOYAGER-LOCAL-QWEN.md`](../../docs/VOYAGER-LOCAL-QWEN.md).
