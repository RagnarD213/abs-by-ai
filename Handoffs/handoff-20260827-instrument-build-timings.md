# Handoff: Instrument a real video build to measure per-stage wall-clock times

**Date:** 2026-08-27
**Project:** Abs By AI
**Business goal this serves:** Technical excellence → indirectly profitability (Dan's hands-on time + the
"do we buy a new Mac / do we optimize the pipeline" decision, currently unanswerable)

---

## Objective

Dan asked whether upgrading his Mac mini would speed up photo editing, video editing and AI-video work.
The analysis produced three candidate software optimizations — but **we have no idea how long any build
stage actually takes**, so we cannot say whether a 2x speedup saves him 4 minutes or 45. This task adds
lightweight, reversible timing instrumentation to the video pipeline, runs one real build through it, and
delivers a table of where the wall-clock time actually goes.

**This task does NOT optimize anything.** It only measures. The optimization decision comes after, informed
by real numbers. Do not swap the Whisper implementation, do not touch encoders, do not parallelize
anything in this session.

---

## Current State

### The hardware (measured this session, not assumed)

| | |
|---|---|
| Machine | Mac mini, **M2 Pro**, Model `Mac14,12` |
| CPU | 10 cores — **6 performance + 4 efficiency** |
| GPU | 16 cores — **completely unused by the pipeline** |
| Memory | 32 GB |
| Boot disk | 926 GB, **145 GB free** |
| External | `/Volumes/Extreme` — 3.6 TB, 2.3 TB free, reads **910 MB/s** (NOT a bottleneck) |

### What runs locally vs. in the cloud (established this session)

**Local — the Mac does all of this:**
- **All video rendering.** Every encode is `libx264` — a pure-CPU encoder. 47 call sites across the
  skills. Presets `fast`/`medium`/`slow`, CRF 16–20.
- **All transcription.** `openai-whisper 20240930` on `torch 2.8.0`. Models used: `small` (9 call
  sites), `small.en` (3), `base` (1). **`word_timestamps=True` in 7 places** — the millisecond word
  timing is load-bearing for EDL recovery, lip-sync xcorr and wrong-take detection.
- **All graphics.** Every lower third, card, caption, CTA pill drawn in `pillow 11.3.0` (PIL), single-threaded.
- **All measurement.** Frame-diff analysis, face tracking, channel analysis, the QC gate.

**Cloud — hardware is irrelevant to these:** Veo 3.1 (Gemini API), FLUX/Seedream (Replicate),
Gemini/nano-banana, Claude, MiniMax.

### Key structural fact that shapes this task

⚠ **There is NO single build entry point.** The pipeline is ~100 discrete Python scripts in
`.claude/skills/longform-edit/reference/` (and siblings in `/ad-edit`, `/shorts`,
`/shortad-from-longform`), run in sequence by the agent, one at a time. So you cannot just time "the
build" — instrumentation has to capture the individual tool invocations.

### How scripts locate ffmpeg (verified — this is what makes the shim approach work)

Every path eventually resolves to **one real binary**:
`Media/video_edit/bin/ffmpeg` (45 MB static build, ffmpeg 6.0)

Call sites reach it three ways:
- `/Volumes/Extreme/_edit_work/bin/ffmpeg` — a **symlink** to the above (14+ scripts)
- the repo absolute path directly (4 scripts)
- `/Volumes/Extreme/_edit_work/invest-health-cutdowns/bin/ffmpeg` (1 script)

**Because all three resolve to the same inode, a shim installed at the real binary catches 100% of calls.**

---

## Key Decisions Already Made

- **Measure before optimizing, and measure before buying hardware.** Dan's call this session. A 2x
  speedup on an 8-minute stage is worth nothing; on a 90-minute stage it's worth a lot. We don't know which.
- **Do not buy the Mac yet.** M4 Pro mini ≈ 2x current render speed, M4 Max Studio ≈ 2.4x (estimate:
  6→10/12 performance cores plus ~25–30% IPC). Real but not transformative, and the software may be
  leaving more on the table than the hardware.
