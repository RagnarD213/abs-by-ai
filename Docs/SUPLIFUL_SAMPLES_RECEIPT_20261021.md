# Supliful account and first sample order: receipt

2026-10-21, Claude (Opus 5.5). Executes `Handoffs/handoff-20261021-supliful-account-and-samples.md`.
Research behind it: [First Abs By AI Supplement: Supplier Research](https://docs.google.com/document/d/1CLNLlgJorAqdKDWVDFLpcxnOexAi8wt4pH7jsVbIkME/edit).
No personal data in this file (public repo): the shipping address, phone, email and card are in Dan's Supliful account only.

## Account

- Dan created the Supliful account himself in his Chrome and is on the **Free plan**. No Pro, no store, no Shopify.
- Billing details and a card were added by Dan (Supliful requires both before any order, samples included).

## Sample order

**Order SPL1238058**, placed by Dan 2026-10-21 7:22 PM CT, type SAMPLE, status New.

| Product | SKU | Qty | Unit (Tier 1) | Line |
|---|---|---|---|---|
| Creatine Hydration Powder (lemon, 300 g) | JTP31CRHY | 3 | $13.25 | $39.75 |
| Greens Superfood | JTP10GREE | 1 | $10.25 | $10.25 |
| Fat Burner with MCT | NOV32FATB | 1 | $11.75 | $11.75 |
| Sleep Formula | JTP32SLEE | 1 | $8.75 | $8.75 |
| Men's Vitality | VOX32MALE | 1 | $10.69 | $10.69 |
| Metabolic Health Formula | JTP32META | 1 | $8.89 | $8.89 |
| GLP-1 Support | JTP32GLP1 | 1 | $10.35 | $10.35 |
| **Subtotal** | | 9 | | **$100.43** |
| Discount (10%, whole order, 3+ units) | | | | −$10.07 |
| USPS standard shipping | | | | $14.48 |
| Fulfillment ($1.99 first unit per product, $1.29 each extra) | | | | $16.51 |
| Processing (2.99%) | | | | $3.63 |
| **Total charged to card** | | | | **$124.98** |

- No plain creatine monohydrate (Dan's call).
- Labels: none. Supliful ships draft products with its generic label, so no placeholder label was made.
- Expected delivery: Supliful makes in 2 to 5 business days, then USPS 2 to 4 days, so about **Oct 27 to Nov 3**.

## The 10 recommendations and Dan's picks

Dan's criteria (2026-10-21): multi-ingredient, not one-ingredient commodities; at least one greens powder (he has sold greens before); men 30 to 60 who want fat loss first, then muscle.

| # | Product | Sample price | Leader's equivalent | Picked |
|---|---|---|---|---|
| 1 | Greens Superfood | $10.25 | Sculpt Nation Greens, $69 | Yes |
| 2 | Fat Burner with MCT (stim-free) | $11.75 | Sculpt Nation Burn Evolved, $49 | Yes |
| 3 | Sleep Formula | $8.75 | Sculpt Nation Burn PM, $49 | Yes |
| 4 | Men's Vitality (tongkat ali 400 mg, zinc 50 mg, maca) | $10.69 | Sculpt Nation Test Boost Max, $49 | Yes |
| 5 | Metabolic Health Formula (berberine source + botanicals) | $8.89 | Noom Metabolic, $49 / 28 days | Yes |
| 6 | GLP-1 Support (digestive blend, probiotic, B vitamins, minerals) | $10.35 | Noom Metabolic, $49 (sold to GLP-1 users) | Yes |
| 7 | Nitric Shock Pre-Workout | $21.55 | Sculpt Nation Pre-Workout, $37 | No |
| 8 | Digestive Enzyme Pro Blend | $11.79 | Sculpt Nation Enzymes, $49 | No |
| 9 | Platinum Turmeric (contains shellfish) | $11.05 | Sculpt Nation Turmeric Black, $49 | No |
| 10 | Apple Cider Vinegar capsules | $8.19 | Sculpt Nation ACV Gummies, $29 | No |

Notes from the pick: Greens Superfood uses a small 4 g scoop (premium greens run about 10 g). GLP-1 Support carries 18 mg iron,
which most men don't need. Left out on purpose: whey and plant protein (commodity; $25 to $48 per tub on samples), magnesium
glycinate, berberine, collagen, glutamine (single ingredient), BCAAs (no EAA product at Supliful).

## Live prices vs the research (read 2026-10-21, logged in, Free plan)

Most moved up about 9% since the archived July prices:

| Product | Research | Live sample (Tier 1) | Live Pro tier 1 (0-49/mo) |
|---|---|---|---|
| Creatine Hydration Powder | $12.15 | **$13.25** | $9.85 |
| Magnesium Glycinate | $11.65 | $12.75 | |
| Sleep Formula | $8.75 | $8.75 | |
| Sleep Support | $9.19 | $10.05 | |
| GLP-1 Support | $9.45 | $10.35 | |
| Hydration Powder | $13.55 | $14.79 | |
| Performance Whey Blend | $23.29 | $25.39 | |
| Creatine Monohydrate | $14.69 | $14.69 | |

The research's creatine margin model assumed $9.85 per jar on Pro, which matches the live Pro tier 1 exactly. The margin table still holds.

## Supliful mechanics learned (for the next session)

- Prices are hidden until login. The logged-in catalog's tRPC call `catalog.getCatalogPricing` returns every product's
  `tierPricing`; its tier 1 is the sample/Free price, tier 2 is Pro 0-49 units.
- A sample needs the product in "My products": "Customize and sell" on the catalog page creates a draft instantly. No label or publishing needed.
- "Order products" stays greyed out until billing information is saved.
- The 10% sample discount applies to the whole order once it has 3+ units (max 3 units per product).

## Next

1. Dan tastes the creatine and the six picks when they arrive (about Oct 27 to Nov 3).
2. Then the research's step 2: Codex label designs, Dan's pick, label check, upgrade to Pro. Not started; no handoff written yet.
