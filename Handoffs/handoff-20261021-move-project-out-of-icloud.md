# Handoff: move the project folder out of iCloud Drive (finish what the 10-21 "Desktop & Documents off" started)

Ops, not a video task. Written 2026-10-21 by the "Video editing performance at scale" session (Claude Fable 5.1).
Model for execution: Codex GPT-6.1 Sol, high (ops), or Claude Opus 5.5 high. Needs a quiet moment for the final
rename only (no running render jobs); everything before that is safe while jobs run.

## What happened on 2026-10-21

- The render-throughput diagnosis (`Handoffs/handoff-20261021-render-throughput-plan.md`) found iCloud syncing the
  whole project (`~/Documents` was in iCloud Drive via "Desktop & Documents Folders"): one CPU core all day, and
  evicted git objects (board entry "Main Git cloud read BLOCKED 2026-10-16").
- 14:49: Dan turned "Desktop & Documents Folders" off. macOS 26 did NOT copy the files back: it created an empty
  `~/Documents` and left everything in `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/`. Every absolute
  path in the pipeline (`/Users/danielrose/Documents/Claude/Projects/Abs By AI/...`) broke for a few minutes.
- 14:53: the Phase 1 session and this one restored the paths with symlinks: **every entry of `~/Documents` is now a
  symlink into the iCloud container** (60 links, plus `.localized` and `.stray-Claude-20261021-1449`, a stub a session
  created in the gap; its only content, one sl09 image, was copied back). Old paths resolve again; git, the ffmpeg
  wrapper and `renderq.py status` verified.
- So the project is STILL inside iCloud Drive and still syncs. The CPU cost is not gone yet. And 8,655 files
  (40.4 GB) in it are cloud-only placeholders ("Optimize Mac Storage"): Media 32 GB, `claude edited long form content`
  5.1 GB, `.git` 0.7 GB (2,040 objects), the rest small. The internal disk had 66 GB free.

**Never turn "Desktop & Documents Folders" back on.** It would try to merge the container and the symlinked folder.

## Goal

`~/Documents/Claude/Projects/Abs By AI` is a real folder (or a symlink to a real folder outside iCloud, e.g.
`~/Projects/Abs By AI`), fully local, with nothing in iCloud Drive syncing it. No script path changes.

## Steps

1. **Make `.git` fully local first** (small, removes the git-hang trap). `brctl download` only queues a request; reading
   the file forces it:
   ```bash
   P="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Abs By AI"
   find "$P/.git" -type f -flags +dataless -exec cat {} + > /dev/null
   find "$P/.git" -type f -flags +dataless | wc -l     # must print 0
   cd "$P" && git fsck --connectivity-only
   ```
   (This session started the first two lines at 15:05; check the count before repeating.)
2. **Free internal disk space before downloading the rest.** 40 GB of evicted files on a disk with 66 GB free would
   leave about 26 GB, below the render queue's 50 GB scratch reserve and the swap headroom. Target: at least 150 GB
   free before step 3. Find what fills the 825 GB used (`du -xsh` of the home folder's top-level dirs; the session's
   `du` of Mobile Documents, Pictures, Movies, Application Support, Caches, Containers was still running at handoff
   time). Likely candidates: iCloud Drive content outside the project that "Optimize Mac Storage" keeps local (748 GB
   in Drive), media inside the project that is already on Extreme/Expansion/Seagate/Google Drive (verify by checksum
   before deleting anything; deletions of real footage need Dan's yes).
3. **Materialize the remaining evicted files** the same way (`find "$P" -type f -flags +dataless -exec cat {} + > /dev/null`),
   in chunks per top-level folder, checking free space between chunks. Verify `-flags +dataless` count is 0.
4. **The rename, at a quiet moment** (`renderq.py status` shows nothing running or waiting, no Codex job live):
   ```bash
   mkdir -p ~/Projects
   mv "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude" ~/Projects/Claude   # same volume: instant
   rm ~/Documents/Claude && ln -s ~/Projects/Claude ~/Documents/Claude
   ```
   `mv` out of the container is a rename on the same APFS volume; running processes keep their open files and their
   working directory follows the rename. iCloud then drops its copy (recoverable 30 days in iCloud's Recently Deleted).
   If the mv refuses because of a still-dataless file, go back to step 3.
5. **Verify:** old path lists 87 entries, `git status` works, `renderq.py status` works, `fileproviderd` CPU stays low
   (`ps -o %cpu= -p $(pgrep -x fileproviderd)`), nothing under `~/Documents/Claude` resolves into `Mobile Documents`
   (`readlink -f`). Delete `~/Documents/.stray-Claude-20261021-1449`. Record the result in this file's results section
   and delete the board entry.
6. **Optional, Dan's choice:** the other 59 Documents entries (Codex folders, PDFs) can get the same treatment or stay
   as links; they are small and not on the render path.

## Starter prompt

> Execute `Handoffs/handoff-20261021-move-project-out-of-icloud.md`: make the project's `.git` fully local, free at
> least 150 GB on the internal disk (ask Dan before deleting any real footage), materialize the remaining cloud-only
> files, then at a quiet moment rename the project out of the iCloud container to `~/Projects/Claude` and point
> `~/Documents/Claude` at it. Verify old paths, git and the render queue afterwards and record results in the handoff.
