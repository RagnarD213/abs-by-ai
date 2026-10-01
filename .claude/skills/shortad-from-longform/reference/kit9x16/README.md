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
| `cut_rules.md` + `_shared/cut/piccuts.py` (`kit_cuts.py` is a shim) | THE POSE-MATCHED CUT: at every talk splice the picture cuts on his frame (from a master) or on the head-matched frame within ±15 (from raw); what will not match is covered by a push. `calibrate` measures the cover threshold on the corpus |
| `build_kit.py` | template + `content.json` (WHAT goes where, phrase-anchored) + the audio EDL → `beats.json`, `beats.py` (shim), `edl_picture.json`, `piccuts.json`, `kit_report.json` (the generated design scored against picture.json's lo/hi BEFORE rendering) |
| `content_from_beats.py` | lifts the content decisions out of an approved hand-written beats.py, with phrase anchors and label kinds |
| `kit_beats.py` | the `beats` module the pipeline imports, reading `beats.json` |
| `kit_base.py` | conform the picture to `edl_picture.json` at the grade (snapped seeks, rewritten pts); its dissolve-patch pass is dormant since round 6 (window splices step like talk splices, `cut_rules.md` 3c) |
| `kit_track.py` | the 608-px talk crop's face track per picture segment; fixed centre where the lean is small |
| `kit_labels.py` | label chips on full-bleed pictures of Dan placed by MEASURING him (person mask, above the head first), the approved square's method; `--verify` on the delivered file |
| `kit_plan.py` | plan.json for the gate, evidence contract v2, read out of the build |
| `kit_deliver.py` | the build order as numbered stages: setup · audio · words · picture · captions · mux · gate · review |
| `kit_fold.sh` | after the judges: merge their findings files (negscan entry excluded), `watch.py --judge`, `kit_negscan.py record`, then the delivery gate → `gate_final.json` + the PASS stamp |
| `blind/blind_page.py` | the blind A/B page: labels hidden, order randomised, sealed `key.json`, Dan's words saved verbatim |

## Build order (from a master)

```
kit_deliver.py setup  --build B --from-build <an approved build dir with grade.py, assets.py, asset dirs>
content_from_beats.py --beats <approved beats.py> --cwd <its dir> --words m.whisper.json --treat sqassets.py --out B/content.json
kit_deliver.py audio  --build B --mode master --approved <the approved vertical>      # his mix, untouched
build_kit.py --from-master --build B --edl edl_final.json --content content.json --words m.whisper.json
             --reference <his 16:9 master> --raw <roll> --grade grade.py             # runs _shared/cut/piccuts.py decide
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
shared chain (`_shared/audio/voice_chain.py` + bed + his tick at graphic entrances) instead of copied:
`kit_audio.py --bed music.mp3` (bed −38 dB, his floor between words, measured 2026-09-18), then Whisper on the
delivered mix → `ref.whisper.json`, `ln -s audio_final.wav his_mix.wav`, `kit_deliver.py words` (clears a stale
`words_ctc.json` first), and `kit_plan.py --transcribe` (delivered-ASR words with forced-alignment timing, the
evidence the gate's `captions:sync` / `script_fidelity` rows need when the audio is ours). The worked chains are in
`/Volumes/Extreme/_edit_work/kit9x16/ad1-raw/run_raw*.sh`.


## For Dan: a vertical as one command (2026-09-28)

A vertical of Muhammad's finished ad used to need a long AI editing session, mostly to write one sheet by hand:
which graphic appears when, what it says, which picture, and whether that picture is real or AI. The kit now
writes that sheet itself by laying Dan's graded raw footage over Muhammad's master frame by frame (wherever they
stop matching, he added something), reading the text on screen with the Mac's own text reader, and finding the
clean original of every picture in our libraries (the library it lives in says real or AI). It stops and asks
("escalates") whenever it is not sure, instead of guessing. Muhammad and the other editors are never asked for
anything. The only AI left is three small calls: "is this picture a bare physique?" (a fraction of a cent), which
sentences make the <=0:59 cutdown (about a dime, checked and re-asked by the kit), and an optional second-opinion judge. The judged watch pass is
still done by fresh reviewer sessions, because the model judge missed defects they catch (below).

## Build order (automatic, from a master) -- `kit_run.py`

```
kit_run.py --master HIS.mp4 --build B --name "<title> | claude | 9x16 | ad N" --shoot <shoot folder> [--deliver <ad folder>]
```

| stage | script | what it does (no model unless named) |
|---|---|---|
| recover | `kit_recover.py` | his transcript (local Whisper), which roll(s) he cut from (>= 95 % of his words), the audio EDL (every window of his mix locked against every place his words occur in the roll, GCC-PHAT), his grade as a 33^3 LUT from matched pixels, then the EDL re-placed on his PICTURE every 3rd frame (split where the take offset steps) |
| measure | `auto_measure.py` | every master frame vs Dan's graded raw: framing fit (interpolated through his push ramps), cell-by-cell agreement, head-box match, scene-change score |
| content | `auto_content.py` | `content.json` + `assets.py` + `auto_content_report.json` (evidence and confidence per entry). Escalations stop the run (exit 3) |
| setup .. mux | the kit's existing stages | unchanged (README build order above) |
| prewatch | `kit_deliver.py gate` | audio gate `--verbatim`, plan, watch pass; then the run stops (exit 4) for the judged watch pass |
| judge | fresh session judges (`watch/JUDGE_PROMPT.md`, thirds) -> `logs/findings_part1..3.json`; `--judge both` adds `gemini_judge.py` as a second opinion |
| fold | `kit_fold.sh` | gate PASS or the run stops |
| pick, cutdown | `cutdown_pick.py` (one text call), `kit_cutdown.py` | the <=0:59: model picks sentences; seams snapped, word tails kept, never opens inside an overlay, every seam proven on pixels; his mix only cut |
| cutgate, cutfold, deliver | the same gates on the cutdown; copies masters, review copies, stamps, recipe |

`run_report.json` in the build dir: every stage with its wall-clock, every AI call with its cost (`ai_ledger.jsonl`),
every escalation, both gate verdicts.

## What escalates (never guessed)

* a banned screen read in his master (email capture, "Meet the new you"): trim or replace is Dan's call
* a physique still with no provenance (no library file, no label in his master): every physique picture needs
  exactly one correct label
* two library copies of one picture that disagree on real vs AI; a library label that disagrees with his burned one
* window, title or overlay text that two reads do not confirm, or that matches nothing he says
* fewer than 95 % of his words found on the raw roll(s) (wrong shoot)

REAL vs AI is never a model's call: a Gemini Flash classifier read three of Ad 1's AI clips as real at 0.95
confidence (2026-09-28). The model is asked only "is this a bare physique?". Motion lifted from his master carries
his own (Dan-approved) labelling; a picture never gets a second chip over his burned one.

## Rules the measurement learned (2026-09-28, Ad 10 + Ad 1)

* Agreement is judged cell by cell over the whole frame, never by a head-box score alone (a plain fridge scores 0.82
  on a wrong framing). Talk agrees ~98 %, an insert ~15 %.
* His framing ramps (Ad 1 opens on a 1.09 -> 1.26 zoom): interpolate between samples, never hold.
* His window can hold a shifted Dan crop: a window is "text side dead + head box >= 0.88", not only cell agreement.
* A shot whose panel words match the window beside it IS that window (judge the last settled read, not a half-typed one).
* A white flash, a whip burst (< 0.4 s, every frame new) or an empty grid is a transition: its time goes to the
  picture it leads into.
* A phone is a tall card hole clearly bigger than the picture in it (the bezel); an app demo stays in cards.
* Full bleed is for a physique photo; a clothed family snapshot goes in the card (both answer keys).
* Vision reads "AI" as "Al"; its confidence is always 1.0, so a line counts only when two reads agree; a read
  taken mid type-on misspells, so the fullest reads are ranked by how well they match what he says.
* A library can hold AI-edited near-duplicates of a real photo (`01_LIGHT_plus8lb` = the real deckchair photo with
  8 lb painted on): candidates are ranked by their pixels after alignment (the worst 24x24 block), provenance is
  shared only among identical copies. A feature-point match alone put an AI image under "Real picture of me".
* Of two crops of one photo, use the one he showed (all of it on screen): the uncropped original showed the Speedo.
* A lift from his master never plays his transition or his next shot: it stops before his flash burst and holds or
  gently stretches its last clean frame (judged one-frame leaks at 57.9, 95.2, 114.9, 155.7, 172.5, 176.7 s, Ad 10).
* His picture can hold another take of a repeated line for a second or two under a window's music: the picture
  refinement tries every place those words are spoken in the roll and keeps a take while it keeps winning.
* The push count is checked AFTER the schedule's own clean-up (`final_topup`); a cut inside a return flash may
  snap onto the insert edge (the flash's length counts as reach).
* Captions: Whisper's mid-sentence capitals are lowercased (names and acronyms kept); AI clips of other people keep
  their captions, only labelled pictures of Dan and phone screens drop them.

## Round-4 lessons (2026-09-29, Ad 10 + Ad 8 judges)

* An uploaded photo's label on the app's next screens lasts only while the photo is ON the phone: the screen is
  matched against the uploaded file every 3rd frame (its own 3000-point detector; the library-wide one spends its
  points on the UI text) and the clip splits where the photo scrolls away.
* When his cut frame cannot be confirmed on the pixels, the picture cuts at HIS cut (the audio cut), moved only by
  the measured pose / head-jump tests. A free pose-match moved 22 of Ad 10's cuts into the other take's pre-roll,
  where Dan's mouth moves with no sound (a lip-lick opened the 142.0 s shot).
* A lifted card clip starts when his picture has LANDED in its hole (no olive band along an edge beyond the
  picture's own olive tones) and stops 4 frames early at a dissolve edge; the last clean frame holds.
* A ramp-out that the next insert would cut short is not a ramp: the push holds to the insert.
* An AI clip whose library file names Dan is a labelled picture of Dan: no captions under it.
* Type-on letters fade in their own colour (never from black); a word right after a lower third is captioned.
* A judge's identity call is checked against the library match before acting: the round-4 judge called Dan's own
  deckchair photo "a stranger" from an old memory about a different recording.

## Round-6 lessons (2026-09-29)

* A label that must come and go on one clip is TIMED on the card (`label_spans`), never made by splitting the clip:
  a labelled card's hole is smaller, so every split resized the phone.
* Dan-approved crops of real photos live in `/Volumes/Extreme/_edit_work/kit9x16/approved_crops/` (listed first in
  `auto_sources.json`, `curated_crop`); a crop that lies wholly inside the matched photo replaces it (the 4:3 dad
  photo in a card cut his head, the framing Dan rejected on Ad 1).
* A boundary between two Dan-window plates does not hide a cut (his head keeps its size): the cut gets its step.
* A word that starts under a graphic but mostly plays after it is captioned from the graphic's end ("30 minutes").
* A lower third whose second line continues the sentence sets both lines in one size.
* His white flash on a return from a full-screen picture is followed, inside his measured flash range: rule returns
  he also flashes first, then his full-screen returns (latest first), then rule-only returns.
* A video that holds a still (a screen recording showing the AI goal image, filed under real footage) never votes on
  the still's real vs AI. A library change re-indexes it (about 40 minutes at 1,434 files) and can surface a new
  conflict; the run escalates rather than guessing.

## Gate-round lessons (2026-09-30)

* The delivery gate runs on the file BEFORE the judges (prewatch): a measured row that fails stops the run there.
* Label clearance is checked on the DELIVERED file with the gate's own measurement, in a loop: a full-bleed chip the
  person mask reads as touching him is re-placed away from that spot (`labels/exclude.json`), a card's chip moves
  72 px lower (`label_dy`, one height across a run of labelled cards), the changed segments re-render, and the file is
  checked again (3 tries). The mask reads a dark chip as part of him on single compressed frames, and nothing short
  of the delivered file predicts which.
* A timed label (`label_spans`) is one plan track per stretch it shows. The banned-screen source
  (`auto_sources.json` `banned_screens`) is always passed to the gate.
* A graphic that mutes captions ends just before a word that plays on after it (decided before the timeline is
  made, so the cut and flash follow); a word may be captioned from a graphic's end only when that is within 0.10 s
  of its start (the gate's caption sync bound is 120 ms); a lone word stranded before a graphic is not captioned.
* A phone lift is cropped to the phone, never a fixed column of his frame. Only Dan-window plates are declared as
  talking-head windows (a stale plate file made a full-bleed picture fail `framing:hair_top`).
* The work tree lives at `~/abs-worktrees/kit-autofill`, never under `/private/tmp` (a restart wipes it).

## Cutdown lessons (2026-10-01, AV-09 and Ad 10)

* The picker (`cutdown_pick.py`, one Pro text call with a 6,000-token thinking budget, about a dime) sees, per
  sentence, what is on screen where it starts and ends (FAR / NEAR / picture), whether captions are on, and whether
  a range may end or start there. Its answer is VERIFIED and re-asked (5 tries, then the run escalates): starts on
  sentence 0, in order, at most 4 ranges, 45 to 58.3 s with the tail pads, at least half captioned, and every seam
  a change of picture or of level, never inside a flash, a graphic's fade-out, or just before a zoom change.
* A zoom change that falls in the last word's tail: the audio keeps its tail, the picture HOLDS the last frame
  before the change (`hold` in cut_plan.json), and the cutdown's plan drops the sliver.
* A seam at a picture edge is not a talk join; `audio_joins` in the cutdown's plan lists the seams (the only places
  his mix is cut), which is what the gate's click check reads.
* The cutdown's review copy and gate stamps deliver beside the full's.
* Run a gate DETACHED (`nohup ... &`, then read its json): in the foreground of an agent shell that backgrounds a
  long command it never returns. Two gates at once also stall each other.
* A re-judge after a small fix: `carry_verdicts.py` carries the judged verdicts onto pixel-identical watch images
  and lists the changed ones for one fresh judge.

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
* **A chip burned into an asset is not verified by the gate's label row.** `phone_mock` / `p_goal` (the phone
  mock-up of the AI goal image, Ad 1 0:05 + 2:18) carry an AI-GENERATED chip burned into the composite above the
  picture, so the plate adds none; `label_tracks` only lists the chips the renderer drew, so that one is checked
  by the watch judges by eye (clear of face and abs every round) and by nothing else. A future kit asset with a
  physique picture should carry NO burned chip and take the kit's measured one.
* **A watch judge is told which boundaries are ramps.** `plan.json` `punch` boundaries at a 50 % ramp crossing
  (`punch_FAR` / `punch_NEAR` strips) show a gradual zoom, not a step; three judges in a row reported them as
  "a declared step that never rendered". Say so in the judge prompt.
