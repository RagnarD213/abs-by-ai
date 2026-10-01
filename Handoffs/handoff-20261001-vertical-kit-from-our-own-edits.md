# Vertical kit, second way in: build the 9:16 from OUR OWN 16:9 edit sheet, in Soft Blue Light

Written: 2026-10-01 by the session that built the kit autofill (memory `vertical-kit-autofill`).

Recommended fresh task: Claude Opus 5.5, high effort. This is pipeline work with a design port inside locked
standards. Expect it to need a handoff of its own partway (see "Stop points").

## Why (Dan, 2026-10-01)

1. "I plan to edit all videos with Claude and Codex going forward."
2. "I don't want to see anything else with these old graphics... everything going forward to be made with soft blue
   lights and hyperframes in the review process in the first round." (memory `old-graphics-retired-soft-blue-hyperframes`)

The kit (`.claude/skills/shortad-from-longform/reference/kit9x16/`) was built for a human editor's master: its first
half reverse-engineers a finished video (which takes, which graphics, which pictures, real or AI). When Claude or
Codex made the 16:9, that answer sheet already exists, so the reverse-engineering is wasted time (over an hour of a
2 h 15 min build) and the main source of stops. And the kit draws Muhammad's old olive graphics, which Dan has retired.

## Goal (three parts, one task)

1. **A second way in.** `kit_run.py` accepts a 16:9 build's own edit sheet and skips `recover`, `measure` and
   `content`. The existing way in (an editor's master) keeps working for Muhammad's remaining masters and any human
   editor.
2. **One sheet format both editors write.** Define it, make Claude's 16:9 builds write it, and write the Codex-side
   instruction so Codex's builds write it too.
3. **Graphics drawn fresh in Soft Blue Light with HyperFrames**, at 9:16, from the same templates the 16:9 used. No
   more cropping a 16:9 graphic into a card.

Not in this task: firing the vertical automatically when Dan approves a 16:9 (Dan was told that waits until this
works on one or two real videos), and the square (1:1) format.

## Read first

1. `AGENTS.md`, `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md`
2. `.claude/skills/shortad-from-longform/reference/kit9x16/README.md` in full (build order, what escalates, the four
   lesson sections) and `answer_keys/PROOF1.md`, `PROOF2.md`
3. `.claude/skills/_shared/SOFTBLUE.md`, `GRAPHICS-STANDARDS.md`, `hyperframes/README.md`
4. Memory: `vertical-kit-autofill`, `old-graphics-retired-soft-blue-hyperframes`, `hyperframes-decision`,
   `review-page-what-i-decided`, `graphic-lock-and-ai-frames-first`, `decision-budget-per-video`,
   `codex-stepwise-editing-approach`, `framing-standard-hair-anchored`

## What exists today (verified 2026-10-01; read it yourself before relying on it)

**The kit's own sheet** (`content.json` + `assets.py`, written by `auto_content.py`): beats (`kind`: bleed, card,
window, stmt, title, winmedia; `t0`, `t1`, `media`, `label_kind`, `caps`, `label_spans`, `flash_after`), lower thirds
(`lines`, `equal`), CTAs, and a media map. `build_kit.py` turns it plus an EDL (`edl_final.json`: `cut_in`, `cut_out`,
`src_in`, `src_out`, `roll`) and word timings into `beats.json`. Everything after that (base, track, labels, words,
picture, captions, mux, the gate pre-check, the clearance loop, judges, fold, cutdown, deliver) reads `beats.json`
and does not care where the sheet came from.

**A Claude 16:9 build** (example `/Volumes/Extreme/_edit_work/ro10/`, the first all-template film): `edl.json`
(pieces: `word_in`, `word_out`, `in`, `out`, `text`), `plan_resolved.json` (42 items: `kind`, `start`, `end`, `src`,
`label`, `t0`, `t1`), `shots.json` (per shot: source frames, `reframe`, `framing`, output frames), `words.json`,
`hf/` (`beats.json`, `configs/`, `manifest.json`, `renders/` = the HyperFrames graphics), and `recipe/`.

