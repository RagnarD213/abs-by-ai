# Handoff: image research and image plan for the cold and remarketing campaigns

Written 2026-10-01 by Claude (brainstorm session). Not executed.
Recommended: **Claude Opus 5.5, high effort.** Task name: `Campaign Images Research AD`.

## Goal

Decide, from real research, which still images Abs By AI should run in Google Ads, separately for the **cold**
audience and the **remarketing** audience. The deliverable is a research report plus a concrete image plan that Dan
picks from. **This task does not generate final images and does not touch any campaign.** Dan reviews the plan, then a
later task makes the images and installs them.

## Why this exists

- Dan received a **$450 Performance Max credit** on 2026-10-01 (account 342-717-0837; 60 days to spend once applied).
- Plan on record from the brainstorm session: one Performance Max campaign mirroring the cold trial campaign, `/start`
  only, Trial Signup `7704441545` as the only goal, about $15/day for 30 days, started around Oct 8-10 once the trial
  campaign has a week of data. URL expansion off, auto-created assets off, brand terms excluded.
- Performance Max **requires** images: at least one landscape (1.91:1), one square (1:1) and a square logo. Google's bar
  for a strong rating is 4 landscape, 4 square, 2 portrait (4:5). Up to 20 images per asset group.
- Dan **rejected reusing the trial-campaign video thumbnails** as the image set. His words: "I feel like that's a lazy
  solution. These images could be really important, and I want to put some real thought, some real research and
  brainstorming into which images we use."

## Dan's starting leanings (treat as hypotheses to test against the research, not as the answer)

- **Remarketing:** leans toward images of himself and a branded feel, so people recognise who they are going back to.
  "Although maybe not all of that. Maybe that should just be some of them."
- **Cold:** leans toward AI-generated images that are very attention-getting and win a high click-through rate, but do
  not cross the line into deceptive clickbait.

If the research disagrees with either leaning, say so plainly and show the evidence.

## The campaigns these images are for

| Audience | Campaign | State |
|---|---|---|
| Cold | New Performance Max campaign (not built yet) | Planned for about Oct 8-10 |
| Cold | Demand Gen trial `24316364155`, video-only today | LIVE, $50/day |
| Remarketing | Demand Gen trial remarketing `24305381214` (site visitors + YouTube viewers) | PAUSED, $10/day |
| Remarketing | Subscriber remarketing `24316408288` | PAUSED |

Details: `Docs/DGEN_CONVERSION_CAMPAIGN.md`, sections dated 2026-10-01. The credit only pays for Performance Max, so
say in the plan whether remarketing images should go into a second Performance Max asset group (site visitors and
YouTube viewers as the audience signal), into the Demand Gen remarketing campaigns as image ads, or both, and why.
The brainstorm session recommended keeping the Demand Gen cold campaign video-only until Performance Max shows whether
image placements produce trials; revisit that with what the research finds.

## Part 1: research (do this properly, it is the point of the task)

1. **What the top fitness direct-response advertisers actually run as still images.** Google Ads Transparency Center
   (adstransparency.google.com), image format, United States, for MadMuscles (AmoApps / Genesis Tech), BetterMe, Noom,
   V Shred, and any other weight-loss or men's fitness app that shows heavy image volume (Simple, Fastic, Zing,
   Muscle Booster, Lasta, Hims weight loss). Collect at least 40 real image ads. Meta Ad Library is a valid second
   source for the same advertisers since their static creative is shared across networks; label which network each
   example came from.
2. **Sort what you find into image types** and count them. Expected buckets, add your own: real before/after,
   illustrated or AI body-type charts, quiz-style "pick your body type" grids, single hero physique, founder or coach
   face, app screenshot or phone mockup, text-led offer card, food or object curiosity image, age-callout image.
   Note which types the same advertiser keeps running for months, since longevity is the best public sign an ad pays.
3. **What works in Performance Max and Demand Gen image placements specifically.** Google's own creative guidance
   (Creative Excellence guide, asset best practices), plus practitioner tests from the last 12 months on: text overlay
   versus clean image, people versus product, faces, real versus AI-generated, native-looking versus polished, and how
   images get cropped across Discover, Gmail, YouTube feed and Display. Separate Google's claims from independent
   tests and say which is which.
4. **Cold versus remarketing creative.** What the evidence says about recognisable-face and branded creative for warm
   audiences versus pattern-interrupt creative for cold ones. Name who does it.
