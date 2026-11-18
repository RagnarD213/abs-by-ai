# Great Again T funnel: live build receipt (2026-11-17, Claude Fable 5.2)

Handoffs executed: `Handoffs/gat-sales-page-contest-20261117/BUILD-HANDOFF.md` and `COMPLIANCE-PAGES.md`. Website build, no edit slot. Spend: $0.

**State: built and live on shop.sixpackabs.com, NOT launched.** Every page carries `noindex`, no ads point at it, the video is the poster placeholder, and the free-month button is closed to the public (see "Blocker").

## Live pages (theme 195457614146, store `1yar3v-ie.myshopify.com`)

| Page | Address | Template |
|---|---|---|
| Quiz | https://shop.sixpackabs.com/pages/great-again-t-quiz | `page.gat-quiz` |
| Sales page (before and after the offer, one page) | https://shop.sixpackabs.com/pages/great-again-t (`?offer=1` shows the offer) | `page.gat-sales` |
| Order page | https://shop.sixpackabs.com/pages/great-again-t-order (`?preview=1` opens the free-month button) | `page.gat-order` |
| Questions, How It Works, Ingredients, Shipping and Returns, Contact, About, Privacy Policy, Terms, Disclaimer | `/pages/great-again-t-questions`, `-how-it-works`, `-ingredients`, `-shipping-and-returns`, `-contact`, `-about`, `-privacy-policy`, `-terms`, `-disclaimer` | `page.gat-info` |

Review page (round 7, compliance pages phone first, live links): https://claude.ai/artifact/V5jWex1Nzp7DsPU4TjZ2gm

## How it is built (never hand-edit the theme's gat files)

Work folder (M6, gitignored): `Media/research/gat-sales-page-contest-20261117/refine/`. Versioned copy of the code: `.claude/skills/design-sales-page/reference/gat-letter/`.

1. `python3 gen.py` re-exports both Docs (letter `1klwTUdTl5q_17MTA5c1Dtv-Agm_-B3rBpxGQPOj1SCI`, compliance `1QErPnqlCvhgdwfXYut6JL-h6O_iLspkjw2FFznYQeLs`) and writes the mockups: 5 funnel pages and 9 information pages (`infodoc.py`). `python3 gen.py check` proves the copy.
2. `python3 build_live.py` writes the theme files (`layout/gat.liquid`, `templates/page.gat-*.liquid`, `snippets/gat-info-*.liquid`, `assets/gat*`) into `~/Projects/Claude/Projects/SixPackAbs Shop Theme` and a plain-file copy in `live-preview/`, then runs the same copy check on the live output. Settings at the top: `LAUNCHED`, `CFG` (prices, discount code, `trialOpen`, `video`, `revealAt`).
3. `./deploy_live.sh` copies only the gat files to the M2 and pushes only those to the live theme (the Shopify CLI is signed in on the M2, not the M6).
4. `python3 capture_all.py` then `python3 build_review.py` rebuild the review page.

Checks passing at delivery: 188 letter paragraphs and 346 information-page paragraphs on their pages in order, word for word; no gold notes, brackets, Google Ads words or dashes on any page; every menu and footer link resolves; no buy button on the nine information pages.

## What was set up

- **Pages:** twelve Shopify pages created (Visible), titles "Great Again T ..." so the handles match the table.
- **Order page:** our page carries the two option rows, order summary, Healthy Back's terms box, the tick box (required for the free month) and the three policy links, then adds the bottle to the cart and hands off to Shopify checkout. It reads the live product first and refuses to sell unless the shop shows exactly $97 and a $67 plan. Button: "Continue To Secure Checkout".
- **Free first bottle:** discount code `FREEMONTH` (id 1565132063042): 100% off Great Again T, subscription purchases only, first payment only, one use per customer. Applied automatically by the order page. Product, $97 price, $67 plan (693056045378) and free shipping from $67 were set earlier the same day (`Docs/GAT_SHOP_OFFER_MATCH_RECEIPT_20261117.md`).
- **Tracking:** PostHog on every page (`site: shop.sixpackabs.com`, `funnel: great-again-t`): `gat_quiz_view/start/step/finish`, `gat_sales_view`, `gat_video_play/watch/end`, `gat_offer_reveal`, `gat_read_click`, `gat_button_click`, `gat_order_view`, `gat_option_select`, `gat_checkout_start`, `gat_checkout_error`, `gat_info_view`. Quiz answers are never sent, only step numbers. Google Ads conversion action "Great Again T Purchase" created (id 7907328453, `AW-18361229851/RurWCMWDwbodEJvEqLNE`, secondary until launch). The purchase pixel is written (`refine/live/shopify-pixel.js`) but **not installed yet**.
- **Support address:** footer and order page now say support@sixpackabs.com (was dan@sixpackabs.com), to match the compliance Doc.

## Verified live (2026-11-17)

Phone 390, tablet 768, desktop 1440 with headless Chrome: quiz, sales page (both states), order page, Privacy, Terms, Contact, Ingredients. Quiz runs four questions and lands on the sales page; `?offer=1` shows the top bar and offer card; menu and footer links open the nine pages. In Chrome: order page, tick box, button, Shopify checkout opened with Great Again T "Deliver every month, $67.00", `FREEMONTH (-$67.00)`, FREE; with a Texas address: Standard $9.99, **Total $9.99**, Recurring subtotal $67.00 every month. No payment was entered.

## Blocker found: refills would be $76.99, not $67

Shopify copies the first shipment's rate onto the subscription: checkout shows "Recurring shipments: Standard · $9.99 every month". Because the first order's subtotal is $0, the $9.99 rate applies and repeats. Until fixed, `trialOpen` is False: the free-month button works only with `?preview=1`. The $97 one-time bottle is correct and open.

Two fixes (Dan picks):
- **A (recommended):** make the plan $57.01 and let the $9.99 shipping repeat: the customer pays exactly $67 a month, which is what every compliance page already says ("$67, shipping included"). Changes: plan price in Shopify Subscriptions; one sentence in the order page terms box ("with free shipping" to "shipping included"); the regular product page would show the plan as $57.01 plus shipping.
- **B:** make Great Again T ship free always and add the first $9.99 as a "Shipping and handling" line in the cart. Keeps "$67 with free shipping", but needs a new hidden product and a shipping profile, and anyone who types the code on the regular product page would get the bottle with no shipping charge.

## Left to do

1. Dan picks fix A or B; apply it; set `trialOpen: True`; rebuild and deploy.
2. Install the purchase pixel (Settings > Customer events).
3. One real test order of each option, then cancel the test subscription (card entry: Codex or Grokbot). Handoff: `Handoffs/handoff-20261117-gat-funnel-finish-shipping-pixel-test-order.md`.
4. Video: when Great Again T VSL (WV-03) is approved, set `CFG['video']` and `revealAt` (the second Dan says "So if you already know you want this").
5. Launch day: `LAUNCHED = True` (removes noindex), rebuild, deploy.
6. The $97 store listing picture in the letter (grey block): the listing is $97 now, so it can be captured.
7. The 7-day reminder email before the first $67 charge; Dan's Part C items in the compliance Doc; the two label differences (directions and warnings wording).
8. 3 and 6 bottle packs are still $129 and $234.

## Undo

Set the twelve pages to Hidden (or delete them) in Online Store > Pages; delete discount `FREEMONTH`; remove the gat files from the theme (`layout/gat.liquid`, `templates/page.gat-*`, `snippets/gat-info-*`, `assets/gat*`); remove conversion action 7907328453.
