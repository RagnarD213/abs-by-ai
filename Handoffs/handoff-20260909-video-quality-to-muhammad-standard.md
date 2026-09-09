# Handoff — get our video editing to Muhammad's standard

**Written 2026-09-09. Not executed.** Model: **Fable 5.1, high effort.** Six phases, ~5–7 sessions;
Phases 0–3 are the block that stops the repeats and should be run first, in order.

---

## Why this exists

Dan, 2026-09-09: *"A lot of what we're doing with the video editing process isn't working, and I'm
not actually going to ship anything that we made because it's far below the quality that the human
editors have made."* His four named defects: **audio, framing (head out of frame), jump cuts, junk
footage left in.**

He is right on all four, and the cause is structural, not a lack of technique. **Every one of these
has already been solved once, measured, and written down — and each fix reached exactly one video.**

---

## The diagnosis, in evidence

### 1. There are 33 QC/gate scripts. One is shared.

`_shared/` contains `audio/`, `timing/`, `motionlib.py`, `sfxlib.py`, `gemini-image.js`,
`whisper-to-scribe.py`. **There is no shared picture, framing, cut, caption or compliance module at
all.** Everything else is a per-video fork:

* four divergent copies of `shorts/reference/*/qc.js` — two of them have **no silent-second check and
  no caption-sync check**, one has **no loudness check**;
* six copies of the `ad-edit` `qc.py` lineage (`website-video/`, `rev1/`, `rev2/`, `rev3/`,
  `rev5/qc5.py`, `modern60/qc_modern.py`), each with progressively fewer checks — `qc5.py` has **no
  banned-screen scan, no caption clearance, no hair gate**;
* four QC forks in `longform-edit/reference/`.

`_shared/audio/README.md` non-negotiable 8 already names this exact failure mode — *"No skill keeps
its own copy of the maths… Grep for forks before assuming a shared fix has landed."* That discipline
was applied to audio only.

### 2. The style gate reaches one of six skills

`qc_style.py` — cuts/min, static run, coverage, dead air, wpm, music bed — appears in exactly one
SKILL.md. **`/ad-edit` and `/shorts` state its rules in prose and run a narrower gate that measures
none of them.** So on every ad and every short, pacing/coverage/dead-air/junk is checked by nothing.

Its own preamble is the thesis of this handoff:

> *"the skill's quality bar was prose and its quality gate was code, and under time pressure a session
> ships what the gate checks."*

### 3. Every gate is built backwards from the last rejection, so each new failure ships once

The website video's framing history — three rejections in a row, each followed by a committed fix that
measured a slightly wrong thing:

| rev | verdict | measured cause |
|---|---|---|
| 1 | rejected | wide kitchen shot; *"don't ever use this super wide crop"* |
| 2 | rejected | *"excessive space above my head in all the shots"* — 159–261 px headroom, median 201 |
| 3 | rejected | **hair cut in 23 of 26 holds**, 17–50 px at 1080p; *"basically not usable"*. The detector read the **hairline**, 90 px inside his hair; **rev 3's own gate passed it at 21–95 px because it measured to the same wrong point** |
| 4 | **approved and locked** | hair-top detector; *"You nailed it"* |

Nine audio commits in eight days, each declaring audio solved. `/ad-edit` lesson 100 states the
pattern outright: *"When a revision passes every gate and still gets rejected, the gate was measuring
the wrong thing."*

### 4. Nothing watches the video, in five of six skills

The watch pass is a hard gate in **`/shortad-from-longform` only** (qc check 15 reads
`logs/watch_pass.json` and refuses without it). `/shorts` — which produced the spray-tan, Zepbound and
supplements batches Dan rejected — **mentions it zero times**, and its SKILL.md line 971 says
*"THE CONTACT SHEET IS NOT A GATE. Every framing fault in this batch survived one."*

`watch.py`'s own docstring records why: *"Ad 1 attempt 1 passed 11/11 on a metric gate and Dan rejected
it: every check measured format, none ever looked at the moving picture."*

### 5. There are documented ways to skip the gate, and one skill instructs it

* `/exercisegeneration` SKILL.md:225 — *"report loudness rather than fail on it (pass `--no-stamp` if
  the row fails)"*. A file with no stamp cannot be caught downstream either.
* `require_stamp.py:47` defaults `synthetic_ok=True` — a weakened 4-row synthetic stamp satisfies a
  caller unless `--strict`. **No SKILL.md passes `--strict` anywhere.**
* `do_no_harm` degrades to `ok=True, not_measured=True` when no untreated baseline was stashed
  (`audio_gate.py:150-156`).
* `qc_style.check_captions` silently returns unless the caller passes `--talking-head`;
  `check_splices` silently returns without `--plan`.
