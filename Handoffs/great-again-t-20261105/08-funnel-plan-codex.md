# Great Again T: comprehensive funnel plan (Codex handoff, 2026-11-10)

**Owner:** Codex, newest Sol (`gpt-6.1-sol`), high effort. **Deliverable:** recommendations only. Do not film, build, change the store or ads, email customers or spend. Dan decides from your recommendations; execution comes in later tasks.

Dan authorized this research and the deliverable; do it start to finish without asking him anything.

## What Dan asked for (his words, condensed)
"I want it to recommend what set this should be on. Do some research and see what the most successful ones are. Options are outdoors, studio, or green screen. I'm leaning towards studio or green screen because, outdoors, I've never seen a successful sales video for fitness filmed outdoors."

"Whether this should be filmed vertically or horizontally, or both, or maybe just as far as we can from horizontal and then turning into vertical."

"Who the spokesperson should be... Maybe I'm not the best spokesperson for this. If you look at Testo Greens and Test Reload, where we saw success with it, it was the older guys that sold almost all the Test Reload. The younger guys in their late 20s and 30s didn't sell as much. The difference is I'm now in my 40s, so I'm kind of in between. Should I be the spokesperson? Should I have someone else be the spokesperson, or should I test both?"

"A January promotion. Should we offer a special discount? Should I just present it as a discount, like January-only free month, etc.? Give me recommendations for how to present the continuity the way Healthy Back Institute does it for Heal and Soothe. Look that up. I think they do it pretty well, but look up the way other brands are presenting their continuity that is effective, converts, and is Google Ads compliant."

"Think about the other details of the VSL as well, like how it should be edited and how the page should look. Should I have nothing on the page or VSL, like we did for Abs By AI? ... go beyond what I made here, and I want a comprehensive set of recommendations for all the important things we'll need to make this VSL a converting piece or a converting funnel."

"Upsells... making the first upsell maybe a bundle package that cancels their subscription. Second upsell: Abs By AI. Third upsell: coaching. That's like $5,000 a month or an extremely high price. Maybe that coaching upsell should be first, so that way the other ones don't seem as high. I do have other supplements to sell. Maybe it'd be better to sell the other supplements and the upsells rather than coaching in the Abs By AI app."

## Read first
- Dan's final VSL script (his own writing): `.claude/skills/dan-copywriting/examples/great-again-t-vsl-final-20261110.txt` (Google Doc `1CmK7ZG45x-p7mXATjvlWzuUpvlr7AQMHUbiQcdMYCFI`). Its offer: $97 for one month; first month free, customer pays shipping; then $67 a month; 31% off; full-year money-back guarantee on unopened bottles; sold only on SixPackAbs.com; quiz-funnel notes in his outline (V Shred style).
- Winners' research: `Docs/testosterone-funnels-20261105/VSL_TRANSCRIPTS.md` (TestoGreens Max horizontal 51:50; V Shred Test Boost Max vertical 28:19 behind a dummy 4-question quiz) and `FUNNEL_MODEL_RECOMMENDATION.md` (VidTao spend, landing pages, quiz test).
- Earlier Great Again T planning: `Handoffs/great-again-t-20261105/START-HERE.md`, `creative-brief.md` (v1.1), `research-evidence.md`, `evidence-record.json`, `01-research.md` (Test Reload winners and losers), `02-offer.md`, `06-studio.md`, `07-demand-test.md`.
- Lessons: `Docs/VSL_SCRIPT_CONTEST_RESULT_20261110.md`. Store and fulfillment: `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_20261105.md` (shop.sixpackabs.com, Shopify, Supliful fulfillment, Dan's other SixPackAbs supplements).
- Rules in `AGENTS.md`: "Marketing advice: proven direct response only" (name which top brand runs each tactic; nothing speculative), "Website design: phone first", "Cart and page design quality" (Opus's Healthy Back Institute cart is the benchmark), "VSL scripts: from Dan's outline". Memory: `model-proven-funnels-exactly` (copy what winners actually do, checked against their pages and transcripts).

## Answer each question with evidence
For every item: your recommendation, which proven brands do it (with links or screenshots), how confident you are, and how to test it cheaply if the evidence is mixed. Prefer brands currently spending (VidTao recent spend if you can access it; never start the paid VidTao trial), and supplement and men's health funnels over generic advice.

1. **Set:** outdoors, studio or green screen. What do the top-spending fitness and supplement VSLs actually use?
2. **Orientation:** vertical, horizontal, both, or horizontal turning vertical. Weigh the traffic (mostly phones via YouTube ads), V Shred (vertical) and TestoGreens (horizontal), and the cost of filming both.
3. **Spokesperson:** Dan (41, ripped, 4.46M-subscriber channel), an older man in his 50s or 60s, or test both. Use the Test Reload talent and age evidence in the files above. Cover truthfulness (the spokesperson's story must be real), casting cost and how to split-test talent on the same script.
4. **January promotion:** a real January discount, a January-only free month, or another framing the winners use for seasonal offers. Scarcity must be real.
5. **Continuity:** how Healthy Back Institute presents Heal-n-Soothe continuity (VSL wording, order page, checkbox, disclosures, cancellation terms), plus at least three other converting supplement brands. Recommend Dan's presentation of "first month free, then $67 a month", and exactly what Google Ads requires for subscription and free-trial offers to stay approved (clear terms, price and billing frequency, easy cancellation). Note what Shopify and Supliful need for subscriptions.
6. **Editing:** how the winners edit (on-camera versus B-roll ratio, study cards, captions, graphics, pacing, cut rate), and a recommended edit spec for Dan's script.
7. **Page:** a bare page with only the video and a delayed button (like Abs By AI) versus copy, bullets, studies and reviews under the video; the quiz pre-page; button delay timing; headline; trust badges; the "studies below this video" section his script promises. Phone first: describe or sketch the 390px page first.
8. **Upsells:** evaluate Dan's sequence (a bundle that replaces the subscription; Abs By AI; coaching around $5,000 a month, possibly first as a price anchor) against his other supplements as upsells, order bumps and downsells. What do V Shred, TestoGreens, Healthy Back Institute and similar funnels actually run after checkout? Recommend the order, prices and offers.
9. **Everything else that decides conversion:** checkout design, order bump, guarantee presentation, Google Ads ad and landing-page policy risk for supplement claims, payment processing and chargeback risk for continuity, tracking (Google Ads purchase conversions, PostHog), retargeting, abandoned-cart follow-up, page speed, and the test sequence and budget (build on `07-demand-test.md`).

## Output
1. A Google Doc titled "Great Again T Funnel Plan (2026-11-10)", shared as anyone-with-the-link can view: an at-a-glance table first (question, recommendation, proven by, confidence), then one short section per question with evidence links, then "Decisions for Dan" (one line each).
2. The same content as `Docs/GREAT_AGAIN_T_FUNNEL_PLAN_20261110.md`, and each open decision added to `Docs/DAN_DECISIONS.md`.
3. Plain language Dan can read quickly. No em dashes or en dashes. Commit and push your files (plain git in a worktree; `scripts/git/safe-push.sh` in the main folder).

Done when the Doc link and both files exist, every question above has a recommendation with named proof, and nothing was built, filmed, changed or spent.
