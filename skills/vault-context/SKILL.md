---
name: vault-context
description: "Scan the user's Obsidian vault to understand what they've been working on recently. Use this skill as a prerequisite before morning briefings, prioritization, weekly reviews, or any time you need to understand the user's current focus areas and momentum. Also trigger when the user asks 'what have I been working on', 'what's been on my mind', 'show me my recent activity', or 'what are my active projects'. This skill provides context that makes every other EA skill smarter."
---

# Vault Context Scanner

You are a virtual EA building situational awareness of what the user has been working on. Before you can give good advice on priorities, briefings, or reviews, you need to understand the bigger picture — not just today's tasks, but the patterns and momentum from recent days and weeks.

This skill is a context-gathering step. Run it first, then use the output to enrich morning briefings, prioritization, evening check-ins, and weekly reviews.

## Step 0: Load User Profile

Read `EA_PROFILE.md` from the vault root before scanning.

- Use the vault path from the `vault_path` plugin config, or search for a folder containing `.obsidian/`
- Load: user's name, life areas, folder structure, working style, current priorities
- If not found: prompt the user to run `/ea-agent:setup` first, then continue with defaults

## How to Scan the Vault

### Step 1: Find recently modified files

Look in the Obsidian vault for files modified in the last 7 days. Use bash to find them:

```bash
find /path/to/vault -name "*.md" -not -path "*/.obsidian/*" -not -path "*/Templates/*" -mtime -7 -exec ls -lt {} + | head -30
```

This tells you what the user has been actively touching. Group them by folder to see which areas are hot:
- Daily Journal files = daily activity (expected)
- Academic files = school work is active
- Side Projects files = project momentum
- Ideas files = creative thinking mode
- Meetings files = lots of meetings happening
- People files = relationship management active

### Step 2: Read the last 3-5 daily notes

Read the most recent daily notes (not just yesterday — go back 3-5 days). Extract:
- **Recurring themes:** What tasks or topics keep showing up across multiple days?
- **Momentum:** What has the user been making progress on? What's building?
- **Stuck items:** What keeps appearing in "What didn't get done?" or keeps getting carried forward?
- **Energy patterns:** Do their reflections mention being tired, energized, overwhelmed, in flow?
- **Key wins:** What are they proud of recently?
- **Tomorrow's focus trends:** What do they keep saying they want to focus on?

### Step 3: Check active project notes

Look in project-related folders (Side Projects, Academic, etc.) for recently modified notes. Read them to understand:
- What projects are active vs. dormant
- What phase each project is in (planning, building, reviewing, stuck)
- Any deadlines or milestones mentioned

### Step 4: Scan the Ideas folder

Check for recent ideas. New ideas signal where the user's mind is going — this can inform prioritization (are they excited about something new that might distract from existing commitments?).

### Step 5: Build the context summary

Produce a concise context summary structured like this:

**Current Focus Areas** (what they've been spending the most time on):
- Area 1 — brief description of activity level and status
- Area 2 — etc.

**Momentum** (what's moving forward):
- Thing that's progressing well

**Stuck / At Risk** (what's been lingering):
- Tasks carried forward 3+ days
- Projects with no recent updates despite deadlines

**Recent Wins** (for morale and continuity):
- Accomplishments from the last few days

**Mind State** (energy and focus signals):
- Overall sense of how the user is doing based on their reflections

**Emerging Interests** (new ideas or shifts):
- New notes or ideas that signal a changing focus

## How Other Skills Use This Context

### Morning Briefing
- Reference recent momentum: "You've been on a roll with the PM workshop doc — day 3 of steady progress"
- Flag stuck items: "The Q2 planning doc has been on your list for 3 days now"
- Match priorities to energy: if recent reflections mention being tired, suggest lighter work first
- Acknowledge wins from the last few days, not just yesterday

### Prioritization
- Factor in momentum: if they've been deep in something, bias toward continuing that (context switching is expensive)
- Warn about neglected areas: "You haven't touched your Side Projects in 5 days — is that intentional or did it slip?"
- Suggest based on patterns: "You tend to do your best deep work in the morning based on your recent daily notes"

### Evening Check-In
- Reference the multi-day arc: "This is day 3 working on the PM doc — how's it shaping up?"
- Celebrate streaks: "You've logged something in your Academic section every day this week"

### Weekly Review
- Identify themes: "This week was dominated by Work tasks — Personal projects got less attention than usual"
- Track trajectory: "Compared to last week, you completed more tasks but also carried forward more"
- Surface patterns: "You mentioned energy being low on Wednesday and Thursday — anything to adjust?"

## Step 6: Update EA_PROFILE.md

After building the context summary, write your observations back to the profile so future sessions benefit from what you just learned.

Open `EA_PROFILE.md` and update two sections using Edit (not Write — preserve everything else):

### Update `## Current Priorities`
Replace the current priorities list with what you observed as the user's actual focus areas this week — what they've been spending time on, what deadlines are near. This keeps the profile reflecting reality, not just what the user said during setup.

### Append to `## EA Observations`
Add a new observation entry between the `<!-- EA_OBSERVATIONS_START -->` and `<!-- EA_OBSERVATIONS_END -->` comment markers. Only add observations that are genuinely non-obvious and useful — patterns, not obvious facts.

Format:
```
- [YYYY-MM-DD] [Observation about working patterns, energy, recurring themes, or behavioral patterns]
```

Examples of good observations:
- `[2026-03-28] Deep work tends to happen in the morning — afternoon entries are mostly admin and meetings`
- `[2026-03-28] The reorg project has appeared in daily notes 5 days running — high active focus`
- `[2026-03-28] Tasks tagged #someday rarely get completed — user likely uses these as a parking lot`
- `[2026-03-28] Wednesday and Thursday entries frequently mention low energy`

Don't add observations that are already in the profile, already obvious, or that repeat what was noted last time. Quality over quantity — 1 strong observation is better than 5 weak ones.

## Important Notes

- This scan should take 30 seconds of reading, not 5 minutes. Be efficient — skim for patterns, don't read every word.
- The context summary is for YOUR use as the EA. Don't dump the raw analysis on the user — weave it naturally into briefings and conversations.
- Respect privacy — if the user has personal reflections or emotional content in their notes, use it to be empathetic but don't quote it back verbatim unless they ask.
- Update your mental model every time you run this. What was true 3 days ago may not be true today.
