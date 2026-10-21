# Handoff: make 20-50 simultaneous video edits run at full machine speed (render throughput plan)

Tooling, not a video task. Written 2026-10-21 (Claude Fable 5.1) after measuring the live Mac while 15 editing jobs and
34 Claude Code sessions were running. Dan: "diagnose what the problem is and make a plan to fix this so that I can
fire 20, 30, 50 video editing tasks at a time, and they don't run slower than if I only did 2 at a time."

Three execution sessions come out of this plan (starter prompts at the bottom): **Phase 1** render queue v3 (budget
cores and memory, not step count), **Phase 2** cheap chroma key (the step that eats half of all render time), **Phase 3**
extra compute (only if Dan still wants 50 at once to feel like 2 after Phases 1-2). Phase 0 is two things only Dan can do.

## 1. Diagnosis (measured 2026-10-21, 13:55-14:10)

The Mac mini (Apple M2 Pro, 10 cores: 6 performance + 4 efficiency, 32 GB RAM) was at:

| measure | value | healthy |
|---|---|---|
| load average (1 min) | 316 | under 10 |
| CPU idle | 0% (73% user, 27% kernel) | kernel under 10% |
| swap used | 4.9 GB -> 5.5 GB of 6 GB in 3 minutes, still growing | near 0 |
| compressed memory | 10 GB | small |
| heavy-slot waits today | median 7 s, p90 68 min, max 151 min, 44 steps waited over 10 min | minutes |
| heavy-slot waits yesterday | median 3 min, p90 73 min, max 122 min, 168 steps waited over 10 min, 148 slot-hours of waiting | |
| light-slot waits today (Whisper, checks) | p90 5.4 min, max 19 min | seconds |
| quick lane | p90 0 s | fine |

The render queue built on 10-20 is doing its job (quick lane p90 is 0 s; CPU inside slots 657%, outside slots 164%).
The slowdown has five causes, in order of size:

### 1a. The queue counts steps, not cores or gigabytes
A "heavy slot" was meant to be roughly one encode. The two heavy slots right now each hold a chroma-key stage running a
Python worker pool of 5-6 processes at about 1 GB each: 11 processes and 10.5 GB for two slots, on a 10-core 32 GB
machine that also runs 34 Claude Code sessions (2.2 GB), the Claude desktop app (1.3 GB), Codex (0.7 GB), Chrome (1.1 GB)
and iCloud. Nothing in `renderq.py` reads memory at all (`grep -n memory renderq.py` finds nothing). Only 10 of 889
ffmpeg-calling files set `-threads`, so each x264 encode starts 15 threads.

The elastic rule makes it worse: slots 3 and 4 open when 30% of the CPU sat idle for 4 seconds, then a 60-minute
6-core key takes the slot. That happened 28 times today. A 4-second snapshot is committing an hour of 6 cores and 6 GB.

**Effect:** more processes than cores, and more resident memory than RAM. Swap filled, 27% of all CPU went to the
kernel (compressing and paging), and every running step slowed, which is exactly "slower than 2 at a time".

### 1b. The house chroma key is the elephant
`.claude/skills/_shared/chroma-key/reference/ds40-claude-r2/`: stage 1 (`Pool(4)`) plus stage 1.5 temporal
(`Pool(WORKERS or 4)`, DIS optical flow and four `cv2.remap` passes per neighbour frame at 2880x1620 float32). Live
measurement: 660 frames in 1454 s, about 2.2 s a frame with 5-6 cores, so a 38 s clip costs about 40 minutes of a
heavy slot, and a one-minute green-screen short with three pieces about 75 minutes.

| | heavy slot-hours | of which chroma key |
|---|---|---|
| 2026-10-20 | 21.3 h (71 videos) | 4.8 h |
| 2026-10-21 (to 14:00) | 18.1 h (24 videos) | 8.5 h; RO-24 alone 12.0 h in 17 steps |

RO-24 keyed each of its three clips **three times** today (and twice yesterday), 40-75 minutes a run, while
calibrating plate, crop and hold-out boxes. Calibration by re-running the full clip is the single largest waste in the
line: about 6 of today's 8.5 key hours. The 10-21 rule in AGENTS.md makes this key the standard for every green-screen
video, so its cost now scales with everything Dan films on green.

