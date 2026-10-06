---
name: video-setup
description: >
  Take a FINISHED organic/content video, long-form or a dedicated Short (usually an editor's final shared as a Google Drive link) all the way to scheduled on every platform: download and file it (project folder, Extreme drive and Google Drive), add it to the Edit Queue, make five thumbnail choices with Codex in the command line (one pool photo, one studio photo, three AI designs; GPT-6.1 Sol high) and stop for Dan's pick, write the title, description with chapters and tags, and queue YouTube, Facebook, Instagram @danrosefit, and TikTok for release through Blotato. Use whenever Dan says a content video is "finished", "done", "final", sends a Drive link and asks to "queue it up", "set it up on all platforms", "put it in Blotato", "schedule it", or "get it on YouTube and everything else", even if he doesn't say "/video-setup". Paid ads go through /ad-setup; reviewing a cut is /revisions; thumbnails alone are /youtube-packaging; cutting Shorts is /shorts.
---

> **Shared writing rules (2026-10-06):** before writing, read `.claude/skills/_shared/WRITING-RULES.md`. It holds the rules every writing skill follows and the list of memory entries (`Docs/memory/`) to read. Where it and this skill disagree, the newer dated line wins.

> **Image generation: Codex only (Dan, 2026-10-01).** Every still image this skill generates (backgrounds, plates, AI frames, thumbnails, covers, posts, retouch passes) is made with `.claude/skills/_shared/codex-image.sh` on the ChatGPT subscription. Where the steps below name Nano Banana Pro, Gemini, Seedream, FLUX, `gemini-image.js`, `rep-t2i.js` or `replicate-edit.js` for a still image, use the helper instead. Read `.claude/skills/_shared/IMAGE-GENERATION.md` first. Video generation is unchanged.

Read `_shared/VIDEO-RULES.md` first.

# /video-setup — finished content video → YouTube + Blotato, every platform

Built 2026-09-13 on Zeeshan's "Ab Wheel Workout" (video 1, "Video 1 Rev 2.mp4", 3:52). Dan: *"Zishan has finished
his video. I want you to cue this up on all platforms, YouTube and everything else, using Blotato… set this up with
descriptions and thumbnails… Before setting it up, though, make the thumbnail images and show me five variations."*
Everything below ran end to end that day. Historical result: YouTube `b_bS9NdmL-g` (scheduled under the retired native-publication workflow for Sun 09-20 9 AM CT, thumbnails 5 vs 1 in Test & Compare), Blotato
schedules 4413699 / 4413701 / 4413702 / 4413703; record in `BLOTATO_QUEUE_PROGRESS.md`.

**Thumbnails are made HERE, by this Claude task, since 2026-10-02 (Dan).** Five choices: one pool-shoot photo, one studio-shoot
photo, three AI-generated designs of Codex's choice, built with `_shared/codex-image.sh --model gpt-6.1-sol --effort high` on
Dan's subscription, shown on one sheet, then STOP for his pick. Rule: `_shared/VIDEO-RULES.md`, first section. The split
described next and "CODEX's task" in Step 2 are superseded; Step 2 stays as the build spec with the new mix.

**Superseded 2026-10-02.** Thumbnail split (Dan, 2026-09-30, every organic content video from now on): Codex makes the thumbnail, Claude does the
upload and setup.** A Claude /video-setup session never designs thumbnails. It starts from the finalized thumbnail file Dan
hands it. If none was given: write the Codex thumbnail handoff (copy `Handoffs/handoff-20260930-ro05-thumbnails-codex.md`;
Step 2 below is its spec), give Dan its starter prompt, and stop, or ask Dan for the path if Codex already made it. The setup
session then has no Dan stop; everything is reversible and runs without asking.
**Blotato-only YouTube (Dan, 2026-10-01): there is NO Private holding upload any more. Blotato creates the one public
YouTube video at release time (title, description, thumbnail, AI flag all travel in its YouTube target). Never upload to
YouTube ourselves and never use YouTube native scheduling.** Anything that needs the YouTube id (thumbnail A/B test,
English captions, the sixpackabs article page) happens after release: see Step 6 and Step 6b.

## Step 0 — before anything

- **CLASSIFY IT FIRST from the video's own ending** (`_shared/VIDEO-RULES.md`, "Ad or organic?", Dan 2026-09-28):
  a "tap/click the button below" CTA = ad; "go to AbsByAI.com" / "leave me a comment" with no button CTA =
  organic. If that verdict disagrees with how the request or handoff labels it, tell Dan and wait before any upload.
- **IS THIS AN AD? If yes, STOP — this skill does not apply.** Ads are never published organically (Dan,
  2026-09-17; `AGENTS.md`); they go through `/ad-setup` only. Check the filed path (`<Editor> Ad Videos/…` = ad,
  `<Editor> Content Videos/…` = content) and `Docs/AD_VIDEO_IDS.md`. Dan asking to "set it up on all platforms" does
  **not** make an ad organic — that exact sentence published Ad 5 on four accounts on 09-16/17. Say "this is an ad —
  ads don't go organic, do you want it posted anyway?" and wait for his answer.
- Every config this skill writes carries `"content_type": "organic"` and a `"source"` path.
  `scripts/blotato/ad_guard.py` blocks the queue without them. Run `python3 scripts/blotato/ad_guard.py --scan`
  before and after the Blotato write.
- `git status`; add an entry to `AI_COORDINATION.md` → ACTIVE TASK.
- ffmpeg is NOT on PATH. Use `Media/video_edit/bin/ffmpeg` / `ffprobe` (absolute path from the project root).
- Video builds cap is two across sessions — a frame extraction is trivial, but check
  `ps -Ao command | grep -E 'ffmpeg|render\.py|whisper'` before a contact sheet of a long video.
- **Machine busy? Do not wait for a build slot (Dan, 2026-09-30).** The Blotato copy and the TikTok cover-first copy
  run even when two or more builds are going: `nice -n 20`, `-hwaccel videotoolbox`, `-c:v h264_videotoolbox`, audio
  stream-copied. Rule and reasoning: `_shared/VIDEO-RULES.md`, "Video builds: never run more than two at once".

## Shorts (DS-/SL- jobs): the same flow, the Shorts helper

A dedicated Short is already filed in `Short-form video content/` and its cover is already approved, so skip Steps 1-2.
Worked examples: DS-04, DS-17, DS-18 (`Docs/DS*_SETUP_RECEIPT_*.md`). no holding upload, then:
build the TikTok cover-first copy with `tiktok_cover.build()` (absolute paths: relative ones break its concat list),
upload master + TikTok copy + cover PNG with `blotato_create_presigned_upload_url` and hash-check each download,
write `scripts/blotato/configs/<slug>.json` (copy `ds18-kettlebell-deadlift.json`), then
`python3 scripts/blotato/organic_short_queue.py <config>` and `--apply`. It queues FB, IG @danrosefit, TikTok and the
public YouTube release (Blotato account 46963) and verifies all four. Shorts go out Tue/Thu/Sat; pick a slot with no
same-minute post on those accounts.

**Fixing a wrong-path upload:** the upload token cannot change an existing video's visibility (no `youtube` scope).
Switch it in Studio (`studio.youtube.com/video/<id>/edit` → Visibility → Private → Done → Save), then read back
`privacyStatus: private` by API.

## Step 1 — download, verify, file

- Drive folder: `~/bin/rclone lsl gdrive: --drive-root-folder-id <FOLDER_ID>` then
  `rclone copy gdrive: <workdir> --drive-root-folder-id <FOLDER_ID>`. Workdir:
  `/Volumes/Extreme/_edit_work/<slug>-publish/`. (The rclone "shared client_id" NOTICE is harmless.)
- Editors' folders hold several files — pick the newest `Rev` by name and modified date; a `.srt` beside it may
  belong to an earlier cut (check its last cue against the video's duration).
- **Even when Dan sends a single-file link, list its parent folder (`search_files` `parentId = '<parent>'`) and read
  the live revision doc before downloading.** If a newer Rev exists, or the doc's latest round asks for changes the
  linked file does not have, the newer file is the final. Verify it answers that round (measure the fix, confirm
  audio and cut unchanged) and set THAT one up. 2026-09-29: Dan linked "Video 3 rev 4" while Zeeshan's "Video 3 Rev 5"
  (the round-5 skin fix) was already in the folder; Rev 4 got queued everywhere and had to be swapped with
  `swap_media.py`.
- `ffprobe` duration + resolution; `md5 -q`.
- File a copy per `/editor-deliveries`: `<Editor> Content Videos/<title> - video N/<title> | <editor> | 16x9 | video N.mp4`
  (content numbers are per editor, in delivery order). md5 must match the download.
- If a revision round for this video is open in `AI_COORDINATION.md`, note that Dan has called it final.
- **Three copies, every time (Dan, 2026-09-29).** Besides the project folder, put the same final (plus its `.srt`) in:
  1. **Extreme drive:** `/Volumes/Extreme/<Editor> Content Videos/<title> - video N/<same file name>` (Codex finals use
     `/Volumes/Extreme/Codex Content Videos/`). md5 must match.
  2. **Google Drive:** `gdrive:<Editor> Content Videos/<title> - video N/` at the My Drive root, beside `Codex Content Videos`:
     `~/bin/rclone copy "<project folder>" "gdrive:<Editor> Content Videos/<title> - video N" --include "*.mp4" --include "*.srt"`
     (in the background; 700 MB takes a few minutes), then `rclone link` on the folder so it is anyone-with-the-link
     (memory `drive-always-public`), then `rclone lsl` to confirm the byte count. Give Dan the folder link.
  - A dedicated Short gets the same two copies under `Short-form video content/` on each drive.

## Step 2: five thumbnail variations, then STOP for Dan's pick (CODEX's task since 2026-09-30)

This step is done by Codex in its own task, never by the Claude setup session (split above). It stays here as Codex's
spec. Codex delivers `<title> - thumbnail FINAL.jpg` (1280x720 JPEG, under 2 MB) in
`social media graphics/youtube/thumbnails/<title>/` and Dan pastes the path into the Claude setup task, which only checks the
file conforms (size, format, under 2 MB) and uses it for the YouTube upload and Blotato's `youtube_cover_url`.

Dan's standing mix (updated 2026-09-30): **one pool photo, two different studio photos on topic-specific Jelly Beans style photographic backgrounds, one enhanced screenshot from the video, and one designer choice.** Same copy on all five. Every Codex cover/thumbnail handoff must list these five slots and link `_shared/VIDEO-RULES.md`, "Five cover and thumbnail choices per video". Read `/youtube-packaging` for the photo, crop and text-clearance rules. The older recipe below is an asset reference; adapt its source count and studio backgrounds to this mix.

Working build to copy: `social media graphics/youtube/thumbnails/Ab Wheel Workout/_build-2026-09-13/build.py`.
It imports the Ad 5 `build_clean.py` for the studio looks and reuses assets, so it costs **$0**:

| variation | source | recipe |
|---|---|---|
| pool ×2 | `_finished-ads-build-2026-09-10/final/p172-photo.jpg`, `p247-photo.jpg` — real Dan composited over a gen-filled 16:9 pool scene (IoU 0.99) | `pool(photo, keep_h)`: crop from the top at the waistline, side scrim, white Manrope + red bar + wordmark |
| studio ×2 | `photos/finalized social media photos/_cutouts/<name>_CUTOUT.png` | `studio(name, waist, 'O1')` dark studio / `'O2'` his own light backdrop |
| screenshot | a frame from the video at the most readable moment of the exercise | `screenshot(src)`: white text, doubled black stroke (the variant A Dan approved on the $17 ab wheel explainer) |

- **Photos are fixed choices, not a search:** p135 and p138 are FROWNING — never. p172 shows a black swim brief
  → `keep_h 0.845`; p247 → `keep_h 0.86`. Measured studio waists: blue-247 0.645, white-23 0.695, white-49 0.679,
  blue-231 0.571 (**but blue-231's raised elbow gets cut off at the top and his arm hides half his face — it was
  swapped out on 09-13**). Rotate photos away from what the previous video used when you can.
- **Screenshot frame:** `fps=1` timestamped contact sheet (`drawtext … %{pts\:hms}`, `tile=8x15`), then pull
  full-res candidates at 0.5 s. For a rollout: deepest extension, whole body incl. feet, head low so the band above
  is clear. Editors burn set labels ("Set 3" chip, olive green) into workout footage — `screenshot()` finds the chip
  by colour and inpaints it, and the **top headline line must cover that spot** (a Telea inpaint on stonework
  leaves a visible smudge on its own).
- **Copy:** short and big reads best — two lines (`AB WHEEL / WORKOUT`) beat three smaller ones at feed size.
  No claims or numbers-as-results (Dan edits copy anyway).
- **QC is in the script:** person-mask clearance ≥ 25 px on the RENDERED file (for the screenshot, measured only
  inside the text's own column range — raised feet elsewhere are not a collision). Fit width for the screenshot
  headline is 0.74 W; at 0.92 W the second line lands on his head.
- Look at the review sheet yourself before sending — every defect fixed on 09-13 (brief visible, elbow cropped,
  smudge, text on head) was visible on the sheet and invisible to the numbers.
- `SendUserFile` the `REVIEW_*.jpg` sheet (display `render`), list the five in plain words, and **stop**. Dan may pick
  one, or two for an A/B test ("A/B test between 1 and 5").

## Step 3: packaging (with Dan's finalized thumbnail in hand)

- **Title:** searchable, no hype claims. 09-13: *"Ab Wheel Workout: 3 Sets For Stronger Abs (Do It With Me)"*.
- **Description** → `<filed folder>/youtube-description.md`: one-line hook; absbyai.com link with
  `utm_source=youtube&utm_medium=video&utm_campaign=longform&utm_content=<slug>`; **chapters read off the contact
  sheet** (set starts, rests, the CTA — the editor's .srt is often from an earlier cut); a how-to paragraph; a link to
  the related explainer video when one exists; the AI-image disclosure line when an AI goal image appears; subscribe
  CTA; 3–5 hashtags.
- **Schedule:** 9 AM CT (14:00Z during CDT, 15:00Z after Nov 1) on a day with no other long-form. Check
  `BLOTATO_QUEUE_PROGRESS.md` for the latest long-forms; recent pattern Sun / Wed. @abs.by.ai retired 2026-09-24; never queue it.

## Step 4: RETIRED (2026-10-01), no YouTube holding upload

Dan dropped the Private holding copy: it duplicated what Blotato's YouTube target already carries (title, description,
thumbnail via `youtube_cover_url`, `ai_generated`), and it was a separate video that nothing carried over to the public
one. Do not run `scripts/youtube/upload.js` for organic content. Check the title, description, chapters and thumbnail
file carefully before the Blotato write instead, since the first YouTube id exists only after release.
(`--synthetic` rule still applies: `ai_generated` true ONLY for realistic AI footage, per `_shared/VIDEO-RULES.md`
"AI label on uploads".)

## Step 5 — Blotato release queue (YouTube + Facebook + IG + TikTok)

The connected Abs by AI YouTube account is Blotato account `46963`. Queue YouTube's release in Blotato for the
chosen time; do not recreate the retired native YouTube schedule. Treat a missing YouTube Blotato schedule as an
incomplete organic setup. Confirm the schedule by reading it back before reporting success.

1. `blotato_create_presigned_upload_url` (filename `.mp4`) → `curl -X PUT -H "Content-Type: video/mp4"
   --data-binary @<file> "<presignedUrl>"` in the background → `curl -sI <publicUrl>` and confirm
   `content-length` equals the local byte count. **Blotato caps uploads at 400 MB** — above that, re-encode
   (`nice -n 20`, `-hwaccel videotoolbox`, `h264_videotoolbox` ~4 Mbps, or ~2.8 Mbps for a film over 12 min, audio
   stream-copied) for Blotato only; YouTube still gets the master. Confirm frame count, duration and audio packets
   match the master.
2. Write `scripts/blotato/configs/<slug>.json` (fields documented at the top of `scripts/blotato/longform_queue.py`):
   hook / body / close in Dan's voice, ManyChat keyword per topic (`ABS` for ab content; the table is in
   `Docs/MANYCHAT_KEYWORDS.md`), `ai_generated` same as YouTube's synthetic flag (same rule: AI footage only, not a labeled AI still).
3. `python3 scripts/blotato/longform_queue.py <config>` (dry run: slot clashes + the 200-post cap), then `--apply`.
   The current helper covers the four non-YouTube accounts. Queue the connected YouTube account through Blotato too,
   using the same release time and media, and verify all five schedules on a fresh pull. Do not fall back to YouTube
   native scheduling if Blotato needs repair; leave the release unscheduled until the Blotato path works.
   - Facebook gets no `mediaType` (FB Reels cap at 90 s). TikTok long-form over ~10 min may exceed the account cap.
   - Organic links go to the absbyai.com root, never `/start` (keeps organic out of the `/start` A/B test).
4. **Give the TikTok post its cover — this step is not optional and cannot be done later.**
   TikTok's API takes no cover image, only a timestamp, so an uncovered post falls back to frame 0 of the video:
   Dan mid-word under a burned caption. `python3 scripts/blotato/tiktok_cover.py` audits the queue,
   `--build` prepends the designed cover as frame 0 (lossless; the viewer sees no change), `--apply` rebuilds
   the schedule with `videoCoverTimestamp: 0`. **A posted video's cover can only be changed within 7 days, in
   the mobile app** — miss that window and the screenshot is permanent. Why and how: `Docs/TIKTOK_COVERS.md`.

## Step 6 — thumbnail A/B in Studio (only when Dan picked two)

Runs AFTER release, on the public Blotato-created video (Dan 2026-10-01). Worked 09-13 through the Chrome MCP:

1. `navigate` to `https://studio.youtube.com/video/<id>/edit`, wait ~5 s.
2. Click the **"A/B Testing"** chip directly under the Title field (the Thumbnail section itself has no test button in
   the current layout). A dialog opens on "Title only" — click **"Thumbnail only"**. Slot 1 already holds the
   thumbnail upload.js set.
3. `find` "file input inside the second 'Add thumbnail' slot" → `file_upload` with the absolute path of the second pick
   (**`file_upload` works now** — the clipboard-paste trick in `/youtube-packaging` is no longer needed here). Never
   click "Add thumbnail" itself; it opens a native picker.
4. Footer reads "Thumbnail test ready" → **Set test** → back on the page click **Save** (top right).
5. Verify by reloading: the Thumbnail section shows both images with a **"Test"** label.
   - Blotato's upload carries thumbnail A; this step only adds B once the video is public. Put a "set up the thumbnail
     test and upload the English captions" line in the coordination entry for the publish day (captions: Studio
     Subtitles, **Upload file**, never the Languages page: setting the video language there turned on auto-dubbing, 09-30).

## Step 6b: the sixpackabs.com article (write now, publish once the video is public)

Every public video gets a page at `sixpackabs.com/videos/<slug>/` from the hourly `spa_sync`, up to an hour after it
goes public. Its body starts as the YouTube description; we replace it with a real article, because Google search is
the only channel that sends sixpackabs.com engaged visitors (GA4, 2026-09-22). Rules, file format, build and verify
scripts: `sixpackabs/articles/README.md`. Read it, and one finished article there as the bar.

1. **Now, in this session:** write `sixpackabs/articles/<youtube-id>.md` from the final's own words (transcribe the
   delivered file; never invent a claim), 800 to 1,500 words, Dan's first person, one `{CTA}` link, 1 to 3 internal
   links, excerpt under 155 characters. Leave `post_id: TBD`. `python3 sixpackabs/articles/build.py --check <file>`
   must print OK (it refuses em and en dashes). Commit it with the config in Step 7.
