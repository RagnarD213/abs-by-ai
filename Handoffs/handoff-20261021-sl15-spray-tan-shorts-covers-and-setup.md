CONTENT | SL-15 | My First Spray Tan SFL Setup

# SL-15 My First Spray Tan shorts (2): covers, then upload and schedule

Written 2026-10-21 by Claude (Opus 5.5). Two Shorts (`SFL`) cut by Claude from the RO-19 long-form "Spray Tanning Guide: How To
Looksmax With A Spray Tan". One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5, high
effort** (cover design is editorial work; the video was edited on Claude; memory `model-routing-plan`). **Use the Codex
subscription to generate the images.**

Dan finalized both on 2026-10-21: *"Hair is OK as is, both approved. Give me the handoff for setup."* Queue: SL-15 `finalized`.
Approval record: `/Volumes/Extreme/_edit_work/SL-15/APPROVAL.md`. Batch card: `Short-form video content/spraytan-SHORTS.md`.
Edit recipe: `.claude/skills/shorts/reference/softblue-sl15/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (the five cover choices made by Codex; Blotato only for organic YouTube; AI
   label rule; Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight, Facebook
   cover registry), "Blotato full?" (waiting list). Closest worked examples:
   `Handoffs/handoff-20261021-sl09-oura-shorts-covers-and-setup.md` and `Docs/SL07_SETUP_RECEIPT_20261018.md`.
4. `Short-form video content/spraytan-SHORTS.md`.

## 1. The two files (final; never re-render or re-edit)

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), the film's approved mix cut only, with
`.audio_gate.json` and `.deliver_gate.json` beside each. Re-hash before any upload; a mismatch means the file changed after
approval: stop and tell Dan. The delivery gate passes every row; `framing:hair_top` and `framing:headroom` are declared for these
two files with Dan's acceptance above (the 8/3 camera framed his hair at the top edge). Older duplicate renders were moved out to
`/Volumes/Extreme/_edit_work/SL-15/superseded/`: never upload anything named `... 2.mp4` or `... 3.mp4`.

| # | file | length | on-screen title (eyebrow SPRAY TANNING) | AI flag | sha256 (first 8) |
|---|---|---|---|---|---|
| 1 | `spraytan-short1_why-you-look-less-ripped-in-photos.mp4` | 57.7 s | Why You Look Less Ripped In Photos | false (real stock, Dan's real photos with the real-photo label) | `ec87695a` |
| 2 | `spraytan-short2_get-a-tan-without-sun-damage.mp4` | 46.6 s | Get A Tan Without Sun Damage | true (AI appointment clip 0:00-0:03.4, AI vampire 0:17.5-0:18.4) | `476b5a6f` |

**Release slots: the parent first.** RO-19 is on the Blotato waiting list (`Docs/RO19_SETUP_RECEIPT_20261013.md` expected
YouTube Sun Jan 17 2027; `Docs/LONGFORM_RELEASE_CALENDAR.md` lists it Wed Oct 21 with "Waitlist (TikTok uploaded by hand Thu
Oct 22)"). Read the live Blotato YouTube queue, `scripts/blotato/video_waitlist.json` and the channel for the parent's real
status before choosing any date. **No Short posts before the parent is verified public.** `Docs/SHORTS_RELEASE_CALENDAR.md`
holds "Spray Tan 1" in the week of Oct 26 (Fri Oct 30, 9 AM Chicago) on the condition that the parent is public by then; if it
is not, put both Shorts on the next free Mon/Tue/Fri/Sat 9 AM slots after the parent's release (Short 1 first) and tell Dan the
dates. If they must wait for the parent, add them to the waiting list (kind `short`) rather than creating a task.

**Both are ORGANIC.** Closing words: 1 "...you'll look much more defined."; 2 "...you're a lot more likely to get that kind of
cancer." No "tap the button". Run the classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every
Blotato write.

## 2. Covers (first half; stop for Dan's picks)

Five choices per Short, each in both layouts (Instagram grid and YouTube Shorts), which count as one choice:
1. one real pool-shoot photo of Dan; 2. one real studio-shoot photo of Dan; 3. one AI-enhanced or AI-generated image of Dan in
the Short's subject; 4. and 5. two more AI images of Codex's choice (Dan or not). Five unique designs per Short: write one line
per option naming its layout, type, colour and composition before building, and check no two share them.

- Codex makes all of them: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No other model. Real photos
  are never redrawn (Codex makes the background; his cutout from `photos/finalized social media photos/_cutouts/` and the type are
  layered in code). For option 3 give Codex a real photo as reference, "lean and shredded, not bulky", and check the face reads
  as him.
- Copy: the Short's title (same on all five), title case. No claims or numbers as results, no AbsByAI.com, no "Real picture"
  label, text clear of his face and every part of his hair.
- Photos: defined abs, tanned looks best for this topic, no frowning photos, Speedo crop at the waistband, different photos
  across the set, none already on the grid (`Short-form video content/covers/posted covers/`). Masculine palettes.
- Topic images for the AI designs: Short 1, a camera flash flattening a pale physique next to the same physique tanned, a
  photographer's studio light, bodybuilders tanned dark on stage; Short 2, a spray-tan booth with the mist, harsh noon sun on a
  beach, a man under a beach umbrella, sunscreen. Approved RO-19 AI frames Codex may use as references:
  `/Volumes/Extreme/_edit_work/ro19/aiframes/` (A1 vampire under the umbrella, A4 the spray-tan appointment) and the RO-19
  long-form thumbnail (Dan in a pop-up tanning tent, `Docs/RO19_SETUP_RECEIPT_20261013.md`).
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the grid-safe
  centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 10 (grouped by Short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl15/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/spraytan SL-15/` and Google Drive
   `Short-form video content/spraytan SL-15/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check Extreme free
   space first (it filled up on 2026-10-20). The project folder now sits in iCloud: confirm both masters are fully downloaded
   (sha256 above) before copying.
2. Per Short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy,
   Instagram PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl15-short<N>-<slug>.json` (copy an `sl07-short*` config; `content_type` organic, `source`, the
   keyword the parent RO-19 uses (`TRACK`, `scripts/blotato/configs/ro19-my-first-spray-tan.json`), `utm_content=sl15-short<N>`,
   `ai_generated` per the table, `"pinned_comment"` through `dan-voice-writer`, YouTube description naming the full video by its
   title "Spray Tanning Guide: How To Looksmax With A Spray Tan"). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per Short. If Blotato is full or the parent is not yet public, finish everything else and
   add each Short to `scripts/blotato/video_waitlist.json` (kind `short`); the daily routine queues it. Never create a one-video
   task.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL15_SETUP_RECEIPT_<date>.md` (schedule ids, cover hashes, pinned
   comments, "articles: written by the routine after release"), `queue.py set SL-15 uploaded` + Edit Queue artifact (`jobs/SL-15`
   was version 4 on 2026-10-21; pin `if_version`) + `mark-synced`, board one-liner, remove this handoff's OPEN line in
   `Handoffs/README.md`, commit and push with `scripts/git/safe-push.sh`.

## Starter prompt

> Name this task "My First Spray Tan SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261021-sl15-spray-tan-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the two spray tan Shorts, show me one review sheet and stop for my picks, then upload and schedule both on every platform through Blotato, never before the parent long-form is public. Use the Codex subscription to generate the images.
