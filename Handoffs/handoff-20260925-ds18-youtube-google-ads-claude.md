# DS-18 R8 handoff for Claude: YouTube and Google Ads setup

Prepared September 25, 2026. This document prepares a new task. No YouTube upload, Google Ads change, organic post, or schedule was made while writing it.

## Dan's decision and goal

Dan reviewed the R8 private copy and said: "All right this is looking great. This video is finalized." He then asked for a separate task to upload this video to YouTube and set it up in Google Ads. Creative approval is complete. Use the exact approved R8 master without another edit or render.

Treat this as the paid video path: one **Unlisted** YouTube upload that Google Ads references. Do not make a Public or Private organic copy, use YouTube native scheduling, or queue it through Blotato. The requested upload and Ads setup belong to the next task, not this handoff task.

## Exact approved files

- Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
- Upload master: `Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4`. SHA256 `aa7fe8747dcb3a4a8b26e1b32b598c1c502606ee00efe878ee99aaf2d1b60ba2`. It is 81,989,796 bytes, 1080x1920, 30000/1001 fps, 1,257 frames, 41.9419 seconds, H.264 and AAC.
- R8 review proxy, **never upload this proxy**: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/DS-18-R8-full-video-review.mp4`. SHA256 `f36557db515117a76db0fa0ab508e23947a10df5c52922632dbbe3512bce62e8`.
- Dan-approved cover: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/covers/instagram/ds-18_how-to-kettlebell-deadlift_cover-C-video-frame-r5.png`. SHA256 `6021589257e4be64fa3131313c6ed56048847408fdbb8b74f782dc475c660706`. It is 1080x1920 and about 3.18 MB. If the YouTube thumbnail tool needs another file format or smaller file, make a faithful export of this approved design, inspect it, and keep the original unchanged.
- Production record: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/WORK_PACKET.json`, `final-r8-manifest.json`, and `notes-r8.md`.
- Finished-file transcript: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/finished-asr-r8.json`. Reuse it for metadata; no new transcription is needed unless the next task finds a specific gap.

Before uploading, hash the local master and inspect YouTube plus Google Ads for an existing upload or asset of this exact R8 version. Do not create a duplicate on retry. If the hash differs, stop using that file and locate the approved master above.

## Verification and the known gate result

R8 removed only the upper-right `KETTLEBELL DEADLIFT` graphic from all five presenter spans. The lower AbsByAI.com mark, synchronized teaching B-roll, red and green arrows, audio, captions, opening, Start Today deletion, final comment CTA, color, runtime, frame size, and cover were preserved. The independent reviewer passed all 1,257 frames and all 15 picture joins with zero open defects. The AAC packet payload is identical to R7. Review evidence: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/independent-r8/findings.json` and `logs/watch_pass_r8.json`. A literal headphone listen was unavailable.

The exact R8 delivery gate is **FAIL, 33 passed, 6 failed, 3 not applicable**, the same six failures as R7: `audio:stamp`, `framing:no_wide_level`, `framing:push_coverage`, `captions:burned`, `captions:sync`, and `compliance:placeholder`. See `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/logs/delivery-gate-r8.json` and the sidecar beside the upload master. Dan finalized R8 after these failures were reported. This is his decision to use the exact file as approved, not a gate PASS. Do not alter thresholds, forge a stamp, silently process audio, or reopen the approved creative solely to make the legacy checks pass. State the gate result accurately in the setup record.

## Read before account work

1. `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, this handoff, and the current `AI_COORDINATION.md`.
2. `.claude/skills/ad-setup/SKILL.md`, especially upload readback, Demand Gen setup, budget preservation, and record keeping. This is a new paid video, so inspect the current campaign and choose the existing campaign's appropriate setup path. Do not assume that DS-18 has an ad number or an existing pair of ad groups.
3. `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, `Docs/GOOGLE_ADS_API.md`, and the current `scripts/youtube/` and `scripts/ads/api/` implementations. Recorded account IDs and budget values can be stale; read live state before changes.
4. `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/edit-queue/README.md` for DS-18 status updates. DS-18 is `finalized` now.

## Execution for the new Claude task

1. Verify the exact master, approved cover, current edit queue state, YouTube channel, campaign status, existing videos and ads. Record the current shared campaign budget, bid settings, audiences, destinations, and enabled or paused states. Preserve them. Do not enable a paused campaign.
2. Prepare a concise YouTube title, description, topic tags, and any useful chapters from the finished transcript. Use the video's actual teaching content. Preserve the approved cover design. Check the current upload script's synthetic-content option against the actual R8 footage instead of copying another ad's setting.
3. Upload the exact master once to the established YouTube channel as **Unlisted**. Install the faithful cover export where supported. Read back the channel ID, saved `privacyStatus: unlisted`, processing success, playable duration and frame size, embeddability, title and thumbnail. If an upload call fails, inspect for a partial video before retrying.
4. Add the verified YouTube video to the existing Google Ads Demand Gen conversion setup using the project's validate-only then apply flow. Use copy that describes this kettlebell instruction accurately and destinations and tracking consistent with the existing campaign. Judge results by cost per trial and paying customer. Keep the shared budget and existing ads unchanged. Read back the actual ad IDs, video asset, groups, URLs, statuses, and Google review state. Do not claim Ads approval while review is pending.
5. Verify the YouTube playback and destination URLs. Record the YouTube ID, exact video URL, thumbnail readback, Ads IDs, campaign settings before and after, metadata, and any unresolved review status in the normal setup records. Update `Docs/AD_VIDEO_IDS.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md` with actual results. Set the DS-18 edit queue state to `uploaded` only after the Unlisted readback and Google Ads entries exist. Commit and push only task-related records, then verify Railway's result and the live site. Do not add a dashboard row unless Dan asks.

This handoff does not authorize a budget increase, a new paid plan, an organic post, a Public upload, a video revision, or changes to other ads. The existing campaign's shared budget may be used as configured. Tell Dan exactly what became active and what remains in Google review.

## Exact next action and starter prompt

Recommended model: **Claude Fable 5.1, high effort**. This task crosses YouTube and Google Ads, and it must handle an approved creative with a recorded gate failure without changing the media or misreporting the checks.

> Read `Handoffs/handoff-20260925-ds18-youtube-google-ads-claude.md` in full and execute it. Dan finalized DS-18 R8. Use only the SHA256-locked full-resolution master and approved cover. Upload one Unlisted YouTube copy, verify its saved visibility and processing, then add it to the existing Google Ads Demand Gen conversion setup while preserving the live budget and other ads. Record IDs and readbacks, update the DS-18 queue to uploaded only after both setups exist, commit and push the operational records, and report the six existing delivery-gate failures honestly. Do not make an organic post or alter the approved video.
