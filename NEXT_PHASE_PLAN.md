# Abs by AI — Full Audit + Next Phase Plan (July 10, 2026)

## Part 1 — What exists today (audit)

Everything below is built, committed, and deployed to absbyai.com unless noted.

**Core product**
- AI body-transformation image generation (Gemini) with credit paywall: 3 free per device, Starter 5/$4.99, Power 20/$14.99, generate-and-lock reveal, Stripe embedded checkout.
- Printed products (canvas / poster / keychain) via Printify + Stripe, aspect-aware no-crop placement. **Never live-tested with a real order.**

**Accounts & membership**
- Email/password accounts (Postgres on Railway), 90-day sessions, member hub with before/after hero and feature tiles.
- Password reset flow (Resend) — **built but dead until `RESEND_API_KEY` is set + domain verified.**
- Membership: $9.99/mo / $59.99/yr Stripe subscriptions, credit-conversion discount, webhook sync, billing portal + "Manage membership" hub card (shipped today), welcome email + FAQ copy done.

**AI features (all membership-gated with free previews)**
- AI Trainer: 9-step intake → personalized program, check-ins regenerate next block.
- AI Nutritionist: meal-prep plans from photo gap, GLP-1 floor mode, swap/check-in.
- Macro tracker: photo meal analysis, 3 free then credit-gated; meal eval harness in `eval/`.
- Sleep Coach: manual or screenshot check-in → "GO HARD" briefing; sleep context feeds trainer + nutritionist prompts.
- Decision Counsel: 5-seat AI panel, 10 sessions/month cap.
- Weight & Progress Log: trends, photos, AI recap; weight context feeds other features.
- My Transformations: gallery, share composite, hero swap, program rebuild, per-card print.

**Growth/infra**
- Email capture → MailerLite (live, synced). Autoresponder copy (8 emails) written in `EMAIL_MARKETING_PLAN.md` — **automation not built in MailerLite yet.**
- Per-user push reminders (weigh-in, photo day, Sunday meal prep, Mon/Wed/Fri workout).
- PWA + Android TWA (built, signed) + iOS Capacitor wrapper (**blocked on Xcode 26 install**).
- PostHog analytics events across all funnels. iOS purchase-strategy memo done (`HANDOFF_ios_iap.md` — recommends external purchase link, not Apple IAP).

---

## Part 2 — Open items (prioritized)

### 🔴 P0 — Revenue is blocked until these are done

**DAN (only you can do these):**
1. **Stripe live mode**: live `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` / `STRIPE_WEBHOOK_SECRET` on Railway; webhook endpoint registered for `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`. Without the last two, cancellations never downgrade members.
2. **Resend**: create account, set `RESEND_API_KEY` + `RESET_FROM` on Railway, verify absbyai.com sending domain. Until then password-reset emails silently don't send.

