# Acceptable Use Policy

**Version:** 2026-10-24  
**Important:** This is a project policy draft, not legal advice. The maintainers may update it without individual notice.

---

## 1. General principle

Use this project only for:

```text
devices, accounts, servers, networks, and data you own or are explicitly authorized to use
lawful research, teaching, testing, and personal automation
activity that complies with the game EULA, server rules, and third-party terms
conduct that respects other people's privacy, property, and physical safety
```

**Technical capability is not authorization.** Being able to open `host://fs` does not mean you may read files on that machine. Being able to open `host://input/keyboard` does not mean you may type on someone else's computer.

## 2. Absolutely prohibited

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

## 3. Minecraft and game scenarios

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

## 4. Host / desktop / files / input

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

## 5. AI / agent scenarios

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

## 6. Abuse reports

See [`ABUSE.md`](ABUSE.md) and [`SECURITY.md`](../../SECURITY.en.md). Do not post tokens, private keys, other people's data, or a complete exploit chain in a public issue.

## 7. Enforcement

The maintainers may, but are not obligated to:

```text
request that abuse stop
remove content or links within maintainer-controlled spaces
refuse support
report to platforms
report to law enforcement
```

The maintainers do not guarantee monitoring of all use and are not a substitute for a third party's responsibility for its own abuse.

## 8. Protection for reporters

Good-faith security research, privacy reports, and abuse reports should not be retaliated against. Test only environments you own or are authorized to test; do not access or disclose other people's data or cause service disruption.

## 9. Not legal advice

This policy is not legal advice and does not replace the law, game EULA, or server rules applicable to you.
