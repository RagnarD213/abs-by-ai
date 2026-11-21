# Clear the 9/23 raw shoot off the Extreme drive (M2), written 2026-11-17

**Run only after the three edits that hold this shoot are finished and Dan has approved them: DS-32 "AI Job", DS-26 "Wispr Flow" and DS-29 "Robot Lawn Mower".** Dan cancelled VSL 2 (WV-02, the /start landing-page video) on 2026-11-17 and removed it from the edit queue. The finished 9/23 films (RO-18 and the others) are already approved; the Shorts cut from them (SL-23, SL-25, SL-37) use the finished masters, not this raw footage. Model: Claude Sonnet 5.5, medium effort, run on the M6 with drive commands over SSH `m2`. Sidebar name: `Clear 9-23 Shoot Setup`.

## Goal
Remove `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/` (195 GB) from the Extreme, with every file safe on **both** the Seagate (`/Volumes/Expansion/Abs By AI Raw Footage/...`) and Google Drive (`gdrive_backup:Abs By AI Raw Footage/...`).

## Gate (stop and report on any failure)
1. Queue check: every list-1 job naming 9/23 or the folder is `finalized`/`uploaded` or gone (`pending_jobs()` in `scripts/backup/nightly_footage.py`, or `Handoffs/video-editing/jobs.json`). The finalized 9/23 jobs include RO-14, RO-15, RO-18, DS-30 and the rest; the three above must be finalized by Dan's words.
2. `python3 scripts/backup/nightly_footage.py --status`: the current inventory fingerprint must equal the recorded one (`206f58a0...`) with `seagate_verified` (2026-10-07) and `drive_verified` (2026-10-09) set. If the footage changed, run `--copy-only-seagate` then `--copy-only-drive` (8 pm to 8 am Chicago) and begin again.
3. This footage feeds finished films whose build folders (`RO-14`, `RO-15`, `RO-18` and others under `_edit_work`) hold exact paths into this folder. Do not rename the folder. Before removal, list every live reference (build folders, `.claude/skills`, `scripts/`, the clip-library `source_path` fields, which are provenance only). Do not touch RO-18's folder: its mower and Wispr assets live in `/Volumes/Expansion/_edit_work/RO-18/` already (clip library B0726-B0731 hold the permanent copies).

## Steps
Same as the 8/28 handoff (`Handoffs/handoff-20261117-clear-828-shoot-from-extreme.md`): (1) leave restore pointers for every edit that names this folder; (2) re-read every file from the Seagate with SHA-256 and `rclone check` against Drive, save the receipts; (3) remove the Extreme files only by that verified list, never `rm -rf` anything else, leaving `RAW_FOOTAGE_ARCHIVED.txt` with the Seagate path, Drive folder, count, bytes and restore steps; (4) `--status` still verified, free space before and after; (5) receipt `Docs/CLEAR_923_SHOOT_RECEIPT_<date>.md`, `scripts/git/safe-push.sh`.

## Hard rules
Never remove a source before every file is verified on both copies. Never touch another shoot, an active job, the clip library or other edit folders. Dan authorized this move (2026-11-17); no extra approval once the gate passes.