5. **Our own data.** Pull click-through and conversion numbers by ad from campaigns `24243839443` and `24316364155`
   (`node scripts/ads/api/client.js`, see `Docs/GOOGLE_ADS_API.md`), the YouTube thumbnail test results on record, and
   which hooks and photos have won before (memory: `thumbnail-design-system`, `cover-photo-selection`,
   `youtube-ad-competitor-research`, `madmuscles-deep-dive`, `ai-ad-creation-research`). The image concepts should be
   built on angles that already earned clicks for us.

Standing rule: recommend only image types a named top player actually runs (`AGENTS.md`, "Marketing advice: proven
direct response only"). If no named player runs it, leave it out.

## Part 2: analysis

- What the patterns mean for a product that is an AI trainer and nutritionist sold by a 40-plus founder who has the
  result himself, through a sales letter and a paid trial.
- Which of our six ad angles (Ad 13 cost of getting abs, RA-01 AI got me abs, Ad 10 busy dad, Ad 4 supplements,
  Ad 3 human trainers, Ad 6 not too old) translate best into a single still image, and which do not.
- Where the line sits between attention-getting and deceptive, stated as a short practical test Dan can apply to any
  concept, with two or three examples on each side taken from the research.
- A verdict on each of Dan's two leanings: confirmed, partly right, or wrong, with the evidence.

## Part 3: the image plan

For **cold** and for **remarketing** separately:

- 8 to 12 image concepts each. For every concept: a one-line description of what is in the picture, any on-image
  text (word for word), which researched pattern it copies and from whom, which ad angle it supports, and whether it
  is a real photo of Dan, an AI-generated scene, or a designed graphic.
- A recommended first set of 10 (4 landscape, 4 square, 2 portrait) and what gets held back as round two.
- For remarketing, the mix of Dan-and-brand images versus other types, with the reasoning.
- A simple test design: what is compared, how many images at once given roughly $15/day, and what result at $150 of
  spend would count as a winner or a loser.
- Rough mockups are welcome if they help Dan choose (low-effort sketches, not finals). Any image generated goes through
  Codex: **use the Codex subscription to generate the images** (`.claude/skills/_shared/codex-image.sh`, rule in
  `.claude/skills/_shared/IMAGE-GENERATION.md`). Real photos of Dan are never redrawn; Codex makes backgrounds only.

## Rules that shape the concepts

- Before and after pairs are always the same person (memory `before-after-same-person`). The standard shirtless before
  is the deck-chair sunglasses photo (memory `standard-before-picture`).
- No unbelievable claims in on-image text (memory `ad-copy-no-unbelievable-claims`, `thumbnail-no-claims`). Never the
  word "trick". On-image text counts as ad copy, so write it with `/ad-copy`.
- Abs visible and defined in any photo of Dan, no frowning default (memory `cover-photo-selection`,
  `frowning-photos-standing-rule`). Speedo photos crop at the waistband.
- No app stick-figure drawings (memory `never-show-stick-figures`).
- No em dashes in anything written.
- Keep Dan's decisions small: the plan should end in one pick list, not a question per image.

## Deliverable and where it goes

- A report page Dan can read on his phone (publish as an Artifact): research findings with the real example ads shown,
  the analysis, then the two image plans and the pick list at the bottom.
- A copy of the findings saved as `Docs/CAMPAIGN_IMAGES_RESEARCH.md` so the build task can read it.
- Then stop. Do not generate finals, do not build or edit any campaign. After Dan picks, write the build handoff
  (generate the picked images with the Codex subscription, then add them to the Performance Max build described above).

## Open risks

- The Transparency Center shows what runs, not what converts. Use longevity and repetition as the proxy and say so.
- The credit's full terms have not been read. If they require paid spend before the credit applies, flag it in the
  report; the build session reads them on Billing > Promotions.
- The Performance Max build prompt from the brainstorm session still says to reuse thumbnails. That line is dead;
  this handoff replaces it.

## Starter prompt

> Name this task `Campaign Images Research AD`. Read `Handoffs/handoff-20261001-pmax-image-research-and-plan.md` and
> execute it. Do deep research on which still images the top fitness direct-response advertisers run on Google
> (Performance Max and Demand Gen image placements), analyse what that means for Abs By AI, and give me two image
> plans: one for the cold campaign and one for the remarketing campaign, each ending in a pick list. Test my two
> leanings against the evidence (branded images of me for remarketing, attention-getting AI images for cold that stay
> short of deceptive clickbait). Do not reuse the video thumbnails. Use the Codex subscription to generate the images
> if you make mockups. Publish the report as a page, save the findings to `Docs/CAMPAIGN_IMAGES_RESEARCH.md`, then
> stop for my picks. Do not build or change any campaign.

Model: Claude Opus 5.5, high effort.
