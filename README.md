# EA Agent

[![Validate](https://github.com/amcheste/ea-agent/actions/workflows/validate.yml/badge.svg?branch=develop)](https://github.com/amcheste/ea-agent/actions/workflows/validate.yml)
[![Version](https://img.shields.io/github/v/release/amcheste/ea-agent?label=version)](https://github.com/amcheste/ea-agent/releases)
[![License](https://img.shields.io/github/license/amcheste/ea-agent)](LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/amcheste/ea-agent/badge)](https://scorecard.dev/viewer/?uri=github.com/amcheste/ea-agent)

A Claude plugin that turns AI into a personalized virtual executive assistant, built around your Obsidian vault as the central knowledge base.

Install it once, run `/ea-agent:setup`, and your EA learns who you are — your tools, your schedule, your priorities, and your working style. Every skill reads your profile to give you personalized, context-aware assistance that gets smarter over time.

## Skills

| Skill | What it does |
|-------|-------------|
| [Setup](skills/setup/) | Onboards you with a short questionnaire and writes your EA profile to your vault. Run this first, and again when upgrading. |
| [Daily Note](skills/obsidian-daily-note/) | Creates your daily journal with morning planning, today's calendar, carry-forward from yesterday, and an evening reflection section |
| [Quick Capture](skills/quick-capture/) | Zero-friction capture — say what's on your mind and it gets filed in the right place in your vault and task manager |
| [Task Manager](skills/task-manager/) | Manages tasks across Apple Reminders and your vault with Eisenhower matrix prioritization and calendar-aware planning |
| [Inbox Processing](skills/inbox-processing/) | Scans Gmail and Slack for action items and surfaces what actually needs your attention |
| [Meeting Notes](skills/meeting-notes/) | Prep briefs before meetings, structured capture during/after, and action item tracking with people notes |
| [Project Setup](skills/project-setup/) | Creates project notes from a template with goals, milestones, task breakdown, and vault linking |
| [Weekly Review](skills/weekly-review/) | Synthesizes your week from daily notes, previews next week's calendar, and guides you through planning |
| [Vault Context](skills/vault-context/) | Scans your recent vault activity to understand momentum, stuck items, and patterns — feeds every other skill |

## Install

### Prerequisites

- **macOS** — required for Apple Reminders and Calendar integration via AppleScript
- **Obsidian** — [obsidian.md](https://obsidian.md)
- **Claude Code** or **Claude Desktop** with Cowork mode

### 1. Install the plugin

```
/plugin install github:amcheste/ea-agent
```

When prompted, enter the full path to your Obsidian vault (e.g., `/Users/yourname/Documents/Obsidian/MyVault`).

### 2. Run setup

```
/ea-agent:setup
```

This walks you through a short questionnaire (about 5 minutes) and writes an `EA_PROFILE.md` file to your vault. Every skill reads this file to personalize its behavior for you — your folder structure, your task lists, your tools, your working style.

You can re-run `/ea-agent:setup` any time to update your profile, and it will automatically detect and handle plugin upgrades.

### 3. Connect your tools

In Claude's MCP settings, connect the tools you want to use:

| Tool | Required for |
|------|-------------|
| **Control your Mac** (`osascript`) | Apple Reminders and Calendar integration — required for task management |
| **Slack** | Inbox processing, morning briefings, evening check-ins |
| **Gmail** | Inbox processing |
| **Google Calendar** | Supplemental calendar (Apple Calendar is the primary source) |

### 4. Set up scheduled tasks (optional)

For a fully automated EA, set up scheduled tasks in Cowork's Scheduled section:

| Task | Suggested schedule | What it does |
|------|-------------------|--------------|
| Morning Briefing | 8:00 AM daily | Creates daily note, syncs tasks, DMs you a summary on Slack |
| Inbox Processing | 8:30 AM weekdays | Scans Gmail and Slack, adds action items to daily note |
| Slack Capture | 9 AM, 12 PM, 3 PM, 6 PM | Sweeps your Slack self-DMs into your vault inbox |
| Evening Reflection | 8:00 PM daily | DMs you reflection prompts based on your day |
| Weekly Review | 4:00 PM Fridays | Creates weekly review note, DMs you the highlights |

After creating each scheduled task, click "Run now" once to pre-approve tool permissions — otherwise the first automatic run will pause waiting for your approval.

### 5. Test it

Say **"Good morning, let's plan my day"** in Cowork or Claude Code. You should get a daily note in your vault with today's calendar and carry-forward items, tasks synced to your task manager, and a morning briefing DM on Slack (if connected).

## How the EA learns about you

When you run `/ea-agent:setup`, your answers are saved to `EA_PROFILE.md` in your vault root. This file is your EA's memory — it's plain markdown, so you can read and edit it directly.

Over time, the **Vault Context** skill adds observations to your profile as it learns your patterns:

- Which times of day you do your best work
- Which tasks you tend to carry forward or drop
- Which projects are gaining or losing momentum
- How your energy and focus vary across the week

These observations accumulate in an `## EA Observations` section of your profile and make every skill smarter the longer you use it.

## Upgrading

When a new version of ea-agent is released, just run:

```
/ea-agent:setup
```

The setup skill checks your profile version and only asks about new fields — it won't make you repeat the whole onboarding.

## Vault structure

The EA expects (or will help you create) a folder structure like this in your vault:

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

Folder names are configurable — the setup skill asks what you actually use.

## Templates

The `templates/` folder contains Obsidian-compatible markdown templates:

- `daily-note.md` — Morning planning + evening reflection
- `weekly-review.md` — End-of-week check-in with metrics and priorities
- `meeting-notes.md` — Agenda, notes, decisions, and action items
- `project.md` — Project overview with goals, milestones, and tasks

Copy these into your vault's `Templates/` folder.

## Day-to-day usage

- **Morning:** The 8 AM briefing creates your daily note. Review priorities, start working.
- **During the day:** "Remind me to..." or "Note to self..." — filed to your vault and task manager instantly.
- **Stuck or overwhelmed:** "What should I focus on?" — your EA pulls tasks, calendar, and deadlines and gives you a realistic plan.
- **Evening:** The 8 PM check-in prompts your reflection. Fill in the evening section of your daily note.
- **Friday:** The weekly review synthesizes your week and sets you up for the next one.

## Philosophy

Your Obsidian vault is the single source of truth for your work and life. Claude acts as your EA — not just following instructions, but noticing when you're overloaded, carrying forward what slipped, briefing you in the morning, and checking in at the end of the day.

A good EA is proactive, remembers context across days, and gets better the longer they work with you. That's what this plugin is designed to enable.

## CI/CD

Every push to `main` and every pull request runs the validation workflow in `.github/workflows/validate.yml`:

| Job | Runs on | What it checks |
|-----|---------|----------------|
| Validate Plugin Structure | push + PR | Plugin manifest fields, SKILL.md frontmatter, required files, all skills reference EA_PROFILE.md |
| Validate Version Consistency | push + PR | Setup skill references a profile version |
| Run Evals | PR only | Skill routing accuracy (85% threshold) and behavioral quality (75% threshold) using the Claude API |

### Setting up the API key secret

The evals job requires an Anthropic API key to call Claude. Add it as a GitHub Actions secret:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

Without this secret the evals job will fail. The structural validation jobs run without it and will still pass.

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

# Custom pass threshold
python evals/eval_runner.py --pass-threshold 90
```

Each full run costs roughly **$0.08** (routing on Haiku, behavioral agent on Haiku, judge on Sonnet).

## Contributing

Contributions welcome. A few things to keep in mind:

- Skills should work for anyone — no hardcoded personal info (that belongs in `EA_PROFILE.md`)
- Keep the EA tone: conversational, proactive, not robotic
- Run `/ea-agent:setup` logic through the upgrade path when adding new profile fields (bump `profile_version`)

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
