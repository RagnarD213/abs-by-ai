# Zeeshan's five-video batch: set up Video 5, confirm Videos 1 to 4, archive all five

**CONTENT, long-form family (LFC).** All five are organic YouTube content videos, not ads. Only Shorts are ever derived from them
(`/shorts`): no vertical, square or 1-minute version.

**Written 2026-10-10 by Claude.** Dan approved the last video of the batch (Video 5) on 10-10 and asked for one handoff that sets
the batch up in Blotato on all platforms and stores the files on the Seagate and on Google Drive.
**Model:** Claude Sonnet 5.5, effort medium (mechanical setup per `model-routing-plan`; Opus high only if Dan rejects the title or
description copy).
**Sidebar name:** `Abs At 40 vs 25 LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State of the batch (checked 10-10)

Every file below is Zeeshan's latest revision in his Drive folder, byte size matched to Drive, and measured 1920x1080 h264 at about
10 Mbps. Nothing accepted as a final is below 1080p. All are in `Zeeshan Content Videos/` in the project folder.

| # | Video | His file | Local final (size) | Release state on 10-10 |
|---|---|---|---|---|
| 1 | Ab Wheel Workout | `Video 1 Rev 2.mp4` | `ab wheel workout - video 1/` (300,660,846) | Public since 09-20, YouTube `b_bS9NdmL-g` |
| 2 | Arms And Shoulders Home Workout | `Video2 Rev 3.mp4` | `arms and shoulders home workout - video 2/` (858,396,944) | Set up 09-22, released Sep 27 |
| 3 | Stop Deadlifting | `Video 3 Rev 5.mp4` | `stop deadlifting - video 3/` (728,005,370) | Queued: YouTube Sun Oct 11, socials Mon Oct 12 |
| 4 | My Honest Oura Ring Review | `Video 4 Rev 3.mp4` | `my honest oura ring review - video 4/` (1,558,234,846) | Queued: YouTube Sun Nov 8 (`Docs/OURA_SETUP_RECEIPT_20261002.md`) |
| 5 | Getting Abs At 40 vs 25 | `Video 5 Rev 3.mp4` | `getting abs at 40 vs 25 - video 5/` (1,598,113,122) | **NOT set up. This handoff.** |

So the Blotato work is: **set up Video 5 from scratch, and confirm Videos 1 to 4 are live or queued on all four platforms.** Do not
re-upload or re-queue a video that is already live or queued; a second copy is a duplicate post.

## 2. Step A: confirm Videos 1 to 4 on all platforms (read only, then fix gaps)

Read the live Blotato schedule and recent posts (never a local receipt alone) and fill this in for each of Videos 1 to 4: YouTube,
Facebook, Instagram @danrosefit, TikTok, each as public, queued with its date, or missing.
- Records to start from: `BLOTATO_QUEUE_PROGRESS.md` (sections for Arms & Shoulders 09-22 and Stop Deadlifting), the board entries
  "Stop Deadlifting", "Oura review (Video 4)" and "Scheduled posts", `Docs/OURA_SETUP_RECEIPT_20261002.md`.
- A Blotato `failed` on a large video may be live anyway (memory `blotato-false-failure-large-video`): check the platform before
  calling it missing.
- A platform that is truly missing for a released video: report it to Dan with the video and the platform, and queue only that one
  platform copy (socials never earlier than the Monday after the YouTube release; rule in `AGENTS.md`). Do not move a queued Sunday.

## 3. Step B: Video 5, thumbnails first

Files: `Zeeshan Content Videos/getting abs at 40 vs 25 - video 5/`
- Master `getting abs at 40 vs 25 | zeeshan | 16x9 | video 5.mp4`, 1,598,113,122 bytes, 20:15, 1920x1080, MD5
  `dfdad6d05e9aba3c4ba34d41495d8f9e`. Re-hash it first. Drive source id `1RoGnpSSUTN0yM06-pGUeCrxBydtvBmz6` (his folder
  `1z0URDLA5cBYsi44fe2AAqwSVPUn09rfR`).
- Subtitles `... video 5.srt` (758 cues, his `Video 5_corrected_fixed.srt`, sidecar, never burned in). Spot check names and the
  last cue against the film before upload.
- It is over Blotato's 400 MB cap: make the platform copy the way Arms & Shoulders and Oura did (video re-encode, audio
  stream-copied; his audio is never reprocessed, memory `editor-audio-untouched`).

Facts for the packaging (confirm each against the film, do not trust this list blind):
- Opens 0:00 - 0:04 on the old Six Pack Shortcuts channel clip inside a YouTube page, then three before pictures, then two after
  pictures. Audio measured -14.4 LUFS, true peak -1.1 dBTP.
- **It contains AI clips** (round 1 listed a man on a couch at 0:04, a deadlift at 0:50, a shirtless man in a gym at 4:38; the
  8:40 barbell clip was removed in the last round). Watch for the ones still in and set the YouTube altered/synthetic flag and
  `ai_generated` accordingly.
- Music: `knox-gym-energy-gym-thunder-538872.mp3` (Pixabay, cleared for Content ID on 09-18).
- Known and accepted by Dan, do not fix: the real-picture label is missing for 0.6 seconds on the first after picture
  (0:08.8 - 0:09.4). Review history: `revision docs/abs-at-40-vs-25-revisions-zeeshan-round{1..4}*.summary.md`.
- Chapters: none exist yet. Build them from the three list cards (4:04, 6:51, 16:11) and the .srt.

Thumbnails: read `.claude/skills/_shared/VIDEO-RULES.md` (thumbnail section, belly rule, text never over his face or hair, Speedo
crop rule, no frowning photos), `.claude/skills/_shared/IMAGE-GENERATION.md`, then `/youtube-packaging`. **The standard five:**
1. One real pool-shoot photo (real photo of Dan, never redrawn; cutout plus type in code).
2. One real studio-shoot photo (same rule). Rotate away from the photos the last few videos used.
3. to 5. Three AI images, each a different design of Codex's choice, that sell "40 vs 25". Thumbnails carry no AI label.

`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every AI image; no outside image model. QC on the
rendered files (every text block at least 25 px clear of his face and hair), look at the sheet yourself, save finals in
`social media graphics/youtube/thumbnails/Getting Abs At 40 vs 25/`, show all five on one review sheet, and **STOP for Dan's pick.**

