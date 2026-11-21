# Where the wall-clock time actually goes in a video build

**Measured 2026-08-27, Mac mini M2 Pro (6P+4E cores, 16-core GPU unused, 32 GB).**
$0.00 AI spend. No production code, no deploy, no native-retest trigger.

Method: a shell shim installed at the one real `ffmpeg`/`ffprobe` binary
(`Media/video_edit/bin/`), so every call site in every skill is captured, plus a
per-stage wrapper. The shim writes timing to a separate log and never touches
stdout/stderr — verified byte-identical stderr against the real binary and a real
two-pass `finish_audio.py` loudnorm parse.

---

## 1. Total wall-clock time for one full build

Build: the **Ad 1 vertical 9:16 master** (3:52.8 finished, 99 EDL segments), rebuilt
from the raw C1591 roll into a scratch copy. **Single-tenant machine, nothing else
running.**

| | |
|---|---|
| **COLD cache (full rebuild)** | **19.1 min** |
| **WARM cache (one-beat revision)** | **6.7 min** |
| of which ffmpeg / x264 | 81 % cold |
| of which single-threaded Python (PIL, numpy) | 19 % cold |

The segment cache is doing its job: a revision costs about a third of a full build.

## 2. The stage table

| stage | wall | in ffmpeg | in Python | % | bound by | which optimization touches it |
|---|---|---|---|---|---|---|
| `05_render` | **8.5 min** | 5.6 min | **2.9 min** | **44.3 %** | x264 + PIL | Mac upgrade; parallel PIL |
| `01_build_base` | **7.1 min** | 7.1 min | 0.0 | **37.4 %** | x264 (99 encodes) | Mac upgrade only |
| `06_master_mux` | 1.9 min | 1.9 min | 0.0 | 10.0 % | x264 | Mac upgrade only |
| `04_captions` | 0.9 min | 0.1 min | **0.7 min** | 4.6 % | **PIL, 1 core** | parallel PIL |
| `02_build_audio` | 0.25 min | 0.24 min | 0.0 | 1.3 % | ffmpeg | — |
| `03_finish_audio` | 0.23 min | 0.22 min | 0.0 | 1.2 % | ffmpeg | — |
| `07_review_540p` | 0.23 min | 0.23 min | 0.0 | 1.2 % | x264 | VideoToolbox |
| **TOTAL** | **19.1 min** | **15.4 min** | **3.6 min** | | | |

Warm revision: `build_base` 2.2 min (concat + a full-decode `ffprobe -count_frames`),
`render` 2.6 min, `master_mux` 1.9 min.

**Top 3 stages = 92 % of the build.** Two of the three are pure x264.

## 3. Single-threaded vs. already-multi-core

| | share of cold build | what can reach it |
|---|---|---|
| ffmpeg / x264 — **already uses all 10 cores** | **15.4 min (81 %)** | only a faster chip |
| single-threaded Python (PIL, numpy) — **1 of 10 cores** | **3.6 min (19 %)** | parallelising, or IPC |

Parallelising every PIL pass perfectly across the 6 performance cores would take
3.6 min down to roughly 0.9 min. **The absolute ceiling on that optimization is
~2.7 min per cold build, and ~5 seconds on a warm revision.**

## 4. Whisper, measured in isolation

| roll | audio | wall | realtime factor | peak RSS |
|---|---|---|---|---|
| C1591 (ad roll) | 6:22 | **45.3 s** | **8.4×** | 2.84 GB |
| C1513 (longform roll) | 40:17 | **4.5 min** | **8.9×** | 3.61 GB |

100 % single-threaded Python. This confirms the docstring's own claim (5:45 in 41s).
**Whisper is much faster than assumed** — it did not appear in the measured build at
all, because that build's transcript already existed.

## 5. The finding that dwarfs all three optimizations

The first attempt at this measurement ran while **four other build sessions were
running on the same Mac. Load average hit 242 on a 10-core machine, 0 % idle.**

`finish_audio.py` — the identical script on the identical input:

| | wall |
|---|---|
| quiet machine | **13.6 s** |
| 4 concurrent builds | **126 s** |

**A 9.3× latency penalty.** And it buys nothing: x264 already saturates all 10 cores,
so four concurrent builds do not raise throughput, they just timeslice. The only real
headroom is the 19 % of each build that is single-threaded Python — so **two**
concurrent builds overlap usefully (one build's PIL under another's x264); beyond two
it is pure loss.

Overnight the shim captured **11,627 invocations / 34.5 h of ffmpeg over 12.4 h wall**
— an average of 2.8× oversubscription sustained all night.

## 6. Where ffmpeg time actually goes (11,627 real calls, 12.4 h)

| bucket | time | share | n |
|---|---|---|---|
| video encodes (mp4) | **26.1 h** | **75.7 %** | 3,629 |
| analysis passes (`-f null`, rawvideo, pipe) | 4.3 h | 12.5 % | 2,887 |
| graphics overlay plates (qtrle) | 3.1 h | 9.0 % | 1,261 |
| frame grabs / contact sheets | 0.7 h | 1.9 % | 3,636 |
| audio | 0.3 h | 0.8 % | 214 |

