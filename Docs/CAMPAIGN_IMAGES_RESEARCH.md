# Campaign images: research and image plan (2026-10-01)

Source handoff: `Handoffs/handoff-20261001-pmax-image-research-and-plan.md`. Status: **research and plan done, waiting
for Dan's picks.** No finals generated, no campaign touched. Report page: https://claude.ai/artifact/NpsVQuSoxo7qXphK7ruyL7 . Evidence crops and rough mockups are embedded in the report page.

## 1. What the top players run as still images on Google

Method: Google Ads Transparency Center, United States, format = Image, all time, viewed 2026-10-01. About 115 image
ads viewed across six advertisers. The Transparency Center shows what runs and the last-shown date only. It does not
show spend, results or first-shown date, so **repetition of the same template in many variants is the proxy for "this
pays"**, and that is an inference.

| Advertiser | Image ads on record | What the images are |
|---|---|---|
| MadMuscles (AmoApps) | about 30,000 | Text card over an AI torso or silhouette ("We're looking for men who haven't exercised in years and want to become unrecognizable. Start the Military Calisthenics Plan. Beginner-friendly. Can be done at home. Your body will thank you. Let's try"), the same card in red, green, blue, camo and stone. Plan cards with one AI figure in a pose ("Tai Chi Plan" + 3 bullets + "Subscribe"). Plan calendars ("Wall Pilates Workout For Men, 7/14/28-day plan", "Tai Chi Made Easy: 30-Day Beginner Plan"). Illustrated posters with an age callout ("Keep it private until it's done. Men 40+. No equipment. Let's try"; "Hate long walks? Start Printable Chair Tai Chi for Men"). |
| Simple (Simple.Life Apps) | about 40,000 | Almost all charts and tables: "Walking based on your weight", "How much should I walk to lose 30 lbs according to my age?" with a Calculate button, "Printable chair yoga for seniors", "Tai Chi Walking based on your age", "Free walking plan to lose 30 lbs". One AI portrait card ("The walking program for seniors is now free!"). |
| BetterMe | about 6,000 (most are store products) | App ads copy the MadMuscles card: "We're looking for girls who want abs and a defined back. Start on Monday. Calisthenics Challenge". Tai Chi walking challenge cards with a list of benefits. |
| V Shred | about 200 | Body-type quiz cards: an illustrated row of body shapes with "1 Quiz to reveal body type", "60 Sec body type & diet quiz", "5 Questions body type quiz". Plain text card "Your Personalized Diet Plan". Supplement product shots with "Ripped in 90 days" on the box. |
| Noom | 71 | Clean pictures with no text on them: food photos, a phone mockup, a medicine bottle. The words sit in the ad text beside the picture: "Lose 15 Pounds in 15 Weeks", "Affordable 16-Week Custom Plan", "Sale Price: $49 First Month". |
| Hims | about 300 | Product on flat colour, and statement cards: "Your hairline has a hormone problem", "82% noticed less thinning", "Bio-hack your hairline". |

Zing Coach and Muscle Booster: 0 image ads found under `zing.coach` and `musclebooster.fitness` (they may use other
domains; not chased). Meta source (third-party write-up, adkit.so): Noom ran a raspberries photo with the on-image line
"15 months on Noom and I'm down nearly 90 pounds" for 153 days in 7 variations.

### Image types counted (about 115 ads viewed, Google)

| Type | Rough share | Who |
|---|---|---|
| Text-led card over an AI or illustrated body ("looking for men..." recruitment card, plan card with bullets) | about 30% | MadMuscles, BetterMe |
| Plan chart, calendar or calculator table (by age, by weight) | about 25% | Simple, MadMuscles, BetterMe |
| Product on flat colour | about 20% | Hims, Noom, V Shred (not usable by us except the phone mockup) |
| Clean photo, no text (food, object, phone) | about 10% | Noom |
| Body-type quiz row (illustrated figures) | about 8% | V Shred |
| Illustrated poster with age callout | about 4% | MadMuscles |
| Statement or stat card | about 3% | Hims |
| Real before/after pair | **0 seen** | nobody |
| Founder or coach face as the picture | **0 seen** | nobody (V Shred's founder appears only on a product box) |

Three things stand out:

1. **The words on the picture do the work.** The winners' images are closer to a small poster than to a photo: who it
   is for (men, men 40+, seniors, girls), the name of the plan, two or three "easy" bullets, a button.
2. **The picture is nearly always AI or illustration**, not a real customer and not the founder.
3. **Nobody runs a real before/after or a founder photo in Google image placements**, including V Shred, whose whole
   brand in video is its founder.

## 2. What works in Performance Max and Demand Gen image placements

Google's own guidance (Google's claims):

