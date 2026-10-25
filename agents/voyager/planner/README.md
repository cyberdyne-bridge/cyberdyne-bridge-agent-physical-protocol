# Local Qwen Voyager planner

This is a **single-step, Voyager-prompt action planner** over the CBAP Voyager
bridge. It is not the upstream `Voyager` class and does not run VoyagerEnv or
the curriculum.

```bash
python3 agents/voyager/planner/local_qwen_action.py \
  --llm http://127.0.0.1:8099/v1/chat/completions \
  --adapter /tmp/voyager-cbap.sock \
  --server-log /path/to/minecraft/logs/latest.log
```

- `local_embeddings.py` replaces OpenAIEmbeddings with a dependency-free
  hashing fallback.
- `prompts/` is copied from the MIT-licensed MineDojo/Voyager action prompt.
- `local_qwen_action.py` asks local Qwen for JavaScript, extracts the main
  async function, and executes it through CBAP.

See [`docs/VOYAGER-LOCAL-QWEN.md`](../../../docs/VOYAGER-LOCAL-QWEN.md).
