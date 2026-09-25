# Ad 10 approved verticals: YouTube and Google Ads setup

Written: 2026-09-25

Recommended fresh task: Codex GPT-6 Astra, high effort.

## Goal

Upload the two exact approved AV-07 Ad 10 vertical masters to YouTube as Unlisted videos, create one matching 9:16 thumbnail, and add both videos as new variants in the existing Ad 10 Demand Gen ad groups. Preserve the existing 16:9 ads and all live campaign settings.

This is an advertising setup job. These videos must never be published organically.

## Read first

1. `AGENTS.md`
2. `.claude/skills/_shared/VIDEO-RULES.md`
3. `AI_COORDINATION.md`
4. This handoff
5. `.claude/skills/ad-setup/SKILL.md`

Use `/ad-setup` as the operating method. Read live state before writing anything. Check existing YouTube uploads first so the task does not create duplicates.

## Dan's final approval

Exact verdict on 2026-09-25:

> This is looking great. This ad is finalized. Create a handoff document to upload and set this ad up on YouTube and Google Ads in a new task

This approval applies to both exact files below. Do not re-edit, transcode, shorten, normalize, or otherwise change either master.

## Exact approved assets

| Version | Exact path | SHA256 | Bytes | Technical facts |
|---|---|---|---:|---|
| Full 9:16 | `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/my dad bod at 38 my dad bod at 40 \| claude \| 9x16 \| ad 10.mp4` | `b25b6e50e106cc4c6407fc949ff6edda25ceab8b1c75a559eff6427b0fc32cc6` | 172461205 | 1080x1920, 30000/1001 fps, 5443 frames, 181.615 seconds |
| 9:16 cutdown | `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/my dad bod at 38 my dad bod at 40 \| claude \| 9x16 59s \| ad 10.mp4` | `36ae2f6d528ebf34692e81040343c88d17046eff27a25bc1c266f2fd816dd00f` | 43503202 | 1080x1920, 30000/1001 fps, 1712 frames, 57.124 seconds |

Review copies are not upload sources.

## Approval and quality evidence

Both exact masters passed the shared delivery gate with 39 of 39 rows passing. Muhammad's audio is untouched and verified verbatim against the approved reference mix. Fresh review sessions inspected every assigned contact sheet and strip and found zero open defects. Every real picture of Dan has the required label, and every label is clear of his face and abs.

Evidence:

- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/notes-vertical.md`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/gate-full.json`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/gate-cutdown.json`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/audio-gate-full.json`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/audio-gate-cutdown.json`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/full-judges/`
- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/cutdown-judges/`

Corpus records:

- `av07-ad10-vertical-full-final-approved-20260925`
- `av07-ad10-vertical-59s-final-approved-20260925`

## Existing live Ad 10 state

Read everything back from YouTube and Google Ads before changing it. These IDs are the last recorded state, not a substitute for a live read.

- Existing YouTube 16:9 video: `Sg3vcEY2P_8`
- Existing Google Ads video asset: `421589398534`
- Campaign: `24243839443`
- Audience: `359638252`
- `/start` ad group: `206979993984`
- Existing `/start` ad: `824793606450`
- Home ad group: `206979994264`
- Existing home ad: `824793582135`
- Config: `scripts/ads/api/dgen-ads/ad10.json`
- Recorded shared campaign budget: $40 per day
- Recorded ad group target CPA: $30

Do not change the budget, bids, audience, existing ads, existing assets, landing pages, or campaign structure. If live state differs from the records, preserve the live state and document the difference.

## YouTube work

Upload both exact masters as new YouTube videos with visibility set to Unlisted. Never use Public visibility and never schedule publication.

Suggested titles:

- `My Dad Bod at 38. My Dad Bod at 40. (Vertical)`
- `My Dad Bod at 38. My Dad Bod at 40. (Vertical 59s)`

For the full version, start from:

- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/youtube-description.md`

Its existing timeline and chapters apply to the full vertical. For the cutdown, create:

- `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/youtube-description-vertical-59s.md`

