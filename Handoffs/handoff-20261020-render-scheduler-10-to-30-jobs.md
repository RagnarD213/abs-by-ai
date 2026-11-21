# Handoff: render scheduler, so 10, 20 or 30 jobs at once run as efficiently as 2

Written 2026-10-20 by Claude (Sonnet 5.5) after an audit with Dan. Type: tooling, not a video task (no CONTENT/AD category).
Recommended model: **Opus 5.5, high effort** (never max). Supersedes `handoff-20261014-render-gatekeeper.md` (same idea, narrower; its Step 0 and five known problems are folded in below).

## /goal

Build a feature that makes it as efficient for Dan to start 10, 20 or 30 editing jobs at the same time as it is to do 2 at a time. His normal way of working is to start many video edits at once. The machine must never be overloaded, and every heavy step must wait in a queue until the best time to start. Total time to finish N jobs with the queue must be no worse than running them two at a time by hand, and each job should finish sooner than it would if all N ran at once.

## Why (audit, 2026-10-20)

- `.claude/skills/_shared/buildcap.py` counts builds correctly (a render's Python, decoder and encoder = one build; cap 2, measured by Dan 2026-08-27). `python3 buildcap.py` right now shows 2 builds. That part works.
- **It is an honor system, not a gate.** Only two shared tools call `buildcap.wait()`: `_shared/cut/speech.py` (Whisper) and `_shared/rolls/roll_sidecar.py`. A grep of `longform-edit`, `shorts`, `ad-edit` and `shortad-from-longform` finds **zero** callers. Renders, x264 encodes, HyperFrames renders, frame checks and QC started from ad hoc scripts (e.g. `stage2_comp.py`, `kit_run.py`, per-round `render_r*.sh`) are not gated. The rule in `VIDEO-RULES.md` ("Video builds: never run more than two at once") only tells sessions to check first.
- **No line to stand in.** Waiting is first come, first served only among tools that choose to wait; ten sessions that start at once can each see a free slot in the same second and all start. Waiting uses `ps` polling (20 s) and a sleeping child process as a marker, with no shared state, so there is no real ordering, no priority and no visibility for Dan.
- **Measured overload now:** load average 40 to 60 on a 10-core M2 Pro with only 2 counted builds (Chrome, Codex, Claude app, Whisper and extra Python all compete). 2026-08-27 numbers: four concurrent builds, load 242, `finish_audio.py` 126 s vs 13.6 s quiet, no throughput gain (`_shared/timing/REPORT_20260827_build_timings.md`). On 2026-10-14 about 10 sessions drove load to 78.
- Result: Dan can only start 2 or 3 jobs at a time safely. The goal is to remove that limit.

## What to build

A real scheduler, not a smarter honor system. Dan and every session (Claude and Codex) must be able to start any number of jobs; heavy steps queue themselves.

1. **One central gate, enforced in code.** A small module (suggested `.claude/skills/_shared/gate/`, extend or replace `buildcap.py`; keep `buildcap.wait()` as a thin compatibility wrapper so existing callers keep working). Usable as a Python context manager (`with gate.slot(label, weight=...)`) and a CLI wrapper (`gate.py run -- <command>`). Kernel file locks (`fcntl.flock`, one file per slot under a shared dir all sessions and the Codex sandbox can write, e.g. `~/.absbyai-gate/`), so a crashed or `kill -9` job frees its slot instantly. Never a PID or busy file that needs cleanup.
2. **Real first-come queue with ordering and priority.** A ticket file per waiter (monotonic sequence), a blocking wait inside the script (no polling loop in the session, no token burn, no 10-minute Bash timeout trap), one line when waiting starts and one when the slot is granted. `--priority` / `GATE_PRIORITY=1` moves a job to the front without preempting a running one. Optional per-video grouping so one video's steps stay together and finish (a half-finished video is worth less than a finished one).
3. **Put the gate inside the shared entry points,** not in skill prose: the shared render, QC (`qc_style`, `deliver/gate.py`, `watch.py`, `clipcheck.py`), audio-finish, transcription, HyperFrames render, `kit_run.py`, the final x264 encode, and a wrapper for the project `ffmpeg` (`Media/video_edit/bin/ffmpeg`) that gates any encode longer than a few seconds. Update the per-skill render scripts and the `render_r*.sh` / `build*.sh` patterns to call it. Keep a `GATE_OFF=1` escape hatch for debugging only.
4. **Right-size the slots instead of a flat 2.** Weight jobs: a full x264 render or HyperFrames render is heavy (1 slot, wants most cores); Whisper, PIL graphics and single-threaded Python are light and can overlap a heavy encode (this is why 2 helps: about 19% of a build is single-threaded). Measure first, then pick the numbers; do not assume. Optionally adapt to the machine: if load average is high from non-video apps, start fewer; if the machine is idle, allow a light job beside a heavy one. Cap total in-flight work, never total queued jobs (30 queued must cost nothing while waiting).
5. **Exempt what must never wait:** ffprobe, single-frame grabs, short stills, review-page `http.server` / `review_server.py` processes, anything under a few seconds, and the existing setup-encode exception (`nice -n 20 ffmpeg -hwaccel videotoolbox`, VIDEO-RULES, Dan 2026-09-30).
6. **Nesting and deadlocks.** The slot holder exports `GATE_HELD=1`; a gated call inside it runs straight through (a render that calls a gated frame check must not need a second slot). Also handle: jobs run from git worktrees, Codex sandbox write access to the lock dir, a slot held by a job that is waiting on Dan (release before any review stop), and the overnight `dispatcher.py` (paused; keep it compatible).
7. **Run at low priority** (`nice`) inside a slot, matching the setup-encode rule, so Dan's interactive work (Chrome, review pages) stays responsive.
8. **Visibility for Dan:** `gate.py status` showing each slot (command, video/job id, session, start time, elapsed), every waiter in order, and an estimated start time from recent durations. Optionally show the queue on the Edit Queue page (`_shared/edit-queue/`, `jobs.json`; statuses are set by `queue.py`). Plain language, no jargon.
9. **Reliability:** drive I/O is a second bottleneck (Extreme and Seagate externals); consider an I/O slot or a per-volume limit. Keep chained steps from re-queuing behind brand new jobs mid-video (see grouping). A job that dies must not strand its waiters.

## Step 0 (required before code): brainstorm and measure

List every additional way this could slow editing, deadlock or be bypassed beyond the above; check real call sites (grep `ffmpeg`, `render.py`, `qc_style`, `whisper`, `clipcheck.py`, `watch.py`, `kit_run.py`, `finish_audio.py`, HyperFrames, Codex scripts). Put the list and a fix for each in the results doc. Then **measure**: one real build alone vs 2, 3, 4 concurrent on a quiet machine, to set the slot count and weights from data (existing report above is from 2026-08-27 and predates newer pipelines).

## Verify

- Start 30 dummy CPU-heavy jobs (mixed heavy and light) through the gate: at most the configured number run, the rest wait at ~0% CPU, order is first-come, a priority job goes next, total wall-clock is within a few percent of running the same jobs two at a time by hand, and load average stays at the chosen ceiling.
- `kill -9` a slot holder: the next job starts within a second. A waiting job that is killed leaves no stale ticket.
- Nested call under `GATE_HELD=1` does not deadlock. Exempt commands never wait.
- Two real short builds (use an existing small recipe in a scratch copy; never run inside another session's live build directory) gated vs ungated, timings recorded.
- Codex can take and release a slot from its sandbox.
- Existing `buildcap.py --selftest` still passes (or is migrated).

## When to run

Wiring the gate into shared scripts mid-build can break running jobs. Check `python3 .claude/skills/_shared/buildcap.py` and `ps -Ao command | grep -E 'ffmpeg|render\.py|qc_style|whisper|clipcheck'` first; wire in during a quiet window, or wire script by script without touching files another session is editing. Do not retrofit already approved masters.

## Deliver

- Update `VIDEO-RULES.md` section "Video builds: never run more than two at once" to say the cap is enforced by the gate, how to start jobs (just start them; they queue), and the status command. Update `AGENTS.md` if a standing rule changes (render-queue check authorization already exists, 2026-10-20).
- Push each shared file the moment it is edited with `scripts/git/safe-push.sh -m "..." -- <files>` (stale-file rule: `--adopt-stale`).
- Results doc `Handoffs/results-YYYYMMDD-render-scheduler.md` (brainstorm list, measurements, slot weights, timings, how Dan uses it). Remove this handoff's row (and the superseded 10-14 gatekeeper row) from `Handoffs/README.md`. Report in chat in plain language.

## Starter prompt (paste to start the task)

> Read `Handoffs/handoff-20261020-render-scheduler-10-to-30-jobs.md` in full, then `.claude/skills/_shared/buildcap.py`, the section "Video builds: never run more than two at once" in `.claude/skills/_shared/VIDEO-RULES.md`, and `.claude/skills/_shared/timing/REPORT_20260827_build_timings.md`. Goal: build a render scheduler so Dan can start 10, 20 or 30 editing jobs at once and the machine never overloads, with heavy steps waiting in a real first-come queue and starting at the best time, as efficient as running 2 at a time. Do Step 0 (brainstorm and measure) first, build the gate into the shared entry points, verify with 30 dummy jobs and two real builds, update the rules, push shared files with safe-push, and write the results doc. Use Opus 5.5, high effort.
