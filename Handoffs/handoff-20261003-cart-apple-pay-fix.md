# Handoff: fix Apple Pay on the web cart and close the cart's open gaps

**Date:** 2026-10-03. Written by Claude (Opus 5.5), the Cart Build session. Not executed.
**Project:** Abs By AI (absbyai.com).
**Business goal this serves:** profitability. Paid traffic lands on this cart; a wallet buyer who sees "Payment Not
Completed" will think the order failed.
**Recommended:** Claude Opus 5.5, high effort. Suggested task name: `Cart Apple Pay Fix`.
**Run it locally on Dan's Mac, not in a cloud session.** The Stripe test keys, the database address, the dashboard
key and the PostHog read key exist only in `~/.absbyai-secrets.env`; the Railway CLI is signed in only there; the
fake-card test drives Stripe's fields in the local Browser pane on `localhost`; the test recipe is in local memory;
and this handoff file itself is not on GitHub yet (see section 6, Git). A cloud session could edit the code and run
the unit tests, but it could not test a payment, confirm the deploy or read Dan's test results.

## 1. Objective

The new web cart (`absbyai.com/cart`) went live on 2026-10-03. Card payments are proven end to end. **Apple Pay is
not:** on Dan's first real test, Apple's sheet said "Payment Not Completed" even though the purchase went through.
Find the cause, fix it, prove it on Dan's iPhone, and close the smaller gaps in section 5 so the cart is fully
functional for every way of paying.

## 2. What happened on Dan's test (facts, all read from production and live Stripe)

- 2026-10-03, about 09:57 CT, iPhone Safari, logged out, `absbyai.com/cart`, Monthly, tick box ticked, Apple Pay (Amex).
- Apple's sheet: **"Payment Not Completed"**. Then the page showed the navy "You're in. Your 7-day free trial is
  active." screen, logged in on a NEW account whose email is the Apple Pay wallet's email, not what step 1 holds.
- Stripe, in UTC: session created 14:57:36; setup intent succeeded and the subscription was created `trialing` at
  14:58:16; `checkout.session.completed` 14:58:17. Payment method: card, wallet `apple_pay`. Trial ends
  2026-10-10 14:58 UTC.
- Server log: `CART_ACCOUNT_CREATED: user 41`, `Membership activated for user 41 (monthly …)`, `CART_CLAIMED: user 41`.
  No error lines. Claim row created and used at 14:58:20.
- So the payment took about 3 seconds and succeeded everywhere. **The only thing wrong is what Apple's sheet was told.**

## 3. Likely causes, in order. None is verified yet.

Read the code first: `c2ExpressClick`, `c2ExpressConfirm`, `c2Reset`, `c2Teardown`, `handleCartComplete` in
`public/index.html` (section "WEB CART v2").

1. **We destroy Stripe's wallet element the instant the payment confirms.** `c2ExpressConfirm` awaits
   `c2.actions.confirm(...)`, then calls `handleCartComplete`, whose first lines are `closeCreditsCheckout(); c2Reset();`.
   `c2Reset` calls `c2Teardown`, which runs `expressEl.destroy()`. If the wallet sheet has not finished closing with
   success when the element that owns it is destroyed, the session is aborted and Apple shows a failure. This is the
   prime suspect. Fix shape: on completion, mark the sessions spent (`c2.sessions = {}`, clear `c2.plan`,
   `c2.actions`, `c2.checkout`) but leave the mounted elements alone, and destroy them a few seconds later or the
   next time the cart opens.
2. **`redirect: 'if_required'` together with `expressCheckoutConfirmEvent`.** Stripe's documented wallet sample is
   `actions.confirm({ expressCheckoutConfirmEvent: event })` with no `redirect` option, which redirects to the
   session's `return_url` after success. Our `return_url` is `/?cart_return={CHECKOUT_SESSION_ID}` and
   `applyCartReturn()` already finishes a purchase that comes back that way. If cause 1 is not it, use the documented
   form for wallets and let the page reload into the done screen.
3. Anything else in how the sheet is completed. Check Stripe's current docs for the Express Checkout Element
   `confirm` event with Checkout Sessions (is there a completion or `paymentFailed` call we owe it?).

**Verify every Stripe detail against the current docs before changing code. Do not work from memory.** The docs
moved a lot in 2026: see the traps in `Docs/WEB_CART.md`.

## 4. Second defect found in the same test: whose email becomes the account

