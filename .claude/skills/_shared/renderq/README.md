# Render queue (`renderq`)

Every heavy video step on the Mac mini waits its turn here, so Dan can start 10, 20 or 30 editing jobs at once and
the machine never overloads. Rule: `VIDEO-RULES.md`, "Video builds: the render queue". Built 2026-10-20; numbers in
`Handoffs/results-20261020-render-scheduler.md` (the queue), `Handoffs/results-20261020-renderq-drives.md` (quick
lane, drives, work and scratch folders) and `Handoffs/results-20261021-renderq-v3.md` (v3: core and memory budgets).

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
- **See the line:** `python3 .claude/skills/_shared/renderq/renderq.py status` (cores and GB per holder, both budgets,
  why the line is closed). **Why is my step waiting?** `renderq.py why [RO-27]`. **See the drives:** `renderq.py drives`.
- **Size worker pools from the allowance:** `Pool(int(os.environ.get("RENDERQ_CORES", 4)))`. Every slot holder exports
  `RENDERQ_CORES` (heavy 4, light 2, quick 2) to everything it runs; a pool sized from `cpu_count()` or a fixed 6 takes
  cores and memory the budget gave to other jobs.
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

| | cores each | waits in | examples |
|---|---|---|---|
| heavy | 4 | 2 always, up to 4 while the budgets allow; each drive at most its cap | x264/ProRes/qtrle encodes, full decodes piped to Python, HyperFrames renders, chroma keys, `clipcheck.py` on long clips |
| quick | 2 | 2 slots, always open, first come first served | the same heavy work on SHORT media: inputs of 20 s or less (or `-t` 20 s, 600 frames), `clipcheck.py` on clips of 15 s or less, HyperFrames graphics of 10 s or less. An AI clip's frame dump, trim or clip check |
| light | 2 | 1 always, up to 3 while the budgets allow | Whisper (`whisper_chunked.py`, `cut/speech.py`), `deliver/gate.py`, `watch.py`, `framecheck/gate.py`, `-f null` analysis passes |
| never waits | | ffprobe, frame grabs (`-frames:v` up to 30), stills, audio-only ffmpeg, stream copies, anything `-t` 5 s or less, the `h264_videotoolbox` setup encode, review servers |

**Drive caps** (`drives.json`, measured 2026-10-20 with `drivebench.py`, two passes on a busy Mac): Extreme 2,
Expansion 3, internal 6, Seagate 2 until measured. A heavy waiter whose drive is at its cap steps aside; the next
waiter on another drive goes first. Re-measure a drive: `python3 drivebench.py Seagate --runs 2 --save` (about 3 min
per run, writes a few GB of test files to the drive and deletes them).

