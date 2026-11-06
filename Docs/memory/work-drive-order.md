---
name: work-drive-order
description: Work goes on the internal drive first, then the Extreme, and the Seagate only when neither has room; Seagate is for finished work and must be checksummed
metadata:
  type: feedback
---

Dan, 2026-11-06: "do things on the internal drive when possible, then the Extreme, and then the Seagate only if it's not possible to do it on the internal and the Extreme."

**Why:** the Seagate is slow (about 240 MB/s vs 970 on the Extreme) and silently corrupted about 400 files in copies on 2026-11-01 to 11-03 (right size and date, bad bytes; only a checksum or `cmp` catches it). The internal drive was freed to about 270 GB.

**How to apply:** `renderq.py workdir JOB --need GB` picks internal `~/Projects/_edit_work/<JOB>` (keeps 80 GB free), then Extreme, then Seagate; a job's existing folder never moves mid-job. Move finished jobs to the Seagate after a checksum check. Never use the Seagate as the only copy. See [[longform-delivery-location]].
