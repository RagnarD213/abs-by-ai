# MEMBERSHIP — Finalized Plan (July 10, 2026)

**Goal:** one paid membership unlocks everything — full training program + rebuilds, unlimited image generations, unlimited AI meal tracking, AI Nutritionist, Sleep Coach full briefings, My Transformations, Progress Log AI recap, and **10 Decision Counsel sessions per month**.

## What already exists (do not rebuild)

- Stripe subscription checkout (monthly $9.99 / annual $59.99), embedded, with credit-conversion discount (`/api/stripe/create-membership-checkout`, `server.js`).
- Webhook keeps `users.membership_status/plan/period_end` in sync across renewals, cancellations, and payment failures (`customer.subscription.updated/deleted`).
- `isActiveMembership()` gating on every feature endpoint, incl. (new today) meal-analysis credits and the 10/month Counsel cap (`COUNSEL_MONTHLY_CAP` in server.js).
- Membership screen UI with plan cards + benefits list (`#membershipSection`, index.html).

## Gaps to close (the actual plan)

| # | Work item | Model / effort | Handoff doc |
|---|-----------|----------------|-------------|
| 1 | Member-facing copy: welcome email, hub "Member" badge copy, membership FAQ/cancel policy blurb | **Haiku 4.5 · low** | `HANDOFF_membership_haiku_low.md` |
| 2 | Manage-membership: Stripe billing portal endpoint + "Manage membership" card in the hub (status, plan, renewal date, cancel link); `past_due` grace messaging | **Sonnet 5 · medium** | `HANDOFF_membership_sonnet_medium.md` |
| 3 | Live-mode cutover runbook + prod verification of the full paid path (subscribe → gates open → cancel → gates close), incl. the two untested prod flows (member full meal plan, Counsel photo direction) | **Opus 4.8 · medium** | `HANDOFF_membership_opus_medium.md` |
| 4 | iOS App Store: membership purchase strategy (Apple IAP vs. external-link entitlement), StoreKit/Capacitor design, entitlement sync with Stripe-side membership | **Opus 4.8 · high** (same doc as #3, part B) | `HANDOFF_membership_opus_medium.md` |
| 5 | (Optional, only if issues suspected) Cross-cutting entitlement & payment-race audit: webhook idempotency, credit-linking on login, cap bypass vectors, downgrade timing | **Fable 5 · high** | `HANDOFF_membership_fable_high.md` |

**Model rationale:** copy tasks need no reasoning depth (Haiku). Item 2 follows existing, well-documented server/UI patterns — Sonnet executes patterned code reliably at a fraction of the cost. Item 3/4 require multi-system judgement (Stripe live mode, Apple policy) — Opus. Fable is reserved for the one task where a missed subtle bug costs real money (payments/entitlement audit), and it's optional.

**Order:** 1 and 2 can run in parallel → 3 (needs 2 deployed) → 4 → 5 last (audits the finished system).

**Dan's prerequisites (no model can do these):**
- Stripe live products + `STRIPE_SECRET_KEY`/`STRIPE_PUBLISHABLE_KEY`/`STRIPE_WEBHOOK_SECRET` (live) on Railway.
- Resend account + `RESEND_API_KEY`, verify absbyai.com sending domain (also needed for password reset, shipped today).
- Apple Developer account decisions in item 4 will need your sign-off (IAP takes 15–30% commission).
