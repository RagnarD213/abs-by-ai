# RA-06 round 3 (2026-10-14): AI motion for approved frames, brighter split screen, centred close, full 9:16

Work dir `/Volumes/Extreme/_edit_work/ra06/` (round 1 files backed up in `round1/recipe_r1/`). The round 1 scripts one level
up were edited in place; the copies here are the round 3 versions.

## Order

| # | command | makes |
|---|---|---|
| 1 | `python3 round3/gen_motion.py I1 v1 I3 v1 I4 v1` | Kling v3 takes from the approved START/END frames (re-hashed first), `motion/ledger.json` |
| 2 | look at each take (strips, 8-12 fps zooms on the risky region), then `s06_inserts06.py` `AI_SHOTS` picks the shots | `cards_9x16/I1.mp4`, `I3.mp4`, `I4.mp4` |
| 3 | `python3 round3/s06b_split_bake.py` then `python3 round3/s06c_split_luts.py 3.4 1.18 2.9 1.05 1.5` | one C2 LUT per split roll, body brightness measured against the talking shots |
| 4 | `python3 s05_plan06.py`, `python3 s04b_holdstart.py beats.json`, `python3 round3/s10b_near_track.py` (dry run) | plan, hold-start heads, close-hold offsets at 3.3 % vs 1 % |
| 5 | `r3_chain_c.sh` (waits for a build slot) then `r3_chain_d.sh` | the full 9:16, audio gate, junk scan, hard-splice scan |
| 6 | `python3 round3/page_r3.py --media` | the review page |

## What this round taught

1. **Kling cannot draw three hand-offs from a START frame (men waiting) to an END frame (men holding sheets).** Four takes, four
   prompt shapes (sequential, men step close, fanned sheets, one at a time): every time the first hand-off was clean and the
   other two sheets simply appeared in the men's hands. The end frame forces the state without the action. Two shots and a cut
   did it: the clean first hand-off, then a closer framing (crop 576x1024 of the 720x1280 take) of the end state from another
   take. The punch-in makes it read as a new shot, not a jump. Budget the retries before the fourth take.
2. **An END frame that barely differs from the START pulls the subject back.** I4's end frame has him still in the doorway, so
   both takes had him step out and then return or re-push the door. Use the clean head of the take; measure where the motion
   reverses on a zoomed strip of the region, not the full frame.
3. **The 9:16 land-then-hold preset's `fixed_under` (40 px at 608) is what let the close sit off centre**, not only the 3.3 %
   band: under it the crop never moves at all. For a centring request, call `landing.track` with `fixed_under=None` and a 1 %
   band on the close (`round3/s10b_near_track.py`). Median offset went 2.8-4.8 % to 0.8-1.2 %. A hold where he leans hard stays
   off centre on any band: make that hold the wide (`LEVEL_OVR` in the planner).
4. **"Very dark" B-roll: measure his body, not the panel.** Body skin median inside a box on him (plank 56, toe touches 72 against
   107-113 on the talking shots) told the story the panel means (75-97) hid. The shaded rolls needed +1 to +2 stops plus a midtone
   gamma in the LUT; the sunlit vacuum roll needed only the base look with round 1's darkening trim removed.
5. **Tightening a split panel moves the caption band onto a different body part.** The band (ink ~1420-1470) sits 146-196 px into
   the bottom panel; the closer vacuum crop put it on his chin. Place the crop so his chin ends above 140 px of the panel, and keep
   the head clear of the corner label.
6. **A chip on an AI clip goes where the action is not.** The I4 towel wave filled the only empty wall above the heads, and the
   button covers the middle, so the chip went on the floor under the caption line.