The cutdown description must not include chapters. Keep the disclosure and use the tracked URL with `utm_campaign=dgen-conv-ad10`.

For both uploads:

- `containsSyntheticMedia=true`
- Not made for kids
- Category 26
- Embedding allowed
- Visibility Unlisted

After processing, read back and record the video ID, title, visibility, processing status, HD status, embeddable state, exact duration, and thumbnail state.

## Thumbnail

The approved 16:9 reference is:

`social media graphics/youtube/thumbnails/Ad 10 My Dad Bod/ad10-muhammad-16x9_O1-dark-studio-studio-gray-26-FINAL.jpg`

Create one 1080x1920 thumbnail that adapts this same dark studio design for both new vertical uploads. Use the `/ad-setup` thumbnail method or the current project thumbnail tooling.

Requirements:

- Match the established Ad 10 dark studio design.
- Keep all text clear of Dan's face and hair.
- Keep his abs visible.
- Do not add a real-picture label.
- Do not add `AbsByAI.com`.
- Do not use the frowning image.
- Install the same approved vertical thumbnail on both new uploads.
- Read back and save proof that each thumbnail was accepted.

## Google Ads work

Read the live Ad 10 copy first. If it differs from `scripts/ads/api/dgen-ads/ad10.json`, use and preserve the live copy.

Keep the existing config entry:

```json
{ "youtubeId": "Sg3vcEY2P_8", "version": "Muhammad 16:9", "utm": "muhammad-16x9" }
```

Add these two entries using the actual new YouTube IDs:

```json
{ "youtubeId": "<full vertical video id>", "version": "Claude 9:16", "utm": "claude-9x16" }
{ "youtubeId": "<57 second video id>", "version": "Claude 9:16 59s", "utm": "claude-9x16-59s" }
```

Run validate only first. The expected change is exactly two new Google Ads video assets and four new ads, one of each vertical version in each of the two existing Ad 10 ad groups. Reuse the existing audience and groups.

If validation matches that scope, apply it. Do not pause or replace the current 16:9 ads. Read back and record every new asset ID, ad ID, ad group, enabled state, final URL, tracking parameter, and policy status.

Policy review may still be pending when the setup is complete. Record the status and any follow-up date without weakening or replacing existing ads.

## Records and closeout

Update these records with the new YouTube and Google Ads IDs:

- `Docs/AD_VIDEO_IDS.md`
- `Docs/DGEN_CONVERSION_CAMPAIGN.md`
- `scripts/ads/api/dgen-ads/ad10.json`
- The current Google Ads result or execution log used by `/ad-setup`
- `Handoffs/video-editing/jobs.json` and `Handoffs/video-editing/00-MASTER.md`, moving AV-07 to uploaded after full readback verification

When the setup is complete, remove this handoff from the Open table in `Handoffs/README.md` and from the HANDOFFS section in `AI_COORDINATION.md`. Commit only the files changed for this setup, push `main`, confirm the push, and verify `https://absbyai.com` still responds successfully.

## Boundaries

- No organic posting anywhere.
- YouTube visibility is Unlisted only.
- Do not upload the review copies.
- Do not alter either approved video.
- Do not create another format.
- Do not change campaign budget, target CPA, audience, copy, existing ads, or existing assets.
- Do not pause the current 16:9 ads.

## Exact next action

Verify both hashes, read live YouTube and Google Ads state, and check YouTube for duplicate uploads before creating the vertical thumbnail or uploading anything.

## Ready-to-paste starter prompt

Read and execute `Handoffs/handoff-20260925-ad10-verticals-youtube-google-ads.md` using `.claude/skills/ad-setup/SKILL.md`. Dan finalized both exact AV-07 masters. Verify their hashes, create the matching 9:16 thumbnail, upload both exact files to YouTube as Unlisted, and add them as `Claude 9:16` and `Claude 9:16 59s` variants to the existing Ad 10 Demand Gen groups. Preserve the live 16:9 ads and all campaign settings. Read back visibility, processing, asset IDs, ad IDs, final URLs, and policy state. Update records, commit, and push. Never publish these ads organically.
