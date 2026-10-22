# How To Make Time For Exercise & Nutrition (RO-18): round 3, four changes to the round 2 film

**LFC (long-form content, 16:9).** Sidebar name: `Make Time Exercise LFC R3`. Written 2026-10-21 by Claude (Opus 5.5) at the end of
round 2. Recommended: **Claude Opus 5.5, high effort** (the video started on Claude). **Fire it with Dan's real robot lawn mower footage
attached** (he is sending it with the starter); if it is not attached, ask for it once and build everything else meanwhile.

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections), `.claude/skills/longform-edit/reference/ro18/README.md`
(items 1 to 25; 19 to 25 are round 2's lessons), `/Volumes/Expansion/_edit_work/RO-18/round2/NOTES-R2.md`, then
`/Volumes/Expansion/_edit_work/RO-18/round3-plan/decisions.json` (Dan's words verbatim).

## Where things are

- Round 2 build: `/Volumes/Expansion/_edit_work/RO-18/round2/` (also reachable as `/Volumes/Extreme/_edit_work/RO-18/round2/`, a link).
  Build round 3 in a new `round3/` beside it: copy `recipe/`, the data files (`shots.json`, `plan_resolved.json`, `words*.json`, `edl.json`,
  `lav.wav`, `fit/`, `framing/*.json`, `hf/`, `assets/`, `srt_fixes.json`, `motion/*-final.mp4`, `motion/specs/`), symlink `stock/` and
  `cache/` entries file by file (round 2 did this; `curl -o` onto a symlink overwrites the target), repoint `W` (`grep -rl RO-18/round2 recipe | xargs sed`).
  Never overwrite `round2/review/` or `round2/final/`.
- Round 2 delivery: `claude edited long form content/21 - How To Make Time For Exercise & Nutrition/` (master, SRT, chapters, edit sheet,
  stamps, notes, recipe). Review page http://127.0.0.1:8982/. VLC copy: `Videos to Review/Make Time Exercise LFC R2 - full film.mp4`.
- Film 10:45 (645.278 s, 19,339 frames). Full render: `recipe/render_final.sh` through the render queue (`renderq.py run --group RO-18`),
  then `finish_chain.sh`; edit sheet + `validate.py`; `hairedge18.py` (every-frame hair edge); watch judge; delivery gate on the delivered copy.

## Dan's round 2 notes (verbatim in decisions.json) and what to do

1. **0:12, C46 (12.38 to 16.10, "But you're busy, you have a job, maybe you have kids"):** replace Pexels 6561340 with library **A0063**
   (`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/lifestyle/A0063_stressed-overweight-dad-kitchen-kids_16x9_6s.mp4`):
   the stressed dad pouring coffee in the kitchen while two kids tug at him. 6.0 s source for a 3.7 s slot: pick the part where the coffee
   spills and the kids tug (look at it; the contact sheet is `Media/clip-library/contact/A0063.jpg`). `kind="clip"`, `label=AI`, chip measured
   clear of faces (the dad is centre, kids right: top left is likely clear), `people="other"`, `physique=False`. Grade to sit with the presenter.
   Approved AI clip already used in RO-16 and RO-07, so no new frames or motion: clipcheck the trimmed range and a fresh `frame-reviewer`
   still apply (three sense questions) before Dan sees it. It is in the first 30 s: no belly framing (he is clothed, framed waist up; confirm).
2. **About 2:05 (Dan said "around 125"), the Wispr Flow screen recording:** his attachment, copied to
   `/Volumes/Expansion/_edit_work/RO-18/round3-plan/assets/wispr-flow-screen-recording-20260923.mp4` (iPhone, 1320x2868, 60 fps, 44.6 s, no audio):
   ChatGPT open, the Wispr Flow keyboard, he taps the mic, the "Listening" waveform, then "I need you to make me a restaurant reservation at
   7 pm." appears in the box. Put it in the **phone card beside Dan** (`kind="phone"`, like P01) on "So go and install Wispr Flow today, reclaim
   that 20 minutes a day, and use it to workout" (124.7 to 129.4, presenter now; the next item is T2 at 129.4). 4.7 s is short for a 44 s
   recording: cut it into two or three hard-cut pieces (`src` list) that show the tap, the waveform and the text landing, at normal speed, never
   held. The recording keeps its own iPhone status bar and a red recording dot: crop it (`crop_top`, ro18 README trap 16, measure the rows).
   Real screen recording of Dan's phone, no label. Why 2:05 and not 1:25: 125 s is the presenter line about installing Wispr Flow; 1:25 sits
   inside the approved G03 dictation card. If the round 3 review shows Dan meant 1:25, it moves there in round 4.
3. **4:21, A6 (260.8 to 265.0, "like you're seeing on the screen right now"):** replace the AI robot mower with **Dan's real robot lawn mower
   footage** from the starter. Copy it into `round3/assets/` first (originals are read-only). Colour correct it to sit with the presenter
   (VIDEO-RULES, all B-roll graded), steady and fixed framing, pick the stretch where the mower is clearly driving itself; the slot can start at
   259.3 ("Buy a robot lawnmower like you're seeing on the screen") if the footage is long enough. No label (real footage, no Dan in it), or check
   who is in it. Register it in the clip library on approval.
4. **9:39, A9 (575.9 to 583.4):** remove it ("It doesn't really match up with what I'm saying"). Dan on camera there. Removing a full-screen item
   re-exposes presenter joins: after `resolve.py`, compare `build.all_segments()` framings with round 2's (the script in NOTES-R2 / this
   session did it for the opener) and make sure no same-framing join appears and no long stretch flips W2/T2. If one does, fix it locally with a
   shot `prefer` field (round 2 added `prefer` to `build.all_segments`).

## Checks before Dan sees anything (all as in round 2)

Clipcheck + fresh `frame-reviewer` on the A0063 trim; look at the mower footage and the screen recording in their slots (context clips);
render the full film; finish chain; `hairedge18.py`; watch judge (fresh agent) + negative-events scan; edit sheet (facts file in
`round2/final/facts.json`: update C46 to A0063 other/False, add the phone and mower items) + `validate.py --hash`; delivery gate on the delivered
copy (known rows: audio tone, captions card_collision, captions burned); one `ra-reviewer` with a brief naming the four changes.

## Deliver

`claude edited long form content/21 - .../How To Make Time For Exercise & Nutrition | claude round 3 | 16x9 | RO-18.mp4` and its sidecars,
REVIEW 540p, review page with only the four changes (`recipe/page2.py` pattern), `Videos to Review/Make Time Exercise LFC R3 - full film.mp4`,
the timestamped change list in chat, `queue.py set RO-18 delivered`, Edit Queue mirror, board entry, wrap-up boxes.

## State at handoff

- Round 2 delivered and reviewed by Dan 2026-10-21; these four notes are his whole reply. Queue RO-18: `delivered`.
- Cost so far about $1.51 of the $15 cap. Round 3 needs no paid generation.
- The machine was overloaded when this was written (Dan: "Do not start the edit in this task"). Heavy steps go through `renderq` and wait their turn.
