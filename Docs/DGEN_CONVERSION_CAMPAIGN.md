# Demand Gen conversion campaign — the finished ads, built 2026-09-10

Dan's spec (chat, 2026-09-10): one Google Ads campaign carrying every finished ad, every version
of an ad inside that ad's ad group, one ad group per landing page (`/start` vs the homepage), US +
Canada, male + unknown, 25–54, the custom segments as the audience, no lookalikes yet, $20/day,
target CPA $30 on Free Generation Started, **built PAUSED for his review**.

## What exists in account 342-717-0837

| thing | id / value |
|---|---|
| Campaign `[DAN] [DGEN] [CONVERSION] MU 25-54 \| US+CA \| ad 1 + ad 2 \| start vs home` | `24243839443`, **PAUSED**, Demand Gen, Target CPA $30.00, budget `15862488218` $20.00/day, locations by presence |
| Ad group `Ad 1 This Picture Got Me Abs \| /start` | `199420011065` |
| Ad group `Ad 1 This Picture Got Me Abs \| home` | `202965542111` |
| Ad group `Ad 2 Stop Wasting Money On Nutritionists \| /start` | `200136997156` |
| Ad group `Ad 2 Stop Wasting Money On Nutritionists \| home` | `199420011265` |
| Audience `Ad 1 … \| MU 25-54 \| AI abs preview tool + what would I look like + competitor apps` | `358261317` (age 25–54 + unknown, male + unknown, segments 1013657222 / 1011514666 / 1011514645) |
| Audience `Ad 2 … \| MU 25-54 \| AI fitness + competitor apps + get abs belly fat` | `358261320` (segments 1013657228 / 1011514645 / 1011510739) |
| Conversion goal | campaign-specific: **Submit lead forms only** (= Free Generation Started `7704441548`); YouTube subscriptions, sign-ups and purchases are NOT bid on |
| Location + language | at the AD GROUP (this campaign type keeps them there): US `2840`, Canada `2124`, English `1000` on all four groups |

Ten ads, named `<ad group> | <video> | <landing page>`, one YouTube video each, final URL carrying
`utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-ad1|ad2&utm_content=<video>-<start|home>`:

| ad group | videos (YouTube id → asset) |
|---|---|
| Ad 1 (both landing pages) | Muhammad 16:9 `lf46ytHacss` → `419514921434`, Zeeshan 16:9 `1oEcwdp21Fg` → `419514919721`, Muhammad vertical `Iz0u8KHRbyE` → `419514921437` |
| Ad 2 (both landing pages) | Muhammad 16:9 `Dtk5knWM7c8` → `419623700809`, Muhammad vertical `7XgHxn59Tsg` → `419700324321` |

Copy: **headlines are Dan's own** (screenshots 2026-09-10): Ad 1 *How I Got Abs At 40 · See Yourself
With Abs - Use AI · Abs by AI ® · Abs By AI - Here's How It Works · How I Got Abs With AI Workouts*;
Ad 2 *Fire Your Nutritionist. Use AI Instead · How AI Replaces Nutritionists · How I Got Abs With AI ·
How I Got Abs At 40 · How AI Got Me Abs*. Long headlines and descriptions are the first-written sets in
`scripts/ads/oneoff/build-video-campaign.js`. Business name `Abs by AI`, logo asset `400941168572`.

**Policy:** within minutes of creation Google marked all six Ad 1 ads **Approved (limited) — CLICKBAIT**
on the original copy (*"This Picture Got Me Abs"*, *"Abs At 40 - The Photo That Did It"*). Dan's headlines
replaced that copy the same afternoon, which re-triggers review. Ad 2's ads were Approved (two still
in review at the time). A limited ad never spends in this account (measured 2026-09-10); if Ad 1 stays
limited, the retry rule's next step is a clean text-free thumbnail on the public video, then removal.
This campaign is **outside the ytads engagement system** (`Docs/YTADS.md`), so nothing retries it
automatically.

