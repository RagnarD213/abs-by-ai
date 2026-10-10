---
name: dan-voice-guide
description: "Writing as Dan: content plan from the owning skill, sentences from the dan-voice-writer agent (clean call, 5 real passages, no rules); bench 10-10: rules in the writer's prompt make Claude easier to catch (92%) than real passages alone (82%)"
metadata:
  type: reference
---

Everything for writing in Dan's voice lives in the repo, so cloud and local sessions share it. Method doc:
`.claude/skills/_shared/DAN-VOICE.md` (rebuilt 2026-10-10, Dan Voice P2B).

**How to write as Dan.** The skill that owns the piece builds a content plan (points, facts, numbers, order, the ask,
length, his own outline wording word for word). The sentences are drafted by the `dan-voice-writer` agent, which runs
`python3 scripts/voice/write.py`: a clean Opus call that sees only 5 whole real passages from the bank
(`_shared/voice/bank/`, picked by format and length, never topic), his own wording, and the plan. Do not polish the
result: fix a wrong fact, a missing point or a hard-rule hit only. For website sales videos and letters and personal
posts, ask Dan for a 3 to 5 minute take and use `/dan-voice` ASSEMBLE instead (80% of sentences stay as he said them).

**Why (bench, 2026-10-10; judges pick the AI piece, chance 50%, goal 60%):** old guide of rules 91%; 5 real passages
and no rules 82% (kept); the same passages plus voice notes 92% (worse); plus a critic and checker revision pass 82%
(no change); 12 passages 80% and Fable as the writer 81% (noise). Rules make Claude tidy and tidy gets caught; a
session that has read writing rules is the losing condition. The Opus judge still catches 39 of 40, so prompting is
near its ceiling. Ledger: `Docs/voice-bench/LEDGER.md`.

**Pieces:** `voice/bank/` and `voice/contrast/` (91 real passages and Claude's cold twins); `voice/POSITIONS.md` (his
takes and stories; no take there or in the outline means ask or a `[DAN: ...]` gap); `voice/STRUCTURE.md` (how he
opens, proves and closes: for the content plan); `voice/CORE.md` and `voice/type-*.md` (the gap list: for reviewing,
never for the writer's prompt); `scripts/voice/voice_check.py` (hard rules plus bands: a tripwire, not a rewrite
list); `dan-voice-critic` agent (second read on request; its "would pass" means little); a hook in
`.claude/settings.json` flags em and en dashes and cut phrases in new text (blocking from 2026-10-17);
`voice/HELD-OUT.md` (never quote; `heldout_guard.py` checks). Raw corpus: `voice-corpus/` (git-ignored) and Drive
folder `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`.

**Open:** Dan's Round 2 blind page (https://claude.ai/artifact/QbzMfnMzQzNsrGDxCyRydK); Phase C (small model trained
on his text) is on by the plan's gate; teleprompter scripts (`--format script`) are unscored, measure by his edit
rate; the voice rules still inside the eight writing skills are background only and due for pruning (Phase D).
Plan: `Handoffs/handoff-20261008-dan-voice-training-part2-plan.md`. Dan's own blind test 10-10: right 13 of 19.
Related: [[scripts-his-wording-not-his-ramble]], [[script-zero-edit-lessons]], [[dan-personal-facts-for-scripts]],
[[no-em-dashes]], [[swearing-never-cut-never-ask]], [[voice-corpus-sources]], [[personal-facts-only-when-relevant]].
