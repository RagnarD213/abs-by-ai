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
| Ad 1 (both landing pages) | Muhammad 16:9 `lf46ytHacss` → `419514921434`, Zeeshan 16:9 `1oEcwdp21Fg` → `419514919721`, Muhammad vertical `Iz0u8KHRbyE` → `419514921437`, Claude square `VFCQAgzNIkA` → `421227330534`, Claude square 59s `C8tjH0-hPFg` → `421227329091`, Claude vertical 59s `Rk7JxYyKawg` → `422716018685` |
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

## 2026-09-16 — Ad 3 square R2.1 added as-is

Dan explicitly instructed the approved full square R2.1 export to be uploaded as-is after the internal checker
findings were disclosed. The exact SHA-256 `a46861e9d1e3c5f4f517f0b9018d5f129807b9b6f2408382a38492121788646b`
was uploaded UNLISTED as `DXRkrfvcJEM`; picture and audio were not changed. YouTube read-back confirmed the Abs by
AI channel, 1080×1080 HD, 4:26, stereo, embeddable, processed, custom thumbnail, not made for kids and AI-use set to
Yes. The existing 11-chapter description and approved dark-studio thumbnail were reused.

The square-only config passed Google `validateOnly` with exactly three intended operations, then created video asset
`422079967995` and one enabled ad in each existing Ad 3 group. Both are honestly `UNKNOWN / REVIEW_IN_PROGRESS` at
creation; this is not a Google approval claim.

| version | video → asset | /start 199782847163 | home 199360345839 |
|---|---|---|---|
| Claude 1:1 R2.1 | `DXRkrfvcJEM` → `422079967995` | **824906283483** | **824906283486** |

Final URLs use `utm_campaign=dgen-conv-ad3&utm_content=claude-square-r2-1-<start|home>`. Both returned HTTP 200 with
tracking intact. Campaign `24243839443` remains ENABLED at **$40/day** with $30 target CPA; both groups remain ENABLED
at $30 target CPA. The previous three enabled Ad 3 variants and two paused superseded-video ads were unchanged.
The shared gate v1.2.0 FAIL record (24 measured PASS, 3 N/A, 2 FAIL, 6 NOT MEASURED) remains preserved as history;
this one-file user-directed release does not change future gate enforcement. Organic/public posting was not done.

## 2026-09-16 — Ad 14 exact-match HD replacement

Muhammad's 260,253,922-byte V3 HD delivery was compared directly with the approved V3 review export. It has the same
5,924-frame timeline and equivalent untouched audio, with no sampled picture change beyond ordinary re-encoding noise.
The HD master replaced the review-grade file in the project; the earlier 79,337,649-byte file remains beside it as a
superseded archive. The new video `SGJoPjnl6AU` was uploaded **Unlisted**, processed successfully, read back as
embeddable, and received the existing approved Ad 14 thumbnail.

The existing Ad 14 audience and ad groups were reused. Google `validateOnly` passed, then the replacement video asset
`422104479381` and two enabled ads were created. The two old low-bitrate ads were paused only after the replacements
were read back:

| version | video → asset | /start `205864199888` | home `200914309675` |
|---|---|---|---|
| Muhammad 16:9 HD | `SGJoPjnl6AU` → `422104479381` | **824922224568** ENABLED, review in progress | **824922224571** ENABLED, review in progress |
| Superseded review-grade | `z5AfM0fhcIg` → `421486077779` | **824835458839** PAUSED | **824835458866** PAUSED |

Final URLs use `utm_campaign=dgen-conv-ad14&utm_content=muhammad-16x9-hd-<start|home>`. The campaign, shared budget,
audience, landing pages, copy, groups and $30 target CPA were unchanged. At that checkpoint, Ads 8, 9, 13 and 15 were not added because
their HD deliveries contain visual edits versus the finalized review references and therefore did not pass the
resolution-only identity condition. Organic/public posting was not done.

## 2026-09-16 — Ads 8, 9, 13 and 15 finalized and added

After reviewing the visual differences from their earlier review proxies, Dan explicitly declared Muhammad's delivered
HD exports finalized. The byte-matching filed masters were uploaded to channel `UC236gjadarHAhEhOMYNGJ9g` as Unlisted,
processed successfully, read back as embeddable, and given their approved dark-studio thumbnails. Descriptions include
chapters, disclosure and tracked homepage links.

Each config passed Google `validateOnly` with 14 intended operations before apply. Four video assets, four audiences,
eight $30-target-CPA ad groups and eight enabled ads were created and read back:

| Ad | video → asset | audience | `/start` group → ad | home group → ad |
|---|---|---|---|---|
| Ad 8 Two AI Futures | `HMZdiJMAI3Y` → `422033285275` | `359424266` | `201149830478` → **`824925649893`** | `203342192834` → **`824966555242`** |
| Ad 9 ChatGPT For Abs | `l4myK7f-sKo` → `422033283313` | `359424269` | `200857678952` → **`824966559286`** | `198969095463` → **`824966559307`** |
| Ad 13 The Cost Of Getting Abs | `hrQf1240kQA` → `421933351559` | `359747866` | `197465035822` → **`824925676464`** | `200980520340` → **`824966566927`** |
| Ad 15 Dad In A T-Shirt | `TqXD2dGgAPs` → `422033325238` | `359743849` | `199925345509` → **`825050916875`** | `198969095983` → **`824925650094`** |

Final URLs use `utm_campaign=dgen-conv-ad8|ad9|ad13|ad15` and
`utm_content=muhammad-16x9-<start|home>`. Policy read-back shows all eight ads ENABLED and
`REVIEW_IN_PROGRESS`. Campaign `24243839443` remains ENABLED at its unchanged **$40/day shared budget**; every new ad
group has the existing $30 target CPA, and no prior campaign assets were changed.

Muhammad's audio was uploaded untouched. Measurements: Ad 8 −14.3 LUFS / −1.9 dBTP; Ad 9 −14.5 / −0.9; Ad 13 −14.1 /
−1.0; Ad 15 −14.0 / −0.9. Ads 9 and 15 exceed the preferred true-peak ceiling by 0.1 dB; this was documented rather
than processed, under the standing editor-audio rule. Organic/public posting was not done.

## 2026-09-18 — Ad 1 Claude vertical 59s added

Dan approved the exact AV-01 cutdown as-is: *“That ad looks good to me. I think that's actually good to ship.”* The
61,749,767-byte master was filed without transcoding and re-hashed as
`aaa81b8a09c673285f18dd4df776a6355dc238e713e13f1cbdc9096d86f61c69`. It is 1080×1920, 1,493 frames and
49.816 seconds. Muhammad's cut audio remains verbatim at −14.40 LUFS / −1.30 dBTP. The exact-file delivery record
remains honest: 34 PASS / 2 FAIL for inherited visual findings that Dan explicitly accepted; no threshold or media
was changed.

