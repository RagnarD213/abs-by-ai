# Install the finalized Instagram covers and YouTube thumbnails

Prepared 2026-09-28 for a new Claude task. Recommended model: Claude Opus 5.5, high effort.

## Goal, final decision and authorization

Install the exact finalized cover selections on their matching Instagram and YouTube destinations. Dan's final instruction: "I like the more ripped R5. Let's go with that and lock that in. Everything is finalized. Create a handoff document for Claude to install all of these in a new task."

All design decisions are final. Instagram row 16 is the stronger R5. Keep its exact title `2-minute home arm workout` and layout. All previous approvals remain locked, including the original horizontal YouTube row 16. Do not regenerate, redesign, retouch, change copy, start a thumbnail test or offer another selection round.

This handoff-writing task changed approval records only. No installed cover, publishing account, queue or schedule was changed. Dan launches the next Claude task using the starter prompt below to execute installation. Routine installation of the approved selections is authorized; do not ask again for design approval or routine thumbnail replacement.

## Read first

- `AGENTS.md`, `CLAUDE.md` and `AI_COORDINATION.md`.
- `.claude/skills/_shared/VIDEO-RULES.md` in full.
- `.claude/skills/coverimage/SKILL.md` for platform installation mechanics. Its new-design and two-variant steps do not apply to this finalized batch.
- `Docs/QUEUE_COVERS_FINAL_20260928.json`, the sole final approval authority. It supersedes `Docs/QUEUE_COVERS_APPROVALS_20260928.json`, which remains untouched as history.

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`

Shared media root, including when running in a worktree:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/queue-bakeoff-20260924/`

Do not resolve media paths against a worktree. These photos and recipes are Git ignored and live in the shared checkout.

## Exact finalized assets

The final JSON contains 31 approved replacement exports and four protected originals, all 35 SHA-256 hashes verified on 2026-09-28. Export count is not the count of account writes. Some rows contain platform companions for the same content; avoid replacing the same destination twice.

| Review rows | Final selection | Folder beneath shared media root |
|---|---|---|
| 04-11, 15, 17-19 | A, separate Instagram and YouTube files | `round3-platform-layouts-20260925-fbd1/covers/` |
| 12-14 | R4 A, separate Instagram and YouTube files | `round4-unfinished-20260926/covers/` |
| 16 Instagram | Stronger R5, approved 2026-09-28 | `round5-row16-retouch-20260928/covers/16-more-ripped-instagram.jpg` |
| 01-03 | Keep original, no replacement | `baselines/blotato-01.jpg`, `blotato-02.jpg`, `blotato-03.jpg` |
| 16 YouTube | Keep original horizontal thumbnail | `baselines/youtube-01.jpg` |

For the first two groups, filenames are `<row>-A-instagram.jpg` and `<row>-A-youtube.jpg`, with two-digit row numbers. The final JSON has every absolute path and exact checksum. All replacement exports are 1080 x 1920 RGB JPEGs. Never use a grid-crop preview as an upload. Do not convert YouTube Shorts covers to 16:9.

Instagram 16 approved cover SHA-256:

`3103f7d401776211ecc522ec9a7d5f6d5ab8b401532d9f46504ccb61170e1d4a`

YouTube 16 protected original SHA-256:

`45bf3d5746753d472513c3ce7cbc9313b7e5e1a5e8c9776a9b23cab9aac56644`

Do not install the older R4 Instagram 16 or any rejected earlier variation. Spiderman Planks is row 10-A, not row 9-A.

The R5 manifest, prompt, generation record and verification remain in `round5-row16-retouch-20260928/`. Its review is `http://127.0.0.1:8795/index.html#row-16`. Review-server availability is not required to install the files. The built-in R5 edit's separate dollar charge was unreported, not zero. No further generation is needed.

## Destination map and duplicate-content rules

Review row numbers refer to this gallery, not production numbering. The following IDs are historical matching leads. Refresh account state before writing. `baselines/inventory.json` and `live-queue-check.json` are September 23/24 snapshots, not a current queue.

