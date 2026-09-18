# kit9x16 — the locked design kit for the 9:16 vertical ad

**What it is.** Muhammad's pacing, panel system, push schedule and cut placement as DATA on the
`/shortad-from-longform` pipeline (`render.py`, `captions.py`, `mux.py`, the shared audio chain, the
shared gate). A build starts from his grammar instead of inventing one. Engine Phase 4
(`Handoffs/handoff-20260916-vqc-phase4-locked-kit.md`); the finding it is built on is "The Muhammad
Standard" (2026-09-11): every approval of our work came where the design was fixed before the AI started.

**What it is not.** Not a second renderer, not an exemption from the gate, not our taste: the kit's output
goes through `_shared/deliver/gate.py --format ad9x16` and the judged watch pass like any delivery, and
Dan judges it blind (`blind/`). Never grade the kit yourself.

| file | job |
|---|---|
| `template.json` | the beat grammar: opening hold, push schedule (ramp / hold / cadence / coverage), insert cadence and max bare stretch, lower-third and CTA timing, flash rule, caption band, label placement rule, the cut rule's numbers. Every value names the `_shared/reference/picture.json` key it is checked against |
| `panels/measure_panels.py` → `measurements.json` | his panel tokens measured off the two masters (BT.709 decode): field, card olive, grid pitch, card hole and its radius, lower-third geometry and opacity, CTA pill — each with the frame it came from and its delta against `vlib.py` |
| `panels/render_panels.py` → `layers/` | his panel system as 1080×1920 layers, rendered by the same `vlib` calls the renderer makes |
| `cut_rules.md` + `kit_cuts.py` | THE POSE-MATCHED CUT: at every talk splice the picture cuts on his frame (from a master, `piccuts.py`'s method) or on the pose-matched frame within ±15 (from raw); what will not match is covered by a push. `calibrate` measures the cover threshold on the corpus |
| `build_kit.py` | template + `content.json` (WHAT goes where, phrase-anchored) + the audio EDL → `beats.json`, `beats.py` (shim), `edl_picture.json`, `piccuts.json`, `kit_report.json` (the generated design scored against picture.json's lo/hi BEFORE rendering) |
| `content_from_beats.py` | lifts the content decisions out of an approved hand-written beats.py, with phrase anchors and label kinds |
| `kit_beats.py` | the `beats` module the pipeline imports, reading `beats.json` |
| `kit_base.py` | conform the picture to `edl_picture.json` at the grade (snapped seeks, rewritten pts); its dissolve-patch pass is dormant since round 6 (window splices step like talk splices, `cut_rules.md` 3c) |
| `kit_track.py` | the 608-px talk crop's face track per picture segment; fixed centre where the lean is small |
| `kit_labels.py` | label chips on full-bleed pictures of Dan placed by MEASURING him (person mask, above the head first), the approved square's method; `--verify` on the delivered file |
| `kit_plan.py` | plan.json for the gate, evidence contract v2, read out of the build |
| `kit_deliver.py` | the build order as numbered stages: setup · audio · words · picture · captions · mux · gate · review |
| `blind/blind_page.py` | the blind A/B page: labels hidden, order randomised, sealed `key.json`, Dan's words saved verbatim |

## Build order (from a master)

```
kit_deliver.py setup  --build B --from-build <an approved build dir with grade.py, assets.py, asset dirs>
content_from_beats.py --beats <approved beats.py> --cwd <its dir> --words m.whisper.json --treat sqassets.py --out B/content.json
kit_deliver.py audio  --build B --mode master --approved <the approved vertical>      # his mix, untouched
build_kit.py --from-master --build B --edl edl_final.json --content content.json --words m.whisper.json
             --reference <his 16:9 master> --raw <roll> --grade grade.py             # runs kit_cuts decide
kit_base.py  --build B --raw <roll> --grade grade.py
kit_track.py --build B
kit_labels.py --build B                                                             # renders labelled bleeds chip-less, measures, places
kit_deliver.py words --build B ; kit_deliver.py picture --build B ; kit_deliver.py captions --build B
kit_deliver.py mux   --build B --out <name>.mp4
kit_deliver.py gate  --build B --video <name>.mp4 --reference-cut <his master> --banned-source <rec> --banned-times ...
  -> a FRESH subagent judges watch/ (JUDGE_PROMPT.md) -> watch.py --judge -> gate.py --format ad9x16 --plan plan.json
kit_labels.py --build B --verify <name>.mp4
```

From raw: the same, with `--from-raw`, no `--reference`, a script-aligned EDL, and the audio built by the
shared chain (`_shared/audio/voice_chain.py` + bed + his tick at graphic entrances) instead of copied.

## Rules carried (do not re-open)

* One format. Bound to his ranges in BOTH directions (`picture.json` lo/hi; overshoot is a warning).
* The kit is not an exemption; a kit output that needs a bound moved is a kit that failed.
* Never raise a bound, never add a `known_gap`, never delete a `must_trigger`.
* An editor's finished mix ships untouched. Same person in a before/after. Real pictures carry the real
  label, off his face and abs, placed by measurement.
* Assets live here in the skill, never only in `Media/`.

## Measured traps (round 5, 2026-09-17)

* **A card's label chip sits 68 px under the hole, not 44.** The gate's person segmenter reads a dark chip 44 px
  under a torso the hole cuts off as his shorts (4,821 px of "body" on the chip at 198.5 s, 12 obstructions in
  the round-5 gate); at a 64 px gap the same frame reads 0 px. `vlib.card_hole` gives a labelled card 114 px at
  the bottom, `plate_card` hangs the chip at `hole[3] + 68`; the kicker keeps its old absolute line. Never move
  the chip back up to make room.
* **Graphic-region beats are declared on the frame grid** (`kit_plan.py`): a graphic enabled at `t0` first draws
  on the first frame at or after `t0`, and the compositor's caption states are frame-exact, so a state that ends
  on that frame does not share a frame with it. Declared at the unquantised `t0`, a 0.9 ms "overlap" read as a
  −104 px collision (six false rows in the round-5 gate).
* **An AI clip's hands are checked frame by frame before it is used**; a clip whose hands melt is replaced by
  one of its own clean frames as a pushed still (`assets.py`: `ai_respect_gym`, `ai_women_pool`), $0.
* **A watch judge is told which boundaries are ramps.** `plan.json` `punch` boundaries at a 50 % ramp crossing
  (`punch_FAR` / `punch_NEAR` strips) show a gradual zoom, not a step; three judges in a row reported them as
  "a declared step that never rendered". Say so in the judge prompt.
