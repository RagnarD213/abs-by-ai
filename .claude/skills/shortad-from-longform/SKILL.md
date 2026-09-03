---
name: shortad-from-longform
description: Rebuild a FINISHED, finalized long-form video as a vertical 9:16 short ad, reproducing the finished video's style as closely as possible — recover its edit from the raw footage, measure its grade, palette and graphics, re-lay them out for a phone, then cut a ≤0:59 version. Use whenever Dan asks for a vertical or 9:16 version of a finished video, to "make a short ad from" a long-form cut, to reproduce an editor's finished style in vertical, or to turn a finalized ad or content video into Shorts/Reels creative — even if he doesn't say "/shortad-from-longform". For cutting shorts out of a video we ourselves rendered, /shorts is cheaper. For editing an ad from raw shoot footage use /ad-edit; for content videos use /longform-edit.
---

# /shortad-from-longform — a finished long-form cut, rebuilt vertical

> ## ⚠ ATTEMPT 2 (2026-08-26) FOUND SIX DEFECTS THAT PASSED EVERY METRIC
>
> Attempt 2 was built to these rules, and its FIRST render still passed the whole gate
> while: **every overlay was invisible** (7 lower thirds, 3 CTA pills, 11 flashes — an
> `enable=` window gates by the main clock while the overlay stream runs from its own
> t=0), **six segments opened on a black frame**, **twelve card beats sat frozen**, **every
> lowercase graphic was garbled** (per-character text drawn with `anchor="lt"` aligns each
> glyph by its own top), **the b-roll wore a porthole vignette**, and — worst — **the
> recovered EDL was missing Dan's entire hook line**, which attempt 1 had also shipped.
> None of that is visible to a metric. Rules **[A2]** below are the ones that catch it.
>
> ## ⚠ ATTEMPT 1 (2026-08-25) PASSED 11/11 QC AND DAN CALLED IT "TRULY AWFUL"
>
> Every numbered rule below marked **[R1]** exists because of that rejection. The
> meta-failure: **the gate measured format (LUFS, frame size, coverage %, change rate)
> and formats were perfect — but no check ever WATCHED the video.** A jump cut, a
> mistimed whoosh, sleepy music and a non-sequitur are all invisible to metrics and to
> contact sheets of still frames. The prose warning in /longform-edit — "a quality bar
> that exists only in prose will be skipped" — has a sibling: **a quality bar built only
> from numbers will pass garbage.** The watch pass in Step 7 is now the gate; the
> numbers are only the preconditions.


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

## Step 1 — RECOVER THE REFERENCE'S EDIT (this is the whole trick)

### 1a. Word-sequence alignment gives take selection and the block structure

Needleman–Wunsch the reference's word list against the raw roll's, monotonic, with a
CHEAP gap penalty on the raw side (the roll is full of unused takes) and an expensive one
on the cut side. `reference/wordalign.py`.

- Expect **>99 % of the cut's words to match**. Less than ~95 % means you have the wrong
  raw roll.
- **Normalise apostrophes away on BOTH sides.** Whisper writes `i'm`; a phrase written
  `im` will not match, and the failure looks like "phrase not found", not like a bug.
- Group the matched pairs by their offset `raw_start − cut_start`. Runs of constant
  offset are the editor's takes; the jumps between runs are their take changes.

### 1b. Whole-segment audio matching, with recursive splitting, gives the exact cuts

Word timings are ±50 ms and some splices sit inside a word gap Whisper timed badly. Refine
with `reference/segfit.py`: for each candidate segment, take its whole span of 24-band
log-mel frames and slide it against the raw within ±5 s; if the match score is below ~0.60,
split the segment at its worst-agreeing frame and recurse.

Long windows are what makes this stable. **A per-window (0.4 s) sliding correlation
over-segments badly** — the first attempt produced 199 "segments" with backwards jumps,
because at that length noise in the mel envelope exceeds the offset differences you are
trying to detect.

Expect: mean score ≥ 0.75, and a segment list in the 60–100 range for a 4-minute ad.

### 1c. VERIFY THE EDL BY WORDS. POSE CANNOT SEE A MISSING WORD. **[A2]**

Attempt 1 verified its EDL by eyeballing pose at 14 timecodes and passed. Conform the
voice, transcribe it, and DP-align it against the reference's transcript
(`reference/a2/wordmatch.py`). Attempt 1's EDL scored **94.7 %** — and the gaps were:

* **Dan's entire hook line was absent from the mix.** Segment 0 pointed at 2.5 s of room
  tone before he speaks. It shipped that way.
* "And this is where I'm at today" replaced by the tail of the previous sentence.
* "With AI", "your life", "screen", "belly fat" and "for free" each clipped off the end of
  a segment, and one range ran BACKWARDS past the previous one, stuttering a phrase.

**Cause, and it will happen again: `segfit.py` splits only where its mel score drops below
0.60, so every pause trim the editor made INSIDE a sentence stays hidden.** The segment
keeps one `src_in`, the source then runs slower than the cut, and the segment's last words
fall off the end.

**Fix: re-derive every segment's offset from WORD alignment against the raw roll's own
transcript, and split wherever that offset steps** (`reference/a2/edl_words.py`,
`reference/a2/edl_resplit.py`). Cut boundaries never move, so the frame plan and the
picture are untouched. On this ad, 73 segments became 99 and fidelity went 94.7 → **98.1 %**;
every remaining difference was two Whisper models disagreeing on the same audio
("gonna"/"going to", "woo"/"WuWu"). **Target ≥ 98 %, and read every "(missing)" by hand.**

Two traps inside this one:
- **envelope correlation is useless under ~2 s.** Dan repeats lines across takes, so a
  different take often scores higher. `reference/a2/edl_verify.py` is a screen, not a
  verdict; the word alignment decides.
- **a stale Whisper cache drifts.** `C1591.whisper.json` (built six days earlier) put
  "personalized" at 296.14; a fresh transcription put it at **296.78**, and two splits
  landed inside the word before that was caught. Re-transcribe the window.

Then still do the pose check — but as a second opinion, not the proof. ⚠ **Do NOT verify
with raw pixel correlation:** the reference is graded, punched in and vignetted, so a
correct conform still scores ~0.35 against it.

### 1d. Multi-roll + organic lessons (ab-wheel reproduction, 2026-08-27)

Recovering Muhammad's 4-roll organic cut added five rules that supersede nothing above
but extend it (`/longform-edit reference/mrepro_*.py` is the working pipeline):

1. **On a MULTI-ROLL video, word-align the cut against each roll separately**, resolve
   per-word candidates by run-continuity (lookahead), and then let AUDIO XCORR be the
   authority: slide 1 s band-passed (300–3400 Hz) windows of the reference mix against
   the candidate roll around the word-derived offset. Voiced regions lock at corr
   0.87–1.00; the word alignment alone wobbled between three hook takes.
2. **Snap every segment boundary into an inter-word gap of the REFERENCE'S OWN
   transcript**, choosing each straddling word's side by per-word xcorr. Boundaries
   placed by anchor midpoints clipped word edges 8 times on this cut (96.7 % → 99.2 %
   conform fidelity after snapping) — including "crunches", the same trailing-fricative
   word the longform skill already documents.
3. **A montage/set section with a steadily CLIMBING offset is a TIME-LAPSE, not a cut
   sequence.** Offset slope ≈ 3 means 3× retime; confirm with the rep-period ratio
   (frame-diff autocorrelation: his cut 1.23 s vs raw 3.70 s = 3.0). All four of his
   workout sets were ~2.87–3.07×, source-continuous with the neighbouring voice spans.
