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

## Phase 3 (2026-10-22): Dan's round 1 picks queued, studio batch retired

Script `scripts/blotato/igtemplate_phase3.py` (backup, retire, swap, place, verify); same batch and state files.

| Slot (5 PM CT, IG + FB) | Post |
|---|---|
| Fri Oct 23 | C1 The Fix 01 jump rope, last slide re-rendered to Dan's new rule (large shirtless cutout, no face avatar) |
| Mon Oct 26 | C2 Receipts 01 crunches (unchanged) |
| Wed Oct 28 | workout-06 "3 ab moves, 10 reps each, 3 rounds", Dan's real 1-minute ab workout, replacing C3 (C3 called a knee-to-elbow move his "Spiderman plank"; Dan's Spiderman plank is elbows to push-up and back). Default "swap" on the review page; Dan approved workout-06 "as is". |
| Fri Oct 30 | fix-02 towel row |
| Mon Nov 2 | workout-05 commercial break |
| Wed Nov 4 | fix-03 deadlift, look up |
| Fri Nov 6 | fix-10 side laterals, lead with the elbows |
| Mon Nov 9 | fix-06 V-sit twist |

- **Studio batch retired:** all 26 unreleased Codex studio posts (52 placements) taken off both platforms and recorded in
  `scripts/blotato/photo_reserve.json` (caption, image hashes, Blotato media URLs, old schedule ids). C3 is recorded there
  too. Image files and `studio27_state.json` untouched. Use the reserve only if the image queue would run dry.
- Captions via `dan-voice-writer` (its clean CLI login has expired, so it used the in-session fallback); 0 long dashes,
  5 hashtags each. Workout stills brightened with `enhance.py`.
- Verified by re-reading the queue: 16 of 16 placements exact (byte-identical slides, in order), 0 studio posts left,
  no other item changed, no duplicate image slots. Queue 192 to 150. Backup: `swap_backup/queue_before_igtemplate_phase3.json`.
- Next: round 2 revisions (Fix 5, Workout 6, Receipts 5) go after Nov 9 once Dan approves them.

## Round 2 picks queued and colour pass (2026-10-22, evening)

Dan's round 2 picks, 5 PM CT, IG + FB: Wed Nov 11 fix-09 curl swing, Fri Nov 13 receipts-02 metabolism, Mon Nov 16
workout-02 five minutes, Wed Nov 18 fix-04 kettlebell, Fri Nov 20 receipts-11 carbs at night, Mon Nov 23 workout-09 ab
wheel, Wed Nov 25 cheat-01 protein per 100 calories (P2, Dan: yes), Fri Nov 27 workout-04 home arms, Mon Nov 30 workout-07
lower abs (revised per Dan's notes, then queued). **Pending (Blotato at 200/200; videos go first):** workout-07 on FB
(Nov 30) and workout-08 V-taper on both (Dec 2). Finish with `python3 scripts/blotato/igtemplate_phase3.py place` when
there is room, then `verify`.
- Colour audit (Dan: every screenshot colour corrected, never raw): `grade_still.py` applies the approved Oct 1 LUT grade
  to raw S-Log3 frames plus a finishing pass; audit table `.claude/skills/instagram-posts/reference/color-audit-r3.md`.
  Queued fix-10 (Nov 6) and fix-06 (Nov 9) regraded and swapped in with `igtemplate_phase3.py refresh <id>`
  (create new, delete old; same slot and caption).
- Captions: `dan-voice-writer` (CLI login expired, in-session fallback); 0 long dashes, 5 hashtags.
- Verified: 33 of 33 placements exact, no duplicate image slots, 0 studio posts. Round 3 review (7 unqueued posts):
  https://claude.ai/artifact/KoNaPVWbjLn9C2FUZhhqK2

## Round 3 picks waiting for room (2026-10-22, night)

Dan's round 3 picks, planned 5 PM CT IG + FB: Fri Dec 4 fix-05 toe touch, Mon Dec 7 receipts-06 sleep, Wed Dec 9
workout-03 kettlebell, Fri Dec 11 fix-08 push-up, Mon Dec 14 receipts-04 light weights. Blotato is at 200/200 and
videos go first, so 13 placements wait (these 10, workout-07 FB, workout-08 both). `queue_topup.py --apply` (run by the
daily `social-queue-daily-refresh` routine) now calls `igtemplate_phase3.place` once no video is waiting; a passed or
taken day rolls to the next free Mon/Wed/Fri 5 PM. Captions via `dan-voice-writer` (in-session fallback). Round 4
review (plank, too old): https://claude.ai/artifact/4Bxwguv9cNTAnksoFLSpT7
