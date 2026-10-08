# Claude handoff: nightly raw footage offload and Seagate check

**Owner requested:** Claude. **Recommended model:** Opus 5.5, high effort. **Date:** 2026-10-05, America/Chicago.

## Goal

Finish the nightly footage routine. Claude should decide when a shoot no longer needs its raw footage because Claude owns most edits and the [Abs By AI Edit Queue](https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs). Keep new footage uploading to Google Drive each night. The SanDisk Extreme stays the working drive.

## Dan's October 7 decision

- The October 7 copy finished at 10:47 pm CDT with exit code 0. All six shoots, 846 raw files and 916.2 GB, passed file checksum checks on Seagate against Extreme. All Extreme originals remain. Dan authorized this copy despite the occasional unresolved soft knocking sound. Stop using the Seagate if it develops repeated hard knocks, clunks, grinding, or disconnections.
- The Codex heartbeat `nightly-seagate-copy-verification` remains ACTIVE at 8 pm America/Chicago for new or changed shoots. It runs `python3 scripts/backup/nightly_footage.py --copy-only-seagate`, then `--copy-only-drive` after the Seagate check. Both modes checksum each shoot, skip unchanged verified shoots, and contain no source removal. The one-time access test and the extra overnight monitor are PAUSED after passing and completing.
- Keep `~/Library/Application Support/Abs By AI/seagate-offload-paused` in place. No Extreme deletion is authorized for now. After Dan's next shoot, the permanent order for any later offload is: copy to Google Drive and verify against Extreme, copy to Seagate and verify against Extreme, then recheck both before removing anything from Extreme. If either check fails or the shoot still has an active raw-footage edit, retain Extreme files. The normal offload code now enforces this order, but remains paused.
- The old Google Drive LaunchAgent remains disabled by macOS removable-volume permissions. The Codex heartbeat runs the safe Drive copy directly each night. Its first full verification is pending. On October 8, Codex created a dedicated Google Drive OAuth client and the `gdrive_backup:` rclone remote. A 1 MB upload and checksum test passed. A small XML file from the 9/23 shoot also uploaded to its actual Drive folder and matched the Extreme checksum. No complete shoot has a current `drive_verified` state yet.

## Current state

- The Mac LaunchAgent `com.absbyai.nightly-footage` is installed but DISABLED. After Extreme was reconnected at 9:21 pm October 5, macOS denied its background Python process access to `/Volumes/Extreme`. The Codex scheduled task can read both drives and now handles Drive uploads directly. Logs from the old agent: `~/Library/Logs/absbyai-footage-offload/`.
- Dan reported a weird knocking noise from the new Seagate at about 7:21 pm on October 5. It was ejected, then remounted at Dan's request for a manual copy. Mac Disk Utility reported `SMART Status: Not Supported` through USB, so that is not a health verdict. At 9:48 pm, a manual rclone copy and whole-shoot checksum check completed for the welcome shoot: 12 matching raw files, 0 differences, 122.8 GB. The first copy attempt had two transient `errno -1` errors; rclone's second attempt succeeded. The source files remain on Extreme. The Seagate's noise has not yet been assessed, so do not treat this as a trusted archive.
- The file `~/Library/Application Support/Abs By AI/seagate-offload-paused` still blocks the normal offload and source removal. The new copy-only mode bypasses this flag without deleting anything. The October 5 manual copy also retained all originals. Manual copy script: `~/Library/Application Support/Abs By AI/manual-seagate-copy-20261005.sh`. Verification log: `~/Library/Logs/absbyai-footage-offload/seagate-copy-screen.log`.
- The Codex heartbeat `review-shoots-for-nightly-archive` is PAUSED. Dan prefers Claude to own the archive decisions. Avoid creating a second recurring reviewer without need.
- The welcome-video first shoot has a fresh `READY_TO_ARCHIVE` marker, based on a completed RX-01 roll audit and no pending raw-footage cut. All other shoots remain on Extreme. Current queue blockers: 7/8 has RO-07 and RO-08; 8/3 has RO-04, RO-06, RO-19, RO-20; 8/14 has RO-01 and RO-03; 8/28 has 37 open raw-footage jobs; 9/23 has 13. Recheck live data before changing any marker.
- The queue file is `Handoffs/video-editing/jobs.json`. List 1 contains raw-footage work. Lists 2 and 3 generally use approved masters. `scripts/backup/nightly_footage.py` checks pending List 1 jobs by shoot date and roll, and treats `finalized`, `uploaded`, and `cancelled` as complete. It requires a `READY_TO_ARCHIVE` marker refreshed within 24 hours and checks the queue and marker again before removing raw files.
- The footage script now uses `gdrive_backup:Abs By AI Raw Footage`. The existing `gdrive:` remote remains configured for other workflows. The dedicated client is authorized, can list existing Drive folders, and passed synthetic and real raw-file checksum tests. The switch was pushed in commit `032aeb6`. The first full cloud run is pending. Cloud copy must pass before any Extreme removal.
- The code and instructions are in `scripts/backup/nightly_footage.py` and `scripts/backup/README.md`. Verify the live site after code changes.

## Next actions

1. Monitor tonight's copy-only run and checksum results. Keep Extreme originals. If the drive begins repeated hard knocks, clunks, grinding, or disconnecting, stop the copy and recommend replacement. Seagate guidance: https://www.seagate.com/support/kb/identifying-hard-drive-sounds-and-determining-what-they-mean/ and https://www.seagate.com/support/kb/what-should-i-do-for-a-noisy-disk-drive-193731en/.
2. A 4 GB write and read test passed on October 6. Disk Utility checks passed earlier, but First Aid cannot rule out a mechanical fault. A Yeti microphone recording was made but did not establish the source of the sound. The 122.8 GB welcome shoot was copied and checksum-verified on October 5, with originals retained.
3. Make Claude the archive decision owner in the edit workflow. At completion of each raw-footage cut, review all List 1 jobs from that shoot plus active handoffs and unqueued videos. When none still needs the source, create or refresh `READY_TO_ARCHIVE` inside the existing shoot folder on Extreme. Remove that marker if new work needs the footage. Never rename a shoot folder because edit plans use exact paths. A shoot missing from the queue is not automatically ready.
4. Keep the Seagate pause flag until Dan explicitly authorizes source removal after his next shoot. When that time comes, verify the disk identity, Drive copy, Seagate copy, active edit queue, and source snapshot before the first deletion. If a replacement disk is mounted as `Expansion`, review the archive identity marker and saved state first.
5. Monitor the first nightly Drive run until each of the six shoots has a current `drive_verified` state. Large uploads may need several nights. Confirm all Extreme originals remain and report actual completed shoot counts to Dan.

## Project delivery rules

Use simple language with Dan. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and `AI_COORDINATION.md` before changing this workflow. Do not use em dashes or en dashes in new writing. In the main project folder, push only task files with `scripts/git/safe-push.sh -m "message" -- <files>`. Push shared files as soon as edited. Verify Railway and the live site after code changes. Do not read or update the paused Victory Dashboard.

## Starter prompt

Finish `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`. Own the shoot archive decision from the Abs By AI Edit Queue and active video work. The 8 pm Codex routine copies and checksums raw footage to Seagate and Google Drive while retaining every Extreme original. The dedicated `gdrive_backup:` connection passed small upload and checksum tests; monitor the first full cloud run. After Dan's next shoot, retain the hard order of Google Drive verification, Seagate verification, then source removal only for finished shoots. Use Claude Opus 5.5 at high effort.
