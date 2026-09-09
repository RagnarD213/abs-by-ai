# Handoff — Website conversion video, REVISION 6

**Written 2026-09-09 from Dan's rev-5 review. Not executed.**
Working dir `/Volumes/Extreme/_edit_work/website-video-828/`. Skill: `/ad-edit` (read it — lessons 107–117 are
this video's history). Rev 5 is delivered at
`claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
(3:50.23, all gates green); rev 4 sits beside it as `*_REV4.mp4`.

Rev 5's framing is **LOCKED and approved** ("You nailed it with this one"). Six changes, nothing else.

---

## ⚠ ONE ANSWER NEEDED BEFORE ITEM 2 — which side of his face

Dan said: *"uneven on the right side of my mouth. On the left side, when you're looking at it, there's a little bit
of a white spot… right in my dimple area near my mouth."* He disambiguated to the **viewer's** frame twice.

**The measurable unevenness is on the viewer's RIGHT**, not the left. Proof sheets built 2026-09-09:
`pv/rev6/tanspot_sheet.jpg` (native + contrast-stretched, four frames) and `pv/rev6/tanspot_AB.jpg` (both
candidates boxed). On the viewer's right, a chalky mottled band runs down the cheek and jawline in every frame —
it reads as the edge of the spray-tan application plus the key light. The viewer's-left cheek (box A, the dimple
area he describes) measures smooth: +4.6 / −4.6 / −0.3 / −3.9 levels against its own surround across four frames,
i.e. no consistent bright patch at all.

**Do not start item 2 until Dan says "viewer's left" or "viewer's right."** Fixing the wrong cheek is a wasted
render and a face edit he did not ask for. The marked image was sent to him on 2026-09-09; if he has not
answered by the time you run this, do items 1 and 3–6 and leave 2.

---

## Item 1 — Audio: another pass toward Muhammad's

Dan: *"the audio is pretty good, but I feel like there's room for improvement… another pass at making the audio
sound more like Muhammad's."*

This **supersedes the standing "do not touch the audio chain" rule** carried by the rev-3/4/5 handoffs. He
approved this chain by ear on rev 2 ("you got it nailed"), so the bar is: measurably closer to the reference on
the rows that are furthest off, with **no regression** on the rows he already liked, and an A/B he can judge.

**Where rev 5 actually sits against his ad** (from `website_video_16x9.mp4.audio_gate.json`, all 11 rows PASS):

| row | ours | his | limit | gap |
|---|---|---|---|---|
| **early decay (room)** | **77 ms** | **40 ms** | ≤ 80 | **the big one — 1.9× his, and 3 ms from failing** |
| **speech spread p90–p10** | **5.6 dB** | **8.2 dB** | ≥ his − 3.0 | **2.6 dB flatter than his, 0.4 dB from failing** |
| LRA | 2.8 LU | 3.5 LU | — | flatter |
| tone | 0.88 mean / 2.02 max | — | ≤ 1.2 / 2.5 | fine |
| voice-over-floor | +2.5 / +0.5 / +0.2 dB vs his | — | ≥ −3.0 | fine |
| dryness | 8.8 dB | 7.4 | ≥ his − 1.5 | fine |
| loudness / TP | −14.50 LUFS / −2.60 dBTP | — | — | fine |

**The lead, and it is a strong one: `audio3.py` never dereverbs.** Its chain is
`highpass → 8 parametric bands → treble shelf → agate → pan → measured gain + alimiter`. The shared
`_shared/audio/voice_chain.py` dereverbs whenever the room measures > 55 ms; this video measures **77** and gets
nothing. This is the same defect that got the spray-tan shorts rejected (85 ms vs his 40) and was fixed there
with spectral dereverb down to 29–40 ms — see `/ad-edit` lessons 28 and the coordination entry for shorts 01.

Two things to do, in order, gating each on the A/B:

1. **Dereverb.** Port the spectral dereverb from `_shared/audio/voice_chain.py` into the website video's chain (or
   switch the video to `voice_chain.py` outright, fitting the EQ per lesson 87 — fit against the gate's own
   metric, iterate, and **ship the first smooth passing curve**, never the over-fitted comb). Target EDT ≤ 50 ms.
2. **Stop crushing the dynamics.** `agate=threshold=0.012:ratio=1.8` plus +9.0 dB into the limiter is what puts
   spread at 5.6 against his 8.2. Back the expander off and re-measure spread *and* floor together — they trade
   against each other (lesson 89: the loudness finish alone costs 0.5–2.6 dB of floor).

**Do not** re-fit the EQ from scratch first — tone already passes at 0.88 dB mean. Fix the room and the dynamics,
then re-check tone and refit only if it moved.

**Re-transcribe the finished mix and diff it** (lesson 29): an expander change that eats a fricative shows up as
a fidelity drop, not as something you can hear in a spot check. Rev 5 is at 99.0 %.

**Deliver an A/B either way** (`AB_his-vs-ours.mp4` is rebuilt by `deliver.sh`) — "sounds better" is only
settleable by ear, and this is the second time he has asked.

---

## Item 2 — The uneven spray tan near his mouth  *(gated on the answer above)*

Dan: *"see if there's anything we can do to try and minimize that appearance… so my face looks even, but still
looks natural and not like I edited my face."*

**A fixed rectangle will not work, and this is measured, not assumed.** The same fixed box scored +8.3, −16.3,
−15.9 and +42.4 levels against its surround at 14 s / 45 s / 100 s / 200 s — because his head moves inside every
hold and the crop changes with the punch level. The patch is a feature *on his face*; it must be tracked.

**Recommended approach — reuse the machinery this video already has:**

- Track the face on the **graded 4K base** (`base.mov`), exactly the way `hairtrack.py` does: sample at 4–8/s,
  map each sample through `tight_cuts.json`, store with a `keeps_sig` so a stale track fails the build. Anchor
  the region off a landmark you can find robustly at 4K (the mouth corner / nostril), not off frame coordinates.
- Apply the correction **inside the punch pass**, before the crop, so there is one 4K→1080p encode and the
  approved framing is untouched. `crop_for()` already gives you the per-segment crop to map into.
- The correction itself: a **soft-edged local gain/tint** pulling the patch toward the surrounding cheek's median
  in each channel — not a blur, not a clone. Feather generously (the patch has no hard edge) and **under-correct
  deliberately.** Dan's constraint is "natural, not edited"; leaving 30 % of it is the correct failure mode.
- Sanity gate: sample N frames, measure patch-vs-surround before and after, and assert the *variance across
  frames* dropped — a correction that flickers is worse than the patch.

Budget ~45 min including the tracker. If the tracker cannot hold a lock (he turns his head a long way at some
punch levels), **say so and ship without it** rather than shipping a smear that moves.

---

## Item 3 — 2:08, replace the curls with toe-touches

Dan: *"the way he's doing these curls is a little bit unnatural-looking… change this to him doing the toe-touches
ab exercise at home without weight."*

The beat is **`AI_C1` = 123.777 → 129.963** (2:03.8–2:10.0), currently "glances at the plan on his phone, then
dumbbell curls in a garage gym." Independent corroboration that he is right: the rev-5 watch pass flagged **23 of
its 30 unexplained jumps inside this one clip.**

- Regenerate **C1 only.** `AI_C2` (129.963–135.513, the water/towel/nod) stays — it is a straight cut from C1 and
  Dan did not complain about it, so the new clip must end in a state that cuts cleanly into it.
- **Same man**, same reference still (`ai/stills/C1.jpg` is the current one; the man's reference is in
  `ai/prompts/`). Continuity across the seven clips is the whole point of the character.
- Setting: **at home, no weight** — toe touches (lying on his back, legs up, reaching for the toes). Home living
  room / bedroom floor, not the garage gym, per Dan.
- Prompts: `/ad-edit` Step 4.5 verbatim — no camera/lens/rig/post/grandeur vocabulary, fight the model's default
  person, frame it slightly wrong, hold ambience density constant with the other six clips.
- **Lesson 110:** Veo's "celebrity likeness" filter is per still, not per character. Budget one retry; filtered
  attempts are not charged.
- **Lesson 115 is mandatory here:** strip the first and last second at 0.1 s and *look* before it goes in. A rep
  exercise ending on a static hold is exactly the beat the model drifts.
- **Lesson 111:** scan for a baked cross-dissolve; if there is one, use `build_inserts.EDIT` to cut the two clean
  shots together (the machinery is already there and `ai_d2` is the worked example).

Cost ≈ $0.13/still + $1.20/clip, budget 2 attempts ≈ **$2.70**.

---

## Item 4 — 1:24, drop the graphic, show the real workout program

Dan: *"remove the graphic and replace this with a clip of scrolling through the workout program… only scrolling
through a few exercises slowly, where we have the AI demos right there. Don't show any of the stick figures…
just a little bit of the text showing it's customized and the AI workout program. Make this look impressive."*

The beat is **`NUM2` = 84.126 → 91.246** (1:24.1–1:31.2), currently the "2 — …" lower third over Dan.

**Read this before planning the shot — it changes the shot.** In `public/index.html:8898`, the AI demo video
renders **only inside the exercise sheet** (`openExerciseSheet`), not on the program list rows. And the fallback
when an exercise has no demo is `getExerciseAnim(...)` — **that is the stick figure Dan is banning.**
`EXERCISE_DEMO_IDS` gates it, and **33 exercises currently have demos live** (`public/exercise-demos/`, 66 files):
bird-dog, cable-tricep-pushdown, calf-raise, chair-dip, crunch, db-bench-press, db-curl, db-goblet-squat,
db-lateral-raise, db-rdl, db-row, db-shoulder-press, dead-bug, face-pull, glute-bridge, hollow-hold,
incline-pushup, knee-pushup, lat-pulldown, leg-curl, leg-extension, leg-press, lying-leg-raise, pike-pushup,
plank, pullup, pushup, reverse-lunge, seated-cable-row, side-plank, split-squat, superman, wall-sit.

So a pure scroll of the list shows no demos at all. **The shot that satisfies what he asked for is:** a short
slow scroll of the program (enough to read that it is a real customized week), then **open two or three exercise
sheets whose exercises have demos, with the demo playing**, scrolled so the video fills most of the phone and
the Setup / How to do it / mistake text sits below the fold. That is "focus on the AI demos, no stick figures,
no excessive text, looks like a real program someone would sign up for."

- **Force a demo-backed program.** Generate or seed the fixture's program from the 33 ids above only — one
  non-demo exercise in shot is a stick figure and a failed item.
- **Capture per lesson 113:** local `node server.js` with `DATABASE_URL=pgmem://local` and a fixture account
  (`.claude/launch.json` has the config), signup → admin beta-members → login, session token into
  `localStorage.absbyai_session_token` before the page loads. Never a real login.
- **Viewport 390×738 CSS at DPR 3 → 1170×2214** (lesson 114) so it fits the 433×820 phone box with no crop. The
  Ad-2 session's 390×664 is a different aspect and will crop.
- **Treatment: a third phone PiP beside Dan**, same box as MACRO and HUB (`PIP_BOX=[150,130,583,950]`) — rule 83,
  an app screen goes next to Dan over the footage, never on a plate. Add `"NUM2"` to `beats.PANEL`, drop
  `("num2", B.NUM2)` from `layout.GFX`, and build `gfx/pip_num2.mov` with `build_inserts.py` (copy the `hub()`
  path; write its `marks` json for the watch pass).
- **This changes the punch plan** (a PANEL beat takes the PIP level), so `punched.mov` re-renders — see the
  order of operations below. Do not try to reuse rev 5's punch for this one.

---

## Item 5 — The three meal clips: chicken → steak

Dan: *"for the clips starting at 208, those are all looking good. I want the same clips, but I would like to
change the protein from chicken to steak. Make it steak instead of chicken, and everything else the same in
those three clips."*

**Reading, stated because the timecode is off and this is dictated:** "those three clips" that are "all looking
good" are the meal run — **`AI_D1` 147.962–151.642, `AI_D2` 151.642–156.679, `AI_D3` 156.679–164.262**
(2:28.0–2:44.3): grilling, portioning into containers, eating. They start at 2:28, not 2:08; 2:08 is the curls
he asked to *replace* in item 3, and he would not call those "looking good" in the same breath. If anything
about that reading looks wrong when you re-read his message, ask before spending the generations.

- **Same three shots, same man, same kitchen, same actions, same lengths** — only the protein changes. Reuse the
  existing stills as the compositional reference; change chicken to steak in the prompt and nowhere else.
- **The rev-5 trims exist because of artifacts in exactly these clips**, and new generations will not inherit the
  fixes. `build_inserts.INPOINT` / `EDIT` currently hold `ai_d1: [(0.3, 4.3)]` and
  `ai_d2: [(1.0, 3.85), (4.7, 7.05)]` for the old clips — **re-derive both from the new footage; do not carry the
  old numbers over.** The beats are the contract, the trims are not.
- **Prompt away from the two known failures** (lesson 115): never ask for breath, smell, steam or leaning in near
  the face (that is what rendered as smoke out of his mouth), and never end a beat on a static row of objects
  (that is what drifted the containers). Have him still working at the end of each shot.
- Frame strips of the first and last second of all three, looked at, before they go in.

Cost ≈ 3 stills + 3 clips ≈ **$4.00**, budget retries ≈ **$6.70**.
**Total AI spend for items 3 + 5 ≈ $10, inside the $25/session standing cap.** State the estimate before the batch.

---

## Item 6 — implied by the above

Re-run everything downstream: mix → audio → captions → `deliver.sh`. The `qc.py` check that asserts NUM2's lower
third clears the captions must be updated when NUM2 becomes a PiP — caption clearance then measures against the
**phone box**, which `qc_frame.py` already checks for MACRO and HUB.

---

## Order of operations, and the render budget

Everything except the audio is upstream of the punch, so do it in this order:

1. **Generations and the capture first, in parallel with nothing** — toe-touches (item 3), steak ×3 (item 5), the
   trainer capture (item 4). Look at every strip. Nothing downstream is worth starting until these are approved
   by eye, because each one invalidates the mix.
2. **The face tracker** (item 2), if Dan has answered.
3. **`layout.py plan`** — diff it against rev 5's. It *will* differ (NUM2 → PIP). Before you accept a punch
   re-render, run the **lesson 116** check anyway: build the per-frame crop for both plans, intersect the
   differing frames with the opaque-coverage map, and see what is actually visible. The spray-tan correction
   forces the re-render regardless if item 2 is in scope.
4. **`layout.py punch`** (~20–25 min on a quiet machine).
5. **`build_inserts.py`** for the new clips + `pip_num2`, then the MOV-vs-beat check (lesson 95).
6. **`layout.py mix`** — **read lesson 117 first.** 21 inputs in one graph livelocked ffmpeg on 2026-09-08 (336
   threads all parked in `tq_receive`, 23 % CPU, 3.5 h projected for a 9-minute job). `MIX_STAGES=3` runs it as
   three passes through lossless rawvideo intermediates and finished in 24 min. The machine was quiet at load 2
   on 09-09 morning, so a single pass may be fine — **benchmark it first**: `MIX_T=20 MIX_OUT=/tmp/x.mov` should
   come back in ~38 s. If it is slower, or if `sample <pid>` shows every thread parked, use `MIX_STAGES=3`.
   Budget ~20 GB per intermediate; they are deleted at the end.
7. **Audio** (item 1) — `MUSIC_DB=-44 COMP=0 python3 audio3.py`, plus whatever the dereverb work changes.
8. **`captions.py`**, then **`deliver.sh`**.
   ⚠ **Export `OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6` before `deliver.sh`.** Whisper
   thread-thrashes on a loaded box: 12 % CPU and 2 minutes of CPU time in 20 minutes of wall clock, against
   40 % and ~4× faster with the cap. This is not in the script yet — put it there.

**Rough total ≈ 2 h of machine time.** Check `ps -Ao command | grep -E 'ffmpeg|whisper'` before starting and cap
concurrent builds at two across all sessions (`AGENTS.md`).

## Gates — all of them, unchanged

`deliver.sh` runs the audio gate + stamp, the contact sheet, `qc.py` (+ `qc_frame.py` + `hairgate.py`),
`watch.py` and the review copy. Rev 5's marks to beat or match: audio 11/11, QC all checks, script fidelity
99.0 %, caption clearance 62–73 px, hair 43 px min / 57 median with 0 of 4754 frames failing the independent
top-rows test, watch 0 frozen / 0 black. **The hair gate must still pass after the punch re-render** — the crops
are anchored per segment, and a new PIP segment at NUM2 gets its own anchor.

Deliver over `website_video_16x9.mp4` with rev 5 preserved as `*_REV5.mp4` (rev 4 is already `*_REV4.mp4`), copy
`pv/` and `recipe/` across, write `notes.md` in the house format, and send the 540p copy plus the audio A/B.

## Housekeeping

- No production code, no deploy, no native-retest trigger — unless item 4's capture needs a fixture-only change,
  which must not ship to production.
- Update the rev-6 entry in `AI_COORDINATION.md`, remove this doc from its HANDOFFS section and from
  `Handoffs/README.md` in the session that runs it.
- **No dashboard row** unless Dan asks (his rule, 2026-09-08).
- Copy the changed recipe back into `.claude/skills/ad-edit/reference/website-video/` and record anything
  measured in the skill's lesson list — the audio dereverb result and the face-tracking technique both belong
  there.

---

## Starter Prompt

> Execute `Handoffs/handoff-20260909-website-video-rev6.md` — revision 6 of the Abs By AI website conversion
> video, from Dan's rev-5 review. Six changes: another audio pass toward Muhammad's reference (the lead is that
> `audio3.py` never dereverbs and the room measures 77 ms against his 40), minimising an uneven spray-tan patch
> near his mouth (**check with Dan which side of his face first — the proof sheets are `pv/rev6/tanspot_AB.jpg`
> and `pv/rev6/tanspot_sheet.jpg`, and the visible unevenness is on the viewer's right while he described the
> viewer's left**), replacing the 2:08 dumbbell-curl AI clip with toe-touches at home with no weight, replacing
> the 1:24 lower third with a phone PiP scrolling the real AI Trainer program and opening two or three exercise
> sheets that have AI demos (never a stick figure — only the 33 ids in `public/exercise-demos/`), and
> regenerating the three meal clips at 2:28–2:44 with steak instead of chicken. Read `/ad-edit` first, especially
> lessons 107–117; the framing is locked and approved, so do not change it. Work in
> `/Volumes/Extreme/_edit_work/website-video-828/`. Budget ~$10 of Veo/nano-banana spend and state the estimate
> before the batch. Run every gate in `deliver.sh` and send the 540p review copy plus the audio A/B when done.

**Model:** Fable 5.1, effort **high**. It is a long multi-stage build with generations, a tracker, an app
capture and four render stages — worth the effort setting, and Fable is the standing choice for this project
(memory `astra-vs-fable-verdict`).
