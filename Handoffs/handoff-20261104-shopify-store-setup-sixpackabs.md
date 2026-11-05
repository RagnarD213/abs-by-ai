# Handoff: Shopify store setup for SixPackAbs (2026-11-04)

**Type:** setup/ops, not video. **Owner:** one new session. **Goal:** configure the new Shopify store's back-end plumbing now, in parallel with the design, copy and label work, so the theme build can start the moment those land.

## Context

- Dan signed up for Shopify himself on 2026-11-04 (free trial, $1/month offer) and is signed in to the store in his Chrome. Claude cannot create accounts or enter passwords; Dan did that step.
- The store will be the home of `shop.sixpackabs.com`, selling six Supliful-fulfilled products to US men 30-60. Names and label look are locked: `Contest/approved/DESIGN-LOCK.md`, `Contest/OWNER-NAMES.md`.
- Dan picked **Claude A, The Numbered Shelf** as the website design (2026-11-04). Direction: light ivory pages, black and gold as accents, product centered on phones, phone first (390 px) then desktop (1440 px). Memory `sixpackabs-shop-design-direction`, `website-phone-first`. Design boards: `Contest/claude/shop-final-design/`.
- Website copy is NOT started. `Contest/claude/shop-final-design/COPY-READY.md` says waiting for Dan's design approval. Do not write site copy here.
- Supliful: Dan has a Free-plan Supliful account with billing and card already added (`Docs/SUPLIFUL_SAMPLES_RECEIPT_20261021.md`). Label production files and specs: `Handoffs/sixpackabs-production-20261103/`.
- Only Electro Creatine pricing is approved: one tub $47 + shipping, three $129, six $234, subscription $42 every 30 days. All other prices are placeholders; do not invent commitments. No free shipping, guarantees, reviews or certifications unless Dan says so.

## Do now (reversible, in Dan's Shopify admin via Chrome)

1. Open the admin (https://admin.shopify.com) in Claude in Chrome and look at what the store currently has. Report the plan name and trial status.
2. Store details: store name SixPackAbs, legal business name and address, support email, currency USD, time zone. Dan's personal info in forms is pre-authorized (memory `personal-info-form-entry-ok`); ask only if the business name or address is unknown.
3. Markets and shipping: sell to the US only. Create shipping profile and rates. A contiguous-US rate table has not been decided, so propose one default (flag-rate by order size) and record it for Dan; do not promise free shipping.
4. Taxes: set up US tax collection for a supplement seller; state what was enabled.
5. Supliful: install the Supliful app from the Shopify App Store, connect Dan's Supliful account, and confirm the connection. Do not push or publish products yet.
6. Policies: add Shopify's template refund, shipping, privacy and terms pages as drafts. Mark them placeholders to be replaced by approved copy.
7. Keep the store password-protected and unpublished. Turn off any sample products or default theme content that could go public.
8. Record every setting changed, plus the answers to the open items below, in a short receipt: `Docs/SHOPIFY_SETUP_RECEIPT_20261104.md`. Push it with `scripts/git/safe-push.sh`.

## Stop for Dan (do not do these)

- **Payments:** bank account, ID verification and payout details. Claude cannot enter these. Stop at that screen and tell Dan exactly what to fill in.
- **Choosing or paying for a Shopify plan.** Leave the trial as is.
- **DNS or connecting `shop.sixpackabs.com`:** changes the sixpackabs.com domain, outside the standing authorization. Only prepare the exact records needed and ask. Not needed until launch.
- **Passwords, 2FA codes, card numbers:** Dan enters them.
- No publishing the store, no test orders with real money, no customer emails.

## Wait for later (not this task)

- Theme build and page code: after Dan approves the design and the copy is written.
- Product pages and photos: need final labels and Supliful approval of them.
- Subscription app: decision open. Research which subscription app works with Supliful (Shopify native subscriptions vs a third-party app) and put one recommendation to Dan with cost. Do not install it until he agrees.
- Final policy wording, final prices for the five non-creatine products.

## Open items to report back

- Plan name and trial end date.
- Default US shipping rates proposed.
- Whether Supliful's Shopify app connected cleanly and what it can sync.
- Subscription app recommendation.
- Anything in the admin that did not match this brief.

## Done looks like

Back-end settings above are configured and verified in the admin, store still locked, receipt written and pushed, payments step handed to Dan with exact instructions. Report in chat, finish with the two wrap-up boxes.

## Recommended model

Claude Sonnet 5.5 at medium effort. This is mechanical admin clicking in Chrome with a checklist (model routing: Sonnet runs checklist work). Use Opus 5.5 high only if the subscription-app research needs deeper judgment.

## Starter prompt

> Read `Handoffs/handoff-20261104-shopify-store-setup-sixpackabs.md` in the Abs By AI project and do it. Dan is already signed in to his new Shopify store in Chrome. Work through the "Do now" list, stop at payments and DNS for Dan, and write the receipt.