YouTube video **`Rk7JxYyKawg`** was uploaded with the AI-content disclosure, processed successfully and read back on
channel `UC236gjadarHAhEhOMYNGJ9g` as **Unlisted**, embeddable and 0:50. The approved Ad 1 dark-studio vertical
thumbnail was reused and read back. No Public or organic copy was created.

Google `validateOnly` proposed exactly one new video asset and two new ads, then the same three-operation batch was
applied. The live Ad 1 copy was read from ad `824641889491` and reused byte-for-byte.

| version | video → asset | `/start` group `199420011065` → ad | home group `202965542111` → ad |
|---|---|---|---|
| Claude vertical 59s | `Rk7JxYyKawg` → **`422716018685`** | **`825155890776`** | **`825155890779`** |

Both ads are ENABLED and `UNKNOWN / REVIEW_IN_PROGRESS`. Final URLs carry
`utm_campaign=dgen-conv-ad1&utm_content=claude-vertical-59s-<start|home>`. Audience `358261317`, both $30 target-CPA
groups, every existing ad, campaign state, Target CPA bidding, and the shared **$40/day** budget were read back
unchanged.

## 2026-09-18 — Ad 14 Codex R4 16:9 added

Dan approved the complete R4 film as-is on 2026-09-17. The exact 213,660,168-byte master was re-hashed as
`515953918d223c389754153cd1fa6388ba9d2d18b942024b6c680d3184979785` immediately before upload; it was not
transcoded. Its recorded review remains honest: audio PASS 13/13 at −14.20 LUFS / −1.90 dBTP; delivery gate 31
measured PASS, 3 N/A, 1 inherited FAIL and 1 NOT MEASURED, all known when Dan approved the exact film.

YouTube video **`ACfVyQqPK08`** was uploaded with the AI-content disclosure and R4-specific chapters. It processed
successfully and read back on channel `UC236gjadarHAhEhOMYNGJ9g` as **Unlisted**, HD, embeddable, not made for kids
and 3:48. The existing approved Ad 14 dark-studio thumbnail was reused; its served maxres file was byte-identical to
the Muhammad Ad 14 thumbnail readback. No Public or organic copy was created.

Google `validateOnly` proposed exactly one new video asset and two new ads in the existing groups, then that same
three-operation batch was applied:

| version | video → asset | `/start` group `205864199888` → ad | home group `200914309675` → ad |
|---|---|---|---|
| Codex R4 16:9 | `ACfVyQqPK08` → **`422819661961`** | **`825282142526`** | **`825282142529`** |

Both R4 ads are ENABLED and `UNKNOWN / REVIEW_IN_PROGRESS`. Final URLs carry
`utm_campaign=dgen-conv-ad14&utm_content=codex-r4-16x9-<start|home>`. The live readback preserved campaign
`24243839443` as ENABLED with Target CPA bidding and the same **$40/day shared budget**; both Ad 14 groups remain
ENABLED at $30 target CPA; Muhammad HD ads `824922224568` / `824922224571` remain ENABLED and APPROVED; superseded
review-grade ads `824835458839` / `824835458866` remain PAUSED. Audience `359315129`, copy and landing pages were
unchanged.

## 2026-09-18 — RA-01 How AI Got Me Abs added as a new ad

Dan approved the exact RA-01 9:16 and 16:9 masters as-is, including the audio. SHA-256 verification matched the
locked handoff values before upload: `02d032180a3eb42dc81d1857613df55ef4b715ab4d31e315834baf2a63003e51`
(9:16) and `bcace8c490c8c8a3f105469c106ee1cbe40f4d839fb480fd7781fb1e4afb6a45` (16:9). Both 57.190-second files
were uploaded without transcoding as **Unlisted**, with `containsSyntheticMedia: true`, and read back on channel
`UC236gjadarHAhEhOMYNGJ9g` as processed, embeddable and `privacyStatus=unlisted`. The installed thumbnails use the
new `studio-blue-109` portrait and compliant copy `SEE YOURSELF / WITH ABS`; both O1 dark-studio and O2 own-backdrop
versions exist in each aspect, with O1 installed. No Public or organic copy was created.

Config `scripts/ads/api/dgen-ads/ra01.json` passed Google `validateOnly` first with exactly 17 new operations: two
video assets, one audience, two $30-target-CPA ad groups, their normal US + CA / English / audience criteria, and
four ads. It reused or modified nothing. The identical batch was then applied and read back:

| version | YouTube → asset | audience | `/start` group → ad | home group → ad |
|---|---|---|---|---|
| Claude vertical | `rfCsWNxuNV0` → **`422804568080`** | **`359952376`** | `195593120770` → **`825172744302`** | `201008893635` → **`825172744311`** |
| Claude 16:9 | `OUw788sF1KY` → **`422804571407`** | **`359952376`** | `195593120770` → **`825172744305`** | `201008893635` → **`825172744314`** |

All four ads are ENABLED and `UNKNOWN / REVIEW_IN_PROGRESS`. Final URLs use
`utm_campaign=dgen-conv-ra01&utm_content=claude-vertical|claude-16x9-<start|home>`. The `/start` ads point to
`https://absbyai.com/start`; the home ads point to `https://absbyai.com/`. Live readback before and after the build
kept campaign `24243839443` ENABLED on Target CPA and preserved budget resource `15862488218` at **$50/day**; no
budget operation was sent. Existing ads, assets, ad groups, bids and statuses were untouched. Re-run
`node scripts/ads/api/client.js policy 24243839443` the next day for the final policy verdict.

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

## 2026-09-21 - Ads 9 + 13 swapped to Muhammad's round 4 finals

Dan finalized round 4 (Ad 9: matching ChatGPT label 0:14, real-photo chip 1:56; Ad 13: real-photo chip 0:41). Files
filed untouched over the masters (09-16 files kept as `… (09-16).mp4`); durations identical, so chapters unchanged.
Audio: Ad 9 -14.5 LUFS / -0.9 dBTP, Ad 13 -14.1 / -1.0. Uploaded Unlisted, processed, embeddable, same thumbnails,
title, description and tags as the live videos.

| Ad | new video → asset | `/start` ad | home ad | paused old ads |
|---|---|---|---|---|
| Ad 9 | `zvVk680kSfo` → `423683149862` | **`825520817992`** | **`825520817995`** | `824966559286`, `824966559307` |
| Ad 13 | `-SuKGXGcbIg` → `423865478571` | **`825601774244`** | **`825601774247`** | `824925676464`, `824966566927` |

Same copy, groups and audiences; `utm_content=muhammad-16x9-r4-<start|home>`. New ads ENABLED, `REVIEW_IN_PROGRESS`.
⚠ Campaign budget read back **$50/day** on 09-21 (docs said $40); unchanged by this session.