2. **Once the video is public** (the Blotato release time; the page appears within the hour): get the page's post id
   with the WordPress.com MCP (`content-items.list`, `post_type: spa_video`, match `_spa_youtube_id`), fill in
   `post_id`, publish with `content-items.update` (payload from `build.py <file>`), then
   `python3 sixpackabs/articles/verify.py <file>` must print OK. If that is a later session, the Step 7 coordination
   one-liner carries "publish sixpackabs article `<file>` after it posts".
3. Content videos only. Ads are never organic and never get a page (the feed excludes unlisted videos). A Short gets
   a 300 to 500 word article only when it answers a searchable question and no existing page covers the same topic.

## Step 7 — record and close

- `BLOTATO_QUEUE_PROGRESS.md`: a `## DONE — <title>` section (source file + md5, YouTube id + time + thumbnail(s),
  the four Blotato schedule ids, keyword, UTM, anything unusual).
- Commit the config, the build script and any doc changes (media stays out — `photos/`, thumbnails and videos are
  git-ignored or must not be committed; the repo is public). Push to `main`.
- Re-read `AI_COORDINATION.md` from disk; replace the entry with a one-liner "scheduled, nothing blocked, delete once
  it posts" (or delete it if Dan has nothing left to do). No dashboard row unless Dan asks.
- Tell Dan in plain words: when it goes live where, which thumbnail(s), and anything he might want to do in Studio.

## Edit queue: always update it (not optional, Dan 2026-09-29)

Every setup touches Dan's pinned Abs By AI Edit Queue page (procedure `.claude/skills/_shared/edit-queue/README.md`):

- **The video is a job on `Handoffs/video-editing/00-MASTER.md`** (`RO-` long-form, `DS-` dedicated short, `SL-` shorts
  set): after the Blotato posts (including YouTube) exist and read back, `queue.py set <ID> uploaded` +
  `ArtifactData set` of the printed file + `queue.py mark-synced <ID>`.
- **A newly final long-form (any editor's, including Zeeshan's own 16:9 finals that were never a job) owes shorts: add
  its `SL-` job in the same session.** Write `Handoffs/video-editing/SL-NN-<slug>-shorts.md` (copy SL-05), add the row
  under LIST 2 in `00-MASTER.md` (and drop the title from the "not delivered yet" line), `queue.py add <json>`, then
  `ArtifactData set` + `mark-synced`. Worked example: SL-05 Stop Deadlifting (2026-09-29).
- Tell Dan which job ID it is on the page.
