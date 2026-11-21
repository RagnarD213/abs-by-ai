# Abs by AI — App Store Connect listing copy (paste-ready)

Drafted 2026-07-22. **Rewritten 2026-08-21 (Dan-approved) for the Guideline 1.1
"body editor" rejection: coaching leads, the photo feature is a labeled
goal-visualization step.** Every field below is sized to Apple's limits and ready to
paste into App Store Connect.

**Screenshot display order (2026-08-21):** coaching screens lead; ONE goal-image
screenshot (the home-hero, which carries the "AI AFTER" label), no before/after morph
sets.
- iPhone 6.9-inch (`6.9-inch/`): `06-ai-trainer-workout` (captured 2026-08-21),
  `07-exercise-demo-plank` (flattened 2026-08-21), `04-macro-tracker`,
  `05-ai-nutritionist`, `00-home-hero` last. Do NOT upload
  `01-the-reveal`, `02-transformations-gallery`, or `03-daily-brief` (all carry
  before/after morph pairs).
- iPad 13-inch (`13-inch-ipad/`): `03-ai-trainer`, `04-ai-nutritionist`,
  `00-home-hero` last. Do NOT upload `01-transformations`, `02-daily-brief`, or
  `05-everything-included` (before/after morph pairs).

---

## 1. App name and subtitle

- **App name** (30 chars max): `Abs by AI` (9 chars)
- **Subtitle** (30 chars max): `Visualize Yourself With Abs` (27 chars)

## 2. Promotional text (170 chars max, editable anytime without review)

> Your complete AI coaching team: personalized workouts, meal plans, photo macro tracking, and sleep coaching — plus an AI goal image of you to keep you motivated. (160 chars)

## 3. Description (4000 chars max — this draft ≈2300; Dan-approved 2026-08-21)

> Abs by AI is a complete AI fitness coaching team in your pocket — a personal trainer, nutritionist, macro tracker, sleep coach, and supplement advisor, all built around one mission: helping you lose the belly fat and build a leaner, stronger body.
>
> **YOUR AI COACHING TEAM**
>
> • **AI Trainer** — a personalized 4-week program built from your photos, your equipment, and your experience level. Every workout laid out day by day with sets, reps, form cues, and swaps.
>
> • **AI Nutritionist** — weekly meal-prep plans and calorie/protein targets built around your goal.
>
> • **Macro Tracker** — snap a photo of any meal and get calories and macros in seconds. Multiple angles, batch meal-prep portions, even leftovers.
>
> • **AI Sleep Coach** — check in each morning (or upload your tracker screenshot) and get a briefing on how to attack the day and fix tonight.
>
> • **Supplement Audit** — photograph your supplement stack and find out what's evidence-backed, what clashes with what, and what's wasted money.
>
> • **Daily Coach Brief** — one morning card that pulls it all together: today's workout, your targets, your weigh-in trend, your focus.
>
> **START WITH A GOAL YOU CAN SEE**
>
> Every good plan starts with a clear target. Upload a photo of yourself and Abs by AI generates a clearly labeled, AI-created goal image — an illustration of your own fitness goal, made only from your own photo, with your explicit consent. It's a motivational target, not a filter and not a promise. Once you can see your goal, your AI coaching team builds the plan to get you there.
>
> **TRACK THE JOURNEY**
>
> Log daily weigh-ins, weekly progress photos, and waist measurements. Watch your trend line move toward your goal. Keep every milestone in your gallery, share your progress, or set your goal image as your home-screen target.
>
> **PRINT YOUR GOAL**
>
> Order your AI goal image as a gallery-quality canvas or poster, shipped to your door. Put it somewhere you'll see it every single day.
>
> Your photos stay yours — they're private to your account, and you can delete your account and your data any time, right in the app.
>
> Abs by AI is a motivation and general-fitness tool, not medical advice. AI-generated images are illustrative goals, not guarantees.
>
> **SUBSCRIPTION**
>
> Abs by AI Membership unlocks the full AI coaching team. It is an auto-renewing subscription:
>
> • Monthly — $19.99 per month
> • Annual — $69.99 per year
>
> Payment is charged to your Apple Account at confirmation of purchase. Your subscription renews automatically unless auto-renew is turned off at least 24 hours before the end of the current period. You can manage or cancel your subscription in your Apple Account settings after purchase.
>
> Privacy Policy: https://absbyai.com/privacy
> Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/

**Do not remove the SUBSCRIPTION block.** Apple auto-rejected the 2026-08-22 submission under Guideline 3.1.2 because the description carried no Terms of Use (EULA) link. The app uses Apple's standard EULA (no custom EULA is set in App Store Connect), so the stdeula link above is the one Apple's automated check looks for.

## 4. Keywords (100 chars max, comma-separated, no spaces)

> sixpack,sixpackabs,six,pack,fitness,workout,coach,macro,calorie,tracker,meal,plan,gym,weight (92 chars)

