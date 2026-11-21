# AUDIT — Money & security review (post-revenue)

**Model:** Claude Fable 5. **Date:** 2026-07-17. **Scope:** read-only review of `server.js` (7,004 lines), `db.js`, and the client payment paths, covering everything shipped since the 2026-07-10 audit (`AUDIT_membership.md`): Stripe live-mode webhook paths, Supplement Audit endpoints, Macro Tracker v2, welcome autoresponder + unsubscribe, accounts/password reset, and the status of every prior finding. Stripe is now LIVE and charging, so severity is ranked by real-dollar exposure.

**No code was changed.** Findings only; fixes are described so they can be applied deliberately.

---

## N1 — CRITICAL — Print checkout charges whatever price the client sends

**Where:** `/api/stripe/create-checkout` (`server.js:6824-6870`) and `fulfillProductOrder` (`server.js:6876-6955`).

The printed-product checkout builds its Stripe line item from **`priceInCents` taken straight from the request body** — the server never looks the price up. `PRODUCT_CONFIG` (`server.js:6741`) knows the real prices ($18–$87) and the real Printify costs ($11–$54 incl. shipping), but nothing checks the paid amount against them: `fulfillProductOrder` verifies only `payment_status === 'paid'` and then **submits the real Printify order**.

**Attack:** POST `create-checkout` with `productType:'canvas', size:'16x20', framed:true, priceInCents:50` (Stripe's minimum), pay $0.50 with a real card, and a genuine framed 16×20 canvas (~$54 of Printify cost) ships to the attacker. Repeatable without limit; each hit is a direct ~$53 cash loss. The endpoint is unauthenticated and the request shape is visible in the page source.

**Related in the same handler:** `imagePreviewUrl` is also client-controlled and becomes the printed artwork (`imageSrc`), so the same trick prints *any* internet image, not just an Abs By AI generation.

**Fix:** ignore the client's price — resolve `PRODUCT_CONFIG[productType].variants[variantKey].price` server-side when creating the session (400 on unknown variant), and as a belt-and-braces check in `fulfillProductOrder`, refuse to submit when `session.amount_total < variant.price`. Build `imageSrc` from `imageId` only.

**This is the one finding worth fixing before anything else.** It is the only place in the app where an attacker converts a small real payment into a larger real cost to the business.

## N2 — MEDIUM today, HIGH at scale — All rate limits are one shared global bucket

**Where:** `aiLimiter` (`server.js:63`), `authLimiter` (`server.js:2461`); no `app.set('trust proxy', …)` anywhere.

express-rate-limit keys on `req.ip`. Behind Railway's proxy with `trust proxy` unset, `req.ip` is the proxy's address, not the visitor's — confirmed live: the production response carries `ratelimit-policy: 10;w=60` headers and Express is not configured to read `X-Forwarded-For`. So the "per-IP" limits are actually **sitewide**:

- **10 AI calls/minute across all users combined.** Two or three simultaneous users generating/tracking will start 429-ing each other. This is a silent revenue/UX ceiling that will look like random "Too many requests" bugs the day traffic arrives.
- **20 auth attempts / 15 min across everyone.** An attacker (or one confused user) can lock signup/login/password-reset for the whole site; conversely brute-force protection isn't per-attacker at all.

**Fix:** `app.set('trust proxy', 1)` so `req.ip` is the client address from Railway's `X-Forwarded-For`, then sanity-check limits still make sense per-user. One line, but verify on live after deploying (the ratelimit-remaining header should stop being shared between two different networks).

## N3 — MEDIUM — Webhook returns 200 on fulfillment failure, so Stripe never retries

**Where:** webhook handler `server.js:44-47` ("Return 200 anyway — session-status on return is a fallback path").

If `fulfillMembershipSession` throws (DB blip, Stripe retrieve hiccup) the webhook still ACKs, so Stripe considers the event delivered and never redelivers. The fallback (`/api/stripe/session-status`) only fires if the buyer's browser is still open on the return path — close the tab at the wrong moment and the result is a **charged customer with no membership**, with nothing left to self-heal it. Same logic applies to credit packs and print orders (a failed Printify submit after payment is currently only recoverable if the buyer revisits).

**Fix:** return 500 from the webhook when fulfillment throws. Every fulfillment path is already idempotent (`fulfilled` map / `member_` / `order_` keys), so Stripe's retries are safe, and its retry schedule (hours–days) becomes the free self-healing layer.

## N4 — MEDIUM — The image paywall is client-side only for direct API callers (pre-existing, now revenue-relevant)

**Where:** `/api/generate-image` credit gate (`server.js:2158-2171`).

Two doors around the paywall for anyone talking to the API directly (the request shape is in the page source):

1. **Omit `deviceId`** → the request skips credit logic entirely and returns an unlocked image ("legacy clients" carve-out).
2. Even when out of credits, the response is `{ imageBase64, locked: true }` — the **full un-blurred image is delivered**; only the client blurs it.

No cash is stolen, but unlimited free Gemini generations undercut the entire credits product. Today the only brake is the rate limiter — which per N2 is one global bucket. Fix when convenient: require `deviceId`, and return no image (or a server-side degraded one) when `locked`.

## N5 — LOW — Anonymous Supplement Audits are uncapped model spend

`/api/counsel` is free-for-everyone by design (sunk-cost hook), but the 25/month cap only applies to logged-in users (`server.js:5632-5646`) — anonymous runs are unlimited and each is a large (24k-token budget) model call. The old F2 concurrency bypass of the cap also still exists (count-then-insert with the model call in between). Cost leak, not cash; bounded today by the (shared) limiter. Revisit if audit traffic or API bills spike.

## N6 — LOW — Remaining un-timeouted upstream calls

The hang class fixed in the Supplement Audit (751f7eb) and `/api/analyze-meal`/`/api/refine-leftovers` (50c51b4) still exists in: `/api/refine-meal`'s Haiku call (`server.js:1835`), and `/api/generate-image`'s Gemini calls + Haiku change-verification (`server.js:2034-2118`, up to ~5 upstream calls per request, none with an AbortController). A stalled connection hangs the request until the platform kills it. Same one-pattern fix as the previous two commits.

## Notes (no action needed unless they bother you)

- `UNSUB_SECRET` falls back to `STRIPE_WEBHOOK_SECRET`/`GITHUB_TOKEN` (`server.js:2605`). Safe cryptographically, but rotating either secret silently invalidates every unsubscribe link already sent. Setting a dedicated `UNSUBSCRIBE_SECRET` on Railway decouples them.
- `express.json({ limit: '100mb' })` on every route is a generous memory-DoS surface; the photos genuinely need large bodies, but 100 MB × concurrent requests is a lot of headroom.
- `/api/send-push` is only protected when `MONARCH_PUSH_SECRET` is set — confirm it is set on Railway, otherwise anyone can push notifications to every subscribed device.

---

## Status of the July 10 findings

| # | Finding | Status |
|---|---|---|
| F1 | Retry double-spends a credit on paid endpoints | **FIXED and verified.** `attemptId` idempotency cache is live on `/api/analyze-meal`, `/api/generate-image`, and (bonus) `/api/supplement/label`. Placement is correct: decrement → `cacheAttempt` with no `await` between them; the 402 out-of-credits response is cached too; client mints the id outside `fetchWithRetry`. |
| F2 | Counsel cap bypassable by concurrent requests | **Open.** Cap raised to 25; still check-then-insert. Low priority (cost, not cash). |
| F3 | Login-folding banks device-farmed free credits | **Open / accepted.** Unchanged at `server.js:2565-2572`. |
| F4 | GitHub-blob persistence: silent 409 drops; hard blocker for >1 replica | **Open.** `persistCreditsStore`/`persistSubscribersStore` still have no retry loop. **Do not scale Railway past one replica** while credits live in the GitHub JSON blob. |
| F5 | Early subscription event can miss the unlinked row | **Open / low.** `syncSubscriptionState` still matches only on `stripe_subscription_id`. |
| F6 | Membership fulfillment benign double-execute | Unchanged, still benign by design. |
| F7 | Non-member previews draw down the monthly cap | **Open / softened** — cap is now 25, so the fairness sting is smaller. |

## Verified clean this pass (checked, no action needed)

- **Stripe webhook signature** verification on the raw body, registered before `express.json` — correct.
- **Membership lifecycle:** trial granted only when `stripe_subscription_id` is empty; real status (`trialing`) read from Stripe at fulfillment; `payment_method_collection:'always'`; `no_payment_required` handled; canceled-but-paid-through honored via `membership_period_end`; comp/beta accounts can't be overwritten by webhooks (linkage severed on grant) and revoke only touches `comp` rows.
- **Credit purchase fulfillment** unchanged and still race-safe (synchronous check-and-set) with the webhook + session-status double path.
- **Accounts:** bcrypt cost 10; `ON CONFLICT` signup race handled; login/reset responses don't enumerate accounts; reset tokens random, stored hashed, single-use, 60-min expiry, all sessions invalidated on reset; admin routes allowlist-gated on top of session auth.
- **New Macro Tracker v2 endpoints** (`/api/saved-preps` CRUD, `/api/refine-leftovers`): all DB queries ownership-scoped (`user_id = $1`), input bounds enforced (≤3 photos, servings 2–20), leftovers math clamps fractions to [0,1].
- **Supplement Audit jobs:** `crypto.randomUUID()` ids; user-owned jobs return 404 to anyone else; anonymous jobs readable only by unguessable id; capped-request costs nothing (cap checked before the model call).
- **Welcome autoresponder:** send-then-advance is idempotent; unsubscribe + welcome-image tokens are HMAC-SHA256 with timing-safe comparison; `kind` column whitelisted (no SQL injection); CAN-SPAM footer + RFC 8058 one-click unsubscribe present; `@example.com` excluded.
- **Per-user data isolation** across meals, programs, meal plans, sleep entries, progress photos, transformations, counsel sessions — every query I checked filters by the session's `user_id`.

## One-paragraph triage for Dan

Fix **N1 today** — it's the only true "attacker pays $0.50, you lose $54, repeat forever" hole, and the fix is small (price lookup server-side + an amount check before submitting to Printify). Then **N2** (`trust proxy`, one line) so real users don't rate-limit each other and login can't be globally locked, and **N3** (return 500 on webhook fulfillment errors) so a paying customer can never end up charged-but-inactive with no retry. N4–N6 are cost/robustness, not cash, and can ride along with normal feature work. The big win from last week: the F1 double-charge fix landed correctly, and all the new feature endpoints (Macro Tracker v2, Supplement Audit, autoresponder) came through clean on auth, ownership, and idempotency.