* `longform-edit/reference/composite_*.py` honour `AUDIO_UNGATED=1`.
* `_shared/audio/selftest.sh` — the regression suite protecting the one working gate — is
  **documented as broken** (README:21).

### 6. We have tried "make it so it can't regress" once, for one skill

`Handoffs/handoff-20260824-abwheel-muhammad-standard-rebuild.md` — *"Plan A: rebuild the ab-wheel
longform to Muhammad's standard. Plan B: rebuild `/longform-edit` so it can't regress."* Plan B is
where `qc_style.py` came from, and it reached that one skill and stopped. **This handoff is Plan B
done across all six skills, which is the part that was never done.**

### 7. Four scripts that SKILL.mds call do not exist

`shortad-from-longform/reference/qc.py` (referenced 5×), `exercisegeneration`'s `qc.py`, `_r2/mono.py`
and `_r2/ghost.py` (the latter two named as **MANDATORY** rules). `make-ad` and `exercisegeneration`
contain **no scripts at all** — SKILL.md only. Their picture rules have never been enforced by anything.

---

## The mechanical difference between his cuts and ours — MEASURED, and already solved once

This is the single highest-value finding in the audit, and it overturns a rule that was in the skill.

`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/notes-vertical-v2.md`, independent audit
2026-09-03:

> *"The conform cut the picture at every AUDIO splice; **Muhammad cuts the picture on a pose-matched
> frame of his own choosing, 1–15 frames away from the sound cut (a J- or L-cut), so his cuts read as
> continuity and ours as jump cuts.**"*

`piccuts.py` in that recipe folder already recovers his picture-cut frame at every talk splice
(render both takes from the raw at the grade, high-pass NCC against his frames): **22 of 33 cuts moved
by −15…+10 frames at confidence ≥ 0.6.** Two related fixes in the same audit: the crop's per-segment
median smoothing used a full window at segment ends, so he landed 78–190 px off centre after each cut
and the crop panned him back over up to 1 s — `facetrack3.py`'s shrinking end-window took **landing
error at every cut to 0 px**.

**And the rule this replaces was measurably wrong** (`AI_COORDINATION_ARCHIVE.md:8564`):

> *"It said he hides every trim under a wide↔punch framing change ACROSS splices… **his talk-to-talk
> splices jump as much as ours (43 of his 72 exceed 4× his own median frame diff; ours 32). The real
> defect was that 100 % of attempt 1's talk ran at one fixed crop — that is what makes a tripod shot
> read as a webcam recording.**"*

So the fix for "jump cuts" is **not** "hide every join". It is: **pose-matched picture cuts offset from
the audio splice, plus never running talk at one fixed crop** (his: 14 pushes, 39 % of talk).

---

## The plan

### PHASE 0 — Close the bypasses *(hours, no new code)*

Nothing is built. The checks already paid for stop being optional.

1. `require_stamp.py` — pass `--strict` from every caller; a synthetic stamp must not satisfy a real
   delivery.
2. Delete the `--no-stamp` instruction from `exercisegeneration/SKILL.md:225-227`.
3. `do_no_harm` `not_measured` → **FAIL**, not pass.
4. `qc_style.check_captions` and `check_splices` → a missing flag is a FAIL, not a silent skip.
5. A SKILL.md that names a script which does not exist → make it an error. Either write
   `shortad/reference/qc.py`, `exercisegeneration/qc.py`, `_r2/mono.py`, `_r2/ghost.py`, or delete the
   claim that those rules are enforced.
6. Fix `_shared/audio/selftest.sh` (unbound variable + pre-09-08 reference paths). Also fix
   `common.stash_untreated()`, missing at 10:03 on 09-09 while `voice_chain.py:158` calls it.
7. Remove `AUDIO_UNGATED=1`.

**Done when:** re-running the CURRENT gates over every delivered file in the project produces a list of
what would not ship today. Expect that list to be long; that is the point.

### PHASE 1 — `_shared/deliver/` — one gate for any finished file *(1–2 sessions)*

Create the module that should have existed beside `_shared/audio`. One gate, called by all six skills,
on the delivered file, with **per-format config, never per-video scripts**.

* Fold in: `qc_style.py`'s rows, the four `shorts/qc.js` forks, the six `ad-edit/qc.py` forks, the four
  `longform` forks, `caption_sync_check.py`, `gain_flatness.py`, `landing_check.py`, the banned-screen
  template scan, `srt_validate.py` (exists, never invoked).
* **Version the gate.** Any change to a check or a setting bumps the version; every stamp at an older
  version becomes invalid. *This alone would have caught 04 invest-health automatically* — it was
  stamped 09-03 with the dereverb settings Dan later rejected and nothing re-checked it.
