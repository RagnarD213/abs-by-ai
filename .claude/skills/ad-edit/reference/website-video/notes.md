# Website conversion video — 16:9 master, REVISION 4

**Rev 3 was reviewed 2026-09-08: the top of Dan's hair was cut off in every hold ("if the video's top is cut off, it's
basically not usable"), the wide level is banned, and he asked for AI clips at 0:19, 0:26, 2:04 and 2:17–2:44, a scroll
through the members' home screen at 2:48, and the better macro-tracker clip at 0:56.** Rev 4 changes exactly those
things, from measurements, and touches nothing else: same EDL and tight cut (incl. rev 3's manual cut), same grade and 4K
base, same card designs and lower thirds, same captions, and the **same audio chain, unchanged** (Dan: "this is the
audio that we want"). **AI generation spend: $9.47** (8 nano-banana stills at $0.134, 7 Veo 3.1 Fast clips at $1.20;
one still re-made after Veo's likeness filter, not charged for the filtered attempt). No production code, no deploy, no
native-retest trigger.

| | |
|---|---|
| master | `website_video_16x9.mp4` — **3:50.23 (unchanged)**, 1920×1080, 29.97 fps, AAC 256k |
| review copy | `REVIEW_540p_website_video.mp4` |
| audio A/B | `AB_his-vs-ours.mp4` — Muhammad's ad, then the same window of ours (audio unchanged from rev 2/3) |
| loudness | −14.50 LUFS · true peak −2.60 dBTP · LRA 2.8 LU · voice centred (L/R +0.9999) · 0 silent seconds |
| script fidelity | 99.0 % re-transcribed off the finished render |
| QC | **all checks PASSED** — the rev-3 suite plus caption clearance vs both phone boxes and the AI tag, the hair gate (never cut · anchored per segment · the detector-free top-rows test on every frame), the AI-GENERATED tag measured present on every insert; the shared audio gate PASSED all 11 rows on the delivered file and stamped it; watch pass 0 frozen runs / 0 black frames; contact sheet from exact grabs checked for the light, a wide frame, a black field, hair at the edge, a caption touching a graphic |
| hair proof | `pv/hairtrack_proof.jpg` (the plan's detector, native 4K scale) · `pv/hairgate_sheet.jpg` (the delivered frames, native 1080p) |

## ❓ One reading to confirm — the FAR level's bottom edge

"Never cut off my hair **or below my shorts line**." The default shipped here is your own rev-1 definition of the two
frames you like: **NEAR** ends at the belly button ("between my head and my belly button"), **FAR** shows the shorts
waistband with a little of the shorts below it ("the top of my head and my shorts visible"). Measured on the delivered
FAR holds, the bottom edge sits about 10–40 px of 4K (a hand's width of the elastic band and a little of the shorts) below the waistband; the counter is not in frame. **If you meant the frame
must never go below the waistband at all, say so — the FAR level becomes 1.58× (bottom ON the waistband) and only the
punch step re-renders (≈30 min).**

## 1 — The hair (the reason rev 3 was unusable)

Rev 3's tracker measured the **hairline** (first row of skin) and subtracted a 40-px guess for the hair; on his tallest
frames it read 296–300 in the 4K frame when the real top of his hair is at 195–215, so 23 of 26 holds cropped the hair
by 17–50 px, and rev 3's own headroom check passed because it measured to the same wrong point.

Rev 4 measures the **top of the hair itself**: a two-stage detector (`hairdet.py`) finds the skin, then walks up through
the dark hair band until the door panel behind him is reached, on the native 4K pixels, 1963 samples at 8 per
second across the cut (1786, plus 1158 measured on the delivered-scale picture valid; a sample whose climb is shorter than 50 px is thrown away, because a short
climb means the walk stopped inside the hair). Validated **by eye at native scale** — `pv/hairtrack_proof.jpg` is his
8 tallest frames and 4 median ones with the detected line drawn on a 50-px grid; the line sits on the top edge of the
hair in every tile. Then the same detector was run on the delivered-scale picture and the crops re-anchored to the
tallest instant either pass saw (a second punch render).

Every crop is anchored to that: `y0 = (the segment's minimum hair top) − 4 % of the crop height`, so the hair sits
~43 px below the top edge at his tallest instant in every hold. **Measured on the delivered master (596 samples,
574 valid):**

| | rev 3 (delivered) | rev 4 (delivered) |
|---|---|---|
| hair top below the top edge, minimum over every valid frame | **1 px (cut)** | **43 px** |
| median | 1 px | 56 px |
| per-segment minimum (the crop is anchored, not loose) | — | 43–53 px in every hold |
| frames with hair-coloured pixels in the top 12 rows of the head band (detector-free test, every frame) | 5371 of 5781 | **0 of 4468** |

The second row of that last line is the check that does not depend on finding anything: it only asks whether the top 12
rows of the head band look like the door panel or like hair. It fails rev 3's file on the first frame; it passes this
one on all 4468 frames with Dan on camera. Both gates now run in `qc.py` (check 11) on every future render.

## 2 — Closer crops, no wide level

Two levels, both from your rev-1 description, alternating strictly across every visible join; the wide level is deleted
(the code now asserts exactly NEAR / FAR / PIP exist and that no crop is wider than the FAR level):

| level | zoom | shows | holds |
|---|---|---|---|
| NEAR | 1.85× | hair → belly button | 10 |
| FAR | 1.46× | hair → shorts waistband | 11 |
| PIP | FAR geometry, Dan at 65 % | the two phone beats | 2 |

The framing also changes across every AI insert (the hidden segment does not advance the alternation), so you never
come back from a clip to the same crop you left.

## 3 — The AI clips (your placements)

Seven Veo 3.1 Fast clips, one consistent man (white, ~42, greying temples, deliberately ordinary, ripped) generated
from one reference still, full frame, tagged **AI-GENERATED** upper-left at 1.5×, captions kept on, 0.5-s fades at the
edges of each run and straight cuts between consecutive clips:

| where | line | clips |
|---|---|---|
| 0:18.7–0:24.9 | "Imagine yourself taking off your shirt at the pool and revealing the same rock hard abs" | A — he pulls a grey t-shirt off at a backyard pool; his wife on the lounger looks up, proud; two people behind glance over |
| 0:24.9–0:29.7 | "And picture how good you feel if you were in peak health with your stubborn belly fat" | B — shirtless easy jog along a beach, smiling. You are back on camera for "finally lost." before the before photo (before → you → after, never adjacent to a ripped man) |
| 2:03.8–2:15.5 | "Once our AI has all this information about you … you'll get far better results" | C1 — glances at the plan on his phone, then dumbbell curls in a garage gym; C2 — water, towel, a small satisfied nod |
| 2:26.4–2:44.3 | "Your AI will also customize your eating plan … a meal plan that you can actually follow … time that you have available" | D1 — grilling chicken and vegetables, shirtless; D2 — portioning into five containers; D3 — eating at the counter, loving it |

**The NUM3 choice (you asked for 2:17–2:44):** the "3 — A nutrition plan built for you" lower third runs 2:16–2:25
under your own line about it, so the clips start at "Your AI will also customize" (2:26) as the handoff recommended.
If you want them from 2:17 instead, the lower third moves onto the first clip — a one-beat re-render.

Two things worth knowing: Veo refused the first kitchen still as a "celebrity likeness" (the same generated man had
passed six other stills); a three-quarter-profile version passed. And clip D2 came back with a cross-dissolve between
two shots baked into it, so it is used as its two clean shots cut together (a cut reads as b-roll; a dissolve reads as
an edit inside the AI clip).

## 4 — The macro-tracker clip at 0:56 (swapped)

The short-ad session's better recording is the real Macro Tracker on absbyai.com with the salmon plate; it was
re-recorded at the phone box's exact aspect (`macro2/record_macro.py`, one real analysis call): photo in → Analyze →
"Analyzing your meal…" → the itemised list (salmon 425, wild rice 201, green beans 52, lemon 5, oil 92 = **775 cal**)
→ **Log Meal** → "✓ … logged" and today's total. The phone sits beside you as before. **Judgment call, flagged:** the
beat now runs 4.4 s longer, to "before AI changed the game", so the logged-meal payoff is on screen long enough to read.

## 5 — The members' home screen at 2:46

"We also have an AI sleep coach, the ability to tweak your goal picture … and much, much more" (2:45.9–2:52.9): one
slow continuous scroll of the real member home — Welcome back, then Macro Tracker, AI Trainer, AI Nutritionist,
Supplement Audit, AI Sleep Coach, My Transformations, Weight & Progress Log, Generate New Image, Support — in the phone
beside you. Captured from a local copy of the site on a fixture account (no real login), which is also why there is no
before/after hero on it; the scroll stops on the last feature tile.

## 6 — Audio: unchanged

`audio3.py` (the chain you approved on rev 2) ran unchanged on the new picture; the shared audio gate PASSED on the
delivered file and stamped it; the A/B is rebuilt beside the master.

## Recipe

`hairtrack.py` (→ `hairdet.py`) → `layout.py plan|punch` → `hairtrack_refine.py` → `layout.py plan|punch` →
`build_inserts.py` (tag, ai_*, macro, hub; `ai/veo.js` + `ai/prompts/`, `macro2/record_macro.py`, `hub/hub_capture.py`)
→ `layout.py mix` → `audio3.py` (bed −44) → `captions.py` → `deliver.sh` (`sheet.py`, `qc.py` + `qc_frame.py` +
`hairgate.py`, `watch.py`, review copy). `rev4.sh` is the chain after the first punch. Working dir
`/Volumes/Extreme/_edit_work/website-video-828/`; rev 3's scripts are in `rev3/`, rev 2's in `rev2/`, rev 1's in `rev1/`.
