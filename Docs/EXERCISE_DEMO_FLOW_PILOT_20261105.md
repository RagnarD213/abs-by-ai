# Exercise demo pilot on Google Flow (2026-11-05)

Pilot of three app trainer demos (chair-squat, bicycle-crunch, db-lunge) made on the Google Flow subscription
(Veo 3.1 Fast and Omni 1.1 Flash twins) instead of the paid Replicate API, gated per `/exercisegeneration`.
Working folder: `Media/exercise-demos/_flowpilot/` (job `veo/job.json`, prompts, `build.sh`, `finish.sh`,
`logofix2.py`, `app-staging/`, `review/`). Flow project: "Exercise Demos Flow Pilot".

## Result per exercise

| exercise | takes (Veo / Omni) | outcome |
|---|---|---|
| chair-squat | 1 / 1 | Both takes moved cleanly (motion review PASS). Both garbled the chest print; Omni take repaired with `logofix2.py` (see below) and rebuilt at native speed. |
| bicycle-crunch | 3 / 2 | Veo pedalled the legs but the torso did not twist; Omni first take straightened both legs. Omni retry (6 s, twist-first prompt) gave one native pedal cycle with a visible twist and a readable print; looped with a 0.3 s seam cross-fade. |
| db-lunge | 6 / 3 | NO PASS. Codex could not anchor the rear foot in a bottom keyframe (61 px slide), so the clip used START = END standing. Every model stepped BACK (reverse lunge) and none reached depth: best rear-knee gap 0.36 shin (about 5 in), 12-20 degree lean, a bob at the bottom. |

## Credits and other cost

- Flow: 23,249 -> 23,113 = **136 credits for 14 takes**. Veo 3.1 Fast 8 s = 10, Omni 4 s = 7, Omni 6 s = 10, Omni 8 s = 12.
  Downloads at 1080p Upscaled are free. About 6 minutes from first submit to last file per batch.
- Paid API: voice-overs only (3 MiniMax clips, about $0.03). No Replicate video.
- Codex images: 13 stills on the ChatGPT subscription.
- Claude allowance is the real cost: the Flow runner (Sonnet) used about 60,000 tokens a clip, and each fresh
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

## Go / no-go for the remaining 49

- **GO for in-place and static moves** (about 40 of the 49: presses, curls, rows, flys, machine moves, squats,
  hip thrusts, crunches, holds), on Flow with an Omni twin for every Veo take and the logo repair pass.
- **NO-GO on Flow for step and travelling moves** (walking-lunge, inchworm, sled-push, db-farmer-carry, burpee):
  same failure as db-lunge. They need real footage or a keyframed bottom pair the image model can anchor.
- **Alternating or fast cyclic moves** (mountain-climber, jumping-jack, battle-ropes, march-in-place,
  db-renegade-row, leg-swings): treat as bicycle-crunch, expect one retry and use Omni 6 s for a native cycle.
- Budget the reviews: about 1 frame review plus 1 to 2 motion reviews per demo, so batch 10 demos per session.
