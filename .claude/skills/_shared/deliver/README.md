# `_shared/deliver` — the one delivery gate

One gate. All six video skills. Run on the **delivered file**, never on the build plan.

```bash
python3 .claude/skills/_shared/deliver/gate.py <file> --format <fmt> --plan plan.json
python3 .claude/skills/_shared/deliver/gate.py --audit        # every format answers for every row
python3 .claude/skills/_shared/deliver/gate.py --plan-keys    # what plan.json may contain
```

Formats: `ad9x16` · `ad16x9` · `ad1x1` · `longform` · `short` · `website` · `exercise-demo`.

---

## Why it exists

Across the six video skills there were **485 Python scripts, 60 of them QC/gate/delivery scripts,
and exactly one shared module** (`_shared/audio`). `_shared/` had **no picture, framing, cut,
caption or compliance module at all**, so a fix landed in one of six pipelines and the other five
kept the bug — which is literally what happened on 2026-09-09, when the spray-tan pipeline kept a
forked `work/dereverb.py` and the same-day shared fix never reached it.

Dan's eleven recorded rejections are **5 audio, 4 framing, 2 wholesale, 1 junk**. They repeat
because ours are *regressions*, not rule misses. A pre-flight checklist fixes a freelance editor's
class of defect. Only shared code fixes ours.

What divergence had already cost, each re-verified 2026-09-09:

* `shorts/reference/full-bleed/qc.js` has **no caption-sync check and no loudness check at all**;
  `scored-source/qc.js` has **no caption-sync check**. Two of four shorts gates could not see a
  desynced caption.
* `ad-edit/reference/modern60/qc_modern.py` contains **exactly one `assert`**. It is a report
  wearing a gate's filename.
* `longform-edit/reference/srt_validate.py` exists and is **invoked by nothing**.
* `ad-edit/reference/rev5/qc5.py` has no banned-screen scan, no caption clearance, no hair gate.

---

## The five non-negotiables

1. **A missing input is `NOT MEASURED`, which FAILS.** Never `[SKIP]`. The ancestor of this gate
   passed 11/11 on a video Dan called *"truly awful"* because every check measured format and none
   ever looked at the moving picture.
2. **No free dials.** Named per-format profiles only. A bound you can pass on the command line is
   not a bound. (`--row` exists for debugging, prints a warning, and never stamps.)
3. **A row a format has not answered for is `UNCONFIGURED`, which FAILS.** Adding a row forces
   every format to decide about it, in writing, in `formats.py`. `gate.py --audit` proves it.
4. **The gate is versioned.** `GATE_VERSION` goes in the stamp; any change to a check or a bound
   bumps it and **every older stamp becomes invalid.** `Docs/VQC_baseline_20260909.md` is why: 20
   delivered files carry a PASS stamp that would fail a re-gate today, and 139 of 166 masters carry
   no stamp at all.
5. **Never raise a threshold to make a build pass.** If a corpus entry fails a bound, that *is* the
   finding. Report it; do not tune it away.

## Evidence contract v2 (2026-09-16)

Composite edits cannot be graded honestly from a flat SRT and a full-frame crop. A delivery plan
that uses any v2 field must include:

```json
"evidence_contract": {"version": 2, "video_sha256": "<delivered file>"}
```

The new fields are `caption_states`, `speech_words`, `graphic_regions`,
`talking_head_windows`, and `label_tracks`; `gate.py --plan-keys` documents their shapes. Renderer
assets may carry their own SHA-256. Missing assets, changed assets, invalid rectangles, and geometry
bound to another render all fail `NOT MEASURED`—stale metadata can never certify new pixels.

`caption_states` are the compositor's real PNG/highlight states, not an SRT approximation. The gate
checks their alpha/ink bounds against graphic regions and verifies the state itself in the delivered
pixels. `speech_words` are timed from delivered-audio ASR, or from source CTC only when this exact
file carries a verbatim audio-gate PASS stamp. The evidence method is explicit in
`speech_words_evidence`, so continuous speech no longer depends on finding silence or trusting an
unverified timing file.

`talking_head_windows` makes the detector work inside full-screen, stacked, and side-by-side
composites. Every state says `motion: tracking` or `motion: fixed-wide`; an intentional fixed-wide
shot still has its hair/face measured but is not falsely failed for not tracking the centre line.

