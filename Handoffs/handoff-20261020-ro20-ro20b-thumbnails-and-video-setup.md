# CONTENT, long-form: Invest In Your Health LFC Setup (videos 1 and 2)

Written 2026-10-20 by Claude (Opus 5.5) at the end of round 4. Sidebar name: **Invest In Your Health LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (thumbnails, titles and descriptions are editorial; the queue steps are checklist).
**Use the Codex subscription to generate the images.** Every generated still uses
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

Two organic long-forms, set up together, in this order:
1. "Why You Should Invest More In Your Health" (RO-20), part 1 of 3.
2. "What To Cut To Afford Getting In Shape" (RO-20B), part 2 of 3.
Part 3, "What To Buy For Your Health At Every Income Level" (RO-20C), is still in editing (round 5) and is NOT part of this task.

**Ready now.** Dan, 2026-10-20: *"video one looks good. This is finalized"* and *"Two looks good. That is finalized."* Both are
`finalized` in the edit queue. Approval records: `approval-round4.json` in each delivery folder.

## Exact approved files (main project folder, never edit them; re-hash before setup)

- `claude edited long form content/18 - Why You Should Invest More In Your Health/Why You Should Invest More In Your Health | claude round 4 | 16x9 | RO-20.mp4`
  sha256 `41e0949adf44fb111a20825c9f5ea12715212ecde5058698cb3775cdd1705c92`, 16:11.6, 29,119 frames, 1.33 GB.
- `claude edited long form content/19 - What To Cut To Afford Getting In Shape/What To Cut To Afford Getting In Shape | claude round 4 | 16x9 | RO-20B.mp4`
  sha256 `88a6314f43424b28312dacdc1775b73ae7d17c8bf45212f6ffdc2bfccd86dec1`, 9:28.5, 17,039 frames, 0.78 GB.
- Each folder: `.srt` (upload, never burn in), `.chapters.txt`, notes, reviews, gate stamps. Both files exceed the 400 MB Blotato
  cap: make an upload derivative per `/video-setup`, keep the master untouched.
- Both films carry AI clips labelled AI-GENERATED on screen (11 in video 1, 5 in video 2): the YouTube AI-content disclosure applies.

Chapters, video 1: 0:00 Reason 1: The Halo Effect, 1:39 How Your Weight Changes Your Relationship, 3:09 Online Dating, 4:41 Reason 2:
You Get More Done, 6:03 Gym Time Or Doctor's Office Time, 7:37 Reason 3: Better Mental Health, 8:59 Reason 4: Bad Health Is Ludicrously
Expensive, 11:48 Money Does You No Good If You're Dead, 14:58 What's Next, 15:11 See Yourself With Six-Pack Abs.
Chapters, video 2: 0:00 You're Being Too Cheap With Your Health, 0:26 The "I'm Broke" Excuse, 0:58 3 Things You Should Never Cut,
1:58 What To Sacrifice, 2:31 1: Bars And Clubs, 4:00 2: Eating At Restaurants, 5:34 3: Junk Food In The House, 6:10 4: Vacations,
7:21 5: Therapy And Psychiatric Medication, 8:37 Subscriptions, Car Payments And Clothes, 9:02 What's Next.

## Read before work

Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails section, release cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`Docs/LONGFORM_RELEASE_CALENDAR.md`. Organic content: run setup Step 0 (classify each from its own ending) and
`python3 scripts/blotato/ad_guard.py --scan` before and after Blotato changes.

## Five thumbnail choices per video, then STOP for Dan's picks

VIDEO-RULES "Thumbnails: the five": one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated Dan, two AI
images of Codex's choice; each its own design. Real photos are never redrawn (cutout + generated background + type in code). No claims on
the thumbnail (memory `thumbnail-no-claims`). Strongest pictures in the films: video 1, the halo effect (people judge you on looks), the
lip-synced "fat guy who has money", online dating; video 2, cutting bars, restaurants and junk food to pay for health. Show all ten on one
sheet (two rows, one per video), stop for his picks.

## After the picks

`/video-setup` for each: title, description with chapters and the UTM link, tags, pinned question comment (`"pinned_comment"` in the
Blotato config), upload Private, AI disclosure.

**Schedule (Dan's words put them back on the calendar):** `Docs/LONGFORM_RELEASE_CALENDAR.md` had RO-20/B/C "off the schedule until Dan
says otherwise"; asking for this setup is that word. Long-forms release Sunday and Wednesday 9 AM CT, one per day, YouTube first, the
other platforms the next day at noon after YouTube is verified public. Read the live Blotato queue (`scripts/blotato/longform_queue.py`),
not a receipt. Order matters: video 1's ending says "In the next video, what you should cut to find that money" and video 2's ending says
"In the next video, from dead broke to baller". So video 1 takes the next free long-form slot after the last queued film, video 2 the
slot right after it, and leave the slot after video 2 free for video 3 if the calendar allows (note it in the calendar as reserved for
RO-20C). Every edited film releases in 2026 (calendar rule): if no 2026 slot is free, tell Dan in one line before using 2027. If Blotato
is full, put them on `scripts/blotato/video_waitlist.json` with their dates; the daily top-up routine queues them. Update the calendar
table. Once video 2 is public, add its watch link to video 1's description (and video 3's to video 2's later).

Then `queue.py set RO-20 uploaded` / `RO-20B uploaded` and mirror to the Edit Queue page, write one setup receipt
(`Docs/RO20_RO20B_SETUP_RECEIPT_20261020.md`), remove this handoff from the OPEN list. Each new long-form gets 3 Shorts
(`Docs/SHORTS_RELEASE_CALENDAR.md`): register their SL jobs if none exist yet; cutting them is a separate task.

## Starter prompt

> CONTENT (LFC). Name this task `Invest In Your Health LFC Setup`. Read and execute
> `Handoffs/handoff-20261020-ro20-ro20b-thumbnails-and-video-setup.md`: set up "Why You Should Invest More In Your Health" (RO-20) and
> "What To Cut To Afford Getting In Shape" (RO-20B), in that order. Use the Codex subscription to generate the images. Make five
> thumbnail choices for each, stop for my picks, then set both up on every platform. Recommended: Claude Opus 5.5, high effort.
