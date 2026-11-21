# How To Make Time For Exercise & Nutrition (RO-18): round 2, Dan's picks, AI motion, then the full film

**LFC (long-form content, 16:9).** Sidebar name: `Make Time Exercise LFC R2`.
Written 2026-10-15 by Claude (Opus 5.5) at the end of round 1; updated 2026-10-18 with Dan's reply. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections: Veo through Flow, continue or
hand off, graphics motion, AI clip sense QC, lip sync fallback, first 5 seconds, budget), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/_shared/veo/README.md`, `.claude/skills/longform-edit/SKILL.md`, `.claude/skills/longform-edit/reference/ro18/README.md`
(this film's recipe and traps: two rolls on one virtual timeline, Extreme drive full), then `RO-18/round2-plan/decisions.json`.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/RO-18/` is a link to `/Volumes/Expansion/_edit_work/RO-18/` (the Extreme drive was full). Round 1
  is in `round1/` (recipe in `round1/recipe/`). Build round 2 in a new `round2/` folder beside it, copy `recipe/` and the data files,
  repoint `W`; never overwrite `round1/review/`.
- Round 1 review page: http://127.0.0.1:8981/ (`python3 .claude/skills/_shared/review_server.py 8981 /Volumes/Expansion/_edit_work/RO-18/round1/review`;
  if `launchctl bootstrap` fails with status 5, run it again once). First minute for VLC: `Videos to Review/Make Time Exercise LFC R1 - first minute.mp4`.
- Rolls: 9/23 C1714 + C1715 (sidecars beside them). `frames.py` maps the virtual timeline (C1715 starts at frame 13800).
  Take map `recipe/edl.py` (29 pieces, last clean take of every line, reason per piece). `shots.json` (57 shots), `words.json` (medium.en,
  14 folded restarts patched, hand fixes listed in the README), `words_out.json`, `plan.py` / `plan_resolved.json`, `hf/` (18 lower thirds).
- Film length 10:45 (645.28 s, from `shots.json`; `piece_map.json` runs on audio time and sits up to 1.5 s off, never map film time through it).

## Locked (Dan, 2026-10-18: "Everything else looks good")

Look C + W2/T2 crops (per-shot hair lifts in `framing/crop_y.json`); voice = audio B (chain fit on this film's assembled voice, EDT 56 ms,
no dereverb) + 0.9 dB at 150 Hz + the standard +3 dB at 120 Hz (`fit/eq_B_bass3.txt`); room tone per roll; no music; no SFX; the take map;
every graphic as shown on the round 1 page (approved as is: the 2026-10-17 HyperFrames-motion rule binds new or revised graphics, so do not
rebuild these unless one changes); every stock and Dan clip except C36 and C37.

## Dan's round 1 decisions (recorded in `RO-18/round2-plan/decisions.json`, his words verbatim there)

1. **Opener: camera.** Drop A1 (treadmill clothes rack): *"just use a camera scene. I don't really feel like that is attention-getting."*
   0:00 to 0:07 is Dan on camera (shot `open.0`). Apply the first-5-seconds rule to that shot (framing, a punch-in on the second sentence
   if it lifts the open); no new clip there.
2. **AI clips: A2, A6, A7, A8, A9 all approved** ("looks good" each). Make motion for those five; A1 is gone.
3. **Wispr Flow:** no ScreenFlow demo; keep the round 1 stock dictation clips, the G03 dictation card and the G04 typing vs talking card.
4. **Robot mower:** keep the AI clip A6 ("Robot mower looks good"); no swap to real mower footage.
5. **Equipment:** keep the G08 six-picture card.
6. **C36 and C37: new clips.** *"images of college students or people that are visibly in their late teens or 20s, not children, and more
   similar to the people watching the video."* C36 (film 449.0 to 454.2, "If you're in high school or college ... all of your homework",
   now Pexels 32520679, a lecture hall) and C37 (457.4 to 462.2, "almost everything you're learning ... useless bullshit anyways", now
   Pexels 6672269, a younger-looking student asleep). Pick clearly adult students, mostly young men like the viewers: e.g. a college guy
   doing homework on a laptop in a dorm or library for C36, a bored college student zoning out or asleep in a lecture hall for C37. Each
   must show the line, never repeat a scene already in the film (A7 and A8 are students too: keep them distinct), and be graded to sit
   with the presenter (not darker). Pexels search: the keyless index method in the ro18 README (browser pane + `recipe/px_recv.py`,
   rename the index between gathers). Real or library footage first if any fits (`clip-library`).

## Then, in order

0. Five frame pairs passed `_shared/framecheck/gate.py` and a fresh `frame-reviewer` on 2026-10-15 (specs, reviews and stamps in
   `round1/aiframes/`, `aiframes/framecheck/`). Run `gate.py START END --verify` on A2, A6, A7, A8, A9 first; any frame edit clears both checks.
