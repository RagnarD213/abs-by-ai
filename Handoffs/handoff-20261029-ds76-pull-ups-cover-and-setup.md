CONTENT (SFC). How To Do Pull-Ups SFC Setup.

# DS-76: approved R2, covers and organic setup

**Ready to start now, after Dan's approval. One Claude setup task, Opus 5.5, high effort.** Not executed yet. **Use the Codex subscription to generate the images.** The image helper's supported baseline is `gpt-6.1-sol` at high effort; verify the newest supported stable Sol in the execution client before generating. Keep all cover work inside this one setup task. Setup and cover tasks are exempt from the edit cap.

## Approval and exact files

Dan approved the complete R2 on October 29, 2026: "Approved". Preserve the approved film byte for byte. Do not reopen colour, audio, crop, graphics, captions, performance selection or timing.

- Project master: `Short-form video content/DS-76 How To Do Pull-Ups/How To Do Pull-Ups SFC R2 - complete Short.mp4`. An identical verified copy is at `/Volumes/Extreme/Short-form video content/DS-76 How To Do Pull-Ups/`.
- Master SHA256 `1dca64b87fd2cb5a607571179986ada41c72b080957ed93efa3bc6ce279d24e5`: 44,231,160 bytes, 1080x1920 H.264, 1,672 frames at 30000/1001 fps (55.789 s), AAC 48 kHz stereo.
- Matching SRT in both folders, `How To Do Pull-Ups SFC R2 - complete Short.srt`: SHA256 `a8cfca6c6c8ff50c4240a7f1db08c5eb9f2fb3af863ad0ad3b7af73eae517176`, 60 cues. One-line captions are already burned into the picture, so do not add a second burned set.
- Approval: `approval-R2.json`. Receipt: `finalization-receipt-20261029.json`. Both are beside the master.
- Work folder, rebuild recipe and evidence: `/Volumes/Extreme/_edit_work/DS-76/round2/`. It holds decisions.json with Dan's words and hashes, independent reviews, the watch judge, the gate JSON and voice stamps. R1 is preserved in `round1/`.
- **Google Drive backup has not been done.** Upload it during setup under `Short-form video content/DS-76 How To Do Pull-Ups/`, verify the actual bytes, and save the folder link (public link, Drive rule).
- Queue DS-76 is finalized, not uploaded. The R1 and R2 review services (9476/9477) and the VLC copy were retired on approval. Footage ranges (C1882) are marked used, and library clips B0611/B0642/B0643/B0645 are set to used-final for DS-76.

## What ships

Organic dedicated Short on how to do pull-ups, and what to do if you can't do one yet: grip, hang, pull, no swinging, the assisted pull-up machine and slow negatives. Actual closing words: "Subscribe to my channel, and go to sixpackabs.com for all my newest videos." There is no tap/click-button CTA. Use `/video-setup`, never `/ad-setup` or Google Ads. This is already the Short: no derivatives.

Locked choices:
- F Deep And Vivid pool grade, Natural Warmth A voice and Original Portrait crop.
- A full-screen, full-body intro with "The Right Way / How to Do Pull-Ups" in the translucent blue glass bar at the bottom.
- The large "How to Do Pull-Ups" title on the windowed gym clips.
- The "Good Form" key-point bar and the "Can't Do One Yet? Do Both Every Week" list card.

Everything is real moving footage plus animated graphics: no realistic AI footage, AI music or AI voice, so `ai_generated=false`. An AI cover still alone does not trigger the synthetic flag.

**Release phase:** under the 2026-10-28 cadence, October 23 gym how-tos are held for phase 3, the January blitz (Dec 26 to Jan 31; Shorts at 9 AM and 6 PM on Mon, Tue, Thu and Sat). This is gym footage, not kitchen. Take the actual slot from `Docs/SHORTS_RELEASE_CALENDAR.md`, `scripts/blotato/release_phases.py` and the live Blotato queue.

## QA history (honest)

- **Independent review and watch pass:** five fresh R1 reviews and two R2 reviews; the final verdict is SHIP. The final-file watch judge found 0 defects across 35 of 35 images, and a frame-match check confirms no source frame repeats.
- **Hair and words:** hair clears the header by at least 128 px on all 553 presenter frames. Delivered audio matches the script word for word.
- **Voice:** the verbatim voice-preservation stamp passes. The reference comparison flags only the tone row, the known result of the standard bass lift.
- **Delivery gate 2.6.2: FAIL, 35 of 39.** Two framing rows measure Dan's Original Portrait choice. `captions:burned` is the legacy detector band. `captions:sync` comes from ASR word starts stretched across silence at 26.25 and 51.87 s; level measurements put the speech onsets on the caption starts. No thresholds were changed. Approval is Dan's creative acceptance, not a numerical PASS. Do not rebuild the film or alter stamps to satisfy a row.

## Execute

1. **Read the rules and check the files.** Read the current `AGENTS.md`, the full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, WRITING-RULES, IMAGE-GENERATION, `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md` and recent approved-cover history. Verify this exact master, SRT and approval. Check for an existing DS-76 setup or config and resume it rather than duplicate.
2. **Make five distinct covers.** Inspect recent actual cover picks and their final selected images (Calories Shorts C, Hamstring Curls, V-Taper). Then make five genuinely distinct designs with the same headline copy:
   - two different AI images of Dan actively doing pull-ups or the assisted machine;
   - one authentic photo from either the pool or the studio shoot, with the original person pixels preserved;
   - two discretionary concepts guided by his picks.

   Vary composition, layout, type and colour. Use a real identity reference and check every AI face: lean and shredded, not bulky, with an overhand grip on a real pull-up bar. Keep text clear of hair and face. No frowning default, no visible standing-brief shape, no website mark and no real-photo disclosure on covers.
3. **Use the Codex subscription to generate the images.** Generate with `.claude/skills/_shared/codex-image.sh`. Deliver all five checked options, each in Instagram and YouTube layouts, on one review page. **Stop for Dan's pick before any upload or scheduling.** If he asks for revisions, show the exact revised files and get approval before installing them.
4. **After his pick, finish backups and media.** Complete the Drive backup, packaging and verified media and cover uploads. Make only the required TikTok cover-first copy, stream-copying the approved audio. Write the title, description, platform captions, links and UTMs, plus a short topic-specific `pinned_comment` question taken from the transcript. Verify all hashes, TikTok frame zero, the YouTube cover, and the Facebook cover registry and live installer. Use the maintained organic guard and `organic_short_queue.py`.
5. **Pick the date from the live queue.** Inspect live Blotato, the calendars and the shared waitlist before choosing a phase 3 slot on all four platforms. If capacity is full, use the shared waitlist and daily top-up with the `gym` flag; never create a per-video routine. If no compliant slot exists, give Dan one concrete date before booking. Re-read the saved schedules before reporting the Short as queued.
6. **Record everything.** YouTube releases through Blotato only, never Public or native scheduling. Record the cover files and hashes, the three-copy verification, media URLs, metadata, and the four schedule IDs or the honest waitlist state. Update only the DS-76 records and keep the job finalized until setup earns "uploaded". No Google Ads work and no Victory Dashboard.

## Starter prompt

How To Do Pull-Ups SFC Setup. Read `Handoffs/handoff-20261029-ds76-pull-ups-cover-and-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Preserve my approved R2 film. Make five distinct cover choices in both Instagram and YouTube layouts, stop for my pick, then complete backups, upload and scheduling in a January-blitz Short slot after that pick.
