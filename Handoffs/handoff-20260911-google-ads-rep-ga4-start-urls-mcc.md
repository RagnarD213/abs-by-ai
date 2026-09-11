# Handoff — Google Ads rep meeting (2026-09-11): GA4 + Ads link, every Search ad to /start, empty MCC account for sixpackabs.com

**Written 2026-09-11 from Dan's notes of his meeting with a Google Ads rep. Three account tasks, one verification
item from the screenshot he took during the call. Nothing here has been executed.** Everything in "What exists"
was read from the live account by the Google Ads API on 2026-09-11 (`scripts/ads/api/client.js`).

Dan's notes, verbatim:

> SET UP GOOGLE ANALYTICS FOR ABSBYAI.COM AND LINK TO GOOGLE ADS ACCOUNT
> CHANGE SEARCH ADS LINKS TO: https://absbyai.com/start MAKE EXISTING HOMEPAGE A SITELINK.
> CREATE SEPARATE ACCOUNT WITHIN MCC FOR SIXPACKABS.COM. LEAVE EMPTY WITH NO ADS AND NO BILLING INFO

The screenshot from the call shows the Recommendations card **"Add at least two callouts to Search - US -
Non-Brand - AI Ab…"** with four empty callout fields. See task 4 — the account already carries four callouts on
that campaign, so this is a verify-and-dismiss, not a build.

## What exists (verified 2026-09-11)

| | |
|---|---|
| Google Ads account | `342-717-0837` (customer `3427170837`). **Direct access under `danroseconsulting@gmail.com`; NOT under the Daniel Rose Marketing MCC `324-458-6445`** (`customer_manager_link` empty; the MCC as login returns `USER_PERMISSION_DENIED`). Memory `google-ads-api-client`. |
| API | `node scripts/ads/api/client.js search "<GAQL>"` / `mutate ops.json [--dry-run] --note "why"`. No developer token; every mutate is ledgered in `ytads_events`. Doc `Docs/GOOGLE_ADS_API.md`. Chrome-driving traps for anything the API cannot do: memory `google-ads-ui-automation` (account chooser `ads.google.com/nav/selectaccount`, `ocid=8444849202` for the client account, `ocid=364714550` for the MCC). |
| Tags on the site | `public/index.html` and `public/start.html` load **`gtag/js?id=AW-18361229851`** (the Ads conversion tag; enhanced conversions on, `em=` verified live 09-08). **There is no GA4 property tag anywhere** — grep for `G-` returns nothing in `public/`. Product analytics is **PostHog**; GA4 is being added for the rep's Ads link, not to replace PostHog. |
| Search campaigns | `Brand - Search - US` `24086091285` (ad group `204012081332`) and `Search - US - Non-Brand - AI Abs Preview` `24148587722` (ad groups `194615821330` AI Abs Generator, `194615821370` Add Abs To Photo, `194615821410` What Would I Look Like With Abs, `194615821570` AI Body Transformation Preview). Both Maximize clicks, $2.00 CPC ceiling since 09-09 (both went dark 09-10 — a separate open item on the board). |
| Search ads | **10 RSAs, all ENABLED, two per ad group: the original pointing at the homepage and the 09-09 `/start` copy** (rotate indefinitely, byte-identical copy — that was the landing-page A/B). Home ads: `821203927140`, `821417868428`, `821344283230`, `821344275016` (`http://absbyai.com` — note **http**) and Brand `818993763993` (`https://absbyai.com`). `/start` ads: `824052727140`, `824096248267`, `824096248690`, `824096248717`, Brand `824096260039`. |
| Assets | Sitelinks: `Contact Us` `419837287031` → `/contact` (ENABLED on Brand only); `FAQ` `401566853985` → `/faq.html` and `Terms & Conditions` `401566879386` → `/terms.html` exist but their campaign links are **REMOVED**. Callouts `AI Future Self Preview` `419836253477`, `Custom Meal Plans` `420021386607`, `Personalized AI Trainer` `420021391323`, `Snap And Track Macros` `420021395013` — **all four ENABLED on BOTH Search campaigns.** No sitelink of any kind on Non-Brand. |
| Conversions | Free Generation Started (primary, working), Trial Signup, Purchase (empty feed — see the board's "Google Ads conversion goals" entry). **Do not let a GA4 import become a primary conversion — it would double-count against these.** |

## Task 1 — GA4 for absbyai.com, linked to the Ads account

1. **Create the property.** In Dan's Chrome (`danroseconsulting@gmail.com`), `analytics.google.com` → Admin → Create
   → Property "Abs By AI", reporting time zone `America/Chicago`, currency USD, business details as Dan's, → Web data
   stream `https://absbyai.com`, stream name "absbyai.com". Enhanced measurement ON (page views, scrolls, outbound
   clicks, site search, video engagement, file downloads). Note the **Measurement ID `G-…`**. If a property already
   exists for absbyai.com (check Admin → Property picker first), reuse it — do not make a second one.
   Creating the property needs no password entry once Chrome is signed in; if Google asks Dan to re-authenticate,
   stop and tell him — Claude does not type credentials.
2. **Install it through the gtag loader that is already on the page** — do not add a second `<script>` loader.
   In `public/index.html` (line ~36) and `public/start.html` (line ~64) add, after the existing `AW-18361229851`
   config, a `gtag('config', 'G-XXXX', { send_page_view: true })`. Grep `public/` for every other HTML file that
   carries the `AW-` loader (`grep -l "AW-18361229851" public/*.html`) and add the same line there. The SPA's
   in-app screen changes already fire `gtag('event','page_view', …)` for Ads (index.html ~line 3747) — that call
   now feeds GA4 too; check it passes a `page_location`/`page_title` so GA4 screens are readable.
   ⚠ Native: the iOS/Android wrappers load the same page, so GA4 will see app sessions as web. Acceptable; note it
   in the doc. **Flag the native retest** as with every web deploy (memory `cross-platform-retest-rule`).
3. **Consent + privacy.** US-only traffic, no consent banner today (Ads tag already runs unconditionally). Add
   "Google Analytics" to the privacy policy's analytics sentence (the section that names PostHog and the Google
   Ads tag — grep `index.html` for "PostHog"). Commit, push, Railway deploy, verify live.
