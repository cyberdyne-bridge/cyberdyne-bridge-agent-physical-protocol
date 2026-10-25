# Disclaimer

**English** | [简体中文](DISCLAIMER.md)

> This is not legal advice. If you plan to use the project commercially, distribute binaries, provide a service, or deploy it in a regulated environment, consult qualified counsel.

## 1. Experimental software, provided "as is"

Cyberdyne Bridge / CBAP is research and experimental software. To the maximum extent permitted by applicable law, the authors and contributors provide the project **"AS IS"**, without any express or implied warranty, including but not limited to:

```text
merchantability
fitness for a particular purpose
non-infringement
freedom from defects
uninterrupted operation
no data loss
no hardware damage
```

The authors and contributors are not liable for any direct, indirect, incidental, special, punitive, or consequential damages arising from use, inability to use, modification, distribution, or reliance on the project.

## 2. Authorized environments only

Use the project only on devices, accounts, servers, and networks you own or are explicitly authorized to use.

Prohibited:

```text
unauthorized access to another person's devices or accounts
bypassing access controls, anti-cheat, or security mechanisms
violating the rules of a public Minecraft server
harassment, destruction, fraud, or attacks against others
using the project for any illegal activity
```

The user bears the consequences of violating game terms, server rules, account bans, network terms, or local law.

## 3. Host / desktop / input risk

The project includes a host test bridge and optional desktop, mouse, and keyboard device interfaces. These are **local test capabilities**, not production remote-administration products.

```text
the host bridge should bind only to 127.0.0.1 by default
input devices are off by default
explicit --enable-input is required
X11 and portal backends have different isolation and consent models
a fixed test token is not a production secret
```

Never expose the host bridge to the public internet and never enable input on a device without consent. The user bears losses caused by misconfiguration, weak tokens, network exposure, or mistaken operation.

## 4. AI / LLM uncertainty

The project may connect to local or external LLMs. Models may:

```text
hallucinate
misunderstand instructions
repeat actions
continue executing in an abnormal state
produce plausible but wrong plans
```

CBAP leases, policy, fencing, audit, estop, and fact verification reduce risk, but **are not a security certification** and cannot guarantee that AI behavior is correct.

## 5. Third-party names and projects

This is not an official project of, and does not represent endorsement by:

```text
Mojang Studios / Microsoft / NetEase
DeepSeek
Qwen / Alibaba Cloud
Mindcraft
Voyager / MineDojo
mineflayer-mcp
PrismarineJS
```

Minecraft is a trademark of Mojang Studios. Third-party components and patches are covered by [`THIRD_PARTY_NOTICES.en.md`](THIRD_PARTY_NOTICES.en.md).

## 6. No security certification / no compliance promise

The project has not undergone:

```text
formal verification
third-party security certification
medical/industrial/automotive/aviation safety certification
privacy compliance audit
export-control review
```

Do not use it directly for personal safety, medical, industrial control, critical infrastructure, or high-value assets.

## 7. AI collaboration disclosure

The project contains substantial AI-assisted or AI-generated code, tests, and documentation. Human maintainers are responsible for architecture, boundaries, and final acceptance, but this is not a guarantee of correctness or safety.

## 8. Limitation of liability

To the maximum extent permitted by applicable law, the authors, contributors, and organization are not liable for any claim, damage, loss, or liability, whether based on contract, tort, strict liability, or any other basis, and whether or not the possibility of such damage was disclosed.

## 9. Detailed terms

This document is an overview. More detailed terms are in:

```text
LEGAL/en/TERMS.md                 terms of use
LEGAL/en/ACCEPTABLE-USE.md        acceptable use
LEGAL/en/PRIVACY.md               privacy
LEGAL/en/ABUSE.md                 abuse reporting
LEGAL/en/INCIDENT-RESPONSE.md     incident response
LEGAL/en/RISK-REGISTER.md         risk register
LEGAL/en/COUNSEL-CHECKLIST.md     counsel checklist
```

## 10. Not legal advice

This document provides risk information only and is not legal advice. If you need commercial use or a public service, complete your own license, privacy, export, tax, and local-law review.
