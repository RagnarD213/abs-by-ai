# HANDOFF — Billing & entitlement correctness review (OPTIONAL)

**Run with: Claude Opus 4.8, HIGH reasoning effort.** (Originally slated for Fable 5 — Opus is sufficient; this is careful review of known failure patterns, not novel design.) Run this LAST, after the Sonnet and Opus tasks have shipped. Skip entirely if budget is tight and no anomalies have appeared.

**Context/authorization:** This is a defensive code-correctness review of our own application (this repo, absbyai.com, owned and operated by Dan). Goal: find bugs that would cause us to lose revenue, double-charge a customer, or grant paid features unintentionally — so we can fix them before going live.

## Scope — review, don't build

Read-only review of `server.js`, `db.js`, `index.html` payment/entitlement paths; produce `AUDIT_membership.md` with findings ranked by severity, each with a concrete failure scenario and a minimal fix. Apply ONLY fixes that are small and obviously correct; anything structural goes in the report.

## Specific correctness questions to examine

1. **Webhook idempotency & ordering**: `checkout.session.completed` vs. return-redirect fulfillment (`fulfillCreditsSession` uses a `fulfilled` map persisted to GitHub — what happens on concurrent webhook + redirect, or a Railway restart between grant and persist?). Same for membership activation vs. `customer.subscription.updated` racing. Risk: double-granting or losing a paid purchase.
2. **Credit linking on login** (`/api/auth/login` folds device balances into the account's canonical device): could alternating logins from two devices miscount balances? The implicit `FREE_CREDITS` default in `getCredits()` for never-seen device ids — does clearing localStorage reset the free allowance, and is that an accepted product tradeoff? State the conclusion either way so Dan can decide.
3. **Counsel monthly cap**: `COUNSEL_MONTHLY_CAP` counts `counsel_sessions` rows — do anonymous-then-linked runs count correctly? Are non-member preview runs counted fairly against members?
4. **Meal-analysis credit consumption** (`/api/analyze-meal`): charge-on-success semantics vs. client retries (`fetchWithRetry`) — could a timeout-and-retry deduct two credits for one analysis? Is the 402 branch correct after a restart mid-persist of the in-memory `creditsStore`?
5. **Membership expiry boundary**: `isActiveMembership` vs. `membership_period_end` timezone/clock skew; `past_due` handling; which gates read a stale user row vs. fresh session data.
6. **Password reset** (new): token single-use behavior under two parallel resets, session invalidation completeness, and whether `request-reset` responses are uniform regardless of account existence.
7. **GitHub-file persistence** (`credits-data.json`, `push-subs.json`): last-writer-wins between concurrent instances — is Railway ever running 2 instances (check config)? Quantify worst-case data loss.

## Ground rules

- Every finding needs a reproducible scenario grounded in the actual code (quote line refs) — no vibes.
- Prioritize: customer double-charge > revenue loss > unintended free access > data loss > polish.
- No dependency changes, no refactors.
