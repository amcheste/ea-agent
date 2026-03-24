# EA Skills

A collection of Claude skills that turn AI into a virtual executive assistant (EA), built around an Obsidian vault as the central knowledge base.

These skills are designed for use with [Claude](https://claude.ai) in Cowork mode or Claude Code. They teach Claude how to manage your daily workflow — planning your mornings, capturing action items, running weekly reviews, and keeping everything organized in your Obsidian vault.

## What's Included

### Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [Daily Note](skills/obsidian-daily-note/) | Creates and manages daily journal notes with morning planning, calendar integration, carry-forward from yesterday, and evening reflection | Done |
| [Quick Capture](skills/quick-capture/) | Zero-friction note capture — just say what's on your mind and it gets filed in the right place | Done |
| [Weekly Review](skills/weekly-review/) | Generates weekly review notes, summarizes daily notes, previews next week's calendar | Done |
| [Inbox Processing](skills/inbox-processing/) | Scans Gmail and Slack for action items, surfaces them in your daily note | Done |
| [Project Setup](skills/project-setup/) | Creates project notes from templates with proper linking and task breakdown | Done |
| [Meeting Notes](skills/meeting-notes/) | Creates meeting notes with prep mode, capture mode, and action item tracking | Done |
| [Task Manager](skills/task-manager/) | Apple Reminders + Apple Calendar integration with Eisenhower matrix prioritization, synced to vault | Done |

### Templates

Obsidian-compatible markdown templates in the `templates/` folder:

- **daily-note.md** — Morning planning + evening reflection
- **weekly-review.md** — End-of-week check-in with metrics and priorities
- **meeting-notes.md** — Agenda, notes, decisions, and action items
- **project.md** — Project overview with goals, milestones, and tasks

## Fresh Install / Disaster Recovery

If you're setting this up on a new machine or recovering from scratch, follow these steps in order.

### Prerequisites

- **macOS** (required for Apple Reminders and Calendar integration via AppleScript)
- **Obsidian** — [download here](https://obsidian.md)
- **Claude Desktop App** with Cowork mode enabled, OR **Claude Code** CLI
- **Slack** (optional) — for morning briefings, evening check-ins, and Slack capture
- **Gmail / Google Calendar MCP connectors** (optional) — for email inbox processing and supplemental calendar

### Step 1: Clone this repo

```bash
git clone https://github.com/amcheste/ea-skills.git ~/ea-skills
```

### Step 2: Set up your Obsidian vault

Create a new vault (or use an existing one) and set up the folder structure:

```
Your Vault/
├── Daily Journal/
├── Weekly Reviews/
├── Meetings/
├── Ideas/
├── People/
├── Templates/
├── Resources/
├── Archive/
└── Home.md
```

Copy the templates from `~/ea-skills/templates/` into your vault's `Templates/` folder.

### Step 3: Install the skills

**For Claude Code:**
Copy the skills into your Claude Code skills directory:
```bash
cp -r ~/ea-skills/skills/* ~/.claude/skills/
```

**For Cowork mode:**
When starting a Cowork session, mount your Obsidian vault folder AND the `~/ea-skills/skills/` folder so Claude can access both.

### Step 4: Customize for your setup

Edit the following files to match your personal setup:

**Reminders lists** — in `skills/task-manager/SKILL.md`, update the list routing section to match your Apple Reminders list names. The defaults are:
- **To Do** — general tasks
- **NCSU** — academic work (change to your school/org)
- **CAM** — work tasks (change to your company)
- **House** — home projects
- **Family** — family tasks
- **Groceries** — shopping

**Daily note log categories** — in `skills/obsidian-daily-note/SKILL.md` and `templates/daily-note.md`, update the Log section categories. The defaults are Academic, Side Projects, Personal. Change to whatever areas of your life you want to track.

### Step 5: Set up Apple integrations

**Apple Calendar:** Add all your calendar accounts (work, personal, iCloud) in System Settings → Internet Accounts. The skills read from the macOS Calendar app directly, so any account you add there is automatically available.

**Apple Reminders:** Create the Reminders lists that match your routing config from Step 4. The skills will also auto-create lists if they don't exist.

### Step 6: Connect MCP tools

In the Claude Desktop App, connect these MCP tools as needed:

- **Control_your_Mac osascript** — required for Apple Reminders and Calendar integration
- **Slack** — required for morning briefings, evening check-ins, and Slack capture
- **Gmail** — required for inbox processing skill
- **Google Calendar** — optional supplement to Apple Calendar

### Step 7: Set up scheduled tasks

Scheduled tasks run automatically on your Mac. Set these up in Cowork's Scheduled section (sidebar → Scheduled → create new):

| Task | Schedule | What it does |
|------|----------|--------------|
| Morning Briefing | 8:00 AM daily | Creates daily note, syncs to Apple Reminders, Slack DMs you a summary |
| Inbox Processing | 8:30 AM weekdays | Scans Gmail + Slack for action items, adds to daily note |
| Slack-to-Obsidian Capture | 9 AM, 12 PM, 3 PM, 6 PM daily | Sweeps your Slack self-DMs into daily note Inbox |
| Evening Reflection | 8:00 PM daily | Slack DMs you reflection questions based on your day |
| Weekly Review Kickoff | 4:00 PM Fridays | Creates weekly review note from daily notes, Slack DMs summary |

**Important:** After creating each scheduled task, click "Run now" once to pre-approve the tool permissions. Otherwise the first automatic run will pause waiting for approval.

### Step 8: Test it

Say "Good morning, let's plan my day" in Cowork or Claude Code. You should get a daily note created in your vault with calendar events and carry-forward items, tasks synced to Apple Reminders, and (if Slack is connected) a morning briefing DM.

## Day-to-Day Usage

Once set up, here's how to use the system:

- **Morning:** The 8 AM briefing creates your daily note and Slack DMs you. Open Obsidian, review priorities, start working.
- **During the day:** Quick capture thoughts by telling Claude "remind me to..." or "note to self..." — it files to your vault + Reminders. Or DM yourself on Slack and the sweep task picks it up.
- **Prioritization:** Ask Claude "what should I focus on?" or "help me prioritize" — it pulls your tasks, calendar, and deadlines and gives you a realistic plan.
- **Evening:** The 8 PM check-in Slack DMs you reflection questions. Fill in your daily note's evening section.
- **Friday:** The 4 PM weekly review creates a summary note and Slack DMs you the highlights.

## Customization

### Log Categories
The daily note template comes with Academic, Side Projects, and Personal. Customize these to match your life:
- Client Work, Internal, Learning
- Day Job, Creative, Family
- Work, Health, Relationships

Edit both the template and the daily note skill's SKILL.md.

### Reminders Lists
Update the routing in `skills/task-manager/SKILL.md` to match your Apple Reminders list names.

### Scheduled Task Timing
Adjust the cron schedules to match your routine. Night owl? Move the morning briefing to 10 AM. Early bird? Set it to 6 AM.

## Philosophy

The idea is simple: your Obsidian vault is the single source of truth for your life, and Claude acts as your EA — helping you stay on top of things without you having to maintain the system yourself.

A good EA doesn't just follow instructions. They notice when you're overloaded and suggest prioritization. They carry forward what you forgot. They brief you in the morning and check in at the end of the day. These skills are designed to enable that kind of proactive, human-feeling assistance.

## Contributing

If you build additional EA skills or improve the existing ones, contributions are welcome. The main things to keep in mind:

- Skills should be generic enough to work for anyone (no hardcoded personal info)
- Templates should use Obsidian's `{{date}}` syntax for compatibility
- Keep the EA tone — conversational, proactive, not robotic

## License

MIT
