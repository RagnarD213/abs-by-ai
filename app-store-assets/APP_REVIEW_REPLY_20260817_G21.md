# App Review reply — Guideline 2.1 Information Needed (rejection of 2026-08-14)

Submission `c4dc7f48-72d6-4ecd-b809-65be264fce85`. Apple asked for seven items. This is the reply text; the **screen recording (item 1) must be attached to the reply** using the "Attach File" control in the Reply to App Review dialog.

**Reply box limit is 4,000 characters.** The text below is within it. Do not paste a longer version — it will be truncated.

---

## Reply text (paste verbatim)

```
Hello,

Thank you. All seven items are answered below, and the screen recording is attached to this reply.

1. SCREEN RECORDING
Attached (5:10). Captured on a physical iPhone 17 Pro running iOS 26 on the TestFlight build of 1.0 (2), in three consecutive segments joined into one file. It begins by launching the app from the Home screen, then shows: creating an account; the In-App Purchase subscription screen with title, duration, price, auto-renewal disclosure, Restore Purchases and Terms/Privacy links, followed by a completed sandbox purchase; the AI-processing consent prompt and the photo library permission prompt; uploading a photo and generating a transformation; the AI Trainer and AI Nutritionist each producing a full plan with its Sources and references card; and permanently deleting the account. The app has no user-to-user content, so there is no reporting or blocking mechanism to show.

2. DEVICES AND OPERATING SYSTEMS TESTED
Physical: iPhone 17 Pro, iOS 26 (TestFlight, build 1.0 (2)).
Simulator, iOS 26.5: iPhone 17 Pro, iPhone 17 Pro Max, iPhone 17e, iPhone Air, iPad Pro 13-inch (M5), iPad Air 11-inch (M4), iPad mini (A17 Pro).

3. FUNCTION AND TARGET AUDIENCE
Abs by AI is a fitness motivation and planning app for adults who want to lose body fat. The problem it solves: an abstract goal is hard to stick to. The user uploads a photo and the app generates an AI image of how they could look at their goal - a personal target, not a stock model - then builds the plan to get there: an AI workout program, an AI meal plan, photo-based meal and macro logging, a sleep briefing, a supplement review and a daily brief. A printed poster or canvas of the goal image can also be ordered. Audience: adults, primarily men aged 25-55.

4. SETUP AND ACCESS
No special setup or sample files are needed. Demo credentials are in App Review Information; that account is a complimentary full member, so every feature is reachable without payment. IMPORTANT: for that reason it deliberately shows no purchase UI. To see the In-App Purchase flow, sign out or create a free account, then open Member Hub > Membership. Main flow: home > Add your photo > choose options > Generate my goal image. Then "Continue to my hub" reaches AI Trainer, AI Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit, Daily Brief, Progress Log and My Transformations. Deletion: Member Hub > Account > Delete my account.

5. EXTERNAL SERVICES
- Anthropic (Claude): checks the uploaded photo is usable; generates workout, nutrition, sleep and supplement text.
- Google (Gemini): generates the transformation image.
- Replicate, running ByteDance Seedream and Black Forest Labs FLUX: the same, on some requests.
- Apple StoreKit with RevenueCat: subscriptions and server-side entitlement checks.
- Stripe: payment for printed posters and canvases only (physical goods).
- Printify: prints and ships those goods.
- Resend: account email. PostHog: analytics. Railway: our backend and database, hosted in the US.
Each acts as a processor for us. No data broker or ad network receives user data.

6. REGIONAL DIFFERENCES
None. The app is offered on the United States storefront only, and every feature, price and piece of content is identical for all users. No region-gated content or behaviour.

7. REGULATED INDUSTRY / THIRD-PARTY MATERIAL
General fitness and wellness. Not a medical device; it does not diagnose or treat any condition, so no licence or regulatory authorisation is required. Health screens carry a "not medical advice - talk to your doctor" disclaimer and a Sources and references card citing the published research and CDC/NIH/FDA/HHS guidance behind each figure, consolidated at https://absbyai.com/sources. No protected third-party material is used: transformation images are generated from the user's own photo, and all other imagery is ours or AI-generated and labelled as such.

This information is also in the Notes field in App Review Information. Happy to provide anything further.
```

---

## Attachment: the screen recording (item 1)

**This is the only part Apple will not accept from anyone but a real device.** A simulator recording does not satisfy "captured on a physical device."

### Shot list — record in this order, one continuous take, roughly 3–5 minutes

Record with the iPhone 17 Pro's own screen recorder (Control Centre → record button), on the **TestFlight build of 1.0 (2)**.

Before starting: **delete and reinstall the app from TestFlight**, or sign out fully, so registration and the permission prompts actually fire. A returning signed-in user will skip most of what Apple wants to see.

1. **Home screen of iOS**, then tap the Abs by AI icon — the recording must begin with launching the app.
2. **Registration.** Tap "Log in" → create a brand new free account (any throwaway email).
3. **Tap "Add your photo."** Let the **AI-processing consent prompt** appear on screen for a couple of seconds, read-able, then Agree. Let the **photo library permission prompt** appear, then Allow.
4. **Pick a photo, choose options, tap "Generate my goal image."** Let the result appear.
5. **Repeat generating until the free generations run out** and the paywall appears.
6. **Open the In-App Purchase screen** (Member Hub → Membership). Hold on it long enough to read the Monthly and Annual prices, the auto-renewal disclosure, Restore Purchases, and the Terms/Privacy links. You do **not** have to complete a purchase in the recording.
7. **Walk the member features briefly** — AI Trainer, AI Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit. A few seconds each is enough; scroll one report far enough to show the Sources card.
8. **Account deletion.** Member Hub → Account → Delete my account → show the confirmation panel. Complete it if you're using a throwaway account; if not, show the panel and cancel.

Then: attach the .mov to the reply via **Attach File** in the Reply to App Review dialog.

### Cost note
Steps 4–5 run real generations against production and cost real money (a few cents each). That is unavoidable — Apple needs to see the real flow.
