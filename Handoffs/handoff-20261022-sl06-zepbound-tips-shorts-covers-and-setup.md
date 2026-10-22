CONTENT | SL-06 | Top 5 Zepbound Tips SFL Setup

# SL-06 Top 5 Zepbound Tips shorts (6): covers, then upload and schedule

Written 2026-10-22 by Claude (Opus 5.5). Six Shorts (`SFL`) cut from the long-form "Top 5 Zepbound Tips To Lose Fat And Keep
Your Muscle" (RO-12). One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5, high
effort** (cover design is editorial work; the video was edited on Claude; memory `model-routing-plan`). **Use the Codex
subscription to generate the images.**

Dan approved all six: D on 2026-10-22 (*"Okay, D is approved"*, round 6), A, B, C, E, F on 2026-10-22 (*"Everything is
approved"*, round 7). Queue: SL-06 `finalized`. Edit history and recipe: `.claude/skills/shorts/reference/softblue-sl06/`
(README sections "Round 6" and "Round 7"); work folders `/Volumes/Extreme/_edit_work/sl06/round6/` and `round7/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (the five cover choices made by Codex; Blotato only for organic YouTube;
   AI label rule; Speedo crop; frowning photos; cover text never over his face or hair; the top section "AI clips of Dan look
   natural": any AI image of Dan has a relaxed closed-mouth smile and no straining flex).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight, Facebook
   cover registry), "Blotato full?" (waiting list). Closest worked example:
   `Handoffs/handoff-20261021-sl09-oura-shorts-covers-and-setup.md` (and SL-07's receipt `Docs/SL07_SETUP_RECEIPT_20261018.md`).
4. `Short-form video content/zepbound-tips-SHORTS.md` (the batch card; update it with the final files).

## 1. The six files (final; never re-render or re-edit)

> ⚠ **Clipped title letters (2026-10-22):** Shorts 1, 4 and 5 ("Not 2.5 mg", "Thursday Evening", "Without Regaining It") have the tails of g/y cut off at the bottom of the title band. Dan decides whether to re-render them first (`Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). Covers may go ahead; do not upload these files until that decision is recorded, then use the hashes of whichever files he approves.

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), Dan's approved mix, with
`.audio_gate.json` and `.deliver_gate.json` (PASS 39/39, gate 2.6.1) beside each. Re-hash (sha256) before any upload; a
mismatch means the file changed after approval: stop and tell Dan. **iCloud trap (2026-10-22):** stale copies named
`… 2.mp4` / `… 3.mp4` from older renders can reappear in that folder; use only the exact names below.

| # | file (`zepbound-tips-` + ...) | length | on-screen title (eyebrow "GLP-1 Tips") | AI intro | sha256 (first 8) |
|---|---|---|---|---|---|
| 1 | `short1_start-at-1-mg-not-2-5.mp4` | 47.0 s | Start At 1 mg, Not 2.5 mg | 0:00-0:04.1, two vials (no person); also AI B-roll in the body | `0ebf77cf` |
| 2 | `short2_use-a-needle-and-vial-not-the-pen.mp4` | 53.9 s | Use A Needle And Vial, Not The Pen | 0:00-0:04.6, pen and vial (no person) | `ad578fa5` |
| 3 | `short3_how-to-inject-in-10-seconds.mp4` | 54.2 s | How To Inject In 10 Seconds | 0:00-0:02.8, kit flat lay (no person); then two credited YouTube clips | `56ed1071` |
| 4 | `short4_inject-on-thursday-evening.mp4` | 50.5 s | Inject On Thursday Evening | 0:00-0:03.3, AI Dan holding a vial | `0458bf1d` |
| 5 | `short5_how-to-come-off-without-regaining-it.mp4` | 58.0 s | How To Come Off Without Regaining It | 0:00-0:03.2, gym bag and meal prep (no person) | `f11bfee8` |
| 6 | `short6_how-much-protein-you-need.mp4` | 54.7 s | How Much Protein You Need On A GLP-1 | 0:00-0:01.9, dinner plate (no person) | `e9b58ad3` |

All six carry AI content: `ai_generated` true on every platform. For other AI B-roll in the bodies, read
`/Volumes/Extreme/_edit_work/sl06/plans.py` (COVERS entries with `ai=`) and `build/<S>/timeline.json` (S = A..F for shorts 1..6).

