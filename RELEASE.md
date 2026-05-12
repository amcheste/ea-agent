# Release Guide

How to cut a release of EA Agent. This document is for maintainers.

## Two version numbers

EA Agent has two independent version numbers. Understanding the difference is important before every release.

| Version | Where | What it tracks | When to bump |
|---------|-------|----------------|-------------|
| **Plugin version** | `.claude-plugin/plugin.json` → `version` | The plugin as a whole | Every release |
| **Profile version** | `skills/setup/SKILL.md` → `profile_version` | The `EA_PROFILE.md` schema | Only when `EA_PROFILE.md` structure changes |

**Plugin version** follows semver (`MAJOR.MINOR.PATCH`):
- `PATCH`. Bug fixes, wording improvements, new eval scenarios, doc updates
- `MINOR`. New skills, new profile fields, new features (backwards compatible)
- `MAJOR`. Breaking changes to skill behavior, vault structure changes, major rewrites

**Profile version** follows a simple `MAJOR.MINOR` scheme (`1.0`, `1.1`, `2.0`):
- `MINOR` bump. New optional fields added to `EA_PROFILE.md`
- `MAJOR` bump. Existing fields renamed, removed, or restructured

When `profile_version` changes, users must re-run `/ea-agent:setup` to get the benefits. The setup skill handles the upgrade automatically. It detects the old version and only asks about new fields.

## Pre-release checklist

Work through this before tagging:

### Code
- [ ] All changes are merged to `main`
- [ ] `version` is updated in `.claude-plugin/plugin.json`
- [ ] If profile schema changed: `profile_version` is bumped in `skills/setup/SKILL.md`
- [ ] If profile schema changed: upgrade handling added to setup skill's Step 4
- [ ] If profile schema changed: `DEVELOPER.md` schema table is updated

### Evals
- [ ] Evals pass locally at or above threshold
  ```bash
  export ANTHROPIC_API_KEY=your-key
  python evals/eval_runner.py --pass-threshold 80
  ```
- [ ] New skills or behaviors have eval coverage

### Docs
- [ ] `README.md` reflects any new skills or changed install steps
- [ ] `DEVELOPER.md` reflects any new patterns or changed conventions
- [ ] This checklist still makes sense (update it if the process changed)

## Cutting the release

Once the checklist is done, releasing is two commands:

```bash
# 1. Tag the commit on main
git tag v1.2.0

# 2. Push the tag
git push origin v1.2.0
```

That's it. The `release.yml` workflow takes over from here:
1. Runs full structural validation
2. Runs evals against the tagged code
3. If both pass → creates a GitHub Release with auto-generated notes
4. If profile_version changed since the last tag → adds an upgrade notice to the release body

If evals fail, the release is not created. Fix the failures, push the fixes to `main`, re-tag, and push the tag again.

## Writing good release notes

GitHub auto-generates release notes from commit messages since the last tag. The output is only as good as the commit messages. Which is why commit messages in this repo follow the format:

```
Short imperative summary (50 chars)

Optional longer explanation of why the change was made,
what problem it solves, or anything a user needs to know.
```

The CI generates notes automatically, but you should review and edit before publishing if needed, especially to:
- Add a plain-English summary at the top for non-technical users
- Make the upgrade call-to-action prominent when profile_version changed

### Profile upgrade release template

When `profile_version` bumps, the release body should include:

```markdown
## ⚠️ Profile upgrade required

This release adds new fields to your EA profile. Run the setup skill to upgrade:

/ea-agent:setup

Your existing profile data is preserved — setup will only ask about the new fields.

### What's new in your profile
- [New field 1] — [what it enables]
- [New field 2] — [what it enables]
```

### Non-upgrade release template

```markdown
## What's new
[2-3 bullet points for the most notable changes]

No profile changes — no action required after updating.
```

## After the release

1. **Notify users**. If your coworkers or family have the plugin installed, let them know a new version is available. A Slack message or text with the release link and the key changes is enough.

2. **Profile upgrade**. If `profile_version` changed, remind them specifically to run `/ea-agent:setup`. Users won't get the new profile fields until they do.

3. **Verify the release**. Check that the GitHub Release page looks right at `github.com/amcheste/ea-agent/releases`.

## Hotfix releases

For urgent bug fixes:

```bash
# Fix the bug on main, then:
git tag v1.1.1
git push origin v1.1.1
```

Same process. No special branch needed at this scale. The CI will validate and release.

## Version history

| Version | Profile version | Date | Summary |
|---------|----------------|------|---------|
| v1.1.0 | 1.0 | 2026-03-28 | Add user profile system, setup skill, CI/CD, eval suite |
| v1.0.0 | (n/a) | 2026-03-28 | Initial release: 8 skills, Obsidian + Apple Reminders integration |
