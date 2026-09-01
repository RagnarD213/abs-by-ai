# Handoff: Cut 6–8 Shorts from "02 – My Honest Zepbound Update"

**Date:** 2026-09-01
**Project:** Abs By AI
**Handing off from:** Claude Code (cloud session `claude/zepbound-update-shorts-htj3rx`)
**Handing off to:** Claude Code **on the Mac mini** (invoke `/shorts`)
**Business goal this serves:** The Zepbound long-form is the biggest unmined raw yield left from the
8/3 shoot (30 min of talking head, 50 discrete beats). It is also the one topic the paid side can
never touch (no drug names in ads), so organic Shorts are the only channel for it.

⚠ **WHY THIS IS A HANDOFF AND NOT A DELIVERY.** Dan asked for this to be executed in a cloud
session on 2026-09-01. It cannot run there: every media folder (`claude edited long form content/`,
`Short-form video content/`, `Muhammad Ad Videos/`, `/Volumes/Extreme`) is git-ignored and lives
only on the Mac, and the cloud egress policy returns **403 on CONNECT to `drive.google.com` and
`youtube.com`** (verified at `$HTTPS_PROXY/__agentproxy/status`), so neither the 16 GB raw roll on
Drive nor any published copy can be pulled. The Drive connector can only stream a file as base64
through the model, which is unusable at video sizes. Only one cloud environment exists
("Default") and it is the blocked one. **This job must run on the Mac.** Everything that could be
prepared without the media is in this document.

---

## Dan's instructions for this batch — VERBATIM, all binding

> Invoke /shorts on "claude edited long form content/02 - My Honest Zepbound Update". Cut 6-8
> shorts, no source second used twice, 45-60 s target. Run work/chancheck.py on the source first,
> fit the voice against "Muhammad Ad Videos/" not the organic cut, pure gain + limiter (not
> loudnorm), captions print "abs" lower case, title on black with picture dropped below, check 17
> centering measured on the delivered file. No drug name in any graphic.

Mapped to the pipeline, each one is a gate, not a preference:

| instruction | mechanism | where |
|---|---|---|
| 6–8 shorts, 45–60 s | 165–205 spoken words at his measured ~200 wpm | shortlist "est." column |
| **no source second used twice** | `segments.js` throws on any overlap between pieces — keep that assert on | `reference/clean-master/segments.js` (the ab-wheel batch added the throw) |
| **`work/chancheck.py` on the source FIRST** | expect the NO-GRAPHICS master to read L/R corr ≈ +0.07 at −7.5 ms (two mics). Take the **RIGHT channel only, as mono** | `reference/clean-master/work/chancheck.py` — repoint `FILES` at the 02 folder and `C1513.MP4` |
| **fit the voice against `Muhammad Ad Videos/`, NOT the organic cut** | `work/finalchain.py` is already written against `Daniel HQ Fitness AD Video v3 HD.mp4` (indoor, same two-mic rig). Re-run the fit on THIS roll — the 03 curve does not transfer (01 needed the opposite low-end correction to the ad roll) | `reference/clean-master/work/finalchain.py` → writes `work/voicechain.txt` |
| **pure gain + limiter, NOT loudnorm** | our shorts sit at −19 to −21 LUFS; reaching −14 is +5 to +7 dB, which loudnorm cannot do linearly under a −1.5 dBTP ceiling — it silently switches to DYNAMIC mode and compresses the floor up against the voice (supplements rev 4, Ad 2 vertical). Measure the gain, apply `volume=` then `alimiter`, verify by measurement | `reference/clean-master/finishaudio.py` (rev-4 version) |
| **captions print `abs` lower case** | `AI` stays upper case; no `/\babs\b/gi → ABS` rule anywhere | `captions.js` |
| **title on black, picture dropped below** | `dropTop 310`: picture rendered into 1080×1610 at the BOTTOM, J2 field carries the title for the whole short, on cards as well as full-bleed. Assert with `work/titleclear.py` on the delivered file | `reference/clean-master/layout.json` (already dropTop geometry) |
| **check 17 centering, measured on the DELIVERED file** | Vision person mask on the finished frames, talk beats only: fail on median > 25 px, > 10 % of talking frames beyond 70 px, or any run beyond 60 px lasting ≥ 1 s. Then the **independent Fable subagent audit** (Step 7b of `/shortad-from-longform`) on the exact delivered files | `/shortad-from-longform` [A4] lesson 0; `reference/clean-master/recentre/` (`personmask.swift` + `anchor.py`) |
| **no drug name in any graphic** | no title, eyebrow, chip, card or caption-suppressing graphic may print Zepbound, tirzepatide, Mounjaro, Ozempic, semaglutide or any brand. Captions are transcript and may carry what he says; graphics may not. Grep the built PNGs' source strings before rendering | `build-assets.py` — add an assert |

