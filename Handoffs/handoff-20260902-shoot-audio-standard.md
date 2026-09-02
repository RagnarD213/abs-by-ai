# Handoff — make the 8/3-shoot audio match Muhammad's reference, once, everywhere

**Created** 2026-09-02 by Claude Code (Opus 5) · **For** Fable, fresh session · **Not executed**

## Why this exists

Dan has now rejected the audio on **four** separate deliverables from the 8/3 Chagrin shoot, in
the same words each time — "the audio is no good", "it sounds echoey", "make it sound like
Muhammad's". Each session diagnosed it, fixed something real, shipped, and got rejected again.
On 2026-09-02 he said plainly: *"This is happening over and over and over again, and it's
unacceptable."*

He is right that it keeps happening. **He is wrong about the cause, and that matters**, because
every session so far has chased the cause he named instead of measuring.

## What the cause is NOT — settle this first, with the measurement, not an argument

Dan believes it is the two-mic fault (both channels summed instead of right-only). **On the
2026-09-02 spray-tan batch it was not.** Measured on the delivered file against the source put
through the identical EQ chain:

| candidate | correlation with the delivered audio |
|---|---|
| **RIGHT channel only + same EQ** | **+0.9912** |
| LEFT channel only + same EQ | +0.5965 |
| L+R sum + same EQ | +0.6877 |

The single-mic fix WAS applied. Do not re-apply it and declare victory; reproduce that table
first (`work/say.py`-style pull, cross-correlate with a ±15 ms lag search) so you know which
problem you are actually solving.

Also ruled out, with evidence, so nobody spends a session on them again:

* **Noise floor** — ours measured 36.0 dB under voice against his 36.2. Already matched.
* **Tone** — octave-band speech shape was fitted to 0.35 dB RMS of his ad.
* **A music bed masking his room** — his EDT is 40 ms full-band and **37 ms high-passed at
  250 Hz**, so his voice is genuinely dry; the short tail is not a filled floor. (An earlier
  session ruled a bed out by autocorrelation, which only detects a *rhythmic* bed — the
  high-pass test is the one that actually settles it.)
* **Level, clipping, silent seconds** — all clean, all already gated.

## What the cause IS

**The room.** Early decay time — milliseconds to fall 20 dB after a speech offset:

| | EDT |
|---|---|
| Muhammad's reference ad | **40 ms** |
| our shipped spray-tan short | **85 ms** |

The 8/3 rolls were shot in a kitchen doorway with hard surfaces. Even the close lav picks the
room up, and **reverb sits inside the words**, so no gate that measures levels, spectra, gaps or
channels can see it. That is precisely why this survived every check four times.

## The fix, already built and measured

`YouTube Long Form Video Content/spray-tan-first/work/dereverb.py` — spectral subtraction of the
late field. In each bin the late reverb is modelled as a scaled copy of that bin 20–150 ms
earlier and removed with a Wiener-style gain and a floor. Direct sound and early reflections are
kept, so the voice stays close rather than going thin.

Settled parameters: `alpha=0.62 d1_ms=20 d2_ms=150 floor_db=-24 smooth=0.30`.

| | shipped (rejected) | with dereverb | target |
|---|---|---|---|
| EDT | 75–85 ms | **37–39 ms** | 40 ms |
| octave shape vs his ad | 0.74 dB | **0.28 dB** | 0 |
| floor-to-voice | 36.0 dB | 50.0 dB | 36.2 dB |

⚠ **`floor_db` is the parameter that matters, and it is counter-intuitive.** Raising `alpha`
past ~0.62 makes EDT *worse*, because the tail starts riding the floor instead of decaying.
Lowering the floor from −14 to −24 dB is what took EDT from 50 ms to 40.

⚠ **ffmpeg cannot do this.** There is no dereverb filter, and `arnndn` has no model on this Mac.
A broadband expander (`compand`) only reached 63 ms and began pumping at 0.6 dB. It has to be a
Python stage — in `render.js` it runs on the concatenated `audio.wav`, before the mux, and is
length-preserving so the picture stays frame-locked.

⚠ **Re-fit the tone AFTER dereverb.** Removing the tail changes the octave shape; the corrective
EQ lives in `work/dereverb_eq.txt` and is applied straight after the Python stage.

## The job

1. **Verify the fix on the spray-tan batch** (already rendered with it — `spray-tan-first/`).
   Run `python3 work/audiogate.py`; every short must read EDT ≤ 55 ms, shape ≤ 1.00 dB.
2. **Apply it to the other three 8/3 long-form Shorts batches**, which all carry the same room
   and were all shipped without it: **Zepbound** (`zep-short1..8`), **supplements**
   (`supp-short1..8`), and, if Dan wants them re-cut, the delivered long-form masters
   `01`–`05` themselves. Re-render audio only where possible (`-c:v copy`).
3. **Promote the gate.** `work/audiogate.py` is wired into `spray-tan-first/qc.js`. Copy both
   into `.claude/skills/shorts/reference/` and into `/longform-edit`, so **no batch from this
   shoot can ship again without the room being measured**.
4. **Measure, do not assume, on any NEW shoot.** The 8/28 shoot and the new home filming set are
   different rooms; re-measure EDT against the reference before assuming these numbers transfer.

## The real lesson to encode

Every previous session fixed something genuinely broken and still shipped rejected audio, because
**the pipeline only measured the things it already knew how to measure.** The gate list grew
(channels, floor, tone, loudness, peaks, silence, sync) and never once asked "how big does the
room sound?" — the one thing a listener hears immediately.

When Dan rejects something on a quality a metric cannot see, the correct response is not another
pass at the metrics that already pass. It is to find the number that separates his reference from
ours, and then make that number a gate.

## Starter prompt

> Execute `Handoffs/handoff-20260902-shoot-audio-standard.md`. Start by reproducing the
> channel-correlation table in the "What the cause is NOT" section so you know the two-mic fix is
> already applied — do not re-apply it. Then verify `spray-tan-first` passes `work/audiogate.py`,
> and apply the same dereverb stage + gate to the Zepbound and supplements Shorts batches.
> Measure EDT on every delivered file; nothing ships over 55 ms.

**Recommended runner:** Fable, high effort. Audio DSP plus multi-batch re-rendering.
