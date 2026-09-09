# VQC-D — Phase 5 + Phase 6: portable framing, and the junk-footage tools wired together

**Part 4 of 4 of the video-quality programme.** Evidence and the full plan:
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.

**Run after VQC-A.** Ideally after VQC-B too, so the new checks land in the shared gate rather than
becoming fork number 34. **Fable 5.1 or Opus 5, high effort. ~1–2 sessions. $0.00 generation spend.**

---

## PHASE 5 — make the framing check work on any set

### Why this is not a copy-paste

`hairgate.py` — the check that catches Dan's head being cut off — **cannot run on footage from any other
location.** It hardcodes `FF=/Volumes/Extreme/_edit_work/bin/ffmpeg`, `DAN_CX=1980`, and depends on
`hairtrack.json`'s `hdr_col`: **the static per-column luma profile of the door panel behind Dan in the
8/28 kitchen set.** Its detector finds the hair top by climbing from skin through the dark hair band
until it reaches that door header's luma (hair ≈(26,28,25), header ≈(34,38,37)).

⚠ **Paths moved 2026-09-09:** a concurrent session split `/website-video` out of `/ad-edit`;
`hairdet.py`, `hairgate.py`, `tanpass.py`, `layout.py` and `deliver.sh` now live in
`.claude/skills/website-video/reference/recipe/`.

### The standard being enforced (LOCKED 2026-09-08, do not renegotiate it)

Dan, approving rev 4: *"The framing and the cropping are all looking good. You nailed it with this one.
Let's lock that in and crop all the videos like this going forward."*

Every talking-head crop is anchored to the **measured top of the hair** — never the frame, never a
skin/hairline detector. Per hold, `y0 = (the hold's minimum hair top) − 4 % of the crop height`
(~43 px of headroom at 1080p). **Two levels only** — NEAR (hair → belly button) and FAR (hair → shorts
line, waistband in frame) — alternating across visible joins. **No wide level exists.** Delivered frames
gated at hair ≥20 px below the top edge, per-hold 30–70 px, median ≤75.

Why a hairline detector is not good enough: on rev 3 it read **296–300 (4K)** where the real hair top was
**196–215** — the line sat **90 px inside his hair**, his hair band is **64 px of 4K not 40**, and
**23 of 26 holds cropped the hair by 17–50 px at 1080p.** Dan: *"basically not usable."* **Rev 3's own
gate passed it at 21–95 px of "headroom" because it measured to the same wrong point.**

### The work

1. **Re-derive the hair-top detector without a set-specific background profile.** Options to evaluate,
   in order: the **mediapipe FaceLandmarker** already in `tanpass.py` (478 points, **CPU delegate —
   Metal crashes on this**) to anchor the face and search upward for the hair band; the **Apple Vision
   person segmentation** in `shorts/reference/recentre/personmask.swift` to bound the head region. Both
   are already compiled and working in this repo for other purposes.
2. **Keep test B, the detector-free top-rows test.** It is what caught rev 3 when the detector was
   wrong: the top 12 rows of the head band must not be hair-coloured — dark-pixel fraction under 0.20;
   hair against the edge reads 0.5+. On rev 3's master it **failed 5371 of 5781 frames** on a file that
   had passed rev 3's own gate. **Any new detector must keep an independent check beside it.**
3. **Prove it on the known-bad file first** (lesson 109, and the VQC-A corpus exists for exactly this):
   it must fail rev 3 and rev 2 and pass rev 4 before it is trusted on anything new.
4. **Native-scale proof sheets.** Every proof sheet lied on rev 3 because *"at that scale a line at the
   hairline and a line at the hair top are two pixels apart."* Sheets must be native-scale and
   contrast-stretched, showing the tallest **and** median frames.

### Wire framing into the skills that have no framing rule at all

| skill | today | needed |
|---|---|---|
| **`/shortad-from-longform`** | **zero mentions** — and it re-crops Dan into vertical. **The widest gap.** | full standard + delivered-file gate |
| **`/revisions`** | checklist covers punch-ins, dead air, fill — **no framing item** | a framing item, so a cut we review is checked for it |
| **`/editor-brief`** | states the quality standard to freelance editors as measurements — **framing is not among them** | the measured framing standard, in the editor's language (no tool steps — see that skill's rule) |
| `/coverimage`, `/youtube-packaging` | partial crop traps only | reference the locked standard |

Adding it to `/revisions` and `/editor-brief` is nearly free and improves the **human** editors' output
too — Muhammad has never been told this standard in measurements.

---

## PHASE 6 — the junk-footage tools, run together

The detectors mostly exist, scattered across three skills' `work/` folders, and have never been run as
one pass. `junkscan.py` on a single shorts batch **"found all six of Dan's timecodes and nine more he had
not reached yet."** This is plumbing, not research.

