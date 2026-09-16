# Handoff: Video-quality engine PHASE 4 — the locked kit for ONE format, proven blind

**Date:** 2026-09-16
**Project:** Abs By AI (video production pipeline — `.claude/skills/shortad-from-longform`, `_shared/deliver`)
**Business goal this serves:** marketing performance — ad versions at volume without a $50/ad editor, at a
quality Dan will publish — with technical excellence as the means

**This is Phase 4 of `Handoffs/handoff-20260911-video-quality-engine.md`.** Phases 1–3 are done and pushed
(`eff3896`, `5e10200`, `0d62064`, `13369d9`); read the three "✅ EXECUTED" sections there first — Phase 3's
records a finding this phase must design around (below). **Do not start this while the corpus is not green.**

**Model:** see the recommendation table at the end. **~2 sessions.** **Generation spend $0** — the kit reuses
existing footage, inserts and graphics; no AI clips are generated to prove it. No dashboard row (Dan's rule
2026-09-08).

---

## Objective

Build the design kit for **one format — the 9:16 vertical ad** — so that a build starts from Muhammad's
pacing, panel system and push schedule instead of inventing them, then put the kit's output in front of Dan
**blind**, beside the cut he already approved, and record his verdict in the corpus in his own words. Only
his pick or a tie unlocks the next format.

## Why this is the phase, and why it has to be blind

"The Muhammad Standard" (2026-09-11; memory `video-editing-strategy-report`): **every approval of our
video work came where the design was fixed before the AI started** — the Ad 1 / Ad 2 verticals and the five
ab-wheel Shorts (all cut from Muhammad's masters), and the website video once its recipe locked after six
rounds. **Every rejection came where the AI had to invent the design.** Measured gap, picture changes per
minute: Muhammad Ad 1 **21.7**, Ad 2 **18.7**; ours (8/14 from-raw) **9.5 / 8.9**. His inserts sit on
textured olive grid panels; ours floated on black, and word captions collided with lower thirds. You do not
get this from a prompt. You get it from a template with the pacing and the panel system already in it.

Dan, 2026-09-14 (memory `video-editing-cost-quality-feedback`): *"Claude isn't producing good enough videos.
The quality just isn't something I could publish, and it's also too expensive… I'm not really getting much
usable other than the square and vertical versions."* **That is the bar this phase is measured against, and
it is why the test is blind and why it is one format.** Reformats of a locked cut are the one category that
works; the kit's bet is that a locked *design* makes a from-raw build work too. If Dan cannot pick the kit's
output over his editor's re-layout, the answer is "no", recorded, and the engine stops spending his limit on
from-raw builds. Codex and Grok are being trialled in parallel (`Handoffs/codex-video-trial/`, decision
Oct 9–11); this phase does not compete with those trials — its kit is what any of the three would build on.

## Current state (verified 2026-09-16)

* **The gate is complete for this format.** `gate.py --format ad9x16` runs 36 rows, `watch:pass` is a hard
  gate with a judged log, `cut:naked_splices` is proven on the corpus (`ad1-vertical-attempt1` 14.2/min
  fails; the approved verticals 0.45–7.0 pass; bound 12/min). `run.py` is 62/62 green.
* **⚠ Phase 3's finding, which this phase must design around:** at the picture level, one of attempt 1's
  jump cuts is **not distinguishable** from one of Muhammad's pose-matched same-scene cuts — his own
  masters carry 7.6–9.5 same-scene cuts per minute. What made his cuts invisible is that **his picture cut
  sits 1–15 frames off the audio splice on a pose-matched frame** (`shortad-from-longform/reference/a2/
  piccuts.py` recovers exactly that from his edits; corpus `muhammad-ad2-16x9`: 22 of 33 cuts moved by
  −15..+10 at confidence ≥ 0.6). **The kit must cut the way he cuts, or the gate will pass a cut Dan
  rejects.** `cut:pose_matched_offset` (VQC-C, still pending) is the row that would measure it.
* **`_shared/reference/picture.json` does not exist.** The engine doc says to fire VQC-C first if so.
  Recommendation, encoded below as step 0: build **only** C's item 6 (the picture reference) here — it is
  half a session and it is the only C item the kit consumes. C's items 1–5 (promote `piccuts.py` to
  `_shared/cut/`, landing error, dead air, grade) can run after, or in parallel by a second session on a
  scratch copy.
