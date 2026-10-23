---
name: documents-symlinked-into-icloud
description: Since 2026-10-23 the Claude folder (all projects, incl. Abs By AI) lives at ~/Projects/Claude, fully local and out of iCloud; ~/Documents/Claude and the old iCloud-container path are symlinks to it. Never turn Desktop & Documents sync back on.
metadata:
  type: project
  modified: 2026-10-23T07:30:00Z
---

On 2026-10-21 Dan turned off iCloud "Desktop & Documents Folders"; macOS left the real folders in
`~/Library/Mobile Documents/com~apple~CloudDocs/Documents/` and every entry of `~/Documents` became a symlink into
that container. On 2026-10-23 07:16 the Claude folder was moved out of iCloud to `~/Projects/Claude` (every file
downloaded first; moved piece by piece with `scripts/icloud-move/evacuate.py`, a symlink left at each old path).

Now: `~/Documents/Claude -> ~/Projects/Claude`, and the container path
`~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude -> ~/Projects/Claude` (kept for sessions and
worktrees that recorded it). Both old paths open the same real folder. The other 59 `~/Documents` entries are still
links into the iCloud container (small, off the render path).

**Why:** iCloud sync cost a CPU core all day (fileproviderd 85% before, ~3% after) and evicted git objects.

**How to apply:** never re-enable "Desktop & Documents Folders". `~/Documents/Claude` is a symlink: `rm` it without
a trailing slash, never `rm -rf` with one. Do not move anything back into iCloud Drive. A file in iCloud that will
not download: `brctl download <file>` and wait; if bird stalls for an hour, `killall bird` (it restarts) unstuck it.
A rename out of iCloud fails with "Operation timed out" if the folder changes meanwhile; nothing moves, retry.
Results: `Handoffs/handoff-20261021-move-project-out-of-icloud.md`. See [[auto-commit-push]].
