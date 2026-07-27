# Round 2 — female model test (Gemini vs Seedream 4.5)

Steps 1–2 of `handoff-20260727-female-seedream-swap.md`. **No production code is
touched by anything in this folder.**

## Why

Every female generation is supposed to be a two-model race (Gemini 2.5 Flash
Image + FLUX Kontext Pro, Claude judge picks). FLUX's safety filter refuses ~75%
of female photos (E005), and `safety_tolerance` is already at its image-input
ceiling of 2 — so women silently fall back to Gemini-only. This batch tests
Seedream 4.5 as the replacement leg for women. Men are out of scope.

## What ran

3 declared start conditions × 2 intensities × 2 models = 12 images, single-shot,
**no `deviceId`** (so no credits spent and no data-file commit / redeploy churn).

- Gemini gets the **full** prompt, the challenger gets the **condensed** one —
  matching what production sends each leg.
- Intensities are `dramatic` (Subtle) and `max` (Ripped) — the only two the
  product actually offers.
- Prompts come from prod `/api/generate-prompt`, driven by the real
  `SYSTEM_PROMPT` / `goalSystemPrompt()` extracted from `public/index.html`
  (`../prompts.js`), so the FEMALE HEAVIER REALISM RULE is exercised for real.

## Known coverage limit

Only **one** female identity exists in the proof assets — round-1's
`heavier-female.jpg` is the same subject as `public/img/proof/female-before.webp`,
and `female-after.webp` is the same woman leaner. So the grid varies starting
body state and declared condition, not identity or skin tone. **No dark-skinned
female subject was tested.** Round 1 found skin tone is exactly where Seedream
won, and that the hardest moderation cases were dark-skinned — so that gap is
worth closing before the result is treated as covering all women.

## Run order

```
node build-prompts.js    # caches prompts + asserts they fit Seedream's 4000-char limit
node run.js              # generates images; reruns reuse cached cells, never re-spend
node build-gallery.js    # blind gallery + key.json (slot-A balance is asserted)
```

`../.env` (0600, gitignored) supplies `GEMINI_API_KEY` and `REPLICATE_API_TOKEN`.

## Result

12/12 produced, **zero Seedream moderation blocks on female photos**, nominal
spend ~$0.47. Longest condensed female prompt is 1,391 chars, so
`condenseForKontext` can feed Seedream unchanged — no extra trim needed in
`server.js`. Blind labels from Dan are the gate for shipping the routing change.