---

## Source files — what to expect in the folder

`claude edited long form content/02 - My Honest Zepbound Update/` should hold, by analogy with 03:

| file | use |
|---|---|
| **`CUT_v*_graded_NO-GRAPHICS.mp4`** | **cut from this.** The 8/27 rebuild took 02 to **48 % insert coverage / 1009-cue SRT**; cutting from the delivered master would make half of every short a card |
| the delivered master (rebuilt 8/27) | timecode reference only; prove frame alignment with matched grabs at 5 timestamps before relying on the SRT against the clean file (03 measured 0.03 s) |
| `*_PRE_AUDIOFIX.mp4` | **never** — comb-filtered two-mic voice |
| `*.srt` (1009 cues, rebuilt 8/27 to carry every word) | build the verbatim shortlist from this |
| `edl.json` / `ranges.py` | the real cut; the repo copy is `.claude/skills/longform-edit/reference/ranges_zepbound.py` |

⚠ **The clean master's audio is almost certainly NOT fixed.** On 03 the handoff claimed the clean
master carried the single-mic chain and it did not — only the DELIVERED master had been repaired
(the 8/23 fix was an audio-only remux of the delivered file). That is exactly why Dan put
`chancheck.py` first. Do not trust any note that says otherwise; measure.

⚠ **Run `work/preflight.py` too.** A concatenated master can carry two timelines (03 held 0.76 s of
extra audio samples spread through the file — captions shipped 280–650 ms late). Extract the
analysis WAV with `aresample=async=1:first_pts=0` and gate the delivered files with `syncgate.py`.

**The grade, if any raw footage is needed** (a better take, a discarded opening):
`curves=all='0/0 0.069/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'` on `C1513.MP4`
(`/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/`; a Drive copy exists at
Drive id `1q03URXJFC1GdvZihcWxBR__-340MQnAs`, 16.1 GB).

**Concurrent-build cap: two.** `ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'` first.

---

## Step 0.5 — BUILD THE VERBATIM SHORTLIST, PUT IT TO DAN, AND STOP

Segment selection is Dan's call (standing rule since 2026-08-04). The cloud session could not
read the SRT, so **the shortlist is not written yet** — but the beats are mapped. Use
`Handoffs/assets/shorts-zepbound-20260901/range-map.md` (all 50 EDL ranges, labels, durations,
approximate master timecodes, exact raw in/out) and pull the verbatim text for each candidate
below from the SRT. Format exactly like `Handoffs/assets/shorts-supplements-20260828/shortlist.md`
(letter, working title, in → out, word count, est. runtime, verbatim quote, one-line reason).

**Candidate beats, ranked from the labels** (durations are source seconds from the EDL; the viewer
must walk away with something — his own result is never the payload):

