# Handoff: five cart design mockups for Abs By AI

Written 2026-10-02 by the cart-research session. Recommended: **Claude Opus 5.5, High effort.**
Suggested task name: `Cart Mockups R1`.

## Goal

Mock up **five designs for the Abs By AI web cart** (the screen where a visitor starts the membership) so Dan can
pick one, or pick pieces from several, before anything is built into the live site.

1. **Design A, "Research pick".** Sticks closely to the recommended cart in the research brief (the ten pieces listed
   under "The recommended cart, top to bottom").
2. **Design B, "Healthy Back Institute".** Closely modeled on the Heal-n-Soothe free-trial cart on
   healthandwellnesstools.com. Dan ran ads to that cart and knows first-hand that it converts. Keep its structure
   and devices; translate the content to our product.
3. **Designs C, D, E, "Our own".** Three further designs that use the principles in the research brief and the best
   ideas from the successful carts, with much more of your own creativity. They should fit our concept (a visitor has
   just seen an AI picture of their own body with abs) and aim to beat the carts we studied, not copy them. Make the
   three clearly different from each other and from A and B, each with one stated idea behind it.

**This is a mockup task only.** No change to `public/index.html`, no deploy, no Stripe change, no site copy change.
Stop for Dan's pick at the end.

## Read first

- The research brief: **https://claude.ai/artifact/SCgHKoUcyN5mik1NvZLfmD** ("Continuity Cart Teardown").
  Read it with the Artifact tool (`action: read`). Its last sections are "The ten ideas for your cart" and
  "Analysis and recommendations for the Abs By AI cart".
- Local copy of the same page and every screenshot: `Docs/cart-research-20261002/`
  - `teardown-artifact-source.html` (the page source, with every quoted renewal sentence)
  - `NOTES.md` (raw research notes: exact wording, defaults, prices for each cart)
  - `full-hwt-free-trial.jpg` and `full-hwt-bogo-trial.jpg`: the two versions of the Healthy Back Institute cart,
    full length. **Design B is built from these.** `full-hwt-product.jpg` is the product page that feeds it.
  - `mm-plans.jpg`, `mm-purchase.jpg`, `full-mm-paywall.jpg` (MadMuscles), `mb-top.jpg`, `mb-plans.jpg` (Muscle
    Booster), `bodi-*.jpg`, `gm-*.jpg` (Gundry MD), `vs-*.jpg` (V Shred), `np-*.jpg` and `full-np-cart.jpg`
    (NativePath), `st-*.jpg` (Stansberry).
- The cart as it is today: `Docs/WEB_CART.md`, and the live demo at `https://absbyai.com/?demo=checkout`
  (add `&locked=1` or `&sex=female`). Markup is `#cartSection` in `public/index.html` (about line 2967).
- Earlier teardown (text only, Sept 10): https://claude.ai/artifact/MevY5JFc7FTEAikSbQhreV
- Skill: `.claude/skills/design-sales-page/SKILL.md`. Read it before designing and follow whatever it locks.
- Standing rules that apply: `AGENTS.md` ("Marketing advice: proven direct response only", "No compliance commentary
  unless the task is compliance", "Never use an em dash"), memory `proven-direct-response-only`,
  `web-cart-pay-first`, `paying-members-count`, `standard-before-picture`, `before-after-same-person`.

## What the research found (short version)

- Every cart that sells continuity puts the renewal sentence next to the button. HBI and BODi add an empty tick box
  the buyer must check. MadMuscles now prints the renewal price on every plan card.
- The first payment is small and shown first: $9.95 (HBI), $15.19 (MadMuscles, Muscle Booster), "$9.92/mo" on the
  button (BODi).
- MadMuscles and Muscle Booster open the paywall with a "Now" and "Goal" body picture. Ours can be the buyer's own
  photo and their own generated image, which none of them can match.
- Every cart except MadMuscles shows a guarantee near the price. Every cart shows ratings or reviews.
- Urgency is split: Muscle Booster, V Shred and NativePath run a countdown on the cart; MadMuscles removed its timer;
  HBI, Gundry MD and Stansberry run none.
- HBI's cart, the one Dan trusts: one default offer, a tiny amount due today, the deal explained under a plain
  heading ("How this FREE Trial Offer Works"), a tick box, doctor and customer quotes down the right side the whole
  way, a 90-day guarantee and the card-statement name under the button, a phone number top and bottom. Its second
  version adds a selector above the form: a pricier one-time choice ("Buy 1 Get 1 Free, $59") sitting above the
  pre-selected free trial.

## The facts every design must use

- Product: Abs By AI membership. Monthly **$19.99**, Annual **$69.99** ($5.83 a month). Today the cart offers a
  **7-day free trial** with Monthly pre-selected. Payment is Stripe's embedded form (email plus card, Apple Pay
  first), and the account is created after payment.
