# VSL landing page research, 2026-09-24 (five reports, verbatim)

Companion to `Handoffs/handoff-20260924-vsl-landing-page-five-mockups.md`. Five research agents ran in parallel in a
cloud session on 2026-09-24. Read the handoff first; come here for the evidence behind any claim in it.

**How to read the caveats.** The cloud session could not reach Dan's Chrome (so VidTao's logged-in library was
unavailable) and its network policy blocked direct fetches of vidtao.com and every competitor site. Reports 2 to 5
therefore rest on search-engine summaries of the named pages, teardown articles, legal filings, and three first-hand
sources: this repo's own documents, the private Cart Teardown artifact of 2026-09-10, and Hormozi's own 2025 handbooks
(full text on GitHub). Every report marks what it could not verify. Report 1 is fully first-hand (it reads this repo).

| # | Report | Words |
|---|---|---|
| 1 | Audit of our own /start page, offer, funnel numbers and compliance record | ~3,700 |
| 2 | Men's fitness direct-response leaders (MadMuscles, V Shred, Kinobody, Athlean-X, Built With Science, over-40 players) | ~3,700 |
| 3 | Women's fitness and GLP-1 quiz funnels (BetterMe, Noom, Welltech, Sweat, Ladder, Hims, Ro, Found) + FTC rules | ~4,600 |
| 4 | Hormozi and info-product VSL structure + published video conversion data | ~3,500 |
| 5 | YouTube / Demand Gen landing rules, Google policy, VidTao/Inceptly doctrine, benchmarks | ~4,800 |

---

# REPORT 01: 01-audit-of-our-own-start-page-offer-and-compliance

# Audit of the existing paid-traffic landing page (/start) and everything around it

Note on quoting: several source lines contain em dashes. Per the project rule I have replaced them with commas or colons inside quotes; wording is otherwise verbatim. The memory files prior sessions cite (`ad-suspension-prevention`, `madmuscles-deep-dive`, `youtube-ad-competitor-research`) are not in this container; what follows is what the repo itself records. The file `.claude/skills/scriptwriting/references/vsl-2026-09-16-lessons.md` referenced by `Docs/VSL_LANDING.md:98` does not exist in this checkout (no git history for it either); `.claude/skills/website-video/reference/LESSONS.md` is the closest surviving lessons file.

## 1. The current /start page, exactly as built

File: `/home/user/abs-by-ai/public/start.html` (638 lines, single file; video config in `public/site-video.js`). Spec: `/home/user/abs-by-ai/Docs/VSL_LANDING.md`. Built 2026-09-09, `noindex`, served by the slug route in `server.js`. Every enabled Google Search ad and every Demand Gen `/start` ad group points at `https://absbyai.com/start`.

Meta copy (lines 6-12): `<title>See Yourself With Abs, Abs by AI</title>`; description "Upload one photo. In about 20 seconds Abs by AI shows you an AI image of your goal body, reads your estimated body fat and lean muscle, and builds the plan to get there."; og:description ends "Free to try."

Section order, top to bottom:

