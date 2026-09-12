> ✅ **EXECUTED 2026-09-12.** Item 0 (banned-screen stage 3), the portable framing tracker, the five
> `framing:` rows, the corpus registration and the skill wiring are all in. Results and the two
> findings are recorded in the "✅ PHASE 2 EXECUTED" section of
> `handoff-20260911-video-quality-engine.md`. Kept on disk as the record of what was asked.

# Phase 2 — portable framing, inside the shared gate

**This is Phase 2 of `Handoffs/handoff-20260911-video-quality-engine.md`, extracted as its own
fireable document at Dan's request (2026-09-11).** Phase 1 is done and pushed (`eff3896`,
`5e10200`); read its "✅ PHASE 1 EXECUTED" section in that doc before starting — it records what
landed, what did not, and why.

**Fable 5.1, high effort. ~2 sessions. $0.00 generation spend.** No dashboard row (Dan's rule
2026-09-08).

---

## Why this is second, and why it is not a copy-paste

**Framing is 4 of Dan's 11 recorded rejections** — the second-largest cause after audio, and the
website video burned three of its six rounds on it. He locked the standard on 2026-09-08:

> *"The framing and the cropping are all looking good. You nailed it with this one. Let's lock that
> in and crop all the videos like this going forward."*

The check that enforces it, `website-video/reference/recipe/hairgate.py`, **cannot run on footage
from any other location.** It hardcodes `FF=/Volumes/Extreme/_edit_work/bin/ffmpeg`, `DAN_CX=1980`,
and — the real blocker — it depends on `hairtrack.json`'s `hdr_col`: **the static per-column luma
profile of the door panel behind Dan in the 8/28 kitchen set.** `hairdet.py` finds the hair top by
climbing from skin through the dark hair band until it reaches that door header's luma (hair ≈20–30,
header 36–37). Point it at a pool shoot, a gym, or Muhammad's master and it has no reference to
climb to.

So today the framing standard is enforced on **one set, in one skill**, and
`/shortad-from-longform` — which *re-crops Dan into vertical for every ad we ship* — has **zero
mentions of framing anywhere**.

⚠ **Why a hairline detector is not good enough, measured:** on rev 3 the hairline read **296–300
(4K)** where the real hair top was **196–215** — the line sat **90 px inside his hair**, his hair
band is **64 px of 4K, not 40**, and **23 of 26 holds cropped the hair by 17–50 px at 1080p**. Dan:
*"basically not usable."* **Rev 3's own headroom gate PASSED it at 21–95 px of "headroom", because
it measured to the same wrong point.** That file is corpus entry `website-rev3` and it is your
primary test.

---

## The standard being enforced — LOCKED, do not renegotiate it

It cost four revisions. This work makes it **portable and enforced**; it does not change what
"correct" means.

* Every talking-head crop is anchored to the **measured top of the hair** — never the frame, never
  a skin/hairline detector.
* Per hold, `y0 = (that hold's minimum hair top) − 4 % of the crop height` (~43 px of headroom at
  1080p).
* **Two levels only** — NEAR (hair → belly button) and FAR (hair → shorts line, waistband in frame),
  alternating across visible joins. **No wide level exists.**
* Delivered frames gated at hair **≥ 20 px** below the top edge, **30–70 px** per hold, **median
  ≤ 75**.

---

## What Phase 1 handed you

| | |
|---|---|
| `_shared/deliver/gate.py` | the runner. Add a row by writing the function in `checks/`, adding one line to `ROWS`, and adding the key to `formats.ALL_ROWS` |
| `_shared/deliver/formats.py` | **the only place a bound may live**, beside the file and date it was measured on. `gate.py --audit` refuses a format that has not answered for a row |
| `checks/picture.py` | the pattern to copy: a `Picture` object that decodes the delivered file ONCE and shares it across every row. Your tracker belongs there, cached the same way |
| `common.Row` | three-state. `Row(key, None, ...)` = NOT MEASURED = FAIL. `Row.na(key, reason)` is the only legal non-run and it demands a written reason |
| `_shared/qc_corpus/run.py` | already knows how to call the gate: an entry's `"deliver": {"format": ..., "plan": ...}` block, and `IMPLEMENTED[row] = "deliver_gate"` |
| `Docs/VQC_baseline_20260909.md` | every delivered master re-gated. **No picture gate has ever been run across a delivery set** — §"Method" says so explicitly |

⚠ **Adding a row to `ALL_ROWS` makes every one of the seven formats fail as UNCONFIGURED until it
answers.** That is the design. Answer each one deliberately — `exercise-demo` genuinely has no
talking head and says so in `not_applicable`; `short` and `ad9x16` very much do.

---

## The architectural point: one tracker, five rows

All five framing rows the corpus asks for are arithmetic on **one** per-frame signal. Build that
first and the rows are cheap:

```
frame t -> (head_top_y, head_height, head_centre_x, valid)      in DELIVERED pixels
```

