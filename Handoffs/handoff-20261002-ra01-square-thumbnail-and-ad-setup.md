# RA-01 square: matching 1:1 thumbnail, Unlisted upload, add to the trial ad group

Created 2026-10-02. Recommended: **Claude Opus 5.5, Medium** (one thumbnail from an existing recipe, then a recipe-backed setup).
Session name: `AI Got Me Abs S Ad Setup`.

## Goal

Dan approved the RA-01 1:1 square on 2026-10-02 (*"This looks good, and it is approved."*). Put it to work:

1. Make ONE 1:1 thumbnail that matches the thumbnail already on RA-01's 16:9 and 9:16 (option **RA-R2A**).
   **Use the Codex subscription to generate the images** if any new image is needed.
2. Upload the square to YouTube **Unlisted**, with that thumbnail.
3. Add it as one more video on the RA-01 ad in the trial campaign.

This is an AD. It never goes out organically: no Blotato, no Public, no native scheduling.

## The exact approved file (do not substitute, do not re-encode)

Folder: `Claude Ad Videos/the ai trick that got me abs - RA-01/`

- **Master:** `the ai trick that got me abs | claude | 1x1 | RA-01.mp4`
- **SHA-256:** `3e7939bcc571c9a895429278d59a40b07465c1bda76ad5c76095ae93723ecedd` (assert it before uploading)
- 1080x1080, 30000/1001 fps, 1714 frames, 57.19 s, about 8.5 Mbps, AAC stereo. It is already under 0:59, so there is
  no separate cutdown.
- Stamps beside it: audio gate PASS, delivery gate 2.4.0 `ad1x1` PASS (39 of 39), label check PASS. Reviewer round 2: SHIP.
- Approval record: `APPROVAL.md` in that folder. Build notes: `notes-square.md`. Corpus entry
  `ra01-ai-trick-1x1-approved-20261002`.
- The `REVIEW 540p 1x1` copy is for viewing only, never the upload source.

Ad or organic check (VIDEO-RULES 2026-09-28): the file ends "To generate an image of yourself with six-pack abs, tap the
button below." That is an ad call to action, so `/ad-setup` is the right path. Record that line in the setup notes.

## Read first

- `.claude/skills/_shared/VIDEO-RULES.md` in full, then `.claude/skills/ad-setup/SKILL.md` in full. This is a new format
  of an ad that is already running: use the skill's added-version path (step 6), not first-time campaign setup.
- `.claude/skills/_shared/IMAGE-GENERATION.md` (Codex only for any generated still; a real photo of Dan is never redrawn).
- `Docs/DGEN_CONVERSION_CAMPAIGN.md`: the "2026-09-18 RA-01" section, the trial campaign sections (10-01) and the
  "2026-10-02: new thumbnails on the trial campaign's 12 ad videos" table.
- `Docs/AD_VIDEO_IDS.md`, `Docs/GOOGLE_ADS_API.md`, memory `google-ads-api-client`, `youtube-upload-capability`,
  `thumbnail-no-claims`, `ads-never-organic`.
- Template for a square added to a live ad: `Handoffs/handoff-20260916-ad3-square-upload-as-is.md` and
  `scripts/ads/api/dgen-ads/ad1-square.json` (a config whose copy is read back from the live ad; the dry run must REUSE
  the ad group, never create one).

## Part 1: the matching square thumbnail

What is installed on the other two formats: **RA-R2A**, the purple scene with the arms-up studio portrait
(`studio-blue-53`). Finals: `social media graphics/youtube/thumbnails/RA-01 The AI Trick That Got Me Abs/trial-20261001/`
(`RA-01 | 16x9 | FINAL.jpg`, `RA-01 | 9x16 | FINAL.jpg`). Durable recipe:
`scripts/covers/trial-campaign-20261001/round2/build.py` (design row `id='RA-R2A'`; its `SIZES` already has
`'1x1': (1080, 1080)`, and `3-R2A` shows how a square layout is composed there). Work folder and generated backgrounds:
`social media graphics/youtube/thumbnails/_trial-campaign-20261001/`.

