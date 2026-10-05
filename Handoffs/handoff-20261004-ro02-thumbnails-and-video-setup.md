# RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else.

**Written 2026-10-04 by Claude (Opus 5.5).** One Claude task does everything: five thumbnail choices (made by Codex in the
command line), stop for Dan's pick, then `/video-setup`. **Fire only after Dan approves the round 3 film.**
**Model:** Claude Opus 5.5, medium. **Sidebar name:** `The Vacuum LFC Setup`.
**Use the Codex subscription to generate the images.**

## 1. State

Round 3 full film delivered 2026-10-04 for Dan's review. Not yet approved by him. If his reply asks for changes, this handoff
waits and a round 4 edit task runs first. It is ORGANIC: it ends "So go to AbsByAI.com, generate that picture of yourself with
abs and take the first step to getting in shape. Thank you for watching guys and I'll see you in the next video." Still run
the skill's Step 0 classification and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## 2. Files (all local)

Folder: `claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/`
- Master: `The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4`, 702 MB, 11:46.6, 1920x1080
  29.97, sha256 `24d71e04f1d952c3809b82e25c10f388fe722c12f7258d9c7cd1cb24d874996d`. Re-hash it first.
- `... RO-02.srt` (203 cues, sidecar) and `... RO-02.chapters.txt` (8 chapters, use as-is).
- Build record: `notes-RO02.md`, `ROUND-3-REVIEW-candidate2.md` (SHIP).

Facts for the packaging:
- **The film contains realistic AI footage** with the on-screen AI-GENERATED label: the two opener clips (0:00 to 0:06.5).
  So `ai_generated: true` in the Blotato config and the AI flag on YouTube. The app demo at 5:46 and 11:04 shows a labelled
  AI goal picture, which alone would not trigger the flag.
- He says Zepbound once (3:40). Organic videos may name the drug.
- **The delivery gate reads FAIL (gate 2.4.0), 32 of 39 rows, reported to Dan with the delivery:** the silent 20-second live
  set (two rows), the poolside far/near framing against two studio bounds, the declared punch cuts, and the two caption rows
  every organic long-form fails. Independent review said SHIP. Do not rebuild or re-gate; if a setup script refuses the stamp,
  tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).

## 3. Thumbnails first

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail section) and `IMAGE-GENERATION.md`, then `/youtube-packaging`.
Five choices: one real pool-shoot photo, one real studio-shoot photo, three AI designs of Codex's choice that sell this topic
(the stomach vacuum, a smaller waist). `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every
image; no outside model; a real photo of Dan is never redrawn. A photo of him holding a vacuum from this shoot's pool set
suits slot 1 if one exists. Show all five on one sheet and **STOP for Dan's pick.**

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link and the 8 chapters, tags),
Blotato release on YouTube, Facebook, Instagram @danrosefit and TikTok at the next open long-form slot, receipt in `Docs/`,
board entry, Edit Queue row. `Handoffs/video-editing/jobs.json` still needs RO-02 moved to delivered (it carried another
session's uncommitted edits on 10-04).

## Starter prompt (Claude Opus 5.5, effort medium)

Read `Handoffs/handoff-20261004-ro02-thumbnails-and-video-setup.md`. Name this session "The Vacuum LFC Setup". This is a
CONTENT long-form and I approved the round 3 film. Use the Codex subscription to generate the images. Make the five thumbnail
choices, show me the sheet and stop for my pick, then run /video-setup.
