# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |
| Older   | ❌        |

Only the latest release receives security fixes.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Report privately via [GitHub Security Advisories](https://github.com/amcheste/ea-agent/security/advisories/new).

Include as much detail as possible:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### What to expect

| Milestone | Timeline |
|-----------|----------|
| Acknowledgement | Within 7 days |
| Status update | Within 14 days |
| Fix / advisory | Within 30 days |

## Scope

**In scope:**
- Skill logic that could expose sensitive user data (vault content, credentials, personal notes)
- Prompt injection vulnerabilities in skill instructions
- Secrets leakage through eval harness or templates

**Out of scope:**
- Issues in Claude itself or the Anthropic API
- Issues in Obsidian or Apple Reminders (report to those projects)
- Social engineering

## Disclosure Policy

We follow coordinated disclosure. Once a fix is released, we'll publish a security advisory crediting the reporter (unless anonymity is preferred).
