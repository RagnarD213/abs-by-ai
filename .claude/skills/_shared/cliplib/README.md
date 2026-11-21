# Clip library (AI clips + B-roll)

One catalog of every reusable AI-generated clip and B-roll clip we own, so an editor (human or AI)
can pull an existing clip instead of generating a new one, buying stock, or scrubbing raw rolls.

| what | where |
|---|---|
| Files (full quality) | `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/` `04 AI-Generated Clips/<category>/` and `03 B-Roll - Real Footage/<dan-filmed, screen-recordings, stock>/` |
| Drive mirror (anyone with link) | folder `1Hby8O4mB4HZS341qvrVKHSHyCGBgP8mi`, same subfolders |
| Human catalog | Google Sheet "Clip Library - AI clips and B-roll (catalog)" in that Drive folder (id in `catalog.json` → `sheet_id`) |
| Source of truth | `Media/clip-library/catalog.json` (gitignored: the repo is public) |
| Offline previews | `Media/clip-library/thumbs/<ID>.jpg` (poster) and `contact/<ID>.jpg` (6 frames) |
| Filmed B-roll still to cut | `Media/clip-library/broll-cut-list.json` / `.md` |

**IDs.** `A0042` = AI clip, `B0031` = B-roll (real, screen recording or stock). The ID is permanent; quote it in
revision docs and EDLs. File name: `<ID>_<what-it-shows>_<shape>_<seconds>s.<ext>`, e.g.
`A0042_man-eating-salad-kitchen_9x16_5s.mp4`.

**AI categories:** ai-dan, people, food-nutrition, gym-and-exercise, lifestyle, concepts-and-gags, exercise-demos.

**Status:** `used-final` (in a finished video; `used_in` says which), `usable-unused`, or `unusable` for a registered
asset later excluded by quality checks. `find` excludes unusable records; `show ID` retains their source history.
Rejected takes are preserved in `07 AI Generation Source Archive`, outside the usable catalog. Files that sat loose in folders 03/04 before the 2026-09-29 sweep and were not catalogued (stick-figure gags,
the robot story montages whose shots are catalogued, a lower-quality toe-touch copy, old `.roll` sidecars) were moved
to `/Volumes/Extreme/_edit_work/_clip_library_set_aside/`. Old file names are kept in each clip's `legacy_name`.

## Preserve clean footage for editors

Keep full clean takes instead of arbitrary short approval trims. When a source has defects, retain every usable clean span as a separate library part, with original source timestamps/frame ranges and explicit excluded-fault notes. The final film editor chooses duration. Keep the original source and QC history; do not register faulty spans as usable or join separated parts into a fake continuous shot. Dan's November 15, 2026 rule in `../VIDEO-RULES.md` supersedes older 2–5 second window recipes.

## Every generated AI clip is filed before the job closes (Dan, 2026-11-16)

For business production footage, every newly generated video take from Flow, a paid API or any other model goes into the existing clip library system, including unused, rejected and unreviewed takes. Preserve each full original promptly in `07 AI Generation Source Archive`, with SHA-256, original path, job/shot/model, generation or collection time and its review disposition; merge its entry into `source-register.json` on the M2 master without replacing other jobs' entries. Use the M2 `clip_library.catalog_lock()` for the complete register read/merge/atomic-write transaction. Duplicate content points to the existing source rather than creating another copy. Keep rejected/unreviewed sources outside the usable catalog.

After the existing quality and approval steps, register every clean used or unused keeper with `clip_library.py add`, preserving full clean footage and separate clean spans, then refresh `clip_library.py sheet` and put usable IDs in the job docs. Approval gates and source restrictions still apply.

Library filing is a required completion check, not a later cleanup task. Reconcile every successful generation output in the job manifest against a source-archive entry and every cleared keeper against a permanent library ID. Verify local and Drive copies by file hashes, the source register and the current human catalog; record the output count, archive references, keeper IDs and verification receipt in the job's final report. Before pausing for review, archive all outputs already generated. A failed/missing collection or mirror stays explicitly incomplete with its exact output IDs and next action; do not claim the job fully filed or complete. No extra permission is needed for this filing. This supersedes older instructions to save only clips used in approved edits or to omit rejected takes entirely. See `.claude/skills/_shared/cliplib/README.md`.

## The rule for every video job

1. **Before generating an AI clip, searching stock, or hunting raw rolls: search the library.**
   `python3 .claude/skills/_shared/cliplib/clip_library.py find "<what the shot needs>" [--aspect 9x16] [--rolls]`
   Look at the `contact/<ID>.jpg` preview of the top hits. If one fits the beat, use it and cite its ID.
   `--rolls` also searches the raw shoot footage index (`_shared/rolls`).
2. **Avoid repeats.** A `used-final` clip is fine to reuse in a different video, but check `used_in` so the same
   audience does not see it twice in a row.
3. **Register every new clip that ends up in an approved video** (and any clean unused keeper) as the last step
   of the job:
   `python3 .claude/skills/_shared/cliplib/clip_library.py add FILE --kind ai|real|screen|stock --slug what-it-shows --description "one concrete sentence" --category <cat> --people dan|ai-dan|other-man|woman|mixed|none --status used-final --used-in "RO-05" [--model kling-v3 --prompt "..."]`
   then `clip_library.py sheet` to refresh the Google Sheet. `add` copies (never moves) the file into the library,
   makes previews and uploads it to Drive.
