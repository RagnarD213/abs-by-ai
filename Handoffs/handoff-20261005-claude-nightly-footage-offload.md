# Claude handoff: nightly raw footage offload and Seagate check

**Owner requested:** Claude. **Recommended model:** Opus 5.5, high effort. **Date:** 2026-10-05, America/Chicago.

## Goal

Finish the nightly footage routine. Claude should decide when a shoot no longer needs its raw footage because Claude owns most edits and the [Abs By AI Edit Queue](https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs). Keep new footage uploading to Google Drive each night. Move completed shoots to the 24 TB Seagate only after its knocking noise is resolved. The SanDisk Extreme stays the working drive.

## Current state

- The Mac LaunchAgent `com.absbyai.nightly-footage` is installed and enabled. It starts at 8:00 pm Chicago time and retries every 15 minutes until 8:00 am. It runs `scripts/backup/nightly_footage.py` from this project. Logs: `~/Library/Logs/absbyai-footage-offload/`. Status: `python3 scripts/backup/nightly_footage.py --status`.
- Dan reported a weird knocking noise from the new Seagate at about 7:21 pm on October 5. The Seagate volume `/Volumes/Expansion` was safely ejected. Dan must physically disconnect it. Mac Disk Utility reported `SMART Status: Not Supported` through USB, so that is not a health verdict. The drive had been essentially blank, and a small write and read probe passed before the noise report. No shoot footage has been moved to it.
- The file `~/Library/Application Support/Abs By AI/seagate-offload-paused` now blocks every Seagate copy and source removal, even if the disk is reconnected. The nightly job remains enabled for Google Drive uploads. A mocked process test confirmed it does not call the Seagate path or remove source files while this flag exists. Do not remove this flag until the drive is checked or replaced.
- The Codex heartbeat `review-shoots-for-nightly-archive` is PAUSED. Dan prefers Claude to own the archive decisions. Avoid creating a second recurring reviewer without need.
- The welcome-video first shoot has a fresh `READY_TO_ARCHIVE` marker, based on a completed RX-01 roll audit and no pending raw-footage cut. All other shoots remain on Extreme. Current queue blockers: 7/8 has RO-07 and RO-08; 8/3 has RO-04, RO-06, RO-19, RO-20; 8/14 has RO-01 and RO-03; 8/28 has 37 open raw-footage jobs; 9/23 has 13. Recheck live data before changing any marker.
- The queue file is `Handoffs/video-editing/jobs.json`. List 1 contains raw-footage work. Lists 2 and 3 generally use approved masters. `scripts/backup/nightly_footage.py` checks pending List 1 jobs by shoot date and roll, and treats `finalized`, `uploaded`, and `cancelled` as complete. It requires a `READY_TO_ARCHIVE` marker refreshed within 24 hours and checks the queue and marker again before removing raw files.
- The current Google Drive remote is `gdrive:`. A small upload and checksum test succeeded, but rclone warns that its shared Google client ID will stop working during 2026. The welcome shoot is not yet on Drive. Cloud copy must pass before any Extreme removal.
- Commits through `07a70cb` are pushed to main. The last changes may still be deploying on Railway. Verify the latest deployment and `https://absbyai.com` before closing this task. The code and instructions are in `scripts/backup/nightly_footage.py` and `scripts/backup/README.md`.

## Next actions

1. Help Dan identify the sound. Occasional soft seek clicks can be normal, but repeated hard knocks, clunks, grinding, or spin-up cycles are a reason to stop using a new drive and exchange it. Ask for a short recording if the distinction is unclear. After ejection, check that its original power adapter and USB cable are fully seated, connect directly to a Mac USB-A port, and put it on a stable surface. Do only a brief listening check. If repeated knocking persists, recommend returning or exchanging it. Do not run a long write test on a drive making hard knocks.
2. If the sound proves normal, run a non-destructive test before putting footage on it. Disk Utility First Aid checks the filesystem, not the mechanics. Seagate's SeaTools diagnostic is available for Windows, not macOS. A Windows short test followed by a longer test is an option; if unavailable, use a test copy plus checksum on the Mac and listen for noise and disconnects. Keep the Extreme copy throughout. Seagate guidance: https://www.seagate.com/em/en/support/kb/identifying-hard-drive-sounds-and-determining-what-they-mean/ and https://www.seagate.com/support/kb/what-should-i-do-for-a-noisy-disk-drive-193731en/.
3. Make Claude the archive decision owner in the edit workflow. At completion of each raw-footage cut, review all List 1 jobs from that shoot plus active handoffs and unqueued videos. When none still needs the source, create or refresh `READY_TO_ARCHIVE` inside the existing shoot folder on Extreme. Remove that marker if new work needs the footage. Never rename a shoot folder because edit plans use exact paths. A shoot missing from the queue is not automatically ready.
4. Update `scripts/backup/README.md` to reflect Claude ownership and the Seagate pause. If the disk checks out or is replaced, remove `seagate-offload-paused`, verify the intended disk identity and volume name, run `--dry-run`, and then observe the first actual offload. The script verifies both Seagate and Google Drive copies before removing raw files from Extreme. If a replacement disk is mounted as `Expansion`, review the archive identity marker and saved state first.
5. Confirm the 8 pm cloud-only run actually uploads missing files and preserves Extreme footage. If the Google shared client ID hits a quota error, set up a personal rclone Google client ID before relying on the cloud copy. Keep Dan informed if the upload needs another night.

## Project delivery rules

Use simple language with Dan. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and `AI_COORDINATION.md` before changing this workflow. Do not use em dashes or en dashes in new writing. In the main project folder, push only task files with `scripts/git/safe-push.sh -m "message" -- <files>`. Push shared files as soon as edited. Verify Railway and the live site after code changes. Do not read or update the paused Victory Dashboard.

## Starter prompt

Finish `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`. Own the shoot archive decision from the Abs By AI Edit Queue and active video work, assess the Seagate knocking before any archive writes, keep the Google Drive nightly backup working, and verify the first safe run. Use Claude Opus 5.5 at high effort. Keep source footage on Extreme until both destinations pass checksum checks.
