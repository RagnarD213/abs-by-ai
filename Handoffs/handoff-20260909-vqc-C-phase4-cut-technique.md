# VQC-C — Phase 4: the cut technique that is actually Muhammad's advantage

> ⚠ **SCOPE CORRECTED 2026-09-11 — still live, but two of its six items moved.** Read this before firing.
>
> * **Item 2 (≥25 % push coverage / never one fixed crop) is now owned by
>   `handoff-20260911-video-quality-engine.md` Phase 1** — it registers the corpus checks `style:coverage`
>   and `style:static_run`. This document already said "or hand the row to VQC-B". **Do not build that row
>   here; verify it exists and move on.**
> * **Item 6 (`picture.json`, the picture reference) is the input to that document's Phase 4 (the locked
>   kit)** — same measurements: talking-head luma, shot-length distribution, cut rate, insert coverage,
>   graphic density, push coverage and ramp shape. **Build it here, and build it FIRST**, so Phase 4 can
>   consume it instead of re-deriving it.
> * **Items 1, 3, 4 and 5 are untouched and are the reason to fire this** — pose-matched picture cuts
>   (`piccuts.py`), 0 px landing, dead air paired with a picture cut, and the grade. Nothing else covers them.
>
> **Fire after Phase 1 of the engine document and before its Phase 4.** The related check `landing_check.py`
> is folded into the engine's Phase 1 gate; the *fix* for it (item 3) is still here.


**Part 3 of 4 of the video-quality programme.** Evidence and the full plan:
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.

**Can run in parallel with VQC-B** — it touches the *cutting* code, not the gate. It needs VQC-A's
corpus to prove the change is an improvement. **Fable 5.1, high effort. ~1–2 sessions.**
**$0.00 generation spend**, but this phase renders — respect the two-concurrent-build cap in `AGENTS.md`.

---

## The finding

Measured on the Ad 2 vertical by an independent audit on 2026-09-03
(`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/notes-vertical-v2.md`):

> *"The conform cut the picture at every AUDIO splice; **Muhammad cuts the picture on a pose-matched
> frame of his own choosing, 1–15 frames away from the sound cut (a J- or L-cut), so his cuts read as
> continuity and ours as jump cuts.**"*

**In plain terms:** when two takes are spliced, the sound and the picture do not have to cut at the same
instant. Ours do, so Dan's head visibly snaps position. Muhammad offsets the picture cut by a few frames
to a moment where Dan's body is in the same position in both takes.

**And the rule this replaces was measurably wrong** (`AI_COORDINATION_ARCHIVE.md:8564`):

> *"It said he hides every trim under a wide↔punch framing change ACROSS splices… **his talk-to-talk
> splices jump as much as ours (43 of his 72 exceed 4× his own median frame diff; ours 32). The real
> defect was that 100 % of attempt 1's talk ran at one fixed crop — that is what makes a tripod shot
> read as a webcam recording.**"*

So the fix is **not** "hide every join". It is two things: **pose-matched picture cuts offset from the
audio splice**, and **never running talk at one fixed crop**.

---

## The work

### 1. Promote `piccuts.py` into `_shared/cut/` — the highest-value item

It already exists, in the Ad 2 recipe folder, and already works: it renders both takes from the raw at
the grade and does a high-pass normalised cross-correlation against the candidate frames to find the
matching pose. **On Ad 2 it moved 22 of 33 cuts by −15…+10 frames at confidence ≥ 0.6.**

Generalise it so it does not depend on having an editor's finished cut to match against:

