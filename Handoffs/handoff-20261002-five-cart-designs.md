# Five Abs By AI cart designs

Created October 2, 2026. Ready for a new design task.

Recommended model: **Codex GPT-6 Astra, high effort**. This is a flagship visual design exploration with browser verification, consistent with Dan's routing. Name the task **Abs By AI Five Cart Designs**.

## Goal and deliverable

Create five complete, polished, interactive cart mockups for Abs By AI. Dan wants one closely following the research recommendations, one closely modeled on Healthy Back Institute's healthandwellnesstools.com cart, and three more creative interpretations of the researched principles. Make the creative designs feel specific to Abs By AI and improve clarity, perceived value and ease of purchase. Do not claim they outperform existing carts before testing.

Deliver a single comparison gallery with five clearly named designs, individual links, full mobile and desktop views, and screenshots. Every design must extend through plan selection, the selected order summary and a simulated payment step. Show the finished designs, not just descriptions or wireframes. Complete all five before asking Dan to choose.

This task ends with design review. Do not replace the live cart, change pricing, enable billing or start an experiment. Any prototype payment controls must be inert or simulated. Keep prototype source separate from production checkout code.

## Read first

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

1. Read `AGENTS.md`, `AI_COORDINATION.md` and `Docs/WEB_CART.md`. Respect other sessions' ownership.
2. Read the full research report and inspect the actual screenshots. Main report:
   `/Users/danielrose/.codex/visualizations/2026/10/02/01a0fdb9-226b-7373-b9cb-c30cb8a8289e/cart-teardown/cart-teardown-report.html`
3. Read the deeper HBI artifact in that same directory: `healthandwellnesstools-cart.html`.
4. Inspect the present cart's code and visual system in `public/index.html`, along with relevant styles and assets. Use `https://absbyai.com/?demo=checkout` for the existing visual baseline. This documented demo disables payment and does not create a Stripe session.
5. Verify what the current product actually includes before writing benefit copy. Ground the offer in real coaching, training, nutrition and member tools found in the product. AI image generation stays a member feature, not a new free acquisition hook.

The research files are local to Dan's computer. If the new task uses a different host, bring the named source bundle into that workspace before starting. Do not substitute remembered competitor pricing or fabricated screenshots.

Additional existing screenshots are in `Docs/cart-research-20261002/`. These came from the parallel research work and were not reconciled with this report. They may supplement it after direct visual inspection. They must not silently overwrite the verified findings below.

## Evidence and its limits

Use these observations as the design foundation:

| Advertiser | Verified mechanism | Source files in the main research directory |
|---|---|---|
| HBI, healthandwellnesstools.com | Free bottle trial selected; $9.95 shipping today; $49.95 plus $3.95 shipping and tax every 30 days beginning day 30. One-time BOGO alternative, two bottles for $59, removes continuity terms. Numbered form sections, concrete summary, substantial reassurance, 90-day guarantee and an unchecked offer agreement immediately before Order Now. | `hwt-cart-initial.jpg`, `hwt-cart-bogo.jpg`, `hwt-offer-detail.jpg`, `hwt-renewal-detail.jpg` |
| HBI, losethebackpain.com | Free collagen jar with $9.95 shipping; monthly replenishment described below payment fields; benefits and doctor recommendation beside the form. | `hbi-collagen-cart.jpg`, `hbi-trial-cart.txt` |
| MadMuscles | Quiz and email lead to personalized summary, program contents, printable bonus, three plan durations. One month is the default because it has the lowest first payment: $15.19, then $39.99 monthly. Initial and renewal prices appear on each card, then again above wallet/card methods. | `madmuscles-plans.jpg`, `madmuscles-cart.jpg`, `madmuscles-cart.txt` |
| Muscle Booster | Personalized target and three plans. Middle four-week plan default, $19.19 initially, explicitly $43.95 every 31 days thereafter. Daily-price framing, repeated CTA, countdown and conditional money-back guarantee. | `musclebooster-plans.jpg`, `musclebooster-cart.jpg`, `musclebooster-plans.txt` |
| NativePath | Single jar selected; larger bundles visibly add value. This inspected route did not show recurring product billing. | `nativepath-cart.jpg` |
| BODi | Annual default, $119 initially, $179 renewal. Monthly equivalent near CTA. Separate optional Shakeology subscription offer with its own renewal explanation. | `bodi-plans.jpg`, `bodi-cart.jpg`, `bodi-cart.txt` |
| BetterMe | Quiz answers feed a wellness profile and personalized goal trajectory. Current cart was not reached in this report. | Report section 08; `betterme-ad.jpg` is ad evidence, not cart evidence. |

