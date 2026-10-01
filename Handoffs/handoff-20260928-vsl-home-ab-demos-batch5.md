# Handoff: 4 home ab exercise demos for the VSL (batch 5), 2026-09-28

**Run on Dan's Mac** (needs `Media/exercise-demos/_character/ai-dan-canonical.jpg`, the Replicate / Gemini /
MiniMax keys in `~/.absbyai-secrets.env`, and `Media/video_edit/bin/` ffmpeg). The cloud session that wrote this
had none of those, so nothing was generated or spent yet.

## Goal
Dan wants impressive-looking, at-home ab exercise clips for the WV-01 VSL (he picks ONE for the live VSL after
seeing all four). Generate all four with `/exercisegeneration`, deliver as a review set. Install into the app only
the ones that already have a library entry in `public/exercises.js` (Dan: "if not, we'll put this in in the future").

## The four exercises

| # | Dan's name | Library id | Install in app? | Class / recipe |
|---|---|---|---|---|
| 1 | V-sit twist | `russian-twist` (feet-up variation; library setup already says "or lifted to advance") | yes, on approval | in-place, one 6s leg, palindrome |
| 2 | Toe touches | none (VSL only for now) | no | in-place, one 4s leg, palindrome |
| 3 | Lying straight-arm, straight-leg jackknife to toes (the **V-up**) | none (VSL only for now) | no | in-place, flip trick (generate TOP fresh, edit back to flat), one 4s leg, palindrome |
| 4 | Claude's pick: **Reverse Crunch** | `reverse-crunch` | yes, on approval | in-place, one 4s leg, palindrome |

Why reverse crunch as the 4th: it is in the library with no demo yet (so it can go live in the app the day Dan
approves it), it is equipment-free, lower-abs focused (rounds out a set that is otherwise upper abs + obliques), and
it is a single symmetric in-place rep, which is the cheapest reliable class. Bicycle crunch and mountain climber
look flashier but are alternating-limb moves; batch 3 proved those burn 2 to 3 Veo legs each and need both sides.

## Framing for all four (VSL use)
16:9, canonical gym, **front three-quarter or true side profile, camera low (about hip height)**, full body head to
feet with margin, static tripod. Floor moves: a black exercise mat under him. Same black tank, white Abs by AI logo.
The WV-01 round 9 Crunch sits inside a phone frame, so keep the subject centred with side margin (the phone crop is
tall and narrow).

## Stills: prompt specifics (use the recipe's likeness preamble in front of each)

1. **V-sit twist (start = rotated LEFT, end = rotated RIGHT).** "Seated on the mat balancing on his sit bones, torso
   leaned back about 45 degrees with a long straight spine (NOT rounded, NOT lying down), knees bent about 90 degrees,
   BOTH FEET LIFTED off the mat, shins roughly parallel to the floor, forming a V shape. Hands clasped together in
   front of his chest. His ribcage and shoulders are rotated to HIS LEFT so his clasped hands are just above the mat
   beside his left hip." End edit: "rotate his ribcage and shoulders to HIS RIGHT, clasped hands just above the mat
   beside his right hip. His feet stay LIFTED in exactly the same spot, his legs do NOT move, his torso angle stays 45
   degrees. The camera does NOT move." Camera: front three-quarter so the rotation reads. Name the wrong answer: "this
   is NOT a crunch, his feet are NOT on the floor."
2. **Toe touches (start = shoulders flat, arms reaching up; end = shoulder blades off the mat, fingertips at toes).**
   "Lying flat on his back, BOTH LEGS STRAIGHT and pointing VERTICALLY at the ceiling, feet together, knees locked.
   Arms straight, reaching up toward his feet, head and shoulders resting FLAT on the mat." End edit: "curl his
   shoulder blades and upper back UP off the mat so his fingertips TOUCH his toes. His legs stay perfectly vertical and
   still, hips stay on the mat." Side profile. Legs must stay vertical in both (name it: "his legs do NOT drop toward
   the floor").
3. **V-up (FLIP: generate the TOP fresh, edit back to flat).** Top: "balancing on his tailbone, straight legs and
   straight torso both lifted, body folded into a sharp V, straight arms reaching forward so his fingertips touch his
   shins near his feet, legs about 60 degrees off the floor." Start edit (flat): "lower him flat: lying fully extended on
   his back, straight legs resting on the mat, straight arms extended OVERHEAD on the mat behind his head, one long
   straight line from fingertips to toes." Anchor camera explicitly. Veo leg: `image` = flat start, `last_frame` = top
   (or generate the lowering and reverse, if the lift morphs, per the superman finding).