| Row | Subject | Historical destination leads |
|---|---|---|
| 01 | Skip breakfast | Blotato `3876744`, keep original |
| 02 | Belly fat emergency | Blotato `4578150`, keep original |
| 03 | Arm workout before photo shoots | Blotato `4722757`, `4722761`, keep original |
| 04 | Deadlift trick | Blotato `4066393`, `4066405` |
| 05 | Towel back move | Blotato `3793992`, `3794055` |
| 06 | Three minutes | Blotato `4066416`, `4066422` |
| 07 | Four ab muscles | Blotato `3793994`, `3794057` |
| 08 | Toe touches | Blotato `3793995`, `3794058` |
| 09 | V-sit twists | Blotato `3793997`, `3794060` |
| 10 | Spiderman planks | Blotato `3793998`, `3794061` |
| 11 | Why I love the ab wheel | Blotato `4315883`, `4315885` |
| 12 | Biggest ab wheel mistake | Blotato `4315887`, `4315890` |
| 13 | How to do ab wheel rollouts | Blotato `4315893`, `4315895` |
| 14 | Ab wheel workout tip | Blotato `4315898`, `4315901` |
| 15 | Ab wheel versus crunches | Blotato `4315903`, `4315906` |
| 16 | Home arm workout long-form | YouTube `QHWOoWbgWcY` stays unchanged; R5 is for its confirmed Instagram counterpart |
| 17 | Deadlift trick, YouTube Short | `D9v9POAKe_Q`, use row 17 YouTube export |
| 18 | Towel back move, YouTube Short | `qH9YRoH2PpM`, use row 18 YouTube export |
| 19 | Three minutes, YouTube Short | `1k518M3EKps`, use row 19 YouTube export |

Machine-readable matching evidence is preserved at `final-installation-20260928/destination-hints.json` under the shared media root. It includes every approved path/hash, historical account/date/post record, protected original and absolute finished-video source. `sources/video-frames.json` also maps rows to finished exports.

For rows 04/17, 05/18 and 06/19, the finished video is the same, but the gallery contains separate approved designs. Apply row 04-06 Instagram exports to their original Instagram queue records. Apply row 17-19 YouTube exports to the three exact YouTube IDs above. Do not overwrite those YouTube IDs with row 04-06 companion exports afterward. Preserve the unused approved companions for their correctly matched future destinations. If an unlisted companion has no distinct destination, record that rather than forcing an extra write.

Rows 03 and 16 share the same long-form source. Row 03's existing queue records are explicitly protected; row 16's approved R5 targets the Instagram counterpart associated with the row 16 selection. Find a distinct intended Instagram post from live records and source/media evidence. If the only candidate is a protected row 03 post, this is a real routing conflict: finish all independent installations, preserve row 03, then report the exact post/account/URL for one destination decision. Do not silently replace a protected original or duplicate the post.

Find matching YouTube Shorts for rows 07-15 through the current upload plan, Studio and exact finished-video source. Record confirmed IDs before changing thumbnails. Use caption, source, campaign and account together when matching mirrors, not a generic phrase such as "ab wheel." The excluded five Shorts are `tqURi3qdrIc`, `_Ep_hVPZYzE`, `o1v3wPkNI2I`, `QuswpGj635A`, `bi_fpkW-3eE`; they have separate installation work and remain untouched.

## Installation procedure

