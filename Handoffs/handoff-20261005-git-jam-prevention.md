# Handoff: stop the main folder from jamming against GitHub again (2026-10-05)

**Ops task, not a video.** Sidebar name: `Git Jam Prevention`.
**Model:** Codex GPT-6 Sol, high.
**When:** after `handoff-20261005-git-unjam-main-folder.md` has run and the folder reads 0 ahead / 0 behind. Parts A and
B can run alongside other tasks. Part C is a design note only; it changes nothing.

## Why

From 10-02 to 10-05 nothing from the shared Claude folder reached GitHub (41 commits stuck). Cause: sessions edited
shared files (rule files, shared docs, shared scripts) and left them uncommitted; GitHub then got newer versions of the
same files; the merge could not run over unsaved edits; and the rules told each session to commit only its own files,
so nobody cleared it. Codex sessions were unaffected because each works in its own worktree.

## Part A: rules (edit `AGENTS.md`, "Delivery and deployment")

Add, dated 2026-10-05, in Dan's plain style, no em dashes:
1. **A shared file is committed and pushed the moment it is edited.** Shared means any file under
   `.claude/skills/_shared/`, `AGENTS.md`, `CLAUDE.md`, `Docs/`, `scripts/`, and any skill file another job also uses.
   Edit it, then `safe-push.sh` that file in the same step, before going back to the task. Never leave one uncommitted
   until the end of a task.
2. **When `safe-push.sh` stops on another session's files (exit 2), the session clears it instead of walking away,**
   if every blocking file was last modified more than 2 hours ago: back the files up to `tmp/`, commit them as they
   are with the message "Commit pending edits from earlier sessions so main can merge", and push again. If a blocking
   file was modified inside the last 2 hours, its owner is live: put up the board note as today and retry at the end of
   the task. This replaces "Do not commit more on top" for that case only.
3. Keep everything else: only `safe-push.sh` from the main folder, never rebase, stash or `add -A`.
Mirror the one-line version in `CLAUDE.md` "Shared-workflow requirements" and in the header comment of
`scripts/git/safe-push.sh`. Update memory `auto-commit-push`.

## Part B: tooling

1. **`scripts/git/safe-push.sh`:** when it stops on exit 2, print each blocking file's last-modified time and say
   which rule applies (older than 2 hours: "commit these and re-run"; newer: "owner is live, retry later"). Add a
   `--adopt-stale` flag that does the backup, the commit and the retry for files older than 2 hours. Add tests beside
   the script's existing ones for both branches.
2. **`scripts/git/drift-check.sh`:** exit non-zero and print one line when the folder has been ahead of GitHub for more
   than 24 hours (age of the oldest unpushed commit).
3. **Morning routine:** add a step to `Docs/BOARD_MORNING_MAINTENANCE.md` and the morning-brief task: run
   `drift-check.sh`; if it fails, the brief clears the jam with `--adopt-stale` before anything else and reports it in
   one line.

## Part C: design note only (write `Docs/CLAUDE_SESSION_WORKTREES.md`, change nothing)

The lasting fix is one working copy per Claude session, as Codex has. Write one page for Dan: how the desktop app's
per-session worktrees would work for this project, what breaks (the push script refuses worktrees today; video work
directories on the Extreme drive use absolute paths and are unaffected; `tmp/`, memory and untracked media are per
folder), what it costs in disk, and how it fits with `handoff-20261001-move-project-out-of-icloud.md`. End with one
recommendation and a yes or no question for Dan. Do not switch anything on.

## Done means

Parts A and B committed and pushed with `safe-push.sh`, tests passing, the deploy confirmed, the page for Part C
written, this handoff's lines removed from the board and `Handoffs/README.md`, and this file deleted.

## Starter prompt (Codex GPT-6 Sol, effort high)

Read `Handoffs/handoff-20261005-git-jam-prevention.md` and execute it. Name this task "Git Jam Prevention". First
confirm the main folder reads 0 ahead and 0 behind GitHub; if it does not, stop and tell me to run the unjam handoff
first. Do parts A and B, write the part C page without switching anything on, and tell me in plain words what changed.
