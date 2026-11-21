# RO-05 Fable-handoff recut (2026-09-24): the Muhammad-style long-form pipeline and its traps

Recipe (code, EDLs, LUTs, framing): `/Volumes/Extreme/_edit_work/ro05-fable/recipe/` and the delivery folder's `recipe-RO-05/`.
Built from scratch after Dan rejected Claude's r10 (VIDEO-RULES "RO-05 rejection"). Status: see `Handoffs/video-editing/00-MASTER.md`.

## Order that worked (style before length)
1. Grade 6 stills side by side with Muhammad Ad 6 / Ad 1 / approved C1652 at their measured numbers (`tools/measure.py`, `stills.py`).
2. Graphics + transitions board: his frame beside ours for every component (`tools/board.py`), sizes corrected from the board.
3. One 60-90 s sample + moving B-roll previews in ONE packet to Dan, then the full cut on the same code (`tools/build.py EDL OUT`).

## Grade (per roll, `tools/fitgrade.py`)
Luma quantile match toward the mean of Ad 6 + C1652 (targets in the file), 30 % per-channel contrast, chroma gain 1.38 but
orange hues (skin, kitchen wood) held at 1.12. A flat 1.35 gain everywhere turned skin orange. One 33-point .cube per roll,
applied in ffmpeg as `rgb48le -> lut3d`. Result median luma 0.28 / sat 0.33 (Ad 6 0.25-0.29 / 0.36-0.38).

## Muhammad components (`tools/orglib.py`, from the ab-wheel reproduction, plus `stack_panel_timed`)
- Bloom flash (measured off his Ab Wheel master at 12.5 s and 39.2 s): one full-white frame, blue-fringed leak from the right,
  double pulse, SILENT, screen-blended. A join-hiding variant puts the white frame ON the cut.
- Glow card: hard cut in; whip-pan between two items inside the card (6 frames, outgoing slides left, incoming follows,
  heavy horizontal blur). Never whip into an empty card; leave a card with a flash.
- Pill sizes that match his frames: white pill 54/46, olive key-point 52/46, chip 64, chevrons 1.25x at (1575,100).

## Traps found (each cost a render)
- **`/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3` is a RAP SONG WITH LYRICS** ("I turn my life into a banger"),
  audible whenever the bed swells. It was the RO-05 r10 bed and passed three reviews before a Whisper pass on the bed caught it.
  Never use it. Before any bed goes in: transcribe it (`whisper small`, no_speech_threshold 0.5) and require zero segments.
  `acoustic_bg.mp3` (Pixabay, cleared, used by the website video) transcribes to zero segments and is the RO-05 bed now.
- **The pantry-door poster of Dan is a second "person"** to Vision's person mask: head measurements must use the LARGEST
  connected component (`tools/hair.py`), or every punch looks unsafe.
- **Top-anchored punches** (crop top = source top) can never remove hair the camera captured; horizontal centre fixed per piece.
- **A piece continuing the same take at the same level must keep the same crop centre**, or the cut is a sideways jump
  (review r1 defects 1-2). `build.layout` enforces it.
- **Lines longer than a B-roll clip**: end the clip and return to Dan for the rest of the line (`card`/`cover` in the EDL);
  laying the whole line over a short clip either overlaps the next line or freezes/overruns the clip.
- **A stack panel continued across pieces must merge into one overlay** (look back for the last STACK, not the last graphic),
  or it re-fades at every cut.
- **Handheld operator footage hides junk with no audio signature**: whips, tilts to the board while Dan talks, headless
  openings. Round-2 review found five. Check every piece's first and last second and every mid-line camera move; use the
  synced GoPro counter angle (offsets `/Volumes/Extreme/_edit_work/ro05/sync/offsets.json`, crop 1280x720 at 320,0) for the
  same moment, or start the next silent speed-up early with the line running over it.
- **Take maps drop content**: reading the rolls' words around every range found three dropped lines of Dan's reasoning
  (testosterone, "any greens", the sharp-knife tip).
- `audio_gate.py` on a re-encoded master needs `--untreated <chain's audio_untreated.json>`.
- Never run two builds into one output directory: the first build's audio step read a picture the second was rewriting.
