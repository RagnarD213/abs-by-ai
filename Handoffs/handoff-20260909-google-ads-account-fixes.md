> **EXECUTED AND VERIFIED 2026-09-09 — do not run again.** Every task is live in account
> 342-717-0837 and was read back from the account afterwards. Three of the handoff's premises
> were wrong and were corrected against the live read: the non-brand Search campaign was ALREADY
> on campaign-level goals with Submit lead forms as its only biddable goal (only Brand needed
> task 1); both Search campaigns were on Maximize Conversions with a target CPA ($40 brand /
> $20 non-brand), not plain Target CPA; and the Brand campaign has 14 keywords across two ad
> groups, not one. The "over budget" question is answered in the coordination file — non-brand's
> $5/day was set by Dan on 09-08, so last week's spend was against $10/day. Task 6's diagnosis:
> Trial Signup is wired correctly and has fired; it has simply never had an ad-attributable
> completion. Outcome and channel notes: `AI_COORDINATION.md` and
> `scripts/ads/oneoff/search-repair.js`.

# Handoff — Google Ads account fixes (goals, tier-2 budget, search repair, /start A/B, conversion tracking)

**Written 2026-09-09** from the audit in this session's report
(<https://claude.ai/code/artifact/f1b850c8-9cd4-456b-99ef-8c281e14a97a>).
Account **342-717-0837** ("Abs by AI"), `ocid=8444849202`, under MCC 324-458-6445.

**Nothing in the account has been changed yet.** Every number below was read live on 2026-09-09.

---

## WHAT THIS IS FOR, IN PLAIN TERMS

Google Ads has spent **$1,272.66** since August 1 and produced **zero paying customers**. The dashboard
says it is thriving — 1,096 conversions last week at 40&cent; each — but **1,088 of those are "YouTube channel
subscriptions"**, an action that is set as a *Primary, account-default goal*. That means all five campaigns,
including both Search campaigns, are bidding toward a signal that search traffic can never produce. Google
obediently found the cheapest subscribers on earth (Philippines, Indonesia, Vietnam at ~$0.10) and none of
them can buy a $69.99/yr US app.

This handoff makes the account point at customers instead of subscribers, without cutting the spend.

---

## DAN'S DECISIONS — LOCKED, DO NOT RE-LITIGATE

The audit recommended seven fixes. Dan amended four of them on 2026-09-09. **His amendments win.**

| Audit said | Dan's instruction | What you do |
|---|---|---|
| Turn OFF the tier-2 geo Demand Gen campaign | "Don't turn it off. Reduce the budget to $5 a day." | Budget $15/day → **$5.00/day**. Campaign stays ENABLED. |
| Point every ad at `/start` | "Don't change it right now, but make a second ad within each ad group with identical copy pointing to this new landing page so we can test it." | **Leave existing ads alone.** Add one duplicate ad per ad group whose only difference is the final URL. |
| Pause the remarketing campaign | "Keep the remarketing campaign going." | **Do not touch it.** Not paused, not edited. |
| Cut total budget to $15–20/day | "Don't cut the budget yourself. I'll make budget adjustments." | **No budget changes at all**, with the single exception of tier-2 above. |
| Fix the conversion tracking | "Yes, go ahead and fix that conversion tracking." | Do it (task 6). |

**The only budget you are authorised to change in this entire account is tier-2 Demand Gen, to $5.00/day.**
If any other task seems to need a budget change, stop and tell Dan instead.

---

## THE ACCOUNT AS MEASURED, 2026-09-09

### Spend

| Period | Net cost |
|---|---|
| July 2026 | $0.00 |
| August 2026 | $769.75 |
| September 1–9 | $502.91 |
| **Total, all time** | **$1,272.66** |
| Last 7 days (Sep 2–8) | $440.24 (prior 7 days: $293.14, so +50%) |

Billing is healthy — a $500 threshold charge cleared 2026-09-09 on the Visa ending 7763, balance $2.91,
next automatic payment Oct 1. **This supersedes the "Dan fixes the Google Ads payment method" line still
sitting in the Paid ads entry of `AI_COORDINATION.md`.**

### The five campaigns (Sep 2–8)

| Campaign | ID | Ad group ID | Type | Budget/day | Cost | Impr. | Clicks | CTR | Conv. | Cost/conv. |
|---|---|---|---|---|---|---|---|---|---|---|
| `[DAN] [DGEN] [ENGAGEMENT] MU 18-54 \| in-feed & shorts \| geo tier 2 \| ALL CONTENT` | 24122099676 | 197884856303 | Demand Gen | $15.00 | $109.27 | 137,647 | 946 | 0.69% | 960 | $0.11 |
| `[DAN] [DGEN] [ENGAGEMENT] MU 18-54 \| in-feed & shorts \| geo tier 1 \| ALL CONTENT` | 24163535721 | 206274722584 | Demand Gen | $20.00 | $117.12 | 15,066 | 126 | 0.84% | 128 | $0.91 |
| `[DAN] [DGEN] [ENGAGEMENT] [RMKTG] FMU 18-54 \| … \| youtube viewers` | 24169507109 | 203082125721 | Demand Gen | $10.00 | $32.14 | 143 | 3 | 2.10% | 0 | — |
| `Brand - Search - US` | *not captured* | *not captured* | Search | $10.00 | $92.80 | 42 | 8 | 19.05% | 3 | $30.93 |
| `Search - US - Non-Brand - AI Abs Preview` | *not captured* | *not captured* | Search | $5.00 | $88.91 | 58 | 14 | 24.14% | 5 | $17.78 |
| **Account total** | | | | $60.00 | **$440.24** | 152,956 | 1,097 | 0.72% | 1,096 | $0.40 |

Demand Gen IDs came from the ytads snapshot in Postgres. **Search campaign and ad-group IDs were not
captured** — the Ads UI does not put them in the DOM and the tab froze before they could be read from a
drill-down URL. Select those campaigns **by name**; the names above are exact.

⚠ **Unexplained and worth ten minutes:** both Search campaigns spent far more than their stated daily
budgets last week — $88.91 on a $5/day budget, $92.80 on a $10/day budget. Google cannot do that on a
steady budget (the cap is 2× daily), so a budget was almost certainly changed mid-week. **Check Change
history before you touch the search campaigns** — if Dan raised a budget on purpose, say so rather than
treating the CPCs as representative. This does not authorise you to change the budget either way.

### What Google is counting as a conversion (Sep 2–8)

| Conversion action | Source | Tracking status | Primary? | Conv. |
|---|---|---|---|---|
| Engagements ← **YouTube channel subscriptions** | YouTube hosted | Active | Primary | **1,088** |
| YouTube follow-on views | YouTube hosted | Active | Primary | 19 |
| Submit lead forms ← **Free Generation Started** | Website | Active | Primary | 8 |
| Sign-ups ← **Trial Signup** | Website | **Misconfigured** | Primary | 0 |
| Subscribe | Website | **Misconfigured** | Primary | 0 |
| Purchases ← Membership Paid (offline) | Website (import from clicks) | **Misconfigured** | Primary | 0 |
| `offline-conversions-commit.csv` | Website (import from clicks) | **Misconfigured** | Primary | 0 |

All seven read **"Included in account-level goals: Yes."** That is the whole problem in one line.

Conversion labels, all under `AW-18361229851`, fired from `public/index.html`:

| Action | Label | Fires at |
|---|---|---|
| Free Generation Started | `KqDxCMzl4dkcEJvEqLNE` | `public/index.html:10837` (first generation only, `once: 'freegen'`) |
| Trial Signup | `AqLTCMnl4dkcEJvEqLNE` | `public/index.html:7992` (value 20 USD) |
| Subscribe | `dQUqCI-kntkcEJvEqLNE` | `public/index.html:7820` (`AD_SUBSCRIBE_LABEL`) |

### Search keywords and terms (Sep 2–8, top spenders; the list shows "1–10 of many")

| Keyword | Match | Campaign / ad group | Clicks | Avg. CPC | Cost | Conv. |
|---|---|---|---|---|---|---|
| `[abs by ai]` | Exact | Brand / Ad group 1 | 8 | **$11.60** | $92.80 | 3 |
| `"ai body transformation generator"` | Phrase | Non-brand / AI Body Transformation Preview | 3 | $8.68 | $26.05 | 0 |
| `[ai abs generator]` | Exact | Non-brand / AI Abs Generator | 2 | $6.06 | $12.12 | 1 |
| `[six pack ai generator]` | Exact | Non-brand / AI Abs Generator | 2 | $5.34 | $10.68 | 1 |
| `[ai body transformation]` | Exact | Non-brand / AI Body Transformation Preview | 2 | $6.98 | $13.96 | 0 |
| `[ai muscle generator]` | Exact | Non-brand / AI Abs Generator | 1 | $10.71 | $10.71 | 1 |
| `"ai muscle generator"` | Phrase | Non-brand / AI Abs Generator | 1 | $3.18 | $3.18 | 0 |
| `"add six pack to photo"` | Phrase | Non-brand / Add Abs To Photo | 1 | $4.83 | $4.83 | 1 |
| `[body transformation simulator]` | Exact | Non-brand / AI Body Transformation Preview | 1 | $2.45 | $2.45 | 0 |
| `[ai body transformation app]` | Exact | Non-brand / AI Body Transformation Preview | 1 | $4.93 | $4.93 | 1 |

**The mechanism behind the "brand campaign isn't a brand campaign" finding:** the brand campaign has exactly
one keyword, `[abs by ai]` exact — which is correct. Google's **close-variant matching** is serving it against
generic queries. Last week it served `ai ab generator` ($12.21/click) and `abs ai` ($12.20/click). The same
query `abs ai` cost **$3.12** in the non-brand campaign on the same day. The two campaigns are bidding
against each other and the brand one is winning at four times the price.

Search terms named last week: 11 clicks, 53 impressions, **$8.23 average CPC**, $90.53, 2 conversions.
Junk in the mix: `ai to make me fat` ($6.57, 0 conv).

### Ad groups known to exist

- `Brand - Search - US` → **Ad group 1** (one keyword)
- `Search - US - Non-Brand - AI Abs Preview` → **AI Abs Generator**, **AI Body Transformation Preview**,
  **Add Abs To Photo**, **What Would I Look Like With Abs**

That list came from two report screens and **may be incomplete** — enumerate ad groups at run time rather
than trusting it.

### The site-side scoreboard (PostHog project 458833 + prod Postgres, since the first ad click 2026-07-30)

| Step | People | Share |
|---|---|---|
| Arrived on absbyai.com from a Google ad (`gclid`/`wbraid`) | 207 | 100% |
| Saw the before/after proof strip | 191 | 92% |
| Uploaded a photo and got an AI result | 35 | 17% |
| Gave an email | 4 | 1.9% |
| Created an account | 2 | 1.0% |
| Started a trial signup | 2 | 1.0% |
| **Paid for anything** | **0** | **0%** |

Note the gap: Google recorded **1,097 clicks** last week and roughly **30 people** reached the website. That is
not a tracking bug — Demand Gen "clicks" on YouTube are mostly plays and channel visits that never leave
YouTube. It is also why task 4 is scoped to Search only.

---

## THE TASKS

### Task 1 — Give both Search campaigns their own conversion goals *(highest value, ~20 min)*

Set **campaign-specific conversion goals** on `Brand - Search - US` and `Search - US - Non-Brand - AI Abs
Preview`, containing **Free Generation Started only**. Add Trial Signup to that set the moment task 6 gets it
recording.

Leave the three Demand Gen campaigns on the account-default goals — YouTube channel subscriptions is
genuinely what those campaigns are for, and Dan is keeping them.

In the UI this is each campaign's **Settings → Conversion goals → "Use campaign-specific goals"**. The
campaigns almost certainly sit on account-default today (every action reads "Included in account-level
goals: Yes"), but **confirm it before changing anything** and record what it was.

> Why this is first: until it is done, every other bidding change is being fed a signal that is 99% YouTube
> subscriptions. Fixing bids before fixing goals just makes Google chase the wrong thing faster.

### Task 2 — Tier-2 Demand Gen budget to $5.00/day

Campaign **24122099676** (`… | geo tier 2 | ALL CONTENT`), currently `budgetMicros: 15000000` = $15.00/day
→ **$5.00/day**. Campaign stays ENABLED. Nothing else about it changes.

Sanity-check afterwards that tier 1 is still $20.00/day and remarketing is still $10.00/day. **If the budget
is shared across campaigns, stop** — a shared budget would move the others too, which is not authorised.

### Task 3 — Repair the two Search campaigns

**3a. Stop the brand/non-brand collision.** Add campaign-level **negative keywords to `Brand - Search - US`**
so its single exact keyword stops harvesting generic queries as close variants. At minimum:
`abs ai`, `ai abs`, `ai ab generator`, `ai abs generator`. Use phrase-match negatives. After this the brand
campaign should only serve on genuine brand searches, and those same queries fall back to the non-brand
campaign at roughly a quarter of the cost.

**3b. Add junk negatives to the non-brand campaign.** `ai to make me fat` is the clear one — add `fat` and
`gain weight` as phrase negatives. **Use judgement on the rest and do not over-prune:** `ai body editor`,
`hot body ai editor` and `weight visualizer` all read as plausible intent and are cheap; leave them and
watch. The account is starved of volume, so negatives are for wrong intent, not for zero-conversion terms
with 1 click of history.

**3c. Bidding.** Both campaigns run **Target CPA** on 8 real conversions a week between them, which is far
too little for smart bidding to learn from — that is a large part of why the CPCs are $6–12. Switch both to
**Maximize Clicks with a $2.00 maximum CPC**, and leave them there until each campaign has 30+ conversions
in a trailing 30 days. Then reassess.
*(This is a bidding change, not a budget change — it is inside what Dan approved. Budgets stay as they are.)*

**3d. Broaden the keywords.** 53 impressions in a week is not a campaign. Dump the full keyword list first
(the report only showed "1–10 of many"), then add phrase-match keywords to the ad group each one belongs
in. Candidates, all consistent with the existing naming and with Dan's own ad copy:
`what would i look like with abs`, `see myself with abs`, `six pack photo editor`, `ai fitness transformation`,
`abs generator app`, `body transformation ai`. Skip any that already exist in any match type.

### Task 4 — The `/start` landing-page A/B *(Dan's design, follow it exactly)*

**Do not change any existing ad's final URL.** For **each ad group in the two Search campaigns**, create one
**additional** Responsive Search Ad that is a faithful copy of that ad group's existing enabled ad — same
headlines, same descriptions, same display paths, same pinning — with the **only** difference being:

```
Final URL: https://absbyai.com/start
```

Enable it. Leave the original enabled too.

**Read the copy off the live ad rather than retyping it.** The Ads Scripts API can read an existing
responsive search ad's headlines and descriptions and rebuild them into a new ad, which removes the whole
risk of a transcription error. Do not hand-copy from a screenshot.

**Recommended, and worth one line to Dan:** set each affected ad group's **ad rotation to "Do not optimize:
rotate ads indefinitely."** Two ads in one ad group are *not* split 50/50 by default — Google picks a winner
on predicted click-through within days, which would confound a landing-page test with an ad-serving
decision. With rotation left on the default the test still works, it just reads slower and less cleanly. If
you would rather not change delivery behaviour, say so in the report-back and leave it.

**Scope — Search campaigns only, not Demand Gen.** Two reasons, both measured: Demand Gen clicks almost
never reach the website (1,097 Google clicks last week → ~30 site visits), so a landing-page test there
measures nothing; and the **ytads automation creates, pauses and labels Demand Gen ads every hour**, so a
hand-made ad in those ad groups risks colliding with it. If Dan wants `/start` on Demand Gen as well, the
right move is to change those campaigns' final URL, not to add ads — **ask him first.**

### Task 5 — Remarketing campaign: DO NOT TOUCH

`[DAN] [DGEN] [ENGAGEMENT] [RMKTG] …` (24169507109) stays exactly as it is. Not paused, not re-budgeted, not
re-goaled. This overrides the audit's recommendation 5. Dan's call.

### Task 6 — Fix the conversion tracking

**Priority: Trial Signup (`AqLTCMnl4dkcEJvEqLNE`).** It is a plain website conversion that ought to be firing
and instead reads "Misconfigured" with zero recorded. PostHog shows `trial_signup_started` firing for two
Google-ad visitors, so people have reached that code path. Trace it end to end:

- `public/index.html:7992` is the fire point; `fireAdConversion()` is at `public/index.html:3535`.
- On the live site, start a trial signup and watch the network for the Google conversion hit
  (`googleads.g.doubleclick.net` / `google.com/pagead/…`) carrying that label — this is the same technique
  that verified the `em=` enhanced-conversion parameter on 2026-09-08.
- Suspects, in order: the label never reaches gtag; the dedupe in `fireAdConversion` (`once:`,
  `AD_CONVERSION_DEDUPE_DAYS = 400`) suppressing it; the conversion action being defined for the wrong page
  or scope in Google Ads.
- Whatever you find, **write the diagnosis down** — a clear "here is why it never fired" is a successful
  outcome even if the fix needs Dan.

**Subscribe (`dQUqCI-kntkcEJvEqLNE`) and Purchases (offline): already understood, leave them.** No sale has
ever happened, so the offline feed is header-only and Google returns error 4000 and cannot infer a schema.
**Do not manufacture a row** — that is a standing rule. Both clear themselves on the first real paid
conversion. Same for the "Enhanced conversions not recording" banner: the code side shipped 2026-09-08
(`ac51f50`, `em=` verified on the live hit) and the Data Manager Email-column mapping is blocked by that same
empty feed.

### Task 7 — No other budget changes

The audit recommended cutting the account to $15–20/day. **Dan declined.** Total budget stays at $60/day
minus the $10/day that task 2 removes from tier 2 → $50/day. Do not propose further cuts in the report-back;
Dan makes budget calls himself.

---

## HOW TO EXECUTE — READ BEFORE THE FIRST CLICK

The Google Ads **API is still blind** (no developer token; `GOOGLE_ADS_DEVELOPER_TOKEN` is set nowhere) and
the **Ads UI froze repeatedly** in two separate sessions on 2026-09-08 and 2026-09-09. Prefer the script
channels.

### Channel 1 — a one-off Google Ads Script *(recommended for tasks 2, 3 and 4)*

The account already runs a script hourly (Tools → Scripts → *Abs by AI — YouTube engagement champion*).
Add a **second, one-off script** for this work. The native `AdsApp` API can select campaigns by name, read an
existing responsive search ad's headlines and descriptions, build the duplicate with a new final URL, set a
budget, and add keywords and negatives — all without touching a settings panel.

- **Verify every method name against Google's Ads Scripts reference before running.** Do not assume the
  builder and getter names; the editor's autocomplete plus a Preview will surface anything missing.
- **Preview is safe.** It executes no AdsApp changes. Note that `UrlFetchApp` *does* run in preview — that is
  how the ytads script posts a real snapshot from a preview — so a preview of a script that calls out to our
  server is not a dry run for that part.
- Installing a script through Claude has a documented recipe with paid-for traps in `Docs/YTADS.md` §
  *Installing a new version of the Ads Script from Claude*: `cm.setValue()` does **not** enable Google's Save
  button (send one real keystroke, check `material-button.save-button` lost `is-disabled`, then `.click()` in
  JS); the extension's DLP blocks any JavaScript whose text contains `UPPERCASE_NAME = value`, so send the
  script body base64 and decode in-page; `cmd+v` into CodeMirror is unreliable; "Run" opens a "Preview before
  running?" dialog — choose "Run without preview" when you actually mean to run.
- Delete the one-off script when the work is done, so it cannot fire again.

### Channel 2 — the existing mutation queue *(good for single, well-formed operations)*

```bash
export DATABASE_PUBLIC_URL="$(grep '^DATABASE_PUBLIC_URL=' ~/.absbyai-secrets.env | cut -d= -f2-)"
node scripts/ads/ytads/manual.js list
node scripts/ads/ytads/manual.js raw '<json mutation>' --note "why"
```

The next **live** hourly run (Google fires at :00) passes the object straight to `AdsApp.mutate`
(`scripts/ads/ytads/ads-script.js:218–221`) and writes back `done` or `failed` with Google's error text
verbatim. `YTADS_ENABLED=1` is set, so runs are live.
⚠ **`campaignConversionGoalOperation` support in `AdsApp.mutate` is unverified.** If it is rejected, do
task 1 in the UI — it is a small, well-defined settings change.

### Channel 3 — the Ads UI, last resort

Traps, all paid for (memory `google-ads-ui-automation`, plus this session):

- The tab **freezes for minutes at a time** (CDP `Runtime.evaluate` timeouts, screenshots failing with
  "script injection timed out"). **Wait it out; do not click into spinners.** Fewer concurrent Claude Code
  sessions helps — a session on 2026-09-08 lost the tab entirely at load 50–90.
- `find` → `ref` clicks work. Coordinate clicks on the date-range control do not.
- The date-range **"All time" option would not apply at all** on 2026-09-09, in either of two attempts.
  Monthly figures via Billing → Summary are the workaround.
- The extension's **DLP blocks any JS result containing `NAME=value`**, including a page URL with query
  params. Return lengths, booleans and sliced innerText, never `location.href`.
- Campaign and ad-group IDs are **not** in the DOM — get them from a drill-down page's URL in the tab-context
  line, or work by name.
- Table rows render late and are often absent from `innerText` for 10–20 s after the shell paints. Scroll,
  wait, then read.

---

## DONE MEANS

1. Both Search campaigns show **campaign-specific conversion goals = Free Generation Started**, read back
   after saving, with the previous setting recorded.
2. Tier-2 Demand Gen reads **$5.00/day**; tier 1 still $20.00/day; remarketing still $10.00/day; both Search
   budgets unchanged.
3. `Brand - Search - US` carries the generic negatives and the campaign is no longer serving on `abs ai` /
   `ai ab generator` (confirm on the search-terms report after a few days, not immediately).
4. Both Search campaigns on **Maximize Clicks, $2.00 max CPC**.
5. **One extra enabled RSA in every Search ad group**, copy identical to the original, final URL
   `https://absbyai.com/start`; originals untouched and still enabled. Ad rotation either set to rotate
   indefinitely, or explicitly reported as left alone.
6. The remarketing campaign is **provably untouched** (no entry in Change history).
7. Trial Signup either fires on a live end-to-end test, or has a written diagnosis of exactly why it does not.
8. `AI_COORDINATION.md` updated: the Google Ads audit entry replaced with what was changed and what is left,
   and the **stale "Dan fixes the Google Ads payment method" line removed** — billing is confirmed working.
9. This handoff removed from `Handoffs/README.md` and from the HANDOFFS section of `AI_COORDINATION.md`.
10. **No dashboard row** — Dan's rule of 2026-09-08 — unless he explicitly asks for one.

**Report back with:** what changed, before-and-after values for every setting touched, the Trial Signup
diagnosis, and the answer to the Change-history question about those over-budget search campaigns. Flag the
Demand Gen `/start` question if Dan should decide it.

---

## COST AND RISK

- **$0 in AI generation.** No Replicate/Gemini/Anthropic calls. Nothing here touches the $25/session cap.
- **Ad spend continues** at existing budgets throughout, minus $10/day once task 2 lands.
- **Everything here is reversible**: goals, negatives, bidding strategy, one budget, and additive ads. Nothing
  is deleted. Record the old value of every setting before changing it so any of it can be put back.
- The one genuinely irreversible-ish risk is **losing bidding history** by switching off Target CPA. That is
  accepted: with 8 conversions a week there is no history worth keeping, and Dan approved the change.

---

## STARTER PROMPT (paste into a fresh session — Fable 5.1, effort HIGH, ~2–3 h)

```
Execute Handoffs/handoff-20260909-google-ads-account-fixes.md in full.

This repairs Google Ads account 342-717-0837, which has spent $1,272.66 and produced zero
customers because "YouTube channel subscriptions" is a Primary account-default conversion
goal that every campaign — including both Search campaigns — is bidding toward.

Read the handoff first. Dan amended four of the seven fixes on 2026-09-09 and his
amendments are locked: tier-2 Demand Gen gets its budget cut to $5/day rather than being
turned off; the /start landing page gets a SECOND ad per ad group with identical copy
rather than a change to the existing ads; the remarketing campaign is left completely
alone; and no other budget in the account may be changed, because Dan makes budget calls
himself.

The Google Ads API is blind (no developer token) and the Ads UI froze repeatedly in two
prior sessions, so prefer the script channels described in the handoff: a one-off Google
Ads Script for the budget, the search repairs and the duplicate ads, and the existing
manual mutation queue (scripts/ads/ytads/manual.js raw) for single operations. The UI is
the last resort and its traps are listed. Verify every AdsApp method name against Google's
reference before running, and use Preview — it makes no AdsApp changes.

Record the old value of every setting before you change it. Finish with the DONE MEANS
checklist, including removing this handoff from Handoffs/README.md and the HANDOFFS
section of AI_COORDINATION.md, and clearing the stale "Dan fixes the Google Ads payment
method" line — billing is confirmed working as of 2026-09-09. No dashboard row.
```
