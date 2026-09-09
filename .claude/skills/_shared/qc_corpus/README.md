# `_shared/qc_corpus` — the files Dan rejected, and the files he approved

> **THE RULE (also in `AGENTS.md`):**
> **No change to any gate, threshold or setting ships unless `python3 run.py` passes.**
> It must **fail every rejected file** and **pass every approved one**.

```bash
python3 run.py                 # the audio selftest, then every gate we have, over every entry
python3 run.py --id website-rev3
python3 run.py --extract       # rebuild the git-ignored excerpt cache from the masters
python3 run.py --fingerprint   # re-record sha256 after a DELIBERATE re-render
```

## Why this exists

Every gate we own was built backwards from the last rejection, so **each new failure shipped exactly
once and the gate that caught it was never proven against the others.** Twice that produced a gate
that scored a **rejected** build as *better* than an approved one:

* **2026-09-02, audio.** `edt`, `dryness` and `floor` all improve as suppression increases, so the
  build Dan called *"absolutely awful, far far worse than before… It sounds like I'm underwater"*
  beat the build he approved on every row the gate had. It hit EDT 32 ms — **past** Muhammad's 40.
* **2026-09-08, framing.** Rev 3's own headroom gate **passed rev 3** at 21–95 px, because its
  detector read the hairline 90 px inside his hair. Dan: *"basically not usable."*

Both files are in the corpus. A gate change that resurrects either one cannot ship.

The pattern is not new — it is generalised from two places it already worked. `selftest.sh` requires
PASS on the approved website rev 2 and FAIL on the rejected rev 1. `hairgate.py` was proven on rev 3's
master first, where its detector-free test B **failed 5371 of 5781 frames on a file that had passed
rev 3's own gate.** This is that, for every gate and every rejection.

## What an entry holds

`corpus.json`, one object per file:

| field | |
|---|---|
| `verdict` | `rejected` · `approved` · `approved-with-notes` · `reference` |
| `dan` | **his own words, verbatim.** The corpus is his standard, not our paraphrase of it |
| `must_trigger` | checks that must **FAIL** this file |
| `must_pass` | checks that must **PASS** it |
| `measured` | the numbers behind the verdict |
| `sha256` | of the master. A file that no longer matches is not the file he judged |
| `excerpt` | `[start, seconds]` — the failing span, for the git-ignored cache |
| `known_gap` | one named check, known to fail, with the reason, the date and what clears it |

## The five outcomes, and what each one means

| | meaning | what to do |
|---|---|---|
| `ok` | the gate agreed with Dan | nothing |
| **`BLIND`** | **a rejected file now PASSES** — the gate cannot see something he rejected on | **add the row that sees it. Never relax anything** |
| **`TIGHT`** | **an approved file now FAILS** — the gate will block good work | read it before touching a bound (see below) |
| `gap` | a recorded `known_gap` is still failing | nothing; it prints every run so it stays visible |
| `STALE!` | a `known_gap` has healed | delete it from `corpus.json` |
| `...` | `--strict-pending`: a `must_trigger` names a check nothing implements | build the check |
| `----` | the file is not on disk (usually: the Extreme SSD is unmounted) | mount it, or accept the smaller run |

⚠ **`TIGHT` is not automatically a bug.** The `do_no_harm` row "over-tightened" onto 16 of 16 shipped
Shorts on 2026-09-09 and was **correct** — those Shorts should never have gone out. A `TIGHT` that
names a file **Dan praised** is a bug in the gate. A `TIGHT` that names a file which shipped without
him seeing it is a finding about the file.

⚠ **A `PENDING` is not a pass.** It is a rejection that nothing can currently catch. The list run.py
prints at the end is the Phase 1–6 build queue, in priority order by how many rejections it covers.

## `known_gap` — a recorded gap, and how it differs from a bypass

Four entries carry `audio_gate:do_no_harm` as a `known_gap`: they were rendered before `voice_chain`
started stashing the untreated signal, so there is no baseline to compare against, the row reads
NOT MEASURED, and Phase 0 correctly made that a FAIL. That is a fact about the files' history, not
about their audio.

A gap is not a bypass, and must never become one:

* it names **one check on one file**, never a class;
* it carries **why**, a **date**, and the condition that **clears** it;
* it is **printed in full on every run** — you cannot forget it is there;
* **every other check on that file still gates** — a new failure is still a MISMATCH;
* run.py **detects when a gap heals** and tells you to delete it (`STALE!`).

**If you are adding a gap so that a change can ship, you are relaxing a bound. Stop.**

## Hard rules

1. **Never raise a threshold to make an entry pass** (memory: `audio-never-over-strip`). If an entry
   fails a bound, that is the finding.
2. **Never delete a `must_trigger` to make the run green.** If nothing implements it, it is PENDING —
   which is the point.
3. **Never commit a master.** This repo is public (memory: `repo-is-public`). `corpus.json` holds the
   path and the sha256; `excerpts/` is git-ignored and regenerates with `--extract`.
4. **A new rejection becomes an entry in the same session it happens**, with his words, before the fix
   is built. That is the only moment the quote and the measurement are both to hand.
5. **A new approval becomes an entry too.** Half of this corpus's value is stopping a gate from
   blocking good work.

## Adding an entry

```jsonc
{ "id": "short-slug", "verdict": "rejected", "date": "2026-09-09",
  "root": "repo",                       // or "ssd" for /Volumes/Extreme/_edit_work
  "path": "…/the file.mp4",
  "excerpt": [235, 30],                 // the failing span
  "dan": "his words, verbatim",
  "must_trigger": ["audio_gate:artifacts", "framing:hair_top"],
  "measured": "the numbers behind the verdict",
  "notes": "what the pipeline got wrong, and where the lesson now lives" }
```

Then `python3 run.py --fingerprint` and `python3 run.py --extract`.

Check names are `family:row`. `audio_gate:*` are the row keys `audio_gate.py` emits. Everything else
(`framing:` `cut:` `junk:` `style:` `captions:` `compliance:` `music:`) is PENDING until the phase
that owns it lands — see `IMPLEMENTED` and `PENDING_OWNER` at the top of `run.py`.

## Where this sits

Programme: `Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.
Phase 0 + 3 (this): `Handoffs/handoff-20260909-vqc-A-phase0-3-bypasses-and-corpus.md`.
The Phase 0 re-gate of every delivered master: `Docs/VQC_baseline_20260909.md`.
