# The hold-out set (locked 2026-10-08)

Real passages of Dan's that the voice bench (`scripts/voice/bench.py`) uses as the "real" side of every
blind pair. **Never quote, paraphrase closely or summarize any of them in a guide, an example file, a skill,
a prompt or a memory entry.** They are listed by source and position only; the text is in
`voice-corpus/heldout/` on the Mac and in the Drive mirror, never in this repo.
`python3 scripts/voice/heldout_guard.py` fails if a file under `.claude/skills/_shared/` contains an 8-word
run from any of them. Run it after editing any voice file.

Whole files flagged held out in the corpus manifest (the HBI "Five Foods To Avoid" script) are off limits
from end to end, not only the passage listed here.

Some of these pieces are published, so their text also sits elsewhere in the repo (Ad 3 in
`scriptwriting/references/finalized-ad-scripts.md`, the sales letter in `design-sales-page/reference/`, one
short in `shorts-scripting/SKILL.md`, video transcripts inside edit plans). Those files stay as they are. A bench
setup must not load them: `bench.py` checks every file a setup gives the writer and stops if one holds
held-out text.

Thin spots: shorts (4 held out, not 6: only eight shorts are confirmed his), ads (5 of the 10 are ads he wrote for other
presenters, because his own ads total under 10,000 words), conversion (5 of 6 sell to business owners).

Changed 2026-10-10: `content-short-01` was the Battle Ropes short. Dan believes Claude wrote that script, so it left
the corpus and the set, and the Kettlebell Deadlift short took its place. Both baselines were re-scored with it.

