# CONTENT SFC: How To Do Bodyweight Squats setup

**Task name: Bodyweight Squats SFC Setup. Start in Claude Opus 5.5, high effort.**
**Use the Codex subscription to generate the images.**

Dan finalized the R2 Short on November 4, 2026: "Approved". Execute one `/video-setup` task: make the cover choices, stop for his pick, then finish upload and scheduling. The edit is finished. Do not rebuild, recolour or reprocess the audio.

## Exact approved file

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/How To Do Bodyweight Squats - DS-61/Bodyweight Squats SFC R2 - DS-61 - 1080p.mp4`
- SHA-256: `29db177a2a910dd324fe65f9d79d9ec2c1b7b772c52731bc9a071e58397a8250`; 45.078 s; 1080x1920; 30000/1001 fps. Captions are burned in; sidecar `Bodyweight Squats SFC R2 - DS-61.srt` beside it.
- Verified identical backup: `/Volumes/Extreme/Short-form video content/How To Do Bodyweight Squats - DS-61/`.
- Approval: `Handoffs/video-editing/DS-61-R2-approval.json` (also `dan-approval-20261104.json` beside the master).
- Work and evidence: `/Volumes/Expansion/_edit_work/DS-61/round2/` (round 1 preserved in `round1/` and the review archives).
- Google Drive backup is NOT done. Upload and verify it under `Short-form video content/How To Do Bodyweight Squats - DS-61/` (anyone with the link can view) and return the link.

## What is in the film

Studio set (10/15 roll C1780), colour B Rich Balanced, voice A Warm Bass Plus, medium full-height crop. Dan's own pool B-roll: squats (C1737) and goblet squats with the kettlebell (C1750). One AI clip (library A0225, Veo 3.1 Fast on the Google subscription): a heavier man in his 50s squats down to a wooden chair on a patio and stands back up, 0:19.3 to 0:25.4, labelled AI-GENERATED. Key-point bars: Beginner Version, The Timer, SixPackAbs.com.

Checks: independent review SHIP (`ROUND-2-REVIEW.md`); watch judge 0 defects; delivery gate 2.6.3 raw FAIL on four known rows only (35 pass): `audio:stamp` (Dan's Warm Bass Plus tone row), `framing:headroom` and `framing:no_wide_level` (forced medium crop, each by a hair on one shot), `captions:sync` (matcher; ordered check paired 51/51 within 20 ms). AI label row passes.

## Classification

**Organic dedicated Short.** Ending: "Subscribe to my channel and go to SixPackAbs.com for all my newest videos." No button CTA. **It contains realistic AI moving footage (the chair clip), so set YouTube's altered/synthetic flag and TikTok's AI flag to true** (VIDEO-RULES, "AI label on uploads").

## Read first

AGENTS.md (Shorts release cadence 2026-10-28), full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, `.claude/skills/_shared/IMAGE-GENERATION.md` (including "Blind Google test"), `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, `Docs/memory/cover-picks-ai-dan-acting-topic.md`.

## Execute one setup task

1. Verify the master hash, approval, SRT and both copies. Finish and verify the Drive backup. Setup takes no edit slot. Keep DS-61 `finalized` until schedules are read back.
2. Inspect recent approved-cover `picks.json` files and their selected images before planning. Five genuinely different Codex designs: two distinct AI images of Dan acting out the topic (for example Dan by the pool at the bottom of a deep bodyweight squat, Dan beside a chair showing the beginner version), one real pool OR studio photo, two history-guided choices. Plus three unlabeled Google options, all eight shuffled with neutral labels (blind test; `blind.py`). Title capitalization on every word.
3. **Use the Codex subscription to generate the images:** `.claude/skills/_shared/codex-image.sh`, newest supported stable GPT at high effort (currently `gpt-6.1-sol`). Real photo pixels preserved; real identity reference for AI Dan, "lean and shredded, not bulky, same size as the reference"; check every face.
4. Show all eight with **both Instagram and YouTube layouts**, then STOP for Dan's pick (`blind.py pick`). A revised pick is shown again before installing.
5. After the pick: title, description, tags, organic URL/UTMs, an easy question in `pinned_comment`, cover URLs, TikTok cover-first copy, cover and ad-guard audits. Blotato releases YouTube; no direct or native-scheduled YouTube upload. Synthetic/AI flags true (above).
6. Date: read the LIVE Blotato queue, `scripts/blotato/video_waitlist.json` and `Docs/SHORTS_RELEASE_CALENDAR.md`, then take the next free Short slot of the current phase (`scripts/blotato/release_phases.py`). Studio footage, not kitchen. If the queue is full, add it to the shared waitlist; never create a single-video routine.
7. Save a setup receipt (`Docs/DS61_SETUP_RECEIPT_<date>.md`) with hashes, three copies, metadata, media URLs, pinned question and schedule IDs read back (or the waitlist entry). Mark DS-61 `uploaded` only after schedules exist. No Google Ads work.

## Starter prompt

Bodyweight Squats SFC Setup. Read `Handoffs/handoff-20261104-ds61-bodyweight-squats-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Set up only my approved R2 master of "How To Do Bodyweight Squats" (sha256 29db177a...8250): back it up to Drive, make the five Codex cover designs plus three unlabeled Google options with Instagram and YouTube layouts, and stop for my pick. After my pick, write the metadata with the AI flags on, then schedule it through Blotato in the next free Short slot or put it on the shared waitlist, and save the setup receipt.
