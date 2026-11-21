# RA-06 "What's The Best Ab Exercise?": round 1 (2026-10-14)

Round 3 (AI motion from approved frames, brighter split screen, centred close, the full 9:16): `round3/README.md`.

A 9:16 ad cut from portrait roll C1664 (313 to 369 s) on the RA-05 recipe, with Dan's RA-14 picks applied (C2 colour,
pair 2 shot sizes, bass lift) and the land-then-hold vertical crop wired into the render. Work dir:
`/Volumes/Extreme/_edit_work/ra06/`. Only files that differ from `../ra05/` and `../ra04/` are here.

## Order

| # | command | makes |
|---|---|---|
| 1 | `node tx/replicate_words.js` on two pieces (309-340.4, 340.2-373), joined in the take-break pause; `python3 s02b_patch.py` | `tx/c1664.whisper.json`, word edges re-timed from the envelope |
| 2 | `HEAD_SRC=313.36 python3 s03_edl.py` | `cut.json`: 45.41 s of talk, 13 pause cuts, one take seam at 19.95 s |
| 3 | `r1_chain_a.sh` | `mix.wav` (fitted tone + bass lift), `mix_nobass.wav`, `words_aligned.json`, `framing.json` |
| 4 | `python3 s05_plan06.py`, `python3 s04b_holdstart.py beats.json` | `beats.json`, a head sample on every hold's first and last frame |
| 5 | `r1_chain_c.sh` | `gfx06.py`, `s06_split.py`, `s06_inserts06.py`, captions, `s10_render06.py`, `draft_9x16.mp4` |
| 6 | `python3 s30_looks06.py` | colour, shot-size and voice option sheets for the outdoor rule |
| 7 | `r1_chain_d.sh` (or `r1_chain_e.sh` to re-mux first) | review copies, `page06.py --media`, audio gate, `junk.py`, `s25_hard.py` |

## What this ad taught

1. **Replicate's large-v3 returns CONTIGUOUS word times** (each word ends where the next starts), so every pause hides
   inside a word and the 60 % overlap rule can drop real words when a pause is cut. `s02b_patch.py` re-times each word edge
   from the silence runs in the 5 ms envelope. It also skipped the first word of a take ("That's" after the take break).
2. **Look at what he does after the last word.** On this take his hands rise 0.7 s after "started"; the hold is 0.30 s,
   not RA-05's 0.85. The RA-05 planner carried its OWN `END_HOLD = 0.85`; it now reads `ra01lib.END_HOLD`.
3. **Land-then-hold in the render** (`s10_render06.py`): per hold, `landing.vertical_dense` on the 5/s track plus the
   hold-start samples, turned into a piecewise-linear `crop` x expression in `n` (Douglas-Peucker knots, 0.6 px) with
   `exact=1`. Commas inside the quoted expression need no backslash. Frame-snapped hold edges against unsnapped cut pieces
   leave sub-millisecond slivers; drop spans under half a frame or the expression gets an empty array.
4. **`-shortest` on the draft mux dropped the last 2 frames** (AAC ends a hair early). Mux with `-af apad -t <total>`.
5. **The audio gate on a muxed draft needs `--untreated mix.wav.audio_untreated.json`**, or its artifacts and do-no-harm
   rows fail as not measured.
6. **The split-screen cue** (three exercises stacked, 16:9 panels on the Soft Blue field, a name chip each) is
   `s06_split.py`. Measure crops in the source's own pixels: a contact sheet shown scaled put the first toe-touch crop
   entirely off Dan. His "spiderman plank" is the plank up to a push-up and back (short4_spiderman-planks), C1683 135.5 s.
7. RA-05's inserts script ran its analysis block whenever no card list was given; guard optional blocks with
   `name in by`.
8. **In a stacked split screen the caption band (ink ~1420-1470 on 1080x1920) lands on the BOTTOM panel.** Put the panel
   there whose subject is upright and whose face can sit above the band (the vacuum, crop 2560x1440 at y 270), never a rep
   whose top position rises into it (toe touches) or a face. Check with the band drawn on the panel frames.
9. **A trailing-off line needs a phrase-sized ride, not a sentence-sized one.** "make your abs real" was 5 dB under its
   neighbours; +3 dB over the whole sentence left it there, because the global finish re-normalises. `s08_audio.py` `RIDE`
   (t0:t1:dB, stacked, 80 ms ramps) on the cut before the shared chain; measure each sentence's LUFS on the muxed file after.
10. **The caption aligner reads the word list inside `cut.json`, not the transcript.** A caption text fix in the transcript
    needs `s03_edl.py` re-run (the cut stays identical) before `s09_align.py`.
