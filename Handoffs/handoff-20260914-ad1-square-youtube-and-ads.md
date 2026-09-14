# Handoff — Ad 1 SQUARE (1:1) + its 0:59 cutdown: upload to YouTube, then add both to Google Ads

**Written 2026-09-14 by the session that built and revised the square. Dan approved both files the same day:**
*"both of these are looking excellent. You nailed it with both the full square version and the cutdown."*
The creative is finished and filed. **Do NOT re-render or re-mux either file.** This handoff covers the two
outward-facing steps that follow.

Read **`/ad-setup`** first; it owns this workflow end to end. The exact precedent is the **Ad 2 square**
(commit `40f1ae9`, 2026-09-12: `git show 40f1ae9` for the doc and the diff). That run went through without a hitch;
copy its shape.

## What exists

| | full length | 0:59 cutdown |
|---|---|---|
| file (in `Muhammad Ad Videos/this picture got me abs - ad 1/`) | `this picture got me abs \| claude \| 1x1 \| ad 1.mp4` | `this picture got me abs \| claude \| 1x1 59s \| ad 1.mp4` |
| picture | 1080×1080, 29.97, **6,976 frames = Muhammad's cut**, 3:52.8 | 1,493 frames, **0:49.8** |
| audio | the approved 9:16 vertical's AAC stream, md5 `16799987c1c532df6847494f5a71000e` | the same mix cut at the seams, no filter |
| gates | `_shared/deliver/gate.py` 1.2.0 **PASS 35/35**, stamp beside the file (sha256 matches) | same, PASS 35/35 |
| corpus | `ad1-square-r1-approved` | `ad1-square-59s-r1-approved` |
| notes | `notes-square.md` → "Round 1" | same |

Also in the folder: 540p/480p review copies and audio A/B files (never upload those), and `recipe-square/`.

## Step 1 — YouTube, unlisted, BOTH files

Per `/ad-setup` steps 3–5 and `/youtube-packaging`.

* Upload with `scripts/youtube/upload.js` + `YOUTUBE_REFRESH_TOKEN` (memory `youtube-upload-capability`, including its
  brand-account trap). Channel **Abs by AI**, visibility **unlisted**, **AI-content disclosure = yes**.
* Title/description/tags: follow Ad 1's existing uploads (`Docs/AD_VIDEO_IDS.md`: Muhammad 16:9 `lf46ytHacss`, vertical
  `Iz0u8KHRbyE`) and Ad 2's square (`youtube-description-square.md` in the Ad 2 folder). Write
  `youtube-description-square.md` and `youtube-description-square-59s.md` in the Ad 1 folder. Chapters go on the full
  length only; a 50 s video gets none. Keep the UTM link.
* ⚠ **Title copy is a compliance surface.** Dan's rule (2026-09-10, memory `ad-copy-no-unbelievable-claims`): *"This
  Picture Got Me Abs"* is too much for ad copy; *"How I Got Abs At 40"* / *"How AI Got Me Abs"* are the shapes to use.
  The file names keep the script title; the YouTube title does not have to.
* Thumbnail: **one 1:1 thumbnail, used on both uploads**, built from the same source as Ad 1's two existing ones
  (`social media graphics/youtube/thumbnails/Ad 1 This Picture Got Me Abs/ad1-muhammad-16x9-lf46ytHacss_O1-dark-studio-FINAL.jpg`
  and `…ad1-vertical-Iz0u8KHRbyE_O1-dark-studio-9x16-FINAL.jpg`), so all versions read as one ad. Save as
  `ad1-square-<id>_O1-dark-studio-1x1-FINAL.jpg`. Thumbnails upload through `file_upload` (~150 KB). ⚠ Memory
  `thumbnail-no-claims` (no claims, no before/after pair) and the frowning-photo rule in `AGENTS.md`. If a real photo of
  Dan's physique is on it, it carries "Real picture of me — not AI-generated", placed off his face and abs.
* Read back `videos?part=status,processingDetails` until `processingStatus: succeeded` and `embeddable: true` on both.
* Add two rows to `Docs/AD_VIDEO_IDS.md` (id, aspect 1:1, duration, thumbnail file).

## Step 2 — Google Ads: the SAME Ad 1, two more `videos` entries

Campaign **`24243839443`** (`Docs/DGEN_CONVERSION_CAMPAIGN.md`). Add both squares to **Ad 1's two existing ad
groups**. Do not create a new ad group or a new audience.

| ad group | id | videos it carries today |
|---|---|---|
| `Ad 1 This Picture Got Me Abs \| /start` | `199420011065` | Muhammad 16:9 `lf46ytHacss` → `419514921434` · Zeeshan 16:9 `1oEcwdp21Fg` → `419514919721` (its ads PAUSED 09-11, retry chain) · vertical `Iz0u8KHRbyE` → `419514921437` |
| `Ad 1 This Picture Got Me Abs \| home` | `202965542111` | same |

