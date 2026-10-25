**LFC.** Task name: `Celebrity Ozempic LFC R4`. Starts only after Dan replies to the round 3 page (http://127.0.0.1:9126/).

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 4 handoff (written 2026-10-25, round 3 delivered)

Round 4 applies the green-screen background template (locked or revised per Dan's round 3 reply) to the WHOLE film, with all
six interview clips, the remaining before/after photo scenes and panels, then the complete film through every gate.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/_shared/greenscreen-bg/README.md` (the template and its rules), the round 3 recipe
`.claude/skills/longform-edit/reference/ro24/round3/README.md`, Dan's round 3 reply (record it verbatim in
`/Volumes/Expansion/_edit_work/RO-24/round4/DAN-DECISIONS.md` first), round 3 decisions `round3/DAN-DECISIONS.md`.

## State after round 3 (work dir `/Volumes/Expansion/_edit_work/RO-24/`)
- Never re-key: plates `round2/key/R*.mkv` (approved key). Colour warm, voice A, take list: locked.
- Timeline with the six clips inserted: `round3/edl_r3.json`, `film_words_r3.json`, `audio/film_voice_r3.wav` (8:38.4),
  `timemap.json` (old film frame -> new). Clip inserts `round3/clips/<name>_insert.mp4/.wav` (+ `inserts.json`). Full source
  videos for clean muted footage: `round3/clips/src/*_full.mp4` (Sharon, Fat Joe); download the other four whole the same way
  and pick clean windows from a 1 frame / 2 s contact sheet.
- Background plan: `round3/bg_plan.json` (planner output + `bg_overrides.json`, editor's calls BG04-BG09); facts
  `round3/recipe/facts_r3.py` (people, clips, pairs, numbers, transformations). Segments after 2:50.5 are planner defaults that
  still need the editor's pass: add `lower_thirds` to the facts (the planner skips big type under a lower third), check BG24
  (0.7 s) and the side-card spans, give each later person clean windows.
- Photo scenes P0-P3 rebuilt (`round3/hf/photos_r3.py`, stats in Dan's approved wording). P4-P7 still round 2 renders: rebuild
  as pairs with stats (pairs planned in facts_r3: Amy 2024/2026, Meghan 2020/2025, Oprah 2022/2025, Fat Joe 2005/2023 for his
  panel). New photos and credits: `round3/photos/photos_r3.json`.
- Graphics polish queued from round 2's re-check: G12 last row in on "keep losing" (about 3 s), G14 small top lines in
  CAPITALS; G14's button placement must be re-measured on the new end shot (its background changes).
- Open with Dan on the round 3 page: template lock, clip trims, Tracy clip placement, B-roll bench press A/B, AI clips A1-A8.
- Round 3 independent review: `round3/review/INDEPENDENT-R3.md` (first build: FIX FIRST, six items, all fixed) and the re-check
  `INDEPENDENT-R3-RECHECK.md`. Its notes still open for the whole film: lower thirds pass over his chest in the corner layout
  (kept: approved graphics), and the clips are used as broadcast (R5 grades the clip too: consider matching it).
- Codex note: the template is Python (`gsbg.py`, numpy/cv2/PIL) plus two HyperFrames templates; the film assembler is
  `round3/recipe/assemble_r3.py` (`--reuse/--redo` re-composes only changed background segments).

## Work
1. Apply Dan's round 3 notes to the template (shared module: change `greenscreen-bg`, re-run the preview stills).
2. Whole-film plan: facts for every section, planner, editor's overrides with a why each; HyperFrames panels and big types.
3. Rebuild P4-P7, G12, G14; place the four remaining clips (Amy, Meghan, Oprah, Tracy) per the page.
4. Any AI clips Dan picks: frames first (frame gate + frame-reviewer), motion on the Flow subscription after his yes.
5. Complete film: `round3/recipe/assemble_r3.py` (whole range), audio gate, hair report, graphics checks, watch pass, delivery
   gate, edit sheet, captions (.srt), fresh `ra-reviewer`, page, Videos to Review copy.

## Efficiency (Dan's rule)
No re-keying. Render through the queue (`renderq.py run --group RO-24`). Test on stills (`stills_r3.py`) and 10-15 s windows
(`--g0/--g1`), never a full render to test a look. The plate decode is the cost: about 3-4 frames a second on a busy Mac.

## Model
**Codex, newest stable Sol at high effort (currently `gpt-6.1-sol`).** Dan, 2026-10-25 (VIDEO-RULES "Reaction videos: the locked
format" and AGENTS.md "Green-screen editing"): "Codex now has the green screen jobs"; Codex handles new green-screen jobs and
their next authorized edit rounds. Round 3 finished on Claude because it was already running; round 4 transfers to Codex
through the sole-owner round workflow (`.claude/skills/_shared/video-rounds/README.md`). Resolve Sol against the client's
model catalog; never guess a future ID.

## Starter prompt
> Celebrity Ozempic LFC R4. Use Codex (newest Sol, high). Read `Handoffs/handoff-20261025-ro24-celebrity-ozempic-round4.md` and Dan's round 3 reply, then execute round 4 of "Reacting To Celebrity Ozempic Transformations" (RO-24) with `$long-form-content-edit` (Claude: /longform-edit): the whole film on the green-screen background template with all six interview clips and the before/after photos, every gate, independent review, deliver the round 4 page.
