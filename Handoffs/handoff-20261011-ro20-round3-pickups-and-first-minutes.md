# RO-20 / RO-20B / RO-20C "Invest In Your Health": round 3, pickups in, first minutes, then the three films

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll, edited together in one task. Sidebar name: `Invest In Your Health LFC R3`.**
Written 2026-10-11 by the round 2 session (Claude Opus 5.5). Replaces `handoff-20261011-ro20-round2-after-dan-review.md` (executed).

## Goal

Round 2 delivered the pickup scripts, the on-screen plan for each pickup, Dan's round 1 revisions, the three approved AI clips
and video 1's first minute. Round 3 starts when Dan has (a) recorded the four audio pickups and (b) answered the round 2 page.
It lays the pickups in, generates the two new job clips if he approves their frames, builds the first minute of videos 2 and 3
(and video 1's again only if he changes something), then, with nothing pending, the three full films.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md` (round 1 recipe, then the round 2 section: how the split is built, traps).
   Working recipe: `/Volumes/Extreme/_edit_work/ro20/recipe/` (the repo copy is a mirror of the files round 2 touched).
3. `/Volumes/Extreme/_edit_work/ro20/round2-plan/videos.json` (the three videos as ranges of the one cut timeline),
   `round2-plan/decisions.json` (Dan's round 1 words), `round2-plan/segs.round1.json` (the framing solve every shot is pinned to).
4. Round 2 page: http://127.0.0.1:8864/ (`round2/`, do not overwrite; build in `round3/` on a new port). Round 1 page: 8862.
5. Dan's reply to the round 2 page. Record it word for word in `round3-plan/decisions.json` before touching anything, then
   re-hash `round2/round2-hashes.sha256`.

## What Dan was asked (four decisions)

1. Frames J1 (boardroom job interview, replaces Ca02 under lower third Ga04): approve or change. Motion 8 s, $0.80.
2. Frames J2 (golf clubhouse partnership handshake, replaces Ca03): approve or change. Motion 4 s, $0.40.
3. Video 2's opening: on camera with roll take `sum1` (film 3014.45 to 3026.9 s), then pickup P2 from "In the last video"
   (recommended), or the whole opening as pickup audio over pictures.
4. Pickup scripts: record as written, or his own edits in the Google Doc
   (`1NI41W27Ipq3yukQ9HX-pLQYxbFEo849Na4Q95UzsGwA`; local copy `round2/pickups/pickups_doc.html`).

Pickup audio lands in `Media/longform-raw/ro20-pickups/` as P1 to P4, two takes each. If it is not there, stop and tell Dan in one line.

## Locked (do not reopen)

Colour D for both sizes; voice 4 (`build.VOICE4`); the chapters; every round 1 graphic and clip Dan did not flag; frames A1, A2, A3.
Round 2 additions are NOT locked until he answers: the finished motion of A1 (lip synced), A2, A3; the dating-app card (Cb11); the
diagram card (Cb12); the three-part card and the three-levels card (stills); the 24 B-roll grades; video 1's first minute.

## State of the build

- **Plan:** `recipe/plan_parts/` carries round 2 (O1, A4, Gb08, Gb09 removed; A1, A2, A3 point at `round2/motion/`; Ca02 and Ca03
  are frame placeholders J1, J2; Cb11 and Cb12 point at `round2/cards/`). `plan_resolved.json` and `hf/manifest.json` agree
  (188 lower thirds). Round 1's locked files are archived in `round1/locked/`. Framing: 499 of 499 shots equal the round 1 solve.
- **Motion:** `round2/motion/A1-t1.mp4` (8 s) and `A1-sync1.mp4` (lip synced slot), `A2-t1.mp4`, `A3-t1.mp4`; prompts beside them;
  `ledger.json`. `gen_motion20.py` refuses any clip not in `decisions.json` `motion_authorized`: add J1 and J2 there (with their
  frame hashes in the round's hash file) only after Dan approves them.
- **B-roll grades:** `round2/broll_grades.json`, read by `gfx.clip_vf(zoom, src)`; before and after strips in `round2/broll/`.
- **Cuts already applied in the plan, not yet in a render:** the two dropped sentences (539.87 to 541.507 s and 900.25 to 904.74 s
  of the cut timeline). They are range boundaries in `videos.json`; set the exact frames on the voice envelope. Do not re-tighten pauses.
- **Not done:** video 1's sign-off (the roll's other closing take, C1511 3974 to 4046 s, three internal restarts listed in
  `videos.json`) has no take-map pass, framing or cut-continuity check yet. The pickup segments are not built: `cards20.py` holds
  the three-part card (`series_card`) and the three-levels card (`levels_card`) as stills only; their motion is timed to the real audio.

## Order of work

1. Record Dan's reply; hashes. Pickups: pick the take, level and tone match to the film voice (gentle EQ match checked by ear and
   on the audio gate rows; the pickup room is not the kitchen), joins on the envelope.
2. If approved: J1 and J2 motion (frames to 1920x1080, Veo 3.1 Fast; J1 8 s take for a 7.4 s slot, J2 4 s take for 3.6 s), read
   every frame, wire them in, `resolve.py`, `preflight20.py`, check Ga04 over the new clip.
3. Build each pickup segment from `round2/pickups/pickups_doc.html` (the picture list per pickup), re-timed to the real words.
   No source twice inside one video; all of his own clips through their grade; AI clips labelled.
4. Video 1 sign-off: take-map pass, cut the three restarts by the take rule, framing, cut-continuity.
5. Round 3 page: only what is new. The first minute of videos 2 and 3 (copies to `Videos to Review/`), J1 and J2 motion in
   context, video 1's ending (P1 into the sign-off) in context. Then stop for Dan.
6. With nothing pending: the three full films (quiet music bed from RO-06 / RO-07 at the audio gate's floor row, SRT, chapters
   re-cut per video, edit sheet, delivery gate, watch pass, one independent `ra-reviewer` per film), `roll_sidecar.py mark-used`,
   queue `delivered` for RO-20, RO-20B, RO-20C.

## Checks, stated honestly

- Audio gate on video 1's round 2 first minute: 12 of 13 rows. The tone row fails (1.34 dB against 1.2) as in round 1 and on
  RO-07: voice 4 is a fixed warm EQ Dan chose by ear. Not tuned.
- A1 lip sync: made with the RO-06 method; I checked the mouth at seven closing sounds on stills and could not confirm every one
  closes on the frame (word times are only good to about 50 ms). It has not been judged at playback speed by anyone but Dan.
- A1, A2, A3: read frame by frame on contact sheets, no fault found. Not reviewed by an independent reviewer yet.
- Delivery gate, watch pass, independent review: not run (no finished film).
- The camera clipped the top of his hair for most of the roll (reported in round 1; unfixable in the edit).

## Cost ledger

Spent: $2.66 (Veo 3.1 Fast A1 $0.80, A2 $0.60, A3 $0.60; sync/lipsync-2-pro A1 $0.66). By video: video 1 $1.46, video 2
$0.60, video 3 $0.60. Planned: J1 $0.80 + J2 $0.40 (video 1, to $2.66). Images: 4 Codex frames on the subscription, $0.
Cap $5.00 per video; ask before any video passes it.

## Recommended model and effort

Claude Opus 5.5, high: pickup joins judged by ear and eye, a new take-map pass, and three long builds.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261011-ro20-round3-pickups-and-first-minutes.md`: round 3 of the three "Invest In Your Health" videos (LFC, content; RO-20, RO-20B, RO-20C in one task). My audio pickups P1 to P4 are in `Media/longform-raw/ro20-pickups/` and my answers to the round 2 page are below. Lay the pickups in, generate the job clips I approved, show me the first minute of videos 2 and 3 and only what else is new, then build the three full films only when nothing is pending. Name this session "Invest In Your Health LFC R3".

[paste the round 2 page reply here]
```
