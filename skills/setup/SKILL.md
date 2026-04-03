---
name: setup
description: "Set up or upgrade your EA profile. Run this when first installing the ea-agent plugin, when upgrading to a new version, or when you want to update your personal preferences. Trigger on phrases like 'setup my EA', 'configure my assistant', 'update my EA profile', 'onboard', 'first run', 'I just installed the EA agent', 'upgrade my profile', or 'personalize my EA'."
user-invocable: true
---

# EA Agent Setup

You are onboarding a new user to their personal EA agent, or upgrading an existing user to a newer profile version. This is the most important skill in the plugin — a good profile makes every other skill dramatically smarter and more personal.

Be warm, conversational, and efficient. This should feel like meeting a new assistant who's getting to know you, not filling out a form.

## Current Profile Version

The current expected profile version is **1.0**.

## Step 1: Find the Vault

**If `vault_path` is already configured** (from a previous setup or plugin config), skip vault discovery entirely and go straight to Step 2 — do NOT ask the user about their vault location.

If vault_path is not configured, locate it:

1. Search common locations:
   - `~/Documents/` — look for folders containing `.obsidian/`
   - `~/` — same check
   - `/Volumes/` — for external drives
2. If multiple vaults are found, ask the user which one to use
3. If none found, ask the user to provide the full path

## Step 2: Check for Existing Profile

Look for `EA_PROFILE.md` in the vault root (e.e., `{vault_path}/EA_PROFILE.md`).

- **File not found** → Fresh install. Go to Step 3 (Full Onboarding).
- **File found, `profile_version: "1.0"`** → Already up to date. Say: "Your EA profile is already set up and up to date! Want to review or update any of your preferences?" Then let them edit any section they want.
- **File found, older version** → Upgrade mode. Go to Step 4 (Upgrade).

## Step 3: Full Onboarding (Fresh Install)

Introduce yourself briefly:

> "Hi! I'm your EA agent. Before I can be really useful, I need to learn a bit about you and how you work. I'll ask you a few quick questions — this takes about 5 minutes and everything gets saved to your vault so I remember it across sessions. You can update it any time by running `/ea-agent:setup`."

Then ask questions in **four conversational batches** — don't dump everything at once.

---

### Batch 1: About You

Ask together:
- What's your name, and what should I call you?
- What timezone are you in?
- What are your main life areas or roles? (e.g., "I'm a software engineer, grad student, and parent")

Wait for their response before continuing.

---

### Batch 2: Your Vault

You already know the vault path. Ask:
- What do you call your daily notes folder? (default: `Daily Journal`)
- Do you have a folder for weekly reviews? (default: `Weekly Reviews`)
- What project/area folders do you have? (e.g., "Academic, Side Projects, Work, Personal")
- Do you have an Ideas folder? A People folder? A Meetings folder?

If the user isn't sure, suggest sensible defaults and confirm.

---

### Batch 3: Your Tools

Ask together:
- Do you use Apple Reminders for tasks? If so, what lists do you have? (e.g., "Work, Personal, Shopping, Home")
- Which Slack workspaces do you use? (just the names, e.g., "Acme Corp, My Startup")
- Which Gmail accounts should I pay attention to?

---

### Batch 4: Working Style and Priorities

Ask together:
- When are you sharpest / most focused? (morning, afternoon, evening)
- How do you like me to communicate — brief and to the point, or more detailed explanations?
- What are your top 2–3 priorities or active projects right now?

---

After all four batches, say: "Great — let me save your profile now." Then proceed to Step 5.

## Step 4: Upgrade Mode

Read the existing `EA_PROFILE.md`. Identify the current `profile_version`. Then:

- Tell the user what version they're on and what's new
- Only ask about fields that are **new** in the current version (don't re-ask existing questions)
- Preserve all existing profile content

**Version history:**
- `1.0` — Initial profile: identity, vault structure, tools, working style, priorities, EA observations

When upgrading from a version older than 1.0 (shouldn't happen, but handle gracefully), run the full onboarding.

## Step 5: Write EA_PROFILE.md

Write (or overwrite) `EA_PROFILE.md` to the vault root using the template below, filled in with the user's answers. Use sensible defaults for anything they skipped.

```markdown
---
profile_version: "1.0"
last_updated: YYYY-MM-DD
---

# EA Profile

> This file is your EA's memory. Edit it any time to update how your EA understands you.
> Your EA reads this before every interaction to personalize its responses.
> To update it, just edit this file or run `/ea-agent:setup`.

## Identity
- **Name:** [full name]
- **Address as:** [preferred first name or nickname]
- **Timezone:** [e.g., America/New_York]
- **Roles:** [e.g., Software engineer, grad student, parent]

## Vault Structure
- **Vault path:** [full path]
- **Daily notes folder:** [e.g., Daily Journal]
- **Weekly reviews folder:** [e.g., Weekly Reviews]
- **Meetings folder:** [e.g., Meetings]
- **Ideas folder:** [e.g., Ideas]
- **People folder:** [e.g., People]

## Life Areas
> These become sections in your daily note log and top-level project folders.
[List each area as: - Area Name (folder: FolderName/)]

## Apple Reminders Lists
> Format: "List Name" — what it's for and when to route tasks here
[List each Reminders list with routing rules]

## Communication Tools

### Slack
[List Slack workspaces]

### Email
[List Gmail accounts]

## Working Style
- **Peak focus hours:** [e.g., Morning 8–11am]
- **Communication preference:** [e.g., Brief and direct]
- **Deep work approach:** [any preferences or notes]

## Current Priorities
> Update this whenever your focus shifts — your EA uses this to give smarter advice.
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## EA Observations
> Your EA writes here over time as it learns your patterns. You can edit or delete entries.
<!-- EA_OBSERVATIONS_START -->
<!-- EA_OBSERVATIONS_END -->
```

## Step 6: Confirm and Orient

After writing the profile, give the user a quick summary:

> "All set! I've saved your EA profile to `EA_PROFILE.md` in your vault. Here's what I've learned about you:
> [brief 3–4 line summary of key profile facts]
>
> From now on, every skill will read this profile automatically. A few things you can do next:
> - `/ea-agent:obsidian-daily-note` — start your day
> - `/ea-agent:task-manager` — see what's on your plate
> - `/ea-agent:inbox-processing` — catch up on email and Slack
>
> You can always update your profile by editing `EA_PROFILE.md` directly or running `/ea-agent:setup` again."

## Tips

- If the user is in a hurry, let them skip batches: "Want to just get the basics in and fill in the rest later?"
- Never make the user feel bad about how their vault is organized — meet them where they are
- If they don't use Apple Reminders, skip those questions gracefully
- If they don't use Slack, skip those questions
- The goal is a useful profile, not a complete one — something is always better than nothing
