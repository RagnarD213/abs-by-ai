# Nightly raw footage backup and offload

`nightly_footage.py` checks every 15 minutes. It transfers only between 8 pm and
8 am Chicago time. The Mac mini, Extreme, Seagate Expansion, and internet must
remain available overnight. The Mac must stay awake while the job runs.

Each shoot's original video, audio, camera XML, and camera proxy files are copied
to Google Drive. The existing Drive folders are reused for the 7/8, 8/3, 8/14,
and 8/28 shoots. New shoot folders under Extreme are discovered automatically.
Edited films, render folders, and the `_edit_work` scratch area are excluded.

The Codex automation `Review shoots for nightly archive` is paused. Claude
now owns the archive decision because it maintains the edit queue. It should
check `Handoffs/video-editing/jobs.json`, the edit queue artifact, active
handoffs, the coordination board, and shoot notes. A
shoot is ready only when no remaining video cut or active review needs its raw
footage. Finalized and uploaded cuts count as complete. New or ambiguous shoots
stay on Extreme. The review refreshes a `READY_TO_ARCHIVE` file inside each
ready shoot folder and removes that file if later work needs the raw footage.
The offload job accepts only decisions refreshed within the last 24 hours and
checks the queue and marker again before removing source files. Do not rename
shoot folders: edit plans contain exact source paths. The welcome-video first
shoot was marked ready on 2026-10-05 after the queue audit found no pending cut.

A ready shoot is copied to Seagate Expansion and Drive. Rclone checks every raw
file against both copies before the source files are removed from Extreme. A
failed or incomplete transfer leaves source footage in place and retries the
next night. The Seagate has a disk identity marker so a different drive mounted
under the same name cannot receive the archive. An `RAW_FOOTAGE_ARCHIVED.txt`
receipt remains in the source folder after a successful offload.

As of 2026-10-05, Seagate offload is paused because the new drive made a
knocking noise. The flag at `~/Library/Application Support/Abs By AI/seagate-offload-paused`
blocks Seagate copies and Extreme removal while letting Google Drive uploads
continue. Leave this flag in place until the Seagate is checked or replaced.

Commands from the project root:

```sh
python3 scripts/backup/nightly_footage.py --dry-run
python3 scripts/backup/nightly_footage.py --status
python3 scripts/backup/nightly_footage.py --install
```

The schedule is a Mac LaunchAgent named `com.absbyai.nightly-footage`. Logs are
under `~/Library/Logs/absbyai-footage-offload/`. To stop it, run
`launchctl bootout gui/$(id -u)/com.absbyai.nightly-footage`. The launch agent
file is at `~/Library/LaunchAgents/com.absbyai.nightly-footage.plist`.

The configured `gdrive:` rclone remote currently uses rclone's shared Google
client ID. It worked in an upload and checksum test on 2026-10-05, but rclone
says the shared ID will stop working during 2026. Replace it with a personal
client ID before that happens; do not treat failed cloud checks as a backup.
