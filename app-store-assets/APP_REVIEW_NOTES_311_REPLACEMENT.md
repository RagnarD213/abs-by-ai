# App Review Information → "Notes" — replacement for the stale 3.1.1 section

**Created 2026-08-12. Must be applied BEFORE pressing "Update Review" on iOS App Version 1.0.**

## Why this exists

The App Review Information **Notes** field on the 1.0 version still contains the response written for the **2026-08-05** rejection. Its Guideline 3.1.1 section describes the *external-link* payment approach — the approach Apple rejected on 2026-08-07 — and states verbatim:

> "There is no in-app purchase and no in-app payment sheet."

That is now false, and it **directly contradicts the reply sent to App Review on 2026-08-12**, which tells Apple the membership is purchasable via real In-App Purchase. A reviewer reading these notes would see us describing the exact thing that got the app rejected. Submitting without fixing this is a strong candidate for a third rejection.

The 1.4.1 section, the physical-goods paragraph, the 4.2 native-functionality paragraph and the account-deletion paragraph are all still accurate — **leave them alone.**

## How to apply

In App Store Connect → Apps → Abs by AI → Distribution → **iOS App Version 1.0** → scroll to **App Review Information** → the **Notes** box.

Select from `GUIDELINE 3.1.1 (payments):` up to (but **not** including) `Physical goods:` — that is 1,179 characters — and replace it with the block below. Resulting length ≈ 3,786 characters, within the 4,000 limit.

Then press **Save**, and only then **Update Review** (the button top-right of the version page — this is the resubmit control; "Resubmit to App Review" on the submission-details page stays greyed out until the version itself is edited and saved).

## Replacement text

```
GUIDELINE 3.1.1 (payments): The membership is now purchasable in the app using In-App Purchase. This build offers two auto-renewable subscriptions in one group - Monthly (com.absbyai.app.membership.monthly, $19.99/month) and Annual (com.absbyai.app.membership.annual, $69.99/year), both with a 7-day free trial. Title, duration and price are read from StoreKit at runtime, so they always match what Apple charges. The purchase screen carries the auto-renewal disclosure, a Restore Purchases control, and Terms of Use and Privacy Policy links. Entitlements are verified server-side against the App Store receipt; the app is never trusted to grant access. We completed a sandbox purchase on a physical device to confirm the flow end to end.

We also audited every other purchase path in the app. Two membership buttons that still opened the browser now open the In-App Purchase screen, and one-time credit packs have been discontinued entirely on all platforms, removing that external link. There is no digital content purchasable in the app by any means other than In-App Purchase. The external links that remain are: managing an existing subscription in Apple ID Settings, a "pay on the website" alternative shown alongside In-App Purchase on the same screen, and a fallback shown only if StoreKit is unavailable. These changes are live in this build - the app loads our live web service, so no new binary was required.

IMPORTANT for verifying 3.1.1: the demo account above is a complimentary full-access account, so it intentionally shows a "beta tester" note rather than any purchase UI. To see the In-App Purchase flow, either stay signed out or create a free account, then open Member Hub > Membership.

```

(Keep the trailing blank line so the `Physical goods:` paragraph stays separated.)

## Automation note

Keyboard input into this page could not be driven from the browser tools on 2026-08-12 — neither synthetic typing nor `cmd+v` reached the field, and a React-level value injection left the **Save** button disabled (App Store Connect only enables Save on a genuine user edit). The field was verified afterwards to be **completely unmodified** (3,256 chars, no stray text in any field). This edit is faster done by hand.
