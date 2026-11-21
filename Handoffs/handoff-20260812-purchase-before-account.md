# Handoff: Let users buy before creating an account (anonymous IAP + alias on signup)

**Date:** 2026-08-12
**Project:** Abs By AI (iOS In-App Purchase)
**Business goal this serves:** Profitability — removes the single biggest friction step standing between a user seeing their result and paying. Every screen before payment costs conversions.

## Objective

Let a native iOS user complete the In-App Purchase **without first creating an Abs By AI account**, then capture the account immediately afterwards and attach the purchase they just made to it. Today the app forces signup *before* the buy button will do anything. **Do not start this until the iOS app has been approved by App Review** — it modifies the exact purchase code Apple has already rejected twice.

## Current State

Dan raised this on 2026-08-12 after watching the purchase flow on his own phone: *"It asked me to make an account before I purchase. I think we should have them purchase and then make the account afterwards."*

He is right on the merits, and it matches the funnel shape he has studied (see the `madmuscles-deep-dive` memory): quiz → paywall → purchase → account. MadMuscles does not ask for an email until after the card is in.

**Why it is built the other way today, and this is deliberate, not an oversight.** `public/index.html` carries an explicit comment above the IAP block (~line 2935):

> THE LOAD-BEARING PART — appUserID. RevenueCat is told our own users.id, and that is the ONLY key the purchase webhook has to find the account to unlock. A purchase made while anonymous cannot be attached to anyone, which is why buying is gated behind having an account.

The gate itself is in `handleIapSubscribe()` (~line 3134):

```js
if (!isLoggedIn()) {
  window._afterAuth = () => { refreshMembership().then(() => showMembershipScreen()); };
  showAuthScreen('signup');
  return;
}
```

And the server independently refuses anonymous purchases — `parseAppUserId()` (`server.js` ~5493) maps RevenueCat's `app_user_id` to `users.id` and **rejects anything that is not a plain positive integer, explicitly naming `$RCAnonymousID:…`**:

```js
// RevenueCat's app_user_id is set by the client to our own users.id. Anything
// that is not a plain positive integer (notably RevenueCat's anonymous
// "$RCAnonymousID:…" form, used before the user signs in) cannot be mapped to
// an account and is ignored rather than guessed at.
```

So this is a two-sided guard, client and server, and **both sides have to change together**. This is the real work; the button gate is the trivial part.

Everything downstream already works and was sandbox-tested on a physical device on 2026-08-12: `POST /api/apple/sync` asks RevenueCat server-side what the account owns and never trusts the client; `applyAppleMembership()` writes the row with two guards (never re-labels a live Stripe sub as Apple-billed, and a revocation only touches a row we already own); the RevenueCat webhook is live on production and sandbox.

## Key Decisions Already Made

- **Deferred until after App Review approval.** Settled 2026-08-12. Rebuilding purchase plumbing hours before a third submission, after two rejections on exactly this code, was the wrong risk for a conversion gain that keeps. Do not re-open the timing.
- **The client is never trusted about entitlements.** Every unlock goes through RevenueCat's REST API server-side. Whatever this change does, it must not introduce a client-asserted entitlement path. Same lesson as the F1 credit double-spend and the locked-image unlock token.
- **Do not simply delete `parseAppUserId`'s anonymous-id rejection.** It exists so an unattributable purchase is *ignored* rather than guessed onto some account. The fix is to make the id resolvable by aliasing, not to start accepting ids we cannot map.
- **An account is still required eventually, not optional.** Membership lives on a `users` row; the web app, the trainer, the nutritionist and the gallery all key off it. The goal is "purchase before account," not "purchase instead of account."
- **The pre-trial quiz stays before the paywall.** It is what makes the trial feel personalized and it needs somewhere to write a profile. The friction being removed is the *signup form*, not the whole pre-purchase experience.

## Detailed Plan

1. **Confirm the RevenueCat restore/transfer setting first.** `Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md` covers this and **should be done before this task** — aliasing an anonymous id onto a real one is exactly the operation that setting governs. Doing this task first means testing against unknown behavior.

2. **Client: allow the purchase while logged out.** In `handleIapSubscribe()`, drop the `!isLoggedIn()` early return. `iapSync()` already calls `Purchases.configure({ appUserID: null })` when there is no `memberState.userId`, which is precisely how RevenueCat mints a `$RCAnonymousID:…`. Verify that is what actually happens rather than assuming — log the id back out of the SDK after configure.

3. **Client: capture the anonymous id and force signup immediately after StoreKit reports success.** Read the current app user id from the SDK, hold it, and show the signup screen with copy making clear the purchase succeeded and the account is to secure it (e.g. "Payment complete — create your account to save your membership"). **The user must not be able to skip this screen into the app**, or they end up paid and unreachable.

4. **Client: alias on signup.** After the account is created and `memberState.userId` exists, call `Purchases.logIn({ appUserID: String(userId) })`. RevenueCat aliases the anonymous id onto the real one and carries the entitlement across — this is the SDK's supported path for exactly this flow, not a workaround. Then call `POST /api/apple/sync` as the existing flow already does, so the unlock is confirmed server-side.

5. **Server: handle the alias.** `parseAppUserId` will now legitimately see events whose `app_user_id` is anonymous, and events whose `original_app_user_id` is anonymous while `app_user_id` is our integer. Decide deliberately how each shape is treated, and keep the rule that an id we cannot map is **ignored and logged loudly**, never guessed. Check what RevenueCat actually sends for an alias/transfer — read the payload from a real sandbox event rather than the docs alone.

