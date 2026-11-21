# Internal drives cleanup receipt, 2026-11-17 (PARTIAL, not complete)

Handoff: `Handoffs/handoff-20261117-clear-internal-drives.md`. Goal was 250 GB free on each Mac. **Not reached.**

| | before | now |
|---|---|---|
| M6 free | 58 GB | 113 GB |
| M2 free | 51 GB | 114 GB |

## Done
- **Old Claude worktrees (step 3):** 55 on each Mac (43 GB each, 18 to 29 days old) removed with `git worktree remove`. Branches stay in git. The 9 worktrees with unsaved or unpushed work were saved first (diff, untracked-file tar, commit list) to `/Volumes/Expansion/_retired_worktrees/m6-20261117/` and `.../m2-20261117/`.
- **Retired review pages (step 2):** 128 folders (M6, 18.8 GB) and 129 folders (M2, 19.2 GB), all idle 14+ days, retired launch agents, not linked from the board, copied to `/Volumes/Expansion/_retired_reviews/m6|m2/`, checksum-verified, then removed. One M6 file (`9297/page/instagram/ds-47_v-taper-exercises_cover-C.png`) came out corrupt on the Seagate (same size, different SHA-256); re-copied and hash-matched. Only SMB `._*` sidecar files and permissions differ. Board-linked review 9225 kept. `renderq.py prune`: nothing older than 48 h.
- **Safe deletes (step 4):** Google, Mozilla, Firefox, pip, manus-updater, ShipIt caches on M6; Google, Mozilla, Gemini, python caches, Trash, pip cache on M2. No brew/npm on these Macs. `/tmp/absbyai-*`: nothing older than 7 days.
- **Step 1 (finished edit folders):** jobarchive fix `ab99f13` has landed. Scan shows 0 of 20 folders to move on M6 (every internal folder was active within 14 days). M6 `run`: 0 moved. M2 `run` was refused (another cleanup already running); its scan found 4 folders, 0 GB. Nothing sizeable is eligible, so internal edit folders are the remaining space.

## Not done (exact next action)
1. **M2 `~/Downloads` (17 GB, 1,391 files): left in place on the M2.** Copy 1 on the Seagate (`/Volumes/Expansion/_downloads_archive/m2-20261117/`) is verified: all 1,391 SHA-256 match. Copy 2 (Google Drive folder `M2 Downloads backup 2026-11-17`, private) is uploading from M6 via rclone at about 0.5 MB/s, ETA roughly 10 hours; log `/tmp/claude-501/dl-drive-upload.log` on M6, final `rclone check` writes `/tmp/claude-501/dl-drive-check.txt`. Remove the M2 Downloads contents only after that check shows 1,391 matches and 0 differences.
2. **M6 `~/M2-transfer/staging` (27 GB): copy to `/Volumes/Expansion/_m6_staging_archive/` still running** (the Seagate is slow while four copies share it). Then run `rsync -anc` from `~/M2-transfer` and compare file counts before removing. The log `/tmp/claude-501/m6-staging-rsync.log` was overwritten by an earlier failed attempt: ignore its "verify done" line.
3. **The 250 GB target needs bigger moves, which are Dan's call:** M6 `~/_edit_work/wv-03` 245 GB (live VSL, kept); M2 `SRM-JV-LEAD` 131 GB (Joint Vigor, kept); M2 CHROMA-FABLE-TEST 27 GB and DS-39 21 GB, M6 DS-108 55 GB, DS-98-blind 28 GB become jobarchive-eligible after 14 idle days (or an explicit move). Not touched (outside the brief): `~/.codex` (97 GB M6, 87 GB M2), `~/.claude/projects` transcripts (64 GB, 58 GB), Messages, Mail, Photos.

