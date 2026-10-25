# AI Disclosure

**Version:** 2026-10-24

## 1. Where AI was involved

This project contains substantial AI-assisted or AI-generated material, potentially including:

```text
Kernel / driver / test code
documentation and diagrams
test cases
commit messages
security notes
the first drafts of this legal directory
```

Human maintainers are responsible for:

```text
architecture and boundaries
security red lines and acceptance
merge decisions
release decisions
```

Human review is not a guarantee of correctness, security, or legal compliance.

## 2. AI output is not fact

AI may:

```text
invent APIs
get boundary conditions wrong
miss threats
produce unsafe defaults
cite laws or cases that do not exist
```

All security and legal text must be reviewed by humans and, where needed, counsel. The legal files here are engineering drafts, not legal opinions.

## 3. Models and training data

This project does not distribute model weights. If you connect DeepSeek, Qwen, or another model, you must comply with its model license and service terms. Model output may contain third-party content; you are responsible for copyright, privacy, and accuracy.

## 4. Prompt injection

Web pages, chats, files, and MCP tool output read by an agent may contain malicious instructions. Do not treat model output as trusted system instruction. Authorization must be decided by the Kernel/policy, not by a prompt.

## 5. Responsibility

The user bears responsibility for actions, costs, errors, and consequences produced by AI. The maintainers do not guarantee that AI behavior matches your intent, law, or industry standards.

## 6. Disclosure recommendation

If you distribute this project or a modified version, retain this disclosure and state:

```text
which parts were AI-assisted
what human review was performed
which known limitations apply
```
