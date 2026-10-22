# CONTENT, long-form: What To Buy For Your Health LFC Setup (video 3)

Written 2026-10-21 by Claude (Opus 5.5) at the end of round 6. Sidebar name: **What To Buy For Your Health LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (thumbnails, titles and descriptions are editorial; the queue steps are checklist).
**Use the Codex subscription to generate the images.** Every generated still uses
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

"What To Buy For Your Health At Every Income Level" (RO-20C), part 3 of the three-film "Invest In Your Health" series.
Parts 1 and 2 ("Why You Should Invest More In Your Health" RO-20, "What To Cut To Afford Getting In Shape" RO-20B) have their own
setup handoff, `handoff-20261020-ro20-ro20b-thumbnails-and-video-setup.md`. Check its state first (board entry `RO-20/B`, the live
Blotato queue): this film releases in the slot right after part 2.

**Ready now.** Dan, 2026-10-21: *"All changes look good. Let's proceed to set up. This is finalized and approved."* Queue state
`finalized`. Approval record: `approval-round6.json` in the delivery folder.

## Exact approved file (never edit it; re-hash before setup)

- `claude edited long form content/20 - What To Buy For Your Health At Every Income Level/What To Buy For Your Health At Every Income Level | claude round 6 | 16x9 | RO-20C.mp4`
  sha256 `933e5af24171b53a2abd81a7ed75d7328f65498f4b54301c32e68e0070fd22fd`, 29:40.9, 53,374 frames, 2.54 GB.
- Same folder: `.srt` (upload, never burn in), `.chapters.txt`, `notes-RO20C-round6.md`, gate stamps. The file exceeds the 400 MB
  Blotato cap: make an upload derivative per `/video-setup`, keep the master untouched.
- The film carries several AI clips labelled AI-GENERATED on screen (the three intro tiles, the cardboard-box man, two excuse-voice
  characters, and others from round 4): the YouTube AI-content disclosure applies.
- Ending: "I'll see you in the next video." (organic; confirm with setup Step 0).

Chapters: 0:00 What To Buy For Your Health At Every Income Level, 0:27 If You're Dead Broke, 2:57 Middle Class: The Best Protein,
5:36 A Better Mattress, 8:54 A Membership At The Best Gym, 10:54 A Sleep Tracker, 12:18 GLP-1 Medication, 15:04 TRT,
16:13 Supplements, 18:38 Over $10,000 A Month: A Home Gym, 21:14 A Meal Prep Service Or A Personal Chef, 22:52 A Maid And A Laundry
Service, 23:31 A Personal Trainer And Nutritionist, 25:07 Beyond The List, 26:47 Summary, 28:36 Your First Step.

## Read before work

Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails section, release cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`Docs/LONGFORM_RELEASE_CALENDAR.md`. Run setup Step 0 (classify from its own ending) and `python3 scripts/blotato/ad_guard.py --scan`
before and after Blotato changes.

## Five thumbnail choices, then STOP for Dan's pick

VIDEO-RULES "Thumbnails: the five": one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated Dan, two AI
images of Codex's choice; each its own design. Real photos are never redrawn (cutout + generated background + type in code). No claims on
the thumbnail (memory `thumbnail-no-claims`). The film's strongest pictures: the three-tier contrast in the intro (homeless Dan deadlifting
on Skid Row, a salmon dinner at home, a mansion home gym); approved AI frames for reference are in
`/Volumes/Extreme/_edit_work/ro20/round6/frames/` (I1, I3) and `/Volumes/Extreme/_edit_work/ro20/round5/frames/` (I2), and library clips
`ai-dan-skid-row-kettlebell-deadlift`, `ai-dan-salmon-dinner-cutting`, `ai-dan-mansion-home-gym-curl`. Show all five on one sheet, stop.

## After the pick

`/video-setup`: title, description with chapters and the UTM link, links to parts 1 and 2 (their watch URLs once public; until then the
description says they are earlier in the series and the link is added after release), tags, pinned question comment (`"pinned_comment"`
in the Blotato config), upload Private, AI disclosure, SRT.

**Schedule.** Dan putting the series into setup brings RO-20/B/C back onto the calendar (the RO-20/B handoff records the same reading).
Long-forms release Sunday and Wednesday 9 AM CT, one per day, YouTube first, the other platforms the next day at noon after YouTube is
verified public. Read the live Blotato queue (`scripts/blotato/longform_queue.py`), not a receipt. This film takes the long-form slot
right after part 2 (the RO-20/B setup reserves it in the calendar if it got that far); if part 2 is not scheduled yet, keep the order
1, 2, 3 on consecutive long-form slots. Every edited film releases in 2026: if no 2026 slot is free, tell Dan in one line before using
2027. If Blotato is full, put it on `scripts/blotato/video_waitlist.json` with its date; the daily top-up routine queues it. Update the
calendar file. Shorts from this film (3, per the Shorts calendar) are a separate `/shorts` job (`SFL`), not part of this task.

## Close out

Edit Queue: `python3 scripts/edit-queue/queue.py set RO-20C uploaded` after upload, mirror to the Edit Queue page. Setup receipt in
`Docs/RO20C_SETUP_RECEIPT_<date>.md`. One board entry while it waits on release.

## Starter prompt

> CONTENT (LFC). Name this task `What To Buy For Your Health LFC Setup`. Execute `Handoffs/handoff-20261021-ro20c-thumbnails-and-video-setup.md`:
> set up "What To Buy For Your Health At Every Income Level" (RO-20C), part 3 of the Invest In Your Health series. Use the Codex
> subscription to generate the images. Make the five thumbnail choices and stop for my pick, then upload and schedule it in the slot
> right after part 2. Recommended: Claude Opus 5.5, high effort.
