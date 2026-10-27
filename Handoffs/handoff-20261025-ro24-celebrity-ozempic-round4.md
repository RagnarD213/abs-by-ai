**LFC.** Task name: `Celebrity Ozempic LFC R4`. Ready to fire: Dan replied to the round 3 page on 2026-10-27.

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 4 handoff (written 2026-10-25, updated 2026-10-27 with Dan's reply)

Round 4 puts the WHOLE film on the locked green-screen background template, with all six interview clips and the rest of the
before/after photo scenes and panels, makes the six AI clip frame pairs Dan asked for, then runs the complete film through
every gate and delivers the round 4 page.

## Dan's round 3 reply (verbatim, with the read-as table): `/Volumes/Expansion/_edit_work/RO-24/round4/DAN-DECISIONS.md`
- **Template LOCKED as the permanent standard** for long-form green-screen videos (README status, VIDEO-RULES, AGENTS.md).
  Apply it unchanged. No style changes this round.
- **First 2:50 approved as delivered** (round 3 export sha256 70b4e83a...). Reuse its rendered frames
  (`assemble_r3.py --reuse`); re-compose only where an approved AI clip lands.
- **Interview clips approved** ("Interclips" in his dictation): keep all six trims, levels and source chips.
- **Tracy Morgan clip: editor's call.** Keep it right before "And Tracy Morgan said it on The Tonight Show" (new film about
  6:34). He did not know what it referred to, so the page shows it in context with its timestamp and a short watch range.
- **"B-roll at 5:33": he could not find it** because it sits after the 2:50 preview. It is B2, the AI-Dan bench press
  (library A0111 0.5-3.6 s, AI-GENERATED label) over "I'm lifting significantly more weight now", new film about 5:33. Keep
  it; on the page, name it in plain words with its timestamp and watch range.
- **AI clips: start and end frames for A1, A3, A4, A6, A7, A8** (A2 and A5 dropped). Ideas: `round2/ai_ideas.json`.

| id | line (new film time, from `round3/timemap.json`) | idea |
|---|---|---|
| A1 | opener, first 5 s (0:00) | two men take the same shot; one shredded and grinning, the other gaunt and grey at his reflection |
| A3 | "Stories like this are used to scare people" (about 2:13) | man at breakfast reads the paper, eyes go wide, lowers it, spooked |
| A4 | "he stays away from the bread, the pasta and the rice" (about 3:01) | waiter sets bread and pasta before a big man, who slides both away and points at a steak |
| A6 | "I out-ate Ozempic" (about 6:50) | man at a buffet stacks his plate into a wobbling tower, reaches for one more roll |
| A7 | "Don't go from 5 mg to zero. Step down gradually" (about 7:44) | one man walks calmly down a staircase step by step; beside him another leaps off the top and lands in a heap |
| A8 | "keep weighing yourself daily" (about 7:50) | man steps on a bathroom scale in the morning, glances down, nods, steps off |

