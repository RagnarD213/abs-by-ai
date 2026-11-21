---
name: ai-ad-creation-research
description: "AI-generated ad research (2026-07-29) — MadMuscles theme system + current winners with YouTube IDs, recommended AI video toolchain, and the 10 ad concepts pitched to Dan"
metadata: 
  node_type: memory
  type: project
  originSessionId: 27de5e92-3562-4169-b0ad-997d965b39d3
  modified: 2026-07-29T23:20:21.751Z
---

Deep-dive follow-up to [[youtube-ad-competitor-research]], focused on AI-GENERATED ads and how to make them.

**MadMuscles creative factory (from VidTao 2026-07-29 + web2appworld breakdown):**
- ~$29.4M/mo YouTube, ~18,000 AI-generated ads launched, all-time top creative (podcast-style tai chi story) = $14.2M lifetime.
- Filenames encode everything: `tm1(theme)_tm2(subtheme)_gM/gF_9x16_len`. Current wave is 100% `tm1(military)_tm2(workout)`; tai chi wave (54% of spend in Jan) is retired for men but sister brand **HARNA** (same publisher AmoApps) runs the identical tai chi playbook at women with a grandma character ($36k/30d).
- Pattern: 9:16, 60–110s, AI character + AI VO, 5–10 versioned variants per script, kill at ~$5k, scale winners to $200k+.

**Current winners w/ YouTube IDs (pulled from VidTao embed players):** "New Respect" military street-interview $224.8k/30d = lfa71t4RAyw; "popitlikethis" $115.5k = HZLYJPGi8gI; "respectguyhk" $59.7k = BKj3GNnWhvI; male tai chi VAR8loamaz $25.9k = 3-dC0_qRXd0; "DG1legalv9mil" $24.3k = Xvzk4fQnxas.

**Toolchain recommended to Dan (2026-07-29):**
- Key insight: no one generates 90s in one shot — ads are 8–15s clips stitched in an editor with ONE continuous VO carrying continuity.
- Main engine **Veo 3.1** (native lip-synced dialogue, 9:16, reference-image character consistency; via the Gemini API account we already have). Value alt **Kling 3.0** (multi-shot subject consistency; on Replicate, account we already have). **Hailuo 2.3** for cheap B-roll. **ElevenLabs** for one cloned narrator voice. **CapCut** for 9:16 assembly + bold auto-captions.
- Character consistency = character bible (never change wardrobe) → character sheet stills via Nano Banana Pro/Seedream → feed as reference into every clip.
- ~$10–40 generation cost per finished 90s ad.
- Our unique edge: the product itself produces the before/after — generate "after" frames through the LIVE product pipeline (per [[proof-banner-image-gen-process]]) and animate from them.

**10 ad concepts pitched (Dan to pick):** 1 Drill Sergeant Test (their $224k format + our future-self photo), 2 Tai Chi Master's First Lesson, 3 Calisthenics Elder, 4 Podcast Confession, 5 The Upload (pure product demo), 6 Two Futures split-screen, 7 The Mirror Talks Back, 8 Every Mission Needs a Target Picture, 9 The AI Roast (humor), 10 Dad's Photo (emotional). Claude recommended starting with 1, 2, 5.
