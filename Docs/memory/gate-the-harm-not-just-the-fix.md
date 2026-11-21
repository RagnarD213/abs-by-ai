---
name: gate-the-harm-not-just-the-fix
description: "When a pipeline gate rewards a correction, it must also bound that correction's damage — and against the file's own untreated signal, not only against the reference"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ca5bd1f-f3fb-45ac-8b45-7db227dec7e6
  modified: 2026-09-09T15:38:04.961Z
---

Twice in eight days a batch shipped because the gate measured the thing being fixed and not the
harm being done. The 2026-09-02 dereverb hit its target (early decay 85 → 32 ms, past Muhammad's
40) and Dan rejected the result as *"absolutely awful… it sounds like I'm underwater."* Every gate
row that existed — `edt`, `dryness`, `floor` — rewards MORE suppression, so the gate scored the
build he hated as *better than* the one he liked.

**Why:** a correction and its damage are the same knob turned different distances. A gate that
only measures the correction has no opinion about how far is too far, so it always votes for more.
The missing comparison was never the reference (a different room) — it was **the file's own
untreated signal**. Measured, our raw channel was closer to Muhammad than our processed output on
every damage metric.

**How to apply:** when adding a row that rewards a correction, ship a row bounding its damage in
the same commit, and bound it against the untreated input, not a constant (`_shared/audio`'s
`do_no_harm`: flux/swirl ≤ ×1.35 of the same file untreated; it blocks 16/16 of the files that
shipped). Calibrate the limit on matched pairs — the same source, both settings — and confirm the
pipeline alone, with the correction disabled, costs nothing. Drop any candidate metric that can't
fail a bad build: `gap` couldn't (the expander costs 1.22× by design) and `sfm` moved the wrong way.
**Never raise the limit to make a build pass** — that is the failure mode the row exists to stop.
Related: [[shoot-audio-two-mics]], [[muhammad-trial-edit-analysis]], [[shared-fix-may-not-reach-the-pipeline]].
