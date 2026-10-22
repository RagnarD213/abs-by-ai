# RA-12 "The First Step To Getting Abs Isn't A Workout": upload and Google Ads setup (9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `First Step Abs AD Setup`.
Written 2026-10-21 by Claude Opus 5.5, right after Dan approved round 2. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-21, on the round 2 page: *"Okay, everything is finalized and approved. Let's proceed to setup."*
Record: `Claude Ad Videos/the first step to getting abs isnt a workout - RA-12/APPROVAL.md` and
`/Volumes/Expansion/_edit_work/ra12/round3-plan/decisions.json` ("final").

| | 9:16 |
|---|---|
| master | `Claude Ad Videos/the first step to getting abs isnt a workout - RA-12/the first step to getting abs isnt a workout \| claude \| 9x16 \| RA-12.mp4` |
| sha256 | `18728d49ab7a8e0f4dd43f0a8aa63554f8edb627362abc1b088e1ab98d94b539` |
| format | 1080x1920, 46.25 s, 1,386 frames, H.264 BT.709 + AAC |
| gates | delivery gate 38 of 39 (known row: `audio:stamp` from the approved bass lift's tone row, as RA-07 shipped), watch pass 0 open defects (captions over the two prospect photos accepted by Dan), independent review SHIP |

**Only the 9:16 exists.** Dan asked for setup on approving the 9:16: set up the 9:16 alone. Do not build a 16:9 in this task.
Assert the hash before anything. The delivery checks are done on this exact file (stamps beside it): do not re-run or re-render.
Closing line: "So take the first step. Tap the button below to see yourself with abs." (button CTA: an AD).
Words: `/Volumes/Expansion/_edit_work/ra12/words_aligned.json`; captions `.../RA-12.srt` beside the master.

AI content (disclosure flag and description), film times: the AI prospect's goal picture 4.1-5.2 s (labelled); a phone lock screen
with his AI goal picture 11.5-12.9 s (library A0180, AI video); a worn-out beginner on a gym floor 14.0-15.5 s (library A0172, AI
video); the app's real generation of the prospect (AI-made before photo) and his AI goal picture 16.8-21.7 s; the analysis card on
that picture 26.8-33.7 s; the app's own AI trainer push-up demo 33.7-39.3 s. **`--synthetic true`.** Keep the description's AI
sentence from `/ad-setup` step 3. The opening clips are REAL footage of Dan (ab wheel 2.3-3.2 s, salad 3.2-4.1 s).

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
Nearest precedent: `Handoffs/handoff-20261018-ra07-setup.md` (same steps) and its receipt if written. Trial group builder
`scripts/ads/api/dgen-trial-group.js`, config template `dgen-ads/ra05.json` (or the newest RA config there).

## Steps

1. **Preconditions** (`/ad-setup` step 0): hash the master, grep the board for RA-12.
2. **Title and tags.** Working title "The First Step To Getting Abs". Lint with `scripts/ads/ytads/lint.js`; if it fails use one of Dan's
   approved shapes (**How AI Got Me Abs**). Tags: the four standard ones plus `ai goal picture,see yourself with abs`.
3. **Description** from the transcript (`/ad-setup` step 3, Replicate Whisper via `transcribe.js`, never local Whisper). No chapters. Keep
   the AI sentence. Link and UTMs as the skill sets them. **No em dash anywhere.**
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.
   The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one AI-enhanced or AI-generated image of Dan on the ad's
   subject (seeing your goal picture first), (4) and (5) two AI images of Codex's choice. Five unique designs (one line each first). Real
   photos: his real cutout over a Codex background, type in code, never redrawn. ⚠ Dan's round 2 reason for the prospect: *"using my own
   picture makes it seem like I don't really have abs and that my abs are AI-generated"*. Option 3 must not present an AI version of his
   abs as the goal picture; prefer an AI scene around his REAL physique (e.g. him holding up a phone showing a goal picture). No claims or
   numbers, no "Real picture" label, no AbsByAI.com, text off his face and hair, no frowning photo, Speedo crop, photos not already used on
   another ad (`Docs/AD_VIDEO_IDS.md`). Build each in 9:16 (and the 16:9 YouTube thumbnail size the upload needs). One review sheet, then
   **stop and ask Dan to pick.**
5. **Upload** after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`, `--synthetic true`. Set the thumbnail, read back
   `privacyStatus: unlisted`, `embeddable: true`, `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
6. **Google Ads: the cold TRIAL campaign `24316364155`.** One new ad group for RA-12 with the video, built with `dgen-trial-group.js ra12`
   (copy the newest RA config): target CPA checked live against the reference group, campaign audience, US + CA, English, logo, CTA asset,
   business name *Abs by AI*. Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra12&utm_content=claude-9x16-vsl`,
   same domain and page as every ad in the campaign (check first). Copy per `/ad-setup` step 6, linted. `validateOnly` first, then apply and
   read back. Do not change the shared budget. Run `node scripts/ads/api/client.js policy 24316364155`, record verdicts, recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` row, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, a receipt
   `Docs/RA12_SETUP_RECEIPT_<date>.md`, edit queue `uploaded`, board entry for the policy recheck. Push with `safe-push.sh` (or from a clean
   worktree if the main folder is blocked).

## Cost

Thumbnails on the Codex subscription ($0); Replicate transcription about 2 cents. No AI video generation.

## Recommended model

Claude Opus 5.5, high effort (the thumbnail designs and copy need judgment; the Google Ads steps are scripted).

## Starter prompt

> AD. First Step Abs AD Setup. Rename this task `First Step Abs AD Setup` and pin it. Read `.claude/skills/_shared/VIDEO-RULES.md` (first sections) and execute `Handoffs/handoff-20261021-ra12-setup.md`: set up the approved 9:16 of RA-12 "The First Step To Getting Abs Isn't A Workout" with /ad-setup. Use the Codex subscription to generate the images: five thumbnail choices, then stop for my pick. After the pick, upload Unlisted with the AI flag on, add it to the trial campaign, record everything. Opus 5.5, high effort.
