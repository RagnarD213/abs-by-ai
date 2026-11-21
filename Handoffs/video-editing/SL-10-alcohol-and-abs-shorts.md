# SL-10: Shorts from "Can You Drink Alcohol And Still Have Abs?" (RO-13, Claude round 2)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-05 when RO-13 was set up for release.

## Source
`claude edited long form content/11 - Can You Drink Alcohol And Still Have Abs/Can You Drink Alcohol And Still Have Abs | claude round 2 | 16x9 | RO-13.mp4`
(7:10.63, 1920x1080, SHA-256 `2296902bf3667c6c6bd30255a4f3155988ddb3a4f38bf5a95ad5d985f10751c0`). Copies on the Extreme drive
(`/Volumes/Extreme/Claude Content Videos/Can You Drink Alcohol And Still Have Abs - RO-13/`) and Google Drive. The `.srt` and
`.chapters.txt` are beside it. This is OUR render, so it is a CONTENT long-form (LFC): it gets Shorts and nothing else.

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out, why it
  stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates** (`_shared/VIDEO-RULES.md`, 2026-10-01).
* Every short gives the viewer a tactic, stands alone, 45-60 s, full-frame 9:16, word-timed captions, steady framing (the standard
  centering in `framing-motion.md`), cuts snapped to silence. Benefit-first titles.
* No covers in this job: covers are made in the setup task.
* **Do not upload or queue.** A short never posts before its parent is public (Wed Oct 21 2026, 9 AM CT).

## This video's specifics
* Natural shorts by chapter: the 4 things alcohol does (0:43 to 2:15), Eat First (2:15 to 2:34, pair with Run Your Normal Fast 4:59 to 5:28),
  Count The Calories + photo your drink (2:34 to 3:04), Kill The Sugary Mixers and "it should taste bad" (3:04 to 3:41), Cap Your Nights
  and the nightly glass of wine (3:41 to 4:21), Stop 3 Hours Before Bed (4:21 to 4:59), How I drink now (6:07 to 6:51). Expect 4 to 5.
* The film contains realistic AI clips (pool-cookout opener 0:00 to 0:03.1, bathroom-mirror clip 0:20.4 to 0:24.2) labelled on screen:
  `ai_generated: true` at setup for any short that uses one. Avoid the mirror clip (a belly-adjacent framing) in the first 30 seconds of a short.
* Shorts stand alone: when a short names a tactic, show it briefly (the photo-your-drink tip needs the app moment, not just the line).
* Zepbound is named at 6:33 to 6:50. Organic may name the drug; keep "talk to your doctor" wording from the long-form.
* The ending of the long-form is a subscribe line; a short ends on its own tactic.

## Deliver
`Short-form video content/alcohol-short<N>_<title>.mp4` (1080x1920) + stamps, and an `alcohol-SHORTS.md` listing each short's in/out,
title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-10-alcohol-and-abs-shorts.md`: propose the shorts segments from "Can You Drink Alcohol And Still Have Abs?" (RO-13) and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers). Deliver, send me the review copies, update the master list. Name this session "Alcohol And Abs SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-10-alcohol-and-abs-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-13 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Alcohol And Abs SFC R1".
