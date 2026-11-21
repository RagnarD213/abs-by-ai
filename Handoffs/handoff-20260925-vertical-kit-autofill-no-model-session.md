# Handoff: make the 9:16 vertical kit fill in its own content sheet, so a vertical needs no AI editing session

Written 2026-09-25 by Claude at Dan's request. **Executor: Claude Opus 5.5, High effort. Run it in Claude Code ON THE MAC
MINI** (it needs `/Volumes/Extreme`, the raw rolls, ffmpeg and Apple Vision). A cloud session cannot do this job.

## Why (the business reason)

Video editing is the biggest cost in Dan's Claude and Codex allowances (see
`handoff-20260918-claude-video-freeze-and-codex-routing.md`: 52% of a week gone in 22 hours). A vertical of a finished,
approved ad is a secondary job: every creative decision was already made by the editor and approved by Dan. It should not
need a long Opus or Codex session per video. Dan asked whether a local AI model on a new Mac Studio could take these jobs
over. The answer we reached (2026-09-25 chat) was: first turn the vertical job into a fixed script, so almost no AI is
needed at all, on the Mac mini he already owns.

The kit is already most of the way there. `.claude/skills/shortad-from-longform/reference/kit9x16/` (read its `README.md`
first) holds Muhammad's pacing, panel system, push schedule and cut rules as data. Dan judged its from-raw Ad 1 vertical
**a tie** with the approved hand-built one (2026-09-18, blind). It then built Ad 10's vertical (AV-07, gate PASS,
delivered 09-24). **The one step that still needs an AI session is writing `content.json`**: the sheet that says WHAT
graphic appears WHEN (beat kind, times, bullet text, which photo, real/AI label). Today a model writes it by hand by
watching the master. This job automates that sheet and wraps the whole build in one command.

## Dan's decisions (do not reopen)

- **The editors change nothing.** Do not ask Muhammad, Zeeshan or Waleed for textless masters, project files or graphics
  lists, and do not message them about this. Everything must be derived from what we already have: the editor's finished
  16:9 master, Dan's raw rolls, and our own asset libraries. (Dan does not want the editors to learn the verticals are
  AI-built.)
- **Goal:** a vertical job runs as one command on the Mac mini with **no Claude or Codex editing session**. AI is allowed
  only for a few small, narrow calls (see "Allowed AI calls"), each with a logged cost.
- **Anything the script is not sure about is escalated, never guessed.** An escalated job goes to the normal
  `/shortad-from-longform` path. A new graphic type is added to the kit once, then it is automatic forever.
- Standing rules still apply in full: `.claude/skills/_shared/VIDEO-RULES.md`, the kit README's "Rules carried", the
  delivery gate. Never move a gate bound, never add a `known_gap`, never delete a `must_trigger`.
- No uploading or publishing. Deliverables go to Dan for review exactly like any vertical.

## The answer keys you test against (already on disk)

| ad | hand-written sheet (the answer key) | status |
|---|---|---|
| Ad 10 (AV-07) | `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/recipe-vertical/content.json` (copy in `Handoffs/video-editing/AV-07-ad10-kit/`) with its `assets.py`, `grade.py` | gate PASS, delivered 09-24, awaiting Dan's verdict |
| Ad 1 (AV-01 parent) | `/Volumes/Extreme/_edit_work/kit9x16/ad1-master/content.json` (lifted from the approved `beats.py`) | Dan-approved vertical; kit from-raw build judged a tie |

Ad 10's sheet shows the full shape: `beats` (kinds `bleed`, `card`, `window` with `header` + `bullets`, `title` with
`headline` + `sub`, plus `stmt`, `winmedia`), each with `t0`/`t1`, `media` (a key into `assets.py`), `label_kind`
(`real`/`ai`) and `caps`; then `lower_thirds` (times + lines), `ctas` (times), `cta_top`/`cta_big`, `no_caps_kinds`,
`deviations`.

## What to build

A new script, `kit9x16/auto_content.py`, that writes `content.json` plus an `auto_content_report.json` with a confidence
level and the evidence for every entry. It runs after the edit recovery (Step 1 of the skill: `edl_final.json`,
`grade.py`, word timings) and needs no model for the normal case.

1. **Find where the graphics are (measurement).** For every master frame, render the matching raw frame through the
   recovered EDL and `grade.py` (BT.709 decode, memory `untagged-video-bt601-trap`) and compare it with the master.
   Where the master differs from Dan's graded raw picture beyond a calibrated threshold, the editor added something
   (graphic, photo, B-roll, lower third, CTA pill). Group those frames into spans, snap `t0`/`t1` to the frame grid
   and to phrase anchors in the word timings. Calibrate the threshold on Ad 1 and Ad 10, never by eye.
2. **Name each span's kind (measurement first).** The panel tokens are already measured in
   `kit9x16/panels/measurements.json` (olive card and hole, grid pitch, lower-third geometry and opacity, CTA pill).
   Match each span against them: a card hole means `card`, text on the field next to a window means `window`, and so on,
   using the plate types the renderer already has (`vlib`/`render.py`: `plate_card`, `plate_statement`,
   `plate_stmt_window`, `plate_title`, `plate_title_card`, `plate_window`, `plate_window_media`). Anything that matches
   no known kind is `unknown` and escalates.
