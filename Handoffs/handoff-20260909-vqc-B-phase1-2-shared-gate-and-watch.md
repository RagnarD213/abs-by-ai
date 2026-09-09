# VQC-B — Phase 1 + Phase 2: one shared delivery gate, and the watch pass everywhere

**Part 2 of 4 of the video-quality programme.** Evidence and the full plan:
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.
**Updated 2026-09-09 after VQC-A ran** — the inventory below is re-measured, not inherited.

> ✅ **VQC-A IS DONE (commit `a696ac4`), so this phase is unblocked.** The seven gate bypasses are
> closed and the regression corpus is live and green at `.claude/skills/_shared/qc_corpus/`.
> **That corpus is your safety net and your acceptance test** — without it this phase is a rewrite of
> ~17 gates with nothing proving the rewrite still catches what they caught, which is exactly how
> checks got lost in the forks in the first place.
>
> **Read `Docs/VQC_baseline_20260909.md` before you start.** It is the current state of every
> delivered master, and three of its findings change what you build here.

**Fable 5.1, high effort. ~2 sessions. $0.00 generation spend**, plus a few cents per video for the
watch pass in Phase 2.

---

## What VQC-A hands you

| | |
|---|---|
| `_shared/qc_corpus/run.py` | 14 files Dan rejected or approved, in his own words. **Green today.** Runs `_shared/audio/selftest.sh` as its step 0 |
| **14 named checks nothing implements** | run.py prints them every run. **Five of them are yours** — see *Your share of the queue* below |
| The NOT-MEASURED discipline | a check that did not run is a **FAILURE**, never a silent skip. Standing rule in `AGENTS.md`. Carry it into every row you write |
| A per-format precedent | `audio_gate.py --profile in-app-demo` — a **named, measured profile**, deliberately not a free `--lufs-target`. Copy that shape |
| A generic gate skeleton | `shortad-from-longform/reference/qc.py` — 20 checks, per-cut numbers in a `qc.json`, missing input ⇒ NOT MEASURED ⇒ FAIL. **Written 2026-09-09. Lift its skeleton; do not merge it as an 18th fork** |

⚠ **`selftest.sh` is a zsh script.** `bash selftest.sh` dies on `${0:A:h}` with *"A: unbound variable"*,
which reads exactly like a real bug and is how it spent a day documented as BROKEN. Run `zsh selftest.sh`.

---

## The problem being fixed — re-measured 2026-09-09

**60 QC / gate / deliver scripts across the video skills. One module is shared** (`_shared/audio/`).
`_shared/` still has **no picture, framing, cut, caption or compliance module at all.**

**17 of the 60 are the main QC forks — 3,083 lines** that mostly re-measure the same things:

| skill | forks | lines |
|---|---|---|
| `website-video/reference/recipe/` | `qc.py` + `rev1/` + `rev2/` + `rev3/qc.py` | 723 |
| `shorts/reference/` | `clean-master` · `full-bleed` · `scored-source` · `zepbound` `qc.js` | 700 |
| `longform-edit/reference/` | `qc_style` · `qc_generic` · `qc_with_inserts` · `qc_investhealth` · `_v3` | 934 |
| `shortad-from-longform/` | `qc.py` (new, generic) + `qc_ad2v2.py` (per-ad fork) | 520 |
| `ad-edit/reference/` | `rev5/qc5.py` · `modern60/qc_modern.py` | 206 |

**Verified examples of what divergence costs** (each re-checked 2026-09-09, not quoted from the audit):

* `shorts/reference/full-bleed/qc.js` has **no caption-sync check and no loudness check at all**;
  `scored-source/qc.js` has **no caption-sync check**. Two of the four shorts gates cannot see a
  desynced caption.
* `ad-edit/reference/modern60/qc_modern.py` contains **exactly one `assert`** (`max(shots) <= 25.0`).
  Everything else it does is `print`. **It is a report wearing a gate's filename** — it cannot fail a
  build for a bare splice, which is the thing it measures most carefully.
