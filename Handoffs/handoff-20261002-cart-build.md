# Handoff: build and ship the approved web cart (navy, Monthly plus Lifetime)

Written 2026-10-02 by Claude (Opus 5.5), the Cart Mockups session. Not executed.
Dan approved the design the same day after five rounds: "Let's lock that as our finalized design."
Recommended: **Claude Opus 5.5, high effort.** Suggested task name: `Cart Build`.

## 1. Goal

Replace today's web cart (`#cartSection` in `public/index.html`) with the approved one, working end to end with real
payments: a buyer taps a buy button on `absbyai.com/start`, lands on this cart, picks Monthly or Lifetime, pays $0
today, and is logged into a new account. Then ship it, test it with Dan's card, and make it the live cart.

## 2. The spec (source of truth)

| item | where |
|---|---|
| Approved boards (versioned copy) | `Docs/cart-design-20261002/boards/`: `Final-Cart-Phone.dc.html` (Monthly picked), `Final-Cart-Phone-Lifetime.dc.html`, `Final-Cart-Desktop.dc.html` |
| What is locked, colours, every line of copy | `Docs/cart-design-20261002/README.md`. Read it in full. |
| Canvas (private) | https://claude.ai/artifact/WUrxcVvv6mZNmnjt3LqrPa, page **APPROVED: final cart** |
| Generator that wrote the boards | `Docs/cart-design-20261002/gen.py` (`blue_board`) |
| Today's cart and how payment works | `Docs/WEB_CART.md`; `showCartScreen`, `handleCartComplete`, `applyPurchaseDeepLink` in `public/index.html` |
| Server side | `server.js`: `MEMBERSHIP_PLANS` (line ~196), `buildMembershipCheckout` (~6666), `POST /api/stripe/create-cart-checkout` (~6767), `fulfillMembershipSession` (~6922), `POST /api/stripe/claim` (~7055), `isActiveMembership` (~6357), `trialReminderSweep` (~7495) |
| Tests | `scripts/cart/cart-fulfillment.test.js` (45 checks, pg-mem and a stubbed Stripe) |
| Research behind the design | `Docs/cart-research-20261002/`, memory `cart-follows-start-button`, `web-cart-pay-first` |

The boards are plain HTML with inline styles. Port the markup and styles into `#cartSection`. Drop the canvas-only
parts (the `x-dc` wrapper and script, fixed heights, `{{holes}}`, `<sc-if>`). Phone layout under about 900 px, the
desktop board above it (1040 px content, form column plus a right column with the bullet box and the guarantee).
Copy is verbatim from the boards. No em dashes or en dashes in anything new.

## 3. What the cart must do

1. **Entry.** Every web non-member who reaches the cart sees this design: from `/start` (`/?join=1&from=vsl`), from the
   analysis page, from a hub tile. It never shows or mentions a photo, a goal picture or body numbers. The native apps
   are untouched: `IS_NATIVE_APP` keeps the In-App Purchase screen.
2. **Plans.** Monthly is pre-selected. Tapping a plan updates the line item and the block above the button, exactly as
   the two phone boards show. Lifetime replaces Annual on the web cart (decision 1). Keep `annual` in `MEMBERSHIP_PLANS`
   for existing annual subscribers and the apps; just stop offering it here.
3. **Tick box (Monthly only).** It starts empty and is required. Tapping the button without it shows a short inline
   message at the box and scrolls to it. Lifetime has no tick box.
4. **Payment fields on the page, in step 3**, not in the overlay sheet used today. Stripe must draw the Apple Pay and
   Link buttons (and Google Pay if it is on); the card fields are Stripe's too. Our own green button stays the final
   action. Apple Pay keeps Apple's own black style: do not fake a navy one (Dan was told on 2026-10-02).
5. **Email.** Step 1 collects it. It becomes the login, as today (`resolveCartAccount`, the claim, the set-password
   email). A logged-in non-member sees their email filled in and locked.
6. **[STATEMENT NAME].** Fill it with the account's real statement descriptor, read from Stripe, not typed by hand.
7. **After payment.** Keep the "You're in" screen and the optional password, restyled to the navy look. Then send a
   buyer who has no goal picture to the photo upload first, then the five questions (decision 2). The cart promised
   "See yourself with abs, then get an AI fitness plan", so that is the order they should get it in.
8. **Review without paying.** `/?demo=checkout` keeps working on the new design with the pay button disabled.
9. **Tracking stays intact:** `cart_viewed`, `cart_plan_selected` (now `monthly` or `lifetime`), `cart_checkout_opened`,
   `cart_checkout_completed`, `account_claimed`, `cart_password_set`, the virtual pageview `/vp/cart`, the Google Ads
   trial conversion with the hashed email, TikTok `StartTrial`, and the ad click ids in the session metadata. Add
   `cart_terms_checked`. Remove `cart_skipped` and the cart video events with their UI.

## 4. Payments: how to build each plan

**Verify every Stripe detail against the current Stripe docs before coding. Do not work from memory.**

**Monthly (no change to the deal):** a subscription, 7-day trial, then $19.99 a month. Same fulfilment as today.

**Getting the fields onto the page.** Recommended: keep Checkout Sessions and switch the session to Stripe's custom
UI mode (Elements driven by a Checkout Session: the Express Checkout Element for wallets, the Payment Element for the
card, confirmed from our own button). That keeps `checkout.session.completed`, `fulfillMembershipSession`, the claim and
the tests almost as they are. If the docs show it cannot do something this design needs, stop and tell Dan what breaks
before choosing a fallback. The known fallback, mounting today's embedded Checkout inline in step 3, changes the approved
look (Stripe draws its own email field and pay button), so it needs his yes.

