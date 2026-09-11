# Video quality engine — one gate, portable framing, the watch pass everywhere, and a locked kit

**Supersedes and merges `handoff-20260909-vqc-B-phase1-2-shared-gate-and-watch.md` and
`handoff-20260909-vqc-D-phase5-6-framing-and-junk.md` (Phase 5).** Both stay on disk as source
material and are marked superseded; everything executable from them is carried here in full, so
this document is self-contained. Written 2026-09-11 at Dan's instruction — he had four separate
video-quality handoffs and fired none of them.

**Evidence and strategy (read first, not executable):**
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md` and the private report
"The Muhammad Standard" (https://claude.ai/code/artifact/0fac6195-accb-415b-99fa-70e3825d4906).

**Fable 5.1, high effort. ~3–4 sessions. $0.00 generation spend**, plus a few cents per video for
the watch pass in Phase 3. **No dashboard row** (Dan's rule 2026-09-08).

---

## Why this exists — measured, not asserted

`.claude/skills/_shared/qc_corpus/corpus.json` holds Dan's verbatim verdicts on **our own** cuts.
**Eleven rejections**, by cause:

| cause | count | Dan's words |
|---|---:|---|
| **Audio** | **5** | *"Why do these audio problems keep happening?… Over and over again, you produce bad audio."* |
| **Framing / cropping** | **4** | *"If the video's top is cut off, it's basically not usable."* |
| Wholesale — worse than the editor's | 2 | *"truly awful"* · *"Everything about his video is better than ours"* |
| Junk footage left in | 1 | *"junk footage and repeated takes were kept in here"* |

**Audio and framing are 9 of 11.** The website video alone took **six rounds over seven days**
(09-02 → 09-09); rounds 1, 2 and 3 were all framing and audio — the same two causes three times.

**The structural reason they repeat:** across the six video skills there are **485 Python scripts,
60 of them QC/gate/delivery scripts, and exactly one shared module** (`_shared/audio/`).
`_shared/` has **no picture, framing, cut, caption or compliance module at all.** A fix lands in one
of six pipelines and the other five keep the bug — which is literally what happened on 2026-09-09,
when the spray-tan pipeline kept a forked `work/dereverb.py` and the same-day shared fix never
reached it (memory `shared-fix-may-not-reach-the-pipeline`).

**Contrast with the human editors, because it changes the fix:** Muhammad's recurring misses are
*rule-based* (a label, a loudness target, a typo). Ours are *regressions* — things that were fixed
and broke again. Pre-flight checklists fix his class of defect. Only shared code fixes ours.

---

## What VQC-A already handed you (done, commit `a696ac4`)

| | |
|---|---|
| `_shared/qc_corpus/run.py` | 14+ files Dan rejected or approved, in his own words. **Green today.** Runs `_shared/audio/selftest.sh` as its step 0 |
| **14 named checks nothing implements** | `run.py` prints them every run. **Phases 1 and 2 own eight of them** — listed per phase below |
| The NOT-MEASURED discipline | a check that did not run is a **FAILURE**, never a silent skip. Standing rule in `AGENTS.md`. Carry it into every row you write |
| A per-format precedent | `audio_gate.py --profile in-app-demo` — a **named, measured profile**, deliberately not a free `--lufs-target`. Copy that shape |
| A generic gate skeleton | `shortad-from-longform/reference/qc.py` — 20 checks, per-cut numbers in `qc.json`, missing input ⇒ NOT MEASURED ⇒ FAIL. **Lift its skeleton; do not merge it as an 18th fork** |

⚠ **`selftest.sh` is a zsh script.** `bash selftest.sh` dies on `${0:A:h}` with *"A: unbound
variable"*, which reads exactly like a real bug and is how it spent a day documented as BROKEN.
Run `zsh selftest.sh`.

**`_shared/qc_corpus/run.py` is the acceptance test for this entire handoff.** Confirm it is green
before you start and keep it green throughout. Without it this is a rewrite of ~17 gates with
nothing proving the rewrite still catches what they caught — which is exactly how checks got lost
in the forks in the first place.

---

## Build order — and the one deliberate change from the old plan

1. **Phase 1 — the shared gate.** The foundation; everything else plugs into it.
2. **Phase 2 — portable framing, INTO that gate.** ⚠ **This is the reorder.** Framing was the
   second-largest rejection cause and sat in VQC-D at the back of the queue. It moves to second so
   it lands *inside* the shared gate rather than becoming fork number 34 — which is what the old
   VQC-D itself warned about.
3. **Phase 3 — the watch pass, mandatory in all six skills.**
4. **Phase 4 — the locked kit.** Gated on 1–3 landing, and on a blind test before it spreads.

**Deliberately OUT of scope**, so a later session knows they were not forgotten:
`handoff-20260909-vqc-C-phase4-cut-technique.md` (pose-matched picture cuts, push coverage, grade)
is still open and unrun; and VQC-D's **Phase 6** junk-footage tooling stays in that document. The
one piece of Phase 6 that belongs here — the *visual* junk pass, which has no audio signature — is
folded into Phase 3's watch checklist, because that is where it can actually be caught.

---

## PHASE 1 — `_shared/deliver/gate.py`

Build the module that should have existed beside `_shared/audio`. **One gate, called by all six
skills, run on the delivered file, with per-format config — never per-video scripts.**

### Design

* `gate.py <file> --format ad9x16|ad16x9|ad1x1|longform|short|website|exercise-demo --plan plan.json`
* Rows come from config, not from copies. Where two formats genuinely differ, that is a config value
  **with a comment naming the video and the date it was measured** — the way `qc_style.py`'s
  constants already do (`MIN_COVERAGE = 0.40  # reference cut ~90%; spray tan shipped 51%; ab wheel 21%`).
