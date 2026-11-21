# Muhammad dedicated Shorts (8): setup receipt, 2026-10-13

Category: CONTENT (SFC). All eight end on a comment call to action; none says tap the button. No Google Ads work, no unlisted upload. Handoff: `Handoffs/handoff-20261013-muhammad-shorts-batch2-setup-and-ads-check.md`. Task: Muhammad Shorts Batch SFC Setup (Claude, Opus 5.5).

## Release dates (9 AM Central, YouTube, Facebook, Instagram @danrosefit and TikTok together)

| Job | Title | Release | State | Cover | AI flag | Config | Master sha256 (16) |
|---|---|---|---|---|---|---|---|
| DS-12 | Top 3 Ways To Looksmax | Thu Oct 15 | QUEUED: 5547609 (FB), 5547610 (IG), 5547611 (TikTok), 5547612 (YouTube) | D | yes | `scripts/blotato/configs/ds12-top-3-ways-to-looksmax.json` | `6d8ba7e870ad2bc6` |
| DS-23 | How To Do Side Laterals | Sat Oct 17 | waiting list | C | no | `scripts/blotato/configs/ds23-how-to-do-side-laterals.json` | `1b3e9e9517452377` |
| DS-08 | I Was 200 Pounds At 38 | Tue Oct 20 | waiting list | F | yes | `scripts/blotato/configs/ds08-i-was-200-pounds-at-38.json` | `83575ea52d874723` |
| DS-09 | How To Make Time To Work Out | Thu Oct 22 | waiting list | F | yes | `scripts/blotato/configs/ds09-how-to-make-time-to-work-out.json` | `cc06dcb57d182511` |
| DS-22 | How To Use The Ab Wheel | Sat Oct 24 | waiting list | C | no | `scripts/blotato/configs/ds22-how-to-use-the-ab-wheel.json` | `75fd5b4fa1997000` |
| DS-14 | 3 Ways To Reduce Alcohol | Tue Oct 27 | waiting list | C | yes | `scripts/blotato/configs/ds14-3-ways-to-reduce-alcohol.json` | `194ad598ddf4a4b0` |
| DS-24 | How To Do Rear Delt Flys | Thu Oct 29 | waiting list | C | no | `scripts/blotato/configs/ds24-how-to-do-rear-delt-flys.json` | `9576cd368ee9acc1` |
| DS-21 | How To Do Hammer Curls | Sat Oct 31 | waiting list | C | no | `scripts/blotato/configs/ds21-how-to-do-hammer-curls.json` | `2822929e077eda03` |

- Queue was 193 of 200 before, so one Short (4 posts) was queued directly and seven are on `scripts/blotato/video_waitlist.json`, ahead of the waiting long-forms. The daily routine `social-queue-daily-refresh` queues each one on its saved date as room frees. Trial run `video_topup.py --assume-free 40` put all seven on the dates above.
- YouTube: Blotato only, `privacyStatus: public` at the slot, nothing uploaded to YouTube by us. Until the slot there is no YouTube video at all.
- Covers Dan picked 10-13: files in `Short-form video content/covers/approved-muhammad-batch/` (Instagram PNG, YouTube JPEG under 2 MB), hashes in `Short-form video content/covers/review/muhammad-batch-20261013/finals-locked.json`. TikTok gets a cover-first copy (frame 0, `videoCoverTimestamp: 0`). Facebook: eight rows added to `scripts/blotato/fb_reel_covers.json` and the live copy.
- All 32 uploaded files (master, TikTok copy, two covers per Short) were downloaded back from Blotato and matched by sha256: `/Volumes/Extreme/_edit_work/muhammad-shorts-publish/uploads.json`.
- HD proof: DS-12, 23, 08, 09, 22 re-hashed against the 10-12 record. DS-14 and DS-24 HD exports match the approved cut frame for frame (average difference 1.2 to 1.3 levels, largest pixel difference 29 to 36). DS-21 V3 HD differs from V2 only on frames 76 to 100, where the caption now reads "bracs".
- Filed: `Short-form video content/ds-NN_<slug>.mp4`, the same on `/Volumes/Extreme/Short-form video content/`, and Google Drive folder https://drive.google.com/open?id=1NqtcxGJw179vMDxPFTUpqMLeOTlPB7Lg (anyone with the link).
- Pinned comment: each config carries `pinned_comment`. Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Article: nothing written at setup for Shorts; routine sixpackabs-article-gap-daily decides after release.
- Ad guard scan: CLEAN before the moves, after the moves and after the queue write.

## Our other Shorts moved back (time only, same schedule ids, verified 48 of 48 on a fresh pull)

