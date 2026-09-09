# VQC-B — Phase 1 + Phase 2: one shared delivery gate, and the watch pass everywhere

**Part 2 of 4 of the video-quality programme.** Evidence and the full plan:
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.

⚠ **DO NOT RUN THIS BEFORE VQC-A.** The regression corpus is what proves a rewritten gate still catches
everything the 33 scattered ones caught. Without it this phase is a rewrite with no safety net, which is
exactly how checks got lost in the forks in the first place.

**Fable 5.1, high effort** (this is the design-heavy phase — see the model note at the bottom).
**~2 sessions. $0.00 generation spend**, plus a few cents per video for the watch pass in Phase 2.

---

## The problem being fixed

There are **33 QC/gate scripts** across the video skills and exactly **one** is shared
(`_shared/audio/`). `_shared/` has **no picture, framing, cut, caption or compliance module at all.**
Consequences measured in the 2026-09-09 audit:

* `qc_style.py` — cuts/min, static run, coverage, dead air, wpm, music bed — appears in **one** SKILL.md.
  `/ad-edit` and `/shorts` state its rules in prose and run a narrower gate. **Pacing, coverage,
  dead air and junk are checked by nothing on every ad and every short.**
* Four divergent copies of `shorts/reference/*/qc.js`; two have **no silent-second and no caption-sync
  check**, one has **no loudness check**.
* Six copies of the `ad-edit` `qc.py` lineage; `rev5/qc5.py` has **no banned-screen scan, no caption
  clearance, no hair gate**.
* Four QC forks in `longform-edit/reference/`.

`qc_style.py`'s own preamble states the stakes: *"the skill's quality bar was prose and its quality gate
was code, and under time pressure a session ships what the gate checks."*

---

## PHASE 1 — `_shared/deliver/`

Build the module that should have existed beside `_shared/audio`. **One gate, called by all six skills,
run on the delivered file, with per-format config — never per-video scripts.**

### Design

* `gate.py <file> --format ad9x16|ad16x9|longform|short|website|synthetic --plan plan.json`
* Rows come from config, not from copies. Where two formats genuinely differ, that is a config value with
  a comment naming the video and the date it was measured — the way `qc_style.py`'s constants already do
  (`MIN_COVERAGE = 0.40  # reference cut ~90%; spray tan shipped 51%; ab wheel 21%`).
* **Version the gate.** `GATE_VERSION` in the stamp. Any change to a check or a bound bumps it, and
  **every stamp at an older version is invalid.** *This alone would have caught 04 invest-health
  automatically* — it was stamped 09-03 on the dereverb settings Dan later rejected, and nothing ever
  re-checked it; we found it by hand after he rejected the video.
* Reuse the enforcement pattern that already works: a sidecar stamp carrying sha256 + every number +
  PASS/FAIL, and `require_stamp` called by every delivery path.

### What to fold in