4. Preserve every source take, including rejected or defective takes (melting hands, fogging mirrors, breath smoke, warped faces), in `07 AI Generation Source Archive`. Never register a defective span as usable.

Other commands: `show A0042`, `verify`, `describe` (Gemini flash-lite re-describes clips from their contact sheets
and flags visible AI defects, about $0.0015 a clip), `drive-sync`, `thumbs`.

**Traps.**
- Frozen recipes written before 2026-09-29 (`shorts/reference/ds17-r4/`, `shortad-from-longform/reference/a8_ad4/`,
  `longform-edit/reference/spec_example_abwheel.py`, some old handoffs) name library files by their old flat path
  in `03`/`04`. Those files were renamed into category folders: `clip_library.py find "<old file name words>"`
  matches `legacy_name` and gives the new path.
- The Extreme drive is exFAT: `shutil.copy2` fails on it (chflags), so the tool copies with `copyfile`.
- The Sheets API is not enabled on rclone's Google project, so `sheet` builds an .xlsx and uploads it over the
  existing Google Sheet through the Drive API (the link never changes). Edits typed into the Sheet are overwritten.
- `_edit_work/_approved_clips/index.json` is a different, stricter machine registry used by the overnight edit
  queue (clip bound to a finalized video's SHA-256). Leave it alone; this library does not feed it.
- Folder `00 ASSETS USED IN THE REFERENCE AD` is a frozen set for the Ad 1 test brief; its clips are catalogued from
  their category copies, and folder 00 itself is left as is.
- Grades Dan approved for filmed B-roll (2026-10-01, clips B0427-B0479; recipe in `/Volumes/Extreme/_edit_work/broll-cuts-20260929/cut.py`):
  the welcome-video rolls (`C02xx-0xx.MP4`, 4K 23.976, untagged) are S-Log3, not S-Cinetone: use the 8/28 LUT built at
  exposure 0.70 plus `eq=saturation=0.88`, and keep 23.976. The 8/28 blue-mat rolls C1679-C1683 (warm low sun) take the
  1.30 LUT plus `colortemperature=temperature=8500:pl=1` or skin reads orange. Hard-sun rolls C1673-C1677 take 1.15-1.30,
  the patio rolls C1684-C1685 take 1.45. To re-grade a clip in place: overwrite the library file, `make_thumbs`,
  `drive_sync(cat, only={id})`, then `sheet`.

## Source ranges, favorites and teaching intent

`add FILE --metadata /private/path/clip.json` accepts exercise/aliases, equipment, angle,
`favorite` (boolean), `intended_use`, source `{file,path,in,out,duration,content_key,sha256}`,
`source_range_key`, grade, approval, candidate IDs, shoot and checks. These fields stay in
`catalog.json`; the human sheet also displays favorites, equipment, intent and original ranges.
Metadata cannot overwrite a permanent ID or a library path. `source_range_key` prevents a
second ID for the same original range. Mutating commands take one catalog lock and read fresh
state before allocating IDs. Python batch callers must use `with catalog_lock():` around their
load/allocate/save transaction too.
An owner-confirmed `approval.exercise` protects the search tags from automatic `describe` suggestions.
The model's separate `vision` proposal is retained without changing the confirmed exercise or its tags.

Both Codex and Claude use the same commands from the project root:

```bash
python3 .claude/skills/_shared/cliplib/clip_library.py find "cable crunch" --favorite
python3 .claude/skills/_shared/cliplib/clip_library.py find "rope" --intended-use "correct demonstration"
python3 .claude/skills/_shared/cliplib/clip_library.py find "rear delt" --equipment "machine" --exclude-mistakes
python3 .claude/skills/_shared/cliplib/clip_library.py show B0001
```

A correct-demonstration query excludes unknown, deliberate-mistake and beginner clips.
Do not silently convert unknown intent into correct form. `show` exposes the original source
path, exact in/out and identity needed to reconstruct a range. Keep Dan's confirmed exercise
names and source corrections; an automatic description never overrides them. Talking through
what will be filmed, resets and accidental camera handling are not reusable exercise B-roll.
Original recordings are always preserved, including excluded material.

The Drive connection can be selected without changing library folders or sharing:
`CLIPLIB_DRIVE_REMOTE=gdrive_backup: python3 .claude/skills/_shared/cliplib/clip_library.py sheet`.
The default is the existing dedicated-client `gdrive_backup:` connection;
the old shared Google client can return project-wide rate-limit errors. Confirm the existing
library root is accessible first. This selects an existing connection; it grants no new access.


October23 finished assets and Claude queue access: `Docs/OCTOBER23_SHARED_EDITOR_ACCESS.md`. Both editing workflows may use every usable catalogued take, not only the initial IDs suggested in a particular brief.

## Generated source archive (November 16, 2026 sweep)

`07 AI Generation Source Archive` in the existing library holds source/alternate exports and `source-register.json`, with hashes and original/duplicate locations. It includes rejected and unreviewed takes and is not a set of usable clips. Check `source-mirror-status.json` for its separate Drive-copy verification. Main catalogued clips retain their own approvals, quality scopes and permanent IDs. Sweep receipt: `Docs/AI_CLIP_LIBRARY_AUDIT_20261116.md`.
