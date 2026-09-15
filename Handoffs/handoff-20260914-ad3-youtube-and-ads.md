# Handoff — Ad 3 "Stop Paying Human Trainers": put the approved 16:9, 9:16 and 9:16 ≤0:59 on YouTube + Google Ads

**Written 2026-09-14. Not yet executed.** Dan approved all three files on 2026-09-14: *"Okay, all these are looking good,
and they are approved."* This is `/ad-setup` for a new version of an ad that is already in the campaign — read
`.claude/skills/ad-setup/SKILL.md` in full before starting; this doc only adds what is specific to Ad 3.

## Goal

1. Upload three videos to YouTube **unlisted** on the Abs by AI channel, each with a description, thumbnail and the
   AI-content disclosure.
2. Add all three to Ad 3's two existing Demand Gen ad groups as new `videos` entries.
3. **Pause** (never remove) the two live ads that still use the old 16:9 with the breath-smoke shot.
4. Record every id, commit, push, and check policy the next day.

## The three approved files (all in `Muhammad Ad Videos/stop paying human trainers - ad 3/`)

| # | file | what it is | length | sha256 (first 16) | bytes |
|---|---|---|---|---|---|
| A | `stop paying human trainers \| muhammad (smoke shot replaced) \| 16x9 \| ad 3.mp4` | Muhammad's v6 HD with the AI bathroom shot (1:13.5–1:18) replaced; his audio bit for bit | 4:25.2 | `85a7da67edc2fc47` | 542,401,194 |
| B | `stop paying human trainers \| claude \| 9x16 \| ad 3.mp4` | our vertical, render 12 | 4:25.2 | `6ef0538cf055183a` | 613,646,735 |
| C | `stop paying human trainers \| claude \| 9x16 59s \| ad 3.mp4` | the vertical's ≤0:59 cutdown | 0:57.9 | `1a295123fca84479` | 115,145,805 |

Verify each with `shasum -a 256` before uploading; if a hash differs, stop and find out why (another session may have
re-rendered). Notes for context: `notes-vertical.md`, `notes-16x9-smoke-shot.md` in the same folder.

⚠ **File C's audio stamp reads FAIL on purpose** (true peak −0.90 dBTP, an AAC overshoot of Muhammad's −1.0 mix). Dan was
told and approved it — see `… 9x16 59s | ad 3.mp4.DAN_ACCEPTED.md`. Upload it as is. Do not re-encode, limit or
normalise any of these files, and do not "fix" the stamp.

⚠ File A still carries Muhammad's own export error at 2:14.1–2:23.1 (a bullet missing "back in my 20s, as a 38 year old
dad running a successful ad agency."). Known and accepted for now; his round-6 re-export (requested in
`revision docs/ad3-revisions-muhammad-round6-9-14-26.md`) will replace it later. Files B and C carry the full text.

## What is live right now (read back before changing anything)

- YouTube `QWW1oumpNg4` — Muhammad's original v6 HD **with the smoke shot**, unlisted, thumbnail
  `ad3-muhammad-16x9_O1-dark-studio-studio-gray-87-FINAL.jpg`.
- Campaign `24243839443` (Demand Gen conversion, $20/day, ENABLED), audience *Ad 3 … AI fitness + competitor apps + get
  abs belly fat*, config `scripts/ads/api/dgen-ads/ad3.json`, read-back `ad3.result.json`:
  - ad group **199782847163** `Ad 3 Stop Paying Human Trainers | /start` → ad **824427749693** (`| Muhammad 16:9 | /start`)
  - ad group **199360345839** `Ad 3 Stop Paying Human Trainers | home` → ad **824344861381** (`| Muhammad 16:9 | home`)
- Run `node scripts/ads/api/client.js policy 24243839443` first and note Ad 3's current review state.

## Steps

### 1. YouTube (unlisted, three uploads)

Titles (unlisted, so recognisability matters, not SEO), following the Ad 1 square pattern:
- A: `Stop Paying Human Trainers! Use AI Instead`
- B: `Stop Paying Human Trainers! Use AI Instead (Vertical)`
- C: `Stop Paying Human Trainers! Use AI Instead (Vertical 59s)`

Descriptions:
- A and B: copy `youtube-description.md` from the Ad 3 folder unchanged. The chapters still apply, because both files
  keep Muhammad's timeline frame for frame.
- C: write `youtube-description-vertical-59s.md` like `Muhammad Ad Videos/this picture got me abs - ad 1/youtube-description-square-59s.md`:
  one or two sentences in Dan's voice, the same 👉 line with `utm_campaign=dgen-conv-ad3`, the same AI disclosure
  paragraph, **no chapters**. Never the word "trick", no result promise in the first two lines.

Thumbnails (`/ad-setup` step 4):
- A: reuse the existing `social media graphics/youtube/thumbnails/Ad 3 Stop Paying Human Trainers/ad3-muhammad-16x9_O1-dark-studio-studio-gray-87-FINAL.jpg`.
- B and C: a vertical video gets a **9:16 thumbnail**. Build ONE 1080×1920 version of the same design: studio-gray-87,
  O1 dark studio, copy `STOP PAYING / PERSONAL / TRAINERS`. Use the Ad 2 vertical's `…-9x16-FINAL.jpg` files as the
  layout reference and the `_ad-setup-2026-09-11/build.py` job pattern. It must print ALL PASS and you must look at it
  before setting it. Set the same file on B and C.