- **The Whisper swap is the one clearly-good optimization** — `mlx-whisper` runs the *same* OpenAI
  models via Apple's framework. Gated on a word-timestamp equivalence test (see Avoid section).
- **The GPU/VideoToolbox encoder idea was narrowed and mostly rejected.** Originally suggested for all
  intermediate renders; corrected after reading the pipeline. Reasons: 3+ chained lossy generations
  compound quality loss; the QC gate measures the finished file (grade curves, frame-diff peaks,
  banned-screen template matching) and is calibrated on x264 output; changing encoders **invalidates the
  segment cache** that makes revisions cheap; VideoToolbox has no CRF equivalent so it's a logic rewrite
  not a flag swap. **Only safe for genuinely disposable outputs** — 540p review copies, contact sheets,
  A/B files.
- **Parallelizing the PIL graphics passes is a "maybe"** — real gain (currently 1 of 10 cores), but
  memory pressure at 32 GB and this pipeline has a documented history of ordering bugs (the SRT
  alphabetical-vs-reading-order fault).
- **Instrument by shimming the tools, not by editing ~100 scripts.** Reversible in one command, and it
  cannot drift out of sync with the scripts.

---

## Detailed Plan

### Step 1 — Build the ffmpeg timing shim

Install a wrapper at the real binary location so every call site is captured.

```
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
mv ffmpeg ffmpeg.real
mv ffprobe ffprobe.real
```

Then write `ffmpeg` (and `ffprobe`) as a shell shim. Requirements — **all of these are mandatory,
each one corresponds to a way this can silently break the pipeline:**

1. **`exec` the real binary** so the process is replaced — no extra process in the tree.
2. **Pass stderr through completely untouched.** ⚠ **CRITICAL: the two-pass loudnorm audio chain
   parses ffmpeg's stderr** to read measured I/TP/LRA/threshold values and feed them into pass two.
   Several scripts also parse ffprobe output. If the shim buffers, filters, reorders or prefixes
   stderr, **the audio chain breaks and the failure will look like an audio bug, not an instrumentation
   bug.** Write timing to a *separate log file*, never to stdout/stderr.
3. **Preserve the exit code exactly.** Scripts use `subprocess.run(..., check=True)`; a mangled exit
   code turns a success into a crash or, worse, a failure into a silent pass.
4. **Handle arguments with spaces correctly** (`"$@"`, never `$*`) — paths here contain
   spaces ("Abs By AI").
5. **Append one line per invocation** to `/Volumes/Extreme/_edit_work/_timing/ffmpeg_calls.log`:
   epoch start, duration in seconds, exit code, output-file basename, and the encoder + preset + CRF if
   present. Keep it machine-parseable (TSV or JSON-lines).

**Verify the shim before running any real build:**
- `ffmpeg -version` returns normally, exit code 0.
- A trivial 1-second encode succeeds and writes a log line.
- ⚠ **Run one real two-pass loudnorm** (`finish_audio.py` against any existing delivered file) and
  confirm the measured values are still parsed correctly. This is the check that catches the stderr trap.
- Confirm timing goes only to the log, never into the pipeline's captured output.

### Step 2 — Time the Python stages

Each pipeline script is one agent-run command. Wrap them so total per-script wall time is captured:

- Simplest reliable approach: run each stage as
  `/usr/bin/time -p python3 <script>.py 2>> /Volumes/Extreme/_edit_work/_timing/stage_times.log`
  with a marker line naming the stage. Note `/usr/bin/time` writes to **stderr** — if a stage's stderr
  is parsed by anything, redirect to a file per stage instead of appending blindly.
- Record for each stage: script name, wall seconds, and (from the ffmpeg log) how much of that was
  inside ffmpeg. **The interesting number is the gap** — script wall time minus ffmpeg time ≈ PIL +
  numpy + Whisper time, i.e. the single-threaded Python work.

### Step 3 — Time Whisper specifically

