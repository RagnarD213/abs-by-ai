AD: Ad 13, The Cost Of Getting Abs, approved round 4 upload and Google Ads replacement.

# Approved setup handoff, 2026-10-05

Recommended model: GPT-6.1 Sol, High.
Session name: The Cost Of Getting Abs S/Sh Ad Setup.
Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
All relative paths below are relative to that root.

## Daniel's decision and scope

Daniel approved all three exact round 4 exports on 2026-10-05 and authorized their upload and Google Ads setup. His words:

> Okay everything is approved and ready for upload. Give me the handoff document for Codex to set these videos up, make the thumbnails, and then add them to Google Ads. I want this horizontal to replace the existing horizontal within Google Ads or whatever existing one we have there. I want this one to replace it

Approval is recorded against the three hashes in `Handoffs/ad13-round4-approval-20261005.json` and the filed recipe's `decisions.json`. No new video approval is needed. This task writes the handoff only; the uploads and ad replacement have not been executed.

This handoff supersedes `Handoffs/handoff-20261004-ad13-round4-setup-codex.md`. Its instruction to leave the old horizontal running is revoked by Daniel's explicit replacement request. The earlier vertical setup handoff supplies background only, not authority to preserve the old horizontal.

The result must be three approved round 4 YouTube uploads: horizontal full, square full and square short. Add the two squares to the existing Ad 13 trial group. Replace existing paid uses of the Ad 13 horizontal with the approved new horizontal, rather than leaving the old horizontal running alongside it. Preserve the already uploaded verticals and their ads.

## Read before executing

- `AGENTS.md` and `.claude/skills/_shared/VIDEO-RULES.md` in full.
- `.claude/skills/ad-setup/SKILL.md`, using the current trial campaign and locked thumbnail selection below where older examples differ.
- `Docs/AD_VIDEO_IDS.md`.
- `Docs/DGEN_CONVERSION_CAMPAIGN.md`, especially the 2026-10-01 trial campaign, conversion remarketing, Performance Max and 2026-10-04 Ad 13 setup sections.
- `Docs/AD13_VERTICAL_SETUP_RECEIPT_20261004.md` and `scripts/ads/api/dgen-ad13-vertical.js` for the verified existing-group setup method.
- `Handoffs/ad13-round4-approval-20261005.json`.
- The ad folder's `recipe-codex-round4/delivery_manifest.json`, `ROUND-4-FINAL-REVIEW.md` and `final_verdicts.json`.
- `AI_COORDINATION.md` for current ownership. The Victory Dashboard is paused as of 2026-10-05: skip all dashboard reads and writes.

## Exact approved upload masters

