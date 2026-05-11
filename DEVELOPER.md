# Developer Guide

Everything you need to build, test, and extend the EA Agent plugin.

## How the plugin works

EA Agent is a [Claude Code plugin](https://code.claude.com/docs/en/plugins.md). A collection of skills packaged for easy installation and distribution. There is no server, no compiled code, and no runtime to manage. The "agent" is a set of markdown instruction files (`SKILL.md`) that tell Claude how to behave in specific situations.

When a user installs the plugin and invokes a skill, Claude reads the skill's instructions and executes them using whatever MCP tools and file access it has available in the user's session.

## Repository structure

```
ea-agent/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, userConfig)
├── skills/
│   ├── setup/               # Onboarding + profile management
│   ├── obsidian-daily-note/ # Daily journal
│   ├── quick-capture/       # Zero-friction capture
│   ├── task-manager/        # Apple Reminders + prioritization
│   ├── inbox-processing/    # Gmail + Slack triage
│   ├── meeting-notes/       # Meeting prep and capture
│   ├── project-setup/       # Project note creation
│   ├── weekly-review/       # Weekly planning
│   └── vault-context/       # Vault scanning + profile learning
├── evals/
│   ├── eval_runner.py       # Test runner
│   ├── requirements.txt
│   └── scenarios/
│       ├── routing.yaml     # Skill routing accuracy tests
│       └── behavioral.yaml  # Response quality tests
├── templates/               # Obsidian note templates
├── .github/workflows/
│   ├── validate.yml         # Structural + eval CI
│   └── release.yml          # Tag-triggered release automation
├── CONTRIBUTING.md
├── DEVELOPER.md             # This file
├── RELEASE.md
└── README.md
```

## Local setup

```bash
git clone https://github.com/amcheste/ea-agent.git
cd ea-agent
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

That's it. No build step, no dependencies beyond Python + the Anthropic SDK for running evals.

## Adding a new skill

### 1. Create the skill directory and file

```bash
mkdir skills/your-skill-name
touch skills/your-skill-name/SKILL.md
```

### 2. Write the frontmatter

```markdown
---
name: your-skill-name
description: "One paragraph describing what this skill does and when to invoke it.
  Include specific trigger phrases — Claude uses this description to decide whether
  to auto-invoke the skill. Be specific about edge cases and example phrases."
---
```

The `description` is the most important field. It determines when Claude invokes the skill automatically. Write it from Claude's perspective: "Use this skill when..."

### 3. Write the skill body

Every skill must follow this structure:

```markdown
# Skill Title

One sentence describing what you (Claude) are doing in this skill.

## Step 0: Load User Profile

Read `EA_PROFILE.md` from the vault root.

- Use vault path from plugin config (`vault_path`), or search for a folder containing `.obsidian/`
- Load: [specific fields this skill needs]
- If not found: prompt `/ea-agent:setup`, then continue with the defaults below

## [Your skill sections]

...

## Tips / EA behavior notes

- ...
```

**Step 0 is mandatory** for every skill except `setup`. It makes the skill generic and personalized at the same time. Any user can install it and it adapts to their setup.

### 4. Add routing eval scenarios

In `evals/scenarios/routing.yaml`, add 2–3 phrases that should trigger your skill:

```yaml
- phrase: "Phrase that should trigger your skill"
  expected_skill: your-skill-name

- phrase: "Another natural-language trigger"
  expected_skill: your-skill-name
```

### 5. Add behavioral eval scenarios

In `evals/scenarios/behavioral.yaml`, add at least:
- One scenario testing the **missing profile fallback** (most important)
- One scenario testing the skill's **core behavior** with a profile present

```yaml
- name: "your-skill handles missing profile gracefully"
  skill: your-skill-name
  user_message: "Natural language request"
  context: "No EA_PROFILE.md exists."
  criteria:
    - "Suggests running /ea-agent:setup"
    - "Does not refuse to help"
    - "Uses generic defaults"

- name: "your-skill core behavior"
  skill: your-skill-name
  user_message: "Natural language request"
  context: "EA_PROFILE.md exists with [relevant fields]."
  criteria:
    - "Specific, observable outcome"
    - "Another specific criterion"
```

### 6. Run evals

```bash
python evals/eval_runner.py --pass-threshold 80
```

Fix anything that fails before opening a PR.

## The EA_PROFILE.md schema

`EA_PROFILE.md` lives in the user's vault root and is written/updated by the `setup` skill. It is the EA's long-term memory for that user.

### Current schema (profile_version: 1.0)

```markdown
---
profile_version: "1.0"
last_updated: YYYY-MM-DD
---

# EA Profile

## Identity
- **Name:** [full name]
- **Address as:** [preferred name]
- **Timezone:** [e.g., America/New_York]
- **Roles:** [e.g., Engineer, parent, student]

## Vault Structure
- **Vault path:** [full path]
- **Daily notes folder:** [e.g., Daily Journal]
- **Weekly reviews folder:** [e.g., Weekly Reviews]
- **Meetings folder:** [e.g., Meetings]
- **Ideas folder:** [e.g., Ideas]
- **People folder:** [e.g., People]

## Life Areas
- Area Name (folder: FolderName/)
- ...

## Apple Reminders Lists
- "List Name": routing description
- ...

## Communication Tools
### Slack
- Workspace: [name]
### Email
- Account: [address]

## Working Style
- **Peak focus hours:** [e.g., Morning 8–11am]
- **Communication preference:** [e.g., Brief and direct]
- **Deep work approach:** [notes]

## Current Priorities
1. [Priority]
2. [Priority]
3. [Priority]

## EA Observations
<!-- EA_OBSERVATIONS_START -->
- [YYYY-MM-DD] [Observation written by vault-context]
<!-- EA_OBSERVATIONS_END -->
```

### How skills read the profile

Skills load the profile at the start of every interaction (Step 0). They use profile values in place of hardcoded defaults:

| Skill | Profile fields used |
|-------|-------------------|
| obsidian-daily-note | daily notes folder, life areas |
| task-manager | Reminders lists + routing rules, peak hours |
| quick-capture | Reminders lists + routing rules, folder structure |
| inbox-processing | Gmail accounts, Slack workspaces |
| weekly-review | weekly reviews folder, life areas |
| meeting-notes | meetings folder, people folder |
| project-setup | life areas + folder paths |
| vault-context | all (reads and writes back observations) |

### Updating the profile schema

When adding new profile fields:

1. Add the fields to the profile template in `skills/setup/SKILL.md`
2. Bump `profile_version` (e.g., `"1.0"` → `"1.1"`)
3. Update the **Upgrade Mode** section in the setup skill to describe what's new in the new version and which questions to ask existing users
4. Update the schema table above in this file
5. Add behavioral evals that confirm the new fields are correctly used
6. Bump `version` in `.claude-plugin/plugin.json` (at minimum a minor bump)

**Important:** `profile_version` and plugin `version` are independent:
- `profile_version` only changes when `EA_PROFILE.md`'s schema changes
- Plugin `version` changes with every release

## Writing evals

### Routing evals (`evals/scenarios/routing.yaml`)

Test that a user phrase triggers the right skill. The eval runner loads all skill descriptions and asks Claude to classify the phrase. This tests whether descriptions are clear and distinct enough.

Good routing scenarios:
- Use natural, conversational language (how a real user would phrase it)
- Cover multiple phrasings per skill (3 is a good target)
- Include edge cases where two skills might be ambiguous

### Behavioral evals (`evals/scenarios/behavioral.yaml`)

Test response quality using a judge LLM. The runner sends the scenario to Claude with the skill content as a system prompt, then asks Sonnet to evaluate the response against your criteria.

Good criteria:
- **Specific and observable**. Can be verified by reading the response text
- **One thing each**. Don't combine multiple checks into one criterion
- **Failure-informative**. If Claude fails this criterion, it tells you something meaningful

Bad criteria (too vague):
- ❌ "The response is helpful"
- ❌ "The EA sounds natural"

Good criteria (specific):
- ✅ "Mentions running /ea-agent:setup when profile is missing"
- ✅ "Does not reference NCSU, CAM, or any hardcoded organization name"
- ✅ "Confirms the capture in one sentence, not multiple paragraphs"

### Running evals locally

```bash
# Full suite
python evals/eval_runner.py

# Just routing (fast, ~$0.02)
python evals/eval_runner.py --routing-only

# Just behavioral
python evals/eval_runner.py --behavioral-only

# Stricter threshold
python evals/eval_runner.py --pass-threshold 90
```

## CI pipeline

| Workflow | Trigger | Jobs |
|----------|---------|------|
| `validate.yml` | push + PR to main | Structure, frontmatter, profile references, version consistency |
| `validate.yml` | PR to main (evals job) | Routing evals (85%), behavioral evals (75%) |
| `release.yml` | push of `v*.*.*` tag | Full validation + evals, then creates GitHub Release |

The evals job requires `ANTHROPIC_API_KEY` to be set as a GitHub Actions secret.