`label_tracks` follow the renderer's source image and transform through the delivered pixels.
Short transition states may be declared `visibility: partial`; they are reported separately, never
counted as an unexplained missing label. A moving three-frame state can provide its exact
`sample_times`; an optional position search is capped at four pixels by the format so codec/frame
rounding is tolerated without allowing a misplaced label to pass. The gate also measures every
full label rectangle against an independent delivered-frame person mask; `label_clearance` can
instead bind an existing equivalent face/abs mask report to the delivered SHA.

Policy scans now have four explicit outcomes: PASS, confirmed FAIL, NEEDS HUMAN REVIEW, and NOT
MEASURED. Every finding must say `disposition: cleared|confirmed_violation|needs_review`; an
unresolved review candidate blocks delivery without being mislabeled as a confirmed violation.

Current automatic v2 exporters are the active `shortad-from-longform/reference/plan_build.py`
vertical path (`ad9x16`) and its square `a11_sq_ad1/plan_sq.py` path (`ad1x1`). The other five
declared formats continue through the legacy plan fields unless their renderer actually uses PNG
states or composite windows; their existing ASS, full-frame and format-specific N/A behavior is
unchanged. In particular, `longform` still requires no burned captions and delivers an SRT. Do not
claim v2 coverage for `ad16x9`, `longform`, `short`, `website`, or `exercise-demo` until that
format's renderer exports these facts.

## Where a number may live

**`formats.py`, beside the file and the date it was measured on.** Nowhere else. If you are about
to write a constant into `checks/`, you are starting fork number eighteen.

The one exception is a decode setting (`fps=6, 64x36`; `fps=2, 48x27`; `fps=12, 48x27` in
`checks/picture.py`). Those are **part of the calibration**: change one and every bound in
`formats.py` is measuring something else, so the whole corpus has to be re-measured and the
calibration table rewritten.

## Two formats have opposite rules, and that is not a bug

Organic longforms carry **no** burned captions — the `.srt` sidecar is the deliverable (Dan,
2026-08-27). Ads and Shorts carry them. `captions:burned` is therefore a per-format value with two
legal settings, and a format must state which one it is.

Likewise **one pinned reference cannot grade every programme.** A trust video holds on Dan's face on
purpose; grading `website` against the long-form `style:coverage` of 0.40 would block the cut Dan
approved (rev 4 measures 37%). That is per-format config — *not* a widened bound.

## Verifying a change

```bash
python3 -m unittest discover -s .claude/skills/_shared/deliver/tests -v
python3 .claude/skills/_shared/deliver/gate.py --audit          # no format has a hole
python3 .claude/skills/_shared/qc_corpus/run.py                 # must stay green (~15 min)
```

The focused fixtures cover positive and negative PNG collisions, early/late continuous-speech
timing, present/missing/wrong and partial label states, stale hashes, invalid square/vertical
windows, clipped hair inside a declared window, fixed-wide intent, legacy ASS parsing, and the four
policy outcomes.

**`run.py` is the acceptance test for this module.** It re-runs our gates over every file Dan
rejected and every file he approved, with his words recorded, and it must fail every rejected one
and pass every approved one. No gate or setting change ships unless it passes.

## Costs, measured 2026-09-11 on this Mac

| row | cost |
|---|---|
| the picture rows together (three decodes, shared) | ~75 s for a 4-minute 1080p master |
| the five `framing:` rows (one 4 fps native decode, FaceMesh + two segmenters) | ~3–4 min for a 4-minute master on a quiet Mac |
| `compliance:banned_screen` (every frame × 28 layout templates at a 384-wide grid) | ~11 min for 4 minutes of video |
| everything else | seconds |

`compliance:banned_screen` is the expensive one and it is deliberate: a sampling scan cannot see a
single-frame violation. The email-capture form was once exposed for **exactly one frame** at 179.41 s
and a 2 fps scan stepped straight over it.

## Known gaps, stated rather than hidden

* **Legacy ASS caption clearance still lacks the old website rev 2 build plan.** Future PNG-caption
  builds use evidence contract v2: actual alpha/ink states, renderer graphic geometry, delivered-
  pixel state verification, and regression fixtures. The legacy ASS path remains intact for old
  masters and is still pending against `website-rev2` because its build assets were not preserved.
