# Handoff: RO-10 round 1 (first all-HyperFrames film) is with Dan; next round builds the full film (2026-09-30)

**Goal.** Finish RO-10 "Calories: The Reason You're Not Losing Weight" (9/23 roll C1704) from Dan's round-1 reply:
apply his notes, then build the full film, gate it, one independent review, deliver. First film whose lower thirds,
fact cards, 3A side lists and cycle diagram all come from the approved HyperFrames templates.

**Review page (round 1).** http://127.0.0.1:8801/ (launchctl `com.absbyai.ro10-round1-review`, serving
`/Users/Shared/absbyai-review/ro10-round1/`; source `/Volumes/Extreme/_edit_work/ro10/round1/index.html`).
Dan's 4 decisions: (1) first minute 0:00 to 1:16.6, (2) the 15 HyperFrames graphics, (3) T1 "Get On A GLP-1
Medication" vs "Take Zepbound", (4) keep the on-camera opener vs AI opener frames. Record his words in
`/Volumes/Extreme/_edit_work/ro10/round2-plan/decisions.json` with sha256 of each file (PRE-RENDER-APPROVAL "How a round works").

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md` ("One graphics
pass for any video"), `.claude/skills/longform-edit/reference/ro10/README.md` (order of scripts and the traps).

**State.**
- Cut: 21 source pieces, 46 shots, 8:38 (`edl.json`, `shots.json`; take choices and every restart in `recipe/edl.py`).
  Gemini verbatim listen results: `listen/listen_*.txt`. Assembled transcript `asr_assembled_medium.json`, film words `words_out.json`.
- Plan: `recipe/plan.py` -> `plan_resolved.json`. 15 template graphics rendered in `hf/renders/` (manifest `hf/manifest.json`,
  beat sheet `hf/BEATS.md`); softblue kinds: 8 way titles (WAY n OF 8), recap G16, phone P01; 15 clips (Pexels in `stock/`,
  library B0017, B0038). Fact-card photos in `assets/`.
- Picture: `recipe/build.py` (framing solved over the whole film by `all_segments()`; side cards W4S = W4 crop at x 0,
  W2 + stretch fallback; HyperFrames composited by `_shared/hyperframes/composite.py` in the frame loop).
- Audio: chain's own fit on C1704 (`FIT.mp4.voice_chain.json`) + 0.9 dB at 150 Hz. First minute audio gate PASS 13/13.
- Checks (`round1/checks/all.json`): clearance, face, fill on every graphic; RGB fidelity 0 changed pixels of 964 M; hair 28 px min.
- Spend: $0 generation; about $1.30 Gemini listening (of $5 per video).

**Next action.** Apply Dan's notes (re-run `resolve.py`, `from_plan.py --render` re-renders only changed scenes), then
`python3 -c "import sys; sys.path.insert(0,'recipe'); import build; build.render_range(0, <end>, '<out>')"` for the full film,
SRT + chapters (RO-12 `finish.py` pattern), `_shared/deliver/gate.py --format longform`, watch pass, one independent
`ra-reviewer`, deliver to `claude edited long form content/10 - Calories The Reason You're Not Losing Weight/`, Edit Queue
status `delivered`, update `00-MASTER.md`. Mark RO-10 as the first full-template film in `hyperframes/README.md`.
After Dan approves the HyperFrames graphics: delete this handoff's rows in `Handoffs/README.md` and `AI_COORDINATION.md`,
and the executed `handoff-20260930-first-full-video-from-hyperframes-templates.md` row.

**Open risks.** The two-build cap (other sessions render heavily; load hit 500 on 09-30). The context clips carry the
re-fitted audio; any clip rendered before the EQ change is not reused. G09 keeps the wall stretch (a slide forces a jump there).

**Starter prompt (Claude Opus 5.5, effort high):**

Read `Handoffs/handoff-20260930-ro10-round1-dan-review.md`. Here is my reply to the RO-10 round 1 page: <paste>. Record the
decisions, apply them, build the full RO-10 film, gate it, run the independent review, deliver it and send me the review copy.