* Delete the forks once they are folded in. Grep for survivors (README non-negotiable 8).

Two rows to add that are documented and enforced nowhere:

* **Lip sync.** Every master finished with loudnorm + alimiter runs ~5 ms late
  (`longform-edit/SKILL.md:1362`). The gate checks audio *length* (±0.10 s), never alignment.
  Cross-correlate the finished audio against the source at checkpoints; it must read 0.000 ms.
* **Compliance.** The Negative Events and Imagery scan — a real Google Ads strike risk — is manual in
  every skill. Banned product screens are template-scanned in `/ad-edit` only, which is how the
  side-by-side before/after reached the delivered spray-tan longform for 5.6 s.

### PHASE 2 — The watch pass becomes mandatory everywhere *(1 session)*

Port `watch.py` + the check-15 pattern into `_shared/deliver/`: **the gate fails unless a watch pass is
logged against that exact file's sha256.**

* Keep the instrument that works: **consecutive frames at −2/−1/0/+1/+2 across every boundary.** Two
  frame-difference detectors failed in a row on a real jump cut (whole-frame gray diff scored it at
  2.0× local median = "clean"; face-region diff ranked it 12th of 28). A 1 s contact sheet cannot see
  it, and `fps=1/N` sheets lag content by ~N/2 s (lesson 94 — three false alarms in one review).
* Automate the first pass: frame **sheets** (25 frames per image), not video-model input — Gemini
  charges $0.15/s of video, ~$36 for one 4-minute ad. Check against a list built from Dan's own
  rejection history: hair at the top edge, head/arm out of frame, junk or placeholder card, naked
  splice, graphic over his face, text off-screen, black frames, duplicate shot.
* Keep Step 7b's **independent subagent audit** for anything Dan will see. It has twice overturned the
  session's own "this is fixed" conclusion, including catching that our eyeball reads of "he's off to
  the left" were mirrored at three of four timestamps.

### PHASE 3 — The regression corpus *(1 session — this is what stops repeats)*

Keep every file Dan **rejected** and every file he **approved**, with the reason.

**Rule: no gate change ships unless it fails every rejected file and passes every approved one.**

The pattern already exists and works: `selftest.sh` requires PASS on website rev 2 and FAIL on rev 1;
`hairgate.py` was proven on rev 3's master first (**test B failed 5371 of 5781 frames on a file that had
passed rev 3's own gate**). Extend to picture, cut and captions. Seed corpus:

| file | verdict | what it must trigger |
|---|---|---|
| website video rev 1 | rejected | wide level exists; audio |
| website video rev 2 | rejected | headroom 159–261 px |
| website video rev 3 | rejected | hair cut, 23/26 holds |
| website video rev 4 | **approved** | must pass everything |
| Ad 1 vertical attempt 1 | rejected | 23/72 naked splices, one fixed crop |
| spray-tan longform | rejected | junk at 4:00, 41 joins, side-by-side at 18:04 |
| 04 invest-health | rejected | artifacts 1.31× his |
| `v2-short3_supplements-3-percent` | rejected | off-centre, arm cut |
| Muhammad ad 1 + ad 2 16x9 | **reference** | must pass everything |

### PHASE 4 — The two changes that ARE Muhammad's advantage *(1–2 sessions)*

1. **Pose-matched picture cuts, offset from the audio splice.** Promote `piccuts.py` out of the Ad 2
   recipe folder into `_shared/cut/` and run it on every talk splice in every skill. This is the
   mechanism behind "his cuts read as continuity and ours as jump cuts."
2. **Never run talk at one fixed crop.** Gate it: ≥25–39 % of talk inside a push (his: 14 pushes,
   39 %). Zoom cuts ≥10 % — 6 % still read as a jump cut to Dan.
3. **Landing error 0 px at every cut** — port `facetrack3.py`'s shrinking end-window.
4. **Dead air to ~zero.** His reference cuts and Waleed's round 1 both measure zero; spray-tan shipped
   36 %, target 23 %. But heed the counter-measurement: a pause removal is itself as visible as the
   fault it fixes (4.97–12.46 against a 1.30 adjacent-frame baseline), and 0.55–0.65 s is breathing
   rhythm — so removals must be paired with a picture cut from item 1.
5. **Grade.** He is ~6 luma brighter on the talking head (67 vs our 55).

Build the picture reference the way `_shared/audio/reference.json` was built — pinned by fingerprint,
from the two finished Muhammad edits we hold — covering luma, shot-length distribution, cut rate,
insert coverage, graphic density. **Bound our output to his ranges in BOTH directions,** with a
do-no-harm counterweight. We already made the overshoot mistake once in audio: EDT 32 ms against his
40, "past" the target, and Dan called it underwater.