6. **Handle the abandonment case explicitly — this is the part that will bite.** A user who buys and then kills the app before creating an account has paid and has no account. Decide and implement one of:
   - persist the anonymous id locally (it already survives in the RevenueCat SDK's own storage) and re-prompt for signup on next launch before anything else — recommended, and cheap;
   - and/or make **Restore Purchases** on a fresh account able to recover it (which it should, once aliasing works).
   Write down which one shipped. **Do not leave this to chance** — it is a paid customer with no access, and it is the most likely support ticket this change creates.

7. **Test the whole matrix in sandbox on a real device.** Buy-then-signup; buy-then-kill-app-then-relaunch; buy-then-signup-with-an-email-that-already-exists (login, not signup — does the entitlement land on the existing account?); restore on a second account; and the plain already-logged-in path, which must be byte-unchanged in behavior. Verify each against the `users` row, not the app UI.

8. **Web is out of scope.** The Stripe path already requires an account for its own reasons and is not part of this. State explicitly in the final write-up which platforms changed — per the standing platform-scoping rule.

9. **OPEN — Dan's call:** whether the post-purchase signup screen can be dismissed at all. Recommend no (a paid user with no account is the failure mode above), but it is his call whether to trade that for a fully frictionless feel.

## Things to Avoid / Lessons Learned

- **Do not start before App Review approval.** This is the twice-rejected code path.
- **Do not remove the server-side anonymous-id guard as the "fix."** Make ids resolvable; do not start accepting unmappable ones.
- **Do not trust the app UI when verifying.** `memberState` is cached client-side; read the database.
- **Sandbox subscriptions renew on an accelerated clock and stop after roughly six renewals**, so an entitlement can disappear mid-test for reasons unrelated to your change.
- **The comp/demo account (`danroseconsulting+applereview@gmail.com`) shows no purchase UI at all by design** — useless for this. Always use a fresh non-comp account.
- **`git pull --rebase` publishes whatever else is unpushed on `main`** — this repo has concurrent sessions touching `todos.json`/`plan.json`. Check `git log origin/main..HEAD` before pushing.
- **Local `node server.js` will not boot** (no real API keys in `.env`). For client-side changes, `node --check` on the extracted inline `<script>` blocks plus push-and-verify-on-prod is the working substitute.

## Relevant Files & Locations

- `public/index.html` — `iapSync()` (~2965), `iapPrepareMembershipScreen()` (~3106), `handleIapSubscribe()` (~3126, holds the gate to remove), `handleIapRestore()`, `RC_PUBLIC_KEY`, `RC_ENTITLEMENT`, `iapState`.
- `server.js` — `parseAppUserId()` (~5493), `applyAppleMembership()` (~5514), `fetchAppleEntitlement()`, `POST /api/apple/sync` (~5701), `POST /api/revenuecat/webhook` (~5612), `APPLE_PRODUCT_PLANS`.
- RevenueCat project `355f4b52`, entitlement `membership`, offering `default` (`$rc_monthly` / `$rc_annual`).
- Apple products: `com.absbyai.app.membership.monthly` (`6799231479`), `com.absbyai.app.membership.annual` (`6799227966`).
- Env: `REVENUECAT_SECRET_KEY` (Railway).
- `app-store-assets/IAP_SUBSCRIPTION_PLAN.md` — the original build record for the IAP work.
- Companion handoff, do this one FIRST: `Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md`.

## Model & Effort Recommendation

Multi-file change across the client, the server and a third-party billing integration, with a real money-losing failure mode (paid user with no account) and identity-aliasing semantics that are easy to get subtly wrong. Falls under the always-Claude override — it is the Apple/RevenueCat purchase integration.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Opus, extended thinking — the alias/webhook semantics and the abandonment case are genuine judgment calls where a subtle mistake costs real revenue and is hard to detect after the fact. |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5, standard thinking, and split it: land steps 2–4 (the happy path) and verify in sandbox, then take steps 5–6 (webhook shapes + abandonment) as a second pass. Escalate to Opus if the RevenueCat alias payloads turn out not to match the documented shapes. |

Override: always Claude regardless of usage — purchase integration code.

## Starter Prompt for the Next Task

> Make it possible to buy the Abs By AI membership on iOS *before* creating an account, then capture the account right after the purchase. Read `Handoffs/handoff-20260812-purchase-before-account.md` first — it has full context. Short version: today `handleIapSubscribe()` in `public/index.html` hard-returns to the signup screen when the user is logged out, and `server.js`'s `parseAppUserId()` deliberately rejects RevenueCat's `$RCAnonymousID:…` form, because our `users.id` is the only key the purchase webhook has to find the account to unlock. Both sides have to change together: let the purchase happen anonymously, force signup immediately after StoreKit reports success, and call `Purchases.logIn()` to alias the anonymous id onto the real one — which is RevenueCat's supported path for this exact flow. Do not "fix" the server guard by accepting ids you cannot map; make them resolvable instead. Pay particular attention to step 6, the user who buys and then closes the app before signing up — that is a paying customer with no access and it must be handled deliberately, not left to chance. Verify the whole matrix in sandbox on a real device against the `users` rows, not the app UI. **Two preconditions: do not start until the iOS app has been approved by App Review, and do the companion handoff `handoff-20260812-revenuecat-restore-behavior-audit.md` first, because the RevenueCat setting it audits governs exactly the aliasing operation this task relies on.**
