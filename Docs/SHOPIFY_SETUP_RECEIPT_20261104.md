# Shopify store setup receipt (2026-11-04, Claude Sonnet 5.5)

Handoff: `Handoffs/handoff-20261104-shopify-store-setup-sixpackabs.md`. Store admin: `https://admin.shopify.com/store/1yar3v-ie` (`1yar3v-ie.myshopify.com`). Store is still locked (private mode on, password in Online Store > Preferences; not recorded here). Nothing published, no orders, no emails.

## Plan and trial

- Plan: **Basic**, $1/month until **February 6, 2027** (list price $39). Card rates 2.9% + $0.30 online. Left as is.

## Settings changed

| Area | Before | After |
|---|---|---|
| Store name | My Store | **SixPackAbs** |
| Store address | "Texas 78628" only | **Rose Digital Holdings LLC, 3520 Cavu Rd, Georgetown TX 78628, US** (same address as the CAN-SPAM footer) |
| Standard shipping (US market) | $8.00, **free over $70.00** | **$8.00 flat, free-shipping threshold switched off** (no free shipping is approved) |

## Already correct, no change

- Currency USD; time zone Central (GMT-6); imperial units, pounds.
- One market only: United States (active). Express shipping $15.00, 1 to 2 business days, left as found.
- Store email is `danroseconsulting@gmail.com`; no store phone set.
- Private mode (password page) on. No products exist, so no sample products to hide. The Horizon theme is the default and stays unpublished-to-public behind the password.
- Policies (refund, privacy, terms, shipping) are Shopify's automated templates and show "Published", but they cannot be seen while the password is on. Not edited. They must be replaced with approved copy before launch.

## Taxes

- Shopify Tax is active (0.35% fee after $100,000 in global sales). Region United States, collecting: none.
- Shopify flags **Texas: action required, physical presence threshold met November 2026**. Turning on Texas collection needs Dan's Texas sales tax permit number, which Claude cannot enter. No state collection enabled.
- No product or shipping tax overrides set. Whether supplements are taxable in each state is not decided here.

## Supliful

- App found: "Supliful: Dropship Supplements" by Brand On Demand Inc. (4.5 stars, 161 reviews).
- **Installed and connected (updated 2026-11-04 evening).** Claude's final Install click was blocked, so Dan clicked it. Shopify recorded the install, but Supliful's return step (`api.cloud.supliful.com/shopify/auth/callback`) showed "Something went wrong". Fix: the callback code is single use, so instead of reloading, Claude opened Settings > Apps > Supliful > Open app. That restarted the sign-in, and `app.supliful.com/stores` now shows SixPackAbs (`1yar3v-ie.myshopify.com`) as "Connected Shopify store". Permissions granted: view and edit products, orders and other data, view customer data. No products synced or pushed. Supliful shows a banner: upgrade to a paid membership to start selling.
- Pricing finding: **Free plan** = 1 store, unlimited product creation, multi-angle mockups, sample order fulfillment. **Automatic order fulfillment is Pro only, $69/month ($660/year).** Dan's Supliful account is on Free, so real customer orders would not fulfill automatically. Upgrade is Dan's decision, not made.
- Nothing synced, no products pushed.

## Payments (Dan only)

Settings > Payments shows "Complete setup" for Shopify Payments. Dan enters the bank account, ID verification and payout details. Not touched.

## Shipping proposal for Dan (not implemented)

Flat $8.00 Standard and $15.00 Express stay as the working default. Proposal to replace with order-size tiers before launch, once Supliful's real shipping costs per tub are known: Standard $8 under $100, $12 from $100 to $199, $16 at $200 and up. Reason: the 3-tub ($129) and 6-tub ($234) bundles weigh several times one tub. No free shipping.

## Subscription app recommendation (not installed)

Use **Shopify's built-in Subscriptions app** (free, no extra monthly fee; Shopify already says it covers the basics) for the $42 every 30 days creatine subscription. Fallback if it proves too limited: Seal Subscriptions (free tier). Skip Recharge (paid, per-transaction fee). **Unverified:** I found nothing saying whether Supliful fulfills Shopify subscription renewal orders, and renewals are exactly what Pro automatic fulfillment would handle. Ask Supliful support before choosing. Sources: Shopify help (Shopify Subscriptions), craftshift.com native vs third-party comparison, Seal Subscriptions site.

## Did not match the brief

- Policies were already published (automated), not drafts; they stay hidden by the password.
- A default free-shipping rule over $70 existed; removed.
- "Business details" (legal entity) still reads "My Store - entity" and asks for entity type and tax ID. Left for Dan with the payments step.

## Dan next

1. Supliful is installed and connected (done).
2. Decide whether to pay $69/month for Supliful Pro (needed for automatic fulfillment).
3. Complete Settings > Payments and the business details (bank, ID, EIN).
4. Provide the Texas sales tax permit number when ready to collect tax.
5. Not needed until launch: DNS for `shop.sixpackabs.com`. Exact records will be prepared and asked for then.
