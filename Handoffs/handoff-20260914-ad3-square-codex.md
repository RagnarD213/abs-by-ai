# Handoff — Ad 3 "Stop Paying Human Trainers": build the 1:1 SQUARE + its ≤0:59 square cutdown (written for Codex)

**Written 2026-09-14 by Claude (Opus 5), for OpenAI Codex. Not yet executed.** Dan wants to try Codex on this job, so
this doc assumes you have never seen this project. It spells out what exists, what "done" means, and every trap that
cost Claude time on earlier squares. Read all of it before touching a file. Where it tells you to read something else,
the reason is given.

---

## 0. The job in one paragraph

Abs By AI runs video ads on Google Ads Demand Gen. Each ad needs three shapes: 16:9 (the editor's original), 9:16 (a
vertical we rebuilt) and 1:1 (square). Google fills YouTube in-feed, Discover and Gmail placements from the square.
**Ad 3's 16:9 and 9:16 are finished and approved by Dan (2026-09-14). Build the square:** a 1080×1080 re-layout of
the approved **vertical** build. It keeps the vertical's exact timeline (7,948 frames at 29.97 fps), edit, colour,
graphics, labels, captions timing and audio, and changes only the geometry. Also build a ≤0:59 square cutdown from
the vertical's existing cutdown plan. Deliver both with review copies, get them through every gate plus an
independent review, then stop for Dan's approval. Do **not** upload anything and do not touch Google Ads.

---

## 1. Who Dan is and how to work with him

- Dan owns the business. He is **non-technical**. Report in plain language: what you did, what he should look at, what
  is his call. No jargon, no code in the report.
- He dictates by voice, so an odd word may be a mis-transcription ("smoke shop" meant "smoke shot").
- **Bias toward action on reversible work.** Do not stop to ask about things you can undo. Stop and ask only for:
  deleting real data, spending money beyond small amounts, anything published or sent to other people.
- **Dan approves videos by watching them.** A build that passes every gate is still not approved until he says so.

---

## 2. Environment facts (not obvious)

| thing | value / trap |
|---|---|
| repo root | `/Users/danielrose/Documents/Claude/Projects/Abs By AI` (**spaces in the path — quote everything**) |
| media drive | `/Volumes/Extreme` (external SSD). Build dirs live in `/Volumes/Extreme/_edit_work/` |
| ffmpeg / ffprobe | **use `"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"`** (and `ffprobe` beside it). Put that dir first on `PATH` for any script that shells out (Whisper calls plain `ffmpeg`). |
| python | `python3` = Apple's Python 3.9 (framework build). numpy, opencv (`cv2`), Pillow, scipy, whisper are installed. In `ps` its command line reads `…/Python.app/Contents/MacOS/Python X.py`, **not** `python3 X.py`. A `pgrep -f "python3 X.py"` matches nothing. |
| shell | zsh. **zsh does not word-split an unquoted `$var`**: `set -- $R` with `R="0 2845"` passes ONE argument. Some scripts (`selftest.sh`) are zsh-only; `bash script.sh` produces fake errors. |
| file names | delivered files contain literal ` \| ` pipes: `stop paying human trainers \| claude \| 1x1 \| ad 3.mp4`. Quote them. |
| machine limit | **Max two video builds at once across all sessions** (renders, big ffmpeg encodes, Whisper, gate runs). Before starting one, run `ps -Ao command \| grep -E 'ffmpeg\|render\|whisper\|gate.py' \| grep -v grep`. If two builds are already running, wait. Four at once measured a 9× slowdown. |
| waiting loops | **a `pgrep -f "<pattern>"` wait loop matches its own command line and never exits.** Wait on a sentinel line in a log file or a captured PID instead. |
| pipes hide failures | `cmd \| tail` returns tail's exit code. Never put a step that must fail the chain behind a pipe. |
| other sessions | several AI sessions work in this repo at once. **Never run a script inside another build's directory** (you would overwrite its intermediates). `/Volumes/Extreme/_edit_work/ad3-vert/` is the approved vertical: **treat it as read-only.** |
| repo is PUBLIC | never commit a video, a photo of Dan, or secrets. Videos/photos are git-ignored; keep it that way. |
| status board | `AI_COORDINATION.md`: short, only open work. Add ONE entry for this job when you start, update it when you finish, **edit only your own entry**, and re-read the file from disk right before editing it. |
| git | follow your trial's branch rules (the Codex trial runs on a private branch). Do not push to `main` unless Dan says so. |

