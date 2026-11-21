CONTENT | Belly Fat Emergency LFC Setup

# Install the approved Belly Fat Emergency thumbnail

Written October 7, 2026. Install Dan's approved Studio Alert revision 4 thumbnail on the existing public YouTube video **Your Belly Fat Is an Emergency: 7 Reasons to Take It Seriously**, video ID `v2R4QpnURqA`. This is an installation task. The thumbnail design is finished and approved.

**New task name:** `Belly Fat Emergency LFC Setup`.

**Recommended model and effort:** Codex GPT-6 Astra, high. The task requires YouTube Studio browser controls and visual verification.

## Approval and exact asset

Dan selected the Studio Alert picture and background, selected option 1 at 20% text opacity, and requested the headline almost reach both sides. Revision 4 enlarges `EMERGENCY` to a measured width of 1,218 pixels on the 1,280-pixel canvas, with approximately 31-pixel side margins. The person and background are unchanged from the selected plate. His face and hair are clear of the headline.

Dan approved the displayed revision 4 on October 7, 2026: "That looks great. Create a handoff document to install this in a new task". This authorizes installing that exact asset without another design or installation approval.

Approved full-size file:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Belly Fat Emergency/_replacement-20261007/EMERGENCY-C-r4-wide-1280x720.jpg`

- JPEG, 1280x720, 240,534 bytes, below 2 MB.
- SHA-256: `cdd813ca044a694f66ef33e7842e17aea7ed95c3f5cb365161bc5910d28c315d`.
- Phone preview: the same folder's `EMERGENCY-C-r4-wide-phone-320x180.png`.
- Drive backup folder: https://drive.google.com/open?id=1dbWJtxb0uwxxMCgk_2okUvTJLy53xc8l . The approved full-size file and phone preview were uploaded there. If the local file is missing, download the named file and confirm its hash before installation.
- Design and approval record: `Handoffs/results-20261007-belly-fat-emergency-thumbnail-review.json`.

The original thumbnail remains available for rollback:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Belly Fat Emergency/belly-fat-emergency_2-pool-photo-172-FINAL.jpg`

Original SHA-256: `cfa707224a43c8fa3bc431c3bfac3e19622eaf74723c813c7fd68fb03e17dbb9`.

## Install and verify

1. Rename the task `Belly Fat Emergency LFC Setup`. Read `AGENTS.md`, `AI_COORDINATION.md`, and `.claude/skills/_shared/VIDEO-RULES.md`. Preserve other sessions' work. The Victory Dashboard remains paused.
2. Verify the approved asset's size and SHA-256. Open `https://studio.youtube.com/video/v2R4QpnURqA/edit` in the signed-in Chrome profile. Confirm the title and video ID match this handoff. Preserve a screenshot of the current thumbnail and any available completed thumbnail-test results before replacement.
3. Under Thumbnail, use Options > Change to choose the approved JPEG. Save. Read the saved Studio state and visually confirm the transparent yellow `EMERGENCY` headline spans nearly the full width over the heavier Studio Alert body.
4. Open `https://www.youtube.com/watch?v=v2R4QpnURqA` and verify the actual public thumbnail, refreshing if needed. Pause before playback so the thumbnail can be inspected. Confirm the saved Studio image and the live public image both match the approved design. The API helper `scripts/youtube/set-thumbnail.js --video v2R4QpnURqA --read-only --out <absolute readback path>` may supply additional readback evidence, but API success alone is not visual live verification. Use the public page's displayed thumbnail or channel video tile as the decisive check; allow for caching.
5. Save Studio and public-page screenshots and a short receipt containing the installed file, hash, installation timestamp in America/Chicago, video ID, and verification evidence. Record it in `Handoffs/results-20261007-belly-fat-emergency-thumbnail-install.json` or an equivalent clearly named receipt. Commit and push the receipt and this task's completed handoff status using `scripts/git/safe-push.sh` for named files. Follow the project delivery rules and preserve unrelated changes. Update only this task's own coordination entry and handoff index row.
6. Report the live video link, installed thumbnail, and verification screenshot to Dan. If the saved image has not propagated publicly, report that specific gap and keep verification open.

## Baseline for a later packaging comparison

Before generation on October 7, Studio Reach showed **4.3K displayed impressions, 1.5% click-through rate, and 301 views**, for October 4 through the check time on October 7. These are Studio's displayed rounded impression and CTR figures. Traffic-source mix by views: Browse 80.1%, Suggested 14.6%, Channel pages 2.0%, Search 1.0%, Direct or unknown 0.7%, Other 1.7%. The separately delayed October 4-6 funnel showed 3.9K impressions and 1.6% CTR.

The baseline JSON and screenshot are in the approved asset folder as `baseline.json` and `baseline-reach.jpg`. Refresh and save the current baseline immediately before installation, since more views and impressions may have arrived. A later CTR comparison needs an explicit date range and similar traffic-source mix. Do not create a monitor or schedule a new task unless Dan asks.

## Scope

Install the exact approved revision 4. Do not regenerate images, revise the design, start an A/B test, edit or re-upload the video, change its title, description or visibility, repost it, change Blotato schedules, or change Google Ads bids, budgets or URLs. Google Ads uses the same YouTube video ID. No thumbnail has been installed in the design task.

This supersedes the installation portion of `Handoffs/handoff-20261007-belly-fat-emergency-thumbnail-replacement.md`; its image-generation phase is complete.

## Ready-to-paste starter prompt

CONTENT. Name this task `Belly Fat Emergency LFC Setup`. Read `Handoffs/handoff-20261007-belly-fat-emergency-approved-thumbnail-install.md`. Install the approved Studio Alert revision 4 thumbnail on existing YouTube video `v2R4QpnURqA` through YouTube Studio, then verify the exact design in Studio and on the public YouTube page. Dan approved the final image; no further approval or generation is needed. Preserve the old thumbnail, save the installation receipt and screenshots, and leave the video and Google Ads settings unchanged.

## Installation status, October 7, 2026

Approved revision 4 installed through YouTube Studio. Saved Studio design, full-size YouTube readback and public YouTube Videos tile verified. Public verification used a fresh browser cache after Chrome retained the old image. Receipt: `Handoffs/results-20261007-belly-fat-emergency-thumbnail-install.json`. Old thumbnail preserved. Video and Google Ads settings unchanged.
