# Nightly raw footage backup and offload

When enabled, `nightly_footage.py` checks every 15 minutes. It transfers only between 8 pm and
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

A ready shoot is first copied to Google Drive and checksum-checked, then copied
to Seagate Expansion and checksum-checked. Rclone checks every raw file against
both copies again immediately before the source files are removed from Extreme. A
failed or incomplete transfer leaves source footage in place and retries the
next night. The Seagate has a disk identity marker so a different drive mounted
under the same name cannot receive the archive. An `RAW_FOOTAGE_ARCHIVED.txt`
receipt remains in the source folder after a successful offload.

As of 2026-10-08, automatic offload and Extreme removal remain paused. The flag
at `~/Library/Application Support/Abs By AI/seagate-offload-paused` remains in
place. The old LaunchAgent is disabled because macOS denied its background
process access to Extreme. A Codex heartbeat at 8 pm Chicago time now runs
`--copy-only-seagate`, then `--copy-only-drive` when the Seagate check finishes.
Both modes retain every Extreme original. On October 7, all six shoots, 846
files and 916.2 GB, were checksum verified on Seagate. Drive verification is
still pending. See
`Handoffs/handoff-20261005-claude-nightly-footage-offload.md`.

Commands from the project root:

```sh
python3 scripts/backup/nightly_footage.py --dry-run
python3 scripts/backup/nightly_footage.py --status
python3 scripts/backup/nightly_footage.py --install
python3 scripts/backup/nightly_footage.py --copy-only-seagate
python3 scripts/backup/nightly_footage.py --copy-only-drive
```

`--copy-only-seagate` copies and checksum-checks raw files from every shoot
folder. It never removes files from Extreme, even when a shoot has a
`READY_TO_ARCHIVE` marker. It may run between 8 pm and 8 am Chicago time. The
first run checks all six existing shoots; later runs skip a shoot whose source
inventory has not changed since its verified Seagate copy. The
`seagate-offload-paused` flag remains in place and continues to prevent the
normal offload path from deleting source footage. Before any future source
removal, that path rechecks the Seagate and Google Drive copies against Extreme.

`--copy-only-drive` uses the same overnight window and source inventory. It
uploads missing raw footage to Google Drive, compares file checksums against
Extreme, and records a verified shoot only after the source inventory remains
unchanged. It cannot remove Extreme footage. New shoot folders get an
anyone-with-link viewing link. The nightly Codex task runs this after the
Seagate check, so the jobs share a lock and never transfer concurrently.

The disabled Mac LaunchAgent is named `com.absbyai.nightly-footage`. Its old
logs are under `~/Library/Logs/absbyai-footage-offload/`. The active schedule is
the Codex heartbeat `nightly-seagate-copy-verification`.

The configured `gdrive:` rclone remote currently uses rclone's shared Google
client ID. A 1 MB upload and checksum test passed on 2026-10-08, but a previous
large upload hit the shared client's quota. Rclone says the shared ID will stop
working during 2026. Replace it with a dedicated client ID before relying on
long uploads; do not treat failed cloud checks as a backup.
