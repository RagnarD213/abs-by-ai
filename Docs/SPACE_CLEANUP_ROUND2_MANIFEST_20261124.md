# Space cleanup round 2: delete manifest (Grokbot, 2026-11-24 ~8:15 PM CT)

Handoff: `Handoffs/handoff-20261124-grokbot-clear-more-space-round2.md` (incl. Claude's 8:30 PM UPDATE).
Measured before: M6 internal 38 GiB free; Extreme 43 GiB free (`df -h`).
Targets: Extreme >= 150 GB, M6 internal >= 100 GB. Stop when met.

Pre-checks run: renderq status (all slots free), editcap status (only SRM-JV-R5 active; AGY-RO24 with Dan),
`keep.txt` (empty), `lsof +D /Volumes/Extreme/_edit_work/DS-109` (no open files),
`grep -R -e DS-109/r1/key -e DS-109/r2/key .claude/skills Docs scripts` (no references).

## To delete (Extreme), in order

| # | Path | Size | What it is | What stays | Second copy of the master | Check |
|---|------|------|------------|------------|---------------------------|-------|
| 1 | `/Volumes/Extreme/_edit_work/DS-109/r1/key` | ~83 GiB | R1 keying/matte cache (8,785 .npy, 2,476 .png, 12 .mkv; regenerable from source) | Everything else in DS-109: r1 src/recipe/captions/review, r2..r4, `setup/` (receipt, covers, publish), approved R4 master | Drive: `_edit_work backup 2026-11-24/DS-109/approved master/DS-109_Alex-Hormozi-Not-Hungry-Youre-Bored_R4.mp4` (+ .srt, APPROVED_FILM.json) and `DS-109/setup receipt/` | Drive md5 `70b85a14916d253a7c914446be8b2a18` = local `r4/review/media/hormozi-not-hungry-bored-r4.mp4` md5; size 67,061,656 = APPROVED_FILM.json bytes; local SHA-256 `ce7c496e...a54` = APPROVED_FILM.json sha256 |
| 2 | `/Volumes/Extreme/_edit_work/DS-109/r2/key` | ~41 GiB | R2 keying/matte cache (2,313 .npy; regenerable) | same as above | same as above | same as above |

Note: a few symlinks in `DS-109/r1/review-independent` point into `r1/key`; they are review caches and will dangle (no live skill/script references them).

## Deliberately not deleted
- `SRM-goldenroots-jointvigor` (Extreme, 571 GB): not provable as a duplicate quickly (M2 unreachable, no Drive copy); not needed for the target.
- `WV-05.moved-to-m2-20261119` (M6, 39 GB): M2 (10.66.0.2) `ssh m2` timed out, so no count/bytes/hash match. Left.
- `SRM-JV-R5-head`, `SRM-JV-R5-clean` (M6): Joint Vigor R5 still active (editcap). Left.
- `DS-98-blind` (M6): Dan has not picked (no DS-98 entry in `Docs/DAN_DECISIONS.md`). Left.
- `WV-07` (incl. key, not backed up), `WV-03` remainder (M6): keep per handoff B.4.
- Everything on the Never-touch list; DS-107 untouched; DS-106/108, RO-*, kit9x16 etc. not needed once the Extreme target is met.
- B.5 stale reservations: already cleared by Claude; AGY-DS107 reservation kept.
