# Space cleanup round 2: receipt (Grokbot, 2026-11-24, done ~8:10 PM ET / 7:10 PM CT)

Manifest: `Docs/SPACE_CLEANUP_ROUND2_MANIFEST_20261124.md`. Delete log on the M6: `~/space_cleanup_r2_20261124/del.log`.

## Free space (`df -h`, GiB)
| Drive | Before | After | Target | Met? |
|-------|--------|-------|--------|------|
| Extreme | 43 | 167 | >= 150 | Yes |
| M6 internal | 38 | 33 (SRM-JV-R5 is actively writing) | >= 100 | No, blocked (see below) |

## Removed (rm -rf on exact paths; no Trash used)
| Path | Size | Second copy of the master | Check |
|------|------|---------------------------|-------|
| `/Volumes/Extreme/_edit_work/DS-109/r1/key` (R1 keying/matte cache) | ~84 GiB freed | Drive `_edit_work backup 2026-11-24/DS-109/approved master/DS-109_Alex-Hormozi-Not-Hungry-Youre-Bored_R4.mp4` (+ .srt, APPROVED_FILM.json) and `DS-109/setup receipt/` | Drive md5 70b85a14916d253a7c914446be8b2a18 = local R4 master md5; 67,061,656 bytes = APPROVED_FILM.json; local SHA-256 ce7c496e...1ca54 = APPROVED_FILM.json |
| `/Volumes/Extreme/_edit_work/DS-109/r2/key` (R2 keying/matte cache) | ~40 GiB freed | same | same |

Kept in DS-109: everything else (r1 src/recipe/captions/review, r2..r4, setup/ with receipt, covers, publish, local R4 master).
Pre-delete checks: renderq status (all free), editcap status (only SRM-JV-R5 active), keep.txt (empty), lsof +D DS-109 (nothing open), grep -R for the two paths in .claude/skills Docs scripts (no hits).
Side effect: some symlinks in `DS-109/r1/review-independent` (review cache) now dangle.

## Reservations
Stale `--help`, `WV-05`, `DS-41-setup` were already cleared by Claude (skip B.5). `AGY-DS107` (15 GB, Extreme) kept. The TEST-SPACE reservation and empty folder created by the gate check were removed (`storage.consume('TEST-SPACE')`, `rmdir`).

## Deliberately kept
- `WV-05.moved-to-m2-20261119` (M6, 39 GB): `ssh m2` (10.66.0.2) timed out, so no count/bytes/hash match. Blocker.
- `SRM-JV-R5-head` / `SRM-JV-R5-clean` (M6, 47 GB): Joint Vigor R5 still active. Blocker until Claude says delivered.
- `DS-98-blind` (M6, 27.5 GB): no DS-98 pick in `Docs/DAN_DECISIONS.md`. Blocker until Dan picks.
- `WV-07` (incl. key, which is NOT backed up) and `WV-03` remainder on the M6: keep per handoff.
- `SRM-goldenroots-jointvigor` (Extreme, 571 GB): not provable as a duplicate quickly; not needed.
- DS-106/107/108, RO-*, kit9x16, other intermediates: not needed once the Extreme target was met. DS-107 untouched.
- Never-touch list fully respected.

## Gate check
`python3 .claude/skills/_shared/renderq/renderq.py workdir TEST-SPACE --need 15 2>&1 | tail -2` printed `/Volumes/Extreme/_edit_work/TEST-SPACE` (a 15 GB job routes to the Extreme; passes). Internal drive remains below its 80 GB reserve, so jobs route to the Extreme.
