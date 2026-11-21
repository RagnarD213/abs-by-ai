# Handoff: stop the main checkout from getting stuck again (safe push script + drift alarm)

Written 2026-10-01 by Claude (Opus 5.5), right after `handoff-20260930-fix-stuck-main-checkout.md` was executed.
Run it in the main project folder `/Users/danielrose/Documents/Claude/Projects/Abs By AI` on Dan's Mac.
Recommended: Claude Opus 5.5, medium effort. About one session.

## Goal

The Mac folder and GitHub were synced on 2026-10-01 (merge `4c70de0`, close-out `323d77b`). That cleared the
backlog but changed nothing about why it built up. This task removes the cause, so a session's commit always
reaches GitHub, and adds an alarm so drift is seen the day it starts instead of 34 commits later.

## Why it happens (in plain language)

- Every Claude session edits the same folder, so the folder almost always holds some other session's
  uncommitted edits.
- GitHub's copy moves all day (Codex worktrees, other sessions, the site's own data commits), so the Mac copy is
  almost always a few commits behind when a session tries to push.
- The rule on record says "pull with rebase, then push" (memory `auto-commit-push`). A rebase refuses to run
  when the folder has uncommitted edits. The session commits anyway, the push is rejected, the commit stays on
  the Mac only. Repeat for two weeks and you get 34 stranded commits.
- Nothing warned anyone. The first sign was a handoff.

This cause is inferred from the folder's state, the 9 leftover stashes (several are `autostash`) and the
memory notes of 09-16, 09-17 and 09-29. Step 1 confirms it before anything is built.

## Can it run beside other work?

Yes. Other Claude sessions, Codex tasks and video builds can keep running. All building and testing happens in
throwaway clones in the scratchpad. The main folder is touched only by: two new script files, small edits to
`AGENTS.md` and `.claude/settings.json`, and the final push. Two cautions: do not run it at the same time as
another session that is itself repairing git in the main folder, and if another session has uncommitted edits
in `AGENTS.md` or `.claude/settings.json`, commit only your own lines (or wait for that session) rather than
sweeping its edits into your commit.

## Decisions already made (do not reopen)

- **Merge, never rebase, in the shared folder.** A merge runs with other sessions' uncommitted edits present as
  long as they are not the same files GitHub changed. A rebase does not.
