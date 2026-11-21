# Handoff: iOS App Store submission prep (walkthrough, screenshots, listing copy, demo account)

**Date:** 2026-07-22
**Project:** Abs By AI
**Business goal this serves:** Adoption (getting the iOS app into the App Store), with profitability close behind (physical print sales + funnel reach).

## Objective

Get everything that does NOT depend on Apple Developer enrollment approval finished now, so that the moment Apple approves the enrollment, Dan only has to do the clicks Apple requires of him (signing, listing form paste, archive/upload, submit). Five tasks, all executable by Claude without approval:

1. **Finish the simulator walkthrough** — features not yet checked inside the app shell: AI Trainer, AI Nutritionist, Sleep Coach, Progress Log, Daily Coach Brief, My Transformations, the print/poster purchase flow, and native share/save.
2. **Take App Store screenshots** at the required sizes (6.9" and 6.5" iPhone classes).
3. **Draft all App Store Connect listing copy** — description, keywords, promo text, age-rating questionnaire answers, App Privacy declarations, and App Review Notes.
4. **Privacy policy** — ✅ already verified: `https://absbyai.com/privacy` returns 200 OK (checked 2026-07-22). Nothing to do unless a re-check fails.
5. **Set up a demo account with comp membership** for the Apple reviewer.

## Current State

- **Environment is ready.** Xcode 26.6 (build 17F113) installed at `/Applications/Xcode.app`, `xcode-select` pointing at it. An **iPhone 17 Pro (iOS 26.5) simulator is booted** (UDID `A43844F9-3EA4-4EB3-B21D-9F8945317C94`). The macOS 26 upgrade blocker from `HANDOFF_iOS_APP_PLAN.md` is resolved.
- **The app builds and runs.** Capacitor 8 wrapper in `ios-app/`, app ID `com.absbyai.app`, loads `https://absbyai.com` live. Build command:
  `cd ios-app && npx cap sync ios && xcodebuild -project ios/App/App.xcodeproj -scheme App -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build`
- **Walkthrough is partially done** (session of 2026-07-22). Verified so far: app launches, site loads, core transform flow works. **Not yet checked:** Trainer, Nutritionist, Sleep Coach, Progress Log, Coach Brief, Transformations gallery, Supplement Audit, print/poster checkout reachability, native share/save (Capacitor Share/Filesystem), keyboard behavior on the AI-feature forms, and the new account-deletion flow.
- **Purchase gating shipped July 14** (`native-app` CSS class + JS early-returns): credit packs, membership plans, and manage-membership are hidden in the app; physical print checkout stays. This is the App Store compliance linchpin — re-verify it during the walkthrough.
- **Account deletion shipped 2026-07-22** (Apple guideline 5.1.1(v) requirement): Member hub → Account → Delete my account. It deliberately stays visible inside the native app (verified in browser with `.native-app` forced; not yet seen in the actual simulator).
- **Apple Developer enrollment:** submitted, awaiting Apple's approval (24–48 hr typical). Nothing in this handoff waits on it — that's the point.
- **Reference docs:** `HANDOFF_iOS_APP_PLAN.md` (the master phased plan — this handoff executes its Phases 3, 5, and 7 prep), `HANDOFF_iOS_APP_STORE.md` (older, superseded, kept for App Store Connect field reference).

## Key Decisions Already Made

- **Ship the existing Capacitor wrapper** — no native rebuild. (Locked 2026-07-14.)
- **Individual Apple Developer enrollment** ($99/yr) — no D-U-N-S needed.
- **Digital purchases stay hidden in-app**; the app sells only physical prints via Stripe (compliant under 3.1.3(e)). Never remove the gating.
- **App name "Abs by AI"**, bundle `com.absbyai.app`, SKU `absbyai-ios`, category Health & Fitness, privacy URL `https://absbyai.com/privacy`.
- **Answer the age-rating questionnaire honestly** about body-image content; 12+/17+ is acceptable — don't game it.
- **Demo account for the reviewer**: a normal user row granted `membership_status='comp'` via the existing admin beta-members endpoint — no new code needed.

## Detailed Plan

### Task 1 — Finish the simulator walkthrough

