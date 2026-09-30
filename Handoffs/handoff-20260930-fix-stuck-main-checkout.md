# Handoff: fix the stuck main checkout so sessions can push again

Written 2026-09-30 by a Claude session (model-routing task). Fire when NO other session is running in the main
project folder `/Users/danielrose/Documents/Claude/Projects/Abs By AI` (Claude sessions run there directly;
Codex sessions use `~/.codex/worktrees/*`, so they do not block this). Recommended: Claude Opus 5.5, medium effort.

## The problem in plain language

The project folder on Dan's Mac is the copy of the code that every Claude session edits. GitHub holds the
official copy, and Railway deploys the site from GitHub. The Mac copy and the GitHub copy have drifted apart
and git refuses to reconcile them:

- **11 commits sit on the Mac that were never pushed to GitHub** (`41bb43b` through `9982b49`). Seven of
  them reached GitHub anyway by content, through worktree sessions, but **five are genuinely missing from
  GitHub**: the 24 studio posts prep (`ba631af`), RO-05 round 4 delivery (`5d16bfd`), RO-05 approval and
  queue finalized (`10a50a3`), the Codex-thumbnail / Claude-upload standing rule in `AGENTS.md`
  (`b1d09ef`), and the matching video-setup description (`9982b49`).
- **GitHub has 47 commits the Mac does not have** (worktree sessions pushed them).
- **97 tracked files carry uncommitted edits** in the Mac copy, and about 70 handoff and skill files exist
  there untracked while also existing on GitHub. Git refuses `pull`, `merge` and `rebase` while those are
  in the way, so every session that commits in the main folder gets "push rejected" and either gives up or
  works around it. The 2026-09-30 routing commit went to GitHub through a temporary worktree for that reason.

Why it matters: Dan's approvals and standing rules are not on GitHub, so worktree and Codex sessions start
from stale rules; every future commit in the main folder fails the delivery rule (commit, push, deploy); and
the longer it sits, the more conflicts pile up.

## Facts gathered (2026-09-30)

- `git status -sb` in the main folder: `## main...origin/main [ahead 12, behind 47]` (12 includes the
  routing commit `015ca38`, already on GitHub as `b4f4fb3`; `git cherry -v origin/main HEAD` marks it `-`).
- `git cherry -v origin/main HEAD` marks the five missing commits with `+` and the rest with `-`.
- Of the 97 modified tracked files, most are byte-identical to the GitHub version (a worktree session pushed
  the same edits). Five differ from GitHub and hold live work: `.claude/skills/_shared/VIDEO-RULES.md`,
  `AI_COORDINATION.md`, `Handoffs/README.md`, `Handoffs/handoff-20260923-ro05-recut-astra.md`,
  `Handoffs/video-editing/00-MASTER.md`.
- Untracked files: about 83,500, almost all under `app-store-assets/` (79,545) and `ios-app/` (3,502). Those
  do not block the pull. The blockers are the untracked files that also exist on GitHub (RO-16 reference
  scripts under `.claude/skills/longform-edit/reference/ro16/`, `zeeshan-master/grade|hair|pill`,
  `Docs/HYPERFRAMES_RESEARCH.md`, several `Handoffs/handoff-2026093*.md`); every one checked was identical
  to the GitHub copy.
- 14 worktrees exist (`git worktree list`); leave them alone.
- Never run `git stash -u` here (memory `auto-commit-push`: it lost untracked work once). Use patch files.

## Steps

1. **Confirm the folder is idle.** No running Claude session in the main folder (check the desktop app's
   session list; `ps aux | grep -c "claude.app/Contents/MacOS/claude"` for stray processes). Stop if one
   is mid-task.
2. **Snapshot everything first.** In the scratchpad: `git diff > dirty.patch`, `git diff --stat > dirty-stat.txt`,
   `git status --short > status.txt`, and copy the five differing files listed above to a `backup/` folder.
   Also `git branch backup/main-before-fix-20260930` so the 12 local commits keep a name.
3. **Clear the identical modified files.** For each modified tracked file: if `git show origin/main:<f>`
   equals the working copy, `git checkout -- <f>`. Keep the five differing files; save their diffs against
   HEAD as individual patch files (`git diff -- <f> > backup/<name>.patch`), then `git checkout -- <f>`.
4. **Clear the colliding untracked files.** For every untracked path that exists in `origin/main`: if
   identical, delete the local copy (git restores it on pull). If any differs, keep a copy in `backup/` and
   delete the local copy. Do not touch `app-store-assets/` or `ios-app/`.
5. **Rebase.** `git pull --rebase origin main`. The seven already-upstream commits drop out on their own.
   Resolve conflicts on the five `+` commits, most likely in `AI_COORDINATION.md`, `Handoffs/README.md`,
   `Handoffs/video-editing/00-MASTER.md` and `.claude/skills/video-setup/SKILL.md`: keep both sides' facts,
   never delete another session's board entry, and keep the em-dash rule in the lines you touch.
6. **Push and verify.** `git push origin main`; `git status -sb` must read `## main...origin/main` with no
   ahead/behind. Confirm on GitHub that `AGENTS.md` carries the "Organic video setup: Codex thumbnail,
   Claude upload" rule and `RO-05` shows approved in the queue.
7. **Re-apply the five live diffs.** `git apply --3way backup/<name>.patch` for each. Where the patch is
   already in the pulled history, skip it. Leave the results uncommitted only if their owning session is
   still open (RO-12, clip library); otherwise commit them as "Re-apply main-checkout edits stranded by
   the 09-30 sync" and push.
8. **Deploy check.** The push triggers Railway; `~/.npm-global/bin/railway deployment list --service abs-by-ai`
   (or the dashboard) shows the new deploy SUCCESS. These commits are docs and skills, so the site should be
   unchanged; load https://absbyai.com once.
9. **Board.** Re-read `AI_COORDINATION.md` from disk; delete the entry "Shared checkout cannot push"; run
   `scripts/board-check.sh`. Remove this handoff's row from `Handoffs/README.md` and the HANDOFFS line on
   the board. Commit and push that too.
10. **Optional, only if cheap:** add `app-store-assets/` and `ios-app/` build output to `.gitignore` if they
    are generated files (check with Dan's iOS memory `ios-capacitor-app` first; the wrapper source itself may
    need to stay tracked). Report either way.

## Risks

- A conflict resolution that drops a board entry or a handoff row silently loses another session's state.
  Diff every resolved file against both sides before continuing.
- If a Claude session is active in the folder during step 3 or 4, its unsaved edits get reverted. Step 1 is
  the guard.
- Railway deploys on every push; nothing here touches app code, but confirm the deploy anyway.

## Starter prompt

```
Execute Handoffs/handoff-20260930-fix-stuck-main-checkout.md. Confirm the main project folder has no other
running session first, snapshot the dirty state to the scratchpad exactly as the handoff says, then sync the
Mac checkout with GitHub: clear identical dirty files, pull --rebase, resolve the five stranded commits, push,
re-apply the five live diffs, confirm the Railway deploy, and clear the board entry. Never git stash -u.
Report what was resolved and anything you could not.
```

Model: Claude Opus 5.5, medium effort (conflict resolution needs judgment; not a Sonnet job). Codex alternative:
GPT-6 Sol high, pointed at the main folder rather than a worktree.
