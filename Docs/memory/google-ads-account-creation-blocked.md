---
name: google-ads-account-creation-blocked
description: Creating a Google Ads account needs Dan — the API refuses it at Explorer access and the UI gates it behind a CAPTCHA
metadata:
  type: reference
---

Measured 2026-09-11 while trying to create an empty "SixPackAbs.com" client account under the Daniel Rose
Marketing MCC `324-458-6445`. **Both channels are closed to Claude:**

- **API:** `CustomerService.createCustomerClient` on `customers/3244586445` (MCC as `login-customer-id`) returns
  `DEVELOPER_TOKEN_NOT_APPROVED` — *"This method is not allowed for use with explorer access."* Everything else
  in `scripts/ads/api/client.js` works without a developer token; account creation specifically does not.
- **UI:** MCC → Accounts → **+** → *Create new account* shows a reCAPTCHA "Let's make sure you're human" before
  any form. Claude is platform-blocked from completing CAPTCHAs.

**So a new Ads account is always a Dan task.** Don't re-attempt it; hand him the click path and the settings.

Related: [[google-ads-api-client]], [[google-ads-ui-automation]], [[autonomy-credentials-framing]].
