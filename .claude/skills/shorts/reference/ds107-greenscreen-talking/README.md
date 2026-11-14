# DS-107 Metabolism Not The Reason SFC R1: a dedicated green-screen TALKING Short (not a reaction)

"Your Metabolism Is Not The Reason You're Fat" (B08), 11/13 green screen, roll C1908 (portrait, full body, no laptop, white
tank, glasses). Built on the M2 (two-Mac routing proof). Work folder `/Volumes/Extreme/_edit_work/DS-107/r1/` (recipe/, key/,
src/, main/, review/). Built from the DS-41 Kevin James recipe with the reaction parts removed. Use this, not the R5 reaction
reference, for any 11/13 talking Short (DS-106 sardines, B10, B14 ...).

Format: Soft Blue shorts standard. Title band y 0-310 for the whole Short (SL-21 `lib.band` geometry, laid over every frame
LAST, so a raised finger goes under it); picture area 1080 x 1610 under it. Dan keyed (house key, 0.75 cache 1620 x 2880) on
the moving Soft Blue field; W/T windows with the picture area's shape; library cutaways fill the picture area (or a square
card at the top of it when two people must stay in shot); real photos full screen with the real-photo chip; HyperFrames
lower thirds; a full-screen study card as a TRANSPARENT overlay (local line-graph template copy) so captions can sit under it.

Order: `transcribe_r1.py` (medium.en + 10 ms level map) -> `plate.py` -> `calibrate.sh` -> `prep.py` (edit list, voices,
words) -> `framing.py` SHOTS_ONLY (key stretches) -> `key_all.sh` (+ `key_tail.sh` in parallel) -> `prep_media.py` ->
`graphics.py` -> `build.sh` (framing, captions, assembly, audio gate, gate plan, watch, delivery gate) -> key measures
(`measure_key.sh`, `mcflicker_alpha.py`) -> `negscan_sheet.py` -> independent review -> `gate_only.sh` -> `page.py`.

## Lessons (each cost a build or a review round)

- **Whisper runs up to 0.5 s early on this roll.** "You" at 205.86 was a lip click (voice from 206.36), "Food" 218.76 really
  219.31. Cut on the 10 ms level map plus a >3.5 kHz map (fricative tails), never on word times. `audio/wordfix.json`.
- **Dan stands close on C1908:** head about 300 cache px wide, hair-to-chin about 440 rows. The gate's framing:no_wide_level
  needs the head >= 27 % of the window: W = 1060 cache px is the widest that passes every hold (1080 read 26.7 %, 1240 24 %).
  His elbows-out stance spans 1045-1093 px, so centre each wide window on his BODY midline at elbow height (stage-1 matte rows
  1300-2100), not on his head; the head-centred window clipped one elbow with free field on the other side.
- **The house-key flicker harness misreads a white tank.** `ds44_mcflicker.py` estimates alpha as distance from the pale check
  backdrop; an off-white tank sits 15-30 levels from it (ratio 1.72, a false fail) and dark hair is low contrast on navy (5.5).
  `mcflicker_alpha.py` runs the same motion-compensated measure on the key's ACTUAL finished alpha: 0.59 overall, hair 0.47.
- **The green screen's dark bottom-left vignette keys to 30 %** (about 140 tiny islands a frame, cache rows 2670-2880, cols
  0-150). Never in these crops, but masked in `assemble.key_frame` anyway.
- **calibrate.py crashes building its sheet when an excerpt touches the piece's end** (asks for one frame too many); the keyed
  excerpts are fine, build the sheet by hand.
- **A 25 fps clip in a 29.97 container (library A0072) repeats every sixth frame:** cache it through `decimate=cycle=6` and play
  the unique frames one per film frame. Check every library clip's real cadence, not its container rate.
- **Library A0063 has a fast spin at clip 1.75-2.75 s** (jacket off, a briefcase appearing): use 0-1.4 s and from 2.85 s.
- **B0448 jump rope: 0.5-1.6 s holds a both-feet hop.** Start at 1.6 s or later (RO-28 used 1.5 s). Opening on Dan's real
  jump rope under the hook worked for the first-5-seconds rule.
- **B0559 (man awake in bed) is median luma 20 and hides his face early:** use it from 39 s with a midtone curve.
- **Graphics timing goes stale silently.** build.sh used to skip graphics when shots.json matched shots-times.json (both
  refreshed by me), and its timing wrapper swallowed a failing graphics.py; three builds shipped old lower-third timing.
  Now graphics re-render whenever the edit list's frame count changes, and every wrapped step returns its real exit code.
- **The study card as an opaque HyperFrames scene fails captions:graphic_clearance everywhere** (the gate reads the mov's alpha
  box = full frame). Render it transparent over the film's own field (`kind: overlay`); captions sit under the plot.
- **captions:sync (energy method) misreads continuation cues** ("to you and" after "I'll prove it"): the 0.6 s look-back lands
  on the previous cue's first word. The reviewer measured those cues at +10/-10/0/0 ms against their own words. Report, never tune.
- **Voice:** a blind 5-trial listen put Balanced first (7.2) over untreated (6.8), the DS-41 house voice (5.0) and the fitted chain
  (4.2). Balanced then failed the tone row (bright at 3.5/5.5 kHz); a per-take EQ (`take_eq.json`) fixed it (mean 0.97 dB).
