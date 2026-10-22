# Render queue (`renderq`)

Every heavy video step on the Mac mini waits its turn here, so Dan can start 10, 20 or 30 editing jobs at once and
the machine never overloads. Rule: `VIDEO-RULES.md`, "Video builds: the render queue". Built 2026-10-20; numbers in
`Handoffs/results-20261020-render-scheduler.md` (the queue) and `Handoffs/results-20261020-renderq-drives.md` (quick
lane, drives, work and scratch folders).

## For sessions (Claude and Codex)

- **Just start the job.** Heavy steps queue themselves. Do not count builds with `ps` and do not write your own wait loop.
- **New job, new folder:** `python3 .claude/skills/_shared/renderq/renderq.py workdir RO-27 --need 40` prints (and
  creates) the job's work folder: the one it already has on any drive, else `/Volumes/<drive>/_edit_work/RO-27` on the
  least busy work drive with room. `--source <footage>` steers away from the hard disk holding the footage; `--why`
  shows the scores. Never type a drive name for a new job.
- **Throwaway files:** `renderq.py scratch RO-27` prints a scratch folder on the internal SSD (`/tmp/absbyai-scratch/RO-27`)
  while it keeps 50 GB free, else `_scratch` in the job folder. Frame dumps, test renders, temporary intermediates.
  Not for review images or anything a later round needs: scratch untouched for 48 h is deleted.
- **Run builds in the background** (`run_in_background`, `nohup`, a chain script). A queued step can wait longer than
  the 10-minute Bash timeout, and a killed waiter loses its place in line.
- **See the line:** `python3 .claude/skills/_shared/renderq/renderq.py status`. **See the drives:** `renderq.py drives`.
- **A whole script as one step** (recommended for per-round `render_r*.sh` / `build*.sh` / chain scripts):
  `python3 .claude/skills/_shared/renderq/renderq.py run --group RO-27 -- bash render_r2.sh`
  Everything inside it runs straight through on that one slot. Add `--light` for checks, `--priority` only when Dan
  is waiting on that exact output. Run it from the job folder so the queue knows its drive.
- **In Python:** `with renderq.slot("RO-27 picture pass", drives=[src, out]):` (heavy) or
  `renderq.slot(label, pool="light")`. A one-shot script can call `renderq.hold_until_exit(label, pool)` once at the
  top. `renderq.workdir(job)`, `renderq.scratch_dir(job)`, `renderq.pool_for_media(clip)` ("quick" for a short clip).
- **Name the video:** `export GATE_GROUP=RO-27` (or run from `/Volumes/*/_edit_work/<job>/`, which names it
  automatically). Steps of a video that is already running go ahead of videos not yet started.
- `GATE_OFF=1` skips the queue. Debugging only, never for a real build.

## What waits and what does not

| | waits in | examples |
|---|---|---|
| heavy | 2 slots always, up to 4 while the Mac has spare CPU; each drive at most its cap | x264/ProRes/qtrle encodes, full decodes piped to Python, HyperFrames renders, `clipcheck.py` on long clips |
| quick | 2 slots, first come first served | the same heavy work on SHORT media: inputs of 20 s or less (or `-t` 20 s, 600 frames), `clipcheck.py` on clips of 15 s or less, HyperFrames graphics of 10 s or less. An AI clip's frame dump, trim or clip check |
| light | 2 always, up to 3 | Whisper (`whisper_chunked.py`, `cut/speech.py`), `deliver/gate.py`, `watch.py`, `framecheck/gate.py`, `-f null` analysis passes |
| never waits | | ffprobe, frame grabs (`-frames:v` up to 30), stills, audio-only ffmpeg, stream copies, anything `-t` 5 s or less, the `h264_videotoolbox` setup encode, review servers |

**Drive caps** (`drives.json`, measured 2026-10-20 with `drivebench.py`, two passes on a busy Mac): Extreme 2,
Expansion 3, internal 6, Seagate 2 until measured. A heavy waiter whose drive is at its cap steps aside; the next
waiter on another drive goes first. Re-measure a drive: `python3 drivebench.py Seagate --runs 2 --save` (about 3 min
per run, writes a few GB of test files to the drive and deletes them).

The wrapper at `Media/video_edit/bin/ffmpeg` (real binary: `ffmpeg.real` beside it) sorts every ffmpeg call by its
command line (reading the length of each input clip from its file header), so all ~600 pipeline scripts are covered
without edits. It prints nothing (voice_chain parses ffmpeg's stderr) and passes the exit code through untouched.
`GATE_VERBOSE=1` makes it say when it waits.

## How it works

- Slots are files in `/tmp/absbyai-renderq/slots/` (not `~`: Codex's workspace-write sandbox can write /tmp only) held
  with `flock`. The kernel frees a slot the moment its holder exits, `kill -9` included. Nothing to clean up. A new
  holder writes who it is (pid, pipe, drives) before the admission lock opens, so a pipe partner or a waiter on the
  same drive never misses it.
- One ticket file per waiter in `queue/`, numbered from a shared counter, each `flock`ed by its waiter; a dead
  waiter's ticket is deleted at the next look. Only the head of the line may take a slot, except that a heavy waiter
  whose drive is full does not count as ahead of anyone. Heavy order: `--priority`, then continuations (a video
  holding a slot or that let one go in the last 2 minutes), then first come. Quick: `--priority`, then first come.
- A slot let go by a build that is still running is kept for it for 0.6 s, so its next step does not lose its turn.
- Extra heavy slots (3-4) and light 3 open only when at least 30% of the CPU sat idle over the last 4 s and nothing
  started in that pool in the last 15 s. CPU is read from the kernel (`host_statistics`), not load average.
- Builds outside the queue using 30%+ CPU count against the heavy pool (`buildcap.builds()`).
- Nesting never deadlocks: a holder exports `GATE_HELD`; anything below a holder (by environment or by process
  ancestry) runs straight through, and so do the two ends of a pipe once one end holds the slot.
- Each step records its drives: an ffmpeg call's input and output files, else the folder a step runs in plus any
  `/Volumes/<drive>/` its command line names. Older code that recorded none is read from its command and folder.
- Work in a slot runs at nice 10.
- Rolling out a new version never disturbs jobs already waiting: they keep the code they started with, the files
  stay compatible both ways, and each new ffmpeg call loads the new code.

## Files

`renderq.py` (library and CLI), `ffshim.py` (wrapper entry), `selftest.py` (`renderq.py selftest`, 34 checks),
`drives.json` (per-drive caps and their measurements), `drivebench.py` (measures a drive), `bench.py` (30 dummy jobs:
queue vs two at a time vs all at once), `bench10.py` (ten real steps through two versions of the queue: before and
after), `realbuild.py` (a small real build from the shared pipeline pieces, for timing). Install or remove the
wrapper: `renderq.py install-shim` / `uninstall-shim`.
