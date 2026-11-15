---
name: process-footage
description: Process raw camera footage after (or during) a shoot, end to end - offload every card to the Extreme drive (making room by moving finished edit folders to the Seagate), keep a verified second copy on the Seagate and back it all up to Google Drive, transcribe and map every roll to its script, put every filmed video on the Abs By AI Edit Queue, write the shoot footage report, and rebuild the "Unfilmed Content And Ads" Google Doc of everything not filmed this shoot or the last one. Use whenever Dan says the SD card is in, "we finished part of the shoot", "offload the footage", "move the footage to the Extreme", "categorize the footage", "add everything filmed to the edit queue", or types /process-footage, even if he only names one of these steps. It does not edit videos, make thumbnails or schedule anything.
---

# /process-footage: from camera card to Edit Queue

Built 2026-11-14 from the 11/13 green-screen shoot (Dan: "do everything that we always do when we've got raw
footage"). Every step below was done by hand on that shoot; the traps it hit are written in. Read
`AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` and memory `work-drive-order` first.

**What Dan gets at the end:** footage safe on three copies (Extreme, Seagate, Google Drive), every filmed video
on the Edit Queue with a work doc, a shoot footage report, and the Unfilmed Content And Ads Doc. Then the two
wrap-up boxes. He starts the edits himself; this skill never launches one.

**Run commands on the Mac the drives are plugged into.** Since 2026-11-14 that is the M2 (`ssh m2`; repo at
`~/Projects/Claude/Projects/Abs By AI`). Check with `ls /Volumes` on each Mac. The card reader is on the same
Mac as the drives. Long jobs run in the background (`nohup`, a log file) and you watch them with Monitor;
tell Dan in one line at each milestone (each card copied, backed up, mapped, queued).

Scripts are in `.claude/skills/process-footage/scripts/` (each has full `--help`):
`offload.py`, `audio_map.py`, `announcements.py`, `register_jobs.py`, `unfilmed_doc.py`.

---

## 1. Look at the card and name the shoot

1. `python3 .claude/skills/process-footage/scripts/offload.py scan` lists every card, its clips, sizes, camera dates, and free space on the
   Extreme and the Seagate.
2. Look at what was filmed before naming anything: the card's thumbnails (`PRIVATE/M4ROOT/THMBNL/*.JPG` on
   the Sony) in one contact grid, plus the shoot plan for the day (filming docs, `Docs/NEXT_SHOOT_LIST.md`).
3. Shoot folder name: `M:DD dan rose fitness shoot - <what was filmed>`, for example
   `11:13 dan rose fitness shoot - green screen`. The date prefix is required: the nightly backup routine
   (`scripts/backup/nightly_footage.py`) finds new shoots by it. Use the shoot day Dan names, not the camera
   clock (the FX30 clock was about 12 hours off on 9/23 and 11/13). A second card from the same day goes into
   the same folder. Never rename a shoot folder later: job docs hold exact paths.
4. Strays: a clip filmed days before the shoot (11/13: a Nov 3 laptop call) is filed separately with
   `--stray-before YYYY-MM-DD` and goes on the Seagate only.

## 2. Make room on the Extreme

Need = card total + 8 GB per clip in flight. If the Extreme is short:
- First `python3 .claude/skills/_shared/jobarchive/jobarchive.py scan`, then `run`. It moves only finished
  edit folders idle 14 days and not in use, and deletes each original only after a SHA-256 re-read from the
  Seagate. This is Dan's standing rule (finished jobs move to the Seagate); no need to ask.
- If that is not enough, do not wait: copy with `--extreme-later` (Seagate first, every byte still checked)
  and bring clips onto the Extreme with `offload.py fill-extreme` as room opens. On 11/13 the Seagate wrote at
  about 90 MB/s while the card read at about 90 MB/s, so moving old folders first was the slow path.
- Never delete raw shoot footage from the Extreme (Extreme deletion is paused in the nightly offload rules),
  never move an edit folder that has activity in the last 14 days, a live review or an edit-cap slot.

## 3. Offload the card

`nohup python3 .claude/skills/process-footage/scripts/offload.py copy --shoot "<folder>" [--stray-before DATE] [--extreme-later] > log &`

