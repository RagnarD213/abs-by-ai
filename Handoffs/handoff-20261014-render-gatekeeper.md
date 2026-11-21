# Handoff: render gatekeeper (enforce the two-builds-at-a-time cap)

Written 2026-10-14 by Claude (Opus 5.5). Type: tooling, not a video task. Recommended model: **Opus 5.5, high effort.**

## Goal

Turn the written rule in `.claude/skills/_shared/VIDEO-RULES.md:1061` ("Cap concurrent video builds at two across all
sessions") into code that enforces it. Today nothing stops a third build, and sessions ignore the rule: on 2026-10-14
the load average hit 78 on the 10-core M2 Pro with about 10 Claude sessions plus Codex building at once.

Evidence for the cap of two: `.claude/skills/_shared/timing/REPORT_20260827_build_timings.md` (four concurrent builds:
load 242, `finish_audio.py` 126 s vs 13.6 s quiet, no throughput gain; two overlap usefully because one build's
single-threaded Python runs under the other's x264).

## Step 0: brainstorm before building (required)

Before writing any code, list every additional way this gatekeeper could slow editing, break a pipeline, deadlock,
or be bypassed, beyond the five below. Check real call sites (grep for `ffmpeg`, `render.py`, `qc_style`, `whisper`,
`clipcheck.py`, `watch.py`, `kit_run.py`, `finish_audio.py`, HyperFrames renders, Codex scripts, the overnight
`dispatcher.py`). For each new problem, write the fix. Put the list in the results doc, then build. Ideas to test, not
conclusions: tiny jobs (ffprobe, single-frame grabs) that should skip the line; Whisper/GPU work that may not compete
for the same cores; external-drive I/O as a second bottleneck; the review-page `http.server` processes (must never be
gated); Codex sandbox write access to the lock directory; jobs run from git worktrees; a slot held by a job that is
waiting on Dan.

## Known problems and the fix for each

1. **An urgent job waits behind long renders.** Add a priority flag (`--priority` / env `GATE_PRIORITY=1`) that puts the
   job at the front of the line. It does not preempt a running job.
2. **Waiting sessions burn tokens or hit the 10-minute Bash timeout.** The wait happens inside the script (blocking lock,
   no polling loop in the session). Skill docs tell sessions to run gated jobs with `run_in_background` so they are
   notified on finish. The gate prints one line when it starts waiting and one when it gets a slot, nothing in between.
3. **A crashed job holds a slot forever.** Use kernel file locks (`fcntl.flock` on one file per slot, e.g.
   `~/.absbyai-gate/slot0.lock`, `slot1.lock`). The OS releases the lock when the process dies, even on kill -9. Never
   a PID file or "busy" marker that needs cleanup.
4. **Nested jobs deadlock** (a render holding a slot calls a gated frame check). The holder exports `GATE_HELD=1` to
   child processes; a gated call that sees it runs straight through without taking a second slot.
5. **Jobs that bypass the gate are not limited.** Put the gate inside the shared entry points (the shared render, QC,
   watch, audio-finish and transcription scripts, and an `ffmpeg` wrapper they call), not in skill instructions. Codex
   uses the same lock directory. Keep a `GATE_OFF=1` escape hatch for debugging only.

## Build

- One small module, e.g. `.claude/skills/_shared/gate/gate.py`, usable two ways: a Python context manager
  (`with gate.slot(): ...`) and a CLI wrapper (`gate.py run -- ffmpeg ...`).
- Slot count from config, default 2. Add `gate.py status` showing who holds each slot (command, session, start time)
  and who is waiting.
- Run all encodes inside a slot at low priority (`nice`), matching the setup-encode rule.
- Update `VIDEO-RULES.md:1061` to say the cap is enforced by the gate and how to call it. Push shared files with
  `scripts/git/safe-push.sh` the moment they are edited.

## Verify

- Start four dummy CPU-heavy jobs through the gate: confirm two run, two wait, and a waiting priority job goes next.
- kill -9 a slot holder: the next job starts within a second.
- Nested call under `GATE_HELD=1` does not deadlock.
- Time one real build alone, then four builds gated vs ungated; record wall-clock totals in the results doc.

## When to run

Only when nothing is rendering: wiring the gate into shared scripts mid-build can break running jobs. Check
`ps -Ao command | grep -E 'ffmpeg|render\.py|qc_style|whisper|clipcheck'` first. Good pairing: the same quiet window
as `handoff-20261001-move-project-out-of-icloud.md`.

## Deliver

Results doc `Handoffs/results-YYYYMMDD-render-gatekeeper.md` (brainstorm list, fixes, timings). Remove this handoff's
row from `Handoffs/README.md` and its line in the HANDOFFS section of `AI_COORDINATION.md`. Report in chat in plain
language.
