# What Codex's 16:9 builds record today, mapped to the edit sheet

Date: 2026-10-01. Read-only inspection. Nothing under `/Volumes/Extreme/_edit_work/` was changed.

Sheet format read from `/Users/danielrose/abs-worktrees/kit-sheet/.claude/skills/_shared/edit-sheet/README.md` and `validate.py` (schema `abs-edit-sheet/1`). Note: the README points to a `CODEX.md` in that folder; it does not exist yet (the folder holds only `README.md` and `validate.py`).

Builds inspected:

1. **RO-17** `/Volumes/Extreme/_edit_work/RO-17/` (organic long-form, Codex queue run `RO-17-20260925-160226`, stage-one DRAFT with five stock placeholders, revision 0).
2. **RO-01** `/Volumes/Extreme/_edit_work/ro01/` (organic long-form, Codex, R3 master delivered for private review 09-18, rounds 4 to 7 in planning). Chosen as the second build because it is by far the most complete of the four candidates and it is 16:9.
3. Glanced for layout comparison: **DS-17 R4** `/Volumes/Extreme/_edit_work/ds-17-r4/r4/` (dedicated short, 9:16, finalized by Dan 09-17) and `ds18-kettlebell-deadlift/`. `DS-01/` is a blocked job (`BLOCKED.md`), not a finished build.

Legend: RECORDED = stored as data in a named file and key. DERIVABLE = computable from named files or scripts. MISSING = not in the build dir.

---

## 1. RO-17

Files that matter: `recipe/build_ro17.py` (the one script that renders the film), `recipe/timeline.json`, `recipe/mapped-words.json`, `recipe/graphics.json`, `recipe/approvals.json`, `recipe/base-receipt.json`, `recipe/render-receipt.json`, `placeholders.json`, `DRAFT-DELIVERY.json`, `REUSE_REPORT.json`, `<master>.audio_gate.json`, `<master>.voice_chain.json`, `<master>.audio_untreated.json`, and the roll sidecar `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1713.roll.json`. `recipe-ro17/` and `logs/` are empty. `SCENE_PLAN.md` is prose only (section time ranges, no data).

