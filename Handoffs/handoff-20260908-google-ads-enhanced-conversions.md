# Handoff — Google Ads "Enhanced conversions not recording": what it means and how to close it

**Written:** 2026-09-08 (Claude Code, Fable 5.1), from the diagnostics panel in account 342-717-0837 and the
tracking code in `public/index.html` / `server.js`.
**Status:** NOT EXECUTED — diagnosis only. Dan asked for a diagnosis and a plan, not the fix.
**Fire when:** any quiet session. ~1 hour, $0 AI spend. No native retest needed (no UI change), but the change
touches the conversion-firing code, so live-verify the three conversion fires in a browser afterwards.

---

## WHAT THE BANNER IS ACTUALLY SAYING

"Enhanced conversions" is Google's feature where, alongside a conversion, the site hands Google a **hashed email**
so Google can match the sale to the ad click even when cookies are gone (Safari, in-app browsers, the iOS/Android
WebViews). Google now switches it **on by default** for every conversion action once the customer-data terms are
accepted, which they were when the actions were built in August. The site was built for click-id (gclid) matching
only and **never sends an email to Google anywhere** — the banner is Google noticing that the feature is on and
nothing is feeding it.

Five conversion actions have enhanced conversions on. Diagnostics (Goals → Conversions → Summary → Diagnostics →
Enhanced conversions → See details) splits them as follows.

| Action | Source | Diagnostic | Real cause |
|---|---|---|---|
| **Trial Signup** | website tag | ✅ healthy, coverage **100 %** | Google's tag auto-collects the email from the member hub (`#hubEmail` shows it on screen when this fires). Works by accident of layout. |
| **Free Generation Started** | website tag | ✅ healthy, coverage blank | Fires for anonymous users; there is no email to collect. Google is content. |
| **Subscribe** | website tag | 🔴 "No recent data in the last 7 days" | **Zero paid conversions have ever happened.** The one real trial was declined on Sep 1. This fire only runs in the member's browser after the trial converts. Nothing is broken; clears on the first real sale. |
| **Membership Paid (offline)** | Import from clicks | 🔴 "No attempted imports with user-provided data" | The offline feed (`/api/ads/offline-conversions-commit.csv`) carries click-id columns only — **no email column exists**. Google fetched it today (last ping Sep 8) and found no user-provided data. **This will NOT clear on its own, even after sales.** |
| **offline-conversions-commit.csv – All records…** | Import from clicks | 🔴 same | The action Data Manager auto-created when the connection was built. Same feed, same gap. (Already on the tidy-up list — see AI_COORDINATION "Google Ads conversion goals".) |

Two of the three red items are therefore **structural** (the feed can never satisfy the setting as built); one is
**volume** (no sales yet). The separate "Offline conversion — no recent data" card on the same page is the empty
feed, diagnosed 2026-09-02: it clears on the first paid conversion. **Do not manufacture a row** to make either card
go green — that is exactly what poisoned the feed in August ("Unparseable gclid", 0 of 3 imported).

## THE DECISION: fix it, don't just silence it

The cheap way out is to untick "Enhanced conversions for leads" on the two import actions. Two of three warnings
vanish in a minute with no code. **Recommendation: do NOT do that.** The email-match route is the only way Google
can ever attribute a sale from an **app** member (the iOS/Android WebViews cannot hold the ad-click cookie, and a
member who signs up on the web and pays a week later inside the app has no usable click id). Trial Signup already
has 100 % email coverage, which is precisely the lead-side half of "enhanced conversions for leads"; the feed just
needs to supply the other half. About 30 lines of code buys attribution for a group that is otherwise invisible.

## THE PLAN

### Step 1 — send the email with every browser-side conversion (`public/index.html`, ~15 lines)

Right now enhanced conversions on the web tag work only because the email happens to be painted on the hub when
Trial Signup fires. Make it deliberate:

- In `fireAdConversion()` (line ~3393), before `gtag('event','conversion', …)`, if `isLoggedIn()` and `auth.email`
  looks like an email, call `gtag('set', 'user_data', { email: auth.email.trim().toLowerCase() })`. Google's tag
  hashes it client-side (SHA-256) before it leaves the browser; we never ship a plaintext email to Google.
- Add `allow_enhanced_conversions: true` to the `gtag('config', 'AW-18361229851', …)` call on index.html only.
  It is required for the manual `user_data` route and harmless alongside automatic collection.
