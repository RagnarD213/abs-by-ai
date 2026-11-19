# The full-build pipeline (round 4), step by step with the tools

**The kit.** Every Joint Vigor build script (191 files, 1.2 MB, no media, no secrets) is snapshotted in the private SRM
repo at `clients/goldenroots-naturals/joint-vigor-vsl/kit/`, laid out like the job folder (`claude-r1/..claude-r4/`).
The live originals are in `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/`; when that folder goes idle the
nightly job archive moves it to `/Volumes/Expansion/_finished_edit_jobs/<mac>-extreme/` (`jobarchive.py restore`).
Paths below are relative to the job root. **The scripts hard-code the Joint Vigor paths** (`R = .../SRM-goldenroots-
jointvigor`, ffmpeg at `.../Abs By AI/Media/video_edit/bin/ffmpeg.real`, frame counts of that film): copy them into the
new job, re-point the constants, and re-measure every source-specific number (key geometry, gains, white balance, card
sizes) instead of reusing it. Shared tools stay in `.claude/skills/_shared/` and are called, never copied.

Times in plans, words and EDLs are **film time at 1x**. The pace (1.1x) is applied once, in the finish. Frame g of the
film is at g * 1001 / 30000 s (29.97 fps); renders are frame exact so chunks concatenate without a seam.

## 0. Lock and set up (first hour)
- Sweep the client thread, `client_ledger.py gate <job> --stage plan` ([CLIENT-LEDGER.md](CLIENT-LEDGER.md)).
- `STYLE-LOCK.md` from the picks and every open ledger item ([STYLE-LOCK-TEMPLATE.md](STYLE-LOCK-TEMPLATE.md)), copy it
  into the job folder. Before the first render: `gate --stage build --brief STYLE-LOCK.md BLOCKS-BRIEF.md`.
- Edit slot, workdir, `TIME-LOG.md` (one line per milestone, with the clock time; the quoting numbers come from it).
- Opening: re-render from the ORIGINAL layers with the picked clips (`claude-r2/work/d_opening.py`), not from a published
  review file. Check heads clear the on-screen words (Joint Vigor: C1 shrink 0.95 then 0.90).

## 1. Key the spokesperson (start immediately; the longest machine step)
- House key = the locked DS-40 R2/R3 key with geometry re-measured for this source (`claude-r1/recipe/key16.py`;
  `claude-r4/key/key_fast.py` is the same maths, faster, proven frame-identical on 96 frames before use), pool driver
  `key/key_driver.py`, progress in `key/PROGRESS.json`, finished pieces listed in `key/full/pieces.json` (renderers read
  that list). Rule: `_shared/chroma-key/README.md`.
- Joint Vigor: 43,081 frames, about 8 h on the M6, about 184 GB. When the drive runs short, `key/offload/offload.py`
  moves finished pieces to the Seagate with a SHA-256 re-read and symlinks them back; throttle it (an offload copy plus
  M2 load dropped the network shares twice).
- Shadows on a white coat are camera shadows, not key holes: measure with `build/coat_scan.py`, fix in the compositor
  (`assemble_r4.coat_lift`, 60% toward the lit coat level inside the opaque core), never re-key.
- Doctor compositor: `claude-r2/work/r2_doctor.py` (`--map wide` = the A2 waist-up framing) over the approved plate.

## 2. Dialogue foundation (`claude-r4/dialogue/tools/`, about 2 h with helpers)
1. `script_lines.py`: the master script as numbered lines, marked camera or VO from the camera script.
2. ASR every camera and VO part (`asr_stream.py`, Whisper), `script_diff_r4.py` against the script.
3. `edl_r4.py`: master order; the last clean complete take of each line; false starts, restarts, slates and part numbers
   dropped; pauses tightened. Output `edl_r4.json`, `takes_r4.json`.
4. `build_dialogue_r4.py`: per-source gains (Joint Vigor: camera +4.0 dB, VO +3.2, testimonials levelled per clip to
   -18 LUFS), the approved voice treatment, whole-film normalisation (Joint Vigor dialogue: -16.2 LUFS, -1.5 dBTP).
5. `approved_check_r4.py` compares the DIALOGUE of the trial lead with the new foundation (sample difference ~1e-7):
   use it only for sound, and only for lines the client did not ask to change. Joint Vigor wrongly treated the whole
   lead, pictures included, as client approved; the lead's pictures are rebuilt from his feedback items.
6. `join_scan_r4.py` (noise steps, clicks, level steps across every cut), `edge_check_r4.py` (any cut inside speech),
   `flags_r4.py` (misreads, ad-libs, dropped words, all listed in `RECEIPT.md` with line numbers), Whisper spot checks.
7. `map_r4.py` writes `MAP.md` and `map.json`: four blocks of about 15 minutes on section boundaries, the VO passages
   that need cover visuals, key-visual times, testimonial slots (placeholders where material is not built yet), the
   product reveal time at 1x and at the locked pace, and the cut version's length and reveal.
