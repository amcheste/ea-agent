# Testing Guide

This document describes every layer of testing for ea-agent — from automated CI to manual end-to-end runs with a real Obsidian vault.

---

## What CI/CD Covers

Every pull request runs three jobs automatically.

### Job 1 — Structural Validation (Ubuntu, ~10 seconds)

| Check | What it catches |
|-------|----------------|
| `plugin.json` fields | Missing `name`, `version`, or `skills` path |
| Tag/version match | Tag `v1.2.0` must match `plugin.json` version `1.2.0` |
| `SKILL.md` frontmatter | Missing `name` or `description` in any skill |
| Required files | `README.md`, `LICENSE`, `.claude-plugin/plugin.json` |
| Profile references | Every skill (except `setup`) must reference `EA_PROFILE.md` |

### Job 2 — Version Consistency (Ubuntu, ~5 seconds)

| Check | What it catches |
|-------|----------------|
| Profile version reference | `skills/setup/SKILL.md` must reference a `profile_version` |

### Job 3 — Evals (Ubuntu, ~90 seconds, PR only, skipped if no skill/eval files changed)

| Check | Threshold | What it catches |
|-------|-----------|----------------|
| Routing accuracy | ≥ 85% | Wrong skill invoked for a given phrase |
| Behavioral quality | ≥ 75% | Skill response fails quality criteria |

**What CI does NOT cover:**
- Real tool calls (Obsidian file writes, Apple Reminders, Gmail, Slack, Calendar)
- The actual Claude Code plugin install flow
- `EA_PROFILE.md` generation via `/ea-agent:setup`
- Cross-skill interactions (e.g. vault-context feeding daily-note)
- Scheduled task automation

These are covered by the manual testing options below.

---

## Running Evals Locally

The fastest way to iterate on skill changes before pushing.

```bash
cd ea-agent
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=your-key-here

# Run everything
python evals/eval_runner.py

# Routing only — fast and cheap (~$0.02)
python evals/eval_runner.py --routing-only

# Behavioral only
python evals/eval_runner.py --behavioral-only

# Single skill (filter by name)
python evals/eval_runner.py --behavioral-only --skill quick-capture

# Custom pass threshold
python evals/eval_runner.py --pass-threshold 90
```

**Cost:** ~$0.08 per full run (routing + behavioral agent on `claude-haiku`, judge on `claude-sonnet`).

### Adding eval scenarios

Routing scenarios go in `evals/scenarios/routing.yaml`:

```yaml
- phrase: "remind me to call the dentist"
  expected_skill: quick-capture
```

Behavioral scenarios go in `evals/scenarios/behavioral.yaml`:

```yaml
- name: "descriptive scenario name"
  skill: skill-name
  user_message: "what the user says"
  context: >
    EA_PROFILE.md exists. vault_path is /Users/test/Vault.
    [any other facts the skill needs]
  criteria:
    - "Observable criterion 1"
    - "Observable criterion 2"
```

**Context tips:**
- Always include `vault_path` and relevant profile fields — the eval runner has no filesystem access and treats the context block as ground truth
- Criteria should be observable from the response text, not dependent on tool execution
- Keep criteria specific — "mentions the standup at 9am" beats "mentions calendar events"

---

## Manual Testing — Real Claude Code Session

The best way to validate the full end-to-end experience.

### Setup

1. Install the plugin from your local clone:
   ```
   /plugin install /path/to/ea-agent
   ```
   Or from GitHub:
   ```
   /plugin install github:amcheste/ea-agent
   ```

2. Run setup:
   ```
   /ea-agent:setup
   ```
   Walk through the questionnaire. Check that `EA_PROFILE.md` is written to your vault root with the correct values.

3. Connect MCP tools in Claude's settings:
   - **Control your Mac** — for Apple Reminders and Calendar
   - **Gmail** — for inbox processing
   - **Slack** — for inbox processing and messaging
   - **Google Calendar** — for supplemental calendar data

### Skill-by-skill test checklist

#### Setup (`/ea-agent:setup`)
- [ ] Asks at least one question before writing any files
- [ ] Writes `EA_PROFILE.md` to vault root
- [ ] Profile contains correct name, vault path, life areas, Reminders lists
- [ ] Re-running detects existing profile and offers to update (not restart)
- [ ] After a version bump, re-running only asks about new fields

