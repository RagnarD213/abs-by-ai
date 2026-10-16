# RO-18 "How To Make Time For Exercise & Nutrition": round 2, apply Dan's round 1 picks, AI motion, then the full film

**LFC (long-form content, 16:9).** Sidebar name: `Make Time Exercise LFC R2`.
Written 2026-10-15 by Claude (Opus 5.5) at the end of round 1. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections: AI clip sense QC, lip sync
fallback, budget), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro18/README.md` (this film's recipe and traps: two rolls on one virtual timeline, Extreme drive
full), then Dan's reply to the round 1 page.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/RO-18/round1/` (recipe in `recipe/`). Its `stock/`, `cache/`, `review/`, `hf/` and `assets/*`
  are links into `/Volumes/Expansion/_edit_work/RO-18/round1/` because the Extreme drive was full (5 GB free on 10-15). Build round 2 in a
  new `round2/` folder (on Expansion, linked the same way), copy `recipe/` and the data files, repoint `W`; never overwrite `round1/review/`.
- Round 1 review page: http://127.0.0.1:8981/ (`python3 .claude/skills/_shared/review_server.py 8981 /Volumes/Expansion/_edit_work/RO-18/round1/review`).
  First minute for VLC: `Videos to Review/Make Time Exercise LFC R1 - first minute.mp4`.
- Rolls: 9/23 C1714 + C1715 (sidecars beside them). `frames.py` maps the virtual timeline (C1715 starts at frame 13800).
  Take map `recipe/edl.py` (29 pieces, last clean take of every line, reason per piece). `shots.json` (57 shots), `words.json` (medium.en,
  14 folded restarts patched, hand fixes listed in the README), `words_out.json`, `plan.py` / `plan_resolved.json`, `hf/` (18 lower thirds).
- Film length 10:45 (645.28 s, from `shots.json`; `piece_map.json` runs on audio time and sits up to 1.5 s off, never map film time through it).

## Locked by the editor in round 1 (Dan saw them as "What I decided"; reopen only if he names them)

Look C + W2/T2 crops (per-shot hair lifts in `framing/crop_y.json`); voice = audio B (chain fit on this film's assembled voice, EDT 56 ms,
no dereverb) + 0.9 dB at 150 Hz + the standard +3 dB at 120 Hz (`fit/eq_B_bass3.txt`); room tone per roll; no music; no SFX; Soft Blue
HyperFrames / softblue graphics; the take map; all stock and Dan clips as listed on the page.

## Dan's decisions on the round 1 page (record his words in `round2-plan/decisions.json`, then act)

1. **Opener** (0:00 to 0:07): A1 "The treadmill clothes rack" (recommended) / camera.
2. **AI clips to drop** from A1 treadmill, A2 voice-to-text rage (lip-synced to Dan's impression voice from "oh Dan, my phone", film 66.3 to
   70.0; source virtual 238.54 to 242.21 on C1714), A6 robot mower, A7 teacher slams the laptop, A8 essays by hand, A9 nobody at work has to know. A dropped
   idea becomes the fallback named on the page.
3. **Wispr Flow demo:** if Dan uploads the ScreenFlow recording, lay his real Wispr Flow under C02 ("You hold down a button, you talk",
   film 54.5 to 60.0) and consider it for C03 to C05; keep the G03 dictation card.
4. **Robot mower:** if (a), after the 10/17 shoot find the robot mower B-roll (DS-29's), grade it to the film, and replace A6 (film 260.8
   to 265.0, "like you're seeing on the screen right now"); A6 then drops.