Step 1 says "Your email becomes your login", but for a wallet payment Stripe takes the email from the wallet and
ignores what `actions.updateEmail()` was given (documented behaviour). Dan typed nothing useful in step 1 and the
account was created under his Apple Pay email. A buyer who types one address and pays with a wallet tied to another
gets an account, and the set-password email, at an address they did not choose.

Proposed fix (default, confirm with Dan in one line before building): when step 1 holds a valid email, it wins.
Send it to the server before the wallet sheet opens (on blur, and again in `c2ExpressClick` if it changed) and store
it on the Checkout Session's metadata (`stripe.checkout.sessions.update`); in `fulfillMembershipSessionInner` prefer
that value over `customer_details.email` for `resolveCartAccount`. When step 1 is empty, keep today's behaviour (the
wallet's email). Stripe's receipts still go to the wallet email; say so in `Docs/WEB_CART.md`.

## 5. Other gaps to close

1. **Rate limit shared by all visitors.** `cartLimiter` (server.js, 40 per 15 minutes) keys on `req.ip`, and
   `trust proxy` is off, so behind Railway every visitor may share one bucket (the open "N2" audit finding; the log
   prints an express-rate-limit `X-Forwarded-For` ValidationError). The cart now creates a Stripe session when the
   page opens and another on a plan switch, so under ad traffic everyone could get "Too many attempts". Give
   `cartLimiter` `keyGenerator: (req) => clientIp(req)` (the helper already exists next to `allowFreeGenByIp`). Do
   not change the other limiters in this task.
2. **See what the phone did.** Claude cannot run Apple Pay. Add temporary PostHog events around the wallet flow
   (`cart_wallet_click`, `cart_wallet_confirm_started`, `cart_wallet_confirm_result` with the result type, the error
   code and message if any, and elapsed ms) so each of Dan's tests can be read back with `POSTHOG_PERSONAL_KEY`
   instead of asking him what he saw. Keep them, they are cheap.
3. **Still unverified on a real iPhone** (card and bank-verification paths are proven): the Apple Pay button's look
   and height, whether a Link button shows, the "or pay by card" divider, the tick box rule on a wallet tap (the
   `click` event calls `event.reject()` when the box is empty), **Lifetime through Apple Pay** (the sheet must not
   call it a subscription or show a recurring amount; if it does, see `applePay.deferredPaymentRequest` on the click
   event's `resolve`), and a logged-in buyer paying by wallet.
4. **Dan's cleanup, his to do:** the test trial from section 2 (user 41) bills $19.99 on 2026-10-10 unless he cancels
   it in the hub (Manage membership). His own account (`danroseconsulting@gmail.com`, the admin) has a real live
   Monthly subscription since 2026-09-14 that renews 2026-10-21; he decides whether to keep it. While it is active the
   cart tells that account "nothing to pay", which is correct.
5. **Not this task:** the sales page still says "$69.99 a year" and no guarantee. That is
   `Handoffs/handoff-20261002-start-page-365-guarantee.md`.

## 6. Current state

- Live: commits `46c14ce` (cart behind a switch), `34268c1` (go-live, old cart removed), `86dff85` (`/cart` for
  everyone, logged in or not). Mechanics and traps: `Docs/WEB_CART.md`. Design spec: `Docs/cart-design-20261002/`.
- Proven in Stripe TEST mode on 2026-10-03 with fake cards: Monthly, Monthly cancel in Stripe's portal, Lifetime, the
  day-7 charge, the double-charge guard, Lifetime cancel, a card that declines on day 7 with all three retries,
  a card declined at checkout, bank verification, an email that already has an account, a logged-in buyer, the
  photo-first routing. Unit tests: `node scripts/cart/cart-fulfillment.test.js` (110 checks).
- Stripe account settings already made: `absbyai.com` is a registered payment method domain (Apple Pay, Google Pay,
  Link active); the webhook endpoint also receives `payment_intent.succeeded` and `payment_intent.payment_failed`.
- **Git: the main folder is out of step with GitHub.** `scripts/git/safe-push.sh` stopped twice on other sessions'
  uncommitted video-skill files (`.claude/skills/shorts/SKILL.md`, `…/kit9x16/sbl_graphics.py`, `…/reference/render.py`,
  `.claude/skills/_shared/framing-motion.md`). Both cart commits were pushed from a clean `git worktree` of
  `origin/main` with a cherry-pick, which the push rule allows. The folder still holds local twins of them
  (`0e93fc7`, `a79912d`, same content as `34268c1`, `86dff85`). If safe-push stops again, do the same: fetch, add a
  detached worktree of `origin/main` in the scratchpad, cherry-pick your commit, link `node_modules` in to run the
  tests, push `HEAD:main`, remove the worktree.

## 7. Plan

1. Read this doc, `Docs/WEB_CART.md`, memory `stripe-test-mode-cart-recipe` and `web-cart-pay-first`.
2. Read Stripe's current docs for the Express Checkout Element with Checkout Sessions (`confirm`, `click`,
   completion, redirect behaviour) and for Apple Pay merchant tokens. Decide between causes 1 and 2 from the docs.