Audience `358261317` (segments `1013657222` / `1011514666` / `1011514645`).

* Tool: `node scripts/ads/api/dgen-add-ad.js <config>` (dry run), then `--apply`. It creates **one ad per video per ad
  group** and reuses anything that already exists **by name**. **There is no `ad1.json` yet** because Ad 1 was built by the
  one-off Ads Script, so write `scripts/ads/api/dgen-ads/ad1-square.json` with:
  * `adNumber: 1`, `label: "Ad 1 This Picture Got Me Abs"`;
  * `videos`: `{youtubeId: <square>, version: "Claude square", utm: "claude-square"}` and
    `{youtubeId: <square 59s>, version: "Claude square 59s", utm: "claude-square-59s"}`;
  * `audience`: label and segments of the EXISTING audience (read its name off the account);
  * `copy`: **byte-identical to Ad 1's live ads.** Read them back through `client.js`, don't retype them. Dan's
    headlines are *How I Got Abs At 40 · See Yourself With Abs - Use AI · Abs by AI ® · Abs By AI - Here's How It Works ·
    How I Got Abs With AI Workouts*; the long headlines and descriptions are the live ones.
* ⚠⚠ **Check the dry run before `--apply`.** It must say it REUSES ad groups `199420011065` and `202965542111` and
  audience `358261317`, and creates only 2 video assets + 4 ads. If it plans to CREATE any ad group or audience, the
  names do not match what the Ads Script built. Stop and fix the config's `label` / audience label to the live names.
  Never delete a duplicate you made by mistake without telling Dan.
* If a Dan headline trips `lint.js`, it belongs in `DAN_APPROVED` in `dgen-add-ad.js` (his "How I Got Abs At 40" shape
  already does). Never rewrite his copy to pass the lint.
* Budget ($20/day), bidding (target CPA $30 per group), and the other ads stay exactly as they are. Never enable or pause
  the campaign.
* Read back: 4 new ads ENABLED (REVIEW_IN_PROGRESS is normal at creation). Record the asset + ad ids in a new
  `## 2026-09-1x — Ad 1 square (1:1) + 59s added` section of `Docs/DGEN_CONVERSION_CAMPAIGN.md`, same shape as the Ad 2
  square section, and update Ad 1's row in the videos table.
* **The next day:** `node scripts/ads/api/client.js policy 24243839443`. ⚠ Ad 1 has a history here: CLICKBAIT limited on
  its first copy (09-10), and Zeeshan's 16:9 ads went APPROVED_LIMITED for exaggerated claims. If a square ad comes back
  limited, follow memory `ad-retry-rule-and-no-trick` (tamer copy → tamer thumbnail → remove; never "trick" the reviewer).

## When it is done

1. Commit the config, its `.result.json`, both docs and the description files (videos and thumbnails are git-ignored);
   push to `main`.
2. Board: delete the Ad 1 square entry from `AI_COORDINATION.md` (ACTIVE TASK) and its struck line in HANDOFFS, this
   doc's row in `Handoffs/README.md`, and this file. In `Handoffs/handoff-20260913-ad-variants-master-queue.md` mark
   the Ad 1 1:1 and 1:1 59s cells **live** with the ids.
3. Dashboard (`/dashboard-tasks`): check off the Ad 1 square row if one exists. **No new row** (Dan's 09-08 rule).
4. Tell Dan the two video ids, and confirm Ad 1's two ad groups now carry 16:9 + 9:16 + 1:1 + 1:1 59s.

## Starter prompt (Sonnet 5, effort medium)

> Execute `Handoffs/handoff-20260914-ad1-square-youtube-and-ads.md` after reading `/ad-setup`: upload Dan's APPROVED
> Ad 1 square and its 0:59 cutdown (`Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs | claude |
> 1x1 | ad 1.mp4` and `… | 1x1 59s | ad 1.mp4`) to the Abs by AI channel as unlisted, with one 1:1 thumbnail in Ad 1's O1
> dark-studio style and the AI-content disclosure. Then add both as `videos` entries on Ad 1's two existing Demand Gen ad
> groups (199420011065 /start, 202965542111 home, campaign 24243839443) with a new `dgen-ads/ad1-square.json` whose copy
> is read back from the live Ad 1 ads. The dry run must REUSE both ad groups and audience 358261317 before you `--apply`.
> Record the ids in `Docs/AD_VIDEO_IDS.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md`, commit and push, and check policy the
> next day. Do NOT re-render either video. Model: Sonnet 5, effort medium.
