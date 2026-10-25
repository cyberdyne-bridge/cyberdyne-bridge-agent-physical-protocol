# Cyberdyne Bridge / CBAP — English Legal Pack

**Version:** 2026-10-24  
**Status:** Complete English translation for convenience and review  
**Not legal advice. Not lawyer-reviewed.**

> The Chinese documents in `LEGAL/` remain the source text.  
> This English pack is provided so international readers can review the same
> boundaries. If the Chinese and English texts differ, the Chinese source
> controls; for commercial use, have counsel review the applicable version.

---

## Contents

1. Disclaimer
2. Terms of Use
3. Acceptable Use Policy
4. Privacy
5. Abuse Reporting and Handling
6. Incident Response
7. Risk Register
8. AI Disclosure
9. Export, Sanctions, and Encryption
10. Counsel Review Checklist
11. Legal FAQ
12. Third-Party Notices
13. Trademarks
14. Security Policy
15. Contributing and Contribution License

---


## Disclaimer

> Source: `DISCLAIMER.en.md`

**English** | [简体中文](../../DISCLAIMER.en.md)

> This is not legal advice. If you plan to use the project commercially, distribute binaries, provide a service, or deploy it in a regulated environment, consult qualified counsel.

### 1. Experimental software, provided "as is"

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

### 2. Authorized environments only

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

### 3. Host / desktop / input risk

The project includes a host test bridge and optional desktop, mouse, and keyboard device interfaces. These are **local test capabilities**, not production remote-administration products.

```text
the host bridge should bind only to 127.0.0.1 by default
input devices are off by default
explicit --enable-input is required
X11 and portal backends have different isolation and consent models
a fixed test token is not a production secret
```

Never expose the host bridge to the public internet and never enable input on a device without consent. The user bears losses caused by misconfiguration, weak tokens, network exposure, or mistaken operation.

### 4. AI / LLM uncertainty

The project may connect to local or external LLMs. Models may:

```text
hallucinate
misunderstand instructions
repeat actions
continue executing in an abnormal state
produce plausible but wrong plans
```

CBAP leases, policy, fencing, audit, estop, and fact verification reduce risk, but **are not a security certification** and cannot guarantee that AI behavior is correct.

### 5. Third-party names and projects

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

Minecraft is a trademark of Mojang Studios. Third-party components and patches are covered by [`THIRD_PARTY_NOTICES.en.md`](../../THIRD_PARTY_NOTICES.en.md).

### 6. No security certification / no compliance promise

The project has not undergone:

```text
formal verification
third-party security certification
medical/industrial/automotive/aviation safety certification
privacy compliance audit
export-control review
```

Do not use it directly for personal safety, medical, industrial control, critical infrastructure, or high-value assets.

### 7. AI collaboration disclosure

The project contains substantial AI-assisted or AI-generated code, tests, and documentation. Human maintainers are responsible for architecture, boundaries, and final acceptance, but this is not a guarantee of correctness or safety.

### 8. Limitation of liability

To the maximum extent permitted by applicable law, the authors, contributors, and organization are not liable for any claim, damage, loss, or liability, whether based on contract, tort, strict liability, or any other basis, and whether or not the possibility of such damage was disclosed.

### 9. Detailed terms

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

### 10. Not legal advice

This document provides risk information only and is not legal advice. If you need commercial use or a public service, complete your own license, privacy, export, tax, and local-law review.

---


## Terms of Use

> Source: `LEGAL/en/TERMS.md`

**Version:** 2026-10-24  
**Applies to:** Cyberdyne Bridge / CBAP code, documentation, websites, and releases  
**Important:** This is a risk-allocation draft, not legal advice. Have counsel review it before commercial use or distribution.

---

### 1. Acceptance

By cloning, downloading, installing, running, modifying, distributing, or deploying this project, or by accessing its website, you confirm that you have read and agree to these Terms, [`DISCLAIMER.md`](../../DISCLAIMER.en.md), [`ACCEPTABLE-USE.md`](ACCEPTABLE-USE.md), and any applicable third-party licenses.

If you do not agree, do not use the project.

If you use the project on behalf of an organization, you represent that you have authority to accept these Terms for that organization.

### 2. Eligibility

The project is intended for users with the relevant technical ability and legal capacity. If you are under 18, use it only with the knowledge and consent of a parent or guardian, and comply with local rules on minors, online services, and game accounts.

### 3. License scope

Original CBAP code and original documentation are provided under the **MIT** license in the root [`LICENSE`](../../LICENSE).

Third-party components, patches, dependencies, external projects, names, and trademarks **do not become MIT because of these Terms**. When redistributing, you must retain:

```text
the root LICENSE
THIRD_PARTY_NOTICES.md
third_party/licenses/
the LICENSE / NOTICE next to each patch
upstream copyright and license notices
```

In particular, the `mineflayer-mcp` patch is distributed under **GPL-3.0** and is not part of the MIT core. If you combine, distribute, or provide a network service using GPL code, you are responsible for assessing GPL obligations.

### 4. Authorized environments only

Use the project only on devices, accounts, servers, networks, and data that you own or are explicitly authorized to use.

You must not:

```text
access unauthorized devices or accounts
bypass authentication, access controls, anti-cheat, or security mechanisms
violate rules or terms on public servers
harass, stalk, threaten, defraud, or damage others
capture another person's screen, keyboard, mouse, files, or credentials
expose the host bridge to the public internet or share it with unauthorized people
use the project for illegal activity
```

**"Technically possible" is not "legally permitted."**

