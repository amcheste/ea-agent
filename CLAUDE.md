# EA Agent — Claude Code Conventions

Project-specific conventions for working on this repo with Claude Code.

## Branch model

- `main` — stable, released code only. Never commit directly.
- `develop` — integration branch. All feature PRs target this.
- Feature branches: `feat/<name>`, `fix/<name>`, `ci/<name>`, `docs/<name>`, `evals/<name>`
- Releases: `develop` → PR → `main` → tag `v*.*.*`

## Commit style

Conventional commits required:

```
feat(inbox): add Slack DM triage support
fix(setup): handle missing vault path gracefully
evals(weekly-review): add edge case for empty task list
chore(deps): bump anthropic to 0.50.0
```

Types: `feat` `fix` `evals` `docs` `chore` `refactor` `ci` `test`

## Plugin versioning

Version lives in `.claude-plugin/plugin.json` → `version`.

- Bump `patch` for bug fixes and eval improvements
- Bump `minor` for new skills or new skill capabilities
- Bump `major` for breaking changes to the EA profile schema

Update `CHANGELOG.md` with every version bump.

## Skill standards

Every skill in `skills/<name>/SKILL.md` must:
1. Start with YAML frontmatter (`name`, `description`)
2. Reference `EA_PROFILE.md` in Step 0 (except `setup`)
3. Have at least one eval scenario in `evals/scenarios/`

CI enforces (1) and (2). Evals enforce (3) on PRs.

## Running evals locally

```bash
cd evals
pip install -r requirements.txt
export ANTHROPIC_API_KEY=<your key>

# All evals
python eval_runner.py

# Routing only (cheaper, faster)
python eval_runner.py --routing-only

# Single skill
python eval_runner.py --skill inbox-processing
```

Pass thresholds: routing ≥ 85%, behavioural ≥ 75%.

## CI overview

| Workflow | Trigger | Purpose |
|---|---|---|
| `validate.yml` | push/PR to main, develop | Structure + version checks |
| `release.yml` | tag `v*.*.*` | Run evals, publish GitHub Release |
| `sast.yml` | push/PR + weekly | Semgrep (p/python, p/secrets) |
| `scorecard.yml` | push to main + weekly | OpenSSF Scorecard |
| `release-drafter.yml` | push to develop | Auto-draft release notes |
| `labeler.yml` | PR opened/edited | Auto-label from branch name |
| `stale.yml` | daily | Close inactive issues/PRs |
| `dependabot` | weekly | Bump pip + Actions SHAs |

## Files never to commit

- `~/.secrets`, `EA_PROFILE.md` (user-specific, generated at runtime)
- Any `.env` file
- Obsidian vault content or personal notes