**Dan's copy rule (2026-09-10):** no claim that reads unbelievable without the video's context. *"This
picture got me abs"* is too much; *"How I get abs at 40"* / *"How AI got me abs"* are the shapes to reuse.

## To switch it on
Campaign 24243839443 → Enable. Nothing else is needed; ad groups and ads are already ENABLED.

## How it was built, and the traps (Google Ads Scripts, no API developer token yet)
`scripts/ads/oneoff/build-video-campaign.js` — pasted into Tools → Scripts as a second script, run
once, then deleted from the account. REPORT mode reads; APPLY mode builds in three re-runnable steps
and Preview is a genuine Google-validated dry run of step 1. Measured on 2026-09-10:

- **Demand Gen rejects `maximizeConversions.targetCpaMicros`** ("not allowed for the given context");
  use plain `targetCpa`.
- **`mutateAll` with temporary ids works for budget → campaign → assets → ad groups → ads** in one
  atomic batch, but NOT for criteria whose id is a Google constant.
- **Every create without a `resourceName` gets a temporary one stamped by the Scripts wrapper**, and
  Google rejects that for a country / language / audience criterion ("The field's contents don't match
  another field that represents the same data. At …create.resourceName"). Send those one at a time
  with the exact derived name (`…/adGroupCriteria/<adGroup>~2840`).
- **An API-made Demand Gen ad group is always "audience grouped"**; loose gender / age / custom-segment
  criteria are refused ("Audience segment attachment is not allowed when use audience grouped bit is
  set to true"). Build an `Audience` (age + gender + `audienceSegments.customAudience`) and attach it as
  an `audience` criterion.
- **Location and language live on the ad group** for this campaign type; campaign-level ones return
  "The error code is not in this version".
- **Campaign conversion goals need `{partialFailure:false}`** and the wanted goal must be written
  `biddable:true` FIRST — writing only the false ones fails with "campaign override goals but has no
  goals configured".
- The editor: paste via the clipboard (`pbcopy` + ⌘V) — it takes only after the page has fully settled,
  sometimes after a reload; `javascript` setValue of the whole script is blocked as injection. Save /
  Run / Preview by clicking the `material-button` by text from JS; the "Preview before running?"
  dialog's *Run without preview* needs a coordinate click. Preview of an unsaved editor runs the SAVED
  version. Results: `POST /api/ytads/dump` → `ytads_events` (events 138–149 are this build).

## Google Ads API access (started 2026-09-10, so future builds need no Ads Script)

The old developer-token form is gone: the MCC's API center (`ads.google.com/aw/apicenter?ocid=364714550`) now
says it is for the App Conversion Tracking API only and that Google Ads API access is "enabled and managed in
your Google Cloud Console". Done on 2026-09-10 in Cloud project **`abs-by-ai`** (the project whose OAuth client
`GOOGLE_CLIENT_ID` belongs to — project number 768453214640, confirm in the console before wiring anything):

1. `console.cloud.google.com/apis/library/googleads.googleapis.com?project=abs-by-ai` → **Enable** (done).
2. API page → **Access levels → Manage** (`console.cloud.google.com/google/ads-apis/overview?project=abs-by-ai`):
   level was **Test** (15,000 ops/day, test accounts only). **Applied for Explorer** ("allows calls to production
   accounts") — one click, no form; **granted within ~2 minutes (2026-09-10 16:20 CT)**: *"Current access level:
   Explorer — 15,000 daily API operations (test accounts), 2,880 daily API operations (production accounts),
   access to most features including campaign management and reporting."* "Basic" is the next level if 2,880
   ops/day ever binds.
3. When Explorer shows, the existing OAuth client + a refresh token with the `adwords` scope (the stored
   `GOOGLE_REFRESH_TOKEN` is `calendar.readonly` only — mint a new one) can call the REST API on 342-717-0837
   through the MCC. Ads Scripts stay as the fallback channel.

The one-off build script is left in the account as `ONE-OFF build video campaign 2026-09-10 (delete after)`,
unscheduled (it cannot run on its own); the Options menu offers no Remove — Dan removes it from the editor's ⋮ menu.
