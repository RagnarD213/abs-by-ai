# RO-12 "Top 5 Zepbound Tips": round 2, generate the two approved clips, then remake the full video

> **EXECUTED 2026-09-30.** Gate 2.4.0 committed (669352a). Nausea clip placed (library A0137); thigh-pinch clip NOT placed (three takes rejected, $5.55 spent, Dan on camera there). Remade, review round 4 SHIP, delivered. Outcome and open items: `claude edited long form content/09 - Top 5 Zepbound Tips/notes-RO12.md`.

Written 2026-09-30 by Claude (Opus 5.5), updated the same day with Dan's approvals. Recipe and locks:
`handoff-20260930-ro12-round1-dan-review.md`. Recommended model: **Claude Opus 5.5, medium** (two keyframe-locked clips and
a rebuild on a working recipe; the gate change in step 0 is small and corpus-checked).

## Dan's decisions (verbatim in `/Volumes/Extreme/_edit_work/ro12/round2-plan/decisions.json`)
> "The nausea clip looks good. The side pinch clip looks good. Modify the Handoffs document to generate those in the next round.
> Cut the burger-eating stock clip. Cut the 'empty your entire vial' ad lib. I realize that sometimes they are not emptying the
> entire vial if they're doing a non-standard dose, and organic videos should not have that rule. I plan to make a lot of organic
> videos where the entire topic of the video is Zepbound. Organic videos can say Zepbound, Tirzepatide, GLP-1, or any of those."

Reviewed master: `claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`,
sha256 `a4230be29b770b1b...`. Work dir `/Volumes/Extreme/_edit_work/ro12/`.

## Locked now (do not re-ask)
| Item | What | Status |
|---|---|---|
| R1 nausea clip | frames `rev1/N1-start.png` + `rev1/N1-end-b.png` | frames APPROVED, motion AUTHORIZED |
| R2 thigh pinch | frames `rev1/P3b-start.png` + `rev1/P3b-end.png` | frames APPROVED, motion AUTHORIZED |
| R3 burger stock | plan item `I15` | CUT, already applied in `recipe/plan.py` |
| R4 "empty the entire vial" ad-lib | source 314.9-322.3 and its insert `I06` | CUT, already applied in `recipe/edl.py` + `plan.py` |
| R5 organic may name the drug | speech and subtitles | STANDING RULE (VIDEO-RULES.md, memory `organic-drug-names-allowed`) |

R3 and R4 are applied; `build.py timeline` resolves (21 blocks, 551.4 s). Do not apply them again. Re-hash the four frames against
decisions.json before generating.

## Steps
0. **Gate change for R5** (so the remake is judged by the right rule). In `.claude/skills/_shared/deliver/formats.py`, for the organic
   formats (`longform`, and `short` if it carries the row): move `compliance:drug_names` to that format's `not_applicable` with the
   reason "Dan 2026-09-30: organic videos may name the drug; the brand-name ban is an ad rule", and remove "Zepbound" and "Ozempic"
   from `srt:shape` `banned_spellings` (keep "GOP", the Whisper mishearing). Ad formats keep the row. ⚠ At 2026-09-30 another session
   had 24 uncommitted lines in `formats.py`: check `git diff` first and do not commit or overwrite their lines; if they are still
   there, stage only your hunk (git hash-object / update-index, as the RO-12 commits did). Run
   `python3 .claude/skills/_shared/qc_corpus/run.py` (must pass), bump `GATE_VERSION` in `gate.py`, note the reason beside it.
1. **Generate motion** with Replicate `google/veo-3.1-fast` (`image` = start, `last_frame` = end, 1080p, 16:9, no audio):
   - R1, 4 s: he takes a bite of chicken, chews, sets the fork down, then presses his stomach and covers his mouth, turning away.
   - R2, 6 s: his right hand moves from resting on the thigh to pinching a fold on the outer thigh and holds the pinch; nothing
     else moves; no syringe, pen or needle ever appears.
   About $0.60 + $0.90. Check every frame for AI giveaways (hands, fingers merging into skin, fork or food morphing, face drift,
   logos reappearing on the shorts). One retry each fits the budget. Only if a take is uncertain, show Dan that clip in context
   before the remake; otherwise go straight to step 2.
2. **Place them** in `recipe/plan.py`:
   - R1 replaces `I03` (stock px10515019) at "The nausea, the fatigue, the days where you feel like garbage" (source 232.26 to
     e("feel like garbage")); `ai=True`, AI-GENERATED chip in a bottom corner clear of his face.
   - R2 is a new insert over "Inject into your thigh on the outer front part right around the middle. Not the inside of your leg,
     not down by your knee" (source 332.42 to about 338.9), ending before the G05 card; `ai=True`, chip clear of the hand.
   Check the insert-length rule (slot never longer than the clip) and the sliver rule; `build.py timeline`, then `stills I03 <R2 id>`.
3. **Remake**: `zsh recipe/rebuild_r2.sh` (about 60 minutes; check the two-build cap first). Negative-events rescan on the new file
   (the burger is gone; record it in `out/negative_events_scan.json` for the new sha), `finish.py`, gate, a fresh independent
   reviewer (copy `REVIEW-BRIEF-R3.md`; scope: the two new AI clips, the ad-lib join near 2:38, the removed burger at about 5:56,
   plus the full-film checks) including the watch-pass judge, then `recipe/deliver.sh`. Send Dan the new REVIEW 540p, set the queue
   to `delivered`, update the board entry.
4. Register both new clips in the clip library (`clip_library.py add ... --status used-final --used-in "RO-12"`). Put any new trap
   in `.claude/skills/longform-edit/reference/ro12/README.md`.

## Still open (Dan's call, one line each in the report)
Brand names in on-screen graphics on organic videos (not ruled; the round-1 graphics say "GLP-1" and "pen", keep them unless he says).

## Cost ledger (this video, $5 AI cap)
Frames: 13 nano-banana-pro 2K images, about $1.95. Motion planned: about $1.50 plus at most one retry each. Gemini: about $1.10
(listening) + $0.90 (YouTube search) + reviewers under $2.30, under the separate Gemini quality-review authorization.

## Starter prompt
> Read `Handoffs/handoff-20260930-ro12-round2-two-clips-then-full-remake.md`. Make the organic drug-name gate change, generate the
> two approved clips for RO-12 "Top 5 Zepbound Tips", place them, remake the full video, gate it, independent review, and send me
> the new review copy.
