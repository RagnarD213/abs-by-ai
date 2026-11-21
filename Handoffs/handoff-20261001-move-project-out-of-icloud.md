# Handoff: get the Abs By AI project out of iCloud's Documents sync

Written 2026-10-01 by Claude (Opus 5.5). Not executed. Run it on Dan's Mac, in the main project folder, at a time when
nothing else is running there. Recommended: **Claude Opus 5.5, high effort** (it moves 304 GB of work that has no backup).

## The problem in plain language

Dan's Mac has iCloud's "Desktop & Documents Folders" switched on, and this project lives inside Documents. iCloud is
built for letters and spreadsheets, not for a folder that dozens of programs write to all day. When two writes collide it
keeps both and names the second one "something 2", then "something 3". It also removes files from the Mac to save space
and leaves only a cloud copy. In this project that has:

- made about 109,000 duplicate-looking files and folders,
- destroyed the iPhone app project (see `handoff-20261001-rebuild-ios-project.md`),
- left 199 files that exist only in iCloud, including copies of git's own index file.

## Measured state, 2026-10-01 (re-measure before acting)

| what | value | how |
|---|---|---|
| Desktop & Documents sync | ON | `defaults read com.apple.finder FXICloudDriveDocuments` = 1 (Desktop = 1 too); macOS 26.5.2 |
| Project folder | `/Users/danielrose/Documents/Claude/Projects/Abs By AI`, **304 GB**, `.git` 23 GB | `du -sh` |
| Free disk | **59 GB** (94% used) | `df -h /System/Volumes/Data` |
| iCloud space left | about 1.09 TB | `brctl quota` |
| Duplicate-pattern items (outside `.git`, `node_modules`) | **109,481**: 79,564 in `app-store-assets/` (21 GB), 24,841 in `ios-app/`, 2,294 in `YouTube Long Form Video Content/`, 1,410 in `Muhammad Ad Videos/`, the rest scattered | `find` for names ending in ` N` or ` N.ext` |
| Duplicates inside `.git` | 40 (for example `.git/index 9`, `index 10`, `index 11`) | `find .git -name "* [0-9]*"` |
| Cloud-only files (not on the Mac) | **199** | `find . -type f -flags +dataless` |
| Git worktrees registered | 15 | `git worktree list` |
| Backups | none (no Time Machine destination) | `tmutil destinationinfo` |

Warning on the duplicate count: the name pattern also matches real files such as `... Ad 14.mp4`. A file is a duplicate
only if a file with the same name minus the number sits next to it. Never delete by name pattern alone.

## Why not simply switch the setting off

Switching off Desktop & Documents does not leave the files where they are. macOS removes everything in Documents and
Desktop from the Mac and keeps it in iCloud Drive; getting it back means downloading it again. With a 304 GB project,
59 GB free and no backup, that is the risky path, and every running session would lose its folder while it happens.
The setting is also Dan's own system setting: an agent may not change it.

**The fix in this handoff is narrower and safe: move this one project out of the synced area.** A move on the same disk
is an instant rename; nothing is copied or downloaded. A shortcut (symlink) left at the old location keeps every saved
path working. Whether to switch the setting off for the rest of Documents stays Dan's separate decision (see the end).

## Preconditions (all must hold; otherwise stop and tell Dan)

1. No Claude or Codex session, render, upload, dev server or scheduled task is running in the project:
   `ps -Ao pid,etime,command | grep -E "ffmpeg|render|whisper|node server|qc_style|hyperframes" | grep -v grep`, the
   Claude and Codex apps' session lists, and `mcp__scheduled-tasks__list_scheduled_tasks` for anything due in the next hour.
2. `Handoffs/handoff-20260930-fix-stuck-main-checkout.md` is not mid-run. Either order is fine; never both at once.
3. The Extreme drive's state does not matter (edit work there only refers to this folder by path).

## Steps

### 1. Record the starting state

`git status -sb | head -1`, `git rev-parse HEAD`, `git stash list`, `git worktree list`, the file count
(`find . -type f | wc -l`) and `du -sk .`. Save them in the scratchpad; step 4 compares against them.

### 2. Bring every cloud-only file back onto the Mac

A cloud-only file is a placeholder. Moving the folder out of iCloud while placeholders remain can lose them.

```bash
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
find . -type f -flags +dataless -print0 | xargs -0 -n 20 brctl download
```

First add up their real sizes (`stat -f %z`) and confirm the total fits in the free space with 10 GB to spare. Repeat the
`find` until it returns nothing. If any file will not download after three tries, stop and report its path: do not move.

