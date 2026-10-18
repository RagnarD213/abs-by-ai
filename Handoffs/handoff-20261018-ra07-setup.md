# RA-07 "Fire Your Trainer!": upload and Google Ads setup (9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `Fire Your Trainer AD Setup`.
Written 2026-10-18 by Claude Opus 5.5, right after Dan approved round 6. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-18, on the round 6 page: *"All right, this is approved. Go ahead and do the setup in the next round."*
Record: `Claude Ad Videos/fire your trainer - RA-07/APPROVAL.md` and `/Volumes/Extreme/_edit_work/ra07/round6-plan/decisions.json` ("final").

| | 9:16 |
|---|---|
| master | `Claude Ad Videos/fire your trainer - RA-07/fire your trainer \| claude \| 9x16 \| RA-07.mp4` |
| sha256 | `ca75555c9736d7cea4bf1336f21e672e40496039ee34ed698a263ec046edcfae` |
| format | 1080x1920, 52.69 s, 1,579 frames, H.264 BT.709 + AAC |
| gates | delivery gate 37 of 39 (known rows: `audio:stamp` from the approved bass lift's tone row, and one caption timing on "20" at 21.3 s inside the approved first 30 s), watch pass 0 defects, independent review SHIP |

**Only the 9:16 exists.** Round 6 built no 16:9 and Dan asked for setup on approving the 9:16: set up the 9:16 alone. Do not build a 16:9 in this task.
Assert the hash before anything. The delivery checks are done on this exact file (stamps beside it): do not re-run or re-render.
Closing line: "Get started building your six-pack abs with AI now. Tap the button below to take the first step." (button CTA: an AD).
Words: `/Volumes/Extreme/_edit_work/ra07/words_aligned.json`; captions `/Volumes/Extreme/_edit_work/ra07/cap_9x16/captions.srt`.

AI content (disclosure flag and description), film times: the fired trainer and robot spotter 0.0-3.4 s (library A0147); the app's AI
generation of Dan and the AI goal picture on a lock screen 14.9-18.9 s (labelled); the AI injury run 36.5-47.0 s (broken-arm man A0179,
gym closed, the same man curling at home, the out-of-order leg press and phone, hack squat, "back next week"). **`--synthetic true`.** Keep
the description's AI sentence from `/ad-setup` step 3.

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
Nearest precedents: `Handoffs/handoff-20261016-ra15-setup.md` and `Docs/RA16_SETUP_RECEIPT_20261017.md` (RA-16 "AI Took My Job" already uses
the thumbnail line "Fire your trainer.": give RA-07 its own designs, not a copy). Trial group builder `scripts/ads/api/dgen-trial-group.js`,
config template `dgen-ads/ra05.json`.

## Steps

1. **Preconditions** (`/ad-setup` step 0): hash the master, grep the board for RA-07.
2. **Title and tags.** Working title "Fire Your Trainer". Lint with `scripts/ads/ytads/lint.js`; if it fails use one of Dan's approved shapes
   (**How AI Got Me Abs**). Tags: the four standard ones plus `personal trainer,ai trainer`.
3. **Description** from the transcript (`/ad-setup` step 3, Replicate Whisper via `transcribe.js`, never local Whisper). No chapters. Keep the
   AI sentence. Link and UTMs as the skill sets them. **No em dash anywhere.**
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.
   The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one AI-enhanced or AI-generated image of Dan on the ad's
   subject (firing a human trainer for AI), (4) and (5) two AI images of Codex's choice. Five unique designs (one line each first). Real
   photos: his real cutout over a Codex background, type in code, never redrawn. Build each in 9:16 (and the 16:9 YouTube thumbnail size the
   upload needs). No claims or numbers, no "Real picture" label, no AbsByAI.com, text off his face and hair, no frowning photo, Speedo crop,
   photos not already used on another ad (`Docs/AD_VIDEO_IDS.md`). One review sheet, then **stop and ask Dan to pick.**
5. **Upload** after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`, `--synthetic true`. Set the thumbnail, read back
   `privacyStatus: unlisted`, `embeddable: true`, `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
6. **Google Ads: the cold TRIAL campaign `24316364155`.** One new ad group for RA-07 with the video, built with `dgen-trial-group.js ra07`
   (copy `ra05.json`): target CPA checked live against the reference group, campaign audience, US + CA, English, logo, CTA asset, business name
   *Abs by AI*. Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra07&utm_content=claude-9x16-vsl`,
   same domain and page as every ad in the campaign (check first). Copy per `/ad-setup` step 6, linted. `validateOnly` first, then apply and read
   back. Do not change the shared budget. Run `node scripts/ads/api/client.js policy 24316364155`, record verdicts, recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` row, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, a receipt
   `Docs/RA07_SETUP_RECEIPT_<date>.md`, edit queue `uploaded`, board entry for the policy recheck. Push with `safe-push.sh`.

## Recommended model

Claude Opus 5.5, high effort. Thumbnails by Codex GPT-6.1 Sol, high, via `codex-image.sh`.

## Starter prompt

> AD. Name this task `Fire Your Trainer AD Setup`. Read `Handoffs/handoff-20261018-ra07-setup.md` and set up the approved 9:16 of "Fire Your Trainer!" (RA-07) with /ad-setup: five thumbnail choices made with Codex (use the Codex subscription to generate the images), stop for my pick, then upload Unlisted and add it to the trial campaign.
