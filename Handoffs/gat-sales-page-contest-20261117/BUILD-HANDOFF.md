# Great Again T sales page: code the approved Design D page, quiz and checkout

Written 2026-11-17 by Claude (Opus 5.5), at Dan's request ("give me a handoff for coding"). Website build, not video: no edit slot.
**Recommended model:** Claude Fable 5.2 at high effort (AGENTS.md: shop and payment builds are Fable's). Alternative if Claude allowance is short: Codex GPT-6.2 Sol High.

## The spec

- **Review page (the approved mockups, phone first):** https://claude.ai/artifact/V5jWex1Nzp7DsPU4TjZ2gm (round 6). Dan reviews it before launch; build from it now.
- **Generator that makes every page (M6, gitignored work folder):** `Media/research/gat-sales-page-contest-20261117/refine/`
  - `gen.py` builds `1-quiz.html`, `2-before-offer.html`, `3-after-offer.html`, `3b-after-offer-bottom-bar.html` (not chosen) and `4-checkout.html`. `python3 gen.py` re-exports the letter Doc first; `python3 gen.py check` must pass.
  - `letterdoc.py` turns Dan's Doc into the letter. `page.css` is all the styling. `assets/` holds every picture.
  - A versioned copy of the code (no images) is in `.claude/skills/design-sales-page/reference/gat-letter/`.
- **Letter copy source:** Google Doc `1klwTUdTl5q_17MTA5c1Dtv-Agm_-B3rBpxGQPOj1SCI` (Draft v2). Dan edits it directly; his edits win. Always re-export before a build. Never type letter copy by hand.
- **Design history and Dan's rules for this page:** `HANDOFF.md`, `LETTER-INSTALL.md` (this folder), memory `gat-sales-page-direction`, `Docs/DESIGN_QUALITY_LESSONS.md` ("Great Again T sales page").

## Locked decisions (do not reopen)

1. Funnel: green quiz (4 questions) → video page → offer reveals when the video reaches "So if you already know you want this" → checkout. Phone first, then 768 and 1440.
2. Offer bar: in the dark header, slides down at the reveal, stays pinned. Not the bottom bar.
3. Offer: first month's supply (60 tablets) free with **$9.99 shipping**, then **$67 a month** until cancelled. Second checkout option: one bottle, one time, **$97**.
4. Checkout: Healthy Back Institute order-page structure, a small bottle in each option row, no big bottle on top. Healthy Back's terms box, tick box and fine print copied with our details (as on `4-checkout.html`). Statement name "SIXPACKABS.COM". Contact **dan@sixpackabs.com** (no phone number).
5. Gold "1 YEAR / 100% MONEY BACK / GUARANTEE" seal (inline SVG in `gen.py`, `seal_svg()`).
6. Studies: 31 entries, no paper titles, always visible, nothing clickable. Study cards: 12.
7. Pictures: real before photos (labels under the photos), subtly aged after photos and founder avatar (label "Real photos of me, not AI-generated" kept), the 3-minute ab video YouTube screenshot with counts circled, food-only MORE / LESS cards (no video frame).
8. **Google Ads words stay off every page:** the full word for T, drugs, needles, prescription, injections, TRT, estrogen, aromatase, steroid, disease names, dying, depressed. `gen.py check` enforces it on all five pages, including alt text and scripts. Dan's 20 claim edits are already in the Doc (`docx/compliance_edits.json`).
9. No em or en dashes in page text.

## Build steps

1. Read the review page top to bottom on a phone width, then the generator. If the food-only swap cards still show missing images, run the open item below first.
2. Decide hosting with the default below and build the live pages from the generator (copy the pattern of `reference/round2-letter/build_live.py` + `verify_live.py`): the live HTML must be generated, not hand-edited, and must pass the same copy check.
3. Video: the final film is Great Again T VSL R8 (WV-03), still rendering on the M2. Until it is approved, use the poster and the placeholder player. Wire the reveal to the real timestamp of "So if you already know you want this" in the final film.
4. Checkout and billing: free first bottle + $9.99 shipping, then $67 every 30 days, cancel any time; one-time $97 bottle. Store state on 2026-11-17: Great Again T lists at **$47** one bottle, $129 three, $234 six on shop.sixpackabs.com. Changing store prices and adding the subscription are reversible shop changes inside this task. Do not change the other supplements.
5. Tracking: Google Ads purchase conversion (value, currency, order id) and PostHog events for quiz start/finish, video play, reveal, button clicks, checkout start and purchase. Do not fake a purchase.
6. Verify on the live site at phone, tablet and desktop width, then run a test order the way AGENTS.md allows (Codex or Grokbot for the real card step; Claude cannot type card details). Record a receipt in `Docs/` and update `Handoffs/README.md`.

## Open decisions, with the default to build

- **Hosting:** default = the pages live on **shop.sixpackabs.com** (Shopify, where Great Again T and Supliful fulfilment already are), the quiz and sales page as Shopify pages with the generated HTML, and checkout through Shopify checkout with a Shopify subscription app for the free-month-then-$67 plan. Our designed order page becomes the pre-checkout page that carries the option rows, terms box and tick box, then hands off to Shopify checkout. If a fully custom checkout is required to match the mockup, report the cost before building it.
- **One picture still missing:** the $97 store listing (grey block in the letter). Once the store shows $97, screenshot the listing (name, picture, price only) and drop it in.
- **Reviews:** built and hidden; stays hidden until real buyer reviews exist.
- **How to cancel:** add the method (email dan@sixpackabs.com, or a link in every order email) once billing is set up.

## Limits

- No ads turned on, no spend, no emails to customers or the list.
- Do not rewrite the letter. Wording questions go to Dan; the Doc is the source.
- Push shared files with `scripts/git/safe-push.sh`. Deploy, then verify live.
