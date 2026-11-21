# HANDOFF — Manage membership (billing portal + hub card)

**Run with: Claude Sonnet 5, MEDIUM reasoning effort.** Patterned backend + frontend work; every pattern to copy is named below. No novel design decisions — where ambiguous, follow the closest existing pattern in the file.

## Context

- `server.js` (~4600 lines): Express, all endpoints in one file. Stripe already configured via `getStripe()`; membership state lives on `users` (`membership_status`, `membership_plan`, `membership_period_end`, `stripe_customer_id`, `stripe_subscription_id`). `isActiveMembership(userRow)` is the gate. `GET /api/membership` returns `{ active, plan, periodEnd, creditDiscountCents }`.
- `index.html`: single-page app; screens are divs registered in the `showScreen` list; `authApi(path, opts)` is the fetch wrapper (throws with `.status`); the member hub is `#hubSection` / `showHub()`; membership UI is `#membershipSection` / `showMembershipScreen()`.
- Local dev: `DATABASE_URL=pgmem://` in-memory Postgres; Stripe calls need real test keys, so verify Stripe paths by code-review + prod, everything else via local preview.

## Task 1 — Billing portal endpoint (server.js)

`POST /api/stripe/create-portal-session` — `requireAuth`. Load the user row (`getUserRow`); 400 if no `stripe_customer_id`. Create a Stripe billing portal session (`stripe.billingPortal.sessions.create({ customer, return_url: SITE_URL })` — `SITE_URL` const already exists). Return `{ url }`. Copy error-handling shape from `create-membership-checkout`.

## Task 2 — Manage-membership card in the hub (index.html)

In `showHub()`/hub rendering: if `memberState.active`, show a card (follow `hub-tile` markup style) with: plan name, "Renews <periodEnd date>" (or "Ends <date>" if `membership_status` is set to cancel — expose `cancelAtPeriodEnd` from `GET /api/membership` if the webhook stores it; if it doesn't, just show the date), and a "Manage membership" button → calls the portal endpoint → `window.location.href = url`. Also un-hide the `hubMemberFaq` block if present (created by another task; guard with `if ($('hubMemberFaq'))`). If not a member, show a compact "Become a member" tile → `showMembershipScreen(() => showHub())`.

You'll need `GET /api/membership` data at hub load — `refreshMembership()` already fetches it; extend `memberState` with `periodEnd`/`plan` (the endpoint already returns them).

## Task 3 — past_due grace messaging

Webhook already records `membership_status`. In `GET /api/membership`, add `status` to the response. In the hub card, if status is `past_due`, show an inline warning: "Payment issue — update your card to keep your membership" with the same Manage button.

## Verification

1. `node --check server.js`.
2. Local preview (`pgmem`): signup → hub shows "Become a member" tile; fake a member by SQL-updating the user row via a temporary eval (or set `membership_status='active'`, `membership_period_end` future) → hub shows the card with date; portal button 400s gracefully without `stripe_customer_id` (show the error toast).
3. Zero console errors.
4. Commit + push to main.
