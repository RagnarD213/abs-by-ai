# VQC baseline — what would not ship today

**Measured 2026-09-09**, Phase 0 of the video-quality programme
(`Handoffs/handoff-20260909-vqc-A-phase0-3-bypasses-and-corpus.md`). The current gates, re-run over
**every delivered master in the project** — 166 files, 21.6 GB — after the seven Phase 0 changes
closed the bypasses.

**Measurement only. Nothing here was fixed, and no file's stamp was changed** (`--no-stamp`
throughout). The handoff says to expect a long list; it is long, and most of it is one of four
causes, not 159 separate defects.

```
                    files   pass   fail
exercise demos         88      0     88
shorts                 56      6     50
longform               13      1     12
editor cuts             6      0      6
ads / website           3      0      3
                      ---    ---    ---
                      166      7    159
```

## Read this before reading the numbers

**159 of 166 failing is not 159 bad videos.** Four causes account for essentially all of it, and only
one of them is "our audio is wrong":

| files | cause | is it a real defect? |
|---:|---|---|
| **88** | exercise demos fail `silence` + `length` — the VO deliberately ends before the loop does | **no** — the gate has no in-app-demo shape for those two rows |
| **71 of 78** | `do_no_harm` reads NOT MEASURED, because the file predates the untreated-baseline stash (2026-09-09). (Separately, **139 of 166 carry no stamp at all**) | **no** — a fact about the file's history; Phase 0 correctly made "nobody looked" a FAIL |
| **6** | editor cuts and Muhammad's own reference fail rows graded against **Ad 1's** pinned numbers | **no** — one pinned reference cannot grade a different programme |
| **62** | **our own Shorts and longforms fail `tone` / `floor` / `artifacts` / `lufs`** | **YES** |

The last row is the finding.

---

## 1. The seven that pass

```
Short-form video content/tan-short1..6_*.mp4          (spray tan, re-rendered 2026-09-09)
claude edited long form content/04 …/FINAL_invest_health.mp4   (re-rendered 2026-09-09)
```

**Every file that passes today was re-rendered in the last 24 hours**, through the shared chain, on
the settings Dan picked by ear. That is the useful half of this report: **the standard is reachable —
6 of 6 spray-tan Shorts clear all eleven rows, including `do_no_harm`.** Nothing older does.

## 2. Our own audio: 50 Shorts and 12 longforms fail on substance

Not the legacy gap — rows that measure the sound.

| batch | files | fails |
|---|---:|---|
| **V2 / V3 / V6 cutdowns** | 23 | `tone` 23, `floor` 23, `lufs` 21, `tp` 7, `artifacts` 6, `edt` 5 |
| **Zepbound (09-02 build)** | 8 | `artifacts` 8 — **the dereverb Dan called "underwater"** |
| **supplements (09-02 build)** | 8 | `artifacts` 8 — same |
| **ab-wheel Shorts** | 5 | `tone` 5, `artifacts` 5, `floor` 4 |
| other Shorts | 6 | `tone` 6, `tp` 4, `artifacts` 4, `lufs` 4 |
| **longform 01 / 02 / 03 / 05** | 4 | `tone`, `floor`, `spread`, `dryness` on all four |

**The 16 Zepbound + supplements Shorts are already owned** by
`Handoffs/handoff-20260909-audio-match-muhammad.md` (parked behind the long-form hold). **The 23
V2/V3/V6 cutdowns and the 4 longforms are not owned by anything** — and 21 of the 23 cutdowns miss
−14 LUFS, which is a platform-loudness miss on files that are already published.

⚠ Everything in this section is a **statement, not a work order.** Re-rendering is out of scope here
and two other handoffs own parts of it.

## 3. Twenty files carry a PASS stamp and would fail a re-gate today

The clearest argument for Phase 1's **versioned gate**: a stamp records a verdict at a moment, and
nothing ever re-checks it when the standard moves.

* 16 Zepbound + supplements Shorts — stamped PASS on 2026-09-02 on the dereverb rejected on 09-09
* `this picture got me abs | claude | 9x16 | ad 1.mp4`, both website-video masters — `do_no_harm` only
* Muhammad's Ad 2 16x9 — measured against Ad 1's reference (see §5)

