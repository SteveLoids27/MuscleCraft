# Automation — one milestone at a time

The Agent **stops after each milestone**. It does not auto-chain to the next one.

## Build one milestone

In **Agent mode**, say:

```
Build Milestone 5 from BUILD_PROMPT.md
```

Or:

```
Read BUILD_PROMPT.md and build the next pending milestone.
```

When the Agent ends with `MILESTONE_COMPLETE`, **review the changes** before starting the next milestone.

## Pipeline (per milestone)

1. `app-planner` (if needed)
2. `app-builder` — implement one milestone
3. `safe-code-improver` — safe review
4. `app-tester` — `python3 -m pytest -v`
5. Mark milestone `done` in `BUILD_PROMPT.md`

## Git workflow (MuscleCraft)

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code (reviewed via PR) |
| `dev-Steve` | Active development — **build all new features here** |

Remote: `git@github-steveloids27:SteveLoids27/MuscleCraft.git`

### Per feature

1. Work on `dev-Steve`
2. Run `python3 -m pytest -v`
3. Commit and push: `git push origin dev-Steve`
4. Open PR into `main` for review

In Agent mode:

```
Build <feature> on dev-Steve, push, and open a PR to main
```

## Open a PR (manual, when ready)

When a feature or milestone is complete on `dev-Steve`:

```
Push dev-Steve and open a PR to main for review
```

Prerequisites: `gh auth login`, SSH via `github-steveloids27`, never commit `.env`.

## Stop / disable

No background loop runs. To cancel mid-milestone, stop the Agent in Cursor.

The old `enabled` flag and stop hook auto-chain are **disabled**. You can delete:

```bash
rm -f .cursor/automation/enabled .cursor/automation/pr-pushed
```
