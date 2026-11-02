# Extreme drive cleanup, 2026-11-01

Dan asked to move RO-20 and the old finished job folders to the Seagate. 20 folders, about 548 GB by disk use, went from `/Volumes/Extreme/_edit_work` to `/Volumes/Expansion/_edit_work`. Extreme free space: 15 GB before, 598 GB after. Each copy passed an rsync dry run, file count and bytes, and sha256 of the largest file plus two random files, with a last recheck that nothing changed or was open before removal. Method: `Handoffs/handoff-20261021-extreme-drive-cleanup.md`, with `nice -n 10`.

| folder | status | size | files and bytes | new path |
|---|---|---|---|---|
| ro20 | MOVED | 200.5 GB | 32764 147667293404 files/bytes | /Volumes/Expansion/_edit_work/ro20 |
| ro19 | MOVED | 69.3 GB | 19959 34003462159 files/bytes | /Volumes/Expansion/_edit_work/ro19 |
| ro06 | MOVED | 54.9 GB | 13078 31945604965 files/bytes | /Volumes/Expansion/_edit_work/ro06 |
| ro07 | MOVED | 52.3 GB | 11272 32796814259 files/bytes | /Volumes/Expansion/_edit_work/ro07 |
| ro11 | MOVED | 37.4 GB | 1497 37319623084 files/bytes | /Volumes/Expansion/_edit_work/ro11 |
| ro13 | MOVED | 28.2 GB | 1556 28796027839 files/bytes | /Volumes/Expansion/_edit_work/ro13 |
| sl07 | MOVED | 23.6 GB | 6605 12929685713 files/bytes | /Volumes/Expansion/_edit_work/sl07 |
| ad1-zee-vert | MOVED | 20.5 GB | 14105 8918630725 files/bytes | /Volumes/Expansion/_edit_work/ad1-zee-vert |
| ds28 | MOVED | 15.9 GB | 1720 13502594564 files/bytes | /Volumes/Expansion/_edit_work/ds28 |
| ra06 | MOVED | 11.9 GB | 4705 3513353501 files/bytes | /Volumes/Expansion/_edit_work/ra06 |
| ra13 | MOVED | 10.8 GB | 3157 4752829521 files/bytes | /Volumes/Expansion/_edit_work/ra13 |
| ra01-sq | MOVED | 10.4 GB | 10323 1565633477 files/bytes | /Volumes/Expansion/_edit_work/ra01-sq |
| ra05 | MOVED | 10.2 GB | 2665 5565867782 files/bytes | /Volumes/Expansion/_edit_work/ra05 |
| ra01 | MOVED | 9.5 GB | 3327 7542897770 files/bytes | /Volumes/Expansion/_edit_work/ra01 |
| ra14 | MOVED | 8.3 GB | 1910 4948748111 files/bytes | /Volumes/Expansion/_edit_work/ra14 |
| ra15 | MOVED | 7.1 GB | 1904 3621325938 files/bytes | /Volumes/Expansion/_edit_work/ra15 |
| revisions-20261008 | MOVED | 6.8 GB | 2136 3077504969 files/bytes | /Volumes/Expansion/_edit_work/revisions-20261008 |
| ro03 | MOVED | 4.9 GB | 1522 2140671027 files/bytes | /Volumes/Expansion/_edit_work/ro03 |
| ra16 | MOVED | 4.4 GB | 1134 2309056328 files/bytes | /Volumes/Expansion/_edit_work/ra16 |
| revisions-20261012 | MOVED | 3.2 GB | 793 1836548457 files/bytes | /Volumes/Expansion/_edit_work/revisions-20261012 |