**Release slots.** `Docs/SHORTS_RELEASE_CALENDAR.md` holds them (Zepbound Tips N = short N): 1 Mon Nov 9, 2 Sat Nov 21,
3 Sat Nov 28, 4 Tue Dec 1, 5 Sat Dec 5, 6 Tue Dec 8, all 9 AM America/Chicago.
Never before the parent is public: the parent RO-12 is on
`Docs/LONGFORM_RELEASE_CALENDAR.md` for **Sun Nov 8** (its 2026-10-01 receipt says Oct 25): read the live Blotato YouTube
queue for its actual slot first and move the shorts with it.

**All six are ORGANIC** (content shorts, no "tap the button"). Closing words: 1 "...a great long-term maintenance dose for me.";
2 "...If you can read a measuring cup, you can do this."; 3 "...or you pushed the plunger too fast."; 4 "...the version of you
that did not need help."; 5 "...Walk down the stairs instead of jumping off the roof."; 6 "...Your snacks should not be carbs."
Run the classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write. Organic
videos may name Zepbound (memory `organic-drug-names-allowed`).

## 2. Covers (first half; stop for Dan's picks)

Five choices per short, each in both layouts (Instagram grid and YouTube Shorts), which count as one choice:
1. one real pool-shoot photo of Dan; 2. one real studio-shoot photo of Dan; 3. one AI-enhanced or AI-generated image of Dan
in the short's subject; 4. and 5. two more AI images of Codex's choice (Dan or not). Five unique designs per short: write
one line per option naming its layout, type, colour and composition before building, and check no two share them.

- Codex makes all of them: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No other model. Real
  photos are never redrawn (Codex makes the background; his cutout from `photos/finalized social media photos/_cutouts/` and
  the type are layered in code). For option 3 give Codex a real photo as reference, "lean and shredded, not bulky", a relaxed
  closed-mouth smile, no straining flex (Dan rejected exactly that on 2026-10-21), and check the face reads as him.
- Copy: the short's title (same on all five). No claims or numbers as results, no AbsByAI.com, no "Real picture" label,
  text clear of his face and every part of his hair. Title case. Check the brand-name rule for graphics in VIDEO-RULES.
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, ten or more different photos across the set, none
  already on the grid (`Short-form video content/covers/posted covers/`). Masculine palettes (memory `thumbnail-masculine-colours`).
- Topic images for the AI designs, and approved pictures Codex may use as references: the intro stills of this batch,
  `/Volumes/Extreme/_edit_work/sl06/round7/frames/` (`A_r7.jpg` two vials 1 mg vs 2.5 mg; `B_r7.jpg` pen in the dark, vial
  and syringe in light; `C_r7.jpg` the kit flat lay; `E2_r7.jpg` gym bag, meal prep and empty vial; `F_r7.jpg` chicken plate
  vs pasta) and `/Volumes/Extreme/_edit_work/sl06/round6/frames/D_r6h.jpg` (AI Dan holding a vial, relaxed, wall calendar
  with Thursdays circled). Ideas: a dose dial or small vs large dose (1); pen vs needle side by side (2); a thigh pinch or
  the kit (3); a calendar with Thursdays circled (4); stairs going down, a scale holding steady (5); protein foods on a plate (6).
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the
  grid-safe centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 30 (grouped by short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl06/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/zepbound-tips SL-06/` and Google Drive
   `Short-form video content/zepbound-tips SL-06/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check
   Extreme free space first (it was at 313 GB on 2026-10-22).
2. Per short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy,
   Instagram PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl06-short<N>-<slug>.json` (copy an `sl09-short*` or `sl07-short*` config; `content_type` organic,
   `source`, keyword `FOOD` as the parent `ro12-zepbound-tips.json` uses, `utm_content=sl06-short<N>`, `ai_generated` true,
   `"pinned_comment"` through `dan-voice-writer`, YouTube description naming the full video "Top 5 Zepbound Tips To Lose Fat
   And Keep Your Muscle" and short 3's description crediting both clips: "Clips: Seattle Children's and SynergenX on YouTube").
   Register each Facebook cover in `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per short. If Blotato is full, finish everything else and add each short to
   `scripts/blotato/video_waitlist.json` (kind `short`); the daily routine queues it. Never create a one-video task.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL06_SETUP_RECEIPT_<date>.md` (schedule ids, cover hashes,
   pinned comments, "articles: written by the routine after release"), `queue.py set SL-06 uploaded` + Edit Queue artifact
   (https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs, `jobs/SL-06` was version 10 on 2026-10-22; pin `if_version`) +
   `mark-synced`, update `Docs/SHORTS_RELEASE_CALENDAR.md` and the batch card, board one-liner, commit and push.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261022-sl06-zepbound-tips-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the six Top 5 Zepbound Tips shorts, show me one review sheet and stop for my picks, then upload and schedule all six on every platform through Blotato on the shorts calendar dates. Use the Codex subscription to generate the images.