- **74 % of all calls are sub-second — and together they are 2.0 % of the time.**
- **The top 10 calls are 50 % of all ffmpeg time.**
- The single longest call was **5 h 20 m**: one longform `picture_final.mp4`.

⚠ **THAT 5-HOUR CALL WAS A BUG, NOT A WORKLOAD — corrected after reading the concurrent
session's notes.** An unbounded `-loop 1 -i wm.png` with no `-t` collapses the whole filter
graph; bounded, the identical pass takes **17 minutes**. A second trap (a deep chain of
`setpts`-shifted alpha overlays) ran at 0.08x realtime against 1.12x flattened. Both are
fixed and now recorded in `/longform-edit`. **Do not read the multi-hour encodes in the
overnight log as the cost of longform rendering** — they are the cost of two defects.

**Clean encode rates measured on this machine:**

| pass | rate |
|---|---|
| heavily-filtered picture pass (1080-class, preset medium) | **0.95x realtime** |
| master mux (overlay + AAC, preset medium) | 2.04x realtime |
| 540p review copy (preset veryfast) | 16.6x realtime |

**These two independent measurements agree.** My 0.95x realtime and the other session's
"17 minutes for a 19-minute programme" (~0.9x) are the same number reached different ways.
So the real rule is simple: **a picture pass costs about one second per second of finished
video.** The 3:52 ad renders in ~4 min per pass; a 19-minute longform in ~17 min per pass.
A longform build runs several passes plus transcription, so it lands around **45-70 min** --
substantial, but under an hour, not the "hours" the raw log suggested.

---

## 7. VERDICT — minutes saved per build

| | ad build (19.1 min) | longform build (~45–70 min) | worth doing? |
|---|---|---|---|
| **1. `mlx-whisper` swap** | **~30 s** | **~3–5 min** | **No, not for speed.** |
| **2. VideoToolbox on disposable outputs** | **~10 s** | ~1–2 min | **No. Definitively.** |
| **3. Parallelise the PIL passes** | **~2.7 min** (ceiling) | ~5–10 min | **Marginal.** |
| **4. Mac upgrade — M4 Pro mini (≈2×)** | **~8.5 min** | **~20–30 min** | **Probably not.** |
| **4b. Mac upgrade — M4 Max Studio (≈2.4×)** | ~9.6 min | ~25–35 min | Same, marginally better. |
| **5. Stop running 4 builds at once** | **~40–70 min** | **~1–2 h** | **Yes. Free. Do this first.** |

### Reading of each

**1. mlx-whisper — do not do it for speed.** Whisper is 8.4–8.9× realtime already and
is 0–4 % of a build. A 2.5× speedup returns half a minute on an ad. It is gated on a
word-timestamp equivalence test, and those timestamps carry EDL recovery, lip-sync
xcorr and wrong-take detection. **The risk is real and the reward is half a minute.**
Revisit only if it also improves accuracy — that would be a different argument.

**2. VideoToolbox — dead.** The only genuinely disposable output in a build is the
540p review copy: **14 seconds**. Contact sheets and A/B files live in the sub-second
bucket that is 2 % of everything. Best case saves ~10 seconds, in exchange for
invalidating the segment cache and recalibrating a QC gate built on x264. **No.**

**3. Parallel PIL — the only software change with a real number, and it is small.**
Ceiling 2.7 min on a cold ad build (14 %), essentially zero on a revision. On longform
it is worth more because there are far more graphics plates. Against this pipeline's
documented history of ordering bugs, I would not spend the risk on an ad build; it is
arguable for longform.

**4. The Mac — genuinely 2×, but on jobs measured in minutes.** M4 Pro saves ~8.5 min
per ad build and ~20–30 min on a longform build. At two or three builds a week that is
well under an hour a week for $1,400–2,000. **That does not pay.** An earlier draft of
this argued the opposite on the strength of multi-hour encodes in the log — those turned
out to be the `-loop 1` bug, and fixing one defect bought back far more than doubling the
CPU would have. **Do not buy the Mac on these numbers.**

**5. Scheduling — the biggest lever, and it costs nothing.** Four concurrent sessions
made one stage 9.3× slower for no throughput gain. **Cap concurrent builds at two.**
This is worth more than all three software optimizations combined, and more than the
new Mac, and it can be done today.

### The honest headline

**Nothing on the original optimization list is worth doing.** Two of the three save
seconds; the third saves under three minutes and carries correctness risk. The
hardware is real but small against how often ad builds actually run.

**The pipeline is not slow — the machine is oversubscribed.** Fix the scheduling
first, then re-measure before spending anything.

---

## Reproducing this

Scripts committed to `.claude/skills/_shared/timing/`:
`ffmpeg_shim.zsh`, `stage.zsh`, `report.py`.
Working files (logs, scratch build, runners) in `/Volumes/Extreme/_edit_work/_timing/`.

⚠ **The shim must never be left installed.** Restore with:
`cd Media/video_edit/bin && mv ffmpeg.real ffmpeg && mv ffprobe.real ffprobe`
