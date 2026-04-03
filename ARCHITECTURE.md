# Architecture

This document explains how ea-agent is structured, how skills work, and how the system is designed to be extended.

---

## Overview

ea-agent is a Claude Code plugin — a collection of skills that run inside a Claude Code session. When invoked, a skill receives the full context of the user's EA profile and uses Claude's language model plus MCP tools to interact with the user's vault, calendar, task manager, and communication tools.

```
┌─────────────────────────────────────────────────────┐
│                   Claude Code                       │
│                                                     │
│   User message → skill router → skill invoked       │
│                                      │              │
│                         ┌────────────▼────────────┐ │
│                         │       SKILL.md          │ │
│                         │  (instructions + rules) │ │
│                         └────────────┬────────────┘ │
│                                      │              │
│                    ┌─────────────────▼────────────┐ │
│                    │         EA_PROFILE.md         │ │
│                    │   (user's vault, preferences, │ │
│                    │    life areas, tools config)  │ │
│                    └─────────┬──────────┬──────────┘ │
│                              │          │            │
│               ┌──────────────▼─┐   ┌───▼──────────┐ │
│               │  Obsidian Vault │   │  MCP Tools   │ │
│               │  (markdown     │   │              │ │
│               │   files)       │   │ • Reminders  │ │
│               └────────────────┘   │ • Calendar   │ │
│                                    │ • Gmail      │ │
│                                    │ • Slack      │ │
│                                    └──────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
ea-agent/
├── .claude-plugin/
│   └── plugin.json            # Plugin manifest — name, version, skills path, user config
├── skills/
│   ├── setup/
│   │   └── SKILL.md           # Onboarding — writes EA_PROFILE.md
│   ├── obsidian-daily-note/
│   │   └── SKILL.md
│   ├── quick-capture/
│   │   └── SKILL.md
│   ├── task-manager/
│   │   └── SKILL.md
│   ├── inbox-processing/
│   │   └── SKILL.md
│   ├── meeting-notes/
│   │   └── SKILL.md
│   ├── project-setup/
│   │   └── SKILL.md
│   ├── weekly-review/
│   │   └── SKILL.md
│   └── vault-context/
│       └── SKILL.md
├── evals/
│   ├── eval_runner.py         # Test harness — routing + behavioral evals
│   ├── requirements.txt
│   └── scenarios/
│       ├── routing.yaml       # Routing accuracy test cases
│       └── behavioral.yaml    # Response quality test cases
├── scripts/
│   └── bump-version.sh        # Version management — updates plugin.json + CHANGELOG
├── templates/                 # Obsidian note templates (copy to vault)
│   ├── daily-note.md
│   ├── weekly-review.md
│   ├── meeting-notes.md
│   └── project.md
└── assets/
    └── logo.png
```

---

## Plugin Manifest

`.claude-plugin/plugin.json` is the entry point Claude Code reads when installing the plugin:

```json
{
  "name": "ea-agent",
  "version": "1.2.0",
  "skills": "./skills/",
  "userConfig": {
    "vault_path": {
      "description": "Full path to your Obsidian vault",
      "sensitive": false
    }
  }
}
```

- **`skills`** — path to the skills directory; Claude Code discovers all subdirectories containing `SKILL.md`
- **`userConfig`** — config keys the user provides at install time; available to all skills at runtime

---

## Skills

Each skill is a directory under `skills/` containing a single `SKILL.md` file.

### SKILL.md structure

```markdown
---
name: skill-name
description: "When to invoke this skill — used by the router"
---

# Skill Title

Instruction prose that Claude follows when this skill is invoked.
```

The `description` field is critical — it's what the router reads to decide which skill matches a user message. Write it as a complete routing specification: include trigger phrases, use cases, and context cues.

### Skill invocation flow

1. User sends a message
2. Claude Code reads all `description` fields and picks the best-matching skill
3. The skill's full `SKILL.md` is loaded as the active instruction set
4. The skill reads `EA_PROFILE.md` from the vault (Step 0 in every skill)
5. The skill uses Claude's tools (Read, Edit, Write, MCP) to act on the user's behalf
6. The skill confirms the action in one or two sentences

### Step 0 pattern

Every skill (except `setup`) begins with a **Step 0** that loads the user's profile:

```markdown
## Step 0: Load User Profile

**If your context already provides profile information, use it directly.**

Otherwise, read `EA_PROFILE.md` from the vault root.
- Use vault path from plugin config (`vault_path`) or search for `.obsidian/`
- If not found: proceed with generic defaults, mention /ea-agent:setup at the end
```