- What a member gets: the AI trainer built from their photo, unlimited transformations, meal tracking and the AI
  nutritionist, progress log, sleep coach, supplement audit. Check `Docs/WEB_CART.md` and the live cart for the
  current benefit lines and use those words.
- The buyer arrives from the analysis page having just seen their goal image and their body-fat numbers.
- **No invented proof.** There are no paying members yet (memory `paying-members-count`), so do not write fake
  ratings, member counts or testimonials as if real. Where a design needs proof, draw the slot with clearly marked
  placeholder text ("Member quote goes here") and say in the notes what real material would fill it (the /review
  page is collecting it). Dan's own before and after is real and can be used; follow `standard-before-picture`.
- Use the public sample before/after pair the demo cart uses for the "Now" and "Goal" pictures.

## Dan's five open decisions (not answered yet)

The research brief ends with five questions. Dan has not answered them. **Do not ask him before starting.** Use the
five designs to show the options, and say in each design's notes which answer it assumes:

1. Offer shape: 7-day free trial (today), or a paid first period (for example $1 or $4.99 for the first week or
   month, then full price), or HBI's shape (a small charge today, then the full price).
2. Default plan: Monthly or Annual pre-selected.
3. Countdown or reservation bar: yes or no.
4. Guarantee length (30 days is the common one).
5. Tick box above the button: yes or no.

Design A follows the brief's recommendation on each. Design B follows HBI on each (small charge today or free
trial with the terms box, tick box yes, no timer, long guarantee). C, D and E each make their own stated choice.

## Deliverable

One artifact, "Cart Mockups", built as a real page:

- Each design drawn at **phone width (about 390 px)** as a live HTML mock, not a picture, with real copy written in
  full: headline, plan cards, the terms block, the button text, the lines under the button. Dan reads the copy as
  much as the layout.
- Design B also gets a **desktop-width** version, because the HBI cart's proof column down the right side only
  exists on a wide screen. Show how that column folds on a phone.
- A switcher at the top to move between A, B, C, D, E, and a way to see two side by side on a wide screen.
- Under each design: a short "Borrowed from" line naming the advertisers behind each device, and a "What I decided"
  list (the assumptions made on the five open decisions and anything else Dan might overrule).
- One comparison table at the end: the five designs against the five decisions.
- End with a single question to Dan: which design, or which pieces of which.

Follow the `artifact-design` skill for the page. Keep the Abs By AI look for the mocks themselves (take colours,
type and button style from the live cart and `/start`), so the differences Dan sees are structure and copy.

## Rules for the copy inside the mocks

- Plain, direct-response copy in Dan's voice. No em dashes anywhere.
- The renewal sentence must state the price, the interval, "until you cancel" and how to cancel, and sit next to
  the button in readable type. That is the one thing every studied cart does.
- Only use devices that one of the studied advertisers actually runs, and name which one. The three creative
  designs can combine and re-stage those devices in new ways for our product; they should not invent a new kind of
  offer.
- Do not add commentary about compliance or legal risk to the page.

## Not in scope

- Building any design into the site, changing prices or the Stripe setup, changing the trial, writing the cart
  video, or touching the iOS and Android apps.
- BetterMe and Noom paywalls were not walked in the research session. Not needed for this task.

## After Dan picks

Write a build handoff for the chosen design (changes to `#cartSection`, the events in `Docs/WEB_CART.md`, tests in
`scripts/cart/cart-fulfillment.test.js`, deploy and live check). That is a separate task.

## Starter prompt

```
Read Handoffs/handoff-20261002-cart-design-five-mockups.md and execute it. Rename this task "Cart Mockups R1".
Mock up five cart designs for Abs By AI in one artifact: A follows the research recommendations closely, B is
closely modeled on the Healthy Back Institute cart, and C, D and E are your own more creative designs built on the
same research. Mockups only: no site changes. Start by reading the research artifact and the screenshots in
Docs/cart-research-20261002/. Do not ask me the five open decisions first; show the options through the designs
and stop for my pick.
```