* `longform-edit/reference/srt_validate.py` exists and is **invoked by nothing** — it appears once, in a
  README table.
* `ad-edit/reference/rev5/qc5.py` has no banned-screen scan, no caption clearance and no hair gate.

`qc_style.py`'s own preamble states the stakes: *"the skill's quality bar was prose and its quality gate
was code, and under time pressure a session ships what the gate checks."* It appears in **one** SKILL.md.

---

## PHASE 1 — `_shared/deliver/`

Build the module that should have existed beside `_shared/audio`. **One gate, called by all six skills,
run on the delivered file, with per-format config — never per-video scripts.**

### Design

* `gate.py <file> --format ad9x16|ad16x9|longform|short|website|exercise-demo --plan plan.json`
* Rows come from config, not from copies. Where two formats genuinely differ, that is a config value
  **with a comment naming the video and the date it was measured** — the way `qc_style.py`'s constants
  already do (`MIN_COVERAGE = 0.40  # reference cut ~90%; spray tan shipped 51%; ab wheel 21%`).
* **A missing input is NOT MEASURED, which FAILS.** Never `[SKIP]`. If a check genuinely does not apply
  to a format, that is an explicit, commented config value a reader can audit — not silence.
* **No free dials.** Named profiles only. A bound that can be passed on the command line is not a bound.
* **Version the gate.** `GATE_VERSION` in the stamp; any change to a check or a bound bumps it and
  **every stamp at an older version becomes invalid.**

  ⚠ **The baseline proves this one.** `Docs/VQC_baseline_20260909.md`: **20 delivered files carry a PASS
  stamp and would fail a re-gate today**, including 16 Zepbound and supplements Shorts stamped on
  2026-09-02 on the dereverb Dan rejected a week later. **139 of 166 masters carry no stamp at all.**
  Nothing re-checks a stamp when the standard moves; versioning is what makes that automatic.

### What to fold in