A1 is an alternative cold open: show it as an option over the approved opening; the approved opening stays until he picks it.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (incl. "Long-form green-screen backgrounds: the
locked template"), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/greenscreen-bg/README.md`, the round
3 recipe `.claude/skills/longform-edit/reference/ro24/round3/README.md`, `round3/DAN-DECISIONS.md`, `round4/DAN-DECISIONS.md`.
AI clips: `.claude/skills/ai-clip-ideas/SKILL.md`, `_shared/IMAGE-GENERATION.md`, `_shared/framecheck/`, `_shared/veo/FLOW-RUNBOOK.md`.

## State after round 3 (work dir `/Volumes/Expansion/_edit_work/RO-24/`)
- Never re-key: plates `round2/key/R*.mkv` (approved key). Colour warm, voice A, take list: locked.
- Timeline with the six clips inserted: `round3/edl_r3.json`, `film_words_r3.json`, `audio/film_voice_r3.wav` (8:38.4),
  `timemap.json` (old film frame -> new). Clip inserts `round3/clips/<name>_insert.mp4/.wav` (+ `inserts.json`). Full source
  videos for clean muted footage: `round3/clips/src/*_full.mp4` (Sharon, Fat Joe); download the other four whole the same way
  and pick clean windows by scene detection (README trap: never from an `fps` contact sheet).
- Background plan: `round3/bg_plan.json` (planner output + `bg_overrides.json`, editor's calls BG01-BG10); facts
  `round3/recipe/facts_r3.py`. Segments after 2:50.5 are planner defaults that still need the editor's pass: add
  `lower_thirds` to the facts (the planner skips big type under a lower third), check BG24 (0.7 s) and the side-card spans,
  give each later person clean, steady windows (no quote boxes, chyrons or flashing cameras behind him; logo bug kept out of
  the corner).
- Photo scenes P0-P3 rebuilt (`round3/hf/photos_r3.py`, stats in Dan's approved wording). P4-P7 are still round 2 renders:
  rebuild as pairs with stats (Amy 2024/2026, Meghan 2020/2025, Oprah 2022/2025, Fat Joe 2005/2023 for his panel). Photos and
  credits: `round3/photos/photos_r3.json`.
- Graphics polish queued from round 2's re-check: G12 last row in on "keep losing" (about 3 s), G14 small top lines in
  CAPITALS; G14's button placement re-measured on the new end shot (its background changes).
- Round 3 reviews: `round3/review/INDEPENDENT-R3*.md` (last: READY FOR DAN). Open notes for the whole film: lower thirds pass
  over his chest in the corner layout (kept: approved graphics); clips used as broadcast; Fat Joe fade-out about 60 ms
  (optional 100 ms).
- Codex note: the template is Python (`gsbg.py`, numpy/cv2/PIL) plus two HyperFrames templates; the film assembler is
  `round3/recipe/assemble_r3.py` (`--reuse/--redo` re-composes only changed background segments).

## Work
1. `editcap.py acquire RO-24` before the first render or generation.
2. **AI frames first, in parallel with the film.** Six start/end pairs through `.claude/skills/_shared/codex-image.sh`
   (Codex subscription, never a paid API). Calm, real-looking people, natural light, no slop (memory
   `ai-clips-natural-or-regenerate`, `ai-clip-sense-qc`: the picture shows the line, cause and effect reads). Each pair:
   `_shared/framecheck/gate.py --verify`, then a fresh independent frame review per pair (Claude: `frame-reviewer` agent).
   Put the passing pairs on an early frames page and tell Dan, then keep building the film. After his yes: motion in Google
   Flow on his subscription (never the paid API unless he says rush), AI-GENERATED label, insert into the film if the film is
   not yet delivered, else next round.
3. Whole-film plan: facts for every section after 2:50, planner, the editor's overrides with a why each; HyperFrames panels
   and big types (`hfbg.py --snap` first, then `--render`); one still per segment through the assembler before any long render.
4. Rebuild P4-P7, G12, G14; place Amy, Meghan, Oprah and Tracy in context.
5. Complete film through the queue (`renderq.py run --group RO-24`), reusing the approved 0-2:50 frames. Then audio gate,
   hair report (>= 20 px), graphics checks, watch pass, delivery gate, edit sheet, captions (.srt), fresh independent
   reviewer, page, Videos to Review copy, `editcap.py release RO-24 --review`.
6. Page (later-round rule): a short revision list with exact timestamps and watch ranges, at least: the rest of the film on the
   template (first new segment at 2:50.5), Tracy clip at about 6:34, the bench press at about 5:33, P4-P7, G12, G14, and the
   six AI frame pairs (or motion takes) each at its line. Videos named by title.

## Efficiency (Dan's rule)
No re-keying. Render through the queue. Test on stills (`stills_r3.py`) and 10-15 s windows (`--g0/--g1`), never a full
render to test a look. The plate decode is the cost: about 3-4 frames a second on a busy Mac.

## Model
**Codex, newest stable Sol at high effort (currently `gpt-6.1-sol`).** Dan, 2026-10-25 (VIDEO-RULES "Reaction videos: the locked
format" and AGENTS.md "Green-screen editing"): "Codex now has the green screen jobs"; Codex handles green-screen jobs and their
next authorized edit rounds. Round 3 finished on Claude because it was already running. Resolve Sol against the client's
model catalog; never guess a future ID. The Claude R3 task stays pinned until this task is verified running (Claude cannot
start or read a Codex task); the R4 editor records the transfer in the round journal (`_shared/video-rounds/README.md`).

## Starter prompt
> Celebrity Ozempic LFC R4. Use Codex (newest Sol, high). Read `Handoffs/handoff-20261025-ro24-celebrity-ozempic-round4.md` and `/Volumes/Expansion/_edit_work/RO-24/round4/DAN-DECISIONS.md`, then execute round 4 of "Reacting To Celebrity Ozempic Transformations" (RO-24) with `$long-form-content-edit` (Claude: /longform-edit): the whole film on the locked green-screen background template, all six interview clips and the before/after photos; start and end frames for AI clips A1, A3, A4, A6, A7 and A8 through the frame gate and an independent frame review, shown to Dan early while the film builds; every gate, independent review, deliver the round 4 page.
