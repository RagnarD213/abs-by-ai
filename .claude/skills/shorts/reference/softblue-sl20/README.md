# `softblue-sl20/`: SL-20 Invest In Your Health shorts (R1, 2026-11-05)

Three Shorts from RO-20 "Why You Should Invest More In Your Health" (Claude film, roll C1511, 8/3 kitchen shoot), built from the
SL-18 approved-master recipe (`softblue-sl18/`, read it first). Work folder `/Volumes/Expansion/_edit_work/SL-20/` (copies here).
Order: `snap.py` -> `batch.py audio, words, plan, track, plan, cues, gfx, proof, render` -> `deliver.py copy` -> `runwatch.sh S` ->
fresh `ra-reviewer` per Short (`REVIEW-BRIEF.md`) -> `rungate.sh S` -> `page_sl20.py` -> `_shared/review_server.py`.
Three review rounds (1, 1b, 1c) before all three SHIP; what each cost is below.

## What is different from SL-18
- **Picture = the film's own graphics-free render** (`round4/v1/base.mp4`): same frames, clock, crops, zooms and grade as the approved
  master but no lower thirds or cutaways. A Claude long-form built with `films_r4.py` writes one; use it instead of the burned master
  (lower thirds sit over Dan's talking frames) and never the raw roll. Audio still comes from the master (verbatim gate).
- **Picture cuts from the film's `layout.json`**, every presenter segment boundary. ⚠ For parts after the first, the segment frames
  needed +54 frames on this film (`snap.py`, part index 2): the money Short's cuts were 1.8 s early and the reviewer found a double cut
  and a last-frame flash. **Always verify the cut list with a frame-difference scan of base.mp4 over each Short's ranges** before
  planning (the scan in the session log: 192x108 gray, diff > max(8, 6x median)).
- **Every talking shot uses `_shared/cut/landing.vertical_track`** (`window_path`): a fixed per-shot crop left Dan up to 276 px off
  centre while he swayed (round 1, all three reviewers).
- **Windows:** the film's W/T cameras both in the full window keep a native ~1.3x step; same-camera neighbours get the mid window.
  The gate's `cut:jump_cut` wants >= 1.15x measured at the shot ENDS: a W shot where he leans in at the end read 1.14x against the next
  T shot, so that T shot went to mid.
- **Captions:** a cue never crosses an audio join or a pause (the merge of a short cue across a trimmed pause showed words 1.6 s
  early); short (< 0.4 s) cues merge only across a gap under 0.15 s; "right now" is never split; a join mid-sentence does not
  capitalise the next word. CTC can put a word on the wrong side of a join: fix with `WORDFIX` from measured levels.
- **Key-point bars sit on a WIDE shot in the full window**: on the close camera his chin reached the bar's top (y 1130) when he
  lowered his head.
- **Internal audio joins fade 5 ms each side** (15 ms left a 7 ms room-tone dropout that a reviewer measured).

## Clip rules this batch enforced
- Film-approved AI clips are re-checked (`frame-reviewer` + `clipcheck.py`) on the USED range: A0072 (family dinner) fails from frame
  146 (greens appear on a plate). A clip is never slowed or held to fill a slot (VIDEO-RULES 2026-10-08): replace it (library stock
  B0485) instead. A static last screen (Cb11 phone, frames 223-235 identical to the reviewed frame 224) can run on at 1x.
- A cover that starts mid-shot can leave a sliver of the next master shot: start covers at a film cut or in a pause before a word.
- Stock that has no blacks and weak colour next to Dan gets a curves + saturation grade (B0485); over-saturated stock gets toned down
  (B0214 `eq=saturation=0.55`).
- Gate `compliance:banned_screen` reads `Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4`; it was moved off the Mac on
  2026-11-05 (NOT MEASURED on the final files). Point `deliver.py` at its new home when found.
