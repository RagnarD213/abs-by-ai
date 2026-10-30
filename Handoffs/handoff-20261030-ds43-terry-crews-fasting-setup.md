# CONTENT SFC: Terry Crews Doesn't Eat Until 2 PM. He's Right. setup

**Task name: Terry Crews Fasting SFC Setup. Start in Claude Opus 5.5, high effort.**
**Use the Codex subscription to generate the images.**

Dan approved the off-the-cuff R2 film on October 30, 2026: "Approve R2". Execute one `/video-setup` task: make five cover choices, stop for his pick, then finish upload and scheduling. The edit is finished. Do not rebuild the film, recolour it, reprocess its audio or swap its clips.

## Exact approved file

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/Terry Crews Fasting - DS-43/Terry Crews Fasting SFC R2 - off the cuff.mp4`.
- SHA-256: `b689924b939651379d3c991f9a3541002ceb1b77f725920a181d3d3dcc7ebda5`; 77.31 s; 1080x1920; 30000/1001 fps.
- Subtitles: `Terry Crews Fasting SFC R2 - off the cuff.srt` beside it (captions are already burned in).
- Approval: `Handoffs/video-editing/DS-43-R2-approval.json`.
- Work and evidence: `/Volumes/Expansion/_edit_work/DS-43/r2/` (round 1 in `r1/`). Recipe: `.claude/skills/shorts/reference/ds43-terry-crews/README.md`.
- Backups are NOT done. Copy it to `/Volumes/Extreme/Short-form video content/Terry Crews Fasting - DS-43/`, upload it to Google Drive under `Short-form video content/Terry Crews Fasting - DS-43/` (anyone with the link can view), verify both by hash and return the link.
- The scripted version in the same folder is NOT being set up. Dan picked off the cuff.

## What is in the film

Reaction Short in the locked format (Bill Maher Codex R5): Terry Crews' Business Insider clip full screen with Dan's corner, then the titled panel with Dan watching (laptop lid visible), then his reply. Silent horizontal clips of Terry shirtless and flexing play above him from 0:15.7 to 0:33.4 (Muscle & Fitness, America's Got Talent, Old Spice), then the moving Soft Blue field. Cutaways: Terry shirtless at the stock exchange (a frame of the Business Insider clip) and stock clip B0317, a restaurant table of steak, bread and wine (real footage). Soft Blue HyperFrames: THE TRUTH / Fasting Does Not Cost You Muscle; WHY IT GETS EASY / Your Body Adapts Over Time; THE TRADE-OFF / Skip Breakfast, Eat A Bigger Dinner; MORE LIKE THIS / Subscribe To My Channel.

Checks: independent review SHIP; watch judge 0 defects; delivery gate 2.6.3 raw FAIL on three known rows only (35 pass), plus `captions:sync` not measured: `audio:stamp` (tone: Terry's clip in the measured window; the same treated voice passed alone on the scripted take), `framing:hair_top` (planned overlap with the panel), `junk:repeated_take` (false alarm: the word "obviously", said once). No threshold changed. Do not claim a technical PASS or repair the approved file. No listening was done by any agent; Dan had the file for review.

## Classification

**Organic dedicated Short.** Ending: "...subscribe to my channel." No button CTA. No AI footage in this version, so no AI label and no synthetic-media flags (the AI clip A0210 was only in the scripted version). Filmed on the green screen, not in the kitchen. **It runs 77.31 s:** check each platform's current limit before upload. Credit the third-party clips the same way recent reaction Shorts (DS-40, DS-44) were credited in their descriptions.

## Read first

AGENTS.md (Shorts release cadence 2026-10-28), full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, IMAGE-GENERATION.md, `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, `Docs/memory/cover-picks-ai-dan-acting-topic.md`.

## Execute one setup task

1. Verify the master hash, approval and SRT. Finish and verify the Extreme and Drive backups. Setup does not take an edit slot. Keep DS-43 `finalized` until schedules are read back.
2. Inspect recent approved-cover `picks.json` files and the selected images before planning. Make five genuinely different designs: **two distinct AI images of Dan acting out the topic** (for example Dan holding back a big breakfast plate while staring at a wall clock on 2 PM, Dan with an empty plate at noon beside a clock), **one real pool OR studio photo**, **two history-guided Codex choices** (may be more AI Dan; do not force object-only designs).
3. **Use the Codex subscription to generate the images:** `.claude/skills/_shared/codex-image.sh`, newest supported stable GPT at high effort (currently `gpt-6.1-sol`). Real photo pixels preserved; real identity reference for AI Dan, "lean and shredded, not bulky, same size as the reference"; check every face; text off face and hair.
4. Show all five with **both Instagram and YouTube layouts**, then STOP for Dan's pick. A revised pick is shown again before installing.
5. After the pick: title, description, tags, organic URL/UTMs, an easy question in `pinned_comment`, cover URLs, TikTok cover-first copy, cover and ad-guard audits. Blotato releases YouTube; no direct or native-scheduled YouTube upload.
6. Date: **Tue Dec 22, 6 PM Central** is the planned slot (`Docs/SHORTS_RELEASE_CALENDAR.md`, phase 2). Read the LIVE Blotato queue and `scripts/blotato/video_waitlist.json` first. If Blotato is full, add one waitlist entry with `kitchen: false`; never create a one-off scheduled task. Update the calendar line once booked.
7. Save a setup receipt (`Docs/DS43_SETUP_RECEIPT_<date>.md`) with hashes, three copies, metadata, media URLs, pinned question and schedule IDs read back (or the waitlist entry). Mark DS-43 `uploaded` only after schedules exist. No Google Ads work.

## Starter prompt

Terry Crews Fasting SFC Setup. Read `Handoffs/handoff-20261030-ds43-terry-crews-fasting-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Set up only my approved off-the-cuff R2 master of "Terry Crews Doesn't Eat Until 2 PM. He's Right." Make five distinct cover choices in both Instagram and YouTube layouts, stop for my pick, then complete the backups, upload and scheduling for Tue Dec 22 at 6 PM Central.
