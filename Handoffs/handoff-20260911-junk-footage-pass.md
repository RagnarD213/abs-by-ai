# Junk-footage pass — the six detectors run as one report, plus take selection

**Extracted 2026-09-11 from `handoff-20260909-vqc-D-phase5-6-framing-and-junk.md` Phase 6**, because
that document's Phase 5 was superseded by `handoff-20260911-video-quality-engine.md` and a half-live
document is a document nobody fires. **This is the whole of the remaining Phase 6 work.** Nothing here
is carried anywhere else.

**Fire after Phase 1 of `handoff-20260911-video-quality-engine.md`** (the shared gate must exist so the
junk rows register there rather than becoming another fork). It is independent of Phases 2–4 and can run
in parallel with them. **Fable 5.1, high effort. ~1 session. $0.00 generation spend** — but it renders
and transcribes, so respect the two-concurrent-build cap in `AGENTS.md`.

---

## Why this is worth a session

Junk footage is **1 of the 11 rejections** in `_shared/qc_corpus/` — the delivered spray-tan longform,
where Dan said: *"junk footage and repeated takes were kept in here. Eliminate this junk footage."*

It is the cheapest item left in the programme. **The detectors already exist and already work** —
they are scattered across three skills' `work/` folders and have never been run as one pass.
`junkscan.py` on a single shorts batch **"found all six of Dan's timecodes and nine more he had not
reached yet."** This is plumbing, not research.

---

## Promote into `_shared/cut/` and run as one report

| tool | current home | what it finds |
|---|---|---|
| `junkscan.py` | `shorts/reference/clean-master/work/` | PAUSE (gap ≥0.55 s) · SPLICE (a picture cut inherited from the source — *"every splice inside a short is a NAKED JUMP CUT unless it is hidden"*) · HEAD (slow start >0.45 s) |
| `fixonsets.py` | same | a gap ≥0.25 s **inside** a word. This is the fix for Dan's *"junk footage in the beginning at 0:01"* — a **0.95 s hesitation** Whisper swallowed inside the word "you're". On one roll: 363 onsets, 328 offsets, **51 swallowed pauses** |
| `repeat_scan.py` | `ad-edit/reference/` | *"A stretched word is a hidden restart until proven otherwise"* — every word >0.7 s, every repeated 4-gram within 25 s. **Verify each flag by re-transcribing the span in isolation** (4 s window, medium.en, `condition_on_previous_text=False`) |
| `orphan_scan.py` | `ad-edit/reference/` | speech-level energy no Whisper word covers. **It passed Dan's 0:32 repeat**, which is why `repeat_scan.py` exists — run both |
| `hard_splices.py` | `ad-edit/reference/` | which splices are **measurably** discontinuous, pre-render. On Ad 2: 135 splices, 76 measurably hard, 37 uncovered, **only 22 both** |
| `pausejump.py` | `shorts/…/work/` | how visible a *created* join is, against a 1.30 adjacent-frame baseline |

**Deliverable:** one `junk_report.json` per cut, produced **before the render**, listing every candidate
with its class, timecode, measurement and suggested action. It turns *"double-check everything"* into a
list. Register its rows in `_shared/deliver/gate.py` so a cut with unresolved high-confidence junk fails.

---

## Take selection — the part that does not exist yet

Today we **remove flubs**; we do not **pick the best take**. The rules are already written down across
the skills and implemented nowhere:

* *later-take-wins **only when the later take is fluent*** (`ad-edit/SKILL.md:434`);
* **a roll's noise floor identifies the bad take** — Dan's own *"did that plane pick up?"* measured
  −45.3 / −20.2 on the retake against ≈−48 dB elsewhere on the roll (lesson 57);
* **cut the whole restated SENTENCE, not the aborted take inside it** — v2 cut only the flub and Dan
  flagged it again, because the sentence restated "all kinds of problems" from 6 s earlier;
* **his rhetorical repeats (anaphora) are deliberate; re-INTRODUCTIONS of the same item are junk.**

---

## Not in this document

The **visual** junk pass — look-aways, glasses adjustments, drinking, recomposing while already talking —
has **no audio signature** (`longform-edit/SKILL.md:383`: *"The 14:30 junk (off-center recomposure while
already talking) had NO audio signature"*). No scanner can find it. Those items moved to the watch-pass
checklist in `handoff-20260911-video-quality-engine.md` Phase 3. **Do not rebuild them here.**

---

## Done when

* The six tools live in `_shared/cut/` and are called from one entry point.
* One `junk_report.json` is produced for the corpus entry `spraytan-longform-rev0` and **reproduces the
  defects Dan named in it** — that file is in the corpus with his words attached, and it is the test.
* Take selection is implemented with the four rules above, and its choices on a real roll are shown to
  Dan as a list before a cut is built on them.
* `_shared/qc_corpus/run.py` is still green.

---

## Traps

* **Do not re-render any delivered master.** Work in a scratch copy — `AGENTS.md`: *never run a pipeline
  script inside another session's live build directory.*
* **0.55–0.65 s is breathing rhythm, not dead air** (`shorts/SKILL.md:445`). Do not strip it.
* **A pause removal is itself as visible as the fault it fixes** — measured at **4.97–12.46** against a
  **1.30** adjacent-frame baseline (`pausejump.py`). Every removal needs a picture cut or an insert over
  it. The picture-cut half of that is `handoff-20260909-vqc-C-phase4-cut-technique.md` item 1.
* **`orphan_scan.py` alone is not enough** — it passed Dan's 0:32 repeat. Run `repeat_scan.py` beside it.
* Verify every `repeat_scan.py` flag by re-transcribing that span in isolation before acting on it.
* **`Media/` is gitignored** — a script that lives only there enforces nothing.
* Respect the **two-concurrent-build cap** in `AGENTS.md`.

---

## Starter prompt

```
Read Handoffs/handoff-20260911-junk-footage-pass.md and execute it. This is the extracted Phase 6 of the
old VQC-D handoff; Phase 5 of that document is superseded and must not be run.

Six junk-footage detectors already exist and work, scattered across three skills' work/ folders, and have
never been run as one pass. Promote them into _shared/cut/, run them as one junk_report.json produced
before the render, and register its rows in _shared/deliver/gate.py. Then implement take selection, which
does not exist at all today -- we remove flubs but never pick the best take.

The test is corpus entry spraytan-longform-rev0 ("junk footage and repeated takes were kept in here"):
the report must reproduce the defects Dan named in it. Confirm _shared/qc_corpus/run.py is green first and
keep it green. Work in scratch copies. Respect the two-concurrent-build cap. Commit, push, verify.
No dashboard row.
```

**Model:** Fable 5.1, high effort.
