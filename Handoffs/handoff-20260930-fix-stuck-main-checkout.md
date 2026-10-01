# Handoff: fix the stuck main checkout so sessions can push again

Written 2026-09-30, **rewritten 2026-10-01 with fresh measurements and a changed method (merge, not rebase)**.
Run it in the main project folder `/Users/danielrose/Documents/Claude/Projects/Abs By AI` on Dan's Mac. It cannot
run in the cloud or in a worktree: the problem is the working copy on this disk.
Recommended: Claude Opus 5.5, high effort.

## The problem in plain language

The project folder on Dan's Mac is the copy every Claude session edits. GitHub holds the official copy, and
Railway deploys the site from GitHub. The two have drifted apart and git refuses to reconcile them, so every
session that commits in the main folder gets "push rejected". Sessions have kept committing locally anyway, so
the gap grows every day.

## Measured state, 2026-10-01 (re-measure before acting; it will have moved)

- `git status -sb`: `## main...origin/main [ahead 42, behind 137]`. Merge base `b3c7e6b`.
- **35 local commits are genuinely missing from GitHub** (`git cherry -v origin/main HEAD`, lines marked `+`):
  RO-05 approval and setup, the thumbnail-split rule, RO-10, RO-11, RO-12, RO-13, RO-16 and SL-05 recipes and
  approvals, HyperFrames templates, delivery gate 2.4.0, and their handoffs. Seven more are marked `-`
  (already on GitHub by content).
- **109 tracked files have uncommitted edits.** 83 are byte-identical to the GitHub version. 26 differ and
  hold live work (skills under `.claude/skills/`, `AGENTS.md`, `scripts/blotato/*.py`,
  `scripts/edit-queue/asset_approval.py` and its test, `scoreboard.json`, `brief-ads.json`, one handoff).
- **Untracked files:** about 4,400 outside `app-store-assets/` and `ios-app/` (leave those two folders
  alone). 86 of them also exist on GitHub and block a merge: 83 identical, 3 differ
  (`.claude/skills/design-sales-page/SKILL.md`, its `reference/round2-letter/README.md`,
  `Handoffs/handoff-20260930-ro05-captions-and-article-after-release.md`).
- **A dry merge of the committed state** (`git merge-tree --write-tree --name-only HEAD origin/main`) reports
  17 conflicted files: `SOFTBLUE.md`, `VIDEO-RULES.md`, `hyperframes/README.md`, eight files under
  `longform-edit/reference/ro16/`, `video-setup/SKILL.md`, `AI_COORDINATION.md`, `BLOTATO_QUEUE_PROGRESS.md`,
  `Handoffs/README.md`, `Handoffs/video-editing/00-MASTER.md`, `Handoffs/video-editing/jobs.json`.
  The snapshot commit in step 3 can add a few more.
- GitHub's side changed app files (`credits-data.json`, `public/img/letter/*`, the /start page). The local
  side changed no app files. Root `*-data.json` files are the live database (memory
  `static-serving-and-json-persistence`): always take GitHub's version of those, never the local one.
- 9 stashes exist (`git stash list`). Do not drop, pop or reorder any of them. The board's "Stashed edits"
  entry refers to commit `5d8284a`; it is no longer `stash@{0}`.
- 14 worktrees exist. Leave them alone.

## Method: snapshot commit, then one merge

A rebase would replay 35 commits and make you resolve the same files many times. One merge resolves each file
once. Committing the dirty files first means nothing on disk is reverted, which is far safer with other
sessions around. Never run `git stash` in any form here (memory `auto-commit-push`).

## Steps

1. **Check for running builds.** `ps aux | grep -E "[f]fmpeg|[b]uild\.py|[f]inish_chain"`. If a video build is
   running, wait and re-check every few minutes; the merge rewrites skill scripts a build may be reading. Open
   Claude sessions that are idle or waiting on Dan do not block this. Do not close or message them.
2. **Safety net.** `git branch backup/main-before-sync-20261001`; in the scratchpad save `git diff > dirty.patch`,
   `git status --short > status.txt`, `git stash list > stashes.txt`, and copies of the 26 differing files and
   the 3 differing untracked files. Re-run the classification (compare each dirty or untracked file with
   `git show origin/main:<path>`) because the lists above are a day old.
