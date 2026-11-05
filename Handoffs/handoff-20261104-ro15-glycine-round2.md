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

## Dan's decisions on the page (record his exact words in `round2-plan/decisions.json`)
1. Colour (a) look C / (b) more colour / (c) brighter. 2. Voice (a) option 5 / (b) gated. 3. Opener: Supplement Graveyard AI or camera.
4. AI clips to drop, and X1/X2 picks for Night Sweats, Thermal Camera, Beanie, Out Like A Light. 5. Oura screenshots: he sends them or
keep stock + lower thirds (G11, G14, C06). 6. Ad-lib "thick build" at 2:03.7: keep or cut.

## Next actions
1. Log picks: `blind.py pick aiframes/blind2/<ID> --chose X? --words "<Dan's words>"`. Install from originals (`blind.py reveal`).
2. END frames for every kept idea, from the picked START, on the same model that made the START; frame spec, `framecheck/gate.py START END`,
   a fresh `frame-reviewer` per pair, `--verify` before any page. Show Dan the END frames (small page), then motion only after his OK.
3. Motion on Flow (`flow-veo` agent, background), `clipcheck.py --verify` + fresh reviewer per take; regenerate slop.
4. Apply decisions 1, 2, 5, 6 (a cut changes the EDL: rerun shots, assemble_audio, words, resolve, from_plan, and check every lower third's
   first and last part timing before rendering, README trap 4).
5. Full film, then: edit sheet, `deliver/gate.py --format longform`, `watch.py` + judge, a fresh `ra-reviewer` on the exact file, SRT (fix
   "aura ring" to "Oura Ring", "absbyai .com" to "AbsByAI.com"), chapters. Deliver to
   `claude edited long form content/29 - Sleep Better With Glycine/` plus a copy in `Videos to Review/`.
6. Edit Queue: `queue.py set RO-15 delivered` when the full film goes to Dan; `finalized` only on his word; then the `/video-setup` handoff.

## Starter prompt
> Sleep Better With Glycine LFC R2. Read `Handoffs/handoff-20261104-ro15-glycine-round2.md` and do round 2 of RO-15 with /longform-edit:
> record my round 1 decisions (pasted below), make the END frames and motion for the AI clips I kept, then build, gate, independently
> review and deliver the full film. My decisions: <paste the reply box>
