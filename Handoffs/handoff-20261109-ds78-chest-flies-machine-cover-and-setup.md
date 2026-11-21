CONTENT (SFC). How To Do Chest Flies On SFC Setup.

# DS-78: finalized R1, covers and organic setup

**Ready to start now. Owner: Codex, newest supported stable Sol at high effort (currently `gpt-6.1-sol`; verify in the client).** Not executed yet. Codex owns setup for Claude-edited videos (AGENTS.md, 2026-11-07). Images: attempt Google AI subscription images first and keep the required Codex subscription choices (AGENTS.md, 2026-11-08; `.claude/skills/_shared/codex-image.sh`). No paid image API unless a subscription attempt actually fails and is recorded. Setup and cover tasks are exempt from the edit cap.

## Approval and exact files

Dan finalized R1 on November 9, 2026: "Let's go with F deep and vivid for the color. B fuller bass for the voice one original portrait for the crop if you already applied those to the existing short, then it's good to go as is. If not, apply those and then show me the finished version." All three were already in the reviewed film, so the reviewed file IS the finalized file (no rebuild). He did not change the fourth page item, so the recommended default stands: the wide side view (B02) plays under "set the seat in the right position". Preserve the film byte for byte. Do not reopen colour, voice, crop, graphics, captions, takes or timing.

