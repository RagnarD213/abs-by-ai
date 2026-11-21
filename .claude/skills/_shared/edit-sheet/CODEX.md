# Codex builds and the edit sheet (inspected 2026-10-01)

Two real Codex 16:9 builds were read file by file: RO-17 (`/Volumes/Extreme/_edit_work/RO-17/`, the newer queue-run
layout) and RO-01 (`/Volumes/Extreme/_edit_work/ro01/`, R3 master), with DS-17 R4 for a layout comparison. The full
field-by-field table is `Docs/EDIT_SHEET_CODEX_MAPPING_20261001.md`.

**Verdict: no converter. Codex writes the sheet itself at delivery.** The three builds share no file names or key
names for the same facts (the cut is `recipe/timeline.json pieces[]` in RO-17, `edit.json` as a list in RO-01,
`edit.json pieces[]` with other keys in DS-17), so a converter would be a new adapter per job. And the newer layout
records LESS than the older one.

## What Codex's builds do not record today

| Sheet field | RO-17 (newest layout) | RO-01 (older, hand-run) |
|---|---|---|
| `framing[].head` (hair top, centre, chin in raw pixels) | MISSING. Crops are preset names handed out by `i % 3`; the pixel boxes are only in the Python script | recorded (`analysis/source-framing.json`, 2 fps) |
| `graphics[].template`, `config`, `text` | MISSING as data: the text lives in Python lambdas in `recipe/build_ro17.py`. The delivered opening title was also patched after the render, so the recipe no longer matches the master | recorded (`graphics.json`), one hand-patched exception |
| `graphics[].driven_by` (which spoken word lands each part) | MISSING: times are whole seconds picked by hand | MISSING |
| graphics a vertical can redraw | NO: `orglib` panels, not the HyperFrames templates | NO: `modern_graphics` panels |
| `pictures[].label_kind`, `label`, `label_source` | MISSING (`type: "stock"` only) | prose only |
| `pictures[].people`, `physique` | MISSING | prose only |
| `pictures[].approved_crop` | MISSING | MISSING |
| `grade` | a string inside the script | recorded (`grade.json`) |
| `edl[].src_f0` (the real first raw frame), `join`, `audio` | derivable to within a frame; not stored | derivable; not stored |
| `words.fixes` | none recorded | regexes inside `build.py` |
| `approvals` in one place with Dan's exact words | empty slot | spread over four files under four key names |

Recorded well in both: the master and its hash, the cut's source and output times, word timings on the delivered
timeline, the untreated audio and the audio gate sidecars.

## The instruction (also in `_shared/EDITOR-CARD.md` and `Handoffs/handoff-20261001-codex-write-the-edit-sheet.md`)

1. At delivery of every 16:9, write `<master name>.edit-sheet.json` beside the master in schema `abs-edit-sheet/1`
   (`README.md` here) and run `python3 .claude/skills/_shared/edit-sheet/validate.py SHEET.json --hash`. A failing
   sheet blocks the delivery gate stamp. Never hand-edit a sheet to make it pass: fix the build's data.
2. The render script READS its facts from data files, so the file and the picture cannot disagree: rolls, grade,
   cut (with `src_f0`, `join`, `audio`), framing with a MEASURED head on every segment (`edit-sheet/headmeasure.py`
   does it from the raw roll), delivered words with a `fixes` list, graphics, pictures, audio, approvals.
3. Graphics are built from the HyperFrames templates (`_shared/hyperframes/from_plan.py`), so each graphic has a
   template name and a config with film-time word starts, and its parts land on Dan's words. A graphic drawn by any
   other renderer goes in the sheet as `codex:<renderer>` and STOPS a vertical build, because it cannot be redrawn
   at 9:16.
4. Every inserted clip or photo records `label_kind` (`ai`, `real`, `none`), the chip text, `label_source`,
   `people` (`dan`, `other`, `none`), `physique` and `approved_crop`. These are facts the editor knows when it places
   the picture; nothing downstream may guess them.
5. No fix after the render without updating the data and the master hash (RO-17's opening-title splice is the
   example of what not to do).
