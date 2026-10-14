AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Never Pay Nutritionist AD R3`. Fire it after Dan answers the round 2 page.

# RA-15 "Never Pay A Nutritionist Again": round 3 (the full build: 9:16 and 16:9 masters, every delivery check)

**Written 2026-10-14 by the round 2 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-15-never-pay-a-nutritionist-again.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra15/` (README: stage order, twelve lessons; `round2/` holds this round's scripts), on top of `../ra05/` and `../ra04/`.
Work folder: `/Volumes/Extreme/_edit_work/ra15/`.

## First: read Dan's answer to the round 2 page

Page: http://127.0.0.1:8828/ (keep it; round 1 is 8818). VLC copy: `Videos to Review/Never Pay Nutritionist AD R2 - whole ad review copy.mp4`.
Record his words verbatim with file hashes in `round3-plan/decisions.json`, the way `round2-plan/decisions.json` does.

- **He approves the three clips:** build round 3 below.
- **He sends a clip back:** fix that clip only (retake from the approved frames with `round2/batch.sh`, inside the $10 cap: $7.00 left;
  or another range of an existing take), re-run the measured check and a fresh independent reviewer with the three sense questions,
  show it moving in context, then build. The cardboard fallback he was offered is the round 1 picture: Dan on camera for 39.01-42.54
  (remove the `cutout` card in `s05_plan15.py`; the inside-hold splice assert must still pass).
- He may also comment on the whole-ad review copy. Anything he does not mention stands.

## What round 2 delivered (all in the 9:16 draft, V2 voice)

| card | clip | used | slot (film time) | sha256 of take |
|---|---|---|---|---|
| `fridge` (I2, replaces the A0017 factory) | `round2/motion/I2-t1.mp4` | take frames 33-86, real speed | 29.03-31.26, on "not a printout that says chicken and broccoli." | 7cab3d8ace13a743 |
| `restaurant` (I4) | `round2/motion/I4-t2.mp4` | frames 32-78 (baked cut at 29/30 before it) | 37.07-39.01, on "Eating at a restaurant? Ask it what to order." | aa3c951abb9d6e9c |
| `cutout` (I5) | `round2/motion/I5-t1.mp4` | shot A frames 6-35, CUT, shot B 89-143, locked camera | 39.01-42.54, on "A nutritionist charges hundreds of dollars per month and sees you twice." | dcaaae3b4ce109f8 |
| `macro` (B0035 phone card) | unchanged recording | now 1.50 s | 35.57-37.07, ends on "every single meal." | |

- All three fill the 9:16 frame. AI-GENERATED chip placed clear of every person over every used frame (`round2/chip_place.json`):
  fridge top right (613, 220), restaurant and cutout top left (60, 220).
- Captions: lines that START inside the cutout card are lifted whole to y 1215 (`LIFTS` in `s07_captions.py`) so the fallen cutout's
  face (y 1380-1550) stays clear. 9:16 only. **The 16:9 needs its own check of the same clip's caption band.**
- Plan: 9 cards, coverage 45.4 % (gate minimum 38 %), 8 Dan holds; the old holds at 39.01 and 41.74 are gone; the inside-hold splice
  assert passes. Spend $3.00 of $10 (`round2/motion/ledger.json`: 7 takes, I4-t3 blocked by the model and free).
- Checks done: `check15.py` on every take (sheets, end strips, self-change maps, cut spikes), by eye on full-res strips; a fresh
  independent reviewer answered the three sense questions per clip: all PASS, "SHOW DAN" (its one optional fix, start shot A at frame 6,
  is applied). Full-rate scan of 28.5-43 s: joins exactly on plan; repeated frames only in the macro recording's own still result screen
  (0.3 s at 36.77) and 0.13 s of the man sitting still in shot B.
- Not done (round 3): every delivery gate, the 16:9, the edit sheet, the full watch pass and the full-film independent review.

## Round 3: build and deliver

1. Re-hash the files in the table below before touching anything.
2. Freeze the 9:16 edit. Then the owed items, in this order: frame-lock the mix to the picture (`s08_audio.py` with `LOCK=`; it hung on a
   saturated machine in RA-05, round 1 here muxed with `-shortest`, mix 16 ms longer), `s04b_holdstart.py`, the land-then-hold check
   (`cut/landing.py motion_stats`), `piccuts.py decide`, `junk.py` on the final cut, `roll_sidecar.py mark-used`.
3. The 16:9 from the same edit (`ra01lib.Aspect("16x9")`): the three AI clips are native 9:16, so in 16:9 each needs the placement rule
   for a vertical clip in a horizontal frame (`_shared/VIDEO-RULES.md`, verticals and squares; a phone or clip panel beside Dan or a
   full-height panel, never a crop that loses the action: the fridge door, the phone and finger on the menu, the cutout on the floor).
   Show the three 16:9 placements to Dan only if they are a new kind of layout for him; otherwise state them in "What I decided".
4. The edit sheet for the 16:9 (`sheet_from_claude_build.py`, `validate.py --hash`). Record `people`/`physique`/`label` for the three
   new clips: `other`, false, AI-GENERATED.
5. `audio_gate.py` with the A/B clip on each delivered file. V2's tone row fails (max 2.90 dB): the known mismatch of the bass standard
   (VIDEO-RULES 2026-10-12). Record it in the notes, never tune it away. The outdoor `artifacts` row is Dan's per-roll exception (RA-01 lesson 2).
6. `deliver/gate.py --format ad9x16` and `--format ad16x9` on the exact files; the watch pass (`deliver/watch.py`) and its judge;
   one fresh independent reviewer (`ra-reviewer`) with the three sense questions in its brief for the AI clips; the negative-imagery scan.
7. REVIEW 540p copies, notes, delivery folder `Claude Ad Videos/never pay a nutritionist again - RA-15/`, copies in `Videos to Review/`
   (replace the round 2 copy), `queue.py set RA-15 delivered` plus the artifact db (`_shared/edit-queue/README.md`), clip library
   `clip_library.py add --used-in "RA-15"` for the three new AI clips (the used ranges, not the raw takes).
8. The analysis card switches to the shared Soft Blue HyperFrames card (`_shared/hyperframes/analysis-card/`) once RA-14 round 3 has
   built it; if it exists, swap it in before the gates.
9. Later-round delivery message: list each change with timestamps in the new full film and short watch ranges (VIDEO-RULES 2026-10-10).

## Files (work folder, sha256 first 16)

| file | sha256 | what |
|---|---|---|
| `draft_9x16.mp4` | 7c41603b2f82c86d | round 2 9:16, V2 mux, 51.18 s (internal) |
| `round2/DRAFT - RA-15 round 2 - whole ad.mp4` | e2e6cf0f59f89436 | the copy Dan reviews (same picture) |
| `picture_9x16.mp4` | ddb8096c434508b7 | round 2 picture |
| `beats.json` | 0d802cb2d5dbbc6b | round 2 plan |
| `s05_plan15.py` / `s06_inserts15.py` / `s07_captions.py` / `gfx15.py` | 943e3863009f488f / 4e1e93a85a0e1661 / 41ffd0fe98c5cef6 / 617c7e7adbe9019e | round 2 code (round 1 copies in `round1/code_r1/`) |
| `cards_9x16/fridge.mp4` / `restaurant.mp4` / `cutout.mp4` / `macro.mp4` | d0cd746a668b6a7e / 48056e4e15f6a820 / e25ff2c962fca852 / d40c17a14cd096de | the round 2 cards |
| `cap_9x16/caption_states.json` | 0d4e67f2b7e22124 | captions with the cutout lift |
| `hf9/plates.json` | d00e2dc433525a3e | flow, macro (1.50 s), enjoy plates |
| `mix_bass.wav` | c05a8be1bdd1973b | V2, Dan's pick |
| `round2/index.html` | a9e5d100dda70435 | round 2 page |
| unchanged from round 1 | see `Handoffs/handoff-20261014-ra15-nutritionist-round2-after-dan-review.md` | cut, EDL, words, framing, grade, LUTs, lower thirds, CTA |

## Traps

- Veo bakes hard cuts and spins rigid objects: never widen a used range without re-running `round2/check15.py` on it (README lessons 8-10).
- The macro plate was rebuilt for 1.50 s; any change to that beat rebuilds it (`PLATES_ONLY=1 python3 gfx15.py`).
- The build cap was full most of round 2 (load 70-140). `r2_chain.sh` waits through `buildcap.wait()`; keep every long step behind it.

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Never Pay Nutritionist AD R3`. Read `Handoffs/handoff-20261014-ra15-nutritionist-round3-full-build.md` and
> `.claude/skills/ad-edit/reference/ra15/README.md`, then run round 3 of RA-15 "Never Pay A Nutritionist Again" with /ad-edit.
> My answer to the round 2 page: [paste it]. Record it, fix anything I sent back, then build the finished 9:16 and 16:9 masters from
> the same edit, run every delivery check and the independent review, deliver to the RA-15 ad folder and Videos to Review, and give me
> the list of what changed with timestamps.

**Recommended model and effort: Opus 5.5, high.** Two masters, the full gate set, the watch pass and an independent review.