### PHASE 5 — Portable framing *(1 session)*

⚠ **Paths moved 2026-09-09, mid-audit:** a concurrent session split `/website-video` out of `/ad-edit` and
moved the recipe — `hairdet.py`, `hairgate.py`, `tanpass.py`, `layout.py`, `deliver.sh` — to
`.claude/skills/website-video/reference/recipe/`. `ad-edit/reference/website-video/` is now a README pointing
there. Every path in this handoff that says `ad-edit/reference/website-video/…` means that new location.
`piccuts.py` and `facetrack3.py` are unaffected (they live in the Ad 2 recipe folder under
`Muhammad Ad Videos/`).

`hairgate.py` **cannot run on any other set.** It hardcodes `FF=/Volumes/Extreme/_edit_work/bin/ffmpeg`,
`DAN_CX=1980`, and depends on `hairtrack.json`'s `hdr_col` — the static per-column luma profile of the
door panel behind Dan in the 8/28 kitchen set. Promoting it is not a copy job:

* Re-derive the hair-top detector without a set-specific background profile (the mediapipe
  FaceLandmarker in `tanpass.py` is the only real face detection in the repo — 478 points, CPU
  delegate, Metal crashes — and it is currently used for a spray-tan colour pass, not framing).
* Keep test B, the detector-free top-rows test — it is what caught rev 3 when test A's detector was
  wrong.
* **Wire framing into the skills that have zero framing rule today**: `/shortad-from-longform` (it
  re-crops Dan into vertical and has no hair rule at all — the biggest gap), `/revisions` (the
  review checklist has no framing item), `/editor-brief` (states the quality standard as measurements
  to freelance editors, and framing is not among them), `/coverimage`, `/youtube-packaging`.

### PHASE 6 — The junk/bad-take pipeline *(1 session)*

The detectors mostly exist and are scattered across three skills' `work/` folders. `junkscan.py`
**"found all six of Dan's timecodes and nine more he had not reached yet."** This is plumbing, not
research. Promote into `_shared/cut/` and run them together as one report:

`junkscan.py` (pause/splice/head) · `fixonsets.py` (a ≥0.25 s gap inside a word — the fix for
"junk footage at 0:01" being a 0.95 s hesitation Whisper swallowed) · `repeat_scan.py` (a stretched
word >0.7 s is a hidden restart until proven otherwise; verify by re-transcribing the span in
isolation) · `orphan_scan.py` (speech energy no word covers) · `hard_splices.py` (which splices are
measurably discontinuous, pre-render) · `pausejump.py`.

Add take selection: today we remove flubs, we do not pick the best take. Rule already written —
*later-take-wins only when the later take is fluent*; a roll's noise floor identifies the bad take
(−45.3 / −20.2 on the retake vs ≈−48 dB elsewhere). And cut the whole restated **sentence**, not the
aborted take inside it — v2 cut only the flub and Dan flagged it again.

---

## Definition of done

Nothing reaches Dan unless:

1. it passed `_shared/deliver/` **at the current gate version**;
2. a watch pass is logged against that exact file's sha256;
3. it went through `/revisions` first — the same review we run on editors' cuts — and the findings
   were fixed.

**Dan should never be the first person to watch a cut.** He is today, which is why he is seeing
head-out-of-frame in delivered files.

---

## Scope note for whoever runs this

Parity with Muhammad on a hero ad is not the goal and should not be sold as one. He is good, he is
cheap, and his advantage is taste applied second by second. Our advantage is a 6.7-minute revision at
$0.00 and volume he cannot economically cover — shorts off every longform, vertical variants,
exercise demos, ad variants for testing. **Point the pipeline there and hold it to his measured
standard.** The gate work pays off either way: it is what makes volume work shippable without Dan
reviewing every frame.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md and execute PHASE 0 and PHASE 3
(close the gate bypasses, then build the regression corpus). Do not start Phase 1 in this session.

Phase 0 is seven small changes, no new machinery — the list is in the doc. When they are done, re-run
the current gates over every delivered file in the project and report what would not ship today.

Phase 3 is the corpus: collect every file Dan rejected and every file he approved (the seed table is
in the doc), and wire the rule that no gate change ships unless it fails every rejected file and passes
every approved one. Fix _shared/audio/selftest.sh first — it is broken, and it is the working example
of exactly this pattern.

Respect the two-concurrent-build cap in AGENTS.md. Commit, push and verify as usual. Do not add a
dashboard row.
```

**Model:** Fable 5.1, high effort. **Estimated:** 2 sessions for Phases 0+3, ~5–7 for all six.
**Spend:** $0.00 for Phases 0–3 (no AI generation); Phase 2's automated watch pass is frame sheets,
a few cents per video.