### 3. Rehearse on a scratch folder

Make `Documents/Claude/Projects/_icloud-move-test/` with a few files, wait for the cloud icon to settle, then run the
same `mv` + `ln -s` as step 4 on it. Confirm the files arrive intact, the symlink resolves, and no error appears. Delete
the test folder and its symlink afterwards.

### 4. Move the project and leave a shortcut, in one command

```bash
mkdir -p "$HOME/Projects" && \
mv "$HOME/Documents/Claude/Projects/Abs By AI" "$HOME/Projects/Abs By AI" && \
ln -s "$HOME/Projects/Abs By AI" "$HOME/Documents/Claude/Projects/Abs By AI"
```

Then prove nothing changed: the step 1 numbers match (file count, size, HEAD, status line, stash list),
`git worktree list` still lists 15 (run `git worktree repair` if any shows as missing), `git fsck --no-dangling` is clean.
iCloud will treat the old copy as deleted and keep it in its own Recently Deleted for 30 days: a free safety net.

### 5. Prove every saved path still works through the shortcut

- Start a fresh Claude session from the old path. `MEMORY.md`, `CLAUDE.md` and `AI_COORDINATION.md` must load. If the
  app keys the project by the new real path instead, link the memory folder:
  `ln -s ~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI ~/.claude/projects/-Users-danielrose-Projects-Abs-By-AI`.
- `.claude/launch.json` preview server starts. One Codex worktree runs `git status`. One scheduled task shows its path
  resolving (`grep -rl "Documents/Claude/Projects/Abs By AI" ~/Library/LaunchAgents ~/.codex 2>/dev/null | head`).
- `scripts/native-smoke-test.sh android` with `SMOKE_USE_EMULATOR=1` still passes (it writes into the project folder).

### 6. Prove iCloud has let go

Create `~/Projects/Abs By AI/_sync-check.txt`. After ten minutes it must show no cloud status
(`brctl status` lists nothing under `Projects`, `xattr -l` shows no `com.apple.file-provider` attribute) and no new
numbered copy may have appeared anywhere in the project. Delete the check file.

### 7. Clean up the duplicates (after the move, so iCloud cannot make more)

Write a script that, for every item whose name ends in ` N` or ` N.ext`, finds the base name beside it and sorts it into:

- **A. base exists and the bytes are identical** (`cmp`; for folders, a recursive compare): a true duplicate.
- **B. base exists but the content differs**: keep both, list them for a person to look at.
- **C. no base beside it**: not a duplicate by this rule (this is where `Ad 14.mp4` lands). Leave it alone, except
  `ios-app/`, which belongs to the iOS rebuild handoff.

Move class A to `~/Projects/_icloud-duplicates-quarantine/` keeping the folder structure (a rename, so it costs no space
and is reversible). Inside `.git`, treat only the 40 numbered copies, and run `git fsck` before and after.

Then ask Dan **once**, with the count and the gigabytes, whether to delete the quarantine for good (batch approval rule;
this is the only destructive step). `app-store-assets/` alone should free most of 21 GB.

### 8. Close out

- Memory: add a note that the project really lives at `~/Projects/Abs By AI` with a shortcut at the old path, and why.
  Update `github-push-false-failure` (its "iCloud duplicate" paragraph is now solved).
- Delete this handoff's lines from `AI_COORDINATION.md` and `Handoffs/README.md`. Report in chat with the numbers.

## Out of scope

Switching the system setting off, anything else in Documents, the stuck checkout, rebuilding the iPhone project.

## For Dan, only if he wants iCloud out of Documents entirely (optional, after this handoff)

System Settings, your name, iCloud, Drive, turn off **Desktop & Documents Folders**. macOS will warn that the files
leave the Mac and stay in iCloud Drive; you then drag them back from iCloud Drive into Documents. Do it only after this
handoff has run, with nothing else running, and expect a long download for whatever is still in Documents.

## Starter prompt

> Read `Handoffs/handoff-20261001-move-project-out-of-icloud.md` in full, then move the Abs By AI project out of iCloud's
> Documents sync exactly as written: re-measure, download the cloud-only files, rehearse on a scratch folder, move the
> project to ~/Projects with a shortcut at the old path, prove every saved path still works, prove iCloud has let go,
> then quarantine the true duplicates and ask me once before deleting them. Stop and tell me if any precondition fails.

Recommended model: **Claude Opus 5.5, high effort.**
