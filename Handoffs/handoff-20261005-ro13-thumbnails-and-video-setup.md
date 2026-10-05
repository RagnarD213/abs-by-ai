# RO-13 "Can You Drink Alcohol And Still Have Abs?": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else.

**Written 2026-10-05 by Claude.** One Claude task does everything: five thumbnail choices (made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 2 film on 10-05 ("everything looks good. This is approved").
**Model:** Claude Sonnet 5.5, medium (mechanical setup; Opus only if Dan rejects the title or description copy). **Sidebar name:** `Alcohol And Abs LFC Setup`.
**Use the Codex subscription to generate the images.**

## 1. State

Round 2 full film delivered 2026-10-04 and approved by Dan. It is ORGANIC: it ends "Thank you for watching guys. If today's
video helped you subscribe to the channel to make sure you don't miss any of my videos." (no tap-the-button CTA). Still run the
skill's Step 0 classification, and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## 2. Files (all local)

Folder: `claude edited long form content/11 - Can You Drink Alcohol And Still Have Abs/`
- Master: `Can You Drink Alcohol And Still Have Abs | claude round 2 | 16x9 | RO-13.mp4`, 1.86 GB, 7:10.63, 1920x1080 29.97,
  sha256 `2296902bf3667c6c6bd30255a4f3155988ddb3a4f38bf5a95ad5d985f10751c0`. Re-hash it first.
- `... RO-13.srt` (138 cues, sidecar, never burned) and `... RO-13.chapters.txt` (11 chapters, use as-is).
- Build record: `notes-RO13.md`, `ROUND-2-REVIEW.md` (SHIP), stamps, `recipe-RO-13/`. Review copy on Drive:
  https://drive.google.com/open?id=120kIR6yquWmTaaiaf9qoAsyCVQ2Kf2UN
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro13/round2/`.

Facts for the packaging:
- **The film contains realistic AI footage** with the on-screen AI-GENERATED chip: the pool-cookout opener (0:00 to 0:03.1) and
  the bathroom-mirror clip (0:20.4 to 0:24.2). So `ai_generated: true` in the Blotato config and the altered/synthetic flag on
  YouTube. Keep the one-line AI-image sentence in the description.
- He says Zepbound several times (6:33 to 6:50). Organic videos may name the drug. The description's "Zepbound tips" link goes in
  only if that video is public by then.
- Content for the description: the 6 rules (Eat First; Count The Calories; Kill The Sugary Mixers; Cap Your Nights; Stop 3 Hours
  Before Bed; Run Your Normal Fast) and what alcohol does (liquid calories, sleep, inhibitions, recovery and testosterone).
  Script sources: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`. UTM link and CTA per `/video-setup` Step 3.
- **The delivery gate reads FAIL (gate 2.4.0), 36 of 39 rows pass.** The three failing rows are the same readings every organic
  long-form shows: `captions:burned`, `captions:card_collision` (the Soft Blue lower thirds read as captions; nothing is burned
  in) and `framing:push_coverage` (measures only the wide holds). The independent review said SHIP. Do not rebuild or re-gate; if
  a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).
- Dan's known notes, accepted by his approval: a thin black hairline top and bottom on the two AI clips; four lower thirds that
  linger 3 to 6 frames past a cut. Not part of this task.

## 3. Thumbnails first

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail section and the 10-04 belly rule: no belly close-ups or fat pinching,
and thumbnails never put text over his face or hair), `IMAGE-GENERATION.md`, then `/youtube-packaging`. Five choices: one real
pool-shoot photo, one real studio-shoot photo, three AI designs of Codex's choice that sell this topic (drinking and keeping
abs; a beer next to a flat stomach is the obvious pull). `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`
for every image; no outside model; a real photo of Dan is never redrawn. No frowning photo unless the design needs it. Show all
five on one sheet and **STOP for Dan's pick.**

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link and the chapters, tags), Blotato
release on YouTube, Facebook, Instagram @danrosefit and TikTok at the next open long-form slot (board: Oct 7 RO-10, Oct 11 Stop
Deadlifting, Oct 14 Oura, Oct 25 RO-12, Nov 1 RO-16 are taken), receipt in `Docs/`, board entry, Edit Queue row (`queue.py set
RO-13 uploaded`, mirror to the artifact db, `mark-synced`). The sixpackabs.com article is written now and published once the
video is public (Step 6b). Never upload to YouTube yourself; Blotato creates the public video at release time.

## 5. Open items from the build (for the board, not blocking)

- `225a4d8` (RO-13 round 2 recipe, board, queue files) is committed locally and was not pushed: `safe-push.sh` stopped on other
  sessions' edits. Run `scripts/git/drift-check.sh` first; push with `safe-push.sh` only.
- Delete the RO-13 round 2 board entry once this task has queued the release.

## Starter prompt (Claude Sonnet 5.5, effort medium)

Read `Handoffs/handoff-20261005-ro13-thumbnails-and-video-setup.md`. Name this session "Alcohol And Abs LFC Setup". This is a
CONTENT long-form and I approved the round 2 film. Use the Codex subscription to generate the images. Make the five thumbnail
choices, show me the sheet and stop for my pick, then run /video-setup.
