# RA-07 "Fire Your Trainer!": round 6 (trim gym closed, new "pulls out his phone" clip for out of order)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R6`.
Written 2026-10-16 (Claude Sonnet 5.5) after Dan reviewed the round 5 page (http://127.0.0.1:8856/). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Round 5 recipe and lessons: `.claude/skills/ad-edit/reference/ra07/round5/` and "RA-07 round 5 lessons" in `.claude/skills/ad-edit/SKILL.md` (read both, then the round 4 lessons above them).
Work folder: `/Volumes/Extreme/_edit_work/ra07/` (round 5 outputs in `round5/`). Delivered round 5 file: `round5/deliver/fire your trainer | claude | 9x16 | RA-07.mp4` (sha256 starts 151fac2e). The round 5 independent review said SHIP; Dan's notes below override it.

## Dan's words (verbatim, 2026-10-16)

> "At 38 seconds, when he's looking at the closed gym, he's looking for about a second too long. I want you to cut that clip off about a second sooner so it doesn't look unnatural with him standing around in front of the gym too long, looking like AI slop. At 41 seconds as well, what he's doing looks unnatural. He's walking, and then he turns backwards as he's walking, but his feet don't move. Doesn't make any sense. I want this to instead be a clip of him seeing the machine is out of order, standing next to it, and then pulling out his phone."

Everything he did not mention is unchanged (he approved nothing else in words this turn; treat it as unchanged): the first 30.1 s (frame-identical to round 2), the broken-arm clip A1 (36.47-38.54), the hack squat H2, "back next week" I5, the cards, captions, CTA, and the audio (`round3/mix_bass_r3.wav`, never touch).

## What round 6 changes

| slot (film time) | now (round 5) | round 6 |
|---|---|---|
| A1 36.47-38.54 | broken-arm clip, 62 frames | unchanged |
| **G1 38.54-39.81 (38 f)** | gym closed: take `round5/motion/G1_v1.mp4` source frames 59-96 (1.25x), he stops, opens both palms, then stands and looks about 0.8 s too long | **trim to the arrival-and-shrug beat only, about 0.45 s** (source frames 59-72, 14 film frames, ends about 39.01). The freed second goes to M1 (below). |
| **M1 39.81-41.01 (36 f)** | home curls, library A0039 from 1.0 s | starts about 39.01 (on "...make it to the gym"), runs to 41.01: 60 film frames, about 2.0 s, same in-point 1.0 s. A0039 is 5 s long, so it plays at its own rate with no hold. |
| **O1 41.01-42.41 (42 f)** | leg press, head turn, feet not moving | **NEW clip, new frames and motion:** he is already standing beside the out-of-order leg press, looks at the OUT OF ORDER sign, then reaches into his pocket and pulls out his phone. See below. |
| H2 42.41-44.01, I5 44.01-47.01 | unchanged | unchanged |

G1 goes below the 1.2 s flash floor on purpose: that is Dan's order ("about a second sooner"), so his words override the floor for this slot. The editor must still judge it: the gesture itself is only about 0.4 s of motion (frame differences 55-70 are the arm swing, then it settles), so cutting at the end of the arm swing keeps motion and removes the standing-around. If, played back, G1 reads as a flash, say so in one line on the page and offer Dan the alternative of dropping G1 and letting A1 into M1 (his call). Do not re-add the standing part.

## The new O1 clip (needs frames first, Dan sees them before any motion)

Concept is Dan's, so no ideas round is needed. It still needs the approved-frames step (VIDEO-RULES: start and end frames, gate, fresh reviewer, Dan's yes, then motion):