* **The matched pairs exist on disk** (all checked 2026-09-16):

  | his | ours (from raw, rejected or unshipped) |
  |---|---|
  | `Muhammad Ad Videos/this picture got me abs - ad 1/… muhammad | 16x9 | ad 1.mp4` | `/Volumes/Extreme/_edit_work/ad1-8-14/ad1_rev4_16x9.mp4` |
  | `Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/… muhammad | 16x9 | ad 2.mp4` | `/Volumes/Extreme/_edit_work/ads234-8-14/c1592/ad2_16x9.mp4` |
  | `YouTube Long Form Video Content/The $17 Ab Wheel Beats Every Crunch - READY FOR UPLOAD/Zeeshan edit/… Zeeshan edit rev 3 - READY FOR UPLOAD.mp4` (Muhammad's v2 HD sits beside it) | `/Volumes/Extreme/_edit_work/abwheel/r2/FINAL_ab-wheel-beats-every-crunch.mp4` |

  and the **approved 9:16 verticals** the kit's output is judged against:
  `Muhammad Ad Videos/this picture got me abs - ad 1/… claude | 9x16 | ad 1.mp4` (his cut, our layout,
  Dan: *"approved"*) and the Ad 2 / Ad 3 equivalents.
* **The pipeline the kit sits on** is `/shortad-from-longform`'s: `beats.py` (beat sheet), `plan_build.py`
  (plan.json + evidence contract v2), `render.py` (one segment per beat → concat → overlays), `captions.py`,
  `build_audio.py` / `finish_audio.py` (the shared audio chain), `a2/piccuts.py`, `a2/cover.py`,
  `cutdown.py`. Its approved outputs are the only from-a-master builds Dan has passed. Build the kit as a
  **plan template + layout profile** on that pipeline — not a new stack. (The strategy report floated
  Remotion; nothing here justifies a second renderer before the first has a locked design.)
* **Raw footage** for a from-raw kit build of Ad 1: the 8/14 shoot (`/Volumes/Extreme/abs by ai 8:14
  shoot | … | dan rose/C1591.MP4`, `C1592.MP4`; S-Log3 4K, four mono tracks — memory
  `shoot-828-slog3-format`; the lav is picked per file by `_shared/audio/pick_lav.py`).

## Key decisions already made (do not re-open)

* **One format first: the 9:16 vertical ad.** It is where the approved output exists to match and where
  the repeat volume is (15 ad variants on `Handoffs/video-editing/00-MASTER.md`).
* **Bound our output to his ranges in BOTH directions.** The dereverb hit EDT 32 ms against his 40 —
  *past* the target — and Dan called it "underwater" (memory `audio-never-over-strip`). Overshooting a
  reference is a warning, not a win. `picture.json` carries a low and a high for every number.
* **Dan judges, blind. Not us.** The failure mode being fixed is our taste; a session grading its own kit
  is that failure mode again. The page hides labels and randomises order; his verdict goes into the corpus
  verbatim whichever way it goes.
* **The kit is not an exemption.** Every kit output goes through `gate.py --format ad9x16 --plan plan.json`
  and the judged watch pass before Dan sees it. A kit output that needs the bound moved is a kit that
  failed.
* **Never raise a bound; never add a `known_gap`; never delete a `must_trigger`.** The corpus stays green.
* **An editor's finished mix ships untouched** (AGENTS.md). Where the kit re-lays out his cut, his audio is
  stream-copied; where it builds from raw, the shared voice chain and gate apply.
* **Same person in a before/after; real pictures carry the real-picture label off his face and abs**
  (AGENTS.md). The kit's card templates carry the chip positions as measured placements, not fixed y.

## Detailed plan

### 0. `_shared/reference/picture.json` — the picture reference (~half a session)

Mirror `_shared/audio/reference/reference.json` (pinned by `sha256`, `name`, `source`, `version`, `window`,
then the numbers). Build it from Muhammad's two finished 16:9 edits (Ad 1, Ad 2) with the gate's own
instruments so the numbers are the gate's numbers: `style:change_rate`, `style:coverage`,
`style:static_run`, `framing:push_coverage` (spread and count of pushes), `cut:naked_splices` (his
same-scene cut rate — **7.6–9.5/min is his range, not a defect**), shot-length distribution from the
watch scan's merged events, talking-head luma (he is ~6 luma brighter, 67 vs our 55 — C item 5), graphic
density (lower thirds + cards per minute, from a hand count on his two edits written into the file with
timestamps), insert coverage, the ramp shape (cuts per 10 s across the runtime). **Every number gets
`lo`/`hi` from the two edits plus the dispersion, and a `measured_on` with file + date.** Then prove it:
both Muhammad edits pass every bound derived from them, and `ad1-vertical-attempt1` fails at least the
push and cut-rate bounds. Register nothing new in the corpus for this — it is a reference, not a gate.

### 1. The kit — a plan template + layout profile for the 9:16 ad (~one session)

In `shortad-from-longform/reference/kit9x16/` (skill-tracked, never only in `Media/`):

* **`template.json`** — the beat grammar as data: the opening hold length, the push schedule (alternate
  NEAR/FAR across joins at his cadence; never one fixed crop — `framing:push_coverage` ≥ ×1.10), the
  insert cadence and the max bare stretch (his `static_run`), where lower thirds sit and how long, the
  CTA pill timing, caption band, label-chip placement rule. Every value cites `picture.json`.
* **`panels/`** — his panel system reproduced as layers: the textured olive grid panel behind inserts, the
  card frame, the lower-third style, at 1080×1920. Measure his from the masters (colour, texture scale,
  corner radius, margins); do not eyeball. Reuse what `a2/cover.py`, `assets.py` and the approved verticals'
  build dirs already hold before drawing anything new.
* **`cut_rules.md` + code path** — the pose-matched cut: at every audio splice inside a talk beat, choose
  the picture cut frame by `piccuts.py`'s method (pose match within ±15 frames), and cover what will not
  match with a push. Write the rule down with the numbers; do not leave it as tribal knowledge.
* **`build_kit.py`** — takes a script-aligned EDL (the audio cut) + the template and emits the plan.json
  `render.py` already consumes, with `joins`, `punch`, `graphics`, `ai_inserts`/`real_photos`, `covered`,
  `cards`, `caption_states`, `talking_head_windows` and `watch_log` filled — so the gate and the watch pass
  measure the kit's intent against its pixels. `--from-master` (re-layout of an approved 16:9, his audio
  stream-copied) and `--from-raw` (the 8/14 footage through the shared chain) are the two entry points.