| Sheet field | Status | Where, with a real value |
|---|---|---|
| `video.master` | RECORDED | `DRAFT-DELIVERY.json` `draft` = `/Volumes/Extreme/_edit_work/RO-17/RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4`; also `recipe/render-receipt.json` `master.path` |
| `video.sha256` | RECORDED | `DRAFT-DELIVERY.json` `draft_sha256` = `c00e7fd1...dd051`; same in `render-receipt.json` `master.sha256`, `placeholders.json` `draft.sha256`, audio gate `sha256` |
| `video.fps` | RECORDED | `recipe/timeline.json` `fps` = `"30000/1001"` |
| `video.frames`, `duration` | RECORDED | `timeline.json` `total_frames` = 13822, `duration` = 461.1940666; `render-receipt.json` `total_frames`, `duration` |
| `video.width`, `height` | DERIVABLE | not stored; ffprobe of the master gives 1920x1080. Hard-coded in the script's scale filter |
| `video.rolls` path | DERIVABLE | constant `SOURCE` in `build_ro17.py`; also `C1713.roll.json` `identity.current_path`. No roll list file in the build dir |
| roll width, height, fps, size | RECORDED (outside the build dir) | `C1713.roll.json` `picture.stored_resolution` = `3840x2160`, `picture.fps_fraction` = `30000/1001`, `identity.size_bytes` = 12281418545. Only a `sample_sha256`, no full-file hash |
| `grade.filter` | DERIVABLE | hard-coded string in `build_ro17.py` `render_base()`: `eq=gamma=1.28:contrast=1.04:saturation=0.92,unsharp=5:5:0.25:5:5:0`. Applied AFTER crop and AFTER the scale to 1920x1080 (so the unsharp is at 1080 scale). Prose copy in `notes.md`. Not in any JSON. Reliable, but needs the Python source parsed |
| `grade.lut` | DERIVABLE | none used (null) |
| `grade.decode` | RECORDED (sidecar) | `C1713.roll.json` `picture.color_tags` all `bt709`, `color_tags_status` = `present` |
| `edl` segments | RECORDED | `recipe/timeline.json` `pieces[]` with keys `index`, `src_in`, `src_out`, `out_f0`, `out_f1`, `frames`, `crop`. 18 pieces, contiguous 0 to 13822. Example: `{"index":1,"src_in":114.76,"src_out":154.5,"out_f0":1535,"out_f1":2726,"frames":1191,"crop":"punch-1"}` |
| `edl[].roll` | DERIVABLE | not in the piece (one roll, the script constant) |
| `edl[].out_in`, `out_out` | DERIVABLE | `out_f0 / fps`, `out_f1 / fps` |
| `edl[].src_f0` | DERIVABLE, plus or minus 1 frame | `round(src_in * fps)`; the render uses `-ss src_in` before `-i` with `-frames:v frames`, so the exact first frame is what ffmpeg's input seek lands on. Not recorded. Note `src_out` is nominal: the real end is `src_in + frames / fps` |
| `edl[].audio` | DERIVABLE, reliable | `make_voice()` cuts the lav from the same `src_in` for `frames / fps`, 6 ms fades. So every segment is `sync`. Not stored as data |
| `edl[].join` | DERIVABLE | not recorded. Every one of the 17 joins skips source time (smallest gap 1.22 s, 442.06 to 443.28), so all are `cut`; RO-17 has no same-take reframes. Whether a join crosses a take could be read from `C1713.roll.json` `takes[]` (`start`, `end`) |
| `framing[].name`, `crop` | DERIVABLE | `timeline.json` `pieces[].crop` holds a preset NAME (`full`, `punch-1`, `punch-2`); the pixel boxes are only in the script dict `crops`: `punch-1` = `crop=3584:2016:128:72`, `punch-2` = `crop=3456:1944:192:84`, `full` = whole 3840x2160. Presets are assigned by `i % 3`, not by measurement |
| `framing[].head` (hair_top, cx, chin) | MISSING | no head measurement anywhere. Searched the build dir for `hair`, `chin`, `face`, `head`, `crop`: hits only in prose (`notes-review.md` "Confirm Dan's hair remains fully in frame"), the SRT words, and pasted instructions inside `queue-run.log`. `C1713.roll.json` has no head track either |
| `words.list` | RECORDED | `recipe/mapped-words.json`, a list of 1618 rows with keys `word`, `start`, `end`, `source_start`, `source_end`, `piece`. Example `{"word":" You","start":0.12,"end":0.64,"source_start":54.8,"source_end":55.32,"piece":0}`. Words carry a leading space. Times are on the delivered timeline |
| `words.timing` | DERIVABLE | `mapped-source`: `mapped_words()` shifts the roll transcript by each piece. Roll transcript engine is in `C1713.roll.json` `transcript_source` = `whisper:small`. No check against the delivered audio (no finished-file ASR, no CTC) |
| `words.fixes` | MISSING (empty in practice) | no fix list; `make_srt()` only wraps lines. The SRT (`RO-17-subtitles.srt`, 142 cues) is cue-level only |
| `graphics[].id`, `t0`, `t1` | RECORDED | `recipe/graphics.json` rows with keys `key`, `start`, `end`, `path`, `sha256`. Example `{"key":"opening","start":1.0,"end":6.0,"path":".../graphics/opening.png"}`. 14 graphics |
| `graphics[].template`, `config`, `text` | DERIVABLE, fragile | NOT in any data file. They exist only as Python lambdas in `build_ro17.py` `make_graphics()` `specs`, for example `orglib.price_pill("CHIPOTLE PROTEIN CUP", "$7", y0=920, size=43)`. Renderers used: `orglib.pill_two_line`, `thin_bar`, `stack_panel`, `num_chip`, `cta_pill`, `price_pill` (from `.claude/skills/longform-edit/reference/orglib.py`). A converter would have to parse the script's source |
| `graphics[].layer` | DERIVABLE | all are full-frame static PNGs overlaid at 0:0 with a 0.20 s fade: `overlay` |
| `graphics[].driven_by` | MISSING | times are hand-picked whole seconds (1.0, 16.0, 29.0 ...); no spoken word is linked to any reveal |
| graphics vs the delivered file | MISMATCH | the delivered opening title is `graphics/opening-safe.png`, patched in after the render by ad hoc shell commands that exist only in `queue-run.log` (around line 77413: re-render of the first 250 frames, stream-copy splice in `cache/opening-fix/`). `recipe/graphics.json` still names `opening.png`. Re-running the recipe does not reproduce the master |
| `pictures[]` id, t0, t1, source, src_in | RECORDED | `placeholders.json` `items[]`: `id`, `type` (`stock`), `in`, `out`, `duration`, `source.path`, `source.trim_in`, `source.trim_out`, `source.sha256`, `source.crop` (prose), `source.rights`, `placeholder.label`. Example: `"id":"trail-mix","in":49.516133,"out":55.522133`, `source.trim_in` 1.0. (`recipe/approvals.json` `at` = 49.5 is the un-snapped time; use `placeholders.json`) |
| `pictures[].label_kind`, `label`, `label_source` | MISSING as fields | `type: "stock"` is the nearest thing. No real/AI enum. `placeholder.label` is the review placeholder text (`PLACEHOLDER - trail-mix - ...`), not a chip. `PRE_RENDER_CHECK.json` `verdict` has prose ("no identity or label concern") |
| `pictures[].people`, `physique` | MISSING | not recorded. The coconut clip shows a man (`intended_action` = "Man drinking from a fresh coconut") but there is no people field |
| `pictures[].approved_crop` | MISSING | no key; `source.crop` is a prose rule ("cover scale to 1920x1080, center crop") |
| `audio.mix` | RECORDED | the master itself |
| `audio.untreated` | RECORDED | `<master>.voice_chain.json` `src` = `/Volumes/Extreme/_edit_work/RO-17/audio/voice_raw.wav`; hash in `render-receipt.json` `voice_raw.sha256`. Untreated metrics in `<master>.audio_untreated.json` (`edt_ms` 58.7) |
| `audio.gate_stamp` | RECORDED | `<master>.audio_gate.json` `verdict` = `PASS`, tied by `sha256` |
| `audio.chain` | RECORDED | `<master>.voice_chain.json` (`dereverb`, `eq`, `voice`, `gain_db` 21.3, `lufs` -14.1) |
| `audio.music` | DERIVABLE | script constant `BED` = `/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3`, level `--bed-db -50.5`; path also in `REUSE_REPORT.json` `audio.evidence[1].path`. No single key for it |
| `approvals.status`, `round` | RECORDED | `placeholders.json` `status` = `approval_required`, `revision` = 0; `WORK_PACKET.json` `revision_number` = 0, `approved_elements` = `[]`; `DRAFT-DELIVERY.json` `gate` = `DRAFT` |
| `approvals.decisions` | RECORDED (empty) | the slot exists: `placeholders.json` `items[].approval` = `{status:"pending", selected_hashes:[], words:null, timestamp:null, selection_fingerprint:null}`. Dan has decided nothing on this build |

