# Handoff: Account-deletion feature (App Store compliance)

**Date:** 2026-07-22
**Project:** Abs By AI
**Business goal this serves:** App adoption (unblocks iOS App Store submission) → profitability

## Objective

Add a "Delete my account" feature so a logged-in member can permanently delete their account and all their data from inside the product. This is required by Apple guideline 5.1.1(v) — any app that lets users create an account must let them delete it in-app — and the iOS app cannot be submitted without it. It is a web-only change (server.js + public/index.html); because both native apps load the live site, deploying it to absbyai.com automatically satisfies the requirement in the iOS Capacitor app AND the Android TWA. It also strengthens the Play Store listing (Google has a matching account-deletion policy).

## Current State

- **No account deletion exists anywhere** — verified 2026-07-22 by grepping server.js and public/index.html; zero hits for any delete-account concept.
- Auth stack: email/password accounts in Postgres `users` table, session tokens in `sessions`. Endpoints live at `server.js` — signup :2687, login :2713, logout :3151, password reset :3104/:3124. `requireAuth` middleware pattern is established.
- **All per-user child tables already have `ON DELETE CASCADE`** (verified in db.js): sessions, meals, saved_preps, programs, meal_plans, counsel_sessions, sleep_entries, transformations, weight_logs, progress_entries, coach_briefs. So a single `DELETE FROM users WHERE id=$1` wipes everything relational. Verify `password_reset_tokens` (db.js:158) and `audit_jobs`/`welcome_images` — if any key on email/user without CASCADE, delete their rows explicitly.
- Membership state lives as added columns on `users` (`stripe_customer_id`, `stripe_subscription_id`, etc. — db.js ~:185). A member may have a LIVE Stripe subscription that must be cancelled, not orphaned.
- Marketing list: subscribers live in `subscribers-data.json` (GitHub-API-persisted JSON — this file IS the database, never untrack it) with a Resend welcome sequence; there is an existing unsubscribe path (`/api/unsubscribe`, HMAC token).
- The member hub UI in public/index.html is where the button belongs (near where "Manage membership" lives; note that button is hidden in native apps via `.app-hide-purchase` — the delete button must NOT be hidden in the app; that's the whole point).

## Key Decisions Already Made

- **Ship before iOS submission** — Dan approved this ordering on 2026-07-22; it's the one near-certain rejection worth fixing preemptively.
- **Web change only, no native code** — both wrappers load the live site, so a Railway deploy delivers it to all platforms.
- **True deletion, not deactivation** — Apple's guideline requires actual account deletion; cascade delete makes this the simple path anyway.
- **Do not build native features preemptively for guideline 4.2** — decided 2026-07-22; submit and react to a 4.2 rejection only if it happens.

## Detailed Plan

1. **Server: `POST /api/auth/delete-account`** in server.js (next to logout, ~:3151), behind `requireAuth` + `authLimiter`. Require the user's current password in the body and verify it against `password_hash` (prevents deletion from a stolen session token).
2. In the handler, in order:
   a. If `stripe_subscription_id` is set and status is active/trialing, cancel the Stripe subscription immediately (`stripe.subscriptions.cancel`). Follow the existing sub-handling patterns around server.js:3901. Tolerate "already canceled" errors.
   b. Remove the user's email from the welcome/marketing sequence in `subscribers-data.json` (reuse the unsubscribe logic rather than duplicating it).
   c. `DELETE FROM users WHERE id=$1` — cascades wipe all feature data. Explicitly delete from any table found without CASCADE in the verification step above.
   d. Do NOT touch `credits-data.json` device balances — credits are device-keyed, not account-keyed, and purchased credits should survive (deleting paid credits would be destructive to the customer).
3. **Client: "Delete account" entry in the member hub** (public/index.html), in the account/settings area near "Manage membership" — visible on web AND native (no `.app-hide-purchase` class). Flow: tap → confirmation screen that states plainly what is deleted (account, transformations, workout/nutrition/sleep/progress data) and that an active membership is cancelled → requires typing password → calls the endpoint → on success clears the local session + `localStorage` account state and returns to the logged-out home with a "Your account has been deleted" toast.
4. PostHog events: `account_delete_started`, `account_delete_confirmed`, `account_delete_completed`.
5. **Verify locally** (pgmem + stubbed Stripe): create user → add meals/program/weigh-in → delete → confirm all rows gone, session invalid, re-signup with same email works. Confirm a user WITH a fake subscription id hits the cancel path.
6. **Deploy + live-verify on absbyai.com**: create a throwaway account, exercise the full UI flow, confirm login afterward fails with "no account". Commit + push per standing workflow (auto-deploys via Railway).
7. Update `AI_COORDINATION.md` and the iOS submission notes: account deletion is done — mention it in App Store Review Notes.

## Things to Avoid / Lessons Learned

- **Never untrack or delete the root `*-data.json` files** — they are the persistence layer (GitHub-API persisted). Edit `subscribers-data.json` only through the existing helpers.
- The `.app-hide-purchase` CSS class hides elements inside native apps — do not reuse it (or any `.native-app`-gated hiding) on the delete button.
- Local env has dummy Anthropic/Gemini keys and pgmem — Stripe and AI paths can only be fully verified on prod; structure the Stripe cancel so it's testable with a stub.
- Beta/comp accounts: the beta-revoke code (~server.js:3861) has a status guard so it "can never cancel a real subscription" — read it before writing the cancel logic; don't accidentally invert that protection.
- Single replica, in-memory maps (`freeIpCounts` etc.) — no cross-instance concerns.

## Relevant Files & Locations

- `server.js` — auth endpoints :2687–:3151, Stripe sub handling ~:3901, beta revoke ~:3861
- `db.js` — schema; users :36, cascades throughout, membership columns ~:185
- `public/index.html` — member hub UI, `IS_NATIVE_APP` / `.app-hide-purchase` gating
- `subscribers-data.json` — marketing list (root, DO NOT untrack)
- Deploy: push to `main` → Railway auto-deploy → verify at https://absbyai.com
- `AI_COORDINATION.md` — update on start and completion

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Codex flagship (current version), **medium** effort |

This is routine, well-specified implementation work — no Anthropic-API code, no copywriting, no open architecture questions. One caution regardless of model: it deletes production data and touches live Stripe subscriptions, so hold whichever model you use to the verification steps (5–6) before calling it done. If the Stripe-cancel interaction turns out messier than expected, escalate effort rather than starting higher.

## Starter Prompt for the Next Task

> Read `handoff-20260722-account-deletion.md` in the Abs By AI project root, plus `AI_COORDINATION.md` (claim the task, Owner = your name). Build the account-deletion feature exactly as specified: `POST /api/auth/delete-account` (password re-check, Stripe sub cancel, subscriber-list removal, cascading user delete) and a member-hub delete flow visible on web and native apps. Start by verifying which tables lack `ON DELETE CASCADE` (check `password_reset_tokens`, `audit_jobs`, `welcome_images` in db.js), then implement server-side first. Verify locally on pgmem, then deploy and live-verify on absbyai.com with a throwaway account. Commit + push per project workflow.
