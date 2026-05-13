# Changelog

All notable changes to ea-agent are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.4.0] — 2026-05-12

### Added
- Brand banner under `assets/` (svg + 1200/2400 png) per [`banner-spec.md`](https://github.com/amcheste/alanchester-brand/blob/main/docs/banner-spec.md). Hero: rendered morning-brief daily note with three priority `→` arrows in Hunter Green as the δ — the EA's synthesized "what matters today" output. README mascot replaced by the banner; `assets/logo.png` preserved.

### Changed
- Brand-aligned README badges (license in Hunter Green `#1F4D3A`, version in Ink `#0B0B0C`).
- Release Drafter workflow bumped to v7.3.0.

### Dependencies
- Dependabot bumps: `github/codeql-action` (3.35.1 → 4.35.4), `actions/labeler` (6.0.1 → 6.1.0), `actions/setup-python`, `release-drafter` (7.1.1 → 7.3.0), `anthropic` (≥0.40.0 → ≥0.101.0 in /evals), `pyyaml` (≥6.0 → ≥6.0.3 in /evals).

---

## [1.3.5]. 2026-04-03

---

## [1.3.4]. 2026-04-03

---

## [1.3.3]. 2026-04-03

---

## [1.3.2]. 2026-04-03

---

## [1.3.1]. 2026-04-03

---

## [1.3.0]. 2026-04-03

---

## [1.2.0]. 2026-04-03

---

## [1.1.0]. 2026-04-03

### Added
- Profile versioning in setup skill to track schema changes across releases
- Version consistency validation in CI (plugin.json ↔ setup skill)

### Changed
- Release workflow now detects profile schema changes and surfaces upgrade
  notice in release notes

---

## [1.0.0]. Initial Release

### Added
- `setup`. Interactive EA profile builder (vault path, preferences, integrations)
- `daily-note`. Create or open today's daily note in Obsidian
- `inbox-triage`. Process inbox items into tasks, notes, and actions
- `weekly-review`. Structured weekly reflection and planning
- `meeting-notes`. Capture and organise meeting notes
- `quick-capture`. Fast capture for ideas, tasks, and links
- `task-manager`. View, add, and complete Apple Reminders tasks
- Eval harness with routing and behavioural checks
- GitHub Actions CI (validate plugin structure, validate version, run evals on PRs)
