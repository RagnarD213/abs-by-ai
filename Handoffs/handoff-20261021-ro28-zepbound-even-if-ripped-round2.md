**CONTENT (LFC).** Task name: `Zepbound Even If Ripped LFC R2`. Model: **Opus 5.5, high effort** (the video started on Claude; VIDEO-RULES 2026-10-20 evening: a video stays with the AI it started on).

# RO-28 "Why Zepbound Improves Your Health Even If You're Ripped": round 2 (after Dan's round-1 reply)

Release ASAP (the script says "this year"; the FDA lower third prints "August 2026").

## Read first
`.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/longform-edit/reference/ro28/README.md` (this film's recipe and traps), then Dan's reply to the round-1 page.

## Where everything is
- Work dir: `/Volumes/Expansion/_edit_work/ro28/round1/` (`/Volumes/Extreme/_edit_work/ro28` links to it). Recipe: `recipe/`
  (frames.py, edl.py, shots.py, plan.py, resolve.py, build.py, gfx.py, stills.py, review_media.py, page.py, page_extra.py,
  chain scripts). Build round 2 in `/Volumes/Expansion/_edit_work/ro28/round2/` (copy the recipe; never overwrite round 1).
- Round-1 page: http://127.0.0.1:8928/ (`review/index.html`; served by `review_server.py 8928`). First minute 1080p:
  `review/first-minute/DRAFT - RO-28 round 1 - first minute.mp4`; VLC copy `Videos to Review/Zepbound Even If Ripped LFC R1 - first minute.mp4`.
- Independent check of the round-1 page and what was fixed from it: `review/INDEPENDENT-CHECK.md`.
- AI frames (7 pairs, gate + fresh reviewer PASS, `gate.py --verify` exit 0): `aiframes/A1,A2,A3,A5,A6,A7,A8-start/end.png`, specs in
  `aiframes/specs/`, prompts in `aiframes/prompts/`, records `aiframes/pairs.json`.

## State at the end of round 1
- Cut: roll C1771, 17 pieces, 6:26.0 (`edl.json`, `shots.json`, 34 shots). Last clean take of every line; the ad-lib "That is (the) standard
  starting dose" and an aside after "seven out of 10 people" cut (listed on the page).
- Framing: W2 3552x1998 @144 and T2 2704x1521 @568, y per shot from the measured hair top (`framing/crop_y.json`); first minute hair
  clearance 48 px minimum (1080p and 540p).
- Colour options (frames.GRADES): A Rich Balanced (recommended, the approved RO-25 grade), B Richer (RO-27 pick), C A + warm. Voice options
  (`options/voice/`): warm bass (recommended; RO-27's pick, first in 11 blind listens), warm bass + 3 dB at 120 Hz, chain default, untreated.
  `fit/eq.txt` holds the warm bass EQ. First-minute audio gate: all rows pass except tone (fixed tone shape, the known mismatch).
- Graphics: 27 HyperFrames (14 lower thirds with CAPITALS eyebrows typed and `topic_case="preserve"`, 10 fact cards, 3 side lists).
  Checks pass except G14 (hand 2 px sideways but below the card) and G16 (59 px), both cleared by eye.
- Clips: 16 (Dan's pool B-roll C1746/C1744/C1742/C1750/C1743 cropped in and graded POOL / POOL_LIFT / POOL_LIFT2; library B0396, B0390,
  B0394, A0152, B0481, A0166, B0273, B0214; Pexels 7556330, 5998399, 8413642).
- AI slots render as the presenter until motion exists (`build.render_range(placeholder_ai=False)`).

## Decisions Dan was asked (5)
1. Colour (a/b/c). 2. Voice (a/b/c/d). 3. Opener: pharmacist double take or camera. 4. Which AI clips to drop, and "lip sync OK" for the
skeptic (about $0.50 of paid Replicate lip sync; VIDEO-RULES 2026-10-20: paid generation is asked every time). 5. Vial: keep stock or Dan films his own.

## Next actions (round 2)
1. Record Dan's words in `round2-plan/decisions.json` (per item: id, path, sha256, verdict, his words, scope).
2. Motion for the approved AI pairs on the Google Flow subscription: queue with `_shared/veo/veo.py add`, spawn the `flow-veo` agent in the
   background; every take through `framecheck/clipcheck.py --verify` and a fresh `frame-reviewer` (three sense questions) before any page.
   A5 lip sync only if Dan said OK; measure it (`longform-edit/reference/ro20/lipmeasure20.py`); one failure means no lip sync (mouth closed).
3. Apply the colour/voice picks (frames.GRADE_KEY via `RO28_GRADE`, `fit/eq.txt`), rebuild changed items, then the FULL film only when
   nothing is pending: delivery gate (`_shared/deliver/gate.py --format longform`), watch pass, edit sheet, hair check on the exact export,
   independent `ra-reviewer`, SRT (fix "Zeban/Zetbound", "R.I.P." -> ripped, "GOP" -> GLP-1), chapters, delivery folder
   `claude edited long form content/21 - Why Zepbound Improves Your Health Even If You're Ripped/`, review page with timestamps.
4. Render-queue lesson: wrap each heavy chain in ONE `renderq.py run --group RO-28` step (the queue waits were 1 to 2.5 hours each on 10-20).

## Starter prompt
> CONTENT (LFC). Rename this task `Zepbound Even If Ripped LFC R2`. Read `Handoffs/handoff-20261021-ro28-zepbound-even-if-ripped-round2.md`
> and do round 2 of "Why Zepbound Improves Your Health Even If You're Ripped" (RO-28) with /longform-edit, using Dan's reply to the
> round-1 page (pasted below). Opus 5.5, high effort.
