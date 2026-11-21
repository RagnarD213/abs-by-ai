# How To Make Time For Exercise & Nutrition (RO-18): round 3, four changes to the round 2 film

**LFC (long-form content, 16:9).** Sidebar name: `Make Time Exercise LFC R3`. Written 2026-10-21 by Claude (Opus 5.5) at the end of
round 2. Recommended: **Claude Opus 5.5, high effort** (the video started on Claude). Dan's real robot lawn mower footage arrived 2026-10-22 and is already in `round3-plan/assets/` (item 3); the round can start any time.

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
   footage. It arrived 2026-10-22 (AirDrop) and was reviewed in the round 2 session; copies are in
   `/Volumes/Expansion/_edit_work/RO-18/round3-plan/assets/`** (originals `~/Downloads/IMG_1005..1008.MOV`):
   - `mower-IMG_1006-open-lawn.MOV` (BEST): iPhone portrait 2160x3840 (rotation tag -90, ffmpeg auto-rotates), 60 fps, **HLG HDR**, 34.2 s.
     The mower drives across open lawn, large and sharp, handheld following it; close passes at 0 to 6 s and 16 to 24 s.
   - `mower-IMG_1005-dock-exit.MOV`: same format, 29.5 s. The mower backs out of its dock by the pool fence and drives off (0 to 9 s); sun
     glare and haze from about 10 s on.
   - `mower-IMG_1007-wide.MOV` (4 s) and `IMG_1008` (21 min, left in Downloads, not copied): low wide shots of the yard, the mower is a speck in
     the distance. Not usable.
   - **Widescreen crop works:** a 2160x1215 window of the portrait frame (y about 1550 to 1650 for these moments) scaled to 1920x1080, after
     HLG to SDR tone mapping. Proof stills: `round3-plan/assets/mower-crop-test.jpg` (the session used
     `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`, then crop;
     it looks rich and natural). Pick the crop's y per moment so the whole mower stays in frame (it moves in the handheld frame); keep it still
     or move it smoothly, never chase. Grade it to sit with the presenter. Real footage, no person in it, no label. The mower's own
     "Mammotion" badge is visible; it is his mower, keep it.
   - **Placement (editor's plan, recorded in the round 2 session's reply to Dan, which he can overrule on the page):**
     a. **4:21 slot (A6, 260.8 to 265.0):** IMG_1006 from about 0.5 s (the close pass), 4.2 s. It may start at 259.3 on "Buy a robot lawnmower
        like you're seeing on the screen" if T4's card hand-off allows.
     b. **4:31, "A robot lawn mower does all of that for you" (270.9 to 273.3):** IMG_1006's second close pass (about 17 to 19.5 s). Presenter
        now; C25 ends 270.64, so close the gap (no presenter flash under 0.9 s).
     c. **4:43, "after that, it goes out by itself, cuts the grass" (about 283.3 to 288.3, after the G15 lower third ends at 283.24):**
        IMG_1005 0.5 to 5.5 s, the mower leaving its dock. Check the glare; stop before 9 s.
   Register the used stretches in the clip library on approval (real B-roll of Dan's own mower).
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

- Round 2 delivered and reviewed by Dan 2026-10-21; these four notes are his whole reply. Mower footage received and reviewed 2026-10-22 (item 3).
- Cost so far about $1.51 of the $15 cap. Round 3 needs no paid generation.
- The machine was overloaded when this was written (Dan: "Do not start the edit in this task"). Heavy steps go through `renderq` and wait their turn.
