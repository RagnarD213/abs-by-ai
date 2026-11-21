# Ad 8 approved verticals: thumbnail, YouTube upload and Google Ads setup

Written: 2026-10-01

Recommended fresh task: Claude Opus 5.5, medium effort (the thumbnail is design work inside a locked standard; the
upload and ads steps are a checklist).

## Goal

Make one 9:16 thumbnail, upload the two approved Ad 8 vertical masters to YouTube as Unlisted videos, and add both
as new variants in the existing Ad 8 Demand Gen ad groups. Keep the existing 16:9 ads and every live campaign
setting as they are.

This is an advertising setup job. These videos never go out on an organic channel.

## Read first

1. `AGENTS.md`
2. `.claude/skills/_shared/VIDEO-RULES.md`
3. `AI_COORDINATION.md`
4. This handoff
5. `.claude/skills/ad-setup/SKILL.md` (the operating method; `/ad-setup`)
6. Memory: `thumbnail-design-system`, `thumbnail-no-claims`, `ad-suspension-prevention`, `google-ads-api-client`

Read live state before writing anything. Check existing YouTube uploads first so nothing is uploaded twice.

## Dan's approval

2026-10-01: "these ads are approved and good to publish." It covers both exact files below. Do not re-edit,
transcode, shorten or normalize either master.

Dan also set a rule in the same message: this is the LAST delivery with the old olive graphics. It applies to
future edits, not to this upload. Do not rebuild these two files.

## Exact approved assets

Folder: `Muhammad Ad Videos/ai showed me two futures - ad 8/`

| Version | File | SHA256 | Bytes | Facts |
|---|---|---|---:|---|
| Full 9:16 | `ai showed me two futures \| claude \| 9x16 \| ad 8.mp4` | `320d14a3f45313a105f1ff1ad61024746e0ddd24f8e89460c82632f351795b5d` | 221214586 | 1080x1920, 30000/1001 fps, 210.877 s |
| 9:16 cutdown | `ai showed me two futures \| claude \| 9x16 59s \| ad 8.mp4` | `e0b8cee104e483bb28d140f8a7db328576ab8fb7927c1112f5f4c8d4ecba400c` | 51194943 | 1080x1920, 30000/1001 fps, 56.023 s |

Verify both hashes before uploading. The `REVIEW 540p` copies are not upload sources.

Evidence that both passed: `notes-vertical.md`, the `.deliver_gate.json` and `.audio_gate.json` stamps beside each
file (delivery gate PASS, 0 open defects; Muhammad's audio untouched), and `recipe-vertical/` (judges' findings for
the full and the cutdown).

## Existing live Ad 8 state (last recorded; read it back live first)

- Existing YouTube 16:9 video: `HMZdiJMAI3Y` (Unlisted), Google Ads video asset `422033285275`
- Campaign: `24243839443` (Demand Gen conversions, shared budget $40 per day)
- Audience: `359424266`
- `/start` ad group `201149830478`, existing ad `824925649893`
- Home ad group `203342192834`, existing ad `824966555242`
- Config: `scripts/ads/api/dgen-ads/ad8.json` (headlines, long headlines and descriptions already approved there)
- Record: `Docs/DGEN_CONVERSION_CAMPAIGN.md` (the Ad 8 row)

Do not change the budget, bids, audience, existing ads, existing assets, landing pages or campaign structure. If
live state differs from the record, keep the live state and write down the difference.

## Step 1: the thumbnail (this task makes it; no Codex handoff for this one)

Dan, 2026-10-01: "We'll have Claude make the thumbnail in the same task as setup."

- One 9:16 thumbnail (1080x1920) used on both uploads. Follow memory `thumbnail-design-system` (black and white
  Manrope, the red bar, abs visible, no blur) and `/youtube-packaging` for the build steps.
