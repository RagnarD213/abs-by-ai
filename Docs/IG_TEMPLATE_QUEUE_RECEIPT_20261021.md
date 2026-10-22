# Instagram template carousels: queue receipt (2026-10-21)

Handoff: `Handoffs/handoff-20261021-instagram-carousels-batch-1.md`. Script: `scripts/blotato/igtemplate_queue.py`
(content list `igtemplate_batch.json`, state `igtemplate_state.json`, plan `igtemplate_plan.json`).

## Phase 1: C1, C2, C3 installed as the next three image posts

Instagram @danrosefit (`67203`) and Facebook Page Abs by AI (`47105`), Mon/Wed/Fri 5 PM America/Chicago, 5-slide
carousels, slides byte-identical to the approved R1 JPEGs and in order.

| Post | Slot | IG schedule | FB schedule |
|---|---|---|---|
| C1 The Fix 01 (jump rope) | Fri Oct 23, 5 PM | 5870966 | 5870970 |
| C2 Receipts 01 (crunches, Vispute 2011) | Mon Oct 26, 5 PM | 5870968 | 5870971 |
| C3 Steal My Workout 01 (3-minute home abs) | Wed Oct 28, 5 PM | 5870969 | 5870972 |

The studio posts that held those slots moved to the end of the studio run, both platforms: S08-B to Wed Dec 23,
S09-A to Fri Dec 25, S06-C to Mon Dec 28 (5 PM). Skip List carousel (IG Sat Oct 24 noon) and every video untouched.

- Captions written through the `dan-voice-writer` agent (its isolated writer login had expired, so it used the documented
  fallback); 0 long dashes, 5 hashtags each; C2 names Vispute et al., JSCR, 2011. `ad_guard` organic check passed.
- C3 timers queued as 1:00 per move (Dan gave no real times). If he gives them, edit
  `template-r1-mockups/source/C3-StealMyWorkout.dc.html`, re-render, and swap the media before Oct 28.
- Verified by re-reading the full queue: 6 of 6 ours exact, 6 moves at their new dates, no other item changed,
  no duplicate image slots. Queue 190 to 196.
- Backup before writes (git-ignored): `scripts/blotato/swap_backup/queue_before_igtemplate_20261021.json` and
  `queue_before_igtemplate_apply.json`.
