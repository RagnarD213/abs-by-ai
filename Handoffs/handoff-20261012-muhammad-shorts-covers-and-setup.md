# Muhammad dedicated shorts (5 now, 2 to follow): covers, then release queue

**Category: CONTENT. Dedicated Shorts (`SFC`), edited by Muhammad. Written 2026-10-12 by Claude (Opus 5.5).
Task name: `Muhammad Shorts Batch SFC Setup`.** One Claude handoff covers both halves (Dan's rule, 2026-10-01):
make the cover choices, stop for Dan's picks, then file and queue. **Use the Codex subscription to generate the images.**

**Recommended model: Claude Opus 5.5, high effort** (cover design is judgment work; the queue half is scripted).

## Goal
Take the five finalized shorts whose high quality files are in hand from "finalized" to "queued for release on YouTube,
Facebook, Instagram @danrosefit and TikTok", each with a cover Dan picked. Two more join when their high quality exports arrive (section 5).

**Left out on purpose (Dan, 2026-10-12): completed videos only.**
- **DS-21 How To Do Hammer Curls:** still in progress (one caption word). No covers, no queue, not in this task.
- **DS-25 How To Do M100s:** `blocked` in the Edit Queue. Dan is filming the M100s B-roll and it will be added to the
  video first. No covers, no queue, not in this task.

## Decisions already made
- Dan finalized all of these on 2026-10-12. His words after the check: *"everything's looking good except for that one
  revision in the Hammer [Curls] video"*. Edit queue: DS-08, DS-09, DS-12, DS-14, DS-22, DS-23, DS-24 are
  `finalized`; DS-21 is `in_progress`; DS-25 is `blocked` (needs the M100s B-roll).
- **None of these is an ad.** Muhammad labeled two files "AD 08" and "Ad 09"; they are DS-08 and DS-09. Every one of the
  nine ends on a comment call to action, none says "tap the button below". They go through `/video-setup` only. Still
  run the classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.
- The four HD exports of earlier approved cuts were proven identical to the approved review copies (same frame count,
  frame subtraction shows only compression noise). Record: `revision docs/shorts-hd-check-muhammad-10-12-26.summary.md`.
- Never re-render or re-edit these files. Muhammad's audio is delivered untouched.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full.
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop, five choices).
3. `/video-setup`, "Shorts" section, the waitlist section and "YouTube Shorts cover verification".
4. `Docs/PINNED_COMMENTS.md` (every video's Blotato config carries a `"pinned_comment"` question).
5. Closest worked example: `Handoffs/handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md` and its receipt.

## 1. The five files ready now
Downloaded to `/Volumes/Extreme/_edit_work/revisions-20261012/muhammad/dl/<folder>/`. All 1080x1920, about 30 fps,
10.6 to 12.9 Mbps, captions burned in. Re-hash before any upload; a mismatch means stop and tell Dan.

| Job | Title | Folder | Length | sha256 (first 16) | Drive id | AI clips inside? |
|---|---|---|---|---|---|---|
| DS-12 | Top 3 Ways To Looksmax | `01_looksmax_hd` | 57.0 s | `6d8ba7e870ad2bc6` | `156EDpDaeEGr_pzJnIyKWgjCU2ZAlSPFa` | Yes (opener, cliff couple, jawline) |
| DS-23 | How To Do Side Laterals | `02_sidelaterals_hd` | 49.6 s | `1b3e9e9517452377` | `1k9UGUaIhrFG-Ds8sJUm49q4w5sqoG8ut` | No |
| DS-08 | I Was 200 Pounds At 38 | `04_ad08_hd` | 50.3 s | `83575ea52d874723` | `10xDY9fZ-FWAcZwXx7PTx_yVniHn1BxPP` | Check the cut (not confirmed here) |
| DS-09 | How To Make Time To Work Out | `05_ad09_hd` | 63.7 s | `cc06dcb57d182511` | `1wp3aCo0SrXNdsrcWI9FljCAYWYybBkTd` | Yes (opener, student, robot) |
| DS-22 | How To Use The Ab Wheel | `07_abwheel_hd` | 44.6 s | `75fd5b4fa1997000` | `1KOmiZVmBN8zBWm_by9qh_3tw9N9WB07E` | No |

- **AI flag:** set YouTube synthetic and TikTok `ai_generated` to true only on the shorts that contain realistic AI
  video clips (table above; confirm DS-08 from its contact sheet). A labeled still goal image alone does not set it.
- **DS-09 is 63.7 s.** Check each platform's Shorts or Reels length limit in `/video-setup` before queuing it; if a
  platform refuses it, tell Dan. Do not trim it.
- Scripts and what each short is about: `Handoffs/video-editing/DS-<nn>-*.md`.

## 2. File them first
Follow `/video-setup` and `/editor-deliveries` naming: copy each file into the project's short-form delivery folder under
the standard name, to the Extreme drive, and to Google Drive (anyone with the link can view). Add or update the Edit
Queue row only at the end (`uploaded` is set after the queue write is read back, never before).

## 3. Covers (first half; stop for Dan's picks)
Five choices per short, each in both layouts (Instagram grid and YouTube), which count as one choice:
1. one real pool-shoot photo of Dan,
2. one real studio-shoot photo of Dan,
3. to 5. three AI-generated images, **each a different design** of Codex's choice (different layout, type treatment,
   color and concept; not one layout with three backgrounds).

