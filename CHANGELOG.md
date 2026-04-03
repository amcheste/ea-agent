# Changelog

All notable changes to ea-agent are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.3.0] — 2026-04-03

---

## [1.2.0] — 2026-04-03

---

## [1.1.0] — 2026-04-03

### Added
- Profile versioning in setup skill to track schema changes across releases
- Version consistency validation in CI (plugin.json ↔ setup skill)

### Changed
- Release workflow now detects profile schema changes and surfaces upgrade
  notice in release notes

---

## [1.0.0] — Initial Release

### Added
- `setup` — interactive EA profile builder (vault path, preferences, integrations)
- `daily-note` — create or open today's daily note in Obsidian
- `inbox-triage` — process inbox items into tasks, notes, and actions
- `weekly-review` — structured weekly reflection and planning
- `meeting-notes` — capture and organise meeting notes
- `quick-capture` — fast capture for ideas, tasks, and links
- `task-manager` — view, add, and complete Apple Reminders tasks
- Eval harness with routing and behavioural checks
- GitHub Actions CI (validate plugin structure, validate version, run evals on PRs)