`qc_style.py`'s rows · the four `shorts/qc.js` forks · the six `ad-edit/qc.py` forks · the four
`longform` forks · `caption_sync_check.py` · `gain_flatness.py` · `landing_check.py` · the banned-screen
template scan · `srt_validate.py` (exists in `longform-edit/reference/`, **never invoked by any
SKILL.md**) · `content_flags.py` · `verify_cover.py` and `tailcheck.py` (both currently hardcoded to one
project's path).

**Method:** for each fork, list its checks; union them; for every check that exists in one fork and not
another, decide deliberately whether it applies to that format and record the decision. **A check that
silently exists in only one fork is the bug.** Then delete the forks and grep for survivors —
`_shared/audio/README.md` non-negotiable 8: *"Grep for forks before assuming a shared fix has landed."*

### Two rows to add that are documented and enforced nowhere

* **Lip sync.** Every master finished with `loudnorm + alimiter` has run ~5 ms late
  (`longform-edit/SKILL.md:1362`), and the fix is written down: *"cross-correlate the finished audio
  against the source at several checkpoints — it must read 0.000 ms."* Nothing does it. The audio gate
  checks audio *length* (±0.10 s), never alignment.
* **Compliance.** The **Negative Events and Imagery** scan — a real Google Ads policy strike risk
  (`ad-edit/SKILL.md:368-384`, item 4) — is manual in every skill. Banned product screens are
  template-scanned in `/ad-edit` only, which is how a side-by-side before/after reached the delivered
  spray-tan longform for 5.6 s at 18:04. The AI-GENERATED label check exists in `qc_frame.py` for
  ad-edit only, while `/make-ad` states the same requirement with no check.

### Phase 1 done when

`_shared/qc_corpus/run.py` (from VQC-A) is green **against the new gate**, every skill's delivery path
calls `_shared/deliver/gate.py`, the forks are deleted, and no SKILL.md names a QC script that does not
exist.

---

## PHASE 2 — the watch pass becomes mandatory in all six skills

Today it is a hard gate in **`/shortad-from-longform` only** (its qc check 15 reads
`logs/watch_pass.json` and refuses without it — described in that SKILL.md as *"the only way a 'watch the
video' rule survives contact with a build that is running late"*). `/shorts` **mentions it zero times**,
and its own SKILL.md:971 says *"THE CONTACT SHEET IS NOT A GATE. Every framing fault in this batch
survived one."*

`watch.py`'s docstring records why it exists: *"Ad 1 attempt 1 passed 11/11 on a metric gate and Dan
rejected it: every check measured format, none ever looked at the moving picture."*

### Build

1. Port `watch.py` (currently `website-video/reference/recipe/`, moved there 2026-09-09) and
   `shortad`'s `a2/watch.py` into `_shared/deliver/watch.py`. Keep both halves: the **automated**
   every-frame scan (frozen runs `d < 0.05` at 30 fps 160×90 gray, black frames, hard discontinuities
   **not** at a boundary the beat sheet knows about) and the **by-eye** boundary strips.
2. **Keep the instrument that works: consecutive frames at −2/−1/0/+1/+2 across every boundary.** Two
   frame-difference detectors failed in a row on a real jump cut — a whole-frame gray diff scored it at
   **2.0× its local median ("clean")**, and a face-region diff ranked it **12th of 28**. A 1 s contact
   sheet cannot see it, and `fps=1/N` sheets lag content by ~N/2 s (ad-edit lesson 94 — three false
   alarms in one review; grab suspect frames with exact `-ss` before calling anything a defect).
3. **Automate the first pass.** Build contact sheets (~25 frames per image) and have a model check them
   against a checklist derived from Dan's own rejections: hair at/over the top edge · head or arm out of
   frame · junk or placeholder card · naked splice · graphic over his face · text off-screen · black
   frames · duplicate shot · a wide level where none should exist.
   ⚠ **Frame sheets, not video-model input** — Gemini charges $0.15 per second of video, ≈$36 for one
   4-minute ad. Sheets are cents.
4. Wire `gate.py` to **fail unless `logs/watch_pass.json` names this file's sha256.**
5. Keep `shortad` Step 7b's **independent subagent audit** for anything Dan will see, and add it to
   `/ad-edit`, `/longform-edit`, `/website-video` and `/shorts`. It has twice overturned a session's own
   "this is fixed" conclusion — including catching that our eyeball reads of *"he is off to the left"*
   were **mirrored** at three of four timestamps.

### Phase 2 done when

All six skills' delivery paths refuse a file with no watch pass; the automated pass reproduces the known
defects in the VQC-A corpus (it must flag rev 3's hair and Ad 1 attempt 1's naked splices); and the
per-video cost is recorded in `_shared/COSTS.md`.

---

## Traps

* **Do not "simplify" a bound while merging.** Every constant in these gates traces to a measurement of a
  file Dan approved or rejected. Carry the provenance comment with the number.
* **Do not raise a threshold to make a build pass** — memory `audio-never-over-strip`.
* Two formats have **opposite** caption rules: organic longforms carry NO burned captions (Dan,
  2026-08-27 — `qc_style.check_captions` inverts under `ORGANIC=1`), ads and shorts do. This is a
  per-format config value, not a bug to normalise away.
* `--reference-mix` mode (shortad, when the audio is the editor's own mix) legitimately demotes six audio
  rows to informational. Preserve that path; do not let it leak to formats that mix their own audio.
* Respect `AGENTS.md`'s two-concurrent-build cap.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-vqc-B-phase1-2-shared-gate-and-watch.md and execute it. Read
Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md first for the evidence.

Confirm .claude/skills/_shared/qc_corpus/run.py exists and is green before you start — VQC-A must have
been run. If it hasn't, stop and say so.

Phase 1 builds _shared/deliver/gate.py: one version-stamped delivery gate replacing the ~15 per-video QC
forks, with lip-sync and compliance rows added. Phase 2 ports the watch pass into it and makes it
mandatory in all six skills, with an automated frame-sheet first pass.

The corpus is the acceptance test: run.py must stay green throughout. Respect the two-concurrent-build
cap. Commit, push, verify. No dashboard row.
```

**Model:** Fable 5.1, high — this is the phase where judgment matters most (deciding, for ~15 forks,
which checks are format-specific and which were lost by accident). If Fable's weekly allowance is short,
Opus 5 at high effort is a reasonable substitute; do **not** run this one at standard effort.
