# Nightly cleanup of finished edit folders (jobarchive)

Dan, 2026-11-14: keep both Macs' fast drives free so edits always run on the internal drive or the Extreme.

Every night at 2:15 AM a LaunchAgent (`com.absbyai.jobarchive`) on each Mac runs `jobarchive.py run --until 8`:
- It looks at `~/Projects/_edit_work`, `~/_edit_work` and, on the Mac the Extreme is plugged into (the M2),
  `/Volumes/Extreme/_edit_work`. Drives shared over the cable (the M6's SMB mounts) are left to the M2.
- It moves a folder to `/Volumes/Expansion/_finished_edit_jobs/<mac>-<drive>/<JOB>/` only when nothing in it
  changed for 14 days and nothing still uses it (see the script's docstring for every keep rule: edit cap,
  render queue, running processes, review on the board or edit cap, keep.txt, and any skill, script, rule
  or clip-library catalog that points at it).
- It removes the original only after every file is re-read from the Seagate (bypassing the disk cache) with a
  matching SHA-256. Symlinks are listed in the job's `.jobarchive-manifest.json`, not copied (exFAT).
- It warns (log + Mac notification on the M6) when a drive drops under 150 GB free.

Commands: `scan` (dry run), `run`, `list`, `restore JOB [--to DIR]`, `install`, `selftest`.
The LaunchAgent runs a private copy at `~/.absbyai-jobarchive/jobarchive.py`; after editing the script, re-run
`install` on each Mac (`scp` it to the M2 first). Log: `~/.absbyai-jobarchive/jobarchive.log`.

To keep a folder forever, add its name to `keep.txt` beside this file.

## Safety repair, November 14, 2026

The installed program pins the actual Expansion volume UUID at installation. It checks that identity
before/during verification, compares the complete file set and hashes, and writes, syncs and reads back
the full manifest and archive index before source removal. A retry preserves an existing full manifest.
Review protection no longer expires with age; both the repository and installed keep lists apply.

A verified archive is retained together with its source until an independent second copy is verified.
Record an existing second-copy path by original source path in the private
`~/.absbyai-jobarchive/verified-second-copies.json` mapping; every removal rehashes that actual copy.
The copy cannot be the source, inside the source, or on the archive volume. No old sources or destinations
are cleaned automatically by this repair. Unknown reference evidence blocks removal.

Restore verifies the original complete manifest and recreates recorded links. An unresolved link
returns an error and is not a completed restore. Tests: `python3 jobarchive.py selftest` from this source folder.
The installed nightly program runs at 2:15 AM; a successful installation is not a verified overnight run.