- Subscribe (7152) and Trial Signup (7294) always have a logged-in user → both now carry the email. Free
  Generation Started (10137) usually fires anonymous → carries nothing, unchanged.
- Nothing about dedupe, value, or the `once:` logic changes.

### Step 2 — add a hashed-email column to the offline feed (`server.js`, ~15 lines)

In the feed query (line ~5826) add `email` to the SELECT, and append an `Email` column to the CSV header and every
row containing **SHA-256 hex of the normalised email**. Google's normalisation, exactly:
lowercase, strip leading/trailing whitespace, and for `gmail.com` / `googlemail.com` addresses remove every dot
before the `@`. Keep the `@example.com` exclusion. Node: `crypto.createHash('sha256').update(norm).digest('hex')`.

**Also widen the feed to email-only rows.** Today the WHERE clause demands `ads_click_id IS NOT NULL`; relax it so
a paid member with **no** stored click id is still emitted with the three click-id columns empty and the email
filled. Google matches whichever key it has; a row with neither is useless and must still be excluded. Keep both
90-day rules keyed on `paid_conversion_pending_at` for the email-only rows (there is no click date to key on).
Count: One on the action still makes re-uploads a no-op, so idempotence is preserved.

### Step 3 — map the new column in Data Manager (Google Ads UI, 5 minutes, Chrome extension)

Tools → Data manager → the HTTPS connection → edit → **Map fields** → map `Email` to Google's **Email** field
(it accepts pre-hashed SHA-256; pick the "already hashed" option if the mapper offers one). Save, then **Run
now / preview**. Expect zero rows — that is correct, the feed is empty until a sale — but the schema must validate.
⚠ Field-mapping traps from the 08-18 build: the URL must end in `.csv`, the header row is the only schema Google
sees, and the connection must not be re-created (that is how the orphan "All records" action appeared).

### Step 4 — privacy policy line (`public/privacy.html`, one sentence)

The Advertising paragraph discloses the click id but not hashed emails. Add: *"If you create an account, a
hashed (one-way encrypted) version of your email address may also be sent to Google to confirm which ads led to a
membership; Google cannot recover the address from it."* Google's enhanced-conversions terms require this
disclosure.

### Step 5 — verify, deploy, and set expectations

- Local: hit the feed with the Basic-auth pair from `~/.absbyai-secrets.env` (`ADS_FEED_USER` / `ADS_FEED_SECRET`)
  and confirm the header has eight columns and no plaintext email anywhere.
- Browser: on absbyai.com logged in, open DevTools → Network, filter `googleads.g.doubleclick.net` / `google.com/pagead`,
  trigger a conversion path, and confirm the hit carries `em=` (the hashed email) — that is the proof enhanced
  conversions are wired.
- Commit, push, Railway deploy, live-verify, then check off the dashboard row if Dan added one.
- **Tell Dan plainly:** the banner will still show "No recent data" for Subscribe and "No attempted imports" for the
  import actions **until the first real paid conversion**, because both are counting events and there are none.
  After this work the setup is correct and both clear by themselves on the first sale. Record that in the
  coordination entry so nobody re-diagnoses it.

## WHAT NOT TO DO

- Do not untick enhanced conversions on the import actions (loses the app-member attribution route).
- Do not seed a test row, a test account, or a fake gclid in the feed — see the August poisoning.
- Do not delete the orphan "All records" action yet — the existing tidy-up decision waits for a real row.
- Do not touch the Data Manager connection's URL or auth; only the field map changes.

## STARTER PROMPT (paste into a fresh session)

```
Execute Handoffs/handoff-20260908-google-ads-enhanced-conversions.md end to end: add gtag user_data (email) to the
browser-side Google Ads conversion fires in public/index.html, add a SHA-256 hashed Email column (and email-only
rows) to the offline conversion feed in server.js, map the column in Google Ads Data Manager via the Chrome
extension, add the one-sentence privacy disclosure, verify the network hit carries the hashed email, commit, push,
deploy, live-verify, then update AI_COORDINATION.md and Handoffs/README.md and remove this handoff from both.
```

**Model / effort:** Fable 5.1, medium effort. One session, ~1 hour, $0 generation spend. The only judgment call is
the Data Manager field mapper's UI, which changes often — drive it by refs, not coordinates.
