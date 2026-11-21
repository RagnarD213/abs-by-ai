---
name: ai-trainer-membership
description: "AI trainer + membership feature — architecture, endpoints, what's pending before it can sell"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5f1252c4-a943-4537-96a3-dabf348e896a
---

Shipped July 7, 2026 (commit 618ded1, deployed to prod and verified). Built from HANDOFF_ai_trainer.md.

- **Membership**: Stripe subscriptions $9.99/mo (`monthly`) / $59.99/yr (`annual`) via `MEMBERSHIP_PLANS` in server.js; embedded checkout `/api/stripe/create-membership-checkout` (requires login). Credits convert at $1 each as a one-time Stripe coupon (only EXPLICIT `creditsStore.balances` entries convert — untouched free devices have none). Member state = `membership_*` columns on users, synced by webhook (`checkout.session.completed` + `customer.subscription.updated/deleted`).
- **Trainer**: 9-step intake (free, works logged-out) → `POST /api/generate-program` (claude-sonnet-4-6, structured JSON, whitelist-constrained to exercises.js ~77 moves, optional before-photo vision with consent toggle). Non-members get stripped preview (why-this-works + structure + Day 1 free); full program persisted in Postgres `programs` table for logged-in users. `GET /api/program`, `POST /api/program/progress`, `POST /api/program/checkin` (member-only, regenerates next block from completion data).
- **Gating**: meal analyses 3 free per device (`creditsStore.mealCounts`, 402 + needsMembership after), members unlimited meals AND image generations.
- Anonymous program → subscribing regenerates from localStorage intake (`absbyai_trainer_intake`) once authed.

**Pending before it can sell:**
1. Stripe dashboard: add `customer.subscription.updated` and `customer.subscription.deleted` to the webhook endpoint's enabled events (Dan action) — otherwise cancellations never downgrade members.
2. Exercise video curation: all `video: null` in exercises.js (spawn-task chip created; UI hides the button until filled).
3. A real end-to-end subscription purchase test (Stripe test mode or a real $9.99) — checkout/coupon path only unit-verified.
4. Workout-day push notifications (plan step 5, optional) not built — existing `/api/push/*` is single-list dashboard infra, would need per-user subs.

Related: [[accounts-member-hub]], [[pay-for-generations]], [[railway-deploy-workflow]].