V Shred, Noom, Gundry and Agora cart coverage was incomplete in this report. Stansberry's captured cart was supplementary, not conclusively the endpoint of its leading ad. VidTao spend is estimated. These advertisers run the observed patterns; that alone does not demonstrate that a specific design element caused profitable sales. Dan has firsthand evidence that the HBI cart worked well for his business, and specifically wants it treated as a major reference.

Do not restart the whole research project. The verified evidence is enough to build five designs. Label creative adaptations as our design decisions, not observed competitor behavior.

## Shared offer across all five

Use the same product and financial terms so Dan can compare visual and structural choices fairly. The research-time project baseline is:

- Seven-day free trial, $0 today.
- Monthly $19.99, selected initially.
- Annual $69.99, with the documented 71% saving versus twelve monthly payments.
- First paid charge after the seven-day trial, then monthly or annual renewal according to selection.
- Account/password setup after payment in the web flow. Do not introduce a password gate for these prototypes.
- The trial reminder row and 48-hour reminder email are OFF by Dan's decision. Do not promise or re-enable them.

Confirm these values against current project code before building. If they changed since the report, use the current verified values consistently across all five and note the difference outside the customer-facing mockup.

Selecting a plan must update all summaries, trial dates and renewal text. Use one clearly identified sample customer profile across the gallery, and keep sample data outside any real customer system. State prototype status in the gallery, not as intrusive internal notes inside every cart.

Do not import competitor prices, physical shipping fields, bottle quantities, guarantees, review counts or medical endorsements into Abs By AI. Use the real product's support and cancellation details. A trial is not a money-back guarantee. Where the product has no substantiated testimonial, use real product evidence rather than invented customer quotations. No arbitrary countdown or new paid bump is required. This is a cart design task, not a new offer-development task.

## Design one follows the recommendations closely

Working name: **Your Plan Is Ready**.

Use the report's recommended order: personalized headline and compact goal recap; actual program contents; two clear plan cards; selected plan summary showing today, first charge and recurring amount; visible available payment methods; cancellation and help; deeper proof or FAQs with a repeated CTA.

MadMuscles is the primary structural reference. Preserve the lowest-commitment monthly default. Make the visitor understand what they receive before showing payment. Use clear initial and renewal prices on the cards and in the final summary. Show an included program summary or printable plan only if the product supplies one. Keep the composition clean and directly usable as a candidate for implementation.

## Design two closely models Healthy Back Institute

Working name: **Start Your Seven Days**.

Study the full healthandwellnesstools.com trial and BOGO screenshots before drawing this. Dan wants recognizable structural fidelity, not a generic page with an HBI label.

Carry across its direct-response density, strong offer selector, product/offer summary, numbered checkout stages, prominent action button, adjacent benefit and reassurance panels, and explicit continuing offer beside the final decision. On desktop, use a form/order column with a supporting value column; on mobile, preserve a logical reading and buying sequence.

Translate physical-product logic into a digital membership. Replace bottle presentation with real app/program previews. Replace shipping stages with relevant contact/plan/payment stages. Map its two-offer comparison to our monthly and annual choices, both with accurate subscription terms. Do not mislabel the annual plan as a one-time lifetime purchase. Adapt the trial agreement treatment if useful, and make its checked state functional in the prototype. Use actual support and trial reassurance where HBI has its physical-product guarantee.

Keep enough of the source's practical, sales-focused character to make the comparison meaningful. Avoid polishing away the very hierarchy and density we are testing.

