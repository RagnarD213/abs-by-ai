# RA-01 square (1:1) plan: what the delivered file must be

Job AS-13. Source handoff: `Handoffs/handoff-20261002-ra01-square.md`. This is the spec the reviewer checks against.
The parent plan is `Handoffs/video-editing/RA-01-plan.md` (sections 4, 5, 7, 12, 13); its rulings still bind unless
this file says the square differs.

## 1. The deliverable

One file: `/Volumes/Extreme/_edit_work/ra01-sq/master_1x1.mp4`. 1080x1080, 30000/1001 fps, h264 yuv420p BT.709,
AAC 48 kHz stereo, 1714 frames, 57.19 s (must be <= 59.00 s). No separate cutdown: the master is already under 0:59.

## 2. What a square is here

A re-layout of the APPROVED 9:16 master, not a new edit. Reference file (Dan approved it 2026-09-18, sha256
`02d032180a3eb42dc81d1857613df55ef4b715ab4d31e315834baf2a63003e51`):
`Claude Ad Videos/the ai trick that got me abs - RA-01/the ai trick that got me abs | claude | 9x16 | RA-01.mp4`.

Must be identical to the 9:16: the timeline (every beat starts and ends on the same frame), the take selection, the
grade, the caption words and timing, and the audio (the same AAC stream, bit for bit). Only geometry may differ.

## 3. Beat map (same frames as the 9:16)

| frames | picture |
|---|---|
| 0-61 | AI image card, AI-GENERATED chip ("This picture got me abs.") |
| 62-91 | Dan on camera, NEAR ("And it's not even real!") |
| 92-151 | AI image card (round 2: in ON the 3.07 s splice, 3 frames earlier than the 9:16), AI-GENERATED chip |
| 152-202 | BEFORE picture card, no chip (Ad 1 precedent, already Dan's call) |
| 203-229 | Dan on camera, FAR (the "other" beat between before and after) |
| 230-248, 249-267, 268-286 | three real after pictures, one at a time, real-picture chip on each |
| 287-368 | AI image card, AI-GENERATED chip |
| 369-744 | Dan on camera, zoom cuts NEAR/FAR; CTA pill 566-614 |
| 745-956 | analysis card (AI image + BODY FAT / FAT TO LOSE / MUSCLE TO GAIN rows + YOUR WORKOUT PLAN band), AI-GENERATED chip |
| 957-1097 | Dan on camera |
| 1098-1190 | macro-tracker phone recording card (stable itemized list + calorie total), no chip |
| 1191-1656 | Dan on camera, zoom cuts; CTA pill 1612-1655 |
| 1657-1713 | end card: AI image, AI-GENERATED chip, "Tap the button below" (round 2: no AbsByAI.com line, Dan's 2026-10-01 rule) |

## 4. Square geometry rules

* Talking head: hair-anchored, two levels only (NEAR = hair to just below the belly button, FAR = hair to the
  waistband plus shorts), same framing heights as the 9:16, a fixed centre per hold (no tracking, no drift, no pan),
  hair never touching the top edge, his face box inside 8-92 % of the width on every frame. Levels alternate across
  every visible join (zoom cut, never a naked jump cut).
* Captions: burned, word-timed, on every beat from the first word to the last, one centred line in the band around
  y 880-960, never on a chip, the pill, a card picture or his face; nothing that must be read below y 980.
* Cards (all except the end card) stop above the caption band, on the flat dark J2AD field (never a blurred photo
  backing). Hard cuts in and out; two physique pictures never share a frame; before, then "other", then after; no
  side-by-side before/after.
* Chips: AI-GENERATED on every AI image; the real-picture label on every real after picture of Dan. Never over his
  face, hair or abs; fully readable; inside the frame. The square's real-picture label reads
  "Real picture of me - not AI-generated" with a hyphen (project rule 2026-09-18: no em dash in new writing).
* A standing portrait may be shown as its 1:1 crop only if the whole head and the shorts line stay in the picture.
  The BEFORE picture must not lose its belly.
* A horizontal or phone clip inside a card is never cropped shorter than the approved 9:16 showed it.
* CTA pill ("Tap the button below" + AbsByAI.com): on both "tap the button below" lines, clear of his face and jaw
  and above the top of his abs, off before the end card starts, never touching a caption.
* No printed numbers in graphics (captions may print the spoken "200 pounds"). No drug names. No banned screens
  (side-by-side before/after app screen, "Meet the new you", email capture). No AbsByAI.com mark other than the
  CTA pill and end card that the approved 9:16 already carries.
* No swipe/whoosh sound effects. The audio must be the approved 9:16's, untouched.

## 5. Review output

Write `/Volumes/Extreme/_edit_work/ra01-sq/ROUND-1-REVIEW.md` in this format:

```
VERDICT: SHIP | DOES NOT SHIP
DEFECTS (most serious first):
  D1  <mm:ss.ff-mm:ss.ff>  <what the plan/rule requires>  ->  <what the file shows>   severity: blocker|major|minor
CHECKED AND CLEAN: <plan sections verified with no finding>
COULD NOT VERIFY: <what and why>
```

A blocker or major defect = DOES NOT SHIP. Minor-only = SHIP with the minors listed.

## 6. Round 2 rulings (planner, 2026-10-02), after ROUND-1-REVIEW.md and three watch-pass judges

* **D1 (three inherited same-framing joins).** Ruling: cover them in the square. The 1:1 frame shows his arms and
  hands, which the vertical's narrow window crops, so the same splice reads as a jump here. (a) Frame 92: the AI card
  comes in ON the splice, 3 frames earlier than the 9:16. A 3-frame level change would be a flash, so this one beat
  boundary moves by 3 frames; captions and audio do not move. (b) Frame 570: a FAR to NEAR level change on the splice;
  to keep every visible join a level change, the holds 607-694 and 695-744 swap to FAR and NEAR. (c) Frame 1079: a
  FAR to NEAR level change on the splice (the hold 957-1078 becomes FAR so the level also alternates across the
  stats card and the macro card), NEAR held to the macro card at 1098. Cut, audio and caption timing are untouched.
* **D2.** The delivery gate stamp (GATE 2.4.0, format ad1x1) is written for the round-2 bytes.
* **D3.** Recipe files describe the round-2 master: `beats.json`, `timeline_1x1.json`, `cta_1x1/cta.json`.
* **D4.** Both CTA pills sit on the frame's centre line (x 224-854).
* **D5.** Final encode raised to CRF 15 (about 8 Mbps).
* **D6.** The end card no longer prints AbsByAI.com (Dan's 2026-10-01 rule binds a new file). The two CTA pills keep
  their AbsByAI.com line exactly as the approved 9:16 has them; that is flagged to Dan as his call.