* **A missing input is NOT MEASURED, which FAILS.** Never `[SKIP]`. If a check genuinely does not
  apply to a format, that is an explicit, commented config value a reader can audit — not silence.
* **No free dials.** Named profiles only. A bound that can be passed on the command line is not a bound.
* **Version the gate.** `GATE_VERSION` in the stamp; any change to a check or a bound bumps it and
  **every stamp at an older version becomes invalid.**

  ⚠ **The baseline proves this one.** `Docs/VQC_baseline_20260909.md`: **20 delivered files carry a
  PASS stamp and would fail a re-gate today**, including 16 Zepbound and supplements Shorts stamped
  2026-09-02 on the dereverb Dan rejected a week later. **139 of 166 masters carry no stamp at all.**
  Nothing re-checks a stamp when the standard moves; versioning is what makes that automatic.

### The 17 forks to fold in — 3,083 lines

| skill | forks | lines |
|---|---|---|
| `website-video/reference/recipe/` | `qc.py` + `rev1/` + `rev2/` + `rev3/qc.py` | 723 |
| `shorts/reference/` | `clean-master` · `full-bleed` · `scored-source` · `zepbound` `qc.js` | 700 |
| `longform-edit/reference/` | `qc_style` · `qc_generic` · `qc_with_inserts` · `qc_investhealth` · `_v3` | 934 |
| `shortad-from-longform/` | `qc.py` (generic) + `qc_ad2v2.py` (per-ad fork) | 520 |
| `ad-edit/reference/` | `rev5/qc5.py` · `modern60/qc_modern.py` | 206 |

