# Why Fat Shaming Is Good: setup receipt

Completed: November 5, 2026. Organic dedicated Short, DS-36.

## Result

**M1 approved, assets uploaded and all four platforms scheduled and read back.** Release is **Tuesday, December 22, 2026 at 9 AM America/Chicago**: `2026-12-22T09:00:00-06:00` / `2026-12-22T15:00:00.000Z`. No waitlist entry was needed. The live queue changed from 193 to 197 of 200 posts. The shared waitlist contains no DS-36 entry.

Dan's cover approval: **"Let's go with M1"**. This approves the existing Instagram and YouTube layouts from cover round2; no further visual change was made. His pick was recorded with `blind.py pick`. The initial eight covers were rejected; the four heavier mirror revisions and their request are retained privately. The simulated heavier cover is AI-modified, not a real before photograph.

| Platform | Account | Saved schedule ID | Saved UTC time |
|---|---|---|---|
| youtube | 46963 | 6530265 | 2026-12-22T15:00:00.000Z |
| facebook | 47105 | 6530261 | 2026-12-22T15:00:00.000Z |
| instagram | 67203 | 6530262 | 2026-12-22T15:00:00.000Z |
| tiktok | 58181 | 6530263 | 2026-12-22T15:00:00.000Z |

YouTube's saved title is exactly **Why Fat Shaming Is Good**. The saved YouTube target has `containsSyntheticMedia: true` and TikTok has `isAiGenerated: true`. The realistic moving scale clip in the approved film requires these flags. TikTok has `videoCoverTimestamp: 0`; Instagram has its approved M1 cover URL; Facebook's M1 cover is registered in both the source and live installer.

All scheduled captions, targets, dates and accounts were read back. Blotato changed each saved post's video URL to a separate service-owned URL; all four actual saved videos were fully downloaded and matched the expected approved master or TikTok derivative hash. The scheduled Instagram and YouTube cover URLs were also downloaded and hash-checked. No native YouTube upload or holding copy was created; the public YouTube ID exists only after release. No Google Ads work or per-video automation was created.

## Approved master and three copies

Only `Short-form video content/Fat Shaming - DS-36/Fat Shaming SFC R2 - off the cuff.mp4` was used. Dan approved this off-the-cuff R2 on November5 with "Approve as final" and then set the title. Approval: `Handoffs/video-editing/DS-36-R2-approval.json`.

