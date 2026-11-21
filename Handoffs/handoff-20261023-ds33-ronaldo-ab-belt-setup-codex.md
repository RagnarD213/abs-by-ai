CONTENT: Ronaldo Ab Belt SFC, approved R5, covers and setup. **Codex task** (Dan, 2026-10-23: "Make both handoffs for Codex").

Task name: **Ronaldo Ab Belt SFC Setup**. Recommended model: **GPT-6.1 Sol, high effort** (newest available GPT; verify the catalog when starting, per AGENTS.md). Written October 23, 2026.

**Use the Codex subscription to generate the images.** In this Codex session, make the images with Codex's own image generation on Dan's ChatGPT subscription (the same path `.claude/skills/_shared/codex-image.sh` wraps for Claude). No paid API, no Gemini or other outside model. One task: five cover choices, one review sheet, **stop for Dan's pick**, then complete organic setup. Worked example of the same job: DS-31 AI Homework (`Handoffs/handoff-20261020-ds31-ai-homework-setup.md`, which follows DS-28 Meal Prep: `Handoffs/handoff-20261017-ds28-meal-prep-setup.md`, receipt `Docs/DS28_SETUP_RECEIPT_20261017.md`, config `scripts/blotato/configs/ds28-meal-prep.json`). Follow it; differences below. Codex has no `/video-setup` skill: read `.claude/skills/video-setup/SKILL.md` in full and follow it with Codex tools.

## Exact approval and files

Dan approved R5 on October 23: "Okay, looks good. This is approved. Give me the handoff or setup." State: **finalized, not uploaded**. Approval: `Short-form video content/Ronaldo Ab Belt - DS-33/APPROVAL.json` (copy on Extreme and `Handoffs/video-editing/DS-33-R5-approval.json`); regression corpus entry `ds33-r5-approved-20261023`.

Project delivery folder: `Short-form video content/Ronaldo Ab Belt - DS-33/`
- Upload master: `Ronaldo Ab Belt SFC R5 - complete Short.mp4`, **62,004,027 bytes**, SHA-256 `b78674a331cd51c6003614ea149dc89095fc1e2539406a0826a5a100f65e80d0`. 1080x1920 H.264/AAC, 1867 frames at 30000/1001, **62.30 s** (under the 66 s ceiling).
- SRT: `Ronaldo Ab Belt SFC R5.srt`. The Short ends on "...for all my newest videos." (0:59-1:01.8; the G04 tag reads "Subscribe & Visit SixPackAbs.com").
- Backup: `/Volumes/Extreme/Short-form video content/Ronaldo Ab Belt - DS-33/` (hash-identical). Evidence: `/Volumes/Expansion/_edit_work/DS-33/r5/` (gate stamps, `ROUND-5-REVIEW.md` SHIP, recipe).
- Older R1-R4 masters in the folder are NOT the upload. Upload only the R5 master; verify the hash first.

## Preserve the final film

The locked reaction format: the Cristiano Ronaldo SIXPAD ad full screen with Dan keyed lower left (0.40, laptop), then the ad silent in a full-width card behind his head (hair overlapping its bottom ~10%), Soft Blue Light, Warm colour, Balanced voice. Do not change the film, thresholds or stamps. Delivery gate 2.6.1: 35 PASS, 4 FAIL (locked voice tone, legacy caption sync, two framing rows where the gate reads the ad's people as Dan's hair); independent review SHIP.