Whisper is the strongest optimization candidate, so measure it in isolation:
- Time one `whisper_run.py` / `tx_runner.py` transcription of a full roll (these are 30–40 minute
  source files) with model `small`, `word_timestamps=True`.
- Record: audio duration, wall seconds, and the **realtime factor** (wall ÷ audio duration). That factor
  is the number that makes the `mlx-whisper` comparison meaningful later.
- Note peak memory if convenient (`/usr/bin/time -l`).

### Step 4 — Run one real build end to end

**OPEN — pick whichever is true when you start:**
- **Preferred: instrument the next real build that needs doing anyway.** The queued work is
  `Handoffs/handoff-20260827-ads-2-3-4-trainer-nutritionist-supplements.md`. Instrumenting a build Dan
  wants regardless costs nothing extra and produces genuinely representative numbers.
- **Fallback if no build is queued: re-run the Ad 1 vertical build** from
  `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/` (the corrected 99-segment `edl_final.json` is
  intact). ⚠ **Write outputs to a scratch directory — do NOT overwrite the delivered, Dan-approved
  `ad1_vertical_9x16.mp4`.**

⚠ **Whichever you pick, note whether the segment cache is warm or cold and say so in the report.** A
cached build reports `[cached]` for untouched beats and will dramatically under-report extraction time.
Both numbers are useful, but they must be labelled — a warm-cache timing presented as a full build would
send the whole hardware decision the wrong way.

### Step 5 — Deliver the timing report

A short table Dan can read in 30 seconds, in chat plus a file at
`/Volumes/Extreme/_edit_work/_timing/REPORT.md`:

| stage | wall time | % of build | CPU-bound? | which optimization would touch it |
|---|---|---|---|---|

Then answer these four questions explicitly:
1. **Total wall-clock time for one full build**, and warm vs. cold cache.
2. **The top 3 stages by time**, and what each is bound by (x264 / Whisper / PIL / I-O).
3. **How much total time is single-threaded** (i.e. what parallelizing could reach) vs. already
   multi-core (i.e. what only a faster chip could reach).
4. **The verdict:** for each of the three optimizations, and for the Mac upgrade, the actual minutes
   saved per build. If the honest answer is "none of this is worth doing," **say that** — that is a
   perfectly good outcome and it saves Dan money.

### Step 6 — Remove the shim

```
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
mv ffmpeg.real ffmpeg && mv ffprobe.real ffprobe
```

⚠ **Do not leave the shim installed.** It is a single point of failure sitting under every video skill,
and a future session will not know it's there. Confirm `ffmpeg -version` works after removal. If you
believe the shim is worth keeping permanently, that's a proposal for Dan, not a default.

### Step 7 — Close out

- Commit the shim script + report to the repo so the method is repeatable
  (`.claude/skills/_shared/timing/` is a reasonable home). **Media files stay out of git** — the global
  `*.mp4` ignore rule is deliberate.
- Update `AI_COORDINATION.md` with the findings, and reset the active-task section if nothing is left.
- **Check off the dashboard task** `business::Execute handoff: instrument a real video build to measure
  per-stage times` (added 2026-08-27). Use the `/dashboard-tasks` skill for the mechanics.

---

## Things to Avoid / Lessons Learned

- ⚠ **The stderr trap is the big one.** Two-pass loudnorm reads its measurements out of ffmpeg's
  stderr. Any shim that touches stderr breaks the audio chain, and it will present as an audio defect.
- ⚠ **Don't optimize in this session.** The whole point is to get numbers first. Dan explicitly chose
  measurement over action here — this is the one case where "bias toward action" does not mean "start
  changing things," because the change is what we're trying to decide about.
- ⚠ **Don't overwrite delivered masters.** `ad1_vertical_9x16.mp4` (rev 2) is Dan-approved and awaiting
  his final nod on one photo swap. Scratch directories only.
- ⚠ **Never delete `_edit_work/clips_graded/`** — that's the segment cache, and it's what makes Dan's
  revisions cheap.
