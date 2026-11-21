# Handoff 1 — upload approved Ad 3 square R2.1 as-is

**2026-09-16 · READY, NOT EXECUTED. Recommended: GPT-6 Astra / High.**

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

## Outcome

Upload the exact approved full square Ad 3 video unlisted to Abs by AI's YouTube channel, then add it to the two existing Ad 3 Google Ads groups. Keep its picture and audio unchanged. Complete the existing YouTube/Google Ads task; do not wait for the separate checker-repair handoff.

## Latest instruction — resolves the previous upload hold

After the assistant explained the failed/unmeasured internal checks and uncertain bathroom-scene concern, Dan instructed on 2026-09-16:

> Okay create two handoff documents:
> 1. To just upload the video as is
> 2. To fix the checking software so that future videos going forward can be checked

For this exact approved export, this later instruction authorizes uploading as-is despite the documented internal-check results. It supersedes the requirement to repair the checker or obtain its PASS before uploading in `handoff-20260916-ad3-square-youtube-google-ads.md` and the earlier setup assessment. **Do not stop again for the same checks, the same disclosed bathroom scene, or repeat creative approval.**

Preserve the truthful FAIL report; do not forge a PASS, change shared thresholds, disable general enforcement, or claim Google has approved this square video. This is a user-directed release of one identified file, not a permanent exception for future videos. If an upload wrapper has since acquired internal gate enforcement, use the existing direct YouTube API upload script within this specific authorization; do not patch shared checks to manufacture a pass. Actual Google/YouTube errors must still be handled honestly. Google decides platform eligibility through its review.

This handoff authorizes execution when started. The session that wrote it only prepared documents; no upload or Ads mutation has occurred.

## Exact master

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/stop paying human trainers - ad 3/stop paying human trainers | claude | 1x1 R2.1 | ad 3.mp4`

- SHA-256: `a46861e9d1e3c5f4f517f0b9018d5f129807b9b6f2408382a38492121788646b`
- 328,520,062 bytes; 1080×1080; 7,948 frames; 30000/1001 fps; 265.198267 seconds; H.264/BT.709, AAC stereo 48 kHz.
- Encoded AAC MD5: `db408fd0bc0ba2a44245df947cb7e1f3`, preserved from the approved full vertical.
- Do not substitute R1, rejected R2, the 540p review, or the optional 59-second square. No re-render, trimming, label changes, scene replacement or audio processing.

Dan's creative approval: “This looks excellent, really great work here. The wide shots look far better than what Claude was doing with that movement tracking around and the tight shots, where you kept that movement. Everything looks great with that ad.”

Recorded results remain: structural 20/20, verbatim audio PASS; shared gate v1.2.0 overall FAIL (24 measured PASS, 3 N/A, 2 FAIL, 6 NOT MEASURED). The failures concern label template matching and an uncertain bathroom scene around 1:14–1:18; missing measurements concern captions/framing. These were disclosed before the as-is instruction. Keep them as history, not a renewed upload prerequisite.

## Read and reuse

1. Current `AGENTS.md`, `AI_COORDINATION.md`, and `.claude/skills/ad-setup/SKILL.md`. Claim only upload/setup ownership; use the existing-ad variant path. The later as-is instruction above controls this file.
2. `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, `Docs/GOOGLE_ADS_API.md`, `scripts/ads/api/dgen-ads/ad3.json`.
3. `output/ad3-square-setup-20260916/setup-manifest.json`, `ads-preflight.json`, `youtube-preflight.json`, `landing-pages.json`. They are prepared evidence, not fresh live state. Their old BLOCKED status is superseded by this instruction.
4. Inspect current arguments and behavior in `scripts/youtube/upload.js`, `scripts/youtube/set-thumbnail.js`, `scripts/ads/api/dgen-add-ad.js` and `scripts/ads/api/client.js` before executing.

## Prepared upload metadata

- Title: **Stop Paying Human Trainers! Use AI Instead**
- Description: `Muhammad Ad Videos/stop paying human trainers - ad 3/youtube-description.md`. Reuse its existing 11 chapters; speech is unchanged. The last chapter begins 4:14 and lasts 11.198 seconds. No new transcription needed.
- Privacy: **unlisted**; category **26**; not made for kids; synthetic-content disclosure **true**; embeddable.
- Tags: `ab workout,abs by ai,ai fitness,six pack abs,personal trainer,ai personal trainer`.
- Approved thumbnail: `social media graphics/youtube/thumbnails/Ad 3 Stop Paying Human Trainers/ad3-muhammad-16x9_O1-dark-studio-studio-gray-87-FINAL.jpg`.
- Thumbnail SHA-256: `1b52955a9ec9683e958b120af9ca3214f5fe0bfd6b8e4250c01f01f6f2c8ca95`. Existing dark design, smiling gray-87 photo, “STOP PAYING / PERSONAL / TRAINERS.” Reuse as requested; no redesign.
- Upload dry run already confirmed channel **Abs by AI**, `UC236gjadarHAhEhOMYNGJ9g`, on 2026-09-16.

