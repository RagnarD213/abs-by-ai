# CONTENT, long-form: Not Losing Weight LFC Setup

Written 2026-10-22 by Claude (Opus 5.5) at the end of round 3. Sidebar name: **Not Losing Weight LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (the film started on Claude; thumbnails, title and description are editorial).
**Use the Codex subscription to generate the images.** Every generated still uses
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

"Why You're Not Losing Weight" (RO-14), 9/23 studio roll C1708. **Ready now.** Dan, 2026-10-22: *"Okay, everything looks good. This
is approved. Give me the handoff or setup."* Queue state `finalized`. Approval record: `approval-round3.json` in the delivery folder.

## Exact approved file (never edit it; re-hash before setup)

- `claude edited long form content/22 - Why You're Not Losing Weight/Why You're Not Losing Weight | claude round 3 | 16x9 | RO-14.mp4`
  sha256 `14f2a85da15f80b10f2594eec3bb1ecfc29a4d030886e597e0bfb503a8e07e3c`, 8:27.6, 15,212 frames, 2.36 GB.
  Work copy: `/Volumes/Extreme/_edit_work/RO-14/round3/final/RO14_MASTER.mp4` (same hash).
- Same folder: `... | RO-14.srt` (upload, never burn in), `... | RO-14.chapters.txt`, `... | RO-14.edit-sheet.json` (approved),
  gate stamps, `ROUND-3-EDITOR.md`, `ROUND-3-REVIEW.md`. The file is over the 400 MB Blotato cap: make an upload derivative per
  `/video-setup` (hardware encoder exemption), keep the master untouched.
- AI footage on screen, each labelled AI-GENERATED: the broken-scale opener (0:00), a man weighing his plate (1:17), piggy bank
  (1:52), giant drink (2:19), trash-can nuggets (2:38), dessert for two (3:33), the salad guy (4:48), man with a doctor (5:30), donut
  (6:16). The YouTube altered/synthetic disclosure and TikTok AI flag apply.
- Ending (organic): "...Go to absbyai.com and start tracking your calories with AI now. And make sure you subscribe to the channel so
  you don't miss the next video." Confirm with setup Step 0.

Chapters: 0:00 Why The Scale Won't Move, 0:29 The Uncomfortable Truth, 1:03 4 Calorie Leaks, 3:18 The Hidden Reasons, 6:23 My Simple System.

⚠ **A different, live film has a near-identical title:** RO-10 "Calories: The Reason You're Not Losing Weight" (YouTube Sun Dec 27).
Give RO-14 a clearly different title and thumbnail, and link the two in each other's description once both are public.

## Read before work

Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails section, release cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`Docs/LONGFORM_RELEASE_CALENDAR.md`. Run setup Step 0 (classify from its own ending) and `python3 scripts/blotato/ad_guard.py --scan`
before and after Blotato changes.

## Five thumbnail choices, then STOP for Dan's pick

VIDEO-RULES "Thumbnails: the five": one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated Dan, two AI
images of Codex's choice; each its own design, one line per option naming its design before building. Real photos are never redrawn
(cutout + generated background + type in code). No claims on the thumbnail, no frowning photo of Dan, text off his face and hair.
The film's strongest pictures: a man glaring at a bathroom scale he thinks is broken (clip library A0207; approved frames
`/Volumes/Extreme/_edit_work/RO-14/round1/aiframes/A1-start.png`, `A1-end.png`), the hidden calorie leaks (trash-can nuggets, giant
drink, weekend piggy bank smash). Show all five on one sheet, stop.

## After the pick

`/video-setup`: title, description with chapters and the UTM link, tags, pinned question comment (`"pinned_comment"` in the Blotato
config), AI disclosure, SRT. Organic videos are never uploaded to YouTube by us: Blotato creates the public video at release.

**Schedule.** Long-forms release Sunday and Wednesday 9 AM CT, one per day; YouTube first, Facebook, Instagram and TikTok the next day
at noon after YouTube is verified public. Read the live Blotato queue (`scripts/blotato/longform_queue.py`), not a receipt. Calendar
rule for this film: "A film still in editing (RO-17, RO-14, RO-18) that finishes before December takes the 2026 Sunday of the newest
not-yet-edited studio film" (RO-22's Dec 13 went to RO-17; RO-30's Nov 29 went to RO-20B). Every edited film releases in 2026: if the
calendar has no 2026 slot left for it, tell Dan in one line with the options before using 2027. If Blotato is full, put it on
`scripts/blotato/video_waitlist.json` with its date; the daily top-up routine queues it. Update the calendar file.
Shorts from this film (3, per `Docs/SHORTS_RELEASE_CALENDAR.md`) are a separate `/shorts` job (`SFL`), not part of this task.

## Close out

Edit Queue: `python3 scripts/edit-queue/queue.py set RO-14 uploaded` after setup, mirror to the Edit Queue page. Setup receipt in
`Docs/RO14_SETUP_RECEIPT_<date>.md`. One board entry while it waits on release; remove this handoff from the OPEN list.

## Starter prompt

> CONTENT (LFC). Name this task `Not Losing Weight LFC Setup`. Execute `Handoffs/handoff-20261022-ro14-thumbnails-and-video-setup.md`:
> set up "Why You're Not Losing Weight" (RO-14). Use the Codex subscription to generate the images. Make the five thumbnail choices and
> stop for my pick, then schedule it on Blotato in its 2026 long-form slot. Recommended: Claude Opus 5.5, high effort.