#### Daily Note (`/ea-agent:obsidian-daily-note`)
- [ ] Creates `{daily_notes_folder}/MM-DD-YYYY.md`
- [ ] Log sections use your life area names (not hardcoded defaults)
- [ ] Schedule section pulls from Apple Calendar and/or Google Calendar
- [ ] Carry-forward section includes unchecked tasks from yesterday's note
- [ ] Briefing is conversational — one paragraph, addresses you by name
- [ ] Links to yesterday's and tomorrow's notes at the bottom

#### Quick Capture (`/ea-agent:quick-capture`)
- [ ] "Remind me to..." adds a `- [ ]` to today's daily note Inbox
- [ ] Same task also appears in Apple Reminders in the correct list
- [ ] Idea captures go to `Ideas/` folder (or today's inbox with `#idea` for small ones)
- [ ] Person notes go to `People/` (creates or appends)
- [ ] Confirms in one sentence — does not ask clarifying questions for clear requests
- [ ] Works without a profile — falls back to generic Reminders list, skips vault write

#### Task Manager (`/ea-agent:task-manager`)
- [ ] "What should I focus on?" applies Eisenhower matrix to open tasks
- [ ] Accounts for meetings when estimating available time
- [ ] Reads tasks from both Apple Reminders and vault daily notes
- [ ] Flags overdue or deadline-approaching tasks

#### Inbox Processing (`/ea-agent:inbox-processing`)
- [ ] Scans Gmail for unread, starred, and recent messages
- [ ] Scans Slack for mentions and DMs
- [ ] Surfaces action items, not noise
- [ ] Adds action items to today's daily note Inbox
- [ ] Handles no accounts gracefully — suggests `/ea-agent:setup`

#### Meeting Notes (`/ea-agent:meeting-notes`)
- [ ] Pre-meeting: generates a brief with context on attendees and agenda
- [ ] Post-meeting: creates structured note in `Meetings/` with decisions and action items
- [ ] Action items get added to task manager
- [ ] Links to relevant People notes

#### Project Setup (`/ea-agent:project-setup`)
- [ ] Creates note in `Projects/` with correct structure
- [ ] Prompts for goals, milestones, and initial tasks
- [ ] Links to relevant vault notes

#### Weekly Review (`/ea-agent:weekly-review`)
- [ ] Reads all daily notes from the past 7 days
- [ ] Surfaces wins, open loops, and carry-forward tasks
- [ ] Pulls next week's calendar events
- [ ] Saves review note to `Weekly Reviews/`
- [ ] Conversational tone — not a dry report

#### Vault Context (`/ea-agent:vault-context`)
- [ ] Scans recent daily notes for patterns
- [ ] Identifies momentum and stuck items
- [ ] Adds observations to `EA_PROFILE.md` `## EA Observations` section

---

## Upgrade Testing

When bumping `profile_version` in the setup skill:

1. Create a vault with an existing `EA_PROFILE.md` at the old version
2. Install the new plugin version
3. Run `/ea-agent:setup`
4. Verify it detects the version mismatch
5. Verify it only asks about new fields — does not overwrite existing data
6. Verify `profile_version` is updated in `EA_PROFILE.md` after completion

---

## Testing Without a Real Vault

For isolated skill testing without touching your production vault:

1. Create a temporary Obsidian vault:
   ```bash
   mkdir -p /tmp/test-vault/.obsidian
   ```

2. Set `vault_path` to `/tmp/test-vault` when running setup

3. Test freely — delete `/tmp/test-vault` when done

This is especially useful when testing the setup skill's questionnaire flow or vault structure creation.

---

## CI Pass Thresholds

| Suite | Threshold | Typical score |
|-------|-----------|--------------|
| Routing | 85% | ~93% |
| Behavioral | 75% | ~80–90% |

If evals are flaky (same scenario passes/fails across runs), the likely cause is model non-determinism on edge cases. Check whether the scenario's criteria are ambiguous or whether the context is underspecified — both are more reliable fixes than adjusting the threshold.