4. **Verify the tag:** visit the live `/` and `/start` in the in-app Browser pane and `read_network_requests` for
   `google-analytics.com/g/collect` carrying the `G-` id on both pages; then GA4 Reports → Realtime shows the visit
   within 60 s. Screenshot both as proof.
5. **Link GA4 ↔ Google Ads:** GA4 Admin → Product links → Google Ads links → Link → pick `342-717-0837` → enable
   personalized advertising ON, auto-tagging is already on (gclids arrive today). Then in Google Ads: Tools →
   Data manager → confirm the GA4 link shows Connected. Set **Attribution/Ads personalization** defaults.
6. **Do NOT import GA4 conversions as primary.** If the rep wants GA4 key events in Ads, mark `generation_started`
   as a key event in GA4 and import it as a **secondary** (observation-only) conversion, or skip the import. The
   existing gtag conversion actions stay primary. Record the choice in `Docs/GOOGLE_ADS_API.md` (new "GA4" section)
   and in memory (`google-ads-ga4-link`: property id, measurement id, what is primary).

## Task 2 — every Search ad to `https://absbyai.com/start`; the homepage becomes a sitelink

This ends the 09-09 Search landing-page A/B (home vs /start) on the rep's advice — Dan agreed in the meeting.
Record that in the account-fixes doc trail (`Docs/GOOGLE_ADS_API.md` or a line in `Docs/VSL_LANDING.md`).

1. **Recommended shape — do not delete ads.** Update the five home RSAs' `final_urls` to `https://absbyai.com/start`
   via the API (`AdService` update with `updateMask: "final_urls"` on `customers/3427170837/ads/<id>`; `--dry-run`
   first). That leaves two identical-URL RSAs per ad group; **pause the five originals** (`manual.js pause
   customers/3427170837/adGroupAds/<ag>~<ad>`) rather than removing them, so their history stays readable.
   Alternative if Google refuses the URL update on an existing ad: leave the originals paused on the old URL and
   let the `/start` copies carry the group. Either way, read back all 10 rows with the GAQL in "What exists" and
   confirm every ENABLED Search ad has `finalUrls = ["https://absbyai.com/start"]` (https, no trailing slash).
   ⚠ Changing a final URL re-triggers policy review — run `client.js policy 24148587722` and `… 24086091285`
   afterwards and again the next day.