- Performance Max: landscape 1.91:1 (1200x628), square 1:1 (1200x1200), portrait 4:5 (960x1200), square logo. Up to 20
  images per asset group. Recommended 4 landscape, 4 square, 2 portrait. Demand Gen adds 9:16 (1080x1920).
- Text on the picture is allowed, but Google asks for at least one picture without overlays in each shape, and for the
  important content to sit in the centre 80% (edges get cropped in Gmail, Discover and the YouTube feed).
- Google says Demand Gen with video plus image gets 6% more conversions per dollar than image only.
- The "under 20% text" rule could not be found on any Google page. Treat it as folklore.
- AI-made pictures: Google has an AI label setting in Google Ads. Set it for AI-made images in the build.
- Discover and YouTube feed image rules refuse a "misleading before-and-after" and a close-up of a body part meant to
  make the viewer feel bad. One Google Partner agency (StubGroup) says weight-loss before/after pictures get refused in
  practice even when real. That matches what the Transparency Center shows: zero before/after pairs.

Independent tests:

- Columbia, Harvard, TU Munich and Carnegie Mellon study on native ads (500M+ impressions): AI-made ads got 0.76% click
  rate against 0.65% for human-made. The best ones were AI ads that did not look AI-made, especially "a large, clear
  human face".
- Motion Creative Benchmarks 2026 (550,000 Meta ads, about $1.3B of spend): text-only ads and pictures with text on them
  are common top performers; only 5 to 8% of ads become winners. This is Meta, not Google.
- Store Growers (Demand Gen practitioner, opinion, no numbers): people beat no people, lifestyle beats product-only,
  unpolished beats studio.
- **Gap:** nobody has published a controlled test of text-on-picture against clean picture inside Performance Max or
  Demand Gen in the last 18 months.

## 3. Cold against remarketing

- No controlled test was found comparing founder or brand pictures for warm audiences with attention-grabbing pictures
  for cold ones. It is practitioner habit, not evidence.
- What the named players visibly do for brand-aware traffic on Google is an **offer or objection card in a fixed brand
  look**: Noom "Sale Price: $49 First Month", "Free Insurance Check", "Worried about starting GLP-1?"; Hims' one
  consistent look across every ad.
- **Performance Max cannot be a remarketing campaign.** Its audience list is a hint, not a fence; Google shows the ads
  past it. Demand Gen can be held to a list. So remarketing pictures belong in the Demand Gen remarketing campaigns
  (`24305381214`, `24316408288`), which the credit does not pay for. A second Performance Max asset group "for
  remarketing" would only split $15/day in two and still serve cold. Recommendation: one Performance Max asset group
  (cold set), and the remarketing set as image ads in Demand Gen remarketing when Dan turns those campaigns on.

## 4. Our own numbers

Demand Gen `24243839443`, 2026-08-01 to 2026-10-01, video ads. The trial campaign `24316364155` went live 2026-10-01
and has no data yet. Conversions here are the old mid-funnel action, not trials, and the counts are tiny.

| Ad angle | Impressions | Click rate | Spend | Cost per click | Conversions |
|---|---|---|---|---|---|
| Ad 6 You're Not Too Old | 4,824 | 1.66% | $65 | $0.81 | 1 |
| Ad 4 Supplements | 5,124 | 1.58% | $50 | $0.62 | 1 |
| Ad 3 Human Trainers | 6,135 | 1.47% | $86 | $0.95 | 0 |
| Ad 1 This Picture Got Me Abs | 9,214 | 1.43% | $127 | $0.96 | 3 |
| Ad 13 Cost Of Getting Abs | 2,425 | 1.36% | $19 | $0.57 | 2 |
| Ad 10 Busy Dad | 7,085 | 1.12% | $56 | $0.71 | 2 |
| RA-01 AI Got Me Abs | 5,498 | 0.78% | $43 | $1.01 | 4 |