- **This pipeline's QC gate has been wrong more often than the media has.** Documented at least four
  times (splice median normalisation, chip-brightness assumption, music-bed floor heuristic, the
  `-c:v ffv1` difference reading 0). If instrumentation appears to show something impossible, suspect
  the measurement first.
- **For the later Whisper decision (not this task):** the go/no-go is a word-timestamp equivalence
  test — run `openai-whisper` and `mlx-whisper` on identical audio and diff every word's start/end. Agree
  within a few ms → safe to swap. Also expect **hallucination behaviour to differ**; the specific traps
  recorded in the skills ("six back abs", "a gold picture", "WuWu stuff", the three fake spray-tan
  captions) may not transfer, and new ones will appear.
- **`ffmpeg` is not on `PATH`** and neither is `whisper` — everything uses absolute paths. Don't assume
  a shell can find them.
- **`/Volumes/Extreme` gets unmounted.** Check it's mounted before starting; every build path is on it.
- The external drive reads at 910 MB/s — **already ruled out as a bottleneck.** Don't re-investigate I/O.

---

## Relevant Files & Locations

| what | where |
|---|---|
| Real ffmpeg/ffprobe (shim target) | `Media/video_edit/bin/ffmpeg`, `ffprobe` |
| Symlink most scripts call | `/Volumes/Extreme/_edit_work/bin/ffmpeg` |
| Pipeline scripts (~100) | `.claude/skills/longform-edit/reference/` |
| Transcription entry points | `whisper_run.py`, `tx_runner.py`, `words.py` |
| Audio chain (the stderr trap) | `finish_audio.py`, `audio_final.py` |
| QC gate | `qc_style.py` (13 checks), `qc_generic.py` |
| Most recent real build | `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/` |
| Segment cache — NEVER DELETE | `/Volumes/Extreme/_edit_work/clips_graded/` |
| Timing output (create) | `/Volumes/Extreme/_edit_work/_timing/` |
| Next queued real build | `Handoffs/handoff-20260827-ads-2-3-4-trainer-nutritionist-supplements.md` |

No secrets, API keys or env vars are needed for this task — it is entirely local and calls no metered
provider. **Expected AI spend: $0.00.** No production code, no deploy, no native-retest trigger.

---

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** Well-specified mechanical work — write a shim, run stages, tabulate. The hard thinking (what to measure, what the traps are) is already done in this document. |
| **If Claude usage is high / approaching a limit** | **Codex, medium effort.** Shell/Python scripting against an explicit spec is squarely in Codex's wheelhouse and this touches no brand voice and no Anthropic API code. |

**No always-Claude override applies** — no copy, no architecture decision, no Anthropic API integration.

Do **not** use Opus for this. The judgment calls are already made; paying Opus rates to run
`/usr/bin/time` is waste. **Escalate to Opus only if** the shim breaks the audio chain in a way that
isn't obvious from the stderr rule above, or if the timings come back incoherent and the pipeline needs
real diagnosis.

---

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20260827-instrument-build-timings.md` in the Abs By AI project and execute it.
>
> Goal: find out where the wall-clock time actually goes in one real video build, so we can decide
> whether the local pipeline optimizations (or a new Mac) are worth doing. **Measure only — do not
> optimize anything this session.**
>
> First action: confirm `/Volumes/Extreme` is mounted, then build the ffmpeg timing shim at
> `Media/video_edit/bin/ffmpeg` per Step 1. Pay close attention to the stderr requirement — the
> two-pass loudnorm chain parses ffmpeg's stderr, so the shim must pass it through completely untouched
> and log timing to a separate file. Verify the shim against a real `finish_audio.py` run before you
> instrument a whole build.
>
> Deliver the Step 5 timing table plus an explicit verdict: for each of the three candidate
> optimizations and for the Mac upgrade, how many minutes per build it would actually save. "None of
> this is worth doing" is an acceptable and useful answer. Remove the shim when you're done (Step 6).
