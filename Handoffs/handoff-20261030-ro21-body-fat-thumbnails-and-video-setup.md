# CONTENT, long-form: Body Fat % LFC Setup

Written 2026-10-30 by Claude (Opus 5.5) at the end of round 4. Sidebar name: **Body Fat % LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (the film started on Claude). **Use the Codex subscription to generate the images.**
Codex stills use `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. **Google image variations are also required (Dan, 2026-10-30): see the thumbnail section.**

"What Every Body Fat Percentage Looks Like (On Me)" (RO-21), 10/15 green-screen roll C1724. **Dan approved round 4 on 2026-10-30; fire any time.** Edit Queue: `finalized`.

## Exact file (never edit it; re-hash before setup)
- `claude edited long form content/24 - What Every Body Fat Percentage Looks Like (On Me)/What Every Body Fat Percentage Looks Like (On Me) | claude round 4 | 16x9 | RO-21.mp4`
  sha256 `81d2c035c87580dcc3cffcb79d463f30c763b90f83d5ddbb43f7ec8f6afbee6b`, 7:27.4, 13,410 frames, 441 MB (over the 400 MB Blotato cap: make an upload derivative per `/video-setup`, low priority).
  Same folder: `.srt` (upload, never burn in), `.chapters.txt`, gate stamps, `recipe-RO-21-r4/ROUND-4-REVIEW.md` (independent SHIP). Work files: `/Volumes/Expansion/_edit_work/RO-21/round4/`.
- Gates: delivery 38 of 39, the one fail is `audio:stamp` from the audio gate's `tone` row, Dan's chosen voice A with the bass lift. The same row failed on round 3 and he approved it. Loudness -14.3 LUFS, true peak -1.8.
- Disclosure: AI footage carries AI-GENERATED: scale clip (0:16 to 0:20), sleeping clip (5:19 to 5:24), and AI still pictures throughout (ladders, level cards, TV, floating cards). The set behind Dan is an AI picture and carries its label. YouTube altered/synthetic disclosure and the TikTok AI flag apply. The one real photo (6:37) carries "Real photo of me, not AI-generated". Music is the cleared Pixabay bed, no attribution needed. Organic: drug names are fine.
- Chapters: 0:00 Every body fat level on me, 1:01 35% body fat, 2:02 30% body fat, 2:47 25% body fat, 3:25 20% body fat, 4:06 15% body fat, 4:43 12% body fat, 5:34 10% body fat, 6:01 8% body fat, 6:42 Recap: your next step at every level.
- Ending line: "Find your level, then start on its action step today." There is no subscribe or website call to action on camera. Confirm with setup Step 0 (organic content, not an ad).
- Title note: a dedicated Short, "What Every Body Fat Percentage Looks Like" (DS-06), already exists. Keep "(On Me)" or another clear difference so the two do not read as the same video.

## Read before work
Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails, release cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md` (including "Blind Google test"),
`.claude/skills/_shared/blind-image/FLOW-IMAGE-RUNBOOK.md`, `Docs/LONGFORM_RELEASE_CALENDAR.md`, memory `cover-picks-ai-dan-acting-topic`.
Worked example of a blind set: `Docs/DS43_COVER_REVIEW_20261030.md`.

## Eight thumbnail choices: five Codex plus three Google, then STOP for Dan's pick
Dan, 2026-10-30: "Make sure that includes Google image variations in addition to Codex."
- **Five Codex designs,** VIDEO-RULES "Thumbnails: the five" (2026-10-25 mix): two distinct AI images of Dan acting out the topic, one real photograph from the pool OR studio shoot, two concepts at Codex's discretion guided by Dan's actual approved-cover history; each its own design. Inspect recent picks first.
- **Three Google designs,** made in Google Flow on Dan's Google AI Ultra subscription with Nano Banana Pro, never the paid API: extra designs following the same mix and pick-history guidance, not copies of the five. Use the same real identity reference photos. Run it as a background sub-agent per the runbook so the task keeps moving. Say the Codex and Google image counts in one line before the batch.
- **Blind, always:** build the set with `_shared/blind-image/blind.py` (`add`, `build`, `pick`). All eight shuffled together, labelled X1 to X8. Never say or hint which came from where, in chat, on the page, in file names or in the receipt shown to Dan. Log his pick with `blind.py pick` and install the winner from its original, never the normalized copy.
- **Refusals are data.** If Google refuses a shirtless image, write it to `google-refusals.txt` in the set folder, one retry with the plain prompt at most, never reword around the filter. Show what exists; Codex's five go forward regardless.
- Real photos are never redrawn and stay out of the Google test. Inspect every AI Dan face. No claims, no frowning Dan, text off face and hair. Show all choices on one page, stop for the pick.
- The film's strongest idea is the promise in the title: every level, on him, and finding yours. The eight-picture ladder that opens the film is the proven visual; a thumbnail still has to read on a phone, so do not shrink it to eight tiny men.

## After the pick
`/video-setup`: title, description with chapters and UTM link, tags, pinned question comment, AI disclosure, SRT. Calendar: **YouTube Wed Dec 30 2026, 9 AM America/Chicago** (`Docs/LONGFORM_RELEASE_CALENDAR.md`, phase 3, the January blitz); Facebook, Instagram and TikTok Thu Dec 31 at noon once YouTube reads public. Read the live Blotato queue first (`scripts/blotato/longform_queue.py`); if it is full, use `scripts/blotato/video_waitlist.json` with the same date and `kitchen: false`. Never upload Public. Update the calendar row ("needs editing", "Not booked").
Studio film, no kitchen footage. Shorts from this film (3) are a separate `/shorts` job (SFL): register it at setup, never before the parent is public.

## Starter prompt
> CONTENT (LFC). Rename this task `Body Fat % LFC Setup`. Read `Handoffs/handoff-20261030-ro21-body-fat-thumbnails-and-video-setup.md` and set up "What Every Body Fat Percentage Looks Like (On Me)" (RO-21). Use the Codex subscription to generate the images, and add the three Google image variations in Flow as the handoff says. Opus 5.5, high effort.
