# RO-05 "How I Make My Daily Salad": upload the captions (and publish the article) after it goes public

**Written 2026-09-30 by Claude (Opus 5.5). Fire on or after Sun Oct 18, 2026, 10 AM CT** (Blotato releases it at 9 AM CT;
give the sixpackabs page up to an hour to appear). Firing it earlier does nothing: the video it targets does not exist yet.

## 0. Update 2026-10-01 (Dan dropped the Private holding upload; Blotato-only YouTube now)
The Private copy `mfoSLivtvdQ` is no longer needed. A session on 09-30 tried captions on it and failed (Studio
"Upload captions failed"), and setting its language to English turned on YouTube auto-dubbing (~20 languages, still Private).
Do NOT touch it again. Whether to delete it (with the dubs) is Dan's call. On Oct 18 upload captions ONLY to the public
Blotato video, from the subtitle editor's Upload file route, never the Languages page.

## 1. Why
Dan wants the film's accurate subtitle file on the public YouTube video. YouTube's automatic captions miss words like
"broccolini", "adobo" and "AbsByAI.com". The upload token has no captions scope, so this is done in YouTube Studio.

⚠ **Upload to the PUBLIC video Blotato creates on Oct 18, not the Private holding copy `mfoSLivtvdQ`.** Blotato uploads its own
copy at release time, so it is a separate video with a new id. Captions on the holding copy never reach viewers.

The same trigger also owes the sixpackabs.com article (board entry "RO-05 salad"), so this handoff does both in one session.

## 2. Files and facts
- SRT: `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.srt`
  (277 cues, English, built from the approved master; last cue ends 14:53.59, film 14:53.86).
- The public video is the Blotato copy (`ro05-blotato.mp4`, same 26,789 frames and duration as the master), so the SRT timing matches as is.
- Blotato YouTube schedule `5014534`, submission `d25daf18-f66a-48da-b94f-871caa87f604`, account 46963, channel "Abs by AI".
- Title: "How I Make My Daily Salad: 700 Calories, $4 a Bowl, Fresh for 7 Days".
- Article: `sixpackabs/articles/TBD-daily-salad.md` (1,187 words, passes `build.py --check`). Rules: `sixpackabs/articles/README.md`.
- Setup record: `BLOTATO_QUEUE_PROGRESS.md` section "DONE: RO-05", receipt `Docs/RO05_SETUP_RECEIPT_20260930.md`.

## 3. Steps
1. **Confirm it posted and get the public id.** `blotato_get_post_status` on the submission id above (or `blotato_list_posts`)
   → the YouTube URL/id. Check with `node scripts/youtube/status.js <id>`: `public`, same title. If it failed or is missing,
   stop and tell Dan (memory `blotato-false-failure-large-video`: a "failed" can still be live, so check the channel too).
2. **Upload the captions in Studio** (Chrome MCP; Dan's Chrome is signed in to the Abs by AI brand channel):
   `https://studio.youtube.com/video/<public id>/translations` → if no English row, **Add language** → English →
   under Subtitles **Add** → **Upload file** → **With timing** → Continue → `find` the file input → `file_upload` with the
   absolute SRT path → **Publish**. Never click the native picker button itself.
3. **Verify:** reload the Subtitles page; the English row shows "Published" by the channel (not only "Automatic"). Open the
   watch page, turn on CC, spot-check around 4:25 ("broccolini") and 8:20 ("adobo").
4. **Publish the article:** follow `/video-setup` Step 6b.2: WordPress.com MCP `content-items.list` (`post_type: spa_video`,
   match `_spa_youtube_id` = the public id) → rename the file to `sixpackabs/articles/<public id>.md`, fill `id`, `post_id`,
   `slug` → `content-items.update` with the `build.py <file>` payload → `python3 sixpackabs/articles/verify.py <file>` prints OK.
   If the page is not there yet, wait for the hourly sync; do not create one by hand.
5. **Close out:** add the public id + "captions uploaded" + article URL to the RO-05 section of `BLOTATO_QUEUE_PROGRESS.md`;
   re-read `AI_COORDINATION.md` from disk and delete the "RO-05 salad" entry and this handoff's line; mark this row executed in
   `Handoffs/README.md`; commit and push (if the shared checkout still cannot push, cherry-pick onto a clean `origin/main`
   worktree as the 09-30 RO-05 session did). No dashboard row.

## 4. Traps
- Never change the video's visibility, title, thumbnail or description; only captions.
- Don't upload captions to `mfoSLivtvdQ` (Private holding copy). Leave that video alone.
- No em dashes in anything written.

## 5. Model and starter prompt
Claude **Sonnet 5, medium** (a mechanical checklist; Studio clicks plus one WordPress update). Escalate to Opus 5.5 only if
Studio's layout has changed and the steps above no longer match.

> Read `Handoffs/handoff-20260930-ro05-captions-and-article-after-release.md` in full and execute it: confirm RO-05 "How I Make My Daily Salad" went public on YouTube through Blotato, upload the RO-05 SRT as English captions to that public video in YouTube Studio, verify them, publish the sixpackabs.com article, update the records, commit and push.