**No AI footage in this Short: `ai_generated: false`, YouTube altered/synthetic OFF.** It contains a third-party ad clip (Ronaldo's SIXPAD commercial) used for reaction/commentary.

## Title and topic

- **Upload title (Dan, 2026-10-22, exact):** "Does Cristiano Ronaldo's Electric Shock Ab Belt Work?"
- Topic: Ronaldo sells an electric ab belt (EMS) that shocks your abs. Dan's take: the belts can build ab muscle, but shocking yourself hard enough is harder than just working out, so there is no saved effort; and no belt burns the belly fat covering your abs. Use the approved words and SRT; no invented personal facts. No em dashes in any title, description, cover or comment.
- Covers: Ronaldo is a real person: an AI cover option shows the belt or the idea, not a fake Ronaldo likeness; a real frame of the ad from the film is fine where it reads as the reaction. Text off Dan's face and hair; masculine palettes.

## Execute

Steps of the DS-31 / DS-28 handoffs with DS-33 names:
1. Verify hashes; confirm no other DS-33 setup owner on `AI_COORDINATION.md` or `Handoffs/README.md`; add a one-line board entry.
2. Five unique covers (VIDEO-RULES first section): one real pool photo, one real studio photo, one AI-enhanced or AI-generated Dan, two AI images of your choice; each in its Instagram and YouTube layouts; one line per option naming its design before building. Real photos of Dan are never redrawn (background only, his cutout and type layered in code: `.claude/skills/_shared/IMAGE-GENERATION.md`). One numbered review sheet on a `review_server.py` page; **stop for Dan's pick.** A pick with a revision is shown again before install.
3. After the pick: Google Drive copy in `gdrive:Short-form video content/Ronaldo Ab Belt - DS-33/`, anyone-with-link, hash-verified; TikTok cover-first copy with the maintained helper; title, description, tags, `https://absbyai.com` link and UTMs, one easy `pinned_comment` question in Dan's voice (`Docs/PINNED_COMMENTS.md`).
4. Config `scripts/blotato/configs/ds33-ronaldo-ab-belt.json` (`"content_type": "organic"`, exact `"source"`, `"ai_generated": false`, cover URLs, pinned question). `scripts/blotato/ad_guard.py --scan` and `cover_audit.py` before and after; Facebook cover registry.
5. Queue on the **next free dedicated-Short Thursday, 9 AM America/Chicago** (`Docs/SHORTS_RELEASE_CALENDAR.md`; the dated table runs to Dec 28, so check the live Blotato queue) for YouTube (account 46963), Facebook, Instagram **@danrosefit** and TikTok, `organic_short_queue.py` dry-run then `--apply`; read every post back. If Blotato is full, finish everything else and add one `kind: short`, `job: DS-33` entry to `scripts/blotato/video_waitlist.json` (the daily top-up routine queues it; never a per-video scheduled task). Add the Short to the calendar doc.
6. Receipt `Docs/DS33_SETUP_RECEIPT_<date>.md`. `python3 scripts/edit-queue/queue.py set DS-33 uploaded` only when all four posts read back; commit the jobs change so the next Claude session mirrors it to the Edit Queue page. Delete your board entry when done.

Read first: `AGENTS.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/video-setup/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, `Docs/PINNED_COMMENTS.md`, `Handoffs/handoff-20260914-ad3-square-codex.md` §2 (Codex environment traps: quoted paths, project ffmpeg). Git: commit docs/configs only, never media (public repo); follow the Codex branch rule in `Handoffs/codex-video-trial/00-start-here.md`.

## Finalization housekeeping already done (Claude, 2026-10-23)

Approval recorded (project + Extreme `APPROVAL.json`, `Handoffs/video-editing/DS-33-R5-approval.json`, corpus entry). Master and SRT hash-identical on Extreme. `Videos to Review` copy deleted; review services 9033-9037 retired. Queue state `finalized` (Edit Queue page mirrored); edit slot released. No covers, uploads or Drive filing done yet.

## Note: no off-the-cuff version exists

Dan asked for an off-the-cuff edit too. The 10/15 rolls hold no off-the-cuff Ronaldo take (all rolls transcribed: only the scripted takes C1727/C1728/C1729 and the watching take on C1730; the off-the-cuff run only starts later on C1730 at 448 s, with the dad bod video). So nothing is on hold: this setup proceeds with the scripted R5 Short.

## Ready-to-paste starter prompt (Codex)

CONTENT: Name this chat Ronaldo Ab Belt SFC Setup. Read Handoffs/handoff-20261023-ds33-ronaldo-ab-belt-setup-codex.md and follow .claude/skills/video-setup/SKILL.md for the finalized Ronaldo Ab Belt R5 Short ("Does Cristiano Ronaldo's Electric Shock Ab Belt Work?"). Use the Codex subscription to generate the images. Make five unique cover choices, show me one numbered review sheet and stop for my pick. After my pick, preserve the exact approved film, finish the backups, and set it up through Blotato for YouTube, Facebook, Instagram @danrosefit and TikTok on the next free Thursday dedicated-Short slot. Verify the covers, saved schedules and pinned question. Use the shared waitlist if full. No extra formats or new edits.
