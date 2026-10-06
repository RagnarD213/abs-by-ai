---
name: member-profile
description: Shared per-account member profile + pre-trial quiz feeding all AI features (shipped July 18 2026)
metadata: 
  node_type: memory
  type: project
  originSessionId: c2f104e0-74a7-4e55-b7e7-a5a9537b3471
---

Shipped 2026-07-18 (Phases 1–5, all on `main`): one shared profile per account that every AI feature reads and writes back to.

- **Storage:** `users.profile` JSONB column (`db.js`, ADD COLUMN IF NOT EXISTS). Fields: sex, bodyType, intensity, ageRange, heightIn, weight+weightUnit, goal, equipment, diet[], dietNote, plus `_meta` per-field provenance (source+at). Behind auth only — never in URLs/logs.
- **API:** `GET`/`PATCH /api/profile` in `server.js`. `sanitizeProfilePatch` whitelists keys + validates enums/ranges (drops invalid). `writeProfileMerge` = read-modify-write JS merge (pg-mem has no jsonb `||`). `readProfile`/`profileContextBlock` (renders a labeled additive prompt block; `''` when empty → graceful).
- **Quiz:** 5-question "Build your plan" wizard in `public/index.html`, mounted at `continueTrialAfterAccountCreation` (the boundary the bridge task left). `seedProfileFromFunnel` seeds sex/bodyType/intensity; quiz writes the rest; membership screen then shows "Your personalized plan is ready". PostHog quiz_started/step_completed/completed/skipped.
- **Backfill:** `backfillProfile` fills MISSING fields for existing users from newest Trainer/Nutritionist intake + latest weigh-in (runs on login + lazily on first untouched `/api/profile` read via `_meta` gate). Never overwrites quiz/funnel data.
- **Feature reads:** Daily Brief, Sleep Coach, Supplement Audit inject the profile server-side (additive). Trainer + Nutritionist PRE-FILL their intake wizards client-side (`trainerPrefillFromProfile`/`nutriPrefillFromProfile`, answers pre-selected, no step removed). `/api/analyze-meal` deliberately NOT injected (pure photo itemizer).
- **Write-backs:** today weigh-in → profile.weight; Trainer/Nutritionist intake save → backfill gap-fill. Factual only, no LLM inferences.

Verified end-to-end on local pgmem + prod boots healthy each deploy. **Open:** live AI-output eyeball needs a comp account — grant beta via `absbyai.com/admin` (ADMIN_EMAILS login). See [[railway-deploy-workflow]], [[static-serving-and-json-persistence]], [[ai-trainer-membership]], [[ai-nutritionist]].
