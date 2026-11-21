# Morning brief measurement evidence

Source baseline: commit `e3fb909daa110cf11df00399e560aa415b456002`. Live Google Ads definitions were read on October 1 UTC (September 30 America/Chicago). No tracking events, goals or campaigns were changed.

## What is verified

| Requested metric | Evidence and safe interpretation |
| --- | --- |
| Free generations | Ads action `7704441548`, Free Generation Started, website tag `AW-18361229851/KqDxCMzl4dkcEJvEqLNE`, primary, one per click. The source fires it after `callGeminiImage` returns, including locked and chooser responses, with a 400-day browser dedupe. It does not test free/paid billing status. Report it as **first image-response conversion (Ads)**, not all free generations. |
| Email leads | Verified narrow business measure: first persisted newsletter address captures in `subscribers`, one row per address, counted by original `subscribed_at`. Source `analysis` maps to AbsByAI; source `sixpackabs` maps to SixPackAbs. Unknown source stays unattributed. This does not cover every account or checkout email. |
| Trials | Ads action `7704441545`, Trial Signup, website tag `AW-18361229851/AqLTCMnl4dkcEJvEqLNE`, primary, one per click. Both anonymous and signed-in membership completion paths fire it. The server omits a trial for returning members, but the client still reports the tag. Report **membership checkout conversion (Ads)**; an actual new-trial total is unverified. |
| Paid | Ads action `7703335439`, Subscribe, website tag `AW-18361229851/dQUqCI-kntkcEJvEqLNE`, primary, one per click. The server requires a collected Stripe post-trial invoice or an Apple trial-to-active transition before marking the pending conversion. The website channel is suppressed after offline reporting. Report **paid membership website reporting (Ads)** as one channel, not all paying customers. |

`ads_signals.js` requires the exact live ID, name, type and tag target before exposing a signal. Campaign figures retain fractional attribution. Core business fields for actual free generations, actual new trials and total paid customers remain unknown until they have a suitable definition/source.

## Misleading mappings explicitly rejected

- PostHog `generation_started` records pressing Generate before the request succeeds. `generation_verifier` records a returned image/chooser response but has no billing/free flag.
- AbsByAI `email_subscribed` fires before `/api/subscribe` completes. SixPackAbs `newsletter_signup` fires after a successful response, but that response is also returned for previously captured addresses. Neither proves a new captured address.
- `membership_subscribed` includes returning-member checkout completions. `trial_signup_started` is an attempt.
- `paid_conversion_reported` is emitted even when the browser reporting function returns false. It is not collected money or a new customer.
- Google Ads GA4 imported `qualify_lead`, `close_convert_lead` and `purchase` names do not establish what the current source sends. They are not automatically assigned to business outcomes.
- Offline purchase actions `7725917733` (Membership Paid (offline)) and `7727033697` (auto-created feed action) are both currently primary. The source feed names Membership Paid (offline), but the active Data Manager destination and dedupe across these actions are not verified. They must not be summed as independent sales. Do not fetch the feed's `-commit.csv` path: that GET stamps reporting state.

## Read-only subscriber aggregate

`subscriber_leads.js` imports only the existing `pg` package, never `db.js` or `server.js` with their startup writers. It connects using existing database credentials and the backend's existing Railway connection configuration. It executes `BEGIN READ ONLY`, a transaction-local timeout, one parameterized aggregate SELECT and `ROLLBACK`, then closes the connection. Only fixed site names and counts leave the database. No address, account ID or event payload is selected.

The two full Chicago-day windows match the visitor comparison. Deleted, excluded and example.com rows are omitted; past deletion and asynchronous persistence can reduce historical counts. Unknown-source captures are reported separately. A failed query leaves counts unknown. A verified empty aggregate gives zero. The live proof succeeded and returned zero first captures for both sites in both September 29 and September 22 windows.

## Exact unresolved decisions and checks

1. Decide whether the brief should display the existing first image-response and membership checkout signals under these precise names, or require actual free-generation and new-trial counts. The latter needs an existing authoritative source to be identified, or separately authorized tracking work. This phase creates none.
2. Read the Data Manager import destination/mapping and dedupe behavior for the two offline purchase actions before defining a paid aggregate. Do not change its configuration in a read-only review.
3. Keep first newsletter captures as a documented subset, or separately define whether account/checkout emails should also count as leads and how those sources can be attributed to a site. Do not infer source for untagged addresses.
4. Visitors mean distinct PostHog persons with a pageview on each hostname, normalized across www/non-www. Native wrappers, ad blockers and device changes affect that measure; it is not a complete person or acquisition ledger.

## Source references

- [Generation tag and response handling](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L11449), [browser dedupe](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L3697).
- [AbsByAI email attempt](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L5557), [SixPackAbs successful response event](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/sixpackabs/theme/sixpackabs-child/assets/js/site.js#L194), [subscriber schema](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/db.js#L202), [first capture and source preservation](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L4549).
- [Checkout tag](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L8592), [returning-member trial restriction](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L6686).
- [Paid website reporting](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L8081), [channel exclusion](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L7139), [collected Stripe invoice rule](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L7201), [offline feed](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L6497).