Plus: `caption_sync_check.py` · `gain_flatness.py` · `landing_check.py` · the banned-screen template
scan · `srt_validate.py` · `content_flags.py` · `verify_cover.py` and `tailcheck.py` (both hardcoded
to one project's path) · `shorts/reference/*/syncgate.py` ×3 · `shorts/reference/recentre/delivered_gate.py`.

**What divergence has already cost** (each re-verified 2026-09-09, not quoted from an audit):

* `shorts/reference/full-bleed/qc.js` has **no caption-sync check and no loudness check at all**;
  `scored-source/qc.js` has **no caption-sync check**. Two of the four shorts gates cannot see a
  desynced caption.
* `ad-edit/reference/modern60/qc_modern.py` contains **exactly one `assert`**
  (`max(shots) <= 25.0`). Everything else is `print`. **It is a report wearing a gate's filename.**
* `longform-edit/reference/srt_validate.py` exists and is **invoked by nothing**.
* `ad-edit/reference/rev5/qc5.py` has no banned-screen scan, no caption clearance and no hair gate.

**Method:** for each fork, list its checks; union them; **for every check that exists in one fork and
not another, decide deliberately whether it applies to that format, and record the decision in the
config.** A check that silently exists in only one fork is the bug. Then delete the forks and grep
for survivors (`_shared/audio/README.md` non-negotiable 9: *"Grep for forks before assuming a shared
fix has landed"*).

### Two rows to add that are documented and enforced nowhere

* **Lip sync.** Every master finished with `loudnorm + alimiter` has run ~5 ms late
  (`longform-edit/SKILL.md:1362`), and the fix is written down: *"cross-correlate the finished audio
  against the source at several checkpoints — it must read 0.000 ms."* Nothing does it. The audio
  gate checks audio **length** (±0.10 s), never **alignment**.
* **Compliance.** The **Negative Events and Imagery** scan — a real Google Ads strike risk
  (`ad-edit/SKILL.md:368-384`) — is manual in every skill. Banned product screens are template-scanned
  in `/ad-edit` only, which is how a side-by-side before/after reached the delivered spray-tan
  longform for 5.6 s at 18:04. The AI-GENERATED label check exists in `qc_frame.py` for `/ad-edit`
  only, while `/make-ad` states the same requirement with no check behind it.

  ⚠ **New since these handoffs were written (Dan, 2026-09-11, now a standing rule in `AGENTS.md`):**
  Dan's REAL photos carry **"Real picture of me — not AI-generated"**; AI images of Dan carry
  **"AI-GENERATED"**. The two are mutually exclusive and **every picture of his physique carries
  exactly one of them.** Build the label row to check that pairing, not just presence.

### Two calibration items the baseline opened — solve them here, properly

1. **The exercise demos (88 files) fail `silence` and `length`, and both are format, not defect.**
   The narration ends and the rep keeps looping. VQC-A deliberately did **not** widen those rows —
   that is raising a bound. Give `exercise-demo` a format config where audio may be shorter than
   picture and a trailing tail is allowed, **with the allowance measured off the batch-1 files Dan
   approved**, and say so in the commit.
2. **One pinned reference cannot grade every programme.** Muhammad's ab-wheel edit, both Zeeshan cuts
   — and **Muhammad's own Ad 1 reference file** — fail rows graded against Ad 1's numbers (his
   reference measures −18.2 LUFS at +0.1 dBTP: too quiet and too hot for a platform). Per-format
   config plus the existing `--reference-mix` path is the answer. **Do not widen a bound to make an
   editor's cut pass.**

### Corpus checks this phase owns (5 of the 14)

```
style:coverage               ← abwheel-8-20-cut       (21% against his ~90%)
style:static_run             ← abwheel-8-20-cut       (64 s bare, twice, against Dan's 30 s rule)
captions:graphic_clearance   ← website-rev2           ("captions don't overlap graphics", a standing rule)
compliance:banned_screen     ← spraytan-longform-rev0 (the side-by-side at 18:04)
cut:uncovered_joins          ← spraytan-longform-rev0 (41 uncovered joins)
```

### Phase 1 done when

`run.py` is green **against the new gate**; those five checks are registered in its `IMPLEMENTED` map
and `run.py --strict-pending` no longer names them; every skill's delivery path calls
`_shared/deliver/gate.py`; the forks are deleted; and no SKILL.md names a QC script that does not exist.

⚠ **21 named-but-missing scripts remain**, listed in `Docs/VQC_baseline_20260909.md` §6 —
`longform-edit` 6, `youtube-packaging` 5, `coverimage` 3, `shortad-from-longform` 3, `photo-edit` 2,
and one each in `ad-edit`, `make-ad`, `revisions`, `teleprompterscripts`. Most are historical build
scripts, not check claims. **Either make each one true or delete the claim.**

---

## PHASE 2 — portable framing, inside the shared gate

### The standard being enforced (LOCKED 2026-09-08 — do not renegotiate it)

Dan, approving rev 4: *"The framing and the cropping are all looking good. You nailed it with this
one. Let's lock that in and crop all the videos like this going forward."*

Every talking-head crop is anchored to the **measured top of the hair** — never the frame, never a
skin/hairline detector. Per hold, `y0 = (the hold's minimum hair top) − 4 % of the crop height`
(~43 px of headroom at 1080p). **Two levels only** — NEAR (hair → belly button) and FAR (hair →
shorts line, waistband in frame) — alternating across visible joins. **No wide level exists.**
Delivered frames gated at hair ≥20 px below the top edge, per-hold 30–70 px, median ≤75.

### Why this is not a copy-paste

`hairgate.py` — the check that catches Dan's head being cut off — **cannot run on footage from any
other location.** It hardcodes `FF=/Volumes/Extreme/_edit_work/bin/ffmpeg`, `DAN_CX=1980`, and
depends on `hairtrack.json`'s `hdr_col`: **the static per-column luma profile of the door panel
behind Dan in the 8/28 kitchen set.** Its detector finds the hair top by climbing from skin through
the dark hair band until it reaches that door header's luma (hair ≈(26,28,25), header ≈(34,38,37)).

⚠ **Paths moved 2026-09-09:** a concurrent session split `/website-video` out of `/ad-edit`;
`hairdet.py`, `hairgate.py`, `tanpass.py`, `layout.py` and `deliver.sh` now live in
`.claude/skills/website-video/reference/recipe/`.

Why a hairline detector is not good enough: on rev 3 it read **296–300 (4K)** where the real hair top
was **196–215** — the line sat **90 px inside his hair**, his hair band is **64 px of 4K not 40**, and
**23 of 26 holds cropped the hair by 17–50 px at 1080p.** Dan: *"basically not usable."*
**Rev 3's own gate passed it at 21–95 px of "headroom" because it measured to the same wrong point.**

### The work

1. **Re-derive the hair-top detector without a set-specific background profile.** Options to
   evaluate, in order: the **mediapipe FaceLandmarker** already in `tanpass.py` (478 points, **CPU
   delegate — Metal crashes on this**) to anchor the face and search upward for the hair band; the
   **Apple Vision person segmentation** in `shorts/reference/recentre/personmask.swift` to bound the
   head region. Both are already compiled and working in this repo for other purposes.
2. **Keep test B, the detector-free top-rows test.** It is what caught rev 3 when the detector was
   wrong: the top 12 rows of the head band must not be hair-coloured — dark-pixel fraction under
   0.20; hair against the edge reads 0.5+. On rev 3's master it **failed 5371 of 5781 frames** on a
   file that had passed rev 3's own gate. **Any new detector must keep an independent check beside it.**
3. **Prove it on the known-bad file first:** it must **fail website-rev2 and website-rev3 and pass
   website-rev4**, all three already in the corpus with Dan's words attached, before it is trusted
   on anything new. It should also fail `v2-short3-offcentre` (*"one of my arms is cut off and
   there's space on the other side"*).
4. **Native-scale proof sheets.** Every proof sheet lied on rev 3 because *"at that scale a line at
   the hairline and a line at the hair top are two pixels apart."* Sheets must be native-scale and
   contrast-stretched, showing the tallest **and** median frames.
5. **Register it as a `framing:` row in `_shared/deliver/gate.py`** — not as a standalone script.

### Wire framing into the skills that have no framing rule at all

| skill | today | needed |
|---|---|---|
| **`/shortad-from-longform`** | **zero mentions** — and it re-crops Dan into vertical. **The widest gap** | full standard + delivered-file gate |
| **`/revisions`** | checklist covers punch-ins, dead air, fill — **no framing item** | a framing item, so a cut we review is checked for it |
| **`/editor-brief`** | states the quality standard to freelance editors as measurements — **framing is not among them** | the measured framing standard, in the editor's language (no tool steps — see that skill's rule) |
| `/coverimage`, `/youtube-packaging` | partial crop traps only | reference the locked standard |

Adding it to `/revisions` and `/editor-brief` is nearly free and improves the **human** editors'
output too — Muhammad has never been told this standard in measurements.

### Phase 2 done when

The framing row runs from `_shared/deliver/gate.py` on any set with no 8/28 door-panel profile;
it fails rev 2, rev 3 and `v2-short3-offcentre` and passes rev 4; `/shortad-from-longform`,
`/revisions` and `/editor-brief` carry the standard; `run.py` still green.

---

## PHASE 3 — the watch pass becomes mandatory in all six skills

Today it is a hard gate in **`/shortad-from-longform` only** (its qc check 15 reads
`logs/watch_pass.json` and refuses without it — described in that SKILL.md as *"the only way a
'watch the video' rule survives contact with a build that is running late"*). `/shorts` **mentions
it zero times**, and its own SKILL.md:971 says *"THE CONTACT SHEET IS NOT A GATE. Every framing
fault in this batch survived one."*

`watch.py`'s docstring records why it exists: *"Ad 1 attempt 1 passed 11/11 on a metric gate and Dan
rejected it: every check measured format, none ever looked at the moving picture."* That file is
corpus entry `ad1-vertical-attempt1`, and Dan's words on it are *"truly awful… definitely won't work."*

### Build

1. Port `watch.py` (now `website-video/reference/recipe/watch.py`) and `shortad`'s `a2/watch.py`
   into `_shared/deliver/watch.py`. Keep both halves: the **automated** every-frame scan (frozen runs
   `d < 0.05` at 30 fps 160×90 gray, black frames, hard discontinuities **not** at a boundary the
   beat sheet knows about) and the **by-eye** boundary strips.
2. **Keep the instrument that works: consecutive frames at −2/−1/0/+1/+2 across every boundary.**
   Two frame-difference detectors failed in a row on a real jump cut — a whole-frame gray diff scored
   it at **2.0× its local median ("clean")**, a face-region diff ranked it **12th of 28**. A 1 s
   contact sheet cannot see it, and `fps=1/N` sheets lag content by ~N/2 s (ad-edit lesson 94 —
   three false alarms in one review; grab suspect frames with exact `-ss` before calling anything a defect).
3. **Automate the first pass.** Contact sheets (~25 frames per image) checked by a model against a
   list derived from Dan's own rejections: hair at or over the top edge · head or arm out of frame ·
   junk or placeholder card · naked splice · graphic over his face · text off-screen · black frames ·
   duplicate shot · a wide level where none should exist.
   ⚠ **Frame sheets, not video-model input** — Gemini charges $0.15 per second of video, ≈$36 for one
   4-minute ad. Sheets are cents.
4. **Add the visual-junk items, which have no audio signature and therefore no scanner can find them**
   (folded in from VQC-D Phase 6; `longform-edit/SKILL.md:383`: *"The 14:30 junk (off-center
   recomposure while already talking) had NO audio signature."*): look-aways, glasses adjustments,
   drinking, recomposing. These are items 1–5 and 7 of longform's twelve mandatory passes and have
   **no automated check anywhere.** They belong on this checklist.
5. Wire `gate.py` to **fail unless `logs/watch_pass.json` names this file's sha256.**
6. Keep `shortad` Step 7b's **independent subagent audit** for anything Dan will see, and add it to
   `/ad-edit`, `/longform-edit`, `/website-video` and `/shorts`. It has twice overturned a session's
   own "this is fixed" conclusion — including catching that our eyeball reads of *"he is off to the
   left"* were **mirrored** at three of four timestamps.

### Phase 3 done when

All six skills' delivery paths refuse a file with no watch pass; **the automated pass reproduces the
known defects in the corpus** — it must flag `website-rev3`'s hair and `ad1-vertical-attempt1`'s
naked splices, both already sitting there with Dan's words attached; and the per-video cost is
recorded in `_shared/COSTS.md`.

---

## PHASE 4 — the locked kit

**Do not start this until Phases 1–3 are landed and green.** Without the gate, a kit just produces
new output nobody checks.

### The finding this is built on

From "The Muhammad Standard" (2026-09-11): **every approval of our video work came where the design
was fixed before the AI started** — the Ad 1 / Ad 2 verticals and five ab-wheel Shorts (all cut from
Muhammad's masters), and the website video once its recipe was locked after six rounds. **Every
rejection came where the AI had to invent the design.**

Measured gap, picture changes per minute (ffmpeg scene > 0.25):

| | per minute |
|---|---:|
| Muhammad Ad 1 | **21.7** |
| Muhammad Ad 2 | **18.7** |
| ours (8/14 from-raw) | **9.5 / 8.9** |

His inserts sit on textured olive grid panels; ours floated on black, and word captions collided
with lower thirds. **You do not get this from a prompt. You get it from a template with the pacing
and the panel system already in it.**

### The work — one format, proven blind, then expand

1. Build the kit for **one format only** — the 9:16 vertical ad, because that is where we have
   approved output to match and the most repeat volume.
2. **Prove it by blind A/B before it spreads.** The matched pairs already exist on disk:
   * Muhammad Ad 1 vs ours — `/Volumes/Extreme/_edit_work/ad1-8-14/ad1_rev4_16x9.mp4`
   * Muhammad Ad 2 vs ours — `/Volumes/Extreme/_edit_work/ads234-8-14/c1592/ad2_16x9.mp4`
   * Zeeshan's approved ab-wheel cut vs `abwheel/r2/FINAL_ab-wheel-beats-every-crunch.mp4`
   Build a blind review page (labels hidden, order randomised) and have **Dan** pick. Do not grade
   this one ourselves — the whole failure mode being fixed is our taste judgment.
3. **Only after Dan picks ours or calls it a tie**, extend the kit to the next format. Recommended
   order from the strategy report: verticals → Shorts → long-form → hero ads last.
4. Every kit output still goes through `_shared/deliver/gate.py` and the watch pass. **The kit is
   not an exemption.**

### Phase 4 done when

One format's kit exists; a blind A/B page has been put in front of Dan with the existing matched
pairs; his verdict is recorded in the corpus as a new entry with his verbatim words, whichever way
it goes.

---

## Traps — all of them, carried from both source handoffs

* **Do not renegotiate the framing standard.** It cost four revisions and Dan locked it on 09-08.
  This work makes it portable and enforced; it does not change what "correct" means.
* **Do not "simplify" a bound while merging.** Every constant in these gates traces to a file Dan
  approved or rejected. **Carry the provenance comment with the number.**
* **Do not raise a threshold to make a build pass** (memory `audio-never-over-strip`). If a corpus
  entry fails a bound, that is the finding — report it, do not tune it away.
* **Do not add a `known_gap` to make `run.py` green.** A gap records one named check on one named
  file with a reason, a date and what clears it. **If you are adding a gap so a change can ship,
  you are relaxing a bound.**
* **Do not delete a `must_trigger` to make the run green.** If nothing implements it, it is PENDING
  — which is the point.
* Two formats have **opposite** caption rules: organic longforms carry NO burned captions (Dan,
  2026-08-27 — `qc_style.check_captions` inverts under `ORGANIC=1`), ads and shorts do. Per-format
  config, not a bug to normalise away.
* `--reference-mix` mode (shortad, when the audio is the editor's own mix) legitimately demotes six
  audio rows to informational. Preserve it; do not let it leak to formats that mix their own audio.
  **An editor's finished mix ships untouched** (`AGENTS.md`; memory `editor-audio-untouched`).
* `do_no_harm` is informational **only** where the file is genuinely not ours
  (`--reference-rows-only`, `--reference-mix`). Keep that boundary exactly where it is.
* Metal crashes the mediapipe FaceLandmarker — **CPU delegate only.**
* The head-top detector returned **0** on a JPEG-noisy photo once (photo pipeline, `blue-213`) —
  **a detector that returns a null must fail loudly, never default to "fine".**
* `personmask`-based centring **over-fires on handheld and outdoor footage**; its own note says
  *"`audit.py` is a shortlist, not a verdict."* Treat any new detector's output the same way until
  it is proven on the corpus.
* **`Media/` is gitignored.** A script that lives only there is not in the repo and enforces
  nothing — that is how `mono.py` and `ghost.py` spent weeks named as MANDATORY while being one
  `rm -rf` from gone.
* Respect `AGENTS.md`'s **two-concurrent-build cap** — check
  `ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'` before starting a gate run.
  (Measured 2026-09-11: the Mac was at load 26 with three builds running.)

---

## Starter prompt

```
Read Handoffs/handoff-20260911-video-quality-engine.md and execute it. For background read
Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md (evidence) and
Docs/VQC_baseline_20260909.md (the state of every delivered master). It supersedes the VQC-B and
VQC-D handoffs — everything executable from them is carried into this one document.

VQC-A is done (commit a696ac4). Confirm `python3 .claude/skills/_shared/qc_corpus/run.py` is green
before you start and keep it green throughout — it is the acceptance test for the whole handoff.

Four phases, in this order:
  1. _shared/deliver/gate.py — ONE version-stamped delivery gate replacing 17 per-video QC forks
     (3,083 lines), per-format config, lip-sync and compliance rows added, 5 corpus checks registered.
  2. Portable framing INTO that gate — today's hair-top check depends on the luma profile of the door
     behind Dan in the 8/28 kitchen and cannot run anywhere else. Prove it against the corpus first:
     it must FAIL website-rev2, website-rev3 and v2-short3-offcentre and PASS website-rev4. Then wire
     the standard into /shortad-from-longform, /revisions and /editor-brief, which have no framing rule.
  3. The watch pass mandatory in all six skills (it is a hard gate in one today; /shorts mentions it
     zero times), including the visual-junk items that have no audio signature.
  4. The locked kit for ONE format, proven by a blind A/B in front of Dan using the matched pairs that
     already exist on the Extreme drive. Do not start Phase 4 until 1-3 are green.

Respect the two-concurrent-build cap. Commit, push, verify. No dashboard row.
```

**Model:** Fable 5.1, high effort. ~3–4 sessions — Phases 1 and 2 are the bulk; Phase 4 should be
its own session.
