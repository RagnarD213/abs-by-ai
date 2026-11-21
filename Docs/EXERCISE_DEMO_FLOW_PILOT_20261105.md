# Exercise demo pilot on Google Flow (2026-11-05)

Pilot of three app trainer demos (chair-squat, bicycle-crunch, db-lunge) made on the Google Flow subscription
(Veo 3.1 Fast and Omni 1.1 Flash twins) instead of the paid Replicate API, gated per `/exercisegeneration`.
Working folder: `Media/exercise-demos/_flowpilot/` (job `veo/job.json`, prompts, `build.sh`, `finish.sh`,
`logofix2.py`, `app-staging/`, `review/`). Flow project: "Exercise Demos Flow Pilot".

## Result per exercise

| exercise | takes (Veo / Omni) | outcome |
|---|---|---|
| chair-squat | 1 / 1 | NO PASS. Both takes moved cleanly (motion PASS on both), but both garbled the chest print. Three tracked logo repairs each failed review (skin wedge, logo sliding up to 35 px, leftover strokes, a notch cut into the elbow). |
| bicycle-crunch | 3 / 2 | NO PASS. Veo pedalled the legs but the torso never twisted (plus slow-down block artifacts). Omni straightened both legs. The Omni retry twisted, but elbow to the SAME-side knee, its print garbled mid-turn and its cycle ends did not match (seam diff 11). |
| db-lunge | 6 / 3 | NO PASS. Codex could not anchor the rear foot in a bottom keyframe (61 px slide), so the clip used START = END standing. Every model stepped BACK (reverse lunge) and none reached depth: best rear-knee gap 0.36 shin (about 5 in), 12-20 degree lean, a bob at the bottom. |

## Credits and other cost

- Flow: 23,249 -> 23,113 = **136 credits for 14 takes**. Veo 3.1 Fast 8 s = 10, Omni 4 s = 7, Omni 6 s = 10, Omni 8 s = 12.
  Downloads at 1080p Upscaled are free. About 6 minutes from first submit to last file per batch.
- Paid API: voice-overs only (3 MiniMax clips, about $0.03). No Replicate video.
- Codex images: 13 stills on the ChatGPT subscription.
- Claude allowance is the real cost (about 2 million Opus reviewer tokens in this pilot): the Flow runner (Sonnet) used about 60,000 tokens a clip, and each fresh
  frame or motion reviewer (Opus) about 150,000 to 180,000 tokens. This pilot ran 11 reviews.

## What broke, and the fixes now in place

1. **Flow renders at 720p and upscales, so the chest print garbles** on full-body shots in every take of both
   models ("Kim by t", "Abo bʒ d"). The approved stills read correctly. Batch 5 recorded that native 1080p Veo
   (Replicate) kept it readable. Fix built: `_flowpilot/logofix2.py` tracks the chest frame to frame (affine ECC),
   inpaints the old print on body pixels only, and pastes only the START still's print pixels. A first version that
   pasted a whole patch failed review twice (skin wedge, sliding logo, doubled shield).
2. **Speed changes stutter or smear.** `setpts` speed-ups drop frames unevenly (reviewer measured 9 vs 19 px per
   frame); `minterpolate` slow-downs left block artifacts on legs. Build at native speed; pick the take whose own
   tempo fits.
3. **`veo.py collect` flagged loop clips (START = END) as wrong frames.** Fixed in `veo.py` (commit dd7f4e1).
4. **The double-pump unit check false-alarms on floor moves** (whole-frame distance saturates while the legs
   cross). Pose landmarks settled it; the reviewer confirmed.
5. **External drive writes `._` files** that break `mono.py qcunit`; run it on an internal copy (`build.sh` does).


## Round 2 (same day): front-facing frames and paid native 1080p (Dan picked "Try paid 1080p")

| test | takes | outcome |
|---|---|---|
| chair-squat, three-quarter front view on Flow (START only; Codex could not hold the feet in an END frame, 3 tries, 20 to 35 px slide) | 2 Veo + 2 Omni | NO PASS. The print is large and readable in most frames, but the shield redraws itself mid-stand (grid, then fishbone) and letters smear; Omni closed his eyes and pursed the mouth through the stand; Veo opened the mouth, squinted and grew stubble at the top. |
| chair-squat side view, paid Replicate `veo-3.1-fast` 1080p | 2 | Print reads "Abs by A" through the rise (Flow 720p read "Kim by t"). Not built: same frames as round 1. |
| bicycle-crunch, paid 1080p | 2 | NO PASS by eye: rolls onto his side with his back to the camera; hands leave the head and arms flail. |