Upload each file with `scripts/youtube/upload.js`, using the flags in `/ad-setup` step 5 (`--privacy unlisted
--category 26 --made-for-kids false --synthetic true`), and log to `youtube-upload-<16x9-clean|vertical|vertical-59s>.log`
in the Ad 3 folder. Check each log's first line reads `channel: Abs by AI (UC236gjadarHAhEhOMYNGJ9g)`. **Never re-run a
successful upload; it creates a second video.** Set thumbnails with `set-thumbnail.js` and read them back. Poll
`videos?part=status,processingDetails` until each reads `succeeded`, `embeddable: true`, `unlisted`.

### 2. Google Ads — three new `videos` entries on the existing groups

1. Read the live copy of ad 824427749693 back from the account and confirm it is byte-identical to `ad3.json`'s `copy`.
   The new ads must carry the same copy. If they differ, the account wins; update the config.
2. Add three entries to `scripts/ads/api/dgen-ads/ad3.json` `videos`, **keeping the existing Muhammad 16:9 entry** so the
   builder still recognises the old ads:
   ```json
   { "youtubeId": "<A id>", "version": "Muhammad 16:9 clean", "utm": "muhammad-16x9-clean" },
   { "youtubeId": "<B id>", "version": "Claude 9:16",         "utm": "claude-9x16" },
   { "youtubeId": "<C id>", "version": "Claude 9:16 59s",     "utm": "claude-9x16-59s" }
   ```
   `version` must differ from `Muhammad 16:9`. The builder names each ad `<label> | <version> | <landing>` and **reuses
   anything with an existing name**, so a repeated version string would silently skip the new ad.
3. Dry run: `node scripts/ads/api/dgen-add-ad.js scripts/ads/api/dgen-ads/ad3.json`. The plan must REUSE both ad
   groups and the audience, and create exactly **3 video assets + 6 ads**. Anything else (a new ad group, a new
   audience) means a name mismatch; stop and fix the config.
4. `--apply`, then keep the read-back in `ad3.result.json` (rename the old one to `ad3.result.20260911.json` first so the
   original record survives).
5. **Pause the two old smoke-shot ads** (reversible; the old video stays on YouTube, unlisted and untouched):
   ```bash
   node scripts/ads/ytads/manual.js pause customers/3427170837/adGroupAds/199782847163~824427749693 --note "Ad 3: replaced by the smoke-shot-fixed 16:9 (Dan approved 2026-09-14)"
   node scripts/ads/ytads/manual.js pause customers/3427170837/adGroupAds/199360345839~824344861381 --note "Ad 3: replaced by the smoke-shot-fixed 16:9 (Dan approved 2026-09-14)"
   ```
   Read back that both read PAUSED and the six new ads read ENABLED. **Do not delete** `QWW1oumpNg4` or remove the old
   ads; deleting needs Dan. Never enable a campaign. Budget stays $20/day; say that it is now shared by more ads.
6. Next day: `node scripts/ads/api/client.js policy 24243839443`. A DISAPPROVED line → rewrite only that line
   (`manual.js headlines`). A video-level limited/disapproved verdict → the retry rule (memory
   `ad-retry-rule-and-no-trick`). Note in the report: the vertical and the 16:9 show the same app screens Muhammad's
   16:9 already had approved.

### 3. Record (same session)

- `Docs/AD_VIDEO_IDS.md`: three rows (A, B, C: aspect, length, link, approved 09-14, thumbnail). Mark `QWW1oumpNg4` as
  *superseded 09-14, ads paused, video kept*.
- `Docs/DGEN_CONVERSION_CAMPAIGN.md`: a dated section with the asset ids, the six new ad ids per ad group, and the two
  paused ids.
- `.claude/skills/editor-deliveries/state.json`: a `filed` row for file A if the schema allows it.
- `AI_COORDINATION.md` (re-read from disk first, edit only the Ad 3 entry): uploaded + ads live + old ads paused; what
  is left (Muhammad's round-6 re-export, which will replace A again).
- Commit scripts/configs/docs (videos and thumbnails are git-ignored), push to `main`.
- Dashboard (`/dashboard-tasks`): check off the Ad 3 vertical row, and check off *"Add the new finished ads to the
  Google Ads campaigns…"* only if every ad it names is now in. Otherwise say what remains.
- Delete this handoff from `Handoffs/README.md` (open list) and the HANDOFFS section of `AI_COORDINATION.md`.

## Out of scope

Organic posting (public YouTube, Blotato); the square (separate handoff
`Handoffs/handoff-20260914-ad3-square-codex.md`); replacing the old YouTube video in place (YouTube cannot swap a
video's file).

## Starter prompt

> Execute `Handoffs/handoff-20260914-ad3-youtube-and-ads.md` end to end. Read it, then `.claude/skills/ad-setup/SKILL.md`,
> then `AI_COORDINATION.md` from disk. Verify the three files' sha256, upload all three unlisted with descriptions and
> thumbnails (build the one 9:16 thumbnail), add them to Ad 3's two Demand Gen ad groups (the dry run must reuse the
> groups and create exactly 3 assets + 6 ads), pause the two old smoke-shot ads, record every id, commit and push, and
> report in plain language with the video links.

**Model / effort:** Claude Sonnet 5, medium. It is a scripted, well-trodden path. Use Opus 5 medium if the 9:16
thumbnail build needs design judgment.
