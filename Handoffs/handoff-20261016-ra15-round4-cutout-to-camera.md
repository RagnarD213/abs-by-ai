AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Never Pay Nutritionist AD R4`.

# RA-15 "Never Pay A Nutritionist Again": round 4 (cardboard cutout out, Dan on camera)

**Written 2026-10-16 by the round 3 session (Claude, Opus 5.5).** Replaces `handoff-20261015-ra15-after-dan-review-round3.md`.
Recipe and lessons 1-27: `.claude/skills/ad-edit/reference/ra15/README.md` (round 3 scripts in `round3/` there). Work folder
`/Volumes/Extreme/_edit_work/ra15/` (the live copies). Delivery folder `Claude Ad Videos/never pay a nutritionist again - RA-15/`
(`notes.md`: round 3 files, hashes, gates). Round 3 page: http://127.0.0.1:8839/.

## Dan's answer to round 3 (2026-10-16), recorded in `round4-plan/decisions.json`

> "Everything in this is looking good except for the cardboard nutritionist cutout. I want to use a camera scene during that. That
> clip didn't really land. Everything else is good, though. Give me the handoff for the next round of edits."

- **One change, both shapes:** the cutout card (39.01-42.54, I5 take 1, library A0178) goes. Dan is on camera from the end of the
  restaurant card (39.01) to the lock-screen card (43.18): "A nutritionist charges hundreds of dollars per month and sees you twice."
- **Everything else is approved as delivered** (round 3 masters 9:16 `2c964e7ab3c9940c`, 16:9 `a8cc2c68c5a398a8`). Do not touch it.
- The cut and the audio do not change: the film stays 51.85 s, 1554 frames, and `mix_bass_r3c.wav` is reused as is.

## Build (work folder; every script's docstring says what it reads)

1. **`s05_plan15.py`**: delete the `cutout` entry from `CARDS` (keep the comment history). The gap 39.01-43.18 becomes Dan holds.
   ⚠ It contains the pause splice at **41.742** (source 120.364 -> 120.497), so the planner must split there with a size change
   (it asserts bare splices are covered). The span becomes two holds (39.01-41.74, 41.74-43.18) instead of the old 0.64 s "twice"
   hold; the planner's `_bare` assert will fail if not.
2. ⚠ **`LEVELS` and `TRACK_HOLD` are indexed by hold.** There are now 10 holds (was 9). Old: `FAR,NEAR,FAR,NEAR,FAR,NEAR,NEAR,NEAR,FAR`
   (0-3 one run, 4 at 24.99, 5 at 33.30, 6 "twice", 7-8 the ending). New default, to confirm by measurement:
   `FAR,NEAR,FAR,NEAR,FAR,NEAR,<6>,<7>,NEAR,FAR` where holds 6-7 (39.01-41.74, 41.74-43.18) must differ; pick the order that keeps
   his arms in frame (`round3/s_edgecheck.py`). `TRACK_HOLD` stays `4:0,0,9` (hold 4 = 24.99, unchanged index).
3. **New head and body samples for the new holds:** `python3 s04b_holdstart.py beats.json` (adds hold edges, keeps the end hold),
   then `python3 s04c_body.py` (body extent, 10 per second; reads the timeline), then `s05_plan15.py` again. Without the body file the
   new holds fall back to head-only tracking (lesson 17: arms off the edge).
4. **Remove `cutout` everywhere it is named:** `s06_inserts15.py` and `s06_inserts16.py` (`want("cutout")` block: with no args they
   build every card and `dur("cutout")` will KeyError), `gfx16.py` (`PL["cutout"]` plate), `round3/s_chips15.py`,
   `round3/s_gateplan15.py` (`AI` list), `round3/s_sheet15.py` (`FACTS`, `SRC_IN`), `round3/page_notes_r3.json` (copy to a round 4
   notes file). The 9:16 caption lift in `s07_captions.py` (`LIFTS`, y 1215) switches itself off when the card is gone: check it did.
5. **Render:** `s07_captions.py 9x16` and `16x9`, `s10_render05.py 9x16` and `16x9` (full, the crops change), mux each with
   `mix_bass_r3c.wav` (same length; no new voice chain). Nothing else is rebuilt: graphics, other cards, analysis card, CTA timing
   (9:16 from 45.31, 16:9 from 44.18) are unchanged.
6. **Check before the gates:** the new hold edges at native frames (`cut/piccuts.py strips` or the watch strips): 39.01 (restaurant
   card -> Dan), 41.742 (the pause splice: must be a visible size change, not a jump cut), 43.18 (Dan -> lock card). Hair never
   within 20 px of the top; `s_edgecheck.py` on both shapes; in the 16:9 his hands never under the CTA (it starts 44.18, after this
   span, so only check nothing moved). Read the delivered transcript against the script for 39-44 s.
7. **Deliver and gate (round 3 sequence):** `round3/r3_deliver.sh 9x16|16x9` (copy, audio gate with A/B, CTC words, Whisper, junk,
   chips), `s20_neg.py` after looking at a 1 fps sheet, `round3/s_gateplan15.py`, `watch.py` + a FRESH judge, `gate.py` (expect
   38/39: only `audio:stamp`, the tone row from Dan's bass lift, the same state RA-14 was approved in), `round3/s_sheet15.py <16x9>`
   then `validate.py --hash`, one fresh `ra-reviewer` per shape (three sense questions for the remaining AI clips; ask it to check the
   39-43 s span above all).
8. **Delivery:** 540p review copies, replace `Videos to Review/Never Pay Nutritionist AD R3 - *` with `... AD R4 - 9x16 / 16x9
   finished ad.mp4`, a round 4 page (`round3/page15r3.py` pattern, one change card) on a FREE port (8838 belongs to another job),
   `queue.py set RA-15 delivered` + the artifact db mirror, `notes.md` updated, board entry.
9. **Clip library:** A0178 (cardboard cutout) is no longer in RA-15. Remove "RA-15" from its `used_in` and set it
   `usable-unused` (or mark it rejected for this ad with Dan's words "That clip didn't really land") in
   `Media/clip-library/catalog.json`, then `clip_library.py sheet`.
10. **Delivery message:** later-round format (VIDEO-RULES 2026-10-10): the one change with its timestamps in the new film and a watch
    range (about 36.5-45.5 s), and say that every other scene is unchanged and approved.

## Files (sha256 first 16)

| file | sha256 | what |
|---|---|---|
| `cut.json` | see `round3/pre_twice/` for the pre-"twice" copy | the cut with "twice" (EDGE_OVERRIDE R2.end=121.92, R3.start=122.2469) |
| `mix_bass_r3c.wav` | reuse | V2 voice, frame-locked to 1554 frames |
| `beats.json` | round 3 final | holds/levels/tracks of round 3 (`round3/code_r2/` has every earlier plan) |
| delivered 9:16 / 16:9 | 2c964e7ab3c9940c / a8cc2c68c5a398a8 | round 3, approved except the cutout |

## Traps

- Hold indices shift by one after the new holds: re-read `LEVELS` against the printed hold list before rendering.
- `s04c_body.py` takes about 7 minutes on a busy machine; it samples every Dan hold, not only the new ones.
- The build cap is often full (RO-14, RO-17 sessions); every long step goes behind `buildcap.wait()` (fixed 2026-10-14 so it no
  longer crashes on an empty command line).

**Recommended model and effort: Opus 5.5, high.** One small picture change, but both masters, the full gate set and two fresh reviews.

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Never Pay Nutritionist AD R4`. Read `Handoffs/handoff-20261016-ra15-round4-cutout-to-camera.md` and
> `.claude/skills/ad-edit/reference/ra15/README.md`, then run round 4 of RA-15 "Never Pay A Nutritionist Again" with /ad-edit.
> My round 3 answer is recorded there: take out the cardboard nutritionist cutout and use a camera scene of me for that line;
> everything else is approved. Build both masters, run every delivery check and the independent review, deliver to the RA-15 ad
> folder and Videos to Review, and give me the change with timestamps.
