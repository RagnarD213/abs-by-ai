---
name: google-play-billing-us-change
description: "Google no longer requires Play Billing for US users — external payment links and alternative billing are allowed, with service fees from 2026-10-01"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6d9fc045-e2bf-45b4-9598-da23f301e252
  modified: 2026-07-27T21:58:55.099Z
---

Following the Epic v. Google injunction, Google **no longer requires Google Play Billing for US users**. Verified against Google's own Play Console Help page (answer 15582165) on 2026-07-27, not from memory — see [[app-store-policy-verify-first]].

What US developers may now do inside a Play-distributed app:
- Use in-app payment methods other than Play Billing
- Link out to external checkout (e.g. our own Stripe page)
- Communicate external pricing and availability to users

Three programs launched 2025-12-09: Payments policy, Alternative billing, External content links. Enrolled developers must report transactions and **pay service fees starting 2026-10-01**. Reported fee under the injunction is ~20% on purchases completed within 24h of an in-app link click.

Scope limits that matter: **US-only**, in effect through **2027-11-01**, and a revised settlement was before the court as of 2026-03-04 — so re-verify before acting on it. **Apple's rules are separate and stricter** — do not assume this applies to the iOS app.

Applied to Abs By AI: Dan chose to ship only the no-dead-end "Continue to my hub" button on the credits paywall (2026-07-27) and to defer any link-out until the iOS app clears Apple review, since changing purchase behaviour mid-review invites rejection. See [[native-app-iap-gating]].
