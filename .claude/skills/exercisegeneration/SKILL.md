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
5. **Extract the clean rep** — Veo obeys the ENDPOINTS but NOT the rep count: fast bodyweight tempo
   (~3s/rep) means a 6s clip contains ~2 reps, often with a bounce. **Sample frames at ≤0.5s intervals**
   (a sparse sheet lied twice), find one full cycle standing→bottom→standing, cut it with ffmpeg, then
   **diff the cut's first and last frames** and nudge the boundaries until the poses match (bw-squat
   took two recut iterations). Cut BEFORE any mid-clip bounce (batch 1's lunge descent bounced at
   ~t3.2; cutting at the first full-depth frame avoided it).
   - **Two-leg builds: join descent + ascent with a 0.3s `xfade` at the zero-velocity bottom**, not a
     hard cut — the two legs render the subject at slightly different scale, so a hard cut pops; the
     crossfade reads as motion blur at the turnaround. Loop join is free: the ascent's `last_frame` IS
     the start still, so the rep ends where it begins.
   - Palindrome (segment + reverse) remains fine for SYMMETRIC in-place motion and for static-hold
     clips — just never for steps.
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