* **Prove the kit on the approved cut first:** `--from-master` on Muhammad's Ad 1 must reproduce the
  approved `ad 1 | claude | 9x16` within the gate (all 36 rows PASS, judged watch pass, `cut:naked_splices`
  within his range) before `--from-raw` is attempted. If the re-layout cannot pass, the kit is wrong, not
  the gate.

### 2. The blind A/B (~half a session; Dan's time ~20 minutes)

* Build **the kit's from-raw Ad 1 vertical** (C1591/C1592, the finalized Ad 1 script) — gated and judged
  like any delivery. **Do not send it to Dan on its own.**
* A local review page (`python3 -m http.server`, as the Codex trial did — artifacts cannot serve video):
  two players side by side per pair, **labels hidden, order randomised per pair, the mapping written to a
  sealed `key.json` the page never reads**. Pairs: **(A)** the kit's from-raw Ad 1 vertical vs the approved
  `ad 1 | claude | 9x16`; **(B, C, D)** the three existing 16:9 matched pairs above (his edit vs our old
  from-raw build) — these calibrate the test: if Dan cannot tell his from our old builds, the test is not
  measuring what we think. One question per pair: *which would you publish, or is it a tie, and why in one
  line.* Dan's words verbatim.
* Record the result as corpus entries (`kit9x16-ad1-blind-<date>`, verdict from his pick, `dan` verbatim,
  `sha256` of the exact file he watched), plus the key. **Whichever way it goes.**

### 3. Only after Dan picks ours or calls it a tie

Extend in the strategy report's order — verticals → Shorts → long-form → hero ads last — one format per
phase, each proven blind before the next. If he picks his: write the delta he named into `template.json`
as the next revision and stop; do not spend a second session polishing without a new blind test.

### 4. Close out

`run.py` green, `gate.py --audit` no holes, commit, push, confirm the Railway deploy, a "✅ PHASE 4
EXECUTED" section in the engine doc with the blind result in Dan's words, this handoff removed from
`Handoffs/README.md` and the HANDOFFS list in `AI_COORDINATION.md`. No dashboard row.

## Things to avoid / lessons learned

* **Do not grade the kit yourself.** Not even "it looks close". The page, the key, Dan's words.
* **Do not send Dan a cut with an open watch-pass defect** to "get a quick reaction". The gate exists so
  he never watches a file with a black frame or a frozen card again.
* **Do not build a second renderer.** Remotion is a later question, if ever; the kit is data + panels on
  the pipeline that already produced approved output.
* **Do not put the kit's assets only in `Media/`** — it is gitignored (that is how `mono.py` spent weeks
  named MANDATORY while one `rm -rf` from gone).
* **Two concurrent builds max across sessions** (AGENTS.md); the corpus run is one; never run in another
  session's build dir — work in a scratch copy on the SSD.
* **The colour trap:** editor masters carry no colour tags; decode with `accurate_rnd` / BT.709 or the
  kit's grade will match the wrong decode (corpus `ad3-vertical-r9-color`, memory
  `untagged-video-bt601-trap`).
* **A subagent that has completed cannot be resumed** — launch a fresh one for the watch-pass judge and
  the Step 7b audit.
