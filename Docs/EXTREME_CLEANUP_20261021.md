# Extreme drive cleanup, 2026-10-21

Handoff: `Handoffs/handoff-20261021-extreme-drive-cleanup.md`. Method: copy to `/Volumes/Expansion/_edit_work/<folder>`, verify (rsync dry run empty, file count and bytes equal, sha256 of the largest file and two random files), then remove the Extreme copy. Authoritative running log: `/Volumes/Extreme/_edit_work/MOVED_TO_EXPANSION.md`.

Extreme free space: 12 GB at start (14:00 CDT). 124 GB after the second folder (17:15). The mover runs on in the background (about 5 to 10 MB/s while renders share the drives).

Deviation: copies ran at normal disk priority (`nice -n 10`) not `taskpolicy -b`, because background-throttled rsync managed about 1 MB/s next to live renders (load average 138).

## Moved (verified)
- sl05, 59.1 GB, now /Volumes/Expansion/_edit_work/sl05, moved 2026-10-21, verified rsync + count/bytes (57902 11195950292 files/bytes) + sha256
- invest-health-cutdowns, 54.3 GB, now /Volumes/Expansion/_edit_work/invest-health-cutdowns, moved 2026-10-21, verified rsync + count/bytes (1657 57030579377 files/bytes) + sha256

## Eligible, queued in the mover (67 folders, 382 GB at scan; `*-publish` folders left out, see below)
- sl05 (59.1 GB)
- invest-health-cutdowns (54.3 GB)
- ro12 (32.8 GB)
- ro05 (32.5 GB)
- zepbound (21.8 GB)
- ad1-sq (18.0 GB)
- spraytan (17.4 GB)
- av05-ad6-vert (14.7 GB)
- supplements (13.0 GB)
- AV-03 (8.4 GB)
- ad3-sq-r2 (8.0 GB)
- sl04 (7.8 GB)
- revisions-20261001 (7.2 GB)
- ad3-sq (7.2 GB)
- revisions-20260928 (6.8 GB)
- revisions-20261005 (6.6 GB)
- revisions-20261002 (5.7 GB)
- ad2-vert (5.1 GB)
- ad2-sq (4.1 GB)
- revisions-20260930 (3.8 GB)
- music-check-20260922 (3.3 GB)
- revisions-20260921 (3.0 GB)
- revisions-0908 (2.3 GB)
- ad3-169patch (2.3 GB)
- ad15-final (2.2 GB)
- revisions-20260920 (2.2 GB)
- ds18-kettlebell-deadlift (2.1 GB)
- revisions-20260918 (2.1 GB)
- sales-letter-assets (1.8 GB)
- ds-17-r4 (1.6 GB)
- ds-17 (1.4 GB)
- ad-setup-20260916-hd (1.4 GB)
- revisions-0909 (1.3 GB)
- revisions-0915m (1.3 GB)
- mealprep (1.2 GB)
- revisions-20260915-armsr2 (1.1 GB)
- revisions-0910 (1.1 GB)
- revisions-20260917 (1.1 GB)
- revisions-0912m (1.1 GB)
- revisions-20260919 (1.0 GB)
- revisions-0914z (1.0 GB)
- revisions-0911 (0.9 GB)
- codex-revisions-adoption-20261005 (0.9 GB)
- revisions-0912 (0.5 GB)
- codex-revisions-recovery-20261005 (0.4 GB)
- revisions-20260929 (0.2 GB)
- revisions-20260926 (0.2 GB)
- wv01-plan (0.2 GB)
- audio (0.1 GB)
- rx01 (0.1 GB)
- vqc-c (0.0 GB)
- vertical-centering-codex-proof-20261003 (0.0 GB)
- video-graphics-standard-20260926 (0.0 GB)
- hyperframes-codex-ro17-fix (0.0 GB)
- muhammad-shorts-brief (0.0 GB)
- revisions-0912w (0.0 GB)
- tx (0.0 GB)

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

## Stayed: `*-publish` folders (about 7 GB in the untouched set)
Left in place: they hold local TikTok upload files for videos still waiting on the Blotato queue. Ask Dan before moving.
