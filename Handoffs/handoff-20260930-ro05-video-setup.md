# RO-05 "How I Make My Daily Salad": upload and schedule (organic content video)

**Written 2026-09-30 by Claude (Opus 5.5).** Job RO-05 on the Edit Queue, state `finalized`. Run it with the `/video-setup`
skill, start to finish.

## 1. What is approved
Dan, 2026-09-30, after watching the round-4 film in VLC: *"Okay, this video is approved and good to go."* That approves the film
as delivered. The three items that were open for him (the G01 lower third over his mouth for 0.36 s during the bite at 0:08.6,
the jump at 8:25.6, six joins covered by a white flash) stay as delivered. Do not re-edit anything. Recorded in
`/Volumes/Extreme/_edit_work/ro05-fable/round4-plan/decisions.json` (`final_approval`).

**It is an ORGANIC content video, not an ad.** Dan confirmed: *"This is an organic content video, so it should be privately
uploaded, set up in Blotato, and added to our YouTube release schedule."* The ending agrees: Dan says "go to AbsByAI.com", then
the Soft Blue end card ("See your future self. Get the plan to build it." / ABSBYAI.COM), with no "tap the button below".
Still run Step 0's classification and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## 2. Files (all local, already filed; no download step)
Folder: `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/`
- Master: `How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.mp4`, 1.91 GB, 14:53.86, 1920x1080 29.97 fps H.264 + AAC,
  sha256 `23fdcb0c86469cb7e7fcd6807e0b5caf17dc40c80c404d2ada7863a84b11378e`. Audio gate stamp PASS beside it.
- Subtitles: `How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.srt` (277 cues, sidecar; upload it as YouTube captions).
- Chapters: `How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.chapters.txt` (10 chapters, first at 0:00, built from the
  section titles; use them as-is in the description).
- **Not** the older `| fable |` file in the same folder: that is the rejected earlier cut.
- Build record, if a fact is needed: `/Volumes/Extreme/_edit_work/ro05-fable/round4/ROUND-4-BUILD.md`.

Facts for the packaging: no AI footage anywhere in the film (all real footage of Dan in his kitchen plus real Abs By AI app screens),
so `ai_generated: false` and `--synthetic false`. Numbers Dan says on camera: about 700 calories, about $4 a bowl, stays fresh 7 days,
salad bar $20 vs $4 homemade; the app estimated 683 calories vs about 720 weighed by hand.

## 3. The steps (per `/video-setup`)
1. **Board + queue:** add the ACTIVE entry ("thumbnail pick pending"). Queue stays `finalized` until the YouTube upload, then `uploaded`
   (`python3 scripts/edit-queue/queue.py set RO-05 uploaded ...`, then write_db the exported row to the Edit Queue artifact,
   pinned `if_version`, then `queue.py mark-synced RO-05`).
2. **Backups:** copy the master to the Extreme drive and Google Drive (Drive: anyone-with-link viewer, memory `drive-always-public`).
3. **Thumbnails, the only stop for Dan:** five variations per the skill, review sheet via `SendUserFile`, then stop and wait for his pick.
   Prefer real shoot photos over video frames and never soft abs (memory `cover-photo-selection`); good frames include the finished
   salad close-ups (0:05 to 0:08) and Dan holding the sealed glass bowl.
4. **Packaging after the pick:** searchable title with no hype claims; description with the UTM link
   (`utm_content=ro05-daily-salad`), the 10 chapters, a how-to paragraph, subscribe CTA, 3 to 5 hashtags. No em dashes anywhere.
5. **YouTube holding upload, PRIVATE only** (`node scripts/youtube/upload.js ... --privacy private --synthetic false`, run in the
   background, never re-run a slow upload). Read back `privacyStatus: private`. Never Public, never a `publishAt`.
6. **Blotato:** the 1.91 GB master is far over Blotato's 400 MB cap (memory `blotato-false-failure-large-video`). Encode a
   platform copy under 400 MB (1080p H.264, video about 3 Mbps, audio copied) with `Media/video_edit/bin/ffmpeg`, check its
   duration and loudness match the master, upload it with `blotato_create_presigned_upload_url`, hash-check the download, write
   `scripts/blotato/configs/ro05-daily-salad.json` (`content_type: organic`, `source` = the master's path), dry-run
   `scripts/blotato/longform_queue.py`, then `--apply`. Accounts: YouTube release, Facebook, Instagram @danrosefit, TikTok.
   Never @abs.by.ai (retired 2026-09-24). ⚠ The film is 14:54: confirm each platform takes that length before queuing, and if
   TikTok or Instagram refuse it, queue the ones that accept it and tell Dan which were skipped.
7. **Release slot:** 9 AM CT (14:00Z while CDT, 15:00Z after Nov 1) on a day with no other long-form, following the Sunday
   long-form cadence. Already taken: Sun Oct 4 (Belly Fat Emergency re-release) and Sun Oct 11 (Stop Deadlifting). Read
   `BLOTATO_QUEUE_PROGRESS.md` and the live Blotato schedule for anything newer, then take the first free slot and record it there.
8. **Verify** every schedule in Blotato, log the receipt (`Docs/RO05_SETUP_RECEIPT_<date>.md`), update the board entry and
   `Handoffs/README.md`, commit and push.

## 4. Traps
- The shared checkout is used by several sessions: never `git stash -u`; `git pull --rebase` only when your tree is clean. A
  session-1 commit for RO-05 round 4 (`5d16bfd`, board + queue records) may still be unpushed; let it ride with yours.
- YouTube engagement ads fire automatically for new videos (memory `ytads-retired-manual-management`); leave that routine alone.
- Swearing on camera stays; never flag it (memory `swearing-never-cut-never-ask`).

## 5. Model and starter prompt
Claude Opus 5.5, effort medium (a known, scripted flow with one Dan stop).

> Read `Handoffs/handoff-20260930-ro05-video-setup.md` in full, then run `/video-setup` for RO-05 "How I Make My Daily Salad": it is an approved organic content video. Build the thumbnail options and stop for my pick; after I pick, package it, upload it to YouTube as Private, queue it in Blotato on the next free long-form slot in our release schedule, verify, and report.
