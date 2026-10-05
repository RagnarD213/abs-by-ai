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
| `kit_track.py` | the 608-px talk crop's face track per picture segment; fixed centre where the lean is small; `--tolerance` px of dead band (the calmer camera, 2026-10-01) |
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

> **2026-10-01, Dan:** the Ad 8 verticals are the last delivery with these olive graphics. Everything after uses Soft
> Blue Light graphics built with HyperFrames (`_shared/hyperframes/`, `_shared/SOFTBLUE.md`), shown in the first review
> round. This kit's measurement, recovery, labels, captions, cutdown and gate loop stand; its GRAPHICS LAYER
> (`vlib.py` plates, lower thirds, CTA pill, flash) must be ported to those templates before the next vertical.
> **Ported 2026-10-01 for sheet builds** ("The second way in" below). A rebuild from an editor's master still draws `vlib.py`.

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

## The second way in: our own 16:9's edit sheet (2026-10-01) -- `kit_run.py --sheet`

For Dan: when Claude or Codex made the 16:9, the answer sheet of that edit already exists, so the kit no longer
reverse-engineers the finished video. `kit_run.py --sheet SHEET.json --build B --name "..."` reads the edit sheet
(`_shared/edit-sheet/`), plans the whole vertical in about 12 seconds (the recover, measure and content stages took
over an hour of a 2 h 15 min build and were the main source of stops), and draws every graphic fresh at 9:16 in Soft
Blue Light with HyperFrames from the 16:9's own configs. The editor-master way in (above) is unchanged: the
answer-key test passes and Ad 8's plan is identical before and after.

| stage | script | what it does |
|---|---|---|
| sheet | `validate.py --hash`, `sheet_to_kit.py`, `clip_fit.py` | rolls, the cut (same-take reframes merged; every picture cut ON its audio cut, no pose search), the 16:9's grade on a HAIR-ANCHORED window of the raw, words (caption fixes applied, split hyphen words joined), `content.json` (every picture a fill, a square card or a whole-clip card by the three-step rule, label from the sheet; every full-screen graphic an `hf` beat; lower thirds; side cards), `assets.py`, `sheet_report.json` |
| setup, audio, kit, base, track | the kit's own | unchanged. The audio is the 16:9's delivered mix, stream-copied. `build_kit.py` takes `piccuts.json` from the sheet and still schedules pushes and level steps |
| graphics | `sbl_graphics.py` | after the kit has fixed the beat times: one HyperFrames render per graphic at 1080x1920 (`_shared/hyperframes/vertical.py`), one media-card plate per card beat, `cap_lifts` (captions rise above a bottom card) |
| labels | `kit_labels.py` | full-bleed chips placed by measurement, drawn as the Soft Blue Light chip |
| picture | `render_sbl.py` | talk and bleed beats from `render.py`; `hf` and `card` beats from the HyperFrames renders (decoded BT.601 to BT.709); overlays composited in RGB (`hyperframes/composite.py`, glass blur under lower thirds) |
| captions .. deliver | the kit's own | the lit word is Soft Blue cyan on a sheet build |

Review before any full build: `sbl_page.py --media` builds the graphic-lock page (first minute, every graphic and clip
at 9:16 with a moving context clip); `sbl_preview.py --range A B` cuts any span with captions and sound.

