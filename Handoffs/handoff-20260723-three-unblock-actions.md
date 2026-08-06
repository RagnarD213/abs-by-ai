# Handoff: Walk Dan through the 3 quick unblocking account actions

**Date:** 2026-07-23
**Project:** Abs By AI
**Business goal this serves:** App adoption (iOS + Android launch) → profitability

## Objective

Guide Dan, step by step and one task at a time, through three short actions that only he can do (they need his personal accounts). Each one unblocks a bigger piece of work Claude Code then finishes on its own. This is a **walkthrough/concierge task, not a coding task** — the assistant's job is clear click-by-click instructions, checking Dan's result at each step, and telling him the exact next-session prompt when a task unblocks. Dan is non-technical: plain language, one step at a time, confirm before moving on.

The three tasks (any order; Task B first is smartest because it starts a 72-hour clock at Google):

- **A. Apple:** check whether Apple Developer Program enrollment is approved.
- **B. Google Play:** click "Verify email address" in the Play Console to finish the paused account conversion.
- **C. Replicate:** put a Replicate API token into Railway as `REPLICATE_API_TOKEN`.

## Current State

- **iOS is 100% prepared for submission** — screenshots (`app-store-assets/6.9-inch/`, `6.5-inch/`), listing copy + review notes (`app-store-assets/LISTING_COPY.md`), reviewer demo account created and pre-populated, simulator walkthrough passed. The ONLY blocker is Apple Developer enrollment approval (Dan already enrolled and paid; approval usually takes 24–48 h).
- **Android app is built and signed** (`android/app/build/outputs/bundle/release/app-release.aab`); the website-verification fix is live. Blocker: Dan's Play Console Personal→Organization conversion is paused on a "confirm how Google should contact you" screen. The org contact email must be on the company domain — `dan@absbyai.com` — and that mailbox's forwarding to `danroseconsulting@gmail.com` was **fixed and verified 2026-07-22**, so the verification email will now arrive. After conversion completes, Google imposes a **72-hour wait** before the app file can be uploaded.
- **Generation upgrade (two AI models compete, a judge picks the winner) is fully coded and live** in single-model fallback mode (commits `ab3cc97`, `c7cb4da`). It activates the moment `REPLICATE_API_TOKEN` exists in Railway. Dan already chose Replicate over BFL-direct and already has a Replicate account (shared with another task). Cost ≈ $0.04/image.
- All three tasks are on Dan's dashboard as "key" priority items (in `todos.json`, pushed to main).

## Key Decisions Already Made

- **Replicate, not BFL direct** — Dan's call 2026-07-22 (account reuse). Code supports both; `BFL_API_KEY` would win if both were ever set, so only set the Replicate one.
- **Apple enrollment: Individual** (already submitted — nothing to change, just check status).
- **Play Console: converting Personal→Organization** (already in progress — do not restart it, just complete the email verification).
- **Task B before the others if Dan asks for an order** — it starts Google's 72-hour clock.

## Detailed Plan

### Task B — Play Console email verification (~5 min, do first)

1. Go to https://play.google.com/console and sign in with Dan's Google account.
2. Find the paused account conversion — the screen titled roughly **"Confirm how Google should contact you"** (it may appear as a banner/notification about completing the switch to an organization account).
3. The contact email field should show **dan@absbyai.com**. Click **"Verify email address."**
4. Google sends a verification email to dan@absbyai.com, which forwards to **danroseconsulting@gmail.com**. Have Dan check that Gmail inbox (and Spam) — it should arrive within a few minutes. This WILL work: the forwarder was tested 2026-07-22. (A past false alarm: self-sent test emails from that same Gmail address get silently dropped by Gmail — Google's email is from Google's servers, so that issue does not apply.)
5. Dan clicks the verification link in the email. Confirm the Play Console shows the conversion progressing/complete.
6. **Write down the completion date** — the `.aab` upload can happen **72 hours after** the organization conversion completes. Add it to the dashboard or tell Claude Code so it gets scheduled.

### Task A — Apple Developer enrollment check (~3 min)