## Account snapshot — refresh before writing

- Demand Gen campaign `24243839443`, ENABLED; budget `15862488218`, **$40/day**. Preserve the fresh live value; the skill's old $20 figure is stale.
- Campaign and both ad groups: target CPA **$30** at preflight. Preserve live bids, audiences, locations and status.
- Existing groups: `/start` **199782847163**, home **199360345839**.
- Six enabled Ad 3 ads were APPROVED/REVIEWED: `/start` **824617143813, 824617143816, 824617143819**; home **824617143822, 824617143825, 824617143828**.
- Existing videos: clean horizontal `86jbUhqBTUQ`, full vertical `xlC-tigurnA`, short vertical `-wTErCSi640`.
- Superseded video `QWW1oumpNg4`: ads **824427749693 / 824344861381** PAUSED. Leave them paused.
- Failed-upload husk `J-fOMvEJwDs`: leave alone; do not use or delete it.
- Earlier inventory found no Ad 3 square. Recheck channel, Ads inventory and local upload logs to avoid duplicates.

## Execute

1. Verify the exact master hash. Refresh relevant YouTube uploads and Ad 3 Ads state; save a before snapshot. Reuse an upload only if its provenance identifies this exact export. On retries, inspect for partial uploads before creating another.
2. Upload via `scripts/youtube/upload.js` with the exact master and metadata above. Save the upload log in the Ad 3 folder with a unique square-R2.1 filename. Set the existing thumbnail through `scripts/youtube/set-thumbnail.js` and inspect its readback.
3. Wait for YouTube processing success. Verify channel, title, unlisted privacy, synthetic disclosure, embeddability, HD square dimensions, approximately 4:25 duration, thumbnail and playback. A processing video may fail Ads validation with `YOUTUBE_VIDEO_DURATION_NOT_DEFINED`; wait rather than creating a duplicate.
4. Create a **square-only config** based on `ad3.json`, with the actual YouTube ID, version **Claude 1:1 R2.1**, UTM **claude-square-r2-1**. Preserve all 11 existing copy lines; earlier preflight confirmed they match live ads. Preserve the label, audience lookup and both destination definitions so the builder reuses existing groups.
5. Validate with `node scripts/ads/api/dgen-add-ad.js <square-only-config.json>` before `--apply`. Expected new work: **one video asset and two ads**; fewer is correct if retrying existing work. Inspect operations and names. Do not create extra groups/audiences, re-enable old ads or submit unrelated variants. The base config retains the superseded video, so do not casually execute its entire inventory.
6. The destinations are `https://absbyai.com/start` and `https://absbyai.com/`, with `utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-ad3&utm_content=claude-square-r2-1-start` or `claude-square-r2-1-home`. Both returned HTTP 200 with tracking intact at preflight. Recheck, then apply only the intended new ads.
7. Read back both ad IDs/resources, video asset, group, URLs, status and policy review state. Compare campaign settings and existing ad statuses with the before snapshot. Report `REVIEW_IN_PROGRESS` truthfully if still pending; do not claim approval based on the old vertical's approval.
8. Update `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the maintained Ad 3 config, setup status and logs with actual IDs. Record “uploaded as-is at Dan's explicit 2026-09-16 instruction; internal findings preserved.” Commit/push only task-owned non-sensitive operational changes to main, verify Railway outcome and live site per project rules. Keep media, secrets and private review evidence out of Git.
9. Retire this handoff's index/board entries on completion. Leave the independent checker-repair handoff open. Report the video link, two ad IDs, review status and unchanged budget.

This 4:25 video exceeds the Shorts-ad three-minute limit documented at preflight. Do not confuse that placement limit with a blanket Demand Gen rejection, and do not substitute the short. Check current official Google specifications only as needed for actual placement/API issues. If Google rejects the exact upload or ad, report its actual error; do not edit the approved video without a new instruction.

No public organic post, new campaign, budget increase, editor message, dashboard row or other video upload is included.

## Starter prompt

Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260916-ad3-square-upload-as-is.md` completely and execute it. Upload the exact approved Ad 3 square R2.1 as-is, unlisted, then add it to the two existing Google Ads groups. Dan explicitly authorized proceeding despite the disclosed internal-check findings; do not wait for checker repair or ask for the same approval again. Preserve the video, audio and campaign settings, verify live results, and record the IDs.