1. **Topbar** (258-261): brand + "Log in" link to `/`.
2. **Hero** (264-323). Two A/B variants, chosen before first paint (`?v=a`/`control`, `?v=b`/`analysis`; flag key `vsl-landing-variant`, which still does not exist in PostHog, so the page's own sticky 50/50 coin splits traffic).
   - H1 control (269): "See Yourself With Abs, Then Get A Personalized Plan To Make It Real." (Dan's headline, 09-09)
   - H1 analysis (272): "Find Out How Far You Are From Abs, From One Photo."
   - Hero visual (mobile slot under the H1): control = the video if `ABS_START_VIDEO` has an id (currently Muhammad's Ad 1 16:9 `lf46ytHacss` as interim per `handoff-20260910-start-vsl-edit-and-install.md`), else the male proof pair with tags "Uploaded photo" / "AI-generated" and the line "Fictional example. The AI-generated image is a visualization of a goal, not a real result, see our Disclaimer." (301). Analysis = a "Sample" mock card "What our AI reads from your photo": Body fat 24% to 12%, Lean muscle 138 to 142 lb, Fat to lose 24 lb, Goal weight 166 lb, focus chips (Lower abs focus, Obliques focus, Shoulders strong, Chest maintain), note "Visual estimates for motivation, not a medical measurement. Based on published body-fat ranges (sources)." (305-318).
   - CTA button (279-283) opens the photo picker in one tap: control "Upload a photo, see your abs"; analysis "Upload a photo, get my analysis".
   - Subtitle UNDER the button (Dan's 09-10 revision, 284-285): control "Upload one photo. In about 20 seconds our AI shows you an image of your goal body, then builds a workout and nutrition plan around it."; analysis "Upload a photo and our AI reads your estimated body fat and lean muscle, shows where your plan should focus, and generates an AI image of your goal body."
   - Under that only a "Privacy Policy" link (286).
3. **Proof** (328-354): H2 "Examples made with Abs by AI"; "A photo goes in; an AI image of the goal comes out. Pick Subtle or Ripped."; three pairs (male2, female, male; order set by Dan 09-09), "Swipe for more"; "Fictional examples. The AI-generated images are visualizations of a goal, not real results or a real transformation, see our Disclaimer."
4. **Video section, variant B only** (357-361): "Watch: what happens after your photo" / "Dan Rose, founder of Abs by AI, walks through the goal image, the analysis and the plan. 3 min 50 s." (script rewrites these when `ABS_START_VIDEO` has an id, 483-487).
5. **What you get** (364-405): H2 "What you get after one photo"; "The image is the start. The analysis and the plan are the point."; six tiles: Your goal image (Free), Your analysis (Free), AI workout program (Membership), AI nutritionist + macro tracker (Membership), Sleep coach (Membership), Supplement audit (Membership).
6. **How it works** (408-416): "Three steps. The first one takes about 20 seconds." 1 Upload a photo (shirtless or sports-bra, neutral pose, even lighting); 2 See your goal image and your analysis; 3 "Start the plan, free for 7 days ... Cancel anytime in two taps."
7. **Founder card** (419-427): photo `/img/dan-founder.jpg`; quote "Most people never start because they can't picture the finish line. Abs by AI shows you the finish line first, then tells you exactly what to do about it, every day." / "Dan Rose · Founder, Abs by AI".
8. **Trial card** (430-444): H2 "Everything in the app, free for 7 days"; "Your goal image stays free. The membership is the plan that goes with it."; four checks (AI workout program built around your equipment and level / AI nutritionist, meal plans and photo macro tracking / Sleep coach and supplement audit / Unlimited goal images and a progress log); CTA `Start your 7-day free trial →` to `/?join=1`; price line "then $19.99/mo or $69.99/yr · cancel anytime, and you won't be charged a dime"; "Not ready? Start with the free goal image" (opens the picker).
9. **FAQ** (447-456), five questions: "Is the image real?" / "What photo works best?" / "Are the numbers a medical measurement?" / "What happens to my photo?" / "What does the trial cost?" (answer: "Nothing for 7 days. After that it's $19.99 a month or $69.99 a year, and you can cancel anytime in two taps, cancel before day 7 and you're never charged. Refund policy.")
10. **Legal** (458): "AbsByAI is an app for generating an image of your fitness goal. **The examples shown above are not real fitness transformations.** They are examples of the type of images our app can make. Abs By AI does not change your body and does not promise any physical result. AI-generated images are labelled as such."
11. **Chips + privacy sentence moved from the hero** (460-463): "Free to try · About 20 seconds · No sign-up to see it" and "Your photo is sent securely to our AI partners (Anthropic, Google, Replicate) to create your result, never sold, delete anytime. Privacy Policy".
12. **Footer links** (464-466): How it works · Terms · Privacy · Refunds · Disclaimer · Sources · Contact · Already a member? Log in.
13. **Sticky mobile CTA** (470-472), appears once the hero button scrolls off: "Upload a photo → see your goal image".

PostHog events (`ph()` at 491-493, all carry `variant`): `vsl_landing_seen {forced, video_live, placeholder}` (634), `vsl_cta_clicked {cta: hero|sticky|trial_card}` (554), `vsl_photo_chosen {bytes, type, cta}` (598), `vsl_handoff {stored}` (610), `vsl_trial_cta_clicked` (618), `vsl_video_play {kind}` (508/513), `vsl_video_progress {pct 25/50/75/100}` (517, mp4 only). Also `$feature_flag_called` and `posthog.register({landing:'vsl', landing_variant})` per `VSL_LANDING.md:40-45`. Hand-off: photo downscaled to 1024 px JPEG 0.85, parked in `sessionStorage.absbyai_vsl_handoff`, then `location.href = /?from=vsl&v=<variant>` forwarding utm_*, gclid, gbraid, wbraid, fbclid, ttclid, msclkid (583-613). In the app: `vsl_handoff_received`, `generation_started {source:'vsl'|'home'}`.

Dan's hero revisions (`Handoffs/handoff-20260910-start-hero-copy-revisions.md`, executed, visible in the file): removed the avatar + "Dan Rose, founder · this picture got me abs · 3:53" caption; moved the subtitle under the button; only a Privacy Policy link under the button; chips and the AI-partners sentence moved above the footer. Dan also removed the boxed AI-disclosure paragraph from the hero on 09-09 and the body-type/intensity chips (answered in the app instead).

## 2. The real offer, prices and trial mechanics

- Free tier: `FREE_CREDITS = 3` free generations per device (`server.js:185`). Credit packs were retired 2026-08-12; the trial is the only way to get more generations (`public/index.html:1944-1949`).
- Plans: `MEMBERSHIP_PLANS` monthly 1999 cents/month, annual 6999 cents/year (`server.js:196-198`). Displayed as "Monthly $19.99, 7 days free, then $19.99/mo" and "Annual $69.99, SAVE 71%, $5.83/mo" (`index.html:2929-2941`, cart 2991-3006). Monthly is first and pre-selected on web and membership screens (Dan, 2026-09-10).
- Trial: 7 days, card required (`payment_method_collection:'always'`), one trial per account for logged-in buyers; anonymous cart buyers always get the trial and reuse is logged (`Docs/WEB_CART.md:31-36`). Reminder email on day 5 (`trialReminderSweep`). Cancel via Manage membership → Stripe portal ("two taps"). Refunds page says full refund within 7 days.
- Web flow (shipped 2026-09-10, `Docs/WEB_CART.md`): upload → result → "Lock in this goal" → **analysis page** → cart (pay first) → account created from the Stripe email → optional password → five onboarding questions → hub. Native apps keep IAP and account-first.
- Analysis page copy (`index.html:2050-2181`): top "We've generated a personalized fitness plan to make your goal image real." / "Click the button below to claim it." / `Start your 7-day free trial →` / "then $19.99/mo · cancel with two taps and you won't be charged a dime"; "What our AI already knows from your pictures" tiles (Body fat, Lean muscle, Fat to lose, Goal weight); "Visual estimates for motivation, not a medical measurement. Based on published body-fat ranges (sources)."; height/weight sliders; "Where your plan will focus" body map; "What this means for your plan" (Training, Food, Protein, Timeline); bottom CTA "Try Abs by AI completely free for 7 days" / "Try out the macro tracker, the AI workout program, the AI nutrition plan, everything in the app."; email capture "Email me my picture + my analysis"; "Continue to my hub →". Locked (out of credits) state: button "Unlock it with a 7-day free trial →", title "Unlock your goal image, free for 7 days" (5440-5444). Paywall copy: "Your result is ready, unlock it" / "You've used your free generations. Before you unlock it, see what our AI already read from your pictures..." / "See what our AI found →" / "Skip to the 7-day free trial →" (1942-1957). Defaults: men 5'9" 185 lb (2100-2105); women's 5'4" default is still an open Dan decision (board).
- Cart copy (`index.html:2969-3030`): "Your plan is ready." / "Start your 7 days free. Nothing is charged today."; recap fine print "AI visualization, not a real result · visual estimates"; timeline Today $0 / Day 5 reminder / Day 7 first charge; four benefits; disclosure directly above the button "7 days free, then $19.99/month, billed automatically and renewed every month until you cancel. Cancel any time before the trial ends and you won't be charged. Manage or cancel in Manage membership. Terms."; `Start my free 7 days →`; "Apple Pay, Link or card · your email becomes your login"; "Continue to my hub without a trial →". No timers, no discounts, no invented social proof.
- Membership screen benefit list (2869-2877): 4-week AI training program and every block after, unlimited future-self images, unlimited AI meal and macro tracking, AI Nutritionist meal-prep plan, Supplement Audits (25/month), AI Sleep Coach, adaptive check-ins.
- Home page hero for comparison (`index.html:1647-1649`): "Visualize Yourself With Abs" / "See how good you'd look with abs. Then get a personalized AI workout and nutrition plan to make your dream body real." / product note "Upload a photo and Abs By AI generates an AI image of your goal. It's a visualization and motivation tool, **the images are AI-generated, not real results.**" (this note shipped in commit `fd23801` during the suspension).

## 3. Compliance constraints on record (quoted)

**Google Ads suspension history** (`AI_COORDINATION_ARCHIVE.md:2174-2226`): account 342-717-0837 suspended 2026-08-09 under Unacceptable Business Practices at $0 spend / 17 impressions; reinstated 2026-08-11 as a billing/identity verification hold. Corrected causal analysis: "the vigilance points are (a) anything reading as a promised physical outcome, and (b) account/billing/identity consistency and linkage, NOT symbols in headlines. Dan's baseline scrutiny is elevated by his suspension history, so the margin has to come from boring creative and slow ramps." Copy that was replaced: `Get Real Abs Using AI Tools`, `Get Sixpack Abs Using AI Tools`, "...make them real" → `See Your Goal Before You Start`, "Visualize yourself with six pack abs, then get an AI workout and nutrition plan." "**Do NOT open a second Ads account under any circumstances**." The AI-made "The Upload" video stays limited under "YouTube & Discover Feed Ad Requirements, Negative Events and Imagery" (body-image policy) regardless.

**Ad-copy lint, hard gate** (`Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md:161-169`): "no physical-result promises ('get abs', 'get a six pack', 'lose', 'burn', 'shred', 'transform your body', 'real results'), no timeframes ('in 30 days', 'in 2 weeks'), no before/after language, no disease, drug, or medication names (no 'Zepbound', 'Ozempic', 'GLP-1'...), no 'guaranteed', no '®'/'™', no superlatives about the viewer's body, no negative self-image phrasing ('out of shape', 'fat', 'embarrassing'), no all-caps, no exclamation marks... Sell the video and the visualization, never the body."

**Demand Gen policy verdicts** (`Docs/DGEN_CONVERSION_CAMPAIGN.md:36-49, 108-112`): "This Picture Got Me Abs" and "Abs At 40, The Photo That Did It" → CLICKBAIT limited; "Why My Diets Kept Failing" → DISAPPROVED CLICKBAIT (the "Why My X Kept Failing" shape is now refused by `dgen-add-ad.js`); Zeeshan's Ad 1 video → `EXAGERRATED_OR_INACCURATE_CLAIMS`. "**Dan's copy rule (2026-09-10):** no claim that reads unbelievable without the video's context. 'This picture got me abs' is too much; 'How I get abs at 40' / 'How AI got me abs' are the shapes to reuse."

**Landing-page compliance** (`Docs/VSL_LANDING.md:118-125`): "What still carries the disclosure above the fold: the 'AI-GENERATED' tag printed on every after-image, the label under it, and the 'Fictional example ... not a real result' line directly under the hero pair (kept at Dan's request). Lower down: the visual-estimate qualifier + /sources on every number, the FAQ, and the legal footer. The headline's 'make it real' is the same phrasing the home page has carried since the August reinstatement; if Google ever flags the page, that phrase and the missing hero paragraph are the first two things to put back."

**Google policy research** (`Handoffs/handoff-20260730-google-ads-compliance-pages.md:31, 54, 72`): "The pages are NOT the biggest suspension risk, the AI before/after imagery is." "Every before/after ... needs a visible 'AI-generated visualization, not a real result' label on or immediately adjacent to the image, not in a footer. Google explicitly prohibits before/after images that misrepresent effectiveness, names Manipulated media as its own Misrepresentation sub-policy, and treats weight loss as a restricted health category." Billing: "Failure to clearly and conspicuously disclose the payment model or full expense ... before and after purchase is not allowed" → trial/auto-renew terms above the pay button. "Google prohibits remarketing/personalized audiences on sensitive health categories including weight loss."

**Meta** (`AI_COORDINATION_ARCHIVE.md:96-120`): before/after is NOT banned outright; prohibited are "statements of inferiority about physical appearance", pinching-fat close-ups, "implying or attempting to generate negative self-perception", "idealized" bodies, clickbait with timeframes. "The trigger is the FRAMING, not the body." Weight-loss ads must target 18+. "Our AI-generated goal imagery is the sharpest risk ... The existing label must appear on the ad creative itself."

**Video/imagery rules that also bind page imagery** (`.claude/skills/_shared/VIDEO-RULES.md:67-104`): never mix people across a before/after pair; Dan's real after pictures carry "Real picture of me, not AI-generated" (thumbnails/covers exempt); AI images keep "AI-GENERATED"; no side-by-side before/after in paid ads (`handoff-20260901-brandon-carter-style-thumbnails.md:72`: "Side-by-side before/after is banned in paid ads only"); never the app's email-capture screen or before/after reveal screen on camera; no "thousands of guys" claims (real count of people who completed a generation was 75 on 2026-09-10, `handoff-20260910-start-vsl-edit-and-install.md:64`).

**FTC / cart rules** (`Handoffs/handoff-20260910-web-pay-first-cart.md:104-106, 245-252`): "Compliance is the moat. MadMuscles' parent, Genesis Tech, was halted by a federal court on the FTC's motion on 2026-06-17 for hidden auto-renew terms, unauthorized and double charges, and obstructed cancellation. Copy their structure; never copy their tricks." No fake/resetting timers, no pre-selected add-ons, no confirmshaming, renewal disclosure stays above the button, "Don't promise what the system doesn't do." Reaffirmed in `handoff-20260924-generator-consult-call-outreach.md:23-25`: "No invented scarcity ('only 10 spots'), no discount devices, no claims about results."

**Medication angle** (`AI_COORDINATION_ARCHIVE.md:3024`): shelved by Dan, "too likely to be disapproved on a brand-new Google Ads account."

## 4. Competitor findings and Dan's funnel/offer decisions

- **Standing rule** (`AGENTS.md:85-91`): "Recommend only funnels, offers, landing pages and ad tactics that the top fitness direct-response players (V Shred, MadMuscles, BetterMe, Noom) actually run. Name which one does it. If none of them do it, do not recommend it. ... Dan's verdict: the free AI-generation front-end funnel should never have been tested, and inventing something new is why it failed. The generation stays a member feature, not the entry hook. Judge paid traffic on cost per trial and cost per paying customer, not a mid-funnel action." Consequence already applied: RA-11 (free-generation entry hook) superseded by RO-17 on 09-24 (`handoff-20260924-edit-queue-phase2-ro17-production-pilot.md:3`).
- **New VSL direction** (`Docs/VSL_LANDING.md:88-97`): Dan selected Claude's "AI Got Me Abs at Forty" script "primarily for a new page that requires signup before generation, also usable on /start"; Dan asked for a "direct ring connection" line written as available. Both VSLs were filmed 9/23 (VSL 1 analysis-page version A + version B "fired them all" intro, rolls C1692-C1700; VSL 2 /start, C1701-C1703) per `Docs/SHOOT_923_FOOTAGE_REPORT.md:26-33`; edit jobs `Handoffs/video-editing/WV-01…` and `WV-02…` are READY, not cut. Scripts live in Google Docs `1qt47J2sWcdLXIQYQ055dooKPad8cOJrFMsYhj0VWrIQ` (teleprompter) and `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4` (b-roll).
- **Cart teardown** (`Docs/WEB_CART.md:7-8`): MadMuscles, V Shred, BetterMe, Noom, Muscle Booster, Blinkist; "ten patterns copied / adapted / refused" live only in a private Artifact ("Cart teardown", 2026-09-10), not in the repo. What was copied is visible in the shipped cart (section 2). Refused: timers, discount devices, invented social proof, order bumps/upsell chains ("we sell one subscription", `handoff-20260910-web-pay-first-cart.md:151-153`).
- **MadMuscles funnel shape** (`Handoffs/handoff-20260812-purchase-before-account.md:15`): "quiz → paywall → purchase → account. MadMuscles does not ask for an email until after the card is in." Adopted on web 09-10.
- **Quiz decision** (`Handoffs/handoff-20260717-member-profile-questionnaire.md:22`): "effort-investment before a paywall raises conversion (Noom/Fitbod pattern), but Abs By AI's own after-photo already does the heavy personalization lift, so a long quiz would be redundant friction." Later moved after payment as onboarding (cart handoff, "Key Decisions").
- **Ad creative study** (`.claude/skills/ad-edit/reference/AD_STUDY.md:36-39, 85-96`): V Shred $101.4M lifetime, remixes prior winners, all-time #1 is a clean white-studio 4:27 listicle; MadMuscles ($488M/yr per VidTao) 0:47-2:16 podcast/interview framing, caption every shot, burned micro-disclaimer on every ad, every winner in 9:16 and 16:9.
- **Tone** (`.claude/skills/ad-outlines/SKILL.md:184-197`, Lesson 7): Dan: "We need to be more controversial... solving what the prospect believes is their problem... like successful direct response advertisers do." Blunt claims OK ("it's mostly a scam" about human experts), but "The edge belongs in the CLAIM, not in language that would get the ad rejected."
- **Codex conversion-strategy report** (2026-09-14) exists only on Dan's Mac (`~/.codex/visualizations/2026/09/14/…/abs-by-ai-conversion-strategy.docx`), not in the repo; the board lists it under "Research to act on".
- Dan's facts for message match: got his abs back at 40 over about two years; one daughter, never "my kids" (`AI_COORDINATION_ARCHIVE.md:3026`).

## 5. Funnel numbers on record (with dates)

- 2026-09-09, PostHog last 30 days, absbyai.com (`Docs/VSL_LANDING.md:8-18`): `$pageview` 571 → `generation_verifier` 55 (9.6%) → `analysis_page_seen` 1 (page shipped 09-08) → `trial_signup_started` 6 → `membership_subscribed` 4 → `paid_conversion_reported` 2. "516 of 571 visitors (90%) leave without ever uploading a photo."
- 2026-09-09, last 60 days, trial funnel (`handoff-20260910-web-pay-first-cart.md:22-33`): `trial_gate_shown` 16 → `account_signup` 6 → `quiz_completed` 3 → `membership_screen_viewed` 3 → `membership_subscribed` 0. Stripe subscription sessions: 11 opened, 1 completed (card later declined), 9 expired. Postgres: 11 real accounts, 1 active.
- Since the first ad click 2026-07-30 (`handoff-20260909-google-ads-account-fixes.md:147-156`): 207 ad arrivals → 191 saw the proof strip (92%) → 35 got an AI result (17%) → 4 gave an email → 2 accounts → 2 trial signups → **0 paid**. Google Ads spend Aug 1 to Sep 9: $1,272.66, zero paying customers; 1,088 of 1,096 "conversions" were YouTube subscriptions.
- Demand Gen conversion campaign first day, 09-10 to 09-11 (`Docs/DGEN_CONVERSION_CAMPAIGN.md:55-59`): $20.14, 1,091 impressions, 17 clicks, 225 views, 0 Free Generation Started; ~18 visitors (8 home, 10 /start, 2 VSL plays), none uploaded. Search logged 7 FGS conversions that week.
- 2026-09-10: /start had ~4 visitors; 75 people had ever completed a generation.
- Board (`AI_COORDINATION.md`, "Ads results follow-up, OPEN 2026-09-15"): Meta $2.02/follow vs <$3 target; no Google results after the 09-09 fixes are recorded in the repo. Trial Signup conversion has never fired from an ad click ("Misconfigured" only because no ad-attributed trial exists, `Docs/GOOGLE_ADS_API.md:165-167`).

## 6. Ads running now (for message match)

Account 342-717-0837. Landing page for all conversion traffic: `/start` (Search, 2026-09-11; DGen has a `/start` and a `home` ad group per ad).

**Search** (`Docs/GOOGLE_ADS_API.md:152-188`): Brand `24086091285` (Maximize Clicks, $2 CPC cap since 09-24; ad groups "Brand - Abs By AI", "Brand - Dan Rose"), Non-Brand `24148587722` ("AI Abs Generator", "AI Body Transformation Preview", "Add Abs To Photo", "What Would I Look Like With Abs"; converting terms: six pack ai, ai six pack, give me abs ai, abs editor ai, six pack generator). Live RSA copy shape: `AI Six-Pack Preview Tool`, `AI Six-Pack Image Generator`, `See Your Goal Before You Start`, "Visualize yourself with six pack abs, then get an AI workout and nutrition plan." Sitelinks: Home, How It Works, FAQ, Contact.

**Demand Gen conversion campaign** `24243839443`, US+CA, male+unknown 25-54, Target CPA $30 on Free Generation Started, budget read back $50/day on 09-21 (`Docs/DGEN_CONVERSION_CAMPAIGN.md`). Ads and themes:
- Ad 1 "This Picture Got Me Abs" (headlines: How I Got Abs At 40 · See Yourself With Abs - Use AI · Abs By AI - Here's How It Works · How I Got Abs With AI Workouts)
- Ad 2 "Stop Wasting Money On Nutritionists" (Fire Your Nutritionist. Use AI Instead · How AI Replaces Nutritionists · How AI Got Me Abs)
- Ad 3 "Stop Paying Human Trainers" (Fire Your Personal Trainer)
- Ad 4 "Stop Wasting Money On Supplements" (How AI Fixed My Supplements · Audit Supplements With AI · The Truth About Supplements)
- Ad 5 "Every Diet You've Tried Failed" (AI Meal Plans Built Around Your Foods; "Why My Diets Kept Failing" disapproved)
- Ad 6 "You're Not Too Old"; Ad 7 "Photoshop To AI"; Ad 8 "Two AI Futures"; Ad 9 "ChatGPT For Abs"; Ad 10 "Busy Dad Fitness"; Ad 13 "The Cost Of Getting Abs"; Ad 14 "Workout Video Overload"; Ad 15 "Dad In A T-Shirt"; RA-01 "How AI Got Me Abs" (added 09-18).
- Ads 11 and 12 do not appear in the campaign doc.
Recurring approved headline shapes across all of them: "How I Got Abs At 40", "How AI Got Me Abs", "Abs By AI - Here's How It Works".

**Engagement campaigns** (`Docs/YTADS.md`, library mode since 09-13): tier 1 `24163535721`, tier 2 `24122099676` ($5/day), remarketing `24169507109` (~$2.50/day, 0 conversions ever, pause is an open Dan decision). Only one enabled ad at a time, chosen by Dan (currently the $17 Ab Wheel long-form).

**Meta**: @danrosefit champion ad set `120250753601020682` at $6.50/day, engagement objective; both [DAN] [ENGAGEMENT] campaigns off (board).

Key files: `/home/user/abs-by-ai/public/start.html`, `/home/user/abs-by-ai/Docs/VSL_LANDING.md`, `/home/user/abs-by-ai/Docs/WEB_CART.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260910-web-pay-first-cart.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260910-start-hero-copy-revisions.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260910-start-vsl-edit-and-install.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260730-google-ads-compliance-pages.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260909-google-ads-account-fixes.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md`, `/home/user/abs-by-ai/Docs/DGEN_CONVERSION_CAMPAIGN.md`, `/home/user/abs-by-ai/Docs/GOOGLE_ADS_API.md`, `/home/user/abs-by-ai/AI_COORDINATION_ARCHIVE.md` (lines 96-125, 2174-2226, 3024-3026), `/home/user/abs-by-ai/.claude/skills/_shared/VIDEO-RULES.md`, `/home/user/abs-by-ai/.claude/skills/ad-outlines/SKILL.md`, `/home/user/abs-by-ai/.claude/skills/ad-edit/reference/AD_STUDY.md`, `/home/user/abs-by-ai/public/index.html` (1630-1649, 1942-1963, 2050-2181, 2852-2946, 2959-3030, 5440-5444, 8250-8253), `/home/user/abs-by-ai/server.js` (185, 196-198), `/home/user/abs-by-ai/Handoffs/video-editing/WV-01-vsl-1-analysis-page-video-version-a-version-b-intr.md`, `/home/user/abs-by-ai/Handoffs/video-editing/WV-02-vsl-2-start-landing-page-video.md`.

---

# REPORT 02: 02-mens-fitness-direct-response-leaders

## Research report: paid-traffic landing pages of the men's fitness direct-response leaders (2025-2026)

### How this was researched, and what could not be reached

Every direct page fetch was blocked by this session's egress proxy: madmuscles.com, vshred.com and le.vshred.com, kinobody.com and go.kinobody.com, athleanx.com, fitfatherproject.com, over40alpha.com, builtwithscience.com, jeffnippard.com, seannal.com, ftc.gov, web.archive.org, and every third-party teardown site tried (web2appworld, funneloftheweek, outgrow, funnelfox, adapty, revenuecat, trustpilot, honestbrandreviews, etc.). The session's web-search budget (200 calls) then ran out mid-task. So the findings below come from three sources, each labeled: (a) search-engine result summaries of the live pages and teardowns, (b) the project's own first-hand competitor work already in the repo: the private "Cart Teardown" artifact of 2026-09-10 (https://claude.ai/artifact/MevY5JFc7FTEAikSbQhreV, a walk of the MadMuscles quiz to its email gate and a capture of V Shred's order form, with paragraph cites to the FTC complaint), `.claude/skills/ad-edit/reference/AD_STUDY.md` (frame-level study of V Shred and MadMuscles ads from VidTao), and `.claude/skills/make-ad/SKILL.md` (VidTao spend data, July 2026), and (c) the FTC action as reported by law-firm and press summaries. Exact above-the-fold copy, button colors and mobile layouts could only be verified where a source quoted them; everything else is marked "could not verify". Treat this as a strong structural map with copy gaps, not a pixel record.

One correction to the brief: Muscle Booster is not a MadMuscles sibling. Muscle Booster is Welltech Apps Limited (Trustpilot 4.3/5 from ~8k reviews). MadMuscles is operated by Amoapps Limited inside the "Genesis Tech" network the FTC sued (Cyprus and Delaware entities). They are competitors that run the same playbook, not one company.

---

### 1. MadMuscles (madmuscles.com)

**Scale (web2appworld breakdown, Jan-Feb 2026; VidTao via make-ad skill, July 2026).** About $29.4M/month on YouTube alone; 3,498 YouTube ads and 3,240 Google Display ads; 2,335 Facebook ads across 38 landing pages in Feb 2026; 493 unique quiz landing pages; traffic 8.1M to 17.4M sessions in January 2026. VidTao's July 2026 read: roughly $488M/yr run rate, 5-10 hook variants per script, losers killed near $5k spend, winners scaled past $200k per 30 days. Top single ad: a 73-second podcast-style tai chi creative, $14.2M lifetime.

**Ad creative (AD_STUDY.md, measured frame by frame).** 0:47-2:16 long, podcast/street-interview framing with an AI character and AI voiceover, a caption on every shot, a burned micro-disclaimer on every ad, and every winner shipped in BOTH 9:16 and 16:9. Themes rotate by performance: tai chi walking (21.5% share, Feb 2026), military workouts (28.4%, now the lead), military calisthenics. Each theme has its own entry URL and gender-specific flow. Health claims seen in ads (wudang.academy critique): "reduce cortisol," "boost testosterone," "melt belly fat in 7 days."

**Ad landing page = the quiz's first screen. No VSL anywhere in the funnel.** Example entry URLs indexed: `madmuscles.com/funnel/default-261/quiz/default-144-gender?stepId=step-goal`, `madmuscles.com/funnel/default-uni-soft` (the one walked first-hand), `madmuscles.com/quiz-workout/step-email`. Page title: "Personalized workout program - MadMuscles". Pinterest pin text for the site: "personalized workouts for men. Take a quiz to pick a workout according to your goal." Exact hero headline wording and button color on screen one: could not verify.

**Quiz order (web2appworld + Good Men Project + first-hand walk).** 48 screens male / 47 female (the first-hand walk counted about 35 steps to the email gate on the "uni-soft" variant). Screen 1: gender, which branches the whole flow (different body images, goal framing, visual language). Screen 2: current body type: "Lean / Average / Chubby". Screen 3: main goal: gain muscle mass / lose weight / shape body. Then the nine captured variables: age, target body, height, weight, target weight, equipment, time budget, training frequency, problem areas, fitness level. Email is collected on the step immediately before the paywall (first-hand: stopped there). Interstitial "social proof" screens exist but their copy could not be verified.

**Pre-paywall / paywall page (first-hand reconstruction + FTC complaint ¶¶131-153).** Headline "Your personalized plan is ready!" with "Personal summary based on your answers" underneath. Then a "discount wheel" that always lands on the biggest discount, then a 10-minute countdown ("discount reserved") (FTC ¶139). Three plan cards priced per day, strike-throughs on each: 1-week $6.93 ($0.99/day, from $13.86); 4-week $15.19 ($0.50/day, "62% off $39.99", badge "POPULAR"); 12-week $25.99 ($0.28/day, "63% off $69.99") and the 12-week card is the one PRE-SELECTED, not the "Popular" one. Orange button "GET MY PLAN". Below: roughly 24 screens of testimonials, before/after photos, FAQ. Renewal text sits below the fold in the smallest type on the page: "By continuing, you agree that your subscription will be auto-renewed at the full price of 39.99 USD each month…" (renews at $39.99/month for the 1- and 4-week plans, $69.99 per 3 months for 12-week). The payment form itself never mentions renewal (FTC ¶141). Wallets on the form: PayPal, Apple Pay, Google Pay, card. Social proof claim "4.5/5 from 62k reviews" while Trustpilot showed 3.8/5. After payment: meal-plan upsell with a bright "Add" and a small grey X, no confirmation before the second charge, then a 20%-off retry, then a supplement subscription (FTC ¶¶144-147). No guarantee block was recorded on the paywall; could not verify one exists.

**The FTC action (June 2026).** Complaint filed June 2, 2026 (FTC v. GM Universeapps Ltd. et al., N.D. Cal. No. 4:26-cv-05232) against Genesis Tech-related entities and eight individuals for Section 5 and ROSCA violations across Wisey, PDF Guru/PDF Master, Lumi, Nebula, and MadMuscles/Harna/Unimeal; "nearly a quarter billion dollars" in revenue from early 2023 to mid-2025. The alleged pattern, in the FTC's words as reported: hook with a free or low-cost offer, "build trust through quizzes and personalized results," hide auto-renewal terms, charge unexpected recurring fees, unauthorized and double charges, and make cancellation difficult. A federal court halted the operation by TRO (the repo records June 17), and a preliminary injunction was entered June 30, 2026 (hearing July 2, Oakland). What changed on the live site since the injunction: could not verify. Note the FTC case as reported is about hidden terms, charges and cancellation; the "fake reviews" element I could substantiate is the inflated review-score claim, not a formal fake-review count.

**Muscle Booster (Welltech), for contrast.** A ~10-minute questionnaire, then a HARD paywall before the plan is shown, no trial. Weekly/monthly/yearly ($9.99/week to $59.99/year), annual pre-selected with "Best value", discounted first period that renews unless cancelled 24 hours before period end. Email, then card. Roughly $700k/month app revenue plus a large web funnel (memory notes ~$35M/yr YouTube). Quiz screen copy: could not verify.

---

### 2. V Shred (vshred.com, Vince Sant)

**Scale and ads (AD_STUDY.md via VidTao).** $101.4M lifetime YouTube ad spend, average ad 2:49. All-time #1 ad ($5.3M, 2020) is a 4:27 clean white-studio listicle with designed typography and a persistent numbered-step chip. The 2026 winner ($2M) is a 1:24 9:16 remix with a caption on every shot, ~1.7s cuts, whip transitions and glitch repeats; a $306k variant uses Dr. Drew authority footage. Ad file names literally document the method: "MIX 2 tips + 3 tips", "winner structure", "(timer)". Ads feature Vince; traffic goes to the Body Type Quiz (July 2023 YouTube ad titled "VShred: Body Type Quiz" is indexed). Some traffic goes through an advertorial pre-lander first: `vshred.com/blog/body-type-quiz-advertorial-1-celebrity-trainer-v3/` and a "Metabolic Assessment Page - Trainer Team Funnel". A $4M VPPA class-action settlement (2025) concerned the Meta/Google pixels on these pages.

**Quiz.** `le.vshred.com/sp/quiz/body-type-quiz`. About one minute; gender, age, height, weight, activity, goal, then body-type framing (ectomorph / mesomorph / endomorph). The answers ride in the results URL: `condition=femaleFatLoss&segment=5&gender=female&age=45&activity=light&macrogoal=fat-loss&units=imperial&inches=64&weight=160`. Exact question wording and first-screen headline: could not verify.

**Results page = the VSL page, one per segment.** Indexed variants: `/sp/survey/male-gr` ("Quiz Results: GET RIPPED"), `male-sf` (Skinny Fat), `male-fl` (Fat Loss Extreme), `results-male-cb` (Clean Bulk), `female-gt` (Get Toned), `female-fl`. Verified copy on the page: "Vince Sant, a Professional Fitness Model, Certified Personal Trainer, Best-Selling Author and Creator of V Shred, shares 3 crucial fixes SPECIFICALLY for YOUR body type and fitness goals" that "you can start using today." First-hand capture (Cart Teardown): a roughly 5-minute "3 secrets" video, autoplay muted with "Click to unmute", followed by the program pitch, testimonials with before/after photos, and the offer. Exact headline above the video, thumbnail style, and CTA button color: could not verify.

**Offer and checkout.** Fat Loss Extreme framed as "over $1,400 in value for just $57," "one-time payment, no hidden fees or subscriptions" (search summary; the first-hand capture saw a $47 SKU, `sku_fat_loss_extreme_for_him_47`, so the price varies by variant or date). Guarantee copy: "ZERO Risk, Unconditional 30-Day Money Back Guarantee"; on the order page "100% MONEY BACK GUARANTEE" plus a "Lifetime Customer Satisfaction Guarantee" under the button. The order form is the outlier of the whole set: thirteen fields before the card (email, mobile, first/last name, company, country, street, apt, city, state, zip, phone, "Create password"), Adyen card fields only, no Apple Pay or PayPal, one "PLACE ORDER" button. After purchase: video upsells at $41-$149 (custom diet plans, coaching, Sculpt Nation supplements); BBB complaints describe stacked bumps with no running total (about $382). The V Shred app is $1 first month then $20/month. A 2025 class action (Goldman v. V Shred) alleges the strike-through "regular" prices were never charged.

---

### 3. Kinobody (Greg O'Gallagher)

**Entry.** The "Kinobody Physique Builder Quiz" (30-60 seconds) recommends a program and hands out a $20 discount on it. No evidence of a webinar; a `go.kinobody.com/faq/` "Movie Star Body" page and Teachable "Warrior Shredding Program - Free Trial" page are indexed, so a free-trial-into-course path exists. Whether current YouTube ads run, and where they land: could not verify.

**Sales pages and offers.** Shopify pages `kinobody.com/pages/masterclass`, `/masterclass-msm`, `/masterclass-dup`, `/movie-star-stack`, `/sales-page-ggp`, `/warrior-shredding-program`, with a SamCart checkout (`moviestar-body.samcart.com`). Movie Star Masterclass: $197; "the most effective program to transform into movie star shape in as little as four months"; "over 40 video lessons," a 4-month training and nutrition plan, "three hard hitting workouts per week, a simple fasting strategy." Guarantee: 60-Day "Transform or It's Free" money-back. Warrior Shredding: $69, "pay once and get lifetime access," 30-day guarantee. Greek God 2.0: "30% off for a limited time," "over 70,000 men enrolled," 30-day guarantee. Site-wide promo codes (NEWYEAR2025, 30% off). Page layout, video presence and headline: could not verify.

---

### 4. Athlean-X, Built With Science, Jeff Nippard, Six Pack Shortcuts, Sean Nalewanyj

**Athlean-X (athleanx.com/ax1, title "Best Men's Workout Plan | ATHLEAN-X").** AX-1: 90-day program, "$97.00 lifetime access, billed one-time," daily workouts plus meal guide, minimal equipment. AX-2 X-TREME: $97 lifetime or "$16.59 per month, 1-year access billed annually at $199" for 40+ programs; NXT $29.95; All Access about $30/month or $300/year. Guarantee is the "X-TRA MILE GUARANTEE": for the full 90 days the team answers questions and modifies exercises to get you through. A dedicated over-40 proof page exists: `athleanx.com/reviews-and-testimonials/fit-over-40`. No quiz found. Headline, video and layout: could not verify.

**Built With Science (Jeremy Ethier; RevenueCat Sub Club 2026 with Ethan Ethier).** 90% of paid traffic goes to a quiz, not the App Store; run head-to-head, "the quiz won on conversion decisively," so store links are kept only for the highest-intent users. The quiz "educates users on the actual product, overcomes objections, and increases perceived value" and its answers build the plan, so it doubles as onboarding. BWS+ is $29.99/month or $189/year with a 14-day free trial; organic converts 35-40% trial-to-paid, cold Meta traffic about 25%. Their biggest win of the year was the pricing page: show ONLY the annual plan, paired with a day-by-day timeline of the trial ("day 1, you get your personalized plan; day 12, a reminder that your trial is about to end and you can cancel anytime"). Standalone courses $69-$119. Entry page indexed: `builtwithscience.com/app-bws-plus` ("Find Your Built With Science+ Program"). Quiz screen copy: could not verify.

**Jeff Nippard.** A Shopify catalog, programs about $40-$50 (Powerbuilding 3.0 $49.99), bundles, "The Muscle Ladder" page. No quiz, no VSL, no trial found. Not a paid-traffic DR funnel in the sense this brief needs.

**Sean Nalewanyj.** Body Transformation Blueprint: one-time $77, "100% 60-day money back guarantee… no questions asked," 250-page ebook plus workouts, exercise videos, meal plans, supplement guide; a "blueprint-giveaway" opt-in page. Page layout: could not verify.

**Mike Chang / Six Pack Shortcuts (legacy).** The mechanism-led long VSL: the "Afterburn effect" ("burn fat up to 14 hours after"), a three-part video program, "90 minutes of exercise per week." The original VSL pages are gone and his classic ad uploads are now private (AD_STUDY confirms 403s). Dan's own SixPackAbs-era winners (AD_STUDY) show the house pattern that era ran: 4-7 minute ads, a persistent CTA lower-third from ~0:22 or ~1:30 to the end ("Click Here Or Go To …"), and an end card of physique plus "CLICK BELOW or go to [URL]".

---

### 5. Men-over-40 advertisers

**Fit Father Project (Dr. Anthony Balduzzi).** Homepage positioning "Weight Loss for Busy Men 40+"; a free lead magnet (free meal plan + workout; "click a button to select your #1 goal"). The sales page is a video letter: `fitfatherproject.com/ff30x-letter-video/` (plus a text version `/FF30X-letter-/` and `ff30x.fitfatherproject.com`). Headline copy verified: "THE PROVEN WEIGHT LOSS PROGRAM FOR MEN 40+" and "world's #1 health & fitness program for guys 40+". Credential and story on page: dual degrees in Psychology & Nutrition from Penn, a naturopathic doctorate, former national champion bodybuilder, and "he watched his own Dad work himself to the bone, lose his health, and die at 42." Counts: "over 52,561 men" (homepage) / "over 35,000 fathers" (older copy); "many guys losing up to 15lbs in their first 30-days." Price $147 (store product "fit-father-30x-program-special"; a "Foundations" tier also exists). Guarantee: "Ironclad 100% Satisfaction Guarantee… after 30 days, if you're not satisfied… 100% refund, no questions asked." A post-purchase upsell page (`us1-ffb-ff4l`, Fit Father For Life) exists. Video length, autoplay and CTA color: could not verify.

**Over 40 Alpha (Funk Roberts).** Homepage title is the offer: "Join Funk's Over 40 Alpha For $1". $1 for 30 days, then $29 every 30 days ("Brotherhood" subscription); alternate pages run a 7-day free trial and a yearly plan (ClickFunnels). Includes daily bodyweight/dumbbell workouts, nutrition, weekly live coaching with Funk, an app and a Facebook group. Guarantee copy conflicts across pages: "100% satisfaction guarantee… refund at the end of the 30-day trial" on one, "cancel at anytime but there will be NO REFUNDS PROVIDED" on another. Page layout: could not verify.

**Others.** "Jacked After 40 / 12-Week Shred System" exists (jackedafter40.com) but could not be fetched. Athlean-X's "Fit Over 40" testimonial page is the only over-40 proof page from a mainstream brand found. "Ripped After 40" and "Old School Labs" landing pages: not found.

---

### 6. Category benchmarks worth carrying into the mockups

- Web-to-app funnels: about 3% of sessions purchase; about 13% reach the paywall; 44.5% of purchases happen on day 0 and non-converters rarely return to the paywall (search summaries of FunnelFox/Adapty 2026 data).
- Noom converts "north of 10%" of quiz completers to paid versus a 2.7% median; Noom runs 365 landing-page experiments a year and its homepage is nearly empty except the quiz CTA. Noom's trial is pay-what-you-want ($0.50 to $18.37, $10 pre-selected "most popular"), then $169 per 4 months, with a separate auto-renew consent checkbox forced by its 2022 $62M settlement.
- BetterMe: 15-20 questions, dozens of segment-specific funnels (men, older users, beginners), an avatar recap ("Goal 165 lb, Level intermediate") above three plan cards with weekly cost on each, "most popular" highlighted, before/after, testimonials, press logos, countdown; web is 4 weeks for $38.95, no trial; app store is $19.99/month with a 7-day trial. Price is not shown until the end of the quiz.
- Wallet-first checkout: up to +20% (FunnelFox). Blinkist's trial timeline: +23% trial starts, −55% complaints. 2024 onward the category moved from paid trials to intro-discount plus a three-option paywall.

---

## Synthesis: patterns that appear across most of these winners

1. **The ad lands on a commitment step, not a brochure.** MadMuscles, Muscle Booster, BetterMe, Noom, Built With Science and V Shred all send paid clicks to a quiz whose first screen is the landing page; Kinobody and Fit Father put a quiz or a goal-select opt-in ahead of the pitch. BWS tested quiz vs. store and the quiz "won decisively." The only long-form-first pages are the classic info-product sellers (Athlean-X, Nalewanyj), who are not the volume buyers.

2. **Screen one is a segment split, and the segment carries through.** Gender first (MadMuscles, BetterMe), then body type "Lean / Average / Chubby" or ecto/meso/endo (V Shred), then goal. The segment names the results page (V Shred `male-gr`, `male-sf`) and changes the imagery. MadMuscles goes further: every ad theme (tai chi, military) has its own entry URL so the page continues the ad.

3. **The pitch page opens with "your plan is ready" and a personal recap.** MadMuscles: "Your personalized plan is ready!" plus "Personal summary based on your answers." BetterMe: avatar with your goal weight and level. V Shred: a per-segment video titled to YOUR body type. The prospect's own numbers sit above the offer.

4. **Founder on camera, credentialed in one line, doing the persuading before the form.** V Shred: "Professional Fitness Model, Certified Personal Trainer, Best-Selling Author," a ~5-minute "3 crucial fixes" video, autoplay muted with "Click to unmute." Fit Father: doctor + bodybuilder + the father-died-at-42 story on a video-letter page. Kinobody and Athlean-X sell on the founder's physique and title. The app funnels (MadMuscles, BetterMe, Noom) put the founder-less video in the AD and run no VSL on the page; the personal-brand funnels put the VSL on the page. Nobody puts video on the checkout itself.

5. **Three plan cards, price per day or week, the long plan pre-selected with a savings badge.** MadMuscles ($0.99 / $0.50 / $0.28 per day, 12-week pre-selected, "63% off"), BetterMe (weekly cost on all three, "most popular"), Muscle Booster ("Best value, save 62%"). The BWS exception (annual only, plus a day-by-day trial timeline) was their single biggest lift. One-time sellers use a value stack instead ("over $1,400 in value for just $57").

6. **Email, then card, then the account.** MadMuscles, BetterMe, Noom and Muscle Booster all collect email on the step before the paywall, take the card, and create the login afterwards. The lone exception, V Shred's 13-field form with "Create password," is the one that draws BBB complaints.

7. **One bright button, repeated, in imperative first person.** "GET MY PLAN" (MadMuscles, BetterMe), "START MY 14-DAY TRIAL" (Noom), "PLACE ORDER" (V Shred), "Join Funk's Over 40 Alpha For $1" as the page title itself. Orange/red on dark or white; a single path with no navigation.

8. **A guarantee sits directly under the button, in body-size type.** V Shred 30-day "Unconditional" plus "100% MONEY BACK"; Kinobody 60-day "Transform or It's Free"; Fit Father "Ironclad 100% Satisfaction," 30 days; Nalewanyj 60-day "no questions asked"; Athlean-X's 90-day "X-TRA MILE" support promise.

9. **Proof is stacked below the offer in a fixed order: before/after photos, a big count, a review score, press logos, FAQ.** "Over 70,000 men enrolled" (Kinobody), "over 52,561 men" (Fit Father), "4.5/5 from 62k reviews" (MadMuscles), Forbes/WSJ logos and a countdown (BetterMe), then roughly two dozen screens of testimonials and FAQ (MadMuscles).

10. **Over-40 players add three things the general funnels lack:** the age in the headline ("FOR MEN 40+"), a credential the buyer's doctor would respect (naturopathic doctor, physical therapist) and a family-mission story, and a low first ask ($1 for 30 days, a free meal plan) before the $147 or $29/month.

11. **The ad and the page are built as a matched pair and iterated the same way:** both aspect ratios per creative, 5-10 hook variants per script, hundreds of landing-page variants (MadMuscles 493, Noom 365 tests/year), kill at ~$5k, scale winners.

## Three things the winners avoid

1. **No password, address or phone before the card.** The app funnels take the account after payment; the one brand that asks for thirteen fields first (V Shred) is the one with the checkout complaints.

2. **No price before the quiz, and no exits.** BetterMe and Noom show the price only after 15-113 screens; homepages are stripped to one CTA; there is no navigation, no "learn more," no second offer on the way to the paywall.

3. **No unproven mechanism as the pitch; also, increasingly, no tricks.** The Mike Chang "Afterburn" mechanism VSL is a dead format; today's pages sell personalization ("your plan," "your body type") rather than a secret. And the devices that FTC and class actions named are now liabilities, not tactics: resetting countdowns and discount wheels (MadMuscles ¶139), renewal terms in the smallest type below the fold (¶141), strike-through prices never charged (Goldman v. V Shred), un-confirmed upsells (¶¶144-147), invented review scores. Noom's court-ordered separate consent checkbox and BWS's trial timeline are what compliant versions of the same page look like.

### Implications for the five Abs By AI mockups (one line each, from the evidence)

Land the ad on the photo upload or a 3-5 screen segment split, not on a brochure; open the pitch with the visitor's own analysis numbers under "Your plan is ready"; put Dan's founder video above the offer, autoplay muted with a click-to-unmute (V Shred pattern) rather than on the cart; show two plan cards with per-month math, the trial timeline instead of a timer (BWS/Blinkist), renewal terms above the button; stack before/after, a real count, and a real guarantee under the button; put "40" and Dan's credential in the headline for the over-40 variant; and keep the compliance list above as a hard filter, since MadMuscles' parent was halted in June 2026 for exactly the devices a naive copy would reproduce.

### Files used
- `/home/user/abs-by-ai/.claude/skills/ad-edit/reference/AD_STUDY.md` (V Shred and MadMuscles ad measurements)
- `/home/user/abs-by-ai/.claude/skills/make-ad/SKILL.md` (MadMuscles VidTao spend and theme data)
- `/home/user/abs-by-ai/Docs/WEB_CART.md`, `/home/user/abs-by-ai/Docs/VSL_LANDING.md`, `/home/user/abs-by-ai/Handoffs/handoff-20260910-web-pay-first-cart.md`
- Cart Teardown artifact: https://claude.ai/artifact/MevY5JFc7FTEAikSbQhreV

### Sources (search-result summaries; pages themselves were not fetchable from this session)
- https://web2appworld.com/breakdowns/madmuscles/
- https://blog.funneloftheweek.com/p/the-biggest-quiz-funnel-of-2025-full-breakdown
- https://goodmenproject.com/health/mad-muscles-app-review-honest-look-at-features-and-subscription/
- https://wudang.academy/blog/madmuscles-exposed
- https://www.ftc.gov/news-events/news/press-releases/2026/06/ftc-sues-stop-sprawling-enterprise-operating-unlawful-subscription-schemes
- https://www.ftc.gov/system/files/ftc_gov/pdf/Growthmind-Wisey-Complaint.pdf
- https://techcrunch.com/2026/06/17/ftc-lawsuit-reveals-how-subscription-scam-networks-evade-app-store-enforcement/
- https://sigmalawgroup.com/blog/2026-07-07-ftc-genesis-subscription/
- https://www.consumerfinancemonitor.com/2026/07/01/ftc-takes-action-to-halt-allegedly-deceptive-subscription-schemes/
- https://outgrow.co/blog/vshred-quiz-funnel-case-study
- https://le.vshred.com/sp/quiz/body-type-quiz and the `/sp/survey/*` results pages
- https://vshred.com/blog/body-type-quiz-advertorial-1-celebrity-trainer-v3/
- https://topclassactions.com/lawsuit-settlements/lawsuit-news/class-action-alleges-v-shreds-supposed-deals-were-just-regular-prices/
- https://www.classaction.org/news/4m-v-shred-settlement-ends-class-action-lawsuit-over-alleged-online-video-privacy-violations
- https://kinobody.com/pages/masterclass, https://kinobody.com/pages/movie-star-stack, https://go.kinobody.com/faq/, https://noobgains.com/kinobody/physique-quiz/
- https://athleanx.com/ax1, https://athleanx.com/ax-2, https://athleanx.com/reviews-and-testimonials/fit-over-40
- https://www.revenuecat.com/blog/growth/ethan-ethier-build-with-science-sub-club-podcast-2026
- https://builtwithscience-support.zendesk.com/hc/en-us/articles/43010821429403
- https://www.fitfatherproject.com/ff30x-letter-video/, https://ff30x.fitfatherproject.com/, https://store.fitfatherproject.com/products/fit-father-30x-program-special
- https://over40alpha.com/, https://www.over40alpha.com/o4a-pricing-options, https://www.over40alpha.com/o4a-7-day-trial
- https://www.seannal.com/blueprint-giveaway.php, https://jeffnippard.com/collections/training-programs
- https://musclebooster.welltech.com/is-musclebooster-free/, https://dr-muscle.com/muscle-booster-workout-app-review/
- https://www.revenuecat.com/blog/growth/web-to-app-onboarding-funnel (Noom), https://medium.com/noom-engineering/the-growth-machine-how-noom-runs-365-landing-page-experiments-per-year-1e098ea33354
- https://blog.funnelfox.com/web-funnels-insights-and-trends/, https://adapty.io/blog/high-performing-paywall-2026/, https://www.rocketshiphq.com/paywall-optimization-fitness-apps/
- https://physicalliving.com/my-unrestrained-review-of-mike-changs-six-pack-shortcuts-program/

---

# REPORT 03: 03-womens-fitness-and-glp1-quiz-funnels

# Women's fitness and weight-loss app funnels: what the biggest paid-traffic advertisers run (2025-2026)

## Read this first: how the research was done and what it could not do

Two hard limits shaped this report. First, every direct page fetch (betterme.world, noom.com, hims.com, ftc.gov, revenuecat.com, funnelfox, techcrunch, paywallscreens, adapty, archive.org, reddit, youtube) was refused by the organization's egress proxy with a policy 403; only github.com is reachable from this session. Second, the session's web-search budget (200 calls) ran out during the final batch. So everything below comes from search-engine summaries of teardown articles, review sites, legal analyses and the advertisers' own pages, not from my own walk through a live funnel. Where a source quotes real copy I pass the quote on and name the source. Where I only have a paraphrase I say so. Where nothing reliable surfaced I write "could not verify". Treat the element orders as best-available reconstructions, not screenshots. If Dan wants the exact live screens, one phone session walking quiz.betterme.world and noom.com would confirm or correct this in twenty minutes.

## 1. BetterMe (betterme.world, quiz.betterme.world)

**Sources:** FunnelFox quiz-funnel guide and "311 analyzed funnels" trend report; ScreensDesign BetterMe showcase; Nutrola pricing and free-vs-paid articles (2026); Medical News Today tester review; Garage Gym Reviews (2026); Forbes Health review; LeadsHook "9 Quiz Funnel Examples"; Unstar, Trustpilot, reviews.io complaint summaries; betterme.world/en/money-back-policy; BetterMe wall-pilates article pages.

**Entry point / above the fold.** BetterMe's paid traffic lands on themed quiz landers, not the homepage. FunnelFox describes the company as running "hundreds of quiz funnels across themes like pilates, yoga, and mental wellness," with the quiz as "the first touchpoint in most of their web flows, from calisthenics to mental health to meal planning." Real copy on the wall-pilates landers, per BetterMe's own pages: "Take a 1-min quiz to get a Wall Pilates Plan" and "Take the quiz to get Your Wall Pilates Plan." The first quiz screen is a gender / age-range picker (Medical News Today: "age range, health goal (like lose weight), physical build (out of four choices) and dream body type (four choices)"). Hero imagery on the themed landers is an illustrated or photographed woman of the target age; exact hero headline for the main quiz.betterme.world root could not verify (page title is simply "BetterMe Plan").

**Quiz flow (reconstructed order).** Gender and age range → goal (lose weight / improve well-being / build muscle) → current body type (4 silhouettes) → dream / target body (4 silhouettes) → focus areas on the body → fitness level and activity → "experience with calisthenics" on that variant → work schedule → sleep schedule → water intake → eating habits (eating times, cravings, diet preferences) → "whether specific events have led to weight gain in the last few years" → height, weight, target weight → name and email. Nutrola counts "15-20 questions"; Garage Gym Reviews and LeadsHook both complain it feels "like filling out a form at a doctor's office," which tells you how thorough it is. The women's flows insert motivational interstitials between question blocks (FunnelFox calls these "micro-rewards": "examples, reassurance, social proof, and mini-insights to keep the pace steady").

**Predicted-results screen.** Every source agrees a personalized projection exists (Nutrola: "The specific date based on '58,000 similar members' creates concrete hope rather than vague promises. This isn't just 'results in 4-6 weeks', it's a personalized timeline that feels scientifically calculated"). The exact on-screen headline and chart styling could not verify from the sources available.

**Email capture.** Medical News Today: after the last section "users are asked to input their name and email so they can receive a customized plan based on their answers directly in their inbox." So the email is framed as delivery of the plan, and it sits after the projection and before the price.

**"Your plan is ready" / paywall page (element order, reconstructed).**
1. Headline that the personal plan is ready, followed by a short summary of the plan (ScreensDesign: "the plan summary creates desire").
2. Countdown timer. Nutrola / MNT describe "a countdown timer ('this price expires in 15:00 minutes')" and note "if you close the app and reopen it, the timer resets."
3. Plan cards: 1-week, 4-week, 12-week, with a crossed-out "original" price and a per-day figure (ScreensDesign: "price broken down by week to appear more affordable"; a complaint quoted on Unstar: checkout shows ".30 a day" while the charge is $25.99/month). A "popular" badge and a pre-selected card are standard in this family of funnels (verified on sibling MadMuscles, see section 7; BetterMe specifically could not verify).
4. "Language suggesting this price was calculated specifically for you" (Nutrola).
5. Member before/after photos and testimonials: reported by reviewers as present; exact copy could not verify.
6. 30-day money-back guarantee block. Real terms from betterme.world/en/money-back-policy: refund only for web purchases "where the money-back option was presented during checkout," claimed within 30 days, and only if the user "follow[ed] the program for at least 7 days within the first 30 days" and "can demonstrate that you have followed the program."
7. Post-purchase one-time upsells: "a Sugar-Free Challenge and a Flat Belly Challenge" (ScreensDesign).

**Pricing.** Web prices are higher than App Store prices: "on the website the 4-week workout plan is $38.95 without a free trial, but in the App Store it's only $19.99 with a free trial" (Garage Gym Reviews). Nutrola: "$19.99 to $49.99 per month in 2026, depending on which 'personalized' plan you are shown, with different users seeing different prices." Plans "from a one-week trial to a 12-week plan, with costs between $17.77 and $94.85." Holiday intro offers like "first month $0.99" appear seasonally.

**Compliance handling.** A BBB-style pattern of complaints: "a difficult cancellation flow, a cheap trial that renews into a much more expensive subscription, a 30-day money-back guarantee people say they can never actually claim" (Unstar). The timer is admitted-artificial by every reviewer who tested it. This is the exact playbook the FTC just sued BetterMe's Ukrainian peer (Genesis Tech / MadMuscles) over, so copy the structure, not the tactics.

**Mobile.** Single column, one question per screen, big tappable answer tiles with illustrations, progress bar at top. Sticky CTA on the paywall could not verify.

## 2. Noom (noom.com)

**Sources:** RevenueCat "Inside Noom's Web-to-App Onboarding Funnel" (113 screens); Growthwaves "The 113-screen onboarding that doesn't feel long"; Retention.blog "The Longest Onboarding Ever"; Zain Manji "14 Product Lessons From Noom's Online Quiz"; Paddle "Fix That Funnel" Noom episode (Andrey Shakhtin); Growth Models "How Noom grew to ~$500MM going AGAINST common marketing advice" (Feb 2026); Noom engineering blog "365 landing page experiments per year"; The Behavioral Scientist critique; Justinmind UX case study; Noom support FAQs; PrettySweet, Nutrola, BetterCare pricing pages; Winston & Strawn / Hunton on the $62M settlement.

**Above the fold.** Growth Models: "Noom's minimalist home page pushes readers to start the evaluation, that's the entirety of the page," abiding by "one page, one purpose." Justinmind quotes the hero as "Lose weight by changing your mind, not just your diet" with a "warm, optimistic hero." Ads promise users will "lose the weight for good" via a "proven psychology-based approach" (Vice). The CTA is a "Take the quiz" style button; no pricing, no navigation.

**Quiz flow.** RevenueCat: "up to 113 screens and takes 10-15 minutes." Paddle's episode counts "120 to 140." Content, in order as described: demographic basics (gender, height, weight, goal weight "up to 40 pounds," target timing) → an early goal-date projection → lifestyle and habits → "health history, behavioral patterns, and emotional relationship with food" → food questions that "double as education" (introducing the green/yellow/red system and calorie density; "there are no 'bad foods'") → objection-handling screens ("Noom answers objections like common hesitations before users even reach the paywall") → loading screens "as teaching moments" with progress bars per section ("demographic profile, weight loss goals, and eating habits") → refer-a-friend / accountability buddy screen → email → paywall.

**Projection screen.** Zain Manji: "Noom delivers a results screen with your goal date, your event marker, and a realistic projection... every few screens, Noom shows an updated projection of when you'll hit your goal weight." He stresses "Noom doesn't overpromise; if your event is in two months, they don't suggest you'll magically hit your ultimate goal by then." Fortune: the plan "includes the predicted date of when you'll reach your goal weight." Exact on-screen sentence could not verify.

**Paywall page.** Growthwaves quotes the headline: "Your personalized health plan is ready," and notes it references "the specific goal weight the user typed earlier." Retention.blog: "With a price of $100 per 2 months, Noom uses a long paywall to include all the reassurances you need to feel comfortable." Pricing device: a pay-what-you-want trial. Real copy per The Behavioral Scientist: "pay what you want, but think of our poor staff who are helping you. At least help them stay fed and sheltered," with an oddly specific suggested minimum (£14.41 in the UK). PrettySweet: trial "7 or 14 days for as little as $0.50," with options "$0.50, $3, $10, or $18," and Noom "states it costs them approximately $10 to offer a 7-day trial." After trial: "$59-70 per month" (Nutrola), hard paywall, no free tier. Urgency copy reported: "Your personalized plan expires in 24 hours" and "Special pricing available now." Money-back guarantee: could not verify one exists on the web funnel. Testimonials: present per Retention.blog ("all the reassurances"); wording could not verify.

**Compliance.** Noom paid $62M ($56M cash + $6M credits) in the Mahood class action over "risk-free" trials that auto-renewed into months of charges with a hard cancellation path. The settlement requires "a separate action (e.g., check box or digital signature) to accept auto-renewal" and an in-account cancel button. That is the floor any new funnel should build to.

**Mobile.** One question per screen, progress bar, conversational copy, generous white space, no site nav. Sticky CTA: could not verify.

## 3. Welltech family: WalkFit, Yoga-Go, FitCoach, Muscle Booster

**Sources:** walkfit.welltech.com "Is Walkfit free"; paywallscreens WalkFit listing; Cybernews, TechScoopNow, Wellfizz, Alibaba wellness guides; Trustpilot / PissedConsumer / BBB summaries for Yoga-Go; Dr Muscle and Fitness Drum Muscle Booster reviews; web-faq.musclebooster.welltech.com.

Same shape as BetterMe, shorter quiz. Muscle Booster (the men's product) opens with "a 10-minute questionnaire that asks questions building anticipation for a personalized program, but once you complete this assessment, it's paywall time. You can't even peek at what you're getting unless you pay upfront." Yoga-Go "shows you a personalized offer at the end of its onboarding quiz, and that price varies by promotion, plan length, platform and region. A discounted first-month rate is offered to new users in most signup flows." WalkFit: "$29.99 monthly, annual ~$8.33/month ($79.99-$99.99)," first month discounted, "New Year or spring reset" promos. Muscle Booster: "$9.99 per week to $59.99 per year." Every sister app has the discounted first period, three plan cards, per-day or per-week framing, and a hard paywall. Compliance: the BBB "issued a public alert about a pattern of unauthorized charges, unclear terms, and unresolved cancellation issues, with more than 1,000 complaints" against Welltech. Exact landing hero copy, timer presence, guarantee and email placement: could not verify per app.

## 4. Simple (simple.life)

**Sources:** ScreensDesign "Simple: AI Weight Loss Coach" breakdown; help.simple.life subscription page; Nutriscan, Nutrola, Fortune reviews.

"Goal-first quizzes with visual personalization." The onboarding "is incredibly thorough," then "after building a personalized plan, the user is presented with a paywall to unlock it, with the offer highlighting a 50% discount and breaking down the price per week." Pricing: Pro $14.99/month, Premium $29.99/month; 3-month ~$9.99/month; annual under $5/month; "different users often see different prices for the same subscription length," and a standing web promo code TOP70 exists in the help center (a permanent "discount" is a TINA red flag, see section 9). Hero copy, timer, guarantee: could not verify.

## 5. Sweat, Ladder, Fit Body, FitOn, Alo Moves (the trainer-brand model)

These are the important counter-examples: proven, large, and they do NOT run the 100-screen quiz-to-discount funnel. They run a short quiz or none, a straight 7-day free trial, and card-required or card-free signup.

- **Sweat** (join.sweat.com): page title "Join Sweat | Start your FREE 7-day trial today!"; body copy: "work out anywhere, anytime... learn from leading trainers like Kayla Itsines and join the world's most powerful female fitness community." Plan cards: "Monthly plan: Auto-renews at $24.99 per month until cancelled. Annual plan: Auto-renews at $134.99 per year until cancelled." Trial terms in plain sight: "Pay nothing today. You will be charged after the trial ends unless cancelled prior." A Google Ads variant lander says "$19.99 monthly subscription with a 7 day free trial." Onboarding quiz "takes less than a minute" and only picks a program.
- **Ladder** (joinladder.com): site title "Your Daily Workout Plan"; nav CTA "Find your plan"; a /quiz page "Find Your Perfect Workout Plan"; TikTok lander headline "Get stronger and workout more, without planning workouts." Offer: "a 7 day, completely free test drive and will not ask for a credit card to start a trial." Quiz asks demographics, goals, equipment, then matches a coach/team.
- **Fit Body (Anna Victoria):** "The first 7 days of Fit Body with Anna Victoria is free no matter which plan you choose"; 1-, 3-, 12-month plans; signup at fitbodyapp.com. No quiz lander could be verified.
- **FitOn:** freemium, no trial gate; Pro "$29.99/year," but Truth in Advertising documented it as a "never-ending sale": "$29.99 is the regular price... despite FitOn claiming this price represents a 70% discount from a $99.99 regular price," and "neither has [changed]." TINA's line: "If it's always a sale, it's never a sale."
- **Alo Moves:** was "$12.99 monthly or $129.99 annually... with a 14-day free trial"; relaunched Dec 2025 as Alo Wellness Club, free with the Alo Access loyalty program. Not a paid-funnel model any more.

## 6. WeightWatchers, Hims / Hers, Ro, Found (the GLP-1 spenders)

- **WeightWatchers** (weightwatchers.com/us/home): quiz-first. Homepage copy: "Take our 5-minute quiz to find the right path for you, then sign up for your membership." Brand line: "We are not your mother's Weight Watchers." The Med+ path adds a BMI and contraindication intake before a clinician visit. Promo framing: "$10 a month for 10 months and the first month is FREE with code RESULTS10." No timer reported.
- **Hims** (hims.com/weight-loss): page title/H1 "Weight Loss Care for Men, Built to Last." CTA reported as "See if I'm eligible." Page pillars: GLP-1 options, "a personal plan," "ongoing care from day 1." Intake: "questions about your location, age, weight loss goals, lifestyle habits, and medical history," then provider review. Pricing framing: "$39 for the first month, then auto-renews at $149/month," medication separate. Hers mirrors it word for word: "Weight Loss Care for Women, Built to Last," a "2-minute eligibility assessment to see what your personalized plan looks like," a free smart scale "($55 value)." Reviewers criticise that "the advertised 'from $149/mo' is the medication alone... so the real cost starts at $298/mo."
- **Ro** (ro.co/weight-loss): "Answer a few questions about your health and goals, all online, no in-person doctor's office visit necessary. You'll find out if you're eligible within 2 days." Pricing: "$39 for the first month, then $149/month... or as low as $74/month prepaid annually, plus medication." A dated, real deadline is used for urgency: "Limited-time offer valid for 2.5 mg and 5.5 mg. Sign up by Dec 31, 2026 to qualify." Reviewers found "some live Ro pages still showing $99 first-month language while the current public pricing page shows $39" (a substantiation risk of its own).
- **Found** (joinfound.com): H1 "Weight Care from Found. Achievable and maintainable weight loss with individualized, medically-guided programs that fit your life." CTA: "Take the quiz to see if it's right for you." Price line in the hero: "Plans from $99/mo with insurance or $169/mo cash, medication included on compounded plans." Quiz is a "3 min eligibility quiz" that returns "a personalized price tailored to your needs and insurance coverage."

Pattern across all four: eligibility quiz as the hook ("see if you qualify" beats "buy"), a first-month price anchor, plain auto-renew disclosure next to the price, and no countdown timers.

## 7. The men's comparator: MadMuscles (AmoMedia / Genesis Tech)

**Sources:** Web2App World MadMuscles breakdown (Jan 2026 data); ScreensDesign; Appllama; support.madmuscles.com; REVERA, Davis+Gilbert, Consumer Finance Monitor, Regulatory Oversight, Kyiv Independent on the FTC case.

Worth including because it is the highest-spending fitness funnel on YouTube ("$29.4M/month on YouTube ads alone... top single ad has burned $14.2M lifetime"; traffic "8.1M to 17.4M (+116%) in January 2026"). Quiz: 48 screens, "gender-split funnels: male and female variants of the same quiz with different imagery and body-type options," body type "slim, average, heavy," goal "gain muscle mass, lose weight or get shredded," nine captured variables. Paywall, exact: "1-Week Trial at $6.93 ($0.99/day) renewing at $39.99/month, 4-Week Plan at $15.19 ($0.50/day, 62% off $39.99) marked 'Popular', 12-Week Plan at $25.99 ($0.28/day, 63% off $69.99) renewing at $69.99/3 months. The 12-week plan is pre-selected." Above those cards, per the FTC complaint exhibits: "countdown timers, claimed flash discounts, and banners such as '1,103 people bought this in the last hour' stacked above the real pricing terms, crowding the recurring-charge disclosure further down the page," with "auto-renewal terms in small, low-contrast text below the fold."

## 8. Benchmarks (use with care; most are vendor-published)

- FunnelFox State of Web2App 2026: "a typical web2app funnel sees around 3% conversion from session start to purchase, with roughly 13% of sessions reaching the paywall"; "56-57% of web subscription revenue is generated without any trial"; "three pricing options plus an introductory offer is the market default"; median refund request lands "1.6 days" after purchase; blended median web LTV "~$67 by month 12"; annual plan "~$69 LTV" locked at month 1; web2app "2x higher conversion rates vs. in-app payments, 1.5x LTV"; "82% of top-grossing apps now route subscriptions outside the App Store"; "Health & Fitness (largest volume)."
- Adapty 2026: Health & Fitness "trial-to-paid 35.0%" (another Adapty cut says 62% median for H&F vs 53% overall; the two figures use different cohorts, so quote the lower); "onboarding paywalls with trials produce the highest install-to-paid at 1.78%"; "Health & Fitness is the only category where annual plans dominate (60.6%)"; paywalls shown after a "value moment" get "trial start rates 2.1x higher" than immediate hard paywalls.
- Generic quiz benchmarks (Interact, Wisefunnel, Email List Validation, Outgrow): quiz completion "35% to 42%" average, "50% or higher" for the best; lead conversion of starters "40.1%"; email capture "58-63%" for multiple-choice quizzes with an immediate reward, up to ~70% for personality-style results; asking for email only (no name) beats name + email by "12-18 percentage points"; healthy start rate "20-40%."
- Noom specifically: "15% increase in quiz completions" in 2024 (Growth Models); Noom runs "365 landing page experiments per year" (Noom engineering blog). App-specific paywall conversion for BetterMe, Noom or Welltech: could not verify (Web2App World explicitly says Noom "detailed paywall pricing data is not yet available").

## 9. Synthesis: what the winners share

1. **The ad lands on a quiz, never on a brochure.** Noom's homepage is "one page, one purpose." BetterMe and MadMuscles land straight on the gender picker. WW, Hims, Ro and Found all lead with "take the quiz / see if you're eligible." Nobody sells on the first screen.
2. **Personalization is proven on the way, not claimed at the end.** Noom teaches its method inside the questions; FunnelFox's "micro-rewards" (mini-insights, reassurance, social proof between question blocks) are how 40 to 113 screens "don't feel long."
3. **A dated projection before the price.** Noom's goal-date chart (with an "event marker") and BetterMe's "58,000 similar members" date do the selling. The credible version is deliberately modest (Manji: Noom "doesn't overpromise").
4. **Email is framed as delivery of the plan** ("enter your email so we can send your plan"), placed after the projection and before the price. Email-only fields convert better than name + email.
5. **A processing / "building your plan" screen** with section-by-section progress bars sits between the last question and the reveal.
6. **The paywall headline is the plan, not the product:** "Your personalized health plan is ready" with the user's own goal weight echoed back.
7. **Three plan cards, one pre-selected, per-day or per-week framing, an intro discount on period one.** FunnelFox: this is now "the market default," and intro offers have largely replaced paid trials.
8. **Risk reversal beside urgency:** "timers and discounts combined with money-back guarantees and clear billing terms"; a trust block (ratings, member counts, security badges) "right before payment."
9. **Post-purchase one-click upsells** (BetterMe's challenges) and an in-funnel refer-a-friend step (Noom).
10. **Mobile-first construction:** one question per screen, big illustrated answer tiles, progress bar, no nav, single column. Sticky CTAs are recommended by FunnelFox ("above the fold, sticky, or bottom") but I could not verify which of these apps use one.

## 10. What transfers to men 35-55 and what does not

**Transfers directly.** The quiz-first landing; a short-to-medium quiz (MadMuscles proves 48 screens works on men; V Shred's five-field body-type quiz proves five works too); the dated projection screen (Abs By AI already computes body fat %, fat to lose and goal weight, which is the exact raw material Noom and BetterMe turn into a date); the "your plan is ready" reveal that echoes the user's own numbers; three plan cards with per-day framing; risk reversal next to the price; eligibility-style framing borrowed from Hims and Ro ("see if you're a candidate" reads as a clinical gate, which suits an analysis-led product); Hims' exact headline grammar ("Weight Loss Care for Men, Built to Last") is the only large-scale copy in this set written to this audience and it is plain, unhyped, and durable.

**Adjust for men.** Cut the emotional-relationship-with-food block; men's funnels (MadMuscles, Muscle Booster, V Shred) ask body type, goal, equipment, time budget and frequency, then move on. Use silhouettes / body-type pickers and target-body pickers (present in every men's flow) rather than mood and self-image questions. V Shred's post-quiz VSL is the closest analogue to Dan's single-VSL plan: "the post-quiz video explicitly states the customers' challenges and goals" with gender-matched imagery.

**Women-specific, leave behind.** "Somatic," "wall pilates," "28-day challenge" theme landers; community-of-women positioning (Sweat's "world's most powerful female fitness community"); the very long behavioural-psychology quiz; reciprocity gimmicks like Noom's "think of our poor staff" pay-what-you-want trial; refer-a-friend mid-funnel.

## 11. Elements that are risky under FTC and Google Ads rules

- **Countdown timers that reset or never end.** BetterMe's reviewers confirm the timer resets on reload; the FTC's June 2026 Genesis Tech / MadMuscles complaint attaches these as exhibits; Google's misrepresentation policy names "false sense of urgency," and its crawlers "detect timers that reset, stock counts that never change, and purchase notifications that cycle through fake names," a top trigger for Unacceptable Business Practices suspensions. Ro's approach (a real "Sign up by Dec 31, 2026" date) is the compliant version.
- **Fake social-proof banners** ("1,103 people bought this in the last hour"): named in the FTC complaint.
- **Perpetual "discounts" and crossed-out prices** that were never charged: FitOn's TINA case; FTC rule that a former price must have been "offered to the public on a regular basis for a reasonably substantial period of time." Simple's standing TOP70 code has the same exposure.
- **Auto-renewal terms below the fold or in low-contrast text, "free" or "one-time payment" dominating the screen, hard cancellation.** ROSCA (still in force after the Eighth Circuit vacated the Click-to-Cancel rule on July 8, 2025) requires clear and conspicuous disclosure of all material terms, express informed consent, and a "simple" cancel method; state auto-renewal laws add checkbox and cancel-button requirements; the Noom settlement shows the remedy (separate consent action, cancel button in the account).
- **Fake, AI-generated or misattributed reviews and testimonials.** FTC Consumer Reviews and Testimonials Rule, effective Oct 21, 2024, civil penalties of nearly $52,000 per violation; AI-generated reviews are explicitly covered. Since Abs By AI's core output is an AI-generated image of the user, any testimonial imagery must be real members with real permission, and the AI image must be labelled as a projection, never as a result.
- **Before/after images.** Google Ads' before-and-after policy blocks comparison photos for weight-loss products even when genuine; Google's Health in Personalized Advertising policy bars remarketing on weight loss and any "negative body-image" or shaming creative. FTC Health Products Compliance Guidance: "Results not typical" does not cure a dramatic testimonial; the ad must state what a typical user actually gets, and the claim needs competent scientific evidence. This bites hardest on the app's own "you with abs" render if it is shown on the ad landing page as an outcome.
- **Weight-loss "Gut Check" claims** the FTC treats as false on their face: two or more pounds a week for a month without diet or exercise, substantial loss regardless of what you eat, permanent loss after stopping, more than three pounds a week for more than four weeks. The projection screen must stay inside these limits.
- **Hidden total cost.** Hims / Hers' "from $149/mo" that omits the $149 membership is drawing the same kind of criticism; show the full first-charge and renewal amount on the card.

## 12. The FTC action, for the record

On June 2, 2026 the FTC filed suit in the Northern District of California (announced June 17; 2-0 vote) against the Genesis Tech enterprise: 15 corporations and 8 individuals, including the Amomedia entities behind MadMuscles, Harna and Unimeal, plus Wisey, PDF Guru / PDF Master, Lumi and Nebula. Alleged violations: Section 5 of the FTC Act and ROSCA. The court issued a temporary restraining order. The complaint's "common playbook": "lure consumers with a free or low-cost offer, build commitment through quizzes or personalization, obscure auto-renewal terms, impose unexpected recurring charges, and make cancellation difficult." Five products "accounted for nearly a quarter billion dollars in global revenue" from early 2023 to mid-2025. It is a lawsuit, not a settlement; no consent order had been reported in the sources I could reach. The complaint treats quizzes, progress bars and timers as "integral parts of the various allegedly deceptive consumer flows and part of the overall message," which is the point for us: the quiz is fine, the deception around the price is what got sued.

## Sources (all reached through search summaries; none fetched directly)
FunnelFox: blog.funnelfox.com/web-funnels-insights-and-trends/, /quiz-funnel-guide/, /web2app-funnel-patterns-2026/, /web2app-funnel-patterns-2026-part-2/, funnelfox.com/state-of-web2app-2026. RevenueCat: revenuecat.com/blog/growth/web-to-app-onboarding-funnel, /web-to-app-funnel-examples. Growthwaves: growthwaves.io/p/the-113-screen-onboarding-that-doesnt. Retention.blog: retention.blog/p/the-longest-onboarding-ever. Zain Manji: zainmanji.medium.com/14-product-lessons-from-nooms-online-quiz-44512d1cae6a. Paddle: paddle.com/studios/shows/fix-that-funnel/noom-full-interview. Growth Models: growthmodels.co/noom-marketing/. Noom engineering: medium.com/noom-engineering/the-growth-machine-how-noom-runs-365-landing-page-experiments-per-year-1e098ea33354. Behavioral Scientist: thebehavioralscientist.com/articles/noom-product-critique-onboarding. Justinmind Noom UX case study. Web2App World: web2appworld.com/breakdowns/noom/, /breakdowns/madmuscles/. ScreensDesign: screensdesign.com/showcase/betterme-health-coaching, /showcase/simple-weight-loss-coach, /showcase/madmuscles-workouts-diet. Nutrola: nutrola.app/en/blog/betterme-free-vs-paid-what-do-you-actually-get, /how-much-does-betterme-cost-now-2026, /is-noom-free-anymore. Medical News Today betterme-review; garagegymreviews.com/betterme-review; forbes.com/health/weight-loss/betterme-review/; leadshook.com/blog/quiz-funnel-examples/; betterme.world/en/money-back-policy; unstar.app BetterMe reviews; welltech pages (walkfit.welltech.com/is-walkfit-free/, musclebooster.welltech.com, web-faq.musclebooster.welltech.com); cybernews.com/health-tech/walkfit-app-review/; Yoga-Go Trustpilot / PissedConsumer / BBB summaries; help.simple.life subscription plans; join.sweat.com signup pages and sweat.com/signup; joinladder.com, /quiz, /pricing, /tiktok/define; annavictoria.com/faq; truthinadvertising.org/articles/fitons-never-ending-sale/; athletechnews.com Alo Wellness Club; weightwatchers.com/us/home and /us/how-it-works/glp-1-program; hims.com/weight-loss; forhers.com/weight-loss; ro.co/weight-loss/ and /pricing/; joinfound.com; outgrow.co V Shred case study; adapty.io/state-of-in-app-subscriptions/ and health-fitness benchmarks; rocketshiphq.com Adapty summaries; tryinteract.com quiz conversion report 2026; wisefunnel.io, emaillistvalidation.com, outgrow.co benchmarks. Legal: ftc.gov press release 2026/06 "FTC Sues to Stop Sprawling Enterprise Operating Unlawful Subscription Schemes"; techcrunch.com 2026/06/17; revera.legal compliance checklist; dglaw.com and consumerfinancemonitor.com 2026/07/01; regulatoryoversight.com; wittelslaw.com and winston.com on Mahood v. Noom; ftc.gov Consumer Reviews and Testimonials Rule Q&A; alston.com and sidley.com rule summaries; gibsondunn.com and cooley.com on the Eighth Circuit vacatur; ftc.gov Health Products Compliance Guidance and "Gut Check"; support.google.com/adspolicy misrepresentation (6020955), misleading representation (15936666), unacceptable business practices (15938071), health in personalized advertising (16701855); stubgroup.com before-and-after policy glossary; gmccheck.com UBP guide.

---

# REPORT 04: 04-hormozi-and-info-product-vsl-structure

# VSL landing page research: Hormozi and the top info/coaching DR operators (2025-2026)

## Access note (read first)

The network egress proxy in this session blocked every operator site and nearly every secondary source (acquisition.com, skool.com, deangraziosi.com, consulting.com, tonyrobbins.com, vshred.com, clickfunnels.com, unbounce.com, cxl.com, vwo.com, wistia.com, medium, substack, web.archive.org and about 40 others). The WebSearch budget for the session also ran out at 200 calls. What I could read in full: GitHub-hosted primary texts, specifically Hormozi's own 2025 "ACQ Advertising Handbook" and "$100M Playbook: Goated Ads" (full transcriptions in `kobe-shem/advisor-skill`), the "$100M Leads" paid-ads course transcript, his "Productize" scaling-course transcript, a 2025 agency VSL-funnel training transcript (Cameron England) with concrete play-rate and engagement KPIs, and a VSL copywriting reference (`oathdriven/rymac-skills`) that compiles the Benson, Brunson, Hormozi and Sabri Suby beat structures. Everything else comes from search-result summaries. I mark anything I could not open as "could not verify". Nothing below quotes live above-the-fold copy from a page I loaded myself; where I give copy, I say where it came from.

Local grounding: `Docs/VSL_LANDING.md` (the current `/start` page: two hero variants, one-tap upload CTA, three proof pairs, what-you-get tiles, how it works, founder card, trial card, FAQ, sticky mobile CTA; the 90 percent drop is visitors never uploading a photo) and `Handoffs/video-editing/WV-02-vsl-2-start-landing-page-video.md`.

---

## 1. Alex Hormozi

### What his own paid pages look like (from his own 2025 handbooks)

**Skool Games landing page (skool.com/games), as screenshotted in Hormozi's Goated Ads playbook and ACQ Advertising Handbook, 2025.** Above the fold: kicker "~ Alex Hormozi and Skool present ~", headline "The Skool Games", subhead "A fun way to build your own business with other people.", one line of feature copy "Simple instructions, live workshops, community, support, realtime leaderboards, friendly competition, and prizes!", a prize callout "Win 1-day with Hormozi", and one button: "PLAY FOR FREE". A second variant is a Skool group page: header "JOIN THE SKOOL GAMES", "PLAY FOR FREE" button, a banner image of Hormozi, then the group card "Build your business, win prizes, make friends, have fun. Win 1-day with Alex Hormozi." with a stats row "17.6k Members | 669 Online | 8 Admins" and a "JOIN GROUP" button. The click goes straight to a four-field signup (first name, last name, email, password) with "SIGN UP" (desktop) or "SUBMIT!" (mobile). Search summaries add: the page carries a VSL and the community is $100/month after a free trial; top 5 in each of 10 categories win a trip to LA and a one-day mastermind. Live page: could not verify.

**Hormozi's stated rule on paid landing pages ($100M Leads paid-ads course, transcript, verbatim):** "My favorite way to get contact information is a simple landing page. Don't overthink it. There are three landing pages that when I look at all of our companies that we use most commonly, which is headline, sub headline, contact info, submit. Same thing except with an image, same thing with an image and then three bullets. Those are the three most common layouts I use. Pick one of them. Doesn't really matter. We've used them all and all you got to do is test it. And the nice thing is the simpler the landing page, the fewer variables you have to test... You get super high conversion rates." Then: "make sure your landing pages match your ads... if your ad is a certain color and a certain person and uses certain words, make sure the landing page uses the same words and same colors and same person." And the qualification dial: "the more steps you get someone or ask someone to go through, the fewer people will do it, but the more qualified the leads will be... If you get too many leads, then add some qualification steps. If you get too few leads, remove some."

**Where the selling happens (ACQ Advertising Handbook, Skool "Bribe" framework, verbatim):** "It's a killer offer-driven ad up front driving to a page that did the heavy lifting... you can pack it into the ad or shift it to the page. We found shorter, proof-heavy creatives worked best for us. We just needed enough to earn the click, then let the page and video sales letter close." That is the clearest first-hand statement of his 2025 model: short proof-heavy ad, page plus VSL closes.

**"Show what happens next" (Goated Ads, CTA chapter):** he ends ads with an animation of the actual landing page and the signup form "to align expectations and reduce friction when they get to the opt-in page". His CTA formula: what to do, how to do it, when to do it, what they get, what happens next. He tests only 1 to 3 CTAs per shoot ("Start free on the next page", "Grab your 14-day free trial on the next page", "Get started on the next page free"). "Clear > Clever."

**His ad-to-VSL-to-call sequence (ACQ Advertising Handbook, agency ad):** the ad's CTA is literally "click, opt in, watch the video (CTA 1). And if it sounds interesting to you, you can apply and schedule a 15-minute call with my team (CTA 2)", and the handbook generalises it: "Click to opt in, watch a seven-minute demo, then book a 15-minute qualification call." Note the seven-minute length.

### The VSL structure he teaches

From his "Productize" training (verbatim): "very strong and very detailed pain based up right at the beginning of the video... speak specifically to the pain of the avatar and then you go proof, promise, plan... why hasn't this problem been solved yet for this person? What's the main impact if it continues? What's the solution? How does the solution work? What makes our solution better than other people's? And then proof that we have that our solution actually works... you want to weave this all the way through." He uses the VSL to remove the repeated 20 minutes from every sales call and to pre-handle objections ("the video sales letter covered some of these common concerns in the video so that the sales guys had a little bit more of advantage going into the call", 4-hour sales guide).

The 11-step version circulating from his Skool Games VSL breakdown (Skool community posts and videohighlight summary, could not open the originals): Niche call-out, Paint (the pain), Epiphany bridge, Guru (credibility), MVO (most valuable offer), FAQ, Proof, Price anchor, Concern handling, Next steps, Guarantee plus scarcity. His stated weighting: hook plus FAQ plus proof is roughly 80 percent of the VSL's effect; put around 85 percent of effort on the hook; test many hooks (one hook tripled watch time in a test he cites). Length guidance attributed to him in the kraken.media summary: five to seven minutes, ten as the ceiling, "five minutes of video saves thirty minutes of conversation".

### His views on the specific questions asked
- **One page, one CTA:** yes, and his own pages carry a single repeated button. His three layouts have exactly one submit.
- **Text-heavy vs video-heavy:** his lead-gen pages are text-light (headline, subhead, form); the VSL carries the persuasion; secondary sources note his book-launch registration pages are "cluttered, copy-heavy" and that "the goal of a long landing page is simple: at any point, the user can stop and buy" (YouTube teardown titles, could not verify the videos).
- **VSL length:** 5-7 minutes typical, 7-minute demo in his agency funnel, 10 max.
- **Autoplay:** no first-hand statement found. Could not verify.
- **Headline weighting:** "the headline is the first sale... after you've written your headline, you spend $0.80 of your advertising dollar."

### Book funnels
$100M Leads is given away free with a free course "to earn trust", and the ads are literally "WHAT'S YOUR EMAIL? (I want to send you some free stuff)" with the book held up. $100M Money Models (Aug 16, 2025): 10-hour YouTube livestream launch, the CTA reframed from "buy" to "donate 200 books" for $5,998 with a 12-playbook bonus stack, an $18K advisory upsell, affiliate leaderboard, hard deadlines; registration pages used a countdown timer and an explainer video (secondary sources). Order page copy: could not verify.

---

## 2. Other operators

**Russell Brunson / ClickFunnels.** Framework: Hook, Story, Offer; the VSL page is a headline that "makes a big, irresistible promise", the video, then the order form; the Perfect Webinar (45-90 minutes: Big Domino, Three Secrets, the Stack) is the long form. The Epiphany Bridge story (life before, journey and conflict, the aha, framework taught as what and why never how, successes) is his standard credibility reveal. Registration pages use curiosity bullets that "tease without giving away the strategy". Live page copy: could not verify (clickfunnels.com blocked).

**Dan Kennedy / Agora-style text sales letter.** VWO's own article ("Do long-form sales letters still work? Yes") and AWAI hold that the long text letter remains the base format. Agora-style financial VSLs run 30-60 minutes with fear or contrarian hooks and heavy proof. The hybrid finding repeated in several guides: a VSL with a text sales letter or transcript beneath it out-converted either alone (no controlled test located; treat as practitioner consensus). Kennedy's current Magnetic Marketing pages: could not verify.

**Jon Benson (VSL inventor, 2006; wrote the "Truth About Abs" VSL, roughly $40M, abs niche).** The original "ugly VSL" was black text with red words on a white screen, his voice reading it, an auto-playing video and an order button that appeared late (one source says the 42-minute mark). Benson himself says his original had an always-visible button and was not stripped of controls. The 3X formula (from a public YAML of the course): Act 1 Hook, first 20 percent (pattern interrupt or "snap suggestion", promise, open loop, qualify the audience; "hook in the first 10 seconds"); Act 2 Story, middle 60 percent (reluctant hero, problem intensification, breakthrough, solution, proof woven in; "the story is the sale, don't rush"); Act 3 Close, final 20 percent (value stack, price anchored high then revealed, guarantee, bonuses, direct CTA, ethical scarcity; "the close should feel like the natural consequence of the story"). His slide-level rules: credibility inserted mid-problem, never up front; the "critical 500 words" at the open; USP in the first 10 slides. Mike Geary's Truth About Abs page was "long, cluttered" and called out one specific person repeatedly.

**Tony Robbins.** Segmented mini-funnels per goal, a segmentation quiz or Messenger flow first, then personalised content and offers; standing CTAs are the free coaching call, UPW tickets, and free trials; the Own Your Future Challenge (with Graziosi) is a free 5-day live event with a VIP upgrade. Page copy: could not verify (tonyrobbins.com and deangraziosi.com blocked).

**Iman Gadzhi.** 2025 funnels: a $27 to $75 workshop or "3 Day Challenge" front end, opt-in with email and phone, then a VSL whose job is to get a survey filled in "so the content can be customised", WhatsApp group, livestream, and a $2,000 to $12K back end via an audit or application call. His 2024-2025 flow is VSL then survey then call, not VSL then checkout. Pages: could not verify.

**Sam Ovens.** Documented $20M funnel: Facebook ad, opt-in page ("how I get 30-50 high-ticket clients a month", target 20 percent opt-in), value video (webinar or VSL), calendar plus survey, strategy call with a script. His sales page (emaildrips capture) is a long VSL page with price, guarantee and FAQ. Current consulting.com: could not verify.

**Dean Graziosi.** Runs challenge funnels with Robbins (free 5-day event, VIP upgrade, replays) and book funnels. Page copy: could not verify.

**Fitness comparables (what the brief asks us to model).** V Shred: quiz to match a program, then "a page that seems to go on forever" led by Vince Sant talking to camera on pain points ("You've tried, you've failed, it's not your fault"), $47 front end, upsells. MadMuscles (web2appworld breakdown): 38 to 493 landing-page variants, a 47-48 screen quiz starting with gender, all traffic to one domain, 2,335 Facebook ads plus 3,498 YouTube and 3,240 Display ads in Feb 2026; no VSL, the quiz is the persuasion. BetterMe and Noom: quiz first in every web flow, one question per screen, social-proof interstitials, results page, in-funnel payment. A "quiz then custom VSL" hybrid exists in template vendors' descriptions, but I found no evidence that V Shred, MadMuscles, BetterMe or Noom run a VSL at the top of their paid landing page; their VSL-style video (Vince Sant) sits on the post-quiz sales page. Could not verify the live pages.

---

## 3. Published conversion data

- **Click-to-play vs autoplay:** Vmaker A/B on an opt-in page, 41.2 percent conversion click-to-play with a visible thumbnail vs 9.7 percent autoplay (widely cited, original test not opened). Unbounce's expert roundup says do not autoplay to drive conversion. Vidalytics reports the opposite for a sales page: "Smart Autoplay" (muted autoplay with unmute) lifted one customer's conversion by 49 percent in a split test (vendor case study, Brent Messer). Reconcile: click-to-play wins on short opt-in pages; muted autoplay with captions is the VSL-vendor default for long-form sales videos. Sound-on autoplay is blocked by browsers anyway.
- **Play button and thumbnail:** a visible play icon produces up to 100 percent more plays (Wistia, cited second-hand). The 2025 agency VSL training gives KPIs: play rate 15-20 percent cold, 20-30 percent warm; average engagement 30-50 percent; post-video opt-in 5-10 percent; a "clunky YouTube embed" costs 5-10 percent of play rate; use a dynamic (moving) thumbnail; put the VSL at the top of the page above the form ("the VSL should be at the top of the page... look at it as if you're on a phone").
- **Length and engagement:** Wistia 2025 State of Video (14M videos): under 1 minute 50-52 percent engagement, 1-3 minutes 46 percent, 3-5 minutes 45 percent, engagement at a four-year low; steepest drop-off at 10-20 seconds, viewer decision in 5-8 seconds. Practitioner beat table (greenfroglabs, second-hand): a 5-minute VSL loses to about 65-75 percent by the end of the hook and 22-30 percent at the close.
- **Video on landing pages at all:** Vidyard on Unbounce, lightbox video 13 percent vs 6.5 percent (100 percent lift); EyeView 80-86 percent; Dropbox explainer plus 10 percent; a registration page 3.77 to 10.20 percent after adding video. All vendor case studies.
- **Delayed CTA:** Vidalytics ties the button reveal to the video position and claims lifts; a Warrior Forum thread titled "Delayed call to action buttons DO NOT increase conversions" reports the reverse for some testers; the rymac reference says persistent CTA for warm or low-price, reveal-at-offer for cold high-ticket. Net: no public controlled test either way. Could not verify a winner.
- **Captions:** 80 percent of social video watched muted (Meta, cited second-hand); captioned videos 80 percent more likely to be watched to completion (Verizon/Publicis, cited second-hand).
- **Long vs short page, text plus video hybrid, hiding controls:** no controlled public test located. The 2025 agency training explicitly says do not hide scrubbing or playback speed for sophisticated buyers; the 2006-era ugly VSL hid them. Could not verify a test.
- **Mobile:** sticky bottom CTA and "CTA within a thumb scroll of the player" are the repeated recommendations; a vertical VSL only pays off if the page is built vertical-first (Panda Video, summary only).

---

## 4. VSL plus quiz vs VSL then application or checkout

- **VSL then application then call:** Hormozi (acquisition.com workshop and agency offers: opt in, 7-minute VSL, 15-minute qualification call), Sam Ovens (value video, calendar plus survey, call), Iman Gadzhi (VSL, survey, WhatsApp, call), Sabri Suby (VSL above the survey, calendar). This is the high-ticket pattern ($2K plus).
- **VSL then checkout on the same page:** Benson-style info products (Truth About Abs), V Shred's post-quiz sales page, ClickFunnels VSL funnel template (headline, video, order form), Hormozi's Skool Games page (video, "PLAY FOR FREE", 4-field signup, trial).
- **Quiz then sales page (video optional):** MadMuscles, BetterMe, Noom, V Shred. The quiz replaces the VSL as the persuasion engine for sub-$100 monthly subscriptions.
- **Quiz then personalised VSL:** described by funnel-tool vendors; I could not verify any of the named operators running it.

For Abs By AI ($19.99/month, 7-day trial), the proven comparables are the second and third patterns, not the application funnel. The photo upload already functions as the quiz's micro-commitment.

---

## 5. Synthesis: 11 structural rules the evidence supports

1. **Headline, subhead, video, one button above the fold; nothing else competes.** Hormozi's three layouts (headline, subhead, contact, submit; plus image; plus three bullets), Skool Games page, ClickFunnels VSL template. Data: Hormozi's own statement that simpler pages test faster and convert higher; no counter-evidence found.
2. **The VSL sits at the top, above any form, sized for a phone.** 2025 agency VSL training (play rate KPI drops if the form is above the video); MadMuscles and BetterMe are mobile-first by design. Data: the 15-20 percent cold play-rate benchmark is measured with the player at the top.
3. **Ad, headline and video must be congruent: same person, same words, same colours, same claim.** Hormozi ("make sure your landing pages match your ads"), the agency training ("incongruency kills the conversion"). Data: Hormozi's practice of showing the landing page inside the ad; no A/B number.
4. **Click-to-play with a strong thumbnail on short pages; muted captioned autoplay is acceptable for a long VSL.** Vmaker 41.2 vs 9.7 percent (click-to-play), Vidalytics plus 49 percent (muted smart autoplay). Burn captions in either way (80 percent muted viewing).
5. **Show a play icon and a moving or human-face thumbnail.** Wistia (play icon up to 2x plays), agency training (dynamic thumbnail lifts play rate). Data: vendor-reported.
6. **Keep the VSL between 3 and 7 minutes for a low-ticket subscription; 10 is the ceiling.** Hormozi (5-7, 7-minute demo, 10 max), agency training (3-10, its own is 4). Wistia: engagement falls with length and drop-off is steepest in the first 20 seconds, so spend most of the effort on the first 30 seconds (Hormozi: 80 percent of effort on the first five seconds of an ad, 85 percent on the VSL hook).
7. **Open on the specific pain of one named avatar, never with an intro.** Hormozi ("very strong and very detailed pain based up right at the beginning"), Benson (snap suggestion, credibility only mid-problem), Truth About Abs (calls out one person repeatedly), V Shred ("it's not your fault"). Data: problem-first hooks beat claim-first in 9 of 12 cold A/B tests cited by the rymac reference (second-hand).
8. **Sequence inside the video: pain, proof, promise, plan, why it has not been solved, mechanism, why ours is better, proof again, offer, price anchor, guarantee, FAQ, next step.** Hormozi's productize sequence and the 11-step Skool VSL; Benson's 20/60/20; Brunson's Epiphany Bridge for the founder story (Dan at 40). Hormozi's weighting: hook, FAQ and proof are 80 percent of the result.
9. **Below the fold repeat the video's argument in scannable text: proof, what you get (stacked with values), guarantee, FAQ, then the same button again.** Truth About Abs and V Shred (long cluttered pages), Hormozi's "at any point the user can stop and buy" (secondary), Sam Ovens' sales page, the VWO position that long-form still works. Data: no controlled long-vs-short test found; the hybrid claim is practitioner consensus.
10. **One CTA, worded identically everywhere, that names the next step and what happens after it.** Hormozi's CTA formula (what, how, when, what you get, what happens next) and his 1-3 tested variants ("Start free on the next page"). Sticky bottom button on mobile (already on `/start`).
11. **Real risk reversal and real scarcity only; no fake timers on a subscription page.** Hormozi's guarantee taxonomy (unconditional, conditional, anti, implied, service) and "scarcity must be true"; the agency training uses "if this doesn't work you don't pay" inside the CTA. The 7-day free trial is the guarantee; state it in the video and next to the button.

Two rules I could not support with data and would test rather than assume: delayed button reveal (split evidence) and hiding video controls (2006 practice, explicitly rejected by 2025 practitioners).

---

## Sources actually opened
- Hormozi, ACQ Advertising Handbook (2025) and $100M Playbook: Goated Ads, full transcriptions: https://github.com/kobe-shem/advisor-skill (paths `knowledge/alex-hormozi/source-texts/books/acq-advertising-handbook/full-text.md`, `.../100m-goated-ads/full-text.md`)
- Hormozi, $100M Leads course, "Paid Ads Playbook pt I" transcript; "Productize" transcript; "Sell better than 99 percent" transcript (same repo)
- Cameron England, "Mastering VSLs" 2025 training transcript (same repo, `knowledge/cameron-england/...`)
- VSL beat structures reference: https://raw.githubusercontent.com/oathdriven/rymac-skills/main/skills/rymac-vsl-copywriting/references/vsl-beat-structures.md
- Benson 3X formula YAML: https://raw.githubusercontent.com/torriani/agentesIA/main/skills/coreai-copy-shared/frameworks/benson/3x-vsl-formula.yaml
- $100M Offers frameworks: https://github.com/getagentseal/founder-playbook (100m-offers)
- Vmaker autoplay figure via https://github.com/ericmjl/skills (video-script-writing research digest)
- Project docs: `/home/user/abs-by-ai/Docs/VSL_LANDING.md`, `/home/user/abs-by-ai/Handoffs/video-editing/WV-02-vsl-2-start-landing-page-video.md`

## Sources seen only as search summaries (not opened)
kraken.media (Hormozi VSL rules), videohighlight.com/v/MEsSN187wUI, skool.com community posts on the Skool Games VSL, stormy.ai webinar-funnel playbook, startupspells and selfpublishing (Money Models launch), unbounce.com autoplay roundup, vidalytics.com case studies, foundrycro.com 2026 benchmarks, warriorforum delayed-CTA thread, wistia.com 2025 State of Video, vwo.com long-form article, breakthroughmarketingsecrets (death of the ugly VSL), tim.blog (Truth About Abs), nellianestclair and growthmodels (Sam Ovens), funneloftheweek and acquisitionrealm (Gadzhi), web2appworld (MadMuscles), heyflow and leadshook (BetterMe, Noom), honestbrandreviews and nourishedwithnatalie (V Shred), bdow and wildmail (Robbins).

Scratch copies of the downloaded source texts are in `/tmp/claude-0/-home-user-abs-by-ai/7b94d061-983c-5207-bdd8-8a682638a7be/scratchpad/src/` if the parent wants exact quotes pulled.

---

# REPORT 05: 05-youtube-demand-gen-rules-and-benchmarks

# YouTube / Demand Gen landing page research for the Abs By AI VSL page

## Access note (read first)

Every direct page fetch in this session was refused by the network egress proxy: vidtao.com, blog.vidtao.com, inceptly.com, Inceptly's beehiiv newsletter, support.google.com (all policy pages), unbounce.com, wordstream.com, web2appworld.com, funnelfox.com, revenuecat.com, heyflow.com, and roughly 25 other domains. The web search tool worked until its 200-call session budget ran out. So everything below comes from search-engine result summaries of the named pages (the tool returns extracted sentences from indexed pages), plus one first-hand source I could read in full: this project's own Google Ads campaign doc, `/home/user/abs-by-ai/Docs/DGEN_CONVERSION_CAMPAIGN.md`, which records real policy verdicts on our ads.

Where I write "search summary" the wording is what the search tool extracted from that page; I did not see the surrounding page. Where I say "could not verify" I could not get the claim from any source. No quote below is invented; anything paraphrased is marked as such.

---

## 1. VidTao (Inceptly's ad library) and Inceptly (the agency)

**What they publish (confirmed to exist via search index):**
- blog.vidtao.com: "How to Create & Run Successful YouTube Ads in 2025" parts 1 and 2 (`/how-to-run-successful-youtube-ads-in-2025-part-1/` and `-part-2/`), "How to analyze competitor YouTube ads for 2026 DTC success" (`/how-to-spy-on-your-competitors-youtube-ads-in-2025/`), "Top 9 Hook Tactics We Extracted From Today's Top Direct Response YouTube Ads", "The YouTube VSL + TSL Hybrid approach to selling High-Ticket (Without a Sales Team)", "VidTao YouTube VSL Top 10 Leaderboard: October 2022", the "[3 Ad Thursday]" series (a $500k wellness gummies ad, a $300k hearing aid ad, "The Fast Lane to Trust: 3 Ads That Build Instant Belief"), "Ad of the week 3: Health and Wellness Tools", and "YouTube Ad Smart Hooks: 3 Ads That are Scaling Now".
- inceptly.com: "Use this 30-year-old lead framework on YouTube ads to scale" (`/30yo-lead-framework-on-youtube-ads/`), "What did this $250K, 30-minute-long ad teach us about seniors on YouTube" (`/winning-youtube-ad-for-seniors/`), "The YouTube Ad Funnel Blueprint", "You miss VAC? Here's how to recreate it in Demand Gen", monthly Google Ads update recaps (April, mid-May, June 2025), and the newsletter post "#1 Direct Response Mini VSL ad of the Month" at inceptly-agency.beehiiv.com.
- I found no public VidTao "top fitness advertisers 2025" leaderboard in the index. The only leaderboard surfaced is the October 2022 VSL top 10. A 2025 fitness ranking, if it exists, is behind VidTao's login. Could not verify.

**Rules and quotes recovered (search summaries):**

From the VidTao 2025 guide (part 1 / part 2):
- "Your CTA should lead to exactly what you just pitched, as any disconnect hurts trust and conversions."
- "Your ad's first 5 seconds acts as a 'hook' to get viewers to stay past when the 'skip ad' button becomes clickable, while the first 10 seconds acts as an 'ad quality' signal to Google that drives down your CPA."
- The guide is framed around "the 4-part structure every high-converting ad uses", "a great script can beat a slick video", "testing multiple hooks", and "simple CTAs that turn attention into action."

From the VSL + TSL hybrid post (4Patriots generator case):
- "The combination of a short VSL ad and text sales page elements together create a full sales argument like a 45-minute VSL." The stated lesson: "you can sell high-ticket products to cold traffic with zero sales team when you make an effective and complete sales argument." Practitioner case study, one advertiser, no conversion numbers surfaced.

From the competitor-analysis post: VidTao's product lets you "scroll down on an ad highlight to see the ad's landing page" and it "provides a direct link between ads and landing pages, allowing users to evaluate the creative and the funnel together." That is a tool feature, not a rule, but it tells you what Inceptly looks at when they judge a funnel: ad plus page as one unit.

From Inceptly's $250K seniors ad teardown (first seen July 11, 2025, ~$258k spend):
- "The landing page echoed the ad with the same claim stack, 'guaranteed acceptance,' 'no exam,' and a big phone CTA."
- "This wasn't creative genius, it was offer clarity plus friction math delivered like late-night TV."
- Friction removers named: "No medical exam," "right over the phone," and the risk-reversal line "Rates never increase, benefits never decrease, coverage never canceled."
- Structure: a ~60-second dramatized scene "looped for 30 minutes" as one ad.

From Inceptly's lead framework post: the ad's lead type should match Schwartz awareness level; "direct leads (offer and promise) work with highly aware audiences, while indirect leads (story, secret, and proclamation) excel when your audience doesn't yet know they need your solution."

**The "ad is the first 30 seconds of the VSL" rule:** I could not find that exact sentence attributed to VidTao or Inceptly. The closest indexed statements are (a) the Inceptly newsletter noting they "refresh 30 seconds of a proven VSL to unlock significant additional revenue" and (b) a VSL-page structure guide (Verlua / Kewise, not Inceptly) that says "the first 30 seconds mirrors the ad" and lists the page as "a curiosity headline, a strong first 30 seconds, text for skimmers, proof, and a clear CTA. It should still work if someone never finishes the video." Treat the 30-second phrasing as widespread practitioner doctrine, not a verified VidTao quote.

---

## 2. What the biggest health / fitness / supplement YouTube advertisers send traffic to

**MadMuscles (the largest fitness-app YouTube spender, per two independent trackers):**
- Web2App World (`web2appworld.com/breakdowns/madmuscles/`): "MadMuscles runs the most expensive YouTube ad operation of any fitness app... $29.4 million per month, with $195.6 million spent in the trailing 12 months." "Traffic doubled from 8.1M to 17.4M (+116%) in January 2026." "The quiz runs 48 screens in the male variant and 47 screens in the female variant." "The funnel lives at madmuscles.com and currently runs multiple theme variants simultaneously including tai chi walking, military workouts, and military calisthenics, with each theme having its own entry URL, ad creative angle, and gender-specific flow." Also: "tiered paywall, and the top ad that burned $14.2M."
- Funnel of the Week ("The biggest quiz funnel of 2025?"): "MadMuscles is driving 10M+ clicks per month through their 493 unique quiz funnel landing pages. Most of that traffic is from YouTube, with VidTao estimating MadMuscles has spent approximately $10M on YouTube in the past year." "Nearly every ad on YouTube has been AI-generated." "Their top spender launching just one month ago and spending an estimated $1.9M" (Sep/Oct 2025).
- Format verdict: quiz landing page, gender-split, one entry URL per ad angle. Not a VSL page. Data-backed on spend and structure (two trackers agree), no conversion rate published.

**BetterMe:** FunnelFox ("What I Found Reviewing 75,000 BetterMe Ads") and its 311-funnel study: "BetterMe runs multiple funnels tailored to specific audience segments but pointing to the same product... at least 12 highly optimized funnels." "BetterMe uses quiz funnels as the first touchpoint in most of their web flows." Web2App World notes "BetterMe World's YouTube spend is relatively modest compared to competitors like MadMuscles." Format: quiz, persona-specific entry pages.

**Noom:** Lazer / Zain Manji product teardown: "The onboarding quiz (described as the growth engine) consists of 12-15 conversational steps." "They don't force authentication pre-quiz on the web since it's a high friction point and they want to optimize for obtaining emails." "The Noom site has little SEO presence since it's just a landing page, and all the value is behind an auth wall, so they need to rely on ads for traffic." MediaRadar: Noom "recently placed programmatic ads on YouTube" and spent "under $100 million on advertising in digital and national TV in the last year." Format: quiz. Noom's quiz is the pattern the others copied ("Noom pioneered this pattern in health apps", RocketShip HQ).

**Gundry MD (Golden Hippo family):** WhyNative's teardown: "Gundry MD's landing pages normally consist of longform sales videos, 1-2 hour presentations that dive deep into an important, health-related topic." "The main focus for the page is the video." "Right away after pressing play Dr. Gundry goes through a checklist of popular breakfast foods... someone who clicks the ad wants to get gratification right away." "There's no option on the page to continue or even buy anything" until the video reveals it; trust elements are "a bio of Dr. Gundry and his accomplishments" and "the outlets where Dr. Gundry has been featured." Format: pure VSL page with delayed buy button. This is the classic supplement DR model and it is the opposite of the app-quiz model.

**Golden Hippo, BioTrust, Organifi, Native Path, Beverly Hills MD, Balance of Nature, LiveGood:** No indexed teardown of their YouTube landing pages surfaced in the session. Balance of Nature's index entries were all iSpot TV spots (35% off offer, doctor spokesperson). General industry sources (Adbeat, native-advertising.net) say for supplements "advertorials win 99.5% of the time on platforms like Taboola and Outbrain, with VSLs winning the other 0.5%" (native, not YouTube), and that health VSLs run "between a late-night infomercial and a documentary, with most having an authoritative figure, like a doctor, as the brand spokesperson." Their specific YouTube destinations: could not verify.

**Caliber, Fitbod, Future, Ladder, Centr, Tempo:** Nothing indexed on their YouTube ad destinations. Pricing facts only: Ladder "offers a completely free 7-day trial with no payment required during trial... $59.99 per month or $299.99 per year"; Caliber "free-forever version, a Pro version for $19 per month." Whether their YouTube ads land on web or app store: could not verify.

**The web-vs-app-store decision:** Google's own 2025 material (Search Engine Land, business.google.com, GML 2025) says Demand Gen and YouTube can now send clicks "directly to your app" and cites "2.8x higher conversion rate for clicks that land on your app versus your mobile website" (Google internal data, 2025) and "2x higher conversion rates" for Web to App Connect on YouTube. Note that figure is about installed-app users, not cold acquisition. Every heavy fitness spender named above (MadMuscles, BetterMe, Noom) sends cold YouTube traffic to a web quiz, not the store. RevenueCat and FunnelFox both describe web2app as the model that "dramatically outperforms sending paid traffic directly to the App Store" (practitioner claim, no number surfaced).

---

## 3. Google Ads compliance for a fitness / AI-image landing page

All policy text below is as extracted by the search tool from support.google.com pages and agency summaries; the policy pages themselves were blocked.

**Clickbait ads policy (support.google.com/adspolicy/answer/15936667, in force since July 2020, folded into Misrepresentation):** "This policy covers advertisement which uses sensationalist or clickbait text or imagery which intend to drive traffic to the Ad through pressurizing the viewer to take immediate action in order to understand the full context of the Ad." Prohibited examples: ads that "claim to reveal secrets, scandals or other sensationalist information"; "clickbait messaging such as 'Click here to find out', 'You won't believe what happened'"; "clearly altered zoomed in body parts"; and "ads which use 'before and after' images to promote significant alterations to the human body." Also "negative life events such as death, accidents, illness... to induce fear, guilt."

**Before and after (StubGroup glossary + Google community):** "Even if your before/after photos are real and from actual clients, they're still not allowed." StubGroup says it "applies universally across all ad formats and landing page content." Google's own phrasing covers the ad; whether the landing page is judged under the same rule is asserted by agencies, and Google does review "your destination landing page" as part of the same review (Search Influence). Treat the landing page as in scope.

**Health in personalized advertising (support.google.com/adspolicy/answer/16701855, plus the Restricted targeting page 143465):** Weight loss is "a sensitive interest category." You "can't offer remarketing (retargeting) for weight loss-related content." Ads "can't use language that implies body shaming or unrealistic results." Google "forbids advertising that creates feelings of negativity through body shaming or suggested negative outcomes if a user doesn't take a certain action." "Discovery and Demand Gen campaigns use advertiser-curated audiences by default and may be restricted." Since May 2025 the restriction does not apply to campaigns targeting licensed healthcare professionals. First-hand corroboration: our own account already shows "Personalized Advertising Enabled" on the Ads link and the board carries a Google Ads remarketing campaign that has "0 clicks/conversions ever", consistent with weight-loss remarketing being throttled.

**Misrepresentation (answer 6020955) and the 2025 split:** Google moved "non-fulfillment... due to lack of qualifications" into a separate "Unacceptable business practices" policy (answer 15938071); violation means "your Google Ads accounts will be suspended upon detection and without prior warning, and you will not be allowed to advertise with Google Ads again." Misrepresentation examples include "making misleading or unrealistic claims regarding weight loss or financial gain," "dishonest pricing practices," "clickbait tactics," "misleading ad design," and "unproven or inaccurate claims." Agencies list "thin or copied content on your website" as a trigger.

**Healthcare and medicines:** nothing specific to a fitness app surfaced beyond the weight-loss claim rules. A photo-to-abs app is not a medicine or supplement, so the main exposure is Misrepresentation and Clickbait, not Healthcare.

**AI-generated imagery:** Google's AI label rollout ("Google introduces new AI labels for Ads", blog.google, and "Updates to AI labeling requirements (July 2026)", answer 17257106): "Ads built with Google's own generative AI tools get the disclosure automatically. Ads built with third-party AI tools depend on the advertiser ticking a box." A "How this ad was made" panel appears in My Ad Center. Labels are required by law in "the European Union, India, and New York." One agency (auditsocials) claims that "as of March 5, 2026, all Google Ads using AI-generated images... must carry a clearly visible 'AI Generated' label"; I could not confirm that date from Google's own text, so treat the mandatory-label date as unverified but the disclosure checkbox as real. "Deepfake-style content depicting real, identifiable people is completely prohibited... even with consent" (agency summary of the synthetic-media rule). Important for us: the product's core output is an AI image of the user himself. The ad and page must never present the AI-abs image as a real result. Nothing surfaced requiring an AI label on the landing page itself; the label rules are about the ad creative. We already upload with `containsSyntheticMedia: true` and the YouTube AI-use flag.

**First-hand evidence from this account (Docs/DGEN_CONVERSION_CAMPAIGN.md, read in full):**
- 2026-09-10: all six Ad 1 ads were marked "Approved (limited), CLICKBAIT" within minutes on the headlines "This Picture Got Me Abs" and "Abs At 40 - The Photo That Did It". Rewritten to "How I Got Abs At 40 / See Yourself With Abs - Use AI / Abs By AI - Here's How It Works", the Clickbait verdict cleared and 8 of 10 went APPROVED.
- Two ads carrying one specific 16:9 video stayed "APPROVED_LIMITED, YOUTUBE_AD_REQUIREMENTS_EXAGERRATED_OR_INACCURATE_CLAIMS" at the video-asset level; the doc's diagnosis was the thumbnail, and the retry ladder is "clean text-free thumbnail, then removal."
- 2026-09-11: headline "Why My Diets Kept Failing" DISAPPROVED, CLICKBAIT; the "Why My X Kept Failing" shape is now refused by our own script.
- Measured: "A limited ad never spends in this account."
These are the most reliable policy signals available to us, because they are verdicts on our exact product.

**Landing page experience (Quality Score, Search):** Google's stated factors, as summarized by several sources of the help page: "relevant and original content, ease of navigation, an optimal number of links with minimal departure points, and meeting the user expectations set by the ad," with "transparency and trustworthiness" (who you are, what you offer, pricing, policies, contact info), load speed and mobile-readiness as further signals. Groas.ai: "Your ad headline must match your landing page H1, which is the single most common cause of 'Below Average' ratings." Foundry CRO's checklist: "target LCP under 2.5s and INP under 200ms... CTA is visible above the fold on a 375px screen, tap targets are at least 48px, and body text is at least 16px." Groas.ai claims "Ads with 'Above average' landing page experience and ad relevance see CPCs 36% below average" (source of that number not shown; unverified).

---

## 4. Demand Gen / YouTube specific guidance

From Google's Demand Gen help set (answers 14693848 best practices, 14733311 Creative Excellence Guide, 13704860 asset specs, 16797388 performance guide) as extracted:
- "Review the page on your website that you're linking to (called the landing page) and make sure to include a clear call-to-action in your ad that takes viewers straight to that landing page."
- Landing page preview: "Google [can] capture a screenshot of your landing page, which will be displayed below your video ad... it gives people a glimpse of what will happen next after they click." Implication: the above-the-fold screenshot of our page is itself ad creative and gets policy-reviewed as such.
- "Captivate people in the first 5-10 seconds of the ad with a problem statement and show how your product or service solves it."
- "Keep text legible on mobile, where most impressions land, and mirror your landing page promise so the click-through experience feels continuous rather than disjointed."
- Video length: "10-20 seconds ideal for Shorts and under three minutes for other placements"; vertical 4:5 / 9:16 matters because "Discover skews mobile."
- Budget: "set your budget to at least 10 times your CPA bid"; consolidate ad groups.
- Web vs app: Demand Gen can now deep-link to the app; Google cites the 2.8x figure above.

---

## 5. Benchmarks

- Unbounce Conversion Benchmark Report (Q4 2024 data, 41,000 pages, published 2025): all-industry median 6.6%. Health and wellness: "median landing page conversion rate for wellness-specific pages is 8.2%"; "about half of the wellness pages have a median conversion rate of between 4.5% to 14.5%." "Fitness-and-wellness landing pages from paid search convert at 4.4% on average, while the top 10% of performers reach 5.8%." "Mobile drives 7x more traffic than desktop to health landing pages, but desktop converts 22% better." Email traffic converts roughly double paid search and paid social for health pages. Data-backed (Unbounce's own page data; conversion is any form/click goal, not purchases).
- VSL vs text: one secondary source (Green Frog Labs, citing "2025 Unbounce data") says "pages featuring a VSL as the primary content element averaging 12.7% conversion rate compared to 4.8% for text-only sales pages." I could not confirm that Unbounce published those numbers; treat as unverified.
- Daily Intel Service VSL benchmark: "0.30%-1.80% for cold VSL traffic and 1.50%-5.50% for warmed traffic, measured as purchases from unique VSL page visits." Practitioner estimates, method unstated.
- WordStream 2025 Google Ads benchmarks: all-industry Search conversion rate 7.52%; "fitness-and-wellness... 4.10%"; health and wellness CPC "$1.63 in 2025"; CPA "$12.95-$27.31." Data-backed (WordStream/LocaliQ client data, Search only, conversion defined by the advertiser).
- FunnelFox 311 web2app funnels (2024-2025): "Only 13% of web2app funnel sessions reach the paywall, with a typical web2app funnel seeing around 3% conversion from session start to purchase." Trend: "many apps have shifted away from the paid trials model to the intro discount offer combined with the three-option paywall." Data-backed on funnel structure; the 3% is their observation across tracked funnels.
- Adapty / RocketShip: "Showing a paywall after 3-5 screens of value demonstration converts 40-60% better than showing it immediately"; "onboarding flows with 3-5 screens before the paywall outperform both shorter (1-2 screens) and longer (6+) flows." Note the tension with MadMuscles' 48 screens; the Adapty data is in-app onboarding, MadMuscles is a cold-traffic web quiz. "Health & Fitness operates roughly 5x more high-volume Web2App funnels (>100 creatives/month) than the next category."
- RevenueCat State of Subscription Apps 2025: Health and Fitness "median trial-to-paid conversion rate of 39.9%, while the top 10% convert at 68.3%"; "82.1% of trials start on D0"; trial-to-paid median by trial length "25.5% (≤4 days), 37.4% (5-9 days), and 42.5% (17-32 days)"; download-to-paid "12.1% at P90." Data-backed (RevenueCat's own SDK data). Our 7-day trial sits in the 5-9 day band.
- Databox / video: "over one-third of respondents indicate that videos and graphics positively improve landing page conversion rates." Survey opinion, not a measured lift. No Databox video-landing-page benchmark for paid traffic exists in the index.

---

## Synthesis: 11 rules for a landing page that YouTube / Demand Gen traffic converts on

1. **The page repeats the ad's claim stack word for word above the fold.** Source: Inceptly seniors teardown ("the landing page echoed the ad with the same claim stack"), VidTao 2025 guide ("your CTA should lead to exactly what you just pitched"), Google Demand Gen guide ("mirror your landing page promise so the click-through experience feels continuous"), Google landing page experience ("meeting the user expectations set by the ad"). Practitioner opinion backed by Google's stated ranking factor. Practical form: the H1 is the ad's headline, and since we run several ad angles, we need one page variant per angle (MadMuscles runs 493 entry URLs for exactly this reason).

2. **Give the click immediate gratification in the first seconds of the page, then earn the rest.** Source: WhyNative Gundry teardown ("someone who clicks the ad wants to get gratification right away"), the VSL-page structure guides ("a strong first 30 seconds", "the first 30 seconds mirrors the ad"). Practitioner opinion. For us the gratification is the photo-to-abs demo, not a sales pitch.

3. **The page must work for someone who never plays the video.** Source: Verlua/Kewise structure ("text for skimmers... three to five short lines that translate the video into scannable outcomes. It should still work if someone never finishes the video"), VidTao's VSL + TSL hybrid case ("short VSL ad and text sales page elements together create a full sales argument"). Practitioner opinion, one case study. Autoplay is not guaranteed on mobile and Google's landing page screenshot is static.

4. **Strip departure points.** Source: Google landing page experience ("an optimal number of links with minimal departure points"), Noom teardown (site "is just a landing page, and all the value is behind an auth wall"). Data-backed as a Google ranking factor. One CTA, no nav, no footer link farm above the legal block.

5. **Keep transparency elements on the page: who Dan is, what the product is, the price, the trial terms, contact and policies.** Source: Google landing page experience ("transparency and trustworthiness: clear identification of who you are, what you offer, pricing, policies, contact info"); Gundry pages carry a bio and press logos for the same reason. Data-backed as a Google factor. For a $19.99/mo trial product this also defends against the Misrepresentation "dishonest pricing practices" line.

6. **Mobile first, measured: LCP under 2.5s, INP under 200ms, CTA visible on a 375px screen, 16px body text, 48px tap targets.** Source: Foundry CRO checklist and Google's Core Web Vitals; Unbounce's finding that mobile is 7x the health traffic but converts 22% worse than desktop. Data-backed on the traffic split; the specific targets are Google's Web Vitals thresholds. A VSL page with a hero video is exactly the kind of page that fails LCP, so the poster frame must be a lightweight image.

7. **Use a friction-removal line as prominently as the promise.** Source: Inceptly seniors teardown ("No medical exam," "right over the phone," "Rates never increase..."), the 2025 web2app trend toward "intro discount... three-option paywall" (FunnelFox). Practitioner opinion. Our equivalents: "7 days free", "one photo, 60 seconds", "cancel anytime".

8. **Decide the format by awareness level, not by category habit.** Source: Inceptly lead framework (direct leads for aware audiences, story/secret leads for unaware). Practitioner framework (Schwartz). The supplement giants use 1-2 hour VSLs because they sell to unaware cold traffic on a mechanism; the app giants use quizzes because the quiz is the personalization. Our ad already tells the story, so the page's job is the demo plus the offer, which argues for a short VSL page with a strong text layer rather than a Gundry-length video.

9. **Put a personalization step before the paywall, but keep it short.** Source: Adapty/RocketShip ("3-5 screens of value demonstration converts 40-60% better than showing [the paywall] immediately"), Noom/BetterMe/MadMuscles all quiz first. Data-backed (Adapty, in-app data) and observed practice (web funnels). Our photo upload plus the body analysis already is the personalization step; the page should sequence it as upload, then analysis, then trial, rather than trial first.

10. **Budget the page for a 3% session-to-purchase reality and a ~40% trial-to-paid reality.** Source: FunnelFox ("around 3% conversion from session start to purchase", "only 13% of sessions reach the paywall"), RevenueCat (39.9% median trial-to-paid for Health and Fitness, 37.4% for 5-9 day trials). Data-backed. Judge the page on cost per trial and cost per paying customer (which also matches Dan's standing marketing rule), not on video plays.

11. **Never let the ad or the page say or show anything the reviewer can read as a result claim or a before/after.** Source: Google Clickbait policy ("'before and after' images to promote significant alterations to the human body"), Misrepresentation ("misleading or unrealistic claims regarding weight loss"), and our own verdicts (Clickbait on "This Picture Got Me Abs", "Abs At 40 - The Photo That Did It", "Why My Diets Kept Failing"; exaggerated-claims limit on a video asset). Data-backed by first-hand enforcement.

---

## Above-the-fold patterns of top advertisers that are policy risks for us

1. **The side-by-side "you now / you with abs" image.** This is the product, and it is also the literal definition of the banned before/after. MadMuscles and BetterMe show illustrated body-type selectors, not transformation photos of one person; Gundry shows no bodies at all. Our hero must show the AI image as a preview ("see yourself with abs") with an explicit "AI-generated preview, not a result" label, and never place a real photo of Dan or a user beside an abs image in a two-panel layout. The board already records that Ad 2's master shows a banned BEFORE/AFTER screen, so this is a live problem, not a hypothetical.

2. **Curiosity-gap headlines.** "This Picture Got Me Abs" was limited for Clickbait on our account. Anything shaped "the photo that did it", "why my X kept failing", "you won't believe" is refused. Headline must be a plain description of the mechanism.

3. **Fear or shame framing.** "Body shaming or suggested negative outcomes if a user doesn't take a certain action" is banned under Health in personalized advertising. No "dad bod", no "still hiding at the pool" language above the fold.

4. **Numbers that imply typical results.** The current post-generation video says "thousands of guys" while 75 people have generated (board note). On a landing page that is a Misrepresentation exposure ("unproven or inaccurate claims"). Use true numbers or none.

5. **Real-person AI likeness.** The product makes an AI image of the viewer himself; that is consent-based and self-directed, which is different from the deepfake rule, but any AI image of Dan used as a testimonial must be labeled and must not be presented as a photograph of a real outcome.

6. **Remarketing.** Weight-loss remarketing is not allowed; our remarketing campaign has 0 clicks ever. Do not design the page around retargeting pixels for weight-loss audiences.

7. **Landing page screenshot in the ad.** Demand Gen can show a screenshot of the page under the video; whatever is above the fold becomes ad creative and is reviewed as such. Design the fold to pass ad review on its own.

---

## Could not verify

- Any 2025-2026 VidTao public ranking of fitness / health / supplement YouTube advertisers.
- The exact "the ad is the first 30 seconds of the VSL" sentence from VidTao or Inceptly.
- The YouTube landing page format used by Golden Hippo's other brands, BioTrust, Organifi, Native Path, Beverly Hills MD, LiveGood, Balance of Nature, Caliber, Fitbod, Future, Ladder, Centr, Tempo.
- Whether Google's before/after rule is enforced on landing pages by the letter of the policy (agencies say yes; Google's text quoted covers ads, and landing pages are reviewed under Misrepresentation).
- The "March 5, 2026 mandatory AI Generated label" date (single agency claim).
- The "12.7% VSL vs 4.8% text page" figure attributed to Unbounce.
- Any published video-landing-page or free-trial-signup benchmark specific to fitness apps from paid YouTube traffic.

Sources consulted (indexed pages, not fetched): blog.vidtao.com (guide parts 1-2, spy-on-competitors, VSL+TSL hybrid, hook tactics, Oct 2022 leaderboard, 3 Ad Thursday series); inceptly.com (seniors teardown, lead framework, funnel blueprint, 2025 update recaps); inceptly-agency.beehiiv.com (mini VSL of the month); web2appworld.com/breakdowns/madmuscles; blog.funneloftheweek.com (biggest quiz funnel of 2025); funnelfox.com and blog.funnelfox.com (311 funnels, BetterMe 75,000 ads); lazertechnologies.com (Noom quiz); whynative.com (Gundry MD); support.google.com/adspolicy answers 15936667, 16701855, 143465, 6020955, 15938071, 17257106; support.google.com/google-ads answers 14693848, 14733311, 13704860, 16797388, 2404197, 16501674; blog.google AI labels; stubgroup.com before/after glossary; unbounce.com healthcare-wellness benchmark; wordstream.com 2025 benchmarks; revenuecat.com State of Subscription Apps 2025; adapty.io and rocketshiphq.com fitness paywall benchmarks; dailyintelservice.com VSL benchmark; foundrycro.com and groas.ai landing page checklists; searchengineland.com web+app campaigns; verlua.com / kewise.com VSL page structure. First-hand: /home/user/abs-by-ai/Docs/DGEN_CONVERSION_CAMPAIGN.md.

---

