# RO-12 "Top 5 Zepbound Tips": upload and schedule (organic content video), Claude half

**Written 2026-10-01 by Claude (Opus 5.5).** Job RO-12 on the Edit Queue, state `finalized`. Run it with the `/video-setup`
skill, **except the thumbnails**: Codex builds those in its own task (`Handoffs/handoff-20261001-ro12-thumbnails-codex.md`) and
Dan gives this session the finalized thumbnail file when he fires it. Do not design, pick or edit a thumbnail here. If the starter
prompt carries no thumbnail path, stop and ask Dan for it. Name this session `Top 5 Zepbound Tips LFC setup`.

## 1. What is approved
Dan, 2026-10-01, after watching the round-2 review copy: *"I think this video looks good. We can go without the thigh pinch
shot... Go ahead and finalize this."* That approves the film as delivered, without the thigh-pinch AI clip. Do not re-edit
anything. Recorded in `/Volumes/Extreme/_edit_work/ro12/round2-plan/decisions.json` (`final_approval`).

**It is an ORGANIC content video, not an ad.** The ending: "Thank you for watching guys. If you enjoyed this video, subscribe to
make sure you get my newest videos as soon as I release them." No "tap the button below". Still run Step 0's classification and
`python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## 2. Files (all local, already filed; no download step)
Folder: `claude edited long form content/09 - Top 5 Zepbound Tips/`
- Master: `Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`, 2.42 GB, 9:11.42, 1920x1080 29.97 fps H.264 + AAC, sha256
  `7f6766c5e1d82881fb2a56b9b7414f6baa0bbe49f027828e507991d9f7cae67b`. Audio gate stamp PASS beside it.
- Subtitles: `Top 5 Zepbound Tips.srt` (180 cues, sidecar; upload it as YouTube captions).
- Chapters: `Top 5 Zepbound Tips - chapters.txt` (7 chapters, first at 0:00; use them as-is in the description).
- Build record: `notes-RO12.md` in the same folder.

Facts for the packaging:
- **The film contains realistic AI footage** (three AI clips of people, each with the on-screen AI-GENERATED label: the nausea
  clip at 1:42, the split-screen gym clip at 6:54, the mirror clip at 7:53). So `--synthetic true` on YouTube and
  `ai_generated: true` in the Blotato config.
- Organic videos may name the drug (Dan, 2026-09-30, VIDEO-RULES.md): the title and description may say Zepbound.
- Dan says "Not medical advice. Talk to your doctor." on screen; put the same line in the description.
- The lower third at 8:23 says WATCH NEXT "How To Keep Your Muscle While You Lose Fat" (RO-01, not published yet). No YouTube
  card can point at it now; note it in the receipt so the card is added when RO-01 is public.
- **Delivery gate stamp reads FAIL (gate 2.4.0), known and reported to Dan before he finalized:** two caption rows misread the
  Soft Blue cards as burned captions (as on RO-05), the quiet 1.5 s end hold counts as a "silent second", and the wide/tight
  spread reads x1.096 against x1.10. Independent review round 4 said SHIP. Do not rebuild or re-gate for these; if a setup
  script refuses the stamp, tell Dan what it refused and stop there.

## 3. The steps (per `/video-setup`)
1. **Board + queue:** edit the RO-12 ACTIVE entry. Queue stays `finalized` until the YouTube upload, then `uploaded`
   (`python3 scripts/edit-queue/queue.py set RO-12 uploaded ...`, then write_db the exported row to the Edit Queue artifact,
   pinned `if_version`, then `queue.py mark-synced RO-12`).
2. **Backups:** copy the master (and .srt) to the Extreme drive and Google Drive per the skill's "Three copies" rule (Drive:
   anyone-with-link viewer, memory `drive-always-public`).
3. **Thumbnail from Dan:** check the file he gives you: 1280x720 (16:9), JPEG or PNG under 2 MB, opens cleanly. If it fails one
   of those, make a conforming copy (resize or re-encode only, never a design change) and say so.
4. **Packaging:** searchable title with no hype claims; description with the UTM link (`utm_content=ro12-zepbound-tips`), the 7
   chapters, a short summary of the five tips, the not-medical-advice line, subscribe CTA, 3 to 5 hashtags. No em dashes anywhere.
5. **YouTube holding upload, PRIVATE only** (`node scripts/youtube/upload.js ... --privacy private --synthetic true`, run in the
   background, never re-run a slow upload), with `--thumbnail <Dan's file>`. Read back `privacyStatus: private`. Never Public,
   never a `publishAt`.
6. **Blotato:** the 2.42 GB master is far over Blotato's 400 MB cap (memory `blotato-false-failure-large-video`). Encode a
   platform copy under 400 MB (1080p H.264, video about 4 Mbps, audio copied) with `Media/video_edit/bin/ffmpeg`
   (`nice -n 20` + VideoToolbox, memory `setup-encodes-low-priority`), check its duration and loudness match the master, upload it
   and Dan's thumbnail with `blotato_create_presigned_upload_url`, hash-check each download, write
   `scripts/blotato/configs/ro12-zepbound-tips.json` (`content_type: organic`, `source` = the master's path), dry-run
   `scripts/blotato/longform_queue.py`, then `--apply`. Accounts: YouTube release, Facebook, Instagram @danrosefit, TikTok. Never
   @abs.by.ai. The film is 9:11: confirm each platform takes that length; if one refuses, queue the others and tell Dan.
7. **Release slot:** 9 AM CT (14:00Z while CDT, 15:00Z after Nov 1) on a day with no other long-form, following the Sunday
   long-form cadence. Already taken at writing: Sat Oct 3, Sun Oct 4, Sun Oct 11, Sun Oct 18. Read `BLOTATO_QUEUE_PROGRESS.md`
   and the live Blotato schedule for anything newer, take the first free slot and record it there.
8. **Verify** every schedule in Blotato, log the receipt (`Docs/RO12_SETUP_RECEIPT_<date>.md`), update the board entry and
   `Handoffs/README.md`, commit.

## 4. Traps
- The shared checkout is used by several sessions and cannot push right now (board: "Shared checkout cannot push"): never
  `git stash -u`; commit only your files and let them ride until that handoff is run.
- YouTube engagement ads fire automatically for new videos (memory `ytads-retired-manual-management`); leave that routine alone.
- Swearing on camera stays; never flag it (memory `swearing-never-cut-never-ask`).

## 5. Model and starter prompt
Claude Opus 5.5, effort medium (a known, scripted flow; no Dan stop once the thumbnail is in hand).

> Read `Handoffs/handoff-20261001-ro12-video-setup.md` in full, then run `/video-setup` for RO-12 "Top 5 Zepbound Tips" (finalized organic content video), without the thumbnail step. The finalized thumbnail is: `<PASTE THUMBNAIL PATH>`. Package it, upload it to YouTube as Private with that thumbnail, queue it in Blotato on the next free long-form slot in our release schedule, verify, and report. Name this session "Top 5 Zepbound Tips LFC setup".