**139 of 166 delivered masters carry no stamp at all.** Most predate the standard; the exercise demos
have none because the old instruction was to pass `--no-stamp` when the loudness row failed — closed
in Phase 0.

## 4. The exercise demos need a format, not a fix (88 files)

Every one fails exactly two rows, and only those two:

```
FAIL  nothing missing: 1 digitally silent second(s)
FAIL  audio 17.164 s vs picture 20.125 s (within 0.1 s)
```

The narration ends and the rep keeps looping. That is the format, and it is what Dan approved. The
loudness row is already handled — the new `--profile in-app-demo` (−24 ±1.5 LUFS, from batch 1's
approved −23.9 / −24.2) passes them at −22.7.

**Recommendation, not done here:** extend the `in-app-demo` profile so `length` allows audio shorter
than picture and `silence` allows a trailing tail, both measured off the batch-1 files Dan approved.
**Deliberately not done in this session** — that is raising a bound, and the rule is that a bound moves
only against a file Dan has actually approved, with him told. The 88 files stay on the list until then.

## 5. One pinned reference cannot grade every programme (6 files)

Muhammad's ab-wheel edit, Zeeshan's ad and Zeeshan's ab-wheel edit all fail `tone` / `floor` /
`artifacts` / `lufs` against Ad 1's pinned reference. **Muhammad's own Ad 1 16x9 — the reference
file — fails `lufs` and `tp`** (−18.2 LUFS at +0.1 dBTP: too quiet and too hot for a platform).

That is not a defect in their work and not a bug in ours. It is the limit of grading every programme
against one 60-second ad: a different room, a different bed, a different target loudness. Phase 1's
per-format config is the answer; `--reference-mix` already handles the case where we carry an editor's
mix verbatim.

## 6. Named-but-missing scripts — the four the handoff listed are fixed; 21 more exist

A sweep of every `foo.py` / `.js` / `.sh` named in a SKILL.md: **312 names across 18 skills, 25 not
found on disk.** The four the handoff named are closed:

| | was | now |
|---|---|---|
| `shortad-from-longform/reference/qc.py` | referenced 5×, **did not exist** | **written** — generic, 20 checks, per-cut numbers in `qc.json` |
| `exercisegeneration`'s `qc.py` | referenced, **did not exist** | **written** at `exercisegeneration/reference/qc.py`, ids are arguments |
| `_r2/mono.py`, `_r2/ghost.py` | named **MANDATORY**, lived only in **gitignored** `Media/exercise-demos/_r2/` | **promoted** to `exercisegeneration/reference/` |

The remaining 21 are historical build scripts named as "how we did it", not as enforced checks —
`longform-edit` (6), `youtube-packaging` (5), `coverimage` (3), `shortad-from-longform` (3),
`photo-edit` (2), and one each in `ad-edit`, `make-ad`, `revisions`, `teleprompterscripts`.
**Worth a pass in Phase 1**, on the same rule: a SKILL.md must not assert a check nothing performs.

> **RESOLVED 2026-09-11 (Phase 1).** Re-swept with a resolver that actually follows cross-skill
> paths (`_shared/audio/pick_lav.py` is real; the first sweep looked for it inside the naming
> skill and counted it missing). **312 names, 10 genuinely absent** — and none of the ten is a
> check claim:
>
> | name | what the SKILL.md actually says |
> |---|---|
> | `auto_grade.py`, `pack_transcripts.py`, `timeline_view.py` (longform-edit) | historical build scripts; `timeline_view.py` is written up as **optional** |
> | `veincomp2.py` (photo-edit) | cited as a **pattern** to follow, not a script to run |
> | `prep.sh`, `framediff.sh` (revisions) | per-batch scratch scripts, written fresh in each review's work dir on the SSD |
> | `p1_landing3.py`, `p1_pananalyse3.py` (shortad) | one audit's own scratch scripts; the builder-side version it points at, `landing_check.py`, **does exist** |
> | `zlib.py` (shortad) | named as a **trap** — "never name a module after the stdlib" — i.e. a file that must NOT exist |
> | `setclip.sh` (teleprompterscripts) | generated by the command printed on the line above it |
>
> So Phase 1's condition *"no SKILL.md names a QC script that does not exist"* is met: every QC and
> gate script named anywhere is on disk. Re-run the sweep with the resolver in this session's
> commit message if you want to check it again.

