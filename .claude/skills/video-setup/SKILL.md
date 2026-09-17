---
name: video-setup
description: Take a FINISHED organic/content long-form video (usually an editor's final shared as a Google Drive link) all the way to scheduled on every platform — download and file it, build thumbnail variations for Dan to pick from, write the title, description with chapters and tags, upload the YouTube holding copy Private, and queue YouTube, Facebook, Instagram @danrosefit, TikTok and the @abs.by.ai mirror for release through Blotato. Use whenever Dan says a content video is "finished", "done", "final", sends a Drive link and asks to "queue it up", "set it up on all platforms", "put it in Blotato", "schedule it", or "get it on YouTube and everything else" — even if he doesn't say "/video-setup". Paid ads go through /ad-setup; reviewing a cut is /revisions; thumbnails alone are /youtube-packaging; cutting Shorts is /shorts.
---

# /video-setup — finished content video → YouTube + Blotato, every platform

Built 2026-09-13 on Zeeshan's "Ab Wheel Workout" (video 1, "Video 1 Rev 2.mp4", 3:52). Dan: *"Zishan has finished
his video. I want you to cue this up on all platforms, YouTube and everything else, using Blotato… set this up with
descriptions and thumbnails… Before setting it up, though, make the thumbnail images and show me five variations."*
Everything below ran end to end that day. Historical result: YouTube `b_bS9NdmL-g` (scheduled under the retired native-publication workflow for Sun 09-20 9 AM CT, thumbnails 5 vs 1 in Test & Compare), Blotato
schedules 4413699 / 4413701 / 4413702 / 4413703; record in `BLOTATO_QUEUE_PROGRESS.md`.

**One stop for Dan, and only one: the thumbnail pick.** Everything else is reversible and runs without asking.
**Permanent visibility rule (Dan, 2026-09-16): upload organic YouTube videos Private and leave them Private;
Blotato owns the scheduled release, including YouTube. Never upload Public and never use YouTube native scheduling.**

## Step 0 — before anything

- **IS THIS AN AD? If yes, STOP — this skill does not apply.** Ads are never published organically (Dan,
  2026-09-17; `AGENTS.md`); they go through `/ad-setup` only. Check the filed path (`<Editor> Ad Videos/…` = ad,
  `<Editor> Content Videos/…` = content) and `Docs/AD_VIDEO_IDS.md`. Dan asking to "set it up on all platforms" does
  **not** make an ad organic — that exact sentence published Ad 5 on four accounts on 09-16/17. Say "this is an ad —
  ads don't go organic, do you want it posted anyway?" and wait for his answer.
- Every config this skill writes carries `"content_type": "organic"` and a `"source"` path.
  `scripts/blotato/ad_guard.py` blocks the queue without them. Run `python3 scripts/blotato/ad_guard.py --scan`
  before and after the Blotato write.
- `git status`; add an entry to `AI_COORDINATION.md` → ACTIVE TASK ("thumbnail pick pending").
- ffmpeg is NOT on PATH. Use `Media/video_edit/bin/ffmpeg` / `ffprobe` (absolute path from the project root).
- Video builds cap is two across sessions — a frame extraction is trivial, but check
  `ps -Ao command | grep -E 'ffmpeg|render\.py|whisper'` before a contact sheet of a long video.

## Step 1 — download, verify, file

- Drive folder: `~/bin/rclone lsl gdrive: --drive-root-folder-id <FOLDER_ID>` then
  `rclone copy gdrive: <workdir> --drive-root-folder-id <FOLDER_ID>`. Workdir:
  `/Volumes/Extreme/_edit_work/<slug>-publish/`. (The rclone "shared client_id" NOTICE is harmless.)
- Editors' folders hold several files — pick the newest `Rev` by name and modified date; a `.srt` beside it may
  belong to an earlier cut (check its last cue against the video's duration).
- `ffprobe` duration + resolution; `md5 -q`.
- File a copy per `/editor-deliveries`: `<Editor> Content Videos/<title> - video N/<title> | <editor> | 16x9 | video N.mp4`
  (content numbers are per editor, in delivery order). md5 must match the download.
- If a revision round for this video is open in `AI_COORDINATION.md`, note that Dan has called it final.

## Step 2 — five thumbnail variations, then STOP for Dan's pick

Dan's standing mix (09-13): **two pool-shoot photos on a natural background, two studio photos, one screenshot
from the video** with big text above his head. Same copy on all five. Read `/youtube-packaging` first for the
type system, the frowning-photos rule, the waistline-crop rule and the text-never-on-Dan rule.

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

## Step 3 — packaging (after the pick)

- **Title:** searchable, no hype claims. 09-13: *"Ab Wheel Workout: 3 Sets For Stronger Abs (Do It With Me)"*.
- **Description** → `<filed folder>/youtube-description.md`: one-line hook; absbyai.com link with
  `utm_source=youtube&utm_medium=video&utm_campaign=longform&utm_content=<slug>`; **chapters read off the contact
  sheet** (set starts, rests, the CTA — the editor's .srt is often from an earlier cut); a how-to paragraph; a link to
  the related explainer video when one exists; the AI-image disclosure line when an AI goal image appears; subscribe
  CTA; 3–5 hashtags.
- **Schedule:** 9 AM CT (14:00Z during CDT, 15:00Z after Nov 1) on a day with no other long-form. Check
  `BLOTATO_QUEUE_PROGRESS.md` for the latest long-forms; recent pattern Sun / Wed. The @abs.by.ai mirror goes the
  next day, same time.

## Step 4 — YouTube holding upload (Private only)

```bash
node scripts/youtube/upload.js --file "<filed mp4>" --title "<title>" \
  --description-file "<filed folder>/youtube-description.md" --privacy private \
  --tags "a,b,c" --made-for-kids false --synthetic true|false \
  --thumbnail "<picked thumbnail A>"
```

- Run it in the background — a 300 MB file takes minutes. **Never re-run on a slow upload: YouTube does not dedupe,
  a second run makes a second video.** Read the output file; only retry after a clear failure.
- Read back the completed record and require `privacyStatus: private`. Do not add a YouTube `publishAt` value or
  schedule it in Studio. A Public, Scheduled or unknown result fails the workflow and must be corrected.
- `--synthetic true` whenever an AI image of Dan appears on screen (the absbyai.com CTA usually shows one).
- Two thumbnails picked → the second goes in via Studio's **Test & Compare** (Studio-only; the token has no
  `youtube.force-ssl`). See Step 6.

## Step 5 — Blotato release queue (YouTube + Facebook + IG + TikTok)

The connected Abs by AI YouTube account is Blotato account `46963`. Queue YouTube's release in Blotato for the
chosen time; do not recreate the retired native YouTube schedule. Treat a missing YouTube Blotato schedule as an
incomplete organic setup. Confirm the schedule by reading it back before reporting success.

1. `blotato_create_presigned_upload_url` (filename `.mp4`) → `curl -X PUT -H "Content-Type: video/mp4"
   --data-binary @<file> "<presignedUrl>"` in the background → `curl -sI <publicUrl>` and confirm
   `content-length` equals the local byte count. **Blotato caps uploads at 400 MB** — above that, re-encode
   (`h264_videotoolbox` ~4 Mbps, audio stream-copied) for Blotato only; YouTube still gets the master.
2. Write `scripts/blotato/configs/<slug>.json` (fields documented at the top of `scripts/blotato/longform_queue.py`):
   hook / body / close in Dan's voice, ManyChat keyword per topic (`ABS` for ab content; the table is in
   `Docs/MANYCHAT_KEYWORDS.md`), `ai_generated` same as YouTube's synthetic flag.
3. `python3 scripts/blotato/longform_queue.py <config>` (dry run: slot clashes + the 200-post cap), then `--apply`.
   The current helper covers the four non-YouTube accounts. Queue the connected YouTube account through Blotato too,
   using the same release time and media, and verify all five schedules on a fresh pull. Do not fall back to YouTube
   native scheduling if Blotato needs repair; leave the holding upload Private until the Blotato path works.
   - Facebook gets no `mediaType` (FB Reels cap at 90 s). TikTok long-form over ~10 min may exceed the account cap.
   - Organic links go to the absbyai.com root, never `/start` (keeps organic out of the `/start` A/B test).
4. **Give the TikTok post its cover — this step is not optional and cannot be done later.**
   TikTok's API takes no cover image, only a timestamp, so an uncovered post falls back to frame 0 of the video:
   Dan mid-word under a burned caption. `python3 scripts/blotato/tiktok_cover.py` audits the queue,
   `--build` prepends the designed cover as frame 0 (lossless; the viewer sees no change), `--apply` rebuilds
   the schedule with `videoCoverTimestamp: 0`. **A posted video's cover can only be changed within 7 days, in
   the mobile app** — miss that window and the screenshot is permanent. Why and how: `Docs/TIKTOK_COVERS.md`.

## Step 6 — thumbnail A/B in Studio (only when Dan picked two)

Worked 09-13 through the Chrome MCP on a SCHEDULED (still private) video:

1. `navigate` to `https://studio.youtube.com/video/<id>/edit`, wait ~5 s.
2. Click the **"A/B Testing"** chip directly under the Title field (the Thumbnail section itself has no test button in
   the current layout). A dialog opens on "Title only" — click **"Thumbnail only"**. Slot 1 already holds the
   thumbnail upload.js set.
3. `find` "file input inside the second 'Add thumbnail' slot" → `file_upload` with the absolute path of the second pick
   (**`file_upload` works now** — the clipboard-paste trick in `/youtube-packaging` is no longer needed here). Never
   click "Add thumbnail" itself; it opens a native picker.
4. Footer reads "Thumbnail test ready" → **Set test** → back on the page click **Save** (top right).
5. Verify by reloading: the Thumbnail section shows both images with a **"Test"** label.
   - It reads **"Ineligible — Your video is not public"** until the publish time. That is expected; the test starts
     once the video is public. Put a "check the test is running" line in the coordination entry for the publish day.

## Step 7 — record and close

- `BLOTATO_QUEUE_PROGRESS.md`: a `## DONE — <title>` section (source file + md5, YouTube id + time + thumbnail(s),
  the four Blotato schedule ids, keyword, UTM, anything unusual).
- Commit the config, the build script and any doc changes (media stays out — `photos/`, thumbnails and videos are
  git-ignored or must not be committed; the repo is public). Push to `main`.
- Re-read `AI_COORDINATION.md` from disk; replace the entry with a one-liner "scheduled, nothing blocked, delete once
  it posts" (or delete it if Dan has nothing left to do). No dashboard row unless Dan asks.
- Tell Dan in plain words: when it goes live where, which thumbnail(s), and anything he might want to do in Studio.

## Edit queue: mark it UPLOADED

After the Private YouTube upload is read back **and** the Blotato posts exist: if the video is a job on
`Handoffs/video-editing/00-MASTER.md` (`RO-` long-form, `DS-` dedicated short, `SL-` shorts set), set it to `uploaded` on
Dan's pinned Abs By AI Edit Queue page (`queue.py set <ID> uploaded` + `Artifact write_db`; procedure
`.claude/skills/_shared/edit-queue/README.md`). A newly final long-form owes shorts: add its `SL-` job in the same session.