### 1c. iCloud is syncing the whole project folder
`~/Documents` is in iCloud Drive (Desktop & Documents Folders is on: `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude`
exists). `fileproviderd` has used 2,735 CPU-minutes (45 hours) in the 20 days since boot and was at 104% of a core
during the measurement, with the CloudDocs container in a permanent "needs-sync-up" state. It is also why `.git`
objects get evicted (board entry "Main Git cloud read BLOCKED 2026-10-16": an iCloud-evicted object). One of ten cores,
all day, plus repository corruption risk.

### 1d. Many sessions, each doing unqueued small work
34 Claude Code sessions, 20 Codex processes, 19 node MCP servers (611 MB), 70 orphaned Python review servers (62
listening ports, some from 20 days ago), WindowServer at 30% drawing all of it. None of this is heavy, but it is the
164% CPU and about 6 GB that the queue cannot see, and it is what tips 32 GB into swap.

### 1e. Minor: Spotlight indexes both work drives; Extreme is 100% full
`mdutil -s` shows indexing enabled on Extreme and Expansion (frame dumps of thousands of PNGs get indexed). Spotlight's
cumulative cost is small (about 6 CPU-hours in 20 days). Extreme has 13 GB free of 3.6 TB (a cleanup handoff is open).

### What the numbers say about the goal
Two chroma keys already want 11 cores. 50 videos at about three keyed clips each is roughly 100 hours of 6-core work:
no scheduler makes that finish as fast as two videos on this machine. What Phases 1-2 can deliver on the current Mac:

