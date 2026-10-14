# framecheck: measure AI start/end frames for body and physics faults before Dan sees them

Built 2026-10-14 on RA-04's leg press clip, after Dan rejected a frame pair where the man pushed at about 90 degrees to
the machine ("No human body works like that... You never should have shown me this"). Every AI clip's START and END
frames go through these checks and then a fresh independent reviewer, before any review page shows them.

| tool | what it measures | the fault it catches |
|---|---|---|
| `posecheck.py IMG [--rail x1,y1,x2,y2] [--out overlay.jpg] [--json]` | MediaPipe pose: torso, thigh and shin angles and lengths, hip and knee angles, the leg line against a machine's guide line | a push at the wrong angle to the body or machine; impossible joints; limbs that grow or shrink between START and END (compare the lengths) |
| `rigid.py START END --part name:box ... --still name:box ... [--guide line]` | local template tracking: each part's displacement, the spread between parts, travel angle against the guide, drift of things that should stand still | a sled or prop that does not move as one piece, moves off its rails, or a frame or background that stretches |
| `lockstill.py START END OUT --box ...` | copies every pixel outside the person and the listed moving boxes from START into END | image-model drift of static machinery and background |

## Rules learned on the first run (seven independent reviews, six fails)

1. **Prove a check on the frames Dan rejected first.** posecheck read 26 and 43 degrees leg-to-rail on his rejected pair.
2. **The automatic rail finder can grab the backrest or an upright.** Mark the rail endpoints by hand on a gridded crop
   (`--rail`) and use `--rail auto` only as a hint.
3. **Track parts with local, high-texture boxes** (a plate rim, a bolt, a shoe logo). A global search jumps to look-alike plates
   on other machines; a box over flat black or the background returns nonsense with a low score. Trust scores above about 0.85.
4. **Image models lengthen legs when they straighten them** (bent frames measured 1.35 to 1.57 torso lengths of leg, straight
   ones 1.84 to 1.88). Compare bone lengths on every candidate pair; more than about 8 % change is a fail, and the foot travel
   must be what straightening those bones allows.
5. **An image model will not keep a machine rigid across an edit.** When a machine part must move exactly, build the END in code
   from START: cut the part out as one sprite, move it along its guide, take only the person from the generated END
   (RA-04's `ad-edit/reference/ra04/r2c_sled.py`). Things to cover in that composite: a phone is not "person" to the segmenter
   (fill its old spot), shoes may not be either (detect them on the moved platform), START's feet resting on the moved part
   must be cut out of the sprite and filled, and the sprite outline must be traced at 5x (a loose outline drags background).
6. **The independent reviewer gets only the pictures, the overlays and the checklist**, never the editor's reasoning, and must
   measure: angles, lengths, displacements, diffs. A fresh agent each time. Expect several rounds; each fail cost minutes, a fail
   reaching Dan costs his trust.
