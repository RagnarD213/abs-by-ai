# Handoff: Finish Google Play Store public listing for Abs by AI (Android)

**Date:** 2026-08-05
**Project:** Abs By AI (Android app, Google Play Console)
**Business goal this serves:** Adoption (app store distribution) — the Android app has been working correctly in internal testing since 2026-07-25; this task is what's left to make it publicly downloadable on the Play Store.

## Objective

Finish the Google Play Console setup checklist for `com.absbyai.app` ("Abs by AI") so it can go from internal-testing-only to a public production release. The app itself needs no further engineering — it's a Capacitor/TWA wrapper around the live absbyai.com site, already verified working end-to-end (full-screen, purchase gating compliant, real photo-upload-to-generation flow tested). This task is entirely Play Console configuration/paperwork, not code.

## Current State

**App functionality — fully verified working, nothing to fix.** On 2026-08-05, drove the real installed internal-test build on Dan's physical Android device (Galaxy A14, `R92W60LKM2D`) over `adb` + Chrome DevTools Protocol:
- App installed, opens full-screen with no browser address bar (confirms the TWA/assetlinks setup from 2026-07-21 still works).
- Purchase gating confirmed via live DOM inspection: 9 `.app-hide-purchase` elements present, 0 visible — matches the required Play/Apple compliance posture.
- Ran a **real end-to-end generation**: uploaded a real photo through the actual native photo picker, selected Male/Heavier/Ripped, generated, got a correct "Meet the new you" result screen, free-generation counter correctly decremented 4→3. Full product loop confirmed working on the real device, real account.

**Play Console setup checklist — 10 of 11 complete as of this session.** (It was 4 of 11 at session start.) Console → Abs By AI (org account, `danroseconsulting@gmail.com` login) → app `com.absbyai.app` → Dashboard → "Set up your app":

| # | Item | Status |
|---|---|---|
| 1 | Set privacy policy | ✅ done (pre-existing) |
| 2 | Sign in details | ✅ done (pre-existing) |
| 3 | Ads | ✅ done (pre-existing) |
| 4 | Target audience | ✅ done (pre-existing) |
| 5 | **Government apps** | ✅ done this session — answered "No" |
| 6 | **Financial features** | ✅ done this session — "My app doesn't provide any financial features" (app only links out to the website for purchases; no in-app financial services) |
| 7 | **Select an app category and provide contact details** | ✅ done this session — Category: Health & Fitness. Contact: support@absbyai.com, +17372909944, https://absbyai.com. Published live. |
| 8 | **Data safety** | ✅ done this session — full 5-step questionnaire completed and saved (see below for exact answers) |
| 9 | Content rating | ❌ **NOT DONE — needs Dan** |
| 10 | Health (declaration) | ❌ **NOT DONE — needs Dan** |
| 11 | Set up your store listing | ❌ **NOT DONE — this session's main remaining task, mostly Claude-doable** |

