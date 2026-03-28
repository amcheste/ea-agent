# Contributing to EA Agent

Thanks for wanting to improve the EA Agent. Contributions are welcome — whether that's a new skill, an improvement to an existing one, new eval scenarios, or a bug fix.

## What we're looking for

- **New skills** — workflows that would benefit any user (not personal/org-specific)
- **Skill improvements** — better instructions, clearer fallbacks, smarter EA behavior
- **Eval scenarios** — more coverage for edge cases and regression protection
- **Profile schema additions** — new fields that make skills smarter (requires `profile_version` bump)
- **Bug fixes** — incorrect behavior, broken fallbacks, hardcoded personal info that slipped in

## Getting started

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ea-agent.git
cd ea-agent
```

See [DEVELOPER.md](DEVELOPER.md) for the full local development setup.

## Before you submit

1. **Run the structural validation** — make sure your skill is well-formed:
   ```bash
   python3 -c "
   import os, re, sys
   for d in sorted(os.listdir('skills')):
       f = f'skills/{d}/SKILL.md'
       if not os.path.exists(f): continue
       c = open(f).read()
       assert c.startswith('---'), f'{d}: missing frontmatter'
       assert 'description:' in c.split('---')[1], f'{d}: missing description'
       if d != 'setup': assert 'EA_PROFILE.md' in c, f'{d}: missing profile load'
   print('All skills valid')
   "
   ```

2. **Run evals** — evals must meet the pass threshold before merging:
   ```bash
   export ANTHROPIC_API_KEY=your-key
   python evals/eval_runner.py --pass-threshold 80
   ```

3. **Add eval scenarios** for any new skill or changed behavior — see [DEVELOPER.md](DEVELOPER.md#writing-evals).

## Skill writing standards

These keep the plugin coherent as it grows.

### Every skill must:
- Start with a `## Step 0: Load User Profile` section that reads `EA_PROFILE.md`
- Include a graceful fallback if no profile exists (suggest `/ea-agent:setup`, then continue with sensible defaults)
- Be generic — no hardcoded names, organizations, folder paths, or Reminders list names that belong in a user's profile
- Have a `description:` in frontmatter that clearly describes when to invoke it, including example trigger phrases

### EA tone guidelines:
- **Conversational, not robotic** — write skill instructions as you'd brief a human assistant
- **Proactive** — skills should anticipate what the user needs next, not just answer the literal question
- **Concise** — briefings and confirmations should be short; don't repeat information back unnecessarily
- **Warm but direct** — friendly tone without being sycophantic

### Profile fallback pattern (use this consistently):
```markdown
## Step 0: Load User Profile

Read `EA_PROFILE.md` from the vault root.

- Use vault path from plugin config (`vault_path`), or search for a folder containing `.obsidian/`
- Load: [list what this skill needs from the profile]
- If not found: prompt `/ea-agent:setup`, then continue with the defaults below
```

## Profile schema changes

If your contribution adds new fields to `EA_PROFILE.md`:

1. Update the profile template in `skills/setup/SKILL.md`
2. Bump `profile_version` in the setup skill (e.g., `1.0` → `1.1`)
3. Add upgrade handling in the setup skill's Step 4 (Upgrade Mode) — document what's new in that version
4. Update `DEVELOPER.md` with the new fields
5. Add behavioral evals that test the new fields are used correctly

See [DEVELOPER.md — Updating the profile schema](DEVELOPER.md#updating-the-profile-schema) for details.

## Pull request process

1. Branch off `main`: `git checkout -b your-feature-name`
2. Make your changes
3. Run evals and confirm they pass
4. Open a PR against `main` with a clear description of what changed and why
5. The CI pipeline will run structural validation and evals automatically
6. A maintainer will review and merge

## PR description template

```
## What this changes
[Brief description]

## Why
[Motivation — what problem does this solve or what does it improve?]

## Skills affected
- [ ] skill-name — what changed

## Evals
- [ ] Added/updated routing scenarios
- [ ] Added/updated behavioral scenarios
- [ ] Evals pass locally at 80%+

## Profile changes
- [ ] No profile schema changes
- [ ] Profile schema changed — profile_version bumped to X.X
```

## What we won't merge

- Hardcoded personal information (names, organizations, specific folder paths)
- Skills that only work for one person's specific setup without profile-driven configuration
- Changes that break existing eval scenarios without a good reason
- Profile changes without a `profile_version` bump and upgrade handling