**Lifetime (new, and not a subscription).** The promise on the page: 7 days free, then one charge of $69.99, lifetime
access, no recurring billing. Requirements, whichever Stripe mechanism you use:
- $0 at checkout. The card is saved with the buyer's agreement to that one stated charge.
- Exactly one charge of $69.99, 7 days after checkout, unless they cancel first. Never a second charge.
- Nothing Stripe shows the buyer (the wallet sheet, the form, the receipt) may call it a subscription or "per year".
- During the 7 days they have full access (`membership_status='trialing'`, `membership_plan='lifetime'`).
- When the charge succeeds: `membership_status='active'`, `membership_plan='lifetime'`, `membership_period_end=NULL`
  (permanent, the same shape as a comp account). `isActiveMembership` already treats that as a member.
- Cancel before day 7 in Manage membership: the pending charge is removed and nothing is ever billed. After the charge,
  Manage membership shows "Lifetime member" and no cancel button.
- Stamp the paid conversion from the successful charge, never from a status change (memory
  `stripe-trial-end-active-before-charge`).

Recommended mechanism: a setup-mode session saves the payment method; a `lifetime_pending` row records the user, the
Stripe customer, the payment method and `charge_at`; a server sweep on the same pattern as `trialReminderSweep` creates
one off-session PaymentIntent at `charge_at` with an idempotency key from the row id; the webhook handles success and
failure. If the charge fails: one retry a day for 3 days with an email each time, then access ends (decision 3). If the
docs show a cleaner native way that meets every requirement above, use it and say why.

## 5. Decisions for Dan (ask once, at the start, in one message)

1. Lifetime replaces Annual on the web cart for every web visitor. Existing annual subscribers and the apps keep
   Annual. **Default: yes.**
2. After checkout, a buyer with no goal picture goes to the photo upload first, then the five questions.
   **Default: yes.**
3. A failed Lifetime charge on day 7: retry once a day for 3 days with an email each time, then access ends.
   **Default: yes.**

Already settled, do not reopen: the design and every line of copy in `Docs/cart-design-20261002/README.md`, including
Dan's quote as he wrote it; Stripe-styled Apple Pay and Link buttons; the 365-day guarantee (the sales page and the
refund policy page are handled by `handoff-20261002-start-page-365-guarantee.md`).

## 6. Steps

1. Read this doc, `Docs/cart-design-20261002/README.md`, the three boards and `Docs/WEB_CART.md`. Send Dan section 5.
2. Read the Stripe docs for the custom UI mode and for saving a card and charging it later. Write the plan for both
   plans in a few lines at the top of `Docs/WEB_CART.md` before coding.
3. Server: add `lifetime` (6999, one-time) to `MEMBERSHIP_PLANS`; the session creation for both plans; the Lifetime
   pending table, sweep, webhook handling and cancel path; the statement descriptor lookup.
4. Client: rebuild `#cartSection` from the boards; plan state; the tick box rule; the on-page Stripe elements; the
   restyled done screen; the routing in step 3.7; the events.
5. Tests: extend `scripts/cart/cart-fulfillment.test.js`. Monthly unchanged. Lifetime: setup creates the account and the
   pending row; the sweep charges exactly once; a second sweep does nothing; cancel before day 7 means no charge; a
   failed charge follows decision 3; the webhook racing the browser still yields one account.
6. Ship it dark first: deploy with the new cart at `/?demo=checkout` (no payment) and behind a URL switch for real
   payment (for example `&cart=v2`), with today's cart still the default. Verify phone and desktop widths, no console
   errors, every event in the network log.
7. **Dan's live card test.** There are no Stripe test keys and Claude cannot type card numbers, so Dan pays with his
   own card on the switch URL: once on Monthly (then cancel in Manage membership), once on Lifetime. Give him a
   one-command script to run the Lifetime charge for his own pending row now instead of in 7 days, so the $69.99
   charge, the receipt wording and the "Lifetime member" state can be checked the same day. He refunds himself in Stripe.
8. Make the new cart the default, remove the old markup, CSS and the switch. Commit only this task's files with
   `scripts/git/safe-push.sh`, confirm the Railway deploy, verify on `https://absbyai.com/?join=1&from=vsl` and from
   `/start`. One push where possible: every deploy drops locked image holds (memory `deploy-drops-locked-holds`).
9. Rewrite `Docs/WEB_CART.md` for the new cart, update memory `web-cart-pay-first`, and flag the native retest (the
   web deploy reaches the iOS and Android wrappers: confirm they still show In-App Purchase and never this cart).
10. Tell the sales-page task the cart is live, so it can ship its Lifetime wording
    (`handoff-20261002-start-page-365-guarantee.md`, part B). Report to Dan in plain words. Delete this handoff's lines
    from `AI_COORDINATION.md` and `Handoffs/README.md`.

## 7. Out of scope

Any change to the design or copy, the native apps, the `/start` page and the policy pages (the other handoff), prices,
ad campaigns, PostHog flags, the day-5 reminder email, refund tooling (Dan refunds by hand in Stripe for now).

## Starter prompt

```
Read Handoffs/handoff-20261002-cart-build.md in full and execute it. Rename this task "Cart Build".
Build my approved web cart from Docs/cart-design-20261002/ into the site and make it work with real payments:
Monthly (7 days free, then $19.99 a month) and Lifetime (7 days free, then one charge of $69.99, not a subscription).
Ask me the three section 5 decisions once at the start, then go. Ship it behind a switch first, stop for my live
card test, then make it the live cart.
```