**Data safety answers, recorded exactly so they aren't re-derived or re-litigated:**
- Does the app collect/share required data types? **Yes.** Encrypted in transit? **Yes.** Account creation method: **Username and password** only (no OAuth/social login exists in the app).
- Delete account URL: **`https://absbyai.com/privacy`** (verified this page explicitly documents: "You can permanently delete your account and everything associated with it — photos, generated images, and feature history — at any time from Member Hub → Account → Delete my account.")
- Partial data deletion (delete some data without deleting account)? **No** — the app only supports full-account deletion, no granular deletion flow exists.
- Data types selected, each marked **Collected only, never Shared** (reasoning: Anthropic/Google/Replicate/Stripe/Resend/PostHog are all service providers processing data on our behalf under contract for our purposes, which is the standard basis for not counting them as "third-party sharing" under Play's definition — this is why the final preview correctly shows "No data shared with third parties"):
  - **Personal info:** Email address, User IDs
  - **Financial info:** Purchase history only (not card/bank numbers — Stripe holds those, we never see them)
  - **Photos and videos:** Photos only
  - **Health and fitness:** Health info, Fitness info (both marked optional/user-choosable, since these come from opt-in features — Sleep Coach, Trainer, Nutritionist, Supplement Audit, Macro Tracker — not the core photo-transform flow)
  - **App activity:** App interactions only (PostHog analytics)
  - **Device or other IDs:** Device or other IDs (the `absbyai_device_id` used for free-credit tracking)
- None selected: Location, Messages, Audio files, Files and docs, Calendar, Contacts, Web browsing, App info and performance — none of these apply to this app.
- Final preview confirmed correct before saving: "No data shared with third parties," all 6 categories listed above with correct sub-items, delete-account link populated, "Data is encrypted in transit" shown, privacy policy link correct.

## Key Decisions Already Made

- **No mandatory closed-testing period blocks production.** This is an Organization Play Console account (not Personal), so once the 11-item checklist is done, "Create and publish a release" unlocks directly — confirmed live in the console (the 4 locked "Release your app" sections all just said "Complete the initial setup tasks first," no separate tester-count/duration gate appeared).
- **Content rating and Health declaration must be answered by Dan personally, not self-certified by Claude.** These are formal certifications to Google (per existing `app-store-policy-verify-first` memory practice and the same caution applied to Apple's App Store submission). Claude's role is to walk Dan through each question live, not click through on his behalf.
- **Everything else in the checklist is factual/objective**, not a judgment call requiring Dan's personal sign-off, so Claude completed those directly: Government apps (objectively no), Financial features (objectively none — app only links to a website), category (Health & Fitness is the obvious fit), contact details (existing support email/phone/site), Data safety (derived directly from what the codebase actually does, verified against `server.js` and the live privacy policy page).
- **The targetSdk deadline is real and time-sensitive.** Per prior research (see AI_COORDINATION.md), Google requires new submissions to target the current API level by **2026-08-31** — about 3.5 weeks out from this handoff's date. Get this submitted before then, or the build needs re-targeting.

## Detailed Plan

1. **Content rating (needs Dan live, ~5 min).** Navigate to Play Console → Abs By AI → `com.absbyai.app` → Dashboard → "Set up your app" → Content rating. This is a IARC questionnaire (violence, gambling, sexual content, controlled substances, user-generated content, etc.). Claude should sit with Dan and read each question aloud, since Dan's own answers are the legal certification — Claude should not guess/pre-fill. Likely straightforward given the app has no violence/gambling/etc., but the AI-generated body-transformation imagery and health/fitness advice content may affect a couple of specific answers — don't assume, read each one.

2. **Health declaration (needs Dan live, ~2 min).** Same location, "Health" item. This declares the app provides fitness/wellness content (Trainer, Nutritionist, Sleep Coach, Supplement Audit, Macro Tracker, body-transformation visualization). Google may ask about medical claims — the app's existing medical disclaimers (added after the 2026-08-05 iOS App Store rejection, see AI_COORDINATION.md's "iOS 1.0 REJECTED" section, commit `bcf8142`) are relevant context: body-fat estimates are qualified as "not a medical measurement," and Meal Plan/Trainer both carry "talk to your doctor" footers. Read Google's actual questions with Dan before answering — don't assume the iOS answers translate directly.

3. **Store listing (Claude-doable, biggest remaining item).** Play Console → Store presence → Store listings → main store listing. Needs:
   - **App name:** "Abs by AI" (already the working title, keep consistent with `com.absbyai.app`'s existing manifest).
   - **Short description** (80 char max) and **full description** (4000 char max). Can adapt from the iOS App Store listing copy already written in `app-store-assets/LISTING_COPY.md` (per the `ios-appstore-prep` memory) — but Android's char limits and tone conventions differ slightly from Apple's, so don't just paste verbatim; check the actual file first, since it hasn't been re-read in this session.
   - **App icon:** 512×512 PNG, 32-bit with alpha. Check `app-store-assets/` for an existing hi-res icon from the iOS submission before generating a new one.
   - **Feature graphic:** 1024×500 PNG/JPEG — **this one has no iOS equivalent**, will need to be created fresh. A simple before/after or hero shot in that banner aspect ratio would work; the existing proof images (`public/img/proof/*.webp`) or `app-store-assets/6.9-inch/00-home-hero*.png` are candidates to adapt/crop from.
   - **Phone screenshots:** 2–8 required, various min/max dimensions (check current Play Console requirements live, they update these occasionally). The iOS 6.9"/6.5" screenshots in `app-store-assets/` are close in aspect ratio to common Android phones but **must be re-captured or re-cropped for Android's exact required dimensions** — don't assume they'll upload as-is. The Android device used in this session (Galaxy A14, already `adb`-accessible) can be used to capture fresh screenshots of the live app if needed, following the same recipe used for the 2026-08-05 real-generation test (push a proof photo via `adb push` + MediaScanner broadcast, drive the UI via `adb shell input tap` after confirming exact on-screen coordinates with a screenshot each time — **coordinate scaling was unreliable and inconsistent throughout this session's UI automation; always take a fresh screenshot immediately before computing a tap/click coordinate, never reuse coordinates from an earlier screenshot**).
   - Save as draft is fine mid-work; nothing here needs to be "sent for review" until Dan wants to actually launch publicly.

4. **After all 11 items are complete**, the dashboard's 4 locked "Release your app" sections unlock (Closed testing, Open testing, Pre-registration, Create and publish a release). The path to public availability is: Test and release → Production → Create new release → attach the existing signed `app-release.aab` (already built, per `android-twa-build-setup` memory — confirm it's still current, or rebuild if the targetSdk deadline forces a rebuild) → roll out.

5. **Before actually publishing to production, loop Dan in for a final go/no-go** — this is an outward-facing, consequential action (makes the app publicly discoverable), consistent with how the iOS submission was handled (everything prepped, final "Submit"/"Resubmit" press left to Dan).