8. `words_r4.py`: film-time words at 1x (`words_film_r4.json`); captions and ducking both read from it.

## 3. Captions (`claude-r4/captions/`)
- Script-corrected ASR words (Joint Vigor: 139 changes, `CHANGES.md`), then forced alignment (`align_r4/align_mms.py`,
  `finalize.py`) to `words_film_r4_aligned.json`; `lowconf_whisper.py` and `onset_check2.py` check doubtful words and
  onsets. Fix captions to what is SAID when the spokesperson deviates harmlessly; mute a throat clear rather than caption
  it; remove a spliced duplicate word from the EDL instead of shipping a stutter.
- Burn order: captions are the top layer over callouts and overlays, so captioned = clean + caption layer exactly
  (`build/caption_pass.py`). Yellow, word by word.

## 4. Parallel block planners
- One shared brief ([BLOCKS-BRIEF-TEMPLATE.md](BLOCKS-BRIEF-TEMPLATE.md); Joint Vigor's is `claude-r4/BLOCKS-BRIEF.md`),
  one agent per block (Opus 5.5 high), started as soon as the dialogue map exists. Each writes only `blocks/bN/`:
  `plan_bN.json`, `SOURCES.md`, `plan_bN_sheet.jpg`, `RECEIPT.md`.
- Each block planner gets its ledger rows in the brief and returns `LEDGER.md` (id, film time, what was done).
- Plan schema (from the trial lead's `claude-r1/cut/plan_r5b.json`): base events `[t, type, ...]` with `cam`
  CLOSE/MEDIUM alternating on every camera span, `hf` graphic .mov with in-point, `clip` (AI, reviewed), `img` (client
  image), `stock` (id + in-point), `split`, `ugc`; overlays `[t0, t1, overlay.mov]`; `callouts`; `stock_files` or
  `stock_paths` maps; `needs_ai` entries (prompt + stock fallback); `needs_build` cards.
- The orchestrator answers questions by appending a timestamped decision to the brief and tells every block. Joint
  Vigor's decisions worth reusing: callouts on spokesperson spans only; key visuals render as the approved stills with a
  slow push-in (no AI motion for KVs); code-built cards from one folder; cross-block reuse resolved at assembly;
  CLOSE/MEDIUM flipped at block joins; planners never drive Chrome or Flow.
- Lint every plan before rendering: `build/lint_plans.py plan1.json ... plan4.json` (stills over 5 s in VO, reuse within
  90 s across blocks keyed by FILE NAME, missing assets).

## 5. Stock first
- `build/fetch_pexels.sh ID...` (1080p rendition, free licence), Pixabay where needed; ids, page URLs and licences in
  each block's `SOURCES.md`.
- The renderer grades every stock shot from its FIRST frame however a render enters it (`assemble_r4._stock_get`), so a
  one-frame patch never takes a different grade. Every insert is then checked as a frame pulled from the final master.

## 6. AI needs: one Flow agent (`claude-r4/ai/`)
- Queue order: needs the casting rule requires first (Joint Vigor: the Japanese people and settings), then the rest.
  Brief files `ai/_tools/FRAME-BRIEF.txt`, `TAKE-BRIEF.txt`; prompt style in `needs.py` (documentary still, natural
  light, real skin, nobody looks at camera, no text or logos, invented people).
- START frame: Nano Banana Pro in Flow (0 credits; client images as references for a recurring character), then
  `_shared/framecheck/gate.py` plus a fresh `frame-reviewer` agent for every frame (`run_gate_v3.sh`).
- Motion: Veo 3.1 Fast frames-to-video, START only, 16:9, 8 s, 10 credits a take, at most 4 takes per need. When Chrome
  blocks downloads for Claude, Claude runs the Codex CLI itself to collect them (AGENTS.md, "Claude calls Codex itself").
- Take review: `clipcheck_takes.sh` plus a fresh reviewer; a take may pass on a RANGE (`ai/INDEX.json` records the
  usable span) when its fault is outside the part used.
- `deliver.sh` (crop Flow's bars, 1920x1080, no audio, PASS file), `grade_ai.py ID START_S` (the film's stock grade,
  recipe saved), checked in rendered stills beside its neighbours. Renders use the stock fallback until a PASS exists.
- Filing before the job closes: `file_archive.py` on the M2 (source archive + `source-register.json` under
  `clip_library.catalog_lock()`), `reconcile_archive.py`, then keepers with `clip_library.py add`
  (`_shared/cliplib/README.md`). Joint Vigor: 136/136 in the register, Drive-verified.

## 7. Testimonials (when the script has customer testimonial slots)
- Joint Vigor's testimonial blocks are dramatized: Flow start frame, Veo 3.1 Fast (9:16, 8 s), the customer's OWN
  written words from the client's site (trimmed, nothing added), Whisper check that every used line is word for word,
  mouth/seal and blink checks (`testimonials2/tools/`), per-clip -18 LUFS, layout with blurred fill, portrait left,
  name and age right and the "Dramatization" tag (`render_tb2.py`, validated by re-rendering the approved block).
- Real length replaces the placeholder at assembly (step 9). Let the last clip run on through the pause; never freeze.

## 8. Cards (`claude-r4/cards/build_cards.py`, `claude-r3/kv/kv_cards.py`)
- Approved stills copied pixel for pixel; new cards in the same style (office plate blur, white card, Montserrat, red tag,
  yellow marker); names in `cards/INDEX.json`, referenced by name in the plans.
- Any card with text: contain-fit (never cover-crop a picture with text), scaled to 78 to 88% and top-anchored over its
  own blur so nothing sits in the caption band (`build/make_fit_cards.py`). Study names, spellings and figures exactly
  as the script and the published source.

## 9. Render, assemble, finish
- `build/assemble_r4.py`: renders any film range picture-only, captioned and clean in ONE pass (two encoders), frame
  exact. Chunks through the render queue (`build/render_chunk.sh`, `asm/run_blocks*.sh`).
- `build/assemble_film.py`: joins the chunks and applies timing shifts while plans keep placeholder times (Joint Vigor:
  testimonial block 2 was 52.758 s against a 69.18 s placeholder, so everything after moved 16.421 s earlier; the
  line-336 false start was cut the same way). Recompute the reveal from the assembled film.
- `build/finish_r4.py` (via `asm/finish_asm.sh`, `finish_clean.sh`): never re-renders picture. 1.1x = picture setpts/1.1
  + fps 29.97 and dialogue atempo 1.1 (pitch kept). Music laid over the WHOLE paced film in one pass: Pixabay bed from its
  chosen offset, fading tail trimmed, looped with 4 s equal-power crossfades, ducked from word timings (attack 80 ms,
  release 350 ms, +6 dB in gaps, bed 20 dB under speech, every word at least 15 dB over the bed), bed in from the first
  spokesperson line with a 1.5 s fade, mix to -13.5 LUFS integrated and true peak at most -1.0 dBTP by a look-ahead gain
  envelope. Whole-film constants in `build/finish_constants.json` so blocks match. The opening's own mix is gain-matched
  and crossfaded in a pause.
- Outputs: captioned and clean at 1x and 1.1x, both SRTs, `gates.json`, `seamscan.json`, contact sheets.

## 10. Patch rounds (after each review)
- `build/patch_chunks.py PATCHES.json` (`[[block, t0, t1, why], ...]`) renders the changed ranges, `splice_frames.py`
  splices them frame exact (crf 12), `caption_pass.py` re-captions. Keep every round's patch file; the review page's
  revision list is built from them.
- `build/verify_patches.py` before the finish: first and last frame of every patch range plus one either side, rendered
  fresh and compared (mean absolute difference over 12 = stale). Skip spokesperson and animation frames (random access
  lands one frame off there).
- More than two or three patch rounds on a chunk: `build/rebuild_chunks.py` rebuilds each chunk in ONE generation from its
  pre-patch file plus every round's renders in order (last wins).
- `build/holdcheck.py` + `hold_fix.py` for one-frame spokesperson pose jumps at cuts. Doctor white-balance steps in the
  camera source: fit per-channel gains on the opaque figure and apply from the step frame on (`assemble_r4.WB_GAIN`).
- Re-finish ONCE per round, then every gate again ([GATES.md](GATES.md)). Keep the previous masters in `asm/out_prevN/`
  with their sha256.

## 11. Receipt, review page, review
- `asm/make_receipt_asm.py` writes `RECEIPT-R2.md`: files with frames, duration and sha256; gates; fix by fix; the
  revision list at 1.1x; cut points; "For a human ear"; gate notes; what was not done.
- `client_ledger.py done` for every item with a frame pulled from the master, then `gate --stage review`.
- `asm/make_review_r2.py --port <PORT>` builds Dan's page (first section: `client_ledger.py report <job>`, each row a
  chapter link); serve with `_shared/review_server.py <PORT> <DIR>`; release
  the slot `--review`; start a fresh Fable reviewer ([REVIEWER-BRIEF.md](REVIEWER-BRIEF.md)). Loop until SHIP.

## 12. Deliver
- `client_ledger.py gate <job> --stage deliver` PASSED, pasted into the receipt and the message draft.
- Captioned + clean + SRT at the locked pace in a Drive folder (anyone with the link), each file's hash checked after
  upload, opened logged out. Client message drafted with the VTurb reveal time (first frame of the product on the spoken
  product word: Joint Vigor 28:27.75 at 1.1x).
- Update the job `STATUS.md` and the SRM `STATUS.md`; nothing is sent until Dan says so.