1. Claim the installation entry on the board. Verify all 35 final hashes before any external write. Preserve the final JSON and all approved assets. Save evidence in `final-installation-20260928/installation/` beneath the shared media root.
2. Fetch fresh Instagram/Blotato schedules and YouTube/Studio details. Back up full records and current cover images, including captions, video media URLs, first comments, accounts, target options, dates, visibility and thumbnail-test results. Build a per-destination plan mapping one exact approved file to one confirmed post/video. Separate replacements, protected originals, unused companions and genuine routing conflicts.
3. Install Instagram exports on matching scheduled Instagram records, including both `danrosefit` and `abs.by.ai` mirrors where confirmed. Use supported cover editing and preserve all unrelated fields. Inspect current API/connector behavior first. A cover JPG goes in the cover field, never in the post's video `mediaUrls`. `scripts/blotato/danrosefit_migration.py` has existing read helpers. `swap_media.py` changes video media and deletes first; do not feed cover JPGs to it or blindly use it for this task.
4. If a supported queue edit requires recreating a scheduled record, save the full original and prefer create, verify, then remove old. Preserve the exact saved UTC timestamp, including November's daylight-saving shift. Preflight capacity. If deleting an existing record first is the only possible route and requires approval, prepare the complete batch and ask once with its count, not once per item. Never leave an unverified replacement or orphan duplicate. Re-fetch after apparent read lag before deciding a create failed.
5. For already-published Instagram posts, use the mobile cover-edit path where available, with the exact approved full cover and literal grid composition. Do not delete/repost a published video to install its cover. If mobile access is unavailable, record the exact remaining post and phone action. A historical missing schedule does not establish publication; check the actual account.
6. For YouTube Shorts, upload the exact 1080 x 1920 YouTube file through Studio's thumbnail file input using the skill's current supported browser workflow. Preserve any available test results before replacing an old thumbnail/test. Confirm Save completes and the button becomes disabled before leaving. The generic `scripts/youtube/set-thumbnail.js` is useful for read-only evidence, but does not reliably install a portrait Shorts shelf cover; do not claim success from a wide API preview. Verify Studio and the actual Shorts/channel tile. Do not reject a correct saved cover only because an old `oardefault.jpg` is CDN cached.
7. YouTube `QHWOoWbgWcY` retains its existing horizontal thumbnail. Do not upload the R5 Instagram portrait to it. Existing public/private/unlisted visibility, title, description and schedule stay as read. This task uploads cover images only, not new video media, and does not use YouTube native publishing/scheduling.
8. Re-read every changed record, compare its actual cover visually against the exact approved design, and prove unrelated fields unchanged. Recheck all four protected originals and all 35 local hashes. For transformed/recompressed platform images, visual composition is the authority; raw byte equality is not expected. Run `python3 scripts/blotato/ad_guard.py --scan` before and after queue writes and use the existing guarded queue workflows.
9. Write `installation/INSTALLATION_REPORT.md` and a machine-readable result list with each row, platform, account, confirmed destination ID, approved file/hash, old/new evidence, verification result, unchanged metadata, replacement schedule IDs, rollback location and any remaining limitation. No unsupported destination is marked complete. Keep photos out of Git. If uploading evidence to Drive, follow the current project rule: anyone with the link can view, except sensitive documents.
10. Update relevant local cover references used by future queues only for the verified destinations. Commit and push task records and any needed script/config changes, preserving other sessions' work. Verify Railway's success or legitimate documentation-only skip and the live app if a deployment occurs. Remove the installation entry and the open handoff row once delivered and approved. Do not create a dashboard task automatically or resume the paused editing dispatcher.

Facebook/TikTok media changes, new posts, revised videos, new schedules, customer communications and unrelated cover projects are outside this approved Instagram/YouTube installation. Do not start generation or charge user credits. Complete every supported destination and report concrete remaining access or routing issues.

## Ready-to-paste starter prompt

> Execute `Handoffs/handoff-20260928-install-finalized-queue-covers-claude.md` in the Abs By AI project. Install all finalized Instagram covers and YouTube Shorts thumbnails using `Docs/QUEUE_COVERS_FINAL_20260928.json`. Instagram 16 is the stronger R5; its original horizontal YouTube thumbnail and rows 01-03 stay unchanged. All selections are final. Match exact destinations, preserve metadata and schedules, verify every saved cover, and deliver the installation report. Resolve independent work before reporting any genuine access or destination conflict. Do not redesign or generate more options.
