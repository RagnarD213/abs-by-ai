# Extreme drive cleanup, 2026-10-21 (finished 2026-10-21 21:03 CDT)

Handoff: `Handoffs/handoff-20261021-extreme-drive-cleanup.md`. Method: copy to `/Volumes/Expansion/_edit_work/<folder>`, verify (rsync dry run, file count and bytes, sha256 of the largest file and two random files), then remove the Extreme copy. Running log on the drive: `/Volumes/Extreme/_edit_work/MOVED_TO_EXPANSION.md`.

**Result:** 57 folders moved, about 374 GB (disk-allocated size). Extreme free space: 12 GB before, about 322 GB after. No folder lost or left half-copied.

Deviations: (1) copies ran at `nice -n 10` normal disk priority, not `taskpolicy -b`: background-throttled rsync managed about 1 MB/s beside live renders. (2) Three folders (`revisions-20261005`, `codex-revisions-adoption-20261005`, `codex-revisions-recovery-20261005`) failed the strict dry-run check only because of `._*` AppleDouble stub files, whose timestamps rsync kept re-syncing. Re-checked excluding `._*` (as the handoff does for counts): 0 differences, equal file count and bytes, sha256 of the 3 largest files equal; then moved.

## Moved (verified)
- sl05, 59.1 GB, now /Volumes/Expansion/_edit_work/sl05, moved 2026-10-21, verified rsync + count/bytes (57902 11195950292 files/bytes) + sha256
- invest-health-cutdowns, 54.3 GB, now /Volumes/Expansion/_edit_work/invest-health-cutdowns, moved 2026-10-21, verified rsync + count/bytes (1657 57030579377 files/bytes) + sha256
- ro12, 32.8 GB, now /Volumes/Expansion/_edit_work/ro12, moved 2026-10-21, verified rsync + count/bytes (1806 33900950701 files/bytes) + sha256
- ro05, 32.5 GB, now /Volumes/Expansion/_edit_work/ro05, moved 2026-10-21, verified rsync + count/bytes (4983 31291378872 files/bytes) + sha256
- zepbound, 21.8 GB, now /Volumes/Expansion/_edit_work/zepbound, moved 2026-10-21, verified rsync + count/bytes (1051 22722027395 files/bytes) + sha256
- ad1-sq, 18.0 GB, now /Volumes/Expansion/_edit_work/ad1-sq, moved 2026-10-21, verified rsync + count/bytes (7853 12693468581 files/bytes) + sha256
- spraytan, 17.4 GB, now /Volumes/Expansion/_edit_work/spraytan, moved 2026-10-21, verified rsync + count/bytes (818 18065923580 files/bytes) + sha256
- av05-ad6-vert, 14.7 GB, now /Volumes/Expansion/_edit_work/av05-ad6-vert, moved 2026-10-21, verified rsync + count/bytes (6684 10093710745 files/bytes) + sha256
- supplements, 13.0 GB, now /Volumes/Expansion/_edit_work/supplements, moved 2026-10-21, verified rsync + count/bytes (759 13422731812 files/bytes) + sha256
- AV-03, 8.4 GB, now /Volumes/Expansion/_edit_work/AV-03, moved 2026-10-21, verified rsync + count/bytes (3032 6185817736 files/bytes) + sha256
- ad3-sq-r2, 8.0 GB, now /Volumes/Expansion/_edit_work/ad3-sq-r2, moved 2026-10-21, verified rsync + count/bytes (5672 3507761409 files/bytes) + sha256
- sl04, 7.8 GB, now /Volumes/Expansion/_edit_work/sl04, moved 2026-10-21, verified rsync + count/bytes (5445 3351037679 files/bytes) + sha256
- revisions-20261001, 7.2 GB, now /Volumes/Expansion/_edit_work/revisions-20261001, moved 2026-10-21, verified rsync + count/bytes (1960 5717118060 files/bytes) + sha256
- ad3-sq, 7.2 GB, now /Volumes/Expansion/_edit_work/ad3-sq, moved 2026-10-21, verified rsync + count/bytes (4730 3360578735 files/bytes) + sha256
- revisions-20260928, 6.8 GB, now /Volumes/Expansion/_edit_work/revisions-20260928, moved 2026-10-21, verified rsync + count/bytes (1407 5846121250 files/bytes) + sha256
- revisions-20261002, 5.7 GB, now /Volumes/Expansion/_edit_work/revisions-20261002, moved 2026-10-21, verified rsync + count/bytes (1166 4992647551 files/bytes) + sha256
- ad2-vert, 5.1 GB, now /Volumes/Expansion/_edit_work/ad2-vert, moved 2026-10-21, verified rsync + count/bytes (1937 3742550124 files/bytes) + sha256
- ad2-sq, 4.1 GB, now /Volumes/Expansion/_edit_work/ad2-sq, moved 2026-10-21, verified rsync + count/bytes (1766 3089323924 files/bytes) + sha256
- revisions-20260930, 3.8 GB, now /Volumes/Expansion/_edit_work/revisions-20260930, moved 2026-10-21, verified rsync + count/bytes (129 3948193144 files/bytes) + sha256
- music-check-20260922, 3.3 GB, now /Volumes/Expansion/_edit_work/music-check-20260922, moved 2026-10-21, verified rsync + count/bytes (38 3500950880 files/bytes) + sha256
- revisions-20260921, 3.0 GB, now /Volumes/Expansion/_edit_work/revisions-20260921, moved 2026-10-21, verified rsync + count/bytes (106 3145010359 files/bytes) + sha256
- revisions-0908, 2.3 GB, now /Volumes/Expansion/_edit_work/revisions-0908, moved 2026-10-21, verified rsync + count/bytes (473 2128072549 files/bytes) + sha256
- ad3-169patch, 2.3 GB, now /Volumes/Expansion/_edit_work/ad3-169patch, moved 2026-10-21, verified rsync + count/bytes (26 2424453940 files/bytes) + sha256
- ad15-final, 2.2 GB, now /Volumes/Expansion/_edit_work/ad15-final, moved 2026-10-21, verified rsync + count/bytes (92 2276111751 files/bytes) + sha256
- revisions-20260920, 2.2 GB, now /Volumes/Expansion/_edit_work/revisions-20260920, moved 2026-10-21, verified rsync + count/bytes (10 2295401030 files/bytes) + sha256
- ds18-kettlebell-deadlift, 2.1 GB, now /Volumes/Expansion/_edit_work/ds18-kettlebell-deadlift, moved 2026-10-21, verified rsync + count/bytes (1075 1274622440 files/bytes) + sha256
- revisions-20260918, 2.1 GB, now /Volumes/Expansion/_edit_work/revisions-20260918, moved 2026-10-21, verified rsync + count/bytes (319 2041619491 files/bytes) + sha256
- sales-letter-assets, 1.8 GB, now /Volumes/Expansion/_edit_work/sales-letter-assets, moved 2026-10-21, verified rsync + count/bytes (1286 293489173 files/bytes) + sha256
- ds-17-r4, 1.6 GB, now /Volumes/Expansion/_edit_work/ds-17-r4, moved 2026-10-21, verified rsync + count/bytes (801 956871358 files/bytes) + sha256
- ds-17, 1.4 GB, now /Volumes/Expansion/_edit_work/ds-17, moved 2026-10-21, verified rsync + count/bytes (795 693425715 files/bytes) + sha256
- ad-setup-20260916-hd, 1.4 GB, now /Volumes/Expansion/_edit_work/ad-setup-20260916-hd, moved 2026-10-21, verified rsync + count/bytes (53 1436744729 files/bytes) + sha256
- revisions-0909, 1.3 GB, now /Volumes/Expansion/_edit_work/revisions-0909, moved 2026-10-21, verified rsync + count/bytes (517 1031732120 files/bytes) + sha256
- revisions-0915m, 1.3 GB, now /Volumes/Expansion/_edit_work/revisions-0915m, moved 2026-10-21, verified rsync + count/bytes (416 1040699402 files/bytes) + sha256
- mealprep, 1.2 GB, now /Volumes/Expansion/_edit_work/mealprep, moved 2026-10-21, verified rsync + count/bytes (148 1164863914 files/bytes) + sha256
- revisions-20260915-armsr2, 1.1 GB, now /Volumes/Expansion/_edit_work/revisions-20260915-armsr2, moved 2026-10-21, verified rsync + count/bytes (100 1158779979 files/bytes) + sha256
- revisions-0910, 1.1 GB, now /Volumes/Expansion/_edit_work/revisions-0910, moved 2026-10-21, verified rsync + count/bytes (598 734542509 files/bytes) + sha256
- revisions-20260917, 1.1 GB, now /Volumes/Expansion/_edit_work/revisions-20260917, moved 2026-10-21, verified rsync + count/bytes (54 1153369454 files/bytes) + sha256
- revisions-0912m, 1.1 GB, now /Volumes/Expansion/_edit_work/revisions-0912m, moved 2026-10-21, verified rsync + count/bytes (370 836439932 files/bytes) + sha256
- revisions-20260919, 1.0 GB, now /Volumes/Expansion/_edit_work/revisions-20260919, moved 2026-10-21, verified rsync + count/bytes (122 988456659 files/bytes) + sha256
- revisions-0914z, 1.0 GB, now /Volumes/Expansion/_edit_work/revisions-0914z, moved 2026-10-21, verified rsync + count/bytes (143 930447978 files/bytes) + sha256
- revisions-0911, 0.9 GB, now /Volumes/Expansion/_edit_work/revisions-0911, moved 2026-10-21, verified rsync + count/bytes (110 886916125 files/bytes) + sha256
- revisions-0912, 0.5 GB, now /Volumes/Expansion/_edit_work/revisions-0912, moved 2026-10-21, verified rsync + count/bytes (102 453250497 files/bytes) + sha256
- revisions-20260929, 0.2 GB, now /Volumes/Expansion/_edit_work/revisions-20260929, moved 2026-10-21, verified rsync + count/bytes (101 130127866 files/bytes) + sha256
- revisions-20260926, 0.2 GB, now /Volumes/Expansion/_edit_work/revisions-20260926, moved 2026-10-21, verified rsync + count/bytes (81 137842932 files/bytes) + sha256
- wv01-plan, 0.2 GB, now /Volumes/Expansion/_edit_work/wv01-plan, moved 2026-10-21, verified rsync + count/bytes (31 164782531 files/bytes) + sha256
- audio, 0.1 GB, now /Volumes/Expansion/_edit_work/audio, moved 2026-10-21, verified rsync + count/bytes (40 119873360 files/bytes) + sha256
- rx01, 0.1 GB, now /Volumes/Expansion/_edit_work/rx01, moved 2026-10-21, verified rsync + count/bytes (103 29520607 files/bytes) + sha256
- vqc-c, 0.0 GB, now /Volumes/Expansion/_edit_work/vqc-c, moved 2026-10-21, verified rsync + count/bytes (13 17768198 files/bytes) + sha256
- vertical-centering-codex-proof-20261003, 0.0 GB, now /Volumes/Expansion/_edit_work/vertical-centering-codex-proof-20261003, moved 2026-10-21, verified rsync + count/bytes (7 14541699 files/bytes) + sha256
- video-graphics-standard-20260926, 0.0 GB, now /Volumes/Expansion/_edit_work/video-graphics-standard-20260926, moved 2026-10-21, verified rsync + count/bytes (6 32412 files/bytes) + sha256
- hyperframes-codex-ro17-fix, 0.0 GB, now /Volumes/Expansion/_edit_work/hyperframes-codex-ro17-fix, moved 2026-10-21, verified rsync + count/bytes (8 97246 files/bytes) + sha256
- muhammad-shorts-brief, 0.0 GB, now /Volumes/Expansion/_edit_work/muhammad-shorts-brief, moved 2026-10-21, verified rsync + count/bytes (6 143902 files/bytes) + sha256
- revisions-0912w, 0.0 GB, now /Volumes/Expansion/_edit_work/revisions-0912w, moved 2026-10-21, verified rsync + count/bytes (1 5350 files/bytes) + sha256
- tx, 0.0 GB, now /Volumes/Expansion/_edit_work/tx, moved 2026-10-21, verified rsync + count/bytes (1 57886 files/bytes) + sha256
- revisions-20261005, now /Volumes/Expansion/_edit_work/revisions-20261005, moved 2026-10-22, verified rsync (excluding ._ stubs, which only differ in timestamp) + count/bytes + sha256 of 3 largest files
- codex-revisions-adoption-20261005, now /Volumes/Expansion/_edit_work/codex-revisions-adoption-20261005, moved 2026-10-22, verified rsync (excluding ._ stubs, which only differ in timestamp) + count/bytes + sha256 of 3 largest files
- codex-revisions-recovery-20261005, now /Volumes/Expansion/_edit_work/codex-revisions-recovery-20261005, moved 2026-10-22, verified rsync (excluding ._ stubs, which only differ in timestamp) + count/bytes + sha256 of 3 largest files