| Short | Title | Was | Now |
|---|---|---|---|
| sl03-short5 | Track A Week Of Meals From 1 Photo | 2026-11-03 | 2026-11-21 |
| sl03-short4 | Stop Buying Salad Dressing | 2026-10-31 | 2026-11-19 |
| sl05-short2 | Safer Lifts Build MORE Muscle Long Term | 2026-10-22 | 2026-11-10 |
| sl05-short5 | Train Legs Without Deadlifts | 2026-10-24 | 2026-11-12 |
| sl04-short4 | Stop Swinging Your Bicep Curls | 2026-10-15 | 2026-11-03 |
| sl05-short4 | 2 Back Exercises To Do Instead Of Deadlifts | 2026-10-20 | 2026-11-07 |
| sl03-short3 | Keep Your Salads Fresh For 7 Days | 2026-11-07 | 2026-11-26 |
| sl03-short6 | Make AI Calorie Tracking Accurate | 2026-11-10 | 2026-11-28 |
| sl03-short2 | The $20 Salad You Can Make For $4 | 2026-11-05 | 2026-11-24 |
| sl03-short1 | Break Your Fast With This | 2026-10-29 | 2026-11-17 |
| sl05-short3 | Deadlifts Build A Powerlifter Body, Not An Aesthetic One | 2026-10-27 | 2026-11-14 |
| sl05-short1 | Deadlifts Cause More Injuries Than Every Other Lift | 2026-10-17 | 2026-11-05 |

Backup of the queue before any change: `/Volumes/Extreme/_edit_work/muhammad-shorts-publish/blotato_queue_before_20261013.json`. Scripts: `scripts/blotato/muhammad_shorts/`.

## Still open

- DS-05: on the waiting list, see below. Once queued, set the Edit Queue row to `uploaded`.

## DS-05 Why Having Abs Beats Being A Fat Millionaire (added 2026-10-16)

**REOPENED AND HELD 2026-10-16. The setup below is superseded for release readiness.** The actual hosted master matches the October 14 V3 HD; it still contains the before photo and repeated closing title reopened by the October 16 revision instructions. F3 is a cover approval only. Fresh live read: 197 Blotato schedules, zero DS-05 matches. Neither the November 3 config date nor December 1 dry-run estimate is a live booking.

DS-05 is held in both waitlist and config. Automatic top-up skips held entries, and the organic submission guard refuses held configs. The master/edit queue is BLOCKED and its existing status file is updated. No corrected full master exists yet; rendering/full QC/independent review are pending a build slot, then Daniel must approve the exact corrected file. Preserve F3, all other entries and the date intent. Sanitized continuation: `Handoffs/handoff-20261016-ds05-correct-version.md`. Full asset provenance remains only in the private task packet. No posts, campaigns, spend or access controls were changed.


- HD export arrived 10-14 (Drive `1oS4rytE_X457rpcm-f_9nhQgBMFSHwhB`, "V3 (HD)"). Proven against the approved V3 review copy: 1,201 frames both, 50.09 s, average difference 0.93 levels, largest 32, loudness -13.6 vs -13.7 LUFS, 10.4 Mbps. Master sha256 (16) `4b0534a4283e3dca`.
- Category: CONTENT (SFC); ends "Comment and let me know...". AI flag true (opener, cliff couple, dating app clips).
- Filed: `Short-form video content/ds-05_why-having-abs-beats-being-a-fat-millionaire.mp4`, same on Extreme, and on Google Drive in the Short-form video content folder (md5 `ad9207b6...` all three).
- Cover: Dan picked F3 on 10-16 (beach road, Dan and a woman in a modest sporty two-piece, fat millionaire envious in his convertible). Review: `Short-form video content/covers/review/ds05-20261014/`, scripts `scripts/covers/ds05-20261014/`. Locked files in `covers/approved-muhammad-batch/`, hashes in `finals-locked.json`. Replicate spend about $0.19 (FLUX Kontext edits; Dan asked for Replicate).
- Blotato media uploaded and hash-checked (master, TikTok cover-first copy, both covers): `uploads.json`, script `scripts/blotato/muhammad_shorts/ds05_setup.py`. Facebook cover row in `fb_reel_covers.json` and the live copy.
- Config `scripts/blotato/configs/ds05-why-having-abs-beats-being-a-fat-millionaire.json`, keyword ABS. Queue 197/200 on 10-16, so it is last on `video_waitlist.json`; trial run puts it on Tue Dec 1, 9 AM Central.
- Pinned comment: "Under 2% of American men under 50 have six pack abs, and about 8% are millionaires. If you had to pick one, a million dollars or six pack abs?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Article: none at setup (Short); routine sixpackabs-article-gap-daily decides after release.
- Ad guard scan: CLEAN before and after.
- After each YouTube release: check the Shorts tile shows the approved cover (fix in desktop Studio if it shows a frame), per `/video-setup`.
- Release check for the seven waiting Shorts: `python3 scripts/blotato/video_topup.py --pending` should fall to the long-forms only by Oct 30.
