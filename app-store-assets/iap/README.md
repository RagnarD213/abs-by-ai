# In-App Purchase assets

`purchase-screen-review.png` — the **review screenshot** App Store Connect
requires on each auto-renewable subscription before it can be submitted.

It is a render of the real production purchase screen (`#iapSection` in
`public/index.html`) at iPhone 6.9" dimensions with a StoreKit stub supplying
the same product shapes the App Store returns, so the prices, trial wording and
auto-renewal disclosure on it are the ones the shipped code actually produces.

Regenerate with the capture script recorded in
`app-store-assets/IAP_SUBSCRIPTION_PLAN.md` if the screen changes.

**Why it could not be captured from the simulator:** StoreKit does not serve
products that are still in "Prepare for Submission", and the products are in
that state precisely *because* they are missing this screenshot. The render is
how that circle gets broken.
