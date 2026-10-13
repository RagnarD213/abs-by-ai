# RA-04 "Top 3 Tips For Getting Abs": the first 8/28 raw ad in Soft Blue Light (round 1, 2026-10-13)

A 9:16 ad cut from portrait roll C1664 with the approved RA-01 recipe (cut, grade, voice chain, hair-anchored
FAR/NEAR crops, captions) and Soft Blue Light graphics through the shared HyperFrames templates. Work dir:
`/Volumes/Extreme/_edit_work/ra04/`. Start the next 8/28 raw ad (RA-02, RA-05 ... RA-16) from this folder, not from RA-01.

## Order

| # | command | makes |
|---|---|---|
| 1 | `python3 s01_env.py` | `lav.wav`, `env.json` (after `pick_lav.py` wrote the roll's `audio_source.json`) |
| 2 | `bash s02_tx.sh` | `tx/<roll>.whisper.json` (chunked medium.en), orphan and repeat scans. Set `-ss`/`-t`/`OFF` to the ad's span |
| 3 | `python3 s03_edl.py` | `cut.json` from `edl_spec.json` (take spans by phrase), airtight pauses |
| 4 | `BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py`, `python3 s09_align.py` | `mix.wav`, `words_aligned.json` |
| 5 | `python3 s04_track.py` | `framing.json` (slow: one 4K seek per sample) |
| 6 | `python3 s05_plan04.py` | `beats.json`: cards, Dan holds and levels, lower thirds, CTA |
| 7 | `python3 gfx04.py` | `hf9/`: lower thirds + CTA (`manifest.json`) and media-card plates (`plates.json`) via `hyperframes/vertical.py` |
| 8 | `python3 s06_inserts04.py` | `cards_9x16/<name>.mp4`, each exactly its frame count |
| 9 | `python3 s07_captions.py 9x16` | `cap_9x16/captions.mov` |
| 10 | `python3 s10_render04.py 9x16` | Dan segments, concat, shared Compositor (glass over footage), captions on top |
| 11 | `LOCK=picture_9x16.mp4 ... python3 s08_audio.py`, mux | the mix locked to the picture length, `draft_9x16.mp4` |
| 12 | `python3 page04.py --media` | `round1/index.html` + stills + context clips (`page_notes.json` holds the copy) |

`r1_chain_a.sh` (4-5) and `r1_chain_c.sh` (3-12) are the chains as run, each behind `capwait4.sh` (two-build cap).

## What this ad taught (keep for the other fifteen)

1. **A pause splice inside a same-size shot is a jump cut.** `s05_plan04.py` puts a level change ON every splice that
   no card covers and asserts none is left bare. "Number one / two / three," became 0.6 s punch-ins, the same on all three tips.
2. **Card and graphic edges snap to the nearest splice** (`snap_to(t, SPL)`), so a cut and a card never land a few frames apart.
3. **Phone cards end above the caption line.** A phone that ran down behind the captions put white words on white app
   screens and a caption across the result picture's abs. `gfx04.py` passes `max_w` so every hole (and its chip) ends by y 1376.
4. **Whisper can give a word zero length** ("Whatever", 172.40-172.40) and the 60 % overlap rule then drops it from the
   captions while the audio still says it. `s03_edl.py` keeps a zero-length word that sits inside the range.
5. **RA-01's caption fix map is per ad.** It rewrote "app" to "abs" ("the Abs by AI abs"). `s09_align.py` now carries no map,
   joins "absbyai" + ".com" into `AbsByAI.com` and cases the brand `Abs By AI`.
6. **The tail guard tests where the silence ENDS.** The silence after the last word starts inside Whisper's last word, so
   "s0 >= last word end" let a pause cut through and made a splice in the end hold.
7. **Length is tight on these scripts** (215 words at 222 wpm): 58.06 s of talk leaves 0.85 s of end hold under 0:59.
8. **The RA-01 grade (1.15x LUT, saturation 1.25) transfers to C1664** (checked side by side with C1663: same set and light).
9. **The fitted voice EQ already lifts the lows to the reference** (+3.8 dB at 110 Hz on this lav), so the 2026-10-12 bass
   standard is offered as an A/B (`mixB.wav`, `--eq "<fitted>,equalizer=f=120:t=q:w=0.8:g=+3.0"`), not stacked blind.
10. **`capwait` can wait 30 to 40 minutes** when three sessions are rendering. Launch chains in the background and let the
    task notification bring the session back; do not poll.
11. **The analysis card takes Soft Blue colours by patching module globals** (`AC.LIME`, `AC.OLIVE`, `AC.PLAN_GREEN`,
    `cardlib.field`) in `s06_inserts04.py`; `ANALYSIS=olive` renders the RA-01 colours. If Dan picks blue, move the
    palette switch into `adkit/analysis_card.py` as an argument.

12. **The app recording B0049 shows the banned before/after screen ("Meet the new you") until about 27.6 s.** Round 1 started
    the result card at 27.3 s, so the banned screen was on screen for the card's first 0.3 s (0:15.3 in the round 1 draft).
    Start the result at 28.0 s (fixed in `s06_inserts04.py`) and look at the first five frames of every app card.

## Open for the final round

Land-then-hold centring is not wired in (crops are fixed per hold, the RA-01 method); measure with `cut/landing.py
motion_stats` and switch if any hold drifts past 3.3 % of the crop width. The 16:9, the edit sheet, the delivery and
audio gates, the watch pass and the independent review all belong to the round that builds the full film.
