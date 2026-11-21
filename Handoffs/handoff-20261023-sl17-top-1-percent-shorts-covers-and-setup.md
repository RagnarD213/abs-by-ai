CONTENT | SL-17 | Top 1 Percent SFL Setup

# SL-17 "I'm 41. My Life Is Top 1%. How I Did It." shorts (3): covers, then upload and schedule

Written 2026-10-23 by Claude (Opus 5.5). Three Shorts (`SFL`) cut by Claude from the RO-26 long-form "I'm 41. My Life Is Top 1%.
How I Did It." One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5, high effort.**
**Use the Codex subscription to generate the images.**

Dan approved all three: Shorts 1 and 3 on 2026-10-22, Short 2 (R2 recrop) on 2026-10-23: *"approved, handoff for setup"*.
Queue: SL-17 `finalized` (Edit Queue artifact `jobs/SL-17` version 3). Reviews: `/Volumes/Extreme/_edit_work/SL-17/review/ROUND-*-REVIEW-*.md`.
Edit recipe: `.claude/skills/shorts/reference/softblue-sl17/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (five cover choices made by Codex; Blotato only for organic; AI label rule;
   Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight, Facebook
   cover registry), "Blotato full?" (waiting list). Closest worked example: `Handoffs/handoff-20261022-sl18-wasted-my-life-shorts-covers-and-setup.md`
   and its receipt `Docs/SL18_SETUP_RECEIPT_*.md` (if written), else SL-19's.
4. The parent's receipt `Docs/RO26_SETUP_RECEIPT_20261017.md` and config `scripts/blotato/configs/ro26-top-1-percent.json`.

## 1. The three files (final; never re-render or re-edit)

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), the film's approved mix cut only, with
`.audio_gate.json` and `.deliver_gate.json` (gate 2.6.1, 39/39 PASS) beside each. Re-hash before any upload; a mismatch means the
file changed after approval: stop and tell Dan.

| # | file | length | on-screen title (eyebrow) | AI flag | sha256 (first 16) |
|---|---|---|---|---|---|
| 1 | `top1-short1_nutrition-matters-more-than-your-workouts.mp4` | 37.6 s | Nutrition Matters More Than Your Workouts (NUTRITION) | **true**: the film's approved AI salad-bite clip 0:18-0:23 (AI-GENERATED chip on it) | `3dd0eb49b83e7070` |
| 2 | `top1-short2_start-with-5-minutes-every-morning.mp4` | 36.0 s | Start With 5 Minutes Every Morning (WORKOUT HABIT) | false (real jump rope, ab wheel, kettlebell, squats) | `2443763bd108c63f` |
| 3 | `top1-short3_every-man-should-train-a-martial-art.mp4` | 43.1 s | Every Man Should Train A Martial Art (MARTIAL ARTS) | false (Pexels judo and Muay Thai clips, Dan's real black-belt photo and hug clip) | `65748f116f2aa8e7` |

**Dates.** `Docs/SHORTS_RELEASE_CALENDAR.md` holds one slot, "Top 1% 1" Sat Dec 19, written when none were edited. All three are
edited now, and edited Shorts release in 2026 ahead of unedited ones (see the calendar's "Moved" notes). Give Short 1 Sat Dec 19
unless an earlier free Mon/Tue/Fri/Sat exists, and Shorts 2 and 3 the next free Mon/Tue/Fri/Sat slots in 2026 (moving
not-yet-edited `*` entries later, as earlier setups did). Check the live Blotato queue, not just the calendar; record the dates
and a dated "Moved" note in the calendar. **Parent first:** RO-26 is on the waiting list with YouTube queued Sun Oct 25, 9 AM
(`video_waitlist.json`; board entry "Top 1 Percent LFC Setup - RELEASE HOLD"). Confirm it is public and use its real watch URL
in each description; if it is not public yet, finish everything else and tie each Short to it with `parent_config` on the
waiting list so none can air before it. If Blotato is full, add each Short to `scripts/blotato/video_waitlist.json` (kind
`short`, its date); the daily routine queues it. Never create a one-video task.

**All three are ORGANIC.** Closing words: 1 "It'll make a huge impact on the rest of your life."; 2 "Working out has made my life
better in so many ways."; 3 "...a better man. It'll make your life so much better." No "tap the button". Run the classification
step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

## 2. Covers (first half; stop for Dan's picks)

Five choices per Short (15 in all), each in both layouts (Instagram grid and YouTube Shorts), which count as one choice:
1. one real pool-shoot photo of Dan; 2. one real studio-shoot photo of Dan; 3. one AI-enhanced or AI-generated image of Dan in
the Short's subject; 4. and 5. two more AI images of Codex's choice (Dan or not). Five unique designs per Short: write one line
per option naming its layout, type, colour and composition before building, and check no two share them.

- Codex makes all of them: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No other model. Real photos
  are never redrawn (Codex makes the background; his cutout from `photos/finalized social media photos/_cutouts/` and the type
  are layered in code). For option 3 give Codex a real photo as reference, "lean and shredded, not bulky, same size as the
  reference", and check the face reads as him. Dan's latest cover taste (memory `cover-picks-ai-dan-acting-topic`): AI Dan
  acting the title out, yellow band, expressive when the topic needs it.
- Copy: the Short's title (same on all five), title case. No claims or numbers as results, no AbsByAI.com, no "Real picture"
  label, text clear of his face and every part of his hair. Masculine palettes (no pink or plum).
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, different photos across the set, none already on the
  grid (`Short-form video content/covers/posted covers/`), and none of the five RO-26 thumbnails reused as-is
  (`social media graphics/youtube/thumbnails/Top 1 Percent/`: Pool, Studio, Martial Arts, Four Habits, The Climb).
- Topic ideas for the AI designs. **Short 1:** AI Dan meal-prepping containers of salad and protein; a plate beating a dumbbell
  on a balance scale; a fork in a salad bowl beside an untouched gym bag. **Short 2:** AI Dan skipping rope at sunrise by the
  pool; a 5-minute timer on a phone beside a jump rope; a ladder of 5, 10, 15 minutes. **Short 3:** AI Dan in a gi with a black
  belt mid-throw; two belts (white and black) side by side; a calm fighter on a mat. Reference stills (grab with ffmpeg):
  `/Volumes/Extreme/_edit_work/SL-17/clips/` (`B0448.mp4` jump rope, `B0030.mp4` ab wheel, `black-belt-group.png`,
  `p6254568.mp4` / `p7989824.mp4` judo and Muay Thai, `Nutrition-B-approved-motion.mp4` salad bite).
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the grid-safe
  centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 15 (grouped by Short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl17/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/top1 SL-17/` and Google Drive
   `Short-form video content/top1 SL-17/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check Extreme free
   space first.
2. Per Short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy, Instagram
   PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl17-short<N>-<slug>.json` (copy an `sl18-short*` config; `content_type` organic, `source`, keyword
   `ABS` as the parent uses, `utm_content=sl17-short<N>`, `ai_generated` true for Short 1 only, `"pinned_comment"` written
   through `dan-voice-writer` (an easy question about that Short), YouTube description naming the full video by its title
   "I'm 41. My Life Is Top 1%. How I Did It." with its watch link). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per Short. Waiting list as in section 1 if Blotato is full or the parent is not public.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL17_SETUP_RECEIPT_<date>.md` (schedule ids or waitlist entries,
   cover hashes, pinned comments, "articles: written by sixpackabs-article-gap-daily after release"), `queue.py set SL-17 uploaded`
   + Edit Queue artifact (`jobs/SL-17`, pin `if_version`, was 3) + `mark-synced`, delete the board line, remove this handoff's
   OPEN line in `Handoffs/README.md`, commit and push (`scripts/git/safe-push.sh` from the main folder, or plain git from a clean
   checkout when safe-push stops on other sessions' conflicts).

## Starter prompt

> Name this task "Top 1 Percent SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261023-sl17-top-1-percent-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the three "I'm 41. My Life Is Top 1%." Shorts, show me one review sheet and stop for my picks, then upload and schedule them on every platform through Blotato on the Shorts calendar, after the long-form is public. Use the Codex subscription to generate the images.
