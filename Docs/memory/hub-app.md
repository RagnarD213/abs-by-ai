---
name: hub-app
description: "The product: trainer, nutritionist, Sleep Coach, native apps, Stripe, Railway, email, SixPackAbs site, deploy traps"
metadata:
  type: reference
---

# App and site internals

Second-level memory index, split out of MEMORY.md on 2026-11-01 so that file loads whole. Same one-line pointers; open the entry before relying on it.

- [Member profile](member-profile.md): users.profile JSONB + quiz
- [Android TWA build](android-twa-build-setup.md): keystore, build command
- [iOS Capacitor app](ios-capacitor-app.md): status, build command
- [iOS App Store](ios-appstore-prep.md): rejection, ASC gotchas
- [Load time](load-time-optimizations.md): local Anthropic key invalid
- [Printify](printify-print-flow.md): print flow, no-crop caveat
- [Inbound email](absbyai-inbound-email.md): dan@absbyai.com to Gmail
- [AI trainer](ai-trainer-membership.md): architecture, endpoints
- [Trainer v3](trainer-v3-ladder.md): 7 stages, tracks, tiers
- [AI Nutritionist](ai-nutritionist.md): meal prep, GLP-1 mode
- [Sleep Coach](sleep-coach.md): Go Hard briefing endpoints
- [Supplement Audit](supplement-audit.md): photo stack audit, evals, original plan
- [Progress Log](progress-log.md): shipped; Resend key unset
- [My Transformations](my-transformations.md): gallery, slider, share
- [Next-phase plan](next-phase-plan.md): Phase 3 roadmap
- [Coach Brief](daily-coach-brief.md): /api/coach/brief, caching
- [Native retest](cross-platform-retest-rule.md): flag after web deploys
- [Store fixes](platform-scoped-compliance.md): that platform only
- [Native IAP](native-app-iap-gating.md): purchases hidden in apps
- [Female generation](female-generation-fix.md): sex detect, verifier; Gemini + Seedream, men FLUX
- [Member unlimited](member-unlimited-fix.md): fixed, no cap
- [Store policy](app-store-policy-verify-first.md): read docs before advising
- [Bake-off look](bakeoff-round1-aesthetic.md): shredded, no tan
- [Play billing](google-play-billing-us-change.md): optional in US
- [Stripe](stripe-trial-end-active-before-charge.md): paid = invoice.paid
- [Deploy holds](deploy-drops-locked-holds.md): push wipes held images
- [index.html](index-html-screen-nesting.md): count div depth
- [Railway API](railway-graphql-and-cron.md): cron, cache traps
- [SPA site](sixpackabs-site-stack.md): WP.com Atomic, SFTP
- [Amazon](amazon-associates-account.md): danrosefit-20
