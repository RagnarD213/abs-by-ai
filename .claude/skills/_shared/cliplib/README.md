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

**Status:** `used-final` (in a finished video; `used_in` says which) or `usable-unused`. Rejected takes are never
filed. Files that sat loose in folders 03/04 before the 2026-09-29 sweep and were not catalogued (stick-figure gags,
the robot story montages whose shots are catalogued, a lower-quality toe-touch copy, old `.roll` sidecars) were moved
to `/Volumes/Extreme/_edit_work/_clip_library_set_aside/`. Old file names are kept in each clip's `legacy_name`.

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
4. Rejected or defective takes (melting hands, fogging mirrors, breath smoke, warped faces) never go in.

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
