# Handoff: Video-quality engine PHASE 3 — the watch pass becomes mandatory in all six video skills

**Date:** 2026-09-12
**Project:** Abs By AI (video production pipeline — `.claude/skills/_shared/deliver`)
**Business goal this serves:** marketing performance (every ad and video Dan ships is gated on the moving
picture, not just its format), with technical excellence as the means

**This is Phase 3 of `Handoffs/handoff-20260911-video-quality-engine.md`.** Phases 1 and 2 are done and
pushed (`eff3896`, `5e10200`, `0d62064`); read their "✅ EXECUTED" sections in that doc first — they
record what landed, what did not, and every measurement behind the bounds. Phase 4 (the locked kit)
must NOT start until this phase is green.

**Fable 5.1, high effort. ~2 sessions. $0.00–$2 generation spend** (contact sheets judged by a
subagent cost nothing; only a model-API route costs cents). No dashboard row (Dan's rule 2026-09-08).

---

## Objective

Make "somebody watched the moving picture" a hard, verifiable gate on every delivered video, in one
shared module, and prove the automated half against the regression corpus. Today the gate row
`watch:pass` exists but is enforced for two formats only; four formats carry a dated `pending` note;
`/shorts` mentions a watch pass zero times; and three separate `watch.py` forks each depend on their
own build's beat sheet, so none can run on a file from another skill. When this phase is done, every
skill's delivery path refuses a file whose `logs/watch_pass.json` does not name that file's sha256,
the automated scan reproduces the corpus's known picture defects, and the seventeen bannered QC forks
are gone.

## Why this is third and why it matters

`watch.py`'s own docstring: *"Ad 1 attempt 1 passed 11/11 on a metric gate and Dan rejected it: every
check measured format, none ever looked at the moving picture."* That file is corpus entry
`ad1-vertical-attempt1`; Dan's words on it are *"truly awful… definitely won't work."* The longform
skill paid twice more: *"attempt 2 passed 15/15 and Dan found 13 problems, eight of which a human sees
in one viewing"*, and a build shipped *all 7 lower thirds, all 3 CTA pills and all 11 flashes
invisible* with every metric green. `/shorts` SKILL.md:977: *"THE CONTACT SHEET IS NOT A GATE. Every
framing fault in this batch survived one."*

## Current State (verified 2026-09-12)

**What the shared gate already has**

* `_shared/deliver/gate.py` — version **1.2.0**, 35 rows × 7 formats, `--audit` clean, corpus
  19/19 green (`python3 .claude/skills/_shared/qc_corpus/run.py`, ~26 min under load).
* `checks/process.py::watch_pass` — the row. Reads the plan's `watch_log` (a `logs/watch_pass.json`),
  ties it to the file by **sha256** via `_log_for` (a filename-only tie is accepted and said so; a log
  naming neither is refused), and passes only when `inspected` is true and `reviewed >= boundaries`.
  `required: true` for `ad9x16` and `ad1x1`; `ad16x9`, `longform`, `short`, `website` carry
  `required: false` + a dated `pending` note and print as PENDING (never as a pass); `exercise-demo`
  declares it not applicable.
* Phase 2's framing tracker (`checks/framing.py`) already flags `website-rev3`'s hair — the first of
  the two corpus defects this phase must reproduce is covered by the gate. Its proof sheet
  `<file>.framing_proof.jpg` is written on every full run.
* `cut:uncovered_joins` (Phase 1) measures same-scene picture jumps per minute off the delivered
  pixels; `ad1-vertical-attempt1` has **not** been measured on it yet (23 of its 72 splices shipped
  as naked jump cuts in 59 s).

**The three watch scripts to fold in — each works, none is portable**

| script | boundaries from | scan | traps |
|---|---|---|---|
| `shortad-from-longform/reference/a2/watch.py` | its build's `beats.py` (timeline, overlays, flashes, pushes) | **writes every frame as a 96×171 PNG** (6,000 files), then frozen `d<0.05` ≥ 8 frames, black `lum<3`, unexplained jumps | ffmpeg path hardcoded to the repo build; PNG-per-frame is slow and litters the build dir |
| `website-video/reference/recipe/watch.py` | `beats.py` + `layout.py` PUNCH + `pip_marks()` + `tight_cuts.json` keeps | same, 160×90 PNGs | ffmpeg hardcoded to `/Volumes/Extreme/_edit_work/bin/ffmpeg` |
| `longform-edit/reference/watch_longform.py` | the plan's declared windows | **streamed** full-frame scan (the right pattern), events **merged** (a dissolve is one event, not 80), **graphic presence** by differencing the delivered picture against the pre-graphics source inside every declared window, boundary strips | the only one with the graphic-presence check |

**Where the watch pass is mandated today:** `/shortad-from-longform` (qc check 15 refuses without
`logs/watch_pass.json`), `/longform-edit` Step 8.5, `/website-video` checklist. `/ad-edit` describes it
in lessons only; `/shorts` not at all.

**The bannered forks** (deprecation banners since Phase 1; nothing deleted). 30 files reference the
engine handoff's banner today: `ad-edit/reference/{modern60/qc_modern.py, rev5/qc5.py}`,
`longform-edit/reference/{content_flags, cutdown_final_gate, qc_generic, qc_investhealth,
qc_investhealth_v3, qc_style, qc_with_inserts, srt_validate, tailcheck, verify_cover}.py`,
`shortad-from-longform/reference/{gain_flatness, landing_check, qc, qc_ad2v2}.py`,
`shorts/reference/{clean-master,full-bleed,scored-source,zepbound}/qc.js`,
`shorts/reference/{clean-master,spray-tan,zepbound}/syncgate.py`,
`shorts/reference/recentre/delivered_gate.py`, `website-video/reference/recipe/{qc, qc_frame,
rev1/qc, rev2/qc, rev3/qc, rev3/qc_frame}.py`. ⚠ Builds COPY these into their own dirs on the SSD, so
deleting the skill copies does not break a running render — but every SKILL.md step that names one
has to be re-pointed at the shared gate in the same commit.

## Key Decisions Already Made (do not re-open)

* **One gate, versioned, on the delivered file.** Any new check or bound bumps `GATE_VERSION`
  (→ 1.3.0) and invalidates every older stamp. Bounds live in `formats.py` only, with the file and
  date they were measured on. A missing input is NOT MEASURED, which FAILS. A row a format has not
  answered for FAILS as UNCONFIGURED. (AGENTS.md, 2026-09-11.)
* **Consecutive frames at −2/−1/0/+1/+2 across every boundary are the instrument.** Two
  frame-difference detectors failed in a row on a real jump cut (a whole-frame gray diff scored it at
  2.0× its local median, a face-region diff ranked it 12th of 28). A 1 s contact sheet cannot see a
  jump cut, and `fps=1/N` sheets lag content by ~N/2 s (ad-edit lesson 94: three false alarms in one
  review). Grab suspect frames with exact `-ss` before calling anything a defect.
* **Frame sheets, never video-model input.** Gemini charges $0.15 per second of video (≈$36 for one
  4-minute ad); sheets are cents or free.
* **The independent subagent audit stays** (Dan, 2026-09-01: *"calling Fable to review should be a
  part of this skill going forward"*). It has overturned a session's own "this is fixed" twice,
  including catching eyeball reads that were mirrored at three of four timestamps.
* **The watch log ties to the file by sha256**, because a re-render keeps the path and the filename.
* **Never raise a bound to make a build pass; never add a `known_gap` to make `run.py` green.**
* **The corpus is the acceptance test.** No gate change ships unless it is green.

## Detailed Plan

### 1. `_shared/deliver/watch.py` — one module, plan-driven, streamed  (~half a session)

Port the union of the three scripts. Boundaries come from **the plan** (the same `PLAN_KEYS` the gate
already documents: `joins`, `punch`, `graphics[].beat`, `ai_inserts[].beat`, `real_photos[].beat`,
`covered`, `cards`), never from a `beats.py` import — that is what made each fork unportable. Find
ffmpeg through `common.FF`. Structure:

```
watch.py <delivered file> --plan plan.json [--out <dir>]      -> <dir>/watch_pass.json + strips + sheets
```

* **scan** — streamed gray at 30 fps 160×90 (never PNG-per-frame): frozen runs (`d < 0.05` for
  ≥ 8 frames), black frames (`lum < 3.0`), and hard discontinuities NOT within ±2 frames of a declared
  boundary. **Merge consecutive over-threshold frames into one event** (watch_longform's rule: a
  dissolve, a wiping graphic and a fast passage each trip every frame they last; eighty "jumps" that
  are one 0.4 s animation is noise). Threshold = the file's own noise (p99 of the diff), not a
  constant.
* **graphic presence** — when the plan gives a `graphics[].mov` or a pre-graphics source
  (`source_picture`, a new plan key), difference the delivered picture inside each declared window at
  full resolution. The only check that sees an overlay that never composited.
* **boundary strips** — for every boundary, consecutive full-resolution frames at −2/−1/0/+1/+2 as
  one strip image; optionally a 2 s clip. These are what the human (or the subagent) looks at.
* **contact sheets for the first pass** — ~25 frames per image over the whole runtime, plus one
  sheet per boundary strip, named so a judge can cite them.
* **writes `watch_pass.json`**: `sha256`, `video`, `boundaries` (count + list), `reviewed`,
  `inspected` (false until a person or the audit subagent sets it), `scan` findings, `sheets` list,
  `judged` (filled in by step 2). The gate's `watch_pass` row already reads this shape.

### 2. The automated first pass — the checklist a judge scores every sheet against  (~half a session)

Derived from Dan's own rejections, each item citing its corpus entry or SKILL lesson:

| item | source |
|---|---|
| hair at or over the top edge | `website-rev3` (*"basically not usable"*) — the framing tracker already fails it; the sheet judge confirms by eye |
| head or arm out of frame; space on the other side | `v2-short3-offcentre` |
| junk or placeholder card; text off-screen | ad-edit / longform lessons; the rev-0 spray-tan junk |
| naked splice (same scene both sides, subject jumps) | `ad1-vertical-attempt1`, 23 of 72 |
| graphic over his face; caption on a card or the CTA pill | website rev 2; Ad 1/2 square audit |
| black frame; frozen segment; duplicate shot | shortad [R1] (six one-frame blacks, twelve frozen cards) |
| a wide level where none should exist | `website-rev1` |
| **visual junk with no audio signature**: look-aways, glasses adjustments, drinking, recomposing while already talking | longform-edit SKILL.md:383 — items 1–5 and 7 of its twelve mandatory passes have **no automated check anywhere** |

**OPEN (decide in step 2, do not block on it):** how the sheets get judged. Two routes, both write
their findings into `watch_pass.json` under `judged` with the sheet name and the item:
(a) **a fresh subagent in the session** reads every sheet against the checklist — $0, and it doubles
as Step 7b's independent audit when it is given the delivered file and the `personmask` CLI too;
(b) **a model API call from `watch.py`** (`claude-sonnet-5` on the sheet images) — cents per video,
runnable outside a session. Recommendation: build (a) now as the mandated path and leave (b) as a
flag only if the local Anthropic key is valid (memory `load-time-optimizations` says the local key was
invalid; test on prod only). Either way the gate does not care who judged — it checks that every
sheet in `sheets` has an entry in `judged` and that `inspected` is true.

### 3. Prove the automated half on the corpus  (the acceptance test for this phase)

* **`ad1-vertical-attempt1` must fail `cut:naked_splices`.** Today that key is PENDING (owner
  "VQC-C phase 4"). Implement it in the gate as the delivered-pixel measurement `cut:uncovered_joins`
  already makes (same-scene spikes per minute, declared beats subtracted), under the `ad9x16` bound,
  and register it in `run.py`'s `IMPLEMENTED`. Measure the file FIRST and write the number beside
  the bound: 23 naked splices in 59 s is ~23/min against a 2.5/min bound, so it should fail by an
  order of magnitude — if it does not, the instrument is wrong, not the file. ⚠ Do not weaken the
  `ad9x16` bound to make the approved verticals pass it; they were measured at 0.2–0.8/min on
  2026-09-11 (`formats.py` calibration table).
* **`website-rev3`'s hair** — already reproduced by `framing:hair_top` (Phase 2). Record in the
  corpus entry's `measured` that the watch sheets show it too.
* **Add a synthetic fixture for the scan half**, because no corpus file carries a frozen run or a
  black frame on purpose: take `qc_corpus/excerpts/website-rev4.mp4` (regenerable with
  `run.py --extract`), inject 10 duplicated frames, one black frame and one uncovered same-scene
  jump with ffmpeg, and add `_shared/deliver/tests/test_watch_scan.py` that asserts all three are
  found and that the clean excerpt reports none. Wire it into `qc_corpus/selftest`-style step 0 or
  `run.py` so a broken scanner cannot make the corpus green.

### 4. Turn the row on everywhere  (~1 hour)

In `formats.py`, set `"watch:pass": dict(required=True)` for `ad16x9`, `longform`, `short` and
`website`, delete the four `pending` notes, bump `GATE_VERSION` to 1.3.0 with a dated line, run
`gate.py --audit`. Add `source_picture` to `PLAN_KEYS` in `gate.py`. Update `_shared/deliver/README.md`
("`watch:pass` is a hard gate for `ad9x16` and `ad1x1` only" → everywhere; costs table).

### 5. Wire the six skills  (~1 hour)

* `/shorts` — has no watch pass at all: add a Step "THE WATCH PASS" before delivery pointing at
  `_shared/deliver/watch.py`, and replace its contact-sheet language with the boundary-strip rule.
* `/ad-edit`, `/longform-edit`, `/website-video` — replace each skill's own watch script reference
  with the shared module (`watch_longform.py`, `recipe/watch.py`); keep their lessons.
* `/shortad-from-longform` — qc check 15 → the shared row; Step 7b stays.
* **Step 7b's independent subagent audit** goes into `/ad-edit`, `/longform-edit`, `/website-video`
  and `/shorts` as written in `shortad-from-longform/SKILL.md:631–652` (fresh subagent on the exact
  delivered file, population statistics, full-res verification of every flag, an explicit opinion on
  the trade-off just made; a completed subagent cannot be resumed).
* Every "Run both until Phase 3 lands" note (ad-edit:407, longform-edit:815, website-video:175,
  shortad:557–560) becomes "the shared gate only".

### 6. Delete the bannered forks  (~1 hour, LAST)

Only after steps 1–5 are green. Before deleting: `ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'`
and read `AI_COORDINATION.md` for builds in flight (2026-09-12 evening: `ad3-vert`, `ad5-vert` may
still be running against their own SSD copies — those copies are theirs and are unaffected).
`git rm` the 30 files listed under Current State, grep every SKILL.md for their names and re-point
each mention, and record the deletion in the README's "The forks this replaces" section (keep the
list as history: it is the provenance of half the bounds).

### 7. Record the cost

`_shared/COSTS.md` gets a "watch pass" row: wall time per 4-minute master (scan + sheets + strips)
and any API spend if route (b) exists. Phase 1 measured ~75 s for the picture rows and Phase 2
~3–4 min for framing on a quiet Mac; the corpus run is ~26 min under load.

### 8. Close out

`python3 .claude/skills/_shared/qc_corpus/run.py` green, `gate.py --audit` no holes, commit, push,
confirm the Railway deploy (it redeploys on every push, even a skills-only one), a "✅ PHASE 3
EXECUTED" section in the engine doc, this handoff removed from `Handoffs/README.md` and the
HANDOFFS list in `AI_COORDINATION.md`, a board entry with what changed. No dashboard row.

## Things to Avoid / Lessons Learned

* **Do not write a frame per PNG.** Two of the three forks dump 6,000 files into the build dir per
  pass. Stream through ffmpeg (`common.gray` / a `Popen` reader) as `watch_longform.py` and
  `checks/picture.py` do.
* **Do not trust a single frame difference to find a jump cut** — see the decisions above. The
  strips are the evidence; a number is a shortlist.
* **Do not let a `--no-watch` or `--skip` flag exist.** Phase 0 closed seven bypasses; the row's
  three states are pass / fail / NOT MEASURED, and NOT MEASURED fails.
* **Do not sample.** The email-capture screen was once exposed for exactly one frame; a 2 fps scan
  stepped over it. The scan half is every frame.
* **Two concurrent video builds max across all sessions** (AGENTS.md). The corpus run counts as one;
  measured 2026-09-12: the audio selftest alone took 8 minutes at load 45.
* **`selftest.sh` is zsh.** `bash selftest.sh` dies with a fake "unbound variable".
* **`Media/` is gitignored** — a script that lives only there enforces nothing; so does a plan that
  only ever lived in a build dir (that is why `captions:graphic_clearance` cannot be proven on rev 2).
* **A subagent that has completed cannot be resumed** — launch a fresh one for a re-audit and restate
  the context.
* **Concurrent sessions edit the same shared files.** `caption_sync_check.py` was clobbered once
  mid-build on 09-11; re-read `AI_COORDINATION.md` from disk before finishing and edit only your entry.
* Two findings from Phase 2 that are Dan's to act on, not this phase's: **Muhammad's Ad 2 16:9
  master shows the app's before/after screen at 3:11 and the email-capture screen at 3:12 and 3:23**
  (a live Google Ads creative; `compliance:banned_screen` now catches it); and **rev 6 passes the
  per-hold headroom ceiling with zero margin** (its opening hold reads exactly 70 px).

## Relevant Files & Locations

* Engine handoff (Phases 1–2 executed sections, Phases 3–5): `Handoffs/handoff-20260911-video-quality-engine.md`
* The gate: `.claude/skills/_shared/deliver/{gate.py, formats.py, common.py, README.md}`,
  `checks/{process.py (watch_pass, _log_for), picture.py, framing.py, compliance.py, captions.py, audio.py, container.py}`
* Corpus: `.claude/skills/_shared/qc_corpus/{run.py, corpus.json, README.md, plans/}`, excerpts via `run.py --extract`
* The three watch forks: `shortad-from-longform/reference/a2/watch.py`,
  `website-video/reference/recipe/watch.py`, `longform-edit/reference/watch_longform.py`
* Step 7b (the subagent audit, verbatim): `shortad-from-longform/SKILL.md:631–652`
* Visual-junk passes: `longform-edit/SKILL.md:366–392`
* `/shorts` contact-sheet warning: `shorts/SKILL.md:973–980`
* Costs: `.claude/skills/_shared/COSTS.md`
* Standing rules: `AGENTS.md` ("One delivery gate, versioned"; "No gate change ships without the regression corpus";
  "Video builds: never run more than two at once")
* Baseline of every delivered master: `Docs/VQC_baseline_20260909.md`
* Memories: `framing-standard-hair-anchored`, `audio-never-over-strip`, `shared-fix-may-not-reach-the-pipeline`,
  `gate-the-harm-not-just-the-fix`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Fable 5.1, high effort** — what Phases 1 and 2 ran on; included in Max at no extra dollar cost (memory `fable-included-in-max`; double-check availability at the time). Opus with extended thinking is the equivalent if Fable is unavailable. |
| **If Claude usage is high / approaching a limit** | **Codex flagship, high effort** for steps 1, 3–4 and 6–7 (a multi-file port with a measured acceptance test); then **one Claude session (Sonnet 5, standard thinking)** for steps 2 and 5 — the checklist wording and the SKILL.md wiring are judgment and voice work Codex does worse. |

Task-type override: none of this touches brand copy or the Anthropic API integration, so it is not
always-Claude — but the corpus proof in step 3 is where being wrong is expensive to unwind, so do not
drop below high effort there whichever tool runs it.

## Starter Prompt for the Next Task

```
Read Handoffs/handoff-20260912-vqc-phase3-watch-pass.md and execute it. Phases 1 and 2 are done
and pushed (eff3896, 5e10200, 0d62064) — read the "✅ PHASE 1 EXECUTED" and "✅ PHASE 2 EXECUTED"
sections of Handoffs/handoff-20260911-video-quality-engine.md first.

Confirm `python3 .claude/skills/_shared/qc_corpus/run.py` is green before you start (it takes
~26 minutes under load) and keep it green throughout — it is the acceptance test.

Build in this order: (1) `_shared/deliver/watch.py` — one plan-driven, streamed module folding in
shortad's a2/watch.py, website-video's recipe/watch.py and longform-edit's watch_longform.py,
keeping the −2/−1/0/+1/+2 consecutive-frame strips at every boundary and watch_longform's merged
events and graphic-presence check; (2) the automated first pass — contact sheets judged against
the checklist in the handoff, findings written into logs/watch_pass.json; (3) prove it: register
cut:naked_splices and measure ad1-vertical-attempt1 on it FIRST, add the synthetic frozen/black/
jump fixture test; (4) set watch:pass required for every format, bump GATE_VERSION to 1.3.0;
(5) wire all six skills, including Step 7b's independent subagent audit into /ad-edit,
/longform-edit, /website-video and /shorts; (6) only then delete the bannered forks and re-point
every SKILL.md mention; (7) record the cost in _shared/COSTS.md.

Never sample frames, never write a frame per PNG, never add a skip flag, never raise a bound to
make a file pass, never add a known_gap to make run.py green. Respect the two-build cap. Commit,
push, confirm the Railway deploy, re-read AI_COORDINATION.md from disk before finishing and edit
only your own entry. No dashboard row.
```
