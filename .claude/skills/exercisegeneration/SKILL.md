---
name: exercisegeneration
description: Generate a photorealistic AI exercise demo video for the Abs By AI Trainer — AI-Dan (Dan's likeness in the logo tank top) performing the movement in the canonical gym as a seamless looping rep, narrated by Dan's cloned voice reading the form cues. Use whenever Dan asks to generate exercise demos, demo videos, replace stick figures, or run a batch of exercises from the library — even if he doesn't say "/exercisegeneration". For ad videos use /make-ad; for retouching Dan's real photos use /photo-edit.
---

# Exercise demo generation ("keyframe-locked" AI-Dan demos)

Produces one finished asset per exercise: a 15–25s MP4 of AI-Dan performing clean looping reps with
Dan's cloned voice coaching the form. Proven end to end on `bw-squat` (2026-08-19, Dan-approved) and on
batch 1 — `pushup`, `reverse-lunge`, `plank` (2026-08-19/20, all three Dan-approved after one revision
round; finals at `Media/exercise-demos/<id>/<id>-AIDAN-narrated-FINAL.mp4`).

## Fixed assets — never regenerate these

| asset | path |
|---|---|
| **Canonical character still** (AI-Dan, black tank, white Abs By AI logo, THE gym — Dan-approved) | `Media/exercise-demos/_character/ai-dan-canonical.jpg` |
| **Narrator voice** (clone of Dan's real workout-video voice, Dan-approved) | MiniMax voice_id **`R8_NE3EBC2N`** (`Media/exercise-demos/bw-squat/dan-real-voice-id-v2.txt`) |
| Exercise copy (setup / execution / mistake per exercise) | `public/exercises.js` |
| Image runner (Google-direct; do NOT use Replicate nano-banana-pro — it rate-limits) | `.claude/skills/_shared/gemini-image.js` |
| Working scripts from the proven run (Veo invocation, VO gen, demucs reclone) | `Media/exercise-demos/bw-squat/*.js` |
| Batch runners from batch 1 (multi-exercise Veo/Kling + multi-script VO) | `Media/exercise-demos/run-batch1-videos*.js`, `gen-vo-batch1.js` |
| Static ffmpeg/ffprobe (no Homebrew on this Mac) | `Media/video_edit/bin/` |

All of `Media/` is gitignored (public repo) — verify with `git check-ignore` before staging anything.

## Per-exercise recipe (~$3, ~10 min)

1. **START still** — `gemini-3-pro-image` via the runner, `--tier draft` (2K, $0.134),
   `--image Media/exercise-demos/_character/ai-dan-canonical.jpg`. Generate **2 candidates**.
   Prompt pattern (see `bw-squat/start-prompt-dan.txt`): "The EXACT same man as in the reference photo —
   reproduce his face with high fidelity (same facial structure, eyes, nose, smile lines, short
   black-and-gray faded haircut, skin tone), same black tank top with the white Abs by AI logo, same
   gym" + an explicit anatomical description of the start position (name every joint angle and contact
   point) + "full body visible head to feet, static tripod framing, 16:9, photorealistic, one person
   only". Side profile for hinge/squat moves; pick the camera angle that makes form legible.
2. **END still** — EDIT the chosen start still with the same model ("Edit this photograph. Keep the
   exact same scene… change ONLY his position…"). **State depth/range EXPLICITLY and aggressively** —
   "until his thighs are FULLY PARALLEL — hips at knee height, NOT a shallow half squat" was required;
   a polite "about 90 degrees" produced a half squat. Name what stays planted ("both feet remain
   completely FLAT in the exact same spot — heels never rise"). **Floor-proximity bottoms (push-up,
   lunge rear knee) take TWO iterative edits**: even the aggressive language stops ~half way on the
   first try — edit the partially-lowered frame itself with "lower him the REST of the way / the FINAL
   inch, chest barely ONE INCH above the floor". Budget 1–2 bottom retries for any pressing or
   kneeling-depth movement. **When editing an already-edited still, anchor the camera explicitly**
   ("the camera does NOT move — the background machines, windows and floor remain in exactly the same
   place in the frame") — chained edits drift the camera lower otherwise, and a drifted end frame makes
   Veo morph the camera mid-rep.
3. **QC stills yourself frame-level** (likeness vs canonical, joint angles, contact points, scene
   consistency) — Dan reviews finished videos in batch mode, but a wrong still is a 13¢ fix and a wrong
   video is $2.40, so gate hard here.
4. **Veo legs — one for in-place moves, TWO for step-based moves** — `google/veo-3.1` on Replicate:
   `image` = start still, `last_frame` = end still (both resized to exactly 1280x720 with
   `sips -z 720 1280`), `resolution: '1080p'`, `aspect_ratio: '16:9'`. Exact invocation:
   `bw-squat/run-veo-dan.js`. Motion prompt states the coupling ("feet stay planted… the camera and
   background never move") and demands "ONE single continuous smooth movement with absolutely no
   pauses, stutters or hesitation".
   - **In-place moves (squat, push-up)**: ONE 6s leg; the clip usually contains a full down-up cycle
     to extract.
   - **Step-based moves (reverse lunge, split squat, step-up): TWO legs, 4s each** — descent
     (start→bottom) AND ascent (bottom→start, `last_frame` = the start still). **Reversed-footage
     palindromes are BANNED for step moves** — Dan rejected the v1: reverse playback of a step-back
     reads visibly wrong as a "return". 4s legs (~$1.60) leave less room for extra reps than 6s.
   - **Submit Veo jobs SEQUENTIALLY** — two simultaneous creates 429-throttle on Replicate.
5. **Extract the clean rep — THE GATED CUT PIPELINE (mandatory; supersedes all earlier frame-sheet
   advice).** Veo obeys the ENDPOINTS but NOT the rep count, it settles/wobbles at segment boundaries,
   it bobs at the bottom of hinges, and it animates background machinery. Every one of Dan's
   double-pump rejections traced to skipping a gate below. Per leg:
   a. **Region-scoped distance signal** (`_r2/mono.py analyze <id> <leg> [x w y h]`, crop scoped to
      the moving part — hands for pushdowns, torso arc for hinges, feet strip for anything planted).
      Whole-frame signals SATURATE once the body leaves the start pose and hide limb-level reversals.
   b. Choose a **strictly monotonic window** (mono.py `cut` refuses >8% dips).
   c. **VELOCITY-BOUNDARY check**: compute frame-to-frame velocity (24fps consecutive diffs, region
      crop). The segment must be ONE clean velocity bell. TRIM boundary frames where velocity decays/
      oscillates before the real movement (settle wobble). If the distance peak arrives at high
      velocity (overshoot-then-backslide), cut AT the peak and append a ~0.17s `tpad` clone HOLD of
      the extremum frame before the reversed half — reads as a squeeze, kills bounce and backslide.
   d. Palindrome (in-place moves) or two-leg xfade (step moves, unchanged from batch 1). Loop must
      start at the exercise's REST pose (reorder rev+seg when the leg was generated bottom-first).
   e. `mono.py qcunit` — the unit must be one unimodal pulse (≤10% secondary bumps), and verify the
      loop junction is a SINGLE velocity dip (bench final: 0.46→0.03→0.30 = one touch-and-go).
   f. **`_r2/ghost.py` background scan.** If ANY stray machine motion flags: don't spot-patch —
      **FREEZE THE WHOLE BACKGROUND**: overlay the live video cropped to the subject's corridor onto
      a full-res frame-0 still (`crop=W:1080:X:0` + `overlay=X:0`). Locked camera makes the seam
      invisible. Size the corridor from a motion heatmap and remember hips travel BACKWARD in squats/
      hinges. Re-scan (STRAY=NONE) and eyeball 3 frames for clipping. Equipment the subject actually
      uses (his own cable stack) keeps moving — everything else must be dead still.
   g. Tempo-normalize the unit into the 2.5–4s band (`setpts`, add `minterpolate` when stretching
      >1.05x).
   The old ≤0.5s frame-sheet sampling is DEPRECATED as a cut-selection method — it missed three
   double pumps in one batch; sheets are for form QC only, the gates above decide the cut.
6. **Voiceover** — `minimax/speech-02-hd`, `voice_id: 'R8_NE3EBC2N'`, `speed: 1.0`, `emotion: 'auto'`.
   Script: **open with "Here's how to do the [exercise name]."** then 3–5 cues built from the
   exercise's `setup`/`execution`/`mistake` copy in `public/exercises.js`, `<#0.3#>` pauses between
   cues. Target 15–20s spoken. Pattern: `bw-squat/clone-dan-voice-v2.js`.
7. **Assemble** — loop the rep enough times to cover VO + ~1s lead-in + ~1s tail (`-stream_loop N-1`),
   then mux (`adelay=1000|1000`, `-c:v copy -c:a aac`). **Do NOT use `apad` or `-shortest` with
   filter_complex** — this Mac's static ffmpeg 6.0 hangs on the first and segfaults on
   `apad=whole_dur`. Build video first, mux plain.
8. **Deliver** — send the finished MP4 in chat (batch = a review set). Dan is the form authority;
   nothing ships unapproved.

### Static holds (plank, wall-sit, side plank…)
No rep to interpolate: generate ONE still of the hold, then a single short i2v clip ("HOLDS the
position completely still… the only movement is subtle natural breathing, camera static") —
**`kwaivgi/kling-v3-video`, `duration: 5`, `mode: 'standard'`, `generate_audio: false` (~$0.35)**;
keyframe locking is unnecessary and it works first try (proven on plank, approved unrevised).
**Palindrome the 5s clip (fwd + reverse) for a guaranteed-seamless 10s loop unit**, then loop under
the VO the same way — breathing is symmetric, so reversal is invisible here.

## Costs
2 stills $0.27 + 1 edit $0.13 + 1 Veo leg $2.40 + VO ~$0.01 ≈ **$2.85/exercise one-take, ~$3.50 with a
still retry**. Step-based moves: add a second bottom edit + a second 4s leg ≈ **$4.50–5.50**. Static
holds are the cheapest: 1 still + 1 Kling clip ≈ **$0.50**. Batch 1 measured: 3 exercises incl. one
full revision round ≈ $13. State the estimated batch cost before running; the standing cap is
$25/session unless Dan authorizes more in the starter prompt.

## Traps (each cost real money or a redo — do not re-derive)
- Replicate's `google/nano-banana-pro` hard rate-limits (E003); the Google-direct runner is the door.
- Veo invents a DIFFERENT voice per clip — never use Veo native dialogue for library narration.
- The READY-FOR-UPLOAD YouTube videos have a continuous music bed; any future voice recloning must run
  demucs vocal isolation first (`ryan5453/demucs`, `stem:'vocals'` — see `bw-squat/reclone-v2.js`).
- Veo `image`+`last_frame` with plain i2v (no end frame) breaks physics mid-rep; with both frames it
  still ignores rep count — hence step 5.
- Dan's cue set for the squat: toes ABOUT PARALLEL (note: `public/exercises.js` says "toes slightly
  out" — unresolved discrepancy, flag when generating squat-family VO), ~90°, chest up/back flat, don't
  bend forward.
- Sparse QC frames (5–6 across 6s) missed a bounce twice; always sample ≤0.5s.
- **A deeper `last_frame` propagates depth into the whole leg** — the v2 push-up's mid-rep bottom
  matched the deepened still with no prompt change. If a rep looks shallow, fix the END STILL, not the
  motion prompt.
- **Dan's revision bar is the reference-video standard**: reverse lunge = PureGym `xrPteyQLGAo` (rear
  knee ~1 inch off the floor, one smooth ~3s down-up, torso upright). When he supplies a reference,
  study it frame-by-frame BEFORE regenerating. `yt-dlp` is blocked by YouTube SABR on this Mac — use
  the Browser pane instead: pause the player, arm a `setInterval` re-pause loop, kill autoplay (or it
  navigates away mid-study), then seek `video.currentTime` and screenshot each pose.

## Later phases (separate tasks, not this skill)
App integration (lazy `<video muted loop playsinline>` behind the stick-figure fallback, 3 call sites
of `getExerciseAnim` in `public/index.html` ~8010/8059/8137, iOS+Android retest — media in workout
cards is a native-retest trigger row), the "AI-generated demonstration" label, and hosting (repo is
public and `.git` is ~20 GB — likely a bucket/CDN, decision pending).

---

## Batch 2 findings (20 exercises, 2026-08-19) — read before the next batch

Batch 2 ran 20 in-place/static exercises in one session and is the first batch large enough to show
where the recipe actually breaks. Working scripts are preserved at `Media/exercise-demos/_batch2/`
(`spec.js` holds all 20 definitions + motion prompts + VO scripts; `gen-stills.js`, `gen-ends.js`,
`run-veo.js`, `run-kling.js`, `gen-vo.js`, `buildrep.py`, `assemble.js`, `qc.py`, `sheet.py`).

### Scale the batch by CLASS, not by count
All 20 were chosen as **in-place reps** (one Veo leg) or **static holds** (one Kling clip). No
step-based move was included, so no exercise needed two legs. That single choice is what made 20
affordable and fast. **Front-load the in-place and hold classes; save step-based moves for their own
batch**, where the two-leg + xfade recipe is the norm rather than the exception.

### 8 of 20 start stills failed the first pass, on eight predictable axes
Generate **2 candidates**, QC hard, and expect ~40% to need a second, more forceful prompt. The
failure modes and the language that fixed each:

| failure | what came back | the fix |
|---|---|---|
| **depth** (wall-sit) | knees ~130°, standing high | "hips exactly as LOW as his knees — thighs form a perfectly HORIZONTAL line… as if sitting in an invisible chair" |
| **pose-class confusion** (hollow-hold) | a V-sit / boat pose | name the wrong answer: "this is NOT a V-sit, NOT a boat pose"; then give absolute distances — "shoulder blades only three inches off the mat", "legs only twelve inches off" |
| **regression ignored** (knee-pushup) | a standard push-up | "his KNEES are ON THE FLOOR bearing his weight… his feet and toes do NOT touch the floor at all" |
| **shape geometry** (pike-pushup) | a long shallow plank | "feet walked in CLOSE to his hands… body folded almost in half… hips almost directly ABOVE his shoulders… a sharp, narrow, TALL inverted V" |
| **torso angle** (chair-dip) | a reclined reverse plank | "torso UPRIGHT and close to VERTICAL — shoulders stacked directly above his hips… chest faces forward, not up at the ceiling" |
| **foot detail** (split-squat) | back heel flat | "the BACK HEEL IS LIFTED HIGH — only the ball and toes touch, the raised heel clearly several inches up in the air" |
| **wrong phase** (crunch) | already crunched up | "head, shoulders, shoulder blades and entire upper back resting FLAT DOWN, completely relaxed and NOT lifted at all" |
| **framing headroom** (db-shoulder-press) | overhead lockout would crop | "WIDE full-body shot… a very generous amount of EMPTY SPACE ABOVE HIS HEAD, at least the height of his whole head and shoulders again" |

**Estimate the travel before accepting a frame.** For an overhead press the hands finish at roughly
1.3× shoulder height off the floor — measure that against the frame edge rather than eyeballing it.

### If a still comes back at the WRONG PHASE, keep it and reverse the pipeline
`glute-bridge` and `superman` returned the finished (top) position when the start was asked for.
Don't regenerate — **use it as the END still, write an edit prompt that moves BACKWARD to the start,
and flip the Veo leg** so `image` = the edited start and `last_frame` = the original. Same cost, and
the camera anchoring is just as good. `run-veo.js` has a `FLIP` set for exactly this.

### Automate rep extraction with a motion signal, but know where it lies
`buildrep.py` samples the leg every 0.1s, computes mean-abs pixel distance of each frame from frame 0,
takes **t=0 → the first prominent peak** as the one-way movement, then palindromes it. That handled
14 of 17 unattended. **It under-triggers when only the limbs move against a busy gym background**
(db-shoulder-press, leg-curl): the signal amplitude collapses to noise and the detector fires early.
**Rule: if `peak_val` is under ~70% of `global_max`, pull a contact sheet and pass the segment in by
hand** — `buildrep.py <id> <t0> <t1>` takes a manual override.

### Palindrome is the correct default for every in-place move
Push, press, curl, raise, extension, crunch, bridge, pike, dip, calf raise — the reversed descent
reads as a real ascent because the motion is symmetric, and the loop join is seamless by
construction. Trim one frame off the head of the reversed segment or the join hitches.
**Only step-based moves need two genuine legs** (batch-1 finding, unchanged).

### Small-range moves need tight framing AND a shorter Veo leg
`calf-raise` failed twice at the wide framing used for everything else: at that distance a heel lift
is a few pixels, and Veo filled the time with a body sway instead. **Two changes fixed it:** reframe
so he FILLS the frame head-to-feet ("the camera is CLOSE… only a small margin above and below"), and
**drop the leg to `duration: 4`** — the shorter leg reached the `last_frame` pose far more completely
than the 6s one, which wandered. `run-veo.js` honours a `VEODUR` env var for this.

### Normalize rep tempo after cutting — Veo's is wildly inconsistent
Raw rep units came out between **1.8s and 9.2s**. Anything under ~2.5s reads frantic and anything over
~5s reads sluggish. Stretch or compress the unit with `setpts` to land every rep in the **2.5–4s**
band before looping (batch-1's approved squat was 3.1s). Do it on the silent unit, before the mux.

### Kling holds are 720p — upscale before assembly
`kling-v3-video` standard returns 1280×720 while Veo returns 1920×1080. Upscale hold units with
`scale=1920:1080:flags=lanczos` so the library is uniform. (Batch 1's approved plank is 1284×716 and
is the odd one out — worth re-exporting whenever that file is next touched.)

### Operational notes
- **Veo `E005` on a create is transient.** knee-pushup was flagged once and went through unchanged on
  a plain retry. Don't rewrite the prompt on the first refusal.
- **Stagger Veo creates ~40s apart and poll concurrently.** 17 legs finished in ~25 min this way with
  zero 429s, versus ~60 min fully sequential.
- **Google's image API rate-limits at ~8 concurrent edits.** Two of a wave of 8 came back with a spend-rate
  error; a 30s wait and a re-run fixed both. `gen-stills.js`/`gen-ends.js` run in waves of 8.
- **Loudness needs no normalization** — every finished file landed at −23.4 to −24.9 dB mean, matching
  batch 1's approved −23.9/−24.2 exactly.
- **Run `qc.py` before delivering.** It asserts, per exercise: 1920×1080/24fps, AAC present, loop-join
  frame diff (<3.0 = seamless; all 20 came in at 0.32–1.2), range-of-motion diff (>2.0), and that the
  VO ends inside the video.

### Batch 2 measured cost — ~$59 for 20 exercises (~$2.95 each)
60 start stills ($8.04) · 22 end stills ($2.95) · 20 Veo legs ($47.20) · 3 Kling holds ($1.05) ·
20 VO clips ($0.20). Veo is **80% of the bill**, so every avoided leg retry is worth several still
retries — QC the stills hard, they are 5% of the cost.

---

## Batch 3 findings (10 exercises, 2026-08-20) — read before the next batch

Batch 3 ran 10 in-place exercises (leg-press, db-bench-press, db-row, db-rdl, db-goblet-squat,
cable-tricep-pushdown, face-pull, incline-pushup, dead-bug, bird-dog). Scripts at
`Media/exercise-demos/_batch3/` (`spec.js`, `retry-loop.sh`, `run-deadbug-flip.js`, adapted
`gen-stills/gen-ends/run-veo/gen-vo/buildrep/assemble/qc`). All 10 passed qc.py first try after the
per-leg fixes below. ~$30 total (~$3/exercise despite heavy congestion — failed Veo runs are free).

### Veo congestion: code 8 / E004 is free, and 4s legs squeeze through
Google shed load for the entire session (gRPC code 8 "high load" + E004), 20+ failures. Failed
predictions are NOT billed. A dumb retry loop (`retry-loop.sh`, one round every ~2.5 min, re-checking
which legs exist on disk) eventually landed everything. **When congested, 4s submissions consistently
succeeded while 6s ones failed in the same window** — drop to `VEODUR=4` for any move whose one-way
motion is under ~2s (most arm moves: row, pushdown, curls, incline push-up).

### Veo SYMMETRIZES asymmetric limb choreography — plan for it
Dead bug (opposite arm + opposite leg) failed twice: Veo extended BOTH legs, then BOTH arms, wandering
through wrong poses before landing the end pose. Bird-dog added a spurious leg-only lift then a
chest-dip floor-sweep. What worked:
- **bird-dog**: 4s leg + explicit anti-choreography language — "the hand never sweeps along the floor,
  his chest never dips, his leg never lifts on its own first — the arm and the leg move together from
  the first instant". Clean direct extension 0→2.0.
- **dead bug**: **FLIP the leg** — start from the asymmetric END still (extended pose) and animate the
  RETURN to tabletop; the initial state pins which limbs are in motion. Even then only a ~1s window was
  clean (the return, cut 2.6→3.6 of a 4s leg); palindrome makes it extend-and-return. Expect to burn
  2-3 legs on any opposite-arm/opposite-leg move, or shoot these as real footage someday.

### Keep-and-reverse works prospectively
Both leg-press START candidates came back at the BOTTOM of the rep (the models bias toward the loaded,
"interesting" pose on machines). Instead of re-prompting, use the good bottom frame as the END still
and edit BACKWARD to the extended start ("EXTEND his legs... platform pushed far away") — same recipe
as batch 2's wrong-phase trick, applied by choice.

### Three new still-failure axes (add to the batch-2 table)
| failure | fix language |
|---|---|
| **profile request comes back FRONTAL** (standing dumbbell moves: rdl, goblet) | "TRUE SIDE PROFILE — the camera is directly at his LEFT side, his chest and the logo face the RIGHT edge of the frame, away from the camera. This is NOT a front view." |
| **hanging dumbbell RESTED on the bench** (db-row, both candidates) | "suspended in MID-AIR clearly BELOW the level of the bench top... absolutely NOT resting on the bench, NOT touching anything. Do NOT draw the dumbbell lying on the bench — that is wrong." |
| **end-still edit RE-RIGS the cable** (pushdown lockout moved the rope to a low pulley) | "the rope stays connected to the SAME HIGH PULLEY... the cable runs UPWARD from his hands... do NOT re-attach the cable to a low pulley — that is wrong." |

### Write prompts against Dan's r2 revision bar from the start
The r2 revision session's fix list (in `_r2/spec.js`) IS the quality spec: full ROM to a NAMED endpoint
(row touches the stomach, heels to glutes, chin over the bar with daylight), joint-safe positions (no
dead hangs, press bottoms stop just below 90°), zero cheating (elbows pinned, no hip swing, no shrug,
no torso rock), name-the-wrong-answer, and physical analogies ("closing a door behind you with your
butt", "tipping out two jugs of water"). Batch 3 wrote every prompt this way and needed no form
revisions at the still stage beyond the axes above.

### Misc
- The clone still reads ~30% slow — a 5-cue script lands 23-26s spoken; trim to 4 cues for tight moves.
- buildrep's `sig()` hardcodes a 6.0s scan window — it crashes on 4s legs; pass the manual `t0 t1` args.
- SendUserFile has a 30 MiB phone limit — a ~26s narrated MP4 can exceed it; re-encode a crf-22 review
  copy for delivery and keep the master on disk.

---

## Batch 2 revision round (10 exercises, 2026-08-20) — Dan's form notes and what fixed them

Dan revised 10 of the 20. Scripts preserved at `Media/exercise-demos/_r2/` (spec.js, run-veo.js with
transient auto-retry, buildrep.py with manual-segment override, calf-kling.js). All his form standards
below are SETTLED — bake them into future prompts so they never recur:

- **Lying leg raise: legs to 45°, never vertical.**
- **Pull-up: chin clearly OVER the bar at the top, and a slight elbow bend at the bottom — never a
  dead hang at full extension** (shoulder safety, and he wants the VO to say so).
- **Seated cable row: pull until the handle TOUCHES the stomach** — full back contraction, not near it.
- **Leg curl: full range, heels close to the glutes, well past 90°.** A 2-inch partial is a reject.
- **Shoulder press: SEATED, and the bottom stops just below 90°** — deep elbows are a reject.
- **Curls: elbows tucked against the ribs and torso dead vertical** — any hip swing is a reject, and
  the demo must not contradict its own VO.
- **"Side Lateral" (renamed from Lateral Raise): elbows bent near 90°, elbows LEAD and finish slightly
  ABOVE shoulder height, hands below elbows — the jugs-of-water pour. VO carries that cue.**
- **Calf raise: on the edge of a step/box holding something for balance, heels below the step at the
  bottom, knees locked straight throughout.**
- **When Dan says "look it up on YouTube": actually do it** (Browser pane, pause loop, seek) and match
  the reference — it settles the target pose before any spend.

### Technique findings this round
1. **A wrong REP CUT can masquerade as a wrong generation.** The lat-pulldown "double-take" was the cut
   running past the bottom into a partial second rise; the fix was a recut, $0. Before regenerating a
   flagged rep, re-inspect the leg — the clean movement may already be in it.
2. **Veo CANNOT do the superman lift** — three attempts all became press-ups/cobras (hands planted). The
   fix that worked: generate the LOWERING direction (image = the correct hold still, last_frame = flat),
   which Veo can't reinterpret, then reverse the segment for the lift. **When Veo repeatedly misreads a
   lift, generate the descent and play it backwards** — valid for any slow symmetric motion.
3. **Veo CANNOT do a calf raise on a box** — two attempts wandered/stepped off/marched, even with
   stay-planted language and last_frame set. **Kling v3 (10s standard, ~$0.70) nailed it first try**:
   slow full-range reps, feet glued. For small-footprint in-place motion where Veo restages, Kling with
   a precise "never steps, never lifts a knee, only the ankles move" prompt is the better engine.
   Kling appearance drifts over 10s, so direct-loop cuts pop (~6.1 frame diff) — palindrome a single
   rise instead.
4. **Overshoot in the leg is recoverable in the cut**: the 45° leg-raise leg went to vertical, but
   crossing 45° happened at t=1.0 — cutting there gave exactly Dan's spec. Generate generous, cut precise.
5. **Editing a still to add a partner object (machine post to grip) works cleanly** as a second pass on
   an approved still — don't cram every prop requirement into one generation.
6. **Toes-on/heels-off a box defeated 3 straight still generations** (model kept reversing it). What
   fixed it: an explicit COMMON-MISTAKE negative example in the prompt ("do NOT draw toes hanging off
   and heels on the box — that is backwards"). Name the wrong answer when a spatial relation keeps flipping.
7. **Google Veo "high load" (code 8) days happen** — this round hit ~10 transient failures. The runner
   retries with 90s+ backoff automatically; a watchdog monitor relaunches an exhausted runner. Budget
   real wall-clock time on such days; the money cost is nil (failed creates don't bill).

Cost of the revision round: ~$13 (11 stills ~$1.50 · 10 Veo legs incl. 2 discards ~$10.40 · 1 Kling 10s
~$0.70 · 6 VO clips ~$0.06). Running total for batch 2 + revisions: ~$72.

---

## THE DOUBLE-PUMP RULE (Dan's #1 complaint, 2026-08-20) — MANDATORY on every rep build

Dan rejected 6 of 10 revised demos for one defect: the rep goes "up, then down, then up again" —
reading as a glitching AI loop, not a real person. **Root cause: rep cuts that include ANY
non-monotonic wobble get that wobble MIRRORED by the palindrome, so it plays twice back-to-back at
every loop boundary.** Veo legs almost always contain settling jitter before the real movement (the
pull-up leg had a full partial rise before the true pull; the press leg had two bounces at the bottom).

**The fix, now tooled in `_r2/mono.py` — use it on EVERY rep:**
1. `analyze <id> <leg> [x w y h]` — dense 12fps frame-diff signal vs frame 0, with an optional region
   crop (**whole-frame diff saturates once the body leaves the start pose; scope to where the moving
   part travels** — the overhead zone for presses, the heel arc for curls).
2. Cut ONLY a **strictly monotonic** run: from the true zero-velocity turnaround (a local minimum,
   often NOT t=0) to the first frame of the peak. `cut` refuses >8% dips; `qcunit` then verifies the
   built unit is one smooth unimodal pulse (≤10% secondary bumps) — run it on every unit before
   assembling.
3. Boundary check on the FINAL video: frame diff across the loop seam should be ≤~20% of the mid-rep
   motion range (this round measured 5–18% on all six).
4. **Short monotonic runs are fine** — slow them with
   `setpts=N*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1` (motion-interpolated slow-mo,
   artifact-free on static-camera gym footage up to ~3.5x). Cut precise, then stretch into the
   2.5–4s tempo band. Never keep a wobble just to make the rep longer.
5. The bottom cut point also SETS the rep's visible depth — the seated press's "slightly below 90°"
   bottom was chosen this way from a deeper leg, free.

Also from this round: a real cycle inside one leg (Kling calf raise) still cannot be direct-loop cut
— appearance drift makes even matching poses differ (~6.1 frame-diff); palindrome the rise instead.

---

## THE BACKGROUND-GHOST SCAN (Dan's instruction, 2026-08-20) — MANDATORY before delivery

Dan caught weight stacks on background cable machines pumping up and down in time with the seated
press — nobody on the machines. **Video models animate sympathetic background motion; QC must look at
the whole frame, not just the exercise.** Tooling: `_r2/ghost.py <id>` builds a per-pixel motion
heatmap across the unit, finds the subject's motion box, and flags any stray motion outside it.
Run it on EVERY unit; eyeball each flag (his own head/feet micro-shifts flag too — that's fine;
machinery moving is not).

**Fixing a ghost costs $0 when the camera is locked off:** overlay a static patch cropped from frame 0
over the offending region for the whole unit (`overlay` of `crop`s from a frame-0 PNG) — seams are
invisible because it is the same pixels. Verify with a second heatmap (press: stack regions dropped
from sd~30 to sd~1). Exception: equipment the subject is actually USING should keep moving (the
row/pulldown stacks he pulls).

Other fine-detail rules settled this round:
- **Pull-up bottom: a FEW degrees of elbow bend** — visibly more straight than "soft", never locked.
  Found for free by cutting the rep from the leg's DESCENT (reversed), whose bottom frames pass
  through exactly that pose.
- **Leg curl finishes slightly PAST 90°** — shin beyond vertical, and Veo often creeps deeper after
  the first "top": extend the cut to the true depth peak rather than the first plateau.
- **Side-lateral top: elbows clearly above the shoulder line AND dumbbells tipped nose-down 45-60°**
  (the pour). Wrist-tilt asks work as a still edit ("front head of each dumbbell points steeply
  DOWNWARD… pinky rotates up").
- The VO must match the video's numbers — the leg-raise video was capped at 45° while the VO still
  said "vertical". When a movement spec changes, re-read the VO script for stale numbers.

---

## Batch 3 revision round (2026-08-20) — new settled rules

Dan's revisions on batch 3 (8 of 10; face-pull and incline-pushup approved as generated). New standards:
- **Machines must look like REAL equipment** — the leg press v1 had a nonsense frame (inert bar above
  the shoulders, no plates, no stack). Name the commercial archetype in the prompt ("plate-loaded
  45-degree leg press exactly like a Hammer Strength", "45-pound plates on each side sleeve") and name
  the wrong answers ("NO cable, NO pulley, NO weight stack, NO bar above his shoulders").
- **Dumbbell bench grip: handles run ACROSS the body like a barbell**, palms toward the feet — never
  fore-aft. A 90° rotate is a clean still edit ("the hexagonal end face of the near dumbbell points at
  the camera").
- **Row: dumbbell to the lower ribs, elbow ABOVE the back line, hard shoulder-blade squeeze — and the
  VO carries the "pulling the starter cord on a lawnmower" cue with a back-contraction focus.**
- **Alternating-limb moves (dead bug, bird dog) must SHOW BOTH SIDES**: generate a mirrored side-B end
  still (edit of the same start still — swap which limbs extend), a second Veo leg, and build the loop
  unit as [side-A rep]+[side-B rep]. Two reps per unit, ~3s each.
- **Cross-leg seams need xfade**: when a unit joins segments from two different Veo legs, the shared
  pose renders slightly differently per leg (dead-bug tabletop measured 8.6 frame-diff). Build the
  looped video with 0.3s xfades at every boundary (xfade chain, not -stream_loop) — reads as settling.
  (bird-dog joined at 1.27 without help because BOTH legs used the same b3-start still as their
  all-fours anchor — anchor multi-leg builds on one shared still when possible.)
- **The ANTIPUMP motion-prompt block works** — append to every motion prompt: "from the very first
  frame to the very last frame the movement progresses in ONE direction only, at a steady controlled
  speed. He NEVER pauses partway, NEVER reverses slightly and continues, NEVER does a partial
  repetition first, NEVER bounces, and NEVER makes any small preparatory or adjustment movements."
  With it, 8/8 revision legs passed mono.py's strictly-monotonic gate on the first attempt.
- **The mono.py + qcunit + ghost.py pipeline is now MANDATORY on every rep** (see THE DOUBLE-PUMP RULE
  and BACKGROUND-GHOST SCAN sections above). Never accept a cut from a 0.4-0.5s frame sheet again —
  round 1's three double-pumps all hid between sparse samples.

---

## Batch 3 second revision (2026-08-20) — the region-scoping rule is absolute

- **A whole-frame monotonic gate is NOT sufficient** — the RDL passed it (2.3% dip) yet had a "severe
  double pump": once the torso is down, whole-frame diff saturates and 3 seconds of bottom-bobbing
  reads as a flat plateau. **Always re-run mono.py analyze with a region crop scoped to the moving
  part** (torso arc for hinges, hands for pushdowns, feet strip for anything foot-planted) before
  trusting a cut. The region signal exposed: RDL's true hinge = first 0.96s only; the pushdown leg's
  SECOND rep locked out deeper than the first but had no valid top (cut the still instead); the goblet
  foot shuffle lives at 0.33-0.92s INSIDE the descent (uncuttable — engine swap to Kling).
- **Veo bobs at the bottom of hinges** — after reaching depth it fills remaining duration with
  micro rises/dips. Cut to the FIRST arrival at depth, never through the hold.
- **Two Veo fails on the same foot-planted move = switch to Kling** (goblet joined calf-raise).
- Dan's settled standards this round: bench bottom = elbows slightly PAST 90°, dumbbells slightly
  below chest line (stretch); pushdown bottom = arms PERFECTLY straight, elbows locked, triceps
  flexed; alternating-limb exercises must never ship single-side or with visible seams (dead-bug/
  bird-dog were finalized only because he's dropping them).
- **Replicate HTTP 402 = account credit drained** (see provider-credit-outages memory) — kill retry
  loops immediately (they can't succeed) and hand back to Dan; topping up is outside standing auth.

### Gemini-API Veo fallback (2026-08-21, Replicate credit drained)
`_batch3/run-gveo.js` — `models/veo-3.1-fast-generate-preview:predictLongRunning` with GEMINI_API_KEY
(bakeoff/.env). Constraints found: **no `lastFrame`** (400 "use case not supported" — plain i2v only),
**1080p requires 8s** (4s+1080p rejected), **audio-directive words ("exhales", "room tone", "no music")
trip an audio safety filter** — strip them from prompts on this path. Because keyframe-locking is
unavailable, generate the leg as an ASCENT from the bottom/lockout still (flip trick) so depth is
guaranteed, then reverse for the descent; expect multiple reps + appearance drift in 8s — region-gate
and cut ONE clean ascent. ~$0.15/s (8s ≈ $1.20) — cheaper than Replicate Veo. Also: on 8s multi-rep
legs the LAST frames drift from the anchor still — prefer runs that include t=0 (the exact still).

### THE VELOCITY-BOUNDARY RULE (2026-08-21) — the actual root cause of double pumps
The monotonic-distance gate misses the killer case: **a settle wobble or hover at the segment
boundary**. Distance-vs-frame0 can pass while frame-to-frame VELOCITY shows motion decaying to zero,
wobbling, then the real rep starting — and the palindrome MIRRORS that boundary wobble into a visible
double-touch at every loop turnaround. Mandatory final check on every rep segment:
1. Compute frame-to-frame velocity (24fps consecutive diffs, region-cropped).
2. The segment must be one clean velocity BELL: accelerate from ~0 at one boundary, decelerate to the
   true minimum at the other. TRIM any leading/trailing frames where velocity decays/oscillates
   before the bell (bench: frames 0-0.17 were a settle; cutting [0.17,1.33] fixed the pump).
3. If the distance peak arrives while velocity is still high (Veo overshoots then backslides — the
   pushdown's lockout at t=1.0 with v=4.5 then a 6% backslide): cut AT the peak and append a
   ~0.17s tpad clone HOLD of the extremum frame before the reversed half. Reads as a deliberate
   squeeze/pause at the contraction and kills both the bounce and the backslide.
4. Verify the finished unit: min velocity across the loop junction should be a SINGLE dip (bench:
   0.46→0.03→0.30 = one touch-and-go).

### Background freeze > spot patches (goblet/bench, 2026-08-21)
When ghost.py flags stray machine motion, don't patch cells — **freeze the entire background**:
overlay the live video cropped to the subject's corridor onto a full-res frame-0 still
(`crop=W:1080:X:0` + `overlay=X:0`). Camera is locked so the seam is invisible; one command kills
every ghost at once. Size the corridor from the motion heatmap and REMEMBER the hips swing BACKWARD
in squats/hinges — cells just outside the torso may be his glutes, not a machine. Verify with a
second heatmap (STRAY=NONE) and eyeball 3 frames for seam clipping.

---

## Background lock, round 2 (2026-08-20 late) — what the ghost scan MISSES and the tools that close it

Dan caught pumping stacks in the press and side-lateral AFTER `ghost.py` said clean. **Why the scan
missed them: ghost.py excludes the subject's whole bounding box, and machinery INSIDE that box (behind
his arm sweep) is never checked — and a stack pumping only while his arm passes near it registers as
"arm motion."** Fixes, all in `_r2/`:

1. **`bglock.py validate <id> x y w h`** — before freezing any rectangle, measure per-frame how much
   of the box ever differs >50 gray levels from frame 0. <8% = he never enters, plain-freeze safe
   (`bglock.py apply`). His arm sweep zones fail this test — rectangles are NOT usable there.
2. **`keyfreeze.py <id> "x,y,w,h;…"`** — the fix for stacks BEHIND the arm's path: per-pixel keyed
   composite inside the box — plate (frame-0) pixels unless the current frame differs strongly
   (threshold 45, dilate 9, blur 3), so his arm stays live while the machinery behind it is pinned to
   the plate. Verify with arm-free frames: max diff vs plate ≤3 gray levels = locked.
3. **Verification standard**: check background stillness on ARM-FREE frames (diff vs plate ≈0), not
   via stdev, which cannot distinguish "arm passes in front of tower" from "tower stack moves."

Rep-cut findings this round:
- **A 4s "one rep" ask still returned 2 partial pulls, and a 6s "EXACTLY ONE repetition" ask returned
  3 pulls.** Veo simply does not obey rep count (batch-1 finding, reconfirmed twice) — but MORE
  attempts per leg means more candidate pulls, and the winning cut ([2.27→2.98] of the 6s leg) had
  BOTH the almost-straight bottom and the chin-over top in one monotonic run. Generate 6s, expect to
  shop among the reps for the one that hits every form beat.
- **When neither rep in a leg satisfies all form requirements, re-roll the leg before compositing
  anything** — a fresh roll that contains the right rep beats surgery across takes.
- Pull-up bottom spec (FINAL, Dan-settled): arms within a FEW degrees of locked — visibly nearly
  straight, never fully locked, never obviously bent.