**A Codex 16:9 build** (example `/Volumes/Extreme/_edit_work/RO-17/`): `WORK_PACKET.json`, `SCENE_PLAN.md`,
`PRE_RENDER_CHECK.json`, `graphics/`, `assets/`, `DRAFT-DELIVERY.json`. NOT inspected in detail. Reading it and
mapping it is step 2.

**HyperFrames templates:** `cycle/` is on main. `lower-third/`, `before-card/`, `side-list/`, `from_plan.py`,
`hfbuild.py`, `checks.py`, `composite.py` exist ONLY in the main checkout's working copy
(`/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/`), which is stuck and
cannot push (board: "Shared checkout cannot push", `Handoffs/handoff-20260930-fix-stuck-main-checkout.md`).

## Work

### Step 0: where to work

Work in a git worktree off `origin/main` under `~/abs-worktrees/` (never `/private/tmp`: a restart wiped the last
one mid-build). Link `Media/video_edit/bin`, `shorts/reference/recentre/personmask` and `_shared/qc_corpus/excerpts`
from the main checkout (memory `qc-corpus-worktree-trap`). The HyperFrames templates you need are not on main yet:
if the stuck-checkout handoff has not been run, copy that `hyperframes/` folder into your worktree read-only as a
starting point and say so in your report; do not commit another session's unpushed files as your own.

### Step 1: define the sheet (`_shared/edit-sheet/`)

One JSON file every finished 16:9 writes next to its master, plus a short README and a validator
(`validate.py SHEET` exits non-zero and names the missing field). Start from the kit's `content.json` and add what a
reverse-engineered sheet never had. At minimum:

- `video`: master path, sha256, fps, frames, duration; raw rolls with paths
- `edl`: every picture segment (roll, source in and out, output in and out) and the audio it rides with
- `framing`: per shot, the crop the 16:9 used and the measured head position (the vertical re-frames from the RAW
  roll, hair-anchored, so it needs the source window, not the 16:9 pixels)
- `words`: word timings on the delivered timeline (CTC), and the caption fix list applied
- `graphics`: one entry per graphic with template name, template config (the HyperFrames config, so it can be
  re-rendered at another shape), exact text, in and out, and which words drive it
- `pictures`: every photo or clip with source file, in and out, real or AI (`label_kind`), who is in it, and
  whether Dan approved a crop for it
- `audio`: the delivered mix and the untreated reference (the audio gate needs both)
- `approvals`: which round Dan approved, and the decisions he made (so the vertical does not re-ask them)

A missing field is caught when the 16:9 is delivered, not when the vertical is built: wire the validator into the
16:9 delivery step of `/longform-edit` and `/ad-edit` (a failing sheet blocks the delivery gate stamp).

### Step 2: both editors write it

- **Claude side:** a converter `sheet_from_claude_build.py BUILD_DIR` that writes the sheet from `edl.json`,
  `plan_resolved.json`, `shots.json`, `words.json` and `hf/`. Prove it on `/Volumes/Extreme/_edit_work/ro10/` and one
  ad build. Then make the skills call it at delivery.
- **Codex side:** open two real Codex builds (RO-17 and one RA or DS build), map their files to the sheet, and
  write (a) `sheet_from_codex_build.py` if their files already hold everything, or (b) the exact instruction Codex
  must follow to save the missing fields, as a Codex handoff (GPT-6 Sol, medium) plus the lines to add to
  `_shared/EDITOR-CARD.md`. Do not edit Codex's in-progress builds. Report plainly which fields Codex does not
  record today.

### Step 3: the second way in

`kit_run.py --sheet SHEET.json --build B --name "..."`: writes `content.json`, `assets.py`, `edl_final.json`,
`grade.py`, `m.whisper.json` / `ref.whisper.json` from the sheet and starts at `setup`. Labels come from the sheet's
`label_kind` (never from a library match, never from a model). Keep: the label clearance loop, the gate pre-check,
caption rules, the cutdown picker and its seam checks, `carry_verdicts.py`. The answer-key regression
(`test_answer_keys.py`) must still pass, so the editor-master path is untouched.

### Step 4: Soft Blue Light graphics at 9:16

Replace the kit's drawing layer (`vlib.py` plates, lower thirds, CTA pill, flash; `render.py` calls them) with
HyperFrames renders in the Soft Blue Light style:

- A 9:16 layout per template family (lower third, before / fact card, side list, cycle, title or statement card, CTA
  button, label chip). Phone-sized type; nothing over his face or abs; the hair-anchored framing rule holds.
- The same config that drew a graphic at 16:9 draws it at 9:16 (step 1's `graphics[].config`), so text and timing
  are never retyped.
- Transitions: no whoosh or swipe sound, ever (memory `no-swipe-sound-effect`). Decide with the standard whether the
  white flash survives; do not carry Muhammad's flash by default.
- **Graphic lock first.** Before any full build, put the 9:16 version of every template on ONE review page in the
  required format (memory `review-page-what-i-decided`: first minute, the frames, "What I decided", all items three
  per row) and get Dan's approval of the look. Stay inside his decision budget (10 to 15 decisions per video).
- The delivery gate's measured ranges (`_shared/reference/picture.json`: flashes, pushes, lower thirds per minute)
  were measured on Muhammad's cuts. If a Soft Blue Light vertical cannot meet a range because the style is different,
  do NOT move the bound: stop and put the question to Dan with the numbers.

### Step 5: prove it on one real video

Pick with Dan, default the newest Dan-approved Claude 16:9 that used HyperFrames graphics (RO-10 if approved by
then). Build its 9:16 and 59s from the sheet with no hand edit of the sheet, through the gate pre-check, three fresh
judges, fold, cutdown, deliver. Any judge or gate finding is fixed in the kit, then rerun. Send Dan the review copies
in a first-round review page that already shows the Soft Blue Light graphics.

## Done means

- `_shared/edit-sheet/` (format README, validator) committed; `sheet_from_claude_build.py` proven on two builds; the
  Codex mapping written as a converter or a Codex handoff, with the missing fields listed
- `kit_run.py --sheet` builds a vertical without `recover`, `measure` or `content`; the answer-key test still passes
- 9:16 Soft Blue Light templates approved by Dan on one review page, then used for one full vertical + 59s that
  passes `gate.py --format ad9x16` (or the format that applies) with 0 open defects
- `kit9x16/README.md` updated (new way in, new graphics, lessons); wall-clock and AI cost per vertical reported next
  to the editor-master numbers (133 to 143 min, about 15 cents)
- This handoff's line removed from `AI_COORDINATION.md` and its row from `Handoffs/README.md`; committed, pushed,
  deploy confirmed

## Stop points (suggest a handoff rather than pushing on)

1. After steps 1 to 3 (sheet, converters, second way in) are proven with the OLD graphics on one build: a clean
   place to stop if context is half used.
2. After Dan approves the 9:16 template page.

## Traps the last session paid for

- Run `gate.py` detached (`nohup ... &`, then read its JSON). In the foreground of an agent shell it can hang for
  hours. Never run two gates at once.
- The person detector reads a dark label chip as part of him on single compressed frames; only the delivered file
  shows it. Keep the clearance loop.
- Never put a seam, or end a graphic, inside a word, a flash or a fade. The cutdown picker's checks encode this.
- A judge's identity or "garbled caption" call gets checked against the library match and the audio before acting.
- At most two video builds at once across all sessions; check what else is rendering first.
- No change to any gate ships unless `_shared/qc_corpus/run.py` passes for the entries that exercise it (the full
  corpus is a many-hour run; run the ad entries, and say which you ran).
- Do not contact or ask the editors for anything. Do not upload or publish anything.

## Starter prompt

> Read `Handoffs/handoff-20261001-vertical-kit-from-our-own-edits.md` in full, then
> `.claude/skills/shortad-from-longform/reference/kit9x16/README.md`, `.claude/skills/_shared/SOFTBLUE.md` and
> `.claude/skills/_shared/hyperframes/README.md`, and execute the handoff. Goal: the vertical kit builds a 9:16 and a
> 59s cutdown straight from the edit sheet of a 16:9 that Claude or Codex made (no reverse-engineering), with every
> graphic drawn fresh in Soft Blue Light with HyperFrames. Define the one sheet format, make Claude's builds write it,
> tell me exactly what Codex's builds are missing, show me the 9:16 graphics on one review page before any full
> build, then prove it on one real video and send me the review copies. Explain the results in plain language.

Model and effort: Claude Opus 5.5, high.