## 2. RO-01 (R3 master)

Files that matter: `build.py` (176 lines; `plan`, `assets`, `picture`, `audio`, `subtitles`, `mux`), `edit.json`, `scene-jobs.json`, `camera-events.json`, `framing.json`, `analysis/source-framing.json`, `grade.json`, `sources.json`, `graphics.json`, `graphics-render.json`, `mapped-words.json`, `gate-plan.json`, `scene-map.json`, `assets-provenance.json`, `audio-plan.json`, `audio-settings.json`, `master.json`, `manifest.json`, gate stamps, and the approval records in `private-review-authorization.json`, `revision4/`, `revision5-plan/decisions.json`, `revision6/decisions.json`.

| Sheet field | Status | Where, with a real value |
|---|---|---|
| `video.master`, `sha256` | RECORDED | `master.json` `path` = `/Volumes/Extreme/_edit_work/ro01/RO01_MASTER_R3.mp4`, `sha256` = `17f666fc...6f4f` |
| `video.fps`, `duration`, size | RECORDED | `RO01_MASTER_R3.mp4.deliver_gate.json` `fps` = `30000/1001`, `duration` = 707.9072, `size` = `1920x1080` |
| `video.frames` | RECORDED | `gate-plan.json` `target_frames` = 21216 |
| `video.rolls` | RECORDED | `sources.json` rows `id`, `path`, `sha256` (full hash), `bytes`, `probe` (full ffprobe: `width` 1920, `height` 1080, `r_frame_rate`). Four rolls C1605 to C1608. Also `manifest.json` `raw_sources[]` |
| `grade.filter` | RECORDED | `grade.json` per roll: `filter` = `scale=in_color_matrix=bt709:in_range=tv,format=gbrp,lut3d=assets/source-grade.cube:interp=tetrahedral`, plus `basis` (prose). Applied BEFORE the crop (`build.py` `picture()`: `cfg['filter'] + ',crop=...,scale=1920:1080'`) |
| `grade.lut` | RECORDED, relative path | `assets/source-grade.cube` inside the filter string, relative to the build dir |
| `grade.decode` | RECORDED | in the filter (`in_color_matrix=bt709:in_range=tv`) |
| `edl` segments | RECORDED | `edit.json`, 38 rows with keys `id`, `roll`, `src_in`, `src_out`, `out_frames` [f0, f1], `out_seconds` [in, out], `reason`. Example `{"id":"risk","roll":"C1607","src_in":14.45,"src_out":30.5661,"out_frames":[810,1293],"out_seconds":[27.027,43.1431]}`. `plan()` asserts contiguity |
| picture segments (finer) | RECORDED | `scene-jobs.json`, 170 rows: `id`, `frames`, `out_frames`, `source`, `source_hash`, `roll`, `source_in`, `crop`, `shot`, `graphic`. `camera-events.json` = the 77 frame numbers where the framing changes |
| `edl[].src_f0` | DERIVABLE, plus or minus 1 frame | `round(source_in * fps)`; not stored |
| `edl[].audio` | DERIVABLE, reliable | `audio()` takes the lav from the same `src_in` for the same length, 7 ms fades: `sync` everywhere. Not stored as data |
| `edl[].join` | DERIVABLE, reliable | a `camera-events.json` frame that is also an `edit.json` `out_frames[0]` is a `cut` (take change); any other camera event is a `reframe` (same take, crop only). `gate-plan.json` `joins` (37) and `punch` (77 ranges) say the same |
| `framing[].crop` | RECORDED | `scene-jobs.json` `crop` = `[x, y, w, h]` in raw pixels, floats, for example `[133.088, 3.082, 1672, 940.5]`. Order differs from the sheet's `[w, h, x, y]`, and the render rounds each to an even number. Widths come from `framing.json` (`far_width` 1672, `near_width` 1428, `cx` per roll) |
| `framing[].name` | DERIVABLE | `scene-jobs.json` `shot` parity: even = FAR, odd = NEAR |
| `framing[].head` | RECORDED as a raw track, sheet row DERIVABLE | `analysis/source-framing.json`, 1377 samples at 2 fps with keys `t`, `roll`, `take`, `hair_top`, `chin`, `cx` (raw pixels), for example `{"t":2.7,"roll":"C1606","hair_top":44,"chin":422.85,"cx":969.09}`. Min hair top and median centre per segment are a direct computation. Corrections are logged in `framing-refinement.json` and `framing-delivered-correction.json` and were applied into `scene-jobs.json` (checked: `scene-050` crop y = 11.08, the corrected value) |
| `words.list` | RECORDED | `mapped-words.json`: `start`, `end`, `text`, `source`, `source_start`, `source_end`. Same words in `gate-plan.json` `words[]` as `{w, t, e}` (2408 words) |
| `words.timing` | DERIVABLE | `mapped-source` from `analysis/<roll>.whisper.json`. A finished-file transcript also exists (`review/final.whisper.json`) |
| `words.fixes` | DERIVABLE, fragile | fixes are regexes inside `build.py` `subtitles()` (`weight protein` to `whey protein`, drug names to `[medication]`, `absbyai.com` casing, `six -pack`). No data list |
| `graphics[]` id, text, t0, t1 | RECORDED | `graphics.json` / `graphics-render.json`, 49 rows, keys seen: `key`, `a`, `b`, `kind` (`lower`, `title`, `number`, `left`), `text`, `y`, `x`, `num`, `teaching`, `video`, `source_in`, `rendered_lines`, `custom_renderer`, `asset_sha256`. Example `{"key":"g31","a":454.50,"b":461.20,"kind":"number","text":"0.8 g protein / lb body weight","y":862,"num":"3","teaching":true}` |
| `graphics[].template`, `config` | DERIVABLE, reliable | the row itself is the config. Renderer is chosen in `build.py` `assets()`: `kind == 'title'` uses `title_image`, `teaching: true` uses `teaching_image`, else `modern_graphics.panel` (from `Media/codex-video-trial/03-organic-abwheel/`). One exception: `g35` has `rendered_lines` (the real on-screen text) different from `text`, with `custom_renderer` = `review/fix_g35.py` |
| `graphics[].layer` | DERIVABLE | `title` = `full` (Dan replaced); `teaching` = `side` (Dan scaled to 720x960 and padded at 1120:60); others = `overlay` |
| `graphics[].driven_by` | MISSING | only `a` / `b`. `scene-map.json` has a `spoken_beat` sentence per scene, but no word-to-reveal link |
| `pictures[]` source, src_in | RECORDED | `assets-provenance.json` rows: `raw`, `source_in`, `source_duration`, `path`, `sha256`, `filter`, `provenance`, `label`. Example `raw` = `.../main camera/C1675.MP4`, `source_in` 24, `path` = `assets/dan-curls.mp4` |
| `pictures[]` t0, t1 | RECORDED | on the graphic row that carries it: `graphics.json` `g25` `video`, `a` 383.72, `b` 394.42, `source_in` 0 |
| `pictures[].label_kind`, `label` | DERIVABLE from prose | `assets-provenance.json` `label` = `"No photo label: real moving footage"`; `scene-map.json` `label` per scene; `gate-plan.json` `ai_inserts` = `[]`, `real_photos` = `[]`. No enum, no chip text field |
| `pictures[].people`, `physique` | DERIVABLE from prose | `scene-map.json` `person` = `"Dan in original footage"`. No physique flag |
| `pictures[].approved_crop` | MISSING | no key |
| `audio.mix` | RECORDED | `mix.wav` and the master |
| `audio.untreated` | RECORDED | `voice-untreated.wav`; `audio-plan.json` `untreated_sha256`; `gate-plan.json` `source_audio`; `mix.wav.audio_untreated.json` |
| `audio.gate_stamp` | RECORDED | `RO01_MASTER_R3.mp4.audio_gate.json` (and `mix.wav.audio_gate.json`) |
| `audio.chain` | RECORDED, on the wav not the master | `mix.wav.voice_chain.json`. There is no `RO01_MASTER_R3.mp4.voice_chain.json` |
| `audio.music` | RECORDED | `audio-settings.json` `bed` = `.../02-organic-sample/cache/independent-bed.mp3`, `bed_db` = -42 |
| `approvals` | RECORDED, spread over several files | `private-review-authorization.json` `user_instruction` = "Yes go ahead and send it to me", `scope`; `revision4/WORK_PACKET.json` `approved_elements` (R3 camera color, R3 audio treatment ...); `revision5-plan/decisions.json` `Dan_message_2026_09_29` = "I approved everything as is here.", `items[]` with `id`, `verdict`, `scope`, `concept_or_copy`, `r3_seconds`, `locked_assets`; `revision6/decisions.json` `user_verdict`, `approved_exact_frame_ids`, `scope`. This is very close to the sheet's `decisions` shape |