### Promote into `_shared/cut/` and run as one report

| tool | current home | what it finds |
|---|---|---|
| `junkscan.py` | `shorts/reference/clean-master/work/` | PAUSE (gap ≥0.55 s) · SPLICE (a picture cut inherited from the source — *"every splice inside a short is a NAKED JUMP CUT unless it is hidden"*) · HEAD (slow start >0.45 s) |
| `fixonsets.py` | same | a gap ≥0.25 s **inside** a word. This is the fix for Dan's *"junk footage in the beginning at 0:01"* — a **0.95 s hesitation** Whisper swallowed inside the word "you're". On one roll: 363 onsets, 328 offsets, **51 swallowed pauses** |
| `repeat_scan.py` | `ad-edit/reference/` | *"A stretched word is a hidden restart until proven otherwise"* — every word >0.7 s, every repeated 4-gram within 25 s. **Verify each flag by re-transcribing the span in isolation** (4 s window, medium.en, `condition_on_previous_text=False`) |
| `orphan_scan.py` | `ad-edit/reference/` | speech-level energy no Whisper word covers. **It passed Dan's 0:32 repeat**, which is why `repeat_scan.py` exists — run both |
| `hard_splices.py` | `ad-edit/reference/` | which splices are **measurably** discontinuous, pre-render. On Ad 2: 135 splices, 76 measurably hard, 37 uncovered, **only 22 both** |
| `pausejump.py` | `shorts/…/work/` | how visible a *created* join is, against a 1.30 adjacent-frame baseline |

**Deliverable:** one `junk_report.json` per cut, produced before the render, listing every candidate with
its class, timecode, measurement and suggested action. It turns *"double-check everything"* into a list.

### Take selection — the part that does not exist yet

Today we **remove flubs**; we do not **pick the best take**. Rules already written down and unimplemented:

* *later-take-wins **only when the later take is fluent*** (`ad-edit/SKILL.md:434`);
* **a roll's noise floor identifies the bad take** — Dan's own *"did that plane pick up?"* measured
  −45.3 / −20.2 on the retake against ≈−48 dB elsewhere on the roll (lesson 57);
* **cut the whole restated SENTENCE, not the aborted take inside it** — v2 cut only the flub and Dan
  flagged it again, because the sentence restated "all kinds of problems" from 6 s earlier;
* **his rhetorical repeats (anaphora) are deliberate; re-INTRODUCTIONS of the same item are junk.**

### The visual junk pass has no audio signature

`longform-edit/SKILL.md:383`: *"The 14:30 junk (off-center recomposure while already talking) had NO
audio signature."* Look-aways, glasses adjustments, drinking, recomposing — items 1–5 and 7 of
longform's twelve mandatory passes have **no automated check anywhere**. These belong on the **watch
pass checklist** (VQC-B Phase 2), not in an audio scanner. Add them there.

---

## Done when

* `_shared/qc_corpus/run.py` is green, and the new framing check **fails rev 2 and rev 3 and passes
  rev 4** on its own, without the 8/28 door-panel profile.
* `/shortad-from-longform`, `/revisions` and `/editor-brief` carry the framing standard.
* One `junk_report.json` is produced for a corpus entry and reproduces the defects Dan named in it.

---

## Traps

* **Do not renegotiate the framing standard.** It cost four revisions and Dan locked it. This phase makes
  it portable and enforced; it does not change what "correct" means.
* Metal crashes the mediapipe FaceLandmarker — CPU delegate only.
* The head-top detector returned **0** on a JPEG-noisy photo once (photo pipeline, `blue-213`) — a
  detector that returns a null must fail loudly, never default to "fine".
* `personmask`-based centring **over-fires on handheld and outdoor footage**; its own note says
  *"`audit.py` is a shortlist, not a verdict."* Treat any new detector's output the same way until it is
  proven on the corpus.
* Respect the two-concurrent-build cap in `AGENTS.md`.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-vqc-D-phase5-6-framing-and-junk.md and execute it. Read
Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md first for context.

Phase 5 makes the hair-top framing check work on any set — today it depends on the luma profile of the
door behind Dan in the 8/28 kitchen and cannot run anywhere else — and wires the locked framing standard
into /shortad-from-longform, /revisions and /editor-brief, which have no framing rule at all. Prove any
new detector against the corpus first: it must fail website video rev 2 and rev 3 and pass rev 4.

Phase 6 promotes the six existing junk-footage detectors into _shared/cut/ and runs them as one report,
and adds take selection (pick the best take, not just remove flubs).

Confirm _shared/qc_corpus/run.py exists and is green first. Respect the two-concurrent-build cap.
Commit, push, verify. No dashboard row.
```

**Model:** Fable 5.1 or Opus 5, high effort.
