# Clear space on the M2 and M6 internal drives, 2026-11-17

**Model:** Claude Sonnet 5, medium effort. Run on the M6 (`ssh m2` for the M2). Dan reviewed and fired this; that is his approval for the moves below. Run after, or alongside, the Extreme cleanup handoff (`handoff-20261117-clear-extreme-drive.md`), whose step 1 fixes the nightly jobarchive blocker both Macs share.

## Goal
Both 1 TB internal drives are nearly full: **M6 60 GB free, M2 50 GB free.** New jobs only start on the internal drive with 80 GB+ free, so work is spilling onto the Seagate. Target: **at least 250 GB free on each Mac.**

## What uses the space (2026-11-17)
**M6:** `~/_edit_work` 247 GB (wv-03, wv03-r8: the live Great Again T VSL, KEEP); `~/Projects/_edit_work` 89 GB; `~/Projects/Claude` 103 GB; review pages `~/Library/Application Support/AbsByAI Reviews` 36 GB; caches 7 GB.
**M2:** `~/Projects/_edit_work` 198 GB; `~/Projects` 315 GB total; review pages 29 GB; `~/Downloads` 17 GB; caches 10 GB; Trash 0.8 GB.

## Steps
1. Finished edit folders in `~/Projects/_edit_work` on both Macs: move to the Seagate through `jobarchive.py run` once its blocker is fixed, with the same keep rules as the Extreme handoff (never WV/GAT, JV, DS-98, RO-39, REALDEMOS-B04, anything in editcap/renderq/board ACTIVE or keep.txt). Hash-verified before removal.
2. Retired review pages: `renderq.py prune` and the review-retire tool (memory `review-pages-retire-idle`) on each Mac. Move retired review folders older than 14 days whose video is approved or scheduled to the Seagate (`/Volumes/Expansion/_retired_reviews/<mac>/`), hash-verified. Keep any on the board as waiting on Dan.
3. Find other large items: `du -xh -d 3 ~ | sort -rh | head -40` on each Mac. Inside `~/Projects/Claude` and `~/Projects` look for render leftovers (`tmp/`, `*/frames/`, `*.mov` intermediates, Whisper caches, old `.git` packs via `git gc`). Move work files to the Seagate; delete only true caches and temp frames that a build regenerates.
4. Safe deletes without asking: `~/Library/Caches` app caches, the Trash, `/tmp/absbyai-*` scratch older than 7 days not held by a running process, Homebrew/pip/npm caches (`brew cleanup`, `pip cache purge`, `npm cache clean --force`). Never delete `/tmp/absbyai-renderq` state.
5. M2 `~/Downloads` (17 GB, may hold important files): make TWO verified copies before removing anything from the M2. (a) Copy to the Seagate under `_downloads_archive/m2-20261117/` and re-read every file with a matching SHA-256. (b) Upload the same folder to Google Drive (business Drive, folder `M2 Downloads backup 2026-11-17`), then confirm every file is there with matching size (and MD5 where Drive reports it). Only when BOTH copies verify, remove the folder's contents from the M2. If either copy fails or is incomplete, leave the M2 copy in place and report the exact files. This Drive folder is a private backup: do not set it to public link sharing.
6. Do NOT touch: the iCloud/Documents links (memory `documents-symlinked-into-icloud`), `~/.absbyai-*` config, Codex folders, Photos library, Mail, anything outside the user's home.
7. Report before/after free space per Mac and every item moved or deleted, in `Docs/INTERNAL_DRIVES_CLEANUP_RECEIPT_20261117.md`; push with `scripts/git/safe-push.sh`. Tell Dan in plain words, with the two wrap-up boxes.
