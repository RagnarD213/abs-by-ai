---
name: female-generation-fix
description: "Female transformation fixes SHIPPED July 16 2026 via overnight scheduled tasks; prod verification pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 365f6983-9286-4f47-acd0-d4284fea6070
---

Women's transformations underperform men's for three diagnosed reasons: (1) sex toggle defaults to Male and is never checked against the photo, so women get male prompts → Gemini refusals or near-copy outputs (confirmed via user screenshot showing the male body-fat table on a female photo); (2) `/api/generate-image` sends no `safetySettings`, so Google's strict defaults block many sports-bra/swimwear photos; (3) FEMALE rules in SYSTEM_PROMPT are written soft (20% BF target, "never masculine" hedging).

**SHIPPED July 16 2026** via overnight scheduled tasks (commits on main, deployed): `a420990` (sex auto-detect, safetySettings, dramatic female prompt), `9fd25fe` (female dramatic/max intensity matches male), plus `9ba7579` ("Fix my result" feedback-driven edit pass — separate feature, same batch). Live-site verification with a real female photo is still pending, as is Phase 3 below.

The original execution plan (Phases 1+2: sex auto-detect via check-photo, safetySettings BLOCK_ONLY_HIGH, retry-on-block with friendly errors, forceful female prompt rewrite, female BF anchors lowered to dramatic 18–20% / max 16–18% / floor 16%) is in repo `HANDOFF_female_generation.md`, recommended to run with Sonnet 5 medium. Phase 3 (deferred): post-generation before/after change scoring with auto-regenerate, plus PostHog logging of block rates. Related: [[load-time-optimizations]] (check-photo is the same Haiku step), [[pay-for-generations]] (blocks waste the credit UX but never double-charge).

**Phase 3 SHIPPED July 18 2026** (`handoff-20260718-female-dramatic-and-items-3-7.md`): A1 per-generation telemetry (client sends `sex`; server logs `GEN_TELEMETRY` + returns a `telemetry` object → PostHog `generation_verifier`), A2 the gender-aware change-verifier + intensify-retry on ALL intensities (female every intensity, male moderate+) + a `weakChange` client nudge. **KEY, NON-OBVIOUS FINDING (verified live): the "female after looks the same" failure was mostly a MALE-BIASED VERIFIER, not the image generator under-changing.** The old `looksDramaticallyChanged` asked only about a male six-pack/serratus, so it rejected legitimately feminine results and burned retries: the SAME female proof photo at `dramatic` went from `verifierPassedFirstTry:false`+2 wasted retries+`finalVerifierPassed:false` (A1) → **passes first try, 0 retries** once the verifier became gender-aware (A2, `buildVerifierQuestion(sex,intensity)` → feminine four-pack/midline/oblique/taper). Quality win + Gemini-cost win. Also shipped Item 4 (realistic/dream toggle, default Dream unchanged), Item 5 (before/after share card), Item 7 (tailored Gemini-block copy). **A3 (lower female BF anchors + stronger female prompt) is PAUSED — Dan chose to eyeball real female photos on prod first, since A2 may have already fixed the no-op**; Item 6 (prompt trim) deferred/likely-skip. Full state in repo `AI_COORDINATION.md`.
