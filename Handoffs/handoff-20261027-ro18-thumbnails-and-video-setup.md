# CONTENT, long-form: Make Time Exercise LFC Setup

Written 2026-10-27 by Claude (Opus 5.5) at the end of round 4. Sidebar name: **Make Time Exercise LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (the film started on Claude; thumbnails, title and description are editorial).
**Use the Codex subscription to generate the images.** Every generated still uses
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

"How To Make Time For Exercise & Nutrition" (RO-18), 9/23 studio rolls C1714/C1715 plus the vertical-set take C1719. **Ready now.**
Dan, 2026-10-27: *"Okay, everything is approved. Give me the handoff or setup."* Queue state `finalized`. Approval record:
`approval-round4.json` in the delivery folder.

## Exact approved file (never edit it; re-hash before setup)

- `claude edited long form content/21 - How To Make Time For Exercise & Nutrition/How To Make Time For Exercise & Nutrition | claude round 4 | 16x9 | RO-18.mp4`
  sha256 `77a05beed86fa0071424c2cf9a03690ed8f889d920a21cb079430e05cc755eaf`, 10:58.4, 19,732 frames, about 2.77 GB.
  Work copy: `/Volumes/Expansion/_edit_work/RO-18/round4/final/RO18_MASTER.mp4` (same hash). Rounds 2 and 3 files in the same folder
  are superseded: use only the round 4 files.
- Same folder: `... | RO-18.srt` (upload, never burn in), `... | RO-18.chapters.txt`, `... | RO-18.edit-sheet.json`, gate stamps,
  `ROUND-4-REVIEW.md`, `NOTES-R4.md`. The file is over the 400 MB Blotato cap: make an upload derivative per `/video-setup`
  (hardware encoder exemption), keep the master untouched.
- AI footage on screen, each labelled AI-GENERATED: stressed dad in the kitchen (0:12), voice-to-text rage (1:06), teacher slamming the
  laptop (7:46), essays by hand (8:23), and the app's self-generation demo result (10:36). The YouTube altered/synthetic disclosure and
  the TikTok AI flag apply. Real, unlabelled: Dan's own robot mower (4:31, 4:41, 4:58), his Wispr Flow take beside his real phone screen
  recording (1:30), the real before photo in the app demo ("Real photo of me, not AI-generated").
- Ending (organic): "...our AI nutritionist designs your nutrition plan. So you don't have to spend any time figuring that stuff out
  either. Thank you for watching guys. Subscribe to the channel if you want more videos like this and I'll see you in the next one."
  Confirm with setup Step 0.

Chapters (from the file): 0:00 You're Not Too Busy To Get In Shape, 0:36 Way 1: Talk Instead Of Typing, 2:22 Way 2: Work Out At Home,
3:33 Way 3: Use A Meal Prep Service, 4:31 Way 4: Buy A Robot Lawn Mower, 5:41 Way 5: Let The Car Drive Itself, 7:33 Way 6: Let AI Do
Your Work, 9:59 Add It All Up: 10+ Hours A Week.

⚠ A dedicated Short with a near-identical title exists: DS-09 "How To Make Time To Work Out" (already released Oct 19). Give RO-18 a
clearly different title and thumbnail; link the two in the description once RO-18 is public.

## Read before work

Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails section "Thumbnails: the five", release cadence, pinned comment,
never Public), `.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`Docs/LONGFORM_RELEASE_CALENDAR.md`. Run setup Step 0 (classify from its own ending) and `python3 scripts/blotato/ad_guard.py --scan`
before and after Blotato changes.

## Five thumbnail choices, then STOP for Dan's pick

The 2026-10-25 mix (AGENTS.md "Thumbnail and cover mix"): **two distinct AI images of Dan acting out the topic, one real photograph
from the pool OR studio shoot, two concepts at Codex's discretion guided by Dan's approved-cover history** (inspect his recent picks
first; AI Dan acting the title out is his most frequent pick). Five genuinely different designs, one line per option naming its design
before building. Real photos are never redrawn (cutout + generated background + type in code); use a real identity reference and
inspect every AI Dan face. No claims on the thumbnail, no frowning photo of Dan, text off his face and hair, masculine palette.
The film's strongest ideas: a busy man with no time (phone, kids, commute) who still gets a workout in; Dan dictating to his phone
instead of typing; the robot mower doing his yard work; "10+ hours a week" given back. Show all five on one sheet, stop.

## After the pick

`/video-setup`: title, description with chapters and the UTM link, tags, pinned question comment (`"pinned_comment"` in the Blotato
config), AI disclosure, SRT. Organic videos are never uploaded to YouTube by us: Blotato creates the public video at release.

**Schedule.** Long-forms release Sunday and Wednesday 9 AM CT, one per day; YouTube first, Facebook, Instagram and TikTok the next day
at noon after YouTube is verified public. Read the live Blotato queue (`scripts/blotato/longform_queue.py`), not a receipt. Calendar rule
for this film: "A film still in editing (RO-17, RO-14, RO-18) that finishes before December takes the 2026 Sunday of the newest
not-yet-edited studio film", but those Sundays are gone (RO-22's Dec 13 went to RO-17, RO-30's Nov 29 to RO-20B), every 2026 slot in
the calendar is taken, and RO-14 already went to Jan 3, 2027 with Dan's OK. RO-18 ranks as a Wednesday film (weakest first). Dan's rule
is that every edited film releases in 2026: tell him in one line that no 2026 slot is free, with one concrete recommendation (the next
free 2027 Wednesday after RO-04's Jan 6, or a 2026 slot he chooses to free), and wait for his yes before scheduling. If Blotato is full,
put it on `scripts/blotato/video_waitlist.json` with its date; the daily top-up routine queues it. Update the calendar file.
Shorts from this film (3, per `Docs/SHORTS_RELEASE_CALENDAR.md`) are a separate `/shorts` job (`SFL`): register it in the Edit Queue
(as RO-14's setup did with SL-23), do not cut it here.

## Close out

Edit Queue: `python3 scripts/edit-queue/queue.py set RO-18 uploaded` after setup, mirror to the Edit Queue page. Setup receipt in
`Docs/RO18_SETUP_RECEIPT_<date>.md`. One board entry while it waits on release; remove this handoff from the OPEN list.

## Starter prompt

> CONTENT (LFC). Name this task `Make Time Exercise LFC Setup`. Execute `Handoffs/handoff-20261027-ro18-thumbnails-and-video-setup.md`:
> set up "How To Make Time For Exercise & Nutrition" (RO-18). Use the Codex subscription to generate the images. Make the five thumbnail
> choices and stop for my pick, then confirm the release date with me and schedule it on Blotato. Recommended: Claude Opus 5.5, high effort.