3. **Clear what is identical, commit what differs.**
   - Modified files identical to GitHub: `git checkout -- <file>` (the merge brings the same content back).
   - Untracked files identical to GitHub: delete the local copy (the merge restores it).
   - Modified files that differ, plus the differing untracked files that collide: `git add` exactly those
     paths and commit as "Snapshot of uncommitted main-checkout edits before the 10-01 sync". Text files only;
     the repo is public, so do not add photos, footage, keys or anything personal. Do not `git add -A`.
4. **Merge.** `git fetch origin && git merge --no-ff origin/main`. Resolve each conflict, then diff the result
   against both sides before `git add`:
   - `AI_COORDINATION.md`, `Handoffs/README.md`, `00-MASTER.md`, `jobs.json`, `BLOTATO_QUEUE_PROGRESS.md`:
     union. Keep every entry and row from both sides, newest wording when the same entry appears twice. Never
     drop another session's board entry. `jobs.json` must still parse (`python3 -m json.tool`).
   - `longform-edit/reference/ro16/*`: the main folder is where RO-16 was built (rounds 2 and 3), so prefer
     the local side and port over anything GitHub's side added that local lacks.
   - Skill and rule files (`VIDEO-RULES.md`, `SOFTBLUE.md`, `video-setup/SKILL.md`, `hyperframes/README.md`):
     keep both sides' additions; when the same rule appears in two wordings keep the later-dated one.
   - Any `*-data.json` or file under `public/`: GitHub's side.
   - New or rewritten lines carry no em dash.
5. **Check before pushing.** `python3 -m py_compile` on every conflicted `.py`; `python3 -m pytest
   scripts/edit-queue/tests -q`; `scripts/board-check.sh` (compress your own wording if over budget);
   `grep -c '<<<<<<<\|>>>>>>>'` across the resolved files must be 0.
6. **Push and verify.** `git push origin main`. `git status -sb` must show no ahead/behind. If the push is
   rejected because GitHub moved again, `git fetch && git merge origin/main` once more and push.
7. **Deploy check.** `~/.npm-global/bin/railway deployment list --service abs-by-ai` shows the new deploy
   SUCCESS; load https://absbyai.com and https://absbyai.com/start once. The merge brings no new app code to
   GitHub, so the live site should not change.
8. **Close out.** Re-read the board from disk, delete the "Shared checkout cannot push" entry, remove this
   handoff's row from `Handoffs/README.md`, run `scripts/board-check.sh`, commit and push. Keep the backup
   branch for a week; say so in the report.
9. **Report to Dan** in plain language: how many commits reached GitHub, which conflicts needed a judgment
   call and what you chose, anything left uncommitted and why, and the backup branch name.

## Risks

- A wrong conflict resolution silently loses another session's rule, recipe or board entry. Diff every
  resolved file against both sides.
- The merge changes files on disk under any open session. Step 1 guards builds; idle sessions re-read files
  when they next act.
- Committing the snapshot publishes those 26 files' current contents to a public repo. They are skills,
  scripts and handoffs already tracked there; check nothing secret was pasted into one (`grep -n -i -E
  "api[_-]?key|secret|token" ` on the staged diff) before committing.

## Starter prompt

```
Execute Handoffs/handoff-20260930-fix-stuck-main-checkout.md in the main project folder (not a worktree, not the
cloud). The folder has uncommitted changes from me and from other sessions since the handoff was measured, so
re-measure first and treat the handoff's lists as examples, not the full set. Wait out any running video build,
make the backup branch and scratchpad copies, revert only files identical to GitHub, commit every differing
dirty file as one snapshot commit so nothing of mine is lost, then merge origin/main (merge, not rebase),
resolve conflicts by the handoff's rules, run the checks, push, confirm the Railway deploy, and clear the board
entry. Never git stash. Report what reached GitHub, each judgment call, and anything you could not resolve.
```

Model: Claude Opus 5.5, high effort. Codex alternative: GPT-6 Sol high, opened on the main folder, not a worktree.
