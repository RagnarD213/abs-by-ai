# `zepbound-honest-update/` — eight Shorts from "02 - My Honest Zepbound Update" (2026-09-01)

Copied from the skill's `reference/clean-master/` (the supplements batch) and adapted. The
supplements batch's own README is kept beside this one as `README_supplements-batch-reference.md`
— everything in it still applies; this file records only what was DIFFERENT on this roll.

## Source and its two timelines (the trap, third occurrence, new cause)

Source: `CUT_v1_graded_NO-GRAPHICS.mp4` (1827.751 s container, 29.97 fps, 49 EDL ranges), never
the delivered `FINAL_zepbound.mp4` (48 % insert coverage) and never `*_PRE_AUDIOFIX.mp4`.

`work/chancheck.py` on the clean master: **L/R corr +0.12, right channel 7.5 ms ahead, right
channel 5–7 dB more dynamic range** — the two-mic signature, identical to the PRE_AUDIOFIX file.
Right channel only, as mono, as on the supplements batch.

⚠ **The AAC stream holds 85,706 × 1024 samples = 622 ms MORE than the container declares, and
this time the excess sits at the 48 joins as ~13 ms pts OVERLAPS.** Three extraction attempts:

| extraction | wav vs container | lag vs `-ss` | verdict |
|---|---|---|---|
| `aresample=async=1:first_pts=0` (the supplements recipe) | +57 ms | +20 → +84 ms, growing | soft compensation cannot keep up |
| `aresample=async=1000` | +19,903 ms | none found | pads silence into every discontinuity — never use |
| per-EDL-segment `-ss/-t` cuts, concatenated | +622 ms | garbage | ⚠ **a `-ss/-t` pull that spans a join comes out ~13 ms LONG** |
| **`aresample=async=1:min_hard_comp=0.005:first_pts=0`** | **+0.6 ms** | **±4 ms at 8 points, corr ~1.0** | **used** |

The default `min_hard_comp` is 0.1 s, so a 13 ms overlap is only ever soft-corrected. Lowering it
to 5 ms makes each overlap a hard trim at the join. **The same filter is now prepended to the
renderer's audio pull** (`render.js`, `TIMELINE_FIX`) because a piece spanning an internal join
otherwise carries the overlap into the delivered audio — measured: without it a 12 s pull straddling
a join was 12.0145 s; with it, exactly 12.000 s and post-join audio at 0.00 ms (corr 1.000).
`-ss` itself is sample-accurate on this file (10 ms and 37 ms offsets reproduce exactly).

## Voice chain: fitted against Muhammad's AD — and the gate was DROPPED

`work/finalchain.py` fits the octave-band shape against `Muhammad Ad Videos/Daniel HQ Fitness AD
Video v3 HD.mp4` (indoor talking head, same rig — never the outdoor ab-wheel cut). Shape
difference **2.03 → 0.33 dB RMS**.

⚠ **This roll does not need the denoiser or the gate the supplements batch needed, and they cost
word tails here.** Floor relative to voice, measured on the plain right channel:

| | 80–250 Hz | 250–1 k | 1–4 k |
|---|---|---|---|
| Muhammad's ad | 25.7 | 36.1 | 28.8 dB |
| ours, right channel, plain | **29.1** | **39.4** | **31.1 dB** |
| ours through the supplements chain (afftdn + gate) | 47.4 | 57.6 | 47.8 dB |

Plain is already 3 dB cleaner than the reference in every band. `work/validate_chain.py`: the
gated chain measured **98.7 % word match and 14.2 dB pumping** against 100 % / 7.8 dB without.
Final chain = right channel → highpass 75 → fitted 8-band EQ → de-esser. Then `finishaudio.py`:
tone-match to the batch median, **pure gain + limiter, not loudnorm** (loudnorm falls back to
dynamic mode silently when the gain exceeds the peak headroom).

## Vertical geometry: his head is at source row 0

`work/vertgeom.py` over all 49 beats: **head top = row 0 on every beat.** The camera framed him
to the top edge, so there is no ceiling to crop (cropTop 0, window 738×1080, 1.46× upscale) and
the picture is dropped to **y=340** (not 310) so the headline's ink (ends ~y300) keeps ≥40 px of
black above his hair. `qc.js`'s old "head clears dropTop by ≥60 px" check is unattainable and
meaningless here; it now measures title-ink-bottom → dropTop off the rendered PNG instead.

Torso centre wanders **0.511–0.586 across beats** (144 px of source, 215 px delivered); every
shot carries its own measured centre. Punch: 678×992 from the top (tightTop 0 — the head is at
row 0, so the punch crops the bottom).


## ⚠ The torso-block anchor is WRONG on this framing — the crops use the HEAD

First render, `work/centregate.py` on the delivered files: A +71 px, E +53 px, G −98 px, every
short with a 70–117 px frame-to-frame spread. Per-shot re-measurement then contradicted the
per-beat numbers by up to 130 px on the SAME span, and the per-frame values were **bimodal**:
the same shot read 0.50 on one frame and 0.58 on the next while the silhouette edges sat still.

Drawn on frames (`work/frames/h_check.jpg`): the "torso block" is the shoulder-to-shoulder band,
and Dan is framed cut at the waist with his arms hanging into the anchor's 60 %-coverage band —
the bulkier frame-right arm flips in and out of the block and drags the centre 150 px. The
supplements set never showed this because he stood behind a counter with his arms above it.

| anchor (per-shot medians, 24 shots) | within-shot sd | cross-shot spread |
|---|---|---|
| torso block | 23–172 px | 206 px |
| silhouette centre | 9–162 px | 218 px (biased by the big arm) |
| **head** | **14–166 px, mostly <80** | **134 px** |

Crops are now the **per-shot head median** (`work/measure_shots.py` → `work/shotgeom.json` →
`work/mkcrops.py`), and `work/centregate.py` measures the same anchor on the delivered file.
**Verify the anchor on drawn frames before trusting any centring number on a new set.**

## Boundaries: eleven pieces ran past a source splice

The long-form cut its pauses tight, so the pause after a beat's last word IS the join.
`snapOut`'s 0.34 s tail walked **0.04–0.30 s into the next take on 11 of 20 boundaries** — a
one-to-nine-frame flash of a different take right before every cut. Detected with a
piece-boundary-vs-`splices.json` scan (now inline in the notes above `SEGMENTS`), fixed with
`outAt`/`inAt` 20 ms inside the frame-measured splice. **Run that scan on every batch.**

## Captions

Whisper heard the drug as "zap bound", "Zetbound" and "dirt zap bound" ("your Zepbound"); fixed per
word before chunking (`PAIR_FIXES`/`WORD_FIXES`), each checked against the delivered SRT.
**Captions print the drug name because he says it** — the no-drug-name rule is a GRAPHICS rule
(titles, eyebrows, chips) and these are organic Shorts. If any of these ever runs PAID, the captions
need a re-render with the name masked. `abs` prints lower case, `AI` upper.

## Not done, deliberately

* No AI cover clips (`inserts.js` is empty) — every join is hidden by the punch alternation.
* Whisper pass b (the orphan-scan insurance) was stopped at 52 %: load average hit 64 with it
  running beside the render, and the caption proofread of all eight reads as continuous speech.
