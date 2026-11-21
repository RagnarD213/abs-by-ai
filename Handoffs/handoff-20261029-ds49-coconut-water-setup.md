# CONTENT SFC: Why I Stopped Drinking Coconut Water setup

**Task name: Coconut Water SFC Setup. Start in Claude Opus 5.5, high effort.**
**Use the Codex subscription to generate the images.**

Dan finalized the complete R2 film on October 29, 2026: "Finalize it". Execute one `/video-setup` task: make five cover choices, stop for his pick, then finish upload and scheduling. The edit is finished. Do not rebuild the film, recolour it, reprocess its audio or swap its clips.

## Exact approved file

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/Coconut Water - DS-49/Coconut Water SFC R2 - complete Short.mp4`.
- SHA-256: `40e0c4d5a2fd4f6daa8a31124b87da0e705120eff76045ef20eb30fc89d342b0`; 50.617 s; 1080x1920; 30000/1001 fps.
- Subtitles: `Coconut Water SFC R2 - complete Short.srt` beside it (captions are already burned in).
- Verified identical backup: `/Volumes/Extreme/Short-form video content/Coconut Water - DS-49/`.
- Approval: `Handoffs/video-editing/DS-49-R2-approval.json` (also `dan-approval-20261029.json` beside the master).
- Work and evidence: `/Volumes/Extreme/_edit_work/DS-49/round2/` (round 1 preserved in `round1/` and the review archives).
- Google Drive backup is NOT done yet. Upload and verify it under `Short-form video content/Coconut Water - DS-49/` (anyone with the link can view) and return the link.

## What is in the film

Scripted take only (no off-the-cuff take was filmed). Dan on camera at the pool (10/15 roll C1759), colour V Deeper And More Vivid, voice B Fuller Bass, crop 1 Original Portrait. Pexels cutaways: cola over ice (library B0401), a man on a treadmill who wipes his forehead (6454301), a packet of coloured drink powder into water (6845784), juice poured into a glass (5538293). Soft Blue HyperFrames: card "Coconut Water / What's In A 1-Liter Bottle / About 180 Calories / Almost 40 g Of Sugar" with an AI-generated 1 L bottle photo in the top third (AI-GENERATED chip), card "The Study / Plain Water Hydrated Just As Well", bar "To Lose Belly Fat / Healthy Drinks Still Count".

Checks: independent review SHIP; watch judge 0 defects; delivery gate 2.6.2 raw FAIL on four known rows only (35 pass): `audio:stamp` (standard bass-lift tone row), `framing:headroom` and `framing:no_wide_level` (approved full-portrait framing), `captions:burned` (detector; captions confirmed on 12 of 12 sampled frames). No threshold changed. Do not claim a technical PASS or repair the approved film.

## Classification

**Organic dedicated Short.** Ending: "Subscribe to my channel and go to sixpackabs.com for more nutrition tips." No button CTA. No realistic AI moving footage; the only AI element is a still product photo on a graphic, which does not trigger the YouTube/TikTok synthetic-media flags (VIDEO-RULES, "AI label on uploads"). Pool footage, not kitchen: allowed in every release phase.

## Read first

AGENTS.md (Shorts release cadence 2026-10-28), full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, IMAGE-GENERATION.md, `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, `Docs/memory/cover-picks-ai-dan-acting-topic.md`.

## Execute one setup task

1. Verify the master hash, approval, SRT and both copies. Finish and verify the Drive backup. Setup does not take an edit slot. Keep DS-49 `finalized` until schedules are read back.
2. Inspect recent approved-cover `picks.json` files and the selected images before planning. Make five genuinely different designs: **two distinct AI images of Dan acting out the topic** (for example Dan by the pool pushing away a big coconut water bottle, Dan holding a coconut water bottle beside a can of Coke), **one real pool OR studio photo**, **two history-guided Codex choices** (may be more AI Dan). Same headline across the set; Title Case on every word.
3. **Use the Codex subscription to generate the images:** `.claude/skills/_shared/codex-image.sh`, newest supported stable GPT at high effort (currently `gpt-6.1-sol`). Real photo pixels preserved; real identity reference for AI Dan, "lean and shredded, not bulky, same size as the reference"; check every face; text off face and hair.
4. Show all five with **both Instagram and YouTube layouts**, then STOP for Dan's pick. A revised pick is shown again before installing.
5. After the pick: title, description, tags, organic URL/UTMs, an easy question in `pinned_comment`, cover URLs, TikTok cover-first copy, cover and ad-guard audits. Blotato releases YouTube; no direct or native-scheduled YouTube upload.
6. Date: read the LIVE Blotato queue, `scripts/blotato/video_waitlist.json` and `Docs/SHORTS_RELEASE_CALENDAR.md`, then pick the next free Short slot of the current phase (`scripts/blotato/release_phases.py`: phase 1 Mon/Tue/Thu/Fri/Sat 9 AM to Nov 25; phase 2 two a day; phase 3 9 AM and 6 PM Mon/Tue/Thu/Sat). Keep it well apart from "3 Healthy Foods 1: Coconut Water Is Just Sugar Water", already waitlisted Mon Dec 14 (same topic). If Blotato is full, use the shared waitlist and the daily top-up; never a per-video automation. Bring Dan one date if the calendar forces a trade-off.
7. Save a setup receipt (`Docs/DS49_SETUP_RECEIPT_<date>.md`) with hashes, three copies, metadata, media URLs, pinned question and schedule IDs read back (or the waitlist entry). Mark DS-49 `uploaded` only after schedules exist. No Google Ads work.

## Starter prompt

Coconut Water SFC Setup. Read `Handoffs/handoff-20261029-ds49-coconut-water-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Set up only my approved R2 master of "Why I Stopped Drinking Coconut Water". Make five distinct cover choices in both Instagram and YouTube layouts, stop for my pick, then complete the Drive backup, upload and scheduling in the next free Short slot, kept apart from the other coconut water Short on Dec 14.
