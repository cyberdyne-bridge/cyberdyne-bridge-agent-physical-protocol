# Voyager-style local Qwen planner

**Date:** 2026-10-25
**Result:** local Qwen generated executable JavaScript; CBAP executed it; the
Minecraft server logged the requested chat. No GPT-4, OpenAI API, or
OpenAIEmbeddings were used.
**Scope:** one action-planner step, not full VoyagerEnv/curriculum.

---

## Components

```text
Qwen3-4B-Instruct-2507-Q4_K_M.gguf
llama-server OpenAI-compatible endpoint: http://127.0.0.1:8099/v1
agents/voyager/planner/local_qwen_action.py
agents/voyager/planner/local_embeddings.py
agents/voyager/planner/prompts/action_template.txt
```

The prompt and response contract are copied from the MIT-licensed Voyager
action prompt. The skill retriever uses a dependency-free **local hashing
embedding** (`LocalHashingEmbeddings`), not OpenAIEmbeddings. It is a small
fallback, not a semantic embedding model.

## Flow

```text
1. Retrieve local skills by hashing embeddings.
2. Render Voyager's action prompt + response format + skill code.
3. Ask local Qwen for JavaScript.
4. Extract the last async function taking `bot`.
5. Execute it through the Voyager CBAP adapter.
6. Verify the server-side chat log (and position when the task moves).
```

## Result

Task:

```text
Say exactly 'qwen voyager 121', then stop.
```

```text
OK  device visible
OK  lease
OK  initial state
OK  Qwen code attempt 1
OK  exec attempt 1
OK  attempt 1 observed
OK  chat observed       server log: qwen voyager 121
OK  result
```

Qwen produced:

```javascript
async function sayQwenVoyager(bot) {
  await bot.chat("qwen voyager 121");
}
await sayQwenVoyager(bot);
```

The server log recorded:

```text
[Not Secure] <bot> qwen voyager 121
```

## Honest boundaries

This is **not** the upstream Voyager autonomous loop:

```text
no VoyagerEnv
no automatic curriculum
no persistent skill library
no critic loop
no GPT-4
no 1.21.1 mining/crafting coverage
```

The adapter `onChat` field returned empty for this particular code path even
though the server logged the message; the planner therefore accepts the
**Minecraft server log** as the authoritative chat fact.

The local embedding class is deliberately simple. For production-quality skill
retrieval, replace it with a real local embedding model and keep the same
`embed_documents` / `embed_query` shape.

## Next step

If the goal is full Voyager autonomy, the next work is:

```text
1. Implement a BridgeEnv with VoyagerEnv-compatible reset/step/observe.
2. Wire ActionAgent + CurriculumAgent + CriticAgent + SkillManager.
3. Replace ChatOpenAI/OpenAIEmbeddings at their construction points.
4. Re-run curriculum on 1.21.1 with server-fact completion.
```