3. **Read the words (free, on the Mac).** Apple Vision text recognition (`VNRecognizeTextRequest` through pyobjc) on
   the clearest frame of each text span: bullets, headers, headlines, lower-third lines, CTA text. Keep the editor's exact
   wording. Cross-check each line against the transcript (graphics usually paraphrase the spoken line). A low-confidence
   read or a mismatch goes to the report as an escalation, not a guess.
4. **Find the clean source for each picture (measurement).** For every `card` and `bleed`, match the picture inside the
   master against our libraries (the ad's own asset folder, earlier `assets.py` files, `photos/finalized social media
   photos/`, `Media/`) with perceptual hashing plus feature matching, so the kit uses the clean original instead of
   the master's labelled frame (Ad 10's `deviations` explain why). Write the `assets.py` entry. `label_kind` comes from
   the matched file's known provenance (real photo vs AI-generated folder or name). No match: a 16:9 motion insert is
   taken from the master itself into the olive card (skill Step 5 rule 3); a still picture of Dan's physique with no
   provenance escalates, because every physique picture needs exactly one correct label.
5. **Lower thirds, CTAs, captions.** Times and lines from steps 1 to 3; `caps` and `no_caps_kinds` follow the rule
   already in the kit (captions off under text-heavy plates).

Then add `kit9x16/kit_run.py`: one command that runs the whole chain in the README's "Build order (from a master)" with
`auto_content.py` in place of the hand-written sheet, stops at the first failure, and writes a single `run_report.json`
(stages, wall-clock, every AI call with its cost, every escalation). The judged watch pass stays mandatory; see below.

## Allowed AI calls (small, narrow, logged)

- **Leftover classification only:** when step 2 or 4 is unsure, one image call that picks from the fixed menu of kinds
  or answers "is this picture real or AI". Make the provider pluggable (Gemini first, because its quality-review spend is
  standing-authorized under $5 per run; a local Ollama or LM Studio model later).
- **The judged watch pass:** today three fresh sessions judge the render (`watch/JUDGE_PROMPT.md`, merged by
  `kit_fold.sh`). Build a Gemini judge that writes findings in the exact same file format, so `kit_fold.sh` and the gate
  take it unchanged. Its findings must be at least as strict as the session judges'; check that on Ad 10 (see Proof 2).
- **The ≤0:59 cutdown:** picking which sentences make the hook, problem, AI demo, payoff and CTA is real editorial
  judgment. Keep it to one text-only call over the transcript that returns sentence ranges; everything after that
  (`plan_cutdown.py` / `vcutdown` in AV-07's recipe) stays scripted.

Total AI spend per vertical target: **under $1**, logged in `run_report.json`. Stay inside the $25 session cap.

## Proof (all three, in order)

1. **Answer-key test.** Run `auto_content.py` on Ad 10 and Ad 1. Compare with the hand-written sheets and report a table:
   beats found vs expected, kinds correct, `t0`/`t1` error (target within 0.2 s), exact text match rate, correct media
   file, correct `label_kind`, escalations. Commit the comparison script so it becomes a regression test. Any label error
   (real vs AI) is a hard failure.
2. **Rebuild test.** Build Ad 10's full vertical end to end with `kit_run.py` from the auto sheet. It must pass the gate
   (`gate.py --format ad9x16`, 0 open defects) and match the delivered AV-07 vertical closely: report per-beat frame
   differences and explain every difference. Run the Gemini judge and the existing session-judge findings side by side
   on the same file and report which defects each caught.
3. **Fresh-ad test: AV-09, Ad 8 "Two Futures"** (finalized 09-16, no vertical exists, job doc
   `Handoffs/video-editing/AV-09-ad8-vertical.md`, claim it with `python3 scripts/edit-queue/queue.py set AV-09 in_progress
   --by Claude`). Run `kit_run.py` with no hand edits to the sheet. If it escalates, fix the kit (not the build folder),
   then rerun. Deliver the full vertical and ≤0:59 exactly as the job doc says, for Dan's review.

## Done means

- `auto_content.py`, `kit_run.py`, the pluggable AI-call module and the answer-key regression test committed in the
  skill's `reference/kit9x16/`, with the kit README updated: the new build order, the escalation rules, a plain-language
  "for Dan" paragraph.
- Proof 1 table, Proof 2 gate result and judge comparison, Proof 3 delivery, and the run report's wall-clock and AI cost
  per vertical, reported to Dan in plain language, including an honest estimate of what share of future verticals will
  run with zero escalations.
- `scripts/edit-queue/config.json` NOT switched over yet. Propose the routing change (AV/AS jobs run `kit_run.py` first,
  fall back to a model session only on escalation) and let Dan decide.
- This handoff's line removed from `AI_COORDINATION.md` HANDOFFS and its row removed from `Handoffs/README.md`.
  Commit, push, confirm.

## Traps

- Read the kit README's "Measured traps" before touching labels: the person mask absorbs a chip already drawn on a frame,
  and a chip over a bright picture grades differently. Measure clearance on the master's own pixels.
- Frame-count differences between two cuts of the same film are measured (`a13_av01_ad1_vert59/align_frames.py`), never
  assumed.
- Defects inherited from the editor's master are still defects to the gate; report them in the master-vs-ours table
  ([A13] item 4 in the skill), do not hide them.
- Do not touch the Ad 6 vertical (AV-05); another session owns it.
- No em dash in anything you write (AGENTS.md rule).
