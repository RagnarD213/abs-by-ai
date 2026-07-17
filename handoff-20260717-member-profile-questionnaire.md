# Handoff: Shared member profile + trial questionnaire

**Date:** 2026-07-17
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability (higher trial conversion via investment/personalization) + app adoption (features feel connected; no repeated questionnaires)

## Objective

Build one shared **member profile** per account that becomes the single source of context for every AI feature (Trainer, Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit, Daily Brief), plus a short 5–6 question "Let's build your plan" questionnaire that fills its essentials during trial signup. After this ships, no feature ever re-asks a question the profile already answers, and each feature quietly enriches the profile as it's used.

**Prerequisite:** `handoff-20260717-bridge-hub-trial-gate.md` must be done first — it creates the trial-gate flow this questionnaire slots into, and deliberately leaves a single function boundary between "account created" and "open membership checkout" for this insertion.

## Current State

- Backend `server.js` (~6,630 lines, Express + Postgres via `db.js`; pgmem fallback locally). Accounts exist (email + password auth, session-based; see memory: accounts-member-hub).
- Each feature currently collects its own context ad hoc: the Trainer has its own intake (sex, equipment tiers none/min/full, 7-stage ladder — memory: trainer-v3-ladder), the Nutritionist asks diet questions, Sleep Coach and Supplement Audit have their own intakes, and the generation form collects sex/body type/intensity. These live in scattered localStorage keys and per-feature server rows — there is no unified profile.
- Feature prompts are built server-side in `server.js` and call the Anthropic API (this is why this task is Claude-owned — it touches the Anthropic prompt-construction code).
- The bridge/trial-gate task defines where the questionnaire mounts: after account creation, before `showMembershipScreen(...)`.

## Key Decisions Already Made

- **Short quiz before the trial gate, rest after** — 5–6 essentials only, framed as "Let's build your plan," so the trial paywall can say "Your personalized plan is ready — start your 7-day free trial to unlock it." Rationale (settled, don't relitigate): effort-investment before a paywall raises conversion (Noom/Fitbod pattern), but Abs By AI's own after-photo already does the heavy personalization lift, so a long quiz would be redundant friction.
- The essential questions (one per screen or one compact screen — executor's choice, mobile-first): age range, height + weight, primary goal (lose fat / build muscle / both), equipment available (none / minimal / full gym — must map to the Trainer v3 tiers), dietary constraints/preferences. Sex is already known from the generation form — carry it in, don't re-ask.
- Profile is **server-side, one record per account** (not localStorage) — it must follow the user across devices and into the native apps. localStorage may cache it.
- Every feature both **reads** the profile (pre-fill intakes, skip known questions) and **writes** back what it learns (e.g., logging meals teaches typical diet; trainer progression updates fitness level).
- Anonymous (pre-account) funnel data — sex, body type, intensity, goal photo, email — seeds the profile at account creation.
- Migration behavior for the 4 existing real users: on next login, backfill their profile from whatever per-feature data exists; ask only for missing essentials the next time they open a feature that needs them. No mass re-onboarding.

## Detailed Plan

1. **Schema:** add a `profiles` table keyed by user id (or a JSONB `profile` column on the existing users table — decide based on how `db.js` migrations are structured; JSONB is likely the pragmatic fit for evolving fields). Fields: essentials above + `updated_at` per-field-group provenance so features can tell fresh data from stale.
2. **API:** `GET /api/profile` and `PATCH /api/profile` (auth-required), with server-side validation. PATCH is merge-semantics so features can write single fields.
3. **Questionnaire UI:** new screen(s) in `index.html`, mounted at the boundary the bridge task left (post-signup, pre-checkout). Progress dots, one tap per answer where possible, "Building your plan…" transition into the membership screen with the "Your personalized plan is ready" framing. PostHog: `quiz_started`, `quiz_step_completed` (step name), `quiz_completed`.
4. **Seed from funnel:** at account creation, write sex/body type/intensity/goal-photo reference and email-capture data into the profile.
5. **Refactor features to read the profile** (the careful part — one feature at a time, verifying each on production before the next):
   - Trainer: pre-fill sex/equipment/fitness level; skip intake steps that are answered.
   - Nutritionist + Macro Tracker: dietary constraints, goal, weight.
   - Sleep Coach and Supplement Audit: pull age/goal context into their prompts.
   - Daily Brief: read everything for tighter briefings.
   In `server.js`, thread profile fields into each feature's Anthropic prompt-builder rather than duplicating questions. Do not change model choices, safety settings, or output contracts of existing prompts — additive context only.
6. **Write-back hooks:** meal logs update dietary patterns; trainer progression updates fitness level; progress-log weigh-ins update weight. Keep write-backs small and factual — no LLM-generated inferences stored as facts.
7. **Migration/backfill** for existing users per the decision above.
8. Verify each feature end-to-end on production (local Anthropic key is invalid), including one full new-user run: generate → trial gate → quiz → checkout page → feature opens pre-filled.
9. Commit, push, confirm Railway deploy, verify live (AGENTS.md).

## Things to Avoid / Lessons Learned

- Do not lengthen the pre-trial quiz beyond ~6 questions — the decision is deliberate; friction here is paid at the highest-value moment of the funnel.
- Don't break existing per-feature intakes for users with no profile data — every read must degrade gracefully to the current ask-the-user behavior.
- Anthropic calls have an established timeout pattern (AbortController, 4-min per attempt — see server.js:3795 and the Supplement Audit fix in commit 751fe7b). Any new/modified call must use it.
- Prompt changes are regression-prone: the Supplement Audit and Trainer have tuned prompts with eval history (see `eval/`) — add profile context without rewording existing instructions.
- Health data caution: the profile holds age/weight/diet — keep it behind auth, never in URLs, and don't log it.

## Relevant Files & Locations

- `server.js` — auth + accounts, feature endpoints and Anthropic prompt-builders (Trainer/Nutritionist/Sleep/Audit/Brief), timeout helper ~3795
- `db.js` — Postgres setup/migrations pattern
- `index.html` — trainer/nutrition/sleep/counsel intake screens (search `data-feature`, `counselIntakeSection` 1977, `trainerSection` 1893, `nutritionSection` 1929)
- Companion: `handoff-20260717-bridge-hub-trial-gate.md` (prerequisite), `TRAINER_V3_WORKOUTS.md`, `eval/`
- Live: https://absbyai.com · Railway auto-deploy from `main` · PostHog project 458833

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Opus, extended thinking |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5, standard thinking — escalate the schema/prompt-threading design decisions to Opus if they get gnarly |

**Always-Claude task** regardless of usage: this is cross-cutting architecture (one profile feeding six features — wrong shape is expensive to unwind) and it edits the Anthropic prompt-construction code. Don't hand this one to Codex. Optionally: have Claude design the schema + API + refactor plan, then let Codex execute the mechanical per-feature refactors under that plan if budget is tight.

## Starter Prompt for the Next Task

> Read `handoff-20260717-member-profile-questionnaire.md` in the Abs By AI repo root and implement it. Prerequisite: the bridge/trial-gate handoff must already be live. Start with the profile schema decision (JSONB column vs. table — inspect `db.js` migrations first) and the GET/PATCH `/api/profile` endpoints, then the 5–6 question pre-trial quiz at the boundary the bridge task left, then refactor features one at a time to read/write the profile, verifying each on production before the next. Do not reword existing Anthropic prompts — add profile context only. Follow AGENTS.md: commit, push, verify Railway deploy and absbyai.com live, and explain the work in plain language.