1. **Frames (Codex subscription, `codex-image.sh --model gpt-6.1-sol --effort high`):** START derived from the approved leg press frames so the room, camera and man are the same (`round4/frames/LP-start_v1.png` and `LP-end_v4b.png` are the references; pass the START to `--image` with "keep the camera, framing, machine, sign, room and man exactly"). **START:** he stands beside the plate-loaded leg press, feet planted, the OUT OF ORDER sign on the backrest, head turned toward the sign, hands empty at his sides, white towel over his shoulder as before. **END:** same camera, same feet, hips, towel and room; his right hand holds a plain black phone in front of his chest, his head tipped down toward it, a thoughtful look. The screen faces him, so no screen content is visible from this angle (this avoids generated UI text). No logo on the phone, exactly five fingers on the visible hand, one phone only. The shorts need a visible side pocket for the pull-out to make sense.
2. **Frame spec + gate + fresh `frame-reviewer`** for the pair before Dan sees it (`_shared/framecheck/README.md`; `props` block with the phone `held_by: right`, the pocket box as the place it comes from; `person.anchored` hip and nose; same feet in START and END). Expect a retake or two. The prop is the risk.
3. **Stop for Dan's yes on the frames** (show START and END beside the 1.4 s slot and the rest of the film). Then motion (stage 2).

Traps for this clip, all from this job:
- **The phone pull-out already failed once on A0179:** a smeared phone out of the pocket (that window of the library clip was cut around). Write the pull in short steps in the prompt ("his right hand goes into his right shorts pocket, comes out holding a phone, lifts it in front of his chest, he looks down at it"), keep the hand small and unobstructed, and read every frame of the hand with the motion gate and a reviewer: hand fingers, phone shape (rigid slab), nothing appears or vanishes in place.
- **Standing is fine: his feet do not need to move, and that is what Dan wants** (his complaint was a walk or turn with static feet). Do not ask for any walking. Say "his feet stay planted" in the prompt and put sliding feet in the negative prompt.
- **The Kling take's first second often holds a still pose, then the action;** pick the window by tracking, not by the 4 s start. The slot is 42 film frames: at 24 fps source played one source frame per film frame (1.25x, `setpts=N/(30000/1001)/TB`, lesson 2 of round 5) the window needs 42 source frames, about 1.75 s, containing the look at the sign, the pull and the phone raised. If the action in the take is slower, a 5 s take is allowed; never slow below 0.85x.
- Kling gives a baked cut now and then and sometimes an unplanned second camera move: check frame differences for a spike over the whole take and the first and last second frame by frame.
- Keep the same man and machine as the approved leg press frames (black plate-loaded press, yellow sign). The round 5 reviewer noted H2's machine is silver and its towel on the other shoulder; Dan did not object and it reads as moving to another machine, so do not spend on it.

## Round 6 order of work

**Stage 1 (this task, no AI motion spent):**
1. Rename the task `Fire Your Trainer AD R6`. Check AI_COORDINATION.md, `git status`, and free space on `/Volumes/Extreme` (it hit 100% on 2026-10-16; a cleanup task was flagged; delete only regenerable check-frame dumps and say so).
2. **G1 trim:** `s75r5_clips.py` G1 `frames` 14 (source frames 59-72; run clipcheck on `59:72` and a fresh frame reviewer for that exact range, since stamps are per range), `s70r5_plan.py` `t_curls` to about 39.01 on a frame boundary, M1 60 frames. Re-plan, re-conform G1 and M1 (the M1 chip stays at its fixed spot), keep every other slot's frames. Round 4's holds in `round4/seg/` are reused; the first 30 s must stay md5-identical (`chain_all.sh` checks it).
3. **O1 frames** as above through gate and reviewer. Build the working film with O1 as the labelled placeholder (band on the floor, y about 1080-1280, not over the sign or machine, as round 4 lesson 5 says) so Dan sees the G1 trim in the film. Use `s86r5_assemble.py` with `PENDING = {"O1"}` and a `PLACE` entry for the new START frame.
4. Review page on port 8856 (reuse; `review_server.py 8856 --remove` then re-add pointing at the new folder, as round 5 did): the whole film, the changed run, G1 in context, the O1 frames with the slot, and the timestamped revision list. **Review-panel testing is silent: mute the video before any test and leave it paused.** Ask Dan once for a yes on the O1 frames.

