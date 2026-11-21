# RO-24 round 2 recipe (Celebrity Ozempic, 10/15 roll C1726, 16:9 green screen)

Dan, 2026-10-21: use the approved house key (Claude's DS-40 Bill Maher R2, `_shared/chroma-key/reference/ds40-claude-r2/`), warm colour,
voice A (Bill Maher voice + 3 dB at 120 Hz). Working state and how to resume: `STATE.md` (copy of the work folder's HOLD.md).

- `ds40key/`: the approved DS-40 R2 key ported to 16:9 without changing its maths: plate per stretch of the take (`plate16.py`),
  4K key inside a per-range box around Dan (`box16.py`, `stage1_16.py`, resumable), output scale 0.75 (2880x1620: Dan's features land
  ~1.1x DS-40's output size, so the approved px settings carry over), the approved `stage15_temporal.py` unchanged except RIM=4
  (measured on the fast-hands stretch: dark rim 8.0 % at RIM 2, 5.8 % at 3, 4.4 % at 4; round 1's key 5.3 %), the approved stage 2
  despeckle/haze clip (`write16.py`, FFV1 plate + head geometry), check renders and the two approved measures ported (`render16.py`,
  `measure16.py`, `mcflicker16.py`). Speed on a busy Mac: about 5 s a frame per lane end to end.
- `edl_film.py`: whole-film timeline from round 1's take list: restarts cut (Gemini listen + lav envelope), pauses over 0.85 s kept at
  0.45 s, join fixes from the seam scan, W/T switch at every cut, round 1's hook cuts kept. `pic_edl.py`: picture EDL (take 4 split for
  its two key ranges; S framing = Dan shifted +519 px under the two left-third side cards).
- `voice_cut.py`: joins are now 40 ms equal-power crossfades (round 1 faded each side to zero: a 30 ms hole in the room tone that
  listeners heard as a click or a cut breath). Verify joins by the level at the cut instant, not only by a model listen (it flipped
  verdicts between runs on unchanged audio).
- `assemble16.py` (+ S framing), `comp16.py` (+ the approved light wrap), `compare_r2.py` (round 1 vs round 2 key), `ctx_r2.py`
  (context clips window by window), `broll24.py` (B-roll inserts with the AI chip), `chain_r2fm.sh` (first minute + checks).
