---
name: load-time-optimizations
description: "Generation load-time work — photo downscaling, Haiku prompt step, keep-warm; and the local-preview API-key gotcha"
metadata: 
  node_type: memory
  type: project
  originSessionId: 75fbbea8-b232-4eec-bf5f-ef4f4b79f427
---

Abs by AI generation was losing users to slow load (a tester bailed before seeing her result). Fixed 2026-06-22 (commit 333eb63, live on absbyai.com):

- **Client-side photo downscale** (`downscaleImage` in index.html, used in `handlePhoto`): resize to ≤1024px + JPEG 0.85 before upload. Measured ~87% payload reduction (4000×3000 1.7MB → 1024px 219KB). Images already ≤1024px pass through untouched. Biggest win on slow mobile connections — the photo otherwise travels phone→Railway→Gemini at full size.
- **Prompt step Sonnet 4.6 → Haiku 4.5** (`/api/generate-prompt`, server.js ~1219), max_tokens 2048→1024. Haiku already used elsewhere in the same server (lines 738/1139), so the model id is proven-valid. Live timing ~1.5–3.3s.
- **Keep-warm heartbeat**: `setInterval` self-ping of `/health` every 4 min near `app.listen`, hits `RAILWAY_PUBLIC_DOMAIN` if set else localhost. Removes cold-start stalls.
- **Perceived-speed loader** (added 2026-06-22, commit d1c35cd): `generate()` now calls `startGenLoader()`/`finishGenLoader()`/`clearGenLoader()` instead of the old `setStatus` spinner. `#genLoader` in index.html shows the user's own (downscaled) photo under an animated AI "scan" (sweeping line + grid + reticle brackets), a front-loaded progress bar easing to a 92% asymptote then snapping to 100% on arrival, and body-specific rotating copy driven by `GEN_STAGES` (text synced to progress %). Honors prefers-reduced-motion. Both loaders now share one `makeProgressLoader({card,bar,pct,status,scan})` controller (commit c6894ba): the initial-generation loader (`startGenLoader`) and the result-screen regenerate loader (`startResultLoader`, used by `adjustIntensity`). On the result screen the AI scan overlays the existing `#afterImg` (`.after-scan`) and a progress card (`#resultGenLoader`) replaces the old spinner. Legacy `setStatus`/`setResultStatus` + their hidden status sections are kept as fallbacks. Copy is split: `GEN_STAGES` (generate — deliberately masculine/bro-ey, user's call) vs `REGEN_STAGES` (regenerate — context-aware: "Re-reading your goal…" etc.), selected via a per-loader `stages` option on `makeProgressLoader`.

**Measured before/after (on prod, 2026-06-22):** prompt step Sonnet 4.6 ~11.5s → Haiku 4.5 ~8.0s (real ~3.5s saved every time, via a temp token-gated `/api/_bench` endpoint that was added, measured, then removed). Photo payload 3.6MB → 0.32MB (91%) on a 3024×4032 photo; upload-time saved scales with connection (~1–2s good wifi, ~5s 4G, ~13–17s weak mobile — and the photo uploads twice, phone→server→Gemini). Gemini image step unchanged (~10–20s floor). Net full-generation: ~28s→~23s good wifi, ~45s→~25s weak mobile (~45% faster — the abandoning tester's case). Couldn't cleanly isolate upload time in a single live round-trip (Gemini per-request variance too high); byte delta is exact, upload time computed from it.

**Gotcha for local testing:** the Claude Preview server (preview_start name `abs-by-ai`, port 3000) boots with an INVALID `ANTHROPIC_API_KEY` — any Anthropic-backed endpoint returns `{"error":"invalid x-api-key"}` locally. GitHub-token features (credits store) DO work locally. To test Claude/Haiku endpoints, hit production (`https://absbyai.com/...`) which has real keys. The Gemini image step (~10–20s) is the unchanged floor. See [[railway-deploy-workflow]], [[pay-for-generations]].
