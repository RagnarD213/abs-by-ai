# Space cleanup receipt, 2026-11-27 (M6 internal and Extreme)

Dan approved steps 1 to 3. Delete logs are on the M6 in `~/space_cleanup_20261127/`.

| Drive | Free before | Free after |
|---|---|---|
| Extreme | 5 GB (falling) | 147 GB |
| M6 internal | 41 GB | 195 GB |

## Removed

1. **Extreme:** `.npy` green-screen caches (rebuildable) in `_edit_work/DS-108`, `DS-109`, `DS-34-r2-keycache`, `RO-23`. Each approved film was first matched to its Google Drive copy by hash. Log: `step1-deleted.txt`.
2. **M6:** from `~/_edit_work/wv-03` (frozen round 6 copy) and `wv03-r8`: 13,674 files (67.1 GB) matched by SHA-256 to `/Volumes/Extreme/_edit_work/WV-03` (`step2-deleted-verified.txt`), and 2,506 `.npy` key caches (46.7 GB) (`step2-deleted-cache.txt`).
3. **M6:** 1,927 files (41.3 GB) from `~/Projects/_edit_work/WV-05.moved-to-m2-20261119` matched by SHA-256 to `/Volumes/Extreme/_edit_work/WV-05` (`step3-wv05-deleted.txt`); two installer images; app and package caches; media older than 7 days in the project `tmp/`.

## Still open

- About 5.1 GB left in `~/_edit_work/wv-03` and `wv03-r8` (files with no match, and the non-cache files in `round2/key`). Delete only after `rclone check` passes against `gdrive_backup:Abs By AI M6 cleanup 2026-11-27/` (`wv-03-frozen/round2/key` and `wv-03-frozen-unmatched`).
- The 97 files in `WV-05.moved-to-m2-20261119` that differ from the Extreme copy are kept.

## Not touched

Joint Vigor (all paths on both drives), DS-98 blind test, paused or unfinished edits, raw shoot footage, chat history. `Handoffs/handoff-20261124-grokbot-clear-more-space-round2.md` overlaps this work and should not be fired as written.
