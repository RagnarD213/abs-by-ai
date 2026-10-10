---
name: dan-voice-guide
description: "Voice guide + corpus + blind bench for writing as Dan; read DAN-VOICE.md and the voice/passages file for the type before writing; 10-08 baseline: judges catch Claude 90% of the time even with the guide"
metadata:
  type: reference
---

Everything for writing in Dan's voice lives in the repo, so cloud and local sessions share it:

- `.claude/skills/_shared/DAN-VOICE.md`: the guide (Part 1, 2026-10-06; rebuild is Phase B).
- `.claude/skills/_shared/voice/`: whole real passages per type (`passages-content.md`, `passages-ads.md`,
  `passages-conversion.md`, `passages-products.md`, added 2026-10-08), the older example files, his edits to Claude
  drafts, `profanity-and-controversy.md` (swearing rules from his own words), `STATS.md` (one baseline per type),
  `HELD-OUT.md` (test passages that must never be quoted).
- `scripts/voice/`: `voice_stats.py` (counts, `--small` for small everyday words), `voice_fingerprint.py` (function-word
  Delta and LUAR style distance), `corpus.py`, `heldout_guard.py` (run after editing any voice file), `bench.py` (the
  blind bench).
- Raw corpus: `voice-corpus/` in the project folder (git-ignored) and Drive folder `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`
  (`voice-corpus-2026-10-08/`). Sources: `Docs/VOICE_CORPUS_INVENTORY.md`, `Docs/VOICE_CORPUS_SOURCES.md`.

**Baseline, 2026-10-08 (Dan Voice P2A).** 40 held-out passages, 80 blind trials per setup, judges a fresh Opus 5.5 and
Gemini: cold Claude was picked out 86% of the time, Claude with today's guide 90% (chance is 50%, the goal is 60% or
less). The guide did not make Claude harder to catch; it changed the giveaway from "over-acts his voice" to "too clean,
too even, too organized". Dan's own blind test on 2026-10-10: he picked his own writing in 13 of 19 pairs (68%).
Reports: `Docs/voice-bench/`.

**Why:** Dan's goal is writing "so well that nobody ever thinks that this is AI". Until 10-08 nothing measured it.

**How to apply:** before writing as Dan, read `DAN-VOICE.md` and the `voice/passages-*.md` file for the type (content,
ads, conversion, products; see [[voice-corpus-sources]]). Do not tidy: keep long loose setups, his exact repeats and
his small words ("really", "very", "kind of", "going to", "so", "just"); do not overcorrect "and" (his rate is about
2.4 to 2.8 per 100, not lower). Check a draft with `voice_stats.py`. Any change to the guide or skills gets scored
with `bench.py` and kept only if the number moves. Next step is Phase B of
`Handoffs/handoff-20261008-dan-voice-training-part2-plan.md`. Related: [[script-zero-edit-lessons]],
[[dan-personal-facts-for-scripts]], [[no-em-dashes]], [[swearing-never-cut-never-ask]],
[[scripts-his-wording-not-his-ramble]].
