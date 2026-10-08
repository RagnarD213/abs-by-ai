# SL-03 Daily Salad shorts (6): covers, then upload and schedule

**Category: CONTENT. Six Shorts (`SFC`) cut from the long-form RO-05 "How I Make My Daily Salad". Written 2026-10-08 by
Claude (Opus 5.5). Task name: `Daily Salad SFC Setup`.** One Claude handoff covers both halves (Dan's rule, 2026-10-01).
**Model (Dan's call, 2026-10-08): ONE task on Opus 5.5 medium. Opus does the covers itself and hands the upload and
schedule half to a Sonnet subagent.** Why: the covers are design judgment (photo choice, layout, judging 30 images by
eye); the second half is a scripted checklist and the token-heavy part, and a subagent runs it in a small clean context
instead of on top of the cover images.

How the one task runs:
1. Opus does section 2 (covers) and stops for Dan's picks, then exports them.
2. Opus does the two checks that gate everything itself: the six file hashes, and the parent long-form public on all
   four platforms. If either fails, nothing is delegated.
3. Opus starts ONE subagent with the Agent tool, `model: "sonnet"`, in the foreground, for section 3 steps 3 to 9. The
   brief gives it this handoff's path, the approved cover paths, the posting order and the slots Opus chose from the
   live queue, and these rules: follow the steps and scripts exactly; dry-run before every `--apply`; never design or
   change a cover; on anything off-script (a failed upload, a slot conflict, a missing tool, a hash mismatch) stop and
   return what happened, do not improvise. It returns a table: short, platform, Blotato post id, scheduled time, cover.
4. Opus verifies on a fresh Blotato pull of its own (24 posts, times, accounts, no same-minute clash, `ad_guard.py
   --scan`), without redoing the work, then does step 10 (receipt, queue, board, push).
5. If the subagent cannot reach the Blotato tools or returns blocked, Opus finishes that part itself and says so.

Dan finalized all six on 2026-10-08: *"All right, these look good. You can go ahead and finalize all of these. Give me
the handoff for installation and setup for all these shorts here."* Queue: SL-03 `finalized`. Hashes and his words:
`/Volumes/Extreme/_edit_work/sl03/final/decisions.json`.

**When to fire: on or after Mon Oct 19 2026.** The parent goes public on YouTube Sun Oct 18 at 9 AM CT, and on Facebook,
Instagram and TikTok Mon Oct 19 at 9 AM CT (`Docs/RO05_SETUP_RECEIPT_20260930.md`). No short is scheduled until the
parent is confirmed public on all four. Fired earlier, the task makes the covers, stops for Dan's picks, and stops again
before any Blotato write.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (five cover choices; Blotato only for organic YouTube; AI label; Speedo crop;
   frowning photos; cover text never over his face or hair; review videos of 45 s or longer go in `Videos to Review/`).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (the locked cover type and grid-safe crop).
3. `/video-setup`, "Shorts" section and "YouTube Shorts cover verification". `Docs/SL05_SETUP_RECEIPT_20261001.md` is the
   closest worked example.
4. `Short-form video content/daily-salad-SHORTS.md` (what each short is).

## 1. The six files (final; never re-render or re-edit)

Folder `Short-form video content/`, each 1080x1920, 29.97 fps, captions burned in (no `.srt`), `.audio_gate.json` and
`.deliver_gate.json` (PASS, gate 2.4.0) beside each. Re-hash before any upload; a mismatch means the file changed after
approval: stop and tell Dan.

| # | file | length | on-screen topic / headline | suggested post title | sha256 (first 16) |
|---|---|---|---|---|---|
| 1 | `daily-salad-short1_break-your-fast-with-this.mp4` | 38.5 s | INTERMITTENT FASTING / BREAK YOUR FAST WITH THIS | Break Your Fast With This | `6b4238165a8bbaf5` |
| 2 | `daily-salad-short2_the-20-dollar-salad-for-4.mp4` | 43.6 s | MEAL PREP / THE $20 SALAD YOU CAN MAKE FOR $4 | The $20 Salad You Can Make For $4 | `d8c3d4fb31aca012` |
| 3 | `daily-salad-short3_keep-salads-fresh-7-days.mp4` | 48.3 s | MEAL PREP / KEEP YOUR SALADS FRESH FOR 7 DAYS | Keep Your Salads Fresh For 7 Days | `c270c1571d1b697f` |
| 4 | `daily-salad-short4_stop-buying-salad-dressing.mp4` | 55.7 s | DAILY SALAD / STOP BUYING SALAD DRESSING | Stop Buying Salad Dressing | `e4848c5f23c37dfa` |
| 5 | `daily-salad-short5_track-a-week-of-meals-from-1-photo.mp4` | 56.8 s | AI MACRO TRACKING / TRACK A WEEK OF MEALS FROM 1 PHOTO | Track A Week Of Meals From 1 Photo | `8f7fd9cf489154f2` |
| 6 | `daily-salad-short6_the-one-line-that-makes-it-accurate.mp4` | 54.4 s | AI CALORIE TRACKING / THE ONE LINE THAT MAKES IT ACCURATE | The One Line That Makes It Accurate | `b824dd8f4bad31b2` |

**All six are ORGANIC, not ads.** Closing words: 1 and 2 "...start doing what I'm doing right here."; 3 "...keeping it in
these sealed glass containers."; 4 "...Too little and it's going to be dry."; 5 "...just by doing this one meal prep
thing alone."; 6 "...almost near accurate for taking pictures." None says "tap the button below". Still run the
classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

**AI flag: false on all six** (`ai_generated: false`, YouTube synthetic false). No AI video clips, no AI images, no stock:
the picture is Dan's own shoot plus the app screen recording in shorts 5 and 6.

## 2. Covers (first half; stop for Dan's picks)

Five choices per short, 30 in all, each choice in both layouts (Instagram grid and YouTube), which count as one choice:
1. one real pool-shoot photo of Dan,
2. one real studio-shoot photo of Dan,
3. to 5. three AI-generated images, each a different design of Codex's choice that sells that short's topic.

- Make them with `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No Gemini or other outside
  model. A real photo of Dan is never redrawn: Codex makes the background only, and his real cutout
  (`photos/finalized social media photos/_cutouts/`) and the type are layered on in code.
- Cover copy: the short's headline from the table (same copy on all five choices). No claims, no `AbsByAI.com`, no
  "Real picture of me" label on a cover, text clear of his face and every part of his hair.
- Photos: abs clearly defined, no frowning photos (`Frowning Photos/` is off limits by default), Speedo photos cropped at
  the waistband. Use ten different photos across the six shorts where the library allows, and check
  `Short-form video content/covers/posted covers/` so a cover already on the grid is not repeated.
- A strong topic image for the AI designs: the finished salad (frames in the clip library, B-roll "finished daily salad
  bowl", registered 2026-10-08 under "SL-03 Daily Salad shorts"), the glass containers, the olive oil and vinegar, the
  phone showing the meal prep result (683 calories) for shorts 5 and 6.
- Show all 30 on one review sheet (three per row, grouped by short), **stop for Dan's picks**, then export his picks to
  `Short-form video content/covers/approved-sl03/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg` (YouTube JPEG 1080x1920 under 2 MB).

## 3. Upload and schedule (second half)

1. **Board and queue:** one ACTIVE line on `AI_COORDINATION.md`. Queue stays `finalized` until all six are queued and read
   back, then `python3 scripts/edit-queue/queue.py set SL-03 uploaded --by Claude --note "..."`, mirror the printed row
   to the Edit Queue artifact (`jobs/SL-03` was version 7 on 2026-10-08; read it first and pin `if_version`),
   `queue.py mark-synced SL-03`.
2. **Parent first:** confirm "How I Make My Daily Salad" is public on YouTube and posted on Facebook, Instagram and TikTok
   (Blotato posts `5014534`, `5014529`, `5014531`, `5014533`; a "failed" on a large video may still be live, verify on the
   platform). If it is not public, schedule nothing and tell Dan.
3. **Capacity:** six shorts x 4 accounts = 24 posts. Count free Blotato slots first; if short, queue in posting order as
   far as capacity allows and tell Dan what is left.
4. **Backups:** copies of the six on the Extreme drive and Google Drive (anyone with the link can view).
5. **YouTube: Blotato only.** No Private holding upload, no YouTube scheduling. Blotato creates and releases the public
   Short at the slot.
6. **Per short:** build the TikTok cover-first copy with `tiktok_cover.build()` (absolute paths), upload master, TikTok
   copy and both covers with `blotato_create_presigned_upload_url`, hash-check each download, write
   `scripts/blotato/configs/sl03-short<N>-<slug>.json` (copy `sl05-short1-deadlifts-cause-more-injuries.json`;
   `content_type: organic`), dry-run `python3 scripts/blotato/organic_short_queue.py <config>`, then `--apply`
   (Facebook, Instagram @danrosefit, TikTok, YouTube). Never @abs.by.ai.
7. **Copy:** titles from the table. Hooks and descriptions: write them from each short's own words (no claims, no em
   dashes). Link `https://absbyai.com/?utm_source=<platform>&utm_medium=short&utm_campaign=daily-salad&utm_content=<slug>`.
   Keyword: the parent uses `FOOD` (`scripts/blotato/configs/ro05-daily-salad.json`); confirm it in
   `Docs/MANYCHAT_KEYWORDS.md`.
8. **Slots:** Tue/Thu/Sat 9 AM CT (14:00Z while CDT, 15:00Z from Nov 1), one short per slot, none at the same minute as
   another post on those accounts. Read the live queue first: SL-05 shorts hold Oct 17 to 27 and the $17 Ab Wheel shorts
   Oct 27 to Nov 5, so the first free slots are probably in early November.
   **Posting order: 1, 4, 5, 2, 3, 6.** Two constraints from Dan's review: shorts 5 and 6 at least a week apart (they
   share the dictated note and the 683 against 720 result), and shorts 1 and 2 not back to back (same closing line).
9. **Verify** every schedule on a fresh pull, and after each YouTube release check the public Shorts tile shows the
   approved cover (the skill's cover verification section; fix through desktop Studio if it shows a frame).
10. **Close out:** `Docs/SL03_SETUP_RECEIPT_<date>.md`, update `BLOTATO_QUEUE_PROGRESS.md`, the board, `Handoffs/README.md`
    and `daily-salad-SHORTS.md`; commit and push docs and configs only (`scripts/git/safe-push.sh`).

## Traps
- TikTok takes no cover image, only frame 0: the cover-first copy is the cover. Posted covers are editable for 7 days, on
  the phone only.
- Blotato's 400 MB cap is not a risk here (the largest file is 117 MB).
- Short 5's title says "1 Photo" and the demo takes several photos in one go. Dan approved the title; leave it.
- The build folder `/Volumes/Extreme/_edit_work/sl03/` is read-only for this task. `batch.py plan` on any of the six
  would rewrite its plan and break the match with the delivered file.

## Starter prompt

> Name this task `Daily Salad SFC Setup`. Read `Handoffs/handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md` in
> full and the files it lists. The six Daily Salad shorts are finalized: do not re-edit them. First make five cover
> choices for each short (one pool photo, one studio photo, three AI designs). Use the Codex subscription to generate
> the images. Show me all of them on one review sheet and stop for my picks. After my picks, confirm the Daily Salad
> long-form is public on all four platforms, then hand the upload and scheduling to a Sonnet subagent as the handoff
> describes (Tue/Thu/Sat slots, order 1, 4, 5, 2, 3, 6), verify its work yourself, and report.

Model and effort: Claude Opus 5.5, medium. Fire on or after Mon Oct 19 to finish in one sitting.
