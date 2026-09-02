# website-video/ — the post-generation conversion video (2026-09-01, 8/28 shoot, C1650+C1651)

The first cut from the 8/28 shoot and the first TRUST-tuned edit: plays on absbyai.com right
after a visitor generates their goal image. Same pipeline shape as `../rev5` and the Ad 3 dir
(`/Volumes/Extreme/_edit_work/ads234-8-14/c1593/`), with these differences:

| file | what is new |
|---|---|
| `make_lut.py` | **S-Log3 / S-Gamut3.Cine → Rec709 33³ .cube built in numpy** (Sony transfer, gamut matrix, soft shoulder). The 8/28 shoot is the first in this format; `lut3d=...:interp=tetrahedral` in `grade.txt`, exposure 1.45×, saturation 0.88. |
| `edl.py` | phrase-anchored spans across TWO rolls, edges validated against a −40 dB envelope |
| `base.py` | multi-source concat; **a:1 is the lav** (4 mono LPCM tracks on this shoot); renders **2560×1440** so the 1.30 punch never upscales |
| `tight.py` | calmer pause pass: pauses ≥0.30 s shortened to ~0.30 s, never removed |
| `layout.py` | 3 levels, 9 s minimum hold, hard splices covered hardest-first with a 3.5 s floor, phone panels LEFT with Dan in the right column |
| `audio2.py` | **gain + alimiter instead of loudnorm** (loudnorm fell back to DYNAMIC on this mix); limiter delay measured (239 samples) and removed; no SFX bed |
| `gfx.py` | J2AD palette, slow drifts, "Results are not guaranteed." on real-physique cards, heading-width assert, CTA card that HOLDS to the last frame |

Numbers on the delivered file: 3:51.56, −14.2 LUFS, TP −2.2 dBTP, L/R +0.9986, 203 wpm,
fidelity 99.0 %, 47 visual changes, median hold 5.1 s, longest 13.7 s, coverage 54 %.


## REV 2 (2026-09-02) -- audio, framing and graphics rebuilt after Dan rejected rev 1

Rev 1's scripts are in `rev1/`. Rev 2 keeps `edl.py`, `make_lut.py`, `env.py`, `tight.py`,
`hard_splices.py` and the cut, and replaces:

- `base.py` + `grade.txt` -- the base is the FULL 3840x2160 (no scale in the grade) so every
  framing level is a downscale.
- `voicefit.py` -- fits the 10-band EQ against Muhammad's ad using `voice_ref_check.py`'s own
  metric (iterate; take the smooth passing iteration, not the over-fit one).
- `audio3.py` -- the fitted EQ, a gentle expander, NO compressor, bed at -44 dB, measured
  gain + limiter finish. `VIN=<wav> VOUT=<wav>` renders test mixes for the gate.
- `layout.py` -- WIDE / MID / TIGHT / PIP crops of the 4K with the light and wide-shot
  assertions; `pip` pre-renders the phone-beside-Dan insert (alphamerge + hairline plate).
- `gfx2.py` -- photo cards, title cards and the PiP plate on Muhammad's measured card system
  (grid field, 1476x924 olive plate, 28 px photo inset, 142 px oblique caps). `PREVIEW_T=<s>`
  renders one frame to `pv/` for checking on a real frame before any encode.
- `gfx_lowerthirds.py` (= rev 1's `gfx.py`) -- only the six lower thirds are still built from it.
- `beats.py` -- 13 beats. `captions.py` / `qc.py` / `watch.py` -- updated lists + the framing checks.
- `stage2.sh`, `stage3.sh`, `deliver.sh`, `wait_stage2.sh` -- the background chain and the
  delivery gates (audio gate + A/B, exact-time contact sheet, QC, watch, review copy, silence).


## REV 3 (2026-09-02) -- head-anchored crops, the repeated line cut, captions clear of lower thirds

Rev 2's scripts are in `rev2/`. Audio (`audio3.py`, bed -44 dB, no compressor) is APPROVED and
unchanged. `rev3.sh` is the whole chain (tight re-render + graphics in parallel, then hard splices ->
head track -> plan -> MOV-vs-beat probe -> punch -> mix -> audio -> captions -> `deliver.sh`);
`wait_rev3.sh` waits on its PROCESS. New or changed:

- `tx_patch.py` -- splices an isolated medium.en pass over the hidden restart into the roll JSON
  (the chunked pass had stitched both attempts into one 2.8 s token). Idempotent; original kept as
  `tx/C1650.whisper.orig.json`.
- `tight.py` -- `MANUAL_CUTS` (base-time spans, edges asserted against the -40 dB envelope, pause
  cuts inside absorbed) and the rule that words inside a removed span are DROPPED from the word map.
- `headtrack.py` -- samples `base.mov` at 4/s, maps through the keeps, writes a keeps signature.
- `layout.py` -- `LEVELS` are (x, w, h); `crop_for()` sets y per punch segment from that segment's
  minimum head top minus 3 % of the crop height; asserts the track is keyed to this cut, y0 in 0..500,
  the light guard. `CROPS` parallels `PUNCH`.
- `gfx.py` (lower thirds) -- `bottom=1080-80` via the new `motionlib.lower_third_bar(bottom=)`.
- `gfx2.py` -- `photo_card(in_dur, out_dur)`; the before card fades 0.30/0.30.
- `beats.py` -- BEFORE = pause after "finally lost." -> "and"; TODAY from "I have the most";
  asserts >= 0.5 s of Dan between them.
- `captions.py` -- `MV_LIFT = 290` (measured: ink bottom 795 against a lower-third top of 858).
- `qc_frame.py` -- checks 10 (caption ink vs lower-third alpha, >= 20 px; no ink in the phone box)
  and 11 (headroom on the delivered frames: >= 15 every frame, per-segment min <= 45, median <= 60,
  ceiling 90; proof frames to `pv/headroom_*.png`). `qc.py` imports it. Both FAIL on rev 2's file.
- `sheet.py` -- contact sheet from exact `-ss` grabs (lesson 94); `deliver.sh` uses it.
- `headtrack_refine.py` -- the QC detector run on `punched.mov`, mapped back to 4K, stored under
  `refine`; `layout.py` takes the per-segment minimum over both tracks (lesson 106). The first rev-3
  pass had the hair on the edge in three TIGHT holds without it.
- `deliver.sh` -- `AUDIO_GATE_SOFT=1` lets the (new, stricter) shared audio gate report instead of
  abort, ONLY because this video's audio chain is the one Dan approved by ear on 2026-09-02 and the
  gate's two new rows (early decay, speech spread) fail the approved rev-2 file identically. The
  reference copies of `audio3.py` / `base.py` / `qc.py` in this folder were re-pointed at
  `_shared/audio/` by the audio-unification session the same evening; the chain that actually rendered
  rev 2 and rev 3 is `audio3.py` at git `2d182f4` (also in the work dir's `rev2/`).