4. **His mix can carry a take-1 LINE spliced into a take-2 region** ("let's talk about
   what it looks like live" = C1633 take 1 at 2.9–6.1 inside a take-2 segment) — and a
   psych-up line grabbed from 30 s later ("All right. Let's do it." at src 73.7). When
   a boundary's words score weakly on BOTH sides, xcorr the phrase against the WHOLE
   roll, then all rolls; corr 0.99 at some distant src is the answer, and a stale
   cached transcript that never heard the line is usually why word alignment missed it.
5. **Graphic-band masking + deeper scales rescues "insert" false positives.** Frames
   the framing fit rejects at scale ≤ 1.7 may be conform punched to ~2× under a pill —
   mask the pill band (top ~210 px) and search scales to 2.3 before calling a window
   an insert. 189 of this cut's low-ncc frames resolved that way; the survivors were
   the real inserts, exactly matching the visual catalog.

---

## Step 2 — MEASURE THE LOOK (four separate measurements, never one)

### Framing
Fit `scale` + `(dx,dy)` per sampled frame by searching over a downscaled copy (`reference/geofit.py`).
Editors alternate two or three sizes — a wide at 1.00 and a punch-in around 1.15–1.25,
usually recentred upward. Correlations of 0.85–0.98 mean the fit is real.

### Tone curve — fit on a CENTRE BOX ONLY
Percentile-match raw→reference per channel **inside a small centre box**, where the
vignette is ≈1.0. Fitting over the whole frame smears the vignette into the curve and the
background comes out far too bright. (This happened; the first fit lifted the doorway
behind Dan by 40 levels.)

### Vignette — measured AFTER the tone curve, as a radial gain
Apply the fitted curve to the raw, then take `median(reference_luma / toned_luma)` in
radial bins. A modern editor's vignette is stronger than it looks: ~1.00 at centre, 0.70
at r=0.9, 0.26 at the corners.
**Re-derive it in the OUTPUT frame's coordinates** — do not carry the 16:9 mask over.

### Palette, grid and type
Sample MEDIAN colour inside flat regions of the actual graphics (not a guessed box).
Get the grid pitch from an FFT of a row/column average. Then check `_shared/motionlib.py`
before building anything: the `J2AD` palette already measures identical to what these
editors use (field 13,14,11 · accent 140,152,88), and `field_bg`, `card`, `chip`,
`bullets_build`, `title_plate`, `oblique`, `encode` are all already written.

---

## Step 3 — MEASURE THE STRUCTURE

Classify every half-second of the reference as "talking head" vs "insert/graphic" by
correlating it against the conform at the two or three known framings. Report:

| metric | modern standard | why |
|---|---|---|
| insert/graphic coverage | **58–65 %** | below ~50 % reads as a webcam recording |
| visual changes / min | **≥ 9**, 15 is comfortable | |
| longest stretch with no visual change | **≤ 16 s** | |

**[R1] Step HIS cut at 1-second intervals (not 4) and reproduce his beat sheet
LITERALLY** — every insert, in order, unless a standing rule bans it, and log each
deviation with its reason. Attempt 1 sampled at 4 s, substituted freely where inspection
was thin, and Dan immediately saw "a lot missing… not reproducing Muhammad's video at
all." The reference IS the spec; deviation is the exception, not the default.

Then read one contact sheet of the insert regions and write the beat list by hand. Nothing
automates "what is this insert" — but the classifier tells you exactly where to look, which
turns a 4-minute video into ~16 frames to inspect.

---

## Step 4 — AUDIO, BEFORE ANY OF THE PICTURE WORK

> ## ⚠ [APPROVED METHOD — Dan, 2026-08-27] THE AUDIO IS THE REFERENCE'S OWN MIX
>
> **This is now the standard for every vertical rebuilt from a finished horizontal, and
> the approach Dan approved on the Ad-1 vertical: "this audio sounds great … probably
> even better than Muhammad's."** The full-length 9:16 master is frame-locked to the
> reference's timeline, so the reference render's ENTIRE audio track — the editor's voice
> edit, his music bed, everything — goes under the rebuilt picture VERBATIM.
>
> ## ⚠⚠ NEVER RUN `loudnorm` ON THE REFERENCE'S MIX. PURE GAIN + LIMITER, ALWAYS.
> **(Dan, 2026-09-02: "the audio sounds horrible … nowhere near as good as Muhammad's …
> never deliver anything again that doesn't sound like Muhammad's videos.")** The Ad-1
> vertical shipped his mix through `loudnorm`, which **silently fell back to DYNAMIC mode**
> — his master was −18.2 LUFS already peaking at +0.0 dBTP, so a +4 dB LINEAR lift under a
> true-peak ceiling is arithmetically impossible and loudnorm compressed instead of erroring.
> Measured on the delivered file: the gain it applied swung **+1.2 dB to +9.5 dB second to
> second (sd 1.00 dB)** and LRA fell **3.5 → 2.4 LU**. In the ear that is the bed and the
> room tone swelling up 9 dB in every gap — worst in the first two seconds of the hook.
> The per-second CORRELATION with his mix was 0.997, so every provenance check said the
> audio was his; correlation is level-normalised and **cannot see a slow gain envelope.**
>
> The processing is now `_shared/audio/voice_chain.py --finish-only` (`finish_audio.py` is a shim to
> it) — and **the delivered file then goes through `_shared/audio/audio_gate.py` like every other
> render**; his mix passes the reference rows by construction and the gate adds loudness, true peak,
> silence and length, and writes the stamp `qc.py` check 17 requires. Under the hood it is:
> **`volume=<G>dB` (one constant gain), then
> `alimiter=limit=0.85:level=disabled`**, compensating the limiter's **239-sample latency**
> (`atrim=start_sample=239,apad=pad_len=239` — re-measure it if you change `attack`, which
> changes the latency and will silently desync the whole track). Iterate G two or three
> times to land the ENCODED file inside −14 ±0.8 LUFS and ≤ −1.0 dBTP; on Ad 1, G = +4.2 dB
> → −14.5 LUFS / −1.3 dBTP / LRA 2.8 / per-second gain sd **0.51**. Ceiling 0.85 rather than
> 0.79 because the shallower ceiling makes the limiter do less work on an already-brickwalled
> master (0.79 cost 0.1 LU of LRA for nothing). `level=1`, the limiter's default, BOOSTS the
> whole mix — always disable it; AAC overshoots the wav's true peak by ~0.5–0.7 dB.
>
> **THE GATE — `reference/gain_flatness.py SOURCE OUTPUT --gain G`, run on the ENCODED
> deliverable, never on the intermediate wav.** It takes the per-second RMS ratio against the
> reference's mix and tests it ONE-SIDED, which is the whole trick: a limiter can only pull
> the loudest seconds DOWN, while a compressor pushes quiet ones UP. Nothing above G
> (max ≤ G + 0.05 dB), p90 ≥ G − 0.25 (most of the file untouched), min ≥ G − 2.5 (shaving,
> not gouging). On the two Ad-1 files it separates them outright: fixed reads
> max +4.20 / p90 +4.20 / median +4.11 / min +2.03 → PASS; the rejected one reads
> max +9.45 with **133 of 232 seconds sitting above the constant gain** → FAIL.
>
> ⚠ **Do NOT gate on the standard deviation.** I tried sd ≤ 0.35 dB first and it failed the
> GOOD file — a correct master measures sd ≈ 0.51 dB purely from legitimate downward shaving,
> and the only way to make an sd gate pass it is to loosen it until the bad file passes too.
> Report sd, gate the ceiling. Also report LRA against the reference's — losing more than
> ~0.8 LU means the lift is too big for that master (Ad 1: his 3.5 → ours 2.8).
>
> Dan does still want the lift ("was a little bit too quiet") — but **level never comes
> before the sound.** If a reference master is hot enough that −14 cannot be reached with a
> flat gain, take the smaller lift and say so.
>
> The conform voice (everything below in this step) is still built — but it is a
> **LIP-SYNC PROXY, not a deliverable**. Before muxing, xcorr every EDL segment's
> conform voice against the reference audio in its own cut window (band 300–3400 Hz;
> per-segment windows — larger windows straddle offset changes and refuse to lock):
> shift any segment over 40 ms (`src_in −= lag`, refine iteratively to ±10 ms), and
> treat a segment whose lag DRIFTS as a **WRONG-TAKE segment** — same words at a
> different pace can never be shifted into sync; fresh-Whisper word durations identify
> the editor's real take. Bed-picking (items 3–4 below) applies ONLY where the
> reference mix cannot be used — e.g. the ≤0:59 cutdown, where time is removed and the
> bed/SFX must be rebuilt over the new duration.

1. **`_shared/audio/pick_lav.py` on BOTH the reference and the raw** (`chan_analyse.py` is a shim).
   Jeff's rolls are not stereo — they carry two different microphones ~7.8 ms apart, sometimes
   polarity-inverted, and the 8/28 rolls carry four mono tracks. **The voice comes from whatever
   `pick_lav` measures as the lav, as mono** — `build_audio.py` reads its `audio_source.json`. A good editor has already fixed
   this in their render (check: L/R correlation ≈ +0.99 at lag 0, zero clipped samples).
2. **Loudness of the reference** — and do not copy it. Editors ship −18 LUFS; ads want
   **−14 LUFS / ≤ −1.5 dBTP**.
3. **Music bed detection: use the SPECTRAL TILT in the speech gaps, not the floor level.**
   A bed shows as 30–120 Hz sitting ~12 dB above the rest of the spectrum in the gaps.
   The "floor above −45 dB ⇒ bed" heuristic false-positives on any hard-limited master.
4. **[R1] Pick the bed by TEMPO AND ENERGY against THIS reference, and A/B it by ear.**
   Attempt 1 reused a bed a previous session had picked by spectral shape against a
   DIFFERENT, older cut. The reference's bed measured a driving ~120+ BPM pulse; the
   reused pick was a 99 BPM soft acoustic strummer at −21 dB — Dan: "it kind of puts me
   to sleep." Measure onset rate + tempo (flux autocorrelation) on the reference's mix,
   shortlist by tempo, then LISTEN to 20 s of each candidate under the voice before
   committing. A bed choice never transfers between references.

   **[A2] Claude cannot listen, so say so and hand Dan an A/B.** Measure his bed's beat
   period in both the 30–150 Hz and 6–14 kHz bands (`reference/a2/tempofit.py`), rank
   candidates on tempo first and band profile second (`reference/a2/pick_bed2.py`), then
   render `AB_music_his-bed-vs-ours.mp4` — the same three lines under his mix, then under
   yours — and tell Dan in the notes that the FEEL is the one thing only he can judge.
   On this ad his bed measured **0.480 s = 125 BPM**; Pixabay "Funk & Breakbeat" matched
   it exactly. Attempt 1's inherited bed measured 99.6 BPM: "it kind of puts me to sleep."
   ⚠ **Licence: Pixabay Content Licence (commercial, no attribution) is the settled
   choice.** Kevin MacLeod's tracks matched the tempo too but are CC-BY, which needs
   perpetual credit and is heavily Content-ID fingerprinted.

---

## Step 5 — THE VERTICAL TRANSLATION RULES

These are the decisions that make or break the port. They are not stylistic preferences;
each one was arrived at by getting it wrong first.

1. **Left/right becomes above/below.** The reference puts bullets left and the talking head
   right. A 9:16 frame has no left and right to give. Dan goes in a full-width window at the
   TOP; the text goes underneath on the field.

2. **The window height ADAPTS to the beat's text.** Measure the wrapped text block, then
   size the window to `1920 − text − margins`, clamped to 820–1220 px. One fixed compromise
   size makes short beats look empty and long beats unreadable.

3. **16:9 SOURCE IS NEVER CROPPED TO FULL-BLEED.** Cropping 1280×720 to 9:16 is a **2.7×
   upscale**. Put it in the olive card instead — which is the editor's own design language,
   and is a DOWNSCALE. Full-bleed is only for natively-vertical or ≥1440-tall sources.
   The talking head is the one exception: 1080p → 608×1080 → 1080×1920 is 1.78×, it is
   unavoidable, and `unsharp=5:5:0.85` carries it.

4. **A card's hole matches the MEDIA's aspect ratio, measured from the file.** A fixed 16:9
   hole cover-crops a portrait photo, and what it crops off a photo of a person is their head.

5. **Centre the vertical crop on the subject's HEAD BAND, not their silhouette.** A
   whole-frame difference centroid is dragged sideways by hand gestures — on this shoot by
   114 px, which put Dan a third of the way from the left edge. Restrict the band to the
   head (y ≈ 90–260 of 1080). Locked-off shot ⇒ one fixed crop for the whole video (sd 18 px).

6. **Captions are suppressed wherever a graphic carries its own words.** Bullets, title
   cards, statements and the CTA pill all paraphrase the very sentence being spoken; running
   captions under them puts two text systems in a 1080-wide frame.

7. **Safe area:** nothing that must be read below y≈1660 or above y≈150; captions centred at
   y≈1250. YouTube Shorts takes the bottom ~230 px and the right ~120 px; IG Reels takes ~350.

8. **[A2] REPRODUCE HIS ZOOM SCHEDULE. THE TALKING HEAD MUST NEVER BE ONE FIXED CROP.**
   ⚠ **This rule replaces attempt 1's, which was measurably wrong.** Attempt 1 concluded
   he "alternates 1.00 ↔ 1.20 ACROSS SPLICES" and that 23 splices shipped as naked jump
   cuts. Fitting his framing per 0.25 s says otherwise:

   * his punch-ins **ramp over ~0.5 s, hold 1.5–3.5 s, then ramp out** — they are an
     emphasis device on particular lines and they mostly SPAN splices rather than landing
     on them (14 of them in a 3:53 ad, covering **39 %** of the talking head);
   * **his talk-to-talk splices jump as much as ours would**: median spike 10.3 against a
     1.92 median frame diff, with 43 of his 72 splices over 4× his own median (ours: 32).

   So the defect was never concealment. It was that 100 % of attempt 1's talk was locked
   off, which is what makes a tripod shot read as a webcam recording and makes every trim
   in it visible. Measure his schedule (`reference/a2/cover.py` for the per-0.25 s scale,
   `reference/a2/geofit2.py` for the per-segment fit) and reproduce it as ramps —
   `zoompan` with a smoothstepped `z` (`reference/render.py: push_z_expr`). QC check 12
   fails a build where under 25 % of the talk is inside a push.

9. **[R1] Mute b-roll must never show anyone TALKING.** A clip of Dan mid-sentence with
   his mouth moving and no matching audio reads as a glitch, not as b-roll. Attempt 1's
   "this is where I'm at today" beat used outdoor footage of Dan talking to camera.
   Pick in-points where the subject is DOING something, and frame-check every in-point
   for visible speech before committing.

10. **Render captions with PIL, not libass.** Manrope is a VARIABLE font and libass takes the
   default instance — ASS captions come out Regular while every graphic is ExtraBold. Build
   one PNG per word state and assemble with the concat demuxer (`duration` directives); that
   is fast and keeps one type system.

11. **[APPROVED 2026-08-27] The talking-head crop FOLLOWS a smoothed face track — never a
   fixed x.** The subject leans through a locked-off shot (Dan's face wandered 835–1037 in
   1920), and a ~608-px 9:16 crop nearly doubles every lean on the phone; Dan caught one
   timestamp and it was a class. Build the track from a skin-band centroid per 0.25 s
   **restricted to FACE height (y 70–240 of 1080 — raised hands pollute a wider band)**,
   median-filter ~2 s, slope-limit 80 px/s, and drive `crop x` with a piecewise-linear
   expression. Same track feeds the window/statement beats' hole crop (per-beat median).
   Verify by drawing the centreline on frames at the extremes of the track.

12. **[APPROVED 2026-08-27] A card still needs MARGINS sized for the push, and the subject's
   full head-to-shorts must survive the tightest zoom.** The still-push crops ~6% per side
   at start and ~8.5% at peak — so the crop must put the hairline ≥10% from the top edge
   and keep the shorts line inside the tightest window, subject horizontally centred.
   Verify by drawing BOTH zoom windows on the asset before rendering. If the source photo
   cannot give hairline + shorts + centred at once, use a different photo — Dan prefers a
   correct different picture over a cropped right one, and mirror-padding past a limb
   makes a visible artifact.

13. **[APPROVED 2026-08-27] App-recording beats retime VARIABLY, never uniformly**: the
   interactions run near real time (1.2–1.9×) and the progress/loading screens ~5× —
   a uniform speed makes the app's loading feel slow (Dan's 3:13 note).

---

## Step 6 — BUILD ORDER

```
a2/edl_words.py    re-derive every src_in from WORD alignment  <-- run this FIRST
a2/edl_resplit.py  split segments at the pause trims he made INSIDE sentences
a2/wordmatch.py    the proof: our conformed voice vs his transcript, target >=98%
a2/cover.py        per-0.25s framing + talk-visible classification
a2/geofit2.py      per-segment framing fit (FFT shift, loops over scale)
a2/tempofit.py     beat period of his bed, low band and hat band
a2/pick_bed2.py    rank candidate beds on tempo first, band profile second
build_base.py      conform the raw to the corrected EDL + tone curve, STAYS 16:9
vlib.py            vertical layout library (plates, type-on reveal, lower thirds, flash)
beats.py           beat sheet stepped at 1s off HIS cut + PUSHES + FLASHES + LOWER_THIRDS
render.py          one output segment per beat -> concat -> overlays (shifted, not gated)
build_audio.py     lav voice (per pick_lav's audio_source.json) -> EQ fitted to HIS mix -> bed -> HIS_SFX list
finish_audio.py    _shared/audio/voice_chain.py --finish-only: CONSTANT gain + alimiter (NEVER loudnorm)
                   then _shared/audio/audio_gate.py on the delivered .mp4 (the stamp qc.py check 17 needs)
captions.py        word-timed, suppressed under text graphics, with a typo correction map
a2/watch.py        THE GATE: per-frame scan + a consecutive-frame strip at every boundary
qc.py              15 checks, the last of which is "the watch pass was done"
cutdown.py         the <=0:59 selection -- built ONLY from Dan's edited script
```

**Keep the base at the source's 16:9.** All reframing happens downstream, so one base
serves both the full-bleed and the windowed layouts. Rendering two bases doubles the
slowest step for nothing.

### The plate pattern
Every graphic beat renders ONE RGBA plate that is opaque everywhere except a rounded
"media hole"; the media is composited UNDERNEATH at the hole's final size. Animating the
hole (rather than the media) lets a card grow open without ever rescaling the picture in it.

### [R1] SFX: match HIS COUNT, measured, and only on graphic entrances
Attempt 1 fired 83 whoosh/pop events across 3:53 — one every 2.8 s — placed
programmatically on every beat boundary including plain b-roll cuts. Dan: "weird
swishing, swiping side effect appearing at random points." Count the reference's actual
SFX events by ear first (listen to the gaps); a typical cut carries a fraction of that.
SFX belong ONLY where a graphic physically enters or exits the frame — never on a
footage-to-footage cut, and never mechanically per beat.

**Count them by measurement, not by ear-guess:** run a high-band (3–14 kHz) transient
detector over every candidate graphic moment in his render and keep the ones above the
p90 of a random baseline. On this ad that gave **21 events, one per 11.1 s**, with ZERO on
his ten white flashes and zero on footage cuts. Then place exactly those, at your matching
beats — do not invent extras. Attempt 1 fired 83. QC check 13 fails anything denser than
one per 6 s.

### EQ-fit the voice to the REFERENCE's mix
Ten bands, several windows across both files, speech-active frames only. **Cap the fit at
+6 dB.** The raw fit here wanted +8.8 dB at 9 kHz — partly the reference's own music bed —
and that lifts lav hiss with the air. Gate BEFORE the EQ, always.

---

## Step 7 — QC: the WATCH PASS is the gate; the metrics are preconditions

**[R1] The metric gate passed a rejected video 11/11.** Before delivery, always run
`reference/a2/watch.py`, which does two things no metric does:

1. **Automated, over EVERY frame of the finished file:** frozen runs, black frames, and
   discontinuities that are not at a boundary the beat sheet knows about. This is what
   caught six one-frame blacks and twelve frozen card beats.
2. **Human, at every boundary:** a 2 s clip AND a strip of CONSECUTIVE frames at
   −4/−2/−1/0/+1/+2/+4/+8. **Consecutive frames are what expose a jump cut, a frozen
   segment or a mistimed animation** — a contact sheet at 1 s intervals cannot, and if you
   cannot play video, say so plainly in the notes rather than claiming you watched it.
3. **Look at real full-resolution frames too.** The garbled lowercase type ([A2] trap 5)
   was invisible at every review size and obvious at 1080 wide.
4. **The audio half is measurement when you cannot listen** — word alignment, clipped
   samples, dropouts, SFX at their planned times, bed tempo — and an A/B file for Dan.

**[MANDATORY, Dan 2026-08-27] AUDIO INTEGRITY ON EVERY DELIVERED FILE — masters AND review
copies.** A mux once silently truncated the audio stream at 2:24 of a 3:52 video, exited 0,
and passed every existing check; Dan heard a minute of silence no metric caught. Two checks,
run on the exact file being handed over (they are qc.py check 16): (1) the audio STREAM's
duration must match the video's within 0.15 s — container duration hides this, probe the
stream; (2) a per-second RMS scan with NO silent second anywhere (the mix carries a bed
throughout, so true silence anywhere is a dropout). Review-copy re-encodes inherit a broken
master, so scan them too before sending. And **overlay caches must be CONTENT-ADDRESSED**
(hash of kind+spec+duration in the filename) — an index-keyed cache put the previous
overlay's text on four lower thirds when one overlay was removed from the list.

### ⚠ STEP 7b — AN INDEPENDENT SUBAGENT AUDIT IS PART OF THIS SKILL (Dan, 2026-09-01)

**"I think calling Fable to review should be a part of this skill going forward."** It has
already overturned my own conclusion twice on the same deliverable, and both times I had
declared the thing fixed:

* it measured a version I had just called centred and found **sd ~110 px, 39 % of talking
  frames beyond 70 px, and two multi-second stretches where his face was cut by the frame
  edge** — which led to the crop-expression bug in rule 0;
* it caught that **my own eyeball reads of "he is off to the left" were MIRRORED** at three
  of four timestamps, which is what broke that bug open.

So after the watch pass, before delivering, launch a **fresh Fable subagent** on the exact
delivered file. Give it the compiled `personmask` CLI and the torso anchor, tell it which
beat kinds to judge (talk only), and demand: the population statistics, every contiguous
run beyond 60 px for >= 1 s, full-resolution verification of anything it flags, **and an
explicit opinion on whatever trade-off you just made** — a faster tracking crop can swap a
centering problem for a visible pan, and you are the last person who will notice that in
your own build. Ask it to be skeptical and to say plainly if you have traded one visible
problem for another. Relay its verdict to Dan rather than your own.

⚠ **A subagent that has completed cannot be resumed** — its transcript is gone and
`SendMessage` fails. Launch a fresh one for the re-audit and restate the context.

### ⚠ STEP 7c — SCAN FOR NAKED JUMP CUTS, AND REMEMBER THAT DAN'S REVISIONS CREATE THEM

He hides his trims under an insert, a framing change or a flash. **When a revision deletes
one of those inserts, the splice underneath is exposed as a naked jump cut** — Dan's REV 2
on Ad 2 removed an AI cartoon at 9.5-14.0 s and the splice at 13.70 s became a hard cut
where his mouth snaps from wide open to closed between adjacent frames.

**Compute the exposure set structurally rather than hunting for it:** list every splice in
the recovered EDL, mark which are covered in HIS beat map and which in YOURS, and the
difference is exactly what your revisions broke. On Ad 2 that was 2 splices out of 68.

⚠ **FRAME-DIFFERENCE DETECTORS DO NOT FIND THESE, and two of mine failed in a row.** A
whole-frame gray diff scored the real jump cut at **2.0x its local median — "clean"** —
because a talking head's global luminance barely moves when only his mouth and head pose
snap. A face-region diff still ranked it 12th of 28. **The instrument that works is the one
the watch pass already prescribes: pull frames at -2/-1/0/+1/+2 across each candidate and
look at them.** A sheet of ten candidates is one image.

**The fix that scales is a 5-frame cross-dissolve applied IN THE BASE**, where there are no
graphics, so every beat, caption and overlay downstream is untouched. Render a patch for
each splice from the raw at the grade -- the outgoing take continuing, fading into the
incoming one -- and overlay it so it REPLACES the incoming segment's first frames. Timeline
length is preserved exactly because nothing is inserted. Then re-render only the beats that
read from the base.

Only then run `reference/qc.py`, which is now **17 checks** (16 = audio integrity, 17 = the
`_shared/audio` gate stamp on this exact file):

1 frame size 1080×1920 · 2 fps 29.97 · 3 duration matches the reference · 4 −14 LUFS ±0.8 ·
5 true peak ≤ −1.0 dBTP · 6 L/R correlation > 0.98 · 7 ≥ 9 visual changes/min ·
8 no stretch > 16 s without a visual change · 9 insert coverage ≥ 55 % ·
10 no banned product screen reachable — **template-matched against the finished picture,
not read off the build plan** · 11 captions present · **12 the talking head is not one
fixed crop (≥ 25 % of talk inside a push)** · **13 SFX no denser than one per 6 s** ·
**14 bed tempo within 15 BPM of the reference bed** · **15 the WATCH PASS was done on this
exact file** — check 15 reads `logs/watch_pass.json` and refuses to pass without it, which
is the only way a "watch the video" rule survives contact with a build that is running late ·
**16 audio integrity: the audio stream runs the video's full length AND no second of the
file is silent** (per-second RMS scan; run it on review copies too) · **17 the audio is
FLAT against the reference's mix — per-second RMS ratio sd ≤ 0.35 dB and no second more
than 0.6 dB above the mean, measured on the ENCODED deliverable.** Check 17 is the one
that catches a compressor having got into the chain; per-second correlation cannot, because
it is level-normalised (Ad 1 scored 0.997 while sounding, in Dan's words, horrible).

---

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
- **Snap every range edge to the nearest beat boundary** (±0.3 s). A range starting 80 ms
  inside a card shows that card already half-open, which reads as a dropped frame.
- Rebuild the captions (re-timed through the range map), the music bed and the SFX over the
  new duration — those three cannot survive having time removed from under them. Cut the
  picture and the voice; regenerate everything else.
- **Assert `total ≤ 59.0` in code.** Shorts ads must never exceed 0:59.

---

## [A3] Attempt 3 (2026-08-26) — what "indistinguishable from his edit" actually took

Dan's bar for attempt 3: *"I should not be able to tell who edited which one. If
necessary, take things directly from his video."* Eight lessons, each paid for:

1. **The "21 SFX events" were OVER-DETECTION OF SPEECH CONSONANTS.** The decisive test is
   a voice-normalised comparison of his mix against the EDL-mapped raw at the same
   moments, in BOTH the 3–14 kHz and 250–2500 Hz bands: every flash "transient" was Dan's
   own sibilance (ratios 0.4–1.4×). **His flashes are silent, and his whole mix contains
   NO whoosh** — only a ~22 ms high-band click (centroid ~10 kHz) at graphic entrances,
   provable at exactly four gap instances. Lift the click from a silent gap in his own
   render and place it at his measured level (peak ≈ 1.3× voice RMS). The synthesised
   whooshes attempt 2 shipped at his "measured density" were themselves the "swiping
   shit" Dan hated.
2. **His content cuts land EXACTLY ON the flash peak** (verified on three instances where
   a static graphic precedes the flash). Place the template peak ON our beat boundary —
   attempt 2's flash windows sat 0–5 frames off our cuts, which reads as a flash NEAR a
   cut instead of one hiding it. And his flash is composited by SCREEN blend, blue→white,
   with a pedestal that floods the frame only at peak.
3. **You cannot decompose his flash asset out of a render where the content moves** —
   subtraction and screen-inversion both leave content ghosts, and min/median across
   instances fails because the instances share the same scene. What works: recover the
   ENVELOPE from the luma trace (the same asset repeats, fingerprint 243/138/162/228/
   174/174/214), the COLOUR and SPATIAL falloff from the pre-cut ramp frames of instances
   whose pre-side is static, take the near-saturated peak from his real frames, and
   resynthesise — then verify PHASE-MATCHED against his frames at ±1/±2/±3/+8.
4. **`edl_resplit` can hallucinate tiny segments pointing at the WRONG TAKES.** Two
   segments of 0.20/0.43 s claimed "pack abs" came from src 53/77 when his audio was ONE
   continuous take (offset constant across every word). Any sub-half-second segment with
   an implausible source jump: check the word-level offsets by hand — the fix deleted two
   splices AND corrected the audio (this was Dan's "0:21 jump cut of two things that
   don't belong together").
5. **A stale Whisper cache can be 2 s off, not 0.6.** The cached raw transcript put
   "You'd" at 147.86; fresh transcription put it at 149.92 — the conform segment built
   from the cache pointed at PURE SILENCE and the words were simply missing (Dan's "weird
   problem with the sound at 1:21"). Word durations picked the right take: his cut's
   0.24/0.34 s matched take 3, not take 2's 0.60/0.60.
6. **NOTHING in his render ever sits still** — his title card measures 0/101 static
   frames. Full-bleed stills and title cards need the same slow push as card media; the
   watch scan's frozen-run check is the enforcement.
7. **Verify the FIRST FRAME of any asset cut near an app screen transition.** The
   after-reveal asset started 0.27 s before the app's transition finished and the card
   OPENED on the banned before/after — twice, at both product beats. The boundary strips
   caught it; the plan said the crop was safe.
8. **His in-card stock photos can be lifted from his own settled card frames** (~700–900
   px — enough for a card that downsizes media). Attempt 3's 0:48 fitness model IS his
   pixels. For 16:9 b-roll the trade stands: his exact clip cropped to 9:16 is a 2.7×
   upscale, so analogous vertical stock still wins — log each such swap as a known
   difference.

### [A3 rev 1] Dan's review of attempt 3: "the audio is the biggest difference" — and the answer

9. **WHEN THE CUT IS FRAME-LOCKED TO THE REFERENCE'S TIMELINE, USE THE REFERENCE'S OWN
   AUDIO.** The conform voice is a lip-sync proxy, not a deliverable: every EDL
   imprecision becomes a clipped word or an awkward splice in it, and no amount of EDL
   polish reaches a hand-cut mix. The reference's own audio drops under the rebuilt
   picture verbatim (one CONSTANT gain + limiter to ad spec — never `loudnorm`, see Step 4)
   — which erases the whole class of
   conform-audio artifacts AND settles the music-bed question (the bed is his). Before
   muxing, xcorr every EDL segment's conform voice against his audio in its cut window
   (band 300–3400, per-segment windows — whole-file windows straddle offset changes and
   refuse to lock): shift segments over 40 ms (src_in −= lag), and treat a segment whose
   lag DRIFTS as a WRONG-TAKE segment — same words at a different pace can never be
   shifted into sync (fresh-Whisper word durations identify his take: 0.50/0.36/0.34 s
   vs 0.34/0.26/0.28 s for "every single day"). Attempt 3 had one different-take stretch
   and 7 shifted segments; after correction every segment locks within ±10 ms.
10. **`alimiter` defaults to `level=1`, which BOOSTS the whole mix up to the ceiling** —
   always `level=disabled` for peak-shaving. And AAC overshoots the wav's true peak by
   ~0.5–0.7 dB, so a −1.4 dBTP wav can fail a −1.0 gate after encode; limit the wav to
   ~−2 dBTP first.
11. **The subject LEANS through a locked-off shot, and a 608-px-wide 9:16 crop amplifies
   it** (±60 px lean = ±110 px on the phone). A fixed crop centred on the measured mean
   reads off-centre at the extremes — Dan caught it at one timestamp and it was a class.
   Fix: a smoothed face track (skin-band centroid per 0.25 s, median filter, slope-limit
   80 px/s) driving a piecewise-linear `crop x` expression — a gentle auto-reframe. Skin
   centroids get fooled by raised HANDS: restrict the band to face height (y 70–240).
12. **App-recording beats: retime VARIABLY, not uniformly** — interactions near real
   time, progress/loading screens ~5× (Dan: uniform speed makes the loading feel slow).

## [A4] Ad 2 (2026-09-01) — Dan rejected rev 0 on CENTERING, and the cause was already written down

His verdict was that the audio "sounds like Muhammad", the graphics were wrong, and **"the most
severe issue is the centering throughout the entire video"**. Ten lessons:

0aa. ⚠⚠ **COUNT THE VIDEO STREAM'S FRAMES AGAINST THE PLAN. THE CONTAINER'S DURATION LIES.**
   A stale, INDEX-KEYED plate in `gfx/p{i}.mov` was reused after a beat's duration changed,
   and because a card is muxed with `shortest=1` a plate 10 frames short **TRUNCATED the
   beat**. The master shipped 8,265 frames against a plan of 8,275: the picture ran 334 ms
   ahead of the audio for the last 85 seconds, and every flash after the hole fired 8 frames
   into the following sentence. **Every duration check passed**, because `format=duration`
   reports the longer of the two streams — so a truncated PICTURE reads back as full length.
   Probe `-select_streams v -count_frames` and assert the count equals `round(DUR*fps)`.
   **Content-address the plate cache exactly like the segment cache** (hash of beat spec +
   duration + frame count); an existence check on an index-keyed name is not a cache.
0ab. ⚠ **A CROSS-DISSOLVE SCORES WELL ON EVERY FRAME-DIFFERENCE METRIC WHILE LOOKING LIKE TWO
   FACES.** A ghost is a SMOOTH blend, so it lowers frame-to-frame difference — which is what
   those metrics reward. Three separate metrics of mine rated six ghosting dissolves as
   successes; frame-by-frame inspection called them "unmistakable double exposures, worse
   than the hard cut they replaced". **A dissolve is only safe when the two sides are nearly
   registered — under about 25 px of head displacement at 1080 — and the only way to confirm
   it is to look.** Where it ghosts, leave his hard cut alone rather than substituting a
   worse artifact.
0ac. ⚠ **SMOOTH THE TRACK INSIDE EACH SOURCE-CONTINUOUS SEGMENT, ZERO-PHASE, AND LET THE CROP
   STEP AT THE SPLICE.** One causal filter across the whole video has not caught up when the
   outgoing frame is the last of its take: measured on 11 of 37 splices the outgoing frame was
   already **54-104 px off centre**, so the tracker's own lag was ADDED to his real pose change
   and made his cuts read bigger than they are. Smooth per segment with a forward-and-backward
   pass, and force a breakpoint pair either side of each splice so the step renders as a step.
   ⚠ And clamp the track lookup INSIDE the sample's own segment: at 4 samples/s a plain
   `round()` one frame before a splice lands on the sample AFTER it, so the pre-step breakpoint
   picks up the post-step value and a step becomes a 187 px ramp.

0. ⚠⚠ **MEASURE CENTERING ON THE DELIVERED FILE. NOTHING UPSTREAM CAN SEE A BAD FILTER
   EXPRESSION.** Two versions were rejected for centering and only the second rejection found the
   real cause, which was neither the tracker nor the beat sheet but the ffmpeg crop expression
   itself. `crop_x_expr` builds a piecewise `if(lt(t,..),..)` chain; assembled by wrapping each
   interval around the previous result **in forward order**, the LAST interval becomes the
   OUTERMOST test, so every frame before the final interval evaluates **the last interval's line
   equation extrapolated backwards across the whole beat**. On a 12 s beat that put the crop 178 px
   too far right in source = **316 px left in the delivered frame**, for twelve seconds. Wrap the
   chain in REVERSE, keep breakpoints at 0.5 s, clamp the output, and **write a self-test that
   evaluates the expression the way ffmpeg does and diffs it against the track**. Then add a gate
   check that masks the FINISHED frames and fails on median > 25 px, >10 % of talking frames beyond
   70 px, or any run beyond 60 px lasting a second. The A/B sheet, the track statistics and the
   beat sheet were all green while the delivered picture was wrong.
0b. ⚠ **SMOOTH THE TRACK FOR HOW FAST HE ACTUALLY MOVES, AND MEASURE THAT FIRST.** His torso runs
   at p90 128 px/s and p99 232 px/s in the source; a 2 s median plus an 80 px/s slope limit follows
   only the slowest 79 % of that and leaves sd 80-110 px. Simulate candidate settings against the
   RAW anchor series before rendering — it is free — and read off the trade against the crop's own
   pan rate. k=3 (~0.75 s) with a 200 px/s limit gave sd 30 px for a 95th-percentile pan of
   ~250 px/s, which inspected on consecutive frames reads as a gentle reframe rather than a swim.
1. ⚠ **NEVER ANCHOR THE CROP ON A COLOUR HEURISTIC. USE APPLE VISION PERSON SEGMENTATION.**
   This is the single most expensive mistake available in this skill, and the project had already
   paid for it once: the 2026-08-27 re-centre session recorded that a skin+dark-garment heuristic
   "bled into the stainless fridge" on this exact kitchen set. Rev 0 used one anyway; the warm wall
   and the fridge sit to his right, so the centroid was dragged **+123 px right in the 1920 source
   = +218 px in the delivered 1080 frame**, and Dan saw it immediately. The tooling already exists
   — `/shorts reference/recentre/personmask.swift` (compile once with `swiftc -O`) plus
   `anchor.py`, whose `torso` value is the midpoint of the TALL columns of the mask, so hands
   leaving frame cannot drag it. Verify with a nine-point A/B across the timeline with the frame
   centre drawn in, before rendering anything.
2. ⚠ **CONTENT-ADDRESS EVERY CACHE. AN INDEX-KEYED ONE SERVES THE WRONG FILE.** Removing two beats
   made the beat list shorter, every later beat shifted index, and the segment cache handed back
   the previous beat's file at the new index — the concat came out **293.6 s against a 276.1 s
   target**. The overlay cache had the identical bug on Ad 1. Key both on a hash of the beat spec
   + duration + start time.
3. ⚠ **READ HIS GRAPHICS TEXT AT HIGH ZOOM AND REPRODUCE IT VERBATIM.** Paraphrasing a header is
   not reproducing his cut. Four of five bullet cards were wrong in rev 0 — headers reworded,
   bullets merged, one split into two so the second began mid-sentence with a lowercase letter.
   Crop each card at 3x and read it.
4. **His bullets colour individual phrases olive, and a phrase can straddle a line break**, so the
   renderer needs per-CHARACTER colour carried through the wrap, not per-line colour.
5. ⚠ **THE HEADER MUST WRAP.** Two of his headers are long and he sets them on two lines. Drawn as
   one line they run off the right edge of a 1080-wide frame — invisible on a contact sheet,
   obvious at full width.
6. ⚠ **DO NOT INVENT GRAPHICS TEXT.** Dan: *"make sure your graphics are mirroring what Muhammad
   had in there and that you're not creating your own graphics text."* That killed six card
   captions I had written and two bullet cards I had invented to break up his long talking
   stretches. If his cards carry no caption, yours carry no caption — and a card caption over a
   burned caption is the "double captions" he flagged.
7. **Captions must be suppressed under CTA pills, not only under bullet screens.** Missing `cta`
   from the suppression list ran the captions straight through all three pills — "With Abs"
   overprinted by "to generate an image".
8. ⚠ **`loudnorm` FALLS BACK TO DYNAMIC MODE WITHOUT ERRORING** when the lift cannot be made
   linearly under the true-peak ceiling. His master was −19.2 LUFS with peaks already at −0.08
   dBTP, so −14 needs +6.4 dB: loudnorm compressed the bed up against the voice, measurable as a
   drop to 0.970 correlation with his mix. Use a **pure gain plus a limiter** and iterate the gain
   two or three times to land on target. Then judge provenance **per second, level-normalised** —
   a whole-file correlation can never reach 1.0 once a limiter is legitimately shaving peaks.
9. ⚠ **A BARE `apad` HAS NO LENGTH AND GENERATES SILENCE FOREVER** — the limiter-delay
   compensation never finishes encoding. Use `apad=pad_len=<the samples you trimmed>`. And
   **measure the limiter delay on ONE probe file processed two ways**: generating `anoisesrc`
   twice gives two different random signals and the correlation is meaningless (it read −1128
   samples; the real delay is 239).
10. **A full-bleed STILL must carry a slow push**, exactly as a still in a card does — the `bleed`
    branch needs `still_chain`, not a plain cover crop. Five stills sat dead-frozen in rev 0 while
    Dan's revision note asked for them "with motion effect" in as many words.

**Recovering the EDL when word runs are not enough:** his pause trims INSIDE a sentence are
invisible to run-detection, because the words either side still match contiguously. Build a dense
**acoustic offset profile** instead — step his cut in 0.10 s hops, lock each 0.70 s window against
the raw independently, and every step in the locked offset is one of his cuts, whether or not a
word went unmatched across it. On this ad that took fidelity from 97.1 % to **98.1 %**.

## [A5] Ad 2 against Muhammad's V2 (2026-09-03) — when the editor revises, DIFF, don't rebuild

Dan dropped Muhammad's `Daniel HQ Ad 2 V2 HD.mp4` (his own execution of Dan's six round-1 notes) into
`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/` beside where the Ad-1 vertical lives, and
invoked the skill with nothing but a screenshot. Twelve lessons, each paid for:

1. **A revised reference is a DIFF against the previous reference, not a new recovery.** Per-frame MAD of
   V2 against V1 at 96×54 grey (both 8,275 frames) found exactly five changed windows and identical audio
   except ~5 s of SFX. Everything else was the sheet Dan had reviewed three times, so only those windows were
   conformed to V2 — at the frame, read off V2 with a consecutive-frame scan (`refdiff.py` / `v2scan.py`
   pattern: MAD > 8 or luma > 150 lists every cut and every flash). The whole build was ~2 hours.
2. **The editor's execution of Dan's notes can itself break a standing rule.** His V2 puts the app's
   EMAIL-CAPTURE screen in the phone at 3:22–3:24 (and again on the 3:12 card, as V1 did). "The reference
   is the spec" never overrides "never show the email screen": the split layout was reproduced, the phone
   content was not — the compliant after-only result went in from his 202.0 s. Tell Dan; he tells Muhammad.
3. ⚠ **ffmpeg's expression parser refuses ~100 nesting levels** — `Missing ')' or too many args`. The
   0.25 s crop-x breakpoints added after rev 3 made a 25 s talk beat 100 nested `if()`s deep and the render
   died on beat 12 (that is why the post-delivery render in the old work dir failed). **Write piecewise-linear
   functions as a FLAT sum: `x0 + Σ slope·clip(t−ta,0,dt)`** — identical function, no nesting, verified past
   400 terms — and keep the self-test that evaluates the string the way ffmpeg does (`render.py selftest`).
4. ⚠ **`ffprobe -of csv` emits fields in ITS order, not the requested one** (`duration` before
   `nb_read_frames`), so the post-delivery check 3b parsed a duration as a frame count and had never run.
   Parse `-of json` by name. (Bit `mux.py` and `qc.py` the same day.)
5. **Scope a cache-version bump to the kind that changed.** A `_v` string covering every kind invalidated
   all 36 segments and started a 25-minute re-render for a one-beat change; and `pkill -f "python3 render.py"`
   does not match a Python.app-framework command line — kill by PID.
6. **His flashes are not only on insert→talk returns.** Measured on V2: one left mid-talk at 14.08 (the
   deleted cartoon's return flash, 0.4 s after the 13.70 splice — his V2 carries that splice bare), one on
   bullets→photo-card (149.85), one on app-card→b-roll (193.26), and NONE on the museum clip's exit (7.21).
   Make the list explicit (`NO_FLASH`, `EXTRA_FLASH`), never purely a rule. And his cut lands ON the peak:
   the envelope is now asymmetric — window 0.10 s before / 0.30 s after the cut, peak at 25 %.
7. **His blur-through between two stills is a plain dissolve under a gaussian blur.** `xfade=hblur` is a
   horizontal smear and reads as a different device; the right build is `xfade=dissolve` + `gblur` whose
   `sigma` is driven per frame through `sendcmd` (0 → 18 px → 0 over 12 frames, `bleed2` kind). Render each
   still with half the transition of headroom so the segment still totals exactly its planned frames.
8. **Stretch a short clip, never loop it.** A 4.5 s clip in a 4.9 s beat gets `setpts*1.15` (a MEDIA entry's
   optional 4th field), not `-stream_loop`, which wraps to frame 0 mid-rep.
9. ⚠ **`voice_chain.py --finish-only` had never run end to end** — `ss` was only defined on the full-chain
   path and the limiter-delay measurement crashed with NameError. Fixed in the module. The first real use of a
   shared code path is a test; run it before the render, not after.
10. ⚠ **The shared gate's tone/floor rows measure the EDITOR'S mixing on the reference-mix path.** They passed
    on Ad 1 only because the pinned reference IS Ad 1's mix; Ad 2's bed sits 6–7 dB hotter between words and
    failed them. `audio_gate.py --reference-mix his_mix.wav` verifies provenance per second (≥ 0.99 median,
    refused otherwise) and records those rows as information; loudness / TP / silence / length / L/R still
    gate, and the stamp carries `mode: reference-mix` plus the mix's sha256.
11. ⚠ **`gain_flatness.py`'s "min ≥ G − 2.5" failed a file Dan approved.** Ad 2 rev 2 ("sounds like
    Muhammad") rode 4.3 dB below its constant on the deepest second; his master is −19.0 LUFS already at
    0.0 dBTP, so ANY lift to −14 shaves the densest speech seconds by 3+ dB (+4.5 dB still reads 3.0).
    Recalibrated to 4.5 — the approved boundary. The rejected loudnorm file still fails on the ceiling test
    (133 seconds ABOVE G), which is the discriminator; the shaving limit was never what caught it.
    Use `--tp -1.4` on an editor's brickwalled master: the AAC overshoot measured 0.2 dB (−1.3 → −1.1 dBTP).
13. ⚠⚠ **HIS PICTURE CUTS ARE NOT HIS AUDIO SPLICES. RECOVER THEM SEPARATELY.** The independent audit
    found our talking head carrying 17 hard picture cuts where his has 5: the conform cut the picture at
    every AUDIO splice, but he cuts the picture on a pose-matched frame of his own choosing, 1–15 frames
    away from the sound cut (a J-/L-cut) — at 96.00 s his picture switches takes 8 frames before the
    audio does, at 114.75 s 15 frames before, at 32.90 s 6 frames after. Rev 3's note that those were "his
    own cuts" was wrong: his picture is continuous within ±3 frames of ours precisely because his cut is
    elsewhere. **Method (`piccuts.py`):** for each talk splice render BOTH takes from the raw at the grade
    over ±15–30 frames, fit each frame to his framing (scale/fy search as `cover.py`), high-pass NCC
    against his frame, and take the crossover frame; then conform the base to a PICTURE EDL
    (`edl_picture.json`, `build_base_pic.py`) whose segments start at his frames while the take alignment
    stays fixed by the audio. 22 of 33 resolved with confidence ≥ 0.6; the rest stayed on the audio splice.
    The crop track, the render's splice breakpoints and the watch pass's "known cuts" all read the picture
    EDL. A cross-dissolve was never the answer to a jump cut — his frame choice is.
14. ⚠ **A per-segment median window must SHRINK to zero at the segment ends.** Smoothed with a full
    window, the crop at a cut sat where he WOULD be half a second later (median over the future only):
    the audit measured him landing 78–190 px off after our cuts and the crop panning him back over up to
    1 s. `facetrack3.py`: `k_eff = min(k, j, n-1-j)` plus a forward/backward slope-limited blend weighted
    toward the pass that is exact at each end — landing error at every cut 0 px, exit error 0, and the
    crop follows at ≤ 200 px/s from there. Verify by printing raw-vs-track at the first and last sample of
    every segment; a mean statistic cannot see this.
15. **The segment cache key must include the MEDIA entry**, not just the beat spec: a crop offset changed
    in `assets.py` served the stale conveyor segment through a `--only` re-render because nothing in the
    key had changed. Same class as the index-keyed caches, one level down.
16. **Audit findings that were all real and all cheap:** a centred 9:16 window of a 16:9 clip slices
    whatever sits at the sides (the conveyor's "MEAL PLANS" read "ME / PLA": place the window with an `ox`
    per media); burned captions over a clip's own engraved text (put his caption band in as a lower third
    above it, chip above that); a 24p clip stretched by frame repetition judders (39 of 145 frames
    duplicated — `minterpolate=mi_mode=mci` after the `setpts`, 0 duplicates); a still whose subject
    touches the top edge loses its crown to a centred push (`oy=0` anchors the push at the top); a second
    subject jammed against the crop edge (`ox` shifts the window). And his lift: on a −19 LUFS master at
    0.0 dBTP the audit's arithmetic showed +5.0–5.2 dB reaches −14.7 with 21 fewer limited seconds than
    +5.8 — take the smaller lift.

12. **Delivery goes beside his file, in the Ad-1 folder's convention:** `Muhammad Ad Videos/<ad>/<ad> |
    claude | 9x16.mp4` + `REVIEW_540p_9x16.mp4` + `AB_audio_his-vs-ours.mp4` + the gate stamp + notes +
    `recipe-vertical-v2/`. The older `EDITED ADS 8-20-26/ad2-fire-your-nutritionist/` folder keeps rev 3.

## Standing content rules that override the reference

The reference editor does not know Dan's ad rules. Check every beat you are reproducing:

- **NO side-by-side before/after, ever, in a paid ad.** Muhammad's 0:03 card is exactly
  that (heavier Dan left, goal phone right, arrow between). **Cut it sequentially instead** —
  the before photo, then the goal phone.
- **NEVER show the email-capture screen**, and never the app's "Meet the new you"
  before/after screen. In the product recording `clip_109_replacement.mp4` those start at
  **26 s and 29 s** — the usable window is **0–25 s**. Assert it in QC.
- **Label AI-generated imagery — and NEVER put the label over a face** (Dan, 2026-08-27:
  "don't cover my face with labels like this. Make that a rule for future ones"). On a
  full-bleed person shot the chip goes low — at the shorts/waistline area, above the
  caption band — sized large enough to read (~68% of frame width on 1080).
- **Casting: white or Asian men 30–50.** Contact-sheet the RENDERED 9:16 crop of every stock
  clip before committing — 4 of the first 10 picks here were off-demographic and one was a
  woman, and none of that is visible from a search-page thumbnail.
- No drug names in graphics.

---

## Traps that cost time here — read before building

1. **Cumulative frame counts, not per-segment rounding.** Rounding each segment's duration
   on its own put ~16 ms of overshoot into every one of 73 cuts and the conform finished
   **1.17 s long**. Compute `round(cut_out × fps)` cumulatively and take differences.
2. **`-vsync 0` and `-r` are contradictory** and ffmpeg errors out. Use `-r` + `-frames:v N`.
3. **`blend=all_mode=multiply` must run in RGB.** On yuv420p it multiplies the chroma planes
   about their 128 offset as if they were luma and **turns every footage frame bright green**.
   `[a]format=gbrp[x];[b]format=gbrp[y];[x][y]blend=...,format=yuv420p`.
4. **A still used as a filter input needs `-loop 1 -framerate`.** Without it the image is one
   frame and `shortest=1` truncates the whole segment to a single frame — which is exactly
   how 29 footage segments silently became stills.
5. **A filtergraph label can be consumed once.** Feeding the voice to both `sidechaincompress`
   and `amix` needs `asplit=2`.
6. **Phrase anchors need `after=`** whenever a phrase repeats ("tap the button below",
   "stressful life", "lose your belly fat"). Without it the anchor matches the first
   occurrence and the beat gets a negative duration.
7. **Pexels needs no key**: `https://www.pexels.com/download/video/<ID>/` curls straight to the
   CDN. Search pages are Cloudflare-gated, but a page loaded in the in-app browser can
   `fetch('/search/videos/<term>/')` same-origin. Prefer results that come back ≥1440 tall.
8. **Probe every downloaded clip's dimensions.** 8 of 10 came back 2160×4096 — those are a
   downscale to 1080×1920 and look far better than anything cropped from 16:9.

### [A2] Six more, every one of which passed the metric gate

9. **An overlay must be SHIFTED onto the main timeline, not just gated onto it.**
   `overlay=...:enable='between(t,a,b)'` gates by the MAIN clock while overlay keeps
   consuming the secondary stream from ITS own t=0 — so by the time the window opens the
   overlay has run out, `repeatlast` pins its last (transparent) frame, and **nothing ever
   appears**. Seven lower thirds, three CTA pills and eleven flashes were all missing from
   a render that passed every check. Fix: `[N:v]setpts=PTS+{t0}/TB[s]` before the overlay.
10. **`setpts=PTS-STARTPTS` on every seeked input that feeds an overlay.** A seeked
   stream's first frame carries a pts above zero, so overlay's frame 0 composites only the
   black background and the segment **opens on one black frame**. It cost six of them, in
   two separate places (the talking head in a window, and video inside a card hole).
11. **Per-character text must be drawn on the BASELINE (`anchor="ls"`), never `"lt"`.**
   PIL's "t" anchor is the ascender line *of the string it is given*, so drawing one glyph
   at a time aligns each by its own top: periods ride up to cap height, commas become
   apostrophes, every ascender-less letter drops. All-caps headlines look fine, which is
   how it survives review — the first full-res frame had "moțivation … sįx-pack abs·"
   burned into the bullets. Draw at `y + font.getmetrics()[0]`.
12. **The vignette fitted on TALKING-HEAD frames must not be applied at full strength to
   anything else.** That fit is his render ÷ our toned conform on frames whose background
   already falls off, so it double-darkens footage. Measured on his own b-roll the corner
   sits at **0.95 of centre** — he barely vignettes footage at all. Ours turned the beach
   and salad shots into portholes. Keep the full profile for the talking head; blend it to
   ~25 % for full-bleed b-roll; none on plated graphics.
13. **A still in a card must not sit dead-frozen** — his photo cards all carry a slow push
   (measured on his 0:48 card, which grows over its 2.5 s). And **a retimed insert needs
   headroom**: cut to the exact beat length it comes out one frame short and
   `-stream_loop` wraps that last frame back to the clip's first, which on a screen
   recording is a visible content jump.
14. **Whisper's mistakes get BURNED INTO the captions.** This roll produced "six back abs",
   "a gold picture" and "WuWu stuff" — three spelling mistakes in a finished ad. Keep an
   explicit correction map in `captions.py`, and break caption groups at full stops or
   you get "life. You're more" as one card.