Use the iOS Simulator MCP tools (`attach` first so Dan can watch if he's around, then `screenshot`/`tap`/`text` for headless verification). The app loads **production** absbyai.com — see cautions below about real AI spend.

Check each of these inside the app shell, logged in as the demo/comp account (create it first — Task 5 — so member features are unlocked):

1. **AI Trainer** — intake wizard renders, keyboard doesn't cover inputs, a program loads, day rows/pills render, stick figures visible.
2. **AI Nutritionist** — intake pre-filled from profile, plan renders.
3. **Macro Tracker** — photo upload from the simulator photo library works (this exercises the same photo path the transform uses).
4. **Sleep Coach** — check-in form + briefing render.
5. **Progress Log** — weigh-in entry, charts render inside safe areas.
6. **Daily Coach Brief** — hub card renders.
7. **My Transformations** — gallery, slider, and **share** (this is the native-share test: Capacitor Share sheet must appear, not a browser fallback).
8. **Supplement Audit** — form renders; do NOT run a full 12-item audit (8-min worst case, real Anthropic spend) — one small run or render-only is enough.
9. **Print/poster flow** — product selector reachable from a result and from the hub; stop at the Stripe checkout screen (do not pay).
10. **Purchase gating re-verify** — no credit packs, no membership plan cards, no manage-membership anywhere; neutral "not available in the app" notes show instead.
11. **Account deletion** — Member hub → Account → Delete my account is visible and opens its confirmation (cancel out; don't delete the demo account).
12. **Native save-to-photos** — save a result image; confirm it lands in the simulator photo library.
13. **General shell checks throughout:** safe areas (nothing under the notch/home indicator), status-bar color, splash, no white flash, keyboard `resize: native` behavior.

Fix anything broken (most likely: safe-area CSS on post-June features that have never been seen in the shell). Fixes are web-side (`public/index.html`) → commit, push, verify on absbyai.com, then just reload the app — no rebuild needed unless native config changes.

### Task 2 — App Store screenshots

- **Required sizes:** 6.9" class (iPhone 17 Pro Max, 1320×2868) and 6.5" class (1242×2688 — boot an iPhone 11 Pro Max-class simulator, or scale). The currently booted iPhone 17 Pro is neither — boot an **iPhone 17 Pro Max** simulator for the 6.9" set:
  `xcrun simctl boot "iPhone 17 Pro Max"` then install/launch the app on it.
- Capture with `xcrun simctl io <udid> screenshot <file>.png`.
- **Shots to take (5–8):** hero/upload screen, a finished transformation result (use the proof-photo assets, NOT real user photos), AI Trainer workout view, Macro Tracker, Daily Coach Brief / member hub, print product selector, Transformations gallery.
- Save to a new `app-store-assets/` folder in the project root so they're findable at upload time.
- Screenshots must show the comp/demo account or logged-out states — no real personal data, no real emails visible.

### Task 3 — Listing copy (draft everything, save as one paste-ready doc)

Write `app-store-assets/LISTING_COPY.md` containing, clearly sectioned:

1. **App name** (30 chars max): "Abs by AI" + optional subtitle (30 chars) — e.g. positioning around AI fitness transformation + coaching.
2. **Promotional text** (170 chars, editable without review).
3. **Description** (4000 chars) — lead with the photo transformation, then the six AI coaching features (Trainer, Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit, Daily Brief), then prints. Brand voice: direct, motivating, no medical claims.
4. **Keywords** (100 chars, comma-separated, no spaces after commas).
5. **Age-rating questionnaire answers** — honest answers for body-image/appearance content; expect 12+ or 17+.
6. **App Privacy declarations** — declare: PostHog analytics (usage data, identifiers); photos processed for AI transformation (**verify current backend retention behavior in `server.js` before writing the answer** — transformations/welcome_images ARE stored for members; say so accurately); account data (email) for the member hub; purchase info via Stripe for physical goods.
7. **App Review Notes** — must include: (a) everything purchasable in-app is a physical product (Printify prints) via Stripe, compliant under 3.1.3(e); digital credits/membership are not offered or purchasable in the app; (b) native features per guideline 4.2 (photo-library integration, native share/save, haptics, keyboard/safe-area handling); (c) safety: refuses photos of minors (REFUSED_MINOR guard) + generation moderation; (d) **account deletion path: Member hub → Account → Delete my account** (reviewers look for this); (e) the demo account credentials from Task 5.

### Task 4 — Privacy policy

Done — `https://absbyai.com/privacy` returned 200 on 2026-07-22. Optionally re-check with `curl -sI https://absbyai.com/privacy | head -1` before submission day, and skim the page to confirm it actually mentions photos, analytics, and account data (the App Privacy answers must not contradict it).

### Task 5 — Demo/reviewer account

1. Sign up a fresh account on `https://absbyai.com` — suggested email: `danroseconsulting+applereview@gmail.com` (deliverable, keeps reviewer traffic identifiable). Generate a strong password and record it ONLY in `app-store-assets/LISTING_COPY.md` (it must go into App Store Connect's review sign-in fields anyway; the repo is private).
2. Grant comp membership via the existing admin endpoint: log in to `absbyai.com/admin` with an `ADMIN_EMAILS` account and add the email under beta members (server: `POST /api/admin/beta-members`, sets `membership_status='comp'`, `membership_plan='beta'`). **OPEN:** Claude needs Dan's admin login to do this via the API, or Dan does this 30-second grant himself in the admin UI — flag whichever at execution time.
3. Log the demo account in inside the simulator and pre-populate it lightly (one transformation using a proof photo, one Trainer program) so the reviewer lands on a living app, not empty states. This doubles as walkthrough coverage.
4. Verify with the account: member hub loads, all six AI features accessible, no payment wall anywhere in-app.

### Ordering

Task 5 first (the walkthrough needs a member account) → Task 1 (fix anything broken) → Task 2 (screenshots of the now-verified screens) → Task 3 (copy, informed by what the walkthrough confirmed). Task 4 is done.

## Things to Avoid / Lessons Learned

- **The app hits PRODUCTION.** Every generation, Trainer program, and audit run in the simulator is real Anthropic/Gemini spend and real PostHog events. Test each feature once, not repeatedly; skip the full 12-item Supplement Audit.
- **Do not complete any Stripe payment** during the print-flow check — stop at the checkout screen.
- **Never remove or weaken the purchase gating** (`app-hide-purchase` class + `IS_NATIVE_APP` early-returns in `public/index.html`) — it is the compliance mechanism.
- **Don't delete the demo account** when testing the deletion UI — cancel at the confirmation step. (Deletion cancels Stripe first and is permanent.)
- **Local env has dummy Anthropic/Gemini keys** — AI output can only be judged against prod, which is what the app loads anyway.
- **Simulator MCP edge-gesture quirk:** swipes starting within 4pt of a screen edge trigger OS gestures (back/home/Control Center), not scrolls — start drags well inside the bezel.
- Web-side fixes deploy via the normal flow (commit → push to `main` → Railway auto-deploy → verify on absbyai.com) and reach the app instantly. A new Xcode build is only needed for native changes (plugins, icons, config).
- Prior rejection risk analysis (Phase 8 of `HANDOFF_iOS_APP_PLAN.md`): 4.2 minimum-functionality is the biggest risk; the pre-planned fallback is adding push notifications for the Daily Coach Brief.

## Relevant Files & Locations

- `ios-app/` — Capacitor wrapper (`capacitor.config.json`, `ios/App/App.xcodeproj`)
- `public/index.html` — the entire web app incl. native-integration script and purchase gating
- `server.js` — admin beta-members endpoint ~line 3881; REFUSED_MINOR guard; account-deletion endpoint
- `HANDOFF_iOS_APP_PLAN.md` — master phased plan (this handoff = Phases 3/5/7 prep)
- `HANDOFF_iOS_APP_STORE.md` — older reference for App Store Connect fields
- `app-store-assets/` — CREATE THIS: screenshots + `LISTING_COPY.md`
- Booted simulator: iPhone 17 Pro, iOS 26.5, UDID `A43844F9-3EA4-4EB3-B21D-9F8945317C94`
- Live site: `https://absbyai.com` · Admin: `https://absbyai.com/admin` (needs `ADMIN_EMAILS` account) · Privacy: `https://absbyai.com/privacy`
- App Store Connect (once enrolled): `https://appstoreconnect.apple.com`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking, for the whole batch (walkthrough + screenshots + demo account are routine; it can competently draft the copy too) |
| **If Claude usage is high / approaching a limit** | Split it: Codex (flagship, medium effort) for Tasks 1, 2, 5 (routine simulator/verification work) — but keep **Task 3 (listing copy) on Claude** (cheapest competent model, Sonnet 5) |

Task-type override: the App Store listing copy is marketing/brand-voice writing — always-Claude regardless of usage. No part of this touches the Anthropic API integration code, so nothing else forces Claude.

## Starter Prompt for the Next Task

> Read `handoff-20260722-ios-appstore-submission-prep.md` in the Abs By AI project root and execute it. Goal: finish all pre-enrollment App Store submission prep — (1) complete the iOS simulator walkthrough of the features listed, (2) take 6.9" and 6.5" App Store screenshots into `app-store-assets/`, (3) draft all listing copy into `app-store-assets/LISTING_COPY.md`, (5) create the Apple-reviewer demo account with comp membership. First concrete action: create the demo account (Task 5, steps 1–2 — ask Dan to do the 30-second comp grant at absbyai.com/admin if you don't have admin credentials), then start the simulator walkthrough with the Xcode 26.6 / iPhone 17 Pro simulator that's already set up. Remember the app hits production — one test per AI feature, no completed payments, and don't actually delete the demo account when testing the deletion UI.