### 5. Host / desktop / input terms

The project may include:

```text
host://desktop
host://fs
host://display
host://input/mouse
host://input/keyboard
```

These are local test facilities, not production remote-administration products.

You agree to:

```text
enable them only on machines you own or are explicitly authorized to control
never bind the bridge to 0.0.0.0 or the public internet
never use a fixed test token as a production secret
never capture screen or input without the knowledge and consent of the person affected
never bypass system permissions on shared or multi-user systems
never use input devices for unauthorized actions
stop the bridge and input immediately when they are not needed
```

Host input is disabled by default. `--enable-input` is an explicit high-risk decision, not a default feature.

### 6. Minecraft / game services

This is not an official Mojang, Microsoft, NetEase, or game-server project.

You agree to:

```text
comply with the Minecraft EULA and server rules
not use automation or anti-cheat evasion on public servers
not use the project to damage other players' experience
accept responsibility for account bans, IP bans, and data loss
not use the project for paid boosting, cheat distribution, or fraud
```

Minecraft is a trademark of Mojang Studios. This project does not use, distribute, or sublicense the Minecraft game, server, or official assets.

### 7. AI / LLM behavior

The project may connect to local or external large language models. You understand that:

```text
model output is probabilistic
models may hallucinate, misunderstand, repeat, or give dangerous advice
models may be affected by prompt injection
model behavior is not the maintainers' intent
```

Leases, policy, fencing, audit, estop, and fact verification reduce risk but are not a security certification. You are responsible for actions, costs, and consequences produced by AI.

### 8. No warranty

To the maximum extent permitted by applicable law, the project is provided **AS IS**, without any express or implied warranty, including but not limited to:

```text
merchantability
fitness for a particular purpose
non-infringement
freedom from defects
uninterrupted operation
freedom from errors
no data loss
no hardware damage
security
compliance
```

Do not use the project for:

```text
medical or life-support systems
industrial control
automotive, aviation, or rail systems
critical infrastructure
unattended control of high-value assets
any scenario where failure could cause personal injury or significant property damage
```

### 9. Limitation of liability

To the maximum extent permitted by applicable law, the authors, contributors, organizers, and maintainers are not liable for any direct, indirect, incidental, special, punitive, or consequential damages, including but not limited to:

```text
data loss
equipment damage
account bans
lost profits
business interruption
third-party claims
legal fees
```

This applies regardless of the legal theory (contract, tort, strict liability, or otherwise) and whether or not the possibility of such damages was disclosed.

Some jurisdictions do not allow certain warranty exclusions or liability limitations. In those jurisdictions, the above applies only to the maximum extent permitted by law and does not exclude non-excludable consumer rights.

### 10. Indemnity

