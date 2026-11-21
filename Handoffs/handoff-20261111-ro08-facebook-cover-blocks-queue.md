# Handoff: Intermittent Fasting (RO-08) cannot be queued, Facebook cover not registered

**Executed 2026-11-13 by Codex.** Approved A registered in repo/live installer; all waiting long-form cover gaps repaired. RO-08 schedules read back for Nov27/28. Receipts: `Docs/DS15_DS19_SETUP_RECEIPT_20261102.md`, `Docs/RO08_SETUP_RECEIPT_20261014.md`.

**Category:** CONTENT, long-form (LFC). Setup repair, not an edit.
**Date:** 2026-11-11. **Written by:** Claude (daily `social-queue-daily-refresh` run).
**Owner:** Codex (setup owner for all videos since 2026-11-07). Grokbot may do it instead if Codex is unavailable.
**Recommended model:** Codex newest Sol (`gpt-6.1-sol`), medium effort. Small, mechanical job.

## What happened

The daily top-up tried to queue "Intermittent Fasting: The Best Way To Get Abs" (RO-08) for Fri Nov 27 2026, 9 AM Central, and refused:

```
PROBLEM: RO-08: longform_queue.py failed: REFUSING video without a valid cover: Facebook video requires its approved cover in fb_reel_covers.json and the live installer
```

The routine's rule is to report a `PROBLEM:` line and never retry or fix it by hand, so nothing was changed. Blotato was at 190 of 200; 65 videos wait. Every day this stays broken, RO-08 blocks its slot, and its Shorts (SL-16, which wait for the parent) stay held.

## What is known (read only, verified 2026-11-11)

- Waitlist entry: `scripts/blotato/video_waitlist.json`, job `RO-08`, config `scripts/blotato/configs/ro08-intermittent-fasting.json`, `kitchen: true`, added 2026-10-14.
- `scripts/blotato/fb_reel_covers.json` has NO entry for RO-08 (only its Short, `sl16-short1`).
- Dan already approved the thumbnails on 2026-10-14: A = `social media graphics/youtube/thumbnails/Intermittent Fasting/Intermittent Fasting - thumbnail FINAL.jpg` (1280x720, 155,487 bytes), B for the later YouTube A/B test. Uploaded copy of A: see `Docs/RO08_SETUP_RECEIPT_20261014.md`. No new cover pick is needed from Dan.
- The receipt's original slot was Sun Jan 24 2027; the top-up now picks Fri Nov 27 (kitchen film, phase 2, allowed). Check `Docs/LONGFORM_RELEASE_CALENDAR.md` for RO-08's dated slot and let the top-up place it; do not hand-schedule.

## Do this

1. Read `.claude/skills/_shared/VIDEO-RULES.md` and the Facebook cover section of `/video-setup` for how a long-form's Facebook cover is registered (look at how a recently queued long-form, e.g. RO-23 or RO-31, appears in `fb_reel_covers.json` and in the live cover installer).
2. Register Dan's approved thumbnail A as RO-08's Facebook cover the same way (entry in `fb_reel_covers.json` with the correct match text, size, `approved` note "A, Dan 2026-10-14" and sha256, plus whatever the live installer needs). Use the approved file's exact pixels; do not make a new image.
3. Run `python3 scripts/blotato/video_topup.py` (dry run). It should now say it would queue RO-08 with no `PROBLEM:`. Do NOT run `--apply` unless you are finishing the whole job: the daily routine will queue it on its next run. If you do apply, also run `python3 scripts/blotato/ad_guard.py --scan` (must print CLEAN) and `python3 scripts/blotato/queue_artifact_data.py`.
4. Check whether other waiting long-forms have the same gap: for each `kind: longform` entry in the waitlist, confirm it has a cover entry. Fix any others the same way (only where Dan's approved cover already exists; otherwise list them).
5. Update `Docs/RO08_SETUP_RECEIPT_20261014.md` with what was registered, push with `scripts/git/safe-push.sh`, and mark this handoff Executed in `Handoffs/README.md`.

## Done looks like

`video_topup.py` dry run shows RO-08 queueable with no PROBLEM line, the receipt records the cover, changes are pushed. Nothing for Dan to approve: the cover is his existing 10-14 pick.

## Authorization

Dan's standing rules cover this: routine reversible setup, Codex owns setup, no questions for Dan. No spend. Do not delete or move any existing Blotato post.
