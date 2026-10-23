# Results: render queue v3 (core and memory budgets), 2026-10-21

Tooling, not a video task. Claude Opus 5.5, high. Phase 1 of `Handoffs/handoff-20261021-render-throughput-plan.md`.
Code: `.claude/skills/_shared/renderq/` (README there), `.claude/skills/_shared/review_server.py`. Phase 2 (the
chroma key) runs in a parallel session; nothing under `.claude/skills/_shared/chroma-key/` was touched.

## What Dan gets

- **Steps start by cores and memory, not by counting steps.** Every step gets a core allowance (heavy 4, light 2,
  quick 2). Past a floor that always runs (2 heavy, 1 light, 2 quick), a step starts only if the cores in use plus
  its own fit in 8 (10 minus 2 kept for the sessions and the UI) and memory has had room for 30 s. The old rule that
  opened two more heavy slots after a 4-second idle snapshot is gone.
- **`renderq.py status` explains itself:** cores and GB per holder (its whole process tree), both budgets, and the
  reason the line is closed ("memory: 6.82 GB free or inactive (needs 8)"). **`renderq.py why [VIDEO]`** says why a
  waiting step has not started (its drive is full, N steps ahead of it, cores, memory, settling).
- **`RENDERQ_CORES`**: every slot holder exports its allowance; the three worker pools in the shared pipeline
  outside the chroma-key folder now size from it, and Phase 2 sizes the key's pools from it.
- **Old review pages stop costing a process each.** 59 review servers were running (some 19 days old). Review
  services now start on demand: launchd holds the port and starts the server when the page is opened; it exits after
  24 h with no visit. Same links. `renderq.py prune` switched the old always-running ones over and stopped the
  hand-started ones older than 48 h.
- **Not switched on: the `-threads` cap in the ffmpeg wrapper** (built, tested, off by default). Measured below: on
  today's Mac a capped encode loses its CPU share to everything that is not capped and runs 2.5-3x slower. It is one
  constant (`THREADS_DEFAULT`) or `GATE_THREADS=1` away once the chroma key (Phase 2) and the other big thread users
  size themselves from `RENDERQ_CORES`.

- **Live since 16:48:15 (atomic rename, nothing restarted).** In the last paired test v3 made the same scheduling
  decisions as v2 (two long steps side by side, short steps in the quick lane beside them). The batch took 512 s
  against 378 s, but that run saw a busier Mac (swap peak 19.6 GB against 12.3 GB) and every step, short ones included,
  ran 25-60% slower. Quick lane since rollout: 7 steps, none waited over 0.1 s.

## 1. Incident first: the project folder moved at 14:49 (fixed 14:53)

