# CONTENT, long-form: 3 Healthy Foods LFC Setup

Written 2026-10-18 by Claude (Opus 5.5) at the end of round 5. Sidebar name: **3 Healthy Foods LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort. **Use the Codex subscription to generate the images.** Every generated still
uses `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

**Ready now: Dan confirmed the round 5 film on 2026-10-18 ("final"); RO-17 is `finalized` in the edit queue.** Approval record:
`claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/approval-round5.json`.

## Exact approved files

Folder: `claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/` (main project folder).
- Master: `3 Healthy Foods That Made Me Fat | claude round 5 | 16x9 | RO-17.mp4`, sha256 `62187e39d262a9ce36902ebf02d12533ab08f8af651fe84f825a13de98ef3fad`,
  1920x1080, 30000/1001, 13,551 frames, 7:32 (452.15 s), about 1.9 GB. Re-hash before setup; never edit it. Over the 400 MB Blotato cap:
  make an upload derivative per `/video-setup`, keep the master untouched.
- Subtitles (upload, never burn in): `... | RO-17.srt`. Chapters: `... | RO-17.chapters.txt` (0:00 intro, 0:45 Trail Mix, 2:19 Dried Fruit,
  3:33 Coconut Water, 5:16 What I snack on instead, 7:15 The swap, recapped).
- Notes, review, stamps: `notes-RO17-round5.md`, `ROUND-5-REVIEW.md`, the `.deliver_gate.json` / `.audio_gate.json` stamps.
- The film carries eight AI clips labelled AI-GENERATED on screen: the YouTube AI-content disclosure applies (VIDEO-RULES, "AI label on uploads").

## Read before work

Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails section at the top, long-form Sunday cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`.
Organic content: run setup Step 0 (classify from its own ending) and `python3 scripts/blotato/ad_guard.py --scan` before and after Blotato changes.

## Five thumbnail choices, then STOP for Dan's pick

Per VIDEO-RULES "Thumbnails: the five": one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated Dan, two AI
images of Codex's choice; each its own design. Real photos are never redrawn (cutout + generated background + type in code). No claims on the
thumbnail (memory `thumbnail-no-claims`). The film's strongest pictures: trail mix outweighing a cheeseburger on a scale (the opener), the
grapes vs raisins handful, coconut-water sugar. Save to `social media graphics/youtube/thumbnails/3 Healthy Foods/`, show all five on one sheet,
stop for his pick.

## After the pick

`/video-setup`: title, description with chapters and the UTM link, tags, pinned question comment (`"pinned_comment"` in the Blotato config),
upload Private, queue YouTube on the next free Sunday 9 AM CT after the last queued long-form (live queue, `scripts/blotato/longform_queue.py`;
if Blotato is full, `video_waitlist.json`), Facebook / Instagram @danrosefit / TikTok no earlier than the following Monday 9 AM. Then
`queue.py set RO-17 uploaded`, mirror to the Edit Queue page, write the setup receipt, remove this handoff from the OPEN list.

## Starter prompt

> CONTENT (LFC). Name this task `3 Healthy Foods LFC Setup`. Read and execute `Handoffs/handoff-20261018-ro17-thumbnails-and-video-setup.md`.
> Use the Codex subscription to generate the images. Make the five thumbnail choices, stop for my pick, then set it up on every platform.
