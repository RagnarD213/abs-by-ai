# Results: render scheduler (render queue), 2026-10-20

Executed `handoff-20261020-render-scheduler-10-to-30-jobs.md` (Claude Opus 5.5, high). Tooling, not a video task.
Code: `.claude/skills/_shared/renderq/` (README there). Commits fa336be, c9f7300, 6045df7, 8a9ee4e, 354faf2.

## What Dan gets

- Start 10, 20 or 30 editing jobs at once. Every heavy step waits in one first-come line shared by Claude and Codex.
- See the line in plain words: `python3 .claude/skills/_shared/renderq/renderq.py status` (each slot, who holds it,
  every waiter in order, an estimated start, any build running outside the queue).
- Nothing in the 600-odd pipeline scripts had to change: the ffmpeg they all call is now a wrapper that queues heavy
  calls and lets quick ones through.

## How it works (short)

- Slots are `flock`ed files in `/tmp/absbyai-renderq/` (not `~`: Codex's workspace-write sandbox cannot write
  there, tested). The kernel frees a slot the instant its holder dies, `kill -9` included.
- Ticket per waiter, shared counter, only the head of the line takes a slot. Order: `--priority`, then
  continuations (a video holding a slot or that let one go in the last 2 min), then first come.
- Heavy pool: 2 slots always, up to 4 when at least 30% of the CPU sat idle for 4 s and nothing started in the
  last 15 s. Light pool (Whisper, checks): 2, up to 3. Work in a slot runs at nice 10.
- Builds outside the queue that use 30%+ CPU count against the heavy pool, so legacy scripts and anything not yet
  wired in still respect the cap.

## Wired in

| entry point | how | pool |
|---|---|---|
| `Media/video_edit/bin/ffmpeg` (and `/Volumes/Extreme/_edit_work/bin/ffmpeg`, a symlink to it) | wrapper; real binary `ffmpeg.real`; execs ffmpeg holding the lock | heavy or light by command line; exempt calls never wait |
| `ad-edit/reference/whisper_chunked.py` (all chunked Whisper) | `hold_until_exit` | light |
| `_shared/cut/speech.py` transcribe | `slot()` around extract and runner | light |
| `_shared/rolls/roll_sidecar.py` | its waits join the light line | light |
| `_shared/hyperframes/hfbuild.render` (Chrome capture plus encode) | `slot()` | heavy |
| `_shared/deliver/gate.py`, `deliver/watch.py`, `framecheck/gate.py` | `slot()` at `__main__` | light |
| `_shared/framecheck/clipcheck.py` (CoTracker on CPU) | `slot()` at `__main__` | heavy |
| `buildcap.wait()` (124 recipe files, 36 Extreme scripts) | now gets in line in the queue | heavy (light for roll_sidecar) |

Exempt (never wait): ffprobe, `-frames:v` up to 30, still-image outputs, audio-only, stream copy, `-t` 5 s or less,
`h264_videotoolbox` (setup-encode exception), commands with no input, review servers.

## Step 0: everything that could slow, deadlock or bypass it, and the fix

1. **Honour system, most tools never asked.** Fix: wrapper on the single ffmpeg path every script uses (no ffmpeg on
   PATH; 21 longform scripts reach the same binary through PATH).
