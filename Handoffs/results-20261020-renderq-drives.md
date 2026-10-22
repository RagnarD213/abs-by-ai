# Results: render queue upgrade (quick lane, drive caps, work and scratch folders), 2026-10-20 evening

Tooling, not a video task. Claude Opus 5.5, high. Code: `.claude/skills/_shared/renderq/` (README there). Builds on
`results-20261020-render-scheduler.md` (the queue itself, same day).

## What Dan gets

- **Short steps stop waiting behind long renders.** An 8 s AI clip's frame dump, trim, clip check or a short graphic
  goes in its own two-slot "quick" lane. In the 10-job test the short steps finished about 3x sooner and the whole
  batch finished sooner, with the long renders no slower (numbers below).
- **Each drive takes only as much as it can handle** (Extreme 2 heavy steps, Expansion 3, internal 6). A job whose
  drive is full steps aside and a job on another drive goes first.
- **New jobs land on the least busy drive with room:** `renderq.py workdir <JOB>`. The video skills now say to use it.
- **Throwaway frames and test renders go to the internal SSD:** `renderq.py scratch <JOB>`. HyperFrames graphics now
  render there and move into place.

## 1. What got past the queue (audit), and what was fixed

| gap | how big | done |
|---|---|---|
| The census of work outside the queue only knew a process named `ffmpeg`; the wrapper runs `ffmpeg.real`, so it counted nothing (0 of 5 live ffmpeg.real seen) | big: the backstop was blind | **Fixed.** It now counts any busy ffmpeg / ffmpeg.real / Python / Whisper / headless-Chrome process tree outside a slot that is not waiting in line (30%+ CPU). Selftest added |
| `buildcap.wait()` (about 500 job scripts) waits its turn, then hands the slot straight back; Vision, cv2, Whisper or PIL work after it runs with no slot | big | **Covered by the census fix** (that work now counts against the heavy pool while it runs). Not converted to hold-until-exit: scripts that run parallel encodes after it would then pile them all onto one slot |
| HyperFrames "cycle" graphics (`hyperframes/cycle/build.py`, reached from `from_plan.py` and Codex's `scripts/video/hyperframes_graphics.py`) rendered Chrome with no slot | medium | **Fixed:** slot (quick when 10 s or less) |
| Whisper run directly: `longform-edit/reference/whisper_run.py` (the skill prescribes it), `scripts/video-audit/transcribe_rolls.py`; copies of `whisper_chunked.py` in job folders silently lost their slot | medium | **Fixed:** light slot; copies find the queue by absolute path |
| `shorts/reference/full-bleed/render.js` used ffmpeg-static (same binary, no wrapper) for x264 encodes | dormant since 09-18, still prescribed | **Fixed:** uses the wrapper when present |
| Frame dumps (`f%03d.png`) and clip checks were queued as heavy, behind 10-minute renders: on 10-20 frame dumps ran 0.7 s median but waited up to 21 min; 21 s clip checks waited up to 73 min | the main slowdown Dan saw | **Fixed:** quick lane |
| A race (old code too, 1 run in 4 on the busy Mac): a new slot holder recorded who it was only after the admission lock opened, so two ends of a pipe could take two slots, and two jobs could slip past a drive cap | small, real | **Fixed:** the holder is written inside the lock (8 of 8 clean afterwards) |

Left as they are (reported, not changed):
- Exempt calls by design (VIDEO-RULES): `-frames:v` up to 30 and `-t` up to 5 s never wait, so a loop of hundreds of
  single-frame grabs (seen live on sl09) or per-shot 30-frame encodes (`ro18/build.py`) run unqueued. The new census
  now counts such a loop while it is busy.
- cv2 full decodes inside `deliver/gate.py`'s light slot; `kit9x16/kit_run.py` measures label clearance in-process
  with no slot (the kit9x16 folder had another session's uncommitted edits, so it was not touched).
- Chrome/Playwright screen captures (`website-video` capture scripts, a few recipe recorders): occasional.
- One-off recipe copies (`ad-edit/reference/*/s15_txmaster.py`, `/Volumes/Expansion/_edit_work/ro28/round1/whisper_words.py`).
- The overnight edit queue (`scripts/edit-queue`, paused) still makes job folders under Extreme only.
- Codex skills under `Media/codex-video-trial/skills/` had another session's uncommitted edits; they read the rule from
  VIDEO-RULES.md, which now carries it.

## 2. Drive measurements and caps

`renderq/drivebench.py`: 1, 2, 3, 4 and 6 streams at once, 5 s per level, uncached (F_NOCACHE), test files written and
deleted. "Mixed" = n steps, each one 1 MB-block reader plus one writer (a render reading source and writing output).
Two passes for the externals, one for internal, all while other sessions kept the Mac at 0% idle. MB/s, average:

| drive | kind | mixed x1 | x2 | x3 | x4 | x6 | cap |
|---|---|---|---|---|---|---|---|
| internal | Apple SSD (APFS) | 2730 | 3354 | 2610 | 3588 | 2870 | **6** |
| Extreme | SanDisk Extreme V3 SSD, USB, exFAT, 99% full | 316 | 619 | 366 | 330 | 359 | **2** |
| Expansion | Seagate Expansion HDD 24 TB, USB, exFAT | 269 | 209 | 240 | 225 | 236 | **3** |
| Seagate | not plugged in | | | | | | **2** until measured |

Cap rule: the most steps at once at which each step still gets 60 MB/s and the drive's total is at least 60% of its
best. Extreme's total peaks at 2 steps and falls 40% at 3 or more (both passes); Expansion holds about 230 MB/s flat,
which feeds 3 steps at 60+ MB/s each. One real 8 s Flow clip dumped to PNG took 5.9 to 7.5 s on every drive (the PNG
encoder is the limit, about 90 MB/s), but the same 192 frames used 769 MB on Extreme against 528 MB on the internal SSD
(exFAT cluster size). Re-measure: `python3 renderq/drivebench.py Seagate --runs 2 --save`.

## 3. Work folders

`renderq.py workdir <JOB> [--need GB] [--source PATH] [--why]`: the job's existing `_edit_work/<JOB>` on any plugged-in
drive (case-insensitive, real spelling returned), else a new one on the drive with the lowest busy score: heavy steps
running there plus half the waiting ones, over its cap, plus 0.15 per job folder touched in the last 3 h; SSD first on a
tie; a hard disk that holds the job's source footage counts 0.5 busier. A drive needs `--need` (default 20 GB) plus its
reserve free (Extreme 30 GB, others 100 GB). Today Extreme has about 30 GB free, so new jobs go to Expansion.
Skills updated: longform-edit, ad-edit, shorts, video-setup; VIDEO-RULES carries the rule for everyone else.
Codex rounds also used `/Volumes/Expansion/Abs By AI Edit Work/<job>/` (RA-13 round 3, RA-16 R4 scripts); the picker
finds and counts folders under both names, and new folders go in `_edit_work`. RA-13 is split across Extreme
(`_edit_work/ra13`) and Expansion (`Abs By AI Edit Work/ra13/round3`) by its own scripts; the picker returns the most
recently used one. Not moved.

## 4. Scratch

`renderq.py scratch <JOB>`: `/tmp/absbyai-scratch/<JOB>` on the internal SSD while it keeps 50 GB free after the
request (it has about 95 GB free and macOS swap grows into it), else `_scratch` in the job folder. Folders untouched
for 48 h are deleted. HyperFrames renders (`hfbuild.render`) now render there (Chrome's frames and encoder chunks) and
move the finished .mov into place. Evidence that reviewers read (clipcheck frames, watch sheets) stays beside the clip.

## 5. Before and after: ten real steps started at once

`renderq/bench10.py`: each run starts the same ten steps within 3 s, each through one queue version's ffmpeg wrapper
and its own private queue folder (the live line was never joined). Extra CPU slots off in both (the Mac never sat
idle). Five long steps (24 s of footage each: picture passes from the 4K 10-bit 9/23 roll on Expansion and the RO-14
master on Extreme, one ProRes 4444 intermediate) and five short ones on an 8 s Flow clip (three frame dumps, two
trims). OLD = the queue as installed this afternoon; NEW = this version.

| run | queue | all ten done | average step done | short steps done (avg) | short steps waited (avg) | long steps done (avg) |
|---|---|---|---|---|---|---|
| 1 | old | 235 s | 130 s | 109 s | 91 s | 152 s |
| 1 | new | 190 s | 89 s | 39 s | 15 s | 140 s |
| 2 | old | 218 s | 116 s | 101 s | 87 s | 131 s |
| 2 | new | 185 s | 78 s | 32 s | 12 s | 125 s |
| **average** | **old** | **227 s** | **123 s** | **105 s** | **89 s** | **142 s** |
| **average** | **new** | **187 s (-17%)** | **84 s (-32%)** | **35 s (3.0x sooner)** | **13 s** | **132 s (-7%)** |

- In the old queue a 1.5 s JPG frame dump waited 72 to 98 s and a 9 s trim waited 64 to 142 s behind 24 s picture
  passes; in the new one both started within 25 s, beside the long steps.
- Long steps were not slowed: they finished sooner, because short steps no longer took their heavy slots. A short
  step itself ran somewhat longer (a trim 9 to 18-25 s) because it shared the CPU with two long encodes, and still
  finished three times sooner.
- The drive caps did not bind in this test: with the Mac at 0% idle only two heavy slots open, and the two picture
  passes per drive never exceeded Extreme's 2. They bind when idle CPU opens slots 3 and 4 (then the extra slots go to
  jobs off a full drive); the selftest covers that logic.
- Live, right after install: a real frame dump of an 8 s Flow clip (192 JPGs to scratch) took a quick slot at once and
  finished in 2 s; the identical dump queued by the old code in the heavy line had waited 112 min.

## Rollout

- Installed by atomic rename while 42 jobs were waiting in the live line; no job was cancelled or restarted. Jobs
  already waiting keep the code they started with; file formats are compatible both ways (new fields are optional;
  older holders' drives are read from their command and folder). Each new ffmpeg call loads the new code.
- Old waiters already in the heavy line stay there (they cannot move to the quick lane); the line drains as they run.
- Older waiters' census (which counts quick-lane jobs as outside the queue) is never reused by the new code.

## Verification

- `renderq.py selftest`: 36 of 36 (21 earlier checks plus: drive caps step aside, old-format holders count against
  their drive, clip length read from the header, quick lane for short clips and not long ones, command-line sorting,
  work folder reuse and choice, no-room fallback, scratch placement, pruning and fallback, census counts a busy
  outside build and not one waiting in line; kill -9 now measured by the queue's own grant time).
- Live after install: `renderq.py status` shows the quick pool and the drive line; a real frame dump went in
  `quick.0` with no wait (2 s), and a copied 6.75 s HyperFrames graphic went in `quick.0` with no wait, rendered in
  `/tmp/absbyai-scratch/`, and its ProRes 4444 .mov (203 frames) was moved into place with the scratch folder removed.
  That render took 119 s on the busy Mac, so a quick slot can be busy for about two minutes; still minutes, not hours.
