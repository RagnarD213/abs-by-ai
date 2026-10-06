---
name: progress-log
description: "Weight & Progress Log — SHIPPED July 10 2026; endpoints, gating, what's still untested"
metadata: 
  node_type: memory
  type: project
  originSessionId: c1442ef9-2414-4a78-b167-b5f335f757ad
---

Weight & Progress Log SHIPPED July 10, 2026 (commit 367e263), built per repo `HANDOFF_progress_log.md`. Tables `weight_logs` + `progress_entries` (photos base64-in-Postgres), users columns `photo_day`/`weigh_reminder`/`last_photo_nudge`. Endpoints `/api/progress/weight|summary|photo|photo/:id|settings|recap`. Trend = 7-day rolling mean (headline everywhere); rate = 30-day regression, null under 7 logged days. Recap membership-gated (402) via `callTrainerModel`. `getWeightContext()` line injected into [[ai-trainer-membership]] and [[ai-nutritionist]] prompts (same pattern as [[sleep-coach]]). Compare mode posts photo pairs to `/api/transformations` ([[my-transformations]]).

Same commit shipped the rest of Phase 1+2: meal-analysis credit gating (credit consumed past free allowance; refine stays free), password reset (needs `RESEND_API_KEY` + `RESET_FROM` + Resend domain verification — NOT set yet, reset emails silently skipped), Counsel 10/month cap (`COUNSEL_MONTHLY_CAP`), per-user push reminders (15-min sweep, 8 AM local via tzOffset in sub meta: weigh-in, photo day + one follow-up, Sunday meal-prep, Mon/Wed/Fri workout), `eval/meal-eval.js` bias harness.

Untested on prod: recap generation (local Anthropic key invalid), push sweep timing, credit-pack purchase from the meal wall. Membership gap-closure plan + per-model handoffs in `MEMBERSHIP_PLAN.md` / `HANDOFF_membership_*.md` (commit b743a10). [[railway-deploy-workflow]] [[pay-for-generations]]
