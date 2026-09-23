# Install five approved YouTube Shorts covers

Prepared September 23, 2026. **Completed September 23, 2026. All five covers installed and verified in YouTube Studio.**

Recommended model: **GPT-6 Sol, Medium effort.**

## Goal and authorization

Install the five exact approved portrait covers on the five existing YouTube Shorts below. Dan approved all five on September 23, including the genuine smiling front-facing stomach vacuum frame. The design choices and thumbnail replacement are authorized. Do not ask for another design approval, redesign the images, edit the videos, re-upload them, or change their visibility, title, description, schedule, or other platforms.

The first Short was due September 24 at 5 PM America/Chicago when the set was reviewed. Read current Studio state before acting. Finish its cover first if it is still pending, then the remaining four.

## Exact approved files

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`

Canonical upload folder: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/next-five-redesign-20260922/finalized/upload/`

The adjacent `manifest.json` records the full paths, SHA-256 hashes, dimensions, and sizes. All five are 1080 x 1920 JPEGs below 2 MB. Use these JPEGs, not any earlier A/B or review variation.

| Order | Short ID | Short title | Exact upload filename | SHA-256 |
|---|---|---|---|---|
| 1 | `tqURi3qdrIc` | Weigh Yourself Every Single Day. Here's Why. | `01-weigh-tqURi3qdrIc.jpg` | `4dbfc488d2b086ba06deb58642df7aa5bbe2cda4cd3338af8698a2c5dd93fb30` |
| 2 | `_Ep_hVPZYzE` | Never Start Your Day With Carbs | `02-carbs-_Ep_hVPZYzE.jpg` | `30047ff87b1cbcbbef082853148e33608d5c0db098aa1ec91258ab4c2a6a9706` |
| 3 | `o1v3wPkNI2I` | 8 Hours In Bed Is Not 8 Hours Of Sleep | `03-sleep-o1v3wPkNI2I.jpg` | `d8593bad437e89ad28f7731ebb1352a03bbe90aac161ffe9803cc8c10783ed48` |
| 4 | `QuswpGj635A` | Why Bodybuilders Suck Their Stomach In | `04-vacuum-QuswpGj635A.jpg` | `ce99ce92885ec8f7348199b400b0614a0094e0a3e91faa62badfb51af3d69777` |
| 5 | `bi_fpkW-3eE` | Try To Knee Yourself In The Face | `05-knee-bi_fpkW-3eE.jpg` | `a87198e9b8d6e3bb1533e1ac936fd3fd54f85fa2c8f390377ab104fa9dcd31c9` |

The final vacuum image uses a real frame from `C1677.MP4` at 10.2 seconds, color graded with the established DS-04 LUT. Dan is smiling and visibly drawing in his stomach. No AI face edit was used. The other approved selections are: weigh-in B background with Dan shirtless in jeans and `WEIGH IN / EVERY DAY`; breakfast B background with a different studio jeans photo and `BREAK YOUR / FAST RIGHT`; sleep A; knee A photo with `KNEE YOURSELF / IN THE FACE` and `AB TRAINING TIP` badge.

The source PNGs are in the sibling `finalized/` folder. They are private personal-photo assets in a Git-ignored media folder, so installation must run on the same machine or with a private transfer of these exact files. Do not add the images to the public Git repository.

## Install and verify

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and `.claude/skills/coverimage/SKILL.md`. Check `AI_COORDINATION.md` for another active owner. Verify each JPEG against the hash and dimensions in `manifest.json`. Inspect the five files visually before upload.
2. In Dan's signed-in Chrome session, open `https://studio.youtube.com/video/<Short ID>/edit` for each ID. Confirm the ID and title in Studio. Capture the current thumbnail and any available A/B test results before replacement. The standing thumbnail replacement authorization in `VIDEO-RULES.md` applies.
3. Use Studio's thumbnail upload control to install the exact corresponding JPEG. For Shorts, preserve the 1080 x 1920 portrait file without converting it to 16:9. Do not use `scripts/youtube/set-thumbnail.js` or YouTube's thumbnail API for these Shorts. The coverimage skill documents the Chrome Studio route.
4. Save and wait until Studio's Save button is disabled before leaving each editor. Saving can take 6 to 13 seconds. Never force navigation through a pending-save warning. Reload that editor and confirm the approved cover persists before moving to the next Short.
5. Inspect all five rows in Studio's Shorts list by eye. Studio's persisted preview is the primary verification because public thumbnail URLs can stay cached. Preserve each Short's existing visibility and schedule. This work does not authorize a new video upload or a Public upload.
6. Write an installation report beside the approved upload folder with the old-thumbnail backup paths, any available test results, upload file hashes, per-ID saved preview verification, preserved metadata, and completion time. Update this handoff and `Handoffs/README.md` after completion. Remove only this handoff's entry from `AI_COORDINATION.md`. Do not create a Victory Dashboard row unless Dan asks.

If a Studio control is unavailable or an ID points to a different video, investigate and report that specific blocker. Do not substitute another image, delete or re-upload the Short, change visibility, or claim installation without a persisted Studio preview.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260923-install-five-approved-shorts-covers.md` in the Abs By AI project and install the five exact approved JPEG covers on their existing YouTube Shorts. Dan finalized all five, including the smiling front-facing vacuum image. Verify the manifest hashes, preserve the current thumbnails and any test results, use YouTube Studio in the signed-in Chrome session, save and reload each editor to confirm, preserve video metadata and schedules, and write a per-video installation report. Do not redesign or re-upload the videos.

## Completion

All five exact approved JPEGs were installed on the existing Shorts, starting with the September 24 video. Studio Save completed for each one, each editor reload showed the cover, and all five Shorts list row previews matched by eye. Visibility remained Scheduled. Private report and old-thumbnail backups: `Short-form video content/covers/review/next-five-redesign-20260922/finalized/upload/installation-report-20260923.md`.