**What the sheet path decides, and how.** Every horizontal clip follows Dan's three-step rule (2026-10-01, VIDEO-RULES
"A horizontal clip in a vertical"): it fills the phone frame; if that cuts something critical at the sides, its centre
square in a card; if the square still does, the whole clip in a card (never cropped shorter). `clip_fit.py` decides
per clip with two small vision calls through `ai_calls.py` (about half a cent a clip, ledgered): first WHERE is what
must stay visible (the crops are centred on it), then the fill and square crops at three moments of the used span are
judged. The verdict is the tightest crop that loses nothing critical; it, its reason and the proof sheet go in
`sheet_report.json` (`pictures[].fit`) and on the review page. Dan's own flips live in `<build>/clip_overrides.json`
(`{"C08": {"verdict": "square", "dan": "<his words>"}}`) and win. A phone screen stays whole; a portrait source fills.
Real-or-AI labels are never asked of the model. Hard cuts by default (`--flash` carries Muhammad's flash). No vignette.
A graphic whose template has no 9:16 layout STOPS the run; nothing is dropped or redrawn by hand.

* The person mask cannot make this call: its extent read the salad table as 90 % wide and the man on the scale as 35 %,
  and on a hands-only clip its centre is the arm, not the bowl (round 1 and round 2 tuning).
* The first prompt (a neutral "is anything lost") chose the square for all 18 clips, including the man on the scale Dan
  named as a fill. The rule that works states his default (fill unless a strong reason) and the strong reasons: the one
  main object is wider than the crop, a face is cut, the hand or tool doing the action leaves the crop, or the scene is
  about things spread across the frame. RO-10: 6 fill, 12 square, 0 whole, 1 phone; both of his worked examples agree.
* A model asked for a horizontal position on three frames laid side by side answers across the strip (0.22 for a
  subject at 0.66): stack the frames top to bottom when a coordinate is wanted.
* Borderline clips flip between runs (C08, C15 on RO-10). The verdict is cached per source span and prompt, and Dan
  sees all of them with the three crops.

**2026-10-02, Dan: fill more of the screen.** The three shapes become a continuous side crop (the narrowest window that
keeps what the clip is about, any shape between the whole clip and full screen); VIDEO-RULES "Verticals and squares".
Not built yet: `Handoffs/handoff-20261002-vertical-kit-round3-fill-more-screen.md`.

**The calmer camera (Dan, 2026-10-01).** `kit_track.py --tolerance` (default 6 source px): the crop lands on him at
every cut, then holds until he is that far off its centre, and only then follows (`_shared/cut/landing.py`, off by
default for every other caller). RO-10: crop travel 10,759 to 7,194 px (33 % less), p90 pan speed 62.9 to 36.4 px/s
(42 % less); `--tolerance 20` is 68 % / 64 % less with him 17 px off centre at the median. The ceiling is the gate's own
centring bound (a hold's median head centre within 6 % of the width, 36 source px).

**Not proven yet on a sheet build (2026-10-01):** `kit_plan.py` and the gate pre-check, the judges, the fold and the
cutdown. The gate's ad ranges (`picture.json`) were measured on Muhammad's 3 to 4 minute ads; RO-10 (an 8:38 organic
film) plans to 0 flashes (his 2.5 to 3.8 per minute), 0 CTAs (2.7 to 3.3), 2.2 inserts per minute (2.4 to 8.5), 27 %
insert coverage (34 to 64 %) and a 49 s longest talk stretch (12.6 to 29.9 s). Those bounds are NOT to be moved;
which format gates a vertical of an organic film is Dan's ruling.

## An editor's master in Soft Blue Light (2026-10-01, AV-11 Ad 13) -- `kit_run.py --master ... --sbl COPY.json`

For Dan: Muhammad's finished ads still have to be measured (there is no answer sheet), but their graphics no longer come
out olive. After the kit has recovered his edit, `master_to_sbl.py` turns what it found into Soft Blue Light graphics
drawn with HyperFrames, and the build continues on the sheet path's graphics and picture stages.

| his graphic (recovered) | Soft Blue Light at 9:16 |
|---|---|
| lower third | `lower-third/` (Motivation): a topic line + the point, each part rising on its word |
| text screen (text left, Dan right) | `side-list/`: the 3A card at the bottom, Dan full frame above, items on their words |
| title / price card | `title-card/` (with rows: a bill that adds up) |
| phone beside Dan | `media-card/`: the whole phone in a card |
| white flash on returns | kept (`render_sbl.py` draws the kit's schedule in Soft Blue white): transitions stay the editor's |
| corner running-total chip | `tally/` exists, but at 9:16 Dan's head fills the top of the frame: fold the total into the price cards |

The words are editorial and live in the build's `sbl_copy.json` (format in `master_to_sbl.py`'s docstring), never typed
into content.json: topic + key-point parts with the PHRASE each lands on, list headings and items, bill rows, and
`pictures` / `media` to swap his low-resolution lift for the clean library original (AI clips fill the frame from their
9:16 originals; a lift that carries his burned olive graphic is replaced; phone lifts are cropped to the phone).
Stages: `recover measure content` (unchanged) then `restyle setup audio kit base track graphics labels words`, then
`kit_deliver.py captions` and `sbl_page.py --sheet B/sbl_sheet.json --media` for the graphic-lock page. The full picture
is rendered only after Dan locks the page.

Lessons (AV-11): a landscape photo of Dan cannot take a full-bleed chip (kit_labels stops): it goes whole in a card.
A lift's first frames can sit inside his blur-in: use the library still. Fix caption spellings in `ref.whisper.json`
after `setup` and before `words`. HyperFrames `check` fails a mask pass in which nothing moves between entrance and
exit ("Timeline did not advance under seek"): give every template a slow drift on a wrapper the mask shares.
A lower third wraps at part boundaries and balances its lines (`vertical.lt_scenes`). A tall card under running
captions ends above the caption line (`media_card_scene(caps=True)`).

### A later round on a master build (2026-10-02, Ad 13 round 2; recipe `../ad13-r2/`)

* The copy file can now add a picture the master does not have (`add_pictures`, explicit times: a new AI opener over his
  talking head), merge several of his pictures into one clip (`until` on the first, `"drop"` on the rest), and keep his
  flash on a card swapped for a full-bleed picture (`flash_after: true`; without it the plan loses the flash and
  `build_kit.py` stops on `flashes_per_min`).
* `sbl_page.py` with `only_media` in page_extra.json shows only the changed pictures under the IDs Dan already reviewed.
* A 9:16 AI opener under the hook lower third: the strip sits at 51 to 68 % of the height, so every face and the action
  must be in the top 45 % of the frame. The first frames had the lower third over the dad's face.
* Unapproved AI motion goes in as START then END stills with a yellow PLACEHOLDER tag (two `img` beats); give a redone
  frame a new file name, because the segment cache is keyed on the media path.
* Calmer camera on this ad: `kit_track.py --tolerance 12` (round 1 was 0): travel 6,655 to 3,910 source px.
* YouTube downloads fail on this Mac; Dan's own 4K screen recordings of old-channel pages are in the library's
  `08 SixPackAbs Archive` (the Crazy 3 Min Home Abs page: `3 min ab workout b roll.mp4`).
* The new 16:9 in Soft Blue Light (`../ad13-r2/h16x9.py`, first minute only, NOT a kit stage yet): `base.mp4` (his cut
  and grade) + his zoom from `auto/framing.json` + `from_plan.py` lower thirds and 3A card + title card, tally chip and
  media cards laid out at 1920x1080 through a second copy of `vertical.py`. Dan has not approved it yet.

### The full build on a master, in Soft Blue Light (2026-10-03, Ad 13 round 3; recipe `../ad13-r2/`)

For Dan: the first full vertical on this path passed the gate (39 rows) after four renders. Every re-render came from a
judge finding, and each cost about an hour, so the checks below go BEFORE the first full render next time.

* **Check the picture take against his master before rendering.** The recovery laid another take of a repeated line
  under his words (segments 60 and 61: roll 266.9 where his audio is roll 370.9; 2.3 s of lips not matching at 3:48).
  For every picture segment whose `src_in` differs from its audio segment's by more than a second, compare three frames
  with his master. The fix is in `edl_picture.json`; after it NEVER rerun `kit` (it rewrites the file) or `track`
  (it drops hand patches): rerun `kit_base.py`, the track by hand, then `--from graphics`.
* **`render.py` crop steps are on the frame grid now** (`_SEGS` / `_SPLICES` from `n0`, expression time from the seek
  point): the crop used to move one frame before or after the picture at cuts whose `cut_in` or beat `t0` sat off the
  grid (judges: 2:14.9, 3:20.0 early; 2:10.3, 2:16.0, 2:51.9 late).
* **A phone lift from his master is cropped to the bare screen** (`round3/phone_screens.py` in the build: inner bezel
  edge, corners painted with the screen's colour). His bezel and grid inside our card read as a phone in a phone, and
  judges and the reviewer both block it. The same goes for WV-01's phone shells: crop to the app screen.
* **A real photo of Dan on a phone screen needs the real label for as long as it shows** (`label_kind` + card-relative
  `label_spans` on the picture in the copy file). `sbl_graphics.py` used to subtract `t0` from spans that were already
  relative, so the chip never drew. A label added after `kit` has run must also be put in `beats.json` by hand.
* **One hold past the gate's centring bound at `--tolerance 12`** (7.4 % at 3:14): splice that segment's samples from a
  `--tolerance 0` track into `facetrack.json`; never touch the bound.
* **Keep the judged round before re-rendering.** `prewatch` overwrites `watch/`. Copy `watch/`, `negscan/` and
  `logs/findings_part*.json` to `roundN/judged_vK/{watch,negscan,logs}` first, then `carry_verdicts.py --prev` it. When a
  new label splits a card, later strips are renumbered: match them by the name after the number.
* **The horizontal** (`../ad13-r2/h16x9_full.py`): flashes measured off his master, phones as full-screen phone cards,
  no burned captions (declared in the plan with the reason). Its gate cannot measure three framing rows (no per-shot
  window data) and fails `cut:jump_cut` on his own same-framing cuts until they get a zoom step.

### Ad 6 lessons (2026-10-02, AV-05 + AS-04)

* The copy file gained four tools (`master_to_sbl.py` docstring): a lower third entry with `"fact"` turns his corner
  picture + tag ("Age: 38") into the full-screen `before-card/` (pass `"whole": true` so a before photo keeps its
  stomach); `extra_beats` adds a picture the recovery did not list (his two small photo panels beside Dan at 2:29);
  `extra_lower_thirds` adds a lower third where a replaced lift carried his burned text; a `pictures` value of
  `"drop"` removes a sliver of his transition that was lifted as a picture.
* A person who fills the 9:16 frame leaves no clear spot for a chip: `kit_labels.py` refused four fill clips of other
  men and the phone-in-hand clip. They go in a centre-square card (`{"ar": 1.0, "ox": ...}`), chip under the hole.
  Decide this BEFORE the labels stage: each refusal costs a 15 minute pass.
* A landscape or chest close-up photo of Dan goes whole in a card with the real label (the flag photo, photo-180).
* `build_kit.py` counts talk under a 3A side card (`hfov`) as his window, not bare talk, for `longest_talk_hand_s`
  (it read 40 s on a design that matches his). His own master had 8 flashes; a bleed that replaces his flashed card
  keeps `flash_after`.
* exFAT costs 2 MB per symlink: the caption frame sequence (one link per frame) took 16 GB and filled the drive.
  `captions.py` now stages it under `~/.cache/absbyai/` when the build is on exFAT. `auto/ocr_frames` (3 GB) and
  `auto/r_*.rgb` can be deleted once `content` has finished.
* The square look for a vertical build: `sq_look.py` (stills of every graphic at 1:1 + a moving sample), layouts in
  `_shared/hyperframes/square.py`.

### Ad 6 round 2 lessons (2026-10-03, AV-05 + AS-04: full builds and the first Soft Blue Light square)

For Dan: this round built all four files after the look was locked. The kit now also builds the SQUARE of a Soft Blue
Light vertical (it had none), and seven faults that only a full build shows are fixed in the kit.

* **The square of a Soft Blue Light build: `sq_render.py` + `sq_plan.py`** (docstrings have the commands). It reads the
  locked vertical build and writes its own folder: `fit` (every picture fills the square or goes in a card WITH ITS
  REASON, our chip placed by measuring the person on the square frames), `graphics`, `picture`, `mux` (the vertical's
  audio stream, md5 asserted), and `--cut` for the 59 second square from the vertical's `cut_plan.json` and its own
  re-grouped caption track. `sq_plan.py` derives the `ad1x1` gate plan from the vertical's. Editorial choices live in
  `<square>/sq_copy.json`. ⚠ MUX BEFORE GATING: a gate run on a file muxed from an older picture passed this round.
  ⚠ Never render the square while the vertical is rewriting `captions.mov` (the renderer now stops if the track is short).
* **A clip of an editor's master can carry a letterbox** (4 px bars top and bottom on three of Muhammad's AI clips; 7 px
  on a full-frame fill). Check every lift's first and last rows; trim the clip, never stretch it.
* **An AI clip with its own internal cut**: a card that starts on the cut frame flashes two frames of the other shot, and
  a slowed clip that runs past its end loops back to frame 0 (`-stream_loop`). Find the cut by frame difference, start
  after it, and never slow a clip to fill a slot: play it at natural speed and return to Dan.
* **A phone lift keeps the editor's backdrop in its corners** (olive on a blue card). Mask it per frame (the phone is
  still landing in the first frames) with a feathered edge, or crop the lift to the phone.
* **`kit_labels.py`**: chip sizes go down to 24, and `labels/prefer.json` lists placements measured beforehand, tried
  first under the same validation. Run a fill-or-box trial (`<build>/filltrial/trial.py`) BEFORE the labels stage: each
  refusal costs a 25 minute pass. Test the 9:16 clips too, not only the 16:9 ones.
* **`kit_plan.py`**: the word aligner can hand a pause to the word before it ("38," ended 0.4 s late), and the gate then
  reads the word's own audio as an abandoned take. A word's end is pulled back to a measured pause when the ASR agrees.
* **`cutdown_pick.py`**: `--list`, `--search N --must "9|14,27|36"` (every selection its checks accept, no model call)
  and `--ranges "0-3,33-37,..."` (a hand pick under the same checks). The model failed five times on Ad 6 (about $1):
  the hook, the demo and the CTA all play with captions paused, and half the cut must carry captions. A range that would
  open a few frames before a picture change is moved to the picture's own start by editing `cutdown_ranges.json`.
* **`kit_cutdown.py`** maps the caption lifts (`CAP_LIFTS`) into the cut; unmapped, captions printed over a side card.
  **`kit_plan_cutdown.py`** no longer declares a one-frame level under a picture at a range start.
* **`kit_fold.sh`** takes `FORMAT=ad1x1`. `carry_verdicts.py` after every small fix: one judge re-reads only the changed
  images. Clear stale images from `cut_audit/watch/` before judging a rebuilt cutdown.
* **The camera after the 2026-10-03 standard (land, then hold): measure it, the watch strips cannot see it.**
  `camcheck.py VIDEO W H [bound]` (run in the build dir) measures the sideways shift of the background strips between
  consecutive frames in every talking shot and lists isolated one-frame crop steps that are not on a cut. Run it on the
  muxed file BEFORE any judge. What it caught on Ad 6, after two rounds of judges measured the same thing by hand:
  the shared `kit_track.py` adds all four times of every push as landing anchors, so (1) each gradual zoom-out began
  and ended with a one-frame sideways jump of 20 to 90 px, and (2) an instant step, which sits half a frame before its
  cut by design, rounded onto the frame BEFORE the cut at some cuts, so the crop changed a frame early. Zoom times are
  not landing anchors: every instant step is on a picture cut, which the segments already carry. Ad 6 used a
  build-local copy without them (`<build>/kit_track_ad6.py`); the shared tracker still needs that change.
  ⚠ `push_z_expr` is already right (the half-frame lead makes the step land on the cut frame): a "snap to the frame
  grid" patch tried here moved the zoom a frame early at nine cuts and was reverted.
* A square-only start for one graphic: `sq_copy.json` `"graphics": {"L12": {"a": 130.9}}` (a bottom lower third over a
  tall card forces the card small). `"prefer"` on a picture lists label spots measured on an earlier build.
* `kit_deliver.py mux` tags the full BT.709 (the caption overlay dropped the matrix tag; ffmpeg and VLC read an
  untagged file as BT.601). ⚠ Never `pkill -f` a pattern containing `|` from a file name: it is an OR. ⚠ In zsh an
  unmatched glob in `rm -f a*.json && ...` aborts the chain: the gate then reports the PREVIOUS run's json.
* **Two cards back to back are one card: `plate_join.py`.** Each card beat gets its own plate, so on the join the accent
  line snaps back, the blue field resets and a phone card's "AbsByAI.com" heading blinks off for five frames (Ad 6,
  2:08 and 4:21, flagged on both formats once the picture under the cards stopped moving). After the graphics stage:
  `plate_join.py --hf B/hf --first <plate id> --second <plate id> --n1 <frames of the first> [--square]` renders one
  plate for both and splits it by frame index (proved on the pixels); the second card takes the first's hole.
  ⚠ Both clips must be the SAME master box: Ad 6's two phone lifts were cut 4 px apart on every side, so at one card
  height the phone in the second was 0.83 % smaller and stepped on the join (it always had; the join made it visible).
  Template-match each lift's first frame in the master to read its box, crop the second lift to the first's box. The
  graphics stage should do this itself for consecutive cards of one clip or one phone demo.