To the maximum extent permitted by applicable law, you agree to indemnify and hold harmless the authors, contributors, and maintainers from third-party claims, damages, liabilities, and expenses (including reasonable attorneys' fees) arising from:

```text
your violation of these Terms or the Acceptable Use Policy
your illegal conduct or infringement of third-party rights
your unauthorized control of devices, accounts, data, or networks
your distribution of a modified version that causes harm
your violation of Minecraft, server, or third-party service terms
```

This indemnity does not apply to a maintainer's own willful misconduct or to liabilities that cannot be limited by law.

### 11. Abuse and termination

The maintainers may, but are not obligated to, take any of the following actions regarding suspected abuse in public distributions, issues, pull requests, links, or services:

```text
request that it stop
remove content
refuse support
suspend or terminate access controlled by the maintainers
report to platforms or law enforcement
```

The maintainers do not promise to monitor all use or to take any particular action on every abuse report.

### 12. Third-party services and links

The project may link to or call third-party websites, models, MCP servers, game services, or software. Those third parties have their own terms and privacy policies. The maintainers are not responsible for third-party content, availability, security, or conduct.

### 13. Privacy

Privacy handling for the website and software is described in [`PRIVACY.md`](PRIVACY.md). If you deploy the project, you are the data controller for your deployment and must provide privacy notices, handle data-subject requests, and comply with local law.

### 14. Export, sanctions, and encryption

The project includes network communication, authentication, encryption-related capabilities, and possible remote device control. You must independently assess export controls, sanctions, encryption import/use rules, and local cybersecurity law. See [`EXPORT.md`](EXPORT.md).

### 15. Changes to these Terms

The maintainers may update these Terms. Continued use after an update constitutes acceptance of the new Terms. Material changes will be noted in the repository or release notes where practical, but individual notice is not promised.

### 16. Severability and no waiver

If a provision is held unenforceable, the remaining provisions remain in effect, and the unenforceable part should be given effect to the maximum extent permitted by law.

Failure to enforce a provision is not a waiver of that provision.

### 17. Entire agreement

These Terms, together with [`DISCLAIMER.md`](../../DISCLAIMER.en.md), [`ACCEPTABLE-USE.md`](ACCEPTABLE-USE.md), [`LICENSE`](../../LICENSE), and [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.en.md), form the basic agreement for use of the project. Third-party licenses control where they conflict with these Terms.

### 18. Governing law and disputes

These Terms do not select an exclusive jurisdiction unless the maintainers specify one in writing. You must comply with the law applicable to you. Dispute resolution should be determined by you and the maintainers within the limits of applicable law; before commercial use or distribution, have counsel add governing law, service, and dispute-resolution terms.

### 19. Contact

General questions: GitHub Issues.  
Security: use the private reporting entry in [`SECURITY.md`](../../SECURITY.en.md).  
Abuse: see [`ABUSE.md`](ABUSE.md).

### 20. Not legal advice

This document is a risk disclosure and draft terms, not legal advice, and does not create an attorney-client relationship. If you need an enforceable contract, privacy policy, export review, or liability limitation, consult qualified counsel.

---


## Acceptable Use Policy

> Source: `LEGAL/en/ACCEPTABLE-USE.md`

**Version:** 2026-10-24  
**Important:** This is a project policy draft, not legal advice. The maintainers may update it without individual notice.

---

### 1. General principle

Use this project only for:

```text
devices, accounts, servers, networks, and data you own or are explicitly authorized to use
lawful research, teaching, testing, and personal automation
activity that complies with the game EULA, server rules, and third-party terms
conduct that respects other people's privacy, property, and physical safety
```

**Technical capability is not authorization.** Being able to open `host://fs` does not mean you may read files on that machine. Being able to open `host://input/keyboard` does not mean you may type on someone else's computer.

### 2. Absolutely prohibited

```text
unauthorized access to, control of, scanning of, or interference with another person's devices, accounts, or network
developing, distributing, or using malware, ransomware, spyware, or keyloggers
stealing credentials, cookies, tokens, private keys, chat logs, screens, or files
bypassing authentication, access controls, anti-cheat, DRM, or security mechanisms
automating in violation of rules on public Minecraft servers or servers you do not control
harassment, stalking, threats, doxxing, discrimination, fraud, or scams
destroying another person's builds, accounts, saves, game experience, or commercial service
exposing the host bridge to the public internet or selling it to unauthorized users
using the project for real-world physical harm, surveillance, or control
violating export controls, sanctions, privacy law, computer-crime law, or local law
```

### 3. Minecraft and game scenarios

Permitted, in an environment you own or are authorized to use:

```text
local single-player
your own LAN server
a test server with the owner's explicit consent
AI/agent protocol research
offline experiments
```

Prohibited:

```text
automation or anti-cheat evasion on public servers such as Hypixel or 2B2T
using headless clients to farm resources, achievements, boosts, or currency
malicious PvP, killing, or destroying other players' builds
bypassing server whitelists, bans, or anti-cheat
packaging automation as a "cheat" for distribution
```

The user bears responsibility for account bans, IP bans, save loss, and server penalties.

### 4. Host / desktop / files / input

Permitted:

```text
on your own isolated test machine
bound to 127.0.0.1
using an allowlisted test directory
demonstrating input devices after explicit consent
stopping the bridge immediately after the demonstration
```

Prohibited:

```text
binding the host bridge to 0.0.0.0, the public internet, or a shared network
enabling mouse or keyboard on another person's computer
capturing screens, recording, or reading files without the user's knowledge
collecting passwords, payment data, identity documents, or private chats
bypassing system permissions on shared or multi-user systems
using a test token as a production secret
running unattended for long periods without a kill switch
```

### 5. AI / agent scenarios

You must:

```text
give the agent the least privilege necessary
use default deny
set rate limits, max_bytes, and max_inflight
retain audit records
configure an estop
require human approval for high-risk actions
never let the agent modify its own safety policy
never let the agent decide whether to leave the allowlist
```

You should not:

```text
give a model a root shell
expose the entire home directory to a model
let a model install or upgrade security components by itself
let a model control real industrial, medical, or transport equipment without supervision
use a prompt as a substitute for a permission system
```

### 6. Abuse reports

See [`ABUSE.md`](ABUSE.md) and [`SECURITY.md`](../../SECURITY.en.md). Do not post tokens, private keys, other people's data, or a complete exploit chain in a public issue.

### 7. Enforcement

The maintainers may, but are not obligated to:

```text
request that abuse stop
remove content or links within maintainer-controlled spaces
refuse support
report to platforms
report to law enforcement
```

The maintainers do not guarantee monitoring of all use and are not a substitute for a third party's responsibility for its own abuse.

### 8. Protection for reporters

Good-faith security research, privacy reports, and abuse reports should not be retaliated against. Test only environments you own or are authorized to test; do not access or disclose other people's data or cause service disruption.

### 9. Not legal advice

This policy is not legal advice and does not replace the law, game EULA, or server rules applicable to you.

---


## Privacy

> Source: `LEGAL/en/PRIVACY.md`

**Version:** 2026-10-24  
**Scope:** the project's static website and local software. It does not cover third-party GitHub, model APIs, or game servers.

---

### 1. Website

The website is a static site hosted on GitHub Pages:

```text
https://www.cyberdyne-bridge.com/
https://www.cyberdyne-bridge.com/legal-en.html
```

The current site:

```text
has no first-party account system
has no first-party comments
has no first-party advertising
has no first-party analytics scripts
has no cookie-consent banner because it does not set non-essential cookies
does not expose a local CBAP service to the web
```

GitHub Pages / GitHub may process access logs, IP addresses, and User-Agent data under its own policies. Read GitHub's privacy statement. The maintainers do not control GitHub's logs.

### 2. Software

CBAP runs locally by default. The maintainers do not collect:

```text
your device files
your screenshots
your keyboard or mouse input
your Minecraft account
your model prompts
your tokens
your audit logs
```

The software may create data on your machine, such as:

```text
/tmp/cbap-*
logs/cbap-audit.jsonl
CBAP OS test files
test screenshots
```

You control this data and are responsible for cleaning, protecting, and backing it up.

### 3. Models and third-party services

If you send prompts, screenshots, file contents, or device state to a third-party model or API:

```text
that third party processes the data under its own terms
the maintainers do not control its retention, training, or cross-border transfers
you must obtain any necessary consent or authorization
do not send secrets, personal data, or other people's data to an unreviewed model
```

### 4. Security reports

Reports submitted through a GitHub Security Advisory are handled through GitHub's mechanisms. Do not submit the following in a public issue:

```text
real tokens or private keys
identity numbers, phone numbers, or email addresses
screenshots of another person's device
unredacted logs
```

### 5. Children and minors

This is not a product for children. Minors must use it with the knowledge and consent of a parent or guardian and must comply with local law and game-service terms.

### 6. Data-subject rights

If you deploy this project and process other people's personal data, you are the controller/processor for that deployment and must independently:

```text
provide a privacy notice
establish a lawful basis
handle access, correction, and deletion requests
assess cross-border transfers where applicable
maintain processing records where applicable
```

The maintainers do not assume these obligations for your deployment.

### 7. Retention

The maintainers do not centrally collect data through this project, so there is no single central retention period. You decide how long local logs and screenshots are retained.

### 8. Third-party links

The site links to GitHub, Mojang/Microsoft, DeepSeek, Qwen, Mindcraft, Voyager, and other third parties. Those sites have their own privacy policies.

### 9. Changes

This notice may be updated. Material changes will be noted in the repository or release notes.

### 10. Contact

For privacy questions, use a repository issue and do not include sensitive personal information. For security issues, use the private channel in [`SECURITY.md`](../../SECURITY.en.md).

### 11. Not legal advice

This notice is a transparency disclosure, not a legal compliance solution for your deployment. Consult counsel or a privacy adviser before commercial use, processing sensitive data, or serving users in regions such as the EU or China.

---


## Abuse Reporting and Handling

> Source: `LEGAL/en/ABUSE.md`

**Version:** 2026-10-24

---

### 1. What counts as abuse

```text
unauthorized control of another person's devices or accounts
using CBAP as a remote-access trojan, backdoor, or spyware
stealing credentials, screens, files, or chat logs
automating in violation of public-server rules
bypassing anti-cheat or access controls
harassment, stalking, threats, or doxxing
distributing cheats or malicious modified versions
exposing the host bridge to the public internet for others to use
impersonating the official project or its maintainers
```

### 2. How to report

Prefer the private channel:

```text
https://github.com/cyberdyne-bridge/cyberdyne-bridge-agent-physical-protocol/security/advisories/new
```

If that entry is unavailable, open an issue **without sensitive details**, titled:

```text
[ABUSE] private channel needed
```

Include:

```text
what happened
which repository, version, or link is involved
whether real devices, accounts, or data are involved
whether there is a risk to personal safety
what outcome you are requesting
what timeline may be made public
```

Do **not** post the following in a public issue:

```text
tokens, private keys, or passwords
identity numbers, phone numbers, or email addresses
screenshots of another person's device
unredacted logs
a complete exploit chain
```

### 3. Emergencies

If there is an immediate risk to life, an ongoing intrusion, extortion, or a child-safety risk:

```text
contact local emergency services or law enforcement first
preserve evidence
then notify the maintainers
```

The maintainers are not an emergency service and cannot guarantee real-time response.

### 4. What the maintainers may do

Within applicable law and platform rules:

```text
request that the abuse stop
remove repository content, links, or releases controlled by the maintainers
refuse support
publish a security notice
report to GitHub or the platform
report to law enforcement
restrict access controlled by the maintainers
```

The maintainers are **not obligated** to monitor all use or to take a particular action on every report.

### 5. Modified versions and distributions

If someone distributes a modified version and abuses it:

```text
the maintainers may publicly clarify that it is unrelated to them
the maintainers may request removal of the official name or logo
the maintainers may address copyright or trademark issues under the LICENSE
the maintainers cannot replace platform or law-enforcement action against a third party
```

### 6. Takedown and copyright complaints

If you believe repository content infringes your copyright, trademark, or privacy:

```text
use GitHub's DMCA, privacy, or trademark process
also send the maintainers a notice without sensitive details
provide proof of ownership, specific URLs, and the requested action
```

The maintainers will respond within reason but do not provide legal advice.

### 7. Good-faith research protection

The maintainers support good-faith security research. Please:

```text
test only environments you own or are authorized to test
do not access, modify, or disclose other people's data
do not cause service disruption
allow reasonable time for a fix
```

### 8. Records

The maintainers may retain records necessary to handle abuse reports for security, legal, and platform-appeal purposes. Do not send unnecessary personal data in a report.

### 9. Not legal advice

This process is not legal advice and does not guarantee any particular outcome.

---


## Incident Response

> Source: `LEGAL/en/INCIDENT-RESPONSE.md`

**Version:** 2026-10-24  
**Applies to:** maintainers, deployers, and owners of systems that have been misused

---

### 1. Stop the bleeding first

If the host bridge, input, or file interface may be abused:

```text
stop the host bridge
stop QEMU / the VM
revoke or rotate tokens
disconnect the network or restrict access to 127.0.0.1
disable --enable-input
remove or isolate suspicious public mappings
preserve logs; do not delete them first
```

### 2. Determine scope

```text
which version or commit
which device_id
whether host://fs, host://display, or host://input is involved
whether real personal data or credentials are involved
whether an unauthorized third party is involved
whether the activity is still ongoing
```

### 3. Preserve evidence

```text
audit JSONL
system logs
network connection records
relevant screenshots and file hashes
timeline
```

Do not post raw logs containing tokens or personal data to a public issue.

### 4. Notification

```text
if this is a project vulnerability: use a private Security Advisory
if your deployment was compromised: notify affected parties under local law and contract
if personal safety is involved: contact emergency services
```

### 5. Remediation

```text
least privilege
default deny
rotate secrets
update dependencies
add audit and alerting
restrict host binding
disable unnecessary devices
```

### 6. Post-incident review

```text
root cause
impact
why detection failed
fix verification
documentation and tests to update
whether a security notice is needed
```

### 7. Do not

```text
delete audit records to hide the incident
continue using a leaked token
blame "the AI decided by itself"
publish exploit details for an unfixed issue
```

### 8. Legal

If you need to notify law enforcement, regulators, or data subjects, follow local law and advice from counsel. This document is not legal advice.

---


## Risk Register

> Source: `LEGAL/en/RISK-REGISTER.md`

**Version:** 2026-10-24  
**Note:** This is an engineering risk register, not legal advice. Adjust severity and likelihood for your deployment.

Scoring:

```text
Severity: L low / M medium / H high / C catastrophic
Likelihood: 1 rare / 2 possible / 3 likely
```

| # | Risk | Severity | Likelihood | Existing controls | Residual risk / next step |
|---|---|---|---|---|---|
| R1 | Host bridge exposed to the internet, becoming a remote-control entry point | C | 1–2 | Loopback by default; Kernel rejects non-loopback; host bridge requires explicit `--allow-public` | The explicit flag can still be misused; add network/host-layer protection |
| R2 | Reuse of a fixed test token | H | 2 | Host bridge generates a random token by default; not written to public status; token file 0600 | CBAP OS examples may still use test values; rotate in production |
| R3 | Input devices used for unauthorized actions | C | 1–2 | Off by default; raw X11 refused by default; portal/isolated input; approvals; estop | Explicit `--allow-unisolated-input` can bypass; add network/host-layer protection |
| R4 | File-interface path escape or symlink | H | 1 | Allowlist; resolve; symlink rejection; 64K limit | TOCTOU and platform differences; keep testing |
| R5 | Screenshot contains sensitive information | H | 2 | Writes only to allowlist; no automatic upload | User may capture passwords or chats; add warning and cleanup guidance |
| R6 | Public Minecraft server violation or ban | H | 3 | Prohibited by documentation; local test only | Cannot be prevented technically; user responsibility |
| R7 | AI hallucination causes wrong action or loss | H | 3 | Lease/policy/estop/facts | Not a security certification; prohibit high-risk use |
| R8 | GPL patch and MIT code distributed together | H | 2 | NOTICE; full GPL text; boundary explanation | Combination/network-service compliance needs counsel |
| R9 | Third-party dependency vulnerability or supply chain | H | 2 | Limited version pinning; tests | Dependabot/secret scanning not enabled; add CI |
| R10 | Personal logs, email, or paths enter the public repository | M | 3 | Identified; not cleaned | Publicity/exposure; owner must decide on redaction/history rewrite |
| R11 | Trademark or official-endorsement confusion | M | 2 | TRADEMARKS; unofficial notice | Screenshots and names may still be misunderstood |
| R12 | Use by minors or vulnerable people | H | 1–2 | 18+ notice | No age verification; need guardian/platform measures |
| R13 | Export, sanctions, or encryption compliance | H | 1 | EXPORT notice | Review for each jurisdiction |
| R14 | Privacy or data-protection law | H | 1–2 | Local by default; no collection | Deployers processing others' data must build compliance |
| R15 | Malicious modified versions or cheat distribution | H | 3 | MIT permits modification; trademark/name policy | Cannot stop third parties; use brand separation |
| R16 | Maintainers asked to answer for third-party abuse | H | 1–2 | Terms/disclaimer/AUP | Enforceability depends on jurisdiction; counsel/insurance |
| R17 | Service interruption or no SLA | M | 3 | AS IS | No support commitment |
| R18 | Hardware or physical damage | H | 1 | No physical control; high-risk use prohibited by documentation | Cannot guarantee |
| R19 | Audit logs contain sensitive information | M | 3 | Local/configurable | Need redaction/retention policy |
| R20 | Changes to model or API terms | M | 2 | Local models preferred | Check third-party terms |

### Priority

```text
P0: R1 R3 R8 R16
P1: R2 R4 R6 R7 R13
P2: R9 R10 R11 R14 R15
```

### Engineering recommendations

```text
host bridge: reject non-loopback by default
remove the fixed default token
input: portal/isolated only by default
add dependency and secret scanning
add race/TOCTOU tests for host fs
add sensitive-information warnings for screenshots
counsel review R8/R13/R16 before release
```

---


## AI Disclosure

> Source: `LEGAL/en/AI-DISCLOSURE.md`

**Version:** 2026-10-24

### 1. Where AI was involved

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

### 2. AI output is not fact

AI may:

```text
invent APIs
get boundary conditions wrong
miss threats
produce unsafe defaults
cite laws or cases that do not exist
```

All security and legal text must be reviewed by humans and, where needed, counsel. The legal files here are engineering drafts, not legal opinions.

### 3. Models and training data

This project does not distribute model weights. If you connect DeepSeek, Qwen, or another model, you must comply with its model license and service terms. Model output may contain third-party content; you are responsible for copyright, privacy, and accuracy.

### 4. Prompt injection

Web pages, chats, files, and MCP tool output read by an agent may contain malicious instructions. Do not treat model output as trusted system instruction. Authorization must be decided by the Kernel/policy, not by a prompt.

### 5. Responsibility

The user bears responsibility for actions, costs, errors, and consequences produced by AI. The maintainers do not guarantee that AI behavior matches your intent, law, or industry standards.

### 6. Disclosure recommendation

If you distribute this project or a modified version, retain this disclosure and state:

```text
which parts were AI-assisted
what human review was performed
which known limitations apply
```

---


## Export, Sanctions, and Encryption

> Source: `LEGAL/en/EXPORT.md`

**Version:** 2026-10-24  
**Important:** This is not legal advice or an export-classification conclusion.

---

### 1. Why this matters

The project includes:

```text
network communication (TCP/TLS/mTLS)
authentication and tokens
remote device control (host bridge)
desktop/input/file access
use of cryptographic libraries
capabilities that could be used for monitoring or automation
```

Different jurisdictions may impose registration, licensing, embargo, or end-user review requirements on:

```text
encryption software
intrusion or monitoring tools
remote-control software
export or re-export
sanctioned regions or parties
end uses (military, intelligence, law enforcement)
```

### 2. You must determine

```text
whether you are in a sanctioned country or region
whether you are on an export-control list
whether the end user or end use is restricted
whether military, intelligence, police, or critical-infrastructure use is involved
whether encryption registration or a license is required
whether local cybersecurity or computer-crime law applies
```

### 3. No guarantees

The maintainers do not represent:

```text
the project's export classification
that it may lawfully be used in every country
that it may be used in every industry
that it may be used for surveillance, law enforcement, or military purposes
```

### 4. Recommendations

```text
consult export counsel before commercial, government, or defense-related use
do not offer downloads or support to sanctioned parties
keep end-user and end-use records where applicable
review the encryption and export terms of dependencies
```

### 5. Not legal advice

This document flags risks only. It is not an export, sanctions, or encryption compliance conclusion.

---


## Counsel Review Checklist

> Source: `LEGAL/en/COUNSEL-CHECKLIST.md`

**Purpose:** An intake checklist for counsel, not legal advice.  
**Project:** Cyberdyne Bridge / CBAP

---

### 1. Entity and operations

```text
who operates the repository and website?
individual, company, or foundation?
where are the servers, domain, and GitHub organization located?
are there employees, contractors, or contributors?
are sponsorships, advertising, or commercial support accepted?
```

### 2. Licensing

```text
does root MIT fit the business model?
is the GPL-3.0 mineflayer-mcp patch compatible with the distribution model?
is GPL code combined with closed-source code?
is a network service offered (possible AGPL/network-service issues)?
are third-party MIT notices complete?
are upstream patch copyright and license notices accurate?
```

### 3. Enforceability of terms

```text
are liability limitations enforceable in the target jurisdiction?
are consumers or minors excluded?
is the indemnity enforceable?
are governing-law and arbitration clauses needed?
are Chinese/English bilingual versions needed?
is a "last updated" and user-consent mechanism needed?
```

### 4. Privacy

```text
does the website collect IP addresses, cookies, or analytics?
how are GitHub Pages logs handled?
does the deployer process personal data?
do PIPL/GDPR/CCPA apply?
are a privacy notice, DPA, or cross-border transfer mechanism needed?
```

### 5. Games and third-party platforms

```text
Minecraft EULA and commercial-use policy
server rules and anti-cheat
Mojang/Microsoft/NetEase trademarks
DeepSeek/Qwen model terms
MCP and upstream project terms
GitHub and Bilibili platform rules
```

### 6. High-risk uses

```text
medical, industrial, transport, or critical infrastructure
surveillance, law enforcement, or military
minors
remote control of another person's device
export and sanctions
```

### 7. Abuse and enforcement

```text
abuse-reporting process
takedown, DMCA, and privacy complaints
law-enforcement request handling
log retention
insurance (cyber/media liability)
```

### 8. Deliverables

```text
reviewed TERMS.md
reviewed PRIVACY.md
reviewed ACCEPTABLE-USE.md
reviewed DISCLAIMER.md
license-compliance opinion
export/sanctions opinion where applicable
```

### 9. Links for counsel

```text
https://github.com/cyberdyne-bridge/cyberdyne-bridge-agent-physical-protocol
https://www.cyberdyne-bridge.com/legal-en.html
```

---


## Legal FAQ

> Source: `LEGAL/en/FAQ.md`

**Not legal advice.** Consult counsel for your specific facts.

### Is this a remote-access trojan?

No. CBAP is a device protocol and reference implementation; the host bridge is a local test facility that should bind only to `127.0.0.1`, with input off by default. Any remote-control capability can be misused, so the project includes an AUP, default deny, and explicit boundaries.

### Can I use it on a public Minecraft server?

It is not recommended and usually violates server rules. The project explicitly prohibits anti-cheat evasion and damaging other players' experience on public servers. Account bans and penalties are the user's responsibility.

### Can I use it commercially?

Original code is MIT-licensed and permits commercial use, but:

```text
third-party GPL patches and dependencies require separate compliance
Minecraft, model, and platform terms still apply
high-risk industries require additional legal and safety review
```

Have counsel review [`TERMS.md`](TERMS.md) and [`COUNSEL-CHECKLIST.md`](COUNSEL-CHECKLIST.md) before commercial use.

### Can I expose the host bridge to the internet?

No. It binds to loopback by default; public exposure turns it into a high-risk remote-control entry point. TLS or a token does not authorize control of another person's device.

### Does the project collect my data?

The maintainers do not centrally collect data through the software. The website is static GitHub Pages with no first-party analytics. GitHub may log access under its own policy. Local logs and screenshots are controlled by you.

### What if my logs contain personal data?

Do not commit them to a public repository. Use `.gitignore`, redaction, and private backups. If already pushed, ordinary deletion does not remove them from history; use a history rewrite or a clean repository.

### Why is there GPL code?

Only the `mineflayer-mcp` compatibility patch is GPL-3.0; it is not part of the MIT core. See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.en.md).

