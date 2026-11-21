# Handoff: Audit RevenueCat restore behavior — one Apple ID entitling multiple app accounts

**Date:** 2026-08-12
**Project:** Abs By AI (iOS In-App Purchase)
**Business goal this serves:** Profitability — this decides whether one $19.99 subscription can unlock unlimited accounts, or whether a paying customer can get locked out of their own membership. Both failure directions are live today and neither has been checked.

## Objective

Determine how RevenueCat is configured to behave when the same Apple ID is used with more than one Abs By AI account, confirm it is the setting Dan wants, and verify the real behavior end to end in sandbox rather than trusting the dashboard label. **Do not start this until the iOS app has cleared App Review** — it involves changing a project-level purchase setting, and the app is mid-submission.

## Current State

**This was discovered by accident, not by looking for it.** On 2026-08-12, while device-testing the paywall fix, Dan created a *new* Abs By AI account on a phone whose **Apple ID / sandbox tester was unchanged** and already owned Monthly Membership. Tapping the trial CTA produced Apple's own dialog: *"You're currently subscribed to this. Your subscription to Monthly Membership renews on Aug 13, 2026…"*

**That dialog is correct behavior and is NOT a defect** — settled, do not re-open. Apple binds subscriptions to the Apple ID, never to our account email, which is exactly why Apple mandates the **Restore Purchases** control that already sits on our IAP screen. It is not an App Review risk.

What it *does* prove is that **one Apple ID is now associated with two different `users.id` values in RevenueCat**, and nobody has ever checked which way that resolves.

Relevant architecture as it stands (all verified in code this session):

- `iapSync()` (`public/index.html` ~2965) calls `Purchases.configure({ appUserID: memberState.userId })`, then `Purchases.logIn({ appUserID })` whenever our account id changes. **So switching Abs By AI accounts on one phone re-points RevenueCat at a different app user id.** That is the exact action that creates this situation.
- `parseAppUserId()` (`server.js` ~5493) maps RevenueCat's `app_user_id` back to `users.id` and **rejects anything that is not a plain positive integer**, explicitly including `$RCAnonymousID:…`.
- `POST /api/apple/sync` (`server.js` ~5701) calls `fetchAppleEntitlement(req.user.id)` — it asks RevenueCat what **this specific app user id** owns. It never trusts the client.
- `applyAppleMembership()` (`server.js` ~5514) carries two deliberate guards: it never re-labels a live Stripe subscription as Apple-billed, and a revocation only applies to a row we already own (so an Apple expiry cannot strip a comp/beta account or a paying web member).

**The whole outcome therefore hinges on what RevenueCat returns for the second app user id, and that is a project setting nobody has read.**

## Key Decisions Already Made

- **The Apple dialog is expected behavior, not a bug, and not a review risk.** Do not "fix" it. Restore Purchases is the intended path and is already present.
- **Do not touch this until the app is approved.** It is a project-level purchase setting; changing it during an active submission adds risk to the thing that is actually blocking the business.
- **The client is never trusted about entitlements** — every unlock goes through RevenueCat's REST API server-side. Any fix must preserve that; do not add a client-asserted entitlement path.
- **`parseAppUserId`'s rejection of `$RCAnonymousID:…` is correct as long as purchases require an account.** It becomes the blocker for the *separate* purchase-before-account handoff (`handoff-20260812-purchase-before-account.md`) — do not delete it here, and do not let the two tasks quietly overlap.

## Detailed Plan

1. **Read the current setting.** RevenueCat dashboard → project `355f4b52` → Project Settings. Find the restore / transfer behavior control (labelled around "Restore Behavior" or "Transfer purchases"). Record the exact current value verbatim in this document — the label wording has changed across RevenueCat releases, so quote what is actually on screen rather than matching it to a remembered option name.

2. **Work out which of the two failure modes we are exposed to.** They point in opposite directions and only one can be true:
   - **Shared across app user ids** → one paid subscription unlocks **unlimited** Abs By AI accounts. Direct revenue leak; trivially abusable (buy once, hand the login around, or just make new accounts).
   - **Kept with the original app user id** → a customer who signs up again with a new email **pays and gets nothing**, and Restore Purchases on the new account will not help them. Support burden and a refund/chargeback risk.
   - **Transferred to the newest app user id** → the anti-sharing behavior, and almost certainly what Dan wants: one Apple ID entitles exactly one Abs By AI account at a time, and Restore Purchases moves it.

3. **OPEN — Dan's call, but recommend "transfer" and say why.** Transfer is the only option where the money and the access stay one-to-one. Its one cost is that a user with two accounts can only hold membership on the most recent one; that is the correct trade and matches how Apple itself frames subscription ownership. Present it as a recommendation, don't set it silently — this is a billing behavior change.