* **With a reference cut** (we are conforming to an editor's edit) — keep the existing NCC path.
* **Without one** (we are cutting from scratch) — search ±15 frames around each audio splice for the
  frame pair minimising pose difference between outgoing and incoming take, scoring on a
  **high-pass** (edge) difference over the torso/head region, not raw luma. A whole-frame gray diff is
  proven blind here — it scored a real jump cut at 2.0× its local median, i.e. "clean".
* Report confidence per cut; below threshold, fall back to the current behaviour and **flag the splice
  for the watch pass** rather than guessing.
* Length must be preserved exactly. Offsetting a picture cut changes which frames are used, not how many.

Wire it into `/ad-edit`, `/longform-edit`, `/shorts`, `/website-video`, `/shortad-from-longform`.

### 2. Never one fixed crop on talk

Gate it in `_shared/deliver/` (or hand the row to VQC-B): **≥25 % of talking-head runtime inside a push.**
Muhammad's reference: **14 pushes covering 39 % of talk.** `shortad`'s qc check 12 already asserts ≥25 %
— it exists in one skill; make it universal.

Related bounds already measured: zoom cuts must be **≥10 %** — a 6 % alternating punch-in still read as a
jump cut to Dan wherever his posture shifted between takes (`longform-edit/SKILL.md:379`). His punches
**ramp over ~0.5 s, hold, ramp out, and mostly SPAN splices** rather than landing on them — reproduce
that shape, do not step the zoom at the cut.

### 3. Landing error to 0 px at every cut

Same audit, second finding: the crop's per-segment median smoothing used a **full window at segment
ends**, so Dan landed **78–190 px off centre after each cut** and the crop panned him back over up to
1 s — a visible drift Dan would read as sloppy. `facetrack3.py`'s **shrinking end-window** took landing
error at every cut to **0 px** (max 16 px in source), with the crop following at ≤200 px/s. Port it.

### 4. Dead air to ~zero, but paired with a picture cut

His reference cuts and Waleed's round 1 both measure **zero dead air**; the spray-tan longform shipped
**36 %** against a 23 % target. Dan's own instruction: *"Remove every pause longer than ~0.3 s. Zero dead
air (reference edit had none)."*

⚠ **Two counter-measurements that must be honoured:**
* **A pause removal is itself as visible as the fault it fixes** — measured at **4.97–12.46** against a
  **1.30** adjacent-frame baseline (`shorts/reference/clean-master/work/pausejump.py`). So every removal
  needs a picture cut from item 1, or an insert, over it.
* **0.55–0.65 s is breathing rhythm, not dead air** (`shorts/SKILL.md:445`). Do not strip it.

### 5. Grade

He is **~6 luma brighter** on the talking head — 67 against our 55. Lift shadows to match; measure, do
not eyeball.

### 6. Build the picture reference, the way the audio one was built

`_shared/audio/reference/reference.json` pins Muhammad's audio by fingerprint. There is **no picture
equivalent**. Build `_shared/reference/picture.json` from the two finished Muhammad edits we hold
(`Muhammad Ad Videos/this picture got me abs - ad 1/…16x9…mp4` and `…nutritionists - ad 2/…16x9…mp4`):
talking-head luma, shot-length distribution, cut rate, insert coverage, graphic density, push coverage
and ramp shape.

⚠ **Bound our output to his ranges in BOTH directions, with a do-no-harm counterweight.** We already made
the overshoot mistake once: the dereverb hit EDT 32 ms against his 40 — *past* the target — and Dan
called the result "underwater". Memory: `audio-never-over-strip`. **Overshooting a reference is a
warning, not a win.**

---

## Done when

* `_shared/qc_corpus/run.py` is still green.
* Re-cutting **Ad 1 vertical attempt 1** (the corpus's worst cut-quality entry, 23 of 72 splices naked)
  with the new `piccuts.py` measurably reduces the exposed-splice count, verified by frame strips at
  −2/−1/0/+1/+2 — **not** by a frame-difference score.
* `picture.json` exists and the two Muhammad references pass every bound derived from them.
* An A/B clip of one join, old versus new, is sent to Dan. **He decides whether it reads as continuity.**
  Doctrine does not.

---

## Traps

* **Do not re-render any delivered master in this session.** Two audio re-render handoffs own those files
  (`handoff-20260909-audio-match-muhammad.md`, `handoff-20260909-invest-health-audio-rerender.md`), and
  `handoff-20260909-website-video-rev6.md` owns the website video. Work in a scratch copy —
  `AGENTS.md`: *never run a pipeline script inside another session's live build directory.*
* Snap every raw seek to the frame grid; an unsnapped seek duplicates the first frame (shortad, 09-03).
* A cross-dissolve is **not** the answer to a jump cut — *"his frame choice is"*
  (`shortad-from-longform/SKILL.md:844`). The 5-frame dissolve in the base is the fallback for a splice
  a revision exposed, not the default.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-vqc-C-phase4-cut-technique.md and execute it. Read
Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md first for context.

This is the phase that fixes why our cuts read as jump cuts and Muhammad's don't: he cuts the picture
1-15 frames off the audio splice on a pose-matched frame. piccuts.py already does this for one ad —
promote it to _shared/cut/, generalise it to work without a reference cut, and wire it into all five
video skills. Then: the ≥25% push coverage rule, the 0 px landing fix, dead air paired with picture cuts,
the grade, and a picture reference measured off Muhammad's two finished edits.

Confirm _shared/qc_corpus/run.py exists and is green first. Work in scratch copies — do not touch any
delivered master. Respect the two-concurrent-build cap. Send Dan an A/B of one join, old vs new, and let
him judge it. Commit, push, verify. No dashboard row.
```

**Model:** Fable 5.1, high. Opus 5 at high effort is an acceptable substitute.
