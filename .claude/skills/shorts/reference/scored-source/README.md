# `scored-source/` — the pipeline for cutting Shorts out of a FINISHED, SCORED edit

Built for the 6 shorts cut from Muhammad Arsalan's ab-wheel organic cut (2026-08-27).
Copy it and adapt `config.js`, `segments.js` and `plan.js`; do not rewrite from scratch.

Use this one — not `full-bleed/` or `band/` — when the source is somebody's **finished 16:9
product** rather than our own rough cut. Three things are different and all three bite:

1. **There is a music bed, so `silencedetect` is useless.** `work/vad.py` builds a voice-band
   activity map instead. `segments.js` snaps every cut into a measured SPEECH gap and asserts it.
2. **Graphics are burned into the pixels.** `plan.js` classifies every shot and `cardCrop` either
   keeps a graphic whole or removes the band entirely. Never a sliced one. `work/gfxbox.py` and
   `work/ltwindows.py` measure where and when they are on screen.
3. **Section transitions are flash blooms.** `work/flashscan.py` checks every piece boundary so a
   short never starts or ends on a white frame.

Plus: `normalize.js` (a scored source gives every short a different loudness — normalise after
render, not before) and `work/stagescan.py` (blackdetect cannot see a stage that has gone empty
while the title and captions still draw).

Paths inside are absolute to this Mac's project root via `config.js`. Fix that first.