At 14:49 iCloud's "Desktop & Documents Folders" was turned off (Phase 0, step 1 of the plan). macOS does not keep the
files in place when that happens: it leaves them in iCloud Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/
Documents/`) and creates a new, empty `~/Documents`. Every script, the ffmpeg wrapper and the render queue use the old
path `/Users/danielrose/Documents/Claude/Projects/Abs By AI`, so for four minutes new ffmpeg calls could not find the
wrapper or the real binary, and running jobs started writing into a fresh empty folder (one image, sl09 `s1-g.png`,
and one empty review log).

- 14:53: the empty folder was moved aside to `~/Documents/.stray-Claude-20261021-1449` and `~/Documents/Claude` became
  a link to the iCloud copy; the stray image was copied back. A parallel session ("Video editing performance at
  scale") made the same fix at the same moment and then linked every other `~/Documents` item; it reports the old
  paths, git, the ffmpeg wrapper and `renderq status` working. Its message: the project stays inside the iCloud
  container for now (8,655 files, 40 GB, are cloud-only placeholders; 66 GB free on the internal disk), moving it out
  is a separate handoff.
- What this means for the plan: turning the setting off did NOT stop iCloud syncing the project (it is still inside
  iCloud Drive). Phase 0 step 1 needs the project moved out of iCloud Drive to achieve its goal.
- Jobs that called ffmpeg between 14:49 and 14:53 may have failed with "not found" and need a re-run.

## 2. What changed in the queue

| | before (v2, 10-20) | v3 |
|---|---|---|
| admission | heavy 2 always, 3-4 when 30% CPU idle for 4 s; light 2, up to 3 | allowance per step; floor 2 heavy, 1 light, 2 quick; past it: cores in use + own <= 8 AND memory had room for 30 s AND 15 s since the last start |
| memory | not read | free + inactive + speculative + purgeable (`host_statistics64`), swap used and swapped-out pages (`sysctl`), macOS pressure level; no subprocess. Samples shared in the queue folder |
| work outside the queue | counted as one heavy slot each | counted by the cores it burns (250% CPU = 3 cores) |
| light vs heavy | independent | a light step past its floor does not take the last cores while a heavy step waits |
| per-holder memory | none | resident set of each holder's process tree every 10 s (one `ps`), peak kept, peak and cores written to `history.jsonl` |
| status | slots and line | + cores and GB per holder, both budgets, why the line is closed; `why` command |
| `-threads` | none | built, OFF by default (section 4) |
| review servers | always running forever | start on demand, exit after 24 h idle; `prune` |
| `run --help` | queued for a heavy slot ("--help" waited 70 min today) | prints usage |

**Deviation from the plan, on purpose: swap IN USE does not close the line; swap GROWING does.** The plan said "never
admit while swap used is over 1 GB". Swap used was 8-17 GB all afternoon and stays high for hours after pressure is
gone (pages of idle sessions), so that rule would have held the queue at its floor for the rest of the day. v3 closes
the line when more than 64 MB was written to swap in the last 30 s, when less than 8 GB is free or inactive, or when
macOS reports memory pressure; swap in use is shown in `status`.

**Deviation: heavy floor 2, quick allowance 2** (the plan: floor 1, quick 1). Both measured below.

## 3. The worker pools (`RENDERQ_CORES`)

`grep -rnE "Pool\(|ProcessPoolExecutor\(" .claude/skills scripts` outside `chroma-key/` finds three:

| file | before | now |
|---|---|---|
| `shorts/reference/ds40-greenscreen/stage1_key.py` | `Pool(4)` | `Pool(RENDERQ_CORES or 4)` |
| `shorts/reference/ds40-greenscreen/stage15_temporal.py` | `Pool(WORKERS or 4)` | `Pool(WORKERS or RENDERQ_CORES or 4)` |
| `longform-edit/reference/ro12/build.py` | `ProcessPoolExecutor(2)` | `min(2, cores // 2)` workers, each chunk encode gets `cores // workers` |

The other ~90 matches are copies in `.claude/worktrees/` (other sessions' checkouts) and job-folder copies on the
drives; neither was touched (running jobs execute those copies). The chroma key (`_shared/chroma-key/`) is Phase 2's.

## 4. Benchmarks: ten real steps started at once (`renderq/bench10.py`)

Same ten steps as 10-20 (five 24 s picture passes / ProRes from the 4K roll on Expansion and a 1080p base on
Extreme, five short steps on an 8 s Flow clip), each run in its own private queue folder. The 1080p source of 10-20
(`RO-14/round2/tmp_base.mp4`) was deleted today; `ad2-sq/base.mp4` (1080p, 276 s) replaces it, so these numbers are
not comparable with 10-20's. New mode `two`: the same steps two at a time with no queue at all (the plan's baseline).
Every run records the kernel's share of all CPU time and swap. The Mac was running Dan's live jobs throughout (load
70-215, 0% idle, swap 8-17 GB), so runs minutes apart saw very different machines: compare within a round.

| round | mode | all ten done | avg step done | short steps done (avg) | long step ran | kernel CPU | swap start -> peak |
|---|---|---|---|---|---|---|---|
| 1 (15:10-15:54) | old (v2) | 296 s | 135 s | 59 s | 57-144 s | 30% | 8.0 -> 10.6 GB |
| 1 | v3 as planned (floor 1 heavy, quick 1 core, -threads on) | 1331 s | 446 s | 179 s | 193-421 s | 43% | 10.8 -> 17.1 GB |
| 1 | two at a time, no queue | 632 s | 361 s | 320 s | 151-224 s | 42% | 11.7 -> 16.7 GB |
| 2 (16:00-16:30) | old (v2) | 384 s | 156 s | 68 s | | 31% | 11.9 -> 14.6 GB |
| 2 | v3 tuned (floor 2 heavy, quick 2, -threads on) | 948 s | 418 s | 204 s | 277-405 s | 43% | 14.4 -> 16.6 GB |
| 2 | two at a time, no queue | 422 s | 244 s | 217 s | 95-155 s | 32% | 14.0 -> 15.9 GB |
| 3 (16:35-16:47) | old (v2) | 378 s | 165 s | 73 s | 78-159 s | 35% | 11.6 -> 12.3 GB |
| 3 | **v3 as shipped (floor 2 heavy, quick 2, -threads OFF)** | 512 s | 214 s | 99 s | 127-216 s | 41% | 12.1 -> 19.6 GB |

What the rounds show:

- **v3 as planned ran the batch 2.1x slower than two at a time (round 1).** Memory never had 8 GB free and swap was
  growing (from the live jobs), so only the floor's ONE heavy step ran: the five long steps ran one after another.
  Swap still grew 6 GB during that run: holding the queue's own steps back did not stop it.
- **The `-threads` cap is what makes each step slow.** In round 2 v3 ran two long steps side by side, as intended,
  but each took 277-405 s against 95-155 s uncapped minutes later. At load 70-200 a process with 4 threads gets a far
  smaller share of the CPU than one with 15: the cap only helps when everything is capped. Today the biggest thread
  users are not (chroma-key worker pools whose cv2/numpy start their own threads, about 2 cores of work outside the
  queue, 30+ sessions). The kernel share did not fall either (43% against 31%). A short PNG frame dump at 1 thread ran
  161 s against 44 s uncapped.
- **Round 3, v3 as shipped:** the same admissions as v2 in this test (two long steps together, the quick lane beside
  them; one 4K pass queued behind a later one because reading its header off the busy hard disk made its ticket
  later, which v2 does too). Each step ran 25-60% slower than in the v2 run minutes earlier, short steps included,
  which v3 does not change at all; swap peaked at 19.6 GB during it against 12.3 GB. The difference is the machine.
- So v3 ships with the cap OFF (`THREADS_DEFAULT = False`), the heavy floor at 2 and quick at 2 cores. Turning the
  cap on is the right next step once Phase 2's key and the other pools size from `RENDERQ_CORES`: then re-run
  `bench10.py OLD NEW --two` and keep it on only if the batch is within 15% of `two`.
- The plan's targets (swap flat, kernel CPU under 10%, batch within 15% of two at a time, quick lane p90 0 s) cannot
  be met by the queue alone on this Mac today: the swap and kernel load come mostly from outside it (section 5).

## 5. Live state at the measurements (what the queue cannot see)

`renderq.py status` with v3, 15:43: cores 14 of 8 in use (three heavy holders admitted by v2's idle rule, 2 cores of
work outside the queue), 6.8 GB free or inactive, swap 11.9 GB, slot holders 6.7 GB (the RO-24 key lane peaked at
6.0 GB, DS-44's key 2.9 GB). 11 heavy waiters, 7 of them held back only by Expansion's drive cap (3). Load 80-215,
swap 8 -> 17 GB over the afternoon while the queue held at most 3-4 heavy steps: the memory comes from the sessions,
the chroma keys' worker pools and iCloud, which Phases 0 and 2 address.

## 6. Review servers

| kind | found | done |
|---|---|---|
| managed, always running (launch agent with KeepAlive) | 52 (32 older than 48 h) | the 32 switched to start on demand; all 32 links answer 200; one tested end to end (port 8873: worker killed, next visit 200, video byte range 206). The other 20 switch when re-run after 48 h, or exit on their own once refreshed with `review_server.py PORT DIR` |
| started by hand (`--serve`, `http.server`) | 7 (4 older than 48 h) | 4 stopped: 8820 (`~/abs-review/as06-ad10/sq/look`, 19 days), 8846 (`ro06/round1`), 8811 (`ro11/round2/opener-page`), 8941 (`Docs/future-reaction-ideas/glp1-aging`). Restart: `python3 .claude/skills/_shared/review_server.py PORT DIR` (then on demand) |
| started by another launch agent (`ro02-round1-review`, `hyperframes-codex-review`) | 2 | listed only |

59 review server processes before; 55 right after (the switch opens each page once to check it, which starts its
server); the switched ones exit after 24 h without a visit. Review services made from now on start on demand from the first `review_server.py PORT DIR`. Tested on spare ports
8197/8198: new on-demand service serves the page; its worker killed, the next visit starts it again; an old
always-running service switched with `--on-demand` on the same link; a worker with no request for the idle limit
exits (unit test, 1.8 s limit). `tests/test_review_server.py`: 3 of 3.

## 7. Verification

- `renderq.py selftest`: 55 checks, 54 of 54 then 55 of 55 at load 70-90 in staging; 53 of 55 live at load 100-123,
  where a different timing check misses each run (launch order of processes started 0.25 s apart, a frame grab
  starting in 1.69 s against 1.5 s, the 10-20 census needing a test process at 30% CPU). (36 checks from 10-20, minus the two idle-CPU checks, plus: two 4-core steps fit an
  8-core budget and a third waits; `why` names the budget; too little memory runs the floor only and `status` says
  why; swapping blocks extra steps and `why` says so; the 30 s headroom window (3 s in the test); `RENDERQ_CORES`
  heavy 4 / light 2 / quick 2 / tunable / unset after `slot()`; the wrapper leaves commands alone by default; with the
  cap on, `-threads` lands before inputs and outputs, a command's own `-threads` is untouched, exempt calls are left
  alone, a nested step gets its holder's allowance, `GATE_THREADS=0` turns it off; the REAL ffmpeg 6.0 runs an encode,
  a filter graph, two outputs and a pipe with the injected options; status shows cores and GB per holder; prune
  `--dry-run` lists and `prune` stops a hand-started review server). Timing checks with 1.5 s limits miss now and
  then at load 90+ (a different one each run, 54 of 55 at worst); every check has passed.
- ffmpeg 6.0 with the injected options: same output streams, no new stderr lines (x264's info line says threads=4
  instead of 7). x264's output bytes depend on its thread count.

## Rollout

- 16:48:15: `renderq.py`, `selftest.py`, `bench10.py`, `README.md` and `review_server.py` (plus its test) replaced by
  atomic rename (copy beside, `os.replace`). Nothing was cancelled or restarted. The live line then held 3 heavy steps
  (admitted by v2's idle rule) and 11 heavy waiters; waiters keep the v2 code they started with (two heavy always, the
  idle rule for 3-4) and drain; every new ffmpeg call and new waiter runs v3. File formats are compatible both ways:
  v3 adds `cores` to slot files and `cores`/`peak_mb` to `history.jsonl`, plus `mem.json`, `rss.json`, `ffcaps.json`
  in the queue folder, which v2 never reads.
- Right after: `status` and `why` read correctly on the live line; a real ffmpeg call through the wrapper returned 0.
- VIDEO-RULES: "Video builds" now states the budgets and the `RENDERQ_CORES` rule; the review-page rule says services
  start on demand and adds the `prune` housekeeping line.
- The v2 snapshot used for the benchmark was removed; to bench against v2 again: `git show da1a198:.claude/skills/_shared/renderq/renderq.py`
  into a sibling folder of `renderq/` with `ffshim.py` and `drives.json` (the folder must sit in `_shared/`).

## Next

1. Phase 2 (chroma key): size its pools from `RENDERQ_CORES` and cap cv2's own threads per worker
   (`cv2.setNumThreads(1)` in each worker), then turn the `-threads` cap on and re-run
   `python3 renderq/bench10.py <old> renderq --two`.
2. Phase 0 step 1 is not done: the project is still inside iCloud Drive, now behind a link. Move it out (separate
   handoff, per the parallel session).
3. Watch `history.jsonl` peaks (`peak_mb`, `cores`) for a few days and tune `ALLOW` / `MEM_AVAIL_MIN_GB` from them.
