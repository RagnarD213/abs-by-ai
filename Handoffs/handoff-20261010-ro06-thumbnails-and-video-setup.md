# RO-06 "How To Work Out At Home On A Budget": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version.

**Written 2026-10-10 by Claude.** One Claude task does everything: five thumbnail choices (images made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 6 film on 2026-10-10 ("All right, this looks good. This is finalized and approved.").
**Model:** Claude Sonnet 5.5, effort medium (mechanical setup per `model-routing-plan`; Opus high only if Dan rejects the title or description copy).
**Sidebar name:** `Work Out At Home LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 6 full film is delivered, gated, independently reviewed (SHIP) and approved by Dan. The Dan-facing copy in `Videos to Review/` and
the review pages (ports 8846 to 8851) were removed on 10-10; the delivery folder is the record.
It is ORGANIC: it ends "go to AbsByAI.com. Thank you for watching and I'll see you in the next video." with no tap-the-button call to action.
Still run the skill's Step 0 classification, and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.
Edit Queue row RO-06 is already `finalized` (artifact mirror done, version 19); when the release is queued set it `uploaded`, mirror with
`ArtifactData` (artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, pin `if_version`), then `queue.py mark-synced RO-06`.

## 2. Files (all local)

Folder: `claude edited long form content/13 - How To Work Out At Home On A Budget/`
- Master: `How To Work Out At Home On A Budget | claude round 6 | 16x9 | RO-06.mp4`, 1.89 GB, 16:38.2, 1920x1080 29.97, h264 + AAC,
  sha256 `258bf12224414aa23e3e70d29dd230015666e23a3b2218410ba710fab6ba563b`. Re-hash it first.
- `... RO-06.srt` (301 cues, sidecar, never burned in) and `... RO-06.chapters.txt` (13 chapters, use as-is).
- Also there: `... REVIEW 540p.mp4`, the audio AB file, stamps (`.audio_gate.json`, `.deliver_gate.json`), `notes-RO06-round6.md`,
  `ROUND-6-REVIEW-2.md`, `round6-record.json`, `recipe-RO-06/`. The round 5 files in the same folder are the superseded cut: ignore them.
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro06/round6/`.

Facts for the packaging:
- **Realistic AI footage is in the film:** four AI clips of a trainer and a client in the first minute (0:33 to 0:47) and three AI clips in
  the closing section (leg press, leg curl, a lifter loading a bar, 14:51 to 15:01), all with the AI-GENERATED chip, plus AI exercise demos
  inside the phone at 15:50. So `ai_generated: true` in the Blotato config (TikTok) and the altered/synthetic flag on YouTube. The six product
  pictures on the price cards are labelled AI stills. Keep the one-line AI-image sentence in the description.
- **Dan promises product links on camera (1:16):** "in the description below, I'm gonna give you my Amazon Associates link to go buy it on
  Amazon for each of my recommended items." The description therefore needs one Amazon link per item, and the Associates disclosure line
  ("As an Amazon Associate I earn from qualifying purchases."). **No Associates links are on record in the repo. Ask Dan for them (or for his
  Associates tag and the product pages) in the same message as the thumbnail sheet, so he answers both at once.** Never invent a link or a tag.
  The items and the prices he says: yoga mat $22, push-up handles $10 (not the $40 rotating ones), jump rope $9, ab wheel $17 (basic setup $58);
  35 lb kettlebell $45 (basic black iron, not rubber coated), 6 lb medicine ball about $20, 25 lb dumbbells $29 a pair (a light pair for side
  laterals and a heavy 40 to 45 lb pair for triceps if buying more), a few strong hand towels. Full setup about $150.
- The chapters file is the outline for the description. UTM link and call to action per `/video-setup` Step 3.
- **The stamps read FAIL and that is known.** Audio gate: the tone row only, with the voice chain Dan approved. Delivery gate 2.5.1: 29 rows
  pass, 10 fail, the same ten as round 5 (listed in `notes-RO06-round6.md` and `round6-record.json`). The independent review said SHIP and Dan
  approved the film. Do not rebuild or re-gate; if a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).
