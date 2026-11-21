# App Review Information → Notes — full replacement (2026-08-17)

Apple's 2026-08-14 rejection ends: *"Include this information in the Notes field of the App Review Information section in App Store Connect for future submissions."* So the Notes field must be **replaced**, not appended to — the current 3,786-character version answers the older 1.4.1/3.1.1 rejections and carries none of the Guideline 2.1 information now being demanded.

This replacement keeps the still-accurate 1.4.1, 3.1.1, physical-goods and account-deletion material in condensed form, and adds all seven 2.1 answers.

**Field limit is 4,000 characters.** Verified length of the block below: see the count printed at the bottom of this file's build check.

## How to apply

App Store Connect → Apps → Abs by AI → Distribution → **iOS App 1.0** → **App Review Information** → **Notes**.
Select all (`cmd+A` inside the field), delete, paste the block below, **Save**. Then press **Update Review** on the version page — "Resubmit to App Review" on the submission page stays greyed out until the version itself is edited and saved.

## Replacement text

```
SIGN-IN: use the demo account in the fields above. It is a complimentary full member, so every feature is reachable with no payment - and for that reason it deliberately shows NO purchase UI. To see the In-App Purchase flow, sign out or create a new free account, then open Member Hub > Membership.

WHAT IT DOES / AUDIENCE: a fitness motivation and planning app for adults, primarily men aged 25-55, who want to lose body fat. The user uploads a photo and the app generates an AI image of how they could look at their goal - a personal target rather than a stock model - then builds the plan to get there: AI workout program, AI meal plan, photo-based meal and macro logging, sleep briefing, supplement review, daily brief. A printed poster or canvas of the goal image can also be ordered.

MAIN FLOW: home > Add your photo > choose options > Generate my goal image. Then "Continue to my hub" for AI Trainer, AI Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit, Daily Brief, Progress Log, My Transformations. No sample files or special setup needed.

ACCOUNT DELETION: Member Hub > Account > Delete my account. Permanent and immediate.

DEVICES TESTED: physical iPhone 17 Pro on iOS 26 via TestFlight; simulator on iOS 26.5 for iPhone 17 Pro, 17 Pro Max, 17e, Air, iPad Pro 13-inch (M5), iPad Air 11-inch (M4), iPad mini (A17 Pro).

EXTERNAL SERVICES: Anthropic (Claude) checks the photo is usable and writes the plans; Google (Gemini) generates the image; Replicate running ByteDance Seedream and Black Forest Labs FLUX generates the image on some requests; Apple StoreKit with RevenueCat handles subscriptions and server-side entitlement checks; Stripe takes payment for printed goods only; Printify prints and ships them; Resend sends account email; PostHog is product analytics; Railway hosts our backend and database in the United States. All act as processors for us. No data broker or ad network receives user data.

REGIONS: United States storefront only. Every feature, price and piece of content is identical for all users; no regional variation.

NO USER-TO-USER CONTENT: photos and generated images are private to the account that made them. There is no feed, sharing between users, or messaging, so there is no reporting or blocking mechanism.

GUIDELINE 1.4.1 / REGULATED INDUSTRY: general fitness and wellness. Not a medical device; it does not diagnose or treat any condition, so no licence is required. Health screens end with a "not medical advice - talk to your doctor" disclaimer and a Sources and references card linking the published research and CDC/NIH/FDA/HHS guidance behind each figure, consolidated at https://absbyai.com/sources. No protected third-party material: transformation images come from the user's own photo; all other imagery is ours or AI-generated and labelled.

GUIDELINE 3.1.1 / PAYMENTS: the membership is purchasable in the app by In-App Purchase - two auto-renewable subscriptions in one group, Monthly (com.absbyai.app.membership.monthly, $19.99/mo) and Annual (com.absbyai.app.membership.annual, $69.99/yr), both with a 7-day free trial. Title, duration and price are read from StoreKit at runtime. The screen carries the auto-renewal disclosure, Restore Purchases, and Terms and Privacy links. Entitlements are verified server-side; the app is never trusted to grant access. No digital content is purchasable by any other means. Printed posters and canvases remain physical goods handled outside In-App Purchase.

PRIVACY: an in-app consent screen names every AI provider before any photo or personal detail is sent, and declining cancels the action. Details and the Face data section are at https://absbyai.com/privacy.
```