This pattern ensures skills degrade gracefully when no profile exists and use context efficiently in automated/eval environments.

---

## EA_PROFILE.md

`EA_PROFILE.md` is written by the `setup` skill and lives in the vault root. It is the EA's persistent memory about the user — plain markdown, user-editable.

### Schema (v1.0)

```markdown
# EA Profile
profile_version: 1.0

## Identity
name: [user's name]
vault_path: /path/to/vault

## Vault Structure
daily_notes_folder: Daily Journal
weekly_reviews_folder: Weekly Reviews
meetings_folder: Meetings
projects_folder: Projects
ideas_folder: Ideas
people_folder: People

## Life Areas
- [Area 1]
- [Area 2]
- [Area 3]

## Working Style
peak_hours: [morning / afternoon / evening]
work_days: [Mon-Fri]

## Apple Reminders Lists
- Work: professional tasks
- Personal: personal todos
- Home: household
- Groceries: shopping

## Tools
gmail: [account]
slack: [workspace]
google_calendar: [enabled/disabled]

## Current Priorities
- [priority 1]
- [priority 2]

## EA Observations
[written by vault-context skill over time]
```

### Profile versioning

`profile_version` tracks schema changes independently of the plugin version. When a new skill requires a new profile field:

1. Add the field to the setup skill's questionnaire
2. Bump `profile_version` (e.g. `1.0` → `1.1`)
3. Bump the plugin's **major** version — this signals to users they need to re-run `/ea-agent:setup`

The setup skill detects the version mismatch on re-run and only asks about new fields, preserving existing data.

---

## MCP Tool Dependencies

Skills access external systems via MCP tools configured in Claude's settings:

| MCP | Tool calls used | Skills that need it |
|-----|----------------|---------------------|
| **Control your Mac** | `osascript` — AppleScript execution | quick-capture, task-manager, obsidian-daily-note |
| **Gmail** | `gmail_search_messages`, `gmail_read_message` | inbox-processing |
| **Slack** | `slack_read_channel`, `slack_send_message` | inbox-processing, meeting-notes |
| **Google Calendar** | `gcal_list_events` | obsidian-daily-note, weekly-review |

Skills degrade gracefully when a tool is unavailable — they skip that data source rather than failing.

---

## Eval System

The eval system in `evals/` validates two properties on every PR that touches `skills/` or `evals/`:

### Routing evals (`routing.yaml`)

Tests that the skill router selects the correct skill for a given user phrase. Uses `claude-haiku` as the classifier. Pass threshold: **85%**.

```yaml
- phrase: "remind me to call the dentist"
  expected_skill: quick-capture

- phrase: "good morning, let's plan today"
  expected_skill: obsidian-daily-note
```

### Behavioral evals (`behavioral.yaml`)

Tests that a skill's response meets quality criteria for a given scenario. The agent runs on `claude-haiku`, the judge runs on `claude-sonnet`. Pass threshold: **75%**.

```yaml
- name: "daily note briefing is conversational not robotic"
  skill: obsidian-daily-note
  user_message: "Good morning, let's start the day"
  context: >
    EA_PROFILE.md exists. User's name is Jordan. vault_path is ...
  criteria:
    - "Addresses the user by name"
    - "Mentions the two calendar events"
    - "Keeps the briefing to a short paragraph"
```

The eval runner builds a system prompt of:
```
You are an EA agent. [no-tools notice] Context: {context} {skill_content}
```

The `no-tools notice` tells the model it has no filesystem access and the context block is authoritative — this prevents the model from attempting file discovery in the eval environment.

---

## Adding a New Skill

1. Create `skills/my-skill/SKILL.md` with frontmatter:
   ```markdown
   ---
   name: my-skill
   description: "Detailed routing description with trigger phrases..."
   ---
   ```

2. Include **Step 0** (load EA_PROFILE.md)

3. Add at least one routing scenario to `evals/scenarios/routing.yaml`

4. Add at least one behavioral scenario to `evals/scenarios/behavioral.yaml`

5. CI will enforce (1), (2), and (3)/(4) on your PR

---

## Release Process

```
feature branch → PR to develop → CI (validate + evals) → merge
develop → PR to main → CI → merge
git tag v*.*.* → release pipeline (validate + evals + GitHub Release)
```

Version lives in `.claude-plugin/plugin.json`. Use `./scripts/bump-version.sh` to bump — it updates `plugin.json`, stamps `CHANGELOG.md`, commits, and tags locally.

See [RELEASE.md](RELEASE.md) for the full release checklist.