- TikTok: 16:38 is over the length some accounts allow (RO-01's TikTok limit is still unresolved on the board). If TikTok refuses it, queue
  the other three and say so.

## 3. Thumbnails first

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail section, the belly rule, text never over his face or hair, the Speedo crop rule,
no frowning photos), `.claude/skills/_shared/IMAGE-GENERATION.md`, then `/youtube-packaging`. **The standard five:**

1. **One real pool-shoot photo** (a real photo of Dan, never redrawn; background-removed cutout plus type in code).
2. **One real studio-shoot photo** (same rule). Rotate away from the photos the last few videos used.
3. to 5. **Three AI images, each a different design of Codex's choice** that sells the topic: a full home workout setup for $58, cheap
   equipment against an expensive gym or a $1,000 barbell set, the seven items laid out on a mat by a pool, a price tag on a kettlebell. They
   do not have to be Dan. Thumbnails carry no AI label.

Same copy on all five unless Dan asks for alternatives; short and big (two lines beats three). The video's own lines: "A Full Home Setup For
$58" and "Basic Setup: $58. Full Setup: About $150." A price is a fact about the equipment, not a result claim, so "$58" may lead.
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every AI image; no outside image model. QC on the RENDERED files:
person-mask clearance of every text block from his face and hair of at least 25 px, and look at the sheet yourself before sending it. Save the
finals in `social media graphics/youtube/thumbnails/How To Work Out At Home On A Budget/`. Show all five on one review sheet (`SendUserFile`,
display render), list them in plain words, ask for the Amazon links, and **STOP for Dan's pick.** He may pick one, or two for an A/B test.
Final file: `<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the product links, the UTM link and the chapters, tags,
pinned comment), Blotato release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**, then Facebook, Instagram
@danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified public. Read the live Blotato YouTube
queue first. As of the 10-10 board these Sundays are taken: Oct 11 Stop Deadlifting, Oct 18 RO-05, Oct 25 RO-12, Nov 1 RO-16, Nov 8 Oura,
Nov 15 RO-13, Nov 22 RO-02, Nov 29 RO-10, Dec 6 RO-01, Dec 13 RO-11, Dec 20 RO-03. So expect **Dec 27**; use `scripts/blotato/longform_queue.py`, which refuses
an off-Sunday or occupied slot. Never upload to YouTube yourself; Blotato creates the public video at release time. Receipt in
`Docs/RO06_SETUP_RECEIPT_<date>.md`, a board entry for the queued release, Edit Queue `uploaded`. The sixpackabs.com article is written now and
published once the video is public.

## 5. Already done at finalization (do not repeat)

Footage ranges marked used on all 20 rolls; clip library: the four AI clips (A0154 to A0157), the second fast jump rope cut (B0542), the
closing app scene (B0543) and its phone screen sequence (B0544, approved for reuse); the approval is in the QC corpus; Dan's two notes are
standing rules (VIDEO-RULES, top two sections).

## 6. Open items (not blocking)

- Dan's one note on the film, kept as is by his call: the toe-touch cutaway at 9:32 has no medicine ball while he talks about the medicine ball.
- The Shorts job cut from this film is separate (`/shorts`), after the release is queued.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.

## Starter prompt (Claude Sonnet 5.5, effort medium)

Read `Handoffs/handoff-20261010-ro06-thumbnails-and-video-setup.md`. Name this session "Work Out At Home LFC Setup". This is a CONTENT
long-form and I approved the round 6 film. Use the Codex subscription to generate the images. Make my five thumbnail choices (1 pool photo,
1 studio photo, 3 unique AI designs of Codex's choice), show me the sheet, ask me for my Amazon links for the items, and stop for my pick,
then run /video-setup.
