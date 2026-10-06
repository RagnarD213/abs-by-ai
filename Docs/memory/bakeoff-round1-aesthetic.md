---
name: bakeoff-round1-aesthetic
description: "Dan's labeled model bake-off (round 1) — his aesthetic is shredded-not-bulky, no tan; the condensed prompt is what delivers it"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3763fe6a-df39-4ce6-bd11-052d516107e8
  modified: 2026-07-24T21:30:48.809Z
---

Round-1 blind model bake-off, labeled by Dan 2026-07-24 (ground truth in `bakeoff/round1/labels.json`, blind key `key.json`, harness in `bakeoff/`).

**Dan's aesthetic, from 80 labels:** shredded/defined abs at low body fat, NOT muscular/bulky, NO added tan, not oiled, natural not airbrushed. Complaint totals: too muscular **33**, too tan **23**, looks fake **20**, not enough change 17. "just right" notes always describe max ab definition with minimal added mass and preserved skin tone.

**Biggest lever:** the **condensed prompt variant** (drops the SKIN TONE tan block + the +lb muscle-anchor language) won **8 of Dan's 10 best picks**; the full production SYSTEM_PROMPT won only 2. Our own prompt is what produces the over-muscled/over-tanned look he rejects — see [[female-generation-fix]] and the tan block ~line 3061 of public/index.html.

**Model read (his best-count):** gpt-image-1.5 ×4 (best-looking but 57s/~19¢/wrong aspect — production headache), flux-kontext ×2, seedream-4.5 ×2 (won skin-tone cases, 0 moderation blocks, fast/cheap — strongest practical pick), gemini-2.5-flash ×1 (never over-muscles but under-changes), nano-banana-pro ×1 (reliable "acceptable", rarely best), flux-2-pro ×0 (dead last — drop it). flux-kontext still refuses all female photos.

**Unsolved:** max/Ripped on a hard body (heavier or Dan's own selfie) got NO acceptable best — models overshoot to bodybuilder OR barely change. The intensity ladder needs a Kino ceiling, not "more."

**Judge:** current prod judge (server.js ~2349) is instructed to pick "more dramatic, more muscular, more defined" — literally optimizing for the 33 "too muscular" rejections. Phase 3 rebuilds it against these labels. Ties to [[next-phase-plan]].