| | ranges (#) | src dur | what the viewer gets | note |
|---|---|---|---|---|
| A | `dont-go-above-2.5` + `unless-youre-obese` (43, 44) | 61.6 | the dose ceiling and the one exception | trim 2–3 s; strongest single instruction in the video |
| B | `muscle-loss-is-the-risk` + `protein-target` (46, 47) | 79.6 | the real risk and the fix (200 lb → 160 g protein) | trim to ~55 s at a sentence boundary |
| C | `escalate-gradually` + `context-max-dose` + `tiny-dose` + `dose-ladder` (34–37) | 66.3 | how to ramp | check the 34→35→36→37 joins — three of them drop stumbles/dups, so they are inherited splices that need a wide/tight framing change |
| D | `wont-damage-your-skin` (41) | 52.1 | the injection-site fear, answered | right length as-is |
| E | `it-doesnt-hurt` (42) + optionally `ice-if-youre-scared` (45) | 51.8 / 76.9 | needle fear, answered | 42 alone is the right length |
| F | `alcohol-knockout` + `how-much-i-drank` + `blowouts-gone` (15–17) | 50.9 | it kills alcohol cravings | ⚠ range 16 keeps a stumble ("no clean internal cut" in the EDL) |
| G | `compounded-vs-brand` (23) | 55.5 | where to get it and why compounded | brand/pharmacy names may be spoken; **never printed** |
| H | `how-to-get-a-script` + `skip-the-membership-fees` (26, 27) | 59.1 | the cheapest path to a prescription | |
| I | `which-day` + `why-thursday` + `inject-thursday-7pm` (30–32) | 47.6 | when to inject and why | |
| J | `even-ripped-people` (9) | 44.4 | contrarian: it is not only for the obese | |
| K | `my-side-effects` (33) | 45.7 | what actually happened to him | borderline: about Dan, but the payload is "here is what to expect" |
| L | `if-youre-obese` + `if-youre-ripped` + `how-to-do-it` (19–21) | 72.8 | who should and should not | trim |
| M | `30-pounds-math` (8) | 35.8 | the arithmetic on 30 lb | under band; extend only if the neighbour reads |
| N | `biggest-mistake` (40) | 24.4 | one mistake to avoid | under band on its own; read it — may pair with C |

**Do NOT cut:** `the-transformation` (14) — its two photo slots at 8:51 (192 lb) and 9:12 (181 lb)
are still EMPTY in the delivered master (only Dan can say which photo is which), and it is the
bragging failure mode. `not-medical-advice` (12) is not a Short but see the compliance note below.
`started-recommending-it` (7) carries the "injected my ex-girlfriend" line — flag, do not pick.

**Flags to surface in the same message as the shortlist:**
1. **Drug name spoken** in most candidates. Organic Shorts CAN name it (the no-drug-names rule is
   ad-compliance; RP did 502K on a Tirzepatide title, 2026-08-25 research). It stays out of every
   graphic. Whisper renders it "Zep bound" — fix the caption token, never print the split.
2. **Dosing shorts (A, C, I) are medical instruction with the disclaimer beat cut away.** Offer Dan
   a persistent small eyebrow line such as `NOT MEDICAL ADVICE` under the title on those three, and
   a description line. His call — it costs headroom and he may prefer the description only.
3. **Profanity/spice:** re-read every candidate's text for the four profanity lines and the Trump
   tan joke's equivalents in this video before he picks (the 8/20 delivery flagged 4 profanities
   across the three videos; locate the ones in 02).

**Then stop and wait for his letters.** Do not transcribe, cut or render before he answers.

---

## Build steps — follow `/shorts` end to end; what is specific here

- **Step 0.8 first** (`chancheck.py`), then **preflight.py**, then the voice fit against the AD
  (`finalchain.py`, re-fit on this roll, verify the shape difference falls under ~0.7 dB and the
  floor stays below his). Chain = `pan=mono|c0=c1` → highpass 75 → afftdn → gate (release
  180–200 ms, never 300) → fitted tone EQ → deesser. **Nothing appended may `pan` again** — a
  second pan renders silence.
- **Finish = pure gain + `alimiter`**, measured to −14 LUFS / ≤ −1.5 dBTP; assert L/R corr
  +1.000 on every delivered file. ⚠ `alimiter attack=5` delays the programme by 219 samples
  (4.97 ms) — trim it (`atrim=start_sample=219,asetpts=N/SR/TB`) and measure 0 ms against the
  picture. ⚠ A bare `apad` generates silence forever; give it a length.
- **Step 1** — word timestamps from the clean master's container-timeline WAV, `medium.en`,
  then `work/fixonsets.py` (swallowed pauses). Never the SRT for captions.
- **Step 3** — cut points = intersection of `work/vad.py` and `silencedetect -26dB/0.05`
  (`work/gaps.py`); no music bed on this master, so silencedetect is valid.
