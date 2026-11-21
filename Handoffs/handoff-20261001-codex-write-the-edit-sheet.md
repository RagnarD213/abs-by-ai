# Codex: write the edit sheet at every 16:9 delivery

Written: 2026-10-01 by the Claude session that built the vertical kit's second way in.
Recommended task: Codex, GPT-6 Sol, medium effort.

## Why

Dan, 2026-10-01: "I plan to edit all videos with Claude and Codex going forward." The vertical kit now builds a 9:16
and a 59 s cutdown straight from the edit sheet of a 16:9 (`kit9x16/kit_run.py --sheet`), with no reverse-engineering
and with every graphic redrawn in Soft Blue Light from the 16:9's own HyperFrames configs. Claude's builds write the
sheet (`_shared/edit-sheet/sheet_from_claude_build.py`). Codex's builds do not record enough to write one, and their
file layout changes job to job, so no converter is possible.

## Read first

1. `.claude/skills/_shared/edit-sheet/README.md` (the format), `validate.py`, `CODEX.md` (what is missing, short)
2. `Docs/EDIT_SHEET_CODEX_MAPPING_20261001.md` (every field of RO-17 and RO-01 against the sheet, with file and key)
3. `.claude/skills/_shared/hyperframes/README.md` and `from_plan.py` (the graphic templates and their configs)
4. `.claude/skills/_shared/EDITOR-CARD.md` section D

## Work

1. In `$long-form-content-edit` (and the ad and shorts skills that produce a 16:9), add a delivery step that writes
   `<master name>.edit-sheet.json` in schema `abs-edit-sheet/1` and runs `validate.py SHEET --hash`. A failing sheet
   blocks the delivery gate stamp.
2. Make the render script read these as DATA files, one fixed layout for every job (names in `CODEX.md`): rolls,
   grade, cut with `src_f0` / `join` / `audio`, framing with a measured head per segment
   (`_shared/edit-sheet/headmeasure.py`), delivered words with a `fixes` list, graphics, pictures, audio, approvals
   with Dan's exact words under one key.
3. Build graphics from the HyperFrames templates through `from_plan.py`, so every graphic has a template name, a
   config and the words that drive it. Record any graphic from another renderer as `codex:<renderer>`; it will stop a
   vertical build until it has a template.
4. Record for every inserted clip or photo: `label_kind`, `label`, `label_source`, `people`, `physique`,
   `approved_crop`.
5. Prove it: write and validate the sheet for the next Codex 16:9 that reaches delivery. Do NOT retrofit or edit
   in-progress builds (RO-17 and RO-01 stay as they are).

## Done means

- The skill text carries the step; one real Codex 16:9 has a sheet that passes `validate.py --hash`
- `kit9x16/sheet_to_kit.py --sheet THAT_SHEET --build <scratch>` runs without a stop (it plans the vertical in
  seconds; no render needed for this check)
- This handoff's line removed from `AI_COORDINATION.md` and `Handoffs/README.md`

## Starter prompt

> Read `Handoffs/handoff-20261001-codex-write-the-edit-sheet.md` and the four files it lists, then execute it: make
> every Codex 16:9 delivery write and validate an edit sheet, with the render reading its facts from data files and
> graphics built from the HyperFrames templates. Prove it on the next 16:9 you deliver. Do not touch in-progress builds.

Model and effort: Codex GPT-6 Sol, medium.