* **An AI clip is checked frame by frame before it is used** (frame difference against the clip's own median, then the
  eye). A0002's phone-held-up half pops every 15 to 25 frames (the phone hops, the hand reshapes, the photo on the
  screen morphs); judges read it first as a splice, then as an AI giveaway. Ad 6 uses one clean frame with a slow push,
  warped on the YUV planes so the colour is untouched (`<build>/ai_phone_still/make.py`).
* **The square's phone-card heading** needs the vertical's 84 px above the card (`square.py` now reserves it); at the
  default top it sat on the card's accent line.
* **A judge list must name every image without a verdict, pairs included.** A pair whose strip was carried is otherwise
  never judged and the gate's watch row fails after a 20 minute fold.
* **A clip graded to match a reference is checked on the DELIVERED file, never on the asset.** Every RGB round trip in
  ffmpeg at default settings lowers each level by about 2 (5 reads 3, 20 reads 18), and a bleed passes through four of
  them plus the bleed vignette: Ad 6's plank clip went in at 0.99 of its reference and came out at 0.80 in the shadows.
  Recipe (`<build>/plank/`): `make_v3.py --measure` reads the end to end curve (asset level to delivered level) from
  the current build, `make_v4.py` applies its inverse and divides by `vignette_soft.png`, and `verify.py VIDEO [card
  rect]` compares delivered patches with the reference after ORB alignment. A card in the square loses about 3 levels
  (no vignette). Fit colour in two passes: a global curve plus cubic, then a shrunk 17-point residual grid (the global
  fit alone left skin yellow). The same loss applies to every clip the kit re-renders, including the talking head; it
  is part of the approved look and was not changed here, but the renderer's scale steps want `accurate_rnd`.

### Sheet-path lessons (2026-10-01)

* Grade in the 16:9's own order (`grade.order`): a float LUT on the 4K crop ran at about 3 frames a second; scaled to
  1080 first, as the 16:9 did, the 8:38 conform takes about 5 minutes and matches its look.
* A killed conform can leave a half-written segment that the next run skips as "exists". `kit_base.py` then fails its
  own frame count (it did: 15,385 of 15,532); delete the short segment, never the check.
* exFAT writes `._` twins of every file: glob results from the Extreme drive must skip names starting with `._`.
* `top` is not a legal `const` name in a HyperFrames page (it is a window property); `check` catches it, `lint` does not.
* The raw of a 16:9 studio film is already a medium close-up: the vertical's widest level (the whole hair-anchored
  window height) cuts the shoulders. That is the footage, not a setting.

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
