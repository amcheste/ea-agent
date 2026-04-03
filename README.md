<div align="center">

<img src="assets/logo.png" alt="EA Agent mascot" width="200" />

# EA Agent

**A Claude plugin that turns AI into a personalized virtual executive assistant — wired into your Obsidian vault, task manager, calendar, and inbox.**

[![Validate](https://github.com/amcheste/ea-agent/actions/workflows/validate.yml/badge.svg?branch=develop)](https://github.com/amcheste/ea-agent/actions/workflows/validate.yml)
[![Version](https://img.shields.io/github/v/release/amcheste/ea-agent?label=version)](https://github.com/amcheste/ea-agent/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/amcheste/ea-agent/badge)](https://scorecard.dev/viewer/?uri=github.com/amcheste/ea-agent)

</div>

---

Install it once, run `/ea-agent:setup`, and your EA learns who you are — your vault structure, your task lists, your working style, your tools. Every skill reads your profile to give you personalized, context-aware assistance that gets smarter the longer you use it.

```
/plugin install github:amcheste/ea-agent
```

Then run `/ea-agent:setup` to complete onboarding (~5 minutes).

---

## Skills

| Skill | What it does |
|-------|-------------|
| [Setup](skills/setup/) | Short questionnaire that writes your EA profile to your vault. Run this first, and again when upgrading. |
| [Daily Note](skills/obsidian-daily-note/) | Creates your daily journal with morning planning, today's calendar, carry-forward from yesterday, and an evening reflection section |
| [Quick Capture](skills/quick-capture/) | Zero-friction capture — say what's on your mind and it gets filed in the right place in your vault and task manager |
| [Task Manager](skills/task-manager/) | Manages tasks across Apple Reminders and your vault with Eisenhower matrix prioritization and calendar-aware planning |
| [Inbox Processing](skills/inbox-processing/) | Scans Gmail and Slack for action items and surfaces what actually needs your attention |
| [Meeting Notes](skills/meeting-notes/) | Prep briefs before meetings, structured capture during/after, and action item tracking with people notes |
| [Project Setup](skills/project-setup/) | Creates project notes from a template with goals, milestones, task breakdown, and vault linking |
| [Weekly Review](skills/weekly-review/) | Synthesizes your week from daily notes, previews next week's calendar, and guides you through planning |
| [Vault Context](skills/vault-context/) | Scans your recent vault activity to understand momentum, stuck items, and patterns — feeds every other skill |

---

## Install

### Prerequisites

- **macOS** — required for Apple Reminders and Calendar integration via AppleScript
- **Obsidian** — [obsidian.md](https://obsidian.md)
- **Claude Code** with MCP support

### 1. Install the plugin

```
/plugin install github:amcheste/ea-agent
```

When prompted, enter the full path to your Obsidian vault (e.g. `/Users/yourname/Documents/Obsidian/MyVault`).

### 2. Run setup

```
/ea-agent:setup
```

This walks you through a short questionnaire and writes `EA_PROFILE.md` to your vault root. Every skill reads this file to personalise its behavior — your folder structure, your task lists, your tools, your working style.

Re-run `/ea-agent:setup` any time to update your profile. It will automatically detect plugin upgrades and only ask about new fields.

### 3. Connect your tools

In Claude's MCP settings, connect the tools you want:

| Tool | Required for |
|------|-------------|
| **Control your Mac** (`osascript`) | Apple Reminders and Calendar — required for task management |
| **Slack** | Inbox processing, morning briefings, evening check-ins |
| **Gmail** | Inbox processing |
| **Google Calendar** | Supplemental calendar (Apple Calendar is the primary source) |

### 4. Set up scheduled tasks (optional)

For a fully automated EA, set up scheduled tasks in Claude's Scheduled section:

| Task | Suggested schedule | What it does |
|------|-------------------|--------------|
| Morning Briefing | 8:00 AM daily | Creates daily note, syncs tasks, DMs you a summary on Slack |
| Inbox Processing | 8:30 AM weekdays | Scans Gmail and Slack, adds action items to daily note |
| Slack Capture | 9 AM, 12 PM, 3 PM, 6 PM | Sweeps your Slack self-DMs into your vault inbox |
| Evening Reflection | 8:00 PM daily | DMs you reflection prompts based on your day |
| Weekly Review | 4:00 PM Fridays | Creates weekly review note, DMs you the highlights |

After creating each task, click **Run now** once to pre-approve tool permissions — otherwise the first automatic run will pause waiting for your approval.

### 5. Test it

Say **"Good morning, let's plan my day"** in Claude Code. You should get a daily note in your vault with today's calendar and carry-forward items, tasks synced to Apple Reminders, and a morning briefing DM on Slack (if connected).

---

## How the EA learns about you

When you run `/ea-agent:setup`, your answers are saved to `EA_PROFILE.md` in your vault root. This file is your EA's memory — it's plain markdown, so you can read and edit it directly.

Over time, the **Vault Context** skill adds observations to your profile as it learns your patterns:

- Which times of day you do your best work
- Which tasks you tend to carry forward or drop
- Which projects are gaining or losing momentum
- How your energy and focus vary across the week

These accumulate in an `## EA Observations` section of your profile and make every skill smarter the longer you use it.

---

## Vault structure

The EA expects — or will help you create — a folder structure like this:

```
Your Vault/
├── EA_PROFILE.md          ← written by /ea-agent:setup
├── Daily Journal/
├── Weekly Reviews/
├── Meetings/
├── Projects/
│   ├── Work/
│   ├── Personal/
│   └── (your areas)
├── Ideas/
├── People/
└── Templates/
```

Folder names are fully configurable — setup asks what you actually use.

---

## Templates

The `templates/` folder contains Obsidian-compatible markdown templates:

- `daily-note.md` — Morning planning + evening reflection
- `weekly-review.md` — End-of-week check-in with metrics and priorities
- `meeting-notes.md` — Agenda, notes, decisions, and action items
- `project.md` — Project overview with goals, milestones, and tasks

Copy these into your vault's `Templates/` folder.

---

## Day-to-day usage

- **Morning** — The 8 AM briefing creates your daily note. Review priorities, start working.
- **During the day** — "Remind me to..." or "Note to self..." — filed to your vault and task manager instantly.
- **Stuck or overwhelmed** — "What should I focus on?" — your EA pulls tasks, calendar, and deadlines and gives you a realistic plan.
- **Evening** — The 8 PM check-in prompts your reflection. Fill in the evening section of your daily note.
- **Friday** — The weekly review synthesizes your week and sets you up for the next one.

---

## Upgrading

```
/ea-agent:setup
```

The setup skill checks your profile version and only asks about new fields — it won't make you repeat the whole onboarding.

---

## CI/CD Pipeline

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **Validate** | Every PR + push to `main`/`develop` | Plugin structure, skill frontmatter, version consistency, eval quality gate |
| **Release** | `v*.*.*` tags | Validate → evals → publish GitHub Release |
| **SAST** | Every PR + weekly | Semgrep secret scanning |
| **OpenSSF Scorecard** | Push to `main` + weekly | Security posture scoring |
| **Release Drafter** | Push to `develop` | Auto-drafts release notes from PR titles |
| **Monthly Dep Release** | 1st of each month | Opens a patch release PR if Dependabot has merged updates |
| **Stale** | Daily | Closes inactive issues and PRs after 60 + 7 days |

### Validate pipeline (every PR)

```
┌─────────────────────────┐   ┌──────────────────────────┐
│  Validate Structure     │   │  Validate Version        │
│                         │   │                          │
│ • plugin.json fields    │   │ • setup skill references │
│ • SKILL.md frontmatter  │   │   a profile version      │
│ • required files        │   │                          │
│ • EA_PROFILE.md refs    │   └────────────┬─────────────┘
└────────────┬────────────┘                │
             └──────────────┬──────────────┘
                            ▼
             ┌──────────────────────────────┐
             │  Run Evals  (PR only,        │
             │  skipped if no skill/eval    │
             │  files changed)              │
             │                              │
             │ • routing accuracy ≥ 85%     │
             │ • behavioral quality ≥ 75%   │
             └──────────────────────────────┘
```

### Running evals locally

```bash
cd ea-agent
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=your-key-here

# Run everything
python evals/eval_runner.py

# Routing only (fast, ~$0.02)
python evals/eval_runner.py --routing-only

# Behavioral only
python evals/eval_runner.py --behavioral-only

# Custom threshold
python evals/eval_runner.py --pass-threshold 90
```

Each full run costs roughly **$0.08** (routing + behavioral agent on Haiku, judge on Sonnet).

To run evals in CI, add your Anthropic API key as a GitHub Actions secret named `ANTHROPIC_API_KEY`:

> **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

---

## Versioning

Follows [Semantic Versioning](https://semver.org/).

```bash
./scripts/bump-version.sh patch    # 1.2.0 → 1.2.1  (bug fixes)
./scripts/bump-version.sh minor    # 1.2.0 → 1.3.0  (new skills or features)
./scripts/bump-version.sh major    # 1.2.0 → 2.0.0  (breaking profile schema changes)
```

Use `major` when bumping `profile_version` in `skills/setup/SKILL.md` — this signals to existing users that they need to re-run `/ea-agent:setup`.

---

## Philosophy

Your Obsidian vault is the single source of truth for your work and life. Claude acts as your EA — not just following instructions, but noticing when you're overloaded, carrying forward what slipped, briefing you in the morning, and checking in at the end of the day.

A good EA is proactive, remembers context across days, and gets better the longer they work with you. That's what this plugin is built to enable.

---

## Contributing

This is Alan Chester's personal EA configuration. It is open for others to **fork and adapt** for their own use — that is the primary use case for anyone other than the owner.

A few things to keep in mind if contributing:

- Skills must work for anyone — no hardcoded personal info (that belongs in `EA_PROFILE.md`)
- Keep the EA tone: conversational, proactive, not robotic
- When adding new profile fields, bump `profile_version` in the setup skill and handle the upgrade path

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide, development workflow, and release process.

---

## License

Released under the [MIT License](LICENSE).
