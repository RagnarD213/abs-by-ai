# Member email and failed-payment recovery, November 14, 2026

Owner: Codex. Dan requested live checks and autonomous fixes in the existing Stripe/Resend/app setup.

## Verified findings

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

Pending deployment and provider readback at the time this implementation receipt was first written. Update this section with actual deployment, enablement, catch-up counts and delivery evidence before final delivery.

Evidence: `/tmp/stripe-recovery-enabled-20261114.jpg`.
