# framecheck: measure AI start/end frames for body and physics faults before Dan sees them

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
