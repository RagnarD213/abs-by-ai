# Member email and failed-payment recovery, November 14, 2026

Owner: Codex. Dan requested live checks and autonomous fixes in the existing Stripe/Resend/app setup.

## Verified findings

- Stripe automatic successful-payment/refund receipts were also OFF; enabled both.
- Stripe failed-card and expiring-card emails were OFF. Enabled both, with Stripe-hosted card-update destinations. Smart Retries already enabled: eight attempts in two weeks; existing cancellation-after-exhaustion policy retained.
- Enabled payment-authentication emails and existing 3/5/7-day reminders when required, without changing 3DS enforcement or billing outcomes. Added customer-portal management links to subscription emails.
- Two recent $19.99 invoices remained past due: one insufficient-funds decline and one transaction-not-allowed decline requiring customer action. An older third invoice belongs to an already-canceled subscription and is excluded from catch-up follow-up. No manual charges or invoice changes authorized or needed.
- Resend dashboard: absbyai.com verified; recent account/password setup emails delivered, including both recent failed-payment customers. Existing API key is send-only, so provider delivery verification uses the signed-in Dashboard instead of expanding key permissions.
- Live WELCOME_ENABLED=true, ROOT-domain sender verified. Generic prospect sequence contains outdated credit-pack offers; members must be removed from that sequence.
- Trial-ending reminders are intentionally OFF (Dan's September 30 direction, recorded in server.js). Preserved. Earlier chat said the reminder was built, but did not establish that it was enabled.

## Implementation

- `member-emails.js`: durable paid-member enrollment and delivery ledger; welcome, day 2, day 7, then weekly product-use emails. Day-2 content checks whether a workout program already exists. No upsells, private health metrics or images in email.
- Sends only to active, unexpired members with confirmed paid enrollment, honors prior marketing unsubscribes, excludes example test addresses, adds signed member-specific unsubscribe (GET and one-click POST). Billing notices remain independent.
- Lease + fixed Resend idempotency key/body prevent duplicate concurrent delivery. Advance only on provider acceptance; recover interrupted advancement; uncertain attempts older than dedupe window are held for review.
- Paid Stripe invoice/lifetime/Apple trial-conversion hooks enroll. Periodic reconciliation verifies Stripe paid invoices or the lifetime paid ledger, recovering lost/out-of-order events and catching up existing paying members. Active status alone never qualifies.
- Account-access emails explain the actual membership stage and one-time lifetime price and point buyers to AI Trainer. Removed false new-trial assumptions for active returning buyers; added reply-to support.
- Prospect welcome sequence stops for members, including trials and past-due members, preventing obsolete credit-pack pitches.

## Validation

- Member-email tests: eligibility, payment enrollment, concurrent sweeps, timing, failure retry, immutable request, opt-out, interrupted sequence advance and uncertain-old-send hold.
- Cart/fulfillment suite: 133 passed, 0 failed (including unpaid/zero-dollar exclusions, positive-payment enrollment, lifetime email copy and one-click unsubscribe).
- Subscriber suite: 42 passed, 0 failed.
- Syntax and diff whitespace checks passed.

## Live rollout

Implementation commit `9f9e346` pushed from an isolated clean worktree because unrelated live edits blocked the shared checkout. Railway deployment `29beea98-fa8f-468e-9522-a762e55eb8e2` succeeded at approximately 20:03 UTC. `MEMBER_EMAILS_ENABLED=true` is live.

The two recent past-due members each received one catch-up billing email using the existing secure portal. Resend Dashboard shows both DELIVERED. Provider IDs: `01a1dba3-764f-70f0-b077-283bb3f5c13d`, `01a1dba3-79fb-76ca-8c6b-f3b5a237703a`. Durable delivery keys are `billing-recovery-start/<invoice id>` in Postgres. No charges retried manually.

First production sweep ran at 20:04:59 UTC. Five paid accounts enrolled and advanced to step 1, with next emails due November 16; these are three customer accounts and two Dan-owned membership accounts. All five welcome emails show DELIVERED in Resend. No failed/blocked member deliveries. Past-due users 60/61 remained outside the paid sequence.

Live unsubscribe tests: invalid token returns HTTP 400; a valid signed POST for nonexistent test ID 0 returns HTTP 200, without changing any member. Actual opt-out mutation and timing/cancellation exclusions passed fixture tests. The app health endpoint returns HTTP 200.

An older active annual account (user 8) has no linked subscription, no confirmed paid marker and no matching Stripe customer by its saved email. It was excluded; membership access was not changed. Apple demo accounts and example test users also did not enroll.

The new tables were created idempotently in production before recording the billing catch-up deliveries. The deployment re-used those same tables. Member product-use emails do not contain health measurements, photos or the owner's private mailing address.

Evidence: `/tmp/stripe-recovery-enabled-20261114.jpg`, `/tmp/stripe-receipts-enabled-20261114.jpg`, `/tmp/absbyai-recovery-delivered-20261114.jpg`.

## Owner correction: generic sequence disabled

Dan rejected the generic workout reminders and repeating weekly check-ins on November 14 as unwanted AI notifications. He will design a more sophisticated sequence in another task. Keep the welcome/account-access/billing messages; do not reactivate day-2/day-7/weekly follow-ups without his replacement sequence.

Added a separate `MEMBER_FOLLOWUPS_ENABLED` switch, default false. The member sweep now selects only step 0 unless that switch is explicitly true. Existing enrollment/delivery history is retained; no customer opt-out preferences are falsified. Production variable is false. Test verifies that overdue follow-ups do not send in the default welcome-only mode. Deployment `2045ae63-2690-4ca6-bc2d-df29fbbc6f63` is queued at this checkpoint.

The exact one-off recovery email shown in chat was authored for this task, not imposed by Stripe; Dan can replace it with his own copy. Stripe automatic failed-card notices remain enabled until a deliberate replacement is implemented.
