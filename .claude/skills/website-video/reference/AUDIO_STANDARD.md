# The audio standard for website videos — "sounds like Muhammad's", as numbers

Dan approved this chain by ear twice: the rev-2 EQ/expander/bed ("you got it nailed. This is the audio that we
want", 2026-09-02) and the gentle dereverb from a four-way A/B on the shorts (2026-09-09). Rev 6 of the website video
combined them and passed every row of the shared gate with margin. Reproduce it; do not re-tune it without an A/B that
beats it on the gate.

## What the finished file must measure (the gate, `_shared/audio/audio_gate.py`, on the DELIVERED file)

| row | Muhammad's ad | rev 6 delivered | limit |
|---|---|---|---|
| one voice (L/R correlation) | +0.993 | +0.9998 | ≥ +0.97 |
| no comb (ripple 300–6 k) | 0.54 dB | 0.49 dB | ≤ his + 0.35 |
| **dry room (early decay after a word)** | **40 ms** | **45 ms** | ≤ 80 (this skill: ≤ 50) |
| tone (10-band error vs his) | 0 | 0.83 mean / 1.72 max dB | ≤ 1.2 / 2.5 |
| clean between words (voice-over-floor, 3 bands) | 27.6 / 34.7 / 28.0 | +2.0 / 0.0 / +1.5 vs his | within 3 dB |
| **no processing damage (spectral flux / HF swirl)** | 0.072 / 0.835 | 0.067 / 0.711 (0.93× / 0.85×) | ≤ his ×1.10 |
| words stop cleanly (drop 64 ms after a word) | 7.4 dB | 8.9 dB | ≥ his − 1.5 |
| loudness | −18.2 LUFS (his, too quiet for us) | −14.5 LUFS | −14 ± 1 |
| speech spread p90−p10 | 8.2 dB | 6.0 dB | ≥ his − 3 |
| true peak | +0.1 (his, too hot) | −2.6 dBTP | ≤ −1.0 |
| silence / length | 0 / exact | 0 / exact | 0 / ± 0.10 s |

The damage row exists because the gate once scored an "underwater" build as BETTER: `edt`, `dryness` and `floor` all
reward more suppression. Processing may not push flux or swirl past his.

## The chain (`reference/recipe/audio4.py`, wrapping `audio3_rev2chain.py`)

```
pick_lav.py <roll>                      which track is the lav, per file (8/28 rolls: four mono tracks, lav is a:1)
dereverb  alpha 0.30 · d1 22 ms · d2 70 ms · floor −10 dB · smooth 0.45     (Dan's ear, 2026-09-09; _shared defaults)
highpass 70 → the rev-2 fitted EQ (9 bells + treble shelf: fill 150–250, cut the 600–900 honk, cut the 1.4–2.2 k edge,
          +7.9 dB air above 6.5 k)  → agate 0.012 / 1.8 / range 0.35 (the expander) → NO compressor
pan=stereo|c0=c0|c1=c0 (centred)  → bed at −44 dB ducked 6:1 by the voice (or none)
measured gain + alimiter limit 0.71, delay measured by cross-correlation and trimmed → −14 LUFS, −2.5 dBTP in PCM
```

Run: `VIN=nocap.mov VOUT=nocap_audio.mov DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45
MUSIC_DB=-44 COMP=0 python3 audio4.py`. For a NEW roll the EQ must be re-fitted against the reference on the gate's
own metric (`voicefit.py` lineage / `voice_chain.py --in`): iterate, and ship the first smooth passing curve, never
the over-fitted comb (lesson 87). Then verify on the delivered file and fold the residual back (the expander, limiter
and AAC all move the spectrum).

## What is NOT a lever (measured, so nobody spends a revision on it)

- **The expander does not set the speech spread.** Default, softened (0.009 / 1.5 / range 0.5) and off all read
  6.0 dB p90−p10 on rev 6. The spread is set by how much gain the limiter has to absorb to reach −14 LUFS from a
  −23 LUFS premix. The next lever, if Dan ever wants it "less flat", is the loudness target — a different decision.
- **EQ does not move voice-over-floor**: it scales the voice and the floor together in-band. Makeup, limiting and the
  bed move it (every 4 dB of bed costs ~2.5 dB of floor; +9 dB into the limiter costs 0.5–2.6 dB).
- **A stronger dereverb is not "closer to his"** even when EDT reads under his 40 ms — it is what he called
  underwater. Room 45 ms with flux/swirl under his beats room 32 ms with flux 1.29× his.

## Rules that came from rejections

- `loudnorm` never, anywhere: it silently falls back to DYNAMIC when the linear target is unreachable and swings the
  gain second to second (rev 1: +1.2 → +9.5 dB; the ad-1 vertical: 133 of 232 seconds pushed up).
- Fit against the source you will ship; refit after any channel fix (the comb-filtered mix wanted the opposite EQ).
- Fit across several windows, not one (one 4 s window read 1.25 dB mean error; five windows read 3.02).
- Locate a matching span in his edit by transcript, never by envelope correlation.
- Re-transcribe the finished mix (script fidelity ≥ 99 %); an expander that eats a fricative is invisible in a spot
  check and obvious there.
- Ship the A/B (`AB_his-vs-ours.mp4`: his three sentences, then ours) with every review copy. "Sounds worse" is only
  settleable by ear, and Dan has asked twice.
- Two-mic rolls: cross-correlate the channels with a lag search on every new roll; a peak at a non-zero lag is two
  mics. `pick_lav.py` does this; `base.py` reads its JSON; nothing writes `pan=mono|c0=c1` by hand.