- **Never `git stash` in any form**, including `--autostash` (it stashes other sessions' live work).
- **Never `git add -A` / `git add .`** The repo is public and the folder holds about 3,500 untracked media and
  output files. A session commits only the paths it names.
- **On a real conflict the script stops and reports. It never auto-resolves another session's file.**
- Root `*-data.json` files and anything under `public/` that the live site writes: GitHub's version wins.
- The 9 existing stashes, the 14 worktrees and branch `backup/main-before-sync-20261001` are left alone
  (the backup branch can be deleted after 2026-10-08).

## What to build

### 1. `scripts/git/safe-push.sh` (the one way every session pushes from the main folder)

Usage: `scripts/git/safe-push.sh -m "commit message" -- <path> [<path> ...]`

Behaviour, in order:

1. Refuse to run outside the main folder on branch `main`, or while a merge, rebase or cherry-pick is in
   progress (`.git/MERGE_HEAD`, `.git/rebase-*`). Refuse if no paths are given.
2. `git add -- <the named paths only>`, then commit with the message given. If nothing is staged, skip the
   commit and carry on (the job may be to push earlier commits).
3. `git fetch origin`. If the folder is not behind, go to step 6.
4. Pre-flight the merge without touching the disk: list the files GitHub's side changes
   (`git diff --name-only HEAD...origin/main`) and compare with (a) tracked files that have uncommitted edits
   and (b) untracked files. For each overlap: if the local file is byte-identical to GitHub's version
   (`git hash-object <f>` equals `git rev-parse origin/main:<f>`), clear it (`git checkout -- <f>` for tracked,
   delete for untracked; the merge brings the same bytes back). If it differs, STOP before merging and print
   the list: these are another session's live edits in the way.
5. `git merge --no-ff --no-edit origin/main`. If it conflicts: `git merge --abort`, print the conflicted
   files, exit non-zero. The local commit is kept; nothing is lost; the report says "needs a hand merge".
6. `git push origin main`. If rejected because GitHub moved again, repeat steps 3 to 6 up to three times.
   After a "remote rejected" message, fetch and compare hashes before retrying: the push may have gone
   through (memory `github-push-false-failure`).
7. Print one final line a session can quote: pushed hash, ahead/behind (must be 0 / 0), and anything it
   stopped on. Exit codes: 0 pushed, 2 stopped on another session's files, 3 merge conflict, 4 push failed.

Write it in bash, quote every path (file names here contain spaces), use `-z` / null-separated lists. No em
dash in any message it prints.

### 2. `scripts/git/drift-check.sh` (the alarm)

Prints ahead / behind for `main` against `origin/main` from the last fetch (it may fetch if the last fetch is
older than 30 minutes; keep it under 2 seconds otherwise). Thresholds: **ahead 3 or more, or behind 40 or
more = WARN**. With `--hook` it prints a one-line warning and always exits 0 (a warning, never a block; the
board-check hook blocks, this one must not).

Wire it in three places:

- `.claude/settings.json`: add it to the existing `PostToolUse` hook list beside `board-check.sh --hook`,
  matcher `Bash` only, timeout 5. Use the `/update-config` skill for the edit.
- The morning brief: add a "Git drift" line. The Claude task lives at
  `~/.claude/scheduled-tasks/abs-by-ai-morning-brief/SKILL.md`; the Codex version is specified in
  `Handoffs/handoff-20260930-codex-dot-01-*` (add the same line to that doc so it survives the move).
- `scripts/board-check.sh`: no change. Keep the two checks separate.

### 3. Rules and memory

- `AGENTS.md`, "Delivery and deployment": add two lines. From the main folder, push only with
  `scripts/git/safe-push.sh`; if it stops, report the files and put one board entry up the same day rather
  than committing more on top.
- Memory `auto-commit-push`: replace the "pull --rebase" and "rebase --autostash" advice with the script;
  keep the "never git stash" history. Update the `MEMORY.md` pointer line (keep it under about 200
  characters; the index is over its size limit, so do not lengthen it).
- Codex reads `AGENTS.md` too. Codex worktrees push from their own clean checkouts, so they do not need the
  script; say that in the rule so Codex does not try to run it in a worktree.

## Steps

1. **Confirm the cause.** `git status -sb` (expect 0 / 0 or a small gap), `git stash list`, and search recent
   session transcripts or the board archive for "rejected" and "cannot pull with rebase". If the evidence
   points somewhere else (for example a dead credential, memory `railway-deploy-workflow` mentions a dead
   remote-URL token since 09-02), stop and report before building.
2. Build the two scripts.
3. **Test in a throwaway clone, never in the main folder.** `git clone` the repo twice into the scratchpad
   with a local bare repo as their shared `origin`. Prove each case: clean push; behind with unrelated dirty
   files (must merge and push, dirty files untouched); behind with an identical dirty file (cleared, pushed);
   behind with a differing dirty file that GitHub also changed (stops, exit 2, nothing changed on disk);
   true commit conflict (aborts, exit 3, commit kept); a path with spaces; push race (retries).
4. Wire the hook and the morning brief line. Trigger the hook once and confirm it prints and does not block.
5. Update `AGENTS.md` and memory.
6. **Use the script for its own delivery:** commit this task's files with `safe-push.sh`, confirm ahead /
   behind 0 / 0, confirm the Railway deploy (`~/.npm-global/bin/railway deployment list --service abs-by-ai`)
   and load https://absbyai.com once. No app code changes, so the site should not change.
7. Close out: remove this handoff's line from the board's HANDOFFS section and its row in
   `Handoffs/README.md`, run `scripts/board-check.sh`, push with the script.

## Risks

- A bug in the script could clear a file that was not identical. The identical test must be a byte hash
  comparison, and the test in step 3 must include a file that differs by one byte.
- A session that ignores the rule and pushes by hand still strands commits. The drift alarm is the backstop;
  that is why both parts ship together.
- The hook runs after every Bash call. Keep it fast and silent when there is no drift.

## Report to Dan

Plain language: what was built, the test cases that passed, where the alarm shows up, and what a session
does now when its push is blocked.

## Starter prompt

```
Execute Handoffs/handoff-20261001-prevent-stuck-checkout-safe-push-and-drift-alarm.md in the main project
folder (not a worktree, not the cloud). First confirm the cause it describes; stop and report if the evidence
points elsewhere. Then build scripts/git/safe-push.sh and scripts/git/drift-check.sh exactly as specified,
test every case in a throwaway clone in the scratchpad (never in the main folder), wire the drift check into
the PostToolUse hook and the morning brief, update AGENTS.md and the auto-commit-push memory, deliver using
the new script, confirm the Railway deploy, and clear the handoff's board line and README row. Never git
stash, never git add -A. Report what was built, which tests passed, and anything you could not finish.
```

Model: Claude Opus 5.5, medium effort. Codex alternative: GPT-6 Sol medium, opened on the main folder.
