# Handoff — Website conversion video, REVISION 6

**Written 2026-09-09 from Dan's rev-5 review. Not executed.**
Working dir `/Volumes/Extreme/_edit_work/website-video-828/`. Skill: `/ad-edit` (read it — lessons 107–117 are
this video's history). Rev 5 is delivered at
`claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
(3:50.23, all gates green); rev 4 sits beside it as `*_REV4.mp4`.

Rev 5's framing is **LOCKED and approved** ("You nailed it with this one"). Six changes, nothing else.

---

## ✅ SETTLED 2026-09-09 — it is the VIEWER'S LEFT, and there are TWO deliverables

Dan picked it off the marked sheet: *"the upper-left-hand screenshot, the blue rectangle."* That is **box A —
viewer's left, his right cheek, the dimple area beside his mouth** — exactly as he first described it. His words
were right; my first sweep was hunting a bigger signature than the blotch actually has.

**He also wants two exports of this revision, so he can judge the retouch himself:**

| | file | contents |
|---|---|---|
| **A** | `website_video_16x9_A_tan-corrected.mp4` | every change in this doc **including** the blotch correction |
| **B** | `website_video_16x9_B_tan-as-is.mp4` | every change in this doc, blotch **left alone** |

Both go through the full gate suite and both get a 540p review copy. Also build **`AB_tan_face.mp4`** — the face
region only, corrected vs as-is, cut together at four timestamps — so he can settle the retouch in twenty seconds
instead of watching 3:50 twice. On his pick, the winner is renamed `website_video_16x9.mp4` and the loser kept as
`website_video_16x9_ALT.mp4`.


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

## Item 2 — The pale blotch beside his mouth (viewer's left)

Dan: *"see if there's anything we can do to try and minimize that appearance… so my face looks even, but still
looks natural and not like I edited my face."*

**Measured on the delivered rev-5 master at 14.0 s** (the frame he pointed at), inside a hand-placed box he
confirmed — not from a detector:

| | |
|---|---|
| location (1080p, that frame) | centroid **x 985, y 288**; extent x 950–1014, y 255–342 |
| size | **1449 px above +8 L**, ≈ a 38 px square — small, which is why a broad sweep missed it |
| blotch vs surrounding cheek | RGB **124/76/63** against **108/66/54** |
| delta | **+15.7 R, +9.7 G, +8.7 B**, mean **+11.4 L**, peak **+25 L** |
| saturation | 0.493 vs the cheek's 0.500 — very slightly paler, i.e. tan that did not take |

**The useful finding: it is almost exactly a multiplicative lift, not a hue shift.** The per-channel ratios are
1.145 / 1.148 / 1.161 — flat across R, G and B. So the correction is a **feathered ×0.87 gain** on the patch, and
124/76/63 × 0.87 = 108/66/55 against a cheek of 108/66/54. That lands on the surrounding skin almost exactly
**while preserving texture and colour ratios**, which is what makes it read as skin rather than as a retouch. Do
not blur, clone, or desaturate — a gain is the whole fix.

**⚠ Do not find it with a brightest-blob search.** I tried, across six frames: outside the hand-placed box it
locks onto the doorframe and blown highlights on his jaw (RGB 173/157/155 — near-grey, and it still passes the
loose `r>g+10` skin test). Only the 14.0 s measurement above is trustworthy. So:

- **Anchor the region off face landmarks** (mouth corner / nostril / eye line) on the **graded 4K base**, the way
  `hairtrack.py` samples and maps through `tight_cuts.json` with a `keeps_sig` so a stale track fails the build.
- **Validate by eye at native scale before rendering** — a proof sheet of the tallest/most-turned frames with the
  region drawn on, per lesson 107. A mask that is 40 px off is a smear on his cheek.
- **Under-correct deliberately.** ×0.90 rather than ×0.87 if it is at all uncertain; leaving a third of it is the
  correct failure mode against "not like I edited my face."
- **Sanity gate:** measure patch-vs-surround on N sampled frames before and after and assert the **variance across
  frames** drops. A correction that flickers is worse than the blotch.
- If the track cannot hold a lock through the big head turns, **say so and ship version A without it** rather than
  shipping something that moves — version B exists precisely so that is not a disaster.


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

**The two versions branch AFTER the mix, not before** — that is what keeps this affordable. Correcting at the
punch stage would mean two punch renders *and* two mixes (+45 min over the plan below). Instead: punch once, mix
once, then run the tan-correction pass over `nocap.mov` for version A. The patch sits on his face, which is never
under a graphic, so the pass is safe — but **assert it**: only touch frames where Dan is actually on camera (skip
the AI-insert and full-frame-card beats) and assert the region never intersects the phone box
`[150,130,583,950]` or a card's alpha.

**Run version B through the same pass with the correction disabled.** It costs ~8 minutes and removes the only
confound in the comparison — otherwise A carries one more encode generation than B, and Dan is being asked to
judge exactly the kind of subtle difference that could hide in it. Same encode settings for both (CRF 16).

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
7. **The tan pass, twice** — `nocap.mov` → `nocap_A.mov` (correction on) and → `nocap_B.mov` (correction off),
   identical settings. ~8 min each.
8. **Audio** (item 1) on both — `MUSIC_DB=-44 COMP=0 python3 audio3.py` with `VIN`/`VOUT` per branch, plus whatever
   the dereverb work changes. **Fit the audio ONCE and apply the identical chain to both**; the two versions must
   differ only in the picture, or the comparison is worthless.
9. **`captions.py`** on both (it already takes `VIN`/`VOUT`), then **`deliver.sh`** on each master. `deliver.sh`
   hardcodes `M=website_video_16x9.mp4` — parameterise it. Every gate is per-file (the audio stamp is keyed to the
   file's sha256), so **both masters must pass on their own.**
10. **Build `AB_tan_face.mp4`** — the face region from A and B at four timestamps where the blotch is visible, cut
   together and labelled, the way the audio A/B works.
   ⚠ **Export `OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6` before `deliver.sh`.** Whisper
   thread-thrashes on a loaded box: 12 % CPU and 2 minutes of CPU time in 20 minutes of wall clock, against
   40 % and ~4× faster with the cap. This is not in the script yet — put it there.

**Rough total ≈ 2 h 40 m of machine time** (the second version adds ~35 min: two tan passes, an extra caption burn and an extra gate run). Check `ps -Ao command | grep -E 'ffmpeg|whisper'` before starting and cap
concurrent builds at two across all sessions (`AGENTS.md`).

## Gates — all of them, unchanged

`deliver.sh` runs the audio gate + stamp, the contact sheet, `qc.py` (+ `qc_frame.py` + `hairgate.py`),
`watch.py` and the review copy. Rev 5's marks to beat or match: audio 11/11, QC all checks, script fidelity
99.0 %, caption clearance 62–73 px, hair 43 px min / 57 median with 0 of 4754 frames failing the independent
top-rows test, watch 0 frozen / 0 black. **The hair gate must still pass after the punch re-render** — the crops
are anchored per segment, and a new PIP segment at NUM2 gets its own anchor.

Deliver **both** masters (`website_video_16x9_A_tan-corrected.mp4`, `website_video_16x9_B_tan-as-is.mp4`) with rev
5 preserved as `*_REV5.mp4` (rev 4 is already `*_REV4.mp4`), copy `pv/` and `recipe/` across, write one `notes.md`
covering both, and send both 540p review copies, `AB_tan_face.mp4` and the audio A/B. On Dan's pick the winner is
renamed `website_video_16x9.mp4` and the loser kept as `website_video_16x9_ALT.mp4`.

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
> `audio3.py` never dereverbs and the room measures 77 ms against his 40); minimising the pale spray-tan blotch
> beside his mouth on the **viewer's left** (confirmed by Dan — measured at 14.0 s as a flat ×1.15 multiplicative
> lift, so the fix is a feathered ×0.87 gain; read item 2 and do NOT use a brightest-blob search, it finds the
> doorframe); replacing the 2:08 dumbbell-curl AI clip with toe-touches at home with no weight; replacing the 1:24
> lower third with a phone PiP scrolling the real AI Trainer program and opening two or three exercise sheets that
> have AI demos (never a stick figure — only the 33 ids in `public/exercise-demos/`); and regenerating the three
> meal clips at 2:28–2:44 with steak instead of chicken. **Deliver TWO masters** — `_A_tan-corrected` and
> `_B_tan-as-is` — both carrying every other change, both through the full gate suite, plus a face-region A/B clip
> so he can judge the retouch quickly. Read `/ad-edit` first, especially lessons 107–117; the framing is locked and
> approved, so do not change it. Work in `/Volumes/Extreme/_edit_work/website-video-828/`. Budget ~$10 of
> Veo/nano-banana spend and state the estimate before the batch. Send both 540p review copies, the face A/B and the
> audio A/B when done.

**Model:** Fable 5.1, effort **high**. It is a long multi-stage build with generations, a tracker, an app
capture and four render stages — worth the effort setting, and Fable is the standing choice for this project
(memory `astra-vs-fable-verdict`).