- Master SHA-256: `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46`.
- 83,262,571 bytes; 59.125733 seconds; 1,772 frames; 1080x1920; 30000/1001 fps.
- SRT: `Fat Shaming SFC R2 - off the cuff.srt`, 4,436 bytes, SHA-256 `eb682397aba4fcd3cfacbfa6d3f9c49885ba7dd9e0d175c474450be978a732b5`.
- Copies verified: project delivery folder on Expansion through the existing link; `/Volumes/Extreme/Short-form video content/Fat Shaming - DS-36/`; [Google Drive backup](https://drive.google.com/drive/folders/1OKdUH5YXNDedX2Bsg4i-uonPkyAHA-Kr).
- Drive master and SRT were fully downloaded and hash-compared. Folder sharing was read back as `anyone / reader`, not searchable.
- The original picture, colour, narration, mix and burned captions remain unchanged. Existing approved-film QA evidence and its two known gate exceptions remain as recorded in the original handoff; setup did not call those exceptions passed or claim a new audible listening check.
- Organic classification was checked from the closing words: "So subscribe and go to SixPackAbs.com for all my latest videos."

## Approved M1 and TikTok copy

Approved files are in `Short-form video content/covers/approved-ds36/` with `APPROVAL.json` and `picks.json`.

- instagram: `Why Fat Shaming Is Good - M1 - instagram.png`, 2,047,374 bytes; SHA-256 `976713874b4ad8c03556f763718925ee373c50497650307efbbfc4f79d81e4f9`.
- youtube: `Why Fat Shaming Is Good - M1 - youtube.jpg`, 301,496 bytes; SHA-256 `0e1dfa9449ab6838dc2d9ffb11c3ea04da8da80bd3c85420d00a65a4d48f6b2b`.

All cover outputs were checked at1080x1920 and at profile-crop size, with no title overlap on detected face/hair. The approved YouTube JPEG is under2MB. No new image generation was needed after the pick.

TikTok's cover-first derivative is `/Volumes/Expansion/_edit_work/ds36-publish/Why Fat Shaming Is Good - M1 - TikTok cover first.mp4`: 83,424,688 bytes, SHA-256 `cc31208de9cbc84ebae57f223b5fc54aa15387e392f236822f608ead7794b56f`. It has1,773 frames versus the master's1,772, with the same2,772 audio packets. A full decode reported no errors; frame-zero similarity to M1 was 49.36dB. Frame zero was visually inspected. The copied audio payload hash is `96f82fa85fb234e8acf5781335bb04d16732847ca710c7fa5f80d21dc7b6c8c1` for both files. The master was not re-encoded.

## Metadata

Config: `scripts/blotato/configs/ds36-why-fat-shaming-is-good.json`.

- Title: **Why Fat Shaming Is Good**.
- Keyword field: `TRACK` (scale/mirror/progress topic). Captions use the filmed SixPackAbs.com invitation; no automatic free-preview CTA was inserted.
- Hashtags: `#FatLoss #WeightLoss #BillMaher #Shorts`.
- Organic destination: SixPackAbs.com root, with `utm_source` per platform, `utm_medium=short`, `utm_campaign=fat-shaming`, `utm_content=ds36-why-fat-shaming-is-good`.
- AI setting: `ai_generated: true`.
- Captions are burned in; no duplicate generated captions requested.
- Pinned comment: **"Do you weigh yourself every morning?"**. Posts and pins automatically after release through the existing `youtube-pinned-comment-daily` routine. It has not been posted now.
- Article: shared Short article/skip workflow after release through `sixpackabs-article-gap-daily`; no long-form article is required at setup.
- Writing method: the normal clean Claude CLI helper could not refresh its OAuth session. A clean Codex writing pass used the same five real bank passages, Dan's filmed wording and content plan. Hard writing checks passed. No authentication or credentials were changed.

Final caption:

Bill Maher is right. Fat shaming can be good. But fat shaming other people is cruel and there's no point to doing it. Instead, use your own shame as motivation.

Weigh yourself every morning. If you're more than three pounds above your goal weight, get back on track with your diet and workouts. Feel that shame when you're only a little over your goal, rather than 20 or 30 pounds over. Feel it, then fix it. Don't stay ashamed forever and do nothing.

So subscribe and go to SixPackAbs.com for all my latest videos.

YouTube also includes the root link/UTMs, a short AI-footage disclosure, and the Bill Maher / Real Time (HBO), "New Rule: The Fudge Report" source credit.

## Hosted assets and actual saved media

The four original uploads below were fully downloaded and checked by byte count and SHA-256 before scheduling.

| Asset | Bytes | SHA-256 | Uploaded URL |
|---|---:|---|---|
| master | 83262571 | `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46` | https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/fa924822-ca62-489e-9f5f-e10b91a308d1.mp4 |
| instagram | 2047374 | `976713874b4ad8c03556f763718925ee373c50497650307efbbfc4f79d81e4f9` | https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/bb6ed167-07a4-4a7a-ba3c-fa3b85db368a.png |
| youtube | 301496 | `0e1dfa9449ab6838dc2d9ffb11c3ea04da8da80bd3c85420d00a65a4d48f6b2b` | https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/ce8a109a-50b5-4bee-abc3-f2f934b9ef03.jpg |
| tiktok | 83424688 | `cc31208de9cbc84ebae57f223b5fc54aa15387e392f236822f608ead7794b56f` | https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/36bfc4dd-ac0c-4a97-9549-86ee87c86718.mp4 |

Actual saved post video URLs, separately downloaded and verified after Blotato copied them:

- facebook schedule 6530261: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/e71d6efb-73ec-4d7e-831e-27863a254ad9.mp4; SHA-256 `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46`.
- instagram schedule 6530262: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/994c3fec-5f95-4b42-8254-3abb6cb27800.mp4; SHA-256 `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46`.
- tiktok schedule 6530263: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/d88e62dd-5cce-47f4-8f9b-788110f8adce.mp4; SHA-256 `cc31208de9cbc84ebae57f223b5fc54aa15387e392f236822f608ead7794b56f`.
- youtube schedule 6530265: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/0c834205-86b0-45cf-9523-9aa08bedfe0f.mp4; SHA-256 `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46`.

## Audits, queue and release follow-through

Preflight:193 scheduled posts, no target-slot clash and no DS-36 waitlist entry. Ad audit was clean and cover audit had zero issues. After queueing:197 scheduled posts, ad audit clean and cover audit zero issues. Config ad guard and every per-platform cover guard passed.

The edit-queue job is `uploaded`, rev7. Its Google Drive status file was read back with the M1 approval and all four schedule references. Codex's documented Drive route updates the pinned queue page; native Claude artifact-database mirroring remains for the next Claude sync, as the skill prescribes.

The Shorts calendar row now names Why Fat Shaming Is Good and is booked. The setup handoff is complete and removed from the open index. There is no remaining action for Dan.

Public covers are a release-time check, not proved by a queued URL. The existing shared cover monitor must inspect all four actual public tiles after release; if YouTube uses an automatic frame, repair its public portrait thumbnail in Studio from the approved M1 YouTube JPEG, without deleting the video. Facebook's existing installer applies M1 after publication. The pinned-comment and Short-article routines handle their existing release work. No separate routine was added.

Private evidence: `Short-form video content/covers/review/ds36-20261105/setup/`, approved cover folder above, and `/Volumes/Expansion/_edit_work/ds36-publish/`. This includes API readbacks, full saved-media verification, before/after audits, the clean metadata draft, the exact pick and TikTok measurements.
