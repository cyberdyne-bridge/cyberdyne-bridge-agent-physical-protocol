# Voyager legacy-GPT bug triage

**Status:** policy + record template  
**Applies to:** Voyager code that depends on GPT-4-era prompts, OpenAI
Chat/Embeddings APIs, or the LangChain OpenAI adapters.

---

## Rule

When a Voyager bug looks like a GPT-era legacy issue:

```text
1. Reproduce on the pinned Voyager commit.
2. Classify the owner:
   - Voyager code
   - OpenAI API / SDK behavior
   - LangChain OpenAI adapter
   - prompt/model-era assumption
3. Search OpenAI upstream first (and LangChain where relevant) for an
   existing report or fix.
4. Record the search URLs, date, query, and result.
5. If already fixed upstream:
      -> record in VOYAGER-LEGACY-BUGS-FIXED.md
      -> do not open a duplicate issue
6. If not fixed, only partially fixed, or likely to affect future work:
      -> record in VOYAGER-LEGACY-BUGS-OPEN.md
      -> include residual impact, minimal repro, boundary, and proposed action
7. Do not post to OpenAI, LangChain, or Voyager without explicit approval.
8. Security/exploit issues go through a private channel first, not a public issue.
```

## Search order

Use the issue search API or web search, with the pinned error text and the
relevant API name:

```text
openai/openai-python          issues + releases
openai/openai-cookbook        examples/changelog
langchain-ai/langchain        OpenAIEmbeddings / ChatOpenAI / deprecations
MineDojo/Voyager              upstream implementation and issues
OpenAI docs/changelog         API behavior changes
```

Record the exact query, because "I searched and found nothing" is not
reproducible without it.

## What counts as fixed

```text
fixed upstream     a release/commit/PR resolves the behavior and the fix is
                   reachable from the pinned dependency, or a documented
                   migration exists
partial            an upstream fix exists but does not cover Voyager's usage
not fixed          no upstream report/fix, or the behavior is intentional and
                   Voyager must adapt
future impact      the issue can change task success, safety, or maintenance
                   later, even if it does not fail today
```

## Do not conflate

```text
Voyager expects GPT-4          != OpenAI API bug
LangChain adapter changed      != OpenAI model regression
prompt works only on GPT-4     != a Voyager runtime bug
local Qwen replacement         != proof the original bug is fixed
```

The record must say which layer is actually failing.

## Record template

Copy this into the fixed or open file:

```text
ID:
Date:
Voyager commit:
Component / file:
Symptom:
Minimal repro:
Expected:
Actual:
GPT-era dependency:
Owner layer:
Upstream search queries:
Upstream URLs checked:
Upstream status:
Evidence:
Residual impact:
Boundary / non-claims:
Decision:
Next action:
```

## Related

```text
docs/VOYAGER-BUGS.md
docs/VOYAGER-LEGACY-BUGS-FIXED.md
docs/VOYAGER-LEGACY-BUGS-OPEN.md
```
