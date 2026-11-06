# Seagate Expansion 22 TB health scan (Codex and Grokbot)

Goal: find out whether the Seagate Expansion drive (`/Volumes/Expansion`, serial NT1H3BA5, exFAT, USB 5 Gb/s) is failing. Between 2026-11-01 and 11-03 about 400 files copied to it came out with a bad stretch near the end (same size and date, wrong bytes). Mac originals were fine. One file (`_edit_work/ro01-publish/RO01_BLOTATO.mp4`) went bad after it had passed a checksum. No kernel disk or USB errors are logged; a 24 GB write/read test passed.

Why this is a handoff: reading the drive's own SMART report needs admin (sudo) rights and a package install (Homebrew is not installed). Claude cannot enter the Mac password.

Dan authorizes everything below. Do all of it, including the admin password (Grokbot has the vault) and installs.

1. Install smartmontools (Homebrew, or the official smartmontools macOS installer from smartmontools.org).
2. `sudo smartctl -a -d sat /dev/disk7` (device node may differ: `diskutil info /Volumes/Expansion | grep "Device Node"`; use the whole disk). If SAT fails try `-d scsi` or `-d sat,12`. Record reallocated, pending and uncorrectable sector counts, UDMA CRC errors, power-on hours, temperature.
3. If SMART is readable, start a long self-test (`sudo smartctl -t long ...`), wait, read the result with `-l selftest`.
4. If the USB bridge does not pass SMART, say so plainly and recommend a direct test another way.
5. Claude already started a full read of every file (log: `/private/tmp/claude-501/seagate-scan.out`, lines `READ ERROR:` are unreadable files; `SCAN COMPLETE` ends it). Read it if present.
6. Write the verdict in `Docs/SEAGATE_HEALTH_20261106.md`: drive healthy / suspect / replace, with the numbers. Do not write secrets into repo files (repo is public).

Do not reformat or move data off the drive. Finished video work on it is also on Google Drive.
