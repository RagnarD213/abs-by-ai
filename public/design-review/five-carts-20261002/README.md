# Abs By AI Five Cart Designs

Design review, October 2, 2026. The live cart and billing code are unchanged.

Open `index.html` directly in a browser, or use the hosted review URL:
https://absbyai.com/design-review/five-carts-20261002/

All HTML, fonts, scripts and images are local to this folder. No installation is needed.

## Contents

1. Your Plan Is Ready: the research-led implementation candidate.
2. Start Your Seven Days: the close HBI structural challenger.
3. Your First Week: an interactive, tangible program preview.
4. Built Around You: a personal editorial composition with the real founder.
5. Choose Your Plan: a compact dark decision screen.

Each design supports monthly and annual selection, updated summaries and disclosures, card/Apple Pay/Link simulations, invalid-email feedback, a declined result, retry, success and reset. HBI also requires its unchecked agreement. The first-week design has seven working day selectors. Gallery supports any pair at 390, 360 or 1440 CSS pixels.

## Sample and offer

Alex is fictional. Goal: visible abs. Routine: 20 minutes daily at home with minimal equipment, consistent with the app's stage 3 training framework. This profile is assumed to be known for this design comparison. The present anonymous checkout normally collects onboarding answers after payment; production personalization needs an explicit source or a neutral fallback. No new pre-payment questionnaire is proposed here.

Fixed review date: October 2, 2026. All first charges fall on October 9, 2026, for a seven-day trial. Plan selection updates the amount and interval; the first charge date correctly stays the same for both plans. Monthly is $19.99; annual is $69.99, equivalent to $5.83/month. The displayed 71% saving is rounded versus 12 monthly payments ($239.88). No offer change.

The app includes 4-week training blocks and future blocks, exercise guidance, nutrition plans with recipes and grocery lists, meal/macro tracking, check-ins, Sleep Coach, 25 Supplement Audits/month and member goal images. The first-week guide is an illustrative use sequence, not a new product feature or a guaranteed outcome. Screenshots show existing demo programs, not a newly generated Alex program. No printable program is promised because one was not substantiated.

## Sources inspected

- `Handoffs/handoff-20261002-five-cart-designs.md`
- `Docs/WEB_CART.md`
- `public/index.html`: membership benefits, cart prices/default, cancellation and available payment copy
- `server.js`: training stage ladder and program generation rules
- Current public baseline: https://absbyai.com/?demo=checkout
- Original October 2 research bundle: `cart-teardown-report.html`, `healthandwellnesstools-cart.html`, full HBI trial/BOGO screenshots and offer/renewal details, MadMuscles plan/payment captures. Original bundle remains unchanged in the research chat's cart-teardown visualization directory.

Original assets, copied without retouching: `public/img/logo.png`, `public/img/dan-founder.jpg`, `public/img/letter/app-workout-day.jpg`. Existing AI exercise images retain their original AI labels. No new AI images or metered generation were needed. Manrope fonts are bundled from Google's font distribution.

HBI fidelity: free-offer emphasis, selected blue offer row, numbered stages, yellow action, pale form fields, adjacent benefit/reassurance panels and unchecked continuing-offer agreement. Digital plan selection replaces bottle/shipping logic. Both Abs By AI options are recurring. No physical-product guarantee, testimonials, ratings or endorsements were borrowed.

## Isolation and interaction

There is no Stripe library, billing endpoint, analytics or customer storage. Cart pages have `connect-src 'none'` and `form-action 'none'`; form submission is intercepted locally. Sample card fields are read-only. Apple Pay and Link are local mock states. Only explicit Support/Terms/Privacy links leave the prototype. No account, payment or email is created.

Select Declined in a design's review bar before opening payment. After a decline, close payment, select Success and reopen to retry. On design 2 the controls are inline. Escape and the close button dismiss modal payment. The success view describes the real next account-setup step without creating one.

## Editing

- `build.py`: five layouts and shared HTML components
- `styles.css`: responsive cart styling
- `cart.js`: local plan and simulated payment behavior
- `build_gallery.py`, `gallery.css`, `gallery.js`: comparison gallery
- `screenshots/`: five full desktop, five full mobile and payment/decline/success captures
- `verification.json`: observed browser check results

Run `python3 build_gallery.py` to regenerate the gallery and the five HTML pages. It does not overwrite screenshots. The pages run from disk or a static server.

## Verification

Checked in the browser at 1440 px desktop, 390 px mobile and 360 px narrow mobile. No horizontal overflow in any concept. Default monthly selection, annual/monthly summary changes, email validation, three payment-method views, success, declined-payment recovery and reset passed on all five. HBI agreement blocking passed. Screenshots visually inspected. Gallery links and embedded comparisons checked. Browser capture needed a device-scale correction for full-page exports; recorded layouts use actual CSS viewport dimensions.

## Recommendation

Lead with design 1. Challenge it with design 2 because it tests a materially different buying structure and follows Dan's firsthand HBI evidence. Designs 3-5 are alternative hypotheses, not measured improvements. Judge a later test on cost per trial, cost per paying customer, trial-to-paid conversion, retention and refunds. This task stops at design review.
