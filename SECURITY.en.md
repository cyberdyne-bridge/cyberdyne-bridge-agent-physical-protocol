# Security Policy

## Supported versions

Security fixes target:

```text
the main branch
the latest GitHub Release
```

Older versions are not promised ongoing security updates.

## Reporting a vulnerability

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

## Scope

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

## Safe harbor

We support good-faith security research. Please:

```text
test only environments you own or are authorized to test
do not access, modify, or disclose other people's data
do not cause service disruption
allow reasonable time for a fix
```

## Do not submit

```text
real tokens / private keys / cloud keys
identity numbers / phone numbers / email addresses
screenshots of another person's device
unredacted logs
```

## Disclosure

The maintainers will try to coordinate a public timeline after confirmation. This is a personal/community project with no commercial SLA.

See [`DISCLAIMER.en.md`](DISCLAIMER.en.md).
