# Demand Gen conversion campaign — the finished ads, built 2026-09-10

Dan's spec (chat, 2026-09-10): one Google Ads campaign carrying every finished ad, every version
of an ad inside that ad's ad group, one ad group per landing page (`/start` vs the homepage), US +
Canada, male + unknown, 25–54, the custom segments as the audience, no lookalikes yet, $20/day,
target CPA $30 on Free Generation Started, **built PAUSED for his review**.

## What exists in account 342-717-0837

| thing | id / value |
|---|---|
| Campaign `[DAN] [DGEN] [CONVERSION] MU 25-54 \| US+CA \| ad 1 + ad 2 \| start vs home` | `24243839443`, **ENABLED — Dan switched it on in the Ads web UI 2026-09-10 16:12 CT** (API `change_event`; built PAUSED), Demand Gen, Target CPA $30.00, budget `15862488218` **$40.00/day** (read back 2026-09-15; Dan said leave it there), locations by presence |
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
| Ad 1 (both landing pages) | Muhammad 16:9 `lf46ytHacss` → `419514921434`, Zeeshan 16:9 `1oEcwdp21Fg` → `419514919721`, Muhammad vertical `Iz0u8KHRbyE` → `419514921437`, Claude square `VFCQAgzNIkA` → `421227330534`, Claude square 59s `C8tjH0-hPFg` → `421227329091` |
| Ad 2 (both landing pages) | Muhammad 16:9 `Dtk5knWM7c8` → `419623700809`, Muhammad vertical `7XgHxn59Tsg` → `419700324321`, Muhammad square `hHiPzQKTzrg` → `420294626051` |

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

**Policy read through the API, 2026-09-10 17:22 CT** (`node scripts/ads/api/client.js policy 24243839443`):
the Clickbait verdict is gone. 8 of 10 ads APPROVED. The two ads carrying **Zeeshan's 16:9 `1oEcwdp21Fg`**
(824179684065 /start, 824179684203 home) are **APPROVED_LIMITED — `YOUTUBE_AD_REQUIREMENTS_EXAGERRATED_OR_INACCURATE_CLAIMS`**
at ad level (no text line is limited). Dan's new headlines, the rewritten description, the call-to-action and the
`lf46ytHacss` / `1oEcwdp21Fg` video assets were still REVIEW_IN_PROGRESS. Serving status SERVING / LEARNING, $0 spent
at that time. Re-run the command to re-check.

**Dan's copy rule (2026-09-10):** no claim that reads unbelievable without the video's context. *"This
picture got me abs"* is too much; *"How I get abs at 40"* / *"How AI got me abs"* are the shapes to reuse.

## 2026-09-11 — first full day, the retry, Ad 5

**Numbers (09-10 16:12 CT → 09-11 ~10:00 CT):** $20.14 spent, 1,091 impressions, 17 clicks, 225 views,
**0 Free Generation Started** (Bidding: LEARNING_NEW). PostHog confirms the clicks land (~18 visitors: 8 home, 10
`/start`, 2 VSL plays) and none uploaded a photo; the tag itself works (Search logged 7 FGS conversions this week).
Ad 2 took ~80 % of the spend; Ad 2's vertical on home (824221872415) had 283 impressions and 0 clicks.

