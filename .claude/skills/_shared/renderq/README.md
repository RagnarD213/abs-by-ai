# Render queue (`renderq`)

Every heavy video step on the Mac mini waits its turn here, so Dan can start 10, 20 or 30 editing jobs at once and
the machine never overloads. Rule: `VIDEO-RULES.md`, "Video builds: the render queue". Built 2026-10-20; numbers in
`Handoffs/results-20261020-render-scheduler.md`.

## For sessions (Claude and Codex)

- **Just start the job.** Heavy steps queue themselves. Do not count builds with `ps` and do not write your own wait loop.
- **Run builds in the background** (`run_in_background`, `nohup`, a chain script). A queued step can wait longer than
  the 10-minute Bash timeout, and a killed waiter loses its place in line.
- **See the line:** `python3 .claude/skills/_shared/renderq/renderq.py status`
- **A whole script as one step** (recommended for per-round `render_r*.sh` / `build*.sh` / chain scripts):
  `python3 .claude/skills/_shared/renderq/renderq.py run --group RO-27 -- bash render_r2.sh`
  Everything inside it runs straight through on that one slot. Add `--light` for checks, `--priority` only when Dan
  is waiting on that exact output.
- **In Python:** `with renderq.slot("RO-27 picture pass"):` (heavy) or `renderq.slot(label, pool="light")`.
  A one-shot script can call `renderq.hold_until_exit(label, pool)` once at the top.
- **Name the video:** `export GATE_GROUP=RO-27` (or run from `/Volumes/*/_edit_work/<job>/`, which names it
  automatically). Steps of a video that is already running go ahead of videos not yet started.
- `GATE_OFF=1` skips the queue. Debugging only, never for a real build.

## What waits and what does not

| | waits in | examples |
|---|---|---|
| heavy | 2 slots always, up to 4 while the Mac has spare CPU | x264/ProRes/qtrle encodes, full decodes piped to Python, HyperFrames renders, `clipcheck.py` |
| light | 2 always, up to 3 | Whisper (`whisper_chunked.py`, `cut/speech.py`), `deliver/gate.py`, `watch.py`, `framecheck/gate.py`, `-f null` analysis passes |
| never waits | | ffprobe, frame grabs (`-frames:v` up to 30), stills, audio-only ffmpeg, stream copies, anything `-t` 5 s or less, the `h264_videotoolbox` setup encode, review servers |

The wrapper at `Media/video_edit/bin/ffmpeg` (real binary: `ffmpeg.real` beside it) sorts every ffmpeg call by its
command line, so all ~600 pipeline scripts are covered without edits. It prints nothing (voice_chain parses
ffmpeg's stderr) and passes the exit code through untouched. `GATE_VERBOSE=1` makes it say when it waits.

## How it works

- Slots are files in `/tmp/absbyai-renderq/slots/` (not `~`: Codex's workspace-write sandbox can write /tmp only) held with `flock`. The kernel frees a slot the moment its holder
  exits, `kill -9` included. Nothing to clean up.
- One ticket file per waiter in `queue/`, numbered from a shared counter, each `flock`ed by its waiter; a dead
  waiter's ticket is deleted at the next look. Only the head of the line may take a slot. Order: `--priority`,
  then continuations (a video holding a slot or that let one go in the last 2 minutes), then first come.
- A slot let go by a build that is still running is kept for it for 0.6 s, so its next step does not lose its turn.
- Extra slots (heavy 3-4, light 3) open only when at least 40% of the CPU sat idle over the last 4 s and nothing
  started in that pool in the last 15 s. CPU is read from the kernel (`host_statistics`), not load average, which
  on macOS counts threads waiting on disk and read 130 at 15% idle during the build of this tool.
- Builds outside the queue (old scripts, another ffmpeg) using 30%+ CPU count against the heavy pool (`buildcap.builds()`).
- Nesting never deadlocks: a holder exports `GATE_HELD`; anything below a holder (by environment or by process
  ancestry) runs straight through, and so do the two ends of a pipe once one end holds the slot.
- Work in a slot runs at nice 10.

## Files

`renderq.py` (library and CLI), `ffshim.py` (wrapper entry), `selftest.py` (`renderq.py selftest`, 20 checks),
`bench.py` (30 dummy jobs: queue vs two at a time vs all at once), `realbuild.py` (a small real build from the
shared pipeline pieces, for timing). Install or remove the wrapper: `renderq.py install-shim` / `uninstall-shim`.