3. Fix section 3. Add the events from 5.2. Fix 5.1. Ask Dan the one-line section 4 question, then build it.
4. Tests: extend `scripts/cart/cart-fulfillment.test.js` for the section 4 email rule (typed email wins; empty step 1
   falls back to the wallet email; an existing account at the typed email is still never logged in automatically).
   Re-run the card path once in Stripe test mode on localhost to prove nothing regressed.
5. One push, confirm the Railway deploy, verify `absbyai.com/cart` loads with no console errors.
6. **Dan's iPhone test** (logged out, a fresh `+something` Gmail in step 1): Monthly with Apple Pay, expect Apple's
   success tick, the "You're in" screen and the account under the step-1 email. Then Lifetime with Apple Pay and a
   second fresh email, and read what the sheet says. Read the PostHog events after each try. He cancels both in the
   hub (Monthly in Stripe's portal; Lifetime with Manage membership, then Cancel). Each costs $0.
7. Update `Docs/WEB_CART.md` and memory `web-cart-pay-first`, flag the native retest, delete this handoff's lines
   from `AI_COORDINATION.md` and `Handoffs/README.md`.

## 8. Things to avoid

- Claude cannot type a real card, use Apple Pay, or trigger a live charge. Fake cards in Stripe test mode on
  localhost are fine. A live Lifetime charge is Dan's to run (`scripts/cart/lifetime-charge-now.sh <email>`).
- Do not put Stripe test keys on production to test Apple Pay unless the switch is locked to Dan: a public test-mode
  switch would hand anyone with card `4242…` a free membership.
- Ad and analytics tags are live on localhost. Before every test purchase block them in the page (the recipe is in
  memory `stripe-test-mode-cart-recipe`); overriding `ttq.track` does not hold, replace `fireTikTokEvent`.
- Do not change the approved design or copy. No em dashes in anything new.
- An account that is already paying or in a trial must never be sold a second membership (`hasOwnMembership`).
- Every deploy drops locked image holds: one push where possible.

## 9. Files and locations

`public/index.html` (cart markup `#cartV2`, styles `.c2-*`, code from "WEB CART v2"); `server.js`
(`buildMembershipCheckout`, `cartLimiter`, `fulfillMembershipSessionInner`, `resolveCartAccount`, section "LIFETIME
PLAN"); `db.js` (`lifetime_pending`, `checkout_claims`); `scripts/cart/`; `Docs/WEB_CART.md`;
`Docs/cart-design-20261002/`; secrets in `~/.absbyai-secrets.env` (`STRIPE_*`, `STRIPE_TEST_*`, `DASH_SECRET`,
`POSTHOG_PERSONAL_KEY`, `DATABASE_PUBLIC_URL`); Railway service `abs-by-ai`.

## 10. Model and effort

| Scenario | Recommendation |
|---|---|
| Claude usage is low right now | **Claude Opus 5.5, high effort.** It wrote this cart, and the test recipe lives in its memory. |
| Claude usage is high or near a limit | Codex, GPT-6 Sol, high effort. Give it this doc and `Docs/WEB_CART.md`; it has no memory of the recipe. |

A tricky payment bug in live checkout code is not Sonnet work.

## Starter prompt

```
Read Handoffs/handoff-20261003-cart-apple-pay-fix.md in full and execute it. Rename this task "Cart Apple Pay Fix".
On my live test the new cart at absbyai.com/cart took my Apple Pay payment but Apple's sheet said "Payment Not
Completed", and the account was created under my Apple Pay email instead of the email in step 1. Check Stripe's
current docs, fix both, fix the shared rate limit, add the wallet tracking events, deploy, then stop and tell me
exactly what to test on my iPhone. Ask me the one section 4 question first.
```