| row | from the track | must FAIL | must PASS |
|---|---|---|---|
| `framing:hair_top` | `head_top_y` ≥ 20 px on every valid sample | `website-rev3` | `website-rev4/5/6` |
| `framing:headroom` | per-hold min in 30–70, median ≤ 75 | `website-rev2` | `website-rev4/5/6` |
| `framing:centering` | `head_centre_x` vs frame centre | `v2-short3-offcentre` | — |
| `framing:no_wide_level` | `head_height` never drops below the FAR level's size | `website-rev1` | — |
| `framing:push_coverage` | variation in `head_height` across talking time | `ad1-vertical-attempt1` | `muhammad-ad2-16x9` |

**That table is the acceptance test, and it is already encoded in `corpus.json`.** Every one of
those files is on disk with Dan's verbatim words attached.

---

## The work, in order

### 0. FIRST, and it is not framing: finish the banned-screen pairing test (~half a session)

Carried forward from Phase 1, where it was found and left honest. **It is a live Google Ads /
app-store exposure and it is the cheapest thing in this document.**

Our banned-screen scan was **blind**, and `/ad-edit`'s and `/website-video`'s still are: whole-screen
template matching matches the *recording*, not the *screen*. The banned source is one person's
generation, so ~30 % of that screen is photographs that differ in every other generation. The
spray-tan longform has carried the app's BEFORE/AFTER screen at **18:04** all along and the old
method scored it **0.526** against a 0.72 bound.

Phase 1 rebuilt it as a paired **chrome** matcher (nav/headline/BEFORE-AFTER strip + body-fat/button/
Safari strip, required to match at geometrically consistent positions). It now flags the real
violation at **0.626** on 87 of 91 frames of that beat — but approved website rev 4 reads **0.577**
across all 6,900 of its frames, because the app's chrome is shared with every other app screen. A
0.003 margin is not a bound, so the row is live but **not corpus-registered**.

**The discriminator is measured and waiting** (written up in `_shared/deliver/formats.py`, `_BANNED`):
a before/after is the same person in the same pose twice, so the photo band's left and right halves
correlate.

| | L/R correlation |
|---|---:|
| the real violation (spray tan, 18:04) | **+0.441** |
| rev 4's macro-tracker screen | +0.222 (−0.041 / −0.013 on other crops) |
| a talking-head control | −0.192 |

Require chrome **and** pairing and they separate with real margin on both axes. **Build it against
more than one frame per verdict** — Phase 1 stopped exactly because three discriminators fitted to
one good frame and one bad frame is a coincidence with code around it. Then register
`compliance:banned_screen` in `run.py`'s `IMPLEMENTED` and delete its `PENDING_OWNER` note.

### 1. Re-derive the hair-top detector with no set-specific background

Options to evaluate, **in this order** — both are already compiled and working in this repo:

1. **mediapipe FaceLandmarker** (478 points), already used by
   `website-video/reference/recipe/tanpass.py`. Anchor the face, then search upward for the hair
   band. ⚠ **CPU delegate only — Metal crashes on this** (`tanpass.py:8`).
2. **Apple Vision person segmentation**, `shorts/reference/recentre/personmask.swift`, already
   compiled at `shorts/reference/recentre/personmask` (arm64). Gives a person mask; bound the head
   region from its top.

The existing `hairdet.py` docstring is the specification of what "hair top" means in measured terms
(hair luma 20–30, band 53–78 px of 4K, the 50–110 px climb validity window). **Keep that definition.
Replace only the thing it climbs *to*** — the door panel — with a background-independent reference.

### 2. Keep test B, the detector-free top-rows test

**It is what caught rev 3 when the detector was wrong.** The top 12 rows of the head band must not
be hair-coloured — dark-pixel fraction under 0.20; hair against the edge reads 0.5+. On rev 3's
master it **failed 5,371 of 5,781 frames** on a file that had passed rev 3's own gate.

⚠ **Any new detector must keep an independent check beside it.** A gate built from the plan's own
detector inherits its bias. This is the single most important line in this document.

### 3. Prove it on the known-bad files BEFORE trusting it on anything new

Run the table above. It must fail rev 2, rev 3 and `v2-short3-offcentre`, and pass rev 4, 5 and 6.
Do not move on from a detector that gets four of six.

### 4. Native-scale proof sheets

Every proof sheet lied on rev 3 because *"at that scale a line at the hairline and a line at the
hair top are two pixels apart."* Sheets must be **native-scale and contrast-stretched**, showing the
tallest **and** median frames. `hairgate.py` already writes `pv/hair_tight*.png` /
`pv/hair_loose*.png` / `pv/hairgate_sheet.jpg` — keep that, and **look at them**.

### 5. Register them as `framing:` rows in `_shared/deliver/gate.py`

Not as a standalone script. Not as fork number eighteen.

### 6. Wire the standard into the skills that have no framing rule at all

