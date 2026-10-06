---
name: supplement-audit
description: "AI Supplement Audit (July 16 2026) — photo-based stack audit that replaced the Decision Counsel; architecture, endpoints, prompts, pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea0a2109-4955-400a-a8b1-28cc3023bdc4
---

Shipped July 16 2026 from HANDOFF_supplement_audit.md. Replaces the [[decision-counsel]] as a product but **reuses its five-seat panel engine** unchanged (Researcher, Skeptic, Coach, Safety Officer → President; all `claude-sonnet-5`; resilient parallel calls; `counsel_sessions` table with `decision_type='supplement-audit'`; 10/month cap; free-preview gating; follow-ups). No DB migration.

**Flow:** user photographs each supplement label → AI reads it → short intake → five experts rule → keep/drop verdict + new stack + dollars saved. Members-only with a free teaser (savings total visible, keep/drop + stack locked).

**Backend (server.js):**
- `POST /api/supplement/label` (aiLimiter, optionalAuth, FREE + uncapped — it's the hook). One vision call (`COUNSEL_MODEL`, ~1500 tok, json_schema) reads ONE product: `{product_name, brand, category, is_blend, ingredients[], serving_info, caffeine_mg_per_serving, est_monthly_cost, needs_panel, read_confidence, unreadable}`. If `is_blend` + doses illegible → `needs_panel:true`, frontend reactively asks for the ingredients-panel photo and re-calls with both images. attemptId idempotency cache reused from analyze-meal. Prompt rule: read ONLY the label, never fill a formula from memory.
- `POST /api/counsel` (the audit): gated to `supplement-audit` only. Intake = `{items[], medications(req), budget_monthly(req), max_daily_servings(req), stack_style(req: simplify|optimize), caffeine_other?, sensitivities?, pregnant_nursing?, ...}`. `sanitizeAuditItems()` hard-clamps the structured items. `assembleAuditContext(userId)` pulls a USER CONTEXT block (latest programs.intake, meal_plans.intake, 14d protein avg from meals, weight trend, sleep avg) + the user's stored `before_image` — so seats never re-ask. President schema gained `keep_drop_table[]` (KEEP/DROP/DOWNGRADE/SWAP/ADD per item), `new_stack[]` (generic ingredient/dose/timing/cost, must fit budget+servings), `monthly_savings`.
- `POST /api/supplement/brand` (aiLimiter, requireAuth, members-only, uncapped): on-demand `{brand_pick, product_name, why, price_note, runner_up}` for one generic ingredient. Keeps the main audit unbiased; natural affiliate hook later (out of scope now).

**Prompt recalibration (the judgment core, HANDOFF Phase 5):** `COUNSEL_CHARTER` prepended to all seats + President — bans unearned caution/hedging ("consult a professional" only with a named finding). Coach = **Lead Counselor** (President's default verdict) with Dan's food-first philosophy (DAN TO REVIEW the bullets). Safety Officer: GREEN is the expected rating for standard products; RED requires a NAMED interaction/contraindication/dangerous dose; med-interaction check + total-caffeine math are its two non-negotiable jobs. Skeptic owns the proprietary-blend attack + is skeptical of over-caution too.

**Frontend (index.html):** hub tile 💊 "Supplement Audit"; landing → photo loop (`renderAuditPhotoLoop`, snap label / type-it fallback / reactive panel prompt / remove) → intake (`renderAuditIntake`) → report (`renderCounselReport`) with verdict card, green **savings banner** (the screenshot-shareable artifact), color-coded keep/drop table, "Your new stack" with Recommend-a-Brand buttons, five counselor cards, follow-up box. Reuses `downscaleImage`. PostHog: kept `counsel_opened/started/completed`; added `supplement_label_scanned`, `supplement_brand_requested`.

**Eval harness:** `eval/counsel-eval.js` + `eval/counsel-cases/` (8 JSON cases). POST structured items directly (no photos). Safety canaries are ship gates: case 4 (St John's Wort + SSRI) and case 5 (fish oil + garlic + warfarin) tagged `mustBeRed`; case 1 (sensible basics) `mustBeGreen`. Run `EVAL_AUTH_TOKEN=<member> node eval/counsel-eval.js eval/counsel-cases` for the full keep/drop; safety rating visible even anonymously.

**Verified locally:** validation paths (retired-type 400, incomplete-intake 400, label missing-photo 400), full frontend flow (photo loop, reactive panel prompt, intake gates, report rendering incl. keep/drop + new stack + brand buttons + savings banner). **NOT yet verified on prod:** live vision/seat calls — local .env has an invalid Anthropic key (see [[load-time-optimizations]]), so full end-to-end + the 8 evals (esp. cases 1/4/5) must run against absbyai.com after deploy.

**Pending / for Dan:** review Coach philosophy bullets (5b) + eval outputs (cases 1/4/5) before prompts called done; decide whether free label-scanning stays uncapped; MailerLite broadcast (copy in EMAIL_MARKETING_PLAN.md §7 — Dan sends). Out of scope: affiliate links, barcode/DB lookup, the old "before-you-buy" mini-check.
