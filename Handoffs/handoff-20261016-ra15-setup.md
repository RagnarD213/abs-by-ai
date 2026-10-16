# RA-15 "Never Pay A Nutritionist Again": upload and Google Ads setup (16:9 + 9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `Never Pay Nutritionist AD Setup`.
Written 2026-10-16 by Claude Sonnet 5.5, right after Dan approved round 4. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-16, on the round 4 page: *"Approved, mark RA-15 finalized."* Record:
`Claude Ad Videos/never pay a nutritionist again - RA-15/APPROVAL.md` and `/Volumes/Extreme/_edit_work/ra15/round4-plan/decisions.json`.

| | 16:9 | 9:16 |
|---|---|---|
| master | `Claude Ad Videos/never pay a nutritionist again - RA-15/never pay a nutritionist again \| claude \| 16x9 \| RA-15.mp4` | same folder, `... \| 9x16 \| RA-15.mp4` |
| sha256 | `f3ba15d60ce63bef56b9e41507359dcd8c74c7d52258a5275d58123b230de65f` | `2d990d91126697c219cb5aae3a9b6731c972cc9c901a89ca6ab6d5790c2d9b5d` |
| format | 1920x1080, 51.85 s, 1,554 frames, H.264 BT.709 + AAC | 1080x1920, same length and audio |
| gates | delivery gate 38 of 39 (only `audio:stamp`: the tone row from Dan's bass lift, the state RA-14 and RA-06 were approved in), watch pass 0 open defects, independent review SHIP | the same |

Assert both hashes before anything. **The delivery checks are done on these exact files** (stamps beside them): do not re-run or
re-render. Closing line: "Tap the button below to generate an image of yourself with abs and to get a personalized nutrition plan to make
it real." (button CTA: an AD). Words: `/Volumes/Extreme/_edit_work/ra15/words_aligned.json`; captions `cap_16x9/captions.srt` and
`cap_9x16/captions.srt`. Notes: `notes.md` in the ad folder. 16:9 edit sheet beside the master (approved).

AI content (for the disclosure flag and the description), times in the film: museum opener 0.0-2.3 s (realistic AI man in a display
case), the app's AI generation of a man who is NOT Dan 17.5-24.99 s (labelled), the AI man at the fridge 29.0-31.3 s, the AI man eating a
steak 31.3-33.3 s, the AI restaurant scene 37.0-39.0 s, and the AI lock-screen goal picture of Dan 43.2-45.3 s. **`--synthetic true` on
both uploads.** The description's AI sentence from `/ad-setup` step 3 stays.

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
Nearest precedents: `Handoffs/handoff-20261016-ra06-setup.md`, `Handoffs/handoff-20261014-ra05-setup.md`; the trial group builder is
`scripts/ads/api/dgen-trial-group.js` with `dgen-ads/ra05.json` as the config template.

## Steps

1. **Preconditions** (`/ad-setup` step 0): hash both masters, grep the board for RA-15 (this doc's line in `Handoffs/README.md` OPEN is the only one).
2. **Title and tags.** Working title "Never Pay A Nutritionist Again". Run it through `scripts/ads/ytads/lint.js`; if it fails, use one of
   Dan's approved shapes (**How AI Got Me Abs**). Tags: the four standard ones plus `nutrition plan,meal plan`.
3. **Description** from the transcript (`/ad-setup` step 3, Replicate Whisper via `transcribe.js`, never local Whisper). A 52 s ad needs no
   chapters. Keep the AI-image sentence. Link and UTMs as the skill sets them. **No em dash anywhere.**
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol
   --effort high` on Dan's subscription. The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one AI-enhanced
   or AI-generated image of Dan on the ad's subject (AI replacing the nutritionist), (4) and (5) two more AI images of Codex's choice.
   Five unique designs (one line each: layout, type, colour, composition, before building). Real photos: his real cutout over a Codex
   background, type set in code, never redrawn. Build each pick in 16:9 and 9:16. No claims or numbers, no "Real picture" label, no
   AbsByAI.com, text off his face and hair, no frowning photo, Speedo crop at the waistband, photos not already used on another ad
   (`/ad-setup` step 4 list and `Docs/AD_VIDEO_IDS.md`). One review sheet, then **stop and ask Dan to pick.**
5. **Upload both** after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`, `--synthetic true`. Set the picked
   thumbnails, read back `privacyStatus: unlisted`, `embeddable: true`, `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
   Upload one at a time or two at most (a big parallel upload once died at 90 %).
6. **Google Ads: the cold TRIAL campaign `24316364155`** (`[DAN] [DGEN] [TRIAL] VSL page`, where every current ad lives; never enable a paused
   campaign). One new ad group for RA-15 with both videos, built with `dgen-trial-group.js ra15` (copy `ra05.json`): target CPA checked live
   against the reference group, the campaign's audience, US + CA, English, logo, CTA asset, business name *Abs by AI*. Final URL on
   `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra15&utm_content=claude-<format>-vsl`, the same
   domain and page as every ad in the campaign (check before creating). Copy: 5 headlines, 3 long headlines, 3 descriptions per `/ad-setup`
   step 6, linted (no "trick", no questions, no withheld payoff, no drug words). `validateOnly` first, then apply and read back. **Read the
   campaign's shared budget and do not change it**; say in the report it is now shared by one more ad group. Run
   `node scripts/ads/api/client.js policy 24316364155`, record the verdicts, recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` rows, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, config and result JSON
   under `scripts/ads/api/dgen-ads/`, edit queue `python3 scripts/edit-queue/queue.py set RA-15 uploaded` + the artifact mirror (only after
   both read-backs and the ads exist). Commit with `scripts/git/safe-push.sh`. Put a policy-recheck board entry up (like RA-06's) until clean.

## Already done (do not redo)

Edit queue: RA-15 `finalized` (2026-10-16). Clip library: A0176 fridge, A0177 restaurant used-final RA-15; A0178 (cardboard cutout) was
removed from the ad in round 4 and is `usable-unused`. Review copies deleted from `Videos to Review`. The round 4 review page service on
port 8978 is still up only so Dan can test the repaired timeline scrubbing; remove it with
`python3 .claude/skills/_shared/review_server.py 8978 --remove` once he has confirmed (or after 2026-10-18).

## Not this task

No Facebook, Instagram, TikTok, Blotato or Public YouTube copy. No pinned comment (ads get none). No square or 59 s cut (the ad is 52 s;
a cutdown only if Dan asks).

## Recommended model and effort

Claude Opus 5.5, high effort (copy, thumbnails choice-making and the ads write-up are editorial; the upload and Ads steps are mechanical but
chained). Sonnet 5.5 is fine for steps 5-7 only if Dan's thumbnail pick is already recorded.

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Never Pay Nutritionist AD Setup`. Read `Handoffs/handoff-20261016-ra15-setup.md` and set up the approved RA-15 "Never Pay A Nutritionist Again" 16:9 and 9:16 with /ad-setup. Both masters already passed every delivery check. Use the Codex subscription to generate the images: make the five thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload both to YouTube as Unlisted, add them to the trial campaign 24316364155 in their own ad group, run the policy check and record everything.
