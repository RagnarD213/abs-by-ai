# Dr Mike Dial SFC setup receipt

Updated: 2026-11-04. Owner: Codex chat `01a1a3d0-06e8-7cb3-9174-4cc21117cf77`.

**Setup complete, uploaded and shared-waitlisted. Not yet scheduled or released.** The exact approved R4 film and revised B covers are installed and verified. The live queue is full at 200/200; one existing shared waiting-list entry covers YouTube, Facebook, Instagram @danrosefit and TikTok. Target **Monday, January 4, 2027, 6 PM America/Chicago** (`2027-01-05T00:00:00.000Z`). No actual publisher schedule IDs exist. The existing `social-queue-daily-refresh` / `scripts/blotato/video_topup.py` schedules the four destinations when capacity opens, keeping this slot while available. No per-video automation, native YouTube holding upload, post removal or unrelated schedule change.

## Exact approvals

Film: Dan approved R4 on November 3: “Okay this looks good. Proceed to setup”. Exact shortened off-the-cuff film, already 5% faster with pitch preserved. Do not apply speed again.

Cover: Dan approved the exact round3 revised B files on November 4: “Looks good. Approve revised B and finish setup on all platforms.” B’s real pointing reaction above C’s full original Dr. Mike image, with tighter headroom and more body. Headline: **Tirzepatide Is An Appetite Dial**. Initial X1-X8 rejected; round2 B was selected with a revision. No invented blind-model pick was logged for this all-real replacement.

Approval record: `Short-form video content/covers/approved-ds37/picks.json`, with identical project-delivery and Extreme approved-cover copies. Native source provenance and review hashes remain in the cover work folder.

## Four uploaded assets, fully downloaded and verified

| Asset | Bytes | SHA-256 |
|---|---:|---|
| video | 76,144,088 | `92431f246bc27b03e0dd4fbc408062aa1b6fa65d134ffed564f940adc390ad41` |
| tiktok | 76,253,268 | `e806ac174599a4cb0656da0dd41efe9dc8124ac98093bc2c53193c5d48a98306` |
| instagram | 383,790 | `341853a32ceb4ddc8d4141c229c9be30163a204f8f6effc561530043579f7420` |
| youtube | 466,230 | `be1a4a00952d3689ad1d2fe398e705cb2ca317ead9e6c4abc68183ef7be275d6` |

All four Blotato staging uploads were downloaded in full and matched local bytes and SHA-256. Both cover downloads decoded as 1080x1920 RGB; the YouTube JPEG is 466,230 bytes, under 2 MB. Staging uploads are not public platform releases.

- [video verified staging asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/342447ae-ec1e-45da-b473-f44f0762716e.mp4)
- [tiktok verified staging asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/cfa535e1-4f10-458b-970c-255ca2589c17.mp4)
- [instagram verified staging asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/bcc4b497-bf08-4a62-bba8-b4a893c56153.jpg)
- [youtube verified staging asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/fb0402de-d5b0-41fa-8275-c457b71fb029.jpg)

TikTok: one approved Instagram-cover frame prepended, 1778 to 1779 frames; 2783 original AAC packet payloads compared and identical, zero decode errors, frame-zero cover PSNR 50.30 dB. The actual uploaded derivative was downloaded, its actual first frame extracted and visually checked against revised B. `videoCoverTimestamp: 0` is in its saved target. No re-encoding or processing of the original audio or approved film.

## Platform package and actual queue state

| Destination | Account | Media | Cover | State |
|---|---|---|---|---|
| YouTube | 46963 | Exact R4 master | Approved YouTube layout | Shared waitlist |
| Facebook | 47105 / page1294282227094660 | Exact R4 master | Approved Instagram layout, repo and live installer registered | Shared waitlist |
| Instagram @danrosefit | 67203 | Exact R4 master | Approved Instagram layout | Shared waitlist |
| TikTok | 58181 | Verified cover-first derivative | Actual approved first frame, timestamp0 | Shared waitlist |

Config: `scripts/blotato/configs/ds37-dr-mike-dial.json`. Exactly one DS-37 entry in `scripts/blotato/video_waitlist.json`; current list index78, active waiting entries59. Dated Shorts calendar cell January4 at6PM is marked Waitlist. Latest live read:200 posts,0 DS-37 schedules. Four saved targets independently passed the shared cover/ad guards. Direct queue dry run refused only the full cap (200+4=204). Shared top-up dry run confirmed no capacity and created nothing.