**CLAUDE (after Dan's #1):**
3. Full prod verification of the paid path (subscribe → every gate opens → cancel → gates close), incl. the untested flows: member full meal plan, Counsel photo direction, program rebuild, progress recap, credit-pack purchase from the meal wall, Counsel 11th-session 429. Write `PROD_VERIFICATION_LOG.md`. (This is `HANDOFF_membership_opus_medium.md` Part A.)

### 🟠 P1 — Growth engine + app stores

**DAN:**
4. MailerLite (all in their web UI): build the automation with Emails 1–5 from `EMAIL_MARKETING_PLAN.md`, authenticate domain (SPF/DKIM), send one real test to yourself. Trial started July 3 — clock is ticking.
5. One real Printify test order per product type (confirm heads aren't cropped).
6. Apple: enroll in Apple Developer Program ($99/yr), confirm macOS 26 upgrade done, install Xcode 26.4. Sign off on the external-purchase-link recommendation in `HANDOFF_ios_iap.md`.

**CLAUDE:**
7. iOS: once Xcode is in — simulator build, native integration test, external purchase link button, App Store assets/submission prep.
8. Counsel marketing page + MailerLite announcement email.
9. PostHog funnel review: where do people drop between landing → generate → signup → subscribe (I can query PostHog directly).

### 🟡 P2 — Polish / hardening

**CLAUDE:**
10. Optional Fable entitlement/payment-race audit (`HANDOFF_membership_fable_high.md`) — run after go-live.
11. Exercise demo videos: all 77 exercises have `video: null` (button hidden until filled).
12. Verify push-reminder sweep fires at correct local times on prod.
13. Legal pass on Counsel/Sleep disclaimers.
14. Google sign-in (deferred; password reset covers the main lockout risk once Resend is live).

---

## Part 3 — Next-phase feature ideas (researched brainstorm)

Research context: fitness apps average ~9% monthly churn and 90%+ 30-day abandonment; the #1 churn driver is loss of motivation. What measurably works: **streaks with social visibility, day-one achievements, time-limited challenges for lapsed users, and adaptive AI that reacts to sleep/recovery data** — that last one we already do better than most.

### Theme A — "One daily loop" (the big retention unlock)
Right now the app is six great silos. The next phase should unify them into one daily habit.

1. **Daily Coach Brief (flagship idea).** One home-screen card each morning, one AI voice: last night's sleep verdict + today's workout + today's macro targets + weight trend + one focus sentence. Every data source already exists server-side (`getTodaysSleep()`, `getWeightContext()`, program day, meal plan). This turns "six tools" into "my coach" and gives a reason to open the app every single day.
2. **Streaks + achievements.** Log-anything streak (workout, meal, weigh-in, sleep all count), milestone badges, weekly consistency score on the hub. Day-one achievement ("First workout logged 🏆") — research shows this has the highest early-retention impact.
3. **Sunday Report email.** Auto-generated weekly recap (weight trend, workouts done, macro adherence, next week's focus) sent via Resend/MailerLite. Pulls people back weekly and showcases membership value. Pairs with the existing Sunday meal-prep push.

### Theme B — Weaponize the goal image (our unique asset)
No competitor has a literal AI-generated picture of the user's goal body.

4. **"Distance to goal" score.** Claude vision compares the latest progress photo to the goal render → "You're ~40% of the way to your goal physique" with a progress bar on the hub. Insanely motivating, technically cheap (one vision call), totally unique.
5. **Transformation time-lapse video.** Stitch progress photos (+ goal image as the final frame) into a shareable morph clip with branding. Viral loop; share composites already exist.
6. **Milestone re-render.** Every 10 lbs lost, offer a fresh goal image from the newest photo — a natural credit/generation sink and a "look how far you've come" moment.

### Theme C — Growth mechanics
7. **Referral program.** Share your transformation → friend signs up → you both get a free generation (or a free week of membership). Credits infra already supports granting.
8. **30-Day Ab Challenge.** Time-limited challenge with daily check-ins, its own streak, and a completion badge + discount offer. Research: time-limited challenges are the best tool for re-engaging lapsed users. Also a natural YouTube/ads tie-in.
9. **Win-back automation.** No log in 5 days → push + email ("Your coach noticed you've been quiet") with a one-tap re-entry. Uses existing push + MailerLite.

### Theme D — Utility deepeners (cheap wins)
10. **Grocery list from meal plan.** One tap → consolidated shopping list (copy/share/print). Trivial to build, huge perceived value, makes the meal plan actually get cooked.
11. **Barcode/label scan in macro tracker.** Photo of nutrition label → parsed macros (Claude vision already reads screenshots for Sleep Coach).
12. **Apple Health / wearable sync (iOS phase 2).** Auto-import sleep + steps + weight via Capacitor HealthKit — removes manual entry friction and feeds every AI feature. Sleep Coach Phase 3 already anticipated this.
13. **Coach Chat.** A persistent conversational thread with full context (program, meals, sleep, weight) — "ask your coach anything." The membership anchor feature long-term; medium build.

### Recommended Phase 3 package (in order)
1. ✅ Daily Coach Brief (A1) — SHIPPED July 14: `/api/coach/brief` + hub card (facts free, coach text members-only, cached per user-day). Verified on prod.
2. Streaks + achievements (A2) — partially done: trainer streak + streak strip on the brief card (July 14); milestone badges/day-one achievement still open
3. Distance-to-goal score (B4)
4. ✅ Grocery list (D10) — already existed in the Nutritionist recipe cards (checkboxes + copy button)
5. Sunday Report email (A3) — once Resend is live
6. Referral program (C7)

Then: 30-Day Challenge + time-lapse video as the marketing wave for the YouTube launch.
