# LFC · Sleep Better With Glycine LFC R2 (RO-15): from Dan's round 1 picks to the full film

**Category: long-form content (LFC).** Organic, Claude-started: Opus 5.5, high effort, every round (VIDEO-RULES, 2026-10-20).
Release slot: Wed Dec 23, 2026; edited and approved by Dec 16 (`Docs/LONGFORM_RELEASE_CALENDAR.md`).

## Read first
- `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
  `.claude/skills/longform-edit/reference/ro15/README.md` (this film's recipe and traps).
- Round 1 work dir: `/Volumes/Extreme/_edit_work/RO-15/round1/` (recipe/, review/, logs/). Review page: http://127.0.0.1:9715/
  (`review_server.py 9715 <round1>/review`). Build round 2 in a new `round2/` folder; never overwrite round 1.
- Independent checks of the round 1 page: `review/INDEPENDENT-CHECK.md` (17 fixes, all applied) and `review/INDEPENDENT-RECHECK.md`.

## State at the end of round 1 (2026-11-04)
- Cut: 9 pieces of C1709, 5:24, last clean take of every line (`edl.json`, reasons in `recipe/edl.py`). 26 shots, W2/T2 alternating,
  crops lifted on 15 shots for hair (`framing/crop_y.json`); first-minute hair minimum 36 px at 1080p.
- Look: locked 9/23 look C (`frames.GRADES["C"]`) recommended; options C-rich, C-bright on the page.
- Voice: option 5 recommended (studio B + bass lift, no gate; `fit/eq.txt` = `FINISH:...`). First-minute audio gate fails only the tone row
  (the known bass-lift mismatch).
- Plan: `recipe/plan.py` (38 items: 8 AI slots A1 to A8, 9 clips, 16 lower thirds, 5 side lists, 1 study card, 1 app phone card).
- AI start frames: blind sets in `aiframes/blind2/<ID>/` (key hidden; `blind.py pick` logs Dan's choice, `blind.py reveal` only to install).
  Pairs: A2, A3, A5, A8 (X1, X2). Single: A1, A4, A6, A7. Reviews: `aiframes/start-frames-review.md`, `aiframes/rereview/`.
  Prompts: `aiframes/prompts/`. Google twins dropped after two failed reviews: A1, A4, A7; A6 refused by Google.
- Spend: about $1 of Gemini listening. Frames on Codex and Google subscriptions. No motion generated. Long-form cap $15 (paid only with
  Dan's yes; default is the Flow subscription via the `flow-veo` agent).

## Dan's decisions (2026-11-05), recorded with hashes in `/Volumes/Extreme/_edit_work/RO-15/round2-plan/decisions.json`
- First minute: approved ("Okay, first minute looks good."). Colour: **C-rich** ("Let's go with color C rich"): `frames.GRADE = "C-rich"`.
- Voice: **A**, option 5, studio B + bass lift, no gate ("Let's go with A for the voice."): `fit/eq.txt` FINISH path unchanged.
- AI clips, his words in the decisions file:
  - A1 Supplement Graveyard: **killed** ("lame, kill that"). The opener stays on camera.
  - A2 Night Sweats: **keep, start frame X2** (pick logged with `blind.py pick`).
  - A3 Thermal Camera: **not mentioned. Ask Dan in one line;** do not drop or make it without his answer.
  - A4 Kicking The Covers Off: **keep** (one Codex frame).
  - A5 Three Blankets: **killed**.
  - A6 Thermostat War: **redo with new START and END frames, two sets** (Codex and Google): the man sweating, larger and more muscular;
    the woman wrapped in a blanket and cold. Old A6 frame retired.
  - A7 Handful Of Capsules: **keep** (one Codex frame). A8 Out Like A Light: **keep, X1** (pick logged).
- Still open on the page: decision 5, his real Oura screenshots (send or keep stock), and decision 6, the "thick build" ad-lib at 2:03.7.
  Ask both in one line with the frames page.
- **New standing rule (Dan, 2026-11-05, VIDEO-RULES top):** every AI idea is first shown as a complete START and END pair; two versions =
  two complete pairs, each END on its own START's model. So A6 comes back as two full pairs; A2, A4, A7, A8 get their END frames.

## Next actions
1. Picks are logged. Install each kept START from its original (`blind.py reveal round1/aiframes/blind2/<ID> --label X?`; tell Dan the
   source only if he asks).
2. END frames for A2, A4, A7, A8 from the kept START on the same model (Codex: `codex-image.sh --image START`; Google: a background Flow
   helper briefed with RO-15 README trap 2 on ~/Downloads). A6: two new full pairs. Every pair: frame spec, `framecheck/gate.py START END`,
   a fresh `frame-reviewer`, `--verify`. Then a small frames page (port 9715 or a new one) showing whole pairs, plus the A3, Oura and
   ad-lib questions. Motion only after Dan picks.
3. Motion on Flow (`flow-veo` agent, background), `clipcheck.py --verify` + fresh reviewer per take; regenerate slop.
4. Apply decisions 1, 2, 5, 6 (a cut changes the EDL: rerun shots, assemble_audio, words, resolve, from_plan, and check every lower third's
   first and last part timing before rendering, README trap 4).
5. Full film, then: edit sheet, `deliver/gate.py --format longform`, `watch.py` + judge, a fresh `ra-reviewer` on the exact file, SRT (fix
   "aura ring" to "Oura Ring", "absbyai .com" to "AbsByAI.com"), chapters. Deliver to
   `claude edited long form content/29 - Sleep Better With Glycine/` plus a copy in `Videos to Review/`.
6. Edit Queue: `queue.py set RO-15 delivered` when the full film goes to Dan; `finalized` only on his word; then the `/video-setup` handoff.

## Starter prompt
> Sleep Better With Glycine LFC R2. Read `Handoffs/handoff-20261104-ro15-glycine-round2.md` and continue RO-15 with /longform-edit: my
> round 1 decisions are already recorded there. Make the START and END frame pairs (END frames for Night Sweats, Covers, Capsules and
> Out Like A Light; two new full pairs for the Thermostat War), run the frame gate and a fresh reviewer on every pair, and show me the
> pairs with the open questions. Run `editcap.py acquire RO-15` before production.

## Round 2 progress (2026-11-05, Claude)
- Frame pairs done: page http://127.0.0.1:9716/ (`review_server.py 9716 /Volumes/Extreme/_edit_work/RO-15/round2/review`), six pairs, each
  gate + fresh reviewer PASS (`round2/aiframes/pairs/*`): A2 (round-1 X1 start; the X2 END failed review twice), A4, A6 X1/X2 (both
  Codex; Google refused the START 8 of 8; key in `pairs/A6-blind.json`, never shown), A7 (START widened for headroom), A8.
- Waiting on Dan: pairs OK / changes, A6 X1 or X2, A3 keep or drop, Oura screenshots, "thick build" ad-lib. Edit slot released (`--review`).
- Recipe lessons: `.claude/skills/longform-edit/reference/ro15/README.md` "Round 2 frames"; commit 224f152 local, push blocked by a
  live shared file: next safe-push carries it.
- Next after Dan answers: motion on Flow (`flow-veo`), then handoff steps 3 to 6.
