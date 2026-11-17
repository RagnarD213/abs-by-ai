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
