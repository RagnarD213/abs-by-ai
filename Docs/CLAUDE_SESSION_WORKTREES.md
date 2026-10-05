# One working copy per Claude session: design note (2026-10-05)

**Status: a note for Dan to decide on. Nothing has been switched on.**

## The idea in plain words

Today every Claude session works in the same folder. When one session leaves a file half-edited, it sits in the way of
every other session's push. That is what jammed the folder from 10-02 to 10-05.

Codex never has this problem because each Codex task gets its own private copy of the project (a "worktree"). It edits
there, pushes from there, and nobody else's unsaved work can block it. The Claude desktop app can do the same thing: when
a session starts, the app makes a private copy under `.claude/worktrees/<name>/` on its own branch. Three of these
already exist in this project from earlier sessions.

The rules and tooling added on 10-05 (push shared files at once, `--adopt-stale`, the 24-hour jam alarm) treat the
symptom. Worktrees remove the cause.

## What it costs

- **Disk: about 0.4 GB per session.** A worktree holds only the files git tracks (3,881 files, 0.4 GB). The 5.2 GB of git
  history is shared, not copied. Ten live sessions is about 4 GB. The Mac has 107 GB free.
- **Cleanup:** the app removes a worktree when its session is archived and nothing was left unsaved. Leftovers need an
  occasional sweep, the same as the 15 Codex ones registered today.

## What breaks

1. **The media is not in the copy.** Most of this project by size is not in git: finished videos, photos, editor
   deliveries, proofs. A worktree would not contain `Claude Ad Videos/`, `photos/`, the editor folders or anything else
   untracked. A video or photo session started in a worktree would not find its inputs, and anything it delivered would
   land in a hidden folder Dan never looks in. Work directories on the Extreme drive use full paths and are unaffected.
2. **The push script refuses worktrees.** `safe-push.sh` is built for the shared folder and exits when run from a
   worktree. A worktree session would push the way Codex does: merge GitHub's main into its own clean copy, then push
   its branch to main with plain git. The rule text in `AGENTS.md` already allows this.
3. **Per-folder things do not follow.** `tmp/`, `node_modules/` and any local scratch files are per folder, so a worktree
   starts without them. Server work needs an install first. Secrets live outside the project and are unaffected. Whether
   project memory is shared with a worktree session needs a one-session test before relying on it.
4. **The status board becomes a copy.** `AI_COORDINATION.md` in a worktree is a snapshot from when the session started.
   A session would have to merge GitHub's main before reading or editing the board. Git then merges two sessions' board
   edits instead of one overwriting the other, which is safer than today, but the board lags by one push.
5. **Clickable files.** The app's file pane opens files inside the session's own folder. A deliverable saved to the main
   folder from a worktree session would not open with one click unless the main folder is added to the session.

## How it fits with the iCloud move

`handoff-20261001-move-project-out-of-icloud.md` should run first. App worktrees live inside the project folder, so
today they sit inside iCloud's Documents sync and would collect the same " 2" duplicate files, including inside git's
own bookkeeping. After the move, every registered worktree path changes, so the move handoff should end with
`git worktree prune` and `git worktree repair`. Starting worktrees before the move adds more paths to fix afterwards.

## Recommendation

Use worktrees for sessions that only touch tracked files: code, site changes, ops, rules, docs, scripts and writing.
Keep video, photo, thumbnail and delivery sessions in the main folder, because their inputs and outputs are not in git.
That split removes most of the shared-file collisions (rule files, `Docs/`, `scripts/`) at almost no disk cost, and the
10-05 tooling covers the media sessions that stay behind. Do it after the iCloud move, not before.

## Question for Dan

After the iCloud move is done, should one session run a one-week trial of worktrees for non-video tasks (it would test
points 2 to 5 on a real task and write the push steps into `AGENTS.md`)? **Yes or no.**
