# `softblue-sl17/`: SL-17 Top 1 Percent shorts (R1, 2026-10-20/21)

The SL-15 batch renderer (`softblue-sl15/`, `softblue-sl07/`: read their READMEs first) adapted to RO-26 "I'm 41. My Life Is
Top 1%. How I Did It.", a Codex-built studio film cut from ONE 4K roll (C1768, the 10/15 shoot). Work folder:
`/Volumes/Extreme/_edit_work/SL-17/` (these are copies kept in git; run from there). Order: `snap.py` -> `fitgrade.py` (once)
-> `batch.py audio, words, plan, track, plan, cues, gfx, proof, render` -> `deliver.py copy` -> `hairv.py S FILE` -> `scan.py S`
-> `runwatch.sh S` -> `junk.py FILE` -> independent reviewer (judge + review, `review/REVIEWER_BRIEF.md`) -> `rungate.sh S`.
Heavy steps queue in the render queue; run analysis steps with `renderq.py run --light --group SL-17 -- ...`.

## What is different from SL-15

- **The film's map is the Codex `cut_map.json`** (`src_in/src_out/out_in/out_out` per cut), copied to `ro26_cut_map.json`.
  Raw lav through it and the film's voice chain matched the master at film 90/100/110 s: lag 0.02 ms, gain -0.04 dB, r 0.9997.
- **4K source, sharper than the film.** `batch.cam` decodes the raw 4K strip at 2x (1920-space coordinates, 4K pixels) and
  `Short.picture` crops 2x and DOWNscales with INTER_AREA to the 1080x1610 picture.