4. **Verify the real behavior, do not trust the label.** The exact state needed is already sitting on Dan's phone, which makes this cheap:
   - Sandbox Apple ID `danroseconsulting+sandbox1@gmail.com` already owns Monthly Membership.
   - App account A = `danroseconsulting+iostest1@gmail.com` (the original buyer).
   - Create app account B on the same phone, tap **Restore Purchases**, and record: does B become a member? Does A *stay* a member? Check both against the database (`users.membership_status` / `membership_source` for both rows), not just the app UI — the UI reads a cached `memberState`.
   - **Sandbox subscriptions renew on an accelerated clock and self-cancel after roughly six renewals**, so if the entitlement has lapsed, re-purchase before drawing any conclusion. A lapsed sandbox sub looks identical to "restore did nothing."

5. **If the setting has to change, re-verify from scratch.** Changing it does not retroactively fix rows already written by `applyAppleMembership`. Query for any user with `membership_source = 'apple'` and confirm the set of Apple-billed accounts still matches the set of real paying Apple IDs.

6. **Check whether the webhook needs a companion guard.** If the answer is "transfer," RevenueCat should send a transfer event and the old account should lose access. Confirm `POST /api/revenuecat/webhook` (`server.js` ~5612) actually handles that event type rather than ignoring it — if it does not, the *old* account keeps membership forever and "transfer" silently degrades into "shared," which is the leak we were trying to close. **This is the single most likely way this task ends up looking done while still being broken.**

7. Record the finding and any change in `AI_COORDINATION.md`, and check off the dashboard task per Rule 9.

## Things to Avoid / Lessons Learned

- **Do not treat the Apple "already subscribed" dialog as the problem.** It is the symptom that exposed the question; the question is a dashboard setting plus a webhook path.
- **Do not verify from the app UI alone.** `memberState` is cached client-side; read the `users` rows.
- **Do not delete `parseAppUserId`'s anonymous-id rejection** to make a test pass. It is what stops an unattributable purchase being guessed onto some account.
- **Sandbox timing will mislead you.** Accelerated renewals and the ~6-renewal cap mean an entitlement can vanish mid-test for reasons unrelated to the setting.
- **This is a real-money setting.** Prefer one careful pass with database verification over fast iteration.

## Relevant Files & Locations

- RevenueCat project `355f4b52`, entitlement `membership`, offering `default`.
- `public/index.html` — `iapSync()`, `iapPrepareMembershipScreen()`, `handleIapSubscribe()`, `handleIapRestore()`, `RC_PUBLIC_KEY`.
- `server.js` — `parseAppUserId()`, `applyAppleMembership()`, `fetchAppleEntitlement()`, `POST /api/apple/sync`, `POST /api/revenuecat/webhook`, `APPLE_PRODUCT_PLANS`.
- Env: `REVENUECAT_SECRET_KEY` (Railway).
- Apple products: `com.absbyai.app.membership.monthly` (`6799231479`), `com.absbyai.app.membership.annual` (`6799227966`).
- Test identities: sandbox tester `danroseconsulting+sandbox1@gmail.com`; app accounts `danroseconsulting+iostest1@gmail.com` (non-comp) and `danroseconsulting+applereview@gmail.com` (**comp — useless for purchase testing, shows no purchase UI by design**).

## Model & Effort Recommendation

Touches billing behavior and the Apple/RevenueCat integration, where being wrong costs real revenue or locks out paying customers — architecture-adjacent and expensive to unwind, so it stays on Claude.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — the work is mostly read-a-setting, reason about three outcomes, and verify in sandbox. Sonnet is sufficient; Opus is not needed for a task this well-scoped. |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5, standard thinking — same pick. This is small enough that it is not worth deferring, and the webhook-transfer check in step 6 is the kind of subtle gap a mini-tier model tends to skip. |

Override: always Claude regardless of usage — it touches the purchase integration.

## Starter Prompt for the Next Task

> Audit how RevenueCat handles one Apple ID being used with more than one Abs By AI account. Read `Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md` first — it has full context. Short version: on 2026-08-12 Dan made a second app account on a phone whose Apple ID already owned Monthly Membership, and Apple correctly said "you're currently subscribed to this." That dialog is expected and is not a bug — but it proved one Apple ID is now pointed at two `users.id` values in RevenueCat, and nobody has ever checked which way that resolves. Depending on the project's restore/transfer setting we are exposed to either a revenue leak (one subscription unlocking unlimited accounts) or a locked-out paying customer (buys again, gets nothing). Start by reading the actual setting in RevenueCat project `355f4b52` and recording its exact on-screen wording, then work through the plan. Recommend "transfer to the newest app user id" to Dan rather than setting it silently. Verify the real behavior in sandbox using the accounts named in the handoff, checking the `users` rows and not the app UI — and pay particular attention to step 6, whether our webhook actually handles the transfer event, because if it does not then "transfer" silently behaves like "shared" and the task will look done while still being broken. **Do not start if the iOS app has not yet been approved by App Review.**