The 17 forks above · `caption_sync_check.py` · `gain_flatness.py` · `landing_check.py` · the
banned-screen template scan · `srt_validate.py` · `content_flags.py` · `verify_cover.py` and
`tailcheck.py` (both hardcoded to one project's path) · `shorts/reference/*/syncgate.py` ×3 ·
`shorts/reference/recentre/delivered_gate.py`.

**Method:** for each fork, list its checks; union them; **for every check that exists in one fork and not
another, decide deliberately whether it applies to that format, and record the decision in the config.**
A check that silently exists in only one fork is the bug. Then delete the forks and grep for survivors
(`_shared/audio/README.md` non-negotiable 9: *"Grep for forks before assuming a shared fix has landed"*).

### Two rows to add that are documented and enforced nowhere

* **Lip sync.** Every master finished with `loudnorm + alimiter` has run ~5 ms late
  (`longform-edit/SKILL.md:1362`), and the fix is written down: *"cross-correlate the finished audio
  against the source at several checkpoints — it must read 0.000 ms."* Nothing does it. The audio gate
  checks audio **length** (±0.10 s), never **alignment**.
* **Compliance.** The **Negative Events and Imagery** scan — a real Google Ads strike risk
  (`ad-edit/SKILL.md:368-384`) — is manual in every skill. Banned product screens are template-scanned
  in `/ad-edit` only, which is how a side-by-side before/after reached the delivered spray-tan longform
  for 5.6 s at 18:04. The AI-GENERATED label check exists in `qc_frame.py` for ad-edit only, while
  `/make-ad` states the same requirement with no check behind it.

### Two calibration items the baseline opened — solve them here, properly

1. **The exercise demos (88 files) fail `silence` and `length`, and both are format, not defect.** The
   narration ends and the rep keeps looping. VQC-A deliberately did **not** widen those rows — that is
   raising a bound. Give `exercise-demo` a format config where audio may be shorter than picture and a
   trailing tail is allowed, **with the allowance measured off the batch-1 files Dan approved**, and say
   so in the commit.
2. **One pinned reference cannot grade every programme.** Muhammad's ab-wheel edit, both Zeeshan cuts —
   and **Muhammad's own Ad 1 reference file** — fail rows graded against Ad 1's numbers (his reference
   measures −18.2 LUFS at +0.1 dBTP: too quiet and too hot for a platform). Per-format config plus the
   existing `--reference-mix` path is the answer. **Do not widen a bound to make an editor's cut pass.**

### Your share of the corpus queue

`run.py` names 14 unimplemented checks. **Phase 1 owns these five** — implementing them and registering
them in `run.py`'s `IMPLEMENTED` map is how you prove the phase landed:

```
style:coverage               ← abwheel-8-20-cut       (21% against his ~90%)
style:static_run             ← abwheel-8-20-cut       (64 s bare, twice, against Dan's 30 s rule)
captions:graphic_clearance   ← website-rev2           ("captions don't overlap graphics", a standing rule)
compliance:banned_screen     ← spraytan-longform-rev0 (the side-by-side at 18:04)
cut:uncovered_joins          ← spraytan-longform-rev0 (41 uncovered joins)
```

The other nine belong to VQC-C (`cut:`, `music:`) and VQC-D (`framing:`, `junk:`).

### Phase 1 done when

`_shared/qc_corpus/run.py` is green **against the new gate**; those five checks are registered and
`run.py --strict-pending` no longer names them; every skill's delivery path calls
`_shared/deliver/gate.py`; the forks are deleted; and no SKILL.md names a QC script that does not exist.

⚠ **21 named-but-missing scripts remain** (VQC-A fixed the four that were enforcement claims). They are
listed in `Docs/VQC_baseline_20260909.md` §6 — `longform-edit` 6, `youtube-packaging` 5, `coverimage` 3,
`shortad-from-longform` 3, `photo-edit` 2, and one each in `ad-edit`, `make-ad`, `revisions`,
`teleprompterscripts`. Most are historical build scripts, not check claims. **Either make each one true
or delete the claim.**

---

## PHASE 2 — the watch pass becomes mandatory in all six skills

Today it is a hard gate in **`/shortad-from-longform` only** (qc check 15 reads `logs/watch_pass.json`
and refuses without it — described in that SKILL.md as *"the only way a 'watch the video' rule survives
contact with a build that is running late"*). `/shorts` **mentions it zero times**, and its own
SKILL.md:971 says *"THE CONTACT SHEET IS NOT A GATE. Every framing fault in this batch survived one."*

`watch.py`'s docstring records why it exists: *"Ad 1 attempt 1 passed 11/11 on a metric gate and Dan
rejected it: every check measured format, none ever looked at the moving picture."* That file is corpus
entry `ad1-vertical-attempt1`, and Dan's words on it are *"truly awful… definitely won't work."*

### Build

1. Port `watch.py` (now `website-video/reference/recipe/watch.py`, moved 2026-09-09) and `shortad`'s
   `a2/watch.py` into `_shared/deliver/watch.py`. Keep both halves: the **automated** every-frame scan
   (frozen runs `d < 0.05` at 30 fps 160×90 gray, black frames, hard discontinuities **not** at a
   boundary the beat sheet knows about) and the **by-eye** boundary strips.
2. **Keep the instrument that works: consecutive frames at −2/−1/0/+1/+2 across every boundary.** Two
   frame-difference detectors failed in a row on a real jump cut — a whole-frame gray diff scored it at
   **2.0× its local median ("clean")**, a face-region diff ranked it **12th of 28**. A 1 s contact sheet
   cannot see it, and `fps=1/N` sheets lag content by ~N/2 s (ad-edit lesson 94 — three false alarms in
   one review; grab suspect frames with exact `-ss` before calling anything a defect).
3. **Automate the first pass.** Contact sheets (~25 frames per image) checked by a model against a list
   derived from Dan's own rejections: hair at or over the top edge · head or arm out of frame · junk or
   placeholder card · naked splice · graphic over his face · text off-screen · black frames · duplicate
   shot · a wide level where none should exist.
   ⚠ **Frame sheets, not video-model input** — Gemini charges $0.15 per second of video, ≈$36 for one
   4-minute ad. Sheets are cents.
4. Wire `gate.py` to **fail unless `logs/watch_pass.json` names this file's sha256.**
5. Keep `shortad` Step 7b's **independent subagent audit** for anything Dan will see, and add it to
   `/ad-edit`, `/longform-edit`, `/website-video` and `/shorts`. It has twice overturned a session's own
   "this is fixed" conclusion — including catching that our eyeball reads of *"he is off to the left"*
   were **mirrored** at three of four timestamps.

### Phase 2 done when

All six skills' delivery paths refuse a file with no watch pass; **the automated pass reproduces the
known defects in the corpus** — it must flag `website-rev3`'s hair and `ad1-vertical-attempt1`'s naked
splices, both of which are already sitting there with Dan's words attached; and the per-video cost is
recorded in `_shared/COSTS.md`.

---

## Traps

* **Do not "simplify" a bound while merging.** Every constant in these gates traces to a file Dan
  approved or rejected. **Carry the provenance comment with the number.**
* **Do not raise a threshold to make a build pass** — memory `audio-never-over-strip`. If a corpus entry
  fails a bound, that is the finding.
* **Do not add a `known_gap` to make `run.py` green.** A gap records one named check on one named file
  with a reason, a date and what clears it; four entries carry the pre-09-09 do-no-harm gap and `run.py`
  tells you when one heals. **If you are adding a gap so a change can ship, you are relaxing a bound.**
* **Do not delete a `must_trigger` to make the run green.** If nothing implements it, it is PENDING —
  which is the point.
* Two formats have **opposite** caption rules: organic longforms carry NO burned captions (Dan,
  2026-08-27 — `qc_style.check_captions` inverts under `ORGANIC=1`), ads and shorts do. Per-format
  config, not a bug to normalise away.
* `--reference-mix` mode (shortad, when the audio is the editor's own mix) legitimately demotes six
  audio rows to informational. Preserve it; do not let it leak to formats that mix their own audio.
* `do_no_harm` is informational **only** where the file is genuinely not ours
  (`--reference-rows-only`, `--reference-mix`). Keep that boundary exactly where it is.
* Respect `AGENTS.md`'s **two-concurrent-build cap** — check
  `ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'` before starting a gate run.
* **`Media/` is gitignored.** A script that lives only there is not in the repo and does not enforce
  anything — that is how `mono.py` and `ghost.py` spent weeks named as MANDATORY while being one
  `rm -rf` from gone.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-vqc-B-phase1-2-shared-gate-and-watch.md and execute it. Read
Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md first for the evidence, and
Docs/VQC_baseline_20260909.md for the current state of every delivered master.

VQC-A is done (commit a696ac4). Confirm `python3 .claude/skills/_shared/qc_corpus/run.py` is green
before you start, and keep it green throughout — it is the acceptance test for this whole phase.

Phase 1 builds _shared/deliver/gate.py: ONE version-stamped delivery gate replacing 17 per-video QC
forks (3,083 lines), with per-format config, lip-sync and compliance rows added, and the five corpus
checks it owns (style:coverage, style:static_run, captions:graphic_clearance, compliance:banned_screen,
cut:uncovered_joins) implemented and registered in run.py's IMPLEMENTED map. Phase 2 ports the watch
pass into it and makes it mandatory in all six skills, with an automated frame-sheet first pass.

A missing input is NOT MEASURED, which FAILS — never a silent skip. Never raise a bound to make a
build pass, and never add a known_gap to make run.py green. Respect the two-concurrent-build cap.
Commit, push, verify. No dashboard row.
```

**Model:** **Fable 5.1, high effort.** This is the phase where judgment matters most — deciding, for 17
forks and ~95 distinct checks, which differences are real format differences and which are checks that
were lost by accident. If Fable's weekly allowance is short, Opus 5 at high effort substitutes; do
**not** run this one at standard effort.
