# Handoff: RO-11 round 1 is with Dan; next round builds the full film (2026-10-01)

**Goal.** Finish RO-11 "When Calories Don't Matter For Fat Loss" (9/23 roll C1705) from Dan's round-1 reply: apply his
notes, generate the AI opener motion he picks, build the full film, gate it, one independent review, deliver.

**Review page (round 1).** http://127.0.0.1:8802/ (launchctl `com.absbyai.ro11-round1-review`, serving
`/Users/Shared/absbyai-review/ro11-round1/`; source `/Volumes/Extreme/_edit_work/ro11/round1/index.html`).
Dan's 3 decisions: (1) first minute 0:00 to 1:01.4, (2) AI opener A (scale), B (awake at 2 AM) or none, (3) the 21
HyperFrames graphics. Record his words against the hashes in `/Volumes/Extreme/_edit_work/ro11/round2-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md`,
`.claude/skills/longform-edit/reference/ro11/README.md` and `../ro10/README.md` (script order and traps).

**State.**
- Cut: 17 source pieces, 53 shots, 9:58 (`edl.json`, `shots.json`; every take choice and restart in `recipe/edl.py`).
  Verbatim listen: `listen/listen_*.txt`. Film words: `words_out.json`.
- Plan: `recipe/plan.py` -> `plan_resolved.json`. 21 template graphics rendered in `hf/renders/` (`hf/manifest.json`,
  `hf/BEATS.md`): 11 lower thirds, 7 fact cards, 2 side lists, 1 cycle. Softblue kinds: 7 section titles
  (FACTOR n OF 7), recap G21. 12 clips (Pexels in `stock/`, library B0287, B0098). Fact-card photos in `assets/`.
- AI opener: frames `aiframes/A-start.png`, `A-end.png`, `B-start.png`, `B-end.png` (nano-banana-pro, reference
  `ref-H.png` = RO-10's man). A01 is a labelled placeholder in the first minute, 0:00 to 0:04.6. No motion generated.
- Audio: chain's own fit on C1705 (`FIT.mp4.voice_chain.json`) + 0.9 dB at 150 Hz. First minute audio gate PASS 13/13, -14.2 LUFS.
- Checks (`round1/checks/all.json`): 20 of 21 graphics PASS clearance, face and fill. G20 reads -211 px at 555.25 s: a
  two-hand gesture passes under the card, not into it (shown to Dan as flagged). Hair 30 px minimum in the first minute.
  Framing solver: zero same-size joins.
- Spend: about $1.70 of $5 ($1.10 Gemini listen, $0.60 opener frames).

**Not done this round (do not claim).** No full film, no SRT or chapters, no delivery gate, no watch pass, no
independent review, no RGB compositor proof on this film (RO-10's proof used the same unchanged code). The junk and
jump-cut pass was run on the source selection and the first minute only.

**Next action.** Record Dan's reply. If he picks an opener: generate the motion from the approved START/END frames
(Veo first/last frame, big body action; RO-12 trap 11), check it frame by frame, replace A01 (kind `clip`, label
AI-GENERATED). Apply notes (`resolve.py`, `from_plan.py --render` re-renders only changed scenes), then the full film with
`build.render_range(0, <end>, <out>)`, SRT + chapters (`../ro10` `finish.py` pattern), `_shared/deliver/gate.py --format
longform`, watch pass, one `ra-reviewer`, deliver to `claude edited long form content/11 - When Calories Don't Matter For
Fat Loss/`, queue `delivered`, register new clips in the clip library.

**Starter prompt (Claude Opus 5.5, effort high):**

Read `Handoffs/handoff-20261001-ro11-round1-dan-review.md`. Here is my reply to the RO-11 round 1 page: <paste>. Record the
decisions, apply them, generate the opener motion I picked, build the full RO-11 film, gate it, run the independent review,
deliver it and send me the review copy.
