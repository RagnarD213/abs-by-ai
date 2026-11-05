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

## Update 2026-11-05

- **Supliful Pro active** ($69/month, Dan subscribed himself). Supliful dashboard: 6 of 8 setup steps done; left are step 7 (set shipping rates, which is only a help article, rates are set in Shopify) and step 8 (publish first product, not done: labels and approvals pending).
- **Shipping policy restored by Dan's call:** Standard $8.00, free at $70 and up; Express $15.00.
- **Cost check against Supliful's USPS rates** (Ground Advantage): up to 0.5 lb $5.29, to 0.75 lb $6.19, to 1 lb $7.49, 1.01 to 2 lb $9.99, 2.01 to 3 lb $12.49, each extra lb +$1.99. Express: $9.99 / $11.99 / $12.49 / $17.99 / $21.99, +$4.49 per lb. **So $8 flat only covers parcels up to about 1 lb; a creatine tub likely ships at $9.99 or more, and free shipping at $70+ (two tubs) means absorbing roughly $12 to $15.** Decision for Dan: keep, or switch to weight-based rates and a higher free-shipping line.
- **Alaska and Hawaii are not shippable by Supliful.** The Shopify US market still includes them; exclude AK and HI before launch.
- Subscriptions app (Shopify) installed; no plan created yet (no creatine product).
- Shopify support: category change escalated, ticket #71877476, Payments team follows up by email to the store account.
- **Decision (Dan, 2026-11-05):** Standard shipping is now **$9.99 flat, free at $70 and up** (saved and reloaded in Markets > United States). Express stays $15.00. Alaska and Hawaii still need excluding before launch.

## Update 2026-11-05 (later)

- **Alaska and Hawaii excluded.** Markets cannot exclude states, so shipping was switched back to shipping profiles (Shopify reset the Markets rates). General profile > Domestic zone is now United States, 60 of 62 states (Alaska and Hawaii off). Standard re-set to $9.99, free at $70 and up; Express $15.00. Verified after reload. Shipping moves to Markets again on July 1, 2027.
- **Electro Creatine (Shopify product 15499014504770)** already existed (made by the shop-build session): Supply option 1/3/6 tubs at $47 / $129 / $234, SKUs SPA-01-1/3/6, and a selling plan "$42 every 30 days" (monthly, 10.64% off, attached). Added a **Flavor** option with **Lemon** (the only flavor Supliful makes for Creatine Hydration Powder; flavors are separate Supliful products). Saved and verified; SKUs, prices and the subscription plan intact. The product shows Active but the store is password-locked.
- **Fulfillment link (blocker found):** Supliful support (Karl) answered the shop-build session's chat: products created directly in Shopify cannot be linked to Supliful by SKU; automatic fulfillment requires publishing the product from Supliful to Shopify, and 3-pack/6-pack bundles must be built in Supliful (Create Bundle, same product x quantity). So the hand-made Electro Creatine and its 3/6-tub variants will not fulfill automatically as they are. Not changed yet; replacing them touches the shop-build session's work.

## Update 2026-11-05 (creatine rebuilt through Supliful)

Dan approved "rebuild it". Why: Supliful support said Shopify-made products cannot be linked by SKU; products must be published from Supliful, and multipacks must be Supliful Single SKU bundles.

- **Supliful:** retail price of Creatine Hydration Powder set to $47 and renamed **Electro Creatine** (description = the approved short copy). Created bundles **Electro Creatine 3 Tubs** ($129, 3 units, cost $29.55) and **Electro Creatine 6 Tubs** ($234, 6 units, cost $59.10). All three published to the SixPackAbs Shopify store (status Published).
- **Shopify (new, Supliful-linked, location "Supliful Fulfillment"):** single tub `electro-creatine` (product 15502997487938, SKU DANIE-CHP-CB49, $47), 3 tubs `electro-creatine-3-tubs` (15502997782850, SKU DANIE-CHP-DFA0, $129), 6 tubs `electro-creatine-6-tubs` (15502997684546, SKU DANIE-CHP-7643, $234). Added the lifestyle photos (scoop, lemon drink, product on stone) and the Home page collection to the single tub, page title "Electro Creatine | SixPackAbs.com", and the existing **$42 every 30 days** selling plan (monthly, 10.64% off the $47 tub) to the single tub only. **Flavor** option (Lemon) added to all three; SKUs kept.
- **Old hand-made product** (15499014504770, SKUs SPA-01-x): set to Draft, handle renamed `electro-creatine-old-draft`. Not deleted.
- **Flavors:** Supliful makes one creatine flavor for this line (Lemon). Creatine Monohydrate is the only other creatine and is unflavored with no approved label. New flavors would each be a separate Supliful product plus label. Adding one later: publish it from Supliful, add `Flavor` value on its product, and have the theme link the flavor and pack products together.
- **One page for 1/3/6 tubs:** Shopify Combined Listings is Plus-only, so the three packs are three products. The pack and flavor picker must be built in the theme as links between the three product pages (handles above). Theme build owns this.
- Not verified: a real test order reaching Supliful (Supliful and Shopify both recommend one before launch).
