# Seagate Expansion 22 TB health check (2026-11-06/07, Claude)

- Full read of every file on the drive (every byte of every file, 6.7 TB): finished Sat Nov 7 00:53 CST, **0 read errors**.
- SMART (the drive's own health report): **unavailable.** macOS does not pass SMART through this USB bridge (smartctl 7.5: "Operation not supported by device" in auto and sat modes). Raw output: `Docs/SEAGATE_HEALTH_RAW_20261106.txt`. A Windows or Linux machine, or a different enclosure, would be needed to read it.
- 24 GB write/read test earlier passed; no kernel or USB errors logged.
- Verdict: **not proven defective.** The Nov 1-3 bad copies point to the write path (exFAT has no crash protection, heavy parallel copies, USB link or power), not to unreadable sectors. Treat it as storage for finished work, never the only copy, always checksummed.
