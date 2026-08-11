# AI generation costs — what we actually spend, and the levers that work

Measured 2026-08-10 from the real Replicate prediction history (708 runs,
2026-07-23 → 2026-08-10) plus PostHog product telemetry. Re-derive with the
Replicate `/v1/predictions` API rather than guessing; note it **403s on Python's
default user-agent**, so send a normal one.

## The headline: content production is the cost, not the product

| | Cost | Share |
|---|---|---|
| Content production (marketing stills, ad clips, retouching, bake-offs) | ~$100 | **92%** |
| Customer-facing generations (the FLUX/Seedream challenger legs) | ~$8 | 8% |

**~$109 in 19 days ≈ $172/month.** Over the same period PostHog recorded ~80 real
user generations in four months. **Optimising the product path is not where the
money is** — it is discretionary project spend on making content, and it is bursty
(Aug 4–7 alone was over half the total).

Biggest line items: `nano-banana-pro` 315 runs ≈ $42 · `kling-v3-video` 33 ≈ $33 ·
`veo-3.1` 5 ≈ $16 · `flux-kontext-pro` 142 ≈ $6.

## Levers that work

1. **Draft cheap, finish expensive.** 315 Pro-rate image runs produced maybe 20
   keepers. Every rejected exploration cost full price. This is the biggest lever.
   - Editing an existing photo → the dial is **resolution** (2K draft $0.134 → 4K
     final $0.24, 44% off drafts). 1K and 2K cost the same, so 2K is the draft tier.
   - Generating a **new** image → the dial is **model** (Nano Banana 2 ≈ half price,
     ~2× faster) for exploration, Pro for the keeper.
2. **Batch API, 50% off.** Google-direct only; Replicate has no batch tier. A
   2-image batch measured **under 4 minutes**, not the documented 24-hour worst case.
3. **Draft video on Dan's Google AI Pro subscription, free.** See the `make-ad`
   skill. Watermarked and 720p, so drafts only — but ~30 of 40 takes are drafts.

## Levers that do NOT work — do not re-derive these

- **Switching models to save money on a retouch.** Measured on
  `public/img/proof/male-before.webp`: `gemini-3.1-flash-image` changed the
  subject's shorts from black to grey and shifted the framing. Same failure class
  the `photo-edit` skill already records for Seedream and FLUX. Nano Banana Pro is
  the only model that edits in place.
- **Leaving Replicate for direct APIs to save on rates.** For the models we use it
  is near parity — FLUX Kontext is $0.04 at Black Forest Labs, Veo is $3.20/8s
  either way. Replicate's volume discounts start around $30–50k/month of spend; we
  are at $172. The one real reason to go direct to Google is **batch**, not rates.
- **Using the Gemini subscription for the API.** Google AI Pro/Ultra are consumer
  products and include **no API access**; API usage bills separately through Cloud
  Billing. The subscription cannot reduce the product's per-generation cost at all.

## The one product-side number worth watching

The round-8 swap moved the male anchor from `gemini-2.5-flash-image` ($0.039) to
`gemini-3-pro-image` ($0.134), so a male generation went ~$0.08 → ~$0.17. Invisible
at 80 generations; at 10,000 it is $1,700 vs $800, and members are unlimited.
Nano Banana 2 is the documented one-line fallback (see `AI_COORDINATION.md`).