The last collision check found DS-16 had reserved January2 at6PM during this setup’s uploads; DS-37 then took the next eligible unoccupied slot, January4 at6PM. The December10 approved5PM exception was counted as that day’s evening Short, preventing an unintended third Short. No other reservation was overwritten.

Facebook: `scripts/blotato/fb_reel_covers.json` and `~/.absbyai/fb-reel-covers/fb_reel_covers.json` both contain the exact first caption line and identical approved image hashes. Repository image: `scripts/blotato/fb_covers/ds37-dr-mike-dial-approved-B-revised.jpg`. The existing installer handles application and verification after release.

## Metadata and release follow-through

Title: **Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right.**

Pinned comment: “When you're losing weight, which is harder for you to deal with, hunger or food noise?” Written in config; existing `youtube-pinned-comment-daily` posts and pins after release. No comment posted before a public video exists.

Title, description, social captions, topic tags, pinned question, keywordFOOD and platform targets are saved. Organic links use the AbsByAI.com root with platform/short/campaign/content UTM values, never /start. Captions preserve the filmed SixPackAbs.com close. No free AI-preview offer was added. Real source-video/real camera footage: synthetic flags false; burned captions preserved with their exact SRT sidecar. YouTube post-release tags/captions and actual public covers remain with existing shared release checks.

Copy method: clean writer call with five real Dan passages and the actual filmed transcript. Existing Claude CLI authentication failed; the documented clean-prompt fallback produced the copy. Hard rules passed, no polish pass, no paid API. Receipt: `scripts/covers/ds37-20261103/setup/writer-receipt.json`.

Article: dedicated Short. No long-form article is required at setup; existing `sixpackabs-article-gap-daily` handles a suitable Short article or recorded skip after release.

After the shared routine creates schedules, read actual saved times, captions, targets and media. Blotato may rewrite media URLs: compare actual downloaded bytes/hashes, not URL strings, before reporting a wrong master or recreating anything. Public tile checks remain with the existing four-platform cover monitor; supplied URLs alone do not prove public cover success.

## Backups and quality limits

Project master/SRT and Extreme copies freshly full-hash-checked November4; existing [Drive master/SRT backup](https://drive.google.com/open?id=1nczhx7nkGY01ThHWi5ANg149r5W_tBYI) independently read for current server bytes/MD5/SHA-256, all matching. This is fresh cloud metadata verification, not a new full Drive-media download. No duplicate backup upload. Shared Drive folder remains master/SRT only. Exact covers, setup metadata and the TikTok derivative also have verified project/Extreme copies.

Master:76,144,088bytes; picture59.325933s, container59.339s,1080x1920,1778frames,30000/1001fps. SRT SHA-256 `c41d0a4ea9837baf2d79e70ffa77920e18d1de6ffbba2dc0bec2bfdabdc8ff0e`. Approved-film raw gate remains35PASS/4FAIL/4N/A/0pending with four independently adjudicated detector mismatches. Approval does not rewrite that evidence. No film repair or new film render. Setup checks used silent offline decoding and images; no audible human listening pass claimed.

Final checks: ad-guard clean across200 schedules before/after; cover audit zero issues before/after; all four new saved targets pass their own guards; actual uploaded TikTok first frame inspected. Source master and all approvals preserved. No image generation or paid generation in the approved-cover/setup phase.

Evidence: `/Volumes/Expansion/_edit_work/DS-37-publish/` (`uploads.json`, individual upload receipts, TikTok/audio verification, actual uploaded-frame image, planned targets, preflight, waitlist receipt, live before/after queue snapshots and final backup receipt).

Edit Queue stays **finalized** until all four actual schedules exist and read back. Its new setup/waitlist note was pushed successfully to the Drive status file. Native ArtifactDB mirror is unavailable to Codex; no mirror success is claimed and syncedRev remains pending. The setup handoff is executed and removed from OPEN.

Repository: owned records committed locally in `e7ba24a`; every unrelated staged item was preserved. Safe-push stopped before merge/push on six live shared files, including the separately staged salad article deletion. No unrelated changes were adopted or pushed. Local setup, uploads, calendar and waiting list remain saved and operational. Final formatting/receipt follow-up also stays local until this same shared-workspace blocker clears.