- Each clip is read from the card once and written to the Extreme folder and
  `/Volumes/Expansion/Abs By AI Raw Footage/<folder>/` at the same time; both copies are re-read and must match
  the card's SHA-256. The manifest `.offload-manifest.json` sits in both folders. Re-running skips verified
  clips, so it is safe after an interruption and for the next card.
- **The card is never formatted or written to.** Tell Dan to keep each card unformatted until the Google
  Drive check (step 4) passes.
- **A card put back in the reader can lie.** On 2026-11-14 card 1 reported a 60 GB clip as 4 GB.
  `offload.py` refuses to recopy a clip whose size changed and keeps the verified drive copies; run
  `offload.py verify --shoot "<folder>"` to re-hash both drives if anything looks off.
- **The Seagate is never the only copy.** It silently corrupted copies on 2026-11-01 to 11-03.

## 4. Back up to Google Drive

```bash
~/bin/rclone copy "/Volumes/Extreme/<folder>" "gdrive_backup:Abs By AI Raw Footage/<folder>" --include "C*.MP4" --include "C*M01.XML" --exclude "._*"
~/bin/rclone check "/Volumes/Extreme/<folder>" "gdrive_backup:Abs By AI Raw Footage/<folder>" --one-way --include "C*.MP4" --include "C*M01.XML" --exclude "._*"
```
Adjust the include patterns for other cameras (GoPro `GX*.MP4`). The `._` files are Mac housekeeping on the
exFAT drives, not footage: always exclude them or the check reports false differences. The 8 PM nightly
routine also copies new shoots to the Seagate and Drive; doing it now means the card can be freed today.
Report "card can be reused" only after this check shows 0 differences for every clip.

## 5. Transcribe and map every roll