### How do I report a vulnerability or abuse?

Security vulnerability: use a private Security Advisory. Abuse: see [`ABUSE.md`](ABUSE.md). Do not post tokens, private keys, other people's data, or a complete exploit chain in a public issue.

### Do these legal files protect me?

They reduce ambiguity and risk, but **do not replace counsel** and cannot guarantee enforceability in any jurisdiction. Get formal legal review before commercial use, distribution, or offering a service.

---


## Third-Party Notices

> Source: `THIRD_PARTY_NOTICES.en.md`

Cyberdyne Bridge's original Kernel, protocol, drivers, and tests are **MIT**-licensed (see [`LICENSE`](../../LICENSE)). The third-party components, patches, runtime dependencies, and names below are not covered by that MIT grant and are used under their own terms.

**This is not legal advice.** If you distribute a combined product, have counsel review it.

---

### 1. Code and patches

| Component | Upstream | License | Location | Notes |
|---|---|---|---|---|
| Mindcraft headless patch | [mindcraft-bots/mindcraft](https://github.com/mindcraft-bots/mindcraft) | MIT | `agents/mindcraft/adapter/patches/mindcraft-headless.patch` | Lazy-load patch only; Mindcraft remains an external planner |
| Voyager state / spike patches | [MineDojo/Voyager](https://github.com/MineDojo/Voyager) | MIT | `agents/voyager/adapter/patches/*.patch` | Mineflayer bridge only; not Voyager's autonomous Python agent |
| mineflayer-mcp place patch | [swaynos/mineflayer-mcp](https://github.com/swaynos/mineflayer-mcp) | **GPL-3.0** | `agents/mcp-mineflayer/driver/patches/mineflayer-mcp-place.patch` | **Not MIT**; distributed only as a patch for an independent GPL external component |

#### GPL-3.0 boundary

`mineflayer-mcp-place.patch` is a patch against GPL-3.0 upstream source. CBAP's MCP driver calls that server through a **separate stdio JSON-RPC process** and does not import GPL code into the Kernel. The patch itself is distributed under GPL-3.0; see:

```text
agents/mcp-mineflayer/driver/patches/LICENSE
third_party/licenses/mineflayer-mcp-GPL-3.0.txt
```

Do not apply the patch to a closed-source fork and then claim the whole product is MIT.

---

### 2. Runtime dependencies (not vendored)

These packages are installed through npm/pip; their source is not copied into this repository. Preserve their licenses when distributing a binary. Versions are governed by `package.json`, lockfiles, and the actual installation.

| Package | License | Purpose |
|---|---|---|
| [mineflayer](https://github.com/PrismarineJS/mineflayer) | MIT | Headless Minecraft client |
| [mineflayer-pathfinder](https://github.com/PrismarineJS/mineflayer-pathfinder) | MIT | Optional pathfinding |
| [mineflayer-collectblock](https://github.com/PrismarineJS/mineflayer-collectblock) | MIT | Block collection |
| [prismarine-physics](https://github.com/PrismarineJS/prismarine-physics) | MIT | Physics data/rules |
| Minecraft data / prismarine-* transitive dependencies | Their own MIT and other licenses | mineflayer dependency tree |
| Python standard library | PSF-2.0 | Kernel and tools |
| MCP SDK (if installed) | Upstream terms | External MCP ecosystem |

License texts are in:

```text
third_party/licenses/
```

---

### 3. External processes and services

| Name | License / terms | Relationship |
|---|---|---|
| [mineflayer-mcp](https://github.com/swaynos/mineflayer-mcp) | GPL-3.0 | Independent stdio process; not MIT code in this repo |
| [Mindcraft](https://github.com/mindcraft-bots/mindcraft) | MIT | External agent; this repo contains only an adapter/patch |
| [Voyager](https://github.com/MineDojo/Voyager) | MIT | External agent bridge; planner not wired |
| Minecraft Java / Mojang / Microsoft | Proprietary | Game/server not distributed; interoperability only |
| DeepSeek / Qwen models | Their model terms | Model weights not distributed; names/compatibility only |
| xdg-desktop-portal / Wayland / X11 | Their open-source licenses | Local input/screenshot backends; not code from this repo |

#### Media and screenshots

```text
assets/DeepSeek-skin.png
site/assets/deepseek-skin.png
```

This is a community-style Minecraft skin asset, not official Mojang material. Verify its source and permission before redistributing it.

CBAP architecture diagrams, CBAP OS screenshots, and terminal captures were produced by this project. Minecraft imagery and names in screenshots are used only to explain interoperability and do not sublicense game assets.

---

### 4. Names and trademarks

See [`TRADEMARKS.en.md`](../../TRADEMARKS.en.md).

```text
Minecraft is a trademark of Mojang Studios / Microsoft.
This project is not an official Mojang, Microsoft, NetEase, DeepSeek, Qwen,
Mindcraft, Voyager, or mineflayer-mcp project and is not endorsed by them.
```

---

### 5. Original-code license

The MIT text in the root `LICENSE` applies to original CBAP code. Third-party patches, dependencies, and names do not change license because they are referenced here.

If you distribute a modified version of this repository:

```text
keep the root LICENSE
keep THIRD_PARTY_NOTICES.md
keep third_party/licenses/
keep the license next to each patch where applicable
do not remove upstream copyright headers
```

---

### 6. Disclaimer

See [`DISCLAIMER.en.md`](../../DISCLAIMER.en.md) and [`SECURITY.en.md`](../../SECURITY.en.md).

---


## Trademarks

> Source: `TRADEMARKS.en.md`

The following names are used only to describe compatibility, interoperability, or technical origin. Their use does not imply official affiliation, sponsorship, or endorsement.

| Name | Owner / note |
|---|---|
| Minecraft | Mojang Studios / Microsoft |
| Mojang | Mojang Studios |
| Microsoft | Microsoft Corporation |
| NetEase | NetEase, Inc. (China Minecraft operator) |
| DeepSeek | DeepSeek |
| Qwen / Tongyi Qianwen | Alibaba Group / Alibaba Cloud |
| Mindcraft | The Mindcraft project and contributors |
| Voyager / MineDojo | MineDojo Team |
| mineflayer / PrismarineJS | The PrismarineJS project and contributors |
| mineflayer-mcp | swaynos / project contributors |
| MCP / Model Context Protocol | The respective project and contributors |
| Wayland / X11 / xdg-desktop-portal | The respective projects and contributors |
| Debian / XFCE / GRUB | The respective projects and contributors |

### Principles

```text
do not use a third-party logo as this project's logo
do not imply official partnership
do not write "compatible with" as "official"
do not remove upstream copyright or license notices
```

The names **Cyberdyne Bridge / CBAP** are used by this project's maintainers; third parties must not use them to impersonate an official release.

If you believe a name is used improperly, contact the maintainers through a repository issue.

---


## Security Policy

> Source: `SECURITY.en.md`

### Supported versions

Security fixes target:

```text
the main branch
the latest GitHub Release
```

Older versions are not promised ongoing security updates.

### Reporting a vulnerability

**Do not post exploit details, tokens, private keys, personal data, or a complete attack chain in a public issue.**

Prefer GitHub's private vulnerability reporting:

```text
https://github.com/cyberdyne-bridge/cyberdyne-bridge-agent-physical-protocol/security/advisories/new
```

If that entry is unavailable, open an issue **without sensitive details** stating that a private channel is needed; the maintainers will provide follow-up contact.

Please include where possible:

```text
affected version / commit
minimal reproduction
impact
whether local access is required
whether host bridge / input / fs is involved
your preferred public timeline
```

### Scope

Priority areas:

```text
CBAP Kernel authentication, lease, fencing, cancel, estop
policy / approval / audit / token
host bridge network binding and token
host://fs path escape / symlink
host://display screenshot path
host://input default denial and opt-in
MCP sandbox / manifest pin
TLS / mTLS configuration
```

Out of scope:

```text
Minecraft game/server vulnerabilities
third-party upstream projects (report upstream)
user misconfiguration, such as exposing the host bridge publicly
social engineering / physical access
```

### Safe harbor

We support good-faith security research. Please:

```text
test only environments you own or are authorized to test
do not access, modify, or disclose other people's data
do not cause service disruption
allow reasonable time for a fix
```

### Do not submit

```text
real tokens / private keys / cloud keys
identity numbers / phone numbers / email addresses
screenshots of another person's device
unredacted logs
```

### Disclosure

The maintainers will try to coordinate a public timeline after confirmation. This is a personal/community project with no commercial SLA.

See [`DISCLAIMER.en.md`](../../DISCLAIMER.en.md).

---


## Contributing and Contribution License

> Source: `CONTRIBUTING.en.md`

### License of contributions

By submitting a pull request, patch, issue attachment, or other contribution, you agree that:

```text
you have the right to submit it
it is licensed under the project's MIT license
you will retain applicable third-party notices
```

Do not submit code you cannot license under these terms.

### Before opening a PR

```bash
python3 tools/cbap_conformance.py --target fake
python3 tools/test_host_desktop.py
python3 tools/test_host_devices.py
```

For host/device changes, also run the relevant safety tests and describe:

```text
what device/action changed
default permission
safe_state
resource limits
whether input/network/filesystem access is involved
```

### Security and privacy

Never commit:

```text
real tokens or private keys
personal logs or diary content
other people's screenshots or data
absolute local paths
production hostnames/IPs
```

Use fixtures, temporary directories, and redacted logs.

### Third-party code

If you add or modify a patch against an upstream project:

```text
record the upstream URL and license
keep the upstream license text
mark GPL/AGPL patches clearly
do not relicense upstream code as MIT
```

See [`THIRD_PARTY_NOTICES.en.md`](../../THIRD_PARTY_NOTICES.en.md).

### Style

```text
small, reviewable commits
tests for behavior changes
no hidden network calls
fail closed by default
document security boundaries
```

### Code of conduct

Be direct about technical problems, not hostile to people. Harassment, doxxing, and malicious use are not welcome.

---


## License texts

- Original CBAP code and documentation: [`LICENSE`](../../LICENSE) (MIT).
- Third-party texts: [`third_party/licenses/`](../../third_party/licenses/).
- `mineflayer-mcp` patch: GPL-3.0, not MIT. See [`THIRD_PARTY_NOTICES.en.md`](../../THIRD_PARTY_NOTICES.en.md).

## End

**This is not legal advice.** Commercial use, binary distribution, service
operation, processing other people's data, and regulated-industry use require
review by qualified counsel for your entity and jurisdiction.
