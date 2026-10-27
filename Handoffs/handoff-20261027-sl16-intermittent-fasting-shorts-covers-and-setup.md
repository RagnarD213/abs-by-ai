CONTENT (SFL) | Intermittent Fasting Shorts | SL-16 | Cover choices and setup

# Intermittent Fasting SFL Setup

Ready to start October 27, 2026. One Claude task handles covers and setup for all four approved Shorts. Recommended: **Claude Opus 5.5, high effort** (cover design decisions and viewer-facing descriptions). **Use the Codex subscription to generate the images.** Use the newest supported stable GPT (currently `gpt-6.1-sol`) at high effort through the shared image helper; verify availability at execution. No separate image task.

## Approval and readiness

Dan reviewed Round 2 at http://127.0.0.1:9116/ and said on October 27, 2026:

> Okay, everything looks good. Everything is approved. Give me the handoff or setup.

That approval also settles the two calls on the page: the caption "can" at 0:19 in Short 1 stays, and hair at the top of the frame (the camera's own framing) is accepted. All four edits are FINAL: do not re-edit, re-render or ask for edit approval again.

Canonical project: `/Users/danielrose/Projects/Claude/Projects/Abs By AI`. Finals: `Short-form video content/` (names below). Manifest with hashes, sizes and the Extreme copies (hash-matched): `Short-form video content/fasting-SHORTS-final-manifest.json`; notes `fasting-SHORTS.md`. Build, recipe, reviews and gate stamps: `/Volumes/Extreme/_edit_work/SL-16/` (recipe copy in git: `.claude/skills/shorts/reference/softblue-sl16/`).

Every file passed independent review (SHIP) and the audio gate; the delivery gate passes all rows except `framing:hair_top` / `framing:headroom` (camera framing, Dan accepted) and, on Short 1, the `junk:repeated_take` false alarm ("if you wake up at nine ... seven", Dan's two examples; a separate fix task exists). **No covers, media uploads, Drive backup, platform schedules or publication have been done.** Edit slot released finished; setup is exempt from the edit cap.

| # | Approved title | File in `Short-form video content/` | Seconds | Realistic AI footage flag | SHA256 |
|---|---|---|---|---|---|
| 1 | How To Start Fasting: Just Skip Breakfast | `fasting-short1_just-skip-breakfast.mp4` | 57.925 | true: workday time-lapse opener 0:00-0:07.7 (library A0169) | `e77bd982d5c4fe0113c2312211b77bdb73087af3b8c34afcf5f8c6eebe45b5b3` |
| 2 | Carbs Are Killing Your Workday | `fasting-short2_carbs-are-killing-your-workday.mp4` | 55.019 | true: donut-then-asleep AI clip 0:00-0:04 (A5) | `9da5c4a23772425ab091fff41fabd51c88434e4317a22e91f155484ed0a4834b` |
| 3 | Never Break Your Fast With Alcohol | `fasting-short3_never-break-your-fast-with-alcohol.mp4` | 37.184 | true: bar-stool sip 0:00-0:01.4 (library A0174) | `0f41a8db9aea880c657ea1d51ac133695b3311944fbd825966c2ca5c5077a452` |
| 4 | Life Will Punch You In The Face | `fasting-short4_life-will-punch-you-in-the-face.mp4` | 54.488 | true: boxing-glove gag 0:06-0:09 (library A0158) | `ae9c7d1ba2088ba20d798b08eb50d2df0bf48d982b852681939ce884bdecb34b` |

All 1080x1920 at 30000/1001 with burned captions; word timings in each build's `words.json`/`cues.json` (the parent SRT does not fit a Short). Hash every file before use. **Short 4's Tyson photo is by Glenn Francis (Wikimedia Commons, CC BY-SA 4.0): its description must credit "Photo of Mike Tyson: Glenn Francis, www.PacificProDigital.com (CC BY-SA 4.0)".**

## Read before execution

AGENTS.md, AI_COORDINATION.md, full `.claude/skills/_shared/VIDEO-RULES.md`, `video-setup/SKILL.md`, `coverimage/SKILL.md`, `_shared/IMAGE-GENERATION.md`, `_shared/WRITING-RULES.md`, both release calendars, `Docs/PINNED_COMMENTS.md`, the parent config `scripts/blotato/configs/ro08-intermittent-fasting.json` (keyword FOOD) and its receipt `Docs/RO08_SETUP_RECEIPT_20261014.md`. Worked example: `Handoffs/handoff-20261025-sl08-calories-shorts-covers-and-setup.md`. Work in the background; deliver links and sheets in chat. Inspect for existing `sl16*` configs and any other owner before writing.

## First: five cover choices per Short (20 choices, Instagram + YouTube layouts each)

Follow AGENTS.md / VIDEO-RULES "Thumbnails: the five" as updated 2026-10-25: per Short, **two distinct AI images of Dan acting out the topic, one real photograph from the pool OR studio shoot, and two concepts at Codex's discretion guided by his approved-cover history** (inspect recent picks first; AI Dan acting the title is his most frequent pick; discretionary choices may include more AI Dan). Five genuinely different designs per Short; one design line each before building. Real photo: original person pixels (cutout + generated background + type in code). AI Dan: real identity reference, lean and shredded not bulky, inspect every face. Title case copy = the approved title. No website mark, claims, real-photo label, frowning photo, text on face/hair, or swim-brief below the waistband crop. Topic directions: skipping breakfast for a late lunch; carbs and the afternoon crash; alcohol on an empty stomach; life punching you in the face / the plan you can keep. Check at feed size and native scale, grid-safe text, YouTube JPEG under 2 MB. **Stop for Dan's picks before any upload or scheduling.**

## After picks: file, package, schedule

1. Verify masters against the manifest; complete and verify the Google Drive backup (anyone with the link can view) with approved covers; record link, sizes, hashes.
2. CONTENT classification: all four end on a teaching line, no button CTA. `content_type: organic`, exact `source`, `ad_guard.py --scan` before and after.
3. Per-Short titles, descriptions (Short 4 carries the photo credit), tags, UTMs, an easy pinned question (`pinned_comment`, no link, under 180 characters), AI flag `true` on all four.
4. Export covers to `Short-form video content/covers/approved-sl16/`; TikTok cover-first copies via `tiktok_cover.build()`; Facebook cover registry; verify downloads match.
5. One config per Short `scripts/blotato/configs/sl16-short<N>-<slug>.json` (FOOD); `organic_short_queue.py` dry run, then `--apply`; read back YouTube, Facebook, Instagram @danrosefit, TikTok. Blotato releases YouTube; never a direct Public upload or native scheduling.
6. Queue full or parent not yet public: add the four to the shared `video_waitlist.json` (`kind: short`, parent dependency). No per-video routine.

## Calendar: resolve before booking

Dan picked **Short 1 for Tue Dec 15, 9 AM Central** (`Docs/SHORTS_RELEASE_CALENDAR.md`, row Dec 14). The other three take the next free Mon/Tue/Fri/Sat 9 AM slots after the parent is public, in 2026 where possible (every edited Short releases in 2026). **Conflict:** the long-form calendar says RO-08 releases Wed Nov 18, but `Docs/RO08_SETUP_RECEIPT_20261014.md` and the board say it waits on the Blotato waitlist for **Sun Jan 24, 2027**. A Short never posts before its parent is public. Check the live Blotato queue/waitlist and the channel first; if the parent really releases Jan 24, 2027, Dec 15 cannot hold: prepare concrete options and ask Dan one scheduling question rather than posting early or displacing approved videos. Covers and all other prep proceed meanwhile.

## Finish

Receipt `Docs/SL16_SETUP_RECEIPT_<date>.md` (master and cover hashes, Drive link, metadata, pinned questions, media URLs, dates and schedule IDs or honest waitlist state). Set SL-16 `uploaded` only after live read-backs. Remove this handoff from the OPEN list, update the board entry, push owned changes with `scripts/git/safe-push.sh`. Dashboard stays paused.

## Starter prompt

Name this task Intermittent Fasting SFL Setup. Read Handoffs/handoff-20261027-sl16-intermittent-fasting-shorts-covers-and-setup.md and execute it with /video-setup. All four Intermittent Fasting Shorts are approved. Use the Codex subscription to generate the images. Make five unique cover choices for each Short (two AI images of me acting out the topic, one real pool or studio photo, two of Codex's choice) and show me the checked sheet, then stop for my picks. After the picks, complete backups, metadata and Blotato setup. Verify the parent film's live release date before booking dates (Short 1 is Tue Dec 15). Keep everything in the background and preserve the approved masters.