- Make them with `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No Gemini or other outside
  image model. A real photo of Dan is never redrawn: Codex makes the background only, his real cutout and the type are
  layered in code.
- Rules that bite: no frowning photo, Speedo photos cropped at the waistband, text never over his face or any of his
  hair, abs visible, no "Real picture of me" label and no AbsByAI.com on a cover, no claims in cover copy.
- Exercise how-to shorts (Side Laterals, Ab Wheel): at least one choice should show the exercise itself.
- Show all choices on one review sheet per short, then **stop for Dan's picks**. Twenty-five covers is a lot to review:
  put the five sheets on one page, numbered, so he can answer in one line per short.

## 4. Queue (second half, after his picks)
- Write each short's Blotato config (title, description, tags, cover, AI flag, `"content_type": "organic"`,
  `"pinned_comment"` with one easy question about that video).
- **Blotato is at its 200 cap.** Do not create a scheduled task or routine to queue a single video. Add each config to
  `scripts/blotato/video_waitlist.json` as `"kind": "short"`; the daily `social-queue-daily-refresh` routine
  (`scripts/blotato/video_topup.py`) queues them on Tue/Thu/Sat as room frees. If room exists today, queue directly
  through the `/video-setup` scripts instead, dry run before every `--apply`.
- YouTube: Blotato only. Never upload organic content to YouTube ourselves, never Public, never native scheduling.
- TikTok takes no cover image through the API; follow `/video-setup` for the cover-first copy or the phone step.
- After any Blotato write, re-read the saved schedule and run the ad guard scan.

## 5. The two that follow
**Update 2026-10-13:** Muhammad sent both HD files at 09:42 UTC (Gmail message `1a134a751d5802e9`, links labeled
"3 Ways To Reduce Alcohol HD" and "How to do Rare Delt HD"). Not yet downloaded or checked. Hammer Curls and DS-05 are in
`handoff-20261013-muhammad-shorts-batch2-setup-and-ads-check.md`.

Muhammad owes high quality exports of DS-24 Rear Delt Flys V3 and DS-14 3 Ways To Reduce Alcohol V3 (both finalized,
his files were review size, about 22 MB). When they arrive:
- Prove each export is the finalized cut before using it:
  `/Volumes/Extreme/_edit_work/revisions-20261012/muhammad/light.sh <name> <new file> <review copy>` then
  `python3 fd.py <name>` in that folder (same frame count; average difference under 3; largest pixel difference under
  about 40). Review copies are in that folder's `dl/03_reardelt_hd` and `dl/06_alcohol_hd`.
- Reduce Alcohol has AI clips (opener and seltzer): AI flag true. Rear Delt Flys: false.
- Then run sections 2 to 4 for them. Covers for all seven can be made in the first pass if Dan prefers one review.

## Open risks
- The Extreme drive must be mounted; the Drive ids in the table are the fallback source.
- Spend: covers are on the Codex subscription, no paid image calls. No other spend is expected.

## Exact next action
Rename the task `Muhammad Shorts Batch SFC Setup`, read the files in "Read first", re-hash the five files, then build the
cover review page and stop for Dan's picks.

## Starter prompt (also in the chat message)
> Execute `Handoffs/handoff-20261012-muhammad-shorts-covers-and-setup.md`. Task name: `Muhammad Shorts Batch SFC Setup`. Category: CONTENT, five dedicated Shorts (SFC) from Muhammad, all finalized, plus two more when their HD exports arrive. Hammer Curls and M100s are not part of this task. Make five cover choices per short (one pool photo, one studio photo, three different AI designs), show them on one page and stop for my picks. Use the Codex subscription to generate the images. After my picks, file the videos and add them to the release queue through the waitlist, since Blotato is full. Do not re-edit the videos and do not treat any of them as an ad.
