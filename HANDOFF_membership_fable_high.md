# HANDOFF — Entitlement & payment-race audit (OPTIONAL)

**Run with: Claude Fable 5, HIGH reasoning effort.** Only task in the membership plan that justifies Fable: a missed subtle bug here silently gives away paid features or double-charges. Run this LAST, after the Sonnet and Opus tasks have shipped. Skip entirely if budget is tight and no anomalies have appeared.

## Scope — audit, don't build

Read-only review of `server.js`, `db.js`, `index.html` payment/entitlement paths; produce `AUDIT_membership.md` with findings ranked by severity, each with a concrete exploit/failure scenario and a minimal fix. Apply ONLY fixes that are small and obviously correct; anything structural goes in the report.

## Specific vectors to examine

1. **Webhook idempotency & ordering**: `checkout.session.completed` vs. return-redirect fulfillment (`fulfillCreditsSession` uses a `fulfilled` map persisted to GitHub — what happens on concurrent webhook + redirect, or a Railway restart between grant and persist?). Same for membership activation vs. `customer.subscription.updated` racing.
2. **Credit linking on login** (`/api/auth/login` folds device balances into the account's canonical device): can alternating logins from two devices mint credits? What about the implicit `FREE_CREDITS` default in `getCredits()` for never-seen device ids — can wiping localStorage farm free credits/meal analyses? (Known/accepted? — state it either way.)
3. **Counsel cap**: `COUNSEL_MONTHLY_CAP` counts `counsel_sessions` rows — can a user avoid row-insert (e.g., anonymous run, then link) to bypass? Are non-member preview runs counted fairly?
4. **Meal-analysis credit consumption** (in `/api/analyze-meal`): charge-on-success semantics vs. client retries (`fetchWithRetry`) — can a timeout-and-retry double-spend a credit? Is the 402 branch reachable with a stale in-memory `creditsStore` after a restart mid-persist?
5. **Membership expiry boundary**: `isActiveMembership` vs. `membership_period_end` timezone/clock skew; `past_due` handling; what gates check `req.user` freshness (session row) vs. a stale row.
6. **Password reset** (new): token single-use race (two parallel resets), session invalidation completeness, enumeration timing side-channel on `request-reset`.
7. **GitHub-file persistence** (`credits-data.json`, `push-subs.json`): last-writer-wins between concurrent instances — is Railway ever running 2 instances (check config)? Quantify worst-case loss.

## Ground rules

- Every finding needs a reproducible scenario, not a vibe. Confirm against the actual code paths (quote line refs).
- Prioritize: money loss > free-feature leak > data loss > polish.
- No dependency changes, no refactors.
