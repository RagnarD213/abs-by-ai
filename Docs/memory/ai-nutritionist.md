---
name: ai-nutritionist
description: "AI Nutritionist feature — architecture, endpoints, design decisions, and what's still pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5f381cde-e3c2-46c1-aece-98e9cf9449ea
---

Shipped July 9, 2026 (commits ecc92f4 → schema fix). Mirrors the [[ai-trainer-membership]] architecture.

**How it works:** 7-step intake wizard (photos or goal fallback → sex/age/height/weight → activity → health goals + GLP-1 question → favorite foods → allergies/diet/dislikes → cooking effort). Server computes maintenance via Mifflin-St Jeor × activity in `computeNutritionTargets()` (server.js), with hard calorie floors (M 1500 / F 1200) and protein ≈0.9 g/lb of goal weight capped at 220 g. Claude (sonnet, `MEALPLAN_SCHEMA` structured output) picks targets inside the server range from the before/after photo gap and builds 3 rotating 10-serving Sunday meal-prep recipes (2 portions/day Mon–Fri, flexible breakfast/snacks budget, weekend guardrails). `sanitizeMealPlan()` clamps model numbers back into the rails.

**GLP-1 users:** calories_mode = "floor" (eat at least), protein-dense smaller portions — the medication creates the deficit; the risk is muscle loss.

**Endpoints:** POST /api/generate-mealplan (free, preview-stripped for non-members — targets/assessment/recipe names free, ingredients+steps members-only), GET /api/mealplan, POST /api/mealplan/swap (regenerate one recipe at same macros, member-only), POST /api/mealplan/checkin (new weight → recomputed targets + fresh plan, member-only). Storage: `meal_plans` table (db.js). Targets feed the macro tracker via localStorage `absbyai_nutrition_targets` ("X / Y cal" display).

**Gotcha found during build:** `callTrainerModel()` hardcoded PROGRAM_SCHEMA in output_config; now takes a schema param — pass the right schema for any new AI feature reusing it.

**Pending:** Sunday "prep day" push notification (web push infra exists, not wired); member/paid full-plan flow untested on prod (only preview path tested end-to-end); no PostHog funnel review yet.
