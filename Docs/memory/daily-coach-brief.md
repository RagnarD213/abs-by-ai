---
name: daily-coach-brief
description: "Daily Coach Brief shipped July 14 2026 — morning hub card, endpoint, caching, gating"
metadata: 
  node_type: memory
  type: project
  originSessionId: f1bc94f5-9653-418f-94e2-6462d7053d1a
---

Daily Coach Brief (Phase 3 flagship, [[next-phase-plan]] item A1) shipped July 14, 2026 (commit 8a391a0).

- `GET /api/coach/brief?date=YYYY-MM-DD` (requireAuth + aiLimiter): fuses today's sleep check-in, next incomplete workout day, meal-plan targets + meals logged today, and 7-day weight trend.
- Deterministic `facts` returned to ALL logged-in users; AI coach text (headline/notes/focus, Sonnet via callTrainerModel) is members-only.
- Cached in `coach_briefs` table (user_id + brief_date unique) with a sha1 fingerprint of the facts — regenerates only when facts change (new check-in, workout done, weigh-in). Model failure falls back to cached text (`stale: true`) or facts-only; the card never breaks.
- Front-end: `hubBriefCard` on the member hub, rendered by `renderHubBrief()`/`paintBrief()` in index.html; rows tap through to Sleep Coach/Trainer/Nutritionist/Progress Log; lock CTA → membership screen. PostHog: `coach_brief_viewed`, `coach_brief_row_clicked`, `coach_brief_unlock_clicked`.
- Grocery list (plan item D10) was already shipped inside the Nutritionist recipe cards — don't rebuild it.
- Verified locally (pgmem): locked path, facts rows, row navigation. Member AI-text path needs prod verification (beta member account from scripts/provision-beta-member.js).
