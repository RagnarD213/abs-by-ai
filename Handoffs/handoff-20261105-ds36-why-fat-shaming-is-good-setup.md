# CONTENT SFC: Why Fat Shaming Is Good setup

**Executed November5, 2026:** M1 approved, all four platforms scheduled and verified for December22, 2026 at9AM Central. Receipt: `Docs/DS36_SETUP_RECEIPT_20261105.md`.

**Task name: Why Fat Shaming Is Good SFC Setup. Start in Claude Opus 5.5, high effort.**
**Use the Codex subscription to generate the images.**

Dan finalized the R2 off-the-cuff Short on November 5, 2026: "Approve as final". He then set its title: "Give me a handoff or setup with the title 'Why Fat Shaming Is Good' for the video." **The title is "Why Fat Shaming Is Good"** (YouTube title and the copy on every cover). The planning name was "Bill Maher Says Fat Shaming Should Come Back. He's Right." (DS-36); do not use it as the title.

Execute one `/video-setup` task: make the cover choices, stop for his pick, then finish upload and scheduling. The edit is finished. Do not rebuild, recolour or reprocess the audio.

## Exact approved file

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/Fat Shaming - DS-36/Fat Shaming SFC R2 - off the cuff.mp4` (the project folder name is a link to `/Volumes/Expansion/_internal-offload-20261031/Short-form video content/`)
- SHA-256 `afd220fd50a3032ef65be251fa4eb9de2bd9ac2cedfa6192971f26b98993ea46`; 59.126 s; 1772 frames; 1080x1920; 30000/1001 fps. Captions burned in; sidecar `Fat Shaming SFC R2 - off the cuff.srt` beside it.
- Verified identical backup: `/Volumes/Extreme/Short-form video content/Fat Shaming - DS-36/`.
- Approval: `Handoffs/video-editing/DS-36-R2-approval.json` (also `dan-approval-20261105.json` beside the master).
- Work and evidence: `/Volumes/Expansion/_edit_work/DS-36/r2/` (round 1 both versions in `r1/`). Independent review `r2/offcuff/ROUND-2-REVIEW.md` (copy beside the master).
- Google Drive backup is NOT done. Upload and verify it under `Short-form video content/Fat Shaming - DS-36/` (anyone with the link can view) and return the link.

## What is in the film

Reaction Short, locked Codex R5 format, studio green screen (10/15 roll C1730, off-the-cuff take). Bill Maher, Real Time (HBO), "New Rule: The Fudge Report" (YouTube Dm4TAdiEFn0, 5:55-6:11 with his littering/racism sentence cut) plays first, full screen with Dan watching lower left, then the titled panel "Bill Maher | Real Time (HBO)". Dan's reply at 1.12x (pitch kept), colour look B. Cutaways: AI clip A0197 (man on a bathroom scale, labelled AI-GENERATED, 0:23-0:25) and Dan's real dumbbell curls by the pool (B0432). Lower thirds: THE TRUTH / Shaming Others Changes Nothing; THE RULE / 3 Pounds Over? Feel The Shame; THE POINT / Feel It, Then Fix It; subscribe card.

Checks: independent reviewer found no remaining defects (build 5). Watch judge 0 defects. Delivery gate 2.6.3 raw FAIL on two known rows only (36 pass): `audio:stamp` (Bill's clip sound inside the tone window; Dan's voice alone passes every row) and `framing:hair_top` (planned hair overlap on the panel). `captions:sync` not measurable by the gate; reviewer measured every cue within 0.23 s.

## Classification

**Organic dedicated Short.** Ending: "So subscribe and go to SixPackAbs.com for all my latest videos." No button CTA. **It contains realistic AI moving footage (the scale clip), so set YouTube's altered/synthetic flag and TikTok's AI flag to true** (VIDEO-RULES, "AI label on uploads").

## Read first

AGENTS.md (Shorts release cadence 2026-10-28), full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `/youtube-packaging`, `.claude/skills/_shared/IMAGE-GENERATION.md` (including "Blind Google test"), `Docs/SHORTS_RELEASE_CALENDAR.md`, `Docs/PINNED_COMMENTS.md`, `Docs/memory/cover-picks-ai-dan-acting-topic.md`.

## Execute one setup task

1. Verify the master hash, approval, SRT and both copies. Finish and verify the Drive backup. Setup takes no edit slot. Keep DS-36 `finalized` until schedules are read back.
2. Inspect recent approved-cover `picks.json` files and their selected images before planning. Five genuinely different Codex designs with the copy "Why Fat Shaming Is Good" (title capitalization on every word): two distinct AI images of Dan acting out the topic (for example Dan stepping on a bathroom scale and frowning at a number just over his goal, Dan doing a standing stomach vacuum at a bathroom mirror), one real pool OR studio photo, two history-guided choices. Plus three unlabeled Google options, all eight shuffled with neutral labels (blind test; `blind.py`).
3. **Use the Codex subscription to generate the images:** `.claude/skills/_shared/codex-image.sh`, newest supported stable GPT at high effort (currently `gpt-6.1-sol`). Real photo pixels preserved; real identity reference for AI Dan, "lean and shredded, not bulky, same size as the reference"; check every face.
4. Show all eight with **both Instagram and YouTube layouts**, then STOP for Dan's pick (`blind.py pick`). A revised pick is shown again before installing.
5. After the pick: title "Why Fat Shaming Is Good", description, tags, organic URL/UTMs, an easy question in `pinned_comment`, cover URLs, TikTok cover-first copy, cover and ad-guard audits. Blotato releases YouTube; no direct or native-scheduled YouTube upload. Synthetic/AI flags true (above).
6. Date: **Tue Dec 22, 2026, 9 AM America/Chicago** (Dan approved the slot 2026-10-28; `Docs/SHORTS_RELEASE_CALENDAR.md` row "Tue Dec 22 | 2 | 9 AM", currently "Not booked"; phase 2, studio footage, not kitchen). Read the LIVE Blotato queue and `scripts/blotato/video_waitlist.json` first. If the queue is full, add it to the shared waitlist for that slot; never create a single-video routine. Update the calendar row when booked.
7. Save a setup receipt (`Docs/DS36_SETUP_RECEIPT_<date>.md`) with hashes, three copies, metadata, media URLs, pinned question and schedule IDs read back (or the waitlist entry). Mark DS-36 `uploaded` only after schedules exist. No Google Ads work.

## Starter prompt

Why Fat Shaming Is Good SFC Setup. Read `Handoffs/handoff-20261105-ds36-why-fat-shaming-is-good-setup.md` and execute it using `/video-setup`. Use the Codex subscription to generate the images. Set up only my approved R2 off-the-cuff master (sha256 afd220fd...ea46) with the title "Why Fat Shaming Is Good": back it up to Drive, make the five Codex cover designs plus three unlabeled Google options with Instagram and YouTube layouts, and stop for my pick. After my pick, write the metadata with the AI flags on, then schedule it through Blotato for Tue Dec 22, 2026 at 9 AM Central or put it on the shared waitlist for that slot, and save the setup receipt.
