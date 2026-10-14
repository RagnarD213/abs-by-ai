# RA-05 "How AI Can Get You REAL Six Pack Abs": round 1 (2026-10-13)

A 9:16 ad cut from portrait roll C1664 (205 to 300 s) on the RA-04 recipe. Work dir: `/Volumes/Extreme/_edit_work/ra05/`.
Only the files that differ from `../ra04/` are here; everything else (`s01_env.py`, `s02_tx.sh`, `s03_edl.py`,
`s04_track.py`, `s07_captions.py`, `s08_audio.py`, `s09_align.py`) is RA-04's, re-pointed at this folder.

## Order

| # | command | makes |
|---|---|---|
| 1 | `bash s02_tx.sh` (span `-ss 188 -t 116`, `OFF = 188.0`), then `python3 s02b_patch.py` | word list with four times and two words corrected |
| 2 | `HEAD_SRC=208.24 python3 s03_edl.py` | `cut.json` (54.15 s of talk). `edl_spec_full.json` keeps the sentence cut for length |
| 3 | `r1_chain_a.sh` | `mix.wav`, `words_aligned.json`, `framing.json` |
| 4 | `python3 s31_bake.py 1.20 1.60`, `python3 s30_looks.py` | the three RA-14 looks re-baked for this roll, comparison sheets in `look/` |
| 5 | `python3 s05_plan05.py` | `beats.json` |
| 6 | `r1_chain_c.sh` | `gfx05.py`, `s06_inserts05.py`, captions, `s10_render05.py`, the draft |
| 7 | `r1_chain_d.sh` | the first 30 seconds, `page05.py --media` |

## What this ad taught

1. **Check a clip's first frames against the banned screens, not its description.** B0049's "Meet the new you" before/after
   screen runs to about 27.6 s; a card that starts at 27.3 s shows it for 0.3 s. Start the result at 28.0 s.
2. **A sibling ad's LUT is not a look.** RA-14's three LUTs were baked for C1667, where his face sat 1.5 stops under. On
   C1664 the same files put his face at 104 and 122 against 81 and 96. Carry the LOOK across (face brightness, tone curve,
   skin hue), re-bake the exposure per roll (`s31_bake.py`), and measure on this roll's frames before rendering.
3. **Carry a framing pick across rolls by body landmark** (pixels under the waistband for the close and wide bottoms), not
   by crop size or head heights: head-height conversion gave crops 14 % larger than the landmark conversion here.
4. **The automatic head edge can find the previous take.** A false start ended one second before the kept take and its tail
   crossed the onset threshold. Print the envelope in 40 ms steps and pin the edge (`HEAD_SRC`).
5. **`s10_render05.py` seeks instead of decoding from frame 0** (RA-14 round 2 lesson 4, wired into the full render): the
   decode is the 95 s this ad uses, not five minutes of roll.
6. **Count the script before promising a length.** 231 words at 226 wpm is 61.3 s airtight. The job doc's 0:59 limit meant
   a line had to go: cut the sentence that sells nothing, show the alternative, and keep the full spec on disk.
7. **Pick B-roll from the same shoot first.** B0435 (physique poses, same pool, same light) needed a small skin match;
   B0438 (another day, overhead sun, hands over his abs) was built, looked at and dropped.
8. **A frame-lock audio pass can stall on a saturated machine** (ffmpeg at 0 % CPU for 34 minutes at load 63). Do not let a
   chain wait on it silently: give the waiter a timeout, and mux the review sample with the unlocked mix.

## Open for the final round

See `Handoffs/handoff-20261013-ra05-round2-after-dan-review.md`, "Next action", item 5.
