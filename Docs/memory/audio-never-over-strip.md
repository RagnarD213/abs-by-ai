---
name: audio-never-over-strip
description: "Dan's standing rule after the \"underwater\" dereverb — never process audio past the reference to win a metric; artefacts are the thing he hears"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: efe4ae8f-2c95-4932-b82b-65c1c116f309
  modified: 2026-09-09T15:05:47.942Z
---

Dan, 2026-09-09, on 04 invest-health: *"The audio sounds absolutely awful. It sounds underwater…
We can never, ever strip audio like this."* Second rejection of the same defect in eight days (the
spray-tan Shorts were the first).

**Why:** noise/reverb reduction is judged by what it COSTS, not by the number it improves. The
spectral dereverb hit early-decay 32–37 ms against Muhammad's 40 — *better* than the target — and
Dan hated it, because suppression that deep makes each frame's gain differ from its neighbour's and
the voice shimmers. Measured on 04: spectral flux 1.31× his. The untreated right channel was closer
to his ad on every damage metric than the processed output was.

**How to apply:**
- Never process past the reference to win a metric. Overshooting the target is a warning, not a win.
- A gate whose rows all reward the same direction (`edt`, `dryness`, `floor` all favour MORE
  suppression) will rate the damaged build as better. Every suppression metric needs a
  counterweight that measures the harm — that is what `artifacts` (flux/swirl) is for in
  `_shared/audio/audio_gate.py`. Never raise `artifact_x` to make a build pass.
- Validate on Dan's ear before re-rendering a batch. He picks from an A/B; doctrine does not.
- The approved dereverb is alpha 0.30 / d1 22 / d2 70 / floor −10 / smooth 0.45. Do not re-tune it.
- **On a wet long-form room, the honest answer may be NO dereverb at all.** Measured on 04
  (2026-09-09): spectral subtraction raises flux *by construction*, so even the approved setting took
  the lav from 1.03× his (untreated) to 1.20×, and the mix to 1.14× against a 1.10× bound — it could
  not pass. Rendering with `--no-dereverb` passed all 13 rows at flux 1.00× his and came in *cleaner
  than the untreated source*. Precedent: website rev 2, the cut Dan called "you got it nailed", is
  EDT 74.7 ms with no dereverb (same shoot, same room).
- **2026-09-29: the dereverb is OPT-IN in `voice_chain.py`** (Dan: "Codex's audio approach works better;
  copy it"). Default = no dereverb, no compressor, fitted EQ. Opt in only with
  `--dereverb-because "<what you heard, on which A/B>"` on a room measuring EDT > 55 ms. The `artifacts`
  row now excuses flux/swirl past his x1.10 only when the file's untreated recording already carried it.
- The 09-09 four-way A/B that chose alpha 0.30 was judged on Shorts material. Do not assume an
  ear-picked setting transfers to a different programme without re-measuring it there.

Related: [[shoot-audio-two-mics]], [[muhammad-trial-edit-analysis]], [[revisions-zero-edit-goal]]
