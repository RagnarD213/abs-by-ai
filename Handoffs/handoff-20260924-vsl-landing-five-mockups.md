# Handoff: five VSL landing page mockups for Abs By AI

Written 2026-09-24 by Claude (Opus 5.5) after a VidTao research session. Not executed. The next task designs the five
mockups; it does not build or deploy a live page.

## 1. Goal

Design five mobile-first mockups of a straight VSL landing page: a video, then a free-trial sign-up, nothing else.
All paid traffic (YouTube / Google Ads Demand Gen, Meta) will go to the winner, so the page has one job: turn a cold
visitor into a started 7-day trial, and then a paying member. Dan picks one or two to build and A/B test.

**Out of scope (Dan's instruction):** quiz funnels, photo-upload front ends, free AI generation as the hook, any
unconventional funnel. The AI generation stays a member feature (standing rule, memory `proven-direct-response-only`).

## 2. The offer and assets the page must use (settled, do not reopen)

| item | fact | source |
|---|---|---|
| Offer | 7-day free trial, then **$19.99/month**. Annual **$69.99** exists (one tap away in the cart) | `Docs/WEB_CART.md`, WV-01 plan §1 |
| Trial order | Trial comes BEFORE photo generation. The page never asks for a photo. | WV-01 plan §1 |
| CTA words | `Start My 7-Day Free Trial` (the video's last on-screen line matches it) | WV-01 plan A11 |
| Where the CTA goes | the existing web cart: card before account, Stripe collects email + card, $0 today, day-5 reminder email, day-7 charge | `Docs/WEB_CART.md` (`/?join=1` → `#cartSection`) |
| Video | **WV-01** founder VSL, 16:9, Version A (result promise) and Version B (support gap: "I fired my trainer, my nutritionist and my meal prep service"). Being edited now. **WV-02** is a separate /start video from roll C1701-C1703. Use a poster frame of Dan as a placeholder. | `Handoffs/video-editing/WV-01-EDIT-PLAN-20260924.md`, `WV-02-...md` |
| The five things members get (the video's structure) | motivation (your goal picture), workouts that adapt, calorie tracking from a food photo, meal prep recommendations, sleep/recovery coaching | WV-01 plan A03-A08 |
| Founder proof | Dan: about 200 lb at 38, abs at 40, business owner, raising a daughter | memory `dan-personal-facts-for-scripts`, DS-08 |
| Photos | `photos/dan transformation photos/`, `photos/Dan Before Pictures/`, `photos/finalized social media photos/`, `photos/pool shoot | 7-31-26 .../`, `photos/studio shoot | 8-28-26 .../`, `public/img/dan-founder.jpg`, `public/img/video-poster.jpg` | local |
| App screens | take real screenshots of the member hub, trainer, food-photo tracker, meal prep and sleep coach from absbyai.com (use the local funnel test recipe, memory `local-funnel-test-recipe`, if a logged-in member view is needed) | live app |
| Current page | `absbyai.com/start` (`public/start.html`, photo-upload A/B). The new page replaces it for paid traffic. | `Docs/VSL_LANDING.md` |

## 3. What the research found (VidTao, 2026-09-24)

Method: Dan's VidTao account (Marketer tier) in Chrome. Pulled the top ~7,500 English ads in Fitness, Bodybuilding,
Personal Training, Weight Loss, Men's Health, Nutrition and Health categories, sorted by total and 30-day spend, then
read the recorded click-through URL of ~1,100 of them and visited the landing pages on a phone-size screen. All spend
figures are VidTao estimates, not audited.

**Finding 1: the biggest men's fitness spenders no longer send cold YouTube traffic to a straight VSL page.**
MadMuscles (~$6.5M in the last 30 days), Muscle Booster, Harna, BetterMe, Meredith Shirk (Rise Workouts / Metaboost,
$31M lifetime) and V Shred all route their top ads into a quiz first. So the men's fitness VSL page we can copy is the
page **behind** V Shred's short survey, which is a pure VSL page. That is the primary template.

**Finding 2: V Shred's ads ARE the sales video.** Their current winners are 4 to 5 minute YouTube ads (e.g.
`OMgL_94HiAo` $2.3M total / $271k last 30 days; `XkHzg0p8gMw` $2.3M / $171k). The landing page continues the pitch
with a 27-minute VSL. Implication: our page must survive a visitor who already watched a long ad (fast, visible CTA
path) and a visitor who did not (the video carries the whole sale).

**Finding 3: the pure VSL page is alive and scaling on YouTube right now, mostly in health/supplement offers.** The
same skeleton shows up everywhere: pre-headline, headline, video, "sound on" line, presenter, press strip, and the offer
hidden until the pitch. The player on 5 of the 7 VSL pages inspected is Vidalytics (muted autoplay with a
"click to play sound" overlay, and CTA buttons revealed at a set timestamp).

**Finding 4: the other half of the market runs "video plus offer" hybrids** where the CTA and the full sales page are
visible from the first second (Gundry, Fit Father, Hormozi). Nobody publishes which works better for a free trial, so
two of the five concepts below exist to test exactly that split.

## 4. Reference library

Screenshots (390 px phone width, captured 2026-09-24) are in
`Media/research/vsl-landing-references-20260924/` (local only; `Media/` is gitignored because the repo is public).
`_capture-script.mjs` in that folder re-captures any page (`node _capture-script.mjs out.jpg URL heightPx [revealJS]`).

| # | Page | VidTao evidence | Format | Screenshot |
|---|---|---|---|---|
| R1 | **V Shred men's VSL** `le.vshred.com/sp/survey/male-fl` (after the survey at `/sp/survey/survey-ga`) | V Shred $23.2M/yr YouTube; the survey page it feeds has taken ~$990k in the last 30 days across its ads | Pure VSL. Offer + sales page hidden until the pitch | `01-...top.jpg`, `02-...revealed.jpg` |
| R2 | **Sculpt Nation (V Shred) Burn Evolved VSL** `sculptnation.com/sp/burn-evolved/burn-vsl-apc` | ad `w1tUMojZ-JM` $1.3M | Pure VSL, vertical video, hidden offer | `03-sculptnation-burn-vsl.jpg` |
| R3 | **TestoGreens Max, men 50+** `testogreensmax.com/gdra/` | ads `uDDcHJ2A0wU` $571k + `DThuCQL5ZY0` $483k (brand ~$2M) | Pure VSL, doctor presenter, hidden buy boxes | `04-testogreens-vsl.jpg` |
| R4 | **Nail Exodus** `stopnaildecay.com/ne/nail-exodus` | ad `-eu58SmI2ZU` **$5.2M total, $907k in the last 30 days**, the hottest pure VSL found | Pure VSL, about two screens tall | `11-nail-exodus-pure-vsl.jpg` |
| R5 | **Gundry MD Bio Complete 3** `www2.trybc3.com/cid/...` | ad `siJblcx4h_c` $2.2M; Gundry MD brand $33.8M | Hybrid: video then offer immediately, long page | `05-gundry-bc3-hybrid.jpg` |
| R6 | **Fit Father 30X, men 40+** `fitfatherproject.com/ff30x-letter-direct-yt` | brand small ($281k top ad); used for its men-40+ offer stack, weak spend signal | Video + offer stack + long letter | `06-fitfather-ff30x.jpg` |
| R7 | **Hormozi scaling workshop** `acquisition.com/workshop-km` | ads `25lRvjoqO8w` $171k, `guSdQkbz_Fs` $51k; Hormozi brand ~$1M | Short video, CTA under it, blunt FAQ | `07-hormozi-workshop.jpg` |
| R8 | **BODi subscription** `bodi.com/us/en/s/fitness/10-minute-subscription` | ad `W66vUe7sn5M` $852k | Membership offer page, annual shown as a monthly price | `08-bodi-subscription.jpg` |
| R9 | **Noom trial** `noom.com/frbs/` | Noom is a named leader in Dan's rule; spend not pulled this session | Trial page, renewal terms in plain sight | `09-noom-trial.jpg` |

Checked and rejected: Tactical X Abs (an ab-stimulator product page, not a VSL), Over 40 Alpha (dead page), Kinobody
(stopped YouTube ads; `moviestarbody.com` is down; the special-offer page is now a store), hims (intake flow),
Ladder / Fitbod / Calistway (app pages that lead into a quiz), Meredith Shirk and V Shred front doors (quizzes).

## 5. What the winners share (the rules every mockup follows)

Above the fold, in this order, on a phone:
1. **Pre-headline in small caps that names the presenter and his authority**: "Celebrity trainer Vince Sant reveals..."
   (R1), "World renowned heart surgeon reveals..." (R5), "Dr. Andreas Boettcher, functional medicine doctor" (R3).
   ⚠ Dan removed the eyebrow from /start in his 09-09 review. The leaders all use one, so each concept that uses it
   also ships a no-eyebrow variant and Dan decides.
2. **Headline = the result + the objection it removes.** R1: "How thousands of men with YOUR body type are dropping
   weight fast WHILE enjoying pizza, pasta, and beer." R3: "5 surprising foods that can plummet T-levels... in guys over
   50." We write ours in Dan's voice, Title Case, with no unbelievable claims and no invented numbers.
3. **The video starts within the first screen, full width.** Poster frame shows the presenter's face and a play cue.
4. **"Make sure your sound is on" line** directly above or below the player (R1, R2, R3, R4). Muted autoplay with a
   big "Tap to turn on sound" overlay (R2, R4 via Vidalytics).
5. **Presenter card** under the video: photo + name + one credential line (R1, R3, R4, R5).
6. **Press strip** ("As seen in") on R2, R4, R5. ⚠ We have no press. Replace with proof we actually own (see 6.3).

The offer, when it appears:
- One clean card. Price anchor on V Shred and Fit Father is a crossed-out "value". Ours is: **7 days free, $0 today,
  then $19.99/month, cancel any time in the app.** Annual $69.99 can be shown BODi-style as "about $5.83/month".
- Terms sit next to the button in readable type (Noom, BODi). This is non-negotiable: the FTC shut down MadMuscles'
  parent in June 2026 over hidden renewals and blocked cancellation (memory `madmuscles-deep-dive`).
- **Risk reversal**: V Shred's 30-day guarantee, Gundry's 90-day "risk-free", Fit Father's 30-day money-back. Ours is the
  trial itself: "Try it free for 7 days. We email you before day 7. Cancel in the app and you pay nothing."
- Big button, repeated after every section (V Shred repeats it 5 times, Fit Father 6).

Below the offer (long-page concepts):
- "This is for you if..." list (R1).
- "What's included" stack with each part named and explained (R1, R6). ⚠ The WV-01 plan forbids inventing dollar
  values for the roles, so no "$197 value" labels. The honest version is the support-gap comparison in the video:
  a trainer, a nutritionist and meal prep are each a monthly bill; the membership is $19.99.
- Before/after proof with name and a results-vary line under each (R1). Ours: Dan's own real before and after only.
- FAQ with blunt answers, including who it is NOT for (R7) and "is there a catch?" (R1).
- Legal footer only. No site navigation anywhere (every VSL page inspected has none).

**Do not copy:** fake countdown timers (R1 has one; it is a dark pattern), invented member counts ("thousands of guys" is
banned on screen, board 09-15; ~75 people have ever generated), press logos we have not earned, "trick"/"secret"
framing (memory `ad-retry-rule-and-no-trick`), unbelievable claims (memory `ad-copy-no-unbelievable-claims`), any em dash.

## 6. The five concepts

Each concept: phone 390 px first, then desktop 1280 px. Same offer, same CTA words, same cart destination. The CTA
behavior and page length are what differ, so the concepts can be A/B tested against each other.

### Concept 1: "The Classic Reveal" (V Shred male VSL, Sculpt Nation, TestoGreens, Nail Exodus)

Hypothesis: the pure VSL format that V Shred uses behind its quiz, and that the hottest YouTube VSL (Nail Exodus) uses
today, converts best when the video carries the sale and nothing competes with it.

Wireframe (phone):
1. Small logo only, centered (no menu).
2. Pre-headline: "40-year-old dad and business owner reveals..." (no-eyebrow variant drops it).
3. Headline, 3 lines max, e.g. "How I Fired My Trainer, My Nutritionist And My Meal Prep, And Got Abs At 40 With AI" (B
   video) or "How A Busy Dad Got Real Six-Pack Abs At 40 With An AI Coach In His Pocket" (A video).
4. Hand-drawn arrow + "Click to play" (R1) and the 16:9 player, full bleed, muted autoplay, "Tap to turn on sound"
   overlay; no visible scrub bar (Vidalytics-style).
5. "Make sure your sound is on" line with a speaker icon.
6. Presenter card: Dan's face circle, "Dan Rose, founder of Abs By AI. Down from about 200 lb at 38 to abs at 40."
7. Nothing else is visible until the pitch.
8. **Revealed at the offer timestamp** (and immediately for a returning visitor): offer card, then short proof strip
   (Dan's before/after, real-photo labels), "What you get" (five helpers, one line each), FAQ (5 questions), second CTA.
   Mock both states side by side: "before reveal" and "after reveal".

### Concept 2: "Video + Offer Hybrid" (Gundry BC3, Fit Father)

Hypothesis: YouTube visitors who already watched a long ad want the button now. Gundry, one of the largest VSL spenders
on YouTube, shows the risk-free offer directly under a short video and lets the page sell below.

Wireframe:
1. Slim top bar: "7-Day Free Trial, $0 Today" + small `Start Free Trial` button (Fit Father's sticky offer bar).
2. Pre-headline + headline (as concept 1, tighter).
3. Player (poster + unmute overlay).
4. **Offer card immediately under the video**: "Try Abs By AI free for 7 days", three check lines (the five helpers
   grouped into three), the big CTA, the terms line.
5. One quote from Dan, card style with his photo (Gundry's "doctor quote" block).
6. Before/after proof block (Dan only, labeled real photos).
7. "How it works in 3 steps": start trial → answer 5 questions → get your plan and your goal picture.
8. Plan selector: Monthly $19.99 (pre-selected) / Annual $69.99 "about $5.83/month" (Gundry package selector, BODi
   framing).
9. FAQ, final CTA, legal footer. Sticky bottom CTA on mobile after the first scroll.

### Concept 3: "The Founder Story Long-Form" (V Shred revealed page body, Fit Father letter, Kinobody historical)

Hypothesis: men 35+ who did not grow up with apps need to read the argument as well as hear it. V Shred's revealed page
is ~17,000 px of long-form sales copy under the video; Fit Father's men-40+ page is the same idea.

Wireframe:
1. Headline + player as concept 1, CTA visible from load under the video.
2. The story in Dan's first person, short paragraphs, pull-quotes: 200 lb at 38, knowing what to do and not doing it,
   hiring the experts, why it still did not work.
3. "The other 165 hours": a simple 7×24 week grid graphic with 3 cells lit (the WV-01 B-version idea) and one line:
   the trainer covers 3 hours a week, you are alone for the other 165.
4. "This is for you if..." (5 bullets, V Shred style).
5. "What you get": five cards, one per helper, each with a real app screenshot and one sentence. No dollar values.
6. "What it would cost to hire this": trainer, nutritionist, meal prep as three rows with no invented prices, just
   "monthly bill", against "$19.99/month, all five" (WV-01 plan B insertion P5 wording rule).
7. Proof: Dan's before/after, large, with the real-photo label and a results-vary line.
8. Offer card with trial terms, then FAQ, then final CTA. CTA repeats after sections 3, 5 and 7.

### Concept 4: "The Membership Tour" (BODi subscription, Noom trial)

Hypothesis: the trial is free, so the biggest objection is "what will I actually get and how hard is it to cancel",
not "is this real". BODi and Noom sell a membership by showing the product and stating the terms plainly.

Wireframe:
1. Headline: "Your Trainer, Nutritionist, Meal Planner And Sleep Coach. One App. $19.99 A Month." Sub: "Try it free for 7
   days." CTA above the fold (Noom puts the trial button in the first screen).
2. Player directly under the CTA (the video is supporting proof here, not the gate).
3. Horizontal swipe cards: the five helpers, each a phone-frame screenshot of the real app screen + one line.
4. "Your first 7 days": a day-by-day strip (day 1 plan, day 2 first workout, ... day 5 reminder email, day 7 decide).
   This makes the trial concrete and is honest about the reminder (the cart already sends it).
5. Plan toggle Annual / Monthly (BODi): Monthly pre-selected per Dan's cart decision, Annual shown as about $5.83/month.
6. Dan's founder card with before/after.
7. FAQ (cancel, what happens on day 7, iPhone/Android, beginners, equipment). Final CTA.

### Concept 5: "Straight Talk" (Hormozi workshop page)

Hypothesis: a skeptical, ad-weary male audience trusts a blunt page more than a hype page. Hormozi's workshop page is
short: video, button, three numbered promises, and an FAQ that states the price and tells the wrong buyer to leave.
(Hormozi is outside fitness; Dan asked for him by name in this research.)

Wireframe:
1. Dark top band (brand black `rgb(5,7,11)`), white headline in plain case, no caps shouting: e.g. "You Already Know
   What To Do. You Just Don't Have Anyone Helping You Do It."
2. Player, then the CTA button directly under it.
3. "What you get": #1 A plan that adapts, #2 Food tracking from a photo, #3 A coach that checks in every day. Each with
   one real screenshot.
4. "What people ask" FAQ with Hormozi-style answers: "How much is it? $19.99 a month after 7 free days. That's it." /
   "Who is this NOT for? If you want a shortcut that works without training or eating better, this isn't it." / "Is
   there a catch? No. We email you before day 7. Cancel in the app."
5. Final CTA. Legal footer.

## 7. Design direction for all five

- Mobile-first at 390 px; desktop 1280 px keeps a single centered column of max ~720 px (every VSL page inspected is a
  single column on desktop too).
- Brand: black `rgb(5,7,11)`, white, red accent `rgb(201,48,45)`, Manrope (memory `thumbnail-design-system`). The
  CTA may use a high-contrast action color (V Shred and Fit Father green, Gundry orange); show the mockups in red first
  and note one alternate.
- Headlines Title Case in Dan's words (his /start review, memory `vsl-landing-page`).
- Every real photo of Dan carries the real-photo chip; every AI goal image carries the AI label; before/after is always
  the same person (memory `before-after-same-person`).
- The player must not send people to YouTube. A YouTube embed shows "More videos" and a YouTube link. Mock a custom
  player (poster, unmute overlay, no scrub bar) and note in the build notes that the build task chooses the host.
- No em dashes anywhere in mockup copy (the AGENTS.md check must return 0 on every file).

## 8. Deliverable for the design task

1. Five standalone HTML mockups, one per concept, each showing phone and desktop, with real images from the paths in §2
   (placeholders only where an asset does not exist yet, clearly marked). Concept 1 shows both the before-reveal and
   after-reveal states.
2. One comparison page that shows all five phone versions side by side with a one-paragraph "why it might win / what
   would kill it" under each, and the reference screenshot it descends from. Publish it as a private Artifact and give
   Dan the link. Do not put competitor screenshots in git (public repo); embed them in the Artifact only.
3. Put the mockup HTML in `Media/research/vsl-landing-mockups-2026XXXX/` (local, gitignored) unless Dan asks for them in
   the repo.
4. End with Dan's pick: which one or two to build, and whether to keep or drop the pre-headline eyebrow.
5. Do NOT build the live page, touch `public/start.html`, change ad destinations or create PostHog flags. The build is a
   separate task after Dan picks. How it will be judged, for the record: cost per started trial and cost per paying
   member, split by variant (memory `proven-direct-response-only`).

## 9. Open questions for Dan (the design task asks these at the end, not before)

- Eyebrow / pre-headline: the leaders all use one; you removed it on 09-09. Keep or drop?
- Offer shown: monthly only, or monthly + annual on the page?
- Do we have any member testimonial we can use with permission? If not, the proof is Dan only.

## Starter prompt

> Read `Handoffs/handoff-20260924-vsl-landing-five-mockups.md` in full, then look at every screenshot in
> `Media/research/vsl-landing-references-20260924/`. Design the five VSL landing page mockups it specifies (phone and
> desktop, real Abs By AI assets, no em dashes), plus the side-by-side comparison page published as a private Artifact.
> Mockups only: do not touch the live site. End with my pick and the three open questions.

Recommended model: **Claude Opus 5.5, high effort** (design and copy work; Fable 5.1 high if Dan wants the stronger
writer on the headlines).
