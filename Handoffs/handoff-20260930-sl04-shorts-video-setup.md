# SL-04 Arms & Shoulders shorts (5): upload and schedule, Claude half

**Written 2026-09-30 by Claude (Opus 5.5).** Job SL-04 on the Edit Queue, state `finalized` (all five shorts approved by Dan
2026-09-30). Run it with `/video-setup`, **Shorts section** ("Shorts (DS-/SL- jobs): the same flow, the Shorts helper"). Covers:
short 2's is already approved; Codex builds 1, 3, 4, 5 in its own task (`Handoffs/handoff-20260930-sl04-shorts-covers-codex.md`)
and Dan pastes the final paths into the starter prompt. Do not design, pick or edit a cover here. If any cover path is missing,
set up the shorts that have one and stop for the rest.

## 1. What is approved
- Shorts 2-5: Dan, 2026-09-30 ("looks good" / "looking good"; short 3 after its eyebrow became SIDE LATERAL TIP).
- Short 1: Dan, 2026-09-30, after the round-3 side-lateral ending: *"the short one is looking good. This is finalized and approved."*
- Do not re-edit anything. Build folder (read-only for this task): `/Volumes/Extreme/_edit_work/sl04/build/`.

**All five are ORGANIC, not ads.** Closing words (delivered-file transcripts, `gate/<S>_asr.json`): short 1 "...like this at the
top." then music-only reps; short 2 "...then do three or four rounds." then live-round clips; short 3 "...just make sure there's
no rocking."; short 4 "...no swinging, no rocking, no momentum."; short 5 "...whichever way works the best for you is perfectly
valid." None says "tap the button below". Still run Step 0's classification and `python3 scripts/blotato/ad_guard.py --scan`
before and after every Blotato write.

## 2. Files (all local and filed; no download step)
Folder `Short-form video content/`, each 1080x1920 29.97 fps, Zeeshan's audio (verbatim gate), `.audio_gate.json` and
`.deliver_gate.json` (PASS, GATE 2.3.2) beside each:

| # | file | length | sha256 (first 16) |
|---|---|---|---|
| 1 | `arms-shoulders-short1_make-your-waist-look-smaller.mp4` | 52.0 s | `952f3596c8090c35` |
| 2 | `arms-shoulders-short2_do-this-before-you-take-your-shirt-off.mp4` | 56.1 s | `8dc39f0e53c3426e` |
| 3 | `arms-shoulders-short3_raise-your-elbows-not-your-hands.mp4` | 30.9 s | `2931ce4f82178f98` |
| 4 | `arms-shoulders-short4_stop-swinging-your-curls.mp4` | 28.2 s | `f052cd5422dc2aa7` |
| 5 | `arms-shoulders-short5_how-to-do-bicep-curls.mp4` | 51.6 s | `d5e9f096788711b7` |

Re-hash each before upload; a mismatch means the file changed after approval: stop and tell Dan.
Short 2 covers (approved): `Short-form video content/covers/posted covers/arms-shoulders-short2_do-this-before-you-take-your-shirt-off_cover-B.png`
and `posted covers/youtube/` same name. Captions are burned in (no `.srt`). No AI footage in any of the five (the parent's AI goal
image at 10:48 is not in them): `ai_generated: false`, `--synthetic false`.