## 4. Step C: Video 5, `/video-setup`

Run the skill's Step 0 classification and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.
Title, description with the UTM link and chapters, tags, pinned comment, then the Blotato release through
`scripts/blotato/longform_queue.py`: **YouTube on a Sunday at 9 AM America/Chicago, one long-form per week, appended after the
last queued long-form; Facebook, Instagram @danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube
video is verified public.** Read the live queue first. On the 10-10 board the Sundays run through Dec 13 (RO-11), with RO-06
expecting Dec 20 and RO-03 Dec 27, so expect **Sun Jan 3, 2027** or the first free Sunday after whatever is queued when this runs.
Never upload to YouTube as Public and never use YouTube's own scheduling.
Then: receipt `Docs/ABS40VS25_SETUP_RECEIPT_<date>.md`, a board entry for the queued release, `youtube-description.md` in the
video's folder, and add its Shorts job to `Handoffs/video-editing/00-MASTER.md` (the list already notes it will need one).

## 5. Step D: store all five on the Seagate and on Google Drive

Copy the whole folder for each of the five videos (master, .srt, `youtube-description.md`), then verify each master by MD5.
- **Seagate** = `/Volumes/Expansion` (22 TB, about 21 TB free on 10-10). It has no `Zeeshan Content Videos` folder yet: create
  `/Volumes/Expansion/Zeeshan Content Videos/<same subfolder names>/`. Skip the stray `.part` files in the video 1 folder.
- **Google Drive** = `Zeeshan Content Videos/<same subfolder names>` in Dan's Drive, each set to anyone with the link can view
  (memory `drive-always-public`; mechanics in memory `drive-backup-capability`, rclone plus the verify script).
  Already on Drive: video 3 (folder `13hMGts3Lck398OMrStF1j3Ajfwp1Q0qT`) and video 4
  (`1EV2xxDCsEx-7EbgKHD9D23OqbkYKHkr2`). Check them, then add videos 1, 2 and 5. Also the `the 17 dollar ab wheel beats every
  crunch - video 1` folder if it is not there (his test video, same contract).
- The Extreme SSD already holds videos 3 and 4 under `/Volumes/Extreme/Zeeshan Content Videos/`. Extreme is not the target here;
  leave it as it is.
- Record each destination path, Drive link and MD5 result in the receipt.

## 6. Already done on 10-10 (do not repeat)

- Video 5 filed and recorded in `.claude/skills/editor-deliveries/state.json` along with videos 3 and 4 and his four newer folders.
- All five finals measured: 1920x1080, about 10 Mbps, each the newest file in his folder.
- Upwork contract closed 10-10 on Dan's go-ahead: $150 milestone released ($180 paid in total on the contract), contract ended
  as completed successfully, 5 stars with public feedback, no bonus (none was promised on this batch).

## 7. Housekeeping

Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only. Re-read `AI_COORDINATION.md` from disk before
finishing and replace the "Zeeshan batch" entry with the queued-release entry. Delete this handoff's README row when it is run.

## Starter prompt (Claude Sonnet 5.5, effort medium)

Read `Handoffs/handoff-20261010-zeeshan-batch-video5-setup-and-archive.md`. Name this session "Abs At 40 vs 25 LFC Setup". This is
a CONTENT long-form batch from Zeeshan and I approved all five videos. Use the Codex subscription to generate the images. First
confirm Videos 1 to 4 are live or queued on all four platforms and tell me any gap. Then for Video 5 make my five thumbnail choices
(1 pool photo, 1 studio photo, 3 unique AI designs of Codex's choice), show me the sheet and stop for my pick, then run
/video-setup. Finish by storing all five videos on the Seagate and on Google Drive, verified.