4. **Reverse crunch (start = knees 90/90, hips down; end = hips curled off the floor).** "Lying on his back, arms flat
   at his sides palms down, knees bent 90 degrees and lifted so his shins are parallel to the floor (tabletop), hips
   and lower back FLAT on the mat." End edit: "curl his knees toward his chest so his HIPS and tailbone LIFT clearly
   off the mat, knees above his chest; shoulders, head and arms stay flat. Knees stay bent at the same angle, he does
   NOT kick his legs straight." Side profile.

## Motion
Replicate `google/veo-3.1-fast`, `image` + `last_frame`, 1080p, 16:9, `VEODUR=4` except the twist (6s). Append the
ANTIPUMP block to every motion prompt. Twist prompt: "his feet and legs stay lifted and motionless, only the ribcage,
shoulders and arms rotate, from his left side across to his right side in one smooth sweep." Then the mandatory
gated cut: `reference/mono.py` region-scoped (hands/torso region), velocity-boundary check, `qcunit`,
full-frame background lock, tempo into 2.5 to 4s. The twist palindrome is a genuine left-to-right-to-left twist, so
it is legitimate.

## Voiceover (MiniMax `R8_NE3EBC2N`, `speed 1.0`, 4 cues, no em dashes)
- **V-sit twist:** "Here's how to do the V-sit twist. <#0.3#> Lean back to about forty-five degrees and lift your feet
  off the floor. <#0.3#> Keep your chest up and your back straight. <#0.3#> Rotate your ribcage side to side, not just
  your arms. <#0.3#> Move slow and controlled, and let your chest follow your hands."
- **Toe touches:** "Here's how to do toe touches. <#0.3#> Lie on your back with your legs straight up toward the
  ceiling. <#0.3#> Reach up and curl your shoulder blades off the floor to touch your toes. <#0.3#> Keep your legs
  still and your lower back pressed down. <#0.3#> Lower slowly. Your abs do the lifting, not your neck."
- **V-up:** "Here's how to do the V-up. <#0.3#> Lie flat with your arms overhead and your legs straight. <#0.3#> In one
  motion, lift your arms and legs and reach your hands to your toes. <#0.3#> Keep your arms and legs straight the whole
  way. <#0.3#> Lower back down slowly under control. Don't just flop back to the floor."
- **Reverse crunch:** "Here's how to do the reverse crunch. <#0.3#> Lie on your back with your knees bent at ninety
  degrees. <#0.3#> Curl your knees toward your chest and lift your hips off the floor. <#0.3#> Then lower slowly
  without arching your back. <#0.3#> Don't swing your legs. Slow up, slower down."

## Budget
About $3 each, ~$12 to $15 with a couple of still retries. Under the $25 session cap; no extra approval needed.

## Deliver
1. Gates per demo: `audio_gate.py --synthetic --profile in-app-demo`, `reference/qc.py`, `_shared/deliver/gate.py
   --format exercise-demo`. Finals at `Media/exercise-demos/<id>/<id>-AIDAN-narrated-FINAL-CANDIDATE.mp4`.
2. Send all four as one review set (crf-22 review copies if over 30 MiB), plus a silent no-VO version of each for
   the VSL insert (the VSL carries Dan's own voice, so the WV-01 editor needs the clean picture).
3. Tell Codex/WV-01 owner (board entry "WV-01 round 9") which files exist; Dan picks one for the live VSL.
4. **App install, only after Dan approves** `russian-twist` and/or `reverse-crunch`: copy the silent-safe narrated MP4
   + a poster JPG to `public/exercise-demos/<id>.mp4|.jpg`, add the id to `EXERCISE_DEMO_IDS` in
   `public/index.html` (~line 8663), commit, push main, confirm Railway deploy, open the exercise sheet live on
   absbyai.com. Media in workout cards is a native-retest trigger: add to the board's Native retest line.
5. Delete this handoff's row from `Handoffs/README.md` and the board's HANDOFFS list.

## Starter prompt
> Execute `Handoffs/handoff-20260928-vsl-home-ab-demos-batch5.md` with /exercisegeneration. Generate all four demos
> (V-sit twist, toe touches, V-up, reverse crunch), run every gate, and send me the four as one review set plus silent
> versions for the VSL. Do not install anything in the app until I approve.

Recommended: Claude Opus 5.5, High effort, on the Mac.