1. **Motion through Google Flow on Dan's subscription** (VIDEO-RULES top section; `veo.py route --said` must print `flow`, Dan did not say
   rush): `veo.py add JOBDIR <ID> --start ... --end ... --prompt-file ...` for the five, then spawn the `flow-veo` agent in the background
   and keep working on C36/C37 and the plan meanwhile. Flow gives 8 s takes at 24 fps 1080p; trim to the slot and conform to 29.97.
   Slots: A2 66.3 to 70.0, A6 260.8 to 265.0, A7 454.2 to 457.4, A8 490.1 to 497.5, A9 575.9 to 583.4. Credits out: ask Dan once with
   the count and dollar estimate, never pay without his yes.
   A2: lip sync on Dan's own impression line from "oh Dan, my phone" (source virtual 238.54 to 242.21 on C1714) with
   `longform-edit/reference/ro06/lipsync.py` (a small paid call, about $0.50, inside the $15 cap), measured with `ro20/lipmeasure20.py`
   before Dan sees it; one failed check means the no-sync fallback (mouth closed, Dan's voice over it).
2. **Before Dan sees any motion:** `framecheck/clipcheck.py TAKE --spec aiframes/<ID>.spec.json [--frames A:B] --verify` plus a fresh
   `frame-reviewer` with the three sense questions. Risks the reviewers named: A6 the bell's path at the top; A7 the lid must close onto
   its own base; A8 the pen must not grow a second clip as it drops; A9 the boss must walk in, not appear.
3. Plan: drop A1; each approved `ai` item becomes `kind="clip"`, `label="AI-GENERATED"`, chip measured clear of faces; C36/C37 to the new
   clips. `resolve.py`, then `from_plan.py --render` (only changed graphics re-render), `dupscan.py`.
4. Full film: `build.render_range(0, 645.28, round2/RO18_MASTER.mp4)`, then the finish chain from RO-17 (`finish.py`, `finish_chain.sh`:
   audio gate, transcript, SRT from the delivered audio with the spellings Wispr Flow, Claude, Abs By AI, ChatGPT, robotaxis, Kelley Blue
   Book; chapters; watch pass; `haircheck.py`; hyperframes `checks.py`), one `ra-reviewer` independent review (the three AI questions per
   clip in its brief; the two new clips' age and fit), edit sheet + `validate.py`, delivery gate (`--format longform`), deliver to
   `claude edited long form content/<NN> - How To Make Time For Exercise & Nutrition/` with the REVIEW 540p copy, A/B, stamps, notes, recipe.
5. Copy the full film to `Videos to Review/Make Time Exercise LFC R2 - full film.mp4`, open the folder. Send Dan the page and file names
   plus the later-round revision list: every change with its exact timestamp in the new film and a short watch range (the opener, the five
   AI clips, C36, C37). Name the video by its title. `queue.py set RO-18 delivered`, mirror to the Edit Queue page, board entry, commit.
   Register the new AI clips and stock in the clip library on approval. End with the two wrap-up boxes (CLAUDE.md).

## Round 1 independent checks (fixed before Dan saw the page)

An independent reviewer found 17 fix-level problems on the first page; all were fixed and re-rendered: the app-tour phone card at the
close overlapped a full-screen clip and wrapped the picture (`resolve.py` now never overlaps a full-screen item and a phone card); a click
at every C1714 join (the room-tone window began on a click, now 286.75 to 289.0 and C1715 944.3 to 947.3); notes-to-Dan wording inside
graphics; rows that appeared before their words (now `reveal` on the word); lower thirds under 3 s; the intro clip, a standing man on
"sitting", a student writing by hand on "AI", two pairs of repeated stock scenes, two dark clips (lifted), the vertical dating-app clip
(dropped); and the RO-14 review-page screenshot (now a grid of this video's own graphics, `recipe/grid.py`). Report:
`round1/review/INDEPENDENT-CHECK.md`. A second reviewer confirmed all 17 and found two more, also fixed: the B0035 app recording's own
status bar doubled in the phone card (`crop_top=92` on P01) and a G04 label ran past the card edge. Report: `INDEPENDENT-RECHECK.md`.
Notes it left (not blocking): C40 is a little darker than the presenter (luma 57 vs 69 to 76); C46 is a posed man with little motion.

## Cost ledger

Known: Gemini about $1.20 (verbatim restart listen in seven chunks; the impression-voice check). Codex images: about 34 (frames and
redraws), on the subscription ($0). Veo: $0 so far (Flow credits from here). Cap: $15 for this long-form (Dan 2026-10-13). Unknown: none.