**2026-09-22 verdict:** all four new ads came back APPROVED / REVIEWED. Removed the four paused old ads
(`824966559286`, `824966559307`, `824925676464`, `824966566927`); read back gone, new four still ENABLED.
`l4myK7f-sKo` / `hrQf1240kQA` marked retired in `Docs/AD_VIDEO_IDS.md`, left up on YouTube unlisted.
Budget re-checked, still **$50/day** (docs say $40, unchanged).

## 2026-09-21 - Ad 15 final version swapped in

Dan finalized Muhammad's round 3 HD (Drive `1V1zsBIQn2XfhDhhJGSKA10F3tV2MQHYU`). Claude added the AI-GENERATED tag on the
prospect's after picture (3:18.8-3:20.4) and replaced the repeated goal-image insert (2:30.9-2:34.8) with camera scene
recovered from raw C1604. Only those spans changed: every other frame is bit-identical to his export, audio bit-exact.
Master MD5 `595b434550202d44de8a1ed7f173d88c`, uploaded Unlisted as `5GQQHP8bpM4` (processed, embeddable, same thumbnail).

`ad15.json` gained a second `videos` entry (`Muhammad 16:9 final`, utm `muhammad-16x9-final`). Google `validateOnly`
passed 3 operations, then applied: new video asset, `/start` group `199925345509` → **`825607455071`**, home group
`198969095983` → **`825607455074`**, both ENABLED and `REVIEW_IN_PROGRESS`. Campaign budget read back at $50/day,
not changed by this work.

2026-09-22: both new ads read APPROVED, so the old ads `825050916875` (/start) and `824925650094` (home), on
`TqXD2dGgAPs`, were PAUSED via `dgen-ads/ad15-pause-0916-ads.json`; new ads ENABLED. YouTube `TqXD2dGgAPs` kept for Dan to delete.

## 2026-09-25: Ad 10 approved verticals

The exact AV-07 masters (SHA256 `b25b6e50e106cc4c6407fc949ff6edda25ceab8b1c75a559eff6427b0fc32cc6` and `36ae2f6d528ebf34692e81040343c88d17046eff27a25bc1c266f2fd816dd00f`) were uploaded to YouTube as Unlisted. Both processed in HD, are embeddable, and have the matching 9:16 thumbnail set and read back. The uploads were made with `containsSyntheticMedia=true`, category 26, and not made for kids. No organic publication.

| version | YouTube | video asset | `/start` group / ad | home group / ad |
|---|---|---|---|---|
| Claude 9:16 | `4nDWFmdjzQQ` | `424707539263` | `206979993984` / `825998531965` | `206979994264` / `825998531971` |
| Claude 9:16 59s | `CR4WAVmSuXY` | `424707544210` | `206979993984` / `825998531968` | `206979994264` / `825998531974` |

The live Ad 10 copy matched `ad10.json`, so it was reused. All four new ads are ENABLED and `REVIEW_IN_PROGRESS` as of 2026-09-25. Recheck policy on 2026-09-26. `/start` URLs use `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-ad10&utm_content=claude-9x16[-59s]-start`; home URLs use `https://absbyai.com/?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-ad10&utm_content=claude-9x16[-59s]-home`. Exact per-ad URLs and IDs are in `scripts/ads/api/dgen-ads/ad10.result.json`. The original 16:9 asset `421589398534` and ads `824793606450` and `824793582135` remain enabled. Both ad groups retain their $30 target CPA and audience `359638252`. The live shared campaign budget read $50/day before the change, versus $40/day in the earlier record. It was preserved at $50/day and is now shared by these additional ads.

## 2026-09-27: DS-18 How To Kettlebell Deadlift added as a new ad

**2026-09-28: RETIRED, it was never an ad.** DS-18 is an organic Short (ends "Leave me a comment", no tap-the-button CTA). Dan caught the mistake; both ad groups `201586678778` and `200462519173` were PAUSED via `dgen-ads/ds18-pause-organic.json` after 90 impressions and $0.62. Budget still $50/day. The YouTube upload was switched to Private and it now releases organically through Blotato (`Docs/DS18_SETUP_RECEIPT_20260928.md`).

Dan finalized Codex R8 on 09-25. The master `Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4` matched the
locked SHA256 `aa7fe8747dcb3a4a8b26e1b32b598c1c502606ee00efe878ee99aaf2d1b60ba2` (81,989,796 bytes) and was uploaded
once, untouched, as **Unlisted** `CMsb0qbo2vM`. Readback: channel `UC236gjadarHAhEhOMYNGJ9g`, `privacyStatus=unlisted`,
processing succeeded, embeddable, HD, 1080x1920, 29.97 fps, PT42S, file size identical to the master. The footage is
all real camera (C1671/C1673) plus graphics, so the upload set `containsSyntheticMedia=false`. The thumbnail is a
JPG export of Dan's approved cover C r5 (set + maxres read back). Metadata: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/youtube/`.
Delivery gate for this file remains **FAIL, 33 passed, 6 failed, 3 n/a** (`audio:stamp`, `framing:no_wide_level`,
`framing:push_coverage`, `captions:burned`, `captions:sync`, `compliance:placeholder`); Dan finalized it knowing that.

