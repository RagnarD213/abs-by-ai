# Results: a cheaper house chroma key with identical output, 2026-10-21

Tooling, not a video task. Claude Opus 5.5, high. Phase 2 of `Handoffs/handoff-20261021-render-throughput-plan.md`.
Code: `.claude/skills/_shared/chroma-key/` (README there). Phase 1 (render queue v3) ran in a parallel session; nothing
under `.claude/skills/_shared/renderq/` was touched. Work folder (media, not in git): `/Volumes/Extreme/_edit_work/cheapkey/`.

## What Dan gets

- **Every keyed frame is bit-for-bit the approved Bill Maher Fat 90-Year-Old R2 key.** Proved on the approved sample: the new code's caches equal the approved code's on 279 of 279 frames, and its pale, navy and pink renders have exactly the SHA-256 values in `approval.json`. The gates cannot move, because the pixels did not.
- **Each frame costs about a third less CPU, and stage 1.5 about half the memory.** On the approved sample (279 frames, same Mac,
  same day, both at the render queue's 4 cores): stage 1 (the 4K key) 1.4-1.7x less CPU, stage 1.5 1.5-1.7x less, about 9.9 to 6.5 CPU-seconds a frame in all; the largest stage 1.5 worker 2.2 GB to 1.0-1.2 GB resident, the whole stage 1.5 step 8.7 GB to 3.6-4.7 GB.
- **No more re-keying whole clips to try a setting** (about 6 of 10-21's 8.5 key hours). `calibrate.py` keys 2-3 s
  excerpts at the piece's hardest moments in the quick lane and makes a contact sheet; the excerpt frames are exactly
  the frames the full key will produce there. `keyonce.py` keys each piece once and skips it in every later round.
- **Per green-screen clip the saving is about 3-3.6x**: one full key plus a few minutes of excerpts, at the lower
  per-frame cost, replaces the three full keys RO-24 ran per clip on 10-21. Detail in section 4.
- **The key now stays inside its allowance:** pools of `RENDERQ_CORES` workers (default 4), one OpenCV/BLAS thread
  each. Before, 4-6 workers each started up to 10 OpenCV threads, which is why Phase 1 had to leave the ffmpeg
  `-threads` cap off.

## 1. How identity was proved

1. The approved code, unchanged, was run again on the approved sample (C1730 at 1400.25 s, 279 frames, same plate,
   same watch boxes). Its pale render is byte-identical to the approved file
   (`2091ddc4…`, `approval.json`), so that run's caches ARE the approved key, frame by frame.
2. The new code was run on the same sample and every cache file compared with the approved run's:
   stage 1 cache 279 of 279 frames identical, stage 1.5 cache 279 of 279 identical (and the new stage 1.5 alone, fed the approved stage 1 cache, also 279 of 279).
3. Rendered pale, navy (card + voice) and pink samples: `x pale.mp4` 2091ddc4…, `x navy.mp4` c8bbc948…, `x pink.mp4` 8a3e1299…: the approved files' hashes, byte for byte.
4. The gate scripts are therefore unchanged by construction (identical pixels give identical `mcflicker.py` and
   `measure_r2.py` numbers: 0.686 / 0.677 motion-free flicker, 2.66% dark rim, 0 specks).

**A faster stage 1 was built and rejected.** Running the 4K blurs in OpenCV (float32) made stage 1 1.9x cheaper
instead of 1.6x, but its alpha differed by up to 0.0017 (under half an 8-bit level). After stage 1.5 that grew to 0.009,
and through the encoder it moved `measure_r2.py`'s counts: 3 floating specks (approved 0) and 453 see-through pixels
at the watch (approved 402). `mcflicker.py` still matched (0.686 / 0.677). Under the quality rule that is a fail, so
the blurs stay scipy's. OpenCV's float64 blur also differs from scipy in the last bits (about 1 M of 7.5 M values per
4K frame), so it was rejected too. Only exact changes are kept.

## 2. What changed (all bit-identical; `reference/ds40-claude-r2/`, originals kept in `approved-original/`)

**Stage 1 (`keylib.py`, `stage1_key.py`), CPU per frame 5.1 s to 2.3-3.7 s:**
- the blurs that do not depend on the plate (the colour-difference blur and the three positivity blurs) were computed
  twice per frame (inner key, then outer key with the local plate); now once;
- the local plate's coarse normalised-convolution scales are skipped once every pixel is filled;
- channel min/max/sum and the 2x2 / 4x4 block means are written out elementwise in numpy's own summation order (a
  2-D block mean sums each block row first, a 3-channel one element by element: getting that order wrong was the
  only non-identical value found on the way);
- erosion (L1 distance), hole fill (border-connected background), the watch case closing (25x25 dilate/erode with an
  outside-is-empty border), the 70 px watch zone (L1 distance) use exact OpenCV equivalents of the scipy calls;
- the "looks like screen" test runs on hole pixels only (exact: per-hole fractions of 0/1 values);
- the local plate is upsampled by a separable float64 bilinear equal to `ndi.zoom(order=1)`;
- workers get the decoder's 16-bit words instead of float32 frames (half the bytes through the pipe), one thread each.

**Stage 1.5 (`stage15_temporal.py`), CPU per frame 4.8 s to 3.3 s, largest worker 2.2 GB to 1.0 GB:**
- each DIS optical flow was computed twice (frame i needs i->j and j->i; frame j needs the same two); each worker now
  keys a run of consecutive frames and keeps the window's flows (neighbours 1-2 apart; `FLOW_CACHE`), frames and greys;
- the neighbour warps, confidences and accumulations run only on the edge band plus 2 px (the only pixels they can
  change: off the band alpha is solid or below 0.004, below any speck cap), using point lists for `cv2.remap`
  (same value per pixel as a full map);
- the float64 colour mix is built in row blocks and the watch boxes on a patch (was about 0.2 GB of temporaries);
- source frames are read with `pread` instead of a memory map (resident memory no longer grows with every frame);
- `ONLY=f1,f2,...` re-keys just the failing frames; `MIN_FRAMES` relaxes the 200-frame guard for excerpts;
- cache files are written under a temporary name and renamed (a killed run leaves no half-written frame).

## 3. Measurements (approved sample, 279 frames, M2 Pro 10 cores, render queue heavy slot = 4 cores)

Measured with `/Volumes/Extreme/_edit_work/cheapkey/prof/stagerun.py` (CPU of every process of the step; peak
resident memory of the largest process and of the whole step, sampled every 3 s). The Mac was heavily loaded all
evening (load average 90-400), so wall-clock times are noisy; CPU seconds are the fair comparison.

| step (279 frames, 4 workers) | approved code | new code | |
|---|---|---|---|
| stage 1, CPU per frame, full runs | 5.08 s (1423 s) | 3.74 s (1048 s) | 1.36x |
| stage 1, CPU per frame, interleaved in one process, same 5 frames | 3.96 s | 2.32 s | 1.70x |
| stage 1, numpy peak per frame | 0.92 GB | 0.83 GB | |
| stage 1, largest process / whole step, resident | 1.95 / 8.5 GB | 2.5 / 10.7 GB before the row-block upsample fix (numpy peak above is after it) | |
| stage 1.5, CPU per frame, same input | 4.83 s (1348 s) | 3.27 s (913 s); 2.79 s (778 s) in the gated run | 1.48-1.73x |
| stage 1.5, largest process resident | 2.21 GB | 0.97-1.21 GB | |
| stage 1.5, whole step resident | 8.71 GB | 3.63-4.68 GB | |
| stage 1.5, numpy working memory per worker | about 0.7 GB (single process) | 0.63 GB (0.53 with `FLOW_CACHE=1`) | |
| key total, CPU per frame | 9.93 s | 6.54 s | 1.52x |

Full runs: approved code 20:14-20:43, new code 22:36-22:48 (load average 90-200 for both). The interleaved
measurement (both codes on the same frames, alternating in one process) is the fairest ratio.

Minutes per 30 s clip (900 frames) of 4-core heavy slot, CPU-bound: before 37 min (9.9 CPU-s × 900 / 4 cores); after about 24 min. The quick-lane calibration pass of three 2.5 s excerpts is about 12 min of 2 cores (measured at load average 35; 6-13 min per excerpt under load 100-280).

## 4. Calibrate on excerpts, key once

`calibrate.py` on the approved sample: one low-resolution pass (14-18 s) picks the tracked hold-out (watch boxes,
frames 0-74), the biggest motion peak (frames 105-179) and the next (frames 202-276, which also holds the other two
watch boxes). Each 2.5 s excerpt is keyed with 3 extra frames each side. Final run (exact code, load average about 35): analysis 14 s, excerpts 4.4, 3.8 and 3.8 minutes on 2 quick-lane cores, 12 minutes in all. **All 225 judged excerpt frames (75 per excerpt) are bit-identical to the approved full key's frames**, stage 1 and stage 1.5, so what the editor judges on the sheet is exactly what the one full key will deliver at those moments. Sheet: `/Volumes/Extreme/_edit_work/cheapkey/cal2/sheet.jpg`.

Two seek traps were found and fixed on the way. Frame-time arithmetic does not say where ffmpeg's `-ss` lands. A
seek more than half a frame before a frame makes the constant-rate raw output repeat that frame and shift every
later frame by one (excerpt 2 of the first try). `calibrate.py` now checks each excerpt's first two frames against
the low-resolution pass before keying.

Per-clip cost, a 30 s piece: before, three full keys at 9.9 CPU-s a frame = 7.4 CPU-hours. After, one full key at
6.5 CPU-s plus one or two excerpt passes (243 frames each) = 2.1-2.5 CPU-hours: 3.0-3.6x cheaper.

## 5. Not done, and why

- **Not 3x per frame.** The handoff's other ideas (temporal confidences at half resolution, float16 intermediates,
  one flow inverted for the other direction, a cheaper DIS preset) all change pixels, and the rule keeps only
  exact changes. What is left per frame is scipy's 4K and quarter-resolution blurs (about 1.3 s) and six to eight
  DIS flows (about 1.4 s); neither has an exact faster equivalent here.
- **Under 400 MB per stage-1.5 worker was not reached:** about 0.63 GB of working memory per worker (0.53 GB with
  `FLOW_CACHE=1`, which costs two more flows a frame). Stage 1 works on 4K float32 frames; its largest process is
  about 2 GB resident for both codes (numpy working memory 0.92 GB approved, 0.83 GB new, measured frame by frame).
- **Running recipes are untouched.** DS-44, RO-24, RO-28 and the shorts copy (`.claude/skills/shorts/reference/
  ds40-greenscreen/`) run their own copies of the old code; new keys copy the reference folder.
