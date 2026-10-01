# Handoff: RO-13 round 1 is with Dan; next round builds the full film (2026-10-01)

**Goal.** Finish RO-13 "Can You Drink Alcohol And Still Have Abs?" (9/23 roll C1707) from Dan's round-1 reply: apply his
notes, generate the AI motion he approves, build the full film, gate it, one independent review, deliver.
Session name for the next round: `Can You Drink Alcohol And Still Have Abs LFC R2`.

**Review page (round 1).** http://127.0.0.1:8803/ (launchctl `com.absbyai.ro13-round1-review`, serving
`/Users/Shared/absbyai-review/ro13-round1/`; source `/Volumes/Extreme/_edit_work/ro13/round1/index.html`).
Dan's 5 decisions: (1) first minute 0:00 to 1:10.8, (2) AI clips: A the opener (0:00 to 0:03), B the mirror (0:17 to
0:24), both / one / neither, (3) "an entire day's deficit" (used) or "an entire week's deficit", (4) the "take a photo of
your drink" beat: real app capture in the phone layout, or keep stock clip C08, (5) the 25 HyperFrames graphics. Record
his words against the hashes in `/Volumes/Extreme/_edit_work/ro13/round2-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md`,
`.claude/skills/longform-edit/reference/ro13/README.md`, then `../ro11/README.md` and `../ro10/README.md`.

**State.**
- Cut: 21 source pieces, 37 shots, 7:10 (`edl.json`, `shots.json`; every take choice in `recipe/edl.py`). Verbatim
  listen: `listen/listen_*.txt`; restart windows re-transcribed in `logs/verify_asr.txt`. Film words: `words_out.json`.
- Plan: `recipe/plan.py` -> `plan_resolved.json`. 25 template graphics in `hf/renders/` (`hf/manifest.json`,
  `hf/BEATS.md`): 19 lower thirds, 3 fact cards, 3 side lists. Softblue kinds: 6 section titles (RULE n OF 6), recap G26,
  three-photo slate P01 (RO-16's approved panels, `assets/g03/`). 17 stock placements from 21 Pexels clips in `stock/`.
- AI clips: frames `aiframes/A-start.png`, `A-end.png`, `B-start.png`, `B-end.png` (nano-banana-pro; B uses RO-10's man,
  `ref-H.png`). A01 and A02 are labelled placeholders in the first minute. No motion generated.
- Audio: chain's own fit on C1707 (`FIT.mp4.voice_chain.json`) + 0.9 dB at 150 Hz. First minute audio gate PASS 13/13,
  -14.2 LUFS; A/B vs Muhammad beside it.
- Checks (`round1/checks/all.json`): 25 of 25 graphics PASS clearance, face and fill. Hair 26 px minimum, 48 median in
  the first minute. Framing solver: zero same-size joins. Every piece's first and last frames looked at
  (`logs/joins_sheet*.jpg`): on camera, eyes on the lens.
- Spend: about $1.70 of $5 ($1.10 Gemini listen, $0.60 AI frames).

**The deficit line (decision 3).** `recipe/edl.py` piece `rules` ends on the first copy ("day's", out 416.28). For
"week's": end `rules` at 412.86 ("easily."), add a piece 417.68 to 420.94, then re-run shots, assemble, medium.en,
words_out, resolve, and change G10's detail copy. Everything after it shifts by about 0.2 s.

**The app capture (decision 4).** If Dan wants it: record a real macro tracker session logging a photo of a drink on the
live app (memory `local-funnel-test-recipe`; the before/after rule does not apply, no physique shown), one capture
session, and place it with kind `phone` (RO-05's approved shell; `gfx.iphone`) over "This is the part where the app does
the work for you. Take a photo of your drink and you're done." (2:58.9 to 3:04.0). Check the side-layout rules (RO-12
trap 6) and the framing solver again.

**Not done this round (do not claim).** No full film, no SRT or chapters, no delivery gate, no watch pass, no
independent review, no RGB compositor proof on this film (RO-10's proof used the same unchanged code). The junk and
jump-cut pass covered the source selection and the first minute only. `roll_sidecar.py` has no sidecar for C1707 and
`mark-used` was not run (do it when the EDL is final). No clip is registered in the clip library yet.

**Known, left for Dan's call.** "far more moderately than I do in the past" (5:55): both takes say "do"; listed on the page.

**Next action.** Record Dan's reply. Generate approved AI motion from the approved START/END frames (Veo first/last
frame; A is one arm move, B is a shirt drop and a head drop, both big body actions; RO-12 trap 11), check frame by
frame (hands, bottle, mirror reflection matching the man), swap A01/A02 to kind `clip` with label AI-GENERATED. Apply
notes (`resolve.py`, `from_plan.py --render` re-renders only changed scenes), then the full film with
`build.render_range(0, <end>, <out>)`, SRT + chapters (`../ro10` `finish.py` pattern), `_shared/deliver/gate.py --format
longform`, watch pass, one `ra-reviewer`, deliver to `claude edited long form content/12 - Can You Drink Alcohol And
Still Have Abs/` (check the next free number), queue `delivered`, register new clips in the clip library.

**Starter prompt (Claude Opus 5.5, effort high):**

Read `Handoffs/handoff-20261001-ro13-round1-dan-review.md`. Name this session "Can You Drink Alcohol And Still Have Abs
LFC R2". Here is my reply to the RO-13 round 1 page: <paste>. Record the decisions, apply them, generate the AI motion I
approved, build the full RO-13 film, gate it, run the independent review, deliver it and send me the review copy.