**Stage 2 (after Dan says yes to the frames; a separate task or the same one):**
5. Motion for O1 (`round5/gen_motion5.py` is the model: add a job with the new START and END; Kling v3 standard 4 or 5 s, `require_pass()`), each take through `clipcheck.py TAKE --spec ... --frames A:B` (spec boxes in the take's 720x1280 pixels, scaled from the frame spec as `round5/clipcheck/*.spec.json` did) and a fresh `frame-reviewer` with the three sense questions, then `--verify`. A failing take is retaken or cut down; if nothing passes inside the budget, put him on camera in that slot and say so in one line.
6. Rebuild the whole 9:16 with `PENDING = set()`, then the gates on the exact file as round 5 did: `chain_all.sh` (queue and wait: two-build cap), mux with `round3/mix_bass_r3.wav`, `audio_gate.py` with `--ab` and `--untreated mix_bass.wav.audio_untreated.json`, `s92r5_chips.py`, `s92r5b_k1push.py`, `s88r5_checks.py`, the negative-imagery sheet by eye and `negative_scan_9x16.json`, `s93r5_gateplan.py` (it names the clips; A1 has two chips; G1, M1 and O1 chips come from `round5/clips/*_chip.png`), `deliver/watch.py` plus a fresh judge subagent and `--judge`, then `deliver/gate.py --format ad9x16`, then a fresh `ra-reviewer`. Known and accepted, report plainly and do not tune: the audio `tone` row (fixed bass lift) and the caption-timing miss on "20" at 21.3 s (inside the approved first 30 s; identical to round 3 and 5).
7. Deliver: `Claude Ad Videos/fire your trainer - RA-07/` (replace the main file, stamps, A/B and 540p), `Videos to Review/Fire Your Trainer AD R6 - whole 9x16.mp4` (replace the R5 copy), the page, edit queue `delivered` (`scripts/edit-queue/queue.py set RA-07 delivered`, then the `ArtifactData` set with `if_version`, then `mark-synced`), board entry, and the later-round revision list in chat with exact timestamps. Prove "everything else unchanged" by pixel difference outside the changed slots (round 5 lesson 4), not framemd5.
8. **The 16:9 comes only after Dan approves the 9:16.** Do not start it in this round.

## Budget

Dan set **$20** for RA-07 AI clips. **$12.00 spent** (round 5 spent $2.00: one Kling take each for G1 and O1). **$8.00 left.** The new O1 needs about $1 a take; expect two to four takes. Frames are free (Codex subscription). At the cap, ask for more first and alone, with the number, and never ship a faulty clip (VIDEO-RULES, 2026-10-13).

## Facts to carry

- Round 5 plan slots (`beats_r5.json`, frames at 29.97): G1 frames 1155-1192, M1 1193-1228, O1 1229-1270. G1 trimmed to 14 frames ends at frame 1168; M1 then runs 1169-1228.
- G1 take `round5/motion/G1_v1.mp4` (97 frames, 24 fps, 720x1280): frames 0-58 he walks in place (treadmill, never use), arm swing frames 59-70, settled by 72. Its round 5 stamp is for frames 59-96 only.
- The O1_v1 take (`round5/motion/O1_v1.mp4`) is retired by this round: he walks in place and then turns his head with static feet. Keep the files, do not reuse.
- Chips: AI-GENERATED, one style, placed by person mask away from face and abs and clear of the caption band; check the new O1 chip against the phone and the sign.
- No em dashes anywhere; title-case graphics; no AbsByAI.com mark at the end; never publish the ad organically (upload and setup is a separate `/ad-setup` task after Dan finalizes).
- Still open from round 3, not in this round: the hack squat lift and the same-sheet clip (I2, Dan on camera 31.63-34.30). Say so in the delivery note; Dan did not answer when asked in round 5.

## Recommended model

Claude Opus 5.5, high effort (editorial and frame work). Frames by Codex GPT-6.1 Sol, high, via `codex-image.sh`. Escalate to Fable 5.1 only for a frame pair or take Opus has failed twice.

## Starter prompt (stage 1)

> AD. Rename this task `Fire Your Trainer AD R6`. Read `Handoffs/handoff-20261016-ra07-fire-your-trainer-round6-trim-and-phone.md` and run stage 1 of round 6 of RA-07 "Fire Your Trainer!" with /ad-edit: trim the gym-closed clip to its arrival-and-shrug beat (about a second shorter) and let the home curls fill the gap, and make start and end frames for a new leg-press clip where he sees the OUT OF ORDER sign, stands next to the machine and pulls out his phone (Codex subscription for the images, frame gate and a fresh reviewer first). Build the whole 9:16 with the new clip as a labelled placeholder so I can see the trim, send me the page with a timestamped list of what changed, and stop for my yes on the frames. AI clip budget: $20 total, $12 already spent.


## Stage 1 done (2026-10-17, Claude Opus 5.5)

- Page :8856 (`round6/page`), VLC copy `Videos to Review/Fire Your Trainer AD R6 - whole 9x16 (phone placeholder).mp4`. Plan `beats_r6.json`; G1 = G1_v1 frames 59-72 (clipcheck + reviewer PASS), first 30 s md5-identical, outside the slots MSE max 0.31.
- **M1 changed:** A0039 FAILED its fresh review on the 2.0 s window (melting hand). M1 is now library **A0080** frames 127-186 (1.25x, crop inside its letterbox, chip at (710,520)); clipcheck + third fresh reviewer PASS. Its chip is fixed in `s75r6_clips.py`; the stage 2 gate plan must declare it.
- **O1 frames APPROVED by Dan, 2026-10-17:** "Phone frames approved, go ahead with stage 2. Handoff for new task" (recorded in `round6-plan/decisions.json`; PH-start.png sha256 eecfbcf6..., PH-end_v1a.png 7ef1f9b0...). Stage 2 is next, in a new task. Earlier note: `round6/frames/PH-start.png` and `PH-end_v1a.png`, spec `PH.spec.json`, gate + reviewer PASS (`gate.py --verify` exits 0). Record his words in `round6-plan/decisions.json` before motion.
- Stage 2 scripts: start from `s70r6_plan.py` (set `PENDING = set()`), `s75r6_clips.py` (add an O1 entry for the new take), `s86r6_assemble.py` (PENDING empty, SRC O1 to round6/clips). $12 of $20 still spent; nothing paid this stage.

## Starter prompt (stage 2, only after Dan says yes to the frames)

> AD. Name this task `Fire Your Trainer AD R6`. Read `Handoffs/handoff-20261016-ra07-fire-your-trainer-round6-trim-and-phone.md` and run stage 2: Dan approved the new leg-press phone frames (the pair is in `/Volumes/Extreme/_edit_work/ra07/round6/frames/`, his words in `round6-plan/decisions.json`). Make the motion (each take through clipcheck and a fresh reviewer first), build the whole 9:16 with it in, run every gate, the watch pass and the independent review, and send me the page with a timestamped list of what changed. AI clip budget: $20 total, $12 already spent.


## Stage 2 done (2026-10-17, Claude Opus 5.5)

- **O1 finished:** take `round6/motion/O1L_v2.mp4` (Kling v3 standard 5 s, `gen_motion6.py O1L v2`) source frames 36-77 at 1.25x; clipcheck PASS + fresh reviewer PASS (note: phone a soft blur for about 0.3 s at film 41.7-42.0 during the arm swing). O1_v1 (4 s) rejected: phone appears in his hand without the hand entering the pocket. Spend this stage $2.25; **total $14.25 of $20**.
- **M1 replaced again:** the independent `ra-reviewer` failed A0080 (power rack reads as a gym; a different man from G1; DOES NOT SHIP). No library clip fits. New AI frames of G1's man curling in his living room: `round6/frames_m1/HC-start.png` + `HC-end.png` (= HC-end_v2a, head held still), spec `HC.spec.json`, frame gate + fresh reviewer PASS (`gate.py --verify` exits 0). **Waiting on Dan's yes** on page :8856.
- Full build with A0080 (`round6/deliver/...RA-07.mp4`, sha 6f6ea724, not for Dan) gated: delivery gate 37/39 (known tone + "20" caption rows), watch pass + fresh judge 0 defects, pixel diff outside 38.5-42.4 s max 0.30, first 30 s md5-identical. Its plan/chip/check scripts are the round 6 copies (`s88r6`, `s92r6`, `s92r6b`, `s93r6`, `chain_s2.sh`).
- Review film: M1 as a labelled placeholder (`s86r6_assemble.py` PENDING {"M1"}, `WORK=round6/work_ph`, `chain_ph.sh`), page `s87r6b_page.py` on :8856, VLC copy `Videos to Review/Fire Your Trainer AD R6 - whole 9x16 (home curls placeholder).mp4`. Dan is also asked: keep the 0.47 s gym-closed clip or drop it (A1 into M1).

## Stage 3 (after Dan's yes on the home-curls frames)

1. `python3 .claude/skills/ad-edit/reference/ra07/round6/gen_motion6.py M1 v1` (job already written: 4 s, eyes follow the weight, head still). Window: 60 source frames at 1.25x containing one full curl up; if the take's curl is slower use a 5 s take (add `M1L`).
2. Spec for the take from `HC.spec.json` scaled 720/941 into the window's first frame; `clipcheck.py --frames A:B`, fresh `frame-reviewer` with the three sense questions, `--verify`.
3. `s75r6_clips.py`: replace the M1 entry (file round6/motion/M1_v1.mp4, start_frame, retime=True, no `pre`, chip placed by person mask away from face and the curling dumbbell, clear of captions); re-run `s75r6_clips.py M1`. `s86r6_assemble.py`: PENDING = set(); `s70r6_plan.py` M1 "what" text. Then `round6/chain_s2.sh` (writes round6/work), `s93r6_gateplan.py`, watch + fresh judge, `gate.py --format ad9x16 --plan round6/plan.json`, fresh `ra-reviewer`, Dan's page with the revision list. Apply Dan's G1 answer if he drops it (then A1 runs into M1: re-plan in s70r6).
4. Deliver per step 7 above.

## Starter prompt (stage 3)

> AD. Name this task `Fire Your Trainer AD R6`. Read `Handoffs/handoff-20261016-ra07-fire-your-trainer-round6-trim-and-phone.md` ("Stage 2 done" and "Stage 3") and run stage 3: I approved the home-curls frames (`/Volumes/Extreme/_edit_work/ra07/round6/frames_m1/`) [and my gym-closed answer: keep / drop]. Make the motion (clipcheck and a fresh reviewer first), build the whole 9:16 with it in, run every gate, the watch pass and the independent review, and send me the page with a timestamped list of what changed. AI clip budget: $20 total, $14.25 already spent.

## Stage 3 done (2026-10-17, Claude Opus 5.5)

Dan: "Everything is approved. Let's edit the full film." M1 = take `M1L_v2` frames 48-107 (Kling, submitted on Replicate seconds before Dan moved all editing AI clips to the Google Veo subscription; any retake now goes through Flow), clipcheck + fresh reviewer PASS, chip fixed on the rug at (718, 1290). Delivered `Claude Ad Videos/fire your trainer - RA-07/` (sha ca75555c), gate 37/39 (tone, "20" caption), watch judge 0 defects, ra-reviewer SHIP (`round6/deliver/ROUND-6-REVIEW.md`), page :8856 (`s87r6c_page.py`), VLC `Videos to Review/Fire Your Trainer AD R6 - whole 9x16.mp4`, edit queue `delivered`. $16.50 of $20 spent.

Next after Dan's yes: the 16:9. Raise first: the real-photo chip at 15.7 s reads "Real picture of me. Not AI-generated."; the 2026-10-17 rule wording is "Real Photo Of Me, Not AI-Generated" (inside the approved first 30 s; Dan's call). Still open from round 3: the hack squat lift and the same-sheet clip.