Round 2 cost: Flow 23,113 -> 23,076 (37 credits); paid API 4 x 6 s = about $2.40; 6 Codex stills; 4 more reviews.

**Final count: 0 of 3 demos pass after 23 video takes** (Flow 18, paid 4, plus 1 Omni lunge 8 s). Native 1080p fixes the print legibility; it
does not fix face drift (eyes, mouth, stubble) or logo-shape morphing, which the stricter motion reviews now catch on every take.
Gemini is running the same brief on three other exercises (`Handoffs/handoff-20261105-gemini-exercise-demo-test.md`); Claude gates its output.

## Verdict: NO-GO on Flow as it stands

0 of 3 demos passed. Credits are not the obstacle (136 for 14 takes). Two problems are:
the 720p print garble on every full-body take, which tracked repair could not clean to the reviewer's bar, and
movement accuracy on anything that is not a single symmetric in-place move.

## What a re-test would need (before the remaining 49)

- **The print problem first.** Options: frame the demos so the chest faces the camera and the print is large (the
  bicycle Omni retry kept it readable while the chest faced the lens), or a plain tank for app demos (Dan's call on the
  look), or native 1080p Veo on the paid API (batch 5 kept the print readable; Dan's call on paying).
- **In-place symmetric moves** (about 40 of the 49: presses, curls, rows, flys, machine moves, squats, hip thrusts,
  crunches, holds): the motion side worked first try on chair-squat for both models; these become a GO once the print is solved.
- **NO-GO on Flow for step and travelling moves** (walking-lunge, inchworm, sled-push, db-farmer-carry, burpee):
  same failure as db-lunge. They need real footage or a keyframed bottom pair the image model can anchor.
- **Alternating or fast cyclic moves** (mountain-climber, jumping-jack, battle-ropes, march-in-place,
  db-renegade-row, leg-swings): treat as bicycle-crunch, expect one retry and use Omni 6 s for a native cycle.
- Budget the reviews: about 1 frame review plus 1 to 2 motion reviews per demo, so batch 10 demos per session.

## Round 3 (2026-11-06): shipped all three to the app

Dan: "better than a stick figure", so the bar for app demos is the best take, not a clean reviewer pass.
- chair-squat: Flow Veo three-quarter front take, left side frozen. Installed 944ef64.
- db-lunge (reverse lunge): keyframed deep bottom (Codex) plus paid 1080p down and up legs, joined at the bottom, hard cut onto the exact START match. Fixed depth, foot plant and loop ghost; still about 17 degree lean on the step and about 2 s standing between reps. Installed 68cdd00.
- bicycle-crunch: paid 1080p side-view mirror pair, palindrome at native speed. Correct opposite elbow to knee, sharp print; hand still crosses the face at each switch, twist comes late (all 5 takes). Installed 68cdd00.
Round 3 paid spend about $3.60 (9 paid 4 s takes), 1 Flow take. Next three: `Handoffs/handoff-20261106-exercise-demos-three-more.md`.

## Round 4 (2026-11-07): Google-made start/end frames (Dan via side session)

Nano Banana Pro in Flow, 0 credits, 14 images. Bicycle crunch: Google never switched the legs in an END made from its START (4 tries, 2 prompts). Lunge: with a strict "keep framing identical, no mat" clause the gym held; the front foot slid ~120 px (fixed with a Google empty-gym plate and a shift), but the gate still failed the leg proportions (shin +15%). No Google pair passed, so no paid video was made and the shipped versions stay. Detail: `Media/exercise-demos/_googleframes/google-results.txt`. Lesson: Nano Banana Pro holds a locked camera only when the prompt says so explicitly, and redraws limb proportions in big pose changes.

## Three more (2026-11-07, Claude): triceps extension, dumbbell fly, weighted crunch

Paid 1080p `veo-3.1-fast` 4 s, 9 takes, $3.80. Crunch passed every gate and reviewer first try on motion (2 takes). Fly (4 takes) and triceps (3 takes) hit the stop rule: fly's near dumbbell sweeps across the face because the END frame placed it head-side of the shoulder; triceps flares the elbows wide at the bottom in a front view every time. Detail and next fixes: `Handoffs/handoff-20261106-exercise-demos-three-more.md`.