5. **Equipment:** (a) keep G08, or (b) the six pieces filmed on 10/17 (DS-27's B-roll) in its place, each on its word.

## Then, in order

0. Six frame pairs passed `_shared/framecheck/gate.py` and a fresh `frame-reviewer` on 2026-10-15 (specs, reviews and stamps in `aiframes/`,
   `aiframes/framecheck/`; rejected versions in `aiframes/rejected/`). Before generating motion run `gate.py START END --verify` on each
   approved pair; any frame edit clears both checks. Dropped in round 1 after three failed tries each: A3 traffic, A4 roll out of bed,
   A5 dish mountain (do not revive without new designs).
1. Motion from exactly those frames: `.claude/skills/ai-clip-ideas/reference/gen-veo-keyframes.js` (Veo 3.1 Fast, no audio, about $0.15 a
   second). Durations: A1 7 s, A2 6 s, A6 6 s, A7 5 s, A8 8 s, A9 8 s. Guard any generation script with `if __name__ == "__main__":`.
   A2: lip sync on Dan's own line (`longform-edit/reference/ro06/lipsync.py`, `ro20/lipmeasure20.py` before Dan sees it); one failed check
   means the no-sync fallback (mouth closed, Dan's voice over it).
2. **Before Dan sees any motion:** `framecheck/clipcheck.py TAKE --spec aiframes/<ID>.spec.json [--frames A:B] --verify` plus a fresh
   `frame-reviewer` with the three sense questions. Risks the reviewers named: A1 hair shape during the head turn; A6 the bell's path at the
   top; A7 the lid must close onto its own base; A8 the pen must not grow a second clip as it drops; A9 the boss must walk in, not appear.
3. Plan: each approved `ai` item becomes `kind="clip"`, `label="AI-GENERATED"`, chip measured clear of faces. `resolve.py`, then
   `from_plan.py --render` (only changed graphics re-render), `dupscan.py`.
4. Full film: `build.render_range(0, 645.28, round2/RO18_MASTER.mp4)`, then the finish chain from RO-17 (`finish.py`, `finish_chain.sh`:
   audio gate, transcript, SRT from the delivered audio with the spellings Wispr Flow, Claude, Abs By AI, ChatGPT, robotaxis, Kelley Blue
   Book; chapters; watch pass; `haircheck.py`; hyperframes `checks.py`), one `ra-reviewer` independent review (the three AI questions per
   clip in its brief), edit sheet + `validate.py`, delivery gate (`--format longform`), deliver to
   `claude edited long form content/<NN> - How To Make Time For Exercise & Nutrition/` with the REVIEW 540p copy, A/B, stamps, notes, recipe.
5. Copy the full film to `Videos to Review/Make Time Exercise LFC R2 - full film.mp4`, open the folder, send Dan the page + file names.
   `queue.py set RO-18 delivered`, mirror to the Edit Queue page, board entry, commit. Register new clips in the clip library on approval.

## Round 1 independent check (fixed before Dan saw the page)

An independent reviewer found 17 fix-level problems on the first page; all were fixed and re-rendered: the app-tour phone card at the
close overlapped a full-screen clip and wrapped the picture (`resolve.py` now never overlaps a full-screen item and a phone card); a click
at every C1714 join (the room-tone window began on a click, now 286.75 to 289.0 and C1715 944.3 to 947.3); notes-to-Dan wording inside
graphics; rows that appeared before their words (now `reveal` on the word); lower thirds under 3 s; the intro clip, a standing man on
"sitting", a student writing by hand on "AI", two pairs of repeated stock scenes, two dark clips (lifted), the vertical dating-app clip
(dropped); and the RO-14 review-page screenshot (now a grid of this video's own graphics, `recipe/grid.py`). Report:
`round1/review/INDEPENDENT-CHECK.md`. A second reviewer confirmed all 17 and found two more, also fixed: the B0035 app recording's own
status bar doubled in the phone card (`crop_top=92` on P01) and a G04 label ran past the card edge. Report: `INDEPENDENT-RECHECK.md`.

## Cost ledger

Known: Gemini about $1.20 (verbatim restart listen in seven chunks; the impression-voice check). Codex images: about 34 (frames and
redraws), on the subscription ($0). Veo: $0 so far. Cap: $15 for this long-form (Dan 2026-10-13). Unknown: none.
