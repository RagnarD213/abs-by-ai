# framecheck: measure AI start/end frames and motion takes for body and physics faults before Dan sees them

Built 2026-10-14 on RA-04's leg press clip, after Dan rejected a frame pair where the man pushed at about 90 degrees to
the machine ("No human body works like that... You never should have shown me this"). Every AI clip's START and END
frames go through the gate and then a fresh independent reviewer, before any review page shows them.

## The routine for every AI frame pair (Claude and Codex, every skill)

1. **Write the frame spec before generating the END** (`spec.json`, format below), from the START frame: what moves and
   along what, what must stay still, what each hand holds, the contact points. Template: `spec.example.json`.
2. **Gate the pair:** `python3 .claude/skills/_shared/framecheck/gate.py START END --spec spec.json`. It prints a PASS or
   FAIL row per check with numbers, writes an evidence sheet (`framecheck/<END>.framecheck.jpg` next to END: skeletons,
   guide lines, part boxes green or red, flagged regions in magenta, hand crops, zoomed START/END crops of every failed
   part) and stamps `END.framecheck.json` with both sha256s. Exit 0 PASS, 1 FAIL. A FAIL is regenerated or rebuilt, never
   shown to Dan.
3. **A fresh reviewer per pair:** the `frame-reviewer` agent (`.claude/agents/frame-reviewer.md`, Opus 5.5 high) with
   only START, END, the spec and the evidence. It measures items A to I, writes `framecheck/<END>.review.md` ending in
   `VERDICT: PASS|FAIL`, and records it: `gate.py START END --review REVIEW.md`. (In a session started before the agent
   file existed, run a general-purpose Opus agent told to read that file first.)
4. **Review pages and motion generation refuse a pair without both:** `gate.py START END --verify` (exit 0 only if the gate
   PASSed at the current `GATE_VERSION`, a reviewer PASSed, and neither frame nor the spec changed since), or in Python
   `sys.path.insert(0, ".claude/skills/_shared/framecheck"); from gate import require_pass; require_pass(START, END)`.
   Any edit to a frame clears both; re-gate and re-review.

## The frame spec (`spec.json`)

Every box is `[x0, y0, x1, y1]` and every line `[x1, y1, x2, y2]` in START pixels. Only `intent` is required; each block
adds checks. Bounds default to the values in `gate.py` `DEFAULTS` (each one calibrated on RA-04, see the comments there);
override per shot under `"bounds"`.