Config `scripts/ads/api/dgen-ads/ds18.json` (RA-01's three custom segments) passed `validateOnly` with 14 operations,
then applied and read back:

| version | YouTube → asset | audience | `/start` group → ad | home group → ad |
|---|---|---|---|---|
| Codex vertical R8 | `CMsb0qbo2vM` → **`425260237702`** | **`359808627`** | `201586678778` → **`826267702259`** | `200462519173` → **`826267702268`** |

Both ads ENABLED, $30 target CPA, `REVIEW_IN_PROGRESS` on 09-27; recheck policy 09-28. URLs use
`utm_campaign=dgen-conv-ds18&utm_content=codex-vertical-r8-<start|home>` (both return 200). Campaign `24243839443`
read ENABLED, Target CPA, budget `15862488218` **$50/day** before and after; no budget operation sent. The 28 existing
ad groups and 64 existing ads read back with identical statuses and target CPAs. The $50/day is now shared by two
more ad groups. No organic copy.

## 2026-10-01: Ad 8 approved verticals

Dan approved both AV-09 masters on 2026-10-01 ("these ads are approved and good to publish"). Both files matched their
recorded SHA256 (`320d14a3...795b5d` full, `e0b8cee1...a400c` 59s) and were uploaded once, untouched, as **Unlisted**
with `containsSyntheticMedia=true`, category 26, not made for kids. Readback on both: channel
`UC236gjadarHAhEhOMYNGJ9g`, `privacyStatus=unlisted`, processing succeeded, HD, embeddable (PT3M31S and PT57S). One
9:16 thumbnail (option A, dark studio, `studio-white-42`, "AI SHOWED ME / TWO FUTURES") was set and read back on both.

`validateOnly` passed with exactly 6 operations (2 video assets, 4 ads), then applied and read back:

| version | YouTube | asset | `/start` group / ad | home group / ad |
|---|---|---|---|---|
| Claude 9:16 | `wsNG444pkNg` | `425910585172` | `201149830478` / `826574115981` | `203342192834` / `826574115987` |
| Claude 9:16 59s | `DP5qT2E962o` | `425910599623` | `201149830478` / `826574115984` | `203342192834` / `826574115990` |

The live Ad 8 copy matched `ad8.json`, so it was reused. All four new ads are ENABLED and `REVIEW_IN_PROGRESS` as of 2026-10-01. Recheck policy on 2026-10-02. `/start` URLs use `utm_campaign=dgen-conv-ad8&utm_content=claude-9x16[-59s]-start`; home URLs use `utm_content=claude-9x16[-59s]-home`. Exact per-ad URLs and IDs are in `scripts/ads/api/dgen-ads/ad8.result.json` (the 09-16 result is kept as `ad8.result.20260916.json`). The original 16:9 asset `422033285275` and ads `824925649893` and `824966555242` remain ENABLED and APPROVED. Both ad groups keep their $30 target CPA and audience `359424266`. The campaign budget `15862488218` read $50/day before and after (the handoff said $40/day; the live value was kept); no budget operation was sent. No organic copy.

## 2026-10-01: new TRIAL campaign to the /start sales page (campaign `24316364155`)

Dan's spec (`Handoffs/handoff-20261001-vsl-trial-campaign-six-ads.md`): `[DAN] [DGEN] [TRIAL] VSL page | 6 ads | MU 25-54 | US+CA`,
$50/day, target CPA $40 on the campaign and on every ad group, Trial Signup (`7704441545`, SIGNUP / WEBSITE) as the only
campaign-specific goal, one ad group per ad, every ad to `https://absbyai.com/start`. Built by
`scripts/ads/api/dgen-trial-campaign.js` (44 operations, `validateOnly` then applied; readback in
`scripts/ads/api/dgen-ads/trial-campaign.result.json`). Each ad is a clone of its approved twin in `24243839443`: same
video asset, copy, logo, call to action and Audience. **ENABLED 2026-10-01 on Dan's instruction, not held for review.**
Campaign `24243839443` was already PAUSED when this session started, so total Demand Gen budget is $50/day.

**Trial conversion proved first.** `/start` buttons go to `/?join=1&from=vsl&v=letter-v1` plus the click id and UTMs; the
cart opens; `create-cart-checkout` on production returned a live session whose metadata carried the click id (session
expired unpaid, no card run); locally `handleCartComplete` sent one conversion to `AW-18361229851/AqLTCMnl4dkcEJvEqLNE`
(value 20 USD, `gclaw` = the landing click id). There are no Stripe test keys, so the card step itself was not run.
Google Ads: the action is ENABLED, last recorded 2026-09-19 (all conversions 1).

| ad group | id | ads (version → ad id) |
|---|---|---|
| Ad 13 The Cost Of Getting Abs | `204553316830` | Muhammad 16:9 r4 `826635661894` |
| RA-01 AI Got Me Abs | `206348100928` | Claude 16:9 `826595554299`, Claude vertical `826595554302` |
| Ad 10 Busy Dad Fitness | `202248166482` | Muhammad 16:9 `826635657832`, Claude 9:16 `826635657835`, Claude 9:16 59s `826635657838` |
| Ad 4 Stop Wasting Money On Supplements | `204553317030` | Muhammad 16:9 `826635661909` |
| Ad 3 Stop Paying Human Trainers | `204320854441` | Muhammad 16:9 clean `826635679183`, Claude 9:16 `826635679186`, Claude 9:16 59s `826635679189`, Claude 1:1 R2.1 `826635679192` |
| Ad 6 You're Not Too Old | `204444440607` | Muhammad 16:9 `826595554443` |

URLs: `utm_campaign=dgen-trial-<ad13|ra01|ad10|ad4|ad3|ad6>&utm_content=<version>-vsl`. All 12 ads `REVIEW_IN_PROGRESS` at
build; recheck with `node scripts/ads/api/client.js policy 24316364155`.

**Frequency cap of 4 per user per day: NOT SET, Google does not offer it here.** The API refuses `frequency_caps` on a
Demand Gen campaign on create and on update (`OPERATION_NOT_PERMITTED_FOR_CONTEXT`), and the campaign and ad group
settings pages in the Ads interface have no frequency setting for this campaign type.

**Watch:** the settings page warns that Trial Signup has had no conversions in the last 7 days, so target CPA bidding has
almost nothing to learn from. If there is no delivery by 2026-10-04, report it to Dan with options.
New formats of Ads 13, 4 and 6 go into these ad groups: add the video id to `ADS` in the script once its twin exists, or
build the ad with `/ad-setup` pointed at campaign `24316364155`.

**2026-10-01, Ad 10 headlines (Dan's own, trial campaign only):** all three Ad 10 ads in `24316364155` now carry
"How Busy Dads Get Abs", "How 40+ Dads Can Get Abs", "A Busy Dad's Fitness System", "How I Got Abs At 40",
"How I Lost Belly Fat With AI". Long headlines and descriptions unchanged. The old campaign's Ad 10 copy was not touched.

**2026-10-01, Ad 3 headlines (Dan's own, trial campaign only):** all four Ad 3 ads in `24316364155` now carry
"Fire Your Personal Trainer", "How AI Replaces Personal Trainers", "Human Trainers Hate Him", "How I Got Abs At 40",
"Trainers Hate This AI App". Long headlines and descriptions unchanged. The old campaign's Ad 3 copy was not touched.

## 2026-10-02: new thumbnails on the trial campaign's 12 ad videos (campaign `24316364155`)

Dan's picks from the Codex thumbnail rounds (`social media graphics/youtube/thumbnails/_trial-campaign-20261001/picks.json`)
were installed on all 12 YouTube videos behind the six ads, **2026-10-02 11:16 to 11:17 AM CT**. Compare click-through for
the 7 days before this moment against the 7 days after. Nothing in Google Ads was edited. Each file sits in
`social media graphics/youtube/thumbnails/<ad folder>/trial-20261001/`; the `before-<id>.jpg` there restores the old
thumbnail with `node scripts/youtube/set-thumbnail.js --video <id> --file <before file>`.

| video | YouTube id | option | before file | read back file | ad, status after install |
|---|---|---|---|---|---|
| Ad 13 16:9 | `-SuKGXGcbIg` | 13-R3B | `before--SuKGXGcbIg.jpg` | `readback--SuKGXGcbIg.jpg` | `826635661894` ENABLED, APPROVED |
| RA-01 16:9 | `OUw788sF1KY` | RA-R2A | `before-OUw788sF1KY.jpg` | `readback-OUw788sF1KY.jpg` | `826595554299` ENABLED, APPROVED |
| RA-01 9:16 | `rfCsWNxuNV0` | RA-R2A | `before-rfCsWNxuNV0.jpg` | `readback-rfCsWNxuNV0.jpg` | `826595554302` ENABLED, APPROVED |
| Ad 10 16:9 | `Sg3vcEY2P_8` | 10-R2A | `before-Sg3vcEY2P_8.jpg` | `readback-Sg3vcEY2P_8.jpg` | `826635657832` ENABLED, APPROVED |
| Ad 10 9:16 | `4nDWFmdjzQQ` | 10-R2A | `before-4nDWFmdjzQQ.jpg` | `readback-4nDWFmdjzQQ.jpg` | `826635657835` ENABLED, APPROVED |
| Ad 10 9:16 | `CR4WAVmSuXY` | 10-R2A | `before-CR4WAVmSuXY.jpg` | `readback-CR4WAVmSuXY.jpg` | `826635657838` ENABLED, APPROVED |
| Ad 4 16:9 | `R08TPEtkjuQ` | 4-R2A | `before-R08TPEtkjuQ.jpg` | `readback-R08TPEtkjuQ.jpg` | `826635661909` ENABLED, APPROVED |
| Ad 3 16:9 | `86jbUhqBTUQ` | 3-R2A | `before-86jbUhqBTUQ.jpg` | `readback-86jbUhqBTUQ.jpg` | `826635679183` ENABLED, APPROVED |
| Ad 3 9:16 | `xlC-tigurnA` | 3-R2A | `before-xlC-tigurnA.jpg` | `readback-xlC-tigurnA.jpg` | `826635679186` ENABLED, APPROVED |
| Ad 3 9:16 | `-wTErCSi640` | 3-R2A | `before--wTErCSi640.jpg` | `readback--wTErCSi640.jpg` | `826635679189` ENABLED, APPROVED |
| Ad 3 1:1 | `DXRkrfvcJEM` | 3-R2A | `before-DXRkrfvcJEM.jpg` | `readback-DXRkrfvcJEM.jpg` | `826635679192` ENABLED, APPROVED |
| Ad 6 16:9 | `Je2yvk00SHE` | 6-R3B | `before-Je2yvk00SHE.jpg` | `readback-Je2yvk00SHE.jpg` | `826595554443` ENABLED, APPROVED |

- Every read back was opened and matches the picked image. On the 9:16 and 1:1 videos YouTube shows the whole image
  centred with blurred sides; no head or text is cut.
- All 12 videos read back Unlisted with the same title, description and tags as before the install.
- Policy right after the install: all 12 ads ENABLED, APPROVED / REVIEWED, and every `YOUTUBE_VIDEO` asset APPROVED. A new
  thumbnail can send an ad back into review, so recheck 2026-10-03: `node scripts/ads/api/client.js policy 24316364155`.
- No challenger thumbnails are held for a later test (`challenger: null` on every video).
- No vertical or square of Ads 13, 4 or 6 exists in the campaign yet; when one is added it needs its own thumbnail.
- PostHog annotation not added: the stored key lacks the `annotation:write` scope.

## 2026-10-02: RA-01 1:1 square added to the trial campaign (campaign `24316364155`)

Dan approved the RA-01 square (AS-13) on 2026-10-02. YouTube `EfoVnGyAJjk`, Unlisted, "How AI Got Me Abs", same description
and tags as `OUw788sF1KY` / `rfCsWNxuNV0`, AI flag false like them (still AI goal images with the on-screen label, no AI
footage). File SHA-256 `3e7939bc...ecedd` asserted before upload. Thumbnail RA-R2A in 1:1 (`RA-01 | 1x1 | FINAL.jpg`; build
`scripts/covers/trial-campaign-20261001/round2-square/build.py`, existing Codex plate `ra01-C`, no new generation). Ad closing
words: "tap the button below", so an ad. Not posted anywhere organic.

Built by `scripts/ads/api/dgen-ra01-square.js` from `dgen-ads/ra01-square.json` (readback `ra01-square.result.json`): video
asset `426180248591`, ad `826755066385` "RA-01 AI Got Me Abs | Claude 1:1 | vsl" in the EXISTING ad group `206348100928`
(reused, validateOnly first), ENABLED, `REVIEW_IN_PROGRESS`. Final URL `...utm_campaign=dgen-trial-ra01&utm_content=claude-square-vsl`.
Headlines, long headlines and descriptions were read back from the live 16:9 ad `826595554299` and are identical. Budget,
bids, audience and the other ads were not touched. The old Demand Gen campaign `24243839443` is PAUSED, so its RA-01 groups
(`195593120770`, `201008893635`) were left alone.

**Clickbait long headline replaced (Dan, 2026-10-02):** the line "AI genius / Busy dad discovers how to use AI to lose his
stubborn belly fat. Video reveals full story" was DISAPPROVED (CLICKBAIT) on RA-01 16:9 and 9:16, Ad 6 and two Ad 10 ads, and
sat unflagged on the third Ad 10 ad and the new square. Account-wide scan (2,254 text lines, every campaign) found it only in
trial campaign `24316364155`. All 7 ads now carry Dan's line "Korean AI prodigy discovers how to use AI to lose belly fat.
Video reveals full story." in that slot (other lines untouched; `scripts/ads/api/dgen-replace-longheadline-20261002.js`, old
state in `dgen-ads/longheadline-replace-20261002.before.json`). All 7 back in review; recheck 2026-10-03:
`node scripts/ads/api/client.js policy 24316364155`. Other disapproved lines found in the scan and NOT changed (different
text): Ad 5 headline "Why My Diets Kept Failing" (paused campaign), the engagement campaigns' "late night snacking" and
"trains abs daily" lines and "The Truth About Protein Shakes" (paused or old), and the "trains abs daily" description on the
two remarketing ads in `24316408288`.

## 2026-10-01: conversion REMARKETING campaign to /start (campaign `24305381214`)

Dan's spec: `Handoffs/handoff-20261001-remarketing-campaigns-conversion-and-subscriber.md`. Built by
`scripts/ads/api/dgen-rmktg-campaigns.js a --no-frequency-cap --apply`; read-back in
`scripts/ads/api/dgen-ads/rmktg-campaign-a.result.json`. It shows the cold trial campaign's ads only to people who
already visited absbyai.com or already watched one of Dan's YouTube videos.

- Name `[DAN] [DGEN] [TRIAL] [RMKTG] VSL page | 6 ads | US+CA | site visitors + youtube viewers`. **$10/day**, target
  CPA **$40**, campaign goal **Trial Signup only** (SIGNUP / WEBSITE), US + Canada by presence, English, male + unknown,
  25-54 + unknown, optimized targeting off. Built PAUSED.
- Both groups exclude members and purchasers: `website | member hub | 540 day` `9480144404` (new, rule: URL contains
  `/vp/hub`), `All Converters` `9441311426`, `Purchasers of Abs By AI` `9469016618`. The exclusions sit inside each
  Audience object (`exclusionDimension`); the API accepts them there.

| Ad group | Id | Audience | Lists | Ads |
|---|---|---|---|---|
| Website visitors, 7 + 30 + 365 day | `206411886211` | `361150564` | `9452848282`, `9453529251`, `9452257061` | 12: `826720144313`, `…316`, `…319`, `826720144442`, `…445`, `…448`, `…451`, `…454`, `…457`, `…460`, `…463`, `…466` |
| YouTube viewers, watched any video 7 + 30 day | `201604959278` | `361150567` | `9453532227`, `9452269226` | 12: `826637064679` through `826637064712` (every third id) |

Each group holds a copy of all 12 enabled ads of cold campaign `24316364155` (six ads, every format), with the copy that
was live there at build time, including Dan's 10-01 headlines on Ad 10 and Ad 3. Ad names: the cold name plus
`| rmktg-site` or `| rmktg-yt`. URLs: `utm_campaign=dgen-rmktg-<site|yt>&utm_content=<ad>-<version>-vsl`
(the ad key is in `utm_content` because one campaign value now covers all six ads).

**List windows fixed the same day.** Every list reported a 30 day membership whatever its name said. Now: website 7 day
`9452848282` = 7 (lookback 7), website 365 day `9452257061` = 365 (lookback 365), YouTube 7 day `9453532227` = 7,
subscribers 540 day `9452604668` = 540. The two 30 day lists were already right. The other mis-named lists (14 day,
540 day, liked, channel page, paywall, generation) were not touched; fix one before using it. Update trap: the mask
`rule_based_user_list.flexible_rule_user_list` is refused (`FIELD_HAS_SUBFIELDS`); use
`…flexible_rule_user_list.inclusive_operands` for the lookback, and `membership_life_span` on its own works for
YouTube lists.

**No frequency cap**, same as the cold campaign: the API refuses it on Demand Gen.

**Keeping it in step with the cold campaign.** This is a snapshot. When a new format of Ad 13, 4 or 6 (or any ad) is
enabled in `24316364155`, re-run `node scripts/ads/api/dgen-rmktg-campaigns.js a --no-frequency-cap --apply`: it adds
only the ads that are missing, to both groups. A headline change in the cold campaign does not carry over by itself.

**Enable both** (after review; ads were still `REVIEW_IN_PROGRESS` when the build session ended):
`ADS_ALLOW_ENABLE_CAMPAIGN=1 node scripts/ads/api/client.js mutate scripts/ads/api/dgen-ads/rmktg-enable.json --note "enable remarketing campaigns"`,
then add a PostHog annotation.

**Watch (report 2026-10-04):** the website group draws on about 110 to 430 people and may not deliver at all. Report its
served status. Subscriber remarketing (Campaign B, `24316408288`) is documented in `Docs/YTADS.md`.

**2026-10-01, Dan rewrote headlines on all six trial ads in the Ads editor.** RA-01, Ad 6, Ad 13 and Ad 4 as well as
Ad 10 and Ad 3; his lines were then copied to every other format of each ad by API and read back (his editor Save
had reverted the first sync). Live copy is the source of truth; the before and after table is in skill `/ad-copy`.

## 2026-10-02: Performance Max TRIAL campaign for the $450 credit (campaign `24308574894`)

Dan's spec: `Handoffs/handoff-20261001-pmax-campaign-build.md`. Built by `scripts/ads/api/pmax-trial-campaign.js`
(`images` uploads the pictures, then 158 operations, `validateOnly` then applied; read-back in
`scripts/ads/api/dgen-ads/pmax-campaign.result.json`). Built PAUSED, read back, **ENABLED 2026-10-02 12:50 PM CT** on
Dan's standing instruction. One campaign only: Dan dropped the remarketing Performance Max idea the same day.

**The credit (Billing > Promotions, read 2026-10-02):** "$450.00 ad credit to spend on Performance Max campaigns", code
`CYYVM-MMLQT-E9FK`, redeemed 2026-10-01, status Active ("applied to your account, and is funding your campaign(s)").
"Complete requirements by" is blank, so no paid spend is needed first. **Expires 2026-11-30.** Credits spent: no data yet.

| Setting | Stored value |
|---|---|
| Name | `[DAN] [PMAX] [TRIAL] VSL page | 6 ads | US+CA | site visitors 30 day` |
| Budget | $15/day (budget `15923601274`, not shared), start 2026-10-02, **end 2026-11-01** |
| Bidding | Maximize conversions, no target. Add a $40 target after the first few trials. |
| Goal | Campaign level, Trial Signup (SIGNUP / WEBSITE) the only biddable goal |
| Asset group | `6754766656` "VSL page | 6 ads | 20 images" |
| Final URL | `https://absbyai.com/start?utm_source=google&utm_medium=pmax&utm_campaign=pmax-trial` |
| Final URL expansion, text customization, video enhancements, image enhancements, image extraction | all OPTED_OUT |
| Location, language | US + Canada, presence only; English |
| Excluded | ages 18-24 and 65+; female; lists `9480144404`, `9441311426`, `9469016618` (members, converters, purchasers) |
| Negative keywords | 90 at campaign level: the 83 on Non-Brand Search `24148587722` plus free, generator, abs editor, abs creator, six pack ai, ai six pack, give me abs ai. No brand terms, no brand exclusion list. |
| Audience signal | Audience `360314754`: list `9453529251` (website visitors, 30 day; about 110 people on Display, 370 on Search) and nothing else. No search themes. |

**Assets.** 15 headlines, 5 long headlines and 5 descriptions, all Dan's own lines as live in `24316364155` (the script
refuses any line that is not live there). Headlines left out: "How AI Replaces Personal Trainers" (33 characters, over
the limit of 30), and five that did not fit the 15 slots ("Human Trainers Hate This AI", "Human Trainers Despise Him",
"Trainers Despise Him", "How Busy 40+ Dads Lose Fat", "The Truth About Supplements"). No new line was written.
Five videos (the limit): Ad 13 16:9, Ad 4 16:9, Ad 6 16:9, Ad 10 9:16, Ad 3 1:1. RA-01 is left out (lowest click-through
of the six, 0.7%). Logo `400941168572`, business name "Abs by AI".

**Images: all 20 finalized pictures** from `output/campaign-images-20261001/Finalized Images/` (both folders, on Dan's
instruction; 20 is the asset group limit): 8 landscape, 8 square, 4 portrait. Asset ids in
`scripts/ads/api/dgen-ads/pmax-images.result.json`. **Google's AI label is set on all 20**
(`synthetic_content_info.advertiser_attestation` = IS_SYNTHETIC, read back).

**What the account did not offer.**
- Call to action "Start now": Performance Max refuses it (`UNSUPPORTED_CALL_TO_ACTION`). Set to **Sign up**.
- Six ads as videos: the limit is five per asset group.
- Everything else in the spec was accepted by the API, including the age, gender and member-list exclusions.

**Traps.** Headline and description text assets must exist before the asset group is created, or Google answers
`NOT_ENOUGH_HEADLINE_ASSET`; the script makes them in their own request. v25 has no `url_expansion_opt_out`; it is
the asset automation type `FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION`. Dates are `start_date_time` / `end_date_time`.

**Watch.** All 60 assets were `REVIEW_IN_PROGRESS` at enable. $15 x 30 days is $450, but Google may spend up to twice
the daily budget on one day, so the month can pass $450 by a few dollars and that part goes to Dan's card.
- **Day 5 (2026-10-07):** spend by channel, new versus returning visitors, policy status of every asset. If it barely
  spends, report it with the list size; do not widen the targeting without Dan.
- **$150 spent (about 2026-10-12):** judge per `Docs/CAMPAIGN_IMAGES_RESEARCH.md` section 9. Three or more trials is a
  winner, zero is a loser, one or two runs to $300.

**2026-10-02, Dan rewrote the copy in the Ads editor (about 1:30 PM CT).** Now 12 headlines, 5 long headlines, 5
descriptions; the live lines are the constants in `scripts/ads/api/pmax-trial-campaign.js`. He cut the headlines that
only fit one ad (supplements, busy dad), added "The Real Truth About Abs", and replaced four long headlines and three
descriptions with lines that sell the click and fit any video or image. One typo in his description was fixed by API
("apps hows" to "app shows"). Before and after table and the lessons: skill `/ad-copy`.

**2026-10-02 12:59 PM CT: budget changed from $15 to $5/day in the Ads interface** (change history, web client). At $5/day to the 11-01 end date the campaign spends about $150 of the $450 credit; the credit expires 11-30.

**2026-10-02, long headlines and descriptions rewritten on all 12 ads of `24316364155`** (Dan: make them persuasive, in his voice, per his Performance Max edit). Headlines untouched. 36 lines: 5 kept, 13 slots filled with his exact Performance Max lines, 18 new in his shapes. Builder and the lines: `scripts/ads/api/dgen-trial-longcopy-20261002.js`; old copy in `scripts/ads/api/dgen-ads/trial-longcopy-20261002.before.json`. All 12 ads went back to review; recheck with `node scripts/ads/api/client.js policy 24316364155`. Remarketing `24305381214` still carries the old long lines.

## 2026-10-04: approved Ad 13 vertical and short added to the trial campaign

Both exact files Dan approved on 10-03 were uploaded Unlisted with synthetic media set true, the existing title plus `(Vertical)` or `(Vertical 59s)`, and the live 16:9 tags. Readback confirmed processing succeeded, embeddable true and not made for kids. Closing words in both final word transcripts: "Tap the button below to get started." No organic posting.

One 1080x1920 thumbnail reuses approved 13-R3B: photo-10, its original mask, repaired robot plate, Impact type and yellow accent, with the same words "HUMAN TRAINERS HATE THIS AI". Builder: `scripts/covers/trial-campaign-20261001/ad13-vertical/build.py`. No new image generation or paid image calls. Both served thumbnails were saved and visually checked. Final: `social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/Ad 13 | 9x16 | FINAL.jpg`, copied into `FINAL APPROVED`.

| Format | YouTube | Video asset | Trial ad | Status on 10-04 |
|---|---|---|---|---|
| Claude 9:16, 244.878 seconds | `f792V7H1Vkc` | `427647278214` | `826888334290` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 9:16 59s, 54.288 seconds | `VPyHyxEkHjo` | `427558235731` | `826888304284` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |

Both were added to existing Ad 13 group `204553316830`, campaign `24316364155`, using `scripts/ads/api/dgen-ad13-vertical.js`. Google validateOnly passed before apply. Headlines, long headlines, descriptions, logo, business name and CTA were cloned unchanged from live 16:9 ad `826635661894`. Exact copy and readback: `scripts/ads/api/dgen-ads/ad13-vertical.json` and `ad13-vertical.result.json`.

Final URLs:

- `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad13&utm_content=claude-9x16-vsl`
- `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad13&utm_content=claude-9x16-59s-vsl`

The live Ad 10 spelling is `claude-9x16`, rather than the handoff's illustrative `claude-vertical`, so that spelling was matched. Campaign budget `15911255930` remained $30/day. Protected before/after comparison confirmed campaign status, budgets, bids, Ad 13 group settings, audience criteria and live 16:9 ad unchanged. That ad remains ENABLED and APPROVED. Old Demand Gen and Performance Max were not modified.

The handoff's remarketing state was stale: `24305381214` and `24316408288` are now ENABLED, not PAUSED. Campaign A (`24305381214`) copies trial ads; campaign B (`24316408288`) copies organic subscriber ads from `24163535721`, not the trial campaign. No remarketing mutation was sent. Dan was asked whether to add these videos to live conversion remarketing. No campaign was enabled or paused.

AV-11 marked UPLOADED and pushed to the Edit Queue Drive status file. AS-10 remains open. Description files sit beside the masters. The four-second legacy chapter was merged into the personal-trainer chapter; the short has no chapters. Policy command ran after apply. Recheck both new trial ads on **2026-10-05** with `node scripts/ads/api/client.js policy 24316364155`. Full receipt: `Docs/AD13_VERTICAL_SETUP_RECEIPT_20261004.md`.

## 2026-10-04: four approved Ad 6 formats added to the trial campaign

Dan finalized all four on 10-04. All source SHA-256 hashes matched `approval_20261004.json` before upload. The exact files were uploaded unchanged to channel `UC236gjadarHAhEhOMYNGJ9g`, Unlisted, not made for kids, embeddable and successfully processed. Full videos keep the original chapters; the 57.758 s cuts have no chapters. Uploads used `--synthetic true`. YouTube omits that field from API readback; the selected AI-use setting is verified in Studio.

The finished files end: "Tap the button below to see how amazing you would look with six-pack abs." Classified AD. No organic posting.

Thumbnails: `Ad 6 | 9x16 | FINAL.jpg` and `Ad 6 | 1x1 | FINAL.jpg`, in `social media graphics/youtube/thumbnails/Ad 6 You're Not Too Old To Get Abs/trial-20261001/` and copied into `_trial-campaign-20261001/FINAL APPROVED/`. Same approved 6-R3B aged-head/original-body cutout (SHA-256 `6709d417252ef5a26223bbaf5f18a98e3a4c64daa18b7aa0f772c5b5d42d2166`), warm gym plate, Impact type, gold accent and "HOW MEN 40+ / GET ABS" copy. Existing plate recomposed with the other ads' rendering functions; no image generation or paid image call. Zero text/person overlap, full head and text kept, all four served thumbnails saved and viewed. Builder: `scripts/covers/trial-campaign-20261001/ad6-formats/build.py <main project path>`.

Campaign `24316364155`, existing group `204444440607`, "Ad 6 You're Not Too Old". Created with `scripts/ads/api/dgen-ad6-formats.js`, `validateOnly` passed before applying. Copy read from live twin `826595554443` and reused exactly, including headlines, long headlines, descriptions, logo, business name and CTA. Config, mutation and verified result in `scripts/ads/api/dgen-ads/ad6-formats*.json`.

| Format | YouTube id | Asset id | Ad id | utm_content | Initial status |
|---|---|---|---|---|---|
| Claude 9:16 | `Yd7iVlosIkQ` | `427555866313` | `826887690637` | `claude-vertical-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 9:16 59s | `C-ThTBOPn2E` | `427458948149` | `826887690655` | `claude-vertical-59s-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 | `3Rx5TmyUARU` | `427555872217` | `826887690931` | `claude-square-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 59s | `aCsSsYG2vKI` | `427555872259` | `826887690943` | `claude-square-59s-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |

All four final URLs are `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad6&utm_content=<table value>`. The explicit vertical UTM values from the handoff were used, matching RA-01's vertical convention; Ad 3/10 use `claude-9x16` instead.

The live trial budget was **$30/day**, budget `15911255930`, before and after. Campaign and Ad 6 group target CPA remain $40. Exact before/after checks prove campaign statuses/budgets/bids, group criteria/audience and all pre-existing trial ads unchanged. No operation targeted the live 16:9 `Je2yvk00SHE` / ad `826595554443`, old Demand Gen `24243839443` or Performance Max `24308574894`.

Policy run on 10-04: all four new ads ENABLED, REVIEW_IN_PROGRESS / UNKNOWN. Recheck date **2026-10-05** with `node scripts/ads/api/client.js policy 24316364155`. Existing 16:9 currently APPROVED_LIMITED / REVIEWED: its "Korean AI prodigy ... Video reveals full story." long headline is DISAPPROVED for CLICKBAIT. This pre-existing line was preserved as instructed; report to Dan before any rewrite.

Remarketing differs from the handoff: both `24305381214` (conversion, $10/day) and `24316408288` (subscriber engagement, $5/day) are already ENABLED. Their status and budget were preserved. Conversion-copy synchronization is pending Dan's answer because the handoff described PAUSED copies. Script `dgen-rmktg-campaigns.js a` only targets conversion campaign `24305381214`; campaign B draws organic engagement ads from another source and is not an Ad 6 trial copy. No ads were added there.

## 2026-10-04: four approved Ad 4 formats added to the trial campaign

All four source hashes matched `Muhammad Ad Videos/stop wasting money on supplements - ad 4/approval_20261004.json` before upload. Exact files uploaded unchanged to channel `UC236gjadarHAhEhOMYNGJ9g`, Unlisted, embeddable, not made for kids, custom thumbnails present and processing succeeded. Full videos keep the live 16:9 chapters; 57.190 second cuts have none. Titles append `(Vertical)`, `(Vertical 59s)`, `(Square)` or `(Square 59s)` to the live title. Live tags and descriptions reused, with long dashes changed to hyphens in new descriptions. Uploads used `--synthetic true`; AI use Yes verified in YouTube Studio for all four.

The finished transcripts end: "Tap the button below to get started." Classified AD. No organic posting. Muhammad's accepted audio remains untouched, including the recorded -0.90 dBTP exception.

Thumbnails reuse approved 4-R2A exactly: studio-gray-55 cutout, supplement-bottle plate, Impact type, red accent and "SUPPLEMENT CORPS HATE HIM" wording. Both shapes use the same rendering functions as the other trial thumbnails. Full head retained, zero text/person overlap, compared beside Ad 3 and Ad 6 at each shape. No image generation or paid image API call. Finals in `social media graphics/youtube/thumbnails/Ad 4 Stop Wasting Money On Supplements/trial-20261001/`, copied into `_trial-campaign-20261001/FINAL APPROVED/`. All four served thumbnails saved and visually checked. Builder and hash receipt: `scripts/covers/trial-campaign-20261001/ad4-formats/`.

Campaign `24316364155`, existing group `204553317030`, "Ad 4 Stop Wasting Money On Supplements". Four ENABLED ads created by `scripts/ads/api/dgen-ad4-formats.js`, only asset/ad create operations, Google validateOnly passed before apply. Headlines, long headlines, descriptions, logo, business name and CTA read from live 16:9 ad `826635661909` and cloned unchanged. Config, protected snapshots, mutation and verified result: `scripts/ads/api/dgen-ads/ad4-formats*.json`.

| Format | YouTube id | Video asset id | Ad id | utm_content | Initial policy status |
|---|---|---|---|---|---|
| Claude 9:16 | `Sr9gux0gB5I` | `427583175764` | `826899511366` | `claude-vertical-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 9:16 59s | `TPlpl0LETqw` | `427583175791` | `826899511387` | `claude-vertical-59s-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 | `kyrAfWkg92k` | `427583175851` | `826899464146` | `claude-square-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 59s | `eJ-dTPw40Hk` | `427583175869` | `826899511576` | `claude-square-59s-vsl` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |

All final URLs: `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad4&utm_content=<table value>`.

Budget `15911255930` remains $30/day. Exact before/after comparisons passed for campaign status/budgets/bids, group settings/target CPA/audience criteria and all existing trial ads. Live 16:9 `R08TPEtkjuQ` / ad `826635661909` unchanged; YouTube metadata and status also compared exactly. No other campaign, ad or budget mutation. Old Demand Gen `24243839443` and Performance Max `24308574894` left untouched.

Policy command ran after apply: all four new ads ENABLED, REVIEW_IN_PROGRESS / UNKNOWN. Live Ad 4 16:9 remains APPROVED / REVIEWED. Recheck date **2026-10-05**: `node scripts/ads/api/client.js policy 24316364155`. The date is recorded; no new automation was requested or created.

Remarketing `24305381214` and `24316408288` already ENABLED. No recorded answer to the earlier Ad 6/13 question in campaign docs or AGENTS.md, so no remarketing mutation. Dan's remaining decision: also add these four formats to live conversion remarketing `24305381214`? Campaign B is organic subscriber engagement, not a trial-ad copy.

AV-03 and AS-02 marked UPLOADED; both commands confirmed the Drive status file uploaded. Setup handoff removed from the coordination board and Handoffs index. No dashboard batch row checked, because other named ads remain outside this task.