---

## What Phase 0 actually changed

| | change | proof |
|---|---|---|
| 1 | `require_stamp.py` is **strict by default** — a `--synthetic` stamp no longer satisfies a camera-audio caller. The old opt-IN `--strict` was passed by **no SKILL.md anywhere**, which is what made it useless. `--allow-synthetic` is the explicit opt-in for `make-ad` / `exercisegeneration` / `findassets` | selftest step 8 |
| 2 | The **only instructed bypass in the repo** is gone (`exercisegeneration/SKILL.md`: *"pass `--no-stamp` if the row fails"*). Replaced by a measured `--profile in-app-demo` (−24 ±1.5 LUFS) — a **named profile, never a free `--lufs-target`**, because a dial that makes a build pass is not a gate | pullup demo now passes loudness at −22.7 |
| 3 | `do_no_harm` **NOT MEASURED is a FAIL**, not `ok=True`. It is informational only where the file is genuinely not ours (`--reference-rows-only`, `--reference-mix`) | selftest step 7; 139 files on this list |
| 4 | `qc_style.py` `check_captions` / `check_splices` **fail as NOT MEASURED** instead of printing `[SKIP]`. Three-state, not boolean: `--talking-head` / `--not-talking-head`, `--plan` / `--no-joins` — so "we forgot" can never look like "it does not apply" | `qc_style.py --help` |
| 5 | Four named-but-missing scripts written or promoted (§6) | `qc.py --help` on both |
| 6 | `selftest.sh` **was never broken.** It is a **zsh** script; `bash selftest.sh` dies on `${0:A:h}` with *"A: unbound variable"* — indistinguishable from a real bug, and how it spent a day documented as broken in the README. It now refuses the wrong shell, and gained two checks | **19/19 PASS in ~90 s** |
| 7 | `AUDIO_UNGATED=1` removed from all seven `composite_*.py`. An env var set once in a shell silently disarms a tripwire for everything that shell runs afterwards and leaves no mark on the file. Correct order: finish and gate the audio, then composite | `grep AUDIO_UNGATED` → nothing live |

**Phase 3 shipped alongside:** `.claude/skills/_shared/qc_corpus/` — 14 entries in Dan's verbatim
words, `run.py` green, `selftest.sh` folded in as its step 0, and the standing rule in `AGENTS.md`.
It names **14 checks that nothing implements yet** — that list is the Phase 1–6 build queue.

## Method, so this can be re-run

* Set: every finished file the pipeline handed to Dan or a platform, under `claude edited long form
  content/`, `Website Videos/`, `Short-form video content/`, `YouTube Long Form Video Content/`,
  `Muhammad Ad Videos/`, `Zeeshan Ad Videos/`, `Media/exercise-demos/`. Excluded: `_pre-*` rollbacks,
  `working files/`, `CUT_*`, `*_PRE_*`, `ROLLBACK`, `SUPERSEDED`, review proxies and A/B clips.
* `_shared/audio/audio_gate.py --no-stamp` on each; exercise demos additionally
  `--synthetic --profile in-app-demo`.
* **Two workers, never more** (`AGENTS.md`: two concurrent video builds; gating is ffmpeg-bound).
  166 files in ~11 minutes.
* **No picture gate was run**: `qc_style.py` needs a per-video `--plan` and `--srt` that do not exist
  for delivered files, and there is no shared framing, cut or caption module at all yet. **So this
  report measures audio only — the framing, jump-cut and junk-footage defects Dan named are not in
  these numbers, and nothing in the repo can currently measure them across a delivery set.** That is
  Phases 1, 4, 5 and 6.