The wrapper at `Media/video_edit/bin/ffmpeg` (real binary: `ffmpeg.real` beside it) sorts every ffmpeg call by its
command line (reading the length of each input clip from its file header), so all ~600 pipeline scripts are covered
without edits. It prints nothing (voice_chain parses ffmpeg's stderr) and passes the exit code through untouched.
`GATE_VERBOSE=1` makes it say when it waits.

## Budgets (v3, 2026-10-21)

A slot used to stand for "one encode". On 10-21 each of the two heavy slots held a chroma key with a pool of 5-6 one-GB
workers: 11 processes and 10.5 GB on a 10-core, 32 GB Mac that also runs 30+ sessions. Swap filled and 27% of all CPU
went to the kernel paging, so every step ran slower than with two jobs. Now:

- **Core budget:** 10 cores minus 2 kept for the sessions, Chrome and the UI = 8. A step starts past the floor only
  if the cores in use (every holder's allowance, plus work outside the queue counted by the cores it burns) plus its
  own fit. The two heavy steps of the floor fill it; a light step does not take the last cores while a heavy step is waiting.
- **Memory budget:** past the floor a step starts only after memory has had room for 30 s without a break: at least
  8 GB free or inactive (`vm_stat`'s free + inactive + speculative + purgeable, read from the kernel), less than 64 MB
  written to swap in the last 30 s, and no macOS memory-pressure warning. Swap IN USE is shown, not used to decide:
  it stays high for hours after the pressure is gone (pages of idle sessions), so "under 1 GB swap" would have shut
  the line for the rest of the day; swap GROWING is the sign that starting more makes things worse.
- **Floor:** 2 heavy, 1 light, 2 quick always run whatever the budgets say, so the line never stalls. Two heavy, not
  the plan's one: two 4-core steps fill the 8-core budget exactly, and a floor of one ran the 10-21 bench 2.1x slower
  than two at a time while swap grew from work outside the queue anyway (results file).
- **Enforced:** the holder exports `RENDERQ_CORES`; the ffmpeg wrapper puts `-threads N` before every input and output
  (and `-filter_threads`/`-filter_complex_threads`) of any call that sets no thread count itself, inside a slot or
  admitted by it. `GATE_THREADS=0` turns that off for one command. Tested on ffmpeg 6.0: same streams, no new lines on
  stderr; x264 output bytes differ from a 15-thread encode of the same command (thread count is part of x264's
  output), so a re-encode is not byte-identical to one made before 10-21.
- **Memory per holder:** `status` shows each holder's resident memory (its whole process tree, one `ps` every 10 s)
  and its peak; the peak goes into `history.jsonl` with the step's cores, so allowances can be tuned from data.
- Tune in one place: `ALLOW`, `CORES_RESERVED`, `MEM_AVAIL_MIN_GB`, `SWAP_GROW_MAX_MB`, `HEADROOM_S` at the top of
  `renderq.py`. Environment overrides for tests: `GATE_ALLOW`, `GATE_BUDGET`, `GATE_MEM`, `GATE_HEADROOM_S`.

## Review servers

`renderq.py prune [--dry-run] [--hours 48]`: review page servers running longer than 48 h. A managed one (a
`com.absbyai.review.PORT` launch agent that kept a Python process alive forever) switches to START ON DEMAND: launchd
holds the port, starts the server when the page is opened, and the server exits after 24 h with no request. Same link,
same cached page, nothing running while nobody looks. One started by hand (`--serve`, `http.server`) is stopped and its
restart command printed. One started by another launch agent is only listed. New reviews start on demand from the
first `review_server.py PORT DIR`.

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
- Past the floor, a step needs both budgets (above) and nothing started in its pool (or the heavy pool) in the last
  15 s, so the last step's real load shows first. CPU and memory are read from the kernel (`host_statistics`,
  `host_statistics64`, `sysctl`), not load average. Memory samples are shared in the queue folder, so a new waiter
  inherits the 30 s history (a gap of over a minute with nobody looking restarts the clock).
- Builds outside the queue using 30%+ CPU count against the core budget by the cores they burn (`buildcap.builds()`).
- Nesting never deadlocks: a holder exports `GATE_HELD`; anything below a holder (by environment or by process
  ancestry) runs straight through, and so do the two ends of a pipe once one end holds the slot.
- Each step records its drives: an ffmpeg call's input and output files, else the folder a step runs in plus any
  `/Volumes/<drive>/` its command line names. Older code that recorded none is read from its command and folder.
- Work in a slot runs at nice 10.
- Rolling out a new version never disturbs jobs already waiting: they keep the code they started with, the files
  stay compatible both ways, and each new ffmpeg call loads the new code.

## Files

`renderq.py` (library and CLI), `ffshim.py` (wrapper entry), `selftest.py` (`renderq.py selftest`, 54 checks),
`drives.json` (per-drive caps and their measurements), `drivebench.py` (measures a drive), `bench.py` (30 dummy jobs:
queue vs two at a time vs all at once), `bench10.py` (ten real steps through two versions of the queue: before and
after; `--two` adds the same steps two at a time with no queue, plus kernel CPU and swap per run), `realbuild.py` (a small real build from the shared pipeline pieces, for timing). Install or remove the
wrapper: `renderq.py install-shim` / `uninstall-shim`.