* **`compliance:banned_screen` is registered in the corpus as of 2026-09-12 (Phase 2 item 0).**
  Stage 3 tests the phone box the chrome located for the screen's own signature: **the band
  between the two chrome strips is a photograph** (white fraction ≤ 0.50, luma sd ≥ 30) — on every
  banned screen it is (0.00–0.30 white, sd 41–68) and on every look-alike it is a white panel
  (rev 4's macro tracker 0.97 / 10, Muhammad's meal screen 0.94 / 19). Each banned time is also
  classified off the source as *paired* (before/after, chrome bound 0.55) or *single* (the
  email-capture form, 0.62). ⚠ Phase 1's proposed L/R pairing test was measured and is **not** the
  discriminator: at the 384 grid a white table reads L/R 0.59 and the real before/after 0.37–0.60.
  It is recorded in the detail. ⚠ Measured on the way: **Muhammad's Ad 2 master shows the
  before/after screen at 3:11 and the email-capture screen at 3:12 and 3:23** — a live ad.
  `/ad-edit`'s and `/website-video`'s own scans are still the blind whole-screen matchers; this row
  is the one that counts.
* **`watch:pass` is a hard gate for `ad9x16` and `ad1x1` only.** Every other format carries a dated
  `pending` note and the gate prints the row as PENDING — never as a pass. Phase 3 of
  `Handoffs/handoff-20260911-video-quality-engine.md` turns it on everywhere.
* **`framing:*` landed 2026-09-12 (Phase 2), composite windows landed 2026-09-16** — five rows on one tracker (`checks/framing.py`):
  mediapipe FaceMesh (plus the full-range detector for a small face) anchors the head band, Apple
  Vision person segmentation (`shorts/reference/recentre/personmask`) gives the hair top, and the
  independent top-rows test from `hairgate.py` now runs on a second segmenter (mediapipe selfie
  segmentation) instead of the 8/28 door panel's luma. Full-frame edits need no plan or set-specific
  reference; composite edits need their renderer window schedule. Evidence contract v2 crops each sample to the declared compositor window before those same
  detectors run and normalizes measurements to that window. Proven on the corpus: fails rev 2, rev 3, `v2-short3-offcentre`, `ad1-vertical-attempt1`; passes
  rev 4/5/6 and Muhammad Ad 2. Known limits: a face on a **photo card** is tracked like Dan on
  camera unless the plan declares the card (the palette filter only drops cutaways whose palette
  differs), and `personmask` is an arm64 binary that must exist on disk — the rows fail NOT MEASURED
  without it, never silently.
* **`style:coverage` for `short` is not measured on approved Shorts.** The five ab-wheel Shorts Dan
  approved are cut from Muhammad's master and have not been re-gated. The bound is borrowed from the
  lowest approved long-form-family reading and says so.

## The forks this replaces

`formats.py` and `checks/` carry the union of the rows in: `website-video/reference/recipe/qc.py`
(+ `rev1` `rev2` `rev3`), `shorts/reference/{clean-master,full-bleed,scored-source,zepbound}/qc.js`,
`longform-edit/reference/{qc_style,qc_generic,qc_with_inserts,qc_investhealth,qc_investhealth_v3}.py`,
`shortad-from-longform/reference/{qc,qc_ad2v2}.py`, `ad-edit/reference/{rev5/qc5,modern60/qc_modern}.py`,
plus `caption_sync_check.py`, `gain_flatness.py`, `landing_check.py`, `srt_validate.py`,
`content_flags.py`, `verify_cover.py`, `tailcheck.py`, the three `syncgate.py` and
`shorts/reference/recentre/delivered_gate.py`.

⚠ **They are still on disk on purpose.** Three sessions were mid-build against them when this module
landed (2026-09-11: `ad1-sq`, `ad2-sq`, `ad3-vert`, `ad4-vert`, `ad5-vert`). Deleting a live
dependency under a running build is how you lose a night's render. Each fork gets a deprecation
banner instead; they come out once those builds have delivered. **Grep for forks before assuming a
shared fix has landed** — `_shared/audio/README.md` non-negotiable 9.
