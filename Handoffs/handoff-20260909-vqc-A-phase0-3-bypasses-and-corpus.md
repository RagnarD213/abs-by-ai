# VQC-A — Phase 0 + Phase 3: close the bypasses, build the regression corpus

**Part 1 of 4 of the video-quality programme.** Evidence, diagnosis and the full six-phase plan:
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md` — **read it first, it is the why.**

**Run this one FIRST.** These two phases are what stop the same defects recurring; every later phase
depends on the corpus existing. **Opus 5, high effort. ~1–2 sessions. $0.00 generation spend.**

---

## Goal

1. **Phase 0** — every quality check we already paid for stops being optional.
2. **Phase 3** — a corpus of Dan's rejected and approved files, and the rule that no gate change ships
   unless it fails every rejected file and passes every approved one.

Dan, 2026-09-09, on the pipeline's output: *"far below the quality the human editors have made… I'm not
actually going to ship anything that we made."* Four named defects: audio, framing, jump cuts, junk
footage. This handoff does not fix those directly — it makes it impossible for a fixed one to come back.

---

## PHASE 0 — close the bypasses

No new machinery. Seven changes.

1. **`--strict` everywhere.** `_shared/audio/require_stamp.py:47` defaults `synthetic_ok=True`, so a
   weakened 4-row `--synthetic` stamp satisfies a caller that wanted the full 11-row gate. **No SKILL.md
   passes `--strict` anywhere.** Make `--strict` the default and add an explicit `--allow-synthetic` for
   the AI-voice skills (`make-ad`, `exercisegeneration`, `findassets`) that legitimately need it. Update
   every caller found by `grep -rl require_stamp .claude/skills/`.
2. **Delete the instructed bypass.** `exercisegeneration/SKILL.md:225-227` says *"report loudness rather
   than fail on it (pass `--no-stamp` if the row fails and note it in the delivery)."* Remove it. If
   synthetic-voice loudness genuinely cannot hit −14 LUFS, add a `--synthetic` row with its own measured
   bound — do not let the file ship unstamped.
3. **`do_no_harm` must not pass when it did not measure.** `_shared/audio/audio_gate.py:150-156` appends
   `ok=True, not_measured=True` when no untreated baseline was stashed. Flip to FAIL with a message
   naming `common.stash_untreated()`. ⚠ Legacy stamps will start failing — that is correct and is the
   input to Phase 3's corpus.
4. **Silent skips become failures.** In `longform-edit/reference/qc_style.py`: `check_captions` returns
   silently unless the caller passes `--talking-head`; `check_splices` returns silently without
   `--plan`. Both must FAIL with "not measured". (`check_pace` already fails without `--srt` — match it.)
5. **A named script that does not exist is an error, not a no-op.** Missing today:
   `shortad-from-longform/reference/qc.py` (its SKILL.md references it 5×; the only real file is
   `qc_ad2v2.py`, a per-ad fork with `TARGET = 276.109167` and `V = 'ad2v2_vertical_9x16.mp4'`
   hardcoded), `exercisegeneration`'s `qc.py`, and `_r2/mono.py` + `_r2/ghost.py` (named as **MANDATORY**
   rules). For each: either write it, or delete the claim that the rule is enforced. **Do not leave a
   SKILL.md asserting a check that nothing performs.**
6. **Fix `_shared/audio/selftest.sh`** — documented broken in `_shared/audio/README.md:21` (unbound
   variable + pre-09-08 reference paths). This is the working example of the Phase 3 pattern; it must run
   before you can extend it. Verify `common.stash_untreated()` exists and `voice_chain.py:158` resolves.
7. **Remove `AUDIO_UNGATED=1`** from `longform-edit/reference/composite_*.py`.

### Phase 0 done when

`selftest.sh` passes, and you have re-run the **current** gates over every delivered master in the
project and produced a report of what would not ship today. **Expect that list to be long — that is the
finding, not a failure.** Put the report at `Docs/VQC_baseline_20260909.md`. Do not fix any of the
files it names in this session.

⚠ Respect `AGENTS.md`'s **two concurrent video builds** cap while re-gating — check
`ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'` first. Gating is ffmpeg-bound.

---

## PHASE 3 — the regression corpus

**The rule:** no change to any gate ships unless it **fails every rejected file** and **passes every
approved file**. Build it at `.claude/skills/_shared/qc_corpus/`.

The pattern already exists and works — `selftest.sh` requires PASS on website rev 2 and FAIL on rev 1;
`hairgate.py` was proven on rev 3's master first, where its detector-free test B **failed 5371 of 5781
frames on a file that had passed rev 3's own gate.** Generalise that.

