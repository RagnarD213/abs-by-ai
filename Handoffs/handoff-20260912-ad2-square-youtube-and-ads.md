# Handoff — Ad 2 SQUARE (1:1): upload to YouTube, then add it to the Google Ads campaign

**Written 2026-09-12, the session that built the square. Dan approved the video the same day
("this video is finalized") and asked for this doc.** The creative is finished and filed; nothing
about the picture or the audio is open. This handoff is the two outward-facing steps that follow.

Read **`/ad-setup`** first — it owns this workflow end to end. Then
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` → "After the build", which is the short
version of the same thing for squares.

## What exists

| | |
|---|---|
| the file | `Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/stop wasting money on nutritionists \| claude \| 1x1 \| ad 2.mp4` |
| what it is | 1080×1080, 29.97, **8,275 frames = Muhammad's V2 to the frame**, 4:36.1. A 1:1 re-layout of the approved 9:16 vertical |
| audio | the **approved vertical's own AAC stream, md5-identical** (`823f4e56e2b4822a0c48d69399c3ff38`) — Muhammad's V2 mix at the one constant +5.2 dB Dan approved on 09-08, −14.7 LUFS / −1.1 dBTP |
| gates | `qc.py` **19/20**, watch pass 88/88, two independent audits (the second returned SHIPS). The one red row is check 20 and BOTH audits concluded it is a gate calibration defect on olive-graded material, not a caption defect — see `notes-square.md` |
| review copies | 540p and 480p in the same folder, plus the audio A/B and `recipe-square/` |
| notes | `notes-square.md` in that folder — read the "APPROVED AND FINALIZED" block at the top before touching anything |

⚠ **Do NOT re-render this video.** Dan changed the label-placement rule on seeing it (labels must not
cover his face or his abs) and was explicit that the change applies **going forward only**, to save
credits. The rule is already in every video skill and in `AGENTS.md`. Ad 2's square ships as it is.

## Step 1 — YouTube, unlisted

Per `/ad-setup` and `/youtube-packaging`.

* Upload with `scripts/youtube/upload.js` + `YOUTUBE_REFRESH_TOKEN` (memory `youtube-upload-capability`;
  the old 10 MB `file_upload` cap does not apply). Channel: **Abs by AI**. Visibility **unlisted**.
* Title/description/tags: copy Ad 2's existing pattern — the 16:9 is `Dtk5knWM7c8` and the vertical is
  `7XgHxn59Tsg` (`Docs/AD_VIDEO_IDS.md` rows 11–12). Keep the UTM link, the chapters and the
  **AI-content disclosure = yes**.
* Thumbnail: a **1:1** crop in the Ad 2 style. The two existing Ad 2 thumbnails are
  `ad2-vertical-7XgHxn59Tsg_C-jeans-black-9x16-FINAL.jpg` and
  `ad2-muhammad-16x9-Dtk5knWM7c8_C-jeans-black-FINAL.jpg` — make the square from the same source so
  all three read as one ad. Thumbnails DO upload through `file_upload` (~150 KB).
  ⚠ Thumbnail copy is a compliance surface (memory `thumbnail-no-claims`): no claims, no before/after pair.
* Add a row to `Docs/AD_VIDEO_IDS.md` with the new id, aspect, duration and thumbnail filename.

## Step 2 — Google Ads, the SAME ad, one more `videos` entry

**This is the whole point of the square** (the rep's ask, 2026-09-11): a Demand Gen video ad serves
across YouTube in-feed, Shorts, Discover and Gmail, and Google fills each placement from the aspect
ratios the ad carries. Ad 2 already carries 16:9 and 9:16; the square fills in-feed / Discover / Gmail
at full size instead of a letterboxed 16:9.

* **`/ad-setup` step 6** — add the new video as ONE MORE `videos` entry on **Ad 2's existing ad groups**,
  not a new ad and not a new ad group. Campaign **`24243839443`** (`Docs/DGEN_CONVERSION_CAMPAIGN.md`):

  | ad group | id | the ad's current videos |
  |---|---|---|
  | `Ad 2 Stop Wasting Money On Nutritionists \| /start` | `200136997156` | 16:9 `Dtk5knWM7c8` → `419623700809` · vertical `7XgHxn59Tsg` → `419700324321` |
  | `Ad 2 Stop Wasting Money On Nutritionists \| home` | `199420011265` | same pair |

* **Muhammad's own 16:9 stays the primary video.** Copy, headlines, budget, bidding and the audience
  (`358261320`) are all unchanged — this adds an asset, it does not re-create the ad.
* Use the **API client** `scripts/ads/api/client.js` (memory `google-ads-api-client`: no developer
  token; `login-customer-id` is the ACCOUNT, not the MCC). Where the API cannot express it, the ytads
  manual mutation queue or the Ads UI — the traps are in `Docs/YTADS.md` and memory
  `google-ads-ui-automation`.
* Record the new video-asset ids in `Docs/DGEN_CONVERSION_CAMPAIGN.md` beside the existing pair.
* **The next day**, run `node scripts/ads/api/client.js policy 24243839443` and check the new asset
  cleared review. ⚠ Ad 5's *Why My Diets Kept Failing* headline was DISAPPROVED for clickbait on this
  same campaign — if anything here is limited, follow the retry rule in memory
  `ad-retry-rule-and-no-trick` (tamer copy → tamer thumbnail → remove; never "trick" the reviewer).

## When it is done

1. Add the YouTube row to `Docs/AD_VIDEO_IDS.md` and the asset ids to `Docs/DGEN_CONVERSION_CAMPAIGN.md`.
2. Delete the Ad 2 square's entry from `AI_COORDINATION.md`, this doc from `Handoffs/README.md`, and
   this file. **No new dashboard row** (Dan's rule, 2026-09-08) — but the existing Key row
   *"Add the new finished ads…"* can be checked off only when its own scope is complete, which today
   still includes Zeeshan's Ad 1 verticals, so leave it.
3. Tell Dan the video id and confirm the two ad groups now carry three aspect ratios each.

## Starter prompt (Fable 5.1, medium)

> Execute `Handoffs/handoff-20260912-ad2-square-youtube-and-ads.md` after reading `/ad-setup`: upload
> the finished Ad 2 SQUARE (`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/stop
> wasting money on nutritionists | claude | 1x1 | ad 2.mp4`) to the Abs by AI channel as unlisted with
> a 1:1 thumbnail in the Ad 2 style and the AI-content disclosure, then add it as one more `videos`
> entry on Ad 2's two existing Demand Gen ad groups (200136997156 and 199420011265 in campaign
> 24243839443) — same ad, not a new one, Muhammad's 16:9 stays primary. Record the ids in
> `Docs/AD_VIDEO_IDS.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md`, then check policy the next day. Do
> NOT re-render the video. Model: Fable 5.1, effort medium.
