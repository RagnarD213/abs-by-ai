---
name: shortad-from-longform
description: ADS ONLY. Rebuild a FINISHED, approved AD as its vertical 9:16, its 1:1 square and its ≤0:59 cutdown, reproducing the finished ad's style: first verify the editor's HD export is the draft Dan approved with no new errors (so Dan never has to watch the export), then recover its edit, measure its grade and graphics, and re-lay them out for a phone or a square feed. Use whenever Dan asks for a vertical, 9:16, square, 1:1 or 1-minute version of a finished ad, to "make a short ad from" an ad cut, or for a square and its ≤0:59 cutdown for Google Ads Demand Gen / Meta feed, even if he doesn't say "/shortad-from-longform". Never for content videos (LFC, SFC, SFL): their Shorts come from /shorts. For editing an ad from raw shoot footage use /ad-edit.
---

## Edit slot first (Dan, 2026-10-21)

At most 5 edits do production at once. Before this edit's first production step (render-queue job, AI generation,
build) and on every resume, run `python3 .claude/skills/_shared/editcap/editcap.py acquire <JOB> --title "<title>"
--type <LFC|SFC|SFL|AD>`. Exit 3 = waiting: no rendering, generating, building or spending (read-only prep is fine);
run `python3 .claude/skills/_shared/editcap/editcap.py wait <JOB>` with `run_in_background`, tell Dan the place in line
in one line, end the turn, and continue when it exits. Review page up or stopping for Dan: `editcap.py release <JOB>
--review`. Edit finished: `editcap.py release <JOB>` (if it prints `WAKE claude <id>`, send that session the message).
Rule: `_shared/VIDEO-RULES.md`, "Active edit cap"; tool: `_shared/editcap/README.md`.

## Video editing task names (Dan, 2026-10-16)