* **Snap every raw seek to the frame grid;** an unsnapped seek duplicates the first frame (shortad, 09-03).
* **Do not cross-dissolve a jump cut.** *"His frame choice is"* the fix (shortad SKILL.md); the pose-matched
  cut is the kit's rule, the 5-frame dissolve its fallback.

## Relevant files & locations

* Engine doc (Phases 1–3 executed, Phase 4 spec): `Handoffs/handoff-20260911-video-quality-engine.md`
* VQC-C (items 1–5 remain open; item 6 is step 0 here): `Handoffs/handoff-20260909-vqc-C-phase4-cut-technique.md`
* The gate + watch pass: `.claude/skills/_shared/deliver/{gate.py, formats.py, watch.py, README.md}`
* The pipeline: `.claude/skills/shortad-from-longform/{SKILL.md, reference/{beats.py, plan_build.py,
  render.py, captions.py, a2/piccuts.py, a2/cover.py, assets.py}}` and its approved build dirs on
  `/Volumes/Extreme/_edit_work/` (`ad1-vert*`, `ad2-vert-v2`, `ad3-vert`, `ad1-sq`)
* Audio reference to mirror: `.claude/skills/_shared/audio/reference/reference.json`
* Corpus: `.claude/skills/_shared/qc_corpus/{run.py, corpus.json, README.md}`
* Strategy report: https://claude.ai/code/artifact/0fac6195-accb-415b-99fa-70e3825d4906 (memory
  `video-editing-strategy-report`); Codex trial: `Handoffs/codex-video-trial/`
* Memories: `video-editing-cost-quality-feedback`, `framing-standard-hair-anchored`,
  `audio-never-over-strip`, `editor-audio-untouched`, `untagged-video-bt601-trap`,
  `before-after-same-person`, `muhammad-trial-edit-analysis`

## Model & effort recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Fable 5.1, high effort**, ~2 sessions: step 0 + step 1 in one, step 2 in the second (the blind page waits on Dan). This is design-and-measurement work on the pipeline Fable built and the gate Fable calibrated; included in Max (memory `fable-included-in-max`). |
| **If Claude usage is high / approaching a limit** | **Codex flagship (GPT-6 Astra), high effort** for step 0 and step 1's `build_kit.py` / panel measurement (a multi-file port against a written spec with a measurable acceptance test: reproduce the approved vertical within the gate), then **one Claude session (Fable 5.1 or Opus, high)** for the pose-matched cut rule, the from-raw build and the blind page. Given Dan's 09-14 cost feedback, this branch is the default unless usage is genuinely idle. |

Task-type override: the blind test and anything Dan reads is always-Claude for voice; the kit's code is not.
Do not drop below high effort for step 0 — a wrong `picture.json` misleads every phase after it.

## Starter prompt for the next task

```
Read Handoffs/handoff-20260916-vqc-phase4-locked-kit.md and execute it. Phases 1-3 of
Handoffs/handoff-20260911-video-quality-engine.md are done and pushed (eff3896, 5e10200, 0d62064,
13369d9) - read their "✅ EXECUTED" sections first, especially Phase 3's finding that a naked splice
and one of Muhammad's pose-matched cuts are not distinguishable by picture alone: the kit must cut the
way he cuts (piccuts.py's pose-matched frame, 1-15 frames off the audio splice).

Confirm `python3 .claude/skills/_shared/qc_corpus/run.py` is green before you start (~50 min under
load) and keep it green throughout.

In order: (0) build _shared/reference/picture.json from Muhammad's Ad 1 and Ad 2 16:9 masters with
the gate's own instruments, lo/hi per number, measured_on per number, and prove both his edits pass
and ad1-vertical-attempt1 fails; (1) the 9:16 kit as a plan template + layout profile on
/shortad-from-longform's pipeline (template.json, panels/, the pose-matched cut rule, build_kit.py
with --from-master and --from-raw), proven first by reproducing the approved "ad 1 | claude | 9x16"
within the gate; (2) the kit's from-raw Ad 1 vertical, gated and watch-judged, on a blind local review
page beside the approved vertical plus the three existing 16:9 matched pairs, labels hidden, order
randomised, sealed key - Dan picks, his words go into the corpus whichever way it goes; (3) nothing
further until he picks ours or a tie.

Never grade the kit yourself, never send Dan a file with an open watch-pass defect, never raise a
bound or add a known_gap, never build a second renderer, keep the kit's assets in the skill not in
Media/. Two concurrent builds max; work in a scratch copy on the SSD. $0 generation spend. Commit,
push, confirm the Railway deploy, re-read AI_COORDINATION.md from disk before finishing and edit only
your own entry. No dashboard row.
```
