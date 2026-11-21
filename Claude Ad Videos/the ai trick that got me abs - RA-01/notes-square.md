# RA-01 "The AI Trick That Got Me Abs": the 1:1 square (job AS-13)

Built 2026-10-02 by Claude (Opus 5.5) from `Handoffs/handoff-20261002-ra01-square.md`.
Work folder `/Volumes/Extreme/_edit_work/ra01-sq/`. Recipe: `recipe-square/` (order of scripts at the bottom).
Nothing was uploaded. No AI generation spend ($0.00). Raw footage untouched. The 9:16 and 16:9 masters are untouched.

## What this is

One file, `the ai trick that got me abs | claude | 1x1 | RA-01.mp4`: 1080x1080, 57.19 s, 1714 frames, about 8.5 Mbps.
It is the approved 9:16 re-laid for a square frame. There is no separate cutdown because the master is already
under 0:59.

| kept exactly as the approved 9:16 | how it was proven |
|---|---|
| the audio | the 9:16's own audio stream was copied, not re-encoded; the packet checksum is identical (`e70729ca...985a`) |
| the cut (which words, which takes, every pause removal) | `cut.json` is the same file; the transcript of the square matches |
| caption words and timing | all 192 caption states start and end on the same frames with the same text |
| the colour grade | the same grade settings on the same camera file |
| the order and length of every picture | every card starts and ends on the same frame, with one 3-frame exception below |

## What I decided (overrule anything)

1. **Dan's shot keeps the vertical's two framings, opened out to a square.** Tight = hair to just below the belly
   button; wide = hair to the waistband plus shorts. Same heights as the vertical, so the square simply shows more of
   the pool on each side. Each shot sits still on its own centre (no tracking). The square is almost a straight crop
   of the camera file (1.02x and 0.87x), so it is sharper than the vertical (1.8x and 1.5x enlargements).
2. **Photo cards sit above the caption line on the dark field, label above the picture**, the same arrangement as
   the vertical. Because a square is short, a standing photo shown whole would be small, so the AI picture and the
   three after pictures are shown as a square crop from the hair to the shorts line (head and waistband both kept,
   measured, not guessed). The before picture is shown whole so the belly is never cut.
3. **The analysis card (body fat / fat to lose / muscle to gain) is side by side:** picture left, bars right. In the
   vertical it is stacked, which does not fit a square.
4. **The macro tracker screen is the same window of the recording as the vertical**, fitted whole. It is smaller on
   screen than in the vertical (0.54x against 0.75x) but larger than in the 16:9.
5. **The "Tap the button below" pill is a compact pill on the chest**, between the jaw and the top of the abs, on the
   centre line. The vertical's pill runs edge to edge; in a square that would run off his chest over the pool.
6. **The real-picture label reads "Real picture of me - not AI-generated" with a hyphen.** The vertical has a long
   dash there; the no-long-dash rule (09-18) binds a new file.
7. **The end card has no "AbsByAI.com" line** (your 10-01 rule). The vertical's end card predates that rule and has it.
   The two mid-video pills still carry AbsByAI.com under "Tap the button below", exactly as the vertical does.
8. **Three small picture changes from the vertical, to hide three jumps.** Three fresh judges and the reviewer each
   flagged the same three pause cuts (0:03.07, 0:19.02, 0:36.00) where you visibly jump. They are in the approved
   vertical too, but its narrow frame hides your hands; the square shows them. Words, audio and captions are
   unchanged. (a) At 0:03 the AI picture now comes in 3 frames earlier, right on the cut. (b) At 0:19 there is a zoom
   cut on the pause cut, and the next two shots swap tight/wide so every cut still changes framing. (c) At 0:36
   there is a zoom cut on the pause cut (the shot before it is wide, the 0.6 s after it is tight, then the macro card).

## Your calls (nothing here was waited on)

1. **Captions sit over the lower abs in the wide shots.** Two judges noted it. It is the same caption line the
   approved Ad 1 square uses (and the vertical's captions also sit on the abs). Say if you want the caption line lower
   or the wide shot a little tighter in squares.
2. **AbsByAI.com on the two "Tap the button below" pills.** Kept as in the approved vertical; removed only from the
   end card. Say if the 10-01 rule should take it off the pills too.
3. **The before picture has no label**, as in the approved vertical (Ad 1 precedent). Still your open call from 09-18.
4. **The 0.6 s tight shot at 0:36** is the shortest shot in the ad (the round 2 reviewer's one minor note). It reads
   as a zoom into the macro card. Say if you would rather that pause cut were left as the vertical has it.
5. **One frame before the end card (0:55.25) has no pill and no caption.** Same frame in the approved vertical. Not
   visible at speed.

## Checks on the delivered file

| check | result |
|---|---|
| audio gate 2.0.0 | PASS, 13 of 13 rows (the outdoor-lav exception is now built into the gate) |
| delivery gate 2.4.0, format ad1x1 | PASS, 39 of 39 rows, 3 declared not applicable, nothing unmeasured |
| label check (every 3rd frame of every labelled card) | PASS, 0 px of contact on all 8 labelled cards |
| face inside 8-92 % of the width, every talking frame | PASS, 29.5 to 71.7 %, 1595 frames, 0 outside |
| hair to top edge | min 50 px per shot (rule: 20 to 70) |
| head centre step at zoom cuts | max 4.1 % of the width; per-shot medians within 1.5 % |
| watch pass | round 1: three fresh judges, all three failed the same three joins; round 2 (after the fix): a fresh judge, 75 of 75 images, 0 defects |
| independent review | round 1 DOES NOT SHIP (`ROUND-1-REVIEW.md`, six findings, all addressed); round 2, a fresh reviewer: **SHIP**, two minor notes (`ROUND-2-REVIEW.md`) |

## Rebuild order (from `/Volumes/Extreme/_edit_work/ra01-sq/`)

`sq_plan.py` -> `sq_assets.py` -> `s07_captions.py 1x1` -> `sq_cta.py 1x1` -> `s10_render.py 1x1` -> `sq_finish.sh`
(mux with the approved audio copied, audio gate, transcript, alignment, strips, watch pass) -> look at
`neg_1x1/negative_sheet.jpg`, then `s20_neg.py` -> `sq_labelcheck.py` -> `s43_r3verify.py 1x1` -> judges ->
`watch.py --judge` -> `s12_gateplan.py 1x1` -> `gate.py --format ad1x1` -> `sq_deliver.py`.
Inputs copied from the approved build and not re-derived: `cut.json`, `beats_9x16_approved.json`, `framing.json`,
`words_aligned.json`, `grade.json`, `face_src_r3.json`.