| key | what it declares | what the gate checks |
|---|---|---|
| `intent` | the action in plain words, START and END | nothing; the reviewer reads it |
| `person.guide` | the line the body works along (a machine's rail), `max_deg` | hip-to-ankle line vs the guide in both frames (default 10 degrees) |
| `person.anchored` | joints that stay put (`hip`, `shoulder` = camera-near side, `nose`) | drift under 15 % of the torso |
| `person.reach` | true for a push or a straightening limb | bone lengths START vs END within 8 %; END hip-to-ankle equals what START's bones allow at END's knee angle |
| `rigid[]` | a group that moves as one piece: `parts` (small high-texture boxes ON the part: bolts, a plate rim, a horn tip, a crisp corner), `guide`, `move_px` [min, max], `extent` (a box around the whole group) | 2+ parts found (score 0.85); the group's move is their median; strong parts agree within 10 px; travel within 5 degrees of the guide; every part matches and stays sharp (0.72) where that move puts it |
| `contacts[]` | a part that rides a group (`box`, `rides`): a shoe on a footplate, a hand on a handle | moves with the group within 12 px |
| `still{}` | named boxes that must not move: machine frame, base, a background rack | moved under 3 px |
| `props[]` | a held object: `box`, `held_by` (`right`/`left`) | in that hand in START; when the hand moves, no half of the START box stays unchanged (a leftover) |
| `may_change{}` | named boxes allowed to change (a TV screen, a moving background person) | excluded from the static check |
| (always) | | static: every pixel outside the person, the groups (moved or uncovered), contacts, props and `may_change` is unchanged; changed regions reported as boxes |

Box choice decides the result (README rule 3 below). Mark boxes on a gridded 2x crop of START, keep them on the part
itself, and avoid flat colour and plain surfaces such as a pillar (a template on a plain vertical surface slides along it).
The gate catches only what the spec declares and cannot count fingers or judge expressions: that is the reviewer's job.

## Proof (2026-10-14): `proof/ra04/run_proof.sh`

| pair | Dan / reviewer verdict | gate | rows that failed, matching the reviewer's fault |
|---|---|---|---|
| F4c_a / F5c_b | rejected by Dan: upright, pushing off the rails | FAIL | leg line 37 and 23 degrees off the rail; legs +20 %; sled off its guide; frame and background moved |
| F4d_b / F5e_b | review 1 FAIL: machine top stretched, sled 7 degrees off the rail | FAIL | frame top moved 46 px, static region at the top of the machine; sled travel +7.3 degrees; legs +11 to +14 % |
| F4h / F5h2 | review FAIL: legs 24 % longer, floating half phone | FAIL | thigh +23 %, shin +27 %, reach +25 %; top half of the phone's START box 98 % unchanged |
| F4h / F5j | review FAIL: near foot slid down the plate, phantom toe, pillar patch | FAIL | near shoe slipped 24 px against the sled. Not caught by the gate: the phantom toe and the pillar patch, both pieces of START moved exactly with the sled (the patch matches START's sled pixels to 0.5 grey levels), so they read as sled; the reviewer finds those |
| F4h / F5m | review FAIL: smeared, stair-stepped footplate | FAIL | footplate corners sharpness 0.29 and 0.56 of START where the sled's move puts them |
| F4h / F5p | review PASS, Dan approved | PASS | every row |

Reviewer proof: the `frame-reviewer` instructions, run fresh on F4h/F5m and F4h/F5p with only the pictures, the spec and the
evidence, failed F5m on the smeared footplate (its own sharpness 0.04 and 0.12 of START) and passed F5p (two optional flaws), and
recorded both in the stamps. `gate.py --verify` now passes F4h/F5p and refuses F4h/F5m.

Robustness: every box in the F4h spec shifted by 4 to 5 px in eight directions: F5p passed all nine runs and the three
rejected F4h pairs failed all nine, each on its named fault. The first version, which trusted each part's own free
search, failed the approved F5p in four of eight.

## Tools

| tool | what it measures | the fault it catches |
|---|---|---|
| `gate.py START END --spec spec.json` | everything below, driven by the spec, with a stamp | all of the below, in one command |
| `posecheck.py IMG [--rail x1,y1,x2,y2] [--out overlay.jpg] [--json]` | MediaPipe pose: torso, thigh and shin angles and lengths, hip and knee angles, the leg line against a machine's guide line | a push at the wrong angle to the body or machine; impossible joints; limbs that grow or shrink between START and END (compare the lengths) |
| `rigid.py START END --part name:box ... --still name:box ... [--guide line]` | local template tracking: each part's displacement, the spread between parts, travel angle against the guide, drift of things that should stand still | a sled or prop that does not move as one piece, moves off its rails, or a frame or background that stretches |
| `lockstill.py START END OUT --box ...` | copies every pixel outside the person and the listed moving boxes from START into END | image-model drift of static machinery and background |
| `clipcheck.py TAKE --spec spec.json [--frames A:B]` | point tracks through a motion take (grid forward and backward, the spec's parts on every frame), with a stamp | things that vanish in place or come from nowhere, parts off their guide, slipping contacts, drifting still parts, a camera that moves when it should be locked ("Motion takes" below) |
| `cotracker_mps.py`, `mps_ops.py` | the tracker behind clipcheck, and the Apple-GPU replacements for ops CoTracker needs | |

## Motion takes: `clipcheck.py` (2026-10-14)

Built on RO-08's donut take, which Dan rejected on 2026-10-13: *"all the donuts just disappear, vaporize, and go nowhere... things
that look like AI slop like this get caught in quality control and don't make it to my review."* Every AI motion take goes through
it, and then through a fresh `frame-reviewer`, before any review page shows it.

1. **The spec:** the frame pair's spec (above) serves the take too; frame 0 of the take is START. Add `"camera": "locked"` when the
   prompt asks for a locked-off camera, and declare under `may_change` what the intent says opens or changes (a fridge door, a
   furnace door and its fire, a wall clock whose hands run, a TV). **Never add a `may_change` box because a check failed:** that is
   how a vanish gets waved through. A prop that is meant to go (food eaten) gets `"may_leave": true`.
2. **Run it:** `python3 .claude/skills/_shared/framecheck/clipcheck.py TAKE.mp4 --spec spec.json [--frames A:B]`. `--frames` checks
   only the part an edit uses (both ends included; the spec's boxes are then in frame A's pixels). Exit 0 PASS, 1 FAIL. It writes
   `clipcheck/<take>.fA-B.clipcheck.jpg` next to the take (the first and last frame with every point lost in place in magenta,
   every point that came from nowhere in orange, event boxes in red, then a strip of crops across each event), a folder of frames
   every 0.25 s for the reviewer (`clipcheck/<take>.fA-B.frames/`) and the stamp `TAKE[.fA-B].clipcheck.json`. A FAIL is
   regenerated, cut around (a part of the take that passes, checked with `--frames`), or dropped; never shown to Dan.
3. **A fresh reviewer:** `frame-reviewer` with the take, the range, the spec and the evidence. It answers A to I plus the three
   sense questions on the sampled frames and records its verdict: `clipcheck.py TAKE [--frames A:B] --review REVIEW.md`.
4. **Pages refuse a take without both:** `clipcheck.py TAKE [--frames A:B] --verify`, or in Python
   `from clipcheck import require_pass; require_pass(TAKE, frames=(A, B))`.

How it works. CoTracker3 (Meta, 2025) tracks a 40 px grid of points (1,296 at 1080p, not on people, not in `may_change` boxes)
forward from the first frame, and a second grid backward from the last frame. A point **vanished** when it is never visible again
(at least 0.4 s before the end), had not moved against what its neighbours say (a local fit, so a pan or zoom is followed), its spot
is still in the picture, no person and no moving thing covers the spot at the end, and the spot looks different at the end than at
the start (patch correlation under 0.5, scaled for zoom). Traced backward, the same test finds what **came from nowhere**. Six or
more neighbouring points make an event. When the camera moves (zoom past 15 % or a shift past 8 % of the width), the test runs in
overlapping windows of 1 to 3 s instead, because a first-vs-last comparison needs the two ends to look alike. The spec's `rigid`,
`contacts`, `still` and `props` boxes get 16 points each and are checked on every sampled frame (parts together and on their guide,
riders not slipping, still parts not moving against the camera, props not lost away from a person). A take is sampled to at most 64
frames (a 6 s take every 3rd frame, 8 per second). About 1 to 2 minutes per take on the M2 Pro when nothing else is rendering.

### Proof (2026-10-14): `proof/ro08/run_proof.sh` and `proof/ro08/run_grid_shift.sh`

| take | Dan's verdict | clipcheck | what it found |
|---|---|---|---|
| A5 donuts, whole take | rejected: "the donuts just disappear, vaporize" | **FAIL** | 50 points in the donut box lost in place, frames 39 to 54 (spot match 0.0); 55 points of empty box "from nowhere" in the same place, 42 to 69 |
| A5 frames 0-24 | shipped as round 3's shot one | PASS | nothing lost |
| A5 frames 84-143 | shipped as round 3's shot two | PASS | nothing lost |
| A6 fridge raid | no note, shipped | PASS | biggest stray cluster 2 points. Without the fridge declared in `may_change`, its two doors swinging open read as a vanish (34 points): the spec has to say what opens |
| A7 bar | no note, shipped | PASS | biggest stray cluster 3 points |
| A8 cartoon cell, 2x push-in | no note | **FAIL** | real morphing the 10-13 review let through: as the camera pushes in, a broken mitochondrion on the right dissolves into the floor (frames 117 to 131) and the purple junk band across the foreground melts into clean floor with nobody sweeping it. Strict, but it is the fault class Dan named |
| A3 water jumps | rejected: "makes no physics sense" | PASS | not this tool's fault class: the water is in its glasses at both ends; what is wrong is cause and effect. The reviewer's three sense questions catch it |

Robustness (`run_grid_shift.sh`): the same verdicts with the grid at 32 px and 48 px. The donut take fails at every spacing
(event 35 to 81 points); its two shipped parts, A6 and A7 pass at every spacing. A7 first failed at 32 and 48 px: the back rail
of his bar stool, hidden under his arm while the stool tilted. That is why an event is dropped when its whole region is found again
within three grid steps (match 0.5 or better: A7's stool 0.69, the donut box 0.10 to 0.18). "Biggest cluster" in the rows counts
before that test.

Reviewer proof (the whole routine, on scratch copies, with the spec's note about Dan's verdict removed): a fresh `frame-reviewer`
failed the whole take on the box emptying (frames 39 to 66), and found on its own the donut in his hand fading out (24 to 30) and a
wall clock that runs backwards and grows a second "10". On frames 84 to 143, the raw take behind round 3's shipped shot two, it also
failed: a muffin standing tilted on its edge with nothing holding it (84 to 116), fingers going see-through as he grabs it (104 to
114, checked: the desk shows through his knuckles) and the clock (which the edit had patched). So the routine is stricter than the
round that shipped: that is the 10-13 standard. `--verify` refused both; on a separate copy with a placeholder PASS review it passed,
and refused again once the spec was edited.

**What it does not catch** (the reviewer's job): a change on the person (hands, faces, clothes, fingers); something that happens
and undoes itself inside the take (A3's splash); a small, faint change under the grid (A5's last glaze smear, frames 74 to 78, was
found by a reviewer, not by this); anything a tracker follows smoothly while it morphs into something else.

### Rules learned building it

1. **Compare the ends, not the moment of loss.** A version that compared each lost spot just before and just after the loss failed
   the two shipped takes: in A6's dark kitchen the person mask missed the man who walks in front of the window and stays there. At
   the end the backward-traced points on that spot plainly came from elsewhere, which is what tells a mover from a vanish.
2. **A moving camera needs windows.** On A8's push-in, a spot 40 px wide at the end was 15 blurred px at the start, and first-vs-last
   flagged 160 points of plain zoom. Windows over which the picture changes little fix that and still see real morphing.
3. **The spec says what opens.** Doors, lids, screens and fires are legitimate changes the tracker cannot tell from a vanish.
4. **Memory, on a Mac other sessions render on.** GPU memory grows with frames x points (64 x 650: 7.8 GB; 96 x 650: 12 GB). At
   144 frames with the swap full a take ran 8 minutes and once never finished. Hence the 64-frame cap and point batches
   (`cotracker_mps.py`). Two ops CoTracker needs are missing on Apple's GPU; `mps_ops.py` replaces them with exact equivalents
   (tracks within 0.05 px of the CPU run).

### Licences (checked 2026-10-14)

- **CoTracker3 is CC BY-NC 4.0, code and weights: non-commercial.** Dan chose it (2026-10-14 starter prompt); these are ads and
  content for a paid product, so running it on them sits outside that licence. The licence-clean tracker is **BootsTAPIR**
  (Google DeepMind; code and checkpoints Apache 2.0). Tried 2026-10-14 and dropped: on Apple's GPU it returns wrong tracks
  (points 150 px off on a still desk, with or without the `mps_ops` patches), and on the CPU a 2 s range ran over 40 minutes
  while other sessions rendered. A licence-clean motion gate needs a CUDA machine for BootsTAPIR, or a test of TAPNext++
  (same repo, same licence) on this Mac; `run_tracker` in `clipcheck.py` is the one place to swap it in.
- **Step 5, 3D body fitting, is not built: the named tools are all non-commercial.** The SMPL-X body model (commercial licence
  only through Meshcapade), SMPLest-X (S-Lab License: non-commercial) and Multi-HMR (NAVER: non-commercial, its Anny checkpoint
  too). The clean path is **Meta's SAM 3D Body** (SAM License, commercial use allowed; its MHR body model is Apache 2.0), whose
  weights are gated: Dan requests access on Hugging Face (`facebook/sam-3d-body-dinov3`) with his own account, then a session gets
  an HF read token. Open in `Handoffs/handoff-20261014-frame-qc-upgrade.md`.

## Rules learned on the first run (seven independent reviews, six fails)

1. **Prove a check on the frames Dan rejected first.** posecheck read 26 and 43 degrees leg-to-rail on his rejected pair.
2. **The automatic rail finder can grab the backrest or an upright.** Mark the rail endpoints by hand on a gridded crop
   (`--rail`) and use `--rail auto` only as a hint.
3. **Track parts with local, high-texture boxes** (a plate rim, a bolt, a shoe logo). A global search jumps to look-alike plates
   on other machines; a box over flat black or the background returns nonsense with a low score. Trust scores above about 0.85.
4. **Image models lengthen legs when they straighten them** (bent frames measured 1.35 to 1.57 torso lengths of leg, straight
   ones 1.84 to 1.88). Compare bone lengths on every candidate pair; more than about 8 % change is a fail, and the foot travel
   must be what straightening those bones allows.
5. **An image model will not keep a machine rigid across an edit.** When a machine part must move exactly, build the END in code
   from START: cut the part out as one sprite, move it along its guide, take only the person from the generated END
   (RA-04's `ad-edit/reference/ra04/r2c_sled.py`). Things to cover in that composite: a phone is not "person" to the segmenter
   (fill its old spot), shoes may not be either (detect them on the moved platform), START's feet resting on the moved part
   must be cut out of the sprite and filled, and the sprite outline must be traced at 5x (a loose outline drags background).
6. **The independent reviewer gets only the pictures, the overlays and the checklist**, never the editor's reasoning, and must
   measure: angles, lengths, displacements, diffs. A fresh agent each time. Expect several rounds; each fail cost minutes, a fail
   reaching Dan costs his trust.
