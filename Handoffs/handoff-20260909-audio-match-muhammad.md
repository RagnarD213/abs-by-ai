# Handoff — make our audio sound like Muhammad's, and stop shipping on metrics alone

**Created** 2026-09-09 by Claude Code (Opus 5) · **For** a fresh session · **Not executed**
**Blocking:** nothing may ship from the 8/3 shoot until this passes Dan's ear, not just the gate.

## What happened

On 2026-09-02 Dan rejected the spray-tan Shorts' audio as "echoey". The diagnosis was correct —
the room measured **85 ms early decay against Muhammad's 40 ms** — and a spectral dereverb was
built, gated, and rolled into `.claude/skills/_shared/audio/`, then applied to **three batches**
(spray tan, Zepbound, supplements).

On 2026-09-09 Dan rejected the result far more strongly: *"absolutely awful, far far worse than
before… It sounds like I'm underwater."*

**He is right, and it is measurable.** The dereverb fixed the one number it was pointed at and
damaged three that nothing measured.

## The measurement that matters

Artifact-sensitive metrics — `flux` (frame-to-frame spectral change on speech), `SFM` (spectral
flatness variance, the musical-noise tell), `swirl` (modulation of the 3–9 kHz envelope), and
`gap` (how far the floor sits below speech, the over-suppression tell):

| | EDT | flux | SFM | swirl | gap |
|---|---|---|---|---|---|
| **Muhammad's ad (target)** | **40 ms** | **0.075** | **0.139** | **0.852** | **22.8 dB** |
| our raw right channel, untreated | 77 ms | 0.067 | 0.136 | 0.539 | 26.9 dB |
| **what we shipped** (α 0.62, floor −24) | 32 ms | **0.098** | 0.138 | **1.014** | **36.7 dB** |

⚠ **THE UNTREATED SIGNAL IS CLOSER TO MUHAMMAD THAN OUR PROCESSED OUTPUT ON EVERY ARTIFACT
METRIC.** Shipped is 1.29× his flux, 1.19× his swirl, and digs the floor **14 dB deeper than his**.
That combination — erratic HF, over-deep gaps — is exactly what "underwater" describes. We
overshot his 40 ms (we hit 32) and paid for the overshoot in artefacts.

Same for the other two batches: `zep-short1` measures flux 1.19×, swirl 1.29×, gap +18.4 dB.

## Why the gate did not catch it

`_shared/audio/audio_gate.py` checks: `comb, dryness, edt, floor, length, lr_corr, lufs,
provenance, silence, spread, tone, tp`.

**Every one of those measures level, tone, channels or SUPPRESSION. Not one measures damage.**
`edt`, `dryness` and `floor` all reward *more* suppression — so the gate actively scored the
underwater version as better. This is the second time in eight days that a batch shipped because
the pipeline measured the thing being fixed and not the harm being done.

## The job

**1. Re-tune, do not remove.** A sweep on the spray-tan roll (all against his numbers above):

| setting | EDT | flux | SFM | swirl | gap |
|---|---|---|---|---|---|
| α 0.62 floor −24 sm 0.30 ← shipped | 32 | 0.098 | 0.138 | 1.014 | 36.7 |
| α 0.45 floor −14 sm 0.35 | 35 | 0.083 | 0.140 | 0.784 | 32.2 |
| **α 0.30 floor −10 sm 0.45** | **45** | **0.076** | 0.138 | **0.693** | 30.4 |
| α 0.20 floor −8 sm 0.55 | 51 | 0.072 | 0.136 | 0.643 | 29.4 |

**Start at α 0.30 / floor −10 / smooth 0.45.** It lands EDT 45 ms against his 40 while holding
flux at his level and swirl *below* it. `floor_db` is the dominant lever — it sets how deep the
suppression can dig, and −24 is what dug the hole.

**2. Add a DO-NO-HARM row to the gate.** No processed output may score worse than the SAME FILE
UNTREATED on `flux`, `SFM`, `swirl` or `gap`. That single rule would have blocked all three
batches. Add it to `audio_gate.py` as a gated row, not a printed note.

**3. Re-render all three batches** once the setting passes: spray tan (6), Zepbound (8),
supplements (8). Pre-fix copies are in `Short-form video content/_pre-audiofix-20260902/`.

**4. ⚠ VALIDATE ON DAN'S EAR BEFORE ANY BATCH RE-RENDER.** Build the A/B on ONE short — untreated
/ candidate / Muhammad, same words — send it, and wait. Do not re-render eight files on a metric.
Both failures so far came from trusting a number over a listen.

## What is already known and must not be re-litigated

* **It is NOT the two-mic fault.** The delivered file measured **+0.9912** against the source's
  right channel through the identical EQ (left 0.60, sum 0.69). Dan attributes it to this every
  time; reproduce that correlation table once, then move on.
* **It is NOT a music bed.** His EDT is 37 ms high-passed at 250 Hz, so his voice is genuinely dry.
* **It is NOT the noise floor or the tone.** Floor already matched (36.0 vs his 36.2); octave
  shape is fitted to 0.2–0.6 dB.
* **His room really is drier than ours** — that part of the original diagnosis stands. The error
  was the size of the hammer, not the target.

## Open question worth testing

We assumed EDT must equal his 40 ms. His ad is the same rig but not necessarily the same mic
distance or room treatment. **Test whether landing at 50–60 ms with zero artefacts sounds closer
to him than 40 ms with artefacts** — the sweep says that trade is available, and the raw signal's
artifact numbers suggest gentler is safer.

## Also affected

`Handoffs/handoff-20260909-website-video-rev6.md` item 1 calls for "another audio pass toward
Muhammad's" and records the website video's room at **77 ms**. It must use whatever setting comes
out of this task — do not let it fork its own chain (AGENTS.md: one module, extend with a flag).

## Starter prompt

> Execute `Handoffs/handoff-20260909-audio-match-muhammad.md`. Dan rejected our dereverbed audio as
> "underwater"; measured, our processed output is further from Muhammad's ad than the UNTREATED
> signal on every artifact metric (flux 1.29×, swirl 1.19×, floor 14 dB deeper) while the gate
> only measured suppression. Re-tune `_shared/audio/dereverb.py` starting at α 0.30 / floor −10 /
> smooth 0.45, add a do-no-harm row to `audio_gate.py` so no output can score worse than the
> untreated file, then build a THREE-WAY A/B on one short (untreated / candidate / Muhammad) and
> send it to Dan. Do not re-render the batches until he approves the sound.

**Recommended runner:** Fable 5.1, high effort. Audio DSP plus a three-batch re-render.