- **Step 4** — splices from the EDL, measured at full frame rate (`work/edl_splices.py` +
  `work/splices.py`), then `work/junkscan.py`. Every inherited splice inside a short is HIDDEN by
  a wide/tight alternation (a naked one scores 7.6 against a 1.3 baseline; removing a pause scores
  as bad or worse).
- **Step 5** — one locked kitchen camera, but **measure a centre per shot** with Vision
  (`recentre/personmask.swift` + `anchor.py`, torso block). 03 measured 0.668–0.697 against a
  0.60 estimate; the same doorway will not be 0.478 either. Never a colour heuristic — it bleeds
  into the stainless fridge on this set.
- **Step 6** — measure the vertical geometry (`work/vertgeom.py`, largest connected component,
  ≥ 20 px run) and pick the global-minimum head position; expect something near 03's
  644×960 @ cropTop 120 → 1080×1610, head ≥ 60 px under the title band.
- **Step 7** — title holds for the whole short on the black band, eyebrow persists, `AbsByAI.com`
  wordmark on every short. **Headlines must work cold without the drug name** — e.g.
  `THE DOSE CEILING NOBODY TELLS YOU` / `WHY THE SHOT KILLS YOUR DRINKING` / `DOES THE SHOT
  HURT?` are mine, not his; he rewrites titles, so offer them and expect edits.
- **Step 8** — captions: `abs` lower case, `AI` upper, punctuation-leading tokens merged before
  chunking, zero-duration words given 120 ms, "Zep bound" corrected per word before chunking.
- **Step 9** — one audio pull per segment, shots rendered `-an`.
- **Step 10** — `qc.js` (incl. the silent-second scan on the MASTER, not only review copies),
  `syncgate.py` (−80 ms calibration), `titleclear.py`, silhouette containment (`framecheck.py`),
  **check 17 centering on the delivered files**, then the Fable subagent audit, then a watch pass
  on the exact files. Contact sheet of every card moment from the finished files.

---

## Delivery

- Work folder: `YouTube Long Form Video Content/zepbound-honest-update/` (working files; source
  stays read-only in `claude edited long form content/`).
- Output: **`zep-short1_<slug>.mp4` … `zep-shortN_<slug>.mp4`** in `Short-form video content/`.
  Prefixes in use: `short`, `v2-`, `v3-`, `v6-`, `abwheel-`, `supp-`. Do not collide.
- `SHORTS.md`: posting order, per-short title, description with
  `utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=<id>`, editorial notes,
  the graphics decisions, and the compliance table (drug name spoken / never printed; the
  disclaimer decision; any profanity; the empty-photo beat excluded).
- 540p review copies to Dan in chat, each scanned for silent seconds first.
- ⚠ **Posting is blocked on the parent video** — 02 is unpublished, its two photo slots are still
  empty and `/youtube-packaging` was never run. Build now, queue nothing in Blotato.
- **Check the delivery folder for ` 2.mp4` conflict copies** before calling the batch final.
- Both media folders are git-ignored — `git check-ignore` before staging anything.

---

## Cost and risk

**AI spend: $0.00** (local Whisper, ffmpeg, PIL, Vision) plus ~$0.20 per Veo clip only if Dan asks
for a join to be covered (Step 6.5). No production code, no deploy, no native-retest trigger.
Nothing destructive: the masters are read-only inputs.

---

## Dashboard

Key task added to the `business` list by the cloud session (via `todos.json` on the branch, since
`absbyai.com` was also egress-blocked there): `money::Execute handoff: cut 6–8 Shorts from the
Zepbound long-form (02) — /shorts, Mac only`. Check it off only when the files are delivered AND
Dan has watched the review copies (Ad 1 attempt 1 had a check-off reverted for exactly this).

---

## Exact next action

**On the Mac:** open a fresh session, invoke `/shorts` on
`claude edited long form content/02 - My Honest Zepbound Update`, do Step 0.8 (`chancheck.py`)
and `preflight.py`, build the verbatim shortlist from the SRT using the candidate table above,
present it to Dan with the three flags, and wait for his letters. Recommended runner: Opus 5,
high effort.