1. First check email: search Dan's inboxes for **"Welcome to the Apple Developer Program"** or anything recent from developer.apple.com.
2. Or check directly: go to https://developer.apple.com/account and sign in with Dan's Apple ID. If the Account page shows an active **Apple Developer Program** membership (team name, membership expiration date), enrollment is approved. If it still says "enrollment pending/processing," it isn't.
3. **If approved:** the iOS submission is unblocked. Tell Dan to start a Claude Code session in the Abs By AI project with the starter prompt in `AI_COORDINATION.md` context, e.g.: *"Apple Developer enrollment is approved. Start the iOS App Store submission — signing in Xcode, App Store Connect listing from app-store-assets/LISTING_COPY.md, screenshot upload, archive, upload, submit."*
4. **If still pending after 48+ hours since payment:** have Dan contact Apple Developer Support at https://developer.apple.com/contact/ (phone callback is fastest). Sometimes they're waiting on identity verification — check for an email requesting ID.

### Task C — Replicate token into Railway (~5 min)

⚠️ **Credential rule for the assistant running this:** never ask Dan to paste the token into chat, and do not type it anywhere for him. Two tokens pasted into chat in the past had to be rotated. Dan copies and pastes it himself, directly from Replicate into Railway.

1. Go to https://replicate.com and sign in (account already exists).
2. Click the account menu (top right) → **API tokens** (or go to https://replicate.com/account/api-tokens).
3. Create a token if none exists (name it something like `absbyai-prod`) and click **Copy**. It starts with `r8_`.
4. In a new tab, go to https://railway.app → open the **Abs By AI** project → click the web service → **Variables** tab.
5. Click **New Variable**. Name: `REPLICATE_API_TOKEN` (exactly that, all caps). Value: paste the token. Save/deploy — Railway redeploys automatically (takes ~1–2 min).
6. Done. Tell Dan the two-model generation upgrade is now armed, and that his next Claude Code session should verify it: *"REPLICATE_API_TOKEN is set in Railway. Run real two-model prod generations on the proof photos to verify the ensemble + chooser end-to-end"* (this is the recorded next action in `AI_COORDINATION.md`, generation-overhaul section).

### Wrap-up

7. When each task finishes, Dan checks it off on his dashboard (the three items are "key" priority under Business).
8. If all three land: the ideal next Claude Code session does the full iOS submission (if Apple approved) and verifies the Replicate ensemble; Android upload gets scheduled for 72 h after the Play conversion completed.

## Things to Avoid / Lessons Learned

- **Never paste API tokens/keys into chat** — they end up needing rotation. Dan handles secrets directly in the provider dashboards.
- Do NOT set `BFL_API_KEY` — Replicate is the chosen path; BFL would override it.
- Play Console: do not restart or change the account conversion — only complete the email verification on the existing paused flow.
- Namecheap/forwarding is already fixed — if the Google email doesn't arrive, wait and re-check Spam before assuming the forwarder broke (it was verified working 2026-07-22).
- Gmail drops self-sent test emails to dan@absbyai.com (duplicate Message-ID) — don't "test" the forwarder that way.
- The 72-hour Google wait is real — don't have Dan try to upload the `.aab` early.

## Relevant Files & Locations

- `AI_COORDINATION.md` (project root) — full status of all three blocked work streams.
- `app-store-assets/LISTING_COPY.md` — everything for App Store Connect (copy, keywords, review notes, demo-account credentials).
- `android/app/build/outputs/bundle/release/app-release.aab` — the signed Android build to upload after the 72-h wait.
- `HANDOFF_ANDROID_INTERNAL_TESTING.md` — the full Play Console upload walkthrough for after the wait.
- Dashboards/accounts: developer.apple.com/account · play.google.com/console · replicate.com/account/api-tokens · railway.app (Abs By AI project → Variables).
- Env var name (value stays secret): `REPLICATE_API_TOKEN`.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Haiku 4.5, no extended thinking — this is a click-by-click walkthrough, the cheapest model handles it fine |
| **If Claude usage is high / approaching a limit** | Same — Claude Haiku 4.5. (Codex is a coding tool; wrong fit for an interactive account walkthrough) |

If a task goes sideways (e.g., Apple enrollment stuck, Play Console shows an unexpected screen), escalate that one question to Sonnet 5 rather than pushing Haiku through ambiguity.

## Starter Prompt for the Next Task

> Read `handoff-20260723-three-unblock-actions.md` in this project. Walk me through the three account tasks in it, one at a time, starting with Task B (Play Console email verification). I'm non-technical — give me one small step at a time, wait for me to confirm each step before the next, and never ask me to paste any password, token, or key into this chat. When a task is done, tell me exactly what to say to Claude Code in my next work session to cash it in.
