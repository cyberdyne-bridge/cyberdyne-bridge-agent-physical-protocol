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

**2026-10-26 audit:** bridge-only. A real **1.21.1** bridge passes CBAP 8/8;
the local-Qwen autonomy loop completes 3/3 iterations; and upstream Voyager
agents complete a 3-task sequence (mine, craft via a seeded verified skill,
chat) 3/3. It still does not include the Voyager paper benchmark. GPT-era
legacy bugs follow
[`docs/VOYAGER-LEGACY-GPT-TRIAGE.md`](../../docs/VOYAGER-LEGACY-GPT-TRIAGE.md).
See
[`docs/VOYAGER-1.21.1.md`](../../docs/VOYAGER-1.21.1.md) and
[`docs/VOYAGER-LOCAL-QWEN.md`](../../docs/VOYAGER-LOCAL-QWEN.md) and
[`docs/VOYAGER-AUTONOMY.md`](../../docs/VOYAGER-AUTONOMY.md) and
[`docs/VOYAGER-UPSTREAM-BENCH.md`](../../docs/VOYAGER-UPSTREAM-BENCH.md).
