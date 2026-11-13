# `softblue-sl21/`: SL-21 What To Cut shorts (R1, 2026-11-13)

Three Shorts from RO-20B "What To Cut To Afford Getting In Shape" (Claude film, roll C1511, 8/3 kitchen shoot), built from
`softblue-sl20/` (read its README and `softblue-sl18/README.md` first). **Copy this folder, not sl20, for the next batch from a Claude
long-form that has a graphics-free `base.mp4`:** it carries two frame-mapping fixes and the caption controls below. Work folder
`~/Projects/_edit_work/SL-21/` (internal drive). Order: copy `base.mp4`, `layout.json`, `plan.json` into `src/` -> `snap.py` ->
`scan.py` -> `batch.py audio, words` -> `prep_clips.py` -> `clipsheet.py` (look, set fx) -> `batch.py plan, track, plan, cues, gfx,
proof, render` -> `deliver.py copy` -> `runwatch.sh S` -> fresh `ra-reviewer` per Short (`REVIEW-BRIEF.md`) -> `rungate.sh S` ->
`shorts_md.py` -> `page_sl21.py` -> `_shared/review_server.py`. Three review rounds (1, 1b, 1c; D a fourth for captions only).

## What is different from SL-20
- **Only real camera changes are picture cuts.** In the RO-20B `layout.json` most presenter segment boundaries continue the same crop of
  the same take (no visible cut), and segment `o0` is already the master's output frame (no part offset). `scan.py` checks every listed
  boundary against a frame-difference scan of `base.mp4`; `silence.json` keeps only the ones the scan sees (9 of 29 here). Treating the
  rest as cuts would have put size steps at arbitrary moments. Seek note: the scan's first frame is `ceil(a0 * FPS)`, not `round`.
- **Frame mapping (two bugs fixed in `batch.py`, both present in sl18/sl20):** (1) `Short.rng` used `ceil(at * FPS)`: a cut time is a
  whole frame rounded to 3 decimals (471.004 s = frame 14116.004), so a talking shot that starts ON a film camera cut began one frame
  late: its first frame showed twice and one source frame was skipped (reviewer E round 1b, 22.39 and 37.04). Now `round()`. (2) `fidx`
  switched to +0.5 for phases outside 0.1-0.9; a phase of 0.907 then ran one frame ahead and held the shot's LAST frame against the
  clamp. Now 0.03-0.97. Verify before rendering: every shot's source indices must step by exactly 1 (the check is in the session's
  build log; add it to `proof` if this recipe is reused).
- **Caption controls in `plans.TEXT`:** ` / ` forces a caption break before the next word; ` + ` keeps the next word in the caption
  being built (no automatic 4-word / 24-letter break); `a_b{a b}` is two words that stay together as one token. Reviewers failed every
  Short twice on phrase splits ("great / shape", "two / or three", "until" or "if" stranded at a line end, "Dan. I don't have",
  "Now I know some / of you guys", "You can enjoy those / vacations"). Read every caption in order as a viewer before the first
  render and set the breaks by hand; the automatic chunker is only a starting point. Also now automatic: a camera change between two
  talking shots counts as a cut for caption timing; short captions never merge across a picture cut or a forced break; "going to"
  moves together; "if" never ends a line. `deliver.flat_words` splits joined tokens back for the gate plan.
- **Captions over a clip's subject move** (`SHOTS[S][idx] = dict(cap=y)`): the card reader, cooks' hands, noodles, measuring spoon (top,
  y 400 = 90 px under the title band) and the pills (y 560, in the felt). Check every clip: is what the clip shows inside canvas
  y 1412-1600? A caption that would be two lines does not fit the floor under a full-body clip (pull-ups): leave it standard.
- **25 fps stock is conformed frame for frame** (`prep_clips.py`: `setpts=N/(30000/1001)/TB`, 1.2x speed, no repeated frames; the fps
  filter repeats every fifth frame). **A file that says 29.97 can still be 25 fps footage with every sixth frame repeated** (Pexels
  7015435, the pancakes): scan every copied clip for near-zero frame differences; `prep_clips.dedup_select` measures each frame and
  drops repeats by index (mpdecimate left one in).
- **Key-point bars sit only on the film's WIDE shots:** on its 1.3x close shots his chin reaches canvas y 1175-1300 (track.json face
  bottoms 580-664 px), under the bar's top at 1130. Measure `fy1` per shot before placing a bar.
- **Cuts into and out of clips go in measured pauses** (10 ms levels), not where the film cut: several film cuts sit inside a word, which
  is fine under the film's lower thirds but strands a caption across the cut in a Short.
- **Opening clip:** the film's beach clip opens at ground level on one young sunbather; under the title "... Until You're Ripped" a
  reviewer flagged it. The aerial stretch of the same clip is the opener. Look at who is centred under the title before choosing.
- **Stock grades:** a dim, flat stock clip (buffet, luma 83 against 124-135 on Dan) gets curves + a little saturation; the October 23
  gym B-roll reads about 35 points darker on his skin than the kitchen and takes a mid lift.
- `deliver.py`: no 540p copy (review default is the 1080p file, AGENTS.md 2026-11-02); the negative-events text is per Short
  (`plans.NEG`), never fixed wording; the banned-screens recording now lives on the Seagate
  (`/Volumes/Expansion/_internal-offload-20261031/Media longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4`).

## Gate
36-37 of 39 on each Short: `framing:hair_top` and `framing:headroom` fail on every Short from roll C1511 (the camera framed his hair at
the top edge; the crop starts at source row 0), the same two the approved film and SL-20 fail. They need Dan's acceptance, never a
changed bound.
