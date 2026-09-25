# Handoff: the new VSL landing page, five design mockups grounded in what proven direct-response advertisers run

**Written 2026-09-24. NOT EXECUTED.** Research session (cloud). The deliverable of the next session is five mockups
for Dan to choose from, not a live page.
**Evidence:** `Docs/VSL_LANDING_RESEARCH_2026-09-24.md` (the five research reports, 20,000 words). Read the handoff
first; open the appendix when you need the source behind a claim.
**Business goal:** every paid click (Google Demand Gen, YouTube, Search) lands on ONE page that turns visitors into
7-day trials and then paying members at a cost that makes ads profitable. Judge it on cost per trial and cost per
paying customer (Dan's rule, `AGENTS.md`), never on plays, uploads or scroll depth.

---

## 1. Read this first: what changed, and what the research could and could not do

**Two decisions of Dan's shape every mockup.**

1. **The free AI generation is no longer the front-end hook** (`AGENTS.md`, "Marketing advice: proven direct response
   only", 2026-09-24): "the free AI-generation front-end funnel should never have been tested ... The generation stays a
   member feature, not the entry hook." The current `/start` page is built around a one-tap photo upload. The new page
   sells the trial from the video; the goal image is shown as something a member gets.
2. **The new VSL was written for signup-before-generation.** Dan chose Claude's "AI Got Me Abs at Forty" script on
   2026-09-16 "primarily for a new page that requires signup before generation, also usable on /start"
   (`Docs/VSL_LANDING.md`). Both website VSLs were filmed on 9/23 and are waiting to be cut: **WV-02** (the /start
   landing-page video, roll C1701-C1703) and **WV-01** (the analysis-page video, version A + version B intro, roll
   C1692-C1700), `Handoffs/video-editing/`. Neither is cut yet. The mockups use a placeholder poster and a stated
   target length; the design session does not need the finished video.

**What the research could not do.** Dan asked for VidTao as the primary tool. The session that ran this research was a
cloud container: it had no access to Dan's Chrome, and its network policy blocked vidtao.com and every competitor site
(madmuscles.com, vshred.com, betterme.world, noom.com, kinobody.com and about forty more). The five reports therefore
rest on search-engine summaries of those pages, published teardowns (Web2App World, FunnelFox, RevenueCat, Growth
Models), the FTC complaint against MadMuscles' parent, Hormozi's own 2025 handbooks (full text), and three first-hand
sources already in this project (the repo's docs, the 2026-09-10 Cart Teardown artifact, the frame-level ad study in
`.claude/skills/ad-edit/reference/AD_STUDY.md`). Where a report could not confirm exact on-screen copy it says
"could not verify". **The structural findings are solid (multiple independent sources agree); the pixel-level details
are not.** Step 0 below closes that gap in about 30 minutes on Dan's Mac, where Chrome and VidTao are reachable.

---

## 2. Non-negotiables: every mockup must pass this list

These are Dan's standing rules plus the compliance record of this exact account. A mockup that breaks one is rejected
before Dan sees it.

**Dan's rules**
- Only patterns that V Shred, MadMuscles, BetterMe or Noom actually run (secondary: Kinobody, Built With Science, Fit
  Father Project, Hormozi). Every section of every mockup names who runs it. Nothing invented.
- The generation is a member feature. No free-generation CTA above the fold. The photo is uploaded after the trial
  starts (inside onboarding), or is shown as the first thing a member does.
- Offer as it exists: **7-day free trial, card required, then $19.99/month or $69.99/year; Monthly pre-selected**
  (Dan, 2026-09-10). Checkout is the existing pay-first cart (`Docs/WEB_CART.md`): email with the card, account after.
- No em dashes anywhere in the copy. Not one.
- No "thousands of guys" or any count. 75 people had ever generated on 2026-09-10. Use true numbers or none.
- Dan's facts: got his abs back at 40, over about two years; one daughter, never "my kids".

**Google Ads and FTC (first-hand verdicts on this account, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, plus
`Handoffs/handoff-20260730-google-ads-compliance-pages.md`)**
- **Headline shapes that passed:** "How I Got Abs At 40", "How AI Got Me Abs", "See Yourself With Abs", "See Your
  Goal Before You Start", "Abs By AI - Here's How It Works". **Shapes that were limited or disapproved (Clickbait):**
  "This Picture Got Me Abs", "Abs At 40 - The Photo That Did It", "Why My Diets Kept Failing". Rule: a plain
  description of the mechanism; nothing that reads unbelievable without the video's context.
- **No physical-result promise in copy:** no "get abs", "lose", "burn", "shred", "transform your body", "real results",
  no timeframes ("in 30 days"), no "guaranteed", no negative self-image language ("dad bod", "out of shape"), no
  shaming. Sell the video, the analysis and the plan, never the body.
- **No side-by-side before/after pair above the fold.** Demand Gen can show a screenshot of the page under the ad, so
  the fold is ad creative and is reviewed as such. The product demo pair (uploaded photo → AI image) may appear below
  the fold exactly as today: "AI-GENERATED" tag on the image, "Fictional example ... not a real result" line beside it.
  Every real photo of Dan carries "Real picture of me, not AI-generated" (`.claude/skills/_shared/VIDEO-RULES.md`).
- **The AI image is never presented as a result.** Label on or next to it, always.
- **No countdown timers, no discount wheels, no "1,103 people bought this in the last hour", no crossed-out prices
  that were never charged, no pre-selected add-ons, no fake reviews.** These are the exact devices the FTC named when
  it halted MadMuscles' parent (Genesis Tech) in June 2026, and the ones Google's Unacceptable Business Practices
  policy suspends for without warning. The "SAVE 71%" on Annual is a real price difference and stays.
- **Renewal disclosure in body-size type directly above the pay button** (already in the cart; repeat the price and
  "cancel anytime" wherever the trial is offered on the page).
- **Transparency elements stay on the page** (Google landing-page experience): who Dan is, what the product is, the
  price, the trial terms, Terms / Privacy / Refunds / Contact links in the footer.
- **Remarketing on weight loss is not allowed**; do not design around retargeting.

---

## 3. What the research says: twelve rules, each with who runs it

1. **The ad lands on a commitment step, not a brochure.** MadMuscles (493 quiz entry URLs, $29M/month on YouTube),
   BetterMe, Noom, Muscle Booster and V Shred all send paid clicks to a quiz; Built With Science tested quiz vs App
   Store and "the quiz won decisively" (90% of paid traffic goes to the quiz). Hims, Ro and Found land on an eligibility
   quiz. Nobody sells on screen one.
2. **The persuasion is either the quiz or a founder video, rarely both at the top.** App funnels (MadMuscles, BetterMe,
   Noom) run no VSL; the quiz personalizes and the paywall closes. Personal-brand funnels (V Shred, Fit Father Project,
   Kinobody, Hormozi's Skool Games page) put the founder on camera above one button. V Shred is the bridge: quiz first,
   then a per-segment results page whose top element is Vince's video.
3. **The pitch page opens with "your plan is ready" and the visitor's own numbers.** MadMuscles: "Your personalized
   plan is ready!" + "Personal summary based on your answers". BetterMe: avatar recap with goal weight and level. Noom:
   goal date echoed back. Abs By AI already computes body fat, fat to lose and goal weight; that is this raw material.
4. **A dated, modest projection before the price.** Noom's goal-date chart, BetterMe's predicted-results date. Noom
   "doesn't overpromise". The FTC treats more than 2 lb/week or "regardless of what you eat" as false on its face, so
   any projection stays inside 1 to 2 lb of fat per week and says "estimate".
5. **Headline, subhead, video, one button; nothing else competes above the fold.** Hormozi's three lead-page layouts
   ("headline, sub headline, contact info, submit ... same thing with an image ... with three bullets"), Skool Games
   page, ClickFunnels VSL template, Noom's near-empty homepage ("one page, one purpose").
6. **Ad, headline and video are one continuous message: same person, same words, same claim.** Hormozi ("make sure
   your landing pages match your ads ... same words and same colors and same person"), Inceptly's $250K seniors
   teardown ("the landing page echoed the ad with the same claim stack"), Google's own Demand Gen guide ("mirror your
   landing page promise"), Google's landing-page-experience factor ("meeting the user expectations set by the ad").
   MadMuscles gives each ad theme its own entry URL for this reason.
7. **The video is at the top, sized for a phone, muted autoplay with burned captions and click-to-unmute** (V Shred's
   results page, verified first-hand in the Cart Teardown; Vidalytics reports +49% for muted smart autoplay on a sales
   page). Click-to-play with a thumbnail wins on short opt-in pages (Vmaker 41.2% vs 9.7%). A play icon and a human
   face thumbnail lift plays (Wistia). Play-rate benchmark on cold traffic: 15 to 20%.
8. **3 to 7 minutes for a low-ticket subscription; 10 is the ceiling.** Hormozi (5 to 7; his agency demo is 7; "five
   minutes of video saves thirty minutes of conversation"), V Shred (~5 minutes). Spend most of the effort on the first
   30 seconds; Wistia's drop-off is steepest at 10 to 20 seconds.
9. **The page must work for someone who never plays the video.** VidTao's VSL + TSL hybrid case ("short VSL ad and text
   sales page elements together create a full sales argument"), Truth About Abs (Benson, the abs-niche VSL that did
   ~$40M), V Shred's "page that seems to go on forever", Fit Father's video letter with a text version. Below the fold:
   the video's argument in scannable text, what you get, founder credential, proof, guarantee, FAQ, the same button.
10. **Plan cards with per-period math, the renewal terms visible, and a trial timeline instead of a timer.** MadMuscles
    and BetterMe show three cards priced per day/week; Built With Science's biggest win of 2025 was showing the trial as
    a day-by-day timeline ("day 1 you get your plan; day 12 a reminder that your trial is about to end"); Blinkist's
    version lifted trial starts 23% and cut complaints 55%. Our cart already has Today $0 / Day 5 reminder / Day 7 first
    charge. Repeat it on the landing page.
11. **One bright button, imperative first person, repeated, plus a sticky mobile bar.** "GET MY PLAN" (MadMuscles,
    BetterMe), "START MY 14-DAY TRIAL" (Noom), "PLAY FOR FREE" (Skool Games). Hormozi's CTA names what happens next:
    "Start free on the next page". Ours: "Start my free 7 days →" (already the cart's button; keep the wording identical
    everywhere).
12. **Risk reversal beside the button, in body-size type.** V Shred ("Unconditional 30-Day Money Back Guarantee" under
    the button), Kinobody (60-day), Fit Father ("Ironclad 100% Satisfaction"), Sweat ("Pay nothing today. You will be
    charged after the trial ends unless cancelled prior"). Our risk reversal is the free week plus whatever `/refunds`
    actually promises; state only what that page says.

**Three things the winners avoid:** a password, address or phone before the card (V Shred's 13-field form is the one
with the BBB complaints); a price or an exit link on the way to the paywall (BetterMe and Noom show the price only at
the end; no nav, no "learn more"); and a secret-mechanism pitch (the Mike Chang "Afterburn" VSL is a dead format;
today's pages sell "your plan for your body type").

**Benchmarks to size expectations (all vendor-published, in the appendix):** web-to-app funnels convert about 3% of
sessions to purchase and 13% of sessions reach the paywall (FunnelFox, 311 funnels); Health & Fitness trial-to-paid
median 39.9%, 37.4% for 5 to 9 day trials (RevenueCat); fitness/wellness paid-search landing pages convert 4.4% on
average to any goal (Unbounce). Our record: 207 ad arrivals since 2026-07-30 → 2 trial signups → 0 paid, $1,272.66
spent (`Handoffs/handoff-20260909-google-ads-account-fixes.md`).

---

## 4. Product facts the page must match

- **Offer:** 7-day free trial, card required (`payment_method_collection: 'always'`), Monthly $19.99 pre-selected,
  Annual $69.99 ("SAVE 71%", $5.83/mo). Day-5 reminder email is real (`trialReminderSweep`). Cancel: Manage membership →
  Stripe portal ("two taps" must stay true). `/refunds` page: read it before quoting any refund promise.
- **What a member gets** (membership screen, `public/index.html` ~2869): the goal image (unlimited), the body analysis,
  a 4-week AI training program built around equipment and level, AI nutritionist with meal plans and photo macro
  tracking, sleep coach, supplement audit (25/month), adaptive check-ins. Six tiles already exist on `/start`.
- **Checkout:** the pay-first cart (`#cartSection`, `Docs/WEB_CART.md`): headline, video slot (`ABS_CART_VIDEO`, empty),
  recap, plan cards, trial timeline, benefits, disclosure above the button, "Start my free 7 days →", Apple Pay / Link /
  card, account created from the Stripe email. Any mockup's CTA lands here (or on the analysis page → cart). Do not
  redesign the cart in this task.
- **Videos:** WV-02 (the /start VSL, from the "AI Got Me Abs at Forty" script) and WV-01 (analysis-page VSL) are filmed,
  not cut. Config lives in `public/site-video.js` (`ABS_START_VIDEO`, `ANALYSIS_VIDEO`, `ABS_CART_VIDEO`). Poster:
  `public/img/video-poster.jpg`. Until WV-02 exists the interim is Muhammad's Ad 1 16:9 `lf46ytHacss`.
- **Ads sending traffic** (`Docs/DGEN_CONVERSION_CAMPAIGN.md`, `Docs/GOOGLE_ADS_API.md`): Demand Gen conversion campaign
  `24243839443` (Ads 1 to 15 + RA-01; themes: "This Picture Got Me Abs" story, Fire Your Nutritionist, Fire Your
  Personal Trainer, Supplements, Diets, "You're Not Too Old", Photoshop To AI, ChatGPT For Abs, Busy Dad, Cost Of
  Getting Abs, Workout Video Overload, Dad In A T-Shirt); Search Brand `24086091285` and Non-Brand `24148587722`
  (keywords: ai six pack, six pack generator, add abs to photo, what would I look like with abs). Every enabled ad's
  final URL is `https://absbyai.com/start`.
- **⚠ Message-match risk to flag to Dan:** Non-Brand Search traffic is people searching for an "AI six pack generator".
  Landing them on a trial-first VSL page with no free generation breaks message match (rule 6). Recommendation in
  section 7.
- **Design tokens** (`public/start.html` lines 98 to 107): Manrope; `--bg #f6f5f2`, `--ink #1b1a18`, `--acc #2f5fe0`
  (button), `--warm #e07b2f`; `.cta-btn` 16px radius, full width. Reuse them so the winner ships as a real page.
- **Events** already defined on `/start`: `vsl_landing_seen`, `vsl_cta_clicked {cta}`, `vsl_video_play`,
  `vsl_video_progress {pct}`, `vsl_trial_cta_clicked`; in the app `cart_viewed`, `cart_checkout_completed`,
  `membership_subscribed`, `paid_conversion_reported`. Mockups annotate where each fires; a quiz adds
  `vsl_quiz_step {n}` and `vsl_quiz_completed`.

---

## 5. The five mockups

Each one is a different bet on WHERE the persuasion happens. They share the non-negotiables (section 2), the offer, the
cart, and the shared spec (section 6). Every headline below is a draft in the approved shapes; Dan edits copy.

### Mockup 1: the founder VSL page (V Shred results page / Fit Father video letter / Hormozi Skool Games)

**Bet:** Dan on camera does the selling in five minutes; the page's job is to get the video played and the button
pressed. Fastest to ship: it is `/start` with the upload hook replaced by the trial.
**Who runs it:** V Shred (`le.vshred.com/sp/survey/male-*`: Vince's ~5-min video at the top, autoplay muted, "Click
to unmute", offer and proof below); Fit Father Project (`/ff30x-letter-video/`, "THE PROVEN WEIGHT LOSS PROGRAM FOR
MEN 40+", credential + story + video); Hormozi's Skool Games page (kicker, headline, subhead, one line of features,
"PLAY FOR FREE", free trial).
**Above the fold (375 px):**
- Kicker: "Dan Rose · Founder, Abs By AI"
- H1 (pick one; all in approved shapes): "How I Got Abs At 40 With AI Instead Of A Trainer" / "How AI Got Me Abs At 40.
  Here's How It Works." / "AI Got Me Abs At 40. Now It Coaches Me Every Day."
- Video: 16:9, poster = Dan's face mid-sentence with a play icon and a "4:30" length chip, muted autoplay with burned
  captions, click-to-unmute overlay. WV-02 when cut; placeholder until then.
- Subhead under the video (one line): "Watch how the system works, then try everything in the app free for 7 days."
- Button: "Start my free 7 days →" (to the cart). Under it, small: "then $19.99/mo · cancel anytime · Privacy Policy".
**Below the fold, in order:** (1) three bullets that translate the video for skimmers (what the AI reads from your
photo; the plan it builds; what changes week to week); (2) "What you get" six tiles (existing), the goal image tile now
"Included"; (3) the product demo pair, labeled, below a "How it works" three-step (photo → analysis + goal image → the
plan, all inside the trial); (4) founder card: real photo labeled "Real picture of me, not AI-generated", one-line
credential, the 40-and-two-years fact; (5) trial timeline Today $0 / Day 5 reminder / Day 7 first charge, plan cards
Monthly (pre-selected) / Annual, renewal line, the button again; (6) FAQ (five existing questions plus "Do I need to
upload a photo first?"); (7) legal + footer links; sticky mobile bar "Start my free 7 days →".
**Measure:** play rate (target 15 to 20% cold), `vsl_trial_cta_clicked ÷ vsl_landing_seen`, cart_viewed, trials, paid.
**Dependencies:** none beyond the video. Ships as a rewrite of `public/start.html`.

### Mockup 2: quiz first, then "your plan is ready" with the VSL (MadMuscles + V Shred + Built With Science)

**Bet:** the biggest spenders in the category all run this, and it turns a cold click into a committed prospect before
the price appears. The quiz replaces the free generation as the micro-commitment.
**Who runs it:** MadMuscles (48 screens, gender first, "Lean / Average / Chubby", goal, then "Your personalized plan is
ready!" + "Personal summary based on your answers", plan cards); V Shred (one-minute body-type quiz → per-segment
results page led by the video); BetterMe and Noom (quiz → projection → email → paywall); Built With Science (quiz beat
the App Store "decisively"; the answers double as onboarding).
**Flow:** Screen 1 IS the landing page: H1 "Build your personalized abs plan in 60 seconds" (or "Get the plan AI built
for me at 40, made for your body"), one question, big tap tiles, progress bar, no nav. Questions (6 to 8, one per
screen, men's-funnel set only, no emotional-relationship-with-food block): age band (Under 35 / 35-44 / 45-54 / 55+) →
current build (Lean / Average / Heavier, silhouettes, not photos) → goal (Lose the belly / Build muscle / Both) → where
you train (Gym / Home with dumbbells / Bodyweight only) → time per session (20 / 30 / 45 min) → days per week → what
has failed before (Trainers / Diets / Supplements / Workout videos; multi-select, this also selects the ad theme to
echo) → height and weight (sliders, the analysis page's controls). Then a 3-second "Building your plan" loader with
three labeled bars (Training / Food / Timeline). Then the **results page**: "Your plan is ready" + a personal recap card
(age band, build, goal, equipment, days, estimated body fat range and fat to lose from height/weight, a modest
timeline), Dan's video ("Here's what the AI does with this"), the trial timeline, plan cards, disclosure, "Start my free
7 days →". Email is asked WITH the card in the cart (MadMuscles order: quiz → paywall → card → account); no separate
email screen.
**Above the fold on screen 1:** progress bar, H1, "Answer 7 quick questions. No email, no photo, no account.", the first
question's tiles. Nothing else.
**Compliance notes:** silhouettes not bodies; the recap says "estimate"; the projection stays under 2 lb/week; the
"what has failed before" screen must not shame ("Trainers were too expensive" is fine, "Nothing works for me" is not).
**Measure:** quiz start, completion (benchmark 35 to 50%), results-page views, trial CTA, trials, paid. Step events
`vsl_quiz_step`.
**Dependencies:** new client-side quiz (state in `sessionStorage`, answers carried into onboarding so the five
post-payment questions are pre-filled); the no-photo estimate (see Mockup 5). Two to three days of build.

### Mockup 3: the minimal page with the trial timeline (Hormozi's three layouts + Built With Science pricing + Blinkist)

**Bet:** the opposite of Mockup 1's long page. Fewer elements, faster load, one decision. Hormozi: "the simpler the
landing page, the fewer variables you have to test ... super high conversion rates."
**Who runs it:** Hormozi (headline, subhead, image or video, three bullets, one submit; Skool Games page); Built With
Science's 2025 pricing page (one plan, day-by-day trial timeline, their biggest lift of the year); Blinkist (timeline,
+23% trials, −55% complaints); Sweat's join page (plain trial terms next to the price).
**The whole page (under two phone screens):** H1 "AI Got Me Abs At 40. Here's How It Works." → subhead "A 4-minute
video from the founder, then 7 days free." → video (click-to-play with a strong face thumbnail; this is the short-page
case where click-to-play wins) → three bullets ("One photo becomes your goal image and your body analysis" / "A
training and food plan built around your equipment, your schedule and what you actually eat" / "Daily check-ins that
adjust the plan as you change") → trial timeline (Today: everything unlocked, $0 / Day 5: reminder email / Day 7:
$19.99/mo unless you cancel) → plan toggle Monthly (pre-selected) / Annual → renewal line → "Start my free 7 days →"
→ one line of founder credential with a labeled real photo → footer links. No FAQ, no tiles, no demo pair (the
product is shown inside the video only).
**Measure:** the same funnel; this is the control for "does the long page add anything".
**Dependencies:** none. Half a day.

### Mockup 4: the story letter with video (Truth About Abs / V Shred advertorial pre-lander / Fit Father text letter)

**Bet:** most YouTube viewers arrive muted and skim; a text sales letter in Dan's voice, with the video beside it,
sells to readers and watchers alike. VidTao's own case: "the combination of a short VSL ad and text sales page elements
together create a full sales argument like a 45-minute VSL."
**Who runs it:** Jon Benson's Truth About Abs (the abs-niche VSL, ~$40M, long cluttered page calling out one specific
man); V Shred's advertorial pre-lander (`/blog/body-type-quiz-advertorial-1-celebrity-trainer-v3/`); Fit Father Project's
text version of the video letter (`/FF30X-letter-/`); Gundry MD (video first, bio + press below); the classic
ClickFunnels "Hook, Story, Offer" page.
**Structure:** H1 "How I Got Abs At 40 Without A Trainer, A Nutritionist Or A Supplement Stack" (this echoes Ads 2, 3
and 4); byline "By Dan Rose, founder of Abs By AI · 6 min read · or watch the 4-minute version"; video at the top
(muted autoplay, captions); then the letter in short paragraphs with subheads following Hormozi's sequence: the pain
(one named avatar: the 40-plus guy who has paid for all of it), why it has not worked (the human-expert cost, the
generic plans), the epiphany (what the picture and the analysis changed), the mechanism (photo → numbers → plan →
daily adjustment, with real app screenshots, no email-capture screen, no before/after reveal screen), proof (Dan's
real photos, each labeled, never side by side with a before; the "AI-GENERATED" goal-image example as a product demo),
the offer as a value stack (what you get, the trial), the risk reversal, FAQ, the button. Buttons after the mechanism,
after the offer, and at the end; sticky bar.
**Compliance notes:** the letter is where result claims creep in. Every sentence passes the section 2 phrase list;
Dan's own story is told as his story ("this is what I did"), never as a promise ("you will").
**Measure:** scroll depth to the offer, CTA clicks by position, trials, paid.
**Dependencies:** the letter (draft from the "AI Got Me Abs at Forty" script and Dan's edited long-form text in
`Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`). One day.

### Mockup 5: numbers first, then the video (Noom projection / BetterMe predicted results / Hims and Ro eligibility)

**Bet:** the analysis is our strongest differentiator and every big funnel puts a personal projection before the price.
Give the visitor his estimated numbers in 20 seconds from three inputs, no photo, then let Dan's video sell the plan
that closes the gap.
**Who runs it:** Noom (goal-date projection updated every few screens, "Your personalized health plan is ready"),
BetterMe (the "58,000 similar members" date screen), Hims / Ro / Found (a 2 to 3 minute eligibility check as the hook:
"See if I'm eligible"), V Shred (macro goal computed from the quiz and carried in the results URL). This is variant B of
today's `/start` ("Find Out How Far You Are From Abs") taken to its conclusion.
**Flow:** Screen 1: H1 "How Far Are You From Abs? Find Out In 20 Seconds." + three controls (age, height, weight;
optional waist) + "Show my numbers →" (no email, no photo). Screen 2 (same page, scrolls into view): the analysis card
in the app's own style (estimated body-fat range, fat to lose to a visible-abs range, goal weight, a modest timeline at
1 to 2 lb/week, "Where your plan will focus"), each number carrying the "visual estimate ... sources" qualifier; then
"Here's the plan that closes that gap" + Dan's video; then the trial timeline, plan cards, disclosure, "Start my free
7 days →"; then what you get, founder card, FAQ, footer.
**Compliance notes:** the estimate is a published-formula estimate (age + sex + BMI, or Navy method with waist and
neck), cited on `/sources`; the timeline never exceeds 2 lb/week; no "you'll have abs by [date]" wording, only "a
realistic range".
**Measure:** numbers-shown rate, video plays after numbers, trial CTA, trials, paid.
**Dependencies:** ⚠ a no-photo estimator does not exist yet; the analysis page estimates from the photo and adjusts
with sliders. The mockup can use static sample numbers; shipping it needs a small client-side formula plus a `/sources`
entry. Flag in the mockup.

---

## 6. Shared spec for all five

- **Phone first.** Design at 375 px, then desktop. CTA visible without scrolling on 375 px; 16 px body text; 48 px tap
  targets; no horizontal scroll. Then a desktop layout where the video and copy sit side by side.
- **Speed.** The hero video is a poster image plus a click or a lazy muted autoplay; the page must hit LCP under 2.5 s
  and INP under 200 ms on a phone. No YouTube iframe above the fold before interaction (the "clunky embed" costs 5 to
  10% play rate); use the poster and load the player on tap, or an mp4 with `preload="metadata"`.
- **One CTA, one wording:** "Start my free 7 days →", blue `--acc`, full width, repeated, plus the sticky mobile bar.
  Every button goes to the same place (the cart, or the analysis page → cart in Mockups 2 and 5).
- **No navigation, no external links above the legal block, no second offer.** Footer only: How it works · Terms ·
  Privacy · Refunds · Disclaimer · Sources · Contact · Log in.
- **Per-angle headline via a query parameter** (MadMuscles' per-theme entry URLs): `?a=trainer` / `?a=nutritionist` /
  `?a=supplements` / `?a=diets` / `?a=age` / `?a=default` swaps the H1 and the first bullet to echo the ad that sent the
  click. Each mockup shows the default plus one alternate.
- **Video treatment stated on each mockup:** poster (Dan's face, play icon, length chip), autoplay policy (muted +
  captions + unmute overlay for Mockups 1, 2, 4, 5; click-to-play for Mockup 3), target length (4 to 5 minutes, 7 max).
- **Disclosure placement:** "AI-GENERATED" on every AI image; "Real picture of me, not AI-generated" on every real
  photo of Dan; the "visual estimates ... sources" line under every number; the renewal line above every button; the
  existing legal paragraph and the AI-partners privacy sentence above the footer.
- **Events:** annotate each mockup with the `vsl_*` events it fires, so the build ships with tracking.
- **Copy voice:** Dan's, plain, first person, blunt where the claim is about the industry (trainers, nutritionists,
  supplements), never about the reader's body. No exclamation marks, no all-caps, no em dashes.

---

## 7. Recommendation and test plan

**Build order if Dan does not pick:** Mockup 1 first (it is `/start` with the hook swapped; ships the day WV-02 is
cut), Mockup 2 second (the category's proven volume funnel; needs the quiz), Mockup 3 as the control, then 4 and 5.
Reasoning: Dan's ads are founder-on-camera story ads, he has just filmed the VSL for exactly this page, and V Shred
(the closest personal-brand comparable) runs video-at-the-top. MadMuscles-style quiz-first is the bigger long-term bet
but is also the one that needs engineering and the one most likely to over-personalize a product whose real
personalization step (the photo) now sits after payment.

**Do not A/B test at this volume** (`Handoffs/handoff-20260910-web-pay-first-cart.md`: "Do not set up an A/B test at
this volume"). Run one page at a time: ship the chosen page, run the normal Demand Gen and Search budget for two weeks
or ~300 landing sessions, whichever first, and compare cost per trial and trials per session against the `/start`
baseline (2 trials from 207 arrivals, 0 paid). Then swap in the next mockup. The winner is the page with the lowest
cost per paying customer after trial-to-paid settles (7 days after the last trial start).

**The Non-Brand Search question (Dan decides).** "AI six pack generator" searchers want the generator. Recommendation:
keep `/start` (the upload page) as the final URL for the Non-Brand Search campaign until the new page has two weeks of
Demand Gen data, then test the new page there with the `?a=generator` headline "See Yourself With Abs. Then Get The
Plan." and the goal image shown as the first thing in the trial. Brand Search and every Demand Gen ad go to the new
page on day one.

---

## 8. Step 0 for the design session: 30 minutes in VidTao and Chrome on Dan's Mac

The cloud research could not open these. Do this first, on Dan's Mac (Cowork or the desktop app with Chrome), and
screenshot each into `Docs/mockups/vsl-2026-09/reference/`. If a screenshot contradicts a claim above, the screenshot
wins; note the correction at the top of the mockup that uses it.

1. **VidTao:** search advertisers "MadMuscles", "V Shred", "BetterMe", "Noom", "Kinobody", "Built With Science", "Fit
   Father Project". For each: the top-spending ad of the last 90 days, its landing page (VidTao links ad to page), the
   page's above-the-fold screenshot at phone width. Also VidTao's top health/fitness advertisers list for the last 90
   days: note any men's fitness advertiser not in this doc and grab its landing page.
2. **Live pages, phone width (Chrome device toolbar 375 px), stop at any email or payment field:**
   `madmuscles.com` (screen 1 and, after generic answers, the paywall), `le.vshred.com/sp/quiz/body-type-quiz` then the
   results page (the video, its autoplay behavior, the button, what sits under it), `quiz.betterme.world` (screen 1, the
   projection screen, the paywall), `noom.com` (screen 1, a projection screen, the paywall), `skool.com/games`,
   `builtwithscience.com/app-bws-plus` (the pricing page with the trial timeline), `fitfatherproject.com/ff30x-letter-video/`.
3. Record for each: H1 wording, video yes/no + autoplay + length chip, CTA wording and color, what is above the fold
   on a phone, plan-card layout, where the renewal terms sit, timer yes/no.

If Dan runs the design session in the cloud instead, skip Step 0 and say so in the report; the mockups still stand on
the structural evidence.

---

## 9. Deliverables of the design session

1. **Five real HTML pages**, one per mockup, in `public/mockups/vsl/1.html` … `5.html` (noindex, `robots: noindex`,
   not linked from anywhere), built from `public/start.html`'s tokens so the winner becomes the live page with little
   rework. Mockup 2 and 5 may fake the quiz/estimate with static screens; say so on the page in a small grey "MOCKUP"
   chip. Placeholder video slot with the poster and a "4:30" chip.
2. **Screenshots** of each at 375 px (full page) and 1280 px (above the fold), in `Docs/mockups/vsl-2026-09/`.
3. **A one-page comparison** (`Docs/mockups/vsl-2026-09/README.md`): a table of the five (bet, who runs it, build
   effort, dependencies, risk), the recommended order, and the Non-Brand Search recommendation, for Dan to pick from.
   Published as a private Artifact link as well, so Dan can review on his phone.
4. **Copy passes:** every page's text through the section 2 phrase list and the em-dash character count = 0 (grep for it).
5. Commit and push (the mockups are static files; a deploy is fine and drops nothing that matters, but bundle it with
   other work if a locked hold is live: memory `deploy-drops-locked-holds`). No dashboard row (Dan's 2026-09-08 rule);
   report in chat with the five links and the comparison.

Out of scope: cutting WV-02 (`Handoffs/video-editing/WV-02-…`), changing the cart, building the quiz or the estimator
for real, touching the Google Ads final URLs. Those are the follow-on handoff once Dan picks.

---

## 10. Close out

When the design session delivers: remove this doc from the Open table in `Handoffs/README.md` and from the HANDOFFS
list in `AI_COORDINATION.md`; add one line under DAN'S DECISIONS pointing at the comparison page ("VSL page mockups:
pick one of five"). Keep `Docs/VSL_LANDING_RESEARCH_2026-09-24.md` (it is the evidence for the build handoff too).

---

## Recommended model and starter prompt

**Claude Opus 5.5, high effort, on Dan's Mac (Cowork or desktop) so Step 0 can use Chrome and VidTao.** Fable 5.1 high
if its allowance is free. Codex Astra high is fine for the HTML if Step 0 has already been done by a Claude session.

```
Execute Handoffs/handoff-20260924-vsl-landing-page-five-mockups.md. Read it fully, then
Docs/VSL_LANDING_RESEARCH_2026-09-24.md. Do Step 0 first (30 minutes in VidTao and the live competitor pages at phone
width, screenshots into Docs/mockups/vsl-2026-09/reference/, note any correction). Then build the five VSL landing page
mockups as real HTML pages in public/mockups/vsl/ from public/start.html's design tokens, following the non-negotiables
in section 2 exactly, with the copy drafted in the approved headline shapes, the trial timeline, the cart as the CTA
destination, and every disclosure in place. Screenshot each at 375 and 1280, write the comparison README with the
recommended build order and the Non-Brand Search recommendation, publish it as a private Artifact, run the em-dash
and banned-phrase checks, commit and push, and send me the five links with a five-line summary. Do not cut the video,
change the cart, or touch Google Ads.
```