## Things to Avoid / Lessons Learned

- **UI automation gotcha, worth preserving for whoever continues this:** Play Console's checklist items, category dropdowns, and expandable data-safety sections are **not plain `<button>` elements** — they're Angular custom components (`console-header`, `dropdown-button`, etc.) where the ARIA-accessible "button" role sits on a `<div>`, not a real button tag. Plain `document.querySelectorAll('button')` misses them. The reliable pattern that worked throughout this session: find the element by its exact visible text (`Array.from(document.querySelectorAll('*')).find(e => e.children.length===0 && e.textContent.trim() === 'exact label')`), then walk up parents looking for either a `console-header`'s `button.expand-button` (for accordion sections) or the nearest `input[type="checkbox"]`/`input[type="radio"]` (for form fields), and `.click()` that directly via `javascript_tool`. Screenshot-coordinate clicking was flaky and inconsistent all session (the same coordinates worked once and failed the next time, even seconds apart) — prefer the DOM-text-match-then-JS-click pattern over `computer` tool coordinate clicks for this specific product.
- **Dashboard checklist accordion sections auto-collapse/re-render** after navigating back to the Dashboard — don't assume a previous session's expand state persists; re-expand and re-locate items each time.
- **Don't self-certify Content rating or Health.** Confirmed this constraint from the equivalent iOS lesson (EU trader status, demo account state) — formal platform certifications are Dan's signature, not Claude's guess.
- **Screencaps taken via `adb shell screencap -p /sdcard/X.png` get auto-indexed into the phone's photo gallery** (confirmed via MediaStore query) and will pollute any photo-picker UI test — always clean up scratch files from `/sdcard/` after driving the device, or better, use `adb exec-out screencap -p > local_file.png` which never touches the device's storage in the first place.

## Relevant Files & Locations

- Play Console: `com.absbyai.app`, developer account "Abs By AI" (org id `7247591650851655945`, app id `4974398073942667839`), login `danroseconsulting@gmail.com` (NOT `dan@absbyai.com` — that's only the in-app contact email, not a Google login).
- iOS listing copy for reference/adaptation: `app-store-assets/LISTING_COPY.md`
- Existing app-store screenshot assets: `app-store-assets/6.9-inch/`, `app-store-assets/6.5-inch/`, `app-store-assets/13-inch-ipad/`
- Live privacy policy (linked from Data safety answers): `https://absbyai.com/privacy`
- Proof/marketing images usable for a feature graphic: `public/img/proof/*.webp`
- Android build/signing details: see memory `android-twa-build-setup.md`
- adb path used this session: `$HOME/Library/Android/sdk/platform-tools/adb`
- Physical test device: Galaxy A14 5G, serial `R92W60LKM2D` (Dan's real phone, was plugged in via USB this session)
- AI_COORDINATION.md → "Queued" section has the standing note to re-check Android internal-testing install; that item is now superseded by this handoff (real device + real generation both confirmed working 2026-08-05).

## Model & Effort Recommendation

This is UI-automation-heavy Play Console configuration work (browser interaction, not code), plus some brand-voice copywriting for the store listing. It doesn't fit neatly into a Codex-vs-Claude split since neither tool's typical "codebase editing" strength is the bottleneck here — the bottleneck is driving an unfamiliar, JS-framework-heavy web console reliably.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — this is what did the work this session, and the DOM-click pattern above should make the remaining Play Console steps faster than this session (which spent significant time discovering that pattern). |
| **If Claude usage is high / approaching a limit** | Still Claude, not Codex — Codex has no browser-automation tool access for this kind of live third-party console work, and the store listing copy is brand-voice work (an always-Claude task type per this skill's own framework). If usage is tight, use Sonnet 5 rather than Opus; this isn't an ambiguous/hard-architecture task, just a long checklist. |

Task-type override: store listing copywriting is explicitly an "always-Claude" task type (brand voice / marketing copy) regardless of usage level — don't hand that specific sub-piece to Codex even opportunistically.

## Starter Prompt for the Next Task

> Continue the Android Play Store public-launch task. Read `handoff-20260805-android-play-store-public-launch.md` in the project root for full context — the app itself is fully verified working (real device, real photo-generation test all passed 2026-08-05), and 8 of 11 Play Console setup items are done this session (Government apps, Financial features, App category/contact details, and the full Data safety questionnaire). Three items remain: Content rating and Health declaration (sit with Dan live for these two — they're his personal certification to Google, don't self-certify), and the Store listing (description, icon, feature graphic, screenshots — this one you can do directly, adapting from `app-store-assets/LISTING_COPY.md` but respecting Android's different size/char requirements). Start by opening Play Console (`danroseconsulting@gmail.com` login, NOT `dan@absbyai.com`) and confirming the checklist still shows 8/11 complete, then ask Dan if he's ready to do Content rating + Health live right now, or wants you to start on the store listing first.
