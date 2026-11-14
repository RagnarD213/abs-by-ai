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
