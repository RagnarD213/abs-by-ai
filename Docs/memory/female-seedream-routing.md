---
name: female-seedream-routing
description: "Women's generations run Gemini + Seedream 4.5; men keep Gemini + FLUX Kontext — shipped 2026-07-28, with Dan's blind-label evidence"
metadata: 
  node_type: memory
  type: project
  originSessionId: cf3e4111-56dd-41d2-906e-71a9b5973c51
  modified: 2026-07-29T23:56:36.429Z
---

Shipped 2026-07-28 (commit `8bee66c`). `server.js` picks the second ensemble
candidate by `sex`: **female → Seedream 4.5** (`bytedance/seedream-4.5` via
Replicate), **male / unknown → FLUX Kontext**. FLUX refuses ~75% of female
photos (E005) with `safety_tolerance` already at its image-input max of 2.

**Dan's blind labels, 12 rows across 4 women: Seedream 9, Gemini 2, neither 1 —
and 6 of 6 at the Ripped tier.** The models fail in opposite directions and this
is the durable finding: **Gemini under-changes** (tagged "not enough change" 7×,
never won a Ripped row), **Seedream over-changes at the Subtle tier** (too
muscular / looks fake, 5×). Skin tone was right for both on essentially
everything. Labels live in `bakeoff/round2-female/out/labels.json` and
`bakeoff/round3-female/out/labels.json`.

CLOSED 2026-07-29 (commit `cec8020`): the judge was validated on the 14 female
labels — it was **tier-blind, not female-blind** (85.7% agreement with Dan at
Ripped, 42.9% at Subtle). Fixed by making the judge tier-aware for female
sub-max generations only: a Subtle tier note + one female exemplar
(`assets/judge-exemplars/ex4-*`) appended after the prompt-cache breakpoint,
plus `JUDGE_SUBTLE_WEIGHTS` (defCap 4, overPenalty 1.5 — rewards stop above the
modest target the way underPenalty punishes below it). Female Subtle agreement
83.3%; male and female-Ripped judging byte-identical, male eval unchanged at
80.5%/100%. Eval harness: `bakeoff/judge-eval-female.js` (TIER_FIX=1), all
calls disk-cached so re-runs are $0. The lean-woman gap also closed 2026-07-28
(`fem-lean-real`, a real subject Dan supplied).

Related: [[bakeoff-round1-aesthetic]] (shredded-not-bulky, condensed prompt),
[[repo-is-public]] (why round-3 photos are gitignored).