| skill | today | needed |
|---|---|---|
| **`/shortad-from-longform`** | **zero mentions** — and it re-crops Dan into vertical for every ad. **The widest gap** | the full standard + the delivered-file gate |
| **`/revisions`** | checklist covers punch-ins, dead air, fill — **no framing item** | a framing item, so a cut we review is checked for it |
| **`/editor-brief`** | states the standard to freelance editors **as measurements** — framing is not among them | the measured framing standard in the editor's language (no tool steps — see that skill's own rule) |
| `/coverimage`, `/youtube-packaging` | partial crop traps only | reference the locked standard |

Adding it to `/revisions` and `/editor-brief` is nearly free and improves the **human** editors'
output too — **Muhammad has never been told this standard in measurements.**

---

## Traps

* **Do not renegotiate the standard.** Four revisions bought it; Dan locked it 09-08.
* **Do not raise a threshold to make a build pass** (memory `audio-never-over-strip`). If a corpus
  entry fails a bound, that is the finding.
* **Do not add a `known_gap` to make `run.py` green.** A gap names one check on one file with a
  reason, a date and what clears it. If you are adding one so a change can ship, you are relaxing a
  bound.
* **A detector that returns a null must FAIL LOUDLY, never default to "fine".** The head-top
  detector returned **0** on a JPEG-noisy photo once (photo pipeline, `blue-213`).
* **`personmask`-based centring over-fires on handheld and outdoor footage** — its own note says
  *"`audit.py` is a shortlist, not a verdict."* Treat any new detector the same until the corpus
  proves it.
* **Metal crashes the mediapipe FaceLandmarker — CPU delegate only.**
* **`Media/` is gitignored.** A script that lives only there enforces nothing.
* **Do not delete the 17 bannered QC forks yet.** Phase 3 does that, after the watch pass lands.
  Several still hold framing rows this gate has not absorbed, and builds run against them.
* **Respect the two-concurrent-build cap** (`AGENTS.md`). Check
  `ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'` before a gate run. Measured
  2026-09-11: the Mac sat at load 17–28 all evening with three other sessions building, which
  roughly doubled every wall-clock number in Phase 1's notes.
* **`selftest.sh` is zsh.** `bash selftest.sh` dies on `${0:A:h}` with *"A: unbound variable"* — it
  spent a day documented as broken for this.

---

## Phase 2 is done when

1. The framing rows run from `_shared/deliver/gate.py` **on a set with no 8/28 door-panel profile**.
2. They **fail `website-rev2`, `website-rev3` and `v2-short3-offcentre`, and pass `website-rev4`,
   `website-rev5` and `website-rev6`** — and `framing:push_coverage` fails `ad1-vertical-attempt1`
   and passes `muhammad-ad2-16x9`.
3. All five `framing:` keys are in `run.py`'s `IMPLEMENTED` and no longer print as PENDING.
4. `compliance:banned_screen` is registered too, with a margin you can defend.
5. `/shortad-from-longform`, `/revisions` and `/editor-brief` carry the standard.
6. `python3 .claude/skills/_shared/qc_corpus/run.py` is **green**, and
   `python3 .claude/skills/_shared/deliver/gate.py --audit` reports no holes.

---

## Starter prompt

```
Read Handoffs/handoff-20260911-vqc-phase2-portable-framing.md and execute it. Phase 1 is done and
pushed (eff3896, 5e10200) — read the "✅ PHASE 1 EXECUTED" section of
Handoffs/handoff-20260911-video-quality-engine.md first for what landed and what did not.

Confirm `python3 .claude/skills/_shared/qc_corpus/run.py` is green before you start and keep it
green throughout — it is the acceptance test.

Do item 0 FIRST: finish the banned-screen pairing test. It is half a session, it is a live Google
Ads exposure, and the discriminator is already measured and written up in
_shared/deliver/formats.py (_BANNED).

Then the framing work. All five framing rows are arithmetic on ONE per-frame signal — head top,
head height, head centre x, valid — so build that tracker first, in checks/picture.py's Picture
pattern, and register the rows in the shared gate rather than as a script.

The hair-top detector today depends on the luma profile of the door panel behind Dan in the 8/28
kitchen and cannot run anywhere else. Re-derive it with mediapipe FaceLandmarker (CPU delegate —
Metal crashes) or Apple Vision person segmentation, both already working in this repo. KEEP the
detector-free top-rows test beside it: that is what caught rev 3 when the detector was wrong.

Prove it against the corpus before anything else: it must FAIL website-rev2, website-rev3 and
v2-short3-offcentre and PASS website-rev4, rev5 and rev6; framing:push_coverage must fail
ad1-vertical-attempt1 and pass muhammad-ad2-16x9.

Then wire the standard into /shortad-from-longform, /revisions and /editor-brief, which have no
framing rule at all today.

Do not renegotiate the framing standard — Dan locked it 2026-09-08. Do not raise a bound to make
anything pass. Do not delete the bannered QC forks (Phase 3 does that). Respect the two-build cap.
Commit, push. No dashboard row.
```

**Model:** Fable 5.1, high effort. ~2 sessions — item 0 plus the detector is the first, the rows and
the skill wiring the second.
