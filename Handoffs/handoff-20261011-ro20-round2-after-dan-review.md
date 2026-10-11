# RO-20 "Why You Should Invest More In Your Health": round 2, after Dan's review of round 1

**CONTENT (LFC), organic long-form, 16:9. Sidebar name: `Invest In Your Health LFC R2`.**
Written 2026-10-11 by the round 1 session (Claude Opus 5.5). Round 1 is delivered and waiting on Dan. Do not start round 2
until Dan has replied to the round 1 page.

## Goal

Re-edit from scratch of the 8/3 kitchen roll C1511 (68:51 raw, 53:04 cut) on the round method. Round 1 sent Dan the look,
the sound, the opening, the AI frames, the finished first minute and every graphic and clip as stills. Round 2 applies his
answers, generates the approved AI motion, rebuilds the first minute, and only when nothing is pending renders the full film.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, then `.claude/skills/_shared/VIDEO-RULES.md` and `PRE-RENDER-APPROVAL.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md` (the recipe, the order, the traps). The working copy of the
   recipe is `/Volumes/Extreme/_edit_work/ro20/recipe/`.
3. Dan's reply to the round 1 page (in the chat that starts round 2). Record it word for word in
   `/Volumes/Extreme/_edit_work/ro20/round2-plan/decisions.json` before building anything.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/ro20/`. Round 1 page: `round1/index.html`, served at http://127.0.0.1:8862/
  (persistent service; refresh with `python3 .claude/skills/_shared/review_server.py 8862 /Volumes/Extreme/_edit_work/ro20/round1`).
- First minute (70.04 s): `round1/first-minute/DRAFT - RO-20 round 1 - first minute.mp4`, copy in
  `Videos to Review/Invest In Your Health LFC R1 - first minute.mp4` (delete it when Dan finalizes the video).
- Cut: `edl.json` (105 pieces), `shots.json` (382 shots), `words_out.json`, `cut_transcript.md`, `take_map_notes.md`,
  `picture_cues.md`. Generated from `takesel/takeplan.py` by `takesel/gen_pieces.py`. **The cut is applied: do not re-run
  the pause tightening on top of it.**
- Plan: `recipe/plan.py` + `recipe/plan_parts/p00..p07` (190 lower thirds, 177 clips, 203 sources, none used twice),
  resolved in `plan_resolved.json`. Lower third renders: `hf/renders/`, manifest `hf/manifest.json`.
- Voice: `voice/film_voice.wav` (whole film through the shared chain, voice 4 flags in `recipe/build.py` `VOICE4`).
- AI frames: `aiframes/O1, O2, A1, A2, A3, A4` start and end, prompts in `aiframes/prompts/`.
- Hashes of everything sent: `round1/round1-hashes.sha256`. Re-hash before touching anything.
- Stock: `stock/` (115 Pexels files; `stock/pexels_index.md` is the search index).

## Nothing is locked yet

Dan has not answered. What the first minute was built with, all open to his overrule:

| item | built with | his options on the page |
|---|---|---|
| Colour | D, bright and natural (`look_option.txt`, `grades.json`) | D, F, E |
| Voice | 4, warm with the light room pass, no gate | 4, 3, 1 |
| Opening | O1 the health vending machine (placeholder) | O1, O2, camera open |
| AI clips | A1 (0:20, lip synced), A2 (15:11), A3 (23:51), A4 (46:25), placeholders | all, some, none |
| Length | one film, 53:04, 31 chapters | one film, drop sections, two films |
| 38:18 | "you can't afford it" twice, as said | leave, cut one, subtitle differently |
| Bryan Johnson 49:33 | name lower third only | name, channel screen capture, nothing |
| The app on screen | NOT built: recommended a full-screen phone card at 19:29 and in the close | build, or lower thirds only |
| His own things | as built (he stays on camera) | he may send phone photos or clips |

## What round 2 does, in order

1. Record his answers (`decisions.json`: per item id, path, sha256, verdict, his words, scope, next action; `motion_authorized`
   list). Add a corpus entry for any rejection before fixing it.
2. Apply plan changes he names (edit the part file, `resolve_part.py`, then `resolve.py`; re-render only changed lower
   thirds with `from_plan.py --render --only`).
3. **AI motion, only for frame pairs he approved:** `recipe/gen_motion.py` (Veo 3.1 Fast, $0.10 a second: O1 8 s, A1 8 s,
   A2, A3, A4 6 s each) and the RO-06 lip sync on A1 only (`../ro06/lipsync.py`, about $0.65). Adapt `gen_motion.py`'s paths
   and its decisions file first (it still reads RO-07's round 3 layout). Read every take frame by frame, judge at speed.
4. If he said yes to the app card: build it from `B0544` (approved app tour screen) with `../ro06/phone_demo.py`'s shell,
   calorie tracking at 19:29 and workouts then nutrition in the close; show it to him as a still and a context clip.
5. Rebuild the first minute with the real clips, the quiet music bed (the RO-06 and RO-07 bed, `bed.py`, level measured on
   the audio gate's floor row), and show it.
6. Full film only when nothing is pending: `build.render_range(0, total)`, SRT (caption fixes listed in the part files'
   SPECIAL blocks; the drug-name rows of the gate are the known organic mismatch), chapters from the page's list, edit
   sheet, delivery gate, watch pass, one independent `ra-reviewer`. `roll_sidecar.py mark-used` for every source range.
   Register the new AI and stock clips in the clip library when Dan approves the film.
7. Later rounds list each change with exact timestamps in the new film (VIDEO-RULES, 2026-10-10).

## Status of checks, stated honestly

- Audio gate on the first minute: 12 of 13 rows pass. The tone row fails (mean error 1.36 dB against 1.2), expected with
  the fixed warm EQ, the same result as RO-07. Not tuned.
- Delivery gate, watch pass, independent review: NOT RUN (no finished film exists).
- Hair: the camera clipped the top of his hair for most of the roll. Both sizes keep the camera's top row. Reported to Dan.
- Round 1 stills were looked at by the editor on contact sheets (`round1/qc/`).
- Context clips ("Play it moving") were still rendering for the later parts when this was written: check `chain.log` for
  `CHAIN COMPLETE`; if it is missing, re-run the context loop at the end of `recipe/chain.sh`.

## Cost ledger

Generation: $0.00 (12 Codex pictures on the subscription). Gemini listening checks: under $0.50. Planned AI motion if all
five clips are approved: $4.05 (O1 0.80, A1 0.80 + 0.65, A2 to A4 0.60 each) of the $5.00 cap, leaving one 6 s retry.
Ask Dan before any spend that would pass $5.00.

## Queue and board

Edit queue: RO-20 is `delivered` (round 1 review). Board entry: "RO-20 - REVIEW". Set `in_progress` when round 2 starts.

## Recommended model and effort

Claude Opus 5.5, high. The work is editorial judgment on his notes plus a long build with several interacting parts.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261011-ro20-round2-after-dan-review.md`: round 2 of "Why You Should Invest More In Your Health" (LFC, content). My answers to the round 1 page are below. Record them, apply the changes, generate only the AI motion I approved, rebuild the first minute, and render the full film only when nothing is pending. Name this session "Invest In Your Health LFC R2".

[paste the reply box from http://127.0.0.1:8862/ here]
```
