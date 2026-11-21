# RA-05 round 2 (2026-10-14): every line kept, the ad sped up 1.06x, frames for the couch clip

Work dir `/Volumes/Extreme/_edit_work/ra05/round2/` (a copy of round 1's inputs; round 1's files are untouched). Review page
http://127.0.0.1:8808/ (`review/`). These files differ from `../` (round 1) and `../../ra04/`; everything else is round 1's.

## Order (run in the work dir)

| # | command | makes |
|---|---|---|
| 1 | `cp edl_spec_full.json edl_spec.json; HEAD_SRC=208.24 python3 s03_edl.py` | `cut.json` at normal speed: 60.96 s, 17 pause cuts |
| 2 | `python3 s03s_speed.py` | keeps it as `cut_tight.json`, rewrites `cut.json` in FILM time (/ `ra01lib.SPEED` = 1.06) |
| 3 | `EQ="<round 1 fitted eq>,equalizer=f=120:t=q:w=0.8:g=+3.0" STRETCH=rb BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py` | `mix.wav`: Rubber Band 1.06x, bass-lift voice |
| 4 | `python3 s09_align.py`, `python3 s04_track.py` | caption timings on the sped mix; head track in film time |
| 5 | `python3 s05_plan05.py` | `beats.json`: open, couch (pending), lock, A1, tour, scan, pose |
| 6 | `python3 gfx05.py` | lower thirds, CTA, the HyperFrames analysis card A1, plates for open / tour / scan |
| 7 | `python3 s06_inserts05.py open scan A1 couch lock tour pose`, `python3 s07_captions.py 9x16` | cards, captions |
| 8 | `python3 s10_render05.py 9x16`, then step 3 again with `LOCK=picture_9x16.mp4`, mux `draft_9x16.mp4` | picture (speed-aware), frame-locked mix |
| 9 | `python3 page_r2.py --media`, `review_server.py 8808 review` | the round 2 page |

Rubber Band runs from a venv: `python3 -m venv ~/.cache/absbyai/rbvenv && ~/.cache/absbyai/rbvenv/bin/pip install pylibrb numpy`.

## What this round taught

1. **A speed-up is one factor in one place, applied to film time.** `ra01lib.SPEED`; `cut.json` carries `speed` and film times;
   every reader that maps film time to source multiplies by it (`s04_track`, `s04b_holdstart`, `s10_render05`). Audio: cut at
   normal speed, stretch, THEN the voice chain (the bed is not sped). Picture: each hold takes `(t - t_in) * SPEED` of source,
   `setpts=PTS/SPEED`, then `fps=30000/1001`. The end hold plays at normal speed (its own branch after the sped spans).
2. **Stretch with Rubber Band (R3 "finer", formants kept), not ffmpeg `atempo`.** On the same mix Rubber Band measured less
   processing damage (flux 0.086 against 0.093, swirl 0.764 against 0.808) and passed every audio-gate row; `atempo` failed
   `artifacts` and `do_no_harm`. Its output is time-exact (-5 ms against the ideal by envelope cross-correlation).
3. **A blind AI listener cannot judge stretch methods.** Five trials gave three different stretches the SAME scores and the same
   fault sentence word for word; it only detected that a clip was faster than the normal-speed control beside it. On a single
   listen with no control it said a viewer would not notice 1.06x. Settle the method on measurements.
4. **The splice crossfade was eating 6 ms per splice** (round 1: 0.10 s by the end, voice ahead of the lips). `s08_audio.py` now
   borrows 3 ms either side of each cut, so the voice is exactly as long as the pieces.
5. **Check an AI reviewer's sync claim by source-frame matching, not by mouth tracking.** Gemini said the voice led by 0.1 s;
   mouth-versus-level correlation was too weak to decide (0.17 to 0.39). Matching draft frames against graded source frames
   showed the picture on the expected frame (0 to +1), so sync is inside one frame (`synccheck.py` is the weak method, kept
   for the record).
6. **The B0049 opening, read frame by frame:** crop screen 0-2.5 s (never), photo in place 3.0 s, Peak tapped 7.35 s, Generate
   pressed 7.90 s, loading 8.0-24.4 s (the page is still scrolling until about 9.6 s), "Meet the new you" 25.0-27.6 s (never),
   result 28.0 s on. `s06_open.py` holds the segment table; the plate's chip has `spans`, so AI-GENERATED appears only with
   the result, not over the man's real before photo.
7. **Derive the END frame from the START frame** (`--image`), then zoom on cloth: the first END take had an embossed swirl
   texture on the sweatpants that only shows at full size. One retake naming the fabric fixed it.