- Project master: `Short-form video content/DS-78 How To Do Chest Flies On The Machine/How To Do Chest Flies On SFC R1 - complete Short.mp4`. Verified identical copies: `/Volumes/Extreme/Short-form video content/DS-78 How To Do Chest Flies On The Machine/` and [Google Drive](https://drive.google.com/open?id=1vP7av_OhEp9mbvkwRNFODzPGTVtpKvZs) (rclone check 0 differences; anyone with the link).
- Master SHA256 `d12e90f5664bb785b9f288010bc022f154e1acbb304d1c9db44fae1dae67697d`: 36,660,044 bytes, 1080x1920 H.264 30000/1001 fps, 51.45 s, AAC 48 kHz stereo, BT.709 tagged.
- SRT beside it (`How To Do Chest Flies On SFC R1 - complete Short.srt`). One-line captions are already burned in; never add a second burned set.
- `approval-R1.json` (Dan's words, choices, hashes) and the audio and delivery gate stamps beside the master.
- Work folder, recipe and evidence: `/Volumes/Expansion/_edit_work/DS-78/round1/` (moved off the internal drive 2026-11-09, contents checksum-verified; the delivery folder is the record). Recipe copy: `.claude/skills/shorts/reference/ds78-chest-fly-machine/`.
- Queue DS-78 is finalized, not uploaded. Review page 9708 and the VLC copy were retired. C1882 ranges are marked used; library clips B0665, B0666, B0667, B0668 are used-final for DS-78.

## What ships

Organic dedicated Short on the chest fly machine: why flies beat bench press for the chest, set the seat so the handles line up with mid-chest, set the starting position for a deep but safe stretch ("as far back as you can go, but no farther", an ad-lib Dan filmed), slight bend in the elbows, squeeze in front, slow return, sets and reps, tempo. Closing words: "Subscribe to my channel and go to sixpackabs.com for all my newest videos." No tap/click-button CTA: `/video-setup`, never `/ad-setup` or Google Ads. This is already the Short: no derivatives.

Locked look: F Deep And Vivid, B Fuller Bass, Original Portrait; windowed real gym clips under a large "How to Do Chest Flies" title (a 9:16 crop cuts his hands at the stretch); "Starting Position: Deep but Safe Stretch" bar; sets-and-reps card; "Tempo: 2-3 Seconds Down, Explode Up" bar. All real footage plus animated graphics: `ai_generated=false`, YouTube synthetic false.

**Release phase:** October 23 gym how-tos are held for phase 3, the January blitz (Dec 26 to Jan 31; Shorts 9 AM and 6 PM Mon, Tue, Thu, Sat). Gym footage, not kitchen (`gym: true`, `kitchen: false`). Take the slot from `Docs/SHORTS_RELEASE_CALENDAR.md`, `scripts/blotato/release_phases.py` and the live Blotato queue. Space it away from the same-set Shorts How To Do Pull-Ups (DS-76, Sat Dec 26 9 AM) and How To Do T-Bar Rows (DS-77, Tue Jan 5 9 AM).

## QA history (honest)

- Independent review (fresh reviewer): DOES NOT SHIP on the first file, then SHIP after fixes on this exact file (clipped final "s", key-point copy that echoed his words, both key-point bars too low for app buttons, delivery gate run). Earlier, an outside listener caught an "f-For" stutter at a join; fixed. Second fresh watch judge: 43/43 images, 0 defects. Negative-events scan: 206 frames, nothing found. Reports: work folder `evidence/independent/ROUND-1-REVIEW.md`.
- Hair: at least 108 px on all 605 on-camera frames; gym-clip windows checked by eye every 6th frame.
- Voice: verbatim stamp PASS against the Fuller Bass mix; the reference gate fails only the known tone row (standard bass lift). Delivered words match the captions.
- Delivery gate 2.6.3: FAIL 35/39, the same four rows as approved DS-76 and DS-77 (two framing rows from Original Portrait, `captions:burned`, `captions:sync`). Do not rebuild or alter stamps.
- Footage note: no close-up of setting this machine's seat or starting position was filmed (the rolls' only unused parts are a 1.5 s reset and resting), so those lines play over the wide side view and the low-angle stretch.

## Execute

1. **Read and verify.** Current `AGENTS.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, `.claude/skills/_shared/IMAGE-GENERATION.md` (incl. the blind Google test), `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, recent approved-cover picks (including `Short-form video content/covers/approved-ds77/picks.json`: Dan picked a touched-up REAL frame for T-Bar Rows). Verify the exact master and approval hashes. Resume any existing DS-78 setup rather than duplicate.
2. **Covers.** The required five: two different AI images of Dan doing the chest fly machine, one real pool or studio photo (original person pixels kept), two concepts guided by his picks; same headline; varied layout, type and colour; first letter of every word capitalized. Real identity reference, face check, "lean and shredded, not bulky, same size as the reference". Plus three unlabeled Google options (blind test). Google subscription attempt first per the November 8 rule. Text clear of face and hair; no frowning default, no brief shape, no website mark. Instagram and YouTube layouts for each. Show all, **stop for Dan's pick** before any upload or scheduling.
3. **After his pick:** packaging, verified media and cover uploads, TikTok cover-first copy (stream-copy the approved audio), title, description, captions, links/UTMs (sixpackabs.com, campaign chest-flies-machine, content ds78-chest-flies-machine), a topic `pinned_comment` question from the transcript. Verify hashes, TikTok frame zero, YouTube cover, Facebook cover registry and live installer. Use the organic guard and `organic_short_queue.py`.
4. **Schedule from the live queue** in a phase 3 slot on all four platforms, or the shared waitlist with the `gym` flag if Blotato is full. Never a per-video routine. Re-read saved schedules before reporting.
5. **Record** cover files and hashes, three-copy verification, media URLs, metadata, the four schedule IDs or the waitlist state, in `Docs/DS78_SETUP_RECEIPT_<date>.md`. Keep the job finalized until setup earns "uploaded". No Google Ads, no Victory Dashboard.

## Starter prompt

How To Do Chest Flies On SFC Setup. Read `Handoffs/handoff-20261109-ds78-chest-flies-machine-cover-and-setup.md` and execute it with `/video-setup`. Preserve my finalized R1 film byte for byte. Try the Google AI subscription first for the images and keep the required Codex subscription choices. Make five distinct cover choices plus the three unlabeled Google options, in both Instagram and YouTube layouts, stop for my pick, then complete upload and scheduling in a January-blitz Short slot.
