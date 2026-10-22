CONTENT | SL-19 | 3 Healthy Foods SFL Setup

# SL-19 3 Healthy Foods That Made Me Fat shorts (3): covers, then upload and schedule

Written 2026-10-21 by Claude (Opus 5.5). Three Shorts (`SFL`) cut by Claude from the RO-17 long-form "3 Healthy Foods That Made
Me Fat". One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5, high effort** (the
Shorts were edited on Claude; cover design is editorial work). **Use the Codex subscription to generate the images.**

Dan finalized all three on 2026-10-21: *"Everything is approved. Give me the handoff or setup."* (He did not ask for the two
optional polish points the audit raised; the files ship as they are.) Queue: SL-19 `finalized`. Batch card:
`Short-form video content/healthyfoods-SHORTS.md`. Final audit: `/Volumes/Extreme/_edit_work/SL-19/ROUND-1B-REVIEW.md`.
Edit recipe: `.claude/skills/shorts/reference/softblue-sl19/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (five cover choices made by Codex; Blotato only for organic; AI label rule;
   Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight, Facebook
   cover registry), "Blotato full?" (waiting list). Closest worked examples:
   `Handoffs/handoff-20261021-sl15-spray-tan-shorts-covers-and-setup.md` and `Docs/SL07_SETUP_RECEIPT_20261018.md`.
4. `Short-form video content/healthyfoods-SHORTS.md` and the parent's receipt `Docs/RO17_SETUP_RECEIPT_20261018.md`.

## 1. The three files (final; never re-render or re-edit)

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), the film's approved mix cut only, with
`.audio_gate.json` and `.deliver_gate.json` (gate 2.6.1, 39/39 PASS) beside each. Re-hash before any upload; a mismatch means the
file changed after approval: stop and tell Dan. The project folder now sits in iCloud (memory
`documents-symlinked-into-icloud`): make sure each master is fully downloaded before hashing or copying.

| # | file | length | on-screen title (eyebrow) | AI flag | sha256 (first 8) |
|---|---|---|---|---|---|
| 1 | `healthyfoods-short1_coconut-water-is-just-sugar-water.mp4` | 56.8 s | Coconut Water Is Just Sugar Water (LIQUID CALORIES) | **false**: stock clips only; the carton fact card is a still AI image with its AI-GENERATED label (VIDEO-RULES: a labelled still does not trigger the flag) | `95643513` |
| 2 | `healthyfoods-short2_trail-mix-more-calories-than-a-big-mac.mp4` | 52.5 s | Trail Mix Has More Calories Than A Big Mac (THE HEALTHY SNACK TRAP) | **true**: AI scale clip 0:00-0:03, AI couch snacker 0:27.8-0:33.1 | `6d98a3fc` |
| 3 | `healthyfoods-short3_my-4-high-protein-snacks.mp4` | 52.2 s | My 4 Go-To High-Protein Snacks (WHAT I SNACK ON) | **true**: AI sardine eater 0:00-0:01.9 (plus the AI Chipotle-cup still) | `56ec71eb` |

(The batch card says the flag is true on all three; Short 1 is false per the rule above. Use this table.)

**Release slots, parent first.** RO-17 is on the Blotato waiting list for YouTube **Sun Dec 13, 2026, 9 AM Chicago** (socials Mon
Dec 14 noon). `Docs/SHORTS_RELEASE_CALENDAR.md`: **Short 1 = Mon Dec 14, 9 AM Chicago** ("3 Healthy Foods 1 (SL-19)"). Shorts 2
and 3 go in 2027 with the other carried-over Shorts, on the next free Mon/Tue/Fri/Sat 9 AM slots after 2026 is full (read the
calendar and the live queue; tell Dan the dates). **No Short posts before RO-17 is verified public**: check the live Blotato
queue, `scripts/blotato/video_waitlist.json` and the channel. If Blotato is full or the parent is still on the waiting list,
finish everything else and add each Short to `scripts/blotato/video_waitlist.json` (kind `short`, the target date); the daily
routine queues it. Never create a one-video task.

**All three are ORGANIC.** Closing words: 1 "...from using a zero-calorie electrolyte powder."; 2 "...wondering why you're still
fat."; 3 "...that's the best fast food snack out there." No "tap the button". Run the classification step and
`python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

