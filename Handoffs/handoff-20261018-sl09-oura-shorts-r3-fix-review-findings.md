# Oura Ring Review SFL R3: fix the review findings, gate, page, deliver (SL-09)

**CONTENT: Shorts extracted from the long-form "My Honest Oura Ring Review After 1.5 Years" (Zeeshan Video 4). SFL.**
Task name: **`Oura Ring Review SFL R3`**. Model: **Opus 5.5, high**. Written 2026-10-18 by `Oura Ring Review SFL R2` (handed off
at 84% context with heavy work left). Same round-1 deliverable for Dan; nothing has been sent to him yet.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, the R2 handoff
`Handoffs/handoff-20261018-sl09-oura-shorts-r2-build-a-h-i-j-k.md` (Dan's picks, sources, rules; it may exist only in the main
project folder until that folder's pending commits reach GitHub), and the batch README
`.claude/skills/shorts/reference/softblue-sl09/README.md` (git copy of the work folder's scripts; how the build works, what it learned).

## Where everything is
- Work folder (run everything from here): `/Volumes/Extreme/_edit_work/sl09/round2/`. Data: `plans.py` (pieces, covers, bars, text,
  ZCUTS = Zeeshan's frame-exact cuts), renderer `batch.py`, scenes `scenes_hf.py`, `render_all.sh S..` (plan, gfx, render, waits for a
  build slot), `fix_tp.py S..` (keeps true peak <= -1.0 dBTP by AAC mode; run after every render), `post.py S..` (deliver.py copy:
  audio gate --verbatim, REVIEW 540p, delivered ASR, gate plan; then watch.py), `rungate.sh S` (delivery gate), `export_stills.py S..`
  (page stills + context clips), `decided.py` + `notes_r1.py` + `page_r1.py` (the page). Clips: `clips/` (candidates.json, CANDIDATES.md).
- Delivered (interim, NOT final): `Short-form video content/oura-short{1..5}_*.mp4` + `oura-ring-review REVIEW/` 540p copies and A/B
  clips; `oura-SHORTS.md` written. Order: 1 = A Train Harder, 2 = I Sleep Score, 3 = H Adrenaline, 4 = K Not Sleeping, 5 = J Oura Or WHOOP.
- Review page (built, interim, not sent): `review/index.html`, served by `review_server.py 8989 /Volumes/Extreme/_edit_work/sl09/round2/review`
  (http://127.0.0.1:8989/). Rebuild with `python3 decided.py && python3 page_r1.py`, then run the review_server command again.
- AI frames (frames only, for Dan's approval; $0): `aiframes/` J1 smart-ring opener for short 5 (gate PASS + frame-reviewer PASS,
  `gate.py --verify` exit 0), K1 "thumbs-up, nods off into his coffee" opener for short 4 (PASS + PASS, verify 0; lockstill used),
  **J2 ring + screenless band on one hand, palm turns over (generated, NOT yet gated or reviewed)** for short 5 at 0:13.8-0:20.6
  ("Oura Ring and WHOOP are my top two options... wrist-based or finger-based"), added because the reviewer said the plan asks to show
  the ring and the WHOOP. Page images in `review/ai/` (add J2 to `notes_r1.AI_ITEMS` once it passes).

## State of each short (latest independent review files: `build/<S>/ROUND-2-REVIEW.md`, `build/<S>/gate/logs/findings.json`)
- **A (short 1), review 2: DOES NOT SHIP.** D1 0:47.41-0:50.15 the groggy-man cover (`groggy`, `clips/A-open__7240841.mp4`) is
  cropped on the back of his head: move the window onto his face (source x about 100-1070 of 2560, so `fx` about 0.06). D2 the opener
  (`wake`, 3801360) cuts before the alarm-clock smash lands (about 1-2 s after the current cut): either run it to the hit and let key
  point G1 start on Dan after it, or start the clip later; keep Zeeshan's lower third covered to o6.7. Advisories worth fixing: crop pan
  0:20.4-0:23.5 on his near shot (steady window or a cover), caption "if you're doing the" 0.5 s late at 0:28, the deadlifter's head
  touching the top at 0:32.7 (portrait 12890962: set `fy`). Already fixed: head off-frame at 0:48 (now covered), curls end.
- **I (short 2): first review started 14:55 in the R2 task (agent writes `build/I/ROUND-2-REVIEW.md`).** Read it when it exists; if it
  is missing, launch a fresh `ra-reviewer` with the brief in step 2 below.
- **H (short 3), review 2: DOES NOT SHIP** (review 1's six fixes held). D1 0.00-0.60 the tunnel opener (31196473) starts on cars at
  a red light with a readable Honda "FREED" badge and plate: start about 0.7 s later. D2 10.177 and D3 20.020: two crop jumps INSIDE
  Zeeshan's own animated zooms (no cut in his source there): ZCUTS 27885 and 28180 are zoom transitions, not hard cuts, so the window
  must not change at those frames (keep one window through each zoom, or glide it like zeeshan-master `slideFrom`). D4 39.2-40.5 the
  key point covers the stock man's chin and mouth (`toss`, 8376628): end the bar earlier or move the clip's framing. D5 25.19-28.99 the
  deserted-highway clip (31720444) is flat grey after my gamma lift and 70% empty: grade it with true blacks or pick another empty-road
  clip; the light-streak clip after it goes nearly black at 30.6-31.8. Should-fix: captions vanishing at cuts 25.19, 34.40, 49.62 while
  words continue; B0333 opening on the man's chin; Dan entering off-centre at 34.40-34.65; delete the stale `... audio_gate 2.json`.
- **K (short 4), review 2: DOES NOT SHIP.** D1 0:19.59-0:25.46 the phone still reads as a good night ("Sleep Score 90 Optimal" is the
  biggest thing) and the highlight on "Restfulness: Fair" is a thin blue outline: from "the problem" (0:20.27) dim everything but that
  row and give it a bold warm call-out, or crop the screenshot to the contributors list so 90 Optimal leaves the frame (psolo code in
  `batch.py`, key `hl`; the screenshot is static 7:19.3-7:26.4, row box [0,433,320,474] in the crop rect [96,170,323,717]).
  D2 0:28.29-0:29.70 the "eat late at night" clip (30205992) shows groceries put away in daylight, and the key-point bar covers the
  hands: find someone eating or snacking at night (Pexels) with the action above y 1130, or library B0537 (eating on a bed, dark).
- **J (short 5), review 1: DOES NOT SHIP; fixed, not yet re-delivered.** The end showed Zeeshan's zoom into his outro: the piece now
  ends 1113.17 and the comparison scene (`hf/renders/J_compare.mov`, re-rendered to 25.6 s) runs to the end. The new render exists in
  `build/J/`; run `fix_tp.py J`, `post.py J`, then a fresh review. The "show the ring and the WHOOP" note is answered by the J1 and J2 AI
  frame ideas for Dan (motion only after his OK, on the Google Flow subscription, `flow-veo` agent).

## What remains, in order
1. Fix A, K (and H, I if their reviews find anything); re-render (`./render_all.sh S`), `python3 fix_tp.py S`, `python3 post.py S`
   (it waits for a build slot). Delete stale images in `build/<S>/gate/watch/` before each new watch pass (reviewers found leftovers).
2. A fresh `ra-reviewer` per changed short: brief = the delivered file, the source pieces (`plans.SEG`), the R2 handoff section, the
   standing rules, JOB 1 = follow `build/<S>/gate/watch/JUDGE_PROMPT.md` and write `findings.json`, JOB 2 = full-resolution audit, write
   `build/<S>/ROUND-2-REVIEW.md` ending `VERDICT: SHIP|DOES NOT SHIP`. Repeat until SHIP.
3. Gate J2 (`framecheck/gate.py J2_start.png J2_end.png --spec J2.spec.json`, write the spec first; lockstill if the desk drifts) and a
   fresh `frame-reviewer`; add it to the page if both pass.
4. For each SHIP short: `python3 "<skills>/_shared/deliver/watch.py" --judge build/<S>/gate/logs/watch_pass.json --findings
   build/<S>/gate/logs/findings.json --by "<reviewer>"`, `python3 deliver.py plan S`, then `./rungate.sh S` (never from a line that says
   gate.py). Gate must PASS at the current GATE_VERSION; never raise a bound. A row that genuinely does not apply goes in
   `build/<S>/gate/declare.json` with its reason (see the softblue-sl07 README for the plan keys).
5. `python3 export_stills.py A I H K J` (stills + context clips from the final REVIEW copies), update `decided.py` (its results line reads
   the files) and `notes_r1.py` (K is under 45 s: no VLC copy, page only), `python3 decided.py && python3 page_r1.py`, re-run the
   review_server command, check `curl -r 0-99` gives 206, open it in the browser pane muted and seek one video.
6. Copy the four shorts of 45 s or more to `Videos to Review/` as `Oura Ring Review SFL R3 - short N - <title>.mp4`,
   `open "Videos to Review"`.
7. `python3 scripts/edit-queue/queue.py set SL-09 delivered --by Claude`, mirror to the Edit Queue artifact (ArtifactData set, pin
   if_version, `queue.py mark-synced SL-09`), board entry `SL-09` to REVIEW with the port, `scripts/board-check.sh`.
8. Push: re-copy changed scripts into `.claude/skills/shorts/reference/softblue-sl09/` and push. Main folder:
   `scripts/git/safe-push.sh` for the board, jobs.json and 00-MASTER (it stopped earlier on live files from other sessions; the R2
   board edit is local commit a2492ca there).
9. Message Dan: the page link, the VLC file names, the AI decisions (J1, K1, J2), one line that only short 1 has a calendar slot
   (Fri Nov 13) and the setup task places the rest. No covers, no upload.

## Locks and decisions so far
- Dan's picks and order from the R2 handoff. No pickups. Zeeshan's picture and mix verbatim; audio gate PASS on all five delivered
  files (true peak kept by AAC mode, never a level change). Captions print what he says ("in your bedtime", "shit" stays).
- Rejected clips and why: see `decided.py`. Cost so far **$0** (Codex frames on the subscription, Pexels and library stock).
- Dan has seen nothing of this round yet.

## Starter prompt
> Read `Handoffs/handoff-20261018-sl09-oura-shorts-r3-fix-review-findings.md` and finish it: fix the independent reviewers' findings on
> my five Oura Ring Review shorts, re-render, re-review until each ships, run the gates, finish the review page and send me the review
> copies, update the master list. Name this task "Oura Ring Review SFL R3".