| id | type | source file (under `voice-corpus/`) | position | words | tier | year | spoken or written |
|---|---|---|---|---:|---:|---:|---|
| content-long-01 | content | `content/tier1/absbyai/2026-arms-and-shoulders-home-workout.txt` | words 1345 to 1626 (middle) | 282 | 1 | 2026 | spoken |
| content-long-02 | content | `content/tier1/absbyai/2026-how-to-work-out-at-home-on-a-budget.txt` | words 923 to 1238 (middle) | 316 | 1 | 2026 | spoken |
| content-long-03 | content | `content/tier1/absbyai/2026-my-honest-zepbound-update.txt` | words 3919 to 4162 (middle) | 244 | 1 | 2026 | spoken |
| content-long-04 | content | `content/tier1/absbyai/2026-the-supplements-i-actually-take.txt` | words 1390 to 1640 (middle) | 251 | 1 | 2026 | spoken |
| content-long-05 | content | `content/tier1/absbyai/2026-how-i-make-my-daily-salad.txt` | words 2064 to 2360 (middle) | 297 | 1 | 2026 | spoken |
| content-long-06 | content | `content/tier1/absbyai/2026-welcome-to-abs-by-ai-channel-intro.txt` | words 658 to 818 (close) | 161 | 1 | 2026 | spoken |
| content-long-07 | content | `content/tier1/absbyai/2026-the-vacuum-best-ab-exercise-for-belly-fat.txt` | words 1962 to 2307 (middle) | 346 | 1 | 2026 | spoken |
| content-long-08 | content | `content/tier1/absbyai/2026-my-honest-oura-ring-review.txt` | words 3701 to 3935 (middle) | 235 | 1 | 2026 | spoken |
| content-long-09 | content | `content/tier1/old-channel/2021-make-15-more-money-no-extra.txt` | words 2431 to 2698 (middle) | 268 | 1 | 2021 | spoken |
| content-long-10 | content | `content/tier1/old-channel/2021-build-website-converts-youtube-ad-visitors.txt` | words 2835 to 3169 (middle) | 335 | 1 | 2021 | spoken |
| content-long-11 | content | `content/tier1/old-channel/2021-college-scam.txt` | words 3079 to 3446 (middle) | 368 | 1 | 2021 | spoken |
| content-long-12 | content | `content/tier1/tlab/2020-travel-like-a-boss-ep252.txt` | words 5658 to 5933 (middle) | 276 | 1 | 2020 | spoken |
| content-short-01 | content | `content/tier1/absbyai-shorts/2026-how-to-kettlebell-deadlift.txt` | words 1 to 148 (whole) | 148 | 1 | 2026 | written |
| content-short-02 | content | `content/tier1/absbyai-shorts/2026-the-five-levels-of-pushups.txt` | words 1 to 192 (whole) | 192 | 1 | 2026 | written |
| content-short-03 | content | `content/tier1/absbyai-shorts/2026-how-getting-abs-looksmaxxes-your-face-own-draft.txt` | words 1 to 175 (whole) | 175 | 1 | 2026 | written |
| content-short-04 | content | `content/tier1/absbyai-shorts/2026-how-to-do-hammer-curls.txt` | words 1 to 199 (whole) | 199 | 1 | 2026 | written |
| ads-01 | ads | `ads/tier2/2020-hbi-five-foods-to-avoid-HELDOUT.txt` | words 135 to 366 (middle) | 232 | 2 | 2020 | written |
| ads-02 | ads | `ads/tier1/2026-absbyai-ad3-written.txt` | words 322 to 612 (middle) | 291 | 1 | 2026 | written |
| ads-03 | ads | `ads/tier1/2020-15-steps-book-ad-the-top-5-reasons-why-you-need-to-advertise-on-youtube.txt` | words 603 to 908 (middle) | 306 | 1 | 2020 | written |
| ads-04 | ads | `ads/tier1/2020-15-steps-book-ad-how-to-start-a-business-with-0.txt` | words 849 to 1112 (middle) | 264 | 1 | 2020 | written |
| ads-05 | ads | `ads/tier1/2026-absbyai-shorts-ad-top-3-tips-for-getting-abs.txt` | words 1 to 214 (whole) | 214 | 1 | 2026 | written |
| ads-06 | ads | `ads/tier2/2023-spy-briefing-dec-martial-arts-vs-romanian-rambo-self-defense.txt` | words 384 to 560 (close) | 177 | 2 | 2023 | written |
| ads-07 | ads | `ads/tier2/2019-hbi-eat-this-not-that-if-you-have-arthritis.txt` | words 419 to 607 (close) | 189 | 2 | 2019 | written |
| ads-08 | ads | `ads/tier2/2023-cpa-alpilean-dr-patlas-himalayan-ice-fat-loss-technique.txt` | words 627 to 799 (close) | 173 | 2 | 2023 | written |
| ads-09 | ads | `ads/tier2/2023-spy-briefing-your-final-warning-before-the-end-of-america.txt` | words 433 to 652 (close) | 220 | 2 | 2023 | written |
| ads-10 | ads | `ads/tier2/2019-hbi-3-ways-i-treated-my-arthritis-naturally.txt` | words 52 to 300 (middle) | 249 | 2 | 2019 | written |
| conversion-01 | conversion | `conversion/tier1/2019-consulting-sales-video-script.txt` | words 54 to 431 (middle) | 378 | 1 | 2019 | written |
| conversion-02 | conversion | `conversion/tier1/2021-black-belt-cart-page-video-script.txt` | words 68 to 328 (middle) | 261 | 1 | 2021 | written |
| conversion-03 | conversion | `conversion/tier1/2026-absbyai-sales-letter-ai-got-me-abs-at-40-dans-sections.txt` | words 1530 to 1716 (close) | 187 | 1 | 2026 | written |
| conversion-04 | conversion | `conversion/tier1/2019-dr-marketing-website-vsl-script.txt` | words 47 to 333 (middle) | 287 | 1 | 2019 | written |
| conversion-05 | conversion | `conversion/tier1/2021-black-belt-sales-video-outline.txt` | words 1 to 369 (opening) | 369 | 1 | 2021 | written |
| conversion-06 | conversion | `conversion/tier1/2020-15-steps-book-sales-page.txt` | words 1749 to 2056 (middle) | 308 | 1 | 2020 | written |
| products-01 | products | `products/tier1/sgm/03-my-story.txt` | words 8 to 292 (middle) | 285 | 1 | 2007 | written |
| products-02 | products | `products/tier1/sgm/10a-immersion-mindset.txt` | words 3247 to 3661 (middle) | 415 | 1 | 2007 | written |
| products-03 | products | `products/tier1/sgm/26-bedroom-mentality.txt` | words 164 to 549 (middle) | 386 | 1 | 2007 | written |
| products-04 | products | `products/tier1/sgm/31-testosterone-and-sex-drive.txt` | words 936 to 1162 (close) | 227 | 1 | 2007 | written |
| products-05 | products | `products/tier1/sgm/05-four-archetypes-of-sexual-failure.txt` | words 1020 to 1298 (close) | 279 | 1 | 2007 | written |
| products-06 | products | `products/tier1/blackbelt/2021-the-ten-pillars-of-great-campaign-management-part-1.txt` | words 2494 to 2899 (middle) | 406 | 1 | 2021 | spoken |
| products-07 | products | `products/tier1/blackbelt/2021-how-to-turn-your-youtube-profits-into-passive-income.txt` | words 2928 to 3286 (middle) | 359 | 1 | 2021 | spoken |
| products-08 | products | `products/tier2/15steps/00-introduction.txt` | words 2950 to 3303 (middle) | 354 | 2 | 2020 | written |