## 2. Covers (first half; stop for Dan's picks)

Five choices per Short, each in both layouts (Instagram grid and YouTube Shorts), which count as one choice:
1. one real pool-shoot photo of Dan; 2. one real studio-shoot photo of Dan; 3. one AI-enhanced or AI-generated image of Dan in
the Short's subject; 4. and 5. two more AI images of Codex's choice (Dan or not). Five unique designs per Short: write one line
per option naming its layout, type, colour and composition before building, and check no two share them.

- Codex makes all of them: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No other model. Real photos
  are never redrawn (Codex makes the background; his cutout from `photos/finalized social media photos/_cutouts/` and the type
  are layered in code). For option 3 give Codex a real photo as reference, "lean and shredded, not bulky, same size as the
  reference", and check the face reads as him. Dan's latest cover taste (memory `cover-picks-ai-dan-acting-topic`, 2026-10-21):
  AI Dan acting the title out, yellow band, expressive when the topic needs it.
- Copy: the Short's title (same on all five), title case. No claims or numbers as results, no AbsByAI.com, no "Real picture"
  label, text clear of his face and every part of his hair. Masculine palettes (no pink or plum).
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, different photos across the set, none already on the
  grid (`Short-form video content/covers/posted covers/`).
- Topic images for the AI designs. Short 1: a coconut water carton next to a soda can, sugar cubes pouring out of a coconut,
  Dan pushing away a carton for plain water with an electrolyte stick. Short 2: trail mix outweighing a cheeseburger on a scale
  (the film's approved A3 frames), a measuring cup of trail mix vs a Big Mac, a hand deep in a giant trail mix bag. Short 3:
  sardines, hard-boiled eggs, a rotisserie chicken and a protein cup laid out together; Dan eating sardines from the tin.
  Approved RO-17 AI frames Codex may use as references: `/Volumes/Extreme/_edit_work/RO-17/round3/aiframes/` (A3 scale, A2 couch,
  A10 sardine eater, S1 carton, S3 chicken cup); the RO-17 thumbnail (Dan shirtless behind trail mix, dried mango, a coconut and a
  carton on electric blue: `social media graphics/youtube/thumbnails/3 Healthy Foods/3 Healthy Foods - thumbnail FINAL.jpg`).
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the grid-safe
  centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 15 (grouped by Short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl19/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/healthyfoods SL-19/` and Google Drive
   `Short-form video content/healthyfoods SL-19/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check Extreme free
   space first (it filled to 0 bytes on 2026-10-20).
2. Per Short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy, Instagram
   PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl19-short<N>-<slug>.json` (copy an `sl07-short*` config; `content_type` organic, `source`, keyword
   `FOOD` as the parent uses (`scripts/blotato/configs/ro17-3-healthy-foods.json`), `utm_content=sl19-short<N>`, `ai_generated`
   per the table, `"pinned_comment"` written through `dan-voice-writer` (an easy question about that Short), YouTube description
   naming the full video by its title "3 Healthy Foods That Made Me Fat"). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per Short. Waiting list as in section 1 if Blotato is full or the parent is not public.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL19_SETUP_RECEIPT_<date>.md` (schedule ids or waitlist entries,
   cover hashes, pinned comments, "articles: written by sixpackabs-article-gap-daily after release"), `queue.py set SL-19 uploaded`
   + Edit Queue artifact (`jobs/SL-19` was version 4 on 2026-10-21; pin `if_version`) + `mark-synced`, delete the board line,
   remove this handoff's OPEN line in `Handoffs/README.md`, commit and push (`scripts/git/safe-push.sh` from the main folder, or
   plain git from a clean checkout when safe-push stops on other sessions' conflicts).

## Starter prompt

> Name this task "3 Healthy Foods SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261021-sl19-healthy-foods-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the three 3 Healthy Foods Shorts, show me one review sheet and stop for my picks, then upload and schedule them on every platform through Blotato (Short 1 on Mon Dec 14), never before the parent long-form is public. Use the Codex subscription to generate the images.
