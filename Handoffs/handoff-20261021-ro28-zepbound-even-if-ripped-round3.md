**CONTENT (LFC).** Task name: `Zepbound Even If Ripped LFC R3`. Model: **Opus 5.5, high effort** (the video started on Claude).

# RO-28 "Why Zepbound Improves Your Health Even If You're Ripped": round 3 (after Dan's round-2 reply)

Release ASAP. Read first: `.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/longform-edit/reference/ro28/README.md` (recipe and traps 1-14), then
Dan's reply to the round-2 page.

## Where everything is
- Work dir: `/Volumes/Expansion/_edit_work/ro28/round2/` (round 1 preserved in `round1/`). Build round 3 in `round3/` (copy the recipe,
  sed `ro28/round2` -> `ro28/round3`; never overwrite round 2).
- Round-2 page: http://127.0.0.1:8929/ (`review/index.html`, `review_server.py 8929`). Dan's round-1 picks: `round2-plan/decisions.json`.
- Locked: colour C (`RO28_GRADE=C`), warm bass voice (`fit/eq.txt`), all round-1 graphics and clips he did not comment on, A1 pharmacist
  quiet double take (`motion/veo/veo/A1d-flow-t3.mp4@0.0`, frames 0-93 only; she turns to camera from 96) with G18 lower third over it ("CONTROVERSIAL TAKE" / "Why You Should Take Zepbound Even
  If You're Ripped"; "Already" dropped for width, offered back), C17/C18/C19 fallbacks for the cut
  A6/A7/A8, stock vial.
- Motion job: `motion/veo/job.json` (veo.py), take specs in take pixels `motion/*.take.spec.json`, prompts `motion/prompts/`.

## Dan was asked (round 2)
0. The A5 skeptic failed every real-or-AI review (11 takes A5/A5b/A5c/A5d; retimes of A5c failed for stutter, frozen hold, 1.25x rush). Dan picks (a) two more Quality takes (200 Flow credits; 700 left on 10-22) or (b) drop it, presenter on camera. plan.py A5 still points at the failed `A5c-t1-f72-127-retime3.mp4`: change it per his pick before any full film.
1. Approve the redrawn A2 frames (doctor says no; ripped patient). 2. Approve the redrawn A3 frames (barbecue, no grill, whole bodies,
white tank tops, skinny-fat middle guy). (The lip-sync question moved into item 0.) Also: "Already" back or not.

## Next actions (round 3)
1. Record his words in `round3-plan/decisions.json`.
2. Approved pairs: motion on Flow (`veo.py add` with take-pixel specs, `flow-veo` agent in the background, 2 takes), `clipcheck.py --verify`,
   a fresh `frame-reviewer`, plus the naturalness question (memory `ai-clips-natural-or-regenerate`: real footage of relaxed people, or AI?
   AI fails; regenerate, never patch). A redraw he rejects: redraw, gate, show only that pair.
3. Lip sync only on his yes (`longform-edit/reference/ro20/lipmeasure20.py`; one failure means mouth closed). If he said "Already" back,
   shrink the G18 point to fit (count before rendering).
4. If nothing is pending: the FULL film. Delivery gate (`_shared/deliver/gate.py --format longform`), watch pass, edit sheet, hair check on
   the exact export (20 px at 1080 and 540), independent `ra-reviewer`, SRT (fix "Zeban/Zetbound", "R.I.P." -> ripped, "GOP" -> GLP-1),
   chapters, delivery folder `claude edited long form content/21 - Why Zepbound Improves Your Health Even If You're Ripped/`, review page
   with a timestamped revision list, VLC copy in `Videos to Review/`.
5. Render queue: wrap each heavy chain as ONE `renderq.py run --group RO-28` step; graphics passes can run on internal scratch (trap 14).

## Starter prompt
> CONTENT (LFC). Rename this task `Zepbound Even If Ripped LFC R3`. Read `Handoffs/handoff-20261021-ro28-zepbound-even-if-ripped-round3.md`
> and do round 3 of "Why Zepbound Improves Your Health Even If You're Ripped" (RO-28) with /longform-edit, using Dan's reply to the
> round-2 page (pasted below). Opus 5.5, high effort.
