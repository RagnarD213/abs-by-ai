# SL-05 Stop Deadlifting shorts (5): upload and schedule, Claude half

**Written 2026-10-01 by Claude (Opus 5.5).** Job SL-05 on the Edit Queue, state `finalized` (Dan, 2026-10-01: "Both are
finalized", after "Everything else is looking good" on shorts 1, 4 and 5). Run it with `/video-setup`, **Shorts section**.
Covers: Codex builds them in its own task (`Handoffs/handoff-20261001-sl05-shorts-covers-codex.md`) and Dan pastes the
final paths into the starter prompt. Do not design, pick or edit a cover here. If a cover path is missing, set up the
shorts that have one and stop for the rest.

**Fire on or after Sun Oct 11 2026, once the parent long-form is confirmed public, and after Dan has the covers.**

## 1. What is approved
All five shorts, as delivered. Do not re-edit anything. Build folder (read-only for this task):
`/Volumes/Extreme/_edit_work/sl05/build/`. Notes: `Short-form video content/stop-deadlifting-SHORTS.md`.

**All five are ORGANIC, not ads.** Closing words (delivered-file transcripts, `gate/<S>_asr_clean.json`): short 1 "...This is
how most people end up quitting."; short 2 "...you will actually build more muscle with the safer exercise."; short 3
"...other exercises that are better for making you look better."; short 4 "...nice and slow and you're going to build those
lats"; short 5 "...then periodically getting injured and getting set back." None says "tap the button below". Still run
Step 0's classification and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

## 2. Files (all local and filed; no download step)
Folder `Short-form video content/`, each 1080x1920 29.97 fps, Zeeshan's audio (verbatim gate), `.audio_gate.json` and
`.deliver_gate.json` (PASS, GATE 2.4.0) beside each:

| # | file | length | on-screen small line / headline | suggested post title | sha256 (first 16) |
|---|---|---|---|---|---|
| 1 | `stop-deadlifting-short1_deadlifts-cause-more-injuries.mp4` | 56.9 s | STOP DOING DEADLIFTS / MORE INJURIES THAN EVERY OTHER LIFT | Deadlifts Cause More Injuries Than Every Other Lift | `b67c57ccdc6852c5` |
| 2 | `stop-deadlifting-short2_safer-lifts-build-more-muscle.mp4` | 50.2 s | BUILD MORE MUSCLE / SAFER LIFTS WIN LONG TERM | Safer Lifts Build MORE Muscle Long Term | `4e47fc961a08f59d` |
| 3 | `stop-deadlifting-short3_deadlifts-build-a-powerlifter-body.mp4` | 50.9 s | WANT AN AESTHETIC BODY? / DEADLIFTS BUILD A POWERLIFTER BODY | Deadlifts Build A Powerlifter Body, Not An Aesthetic One | `51c89fab6871185f` |
| 4 | `stop-deadlifting-short4_two-back-exercises-instead-of-deadlifts.mp4` | 59.1 s | SKIP THE DEADLIFT / 2 BACK EXERCISES TO DO INSTEAD | 2 Back Exercises To Do Instead Of Deadlifts | `44a35a16779c29e7` |
| 5 | `stop-deadlifting-short5_train-legs-without-deadlifts.mp4` | 38.3 s | SKIP THE DEADLIFT / TRAIN LEGS WITHOUT DEADLIFTS | Train Legs Without Deadlifts | `4381f541c459fc36` |

Re-hash each before upload; a mismatch means the file changed after approval: stop and tell Dan. Captions are burned in
(no `.srt`). **AI flag:** shorts 1, 2, 3 and 4 contain Zeeshan's AI video clips (`ai_generated: true`, YouTube synthetic
true); short 5 has stock only (`false`).

## 3. Packaging (per short)
- Titles: the "suggested post title" column (Dan saw the draft titles and asked for no change; he can still change one).
  Hooks and body copy: start from `stop-deadlifting-SHORTS.md`, "Suggested posting order and descriptions". No claims, no
  em dashes anywhere.
- Link: `https://absbyai.com/?utm_source=<platform>&utm_medium=short&utm_campaign=stop-deadlifting&utm_content=<slug>` (the
  queue script builds the per-platform links from the config).
