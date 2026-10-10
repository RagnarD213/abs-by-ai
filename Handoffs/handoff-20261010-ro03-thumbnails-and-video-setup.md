# RO-03 "The Vacuum: Workout Only": thumbnails, then upload and setup

**CONTENT, long-form family (LFC).** A 2:32 follow-along. Nothing else is derived from it: no vertical, square or 1-minute version.

**Written 2026-10-10 by Claude.** One Claude task does everything: five thumbnail choices (images made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the full film on 2026-10-10 ("All right, this looks good. Give me the handoff for setup.").
**Model:** Claude Sonnet 5.5, effort medium (mechanical setup per `model-routing-plan`; Opus high only if Dan rejects the title or description copy).
**Sidebar name:** `Vacuum Workout Only LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 2 full film is delivered, gated, independently reviewed and approved by Dan as delivered. The copy in `Videos to Review/` and the
review page (port 8877) were removed on 10-10; the delivery folder is the record.
It is ORGANIC: it ends "So go to AbsByAI.com now, see yourself with abs, and take that first step. Thanks for watching the video guys, and
I'll see you next time." with no tap-the-button call to action. Still run the skill's Step 0 classification, and
`python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.
Edit Queue row RO-03 is already `finalized` (artifact mirror done); when the release is queued set it `uploaded`, mirror with `ArtifactData`
(artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, read the version first and pin `if_version`), then
`queue.py mark-synced RO-03`.

## 2. Files (all local)

Folder: `claude edited long form content/13 - The Vacuum Workout Only/`
- Master: `The Vacuum Workout Only | claude round 2 | 16x9 | RO-03.mp4`, 151 MB, 2:31.6, 1920x1080 29.97, h264 + AAC,
  sha256 `b18ceaf68af7f84e98ddfd6e60af5ecd4c7d4d781785fe4bf86ec1a151812a7b`. Re-hash it first.
- `... RO-03.srt` (27 cues, sidecar, never burned in) and `... RO-03.chapters.txt` (6 chapters, use as-is: Set 1, Rest, Set 2, Rest,
  Set 3, How To Start If You're A Beginner).
- Also there: `... REVIEW 540p.mp4`, the audio AB file, the edit sheet, stamps, `notes-RO03.md`, `ROUND-2-REVIEW.md`, `recipe-RO-03/`.
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro03/round2/`.

Facts for the packaging:
- **No AI footage, no AI image, no stock.** Every frame is Dan's real 8/14 poolside footage. So `ai_generated: false` in the Blotato config
  and no altered/synthetic flag on YouTube. Do not add the AI-image sentence to the description.
- **It is the workout-only companion to RO-02** "The Vacuum: The Best Ab Exercise For Belly Fat" (queued for Sun Nov 22;
  `Docs/RO02_SETUP_RECEIPT_20261005.md`). The description should send people to that film for the full explanation, by title until it has
  a public link, and by link once it does. RO-02's description is in
  `claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/youtube-description.md`; do not copy it, match its voice.
- What the film is, in his words: three standing vacuum holds of 20 seconds, 30 seconds of rest between. Between sets take deep belly
  breaths. During a hold take short breaths through your nose. Best time: first thing in the morning, fasted. Beginners: one timed
  20-second set every morning in the mirror. UTM link and call to action per `/video-setup` Step 3 (campaign content `ro03-vacuum-workout`).
- **The stamps read FAIL and that is known.** Audio gate on the whole film: 4 rows, because the three holds are music only (the talking
  sections alone pass every row). Delivery gate 2.5.1: the rows are listed in `notes-RO03.md`. Dan approved the film. Do not rebuild or
  re-gate; if a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is under Blotato's 400 MB cap: no platform copy is needed. 2:32 is inside every platform's length limit.

## 3. Thumbnails first

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail section, the belly rule, text never over his face or hair, the Speedo crop rule,
no frowning photos), `.claude/skills/_shared/IMAGE-GENERATION.md`, then `/youtube-packaging`. **The standard five:**

1. **One real pool-shoot photo** (a real photo of Dan, never redrawn; background-removed cutout plus type in code).
2. **One real studio-shoot photo** (same rule). Rotate away from the photos the last few videos used, and away from RO-02's thumbnail so
   the two vacuum videos do not look like the same video.
3. to 5. **Three AI images, each a different design of Codex's choice** that sells the topic: a 20-second timer, a follow-along workout, a
   tight waist. No belly fat framing and no hands on a stomach. Thumbnails carry no AI label.

Same copy on all five unless Dan asks for alternatives; short and big (two lines beats three). The video's own words: "The Vacuum Workout",
"Follow Along", "3 sets of 20 seconds". No result claim.
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every AI image; no outside image model. QC on the RENDERED
files: person-mask clearance of every text block from his face and hair of at least 25 px, and look at the sheet yourself before sending it.
Save the finals in `social media graphics/youtube/thumbnails/The Vacuum Workout Only/`. Show all five on one review sheet (`SendUserFile`,
display render), list them in plain words, and **STOP for Dan's pick.** He may pick one, or two for an A/B test.
Final file: `<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link, the pointer to RO-02 and the chapters,
tags, pinned comment), Blotato release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**, then Facebook,
Instagram @danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified public. Read the live
Blotato YouTube queue first. As of the 10-10 board these Sundays are taken: Oct 11 Stop Deadlifting, Oct 18 RO-05, Oct 25 RO-12, Nov 1
RO-16, Nov 8 Oura, Nov 15 RO-13, Nov 22 RO-02, Nov 29 RO-10, Dec 6 RO-01, Dec 13 RO-11, and RO-06's setup expects Dec 20. So expect
**Dec 27**, or Dec 20 if RO-06 is not queued yet when this runs; use `scripts/blotato/longform_queue.py`, which refuses an off-Sunday or
occupied slot. Either date is after RO-02's release, which is the right order for a companion video. Never upload to YouTube yourself;
Blotato creates the public video at release time. Receipt in `Docs/RO03_SETUP_RECEIPT_<date>.md`, a board entry for the queued release
(replace the RO-03 APPROVED entry), Edit Queue `uploaded`.

## 5. Already done at finalization (do not repeat)

Footage ranges marked used on rolls C1624, C1625, C1626 and C1629. Dan's approval is recorded in
`/Volumes/Extreme/_edit_work/ro03/round2-plan/decisions.json`, the watch log, the edit sheet and the QC corpus. No new clip went into
the clip library: the opening clip is this film's own live set.

## 6. Open items (not blocking)

- Dan was shown two optional changes and asked for neither: set 3 is the same picture as set 1 and ends on him reaching for his phone;
  all six lower thirds carry a FULL CAPS word. The film ships as delivered.
- The phone timer's beep at the end of each hold is faint under the music. Not lifted.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.

## Starter prompt (Claude Sonnet 5.5, effort medium)

Read `Handoffs/handoff-20261010-ro03-thumbnails-and-video-setup.md`. Name this session "Vacuum Workout Only LFC Setup". This is a CONTENT
long-form and I approved the full film. Use the Codex subscription to generate the images. Make my five thumbnail choices (1 pool photo,
1 studio photo, 3 unique AI designs of Codex's choice), show me the sheet and stop for my pick, then run /video-setup.