At the start of a video editing/review task, name the chat `<Recognizable Video Title> <Type> R<round>` under the [shared naming rule](../_shared/VIDEO-RULES.md#video-editing-task-names-dan-2026-10-16). Use LFC for long-form, SFC for dedicated shorts, and SFL for shorts extracted from long-form; paid ads use `<Title> AD R<n>` (existing V/S/Sh format markers may follow AD). Put the recognizable video title first, omit internal job codes and generic action prefixes, and use the same name in handoff prompts. Asset/brief work supporting an existing editing task keeps that task's name and round.

> **Image generation: Codex only (Dan, 2026-10-01).** Every still image this skill generates (backgrounds, plates, AI frames, thumbnails, covers, posts, retouch passes) is made with `.claude/skills/_shared/codex-image.sh` on the ChatGPT subscription. Where the steps below name Nano Banana Pro, Gemini, Seedream, FLUX, `gemini-image.js`, `rep-t2i.js` or `replicate-edit.js` for a still image, use the helper instead. Read `.claude/skills/_shared/IMAGE-GENERATION.md` first. AI video clips: every one is made in Google Flow on Dan's subscription by the background `flow-veo` agent; paid Replicate only when Dan says rush (VIDEO-RULES "AI video clips: Google Flow subscription first, paid API only on \"rush\"", 2026-10-17).

Read `_shared/VIDEO-RULES.md` first.

## How to build today: the kit (`reference/kit9x16/README.md`)

Steps 1 to 8 of the old hand pipeline are what the kit does; do not hand-run them (they are kept, word for word, in
`reference/LESSONS.md`). The commands, all from `reference/kit9x16/` (full detail and every stage's lesson in its README):

```
kit_run.py --master HIS.mp4 --build B --name "<title> | claude | 9x16 | ad N" --shoot <shoot folder> [--deliver <ad folder>]
kit_run.py --master HIS.mp4 --build B --sbl COPY.json ...      # an editor's master, his graphics redrawn in Soft Blue Light HyperFrames
kit_run.py --sheet SHEET.json --build B --name "..."           # our own 16:9's edit sheet (never reverse-engineered)
sbl_page.py --sheet B/sbl_sheet.json --media                   # the graphic-lock page for round 1
kit_deliver.py audio --build B --mode master --approved <the approved vertical>   # his mix, stream-copied, gate --verbatim
kit_deliver.py gate  --build B --video <name>.mp4 --reference-cut <his master> ...  # audio gate, plan, watch pass; stops for the judged watch pass
kit_cutdown.py                                                 # the <=0:59: his mix only cut at the seams
```

Square builds gate with `--format ad1x1` (`reference/a11_sq_ad1/plan_sq.py` writes the plan); verticals with `--format ad9x16`
(`reference/plan_build.py`). Builds run in the background; heavy steps wait in the render queue on their own (VIDEO-RULES
"Video builds: the render queue", 2026-10-20; `python3 .claude/skills/_shared/renderq/renderq.py status` shows the line).
`ffmpeg`/`ffprobe` are NOT on PATH: use `Media/video_edit/bin/` (gitignored, present on Dan's Mac).

## Audit 2026-10-20: rules that now govern

This file used to contradict these; where older text below disagrees, the rule named here wins.

- Ads only: VIDEO-RULES "Categorize every video before editing it" (2026-10-04).
- Graphics: VIDEO-RULES "All new or revised video graphics move in Soft Blue Light HyperFrames" (2026-10-17); olive retired for new verticals (`reference/kit9x16/README.md`, 2026-10-01).
- Analysis card: VIDEO-RULES "The analysis card is Soft Blue Light, built with HyperFrames, in every video" (2026-10-14).
- Fill the frame: VIDEO-RULES "Verticals and squares: fill as much of the screen as the clip allows" and "Squares and verticals: fill the frame, no boxes without a reason" (2026-10-02).
- Crop motion: VIDEO-RULES "Verticals: the camera lands on Dan, then holds" (2026-10-03, locked 2026-10-05).
- Rounds: PRE-RENDER-APPROVAL.md decision budget; VIDEO-RULES "Short-form and ads: build the whole video instead of only the first 30 seconds when it is nearly approved" (2026-10-14) and "Video rounds start automatically; editor chooses same task or fresh handoff" (2026-10-20).
- Audio: VIDEO-RULES "Audio: one standard, enforced by a stamp" (editor's mix untouched, 2026-09-10); our own mixes: "A subtle bass lift on his voice is the standard" (2026-10-12).
- Gate: VIDEO-RULES "One delivery gate, versioned, on the delivered file" (2026-09-11; `qc.py` retired 2026-09-16).
- Real-photo label: VIDEO-RULES "Real-photo labels include touched-up photographs" (2026-10-17).
- AI clips: VIDEO-RULES "AI video clips: Google Flow subscription first" (2026-10-17) and "AI clips that make no physical sense, or do not show the line, never reach Dan" (2026-10-13/14).
- Hair: VIDEO-RULES "Head and hair clearance blocks review delivery" (2026-10-20).
- Reviewer model: AGENTS.md "Model routing" (2026-10-02): reviews on Opus 5.5, Fable escalation only.
- Review copies: VIDEO-RULES "Review videos also go in `Videos to Review/`, for VLC" (2026-10-08).
- B-roll: VIDEO-RULES "All B-roll is colour corrected before it goes in a video" (2026-10-11) and "Clip library first" (2026-09-29).
- Thumbnails: VIDEO-RULES "Thumbnails: the five, each its own design, always made by Codex" (2026-10-13), via `/ad-setup`.
- Builds: VIDEO-RULES "Video builds: the render queue" (2026-10-20).
- Task names: VIDEO-RULES "Video editing task names" (2026-10-16).

## This skill is for ADS only (Dan, 2026-10-04)

The vertical, the square and the 1-minute cut are made from an AD. A long-form content video is never given these
formats: it gets Shorts through `/shorts`. Check the category before any work (VIDEO-RULES, "Categorize every video
before editing it"). If the video is content, stop and tell Dan in one line; only his own words naming that video and
that format override it. `kit_run.py` refuses a content edit sheet without `--dan-asked`.

## A horizontal clip in the vertical or square frame keeps its full height (Dan, 2026-10-01)

Never crop rows off a 16:9 clip that sits as a card in a 9:16 or 1:1 frame: it only makes the card shorter and adds black
space. Dan: *"There's not ever any reason for you to crop horizontal videos within a vertical frame and make them shorter than they already are. There's already too much black space, so avoid crops like you did on that first draft of the power lifter clip that unnecessarily make the video shorter when we have a horizontal within a vertical frame."* Crop the sides to make a card taller if nothing essential is lost; never the height. An editor's
burned pill stays whole inside the card and our duplicate bar comes off for that shot (SL-05 short 3, round 3). In
`shorts/reference/zeeshan-master/plan_shots.py` terms: no `cardCrop` with a y range short of 0-1. Full rule: `_shared/VIDEO-RULES.md`.

## Cutdowns stand alone: show the whole exercise, not a detail of it (Dan, 2026-09-30)

Applies to every <=0:59 cutdown of a long-form ad. Full rule: [VIDEO-RULES.md](../_shared/VIDEO-RULES.md#shorts-stand-alone-show-the-whole-exercise-not-a-detail-of-it-dan-2026-09-30).

- **A short must make complete sense to a viewer who never saw the long-form.** Leave out details that only work
  with the full video's context: a set-up step, a position check, a reference back to something said earlier.
- **When a short tells the viewer to do an exercise, show the whole exercise briefly:** a few complete reps (a demo or
  live-round clip from the same source), not an isolated detail of it. A detail cue (grip, thumbs, arm angle, elbow
  height) stays only when the complete movement is also on screen in the same short.
- Dan, approving SL-04 short 1 round 3: *"we want to avoid including details in it that won't be understood if the
  viewer didn't watch a full long form... if we say to do a certain exercise, rather than just showing individual
  details that don't make sense without full context, show the full exercise briefly."* Why: round 2 ended on the
  side-lateral arm-angle set-up with no exercise shown (*"It's not clear why I'm showing them the arm angle when I
  don't show the complete exercise"*); round 3 replaced it with his thumbs cue plus live-round reps and was approved.
- How to apply: at segment selection, for every exercise a candidate names, write down where its complete movement is
  (inside the segment, or another range of the same source to append, e.g. the live round). A candidate whose exercise
  never appears whole is either paired with a range that shows it or dropped. The reviewer checks it on the delivered file.

## Default jump-cut and junk-footage QC (Dan, 2026-09-29)

Follow [CUT-CONTINUITY-QC.md](../_shared/CUT-CONTINUITY-QC.md) during source selection, before approval previews, and on the exact final candidate. Inspect every actual source/picture join, including reused composites, for a presenter jump without a distinct fixed wide/tight cut or complete approved clip cover. Fix uncovered jumps and recheck every boundary the repair creates. Detect and remove confirmed unscripted noises, empty lead-ins, unnecessary pauses and off-camera resets while protecting complete words, natural breaths and teaching action. Native consecutive frames plus moving/audio context are required; sparse scans and ASR alone cannot clear a join or authorize deletion. Keep the current still/frame, motion and full-render approval boundaries. This dated rule supersedes older suggestions that a pose match or audio fade alone clears a naked cut.

## Approval before the full render (Dan, 2026-09-26)

> **ROUND METHOD, READ FIRST:** follow [PRE-RENDER-APPROVAL.md](../_shared/PRE-RENDER-APPROVAL.md) (Codex's stepwise approach, Dan 2026-09-28) and its decision budget; never one-shot a video. **For a vertical or square of an APPROVED ad**, round 1 is the graphic-lock page (`reference/kit9x16/sbl_page.py --media`) plus the WHOLE video, unless it brings a new graphic family or an AI clip Dan has not seen (VIDEO-RULES "Short-form and ads: build the whole video instead of only the first 30 seconds when it is nearly approved", 2026-10-14). Rounds advance on their own (VIDEO-RULES "Video rounds start automatically; editor chooses same task or fresh handoff", 2026-10-20).

## Graphics: Soft Blue Light in every video (Dan, 2026-09-26)

Every new or revised graphic uses the approved Soft Blue Light family, and every lower third uses the Motivation format with a topic that fits the narration. Spec: [GRAPHICS-STANDARDS.md](../_shared/GRAPHICS-STANDARDS.md). Build with the HyperFrames templates in `_shared/hyperframes/`, moving for the graphic's whole screen time (VIDEO-RULES "All new or revised video graphics move in Soft Blue Light HyperFrames", 2026-10-17); [SOFTBLUE.md](../_shared/SOFTBLUE.md) holds the look. Older palettes and graphic systems described further down (J2/olive, `motionlib` GREEN/J2AD/MIL/PAPER, graphics rebuilt from Muhammad's) are historical: use them only to re-export an already approved olive vertical. Cutting, camera colour, audio, captions and transitions keep the rules below.

For format conversions of an editor's master: `kit_run.py --master HIS.mp4 --sbl COPY.json` redraws his graphics in Soft Blue Light HyperFrames (`reference/kit9x16/README.md`, "An editor's master in Soft Blue Light", 2026-10-01: the Ad 8 verticals were the last olive delivery). Olive/J2 stays only for re-exports of an already approved olive vertical.

**Left-third text/list graphics (Dan, 2026-09-28):** use the approved 3A card exactly in every horizontal video (today the HyperFrames `side-list/` template, `_shared/hyperframes/side-list/`); squares put the full-width card at the bottom; verticals keep the full-frame camera crop with the card over it at the bottom (locked 2026-09-28); never the card mid-frame over Dan. Spec and references: the 3A section of [GRAPHICS-STANDARDS.md](../_shared/GRAPHICS-STANDARDS.md). Adapt only the heading and points, and show one short contextual sample before a full edit.

# /shortad-from-longform — a finished long-form cut, rebuilt vertical

## Edit queue status — REQUIRED when this video is a job on Dan's edit queue

If the video is on `Handoffs/video-editing/00-MASTER.md` (IDs like `RA-01`, `DS-04`, `RO-02`, `SL-01`, `AV-05`, `AS-04`),
keep its status current on Dan's pinned **Abs By AI Edit Queue** page: `in_progress` when you start building,
`delivered` when the review copy goes to Dan, and **`finalized` the moment Dan says it is finalized / approved** (his
words, never a passed gate). Never set `uploaded` here; that is `/ad-setup` (ads) or `/video-setup` (organic), after
the upload. Procedure (one script call + one `Artifact write_db`): `.claude/skills/_shared/edit-queue/README.md`.

## Square and vertical camera movement (locked 2026-10-05)

Verticals and squares land on Dan after every cut and hold until he drifts 3.3 % of the crop width: shared `_shared/cut/landing.py` (scaled vertical preset; `kit9x16/kit_track.py`, 20 px dead band). Rule: VIDEO-RULES "Verticals: the camera lands on Dan, then holds" (2026-10-03, locked 2026-10-05, `Docs/VERTICAL_CENTERING_CODEX_20261003.json`). Older tracking numbers further down (80, 170, 200 px/s; one fixed crop) are history. For approved-master adaptations, preserve the existing zoom, framing height, edit and audio.

**The finished video cannot be reframed. It has to be REBUILT.** A finalized cut has
graphics, captions and lower thirds burned into the pixels; crop it to 9:16 and you crop
its type. The only honest route is to re-cut from the ORIGINAL RAW FOOTAGE and rebuild
every graphic in a vertical layout.

That sounds like starting over. It isn't — because the finished cut is a complete,
machine-readable specification of itself. **Everything the editor decided can be measured
back out of the render**: which takes they used, every pause they trimmed, their tone
curve, their vignette, their palette, their type, where every insert sits, how loud they
mixed. Recover those, and the rebuild is a conform plus a layout pass, not a re-edit.

Two deliverables, always:
1. **the full-length 9:16 master** — same script, same beats, same order as the reference
2. **a ≤0:59 cutdown** selected out of that master (never re-cut from source)

---

## Step 0 — get the reference and the raw, and never confuse them

```bash
python3 -m gdown <DRIVE_FILE_ID> -O reference.mp4      # installed for python3.9
```
`ffmpeg`/`ffprobe` are NOT on PATH — use `Media/video_edit/bin/`.

**Confirm which video and which editor before you measure anything.** Dan runs tryouts
where several editors cut the same script; a Drive file's owner is often not the person
he names in chat. Check `get_file_metadata` → `owner`.

Probe both, and transcribe the reference with local Whisper `small`, `word_timestamps=True`.
You need the raw roll's word timestamps too — a previous /ad-edit or /longform-edit session
has usually already written one (`<ROLL>.whisper.json`); reuse it.

---

## ⚠ Step 0b — WATCH HIS HD ONCE AGAINST THE DRAFT DAN APPROVED, BEFORE ANY CUT (Dan, 2026-09-11)

*"Watch the video once before making the cut, just to ensure the high-definition version is exactly
the same as the last approved draft and that no new errors got introduced in the high-definition
version. This way, I can skip watching that final export."*

**Dan no longer watches the editor's HD export. This step is his watch, so it is never skipped.**
The vertical inherits the HD frame for frame and bit for bit (his audio goes through untouched), so
any fault in the HD ships in our master and our cutdown. Hours of recovery and render on a bad
HD are wasted. Do this step before Step 1.

1. **Find the approved draft**: the file Dan's LAST round of notes was written against, or the
   cut he approved outright. The revision doc's last round names it (a Drive link). The
   `/revisions` sessions leave their downloads in `/Volumes/Extreme/_edit_work/revisions-MMDD/dl/`
   (e.g. `ad5_v3.mp4`); otherwise `gdown` it from the doc's link. Confirm the Drive owner is the
   editor, as in Step 0. **If you cannot identify which draft was approved, the step has not run.**
   That counts as a failure, not a pass: say so to Dan and do not start the cut.
2. **Run the comparison** (~35 s for a 4-minute ad; a light decode, not a build):
   ```bash
   python3 reference/hd_vs_draft.py --hd "<his HD>.mp4" --draft "<approved draft>.mp4" --out <build dir>/hdcheck
   ```
   It diffs every frame (96×54 grey, MAD > 6 = changed; calibrated on Ad 2 V1→V2 and Ad 5) and
   every second of audio after aligning both timelines. It also checks what only an export can
   break: frame size and rate, frame count, whether the end still lines up, a truncated audio
   stream, a new silent second, new clipping, a new frozen or black run, loudness and true peak,
   and **whether the HD is real HD or an upscale of the draft**. That last check is spectral:
   real 1080p reads about −12 dB (Ad 5's HD, full file: −13.7), a 540p/720p upscale −19 to −21,
   gate −16. A real HD that fails close to −16 (soft or dark footage) gets a full-res look at `spot/`
   and a note to Dan. Never move the gate to pass it. It writes `hd_vs_draft.json`,
   `strips/` (HD over draft, consecutive frames at the start and end of every changed window,
   full resolution) and `spot/` (ten full-res HD frames).
3. **Look, don't just read the verdict.** Open `spot/` (compression blocks, a wrong crop,
   letterboxing and a missing graphic show there first) and every strip in `strips/`.
   * **Exit 0, IDENTICAL**: every frame Dan approved, and nothing new. Proceed.
   * **Exit 1, DIFFERS**: **match every changed window, audio second and end offset to a numbered
     note in Dan's last round.** A change explained by a note is expected. Watch its strips for
     the damage a revision causes: a naked jump cut where an insert was removed (Step 7c), a
     graphic that lost its timing, a clipped word at the new splice. **Then check the reverse:
     every note in that round must appear as a change.** A requested fix that is missing gets
     reported, not silently inherited. Ad 5: Muhammad's HD carried the round-3 limiter fix
     (true peak −0.2 → −1.0 dBTP) but not the round-3 2 s end hold. An UNEXPLAINED change is a
     new error: stop.
   * **Exit 2, EXPORT FAULT** (or a measurement that could not run): stop.
4. **When you stop**, tell Dan in a few lines: what differs, the timestamp, the strip, and whether
   it is a new error or a missing fix. He tells the editor. Do not start the cut on an HD that
   has an unexplained difference unless Dan says to build on it anyway.
5. **Report it either way.** The first section of `notes-vertical.md` is **"The HD export vs the
   approved draft"**. Use Ad 5's notes as the template: same cut or not, frame counts, the
   largest per-frame difference, mix correlation and level, loudness/TP of both, each change
   with the note it answers, and each note not done. Put the one-line verdict in the delivery
   message too, because it is what lets Dan skip the export.

What this step cannot see is a fault that was already in the draft Dan approved. That is his
approval, not our gate. Our own watch pass (Step 7) still runs on the vertical we build.

---

## Step 4 — AUDIO, BEFORE ANY OF THE PICTURE WORK

> ## ⚠⚠⚠ THE EDITOR'S AUDIO, UNTOUCHED. NO GAIN, NO LIMITER, NO MONO SUM, NO LOUDNESS TARGET.
> **(Dan, 2026-09-10, on the Zeeshan Ad 1 vertical: "What the fuck happened to the audio? Zishan's audio
> sounds much better. This is an awful mistake which can't happen again. … Use Zishan's audio.")**
> That build lifted his −23.5 LUFS mix +9.9 dB into a 4×-oversampled limiter, summed it to mono and
> re-encoded it, to pass OUR rows (−14 LUFS, L/R ≥ 0.98) — rows Zeeshan's own mix fails. Every check it
> faced was level-normalised or target-based, so it passed 20/20 while the loudness range fell 5.9 → 4.1 LU.
>
> **The method now, for every vertical or cutdown rebuilt from an editor's finished cut:**
> * **Full length: COPY his audio stream** from his export into the rebuilt picture (`-map 1:a -c:a copy`);
>   `reference/a6/zmux.py` asserts the audio stream's md5 equals his, bit for bit.
> * **Cutdown: CUT his mix and nothing else** — `cut/his_mix.wav`, his decoded mix cut at the seams with
>   4 ms raised-cosine joins, encoded AAC 320k with no filter of any kind.
> * **Gate: `audio_gate.py <file> --reference-mix <his> --verbatim`**, and `"audio_mode": "verbatim"` in
>   `qc.json`. The verbatim rows fail any change to his level (every second within ±0.5 dB), his dynamics
>   (loudness and LRA within 0.3 LU) and his stereo image (L/R within 0.01); the absolute −14 LUFS and
>   L/R rows are declared not applicable, with that reason, because **his mix is the standard.**
> * **If his export is too quiet for a feed, ask the editor for a louder export.** A small constant lift only when
>   Dan asks for one: the approved Muhammad verticals (+4.2 dB, loudness range 3.5 → 2.8 LU, no mono) are its
>   ceiling, and the rejected Zeeshan build (+9.9 dB into the limiter, 5.9 → 4.1, mono) is what past it sounds like.
>   Never a mono sum. Both rejected files are corpus entries (`ad1zee-vertical-processed-audio`, `…-59s-…`); his
>   own export is the approved anchor (`zeeshan-ad1-16x9`).
>
> The history of how we got it wrong (the reference's own mix through gain + limiter, `loudnorm`, the conform-voice
> proxy and bed picking) is in `reference/LESSONS.md`, part 3. Do not revive it. If we ever mix the voice ourselves,
> start from the +3 dB at 120 Hz lift (VIDEO-RULES "A subtle bass lift on his voice is the standard", 2026-10-12).

## ⚠ STANDING RULE — SUBTITLES (Dan, 2026-09-08: "lock this in … make all subtitles going forward this good")

1. **Whisper is the source of the WORDS only. Every caption timing comes from a CTC forced alignment of those
   words to the delivered mix** (`reference/a2/align_ctc.py`: wav2vec2 `forced_align`, one Whisper segment at a
   time with 0.6 s padding, exact segment ownership by order, digits spelled out, the caption FIX map applied
   before aligning, and a monotonic repair for the tiny words the aligner slips). Whisper's own word starts
   measured 128 ms early on average and up to 300 ms on an editor's mix; the karaoke highlight then lights
   the wrong word, and Dan calls that "very confusing … unprofessional".
2. **The last word of a line holds until the next line** (up to 0.8 s), never dropping at its own acoustic
   end — a 40 ms word must not flash for one frame (`captions.py`).
3. **Every delivered file — masters AND review copies — passes `reference/caption_sync_check.py` (qc check
   20) before it goes to Dan:** at the instant each word is spoken the word lit on screen must be THAT word
   for ≥ 97 % of words with no run of three misses, and no highlighted word may sit outside speech. It also
   prints the disagreement against an independent second transcription (Whisper `medium`); if the two
   Whispers agree with each other and not with the alignment, the alignment is broken. The rejected Ad 2 V2
   file scored 44 % on this test; the approved rev 1 scored 98.8 %.
4. **Never trust the plan, measure the pixels:** the gate reads the delivered video's caption band frame by
   frame; a caption stream that is right in `cap/list.txt` and wrong on screen (a mux offset, a stale
   index-keyed PNG cache) fails here and nowhere else.

## THE DELIVERY GATE — `_shared/deliver/gate.py` **(REQUIRED on the delivered file, 2026-09-11)**

```bash
python3 .claude/skills/_shared/deliver/gate.py <delivered file> --format ad9x16 --plan plan.json
```

**One gate, all six video skills, run on the file that is actually going out.** It carries the
union of the rows that used to live in seventeen per-video QC forks, with every bound in
`_shared/deliver/formats.py` beside the file and the date it was measured on. It writes
`<file>.deliver_gate.json`; `gate.require_stamp(<file>)` refuses anything without a PASS stamp at
the current `GATE_VERSION`.

- **A missing input is `NOT MEASURED`, which FAILS** — never a silent skip. `--plan-keys` lists what
  `plan.json` may carry; a row whose key is absent says so and fails.
- **A row this format has not answered for FAILS as `UNCONFIGURED`.** If a check genuinely does not
  apply here, add it to that format's `not_applicable` in `formats.py` with a written reason.
- **Never raise a bound to make a build pass.** `python3 .claude/skills/_shared/qc_corpus/run.py`
  must stay green, and it is what proves a bound change did not resurrect a rejected cut.
- **PNG captions and composite layouts use evidence contract v2.** The caption compositor writes
  `cap/manifest.json`; `plan_build.py` copies its per-word PNG/highlight states, delivered-audio
  word timing, graphic regions, actual Dan-window rectangles, fixed-wide/tracking intent, and
  transformed label states into `plan.json`, then binds all of it to the delivered file's SHA-256.
  Never hand-type or copy this geometry from an older render. A stale hash, missing manifest, or
  missing renderer asset is `NOT MEASURED` and blocks delivery.
  Square builds use `reference/a11_sq_ad1/plan_sq.py` and gate with `--format ad1x1`; vertical builds use
  `reference/plan_build.py` and `--format ad9x16`.
- **Policy candidates are not automatic violations or passes.** Each negative-events finding gets
  `disposition: cleared`, `confirmed_violation`, or `needs_review`. The last one prints NEEDS HUMAN
  REVIEW and blocks the gate until a person records the disposition.

**The shared gate is the only gate (2026-09-16, Phase 3 of `Handoffs/handoff-20260911-video-quality-engine.md`).**
The per-video QC forks that used to sit in `reference/` are deleted; every row they carried, framing and the watch
pass included, lives in `_shared/deliver`, and `python3 .claude/skills/_shared/deliver/gate.py --formats` says what
each format is held to. Do not resurrect a fork from git history to "double-check": a second gate with its own copy
of a bound is exactly how the 2026-09-09 dereverb fix reached one pipeline and missed the other (memory
`shared-fix-may-not-reach-the-pipeline`).
**Framing landed in the shared gate 2026-09-12** (the five `framing:` rows, Step 5 rule 14) and **the watch pass
on 2026-09-16** (`_shared/deliver/watch.py`, the `watch:pass` and `cut:naked_splices` rows).

## Independent review before delivery

### ⚠ STEP 7b — AN INDEPENDENT SUBAGENT AUDIT IS PART OF THIS SKILL (Dan, 2026-09-01)

**"I think calling Fable to review should be a part of this skill going forward."** It has
already overturned my own conclusion twice on the same deliverable, and both times I had
declared the thing fixed:

* it measured a version I had just called centred and found **sd ~110 px, 39 % of talking
  frames beyond 70 px, and two multi-second stretches where his face was cut by the frame
  edge** — which led to the crop-expression bug in rule 0;
* it caught that **my own eyeball reads of "he is off to the left" were MIRRORED** at three
  of four timestamps, which is what broke that bug open.

Model: AGENTS.md "Model routing" (2026-10-02): reviews run on Opus 5.5; Fable is escalation only. One complete-candidate review; after a fix, re-review only what changed (PRE-RENDER-APPROVAL.md, approval order step 6).

So after the watch pass, before delivering, launch a **fresh `ra-reviewer` agent (Opus 5.5, high)** on the exact
delivered file. Give it the compiled `personmask` CLI and the torso anchor, tell it which
beat kinds to judge (talk only), and demand: the population statistics, every contiguous
run beyond 60 px for >= 1 s, full-resolution verification of anything it flags, **and an
explicit opinion on whatever trade-off you just made** — a faster tracking crop can swap a
centering problem for a visible pan, and you are the last person who will notice that in
your own build. Ask it to be skeptical and to say plainly if you have traded one visible
problem for another. Relay its verdict to Dan rather than your own.

⚠ **A subagent that has completed cannot be resumed** — its transcript is gone and
`SendMessage` fails. Launch a fresh one for the re-audit and restate the context.

## Step 8 — THE ≤0:59 CUTDOWN

**Select intervals out of the approved master. Never re-cut from source.** Selection
carries every decision through unchanged; a re-cut re-litigates all of them.

- **[R1] WRITE THE CUTDOWN'S TRANSCRIPT FIRST and read it as prose.** Assemble the
  words the selected ranges keep and read the result aloud as one script BEFORE mapping
  any ranges. Every seam must be both a sentence boundary and a THOUGHT boundary — a
  topic list left dangling ("You're more attractive to women… you feel better." → hard
  cut to the product) is a non-sequitur even when the splice is clean. Attempt 1
  selected ranges by topic doctrine, never read the result, and Dan's verdict was "the
  cutdown makes no sense at all." If the prose doesn't read, change the selection, not
  the seams.
- Content follows Dan's settled shorts-ad doctrine (see `/ad-outlines`): **sell the
  GENERATION almost exclusively**, give the trainer/nutritionist exactly one beat near the
  end, say the CTA twice. Hook, mechanism, proof, CTA.
  (Dan to confirm, 2026-10-20 audit: this doctrine against AGENTS.md "Marketing advice: proven direct response only", 2026-09-24.)
- **Snap every range edge to the nearest beat boundary** (±0.3 s). A range starting 80 ms
  inside a card shows that card already half-open, which reads as a dropped frame.
- Rebuild the captions (re-timed through the range map). The audio is his mix CUT at the seams with 4 ms
  raised-cosine joins and nothing else (Step 4; `kit9x16/kit_cutdown.py`).
- **Assert `total ≤ 59.0` in code.** Shorts ads must never exceed 0:59.

---

## Standing content rules that override the reference

The reference editor does not know Dan's ad rules. Check every beat you are reproducing:

- **NO side-by-side before/after, ever, in a paid ad.** Muhammad's 0:03 card is exactly
  that (heavier Dan left, goal phone right, arrow between). **Cut it sequentially instead** —
  the before photo, then the goal phone.
- **NEVER show the email-capture screen**, and never the app's "Meet the new you"
  before/after screen. In the product recording `clip_109_replacement.mp4` those start at
  **26 s and 29 s** — the usable window is **0–25 s**. Assert it in QC.
- **A before and after picture are the SAME PERSON** (Dan, 2026-09-12: *"don't mix before-and-after pictures… That doesn't really make sense if you change the person."*). Never pair one person's before with another's after — in an app recording, a result screen, a card or a thumbnail. If that person's after does not exist, generate it for THEM through the live product (a real generation, never a composite) or change the before so the pair matches. ⚠ The only real app recording in the asset library uploads a man who is NOT Dan, so every phone demo cut from it inherits this.
- **Dan's REAL physique photos carry the real-photo label (today "Real Photo Of Me, Not AI-Generated", plural "Real Photos Of Me, Not AI-Generated"); AI images of Dan keep AI-GENERATED; every picture of his physique carries exactly one.** Wording and scope: VIDEO-RULES "Real-photo labels include touched-up photographs" (2026-10-17) and "Label Dan's real pictures" (2026-09-11; no label on thumbnails or covers, 2026-09-16).
- ⚠ **LABEL PLACEMENT — NEVER OVER HIS FACE AND NEVER OVER HIS ABS** (Dan, 2026-09-12, on the Ad 2 square: *"the label will not block my face or my abs… put it above my head, to the side, or somewhere that it doesn't block my face and my abs in all of these after pictures"*). This REPLACES the old "low on the frame, at the shorts/waistline" rule, which is what put the chip across his lower abs. Put it **above his head, off to one side, or anywhere in the frame his body does not occupy** — still inside the safe area, still large enough to read, still clear of the caption band. **The picture exists to show the physique; a label over the abs defeats the picture.** Choose the position by MEASURING him on the RENDERED frame (person mask → the bounding box of head + torso, then place the chip in the largest clear band), never at a fixed y — every photo frames him differently. If nothing is clear enough, shrink the chip or move it to a corner before you put it on him. Applies to BOTH labels on any picture of Dan.
- **Label AI-generated imagery — and NEVER put the label over a face** (Dan, 2026-08-27:
  "don't cover my face with labels like this. Make that a rule for future ones") **OR OVER HIS
  ABS** (Dan, 2026-09-12 — see the placement rule above). On a full-bleed shot of Dan the chip
  goes **above his head or off to one side**, in the largest band his body does not occupy,
  sized large enough to read (~68% of frame width on 1080). ⚠ The old wording here said "low —
  at the shorts/waistline area", and that is exactly what put the chip across his lower abs on
  the Ad 2 square; a fixed y is the mistake, measure him on the rendered frame instead.
- **Casting: white or Asian men 30–50.** Contact-sheet the RENDERED 9:16 crop of every stock
  clip before committing — 4 of the first 10 picks here were off-demographic and one was a
  woman, and none of that is visible from a search-page thumbnail.
- No drug names in graphics.

---

## Delivery naming and review delivery

- **Delivery goes beside his file under the `/editor-deliveries` convention — `title | editor | aspect |
  number`, lowercase, single-spaced pipes:** `Muhammad Ad Videos/<ad folder>/<title> | claude | 9x16 | ad N.mp4`
  + `<title> | REVIEW 540p 9x16 | ad N.mp4` + `<title> | REVIEW 480p 9x16 phone | ad N.mp4` + `<title> | AB audio
  his-vs-ours | ad N.mp4` + the gate stamp beside the master + `notes-vertical-v2.md` + `recipe-vertical-v2/`.
  (The un-suffixed `… | claude | 9x16.mp4` name the first delivery used was renamed by that skill on 2026-09-03;
  a second delivery under the old name made a duplicate master — `deliver.py` now writes the convention.)
  Review copies of 45 s or longer also go to `Videos to Review/` as `<task name> - <what it is>.mp4`; serve review pages
  with `.claude/skills/_shared/review_server.py PORT DIR`, layout `reference/kit9x16/sbl_page.py` (VIDEO-RULES "Review videos also
  go in `Videos to Review/`, for VLC", 2026-10-08).
- The first section of `notes-vertical.md` is "The HD export vs the approved draft" (Step 0b), and its one-line verdict goes
  in the delivery message. Later rounds that change only a few things deliver a revision list with exact timestamps and
  short watch ranges (VIDEO-RULES "Later-round video review timestamps", 2026-10-10). Review previews are held to the
  framing rows like the master (VIDEO-RULES "Head and hair clearance blocks review delivery", 2026-10-20).
- Edit-queue status (`in_progress`, `delivered`, `finalized` on Dan's words) per the section above; upload and the five
  thumbnails are `/ad-setup`, never here.

## Shared kit: the analysis card (Soft Blue Light HyperFrames since 2026-10-14)

When a line says the app ANALYSES the picture and builds the plan, use the shared card instead of inventing a graphic: the
HyperFrames template `.claude/skills/_shared/hyperframes/analysis-card/` (`build.py`). Rule: VIDEO-RULES "The analysis card is Soft Blue
Light, built with HyperFrames, in every video" (2026-10-14). The J2 card `_shared/adkit/analysis_card.py` (approved on RA-01,
2026-09-18; geometry and chip rules in `_shared/adkit/README.md`) is only for re-exports of films already approved with it (RA-01).

## Build history and the hand pipeline: `reference/LESSONS.md`

Everything the 2026-10-20 audit marked as history moved there word for word, with its *Historical (superseded …)* markers:

1. The two first attempts (2026-08-25/26): six defects that passed every metric; 11/11 QC and "truly awful"
2. The hand pipeline the kit replaced: Step 1 recover the edit (1a word alignment, 1b segment audio fit, 1c verify by words, 1d multi-roll), Step 2 measure the look, Step 3 measure the structure
3. Step 4, superseded audio section: the reference's own mix, gain + limiter, `loudnorm`, the conform voice, bed picking
4. Step 5 the vertical translation rules (1 to 14), Step 6 build order, the plate pattern, SFX count, EQ fit
5. Step 7 the watch pass, Step 7c naked jump cuts, the retired `qc.py` check list (1 to 20)
6. [A3] Attempt 3 · [A4] Ad 2 centering · [A5] Ad 2 vs Muhammad's V2 · [A6] Zeeshan's Ad 1 · [A7] Muhammad's Ad 5 · [A8] Muhammad's Ad 4 · [A9] Ad 5 round 1 · [A10] the first square · [S1] the square translation and "START HERE: the approved square" · [A12] Muhammad's Ad 3 (A12.1 to A12.13)
7. Traps that cost time here (1 to 8) and [A2] six more (9 to 14)
8. [A13] Ad 1's 9:16 cutdown · [A14] RA-01 square · [A15] Ad 4's four formats · [A16] Ad 10 square
