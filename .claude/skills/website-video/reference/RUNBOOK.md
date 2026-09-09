# Runbook — every stage, the command, and what to look at before the next stage

Work in a scratch copy on the external drive: `/Volumes/Extreme/_edit_work/<video-slug>/` (copy `reference/recipe/`
there; the recipe is code, the work dir is data). `export PATH=/Volumes/Extreme/_edit_work/bin:$PATH` (static ffmpeg;
Whisper shells out to a bare `ffmpeg`). Cap concurrent encodes at two machine-wide (`ps -Ao command | grep -E
'ffmpeg|whisper'` first). Long stages go in the background with a completion line and a `wait`, never a filename poll.
Each stage's script has its numbers at the top of the file with the date they were measured; a new set re-measures.

| # | stage | command | look at before moving on |
|---|---|---|---|
| 0 | inputs | script doc → `script.txt`; rolls listed in `rolls.txt`; `pick_lav.py <roll>` per roll → `<roll>.audio_source.json` | verdict per roll (`two-mics` / `single-live`); the lav's SNR |
| 1 | grade + base | `make_lut.py` (S-Log3 → 709, exposure and saturation fitted against the approved skin), `base.py` → `base.mov` at full 4K with the lav mono | a skin-percentile fit vs the approved look (≤ 5 levels), never a luma lift |
| 2 | transcribe + cut | `whisper_chunked.py` (overlapping windows; copies of it, `repeat_scan.py` and `orphan_scan.py` are in the recipe, originals in /ad-edit reference) → `repeat_scan.py` + `orphan_scan.py` → `edl.py` (phrase-anchored spans per roll, edges validated against the −40 dB envelope) → `tight.py` (pause cuts ~0.30 s, `MANUAL_CUTS` for restarts) → `tight.mov` + `tight_cuts.json` | 0 orphans, 0 stretched words / repeated 4-grams; a dry run (`RENDER=0`) printing the words around every manual cut |
| 3 | hair track | `hairtrack.py` (8/s on the 4K base, mapped through the keeps) → `hairtrack.json` + `pv/hairtrack_proof.jpg` | **the proof sheet at native scale**: the line sits on the top of the HAIR on the tallest and median frames; longest run of discarded samples < 2 s |
| 4 | beats | `beats.py` — every beat anchored to a PHRASE searched after a time; OVERLAY / PANEL / AI sets; the assertions (before → Dan → after gap, insert clearances) | `python3 beats.py` coverage print: any graphic ≈ 55 %, Dan fully replaced ≤ 30 %, longest bare stretch ≤ 35 s |
| 5 | product screens | local server (`.claude/launch.json` → `abs-by-ai`, pgmem DB); `hub/hub_capture.py`, `macro2/record_macro.py`, `trainer/trainer_capture.py` (seed the program through `absbyai_trainer_program`, only ids with demos, `getExerciseAnim = () => ''`) | the captures at full size; no stick figure, no hero before/after, no email form; scroll ends on the last tile. A blank capture = a real bug in the app (lesson 121): fix it, it is live |
| 6 | AI stills + clips | `ai/gen_rev6.sh stills` pattern (nano-banana, `--image` the man's reference or the still being edited) → LOOK → `ai/gen_rev6_clips.sh <names>` (Veo 3.1 Fast 8 s 16:9 1080p) → `strip.py` first/last/whole | `AI_CLIPS.md` checklist per clip; regenerate, don't trim around a flaw |
| 7 | plan + punch | `layout.py plan` (assert: NEAR/FAR/PIP only, no crop past the light, hair ~43 px in every hold) → `layout.py punch` (~4 min quiet / 25 loaded) → `hairtrack_refine.py` → `layout.py plan` again; re-punch if any anchor moved (it converges in one pass) | the plan print: hair-below-edge column 43–44 px on every hold; the alternation never repeats across a visible join |
| 8 | graphics + inserts | `gfx.py` / `gfx2.py` (lower thirds at bottom=1000, cards, PiP mask/plate) → `build_inserts.py tag ai_* macro hub num2` → the MOV-vs-beat check (`rev6.sh` step 0 pattern) → a native-scale composite preview of every PiP over a real frame (PIL, not `-ss` + overlay) | every MOV within 0.1 s of its beat; headings measured against the panel width; the preview at 1080p |
| 9 | mix | `MIX_T=20 MIX_OUT=/tmp/x.mov python3 layout.py mix` (benchmark; ~15–40 s is healthy) → `python3 layout.py mix` (single pass) or `MIX_STAGES=3` if the benchmark is slow or `sample <pid>` shows every thread parked → `nocap.mov` | one frame grabbed at each PiP and each insert |
| 10 | retouch (only if Dan asked) | `tanpass.py track` on THIS mix → `proof` (look) → `GAIN=0.90 … render nocap_A.mov` and `GAIN=1.00 … render nocap_B.mov` → `gate nocap.mov nocap_A.mov` | proof sheet incl. the fade frames; the gate's per-frame change is constant (sd < 0.02); B − mix mean ≈ 0 |
| 11 | audio | `VIN=nocap.mov VOUT=nocap_audio.mov DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45 MUSIC_DB=-44 COMP=0 python3 audio4.py` (identical env on every version) | premix I / TP / LRA printed; limiter delay ~239 samples; `AUDIO_STANDARD.md` |
| 12 | captions | `VIN=nocap_audio.mov VOUT=website_video_16x9.mp4 python3 captions.py` (words from the tight list, lifted over lower thirds, shifted over PiPs, suppressed on cards) | cue count; "abs" lowercase; the first 30 s proofed by ear |
| 13 | gates | `./deliver.sh website_video_16x9.mp4` (audio gate + stamp + A/B, exact-grab sheet, `qc.py` incl. `qc_frame.py` + `hairgate.py`, `watch.py`, 540p copy, silence) | every row PASS; then the HUMAN pass over `watch/strip/*.png`, `pv/final_sheet_5s.jpg`, `pv/hairgate_sheet.jpg` with `REVIEW_HISTORY.md` open |
| 14 | A/B clips | `ab_face.py A B AB_<region>.mp4` for any subjective retouch; the audio A/B comes from the gate | 20 seconds each; labelled |
| 15 | deliver | copy master + stamp + review + A/Bs + `notes.md` + `pv/` + `recipe/` to the delivery folder; previous rev → `*_REV<n>`; send the review copies and A/Bs in chat; coordination entry | `notes.md` for a non-technical reader: per item what changed and why, the gate table, what to look at |
| 16 | finalize (on Dan's approval) | export from `nocap_audio.mov` at CRF 14 / slow / 320k → `deliver.sh` on that file → both folders (`claude edited long form content/…` and `Website Videos/…`) → the YouTube-unlisted + `site-video.js` handoff | the stamp on the filed file matches; nothing video-sized in git (`*.mp4` / `*.mov` and `Website Videos/` are ignored) |

## Traps that cost hours (each one happened)

- A moved beat edge is not automatically a re-punch: diff the per-frame crops of the two plans and intersect with the
  opaque-coverage map before spending 20 minutes (lesson 116). A new PiP always forces it (visible level change).
- The 21-input overlay graph livelocks ffmpeg on a loaded machine (all threads parked in `tq_receive`); benchmark 20 s
  first and stage the mix if it is slow (lesson 117).
- Any pass that pipes the picture through RGB darkens it by ~1.4 levels; stay in yuv420p (lesson 119).
- A face detector inside an insert's fade sees the AI man; exclude insert beats and hold Dan's last landmarks through
  the fade (lesson 119). Key every track to the picture it was measured on (`src_sig`), not just the cut.
- `card_in` holds dead after its entrance; every card carries a slow drift; a card the video ends on never fades out.
- A looped image input defaults to 25 fps — `-framerate 30000/1001` on every `-loop 1` input, or a plate drops for one
  frame and exposes what it covers.
- Contact sheets from `fps=1/N` lag the content by N/2 s; grab suspect frames with an exact `-ss` before calling
  anything a defect.
- The harness kills a foreground command at five minutes: background every render, print a completion line, wait on
  the process (`render_wait.sh` pattern), never on a filename.
- The other sessions' edits: `_shared/audio` may be mid-edit by a concurrent session; read `git status` before assuming
  the gate on disk is the committed one, and never edit it from here.