- Picture: a real, finished photo of Dan from `photos/finalized social media photos/` (a shoot photo, never a video
  frame, never soft abs; memory `cover-photo-selection`). Pool photos get the waist crop (memory `speedo-crop-rule`).
- Words: no claim. The thumbnail is an ad surface (memory `thumbnail-no-claims`, `ad-copy-no-unbelievable-claims`).
  Stay inside the idea the ad itself states, for example "AI SHOWED ME TWO FUTURES" or "TWO FUTURES". Never "trick".
- Build 3 options, pick the strongest yourself, and show Dan all 3 in the final message so he can swap it. Do not
  wait for his pick to upload: a thumbnail is replaceable in Studio.
- Save into `social media graphics/youtube/thumbnails/AI Showed Me Two Futures - vertical/`.

## Step 2: YouTube

Upload both masters with `scripts/youtube/upload.js` as UNLISTED. Never Public, never a scheduled publish.

- Titles: `AI Showed Me My Two Futures (Vertical)` and `AI Showed Me My Two Futures (Vertical 59s)`
- Description: start from `youtube-description.md` in the ad folder (the 16:9's). Its chapters fit the full vertical
  (same running time). The 59s gets the same description with no chapters.
- Set the AI-content disclosure (altered or synthetic content: yes), the tags from the 16:9, and the thumbnail.
- Confirm on each video: Unlisted, not made for kids, thumbnail applied, processing finished in HD.
- Append both ids to `youtube-upload.log` in the ad folder.

## Step 3: Google Ads (Demand Gen)

Follow `/ad-setup` and the way Ad 10's verticals were added (`Handoffs/handoff-20260925-ad10-verticals-youtube-google-ads.md`,
`scripts/ads/api/dgen-ads/ad10.json` and its result file are the worked example).

- Add both new YouTube videos to `scripts/ads/api/dgen-ads/ad8.json` under `videos` with their own `utm` values
  (`claude-9x16` and `claude-9x16-59s`), then create one new video ad per video in EACH of the two existing Ad 8 ad
  groups (four new ads), reusing the approved copy in that file. New ads are created ENABLED; nothing existing is
  paused or edited.
- Final URLs and UTMs follow the existing Ad 8 ads (one group lands on `/start`, the other on the home page).
- Run the policy read afterwards (`node scripts/ads/api/client.js policy 24243839443`) and record each new ad's
  status. A "limited" or "disapproved" result follows memory `ad-retry-rule-and-no-trick`.

## Step 4: record and close

- Update the Ad 8 row in `Docs/DGEN_CONVERSION_CAMPAIGN.md` with the two video ids, asset ids and four ad ids.
- Edit Queue: `python3 scripts/edit-queue/queue.py set AV-09 uploaded --by Claude --note "<ids>"`, then `push`, write
  the exported row to the queue artifact (memory `edit-queue-artifact-is-working-list`), then `mark-synced AV-09`.
- AS-08 (the square version) is unblocked by this approval; leave it for its own task.
- Remove this handoff's line from `AI_COORDINATION.md` and its row from `Handoffs/README.md`. Commit and push.
- Final message to Dan: the two YouTube links, the four ad ids with policy status, the three thumbnail options with
  the one used, and a numbered action list.

## Do not

- Do not publish either file to Facebook, Instagram, TikTok, Blotato or Public YouTube.
- Do not touch Ad 6 (AV-05) or any other ad's assets.
- Do not ask the editors for anything.

## Starter prompt

> Read `Handoffs/handoff-20261001-ad8-verticals-upload-and-ad-setup.md` in full and execute it with `/ad-setup`. Make
> the 9:16 thumbnail first (3 options, use the strongest), upload both approved Ad 8 verticals to YouTube as
> Unlisted, add them to the existing Ad 8 Demand Gen ad groups without changing anything that is live, run the
> policy check, record every id, and update the Edit Queue. Do not re-edit the videos.

Model and effort: Claude Opus 5.5, medium.