**Retry rule, attempt 2 (applied at once on Dan's instruction, not after the 2-day $0 wait):** the two Zeeshan
16:9 `1oEcwdp21Fg` ads (824179684065 /start, 824179684203 home) were still APPROVED_LIMITED
(`YOUTUBE_AD_REQUIREMENTS_EXAGERRATED_OR_INACCURATE_CLAIMS`, ad level, no text line flagged) with $0 spent. They are
**PAUSED** and replaced by `… | Zeeshan 16:9 | /start | r2` **824329225648** and `… | home | r2` **824329225651** —
same video, copy that passes `lint.js { tame: true }` (headlines *Abs By AI - Here's How It Works · An AI Picture Of
Yourself With Abs · How The Abs By AI App Works · Daniel Rose On The Abs By AI App · AI Workout And Meal Plans At 40*).
Because the flag is at ad level and the identical copy is APPROVED on the Muhammad ads, the video itself is the
likely trigger — so attempt 3 (clean text-free thumbnail on `1oEcwdp21Fg`) is the probable next step; if that fails,
remove both chains and restore the thumbnail.

**Ad 5 added 2026-09-11 ~10:15 CT** (one atomic 14-op API batch): ad group `Ad 5 Every Diet You've Tried Failed |
/start` **200151423317** (ad **824412395729**) and `… | home` **200151529597** (ad **824329323031**), video asset
`419894297239`, audience **358973573**, US + CA + English on both, `utm_campaign=dgen-conv-ad5`. Its organic upload `bwfSQopZy1w` is private until 09-16, so the ad
runs on a separate **UNLISTED copy `Yo-6TQik3qY`** (Muhammad V3 HD 16:9, Dan's thumbnail B2 "Why Most Diets Fail",
synthetic-media disclosure on, description with "trick" removed). Audience: a new `Ad 5 … | MU 25-54 | AI fitness +
competitor apps + get abs belly fat` (same dimensions as Ad 2's). Copy: Dan's shapes *How I Got Abs At 40* / *How AI
Got Me Abs* plus *Why My Diets Kept Failing · AI Meal Plans Built Around Your Foods · Abs By AI - Here's How It Works*.
Not added: Claude's Ad 5 verticals and Zeeshan's Ad 1 verticals (both still awaiting Dan's approval), Ads 3/4 (no HD
final in `Muhammad Ad Videos/` yet). Budget unchanged at $20/day.

## 2026-09-11 afternoon — Ads 3 + 4 added (first run of `/ad-setup`)

Muhammad's HD finals (Ad 3 v6, Ad 4 V4; both approved 09-10) uploaded UNLISTED and built by the new reusable
builder `scripts/ads/api/dgen-add-ad.js` (configs + read-backs in `scripts/ads/api/dgen-ads/`), 14 atomic ops each,
Google dry run first. Every new ad group carries a **$30 ad-group target CPA**, matching what Dan set on all six
existing groups in the web UI at 13:36 CT today.

| ad | video (asset) | audience | ad group → ad |
|---|---|---|---|
| Ad 3 Stop Paying Human Trainers | `QWW1oumpNg4` | Ad 3 … AI fitness + competitor apps + get abs belly fat | /start **199782847163** → **824427749693**; home **199360345839** → **824344861381** |
| Ad 4 Stop Wasting Money On Supplements | `R08TPEtkjuQ` | Ad 4 … same segments | /start **202812319169** → **824427753506**; home **203842477407** → **824427753800** |

`utm_campaign=dgen-conv-ad3|ad4`. Copy: Dan's *How I Got Abs At 40 · How AI Got Me Abs* on both; Ad 3 adds his
*Fire Your Personal Trainer* + two plain lines; Ad 4 is all his own supplements copy (*How AI Fixed My Supplements ·
Audit Supplements With AI · The Truth About Supplements* and his long headline / description) + plain lines. Budget
unchanged at $20/day, now shared by 10 ad groups.

⚠ **Ad 5 policy, read 09-11 afternoon:** its headline *Why My Diets Kept Failing* is **DISAPPROVED — CLICKBAIT** on
both ads, and the video asset `Yo-6TQik3qY` is APPROVED_LIMITED (exaggerated claims). Dan's rule is to rewrite only
the flagged line; left to the session that owns Ad 5 (ACTIVE TASK entry). The "Why My X Kept Failing" shape is now
refused by `dgen-add-ad.js`.

## 2026-09-12 — Ad 2 square (1:1) added as a third `videos` entry

Ad 2's finished 1:1 re-layout (approved + finalized 09-12) uploaded UNLISTED (`hHiPzQKTzrg`) and added with
`dgen-add-ad.js scripts/ads/api/dgen-ads/ad2-square.json --apply`: reused both existing ad groups and the
existing audience by name, created one video asset and one new ad per landing page — the existing 16:9 and
9:16 ads were untouched. Copy is byte-identical to the existing Ad 2 ads (Dan's *Fire Your Nutritionist. Use
AI Instead · How AI Replaces Nutritionists · How I Got Abs With AI · How I Got Abs At 40 · How AI Got Me
Abs* + the same long headlines/descriptions). Budget unchanged at $20/day, now shared by 3 ads per group
instead of 2.

| ad | video (asset) | ad group → new ad |
|---|---|---|
| Ad 2 Stop Wasting Money On Nutritionists | `hHiPzQKTzrg` → `420294626051` | /start **200136997156** → **824523055421**; home **199420011265** → **824523055424** |

`utm_campaign=dgen-conv-ad2&utm_content=muhammad-square-<start\|home>`. Both new ads ENABLED,
REVIEW_IN_PROGRESS at creation. Check `node scripts/ads/api/client.js policy 24243839443` the next day.

## 2026-09-14 — Ad 1 square (1:1) + its 0:59 cutdown added

Dan approved both Ad 1 square files 09-14 (*"both of these are looking excellent"*). Uploaded UNLISTED —
full length `VFCQAgzNIkA` (3:53), 59s cutdown `C8tjH0-hPFg` (0:50) — with a matching 1080×1080 thumbnail
(`ad1-square-VFCQAgzNIkA_O1-dark-studio-1x1-FINAL.jpg`, same studio-blue-89 source and "HOW TO USE AI / TO
GET IN SHAPE" copy as Ad 1's existing 16:9/9:16 thumbnails) set on both. Added with
`dgen-add-ad.js scripts/ads/api/dgen-ads/ad1-square.json --apply`: reused both existing ad groups and the
existing audience by name, created two video assets and one new ad per video per landing page — the
existing 16:9 and 9:16 ads were untouched. Copy is byte-identical to the live Ad 1 ads, read back from the
account first (Dan's *How I Got Abs At 40 · See Yourself With Abs - Use AI · Abs by AI ® · Abs By AI -
Here's How It Works · How I Got Abs With AI Workouts* + the same long headlines/descriptions); the three
headlines the lint had not seen yet (®, and "How I Got Abs With AI Workouts") were added to `DAN_APPROVED`
in `dgen-add-ad.js` rather than rewritten. Budget unchanged at $20/day, now shared by 5 ads per group
instead of 3.

| ad | video (asset) | ad group → new ad |
|---|---|---|
| Ad 1 This Picture Got Me Abs, square | `VFCQAgzNIkA` → `421227330534` | /start **199420011065** → **824641889488**; home **202965542111** → **824641889494** |
| Ad 1 This Picture Got Me Abs, square 59s | `C8tjH0-hPFg` → `421227329091` | /start **199420011065** → **824641889491**; home **202965542111** → **824641889497** |

`utm_campaign=dgen-conv-ad1&utm_content=claude-square<-59s>-<start|home>`. All four new ads ENABLED,
REVIEW_IN_PROGRESS at creation. Check `node scripts/ads/api/client.js policy 24243839443` the next day —
Ad 1 has a policy history (CLICKBAIT limited on its original copy 09-10, Zeeshan's 16:9 APPROVED_LIMITED
for exaggerated claims), so watch these four closely.

## 2026-09-14 evening — Ad 3 clean 16:9 + 9:16 + 9:16 59s added, smoke-shot ads paused

Dan approved all three 09-14 (*"Okay, all these are looking good, and they are approved."*). Uploaded UNLISTED with
sha256 verified first; added with `dgen-add-ad.js scripts/ads/api/dgen-ads/ad3.json --apply` (3 new `videos`
entries, the old `Muhammad 16:9` entry kept so its ads are recognised). Plan reused both ad groups and audience
`358991501`; 3 video assets + 6 ads, 9 operations. Copy byte-identical to the live Ad 3 ads (all 11 lines read back
APPROVED first). Read-back `ad3.result.json`; the 09-11 original is `ad3.result.20260911.json`.

| version | video → asset | /start 199782847163 | home 199360345839 |
|---|---|---|---|
| Muhammad 16:9 clean (smoke shot replaced) | `86jbUhqBTUQ` → `421279652331` | **824617143813** | **824617143822** |
| Claude 9:16 | `xlC-tigurnA` → `421096838324` | **824617143816** | **824617143825** |
| Claude 9:16 59s | `-wTErCSi640` → `421279652334` | **824617143819** | **824617143828** |

**PAUSED** (not removed, `manual.js` m62/m63): `824427749693` (/start) and `824344861381` (home), the two ads on
`QWW1oumpNg4`, the old 16:9 with the AI breath-smoke shot. Both were APPROVED; the video stays on YouTube.
`utm_content=muhammad-16x9-clean|claude-9x16|claude-9x16-59s-<start|home>`. All six ENABLED, REVIEW_IN_PROGRESS.
Campaign budget read back at **$40/day** (the 09-11 notes say $20; not changed here), shared by more ads now.

⚠ **Trap: a dropped upload still creates a video.** The first vertical upload failed at 90 % (`fetch failed`) and
left an empty unlisted husk `J-fOMvEJwDs` (0 s, stuck processing). List the channel's uploads before any retry.
⚠ **Trap: Google refuses an asset while YouTube is still processing** (`YOUTUBE_VIDEO_DURATION_NOT_DEFINED` in
the dry run) — wait for `processingStatus: succeeded`, then re-run.

## 2026-09-15 — Ads 6, 7, 10 and 14 added

Dan instructed the upload/setup session to use every available export and leave the shared campaign budget at
**$40/day**. All four masters passed the full-frame `compliance:banned_screen` scan before upload. They were uploaded
UNLISTED with chaptered descriptions, tags, custom thumbnails and `containsSyntheticMedia: true`; YouTube read-back
confirmed `processingStatus: succeeded`, `unlisted`, and `embeddable=true`. Each config passed Google `validateOnly`
before its 14-operation atomic apply. Every new group is ENABLED, US + CA, English, male + unknown, age 25–54 +
unknown, carries a **$30 target CPA**, and uses the same three custom segments as Ads 2–4. The campaign itself was
already enabled; its $40/day budget is shared across all groups.

| ad | video → asset | audience | /start group → ad | home group → ad |
|---|---|---|---|---|
| Ad 6 You're Not Too Old | `Je2yvk00SHE` → `421668364056` | `359315789` | `199737961146` → `824793581487` | `200408248299` → `824835138385` |
| Ad 7 Photoshop To AI | `92A3JhaU4wE` → `421486048157` | `358684278` | `200289025116` → `824919205805` | `203111703551` → `824919205814` |
| Ad 10 Busy Dad Fitness | `Sg3vcEY2P_8` → `421589398534` | `359638252` | `206979993984` → `824793606450` | `206979994264` → `824793582135` |
| Ad 14 Workout Video Overload | `z5AfM0fhcIg` → `421486077779` | `359315129` | `205864199888` → `824835458839` | `200914309675` → `824835458866` |

Final URLs use `utm_campaign=dgen-conv-ad6|ad7|ad10|ad14` and `utm_content=muhammad-16x9-<start|home>`.
Copy uses Dan's approved *How I Got Abs At 40* and *How AI Got Me Abs* on every ad, plus plain descriptions of
the age-40 story, Photoshop story, busy-dad system, or workout-video overload. Initial policy read-back: all eight
ads are ENABLED and `REVIEW_IN_PROGRESS`; re-run `node scripts/ads/api/client.js policy 24243839443` the next day.

Known replacement items, explicitly accepted for this launch: Ad 7's better 09-14 re-export fixes the off-screen
header but reads `AI-GENERATEd` at 2:48–2:51; Ad 14 is the available 79 MB / 3.0 Mbps export and should be replaced
when Muhammad supplies V3 HD. Audio was left untouched: Ad 6 −13.7 LUFS / −1.1 dBTP; Ad 7 −14.2 / −1.1; Ad 10
−13.5 / −1.0; Ad 14 −13.9 / −0.8 (the last is 0.2 dB over the preferred true-peak ceiling, documented rather than
processed). Organic/public posting was not part of this run.

## Switched on
Dan enabled campaign 24243839443 in the Ads web UI on 2026-09-10 at 16:12 CT (it had also been flipped on and
off at 15:49). Ad groups and ads were already ENABLED. The API client refuses to enable a campaign itself unless
`ADS_ALLOW_ENABLE_CAMPAIGN=1` — that switch is Dan's.

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

## Google Ads API access (LIVE 2026-09-10 — future builds need no Ads Script)

**Done.** `GOOGLE_ADS_REFRESH_TOKEN` minted 2026-09-10, first calls proven, client `scripts/ads/api/client.js`.
**No developer-token header is needed**, and 342-717-0837 is called with **itself** as `login-customer-id` — it is
not under the MCC. Usage, measured answers and traps: **`Docs/GOOGLE_ADS_API.md`**. How access was obtained:

The old developer-token form is gone: the MCC's API center (`ads.google.com/aw/apicenter?ocid=364714550`) now
says it is for the App Conversion Tracking API only and that Google Ads API access is "enabled and managed in
your Google Cloud Console". Done on 2026-09-10 in Cloud project **`abs-by-ai`** (the project whose OAuth client
`GOOGLE_CLIENT_ID` belongs to — project number 768453214640, confirmed on the project dashboard 2026-09-10):

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