Reading: the age angle (Ad 6) and the "stop paying for X" angles (Ad 4, Ad 3, Ad 13) earn the clicks. RA-01 earns the
fewest clicks but the most conversions per dollar. No YouTube thumbnail test result is on record yet to add.

## 5. Analysis

**Which of the six angles work as one still picture**

| Angle | As a still | Why |
|---|---|---|
| Ad 6 Not too old | Best | It is an age callout, which is exactly what MadMuscles and Simple put on their pictures. Our top click rate too. |
| Ad 10 Busy dad | Strong | "Looking for men..." recruitment card with busy dads as the group named. |
| Ad 3 Human trainers | Strong | MadMuscles' own Google ad text is "Don't waste money on an expensive coach. Get yourself one that's always ready to go!" |
| Ad 13 Cost of getting abs | Good | A price card (Noom "Sale Price: $49 First Month"). Needs a true trainer price from the Ad 13 script. |
| RA-01 AI got me abs | Weak alone | It is a story. Works only as a phone picture of the app, or as Dan's photo with "How I Got Abs At 40". |
| Ad 4 Supplements | Weakest | Needs the argument to make sense. Held for round two as a statement card. |

**The line between attention-getting and deceptive: three questions**

1. Is the body in the picture either really Dan, or plainly a drawing or a generic scene, and never an AI body shown as
   a result someone got?
2. Does the text say who it is for and what it is, with no result number and no held-back reveal?
3. If the viewer taps and lands on /start, does the page give them exactly what the picture showed?

| Fine | Over the line |
|---|---|
| MadMuscles "Tai Chi Plan: beginner-friendly, no equipment needed" | MadMuscles "become unrecognizable" over an AI six-pack (an AI body shown as the result) |
| Noom food photo + "Affordable 16-Week Custom Plan" | Simple "How much should I walk to lose 30 lbs" calculator (a result number as the hook) |
| Simple "Printable chair yoga for seniors" chart | V Shred "88% of people ignore their body type" (a statistic from nowhere) |
| | Our own "This Picture Got Me Abs" (Google limited it on 09-10) |

**Verdict on Dan's two leanings**

- **Cold = attention-getting AI images: CONFIRMED, with one correction.** The cold images of MadMuscles, Simple and
  BetterMe are almost all AI or illustrated. The correction: the attention comes from the words on the picture (who it
  is for, the plan, how easy), not from a wild picture. Add one clean, no-text picture per shape, as Google asks and
  Noom does. One real photo of Dan goes into the cold set as a control, because he is the one thing no competitor has:
  a real 40-plus man with the result.
- **Remarketing = Dan and branded: PARTLY RIGHT.** No named player was seen running a founder photo as a Google image
  ad, so there is no proof for an all-Dan set. What they do run to people who know them is an offer or objection card
  in one fixed brand look. Dan's own instinct ("maybe just some of them") is the right call: half Dan in the brand look,
  half offer, objection and app cards.

## 6. Cold image plan (Performance Max asset group; also usable as Demand Gen image ads later)

On-image text follows `/ad-copy`: a person and the outcome he wants. Offer wording from /start: 7-day free trial, $0
today, then $19.99 a month.