- Build `RA-01 | 1x1 | FINAL.jpg` (1080x1080) in the same design: same portrait, same purple scene, same copy, same type.
  Start from the existing generated background. Only if the square needs more background than exists, generate it with
  `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` (Dan's subscription, no paid image API).
  Codex makes the background only; Dan's real cutout and the type are layered on in code.
- Do not run or change the round-1 or round-2 outputs in place: write the square to a new `round2-square/` folder and
  the final beside the other two in `trial-20261001/`.
- Check it at full size and at phone size: text clear of his face and every part of his hair, abs visible, nothing cut
  at the edges, no real-picture label and no AbsByAI.com on a thumbnail, copy identical to the 16:9.
- Dan asked for one matching thumbnail, not a five-choice round. Do not stop for a pick: install it, and show it to him
  in the final report beside the 16:9 so he can ask for a change.

## Part 2: YouTube (Unlisted)

- `scripts/youtube/upload.js` (read its arguments first). Visibility **unlisted**. Read the saved visibility back; anything
  else is a failure to fix before continuing.
- Title, description, tags: match the two RA-01 uploads (`OUw788sF1KY` 16:9, `rfCsWNxuNV0` 9:16). The description text
  is `Claude Ad Videos/the ai trick that got me abs - RA-01/youtube-description.md`. Read the live title back from one
  of the two existing videos and reuse it.
- AI label: this ad contains no AI video clips, only still AI goal images that carry the on-screen AI-GENERATED label.
  Per VIDEO-RULES 2026-09-27 that does not trigger YouTube's altered/synthetic flag. Check how the two existing RA-01
  uploads were set and match them; record the choice.
- Set the thumbnail from Part 1 (`scripts/youtube/set-thumbnail.js`), then save a `readback-<id>.jpg` and open it.
- Add the row to `Docs/AD_VIDEO_IDS.md`.

## Part 3: Google Ads

- Account `3427170837`. Trial campaign `24316364155`, RA-01 ad group `206348100928`. Existing ads there: 16:9
  `826595554299`, 9:16 `826595554302`. Treat these ids as a recorded snapshot: read the live state first
  (`node scripts/ads/api/client.js ...`, see `Docs/GOOGLE_ADS_API.md`).
- Add the square as one more video on RA-01 in that ad group, following `/ad-setup` step 6. Read the headlines, long
  headlines and descriptions back from the live RA-01 ads and reuse them exactly. Dan rewrote the trial headlines himself
  on 10-01, so never restore older copy from `ra01.json`.
- Write `scripts/ads/api/dgen-ads/ra01-square.json`, run `validateOnly` first, confirm it reuses the ad group, then apply.
- RA-01 also had ad groups in the older Demand Gen campaign (config `ra01.json`, set up 09-18). Check whether those are
  still enabled. If they are, add the square there too and say so; if they are paused or removed, leave them alone.
- Read the new ad's status and policy back. Put a one-line board entry up for the next-day policy check
  (`node scripts/ads/api/client.js policy 24316364155`), and add the square to the table in
  `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

## Close out

- `python3 scripts/edit-queue/queue.py set AS-13 uploaded --by Claude --note "..."`, mirror it to the Edit Queue artifact
  (the `jobs/AS-13` document is at version 2; pin `if_version`), then `mark-synced`.
- Update the RA-01 row of the format matrix in `Handoffs/video-editing/00-MASTER.md` (square uploaded).
- Delete the board entry "RA-01 square" and this handoff's lines in `AI_COORDINATION.md` and `Handoffs/README.md`.
- Commit with `scripts/git/safe-push.sh` (docs, configs and scripts only, never media).
- Report to Dan in plain language with a numbered action list, the thumbnail shown last. No em dashes anywhere.

## Do not

Re-encode or re-edit the master; upload Public or schedule natively; post anywhere organic; create a new campaign or ad
group; change budgets, bids, audiences or other ads' copy; use any image model other than Codex on the subscription;
add a dashboard row.

## Starter prompt

> Read `Handoffs/handoff-20261002-ra01-square-thumbnail-and-ad-setup.md` and the files it lists. Name this session
> "AI Got Me Abs S Ad Setup". Make the one matching 1:1 thumbnail for the approved RA-01 square (same RA-R2A design as
> the 16:9 and 9:16; use the Codex subscription to generate the images if a new background is needed), upload the
> square to YouTube Unlisted with that thumbnail, add it to the RA-01 ad group in the trial campaign with the live copy
> read back, verify, and send me a numbered action list with the thumbnail last. Never Public, never organic. No em dashes.

Model and effort: Claude Opus 5.5, Medium.