- the batch finishes as fast as the machine physically can (no swap collapse: today's kernel share of 27% goes back to work),
- short steps, review pages and the sessions themselves stay instant (already true for the quick lane),
- the dominant step costs 3-5x less, so the same machine does 3-5x the videos per day,
- Dan's priority order is honoured (`--priority` exists already).

Making 50 at once feel like 2 at once needs about 25x the compute: that is Phase 3 (cloud render workers or a second
machine), and it only pays once Phases 1-2 have removed the waste.

## 2. Phase 0: Dan, five minutes (today)

1. **Turn off iCloud sync for the project folder.** Recommended: System Settings > [Dan's name] > iCloud > iCloud Drive
   > turn off "Desktop & Documents Folders" (choose Keep a Copy). The files stay on the Mac; the repo is on GitHub and
   media is backed up nightly to Seagate and Drive. Alternative if Dan wants other Documents to keep syncing: a Claude
   session moves the project to `~/Projects/Abs By AI` and leaves a symlink at the old path, at a quiet moment with no
   jobs running (hundreds of scripts hard-code the old path; the symlink keeps them working). Claude cannot change a
   system setting itself.
2. **Stop Spotlight indexing the work drives** (needs Dan's password):
   ```bash
   sudo mdutil -i off /Volumes/Extreme /Volumes/Expansion
   ```

## 3. Phase 1: render queue v3, budget cores and memory (Claude Opus 5.5, high; one tooling session, about half a day)

Code: `.claude/skills/_shared/renderq/renderq.py`, `ffshim.py`, `selftest.py`, `buildcap.py`. Keep every existing
behaviour (quick lane, drive caps, workdir, scratch, priority, continuations) and add:

1. **Core budget instead of slot count.** Each admission carries a core allowance: heavy 4, light 2, quick 1 (tunable
   in one table). Budget: 10 cores minus 2 reserved for sessions, Chrome and the UI. Admit the head of the line only
   while allowances in use plus the new one fit the budget. This replaces "2 always, up to 4" and the 4-second idle rule.
2. **Memory budget.** Before admitting, read free + inactive memory and swap in use (`vm_stat`, `sysctl vm.swapusage`,
   no subprocess if `host_statistics` offers it). Never admit while swap used is over 1 GB or less than 8 GB is free,
   except that one heavy and one light step may always run so the line never stalls. Elastic admission beyond the
   base needs headroom for 30 s, not 4 s. Track each holder's resident set (sum of its process tree, `ps -o rss`)
   every 10 s and show it in `status`.
3. **Enforce the allowance.** The ffmpeg wrapper injects `-threads <allowance>` (and `-filter_threads`) when the command
   sets none; `renderq.run`/`slot()` export `RENDERQ_CORES`; the chroma-key stages and every `Pool(` in the pipeline
   size from it (`int(os.environ.get("RENDERQ_CORES", 4))`). Grep list: `grep -rnE "Pool\(|ProcessPoolExecutor\(" .claude/skills scripts`.
4. **Status that explains itself.** `renderq.py status` prints cores and GB per holder, the two budgets, and the reason
   a slot is closed ("memory: 5.4 GB swap in use"). Add `renderq.py why` for a waiting ticket.
5. **Housekeeping.** `review_server.py` exits after 24 h without a request (70 orphans today); `renderq.py prune`
   kills review servers older than 48 h and reports them. Rule line in VIDEO-RULES.
6. **Verification before rollout.** `selftest.py` additions: budget admission, memory refusal, allowance injection,
   `RENDERQ_CORES` honoured. Then `bench10.py` old vs new, and a live 10-job start recorded in a results file: target
   swap flat, kernel CPU under 10%, total batch time within 15% of the two-at-a-time serial time, quick lane p90 still 0 s.
   Roll out by atomic rename exactly as on 10-20 (waiting jobs keep their code).

## 4. Phase 2: a cheap house key with identical output (Claude Opus 5.5, high; one session, maybe two)

Code: `.claude/skills/_shared/chroma-key/` (README, `reference/ds40-claude-r2/stage1_key.py`, `stage15_temporal.py`,
`keylib.py`, `stage2_comp.py`). The locked style stays locked: a change is accepted only if the existing exact-file
gates and the measured edge metrics match the R2 output on the same clip (bit-identical where a gate demands it).

1. **Calibrate on excerpts, key once.** Plate, crop and hold-out calibration runs on two or three 2-3 s samples of the
   clip in the quick lane (seconds, not an hour), with a contact sheet for the editor; the full-clip key runs exactly
   once. Write this into the chroma-key README and VIDEO-RULES; `run_key.sh`'s `.done` cache becomes the rule for every
   recipe, Claude and Codex, so a round never re-keys an approved piece.
2. **Profile per frame** (`cProfile` on 30 frames): expected hot spots are DIS flow, the four `cv2.remap` calls per
   neighbour, the Gaussian normalised convolution and float32 copies at 2880x1620.
3. **Speed-ups to test, in order, each gated:** compute the temporal confidence maps at half resolution and upsample
   the weights only (not the colour); reuse one flow computation per frame pair in both directions; replace the four
   remaps with one remap of a stacked array; float16 intermediates where the gate still passes; memory-map once per
   worker instead of per frame (cuts the 1 GB per worker). Target: at least 3x faster, under 400 MB per worker.
4. **Measure and record:** minutes per 30 s clip and GB per worker before and after, same hashes or metrics, in
   `Handoffs/results-<date>-cheap-key.md`; update the README's cost line so planners can estimate.

## 5. Phase 3: extra compute, only after Phases 1-2 (Dan's decision)

If Dan still wants a 50-job batch to feel like a 2-job batch: a cloud CPU worker pool for keys and encodes (push the
clip, pull the matte; a 64-vCPU on-demand VM is roughly $3 an hour, estimate to verify, and runs about ten keys at
once), or a second Mac on the LAN as a render node (bigger up front, nothing per job). Recommend a one-week cloud trial
measured in dollars per keyed clip. Not before Phases 1-2: today about 40% of the machine's work is waste.

## 6. Starter prompts

**Phase 1 (fire now; Claude Opus 5.5, high; title `Render queue v3 budgets`):**
> Execute Phase 1 of `Handoffs/handoff-20261021-render-throughput-plan.md`: make the render queue
> (`.claude/skills/_shared/renderq/`) admit by a core budget and a memory budget instead of slot count, inject
> `-threads` from the allowance in the ffmpeg wrapper, export `RENDERQ_CORES` and size every `Pool(` in the pipeline
> from it, add memory-aware status, prune orphan review servers, extend selftest, run bench10 old vs new, roll out by
> atomic rename, and record results in `Handoffs/results-<date>-renderq-v3.md`. Do not touch running jobs.

**Phase 2 (fire after Phase 1 is live; Claude Opus 5.5, high; title `Cheap house chroma key`):**
> Execute Phase 2 of `Handoffs/handoff-20261021-render-throughput-plan.md`: make the house chroma key
> (`.claude/skills/_shared/chroma-key/reference/ds40-claude-r2/`) at least 3x cheaper with identical gated output,
> calibrate on 2-3 s excerpts in the quick lane and key each clip once, make the `.done` cache the rule for every
> recipe, and record minutes per clip and GB per worker before and after in `Handoffs/results-<date>-cheap-key.md`.
