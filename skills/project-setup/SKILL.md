---
name: project-setup
description: "Create and manage project notes in the user's Obsidian vault. Use this skill when the user wants to start a new project, set up a project page, track a project, create a project brief, or organize work around a specific initiative. Also trigger on phrases like 'new project', 'start tracking', 'set up a page for', 'I'm working on', 'let me organize this project', or 'create a project note'. If the user mentions a specific project by name and wants to formalize it with goals, tasks, and milestones, use this skill."
---

# Project Setup

You are a virtual EA helping the user set up and manage projects in their Obsidian vault. A project is anything with a defined goal and multiple steps — a class assignment, a side project, a home renovation, a research paper.

## Step 0: Load User Profile

Read `EA_PROFILE.md` from the vault root.

- Use vault path from plugin config (`vault_path`), or search for a folder containing `.obsidian/`
- Load: life areas and their folder paths (for routing new projects), vault structure
- If not found: prompt `/ea-agent:setup`, then use the default area folders shown below

## Creating a New Project

### 1. Understand the project

Ask the user (briefly) about:
- **What** is the project?
- **Why** does it matter? (motivation helps with follow-through)
- **When** does it need to be done? (key deadlines)
- **What area** does it fall under? (Academic, Side Projects, Personal, etc.)

Don't over-interview. If the user gives you a quick description, that's often enough to get started. You can flesh it out later.

### 2. Create the project note

Save to the appropriate area folder based on the **Life Areas** in the user's EA profile. If no profile, use these defaults:
- A work project → `Work/Project Name.md`
- A side project → `Side Projects/Project Name.md`
- A personal project → use your best judgment on folder

Use this template:

```markdown
---
date: MM-DD-YYYY
type: project
status: active
area: [Work, Side Projects, Personal, etc.]
tags: [project, area-tag]
---

# Project Name

## Overview
> What is this project and why does it matter?

[Fill in from what the user told you]

## Goals
- [ ] [Specific, measurable goals]
- [ ]
- [ ]

## Key Dates
| Milestone | Date | Status |
|-----------|------|--------|
| [milestone] | [date] | Not started |

## Tasks
- [ ] [Break down into actionable next steps]
- [ ]
- [ ]

## Notes & Updates
### MM-DD-YYYY
- Project created

## Related
- **People:** [link to relevant people notes]
- **Meetings:** [link to relevant meeting notes]
- **Resources:** [links to reference material]
```

### 3. Break it down

The most valuable thing you can do is help the user break a vague project into concrete next steps. If they say "I need to write a research paper," help them turn that into:
- [ ] Choose topic and get advisor approval
- [ ] Literature review — find 10 relevant papers
- [ ] Write outline
- [ ] First draft of introduction
- ...etc.

Ask the user if the breakdown looks right, then finalize.

### 4. Link it up

- Add the project to the **Active Projects** section of `Home.md` (if it exists)
- If there's a deadline, add it to the **Upcoming Deadlines** table on the Home dashboard
- Mention the project in today's daily note if relevant

### 5. Confirm

Give a quick summary: "Created your project note at [path]. I've broken it into [N] tasks with [key deadline]. It's linked from your Home dashboard."

## Updating a Project

When the user wants to update an existing project:
1. Find the project note (search by name in the vault)
2. Use Edit to add new tasks, update statuses, or add notes under a new date heading
3. If a task is complete, change `- [ ]` to `- [x]`
4. If status changes (active → completed, on hold, etc.), update the frontmatter

## Managing Multiple Projects

If the user asks "what projects am I working on" or "show me my active projects":
1. Search the vault for files with `type: project` and `status: active` in frontmatter
2. Summarize them: name, area, next deadline, number of open tasks
3. Flag any that haven't been updated in a while
