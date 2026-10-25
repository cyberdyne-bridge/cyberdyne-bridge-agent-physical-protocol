# Terms of Use

**Version:** 2026-10-24  
**Applies to:** Cyberdyne Bridge / CBAP code, documentation, websites, and releases  
**Important:** This is a risk-allocation draft, not legal advice. Have counsel review it before commercial use or distribution.

---

## 1. Acceptance

By cloning, downloading, installing, running, modifying, distributing, or deploying this project, or by accessing its website, you confirm that you have read and agree to these Terms, [`DISCLAIMER.md`](../../DISCLAIMER.en.md), [`ACCEPTABLE-USE.md`](ACCEPTABLE-USE.md), and any applicable third-party licenses.

If you do not agree, do not use the project.

If you use the project on behalf of an organization, you represent that you have authority to accept these Terms for that organization.

## 2. Eligibility

The project is intended for users with the relevant technical ability and legal capacity. If you are under 18, use it only with the knowledge and consent of a parent or guardian, and comply with local rules on minors, online services, and game accounts.

## 3. License scope

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

## 4. Authorized environments only

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

## 5. Host / desktop / input terms

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

## 6. Minecraft / game services

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

## 7. AI / LLM behavior

The project may connect to local or external large language models. You understand that:

```text
model output is probabilistic
models may hallucinate, misunderstand, repeat, or give dangerous advice
models may be affected by prompt injection
model behavior is not the maintainers' intent
```

Leases, policy, fencing, audit, estop, and fact verification reduce risk but are not a security certification. You are responsible for actions, costs, and consequences produced by AI.

## 8. No warranty

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

## 9. Limitation of liability

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

## 10. Indemnity

To the maximum extent permitted by applicable law, you agree to indemnify and hold harmless the authors, contributors, and maintainers from third-party claims, damages, liabilities, and expenses (including reasonable attorneys' fees) arising from:

```text
your violation of these Terms or the Acceptable Use Policy
your illegal conduct or infringement of third-party rights
your unauthorized control of devices, accounts, data, or networks
your distribution of a modified version that causes harm
your violation of Minecraft, server, or third-party service terms
```

This indemnity does not apply to a maintainer's own willful misconduct or to liabilities that cannot be limited by law.

## 11. Abuse and termination

The maintainers may, but are not obligated to, take any of the following actions regarding suspected abuse in public distributions, issues, pull requests, links, or services:

```text
request that it stop
remove content
refuse support
suspend or terminate access controlled by the maintainers
report to platforms or law enforcement
```

The maintainers do not promise to monitor all use or to take any particular action on every abuse report.

## 12. Third-party services and links

The project may link to or call third-party websites, models, MCP servers, game services, or software. Those third parties have their own terms and privacy policies. The maintainers are not responsible for third-party content, availability, security, or conduct.

## 13. Privacy

Privacy handling for the website and software is described in [`PRIVACY.md`](PRIVACY.md). If you deploy the project, you are the data controller for your deployment and must provide privacy notices, handle data-subject requests, and comply with local law.

## 14. Export, sanctions, and encryption

The project includes network communication, authentication, encryption-related capabilities, and possible remote device control. You must independently assess export controls, sanctions, encryption import/use rules, and local cybersecurity law. See [`EXPORT.md`](EXPORT.md).

## 15. Changes to these Terms

The maintainers may update these Terms. Continued use after an update constitutes acceptance of the new Terms. Material changes will be noted in the repository or release notes where practical, but individual notice is not promised.

## 16. Severability and no waiver

If a provision is held unenforceable, the remaining provisions remain in effect, and the unenforceable part should be given effect to the maximum extent permitted by law.

Failure to enforce a provision is not a waiver of that provision.

## 17. Entire agreement

These Terms, together with [`DISCLAIMER.md`](../../DISCLAIMER.en.md), [`ACCEPTABLE-USE.md`](ACCEPTABLE-USE.md), [`LICENSE`](../../LICENSE), and [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.en.md), form the basic agreement for use of the project. Third-party licenses control where they conflict with these Terms.

## 18. Governing law and disputes

These Terms do not select an exclusive jurisdiction unless the maintainers specify one in writing. You must comply with the law applicable to you. Dispute resolution should be determined by you and the maintainers within the limits of applicable law; before commercial use or distribution, have counsel add governing law, service, and dispute-resolution terms.

## 19. Contact

General questions: GitHub Issues.  
Security: use the private reporting entry in [`SECURITY.md`](../../SECURITY.en.md).  
Abuse: see [`ABUSE.md`](ABUSE.md).

## 20. Not legal advice

This document is a risk disclosure and draft terms, not legal advice, and does not create an attorney-client relationship. If you need an enforceable contract, privacy policy, export review, or liability limitation, consult qualified counsel.