---

## 3. What is approved and must be reproduced exactly

### 3.1 The approved vertical (the source of truth for the square)

Build dir: **`/Volumes/Extreme/_edit_work/ad3-vert/`** (50 GB; mostly caches, see §5.1).

| delivered file (in `Muhammad Ad Videos/stop paying human trainers - ad 3/`) | frames | sha256 (first 16) |
|---|---|---|
| `stop paying human trainers \| claude \| 9x16 \| ad 3.mp4` (master, 4:25.2) | 7,948 @ 30000/1001 | `6ef0538cf055183a` |
| `stop paying human trainers \| claude \| 9x16 59s \| ad 3.mp4` (cutdown, 57.92 s) | 1,736 | `1a295123fca84479` |

The vertical's build is `ad3_vertical_9x16.mp4` + `cut/ad3_vertical_9x16_59s.mp4` in the build dir (same bytes).

Read these, in this order:
1. `Muhammad Ad Videos/stop paying human trainers - ad 3/notes-vertical.md`: what the vertical is and every deliberate
   deviation from Muhammad's cut. **Every deviation carries into the square.**
2. `Handoffs/handoff-20260911-square-ads-00-shared-rules.md`: the square rules shared by every ad.
3. `.claude/skills/shortad-from-longform/SKILL.md`, sections **[S1] THE SQUARE (1:1) TRANSLATION** (read "START HERE"
   and all numbered lessons; this is what the first two squares cost) and **[A12]** (Ad 3's own vertical lessons).
   Also the "Standing content rules" and "Traps" sections near the end. It is a long file. Search for the headings.
4. `.claude/skills/shortad-from-longform/reference/a11_sq_ad1/README.md`: the **approved** Ad 1 square's tools.
5. `.claude/skills/shortad-from-longform/reference/a10_sq/README.md`: the Ad 2 square (geometry lessons; its label
   placement predates Dan's rule, so don't copy that part).

### 3.2 The look to match: the approved Ad 1 square

Dan approved the Ad 1 square with no further revisions (2026-09-14): *"both of these are looking excellent. You nailed
it with both the full square version and the cutdown."* Watch its review copies before designing anything:
`Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs | REVIEW 540p 1x1 | 1x1 | ad 1.mp4` (and the
`59s` one). Its layout constants live in `reference/a11_sq_ad1/sqlib.py`.

⚠ **Not obvious:** the Ad 1 square was built on an OLDER pipeline (`render.py`/`sqlib.py`, "attempt 3"). Ad 3's vertical
is on the NEWER pipeline (`render3.py` + `g3.py` + `g5.py`, from Ads 4/5). **No square has been built on `render3.py`
yet. Yours is the first.** So you port the *geometry and rules* of `a11_sq_ad1` onto Ad 3's `render3.py`
compositor. You do not copy Ad 1's code wholesale, and you do not rebuild Ad 3 on Ad 1's pipeline.

---

## 4. Definition of done

In `Muhammad Ad Videos/stop paying human trainers - ad 3/`:

- `stop paying human trainers | claude | 1x1 | ad 3.mp4`: 1080×1080, **exactly 7,948 frames**, 30000/1001, H.264
  High, 8–12 Mbps, tagged BT.709 (`-color_primaries bt709 -color_trc bt709 -colorspace bt709`), yuv420p,
  `+faststart`.
- `stop paying human trainers | claude | 1x1 59s | ad 3.mp4`: same spec, **exactly 1,736 frames**.
- **Audio of the master = the approved vertical master's AAC stream, stream-copied** (`-c:a copy`). Its md5 must equal
  the vertical's. It is Muhammad's original stream, md5 `db408fd0bc0ba2a44245df947cb7e1f3` (measure with
  `ffmpeg -i <file> -map 0:a:0 -c copy -f md5 -`). **Audio of the cutdown = the approved vertical cutdown's AAC stream,
  stream-copied**, md5 asserted the same way. The timelines are identical, so no audio work is needed at all. **Never
  re-encode, normalise, limit, EQ or mono-sum audio.** Dan rejected exactly that on 2026-09-10.
- `REVIEW 540p 1x1` copies of both (`scale=540:540`, crf 23, AAC 160k), named like the Ad 1 folder's.
- The `.audio_gate.json` stamp beside each delivered file (see §7). ⚠ The cutdown's stamp will FAIL on true peak
  (−0.90 dBTP). That is inherited from the approved vertical cutdown, which Dan accepted
  (`… 9x16 59s | ad 3.mp4.DAN_ACCEPTED.md`). Write the same kind of note for the square cutdown. **Never change a gate
  bound to make it pass.**
- `notes-square.md`: plain-language notes for Dan (what the square is, every layout decision per beat type, every
  difference from the vertical, the gate results, anything for his judgment). Also `recipe-square/`: a copy of every
  script and JSON you changed or wrote.
- Your independent review (§8) says it ships.
- Review copies sent to Dan. **Then stop.** Approval, YouTube and Google Ads come later
  (`Handoffs/handoff-20260914-ad3-youtube-and-ads.md` is the template for that later job).

---

## 5. Build

### 5.1 Make your own build dir (copy selectively, never build inside `ad3-vert/`)

`/Volumes/Extreme/_edit_work/ad3-sq/`. Copy from `ad3-vert/`:
- all `*.py`, `*.sh`, `*.json`, `*.cube`, `*.npz` at the top level
- `base.mp4` (705 MB: Muhammad's cut conformed from the raw camera roll, 1920×1080, 7,948 frames, **ungraded**; the grade
  is applied at render time)
- `lifts/` (his stock clips lifted from his render), `assets/` (the lock-screen stills etc.), `ref/ad3_v6hd.mp4` (his HD),
  `words_ctc.json`, `cap/list.txt` only if you want the caption schedule (the PNGs in `cap/` are 9:16 and must be
  regenerated)
- `cut_plan.json`, `cut/his_mix.wav`, `cut/beats.py` and `cut/cut_timeline.json` (the cutdown's plan)

**Do NOT copy:** `watch/` (17 GB), `rc/`, `segs/`, `centering/`, `hg2/`, `lc/`, `cap/*.png`, `cut/*.mp4`, `_approved_*`,
`_rejected_*`, `picture*.mp4`, `ad3_prelt.mp4`, `logs/`, `test/`. They are caches or old renders.

Keep untouched copies of the files you will edit (`render3_9x16_orig.py`, `g5_9x16_orig.py`, …) so the diff is reviewable.

⚠ `media_map.json` holds **absolute paths** into the asset library. Leave them. It already points at
`ai-trainer-vs-robot-story-35s_v2.mp4`, the story clip whose bathroom shot was regenerated to remove a breath-smoke
artifact. **Never point anything at the v1 clip** (`…-35s.mp4` without `_v2`).

### 5.2 How the vertical's pipeline works (read the files; this is the map)

- `beats.py`: the beat sheet. `B.timeline()` returns the beats (each `kind`, `n0`, `n1`, params) and overlays (lower
  thirds `lt`, CTA `pill`), plus `B.FLASH` (Muhammad's light-leak flash frames) and `B.NTOT = 7948`. **Frame n of the
  vertical = frame n of Muhammad's 16:9.** Beat counts: talk 17, cardv 8, window 7, phonecard 4, card 3, bleedv 2,
  photoseq 1.
- `render3.py`: a per-frame Python compositor. One renderer per beat kind (`r_talk`, `r_window`, `r_card`, `r_cardv`,
  `r_bleedv`, `r_phonecard`, `r_photoseq`), then overlays, flashes and captions are composited, then frames are piped
  into x264. It renders in chunks: `master15.sh` shows the chunk/concat/mux chain (`--from/--to`, concat, `zmux.py`).
- `g5.py` (base graphics: `VW, VH = 1080, 1920`, `CAP_Y = 1400`, `TOP_SAFE, BOT_SAFE = 150, 1660`, `window_rect`,
  `window_plate`, `card_hole`, `card_plate`, lower thirds, pills) and `g3.py` (Ad 3's additions on top: `real_chip`,
  `photo_on_field`, `label_candidates`, the phone frame). `captions.py` renders the word-highlight caption PNGs
  (`cap/`) from `words_ctc.json`.
- **Colour:** `his.cube` (3D LUT), `vignette.json`, `grade_post.json`, `grade_seg.json`, `grade_final.json`, applied inside
  `render3.py` to base frames (talk and window beats). **Dan approved this colour after rejecting an earlier one.** Do not
  refit, retune or re-decode any of it. See §6.1.
- `crop.json`: per-frame talking-head crop `[x0, y0, w, h]` in **base (1920×1080) pixels**. The vertical uses w=576,
  h=1024 (9:16), scaled up to 1080×1920. `y0` is anchored to the top of Dan's hair (Dan's locked framing standard: hair
  just under the top edge, never a wide shot). `h` varies with Muhammad's punch-ins (NEAR/FAR zoom levels).
- `label_place.json`: where the "Real picture of me — not AI-generated" chip sits on each of the four photo-shoot
  stills. It was measured for the 9:16 layout and **must be re-measured for the square**.

### 5.3 The geometry port: what changes, per beat kind

Start by changing the constants (`VW = VH = 1080`) in `render3.py`, `g5.py` and `captions.py`, and every hard-coded
9:16 number you find (grep for `1920`, `1400`, `1660`, `1330`, `608`, `576`, `1024` and the explicit rects). Then go
beat by beat. **Settle every per-beat decision on still frames before any full render** (`render3.py --stills
100,200,… --dir stills` exists; make it write 1080×1080) and look at them.

| kind | vertical | square (default; deviate only with a reason in `notes-square.md`) |
|---|---|---|
| **talk** | 576×1024 crop → 1080×1920 | Keep the **same vertical extent** (hair anchor and Muhammad's zoom): take `h` and `y0` from `crop.json`, width = `h` (a square), centred on the crop's own centre x (`x0 + w/2`), clamped to 0…1920, then resize to 1080×1080. So the head sits at the same height with more width, and nothing is upscaled much (about 1.05×). This is what the Ad 2 square did ("face track shifted by (608−1080)/2"). |
| **window** (Dan above, text screen below) | Dan in a full-width window, text in the field below | **Stacked**, as the approved Ad 1 square: window height from the wrapped text, clamped **380–820 px** (Ad 1 approved at 518–774). One bullet size, **42 px**. **Text bottom line y = 1030**, no extra gap after the last bullet. Header drawn at the same size the plate draws it (Ad 1's bug: sized at +30 but drawn at +48, which pushed text 16 px past the line). Window crop anchored at the hair (`window_src` already pads above the frame for headroom, so keep that). The `phone` body variant (Dan above, app screenshot scrolling below) needs the same stacked treatment with the phone sized to fit above the bottom line. |
| **card** (still in Muhammad's olive card) | card with blur-in + slow push | Card at the still's own aspect inside the square with his margins; keep the blur-in and push. |
| **cardv** (16:9 clip in his card) | 16:9 hole in the card | Card 1080 wide at most, **16:9 hole** (≈1000×563), clip at its own aspect, never full-bleed, never cropped to square. |
| **bleedv** (native 9:16 AI clip full-frame: frames 49–224 opener, 1944–2845 the AI trainer story) | full-bleed 9:16 | Undecided; **decide by looking.** A 1:1 cover crop of a 1080×1920 clip keeps 1080×1080 of it (vertical offset `oy` per shot). Contact-sheet every shot of the story (`ai-trainer-vs-robot-story-35s_v2.mp4` is 7 shots of 121 frames) at your chosen `oy`. If any shot loses a head or the key action, use a full-height portrait (608×1080) centred on Muhammad's dark grid field instead. Record the decision per beat. The AI-GENERATED chip must not cover a face. Keep the caption scrim. |
| **phonecard** (phone in his olive card) | phone card, recording on his time map | Keep the phone at its size or shrink to fit above the bottom line; keep the scroll/time maps exactly. ⚠ See §6.4 on the lock screen and the stranger photo. |
| **photoseq** (four real photo-shoot stills of Dan, rapid) | each photo on the field in `BOX = (60, 170, VW-60, 1330)` with the real-picture chip; pop-zoom on the last | Full-height portraits centred on the field (the shared rules' rule 4 allows two side by side, but these flip rapidly, so one at a time is right). **Re-measure the chip placement** with a person mask (§6.2). Keep the pop-zoom. |
| overlays: `lt` lower thirds | `y_bottom=1600` | bottom above **980**, left margin as Ad 1's. |
| overlays: `pill` (CTA) | near bottom | bottom above **980**; captions muted under it (already in the mute list). |
| flashes | full-frame | unchanged (square frame). |
| captions | `CAP_Y 1400` | **CAP_Y ≈ 880–900** (Ad 1 square). Regenerate the PNGs; the caption cache key includes `CAP_Y`. Keep the same word timing (`words_ctc.json`) and the same mutes. Add a soft dark scrim behind the band wherever it sits over busy footage (Ad 1 lesson 12: green highlight on green shorts was unreadable). |

**Safe area** (shared square rules): nothing that must be read below y≈980 (except window/statement text down to 1030)
or above y≈80, and nothing readable in the right-hand 100 px. For Dan's judgment only, don't redesign: Google's square
safe-zone template marks only y 48–689 as clear of YouTube UI in some inventory. Ad 1 was approved below that anyway;
mention it in the notes.

### 5.4 Render and mux

- Render in chunks like `master15.sh`: chunk boundaries `0–2845`, `2845–5640`, `5640–7948`. Encode, concat with
  `-c copy`, assert the concatenated frame count is 7,948 by **counting frames** (`ffprobe -count_frames -select_streams v
  -show_entries stream=nb_read_frames`), never from container duration.
- Mux with a copy of `zmux.py` adapted: picture stream copied, **audio = `-map 1:a:0 -c:a copy` from the approved vertical
  master**, md5 asserted, written to a temp name and atomically renamed.
- Never overwrite a file a review or gate is reading. Render revisions to a new name.

### 5.5 The cutdown

- The cutdown is **the same six segments** as the vertical's (`cut_plan.json`: master frames `p0–p1` → cut frames
  `c0–c1`: 0–219, 439–639, 4392–4886, 5278–5640, 6822–7022, 7687–7948). Build it the way the vertical did
  (`cut6.sh` → `zcut_build3.py` → `render3.py --cutplan cut_plan.json --out cut/picture.mp4`), adapted for 1:1, then mux
  with the **vertical cutdown's AAC stream copied**, md5 asserted, 1,736 frames asserted.
- ⚠ `cut/` in the vertical build is a **forked** build dir with its own copies of `beats.py`, `g3.py`, `g5.py`,
  `captions.py` and an embedded time map. **A fix in the master's copy does NOT reach it.** Regenerate `cut/` from your
  fixed master files (that's what `zcut_build3.py` + the `cp` lines in `cut6.sh` do) every time you change graphics.
- `cut6.sh` also asserts the cut timeline never opens an app card before 5.84 s into the recording (the stranger photo,
  §6.4). Keep that assert.
- Selection-cutdown traps from the Ad 1 square (all real defects that every automated gate missed; `a11_sq_ad1/README.md`
  has details): frame-exact ranges (never `-ss <seconds>`; select by frame index and assert each range's first and last
  frame against the master's pixels); caption mutes must be **clamped** to ranges, not dropped; the first word after a
  seam must not be muted; a range must not open part-way through a lower third whose start was cut away; the concat
  demuxer's trailing `file` line is rendered, so write a blank caption state last.

---

## 6. Rules Dan has set that a gate will not fully catch

1. **Colour must match the approved vertical.** Muhammad's files carry no colour tags. ffmpeg decodes untagged video
   with the BT.601 matrix, while VLC and browsers show untagged HD as BT.709. Dan rejected a vertical whose grade was fitted
   on the wrong reading ("I look more tan"). The copied pipeline already decodes correctly. **Do not change any
   decode flags, LUT, curve or unsharp setting inside it.** Verify instead: take ~10 talk frames, crop the same source
   region from your square and from the approved vertical (both decoded the same way), and confirm mean per-channel
   difference ≤ 1.5 levels. Report the numbers.
   ⚠ For your own measurements, decode with `scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int`.
   Without `accurate_rnd`, ffmpeg's RGB conversion reads about 1.7 levels dark.
2. **Labels on any picture of Dan go ABOVE or BESIDE his head, never over his face or his abs** (Dan, 2026-09-12 and
   09-13). Measure placement with a person mask on the *rendered* frames (every 3rd frame of the beat plus the last,
   because stills push/zoom), union the masks, dilate 16 px, search above-head first, then beside-head (1–3 lines),
   then anywhere clear. Bigger type wins over fewer lines. Ad 1's tool: `reference/a11_sq_ad1/sqlabelplace.py` (it
   has a `--verify` mode, §7). The person mask CLI is Apple Vision:
   `.claude/skills/shorts/reference/recentre/personmask.swift` (compile with `swiftc -O`).
3. **Exactly one label per picture of Dan's physique:** real photo-shoot pictures carry "Real picture of me — not
   AI-generated"; AI images and clips carry "AI-GENERATED". His two 200 lb BEFORE pictures (2:26–2:33) are unlabelled
   in the approved vertical; keep that (it is an open question for Dan, not yours to change).
4. **The stranger-photo trap.** The only real app recording on disk uploads a photo of a man who is **not Dan**. The
   vertical cuts around it (a source floor and ceiling on the recording, and a lock screen rebuilt with Dan's own goal
   image, `assets/lock_screen_dan.png`). Your square must keep those exact time maps and assets. After rendering, look
   at every frame of the phone beats (5278–5362 upload, 5509–5640 lock screen) at full size: no stranger's photo anywhere.
   `znostranger.py` in the build scans for it; run it on your render.
5. **Before/after compliance (Google Ads):** never a before picture and an after/goal picture on screen at the same
   time, and never back to back without a camera (talking) scene between them. No morphs, no body-shaming zooms, and
   never the app's email-capture screen or its before/after reveal screen. The vertical is compliant. Re-laying out must
   not make two pictures share a frame.
6. **AI clips must not look fake.** Dan rejects any AI giveaway even when the clip is labelled: breath/steam/fog,
   melting or extra fingers, faces that change, lips moving without speech, reflections that do not match. A cover crop
   can move a giveaway into view or cut the action badly, so read the story shots after your crop.
7. **Framing standard:** hair-anchored, never a wide shot, Dan centred. The talk crop rule in §5.3 preserves it.
8. **Nothing Dan approved changes except geometry.** Same edit points, same flashes, same text wording (including the
   full 2:14 bullet: "Because even though I was a personal trainer back in my 20s, as a 38 year old dad running a
   successful ad agency."), same labels, same SFX, same colour, same audio.

---

## 7. Gates (run on the exact delivered bytes, in your build dir, master AND cutdown)

The vertical's gates were written for 1080×1920. Each must be re-bounded for 1080×1080, **as a fraction of frame
height where the bound is a size** (e.g. hair margin 36/1920 = 1.875 % → 20 px), and must read the build's own
`CAP_Y`. Don't reuse a 9:16 constant silently. A gate measuring empty field fails a correct build or passes a broken
one. Copies of the square versions exist in `reference/a10_sq/` and `reference/a11_sq_ad1/` (`hairgate_sq.py`,
`sqhairgate.py`, `sqlanding.py`, `jumpcuts_sq.py`, `sqtextcheck.py`).

| gate | what | pass |
|---|---|---|
| `qc.py <file> --build-dir .` with a square `qc.json` | 20 structural checks (size, fps, frame count vs reference, audio is his, captions present, coverage, banned screens, watch pass done, centring, caption sync…) | 20/20 master; cutdown 18/20 is expected **only** for the two true-peak rows |
| watch pass | `watch.py <file>` → `zwatch_sheets.py` → **look at every sheet** → `zwatch_mark.py <file> "<what you looked at and found>"` | a written, honest note. The mark ties to the file's sha256; re-mark after any re-render |
| hair gate | `zhairgate2.py`, re-bounded for 1080 tall | PASSED |
| `caption_sync_check.py` | highlighted word vs forced alignment, reading the square's `CAP_Y` | CAPTION SYNC PASS |
| `landing_check.py` | talk cuts don't jump | pass |
| `sqlabelplace.py --verify <file>` (port) | no chip box within 8 px of Dan's person mask on any labelled beat | all pass |
| `sqtextcheck.py <file>` (port) | each text screen's ink ends ≤ 1036 and the empty band under it ≤ 70 px | all pass |
| `znostranger.py` | no stranger photo in the phone beats | 0.0000 |
| audio | `python3 .claude/skills/_shared/audio/audio_gate.py <file> --reference-mix <his mix: ref/ad3_v6hd.mp4 for the master, cut/his_mix.wav for the cutdown> --verbatim --ab <A/B clip path>` | master PASS; cutdown FAIL on `tp` only (accepted, write the note) |
| delivery gate | `python3 .claude/skills/_shared/deliver/gate.py <file> --format ad1x1 --plan plan.json` (check `formats.py` for the exact square format name; build `plan.json` with a port of `plan_build.py --transcribe`) | compare with the vertical's result: its only FAIL was `compliance:labels` (the gate takes one chip position per kind, a known limit) plus six NOT MEASURED rows. **Report new failures; never tune a bound.** |

⚠ **Changing any shared gate or threshold** (anything under `.claude/skills/_shared/`) requires
`python3 .claude/skills/_shared/qc_corpus/run.py` to pass before you commit it. It takes ~30 minutes and re-grades
every file Dan approved or rejected. Prefer square-specific copies in your build dir over editing shared gates.

---

## 8. Independent review (mandatory; expect "does not ship" the first time)

Every earlier build had real defects that passed all gates and were caught only by an independent reviewer. After your
gates pass, run a **separate** review (a fresh agent/session with no memory of your build) on both delivered files, with
this brief:

- Verify frame counts, audio md5s, and that frames match the vertical's timeline (sample frame n in both; same content).
- Every beat boundary and cutdown seam as consecutive frames (−2…+2): jump cuts, black/duplicate frames, graphics
  opening half-drawn, a flash off the cut.
- Every graphic at full size: text verbatim vs the vertical, nothing cut at an edge, nothing readable below 980
  (text screens 1030) or in the right 100 px, text-screen bottom band.
- Every label: above/beside Dan's head, never on face or abs; exactly one per picture; AI chips off faces.
- Talk frames: Dan centred, hair not cut, no wide shot.
- Story/AI shots after the crop: no giveaway, no head cut off, key action visible.
- Phone beats: no stranger's photo on any frame.
- Compliance: before and after never together or back to back.
- Colour vs the vertical (the §6.1 measurement).

Fix what it finds, re-render, re-run the gates it touches, and re-review the fixed beats. Record every round in
`notes-square.md`.

---

## 9. Deliver and report

1. Copy both masters into the Ad 3 folder under the §4 names, verify with md5, run the audio gate on the delivered
   copies (stamps beside them), write the cutdown's accepted-true-peak note, make the 540p review copies, copy the
   A/B audio clips, write `notes-square.md` and `recipe-square/`.
2. **Show Dan the review copies.** Report in plain language: what the square looks like, the layout decisions per beat
   type, what (if anything) needs his eye, gate and review results in one or two sentences each.
3. Update your `AI_COORDINATION.md` entry: *"Ad 3 square delivered, awaiting Dan's approval."* Nothing else.
4. Do not upload, do not touch Google Ads, do not check dashboard tasks. On Dan's approval a separate job adds the
   square to Ad 3's Demand Gen ad groups (template: `Handoffs/handoff-20260914-ad3-youtube-and-ads.md`, one more
   `videos` entry per file).

---

## 10. Quick reference

| item | value |
|---|---|
| Muhammad's HD (16:9, untagged) | `/Volumes/Extreme/_edit_work/ad3-vert/ref/ad3_v6hd.mp4`, 7,948 frames, audio md5 `db408fd0bc0ba2a44245df947cb7e1f3` |
| approved vertical master / cutdown | `ad3-vert/ad3_vertical_9x16.mp4` / `ad3-vert/cut/ad3_vertical_9x16_59s.mp4` |
| approved square template (look) | Ad 1 square, `Muhammad Ad Videos/this picture got me abs - ad 1/` + `reference/a11_sq_ad1/` |
| story clip | `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-trainer-vs-robot-story-35s_v2.mp4` (1080×1920, 24 fps, 847 frames; only v2) |
| story map | vertical frames 1944–2845 ← source seconds on a straight line (`STORY_MAP` in `beats.py`); the clip's own shot cuts land on frames 2065, 2202, 2339, 2477, 2614, 2751 |
| timeline | 29.97 fps (30000/1001), 7,948 frames, 265.198 s; cutdown 1,736 frames, 57.92 s |
| Dan's standing rules | `AGENTS.md` (loaded in this project's `CLAUDE.md`) |

## Starter prompt (paste into Codex)

> You are building the 1:1 square version of an approved video ad. Read
> `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260914-ad3-square-codex.md` completely, then
> every document it tells you to read, in order, before changing anything. Treat
> `/Volumes/Extreme/_edit_work/ad3-vert/` as read-only; build in `/Volumes/Extreme/_edit_work/ad3-sq/`. Port the
> approved Ad 1 square's layout rules onto Ad 3's `render3.py` pipeline, settle every beat type on still frames first,
> then render the full square and the ≤0:59 square cutdown with the approved vertical's audio stream-copied (md5
> asserted). Run every gate in §7 and an independent review (§8), fix what they find, deliver per §9, and stop for Dan's
> approval. Never run more than two video builds at once, and never tune a gate bound to pass. Report to Dan in plain,
> non-technical language.

**Recommended:** Codex's strongest model at high reasoning effort. This is compositor geometry plus a review loop;
expect one long session or two. Fallback if Codex struggles: Claude Opus 5 / Fable 5.1, high effort, with the same
document.