Notes on what's in and out:
- `sixpack`, `sixpackabs` — brand carry-over terms from Dan's prior company.
- `six`, `pack` — separate tokens so multi-word searches like "six pack" and "six pack abs" match (Apple combines keyword tokens with name/subtitle words; `abs` comes from the subtitle).
- Removed `abs` and `ai` — Apple already indexes every word in the app name ("Abs by AI") and subtitle ("Visualize Yourself With Abs"), so repeating them in the keyword field wastes characters.
- Removed `sixpackabs.com` (searchers don't type ".com") and `sleep`, `body`, `transformation` — lowest search relevance per character.
- 8 characters spare if another term is ever wanted (e.g. `diet` fits).

## 5. Age-rating questionnaire (answer honestly — expect 12+/13+)

Apple's questionnaire wording changes; answer by these facts:

- **Realistic violence / cartoon violence / horror:** None.
- **Sexual content or nudity:** None. (Shirtless male torsos and sports-bra/swimwear photos are standard fitness content, not nudity — answer None, same category as every fitness app.)
- **Profanity or crude humor:** None.
- **Alcohol, tobacco, drug use or references:** None. (Supplement Audit discusses dietary supplements, not drugs.)
- **Medical/treatment information:** Infrequent/Mild. (Sleep Coach and Supplement Audit give general wellness guidance; every surface carries a "not medical advice" disclaimer; the Supplement Audit checks interactions against user-listed medications.)
- **Gambling, contests:** None.
- **Unrestricted web access:** No. (The app loads only absbyai.com content.)
- **User-generated content shown to other users:** No. (Photos are private to the account; sharing is user-initiated via the OS share sheet.)
- If Apple's newer questionnaire asks about **health/wellness or appearance/body-image topics**: answer Yes/present — the entire app is body-transformation imagery and fitness coaching for adults. Do not game this; 12+/13+ is fine for the category.

## 6. App Privacy declarations (Data Collection)

The app does NOT use data for cross-app tracking and shows no third-party ads → answer **"No"** to Tracking (no ATT prompt needed).

Declare these data types (all **linked to identity** via the account, none used for tracking):

| Data type | Collected? | Purpose | Notes (verified in server.js 2026-07-22) |
|---|---|---|---|
| Contact Info → Email Address | Yes | App Functionality | Account sign-in; also marketing emails with unsubscribe (welcome sequence via Resend) |
| User Content → Photos or Videos | Yes | App Functionality | Body photos are processed by AI to generate the after image; **finished before/after transformations and weekly progress photos ARE stored on our servers** (welcome_images, transformations, progress_entries tables), private to the account, deleted with the account |
| User Content → Other User Content | Yes | App Functionality | Meal photos, supplement-label photos, sleep-tracker screenshots — analyzed to produce results |
| Health & Fitness → Fitness | Yes | App Functionality | Weigh-ins, waist measurements, workout completion, sleep check-ins, calorie/macro logs |
| Identifiers → User ID / Device ID | Yes | App Functionality, Analytics | Account id; anonymous device id for free-generation credits; PostHog distinct id |
| Usage Data → Product Interaction | Yes | Analytics | PostHog usage events (screens used, features run) |
| Purchases → Purchase History | Yes | App Functionality | Physical print orders; payment handled entirely by Stripe — we never see card numbers |

Not collected: location, contacts, browsing history, search history, diagnostics/crash data, financial info (Stripe holds it), sensitive info categories beyond the above.

Privacy policy URL: `https://absbyai.com/privacy` (live, returns 200 — re-check before submission day). Confirm the page's wording still matches the photo-storage answer above.

## 7. App Review Notes (paste into the Review Notes field)

> **Sign-in for review:** use the demo account below (already a full member — no payment needed to reach any feature).
>
> **Business model — no digital purchases in the app (guideline 3.1.3(e)):** The only thing purchasable inside the app is a PHYSICAL product — a printed canvas or poster of the user's AI image, fulfilled by Printify and paid via Stripe checkout, which is permitted outside IAP as goods consumed outside the app. Digital items (generation credit packs, membership subscriptions) are NOT offered, shown, or purchasable anywhere in the iOS app; members manage their membership on the website. You will see neutral "manage from the website" notes instead of purchase buttons.
>
> **Native functionality (guideline 4.2):** native photo-library picker for all photo features; native share sheet and save-to-Photos for transformation images (with proper NSPhotoLibraryAddUsageDescription); native keyboard/safe-area handling; splash and status-bar integration via Capacitor.
>
> **Safety:** the generation flow refuses photos of apparent minors (hard REFUSED_MINOR guard in the AI pipeline) and runs content moderation on inputs and outputs. All coaching surfaces carry "not medical advice" disclaimers.
>
> **Account deletion (guideline 5.1.1(v)):** Member hub → Account → "Delete my account" — permanent, in-app, cancels any subscription first.
>
> **Demo account:** see credentials below / in the review sign-in fields.

## 8. Other App Store Connect fields

- **Category:** Health & Fitness (primary). Secondary: Lifestyle.
- **Bundle ID:** `com.absbyai.app` · **SKU:** `absbyai-ios`
- **Support URL:** `https://absbyai.com` · **Marketing URL:** `https://absbyai.com`
- **Copyright:** © 2026 Rose Digital Holdings LLC

---

## Reviewer demo account (App Review sign-in fields)

- Email: `danroseconsulting+applereview@gmail.com`
- Password: `AppleReview-70edff12010a`
- Status: READY (2026-07-22). Comp membership granted by Dan via the admin panel; verified `active:true, status:"comp", plan:"beta"` via the API. Pre-populated in the iOS simulator: one real transformation (pool proof photo, Lean/Ripped, passed first try, locked in as the goal — shows on the hub and in My Transformations) and one real AI Trainer program (full gym, intermediate, Stage 4 of 7, photo-based analysis, week 1 AI-personalized). Daily Brief renders against the live program. No paywall or purchase UI anywhere in the app for this account.
