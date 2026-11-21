# Clear the 8/28 raw shoot off the Extreme drive (M2), written 2026-11-17

**Run only after both edits that hold this shoot are finished and Dan has approved them: DS-25 "How To Do M100s" and RO-09 "Pushup Masterclass: 6 Levels From Beginner To Advanced".** Dan cancelled the five 8/28 ads (RA-02, RA-03, RA-08, RA-10, RA-11) on 2026-11-17 and removed them from the edit queue, so nothing else needs this footage. Model: Claude Sonnet 5.5, medium effort. Run on the M6, drive commands over the SSH connection `m2`. Sidebar name: `Clear 8-28 Shoot Setup`.

## Goal
Remove `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/` (229 GB) from the Extreme, with every file safe on **both** the Seagate (`/Volumes/Expansion`) and Google Drive (`gdrive_backup:Abs By AI Raw Footage/...`). Dan: "Put it on the Seagate and Google Drive."

## Gate (stop and report if any fails; never remove on a guess)
1. `python3 -c` the `pending_jobs()` logic in `scripts/backup/nightly_footage.py` for this shoot (or read `Handoffs/video-editing/jobs.json`): every list-1 job whose roll or file names 8/28 must be `finalized` or `uploaded` (or gone). DS-25 and RO-09 must be finalized by Dan's words. If one is not, stop and say which.
2. `python3 scripts/backup/nightly_footage.py --status`: the shoot's current inventory fingerprint must equal the recorded one (`7bfa7435...`, state file `~/Library/Application Support/Abs By AI/nightly-footage.json` on the M2) with `seagate_verified` and `drive_verified` set. If the footage changed (new or edited files), run `--copy-only-seagate` then `--copy-only-drive` (8 pm to 8 am Chicago window) and start again.
3. DS-25 also takes B-roll from the 10/15 shoot (C1736) and RO-09 takes C1732 from the 10/15 shoot: those stay where they are; this handoff only moves the 8/28 folder.

## Steps
1. Make every edit's source path survive. Edit plans hold exact paths into this folder (`main camera/`, `regular gopro 1/`, `regular gopro 2/`, `360 gopro/`). Do not rename the folder. After removal, those paths will not exist, so for DS-25, RO-09 and every finished 8/28 job note, add a pointer in the job's `notes` or the shoot's receipt: "raw footage restored from `/Volumes/Expansion/Abs By AI Raw Footage/<folder>/` or Drive `Abs By AI Raw Footage/<folder>`". Also search `.claude/skills`, `scripts/` and `Media/clip-library/catalog.json` for the folder name and list any live reference (clip-library `source_path` is provenance only, the permanent copies live under `_asset_library_stage`).
2. Independent re-read, the Seagate has corrupted copies before (Nov 1 to 3): SHA-256 every file under the Extreme folder and the same relative file on the Seagate (`/Volumes/Expansion/Abs By AI Raw Footage/<folder>/`); they must all match, same file count and byte total. Then `rclone check` (hash compare) the Extreme folder against Drive. Save both receipts to `/Volumes/Extreme/_backup-receipts/` and `Docs/`.
3. Only if every file matched on both: remove the Extreme files **by that verified list**, never `rm -rf` a path that is not the verified shoot folder. Leave `RAW_FOOTAGE_ARCHIVED.txt` in the (now empty) folder with the date, the Seagate path, the Drive folder, file count, byte total, and how to restore (rclone copy back, or copy from the Seagate, then SHA-256 compare).
4. `python3 scripts/backup/nightly_footage.py --status` must still list the shoot verified. Record free space before and after (`df -h /Volumes/Extreme`).
5. Receipt `Docs/CLEAR_828_SHOOT_RECEIPT_<date>.md`, push with `scripts/git/safe-push.sh`, one short board line if the board entry is still wanted.

## Hard rules
Never remove a source before every file is re-read from the Seagate and compared on Drive. Never touch another shoot, an active job (`editcap.py status`, `renderq.py status`, `AI_COORDINATION.md` ACTIVE), the clip library or the 10/15 rolls. Standing permission: Dan has authorized this move (2026-11-17); no extra approval needed once the gate passes.
