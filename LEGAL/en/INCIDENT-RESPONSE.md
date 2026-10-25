# Incident Response

**Version:** 2026-10-24  
**Applies to:** maintainers, deployers, and owners of systems that have been misused

---

## 1. Stop the bleeding first

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

## 2. Determine scope

```text
which version or commit
which device_id
whether host://fs, host://display, or host://input is involved
whether real personal data or credentials are involved
whether an unauthorized third party is involved
whether the activity is still ongoing
```

## 3. Preserve evidence

```text
audit JSONL
system logs
network connection records
relevant screenshots and file hashes
timeline
```

Do not post raw logs containing tokens or personal data to a public issue.

## 4. Notification

```text
if this is a project vulnerability: use a private Security Advisory
if your deployment was compromised: notify affected parties under local law and contract
if personal safety is involved: contact emergency services
```

## 5. Remediation

```text
least privilege
default deny
rotate secrets
update dependencies
add audit and alerting
restrict host binding
disable unnecessary devices
```

## 6. Post-incident review

```text
root cause
impact
why detection failed
fix verification
documentation and tests to update
whether a security notice is needed
```

## 7. Do not

```text
delete audit records to hide the incident
continue using a leaked token
blame "the AI decided by itself"
publish exploit details for an unfixed issue
```

## 8. Legal

If you need to notify law enforcement, regulators, or data subjects, follow local law and advice from counsel. This document is not legal advice.