### Structure

`corpus.json` — one entry per file: path, sha256, verdict (`rejected` / `approved` / `reference`), the
date, **Dan's own words**, and `must_trigger`: which check(s) must fire. Store a short excerpt (the
failing 20–30 s) rather than the full master where the file is large; record the full path too.

### Seed entries

| file | verdict | must trigger |
|---|---|---|
| website video rev 1 | rejected | a wide level exists; audio |
| website video rev 2 | rejected | headroom 159–261 px, median 201 |
| website video rev 3 | rejected | hair cut in 23 of 26 holds, 17–50 px @1080p |
| website video rev 4 | **approved** | nothing — *"You nailed it"* |
| Ad 1 vertical attempt 1 | rejected | 23 of 72 splices naked; 100 % of talk at one fixed crop |
| spray-tan longform | rejected | junk at 4:00; 41 uncovered joins; side-by-side at 18:04 |
| spray-tan Shorts (09-02 build) | rejected | artifacts — *"sounds like I'm underwater"* |
| 04 invest-health | rejected | artifacts, flux 1.31× his |
| `v2-short3_supplements-3-percent` | rejected | off-centre, arm cut (torso centre wandered 0.411→0.505) |
| ab-wheel 8/20 cut | rejected | coverage 8.7 % |
| website video rev 5 | approved-with-notes | record the 6 rev-6 items; do not gate on them |
| Muhammad ad 1 + ad 2 16x9 | **reference** | must pass everything we hold ourselves to |

Recover exact quotes from `Handoffs/handoff-20260902-website-video-rev2.md`,
`…-rev3.md`, `handoff-20260908-website-video-rev4.md`, `handoff-20260821-spraytan-rev1.md`,
`AI_COORDINATION_ARCHIVE.md` (search "truly awful", "junk footage", "underwater"), and
`revision docs/`. **Use Dan's words verbatim** — the corpus is his standard, not our paraphrase of it.

### Runner

`_shared/qc_corpus/run.py` — runs the current gates over every entry and asserts the verdict matches.
Exit non-zero on any mismatch. Two failure modes to report distinctly:

* **a rejected file now passes** → the gate is blind to something Dan rejected (this is the audio-gate
  failure of 09-02, where every row rewarded more suppression and the build he hated scored *better*);
* **an approved file now fails** → the gate is over-tight and will block good work (this is the 09-09
  do-no-harm row blocking 16 of 16 shipped shorts — correct there, but the same signal must be
  distinguishable from a false positive).

### Phase 3 done when

`run.py` is green, `selftest.sh` is folded into it, and **`AGENTS.md` carries a new standing rule**:
*no gate or setting change ships without `_shared/qc_corpus/run.py` passing.* Add a line to
`_shared/audio/README.md` pointing at it.

---

## Traps

* **The corpus is a picture-and-audio corpus.** Some rejected files are 1 GB. Store excerpts + sha256 of
  the full file; never commit masters (repo is public — memory `repo-is-public`).
* **Do not re-render anything in this session.** Two other audio re-render handoffs are open
  (`handoff-20260909-audio-match-muhammad.md`, `handoff-20260909-invest-health-audio-rerender.md`) and
  own those files. This handoff only measures.
* **Never raise a threshold to make a build pass** (`memory: audio-never-over-strip`). If a corpus entry
  fails a bound, that is the finding.
* A concurrent session split `/website-video` out of `/ad-edit` on 2026-09-09 and moved `hairdet.py`,
  `hairgate.py`, `tanpass.py`, `layout.py`, `deliver.sh` to
  `.claude/skills/website-video/reference/recipe/`. Use that path.

---

## Starter prompt

```
Read Handoffs/handoff-20260909-vqc-A-phase0-3-bypasses-and-corpus.md and execute it end to end
(Phase 0 then Phase 3). Read Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md first for
the evidence behind it.

Phase 0 is seven small changes that stop our existing quality checks from being skippable — the list is
in the doc. Then re-run the current gates over every delivered master and write the baseline report to
Docs/VQC_baseline_20260909.md. Do not fix the files it names.

Phase 3 builds .claude/skills/_shared/qc_corpus/ from the seed table in the doc, using Dan's verbatim
words, plus run.py and the standing rule in AGENTS.md.

Respect the two-concurrent-build cap in AGENTS.md. Commit, push, verify. No dashboard row.
```

**Model:** Opus 5, high. **Spend:** $0.00.