| # | Picture | On-image text | Pattern copied | Angle | Made how |
|---|---|---|---|---|---|
| C1 | Dark home gym at dawn, a fit man in his 40s from behind with a phone | "LOOKING FOR MEN 40+ WHO WANT ABS" / "AI trainer + AI nutritionist" / button "START FREE TRIAL" | MadMuscles "We're looking for men..." card | Ad 6 | AI scene + type set in code |
| C2 | Black and white ink poster, a dad in a plank on the living room floor, a toy truck beside him | "HOW BUSY DADS GET ABS" / label "Men 40+" / button "LET'S TRY" | MadMuscles "Keep it private. Men 40+" poster | Ad 10 | AI illustration + type in code |
| C3 | Weekly plan grid, each cell a small frame of AI-Dan doing the exercise (never stick figures) | "HOW MEN 40+ LOSE BELLY FAT" / "Your week, built by AI" | MadMuscles and Simple plan calendars | Ad 6 | Designed graphic from our exercise demo frames |
| C4 | Two price tags side by side on a gym bench | "FIRE YOUR PERSONAL TRAINER" / "Human trainer: [price from Ad 13 script] a month. AI trainer: $19.99." | Noom price card + MadMuscles "expensive coach" line | Ad 3, Ad 13 | AI scene + type in code |
| C5 | Morning kitchen, a fit man in his 40s with a phone and a coffee, kid's cereal bowl and lunchbox on the counter. No text. | none | Noom clean photo | Ad 10 | AI scene |
| C6 | A phone on a gym bench showing the real app plan screen, a dumbbell beside it. No text. | none (real app screen) | Noom phone mockup | RA-01 | AI scene + real screenshot |
| C7 | Table with age rows 40-44, 45-49, 50-54, 55+, one row lit up | "HOW TO GET ABS AFTER 40" / "Pick your age" | Simple "according to my age" tables | Ad 6 | Designed graphic |
| C8 | A trainer's whistle and clipboard hanging on a hook in an empty gym | "TRAINERS HATE THIS AI APP" | MadMuscles text card + their coach line | Ad 3 | AI scene + type in code |
| C9 | Real studio photo of Dan, abs visible, plan-card layout | "HOW I GOT ABS AT 40" / three bullets: AI trainer, AI nutritionist, 7 days free | MadMuscles plan card (one figure + plan name + bullets + button) | RA-01, Ad 6 | Real photo of Dan on a Codex background |
| C10 | Shelf of unbranded supplement tubs with a receipt | "SUPPLEMENT CORPS HATE HIM" | Hims statement card | Ad 4 | AI scene + type in code. Round two. |
| C11 | Illustrated row of four dads' body shapes | "HOW 40+ DADS CAN GET ABS" / "Which one are you?" | V Shred body-type row | Ad 10 | AI illustration. Round two (we have no quiz on /start, so the tap would not land on what the picture promises). |

**First set of 10:** landscape C1, C4, C3, C5 (clean). Square C1, C9, C7, C6 (clean). Portrait C2, C8.
**Round two:** C10, C11, and second versions of whichever type gets the clicks.

## 7. Remarketing image plan (Demand Gen remarketing campaigns)

One fixed brand look on every picture: the black, white Manrope and red bar system from the YouTube banner, logo top
left.

| # | Picture | On-image text | Pattern copied | Made how |
|---|---|---|---|---|
| R1 | Dan studio photo, brand look | "HOW I GOT ABS AT 40" | MadMuscles plan card (one figure + title) | Real photo, Codex background |
| R2 | Dan photo beside an offer panel | "7 DAYS FREE" / "$0 today. Then $19.99 a month. Cancel in two taps." | Noom "Sale Price: $49 First Month" | Real photo + designed graphic |
| R3 | Dan photo, objection card | "TOO OLD TO GET ABS?" / "I got mine at 40." | Noom "Worried about starting GLP-1?" | Real photo + designed graphic |
| R4 | Dan studio photo, clean, no text, logo only | none | Noom clean photo; Google's one-clean-per-shape rule | Real photo |
| R5 | Dan pool photo cropped at the waistband, clean, no text | none | same | Real photo |
| R6 | Phone showing the real app, brand look | "YOUR AI TRAINER IS READY" | Noom phone mockup card | Designed graphic + real screenshot |
| R7 | What-you-get card | "AI TRAINER. AI NUTRITIONIST. SLEEP COACH." / button "START FREE TRIAL" | MadMuscles three-bullet plan card | Designed graphic |
| R8 | Price card | "FIRE YOUR PERSONAL TRAINER" / trainer price against $19.99 | Noom price card | Designed graphic |
| R9 | AI-Dan exercise frame in the gym | "HOW MEN 40+ LOSE BELLY FAT" / "Today's workout is ready" | MadMuscles plan card | Exercise demo frame + type |
| R10 | Statement card, text only | "HUMAN TRAINERS HATE HIM" | Hims statement card | Designed graphic. Round two. |