2. **Sitelinks.** Create a SITELINK asset **"Abs By AI Home"** → `https://absbyai.com`,
   description lines "Upload a photo, see your abs" / "AI trainer, meals, tracking" (≤35 chars each, no claims —
   memory `ad-copy-no-unbelievable-claims`), and link it to BOTH Search campaigns (`campaign_asset` field type
   SITELINK). Google wants ≥4 sitelinks to serve the rich format, and every sitelink URL must differ from the ad's
   final URL and from each other: re-link the existing `FAQ` `401566853985` and `Contact Us` `419837287031` to both
   campaigns, and add **"How It Works"** → `https://absbyai.com/how-it-works.html` (the page exists; `about.html` is
   the spare). Never a demo URL (`?demo=…`). Leave `Terms & Conditions` unlinked (it was removed on purpose).
   Verify in the UI: Assets → Sitelinks shows 4 on each campaign, status Eligible.
3. **UTMs:** the Search RSAs carry no tracking template today and `/start` reads `gclid` for the Ads conversion.
   PostHog attribution comes from the referrer + gclid; do not add UTMs unless the page's funnel needs them
   (`Docs/VSL_LANDING.md`).

## Task 3 — an empty client account for sixpackabs.com inside the MCC

1. **Where:** the Daniel Rose Marketing MCC `324-458-6445` (`ads.google.com` → account chooser → the MCC, `ocid=364714550`).
   Accounts → **+ → Create new account** → name **"SixPackAbs.com"**, time zone `America/Chicago`, currency USD,
   **skip billing** and **decline every "create your first campaign" step** — the account must have **no campaigns,
   no ads, no payment profile**. Google's new-account wizard defaults to "Smart" campaign creation; choose "Switch to
   Expert Mode" / "Create an account without a campaign" (the link at the bottom of the wizard).
2. **API first, UI second:** `CustomerService.createCustomerClient` on `customers/3244586445` with the MCC as
   `login-customer-id` may work for the MCC even though it fails for the Abs account (that failure was the missing
   manager link, not the MCC itself). `client.js` is wired to `3427170837` — check how it sets `login-customer-id`
   before assuming an env override exists; a raw `fetch` with the same OAuth token is fine for this one call. If
   it returns `USER_PERMISSION_DENIED`, use the UI.
3. **Verify** by GAQL from the MCC login: `SELECT customer_client.id, customer_client.descriptive_name,
   customer_client.status FROM customer_client` shows the new CID; open it and confirm Campaigns is empty and
   Billing shows "no payment profile". Record the new CID in `Docs/GOOGLE_ADS_API.md` and memory
   (`google-ads-sixpackabs-account`). **Nothing else** — no conversion tag, no linking to the SixPackAbs site.

## Task 4 — the callouts recommendation in the screenshot

Both Search campaigns already carry four ENABLED callouts (ids above). Open Recommendations on Non-Brand: if the card
still shows, it is stale or wants ad-group-level callouts — **dismiss it**, do not add duplicates. If the four are
somehow missing from Non-Brand in the UI (the API says they are linked), re-link the four existing asset ids rather
than typing new text. Note the outcome in this handoff's board entry.

## Finish

- Delivery rules: the tag change is a code change → commit, push, Railway deploy, verify live on `/` and `/start`,
  flag the native retest. Account changes: read back every one by API and paste the read-back into the coordination
  entry, not just "done".
- Board: the Search campaigns "went dark on 09-10" entry is separate — do not touch the CPC ceiling here.
- No dashboard row exists for this; do not add one (Dan's 09-08 rule). Delete this doc's row from `Handoffs/README.md`
  and its HANDOFFS line in `AI_COORDINATION.md` when done; leave a 3-sentence "waiting on Dan" entry only if a step
  needed his login.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-google-ads-rep-ga4-start-urls-mcc.md`: create GA4 for absbyai.com through the
> existing gtag loader (index.html + start.html + any other page carrying AW-18361229851), link it to Google Ads
> 342-717-0837 with no primary conversion import; move every Search RSA's final URL to https://absbyai.com/start and
> pause the home originals, add the homepage + FAQ + Contact sitelinks to both Search campaigns; create an EMPTY
> "SixPackAbs.com" client account under MCC 324-458-6445 (no campaign, no billing); verify the four callouts already
> on Non-Brand and dismiss the recommendation. API first (`scripts/ads/api/client.js`, dry-run then apply), Chrome
> only where the API cannot. Read back everything, commit/push/deploy/verify the tag, update the board. Model: Fable 5.1, effort high.
