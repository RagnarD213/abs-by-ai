# RA-09 "Do You Think AI Is Changing The World?": upload and Google Ads setup (9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `AI Changing World AD Setup`.
Written 2026-10-22 by Claude Opus 5.5, right after Dan approved round 1. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-22, on the round 1 page: *"Okay, everything looks good as is. This is approved. Proceed to setup."* (colour A, voice V1,
opening A0014, whole 9:16). Record: `Claude Ad Videos/do you think ai is changing the world - RA-09/APPROVAL.md` and
`/Volumes/Expansion/_edit_work/RA-09/r1-final/decisions.json`.

| | 9:16 |
|---|---|
| master | `Claude Ad Videos/do you think ai is changing the world - RA-09/do you think ai is changing the world \| claude \| 9x16 \| RA-09.mp4` |
| sha256 | `225018256b1c6d0013bd1108b28529ebbb04e9217894b5318393e980de26c2d2` |
| format | 1080x1920, 58.63 s, 1,757 frames, H.264 BT.709 + AAC |
| gates | audio gate PASS, delivery gate ad9x16 PASS 39/39, watch pass 0 open defects, independent review SHIP |

**Only the 9:16 exists** (as on RA-12). Set up the 9:16 alone; do not build a 16:9 in this task. Assert the hash first; the checks are
done on this exact file (stamps beside it): do not re-run or re-render. Captions SRT beside the master.
Closing line: "Tap the button below now to get started." (button CTA: an AD). Words: `/Volumes/Expansion/_edit_work/RA-09/words_aligned.json`.

AI content (disclosure flag and description), film times: opening robot-and-ripped-man clip 0-2.4 s (library A0014, AI video); the AI
prospect's goal picture 9.3-11.8 s; the app's real generation of the prospect (AI-made before photo) and his AI goal picture 16.6-23.2 s;
the analysis card on that picture 25.1-31.9 s; the app tour with the app's own AI trainer demo 31.9-36.8 s; AI clips of a man in a sling
at the gym 43.9-46.0 s, a closed gym 47.7-48.2 s and a home dumbbell workout 49.2-51.2 s. **`--synthetic true`.** Keep the description's
AI sentence from `/ad-setup` step 3. Real footage of Dan: the ab wheel clip 13.4-15.7 s and every talking shot.

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
Nearest precedent: `Handoffs/handoff-20261021-ra12-setup.md` (same steps) and its receipt if written. Trial group builder
`scripts/ads/api/dgen-trial-group.js`, config template: the newest RA config in `dgen-ads/`.

## Steps

1. **Preconditions** (`/ad-setup` step 0): hash the master, grep the board for RA-09.
2. **Title and tags.** Working title "Do You Think AI Is Changing The World?". Lint with `scripts/ads/ytads/lint.js`; if it fails use one of
   Dan's approved shapes. Tags: the four standard ones plus `ai fitness coach,ai six pack abs`.
3. **Description** from the transcript (`/ad-setup` step 3, Replicate Whisper via `transcribe.js`). No chapters. Keep the AI sentence. Link
   and UTMs as the skill sets them. **No em dash anywhere.**
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.
   The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one AI-enhanced or AI-generated image of Dan on the ad's
   subject (AI changing the world / AI coaching his body), (4) and (5) two AI images of Codex's choice (the robot-and-ripped-man idea fits).
   Five unique designs (one line each first). Real photos: his real cutout over a Codex background, type in code, never redrawn. Option 3
   must not present an AI version of his abs as a goal picture (Dan, RA-12 R2: it makes his real abs look AI-made); an AI scene around his
   REAL physique is fine. No claims or numbers, no "Real picture" label, no AbsByAI.com, text off his face and hair, no frowning photo,
   Speedo crop, photos not already used on another ad (`Docs/AD_VIDEO_IDS.md`), masculine colours. One review sheet, then **stop and ask Dan to pick.**
5. **Upload** after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`, `--synthetic true`. Set the thumbnail, read back
   `privacyStatus: unlisted`, `embeddable: true`, `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
6. **Google Ads: the cold TRIAL campaign `24316364155`.** One new ad group for RA-09, built with `dgen-trial-group.js ra09` (copy the newest RA
   config): target CPA checked live against the reference group, campaign audience, US + CA, English, logo, CTA asset, business name
   *Abs by AI*. Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra09&utm_content=claude-9x16-vsl`,
   same domain and page as every ad in the campaign (check first). Copy per `/ad-setup` step 6, linted. `validateOnly` first, then apply and
   read back. Do not change the shared budget. Run `node scripts/ads/api/client.js policy 24316364155`, record verdicts, recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` row, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, a receipt
   `Docs/RA09_SETUP_RECEIPT_<date>.md`, edit queue `uploaded`, board entry for the policy recheck. Push with `safe-push.sh` (or from a clean
   worktree if the main folder is blocked).

## Cost

Thumbnails on the Codex subscription ($0); Replicate transcription about 2 cents. No AI video generation.

## Recommended model

Claude Opus 5.5, high effort.

## Starter prompt

> AD. AI Changing World AD Setup. Rename this task `AI Changing World AD Setup` and pin it. Read `.claude/skills/_shared/VIDEO-RULES.md` (first sections) and execute `Handoffs/handoff-20261022-ra09-setup.md`: set up the approved 9:16 of RA-09 "Do You Think AI Is Changing The World?" with /ad-setup. Use the Codex subscription to generate the images: five thumbnail choices, then stop for my pick. After the pick, upload Unlisted with the AI flag on, add it to the trial campaign, record everything. Opus 5.5, high effort.
