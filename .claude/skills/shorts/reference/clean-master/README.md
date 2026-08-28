# `clean-master/` — cutting Shorts from OUR OWN clean long-form master

Built for the eight Shorts cut from `03 - The Supplements I Actually Take` (2026-08-28).
Copy it and adapt `config.js`, `segments.js` and `plan.js`; do not rewrite from scratch.

Use this one — not `scored-source/`, `full-bleed/` or `band/` — when the source is a long-form
**we rendered ourselves** and a `CUT_*_NO-GRAPHICS.mp4` exists beside the delivered master.
Four things are different from the other pipelines and all four matter:

## 1. ⚠ RUN `work/preflight.py` FIRST. THE SOURCE MAY HAVE TWO TIMELINES.

**A master assembled by concatenating segments can hold more audio samples than its container
declares, spread through the file.** The supplements master (62 ranges) holds 0.76 s more.
Whisper word timestamps and every silence measurement live on the DECODED-SAMPLE timeline;
`-ss`, and therefore every cut and the whole picture, live on the CONTAINER timeline. They
agree at t=0 and drift ~0.5 ms per second — **669 ms apart by the end of that video.**

The first build of this batch shipped **captions 280–650 ms late** and **clipped the first word
off two shorts**, while passing QC 12/12, the splice test, loudness, duration and the centring
audit. Nothing compared delivered audio against delivered captions.

Extract analysis audio on the container timeline:

```
ffmpeg -i SRC -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 48000 -c:a pcm_s16le work/audio48k.wav
```

Residual lag then collapses to a constant −20…−42 ms — inside one AAC frame. Full write-up:
`work/TIMELINE_TRAP.md`.

## 2. `syncgate.py` is a HARD GATE and `qc.js` will not pass without it

It transcribes each DELIVERED short and matches every caption's first word against the heard
audio. It is the only check that measures what a viewer experiences. `qc.js` refuses to pass a
file the gate has not seen, keyed on mtime so a re-render invalidates the stamp.

⚠ **It carries a calibration, and the calibration is not a fudge.** The gate uses `base.en`
while captions come from `medium.en`, and base.en reports word onsets a median of **exactly
−80 ms** earlier — measured on the same source audio over three spans, n=414, −80 ms in all
three independently. Uncorrected it fails good builds. Re-measure if either model changes.

## 3. Shot boundaries come from the EDL, not from scene detection

We own the cut, so `edl.json` lists every splice. `work/edl_splices.py` computes their nominal
positions and `work/splices.py` **measures** each one as a full-frame-rate frame-difference
peak, because `render.py` rounds every range to whole frames and the error accumulates
monotonically (+1.137 s over 62 ranges — exactly the amount by which the EDL undershoots the
master). All 61 boundaries came back at 3.2x–22x the local median. `detect-shots.js` then just
intersects that table with the chosen pieces. This is strictly better than the 320x180 `scene`
detector, which put a boundary 0.60 s early on the ab-wheel batch.

## 4. Cut points are the INTERSECTION of two silence measurements

A clean master has no music bed, so `silencedetect -26dB/0.05` is valid here — which makes it a
free independent control on `work/vad.py`'s speech-band map rather than a replacement for it.
`work/gaps.py` intersects them, so every cut is both "nobody is talking" and "nothing is
audible". They agreed on 85 % of silencedetect's intervals; the intersection kept 1082 gaps.

⚠ **`snapIn` must accept a gap that CONTAINS Whisper's claimed word start**, not only one that
ends before it. Whisper stretches short words backwards across real pauses; without that clause
short E opened on "...from there. So this is the biggest mistake" — a fragment of the previous
sentence. When the claimed start is inside measured silence, the word begins at the gap's end.

## Also fixed here, and it affects every earlier batch

**`captions.js` silently dropped every zero-duration Whisper word.** The `>50 % overlap` test
computes `0/1e-6 = 0` for a word with `start == end`. Nine such words on this roll; it ate one
in five of the eight shorts, turning "creatine is not an **option** for me" into "not an for
me". Also fixed: mis-hearing corrections now run **per word, before chunking** (a two-word fix
straddled a four-word chunk boundary and the line-level regex never saw it), hyphen-initial
tokens merge like punctuation ("sub -step"), and the first word of each piece is capitalised.

## Layout notes specific to a locked talking-head master

* **Measure whether the set is payload before choosing a layout.** `work/stackscan.py` takes the
  temporal median of a region and reports departures from it. Here the supplement stack moved by
  1.07 grey levels over 23 minutes, so the band layout would have cost 60 % of subject height to
  preserve wallpaper. Full-bleed won.
* **Cropping the top off IS the right direction when the subject sits low.** It narrows the
  window (the documented trap) but makes the subject bigger, and the trade is measurable:
  644x960 at 1.68x beats a full-height 608x1080 at 1.78x on both size AND sharpness.
  `work/vertgeom.py` picks it from the global minimum head position.
* ⚠ **The Vision mask leaves a faint sliver along the top frame edge on some frames**, so raw
  mask-top is not head-top — it reported row 15 against a true ~180 on three beats, a 160 px
  error that would have set the batch's geometry. Take the largest connected component and
  require a real run width (`work/vertgeom.py`).
