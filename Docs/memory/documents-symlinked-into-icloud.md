---
name: documents-symlinked-into-icloud
description: Since 2026-10-21 every entry of ~/Documents is a symlink into the iCloud container; the project still lives (and syncs) inside iCloud Drive until the move-out handoff runs. Never turn Desktop & Documents sync back on.
metadata:
  node_type: memory
  type: project
  originSessionId: 242c1273-1019-440a-bbcc-4745fb8294a4
  modified: 2026-10-21T20:01:45.045Z
---

On 2026-10-21 Dan turned off iCloud "Desktop & Documents Folders" (the diagnosis found iCloud sync costing a full
core and evicting git objects). macOS 26 emptied `~/Documents` instead of copying files back; the real folders stayed
at `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/`. Paths were restored with symlinks: every entry of
`~/Documents` (60) links into that container, so `/Users/danielrose/Documents/Claude/Projects/Abs By AI` resolves
again, but the project is still inside iCloud Drive and still syncs, with ~8,655 cloud-only placeholder files (40 GB,
mostly Media, plus `.git` objects).

**Why:** turning the setting off was the right call but macOS did not keep local copies; the symlinks are the bridge
until the project is moved out properly (`Handoffs/handoff-20261021-move-project-out-of-icloud.md`).

**How to apply:** never re-enable "Desktop & Documents Folders" (it would merge the container with the links).
`~/Documents/Claude` is a symlink: `rm` it without a trailing slash, never `rm -rf` with one. A git hang in the main
folder is usually a cloud-only object: read the file (`cat > /dev/null`) to force the download; `brctl download` only
queues it. Shell cwd may print as the container path; both paths are the same files. See [[auto-commit-push]].