- Config per short: copy an SL-04 config (`scripts/blotato/configs/sl04-short1-make-your-waist-look-smaller.json`) to
  `scripts/blotato/configs/sl05-short<N>-<slug>.json` (`content_type: organic`, `source` = the file above). Keyword: the
  parent uses `TRAIN` (`scripts/blotato/configs/stop-deadlifting.json`); confirm it in `Docs/MANYCHAT_KEYWORDS.md`.

## 4. Steps
1. **Board + queue:** add an ACTIVE entry. Queue stays `finalized` until all five are queued and read back, then
   `python3 scripts/edit-queue/queue.py set SL-05 uploaded --by Claude --note "..."`, mirror the printed row to the Edit
   Queue artifact db (pinned `if_version`; it was version 5 on 2026-10-01), `queue.py mark-synced SL-05`.
2. **Parent first:** "Why I Stopped Deadlifting at 40" is queued in Blotato for Sun Oct 11 9 AM CT on four platforms
   (`BLOTATO_QUEUE_PROGRESS.md`, config `scripts/blotato/configs/stop-deadlifting.json`). Confirm it actually posted on each
   platform before any short is scheduled. No short posts before its parent is public.
3. **Capacity:** the board lists Blotato near its 200-post cap. Five shorts x 4 accounts = 20 posts. Count free slots first;
   if there are not enough, queue in posting order as far as capacity allows and tell Dan what is left.
4. **Backups:** Shorts copies on the Extreme drive and Google Drive (the skill's three-copies rule; Drive anyone-with-link).
5. **YouTube: Blotato only (Dan, 2026-10-01).** No Private holding upload. Blotato creates and releases the public YouTube
   Short at the scheduled time. Follow the current `/video-setup` text, which overrides the SL-04 handoff on this point.
6. **Blotato per short:** `tiktok_cover.build()` cover-first TikTok copy (absolute paths), upload master + TikTok copy +
   both cover PNGs with `blotato_create_presigned_upload_url`, hash-check each download, write the config, dry-run
   `python3 scripts/blotato/organic_short_queue.py <config>`, then `--apply` (FB, IG @danrosefit, TikTok, YouTube). Never
   @abs.by.ai.
7. **Slots:** Tue/Thu/Sat 9 AM CT (14:00Z while CDT, 15:00Z after Nov 1), one short every 2-3 days, in the order from
   `stop-deadlifting-SHORTS.md` (short 1, 4, 2, 5, 3), none at the same minute as another post. Already taken (check live for
   newer): SL-04 shorts Oct 6-15, the $17 Ab Wheel shorts Oct 27 to Nov 5. The first free slots after Oct 11 are likely
   from Oct 17.
8. **Verify** every schedule in Blotato, write `Docs/SL05_SETUP_RECEIPT_<date>.md`, update `BLOTATO_QUEUE_PROGRESS.md` (the
   parent entry's "Owes: SL-05 shorts"), the board and `Handoffs/README.md`, commit and push (docs and configs only).

## 5. Traps
- Shared checkout: never `git stash -u`. If `main` cannot pull or push (board: "Shared checkout cannot push"), build the
  commit on `origin/main` with a temporary index, as SL-04's commit `dda0238` did.
- A Blotato `failed` on a video can still be live (memory `blotato-false-failure-large-video`); these files are all under 45 MB.
- TikTok covers are only settable at upload (frame 0); posted covers are editable for 7 days, on the phone only.
- Short 4 runs 59.1 s: under the 60 s Shorts limit, do not re-encode it longer.
- YouTube engagement ads fire automatically for new videos; leave that routine alone.

## 6. Model and starter prompt
Claude Opus 5.5, effort medium (a known, scripted flow).

> Read `Handoffs/handoff-20261001-sl05-shorts-video-setup.md` in full, then run `/video-setup` (Shorts section) for the five SL-05 Stop Deadlifting shorts (approved organic shorts). The finalized covers are: `<PASTE THE COVER PATHS>`. Confirm the parent long-form is public, then queue all five in Blotato on Tue/Thu/Sat slots in the order in the handoff, verify, and report.