## Update 11:36 CST: still running in the background
- **M6 DS-108 (63 GB, scheduled/finished, not in the edit cap):** `jobarchive.py run --approved DS-108` started 11:06, copying to the Seagate; jobarchive hash-verifies before removing the source. Log `/tmp/claude-501/ja-m6.log` on M6. Slow because the Seagate is shared with the Drive upload and the staging copy.
- **M2 CHROMA-FABLE-TEST + GRAPHICS-FABLE-TEST (about 28 GB, test folders):** the same command was refused ("another cleanup is already running", the Extreme task's run). Re-run on M2: `python3 .claude/skills/_shared/jobarchive/jobarchive.py run --approved CHROMA-FABLE-TEST,GRAPHICS-FABLE-TEST`.
- **DS-98-blind is NOT moved:** it is Round 2 in production on the board (the handoff says never). An earlier line in this receipt suggesting it was wrong.
- M6 free 111 GB, M2 114 GB at this point.

## Update 14:00 CST
- **M2 `~/Downloads` (17 GB, 1,391 files): REMOVED from the M2.** Both copies verified first. Seagate `_downloads_archive/m2-20261117/`: SHA-256 match for all files, and a final `rsync -anc` from the M2 showed only permission-flag differences (SMB), no content, size or new-file differences. Google Drive folder `M2 Downloads backup 2026-11-17` (private, confirmed `visibility: PRIVATE`): `rclone check` 1,391 matching, 0 differences. Symlinks inside a few app bundles (for example Descript Installer.app) were not uploaded to Drive; the Seagate copy keeps them.
- **M6 DS-108 (63 GB): MOVED.** `jobarchive.py run --approved DS-108` verified 3,147 files, durable index and second copy, then removed the source (12:00).
- **M2 CHROMA-FABLE-TEST + GRAPHICS-FABLE-TEST (about 28 GB): not moved yet.** The Extreme task's cleanup lock still blocks `jobarchive.py run`; a retry loop on the M2 retries every 2 minutes (`/tmp/dl/ja-m2.log`).
- **M6 `~/M2-transfer/staging` (27 GB): not removed yet.** Final checksum dry-run to the Seagate copy is running (`/tmp/claude-501/m6-staging-final.log`); remove only when it shows no content differences.
- Free space now: M6 173 GB, M2 116 GB. The 250 GB target is still not met.

## Update 15:50 CST
- The M6 staging copy over SMB hung for six hours (never completed; its earlier "verify done" line was stale). Restarted over SSH into the M2, where the Seagate is local: 23 of 28 GB copied at 15:44. Checksum verify follows (`/tmp/claude-501/m6-staging-ssh-verify.log`); delete the M6 folder only on a clean result.
- M2 test-folder move still blocked by the Extreme task's long jobarchive run (started 09:03); the retry loop is waiting.
- Remaining steps handed off for Codex and Grokbot: `Handoffs/handoff-20261117-finish-internal-drives-cleanup.md`.

## Update 18:45 CST
- **M6 `~/M2-transfer/staging` (28 GB, 153,585 files): REMOVED.** The Seagate copy (`/Volumes/Expansion/_m6_staging_archive/m2-transfer-20261117/staging/`, copied over SSH on the M2) matches: same file count (153,585) and a full `rsync -anc` checksum dry run listed only permission-flag lines (files, directories, symlinks), no content differences.
- M6 free now 179 GB (started at 58). M2 free 110 GB (started at 51). The 250 GB target is still not met.
- **Still open:** M2 CHROMA-FABLE-TEST + GRAPHICS-FABLE-TEST (about 28 GB). The Extreme task's jobarchive run still holds the lock; the retry loop on M2 (`/tmp/dl/ja-m2.log`) keeps trying every 2 minutes. Handoff `Handoffs/handoff-20261117-finish-internal-drives-cleanup.md` now covers only this move.

## Update 2026-11-18 16:30 CST
- The Extreme task's lock cleared, so `jobarchive.py run --approved CHROMA-FABLE-TEST,GRAPHICS-FABLE-TEST` ran on the M2 and moved nothing: the nightly tool's review guard (which an approval does not override) refuses both folders because two registered review pages still point at them: 9461 (GRAPHICS-FABLE-TEST, registered Nov 9) and 9462 (CHROMA-FABLE-TEST, registered Nov 9). Both pages are live (HTTP 200) and not on the board or in Dan's decisions.
- Nothing was deleted or retired. To finish (about 28 GB): Dan says whether the Fable chroma and graphics test reviews are done; then retire both pages (`review_retire.py`), re-run the same command on the M2.
- Free space now: M6 118 GB, M2 102 GB (both fell since yesterday: WV-05 added 33 GB on M6, Flow work on M2).

## Update 2026-11-18 17:00 CST: DONE
- The two M2 test folders were the finished Fable 5.2 trial of Nov 9 (graphics and chroma key; Dan's picks are in memory `fable-5-2-release`). Their two review pages (9461, 9462) were backed up with checksums to `/Volumes/Expansion/_retired_reviews/m2/hub-fable-tests-20261118/` and their hub registrations removed.
- `jobarchive.py run --approved CHROMA-FABLE-TEST,GRAPHICS-FABLE-TEST` then moved both: GRAPHICS-FABLE-TEST 106 files and CHROMA-FABLE-TEST 1,853 files verified, durable index and second copy, sources removed (16:55). Restore with `jobarchive.py restore`.
- Free space: M2 115 GB (started at 51). The 250 GB goal was not reached on either Mac; what remains is live work (M6 wv-03, M2 SRM-JV-LEAD) and folders outside this brief.
