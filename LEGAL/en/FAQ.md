# Legal FAQ

**Not legal advice.** Consult counsel for your specific facts.

## Is this a remote-access trojan?

No. CBAP is a device protocol and reference implementation; the host bridge is a local test facility that should bind only to `127.0.0.1`, with input off by default. Any remote-control capability can be misused, so the project includes an AUP, default deny, and explicit boundaries.

## Can I use it on a public Minecraft server?

It is not recommended and usually violates server rules. The project explicitly prohibits anti-cheat evasion and damaging other players' experience on public servers. Account bans and penalties are the user's responsibility.

## Can I use it commercially?

Original code is MIT-licensed and permits commercial use, but:

```text
third-party GPL patches and dependencies require separate compliance
Minecraft, model, and platform terms still apply
high-risk industries require additional legal and safety review
```

Have counsel review [`TERMS.md`](TERMS.md) and [`COUNSEL-CHECKLIST.md`](COUNSEL-CHECKLIST.md) before commercial use.

## Can I expose the host bridge to the internet?

No. It binds to loopback by default; public exposure turns it into a high-risk remote-control entry point. TLS or a token does not authorize control of another person's device.

## Does the project collect my data?

The maintainers do not centrally collect data through the software. The website is static GitHub Pages with no first-party analytics. GitHub may log access under its own policy. Local logs and screenshots are controlled by you.

## What if my logs contain personal data?

Do not commit them to a public repository. Use `.gitignore`, redaction, and private backups. If already pushed, ordinary deletion does not remove them from history; use a history rewrite or a clean repository.

## Why is there GPL code?

Only the `mineflayer-mcp` compatibility patch is GPL-3.0; it is not part of the MIT core. See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.en.md).

## How do I report a vulnerability or abuse?

Security vulnerability: use a private Security Advisory. Abuse: see [`ABUSE.md`](ABUSE.md). Do not post tokens, private keys, other people's data, or a complete exploit chain in a public issue.

## Do these legal files protect me?

They reduce ambiguity and risk, but **do not replace counsel** and cannot guarantee enforceability in any jurisdiction. Get formal legal review before commercial use, distribution, or offering a service.
