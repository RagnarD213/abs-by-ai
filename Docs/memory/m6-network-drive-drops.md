---
name: m6-network-drive-drops
description: 11-16: M6 reaches the Extreme/Seagate only over the M2 cable share; it dropped ~20 min under M2 load and killed an M6 edit's jobs; long M6 runs need a keepalive that remounts and resumes
metadata:
  type: project
---
On 2026-11-16 ~12:20-12:40 CT the Extreme and Expansion SMB shares vanished from the M6 during the Joint Vigor R4 priority edit. The M2's smbd was timing out (load ~25, plus a big Extreme->Seagate copy running on the M2); the 60 s mount keeper kept failing with NetFS -6600 / timeouts until the load eased. Every M6 process reading the job folder died (key driver, helpers).

**Why:** an M6 edit whose folder is on the Extreme does all its I/O across the cable share; the M6 internal had only 36 GB free (80 GB floor), so `renderq.py workdir` could not place the job locally.

**How to apply:** for a long unattended M6 edit on M2 drives, run a keepalive (template: `~/Library/Application Support/AbsByAI/jv-r4-keepalive.sh`) that remounts and restarts resumable steps; keep heavy copies on the M2 at throttled disk priority (`taskpolicy -d throttle`); prefer the M2 for jobs that are mostly disk I/O; free M6 internal space so big jobs can live locally. Related: [[work-drive-order]], [[two-mac-edit-routing]].