**Mix: 5 Dan (R1 to R5), 5 offer, app and plan cards (R6 to R10).** People who visited already know what he looks
like from the video and the sales letter, so his photo is the recognition cue. What they lacked was a reason to come
back, which is what the offer and objection cards carry, and that is the part the named players actually run.

**First set of 10:** landscape R1, R2, R6, R4 (clean). Square R2, R3, R7, R5 (clean). Portrait R1, R8.
**Round two:** R9, R10. Before/after pairs stay out of Google image placements for now (nobody runs them there).

## 8. Build spec for the image task (Dan's instruction, 2026-10-01)

- **Five variations of every image.** 20 images in the two first sets x 5 = 100 generations. A variation changes
  something a viewer would notice: the scene, the colour, which photo of Dan, the crop, or the headline (from Dan's own
  approved lines only). This mirrors MadMuscles running one card in five or more colours.
- **Budget: up to $50 for AI image generation** (Dan's authorization for that task). Codex on the ChatGPT subscription
  comes first and costs no cash: use the Codex subscription to generate the images
  (`.claude/skills/_shared/codex-image.sh`). The $50 covers the paid image API only for an image Codex has failed
  twice (`ALLOW_API_IMAGE=1`), and for a second look from another model on the scenes that matter most. State the
  running total.
- Real photos of Dan are never redrawn: Codex makes the background, his cutout
  (`photos/finalized social media photos/_cutouts/`, 103 files) and the type go on in code. Type is always set in code.
- Each picked image is delivered in the shape listed for it, upscaled locally, important content inside the centre 80%.
- Dan sees all five of each on one review page and picks. Up to two variations of a concept may go live at once
  (20 image slots per asset group).
- Set the Google Ads AI label on AI-made images.

## 9. Test design

- **Performance Max, about $15/day:** load all 10 cold images in one asset group. Google decides the split; there is no
  way to force an even test at this budget.
- **At $150 of spend (about 10 days):** the campaign is judged on trials, the images on clicks.
  - Campaign winner: 3 or more trials (about $50 each or better, against the $40 target). Loser: 0 trials. One or two:
    run to $300.
  - Images: read the asset report. Any image with under 5% of impressions or a "Low" rating is swapped for its next
    variation. Compare the types as groups: text cards (C1, C2, C4, C7, C8) against clean pictures (C5, C6) against
    Dan (C9).
- **Remarketing, Demand Gen $10/day:** one image ad per ad group beside the videos. The lists are small, so judge at
  30 days, not by spend.
- **Demand Gen cold campaign stays video-only** until Performance Max shows whether image placements produce trials.

## 10. Open items

- The credit's terms are unread. Google's general terms say only spend after redeeming counts and credits usually last
  60 days. The build session reads Billing > Promotions first.
- Longevity could not be measured in the Transparency Center (it shows last-shown only).
- Health-interest remarketing: Google bars remarketing lists for advertisers it files under health or negative body
  image. Our lists work today; keep the pictures positive (no shaming close-ups) so that stays true.

## Sources

Google Ads Transparency Center (madmuscles.com, simple.life, betterme.world, vshred.com, noom.com, hims.com), viewed
2026-10-01. Google help: support.google.com/google-ads/answer/17091269, /13704860, /14530211, /13703192, /12080169,
/16915411; support.google.com/adspolicy/answer/143465. adbeacon.com/ai-creative-wins-clicks-loses-conversions.
motionapp.com/library/research/creative-benchmarks-2026. storegrowers.com/demand-gen-ad-creative.
stubgroup.com/glossary/before-and-after-images-policy-clickbait-ads. adkit.so/resources/ads-examples/facebook-ad-examples.
web2appworld.com/breakdowns/madmuscles. blog.funnelfox.com/betterme-web2app-ads-analysis. growthmodels.co/noom-marketing.