- **The film's look is MEASURED, not copied from its recipe.** Recipe grade B (`eq=contrast=1.12:gamma=1.15:saturation=1.14:
  brightness=0.012`) on the raw read 4-5 levels brighter and greener than the delivered master on aligned frames (a later step of
  the Codex pipeline shifted most of the film; only its R5-patched pillar-4 seconds match grade B alone). `fitgrade.py` fits one
  tone curve per channel after grade B from 8 aligned frame pairs (binned medians, blurred), tests on 4 held-out frames
  (mae 5.0 -> 1.95 of 255), and writes the ffmpeg `curves` filter to `curves.json`. Check any recipe grade against the master
  before trusting it.
- **A line the film dropped can be restored** (`plans.VIRT`): treat the raw lav with the film's FIXED chain (its
  `voice_chain.json` `voice` string + measured `gain_db` + the same `alimiter` and limiter delay), null-test it against the master
  on a range the film did use (r 0.9997 here), and park it in `master_audio_ext.wav` at a virtual film time past the end;
  `A_pieces` maps the virtual time to the raw roll. Keep the speaker's own pauses and breaths around it (reviewer A2 caught a
  0.08 s pause and a cut mid-breath that made the line sound spliced in). A line removed in a script pass may still be one the
  speaker kept: check the as-delivered script doc and whether he filmed it.
- **Windows tighter than SL-15: 678x1010 and 580x865** (1920 space). The 10/15 studio camera frames Dan small; at 724x1080 his
  hair-to-chin was 25.9-26.9 % of the window and the gate's `framing:no_wide_level` failed (min 27 %).

## What this round learned (three reviewers, all DOES NOT SHIP the first time)

- **Hair clearance covers B-roll of Dan too** (`hairv.py`: talking shots plus `DANCLIPS`). The library kitchen clip B0441 and
  Dan's Instagram promotion clip both have his hair at the top row of the SOURCE: no crop fixes that, pick another clip. The
  every-frame dark-pixel edge test is calibrated on the studio backdrop only (outdoor trees read as hair); two-person clips need a
  by-eye strip of Dan's head.
- **A crop position must be checked on the rendered frame**: `fx` 0.88 on B0460 showed an empty pool deck (Dan stands at x 0.49).
- **Key points echo easily.** Three of six first-draft bars repeated the words under them; distil the idea (the 5-10-15 ladder,
  "Short Breaks Are Fine, Quitting Isn't"). Give line 2 at least 1.5 s of full visibility, and keep line 1 short enough not to
  wrap (a wrapped "Grow From 5 To 15" revealed "15" before "From 5 To").
- **Eyebrows stay in CAPITALS** (Dan 2026-10-20, GRAPHICS-STANDARDS "Eyebrow exception"): the title band's eyebrow ("NUTRITION")
  and the bar's "KEY POINT" (the lower-third build uppercases it). Main points, headings and bar lines are title case.
- **Audio joins are crossfades, not fade-out/fade-in** (`cmd_audio`): 15 ms of the outgoing take's audio past its out point under
  15 ms of the incoming take's pre-roll, equal power, no timing change. The old 15 ms fades left 20-50 ms holes at -75 to -79 dB that
  blind listening flagged as "rushed" or "click" (reviewers A3, D2). Keep the speaker's own sentence pause (~0.3 s) at a join and
  end a piece in the measured floor, not inside a word's decay; a restored raw line starts exactly where the film's take left off.
- **Check bar line wraps on the RENDERED frame**: `lt_scenes` meta said one line for parts that the browser wrapped ("Short Breaks
  Are Fine,", "BJJ, Muay Thai Or Judo:") while longer-measuring lines fitted. Keep lines short and look at a settled frame.
- **Line 2 of a bar: at least 1.5 s fully readable** (bar `b` about 1.9 s after line 2 lands), ending before the next picture cut,
  and never carried onto a clip where a face sits at the bar's height (A's AI fork clip).
- **Captions:** a cue under 0.4 s that does not end a sentence merges into the next; gaps under 0.1 s are bridged (one-frame blinks).
- **Shot edges:** look at the last 0.3 s of every talking shot and the first frames after a join (a look-up at 3.4 s, a blink with
  the tongue showing at a join): move the cover or the in point.
- **A horizontal exercise (ab wheel rollout) is a `span` card** the width of the move; a vertical fill crop cut his head and feet.
- **Ambiguous words: two Gemini passes disagreed** ("I'd ... cost" vs "I ... costs"); captions follow the filmed script when the
  audio is genuinely ambiguous; when every listener agrees ("in relationships"), the caption follows the audio.
- **The Extreme drive filled to 0 bytes mid-round** (other sessions): delete your own `build/*/trk` frame dumps once
  `track.json` exists; keep frame dumps in `/private/tmp`.

## Title band descender fix (2026-10-22)

`lib.band()` now draws the title at y 86 with a 96 px line step (was 96 / 100). With title-case titles, a second line with g, j, p, q or y at 88 px ran its descenders to row 312, cut by the glass line at 309 and the picture at 310 (SL-17 reviewer B5; 11 delivered Shorts were affected, `Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). The lowest glyph row is now 298. `batch.py gfx|proof|render` runs `_shared/softblue_titlecheck.py` on every TITLE first and stops if any lowest white row is 299 or lower down. Check a batch by hand: `python3 .claude/skills/_shared/softblue_titlecheck.py titles <batch dir>`.
## Round 2 (Dan, 2026-10-22): centre on the whole body, not the face

- **A wide-armed move (jump rope) is centred on the ARM SPAN, not the face.** B0448 at `fx` 0.5 had his face centred, but his
  hands' midpoint sat at x 0.45: the left hand touched the edge and Dan saw "a lot of space near my right hand". `fx` 0.4725
  (49 px) balanced the hands; his head then sits about 40 px right of centre, which a fixed crop cannot avoid when the span is
  nearly the full 1080 px.
- **A `span` card is measured from the person mask's extremes over the whole clip**: the wheel at full extension (min x 0.174)
  on the LEFT edge, the shoes (max x 0.84) at or just past the RIGHT edge. B0030 R1 `span` 0.30-0.98 cut the wheel and his head
  off the left with empty space past the shoes; R2 uses 0.17-0.83.
- Check a cover crop on the rendered frames across the clip, not one still: show Dan a before/after side-by-side of the changed
  seconds on a later-round page.