## Designs three through five are creative interpretations

The designer has broad creative freedom in composition, typography, hierarchy, color treatment, app presentation and interaction. Retain recognizable Abs By AI branding and researched selling principles. Do not produce three palette swaps of Design one. The following are starting territories, not mandatory wireframes; improve or rename them if a stronger direction emerges.

### Design three makes the actual program tangible

Working name: **Your First Week**.

Make the immediate member experience concrete through real app previews and a concise first-week program outline. Connect what the visitor said they want with what they can do after joining. Ground this in MadMuscles' program contents and printable-plan presentation, and BetterMe's personalized recap. Give the order summary a strong, stable place in the composition. Keep it a complete checkout, not a feature landing page.

### Design four emphasizes personal guidance

Working name: **Built Around You**.

Create a more personal, editorial composition centered on the user's goal, schedule and training preferences, with the payment decision kept simple. Use genuine Dan/product material only where available and appropriate. Ground the concept in BetterMe's profile and trainer presentation, MadMuscles' personal summary and HBI's benefit/reassurance structure. Use product credibility without borrowed endorsements or invented testimonials.

### Design five makes choosing and buying exceptionally clear

Working name: **Choose Your Plan**.

Create the strongest compact, mobile-first decision screen: visually decisive plan comparison, concrete membership value and an immediately understandable total. Use MadMuscles' review panel and low-first-payment framing, Muscle Booster's plan hierarchy and BODi's annual-cost presentation as references. The page can be visually bolder and more distinctive than the conservative design. A sticky payment summary is a permissible creative adaptation, but must not obscure information or the form.

## Build and presentation standards

- Produce complete responsive HTML/CSS prototypes with working plan selection and simulated progression to payment. Prefer code-native interface design for accurate typography and interactive states.
- Use the existing approved logo and real product assets. If image generation would materially improve a concept, follow the current project image rules: **Use the Codex subscription to generate the images.** Read the shared image/video rules before any photo or generated-image work. Do not redraw real photographs of Dan.
- Use customer-facing copy that belongs to Abs By AI. Keep advertiser names, research commentary and design explanations in the comparison gallery, outside the cart itself.
- No em dash or en dash in new writing.
- Show each design at approximately 390 px mobile width and 1440 px desktop width. Check a narrower 360 px phone for overflow. Ensure terms, totals and payment actions remain readable.
- Capture at least one full mobile and one full desktop screenshot per concept, plus any separate payment state necessary to understand it. Inspect all screenshots before delivery.
- Include a concise rationale for each: advertiser reference, what was retained, what is our adaptation, intended benefit and principal tradeoff. Include a comparison view and recommend one lead candidate and one challenger. The recommendation is a hypothesis for testing.
- Keep all five self-contained and usable from the gallery. Do not make Dan open a development tool or install packages to compare them.

## Completion and scope

Finish all five, verify their links and interactions, and deliver the gallery plus screenshots and editable source. Save the outputs durably under a dedicated design/review directory according to the project workflow, outside live checkout routes. Do not overwrite the research artifact. Use only task-owned files in any commit; follow the safe-push rule for the shared checkout. Do not add a dashboard task unless Dan requests it.

At delivery, recommend which design to implement first and which to test against it, in plain language. Judge eventual performance on cost per trial, cost per paying customer, trial-to-paid conversion and retention/refunds. Do not select a winner solely because it is prettier.

Stop after the five-design review deliverable so Dan can choose. His later choice will define the production implementation task.

## Starter prompt

Name this task Abs By AI Five Cart Designs. Read and execute `Handoffs/handoff-20261002-five-cart-designs.md` in the Abs By AI project. Create all five complete interactive cart mockups: one faithful to the research recommendations, one closely modeled on the healthandwellnesstools.com Healthy Back Institute cart, and three distinct creative adaptations for Abs By AI. Deliver a comparison gallery with mobile and desktop screenshots, working plan selection and simulated payment states. Use the existing research and actual product features. If images are needed, use the Codex subscription to generate the images. Finish all five before asking me to choose. This is a design review task; do not replace the live cart.