## 3. Packaging (per short)
- Titles, hooks and body copy: start from `Short-form video content/arms-shoulders-SHORTS.md` ("Suggested posting order and
  descriptions"). Short 1's line there is updated for its new ending (thumbs cue, live-round reps). Searchable titles, no claims,
  no em dashes anywhere.
- Link: `https://absbyai.com/?utm_source=<platform>&utm_medium=short&utm_campaign=arms-shoulders-home-workout&utm_content=<slug>`
  (the queue script builds the per-platform links from the config).
- Config per short: copy `scripts/blotato/configs/ds18-kettlebell-deadlift.json` to `scripts/blotato/configs/sl04-short<N>-<slug>.json`
  (`content_type: organic`, `source` = the file above, keyword: pick one that fits, e.g. `SHOULDERS` / `ARMS`, and check it exists in
  ManyChat per `Docs/MANYCHAT_KEYWORDS.md`, else use the parent's `ABS`).

## 4. Steps
1. **Board + queue:** add the ACTIVE entry. Queue stays `finalized` until all five are uploaded and queued, then
   `python3 scripts/edit-queue/queue.py set SL-04 uploaded --by Claude --note "..."`, write_db the exported row to the Edit Queue
   artifact (pinned `if_version`), `queue.py mark-synced SL-04`.
2. **Parent first:** the long-form "Arms & Shoulders Home Workout" was queued public for Sun Sep 27 (Blotato `4722756`, `4722757`,
   `4722920`, `4722764`; `BLOTATO_QUEUE_PROGRESS.md`). Confirm it actually posted before any short is scheduled; no short posts
   before its parent is public.
3. **Capacity:** the board lists Blotato at its 200-post cap. Five shorts x 4 accounts = 20 posts. Count free slots first; if
   there are not enough, queue in posting order as far as capacity allows and tell Dan what is left.
4. **Backups:** the Shorts copies on the Extreme drive and Google Drive (skill's "Three copies" rule; Drive anyone-with-link, memory
   `drive-always-public`).
5. **YouTube holding upload, PRIVATE, per short** (`node scripts/youtube/upload.js ... --privacy private --synthetic false` with the
   YouTube cover; run in the background, never re-run a slow upload). Read back `privacyStatus: private`. Never Public, never `publishAt`.
6. **Blotato per short:** `tiktok_cover.build()` cover-first TikTok copy (absolute paths), upload master + TikTok copy + both cover
   PNGs with `blotato_create_presigned_upload_url`, hash-check each download, write the config, dry-run
   `python3 scripts/blotato/organic_short_queue.py <config>`, then `--apply` (FB, IG @danrosefit, TikTok, public YouTube release,
   verified). Never @abs.by.ai.
7. **Slots:** Tue/Thu/Sat 9 AM CT (14:00Z while CDT, 15:00Z after Nov 1), one short every 2-3 days, in the order from
   `arms-shoulders-SHORTS.md` (short 2, 1, 5, 3, 4), no same-minute clash with other posts. Taken already (check live for newer):
   DS-18 Sat Oct 3, the $17 Ab Wheel shorts Oct 27 to Nov 5.
8. **Content ID:** shorts 1 and 2 end on Zeeshan's live-round track, which has sung vocals. Check the parent's YouTube Content ID
   status in Studio first; if the parent carries a claim on that song, tell Dan before those two go out.
9. **Verify** every schedule in Blotato, write `Docs/SL04_SETUP_RECEIPT_<date>.md`, update `BLOTATO_QUEUE_PROGRESS.md` (the parent
   entry's "Owes: SL-04 shorts"), the board entry and `Handoffs/README.md`, commit and push (docs and configs only).

## 5. Traps
- Shared checkout: never `git stash -u`. If `main` cannot pull or push (see the board's "Shared checkout cannot push"), build the
  commit on `origin/main` with a temporary index, as SL-04's commit `dda0238` did (in zsh, quote `"<sha>:refs/heads/main"`).
- A Blotato `failed` on a video can still be live (memory `blotato-false-failure-large-video`); these files are all under 40 MB.
- TikTok covers are only settable at upload (frame 0); posted covers are editable for 7 days, on the phone only.
- YouTube engagement ads fire automatically for new videos; leave that routine alone.

## 6. Model and starter prompt
Claude Opus 5.5, effort medium (a known, scripted flow).

> Read `Handoffs/handoff-20260930-sl04-shorts-video-setup.md` in full, then run `/video-setup` (Shorts section) for the five SL-04 Arms & Shoulders shorts (approved organic shorts). Short 2's cover is already approved. The finalized covers for shorts 1, 3, 4 and 5 are: `<PASTE THE FOUR COVER PATHS>`. Upload each to YouTube as Private, queue all five in Blotato on Tue/Thu/Sat slots in the order in the handoff, after confirming the parent long-form is public, verify, and report.
