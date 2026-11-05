CONTENT (SFC). How To Do T-Bar Rows SFC Setup.

# DS-77: finalized R1, covers and organic setup

**Ready to start now. One Claude setup task, Opus 5.5, high effort.** Not executed yet. **Use the Codex subscription to generate the images.** The image helper's supported baseline is `gpt-6.1-sol` at high effort; verify the newest supported stable Sol in the execution client before generating. Keep all cover work inside this one setup task. Setup and cover tasks are exempt from the edit cap.

## Approval and exact files

Dan finalized R1 on November 5, 2026: "Let's go with F Deep and Vivid for the color. Fuller base for the voice original portrait for the crop apply those options, rebuild the full film, and then this is finalized." Then: "Only rebuild the full film if they didn't already have those options." and "Okay, just make sure the voice matches my words." ("Fuller base" = voice B Fuller Bass.) F and Original Portrait were already in the reviewed film, so only the sound was swapped to voice B; the video stream is byte-identical to the reviewed build. Preserve the film byte for byte. Do not reopen colour, voice, crop, graphics, captions, takes or timing.

- Project master: `Short-form video content/DS-77 How To Do T-Bar Rows/How To Do T-Bar Rows SFC R1 - complete Short.mp4`. Identical verified copy: `/Volumes/Extreme/Short-form video content/DS-77 How To Do T-Bar Rows/`.
- Master SHA256 `eddb7539ae03db9c853040f303ad6f7c6706ab4c48699d684a82a07171715d23`: 45,780,072 bytes, 1080x1920 H.264, 1,515 frames at 30000/1001 fps (50.55 s), AAC 48 kHz stereo.
- Matching SRT beside it, `How To Do T-Bar Rows SFC R1 - complete Short.srt`: SHA256 `a6911389b2ccba22e85fcf7dad8524cbaafddbb461faa3a0682880d74cee4ae0`, 52 cues. One-line captions are already burned in; do not add a second burned set.
- Approval `approval-R1.json` and receipt `finalization-receipt-20261105.json` beside the master.
- Work folder, recipe and evidence: `/Volumes/Extreme/_edit_work/DS-77/round1/` (decisions.json, take-choice.json, four independent reviews, watch judge, gate JSON, voice stamps, `notes-DS-77-R1.md`).
- **Google Drive backup has not been done.** Upload under `Short-form video content/DS-77 How To Do T-Bar Rows/`, verify bytes, save the public folder link.
- Queue DS-77 is finalized, not uploaded. Review service 9707 and the VLC copy were retired on finalization. Footage C1882 ranges are marked used; library clips B0644/B0723/B0724/B0725 are used-final for DS-77.

## What ships

Organic dedicated Short on the chest-supported T-bar row: why the chest pad protects the lower back, widest grip, handles at about 45 degrees, pull to the stomach and squeeze, slow lowering, sets and reps, tempo. Actual closing words: "So if you want to lose your belly fat and build muscle at the gym, try them this way in your next workout. Subscribe and go to sixpackabs.com for all my newest videos." No tap/click-button CTA: use `/video-setup`, never `/ad-setup` or Google Ads. This is already the Short: no derivatives.

Locked: F Deep And Vivid, B Fuller Bass, Original Portrait; full-screen side-angle intro with "The Right Way / How to Do T-Bar Rows" in the blue glass bar; large "How to Do T-Bar Rows" title on the windowed gym clips; sets card; "Tempo: 2-3 Seconds Down, Explode Up" bar. All real footage plus animated graphics: `ai_generated=false`.

**Release phase:** October 23 gym how-tos are held for phase 3, the January blitz (Dec 26 to Jan 31; Shorts 9 AM and 6 PM Mon, Tue, Thu, Sat). Gym footage, not kitchen. Take the slot from `Docs/SHORTS_RELEASE_CALENDAR.md`, `scripts/blotato/release_phases.py` and the live Blotato queue. Space it away from How To Do Pull-Ups (DS-76, Sat Dec 26 9 AM), same set and format.

## QA history (honest)

- Three independent reviews said DOES NOT SHIP; every item was fixed (head cut off by the camera's own framing, camera jolts at clip edges, captions on window edges, "2 2 Working Sets", squeeze timing, three caption words). The fourth: SHIP. Watch judge 35/35 images, 0 defects. Both were carried to the voice-B file because its video stream is byte-identical.
- Hair: at least 122 px on all 683 presenter frames, at least 30 px on every gym-clip frame.
- Voice: verbatim stamp PASS against the Fuller Bass mix; that mix fails only the known tone row (standard bass lift). Delivered words match the captions (169 aligned, median timing -3 ms).
- Delivery gate 2.6.3: FAIL 35/39, the same four rows as approved DS-76 (two framing rows from Original Portrait, `captions:burned`, `captions:sync`). Do not rebuild or alter stamps to satisfy a row.
- Caption note: "this way **in** your next workout" is printed from acoustic evidence (a short front vowel); the teleprompter said "on". Dan was told and finalized.

## Execute

1. **Read and verify.** Current `AGENTS.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, IMAGE-GENERATION (incl. the blind Google test), `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, recent approved-cover picks. Verify the exact master, SRT and approval. Resume any existing DS-77 setup rather than duplicate.
2. **Five Codex covers plus three unlabeled Google options.** Two different AI images of Dan doing chest-supported T-bar rows, one real pool or studio photo (original person pixels kept), two concepts guided by his picks; same headline; varied layout, type and colour; title capitalization on every word. Real identity reference, face check, "lean and shredded, not bulky". Text clear of face and hair; no frowning default, no brief shape, no website mark. Instagram and YouTube layouts for each. **Use the Codex subscription to generate the images** with `.claude/skills/_shared/codex-image.sh`. Show all, **stop for Dan's pick** before any upload or scheduling.
3. **After his pick:** Drive backup, packaging, verified media and cover uploads, TikTok cover-first copy (stream-copy the approved audio), title, description, captions, links/UTMs, a topic `pinned_comment` question from the transcript. Verify hashes, TikTok frame zero, YouTube cover, Facebook cover registry and live installer. Use the organic guard and `organic_short_queue.py`.
4. **Schedule from the live queue** in a phase 3 slot on all four platforms, or the shared waitlist with the `gym` flag if Blotato is full. Never a per-video routine. Re-read saved schedules before reporting.
5. **Record** cover files and hashes, three-copy verification, media URLs, metadata, the four schedule IDs or the waitlist state, in a setup receipt. Keep the job finalized until setup earns "uploaded". No Google Ads, no Victory Dashboard.

## Starter prompt

How To Do T-Bar Rows SFC Setup. Read `Handoffs/handoff-20261105-ds77-t-bar-rows-cover-and-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Preserve my finalized R1 film byte for byte. Make five distinct cover choices plus the three unlabeled Google options, in both Instagram and YouTube layouts, stop for my pick, then complete backups, upload and scheduling in a January-blitz Short slot.