## Stayed: protected by a live reference (check 2)
- ro05-fable (62.3 GB): PRE-RENDER-APPROVAL.md handoff-20261002-sl03-salad-shorts-round2.md handoff-20261004-sl03-salad-shorts-round3-revise-shorts-2-and-4.md
- ad5-vert (42.4 GB): handoff-20260911-square-ad5-muhammad.md handoff-20260912-ad5-vertical-revisions-round2.md
- ad4-vert (37.4 GB): handoff-20260911-square-ad4-muhammad.md
- website-video-828 (27.0 GB): shoot-828-slog3-format.md
- ro01 (25.0 GB): CODEX.md handoff-20260926-ro01-r4-graphics-and-clips-approval.md handoff-20261007-ro01-approved-b1-install-and-setup.md
- ad2-vert-v2 (20.8 GB): ad2-vertical-approved.md
- ad1-8-14 (20.7 GB): 01-reference-study.md handoff-20260911-codex-video-editing-trial.md handoff-20260911-video-quality-engine.md video-editing-strategy-report.md
- ad3-vert (15.4 GB): handoff-20260911-square-ad3-muhammad.md
- grok-ad1-first-cut (14.8 GB):
- ads234-8-14 (14.0 GB): handoff-20260911-video-quality-engine.md
- abwheel (11.6 GB): 01-reference-study.md VIDEO-RULES.md handoff-20260911-codex-video-editing-trial.md
- hyperframes-r2 (2.8 GB): README.md VIDEO-RULES.md
- AV-01 (1.7 GB): scoreboard.json
- broll-cuts-20260929 (1.1 GB): README.md
- revisions-0911m (0.2 GB): handoff-20260912-ad5-vertical-revisions-round2.md
- softblue-rollout (0.1 GB): GRAPHICS-STANDARDS.md SOFTBLUE.md
- DS-01 (0.0 GB): scoreboard.json
- grok-ad1-first-cut (14.8 GB): holds the ffmpeg wrapper target of the `_edit_work/bin` symlinks (named in the handoff)

## Stayed: `*-publish` folders
stop-deadlifting-publish (2.3 GB), arms-shoulders-publish (1.9 GB), ro02-publish (0.9 GB), ro05-publish (0.8 GB), ro16-publish (0.7 GB), ro10-publish (0.6 GB), abwheel-workout-publish (0.5 GB), sl04-publish (0.3 GB), belly-fat-emergency-publish (0.2 GB), oura-review-publish (0.0 GB). Left in place because some hold local TikTok upload files for videos still waiting on the Blotato queue. Needs Dan's go-ahead to move.

## Not covered (would free the most, needs Dan's decision)
Raw shoot folders (about 830 GB; copies on Expansion, Seagate and Drive, but active edits read them from Extreme), `kit9x16` (160 GB build caches), finished-video folders touched in the last 14 days (ro20 200 GB, ro19 69, ro06 55, RO-17 55, ro07 52, ro11 37).
