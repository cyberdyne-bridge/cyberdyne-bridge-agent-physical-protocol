# Risk Register

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

## Priority

```text
P0: R1 R3 R8 R16
P1: R2 R4 R6 R7 R13
P2: R9 R10 R11 R14 R15
```

## Engineering recommendations

```text
host bridge: reject non-loopback by default
remove the fixed default token
input: portal/isolated only by default
add dependency and secret scanning
add race/TOCTOU tests for host fs
add sensitive-information warnings for screenshots
counsel review R8/R13/R16 before release
```
