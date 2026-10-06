---
name: stripe-trial-end-active-before-charge
description: "Stripe marks a subscription \"active\" at trial end about an hour BEFORE it attempts the first charge; never treat trialing→active as a sale"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3f9fd2a8-7eac-46d0-9679-efdaeb89445a
  modified: 2026-09-02T20:51:13.501Z
---

Stripe flips a subscription from `trialing` to `active` the moment the trial ends, and only attempts the first real charge ~1 hour later. Measured on the account's first real trial (2026-09-01): active at 07:37, card declined at 08:38, past_due by 08:41, then the customer deleted their account. Zero trial→paid sales have ever happened as of 2026-09-02.

**Why:** the Google Ads "paid" conversion used to be stamped on the trialing→active transition, which would have reported a $69.99 sale for money that never arrived.

**How to apply:** the sale is stamped from the `invoice.paid` webhook (billing_reason `subscription_cycle`, amount_paid > 0) in `recordPaidInvoiceConversion()` in server.js (commit `ee91b26`); the Stripe webhook endpoint delivers `invoice.paid`. The offline conversion feed being empty is correct until a real paid invoice exists — Google's error 4000 on a header-only file clears on its own then. See [[pay-for-generations]] and [[ai-trainer-membership]].