Run both in the background, at the same time:
- **Roll sidecars** (the editors' word-timed transcripts, mic pick, contact sheet):
  `ls "/Volumes/Extreme/<folder>"/C*.MP4 > manifest.txt` then
  `python3 .claude/skills/_shared/rolls/roll_sidecar.py build @manifest.txt`. Whisper waits for the render
  queue and can run slower than real time; let it finish overnight if needed.
- **Fast map** with Gemini on each roll's audio (minutes, about $0.01 to $0.05 per hour of footage):
  `python3 .claude/skills/process-footage/scripts/audio_map.py --shoot-dir "/Volumes/Extreme/<folder>" --out ~/process-footage/<MMDD>`.

Then export the shoot's script documents (filming scripts, ad scripts, any reaction or studio docs):
`python3 .claude/skills/process-footage/scripts/unfilmed_doc.py export --out ~/process-footage/<MMDD>/docs <DOCID> ...`

**Match each mapped segment to a script** by the code and title Dan announces ("this video is L01 ..."). When
sidecars exist, confirm with `python3 .claude/skills/process-footage/scripts/announcements.py "<Extreme folder>" "<Seagate folder>" --gaps map.json`:
every announcement must sit inside its row's range, and every gap must be crew chat, framing, setup or a
break. On 11/13 this corrected four start times and proved no take was missed.

**Before asking Dan about a clip, compare it with the script text.** On 11/13 "Here's why sardines beat
protein bars" looked like a new title but was the first line of script B05. Ask Dan only about footage that
matches no script. He offers to help: list each unsure clip with its time and first words.

Also record per roll: orientation (Sony portrait clips carry rotation -90; decode to vertical, add no
transpose), length, camera, colour profile, and any partial or aborted takes.

## 6. Put every filmed video on the Edit Queue

1. Categorize each video before anything else: **AD** or **CONTENT**, and long or short (AGENTS.md,
   "Categorize every video before editing it"). Sales videos (VSL, upsells) are ADs.
2. **Update existing rows first.** Search `Handoffs/video-editing/jobs.json` for blocked rows this shoot
   filmed (titles, "not filmed", "next shoot"): set them `ready` with the new rolls and update their job docs
   (`queue.py set <ID> ready --by Claude --note "..."`), instead of adding duplicates. A partial take stays
   `blocked` with `--needs` saying what is missing.
3. New rows: `python3 .claude/skills/process-footage/scripts/register_jobs.py next-ids`, write a spec (format in the script's help), run
   `register_jobs.py check spec.json`, then `apply spec.json`. Groups must be ones the page shows:
   VSL and upsells in `Website VSLs`; every ad (long or short) in `Short-form ads`; long-form content in
   `Organic long-form`; dedicated Shorts and reaction Shorts in `Dedicated shorts` with sub `Talking`
   (exercise demos: `Workout`). Titles are the recognizable video titles, written in full ("Great Again T L01:
   ...", never "GAT"). Each job doc names its exact rolls and minute ranges, the script source, orientation and
   deliverable (ads: one master now, vertical/square/1-minute versions later as List 3 jobs; long-form: Shorts
   later from List 2; dedicated Shorts: nothing derived).
4. Mirror to the page: `ArtifactData batch` on `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection
   `jobs`, one `set` per printed entry (existing docs need `if_version`), then `queue.py mark-synced <ids>`.
   Confirm with `~/bin/rclone cat "gdrive_backup:Abs By AI automation/edit-queue-status.json"` that every new
   id is present with the right group and state. Do not republish the page itself unless a needed group is
   missing; if a publish is refused as "not the latest version", never force it, use a group the page shows.

## 7. Write the shoot footage report

`Docs/SHOOT_<MMDD>_FOOTAGE_REPORT.md` (model: `Docs/SHOOT_1113_FOOTAGE_REPORT.md`): where the files are on
each drive, format and camera facts, the camera clock offset, a roll map table (roll, orientation, length,
content with minute ranges), a by-video list split into ads and content, partial or missing takes, and a
dated double-check section (sizes on both drives, Drive check result, transcript cross-check, unfilmed
scripts). Add each later card as its own dated section.

## 8. Rebuild the Unfilmed Content And Ads Doc

Dan, 2026-11-14: one Doc with everything not filmed from this shoot and the shoot before, ads and content, so
the next shoot films those before any new ideas (memory `shoot-unfilmed-first`).
1. Gather every planned script from this shoot's and the previous shoot's documents, plus anything still
   carried in the previous unfilmed Doc and blocked "not filmed" queue rows. Subtract what was filmed (step 6).
   Leave out scripts Dan struck through; say so in a note. Mark partial takes ("only the opening line was
   filmed") and older versions superseded by a newer filmed script.
2. Write a spec and build: `python3 .claude/skills/process-footage/scripts/unfilmed_doc.py build spec.json --out unfilmed.html`. The summary
   at the top is generated from each item's `format` (ad-long, ad-short, long, short) and `label`.
3. Upload as a Google Doc: Drive `create_file` with `title` "Unfilmed Content And Ads (<shoot date>)",
   `contentMimeType` `text/html`, and the HTML as a file reference
   (`sha256:<hash>:<absolute path>`, the file must be on the Mac this session runs on). Then `share_file` with
   `permissionId` `anyoneWithLink`, role `reader` (Drive always public rule).
4. Read it back (`unfilmed_doc.py export` of the new id) and check the summary and part headings arrived.
5. Put the new link at the top of `Docs/NEXT_SHOOT_LIST.md` ("FILM THIS FIRST" line) and in memory
   `shoot-unfilmed-first`, replacing the old link.

## 9. Save and report

- `scripts/git/safe-push.sh -m "..." -- <job docs> Handoffs/video-editing/jobs.json Handoffs/video-editing/00-MASTER.md Docs/SHOOT_<MMDD>_FOOTAGE_REPORT.md Docs/NEXT_SHOOT_LIST.md`.
  Never commit `Media/footage-index/` (private; the repo is public). If safe-push stops on another session's
  live file, keep the local commit and retry before finishing.
- Also update `Docs/NEXT_SHOOT_LIST.md` rows and `Docs/PICKUPS_NEXT_STUDIO_SHOOT.txt` for pickups and B-roll
  that were filmed.
- Chat report: drives and Drive status, card(s) safe to reuse or not, the roll map in plain words, every queue
  entry by title grouped ads / long-form / Shorts, anything still running, then the two wrap-up boxes with
  the Edit Queue link and the Unfilmed Doc link.

## Not part of this skill

Editing (Dan fires jobs from the Edit Queue), covers and thumbnails, setup, uploads and scheduling (Codex
owns setup), and any deletion of raw footage.
