# Ad 4 "Stop Wasting Money On Supplements": make the other formats (vertical, vertical 59s, square, square 59s)

Created 2026-10-01 by Dan's planning session. Recommended: **Opus 5.5, High** (secondary cut from an approved master).
Session name: `Stop Wasting Money On Supplements AD R1`.

## Why

Ad 4 goes into the new trial campaign (`handoff-20261001-vsl-trial-campaign-six-ads.md`) and today runs as horizontal
only (YouTube `R08TPEtkjuQ`). Dan counts horizontal, vertical, square and the short cutdowns as ONE ad unit, so it needs the rest.

## Deliver

1. 9:16 full length
2. 9:16 at 0:59 or under
3. 1:1 full length
4. 1:1 at 0:59 or under

All four rebuilt from the approved 16:9 master with `/shortad-from-longform`, matching the editor's grade, graphics and
audio (his audio stays untouched: memory `editor-audio-untouched`).

## Read first

- `.claude/skills/_shared/VIDEO-RULES.md` in full, then `Handoffs/video-editing/00-RULES.md`.
- The job specs, which hold the master's path and the ad-specific notes: `Handoffs/video-editing/AV-03-ad4-vertical-regrade-and-masters.md` (vertical) and
  `Handoffs/video-editing/AS-02-ad4-square.md` (square). Claim both rows with `scripts/edit-queue/queue.py`.
- Memory: `untagged-video-bt601-trap`, `cutdown-seams-single-source`, `caption-trailing-entry-overprint`,
  `framing-standard-hair-anchored`, `decision-budget-per-video`.
- A vertical and its cutdown already exist, held in `/Volumes/Extreme/_edit_work/ad4-vert/`. They need the re-grade in AV-03
  (BT.601 colour fault) and `deliver4.py` refuses the -0.9 dBTP verbatim stamp, which Dan accepted on 09-11. Fix and deliver
  those; do not start the vertical from zero. Re-copy the skill's `caption_sync_check.py` into the work folder first.

## Order of work

Build the 9:16 full first, then its 59s cutdown, then the square and its cutdown from the same locked edit. The queue
normally holds the square until the vertical is approved; this handoff builds all four in one task so Dan reviews the ad
once, on one review page (memory `review-page-what-i-decided`). Each file passes its gates and an independent review first.

## Done when

Four files delivered with gate PASS and a reviewer SHIP, queue rows moved to DELIVERED, review copies linked in chat with a
numbered action list. Do NOT upload to YouTube or Google Ads: after Dan approves, `/ad-setup` uploads them Unlisted and
adds them to the Ad 4 ad group in the new trial campaign. Ads never go out organically. No em dashes.
