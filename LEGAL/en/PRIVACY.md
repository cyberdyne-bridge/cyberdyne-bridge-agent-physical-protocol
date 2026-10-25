# Privacy

**Version:** 2026-10-24  
**Scope:** the project's static website and local software. It does not cover third-party GitHub, model APIs, or game servers.

---

## 1. Website

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

## 2. Software

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

## 3. Models and third-party services

If you send prompts, screenshots, file contents, or device state to a third-party model or API:

```text
that third party processes the data under its own terms
the maintainers do not control its retention, training, or cross-border transfers
you must obtain any necessary consent or authorization
do not send secrets, personal data, or other people's data to an unreviewed model
```

## 4. Security reports

Reports submitted through a GitHub Security Advisory are handled through GitHub's mechanisms. Do not submit the following in a public issue:

```text
real tokens or private keys
identity numbers, phone numbers, or email addresses
screenshots of another person's device
unredacted logs
```

## 5. Children and minors

This is not a product for children. Minors must use it with the knowledge and consent of a parent or guardian and must comply with local law and game-service terms.

## 6. Data-subject rights

If you deploy this project and process other people's personal data, you are the controller/processor for that deployment and must independently:

```text
provide a privacy notice
establish a lawful basis
handle access, correction, and deletion requests
assess cross-border transfers where applicable
maintain processing records where applicable
```

The maintainers do not assume these obligations for your deployment.

## 7. Retention

The maintainers do not centrally collect data through this project, so there is no single central retention period. You decide how long local logs and screenshots are retained.

## 8. Third-party links

The site links to GitHub, Mojang/Microsoft, DeepSeek, Qwen, Mindcraft, Voyager, and other third parties. Those sites have their own privacy policies.

## 9. Changes

This notice may be updated. Material changes will be noted in the repository or release notes.

## 10. Contact

For privacy questions, use a repository issue and do not include sensitive personal information. For security issues, use the private channel in [`SECURITY.md`](../../SECURITY.en.md).

## 11. Not legal advice

This notice is a transparency disclosure, not a legal compliance solution for your deployment. Consult counsel or a privacy adviser before commercial use, processing sensitive data, or serving users in regions such as the EU or China.