Caution on RO-01: the R2 and R3 masters were produced by follow-up scripts (`revise_r2.py`, `post_r2.py`, `post_r3.py`, `review/fix_g35.py`) rather than a clean rerun of `build.py`. The JSON files were updated in place (backups: `pre-boundary-edit.json`, `pre-listening-graphics.json`), so they appear to describe R3, but that is not proven by a hash in any one file.

---

## (a) Verdict: can a converter write a valid sheet from these files alone?

- **RO-01: yes.** Every field `validate.py` requires is recorded or cleanly derivable: EDL, crops, a measured head track, words, graphics text and config, picture sources, both audio files, approvals. `driven_by` would be an honest empty list. It needs an adapter written for RO-01's own key names.
- **RO-17: no.** Three blockers. (1) `framing[].head` does not exist, and the validator requires `hair_top`, `cx`, `chin` on every segment; it could only be filled by a new measurement of the raw. (2) Graphic text and renderer exist only as Python lambdas in `build_ro17.py`, and the delivered opening title was patched outside the recipe, so the data does not match the master. (3) Pictures have no real/AI label, people or physique fields.
- **Overall: no single converter.** The two long-forms share no file names or key names for the same facts, and the richer build (RO-01) is the older one. A per-job adapter would be needed every time. The dependable fix is for Codex to write the sheet itself at delivery.