2. **Work that is not ffmpeg** (Whisper inference, HyperFrames' Chrome, CoTracker, Python compositing). Fix: Whisper,
   HyperFrames and clipcheck take slots; Python feeding a piped encoder runs inside the encoder's slot; Python phases
   before the first encode are single-core and the census counts busy ones.
3. **Pipe deadlock** (decoder and encoder each needing a slot in a full pool). Fix: the two ends of a pipe share one
   slot. Live bug found on DS-33: both ends queued at the same moment and took two slots; fixed under the mutex,
   selftest added.
4. **Nested deadlock** (a render calls a gated check). Fix: `GATE_HELD`, verified against the live lock, plus an
   ancestry check for children whose environment was stripped.
5. **Parallel encodes inside one script** riding one slot. Fix: only pipe partners ride; parallel encodes queue.
6. **Mid-video re-queue behind new videos.** Fix: continuation class (2-minute grace) plus a 0.6 s hold of a just-freed
   slot for the same build. Measured: steps of a running real build waited 0 to 23 s between steps.
7. **Claude's 10-minute Bash timeout kills a waiting command.** Fix: rule to run builds in the background; a killed
   waiter's ticket is cleared at the next look (tested).
8. **Scripts parse ffmpeg's stderr** (voice_chain loudnorm). Fix: the wrapper never writes to stdout or stderr
   (tested); exit codes pass through (tested).
9. **Shared temp file in Whisper:** `whisper_chunked.py` wrote every chunk to `/tmp/_chunk.wav`, so two runs at once
   corrupted each other's transcripts. Fixed (per-process name).
10. **Old waiters double-wait:** Codex `pipeline_slot.py`, `dispatcher.py` `foreign_builds`, a few `wait_slot.sh`
    loops still count `ps`. With the queue keeping 2 to 4 builds busy they can wait a long time. Fix: rule says drop
    them in new rounds; `buildcap.wait()` already joins the queue. Overnight dispatcher (paused) stays compatible:
    the sessions it launches hit the wrapper.
11. **Codex sandbox:** home folder not writable and `ps` not allowed in workspace-write. Fix: queue in `/tmp`; the
    ancestry check falls back to the parent pid; the census keeps its last reading instead of erasing it.
12. **Load average misleads on macOS:** 130 at 15% idle today (it counts threads waiting on disk). Fix: the queue
    reads real CPU idle from the kernel (`host_statistics`), never load average.
13. **Single-core Python renders under a flat cap of 2** leave most of the Mac idle (`stage2_comp.py`,
    `render_key.py` at about 1 core each today). Fix: idle-CPU extra slots.
14. **iCloud sync cost:** writing intermediates under the project folder (`tmp/ro27-r2-work`) kept `fileproviderd` at
    50 to 160% CPU. Fix: rule to keep intermediates on `_edit_work` or scratch.
15. **Queue code breaks a build:** if `renderq` cannot load or errors, every entry point and the wrapper run the job
    ungated and log it (`events.log`). Never a failed render because of the queue.
16. **A stuck process outside the queue blocks a heavy slot:** it shows in `status` as "outside the queue" with pid.
17. **Bypasses not covered:** another ffmpeg binary (none found in use), `npx hyperframes render` called directly by
    `scripts/video/hyperframes_graphics.py` and `cycle/build.py` (its encode still hits the wrapper; Chrome does not).
    Low share of time; left as is.
18. **Drive I/O:** encodes run near 1x realtime, so reads are tens of MB/s against hundreds available on the
    externals; no per-volume slot added.
19. **Memory:** light pool capped at 3 (Whisper peaks 3.6 GB each).
20. **Slot held while waiting on Dan:** slots belong to commands, which end before a session stops for review.

## Measurements (all on a busy Mac: other sessions kept it at 0 to 20% idle, load 110 to 250)

A quiet machine never occurred during the session, so absolute times are inflated; comparisons are back to back.

**30 dummy jobs** (`bench.py`: 10 x264 1080p encodes, 10 numpy-fed pipe renders, 10 single-core jobs), each mode
started all 30 at once:

| mode | run | all done | average job finished | median | each x264 job ran |
|---|---|---|---|---|---|
| queue | 1 | 136 s | 64 s | 54 s | 14 s |
| two at a time by hand | 1 | 134 s | 73 s | 74 s | 10 s |
| two at a time by hand | 2 | 171 s | 85 s | 88 s | 13 s |
| queue | 2 | 165 s | 69 s | 51 s | 17 s |
| all 30 at once, no queue | 1 | 78 s | 50 s | 64 s | **76 s** |

- Queue vs two at a time: total time 150 s vs 153 s (same, within 2%); the average job finishes **16% sooner**
  (66 s vs 79 s) because light jobs run beside heavy ones.
- All at once looks fastest only because, on a Mac already full of other sessions' work, 30 extra processes take CPU
  away from those sessions' real builds. Each encode ran 5 to 8 times slower. With every session in the queue there
  is no one to take CPU from; the 2026-08-27 measurement of that case: no throughput gain, 9.3x slower steps.
- 30 jobs waiting cost about 0.1 core in total (waiters far back in line now check every 3 s).

**Two real builds** (`realbuild.py`: 20 s of the 10/15 4K 10-bit roll, picture pass, Soft Blue lower third piped
render, master mux, review copy, Whisper; shared pipeline code, scratch output):

| | wall | time actually working, per build |
|---|---|---|
| one build alone (7% idle) | 93 s | 93 s |
| two at once, no queue | 186 s | 182 s each |
| two through the queue | 237 s | 64 s and 76 s (waited 101 and 142 s in line behind other sessions' real jobs) |

Inside the queue each step ran 2.4 to 2.8 times faster than when the two fought each other unqueued (master mux 12 to
23 s vs 48 to 52 s, Whisper 18 to 24 s vs 42 to 46 s). The queued pair took longer overall only because it waited its
turn behind earlier jobs from DS-33, DS-40, SL-06 and SL-15, which is the first-come rule working.

**Slot numbers chosen:** heavy 2 base, because x264-bound work saturates the CPU with two (08-27 data, confirmed:
idle 0% with two encodes plus background); up to 4 when 30% or more is idle, because today's dominant renders are
single-core Python feeding a starved encoder (1 to 2 cores each). Light 2 base, 3 max (Whisper memory).

**Not done, worth doing once:** re-run `python3 .claude/skills/_shared/renderq/bench.py --jobs 30` overnight on a
quiet Mac to tune `IDLE_MIN` and the burst cap with clean numbers. Skipped the planned 3- and 4-way ungated real
builds: by then the queue was live and they would have held up four sessions' real work for about 15 minutes.

## Verification

- `renderq.py selftest`: 21 of 21 pass (first come, priority next, one at a time in a one-slot pool, `kill -9`
  holder: next job starts within a second, killed waiter leaves no ticket, nesting with and without `GATE_HELD`,
  `buildcap.wait()` inside a slot, frame grab and audio never wait, heavy encode waits, exit codes, silent wrapper,
  pipe on one slot, pipe partners queued together take one slot, light beside heavy, extra slot only when idle,
  `GATE_OFF`, continuation ordering, command-line classification).
- `buildcap.py --selftest`: 20 of 20 pass.
- Codex (`codex exec -s workspace-write`, gpt-6.1-sol, the overnight queue's sandbox) joined the live line, waited
  11 min behind real jobs, was granted heavy slot 1 with `GATE_HELD` set inside its command, and released it
  (`events.log`, `history.jsonl`). The first two attempts exposed the home-folder and `ps` limits, both fixed.
- Live: within minutes of the wrapper going in, DS-33, DS-40, SL-06, SL-15 and RO-20 jobs were queuing and running in
  order (`/tmp/absbyai-renderq/events.log`).

## How Dan uses it

Start the jobs. That is all. If something seems slow, ask any session for "the render queue status"; it runs the
status command and reads it back in plain words. To push one job to the front: start it with `--priority`.
