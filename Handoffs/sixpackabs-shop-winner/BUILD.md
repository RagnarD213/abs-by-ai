# Handoff: build shop.sixpackabs.com (Shopify theme) and the sixpackabs.com homepage changes

Written 2026-11-05. **Fire now.** Not video. Recommended: **Claude Opus 5.5, high effort** (design-faithful page build; Dan judged Codex weak at design and picked Opus's cart as the benchmark). Must run **locally on Dan's Mac**: the design package is in `Contest/`, which is never committed (the repo is public).

## Goal

Code the approved Claude A shop design as a Shopify theme for the SixPackAbs store, matching the approved boards pixel-for-pixel at phone width (390) first, then desktop (1440). Then prepare the sixpackabs.com homepage changes (black top bar with gold logo, Supplements row, Shop links) for launch day. Stop for Dan's review before anything goes public.

## Approved inputs (read first)

- `Contest/claude/shop-final-design/COPY-READY.md`: approval, exact canvas version `1793888276-ce2e`, what is still open.
- Boards: canvas https://claude.ai/artifact/B5a3ooH254JfKdt8abBQAu (read with the Artifact tool) and the identical local copies `Contest/claude/shop-final-design/canvas/project/*.dc.html`. Previews: `previews/1-phone/` (start here), `previews/2-desktop/`, `previews/3-phone-and-desktop/`.
- **Copy:** `COPY-MAP.md` / `copy-map.csv`, column "Layout text". Dan, Nov 5: "We have our copy set." The board text is final. Do not rewrite it, do not run a copy task, no em dashes.
- Design tokens and component styling: `src/kit.py` (CSS at the top: ivory `#f3ede1`, paper `#faf6ee`, card `#fffcf6`, ink `#151412`, band `#171513`, gold `#C9A766`, gold text `#7d5f2a`, line `#e2d7c3`; fonts Archivo for display and the wordmark, Inter for body). The board HTML in `src/board-sources/` is drawing source, not site code, but its markup and CSS are the exact spec to match.
- Product facts, Supplement Facts, directions, cautions: `src/data.py` (transcribed from the final labels). Never edit facts.
- Sitemap and who controls each surface: `SITEMAP.md` and board X01. Design system: X02.
- Images: only the 49 files in `APPROVED-ASSETS.txt` (hash-checked). Logo: `assets/img/logo-symbol-gold.png` + "SIXPACKABS.COM" in Archivo 800, gold `#C9A766`. Guarantee seal: `assets/guarantee-seal.svg` (from absbyai.com/start).
- Store state: `Docs/SHOPIFY_SETUP_RECEIPT_20261104.md` (store `1yar3v-ie.myshopify.com`, Basic trial, password on, Horizon theme, Supliful app connected, no products, no subscription app).

## Privacy rule (label session, Dan-approved)

Website images = `Contest/claude/labels-final-round1/mockups-web/` derivatives only (already in `assets/`). **Never** upload or reference `mockups/`, the flat full-wrap proofs, print PDFs, SVGs, or `Contest/approved/sixpackabs-labels-final-20261105/` files: their back panels carry Dan's home address. Never commit `Contest/`.

## Build

1. **Theme code home:** a new private GitHub repo `sixpackabs-shop-theme`, checked out at `~/Projects/Claude/Projects/SixPackAbs Shop Theme` (same pattern as the private Social Response Marketing repo). Start from a duplicate of Shopify's Horizon theme (current reference theme, native cart drawer and selling plans) and restyle it; build custom sections where the boards need them. Shopify CLI (`shopify theme dev` / `theme push --unpublished`): if the CLI login needs Dan's browser approval, ask him once to click it.
2. **Global:** header (black band with gold rule, centered gold logo on phone with menu and cart icons; desktop nav per S03), phone menu, footer, design tokens, fonts, buttons, sticky add-to-cart bar on phones (shows once the main button scrolls off).
3. **Pages, phone first then desktop:** S01 home (F01 first screen), S02 all products, S04 to S09 product pages (F04 to F09 first screens: full-width centered hero on the stone, offer block, Supplement Facts panel then the guarantee card, Suggested Supplements), S10 cart drawer, S13 help, S14 policy layout, S15 contact, S16 states (sold out, search, toast, 404, password page). S11/S12 are Shopify-controlled: set only logo, colors and fonts in checkout branding.
4. **Products (draft, never active):** create the six products in Shopify as drafts with the approved images, facts and copy, so the theme renders real data. Offer = variants "1 / 3 / 6" at $47 / $129 / $234 (3 featured, 1 default). **Check before relying on it:** how Supliful maps a 3- or 6-unit variant to fulfillment, and whether Supliful's push will overwrite or duplicate these drafts. If Supliful needs its own product records, keep the theme logic variant-based and record the mapping problem for Dan instead of forcing it.
5. **Subscription ($42 every 30 days, opt-in, terms visible before add to cart):** build the theme to render Shopify selling plans generically, so any subscription app works. The app itself (receipt recommends Shopify Subscriptions, free) is **not installed**: ask Dan once, with the recommendation, before installing.
6. **Placeholders:** support email, response time, the "X" policy numbers and shipping rates are not decided. Put them in theme settings with visible-to-admin defaults, never invented values on public pages; list each for Dan.
7. **sixpackabs.com homepage (WordPress.com, boards C00 to C02):** build the black top bar with the gold logo, Shop in nav, menu and footer, and the six-card "Supplements" row between the long-form videos and Shorts (swipe on phones, six across on desktop), with the Electro Creatine strip removed. **Prepare it as a draft or staged template only.** Going live waits for the shop launch, because the cards would link to a password page. Standing site authorization covers the edit itself; the timing is Dan's call.

## Verify

- Every page at 390 first, then 1440: screenshot the theme preview beside the matching board preview; fix differences in spacing, type, colors, image crops. No horizontal scroll on phones. Products centered on phones.
- Add to cart for each offer, cart drawer quantities and totals, sticky bar, menu, search, 404, password page.
- Lighthouse mobile on home and one product page; report the scores.
- Check every public string against `copy-map.csv` (no invented copy, no em dashes, no product numbers).

## Stop for Dan (do not do these)

- Publishing the theme, removing the store password, or launching.
- DNS for `shop.sixpackabs.com`; Shopify Payments, business details, Texas tax permit.
- Supliful Pro ($69/month) or any paid app or theme purchase; installing the subscription app before he agrees.
- Making the sixpackabs.com homepage changes live before the shop launches.
- Test orders with real money, customer emails.

## Deliver

- A phone-first review page (phone screenshots first and readable, desktop beside or after) linking the unpublished theme preview URL, plus the list of open business facts.
- Receipt `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_<date>.md` (theme id, preview URL, repo, what was built, what is open; no address, no secrets), pushed with `scripts/git/safe-push.sh`. Theme code pushed to the private repo.
- Remove this handoff from `Handoffs/README.md` OPEN when done. End with the two wrap-up boxes.

## Starter prompt

> Read `Handoffs/sixpackabs-shop-winner/BUILD.md` in the Abs By AI project and do it. Dan approved all the SixPackAbs shop boards on Nov 5 (canvas version 1793888276-ce2e) and the board text is the final copy. Build the Shopify theme phone first, keep the store locked, prepare the sixpackabs.com homepage changes without making them live, and stop for my review with a phone-first review page.