## (b) What Codex must start saving at build time

Simplest instruction: at delivery write `<master name>.edit-sheet.json` next to the master in schema `abs-edit-sheet/1` and run `python3 .claude/skills/_shared/edit-sheet/validate.py SHEET.json --hash`; a failing sheet blocks the delivery. To make that possible, the build must save these facts as data (not as code or prose):

1. **Rolls**: `sources.json`, one row per raw roll: `id`, `path` (absolute), `sha256`, `width`, `height`, `fps`. (RO-01 already does this; RO-17 does not.)
2. **Grade**: `grade.json`: `filter` (the exact ffmpeg chain), `lut` (absolute path or null), `decode` (`bt709`), `order` (`before_crop` or `after_crop_and_scale`). Never only a string inside the script.
3. **EDL**: `edit.json`, one row per picture segment, including every punch-in change: `roll`, `src_in`, `src_out`, `src_f0` (the real first raw frame), `out_f0`, `out_f1`, `out_in`, `out_out`, `shot`, `audio` (`"sync"` or `{src_in, src_out}`), `join` (`first`, `cut` for a take change, `reframe` for same take).
4. **Framing**: `framing.json`, one row per EDL segment: `name`, `crop` as `[w, h, x, y]` in raw pixels (the even integers actually rendered), `head` `{hair_top, cx, chin}` in raw pixels (min hair top over the shot, median centre), `measured` (how). Measure the head on every build; RO-17 skipped it.
5. **Words**: `words-delivered.json`: `list` of `{w, t0, t1}` on the delivered timeline, `timing` (`mapped-source`, `ctc` or `whisper`), `fixes` as `[[heard, shown], ...]` (empty list if none). Fixes go here, not in regexes.
6. **Graphics**: `graphics.json`, one row per graphic: `id`, `template` (`codex:<renderer function>`), `config` (every argument passed to the renderer, including all text, position and size), `text` (list of every on-screen string, copied from the config), `t0`, `t1`, `layer` (`overlay`, `side`, `full`), `driven_by` (list of `{part, phrase, t}`; empty list if hand-timed). The script must read this file to render, so the file and the picture cannot disagree.
7. **Pictures**: `pictures.json`, one row per inserted photo or clip: `id`, `t0`, `t1`, `kind` (`clip`, `photo`, `phone`), `sources` `[{path, src_in, frames}]`, `label_kind` (`ai`, `real`, `none`), `label` (chip text), `label_source` (what the label is based on), `people` (`dan`, `other`, `none`), `physique` (true or false), `approved_crop` (null or `{path}` / `{box}`), `library_id`.
8. **Audio**: `audio.json`: `mix`, `untreated` (absolute path of the untreated assembly), `gate_stamp`, `chain`, `music` (path or null), `music_db`. Keep `<master>.voice_chain.json` on the master, as RO-17 does.
9. **Approvals**: one `approvals.json` at the build root, appended each round: `status` (`approved` or `pending`), `round`, `decisions` `[{id, verdict, dan (his exact words), scope}]`, `source`. One key name for Dan's words in every job.
10. **No patch outside the data.** Any fix after the render (such as RO-17's opening title splice) must update the JSON above and the master hash, or be done by rerunning the recipe.

## (c) Is Codex's layout consistent across jobs? No.

| Fact | RO-17 (09-25) | RO-01 (09-18 onward) | DS-17 R4 (09-17, 9:16) |
|---|---|---|---|
| Render script | `recipe/build_ro17.py`, self-contained | `build.py` at the root plus about 20 follow-up scripts | `recipe/build.py` plus JS (`segments.js`, `captions.js`) |
| EDL file and keys | `recipe/timeline.json` `pieces[]`: `src_in`, `src_out`, `out_f0`, `out_f1`, `crop` | `edit.json` list: `roll`, `src_in`, `src_out`, `out_frames`, `out_seconds` | `edit.json` `pieces[]`: `id`, `start`, `end`, `frames`, `out` |
| Crop | preset name; boxes in code | `scene-jobs.json` `crop` [x, y, w, h] | `scene-map.json` `crop` |
| Head measurement | none | `analysis/source-framing.json` | `<master>.framing_proof.jpg`, gate plan `punch` |
| Grade | string in code | `grade.json` per roll, LUT | LUT listed in `manifest.json` `sources` |
| Words | `recipe/mapped-words.json` (`word`, `start`, `end`) | `mapped-words.json` (`text`, `start`, `end`) and `gate-plan.json` (`w`, `t`, `e`) | `caption-timing-ctc.json` (`word`, `start`, `end`, `score`; CTC-timed), `delivered-words.json` |
| Graphics | `recipe/graphics.json` (`key`, `start`, `end`, `path`); text in code | `graphics.json` (`key`, `a`, `b`, `kind`, `text`) | captions and labels in JS / ASS files |
| Pictures | `placeholders.json` `items[]` | `assets-provenance.json`, `scene-map.json` | `scene-map.json` (`picture_source`, `person`, `label`) |
| Roll list | script constant plus external roll sidecar | `sources.json`, `manifest.json` | `manifest.json` `sources[]` with `sha256` |
| Audio records | sidecars on the master | sidecars on `mix.wav`; `audio-plan.json` | sidecars on `voice.wav` |
| Dan's words | `items[].approval.words` (null) | `user_instruction`, `Dan_message_2026_09_29`, `user_verdict` | `records/dan-final-approval-20260917.json` `dan_verbatim`, `scope` |
| Packet files | `WORK_PACKET.json`, `SCENE_PLAN.md`, `PRE_RENDER_CHECK.json`, `DRAFT-DELIVERY.json`, `REUSE_REPORT.json` at the root | none at the root; `WORK_PACKET.json` only inside `revision4/` | none; `FREEZE.json`, `records/` |

Common ground across all three: the shared audio sidecars (`.audio_gate.json`, `.voice_chain.json`, `.audio_untreated.json`), 30000/1001 timing, and source-mapped word timings. Everything else differs by job. The newer queue-run layout (RO-17) records LESS of what the sheet needs than the older hand-run RO-01: it dropped the head measurement, the per-roll grade file and the data-driven graphics.
