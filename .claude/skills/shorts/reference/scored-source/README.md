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

`recentre/` is the centring audit, extended from the 2026-08-27 tooling to cover CARDS as well
as 9:16 crops: `collect2.py` samples every shot with a human subject, `personmask` (Apple Vision)
masks them, `audit2.py` projects the torso anchor through each shot's own geometry and reports
pixels off centre on the delivered canvas, and `propose.py` renders shipped-vs-proposed five
frames across each shot. **Look at that sheet before adopting anything** - it over-fires on any
shot where the subject travels.

`work/boundcheck.py` re-checks every shot boundary against a full-frame-rate frame-difference
peak. Run it every build: a boundary landing early gives the WRONG SHOT's content the previous
shot's treatment, and it presents as a framing bug, not a timing one.

Plus: `normalize.js` (a scored source gives every short a different loudness — normalise after
render, not before) and `work/stagescan.py` (blackdetect cannot see a stage that has gone empty
while the title and captions still draw).

Paths inside are absolute to this Mac's project root via `config.js`. Fix that first.
