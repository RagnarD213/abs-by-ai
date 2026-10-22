CONTENT | SL-18 | I'm 41 Wasted Life SFL Setup

# SL-18 I'm 41. I Wasted My Life. shorts (2): covers, then upload and schedule

Written 2026-10-22 by Claude (Opus 5.5). Two Shorts (`SFL`) cut by Claude from the RO-25 long-form "I'm 41. I Wasted My Life."
One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5, high effort** (the Shorts were
edited on Claude; cover design is editorial work). **Use the Codex subscription to generate the images.**

**Urgent: Short 1 airs Mon Oct 26, 9 AM Chicago.** Show Dan the cover sheet as early as possible (by Fri Oct 23) so the queue
write lands before the weekend. Short 2 airs Sat Dec 12.

Dan finalized both on 2026-10-22: *"Everything is approved. Give me the handoff for setup."* There is **no third Short**: the
calendar's "Wasted My Life 3" slot (Tue Dec 15) goes to another video Dan picks; this task does not fill it. Queue: SL-18
`finalized`. Batch card: `Short-form video content/wastedlife-SHORTS.md`. Reviews: `/Volumes/Expansion/_edit_work/SL-18/build/<B|D>/ROUND-*-REVIEW.md`.
Approvals: `/Volumes/Expansion/_edit_work/SL-18/approval_B.json`, `approval_D.json`. Edit recipe: `.claude/skills/shorts/reference/softblue-sl18/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (five cover choices made by Codex; Blotato only for organic; AI label rule;
   Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight, Facebook
   cover registry), "Blotato full?" (waiting list). Closest worked example: `Handoffs/handoff-20261021-sl19-healthy-foods-shorts-covers-and-setup.md`
   and its receipt `Docs/SL19_SETUP_RECEIPT_*.md`.
4. `Short-form video content/wastedlife-SHORTS.md` and the parent's receipt `Docs/RO25_SETUP_RECEIPT_20261017.md`.

## 1. The two files (final; never re-render or re-edit)

> ⚠ **Clipped title letters (2026-10-22):** Short 1 ("Backfire Long Term") have the tails of g/y cut off at the bottom of the title band. Dan decides whether to re-render them first (`Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). Covers may go ahead; do not upload these files until that decision is recorded, then use the hashes of whichever files he approves.

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), the film's approved mix cut only (plus the
declared audio repairs), with `.audio_gate.json` and `.deliver_gate.json` (gate 2.6.1, 39/39 PASS) beside each. Re-hash before
any upload; a mismatch means the file changed after approval: stop and tell Dan. The project folder sits in iCloud (memory
`documents-symlinked-into-icloud`): make sure each master is fully downloaded before hashing or copying.

| # | file | length | on-screen title (eyebrow) | AI flag | sha256 (first 8) | airs |
|---|---|---|---|---|---|---|
| 1 | `wastedlife-short1_why-adhd-meds-backfire-long-term.mp4` | 62.5 s | Why ADHD Meds Backfire Long Term (ADHD MEDICATION) | **true**: AI pill-and-water desk clip 0:08-0:13 (library A0209) | `130d3c14` | **Mon Oct 26 2026, 9 AM Chicago** |
| 2 | `wastedlife-short2_build-your-value-before-you-date.mp4` | 63.0 s | Build Your Value Before You Date (DATING IN YOUR 20S) | **true**: AI pool couple, two AI dating-app screens, AI dinner date 0:22.0-0:25.5 (library A0208) | `bbd9d0cb` | **Sat Dec 12 2026, 9 AM Chicago** |

Dates from `Docs/SHORTS_RELEASE_CALENDAR.md` ("Wasted My Life 1" Mon Oct 26, "Wasted My Life 2" Sat Dec 12). The parent RO-25
is public (https://www.youtube.com/watch?v=xyi-B_5tccw, Oct 18), so the parent-first rule is already met; still confirm it
loads. If Blotato is full, finish everything else and add the Short to `scripts/blotato/video_waitlist.json` (kind `short`, its
date); the daily routine queues it. Never create a one-video task. **For Short 1, the waiting list must not make it miss Oct 26:**
if the queue has no room by Fri Oct 23, tell Dan in one line (he may free a slot), do not delete anything yourself.

**Both are ORGANIC.** Closing words: 1 "...the long-term effects get so bad that you have to quit."; 2 "...you'll be able to
attract far better women than you can today." No "tap the button". Run the classification step and
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
  label, text clear of his face and every part of his hair. Masculine palettes (no pink or plum). Drug names are fine in organic
  (memory `organic-drug-names-allowed`).
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, different photos across the set, none already on the
  grid (`Short-form video content/covers/posted covers/`).
- Topic images for the AI designs. **Short 1:** a pill bottle beside a phone battery icon draining to red; AI Dan at a desk
  wired and buzzing, then slumped over it (a split before/after); a line that shoots up then crashes (the Short's own graph shape,
  cyan up, red down). **Short 2:** AI Dan in the gym or at a laptop building, his phone face down with a dating app on it; a
  ladder of better options climbing with the years; a fit couple at a candlelit dinner (the film's dinner clip). References Codex
  may use: `/Volumes/Expansion/_edit_work/SL-18/clips/` (`DESK.mp4` frames 0-111, `DATEA.mp4`, `A0061.mp4` pool couple, `A0089.mp4`
  phone screens; grab stills with ffmpeg) and the RO-25 thumbnail folder `social media graphics/youtube/thumbnails/Im 41 I Wasted My Life/`
  (finalized C and the round-2 abandoned-house image) for the film's look.
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the grid-safe
  centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 10 (grouped by Short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl18/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/wastedlife SL-18/` and Google Drive
   `Short-form video content/wastedlife SL-18/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check Extreme free
   space first (it has run down to 0-13 GB this week).
2. Per Short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy, Instagram
   PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl18-short<N>-<slug>.json` (copy an `sl19-short*` config; `content_type` organic, `source`, keyword
   `ABS` as the parent uses (`scripts/blotato/configs/ro25-wasted-my-life.json`), `utm_content=sl18-short<N>`, `ai_generated`
   true, `"pinned_comment"` written through `dan-voice-writer` (an easy question about that Short), YouTube description naming
   the full video by its title "I'm 41. I Wasted My Life." with its watch link). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per Short. Waiting list as in section 1 if Blotato is full.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL18_SETUP_RECEIPT_<date>.md` (schedule ids or waitlist entries,
   cover hashes, pinned comments, "articles: written by sixpackabs-article-gap-daily after release"), `queue.py set SL-18 uploaded`
   + Edit Queue artifact (`jobs/SL-18` was version 4 on 2026-10-22; pin `if_version`) + `mark-synced`, delete the board line,
   remove this handoff's OPEN line in `Handoffs/README.md`, commit and push (`scripts/git/safe-push.sh` from the main folder, or
   plain git from a clean checkout when safe-push stops on other sessions' conflicts; the main folder had an unfinished merge
   in `Handoffs/video-editing/jobs.json` on 2026-10-22).

## Starter prompt

> Name this task "I'm 41 Wasted Life SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261022-sl18-wasted-my-life-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the two I'm 41. I Wasted My Life. Shorts, show me one review sheet and stop for my picks, then upload and schedule them on every platform through Blotato (Short 1 on Mon Oct 26, Short 2 on Sat Dec 12). Use the Codex subscription to generate the images.