Ad folder:
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/`

Use these original files in that folder. Do not upload the review proxies, comparison clips, superseded renders or Downloads aliases. Do not edit, re-encode, trim, pad or remux the approved movies.

| Filename | Runtime / size | SHA-256 |
| --- | --- | --- |
| `i added up what getting abs was supposed to cost \| codex \| 16x9 \| ad 13.mp4` | 244.877967 s, 1920x1080 | `e7b5ff4597c10539d25d737806056a2c209b5c02899b54419cff50a242ce1ed3` |
| `i added up what getting abs was supposed to cost \| codex \| 1x1 \| ad 13.mp4` | 244.877967 s, 1080x1080 | `43fe4f707ac41759fd94c6353289396cce967b1e97d30560df373a6c9c2d45f1` |
| `i added up what getting abs was supposed to cost \| codex \| 1x1 59s \| ad 13.mp4` | 54.287567 s, 1080x1080 | `d59a126976bb12ec25e8ff6c12520bcf32dbfd4b6d99c9162859efa736f51c12` |

The 59s filename means the approved short variant. Its actual runtime is 54.29 seconds; do not extend it. Each movie has a matching `.mp4.deliver_gate.json`, PASS with 39 passing rows, plus audio evidence and completed judging and independent review. On 2026-10-05 the original files were rehashed and matched the approval. Rehash again before upload and verify matching PASS stamps. A hash mismatch requires locating the approved original, not inferring approval for a different movie.

## Thumbnails: finish the approved design in the required formats

The design is already selected: Ad 13 **13-R3B**, with the words **HUMAN TRAINERS HATE THIS AI**. This is format adaptation of the locked selection, not a new thumbnail choice round. Preserve its real Dan photo, original mask, repaired robot background, typography, yellow accent and wording. Do not reopen the approved choice or default to five new designs.

- Reuse the approved horizontal final:
  `social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/Ad 13 | 16x9 | FINAL.jpg`.
- Build one matching 1080x1080 square final and use it for both square uploads. Start from the existing layered builders, not a flattened crop that cuts Dan or the words.
- Sources: `scripts/covers/trial-campaign-20261001/round3/build.py`, `scripts/covers/trial-campaign-20261001/ad13-vertical/build.py` and the corresponding approved finals. The vertical receipt documents photo-10 and its original mask.
- Visually inspect the square at native size and phone size. Keep text clear of face and hair, retain complete wording, and follow the standing thumbnail rules. Save the reproducible build and final in the existing Ad 13 thumbnail folder and copy the new final into `social media graphics/youtube/thumbnails/_trial-campaign-20261001/FINAL APPROVED/`.
- Use the Codex subscription to generate the images. That instruction applies if generation is actually needed; reuse the already approved assets first. Never redraw the real photograph of Dan or use a paid image API.

## YouTube setup

1. Verify classification from the finished closing transcript and record its exact words. These are ads with the button CTA.
2. Upload the three exact originals to channel `UC236gjadarHAhEhOMYNGJ9g`, **Unlisted**, embeddable, not made for kids, synthetic media **true** because the films include realistic AI footage. No Public upload, native scheduling or organic posting.
3. Use recognizable Ad 13 titles with format/version suffixes. Reuse the current verified Ad 13 description and topic tags from the vertical setup, preserving the current /start trial offer. Do not revive the old free-preview description template.
4. Reuse appropriate master chapters for both full films. Every chapter, including the final one, must meet YouTube's minimum duration. The 54-second short gets no chapters.
5. Install the approved horizontal thumbnail and matching square thumbnail. Read back channel, privacy, synthetic setting where available, processing success and embedding. Fetch the served thumbnails and visually inspect them.
6. Save upload IDs and receipts as each operation finishes. Before retrying an uncertain upload, inspect the channel and logs to recover an existing upload instead of creating a duplicate. Reuse a verified upload if another setup task has already completed it.

## Google Ads: replacement, not an extra old horizontal

### Inventory first

Primary target: trial campaign `24316364155`, existing Ad 13 group `204553316830`. Known old horizontal ad: `826635661894`, using YouTube `-SuKGXGcbIg`. Read current live state; these IDs are starting points, not proof of today's state.

Inventory **all current Google Ads references to the existing Ad 13 horizontal** across the account, including ad-level video assets and Performance Max asset-group bindings. The campaign records identify older Demand Gen horizontal ads `825601774244` and `825601774247` and a Performance Max use of Ad 13; verify their actual current status and video references. Include the conversion remarketing copies of this same horizontal if present. Do not replace another video's asset merely because its name is similar.

Daniel's replacement authorization covers the existing Ad 13 horizontal wherever it is currently used for paid ads. This supersedes the old handoff's blanket restriction on changing older Demand Gen or Performance Max for this specific replacement. Everything else in those campaigns stays as found.

### Execute the replacement and square additions

- Read the live Ad 13 copy, logo, business name, CTA, URLs and settings. Clone them unchanged for the replacement. Do not use stale copy from a historical config. Preserve landing pages and campaign tracking conventions; use an appropriate new version identifier in `utm_content` where needed.
- Create or reuse a YouTube video asset for the new approved horizontal. If Google's format does not permit replacing the video in an existing ad, create a replacement ad in the **same group**, verify it, then pause the old horizontal ad. Do not delete the old ad or its history.
- For a currently enabled old ad, enable the verified replacement and pause the old one. Prefer an atomic validated cutover where supported. For a paused old ad that remains configured, keep its replacement paused. Never enable a paused campaign or group.
- For Performance Max, replace only the old Ad 13 video binding with the new one in each matching asset group. Retain every other video and asset, preserving the original asset count and campaign settings. Do not merely add a sixth video or leave both Ad 13 versions attached.
- Validate mutations before applying. Read back the new video references, replacement statuses and old-ad PAUSED states. After cutover, the old horizontal must have no enabled paid-ad use remaining. Preserve its Unlisted YouTube upload; there is no request to delete it.
- Add the square full and square short as separate ads in existing trial group `204553316830`, cloning current Ad 13 copy and settings. Follow `/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad13&utm_content=<version>-vsl`, with distinct `codex-1x1` and `codex-1x1-59s` version values.
- Do not expand these new squares or the existing verticals into additional live remarketing groups as part of this task. The previous vertical task left that separate expansion decision open. Replacing an existing horizontal reference is authorized; adding extra formats outside the trial group is a different action.
- Re-read campaign and remarketing states instead of relying on old PAUSED notes. The 2026-10-04 receipt found conversion remarketing `24305381214` and subscriber remarketing `24316408288` already enabled. Avoid the broad remarketing sync script, which can add unrelated formats and ads. Subscriber remarketing uses organic videos, not trial-ad copies.
- Preserve budgets, bids, audiences, campaign/group states and every unrelated ad. Preserve existing Ad 13 vertical videos `f792V7H1Vkc` and `VPyHyxEkHjo`, and trial ads `826888334290` and `826888304284`.

Read policy status after applying and report pending review honestly. If Google rejects a replacement operation, keep the working old ad intact and record the exact unresolved reference. Do not call replacement complete while an old enabled horizontal reference remains. Do not rewrite video or ad copy without a separately identified need.

## Records and completion

Write `Docs/AD13_ROUND4_SETUP_RECEIPT_20261005.md` with:
- Three new YouTube IDs, exact upload hashes, thumbnail paths/hashes and served-thumbnail evidence.
- Each old horizontal reference and its replacement, by campaign, group/ad or asset-group binding.
- Before/after status, preserved budget/settings evidence, validation and mutation readbacks, policy status, and any unfinished replacement.
- The two square ad IDs and video assets, and confirmation that the existing verticals were preserved.

Update `Docs/AD_VIDEO_IDS.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md` from verified results. Mark AS-10 finalized from this approval, then uploaded only once the uploads and ads are verified, following the edit-queue instructions. Keep queue synchronization separate from media upload receipts. Skip the paused Victory Dashboard.

Commit and push only this task's scripts/configs/records under the current project Git rules. Do not include unrelated edits. Report the three video links, show the finished thumbnails, list replaced old ads/assets and any pending Google review, and state the preserved budget. Do not claim any operation succeeded without readback.

## Ready-to-paste starter prompt

AD. Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20261005-ad13-approved-upload-and-replace-horizontal-codex.md` and the files it lists. Name this session "The Cost Of Getting Abs S/Sh Ad Setup". Daniel approved all three exact round 4 exports and authorized upload and replacement on 2026-10-05. Finish the matching approved 13-R3B thumbnails, upload the three originals to YouTube Unlisted, add the square full and short to the existing Ad 13 trial group, and replace the existing Ad 13 horizontal wherever it is currently used in Google Ads. Verify the replacement and pause old horizontal ads, preserving campaign states, budgets, other ads and the approved verticals. Use the Codex subscription to generate the images. Skip the paused Victory Dashboard. No organic posting. No em dashes.
