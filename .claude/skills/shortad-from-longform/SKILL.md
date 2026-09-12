---
name: shortad-from-longform
description: Rebuild a FINISHED, finalized long-form video as a vertical 9:16 short ad, reproducing the finished video's style as closely as possible — first verify the editor's HD export is the draft Dan approved with no new errors (so Dan never has to watch the export), then recover its edit from the raw footage, measure its grade, palette and graphics, re-lay them out for a phone, then cut a ≤0:59 version. Use whenever Dan asks for a vertical or 9:16 version of a finished video, to "make a short ad from" a long-form cut, to reproduce an editor's finished style in vertical, or to turn a finalized ad or content video into Shorts/Reels creative — even if he doesn't say "/shortad-from-longform". For cutting shorts out of a video we ourselves rendered, /shorts is cheaper. For editing an ad from raw shoot footage use /ad-edit; for content videos use /longform-edit.
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

> ## ⚠⚠⚠ THE EDITOR'S AUDIO, UNTOUCHED. NO GAIN, NO LIMITER, NO MONO SUM, NO LOUDNESS TARGET.
> **(Dan, 2026-09-10, on the Zeeshan Ad 1 vertical: "What the fuck happened to the audio? Zishan's audio
> sounds much better. This is an awful mistake which can't happen again. … Use Zishan's audio.")**
> That build lifted his −23.5 LUFS mix +9.9 dB into a 4×-oversampled limiter, summed it to mono and
> re-encoded it, to pass OUR rows (−14 LUFS, L/R ≥ 0.98) — rows Zeeshan's own mix fails. Every check it
> faced was level-normalised or target-based, so it passed 20/20 while the loudness range fell 5.9 → 4.1 LU.
>
> **The method now, for every vertical or cutdown rebuilt from an editor's finished cut:**
> * **Full length: COPY his audio stream** from his export into the rebuilt picture (`-map 1:a -c:a copy`);
>   `a6/zmux.py` asserts the audio stream's md5 equals his, bit for bit.
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
> Everything below in this box is the HISTORY of how we got it wrong: the gain + limiter method was never
> confirmed by Dan (the 09-02 rebuild sat at "Dan listens"), Ad 2's approval covered its picture, and on a
> quieter master the same method did the damage Dan heard. Do not revive it.
>
> ## [SUPERSEDED 2026-09-10 — history] THE AUDIO IS THE REFERENCE'S OWN MIX
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
> silence and length, and writes the stamp `qc.py` check 18 requires. Under the hood it is:
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

14. **⚠ THE FRAMING STANDARD IS LOCKED (Dan, 2026-09-08) AND THE DELIVERED FILE IS GATED ON IT
   (2026-09-12).** Framing is 4 of Dan's 11 recorded rejections, and until 2026-09-12 this skill —
   which re-crops Dan into vertical for every ad — had no framing rule at all. The standard, which
   cost the website video four revisions and is not open for renegotiation (memory
   `framing-standard-hair-anchored`):
   * **every talking-head crop is anchored to the MEASURED TOP OF HIS HAIR** — never to the frame
     edge, never to a skin/hairline detector (rev 3's hairline detector read 90 px inside his hair
     and cut it in 23 of 26 holds: *"basically not usable"*);
   * **per hold, that hold's tallest hair instant sits ~4 % of the crop height below the top edge**
     (~43 px at 1080p, ~77 px in a 1080×1920 vertical). Delivered: hair ≥ 20 px from the edge on
     every frame, per-hold minimum 30–70 px, median ≤ 75 px, all ×(H/1080);
   * **two levels only** — NEAR (hair → belly button) and FAR (hair → shorts line, waistband in
     frame). **No wide level exists**, and no knees in a talking shot;
   * **the head band sits on the vertical centre line** (rule 5 and rule 11 say how: a smoothed
     face track, never one fixed x). Dan caught `v2-short3` 133 px off: *"one of my arms is cut
     off and there's space on the other side"*;
   * **a push schedule, never one fixed crop** (rule 8).
   The delivery gate's `framing:` rows (`_shared/deliver/checks/framing.py`) measure all five off
   the DELIVERED pixels with mediapipe FaceMesh + Apple Vision person segmentation — no plan, no
   set-specific background — and `<file>.framing_proof.jpg` is the native-scale proof sheet. Look
   at it: the green line must sit on the top of his hair on the tightest tiles.

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
                   then _shared/audio/audio_gate.py on the delivered .mp4 (the stamp qc.py check 18 needs)
a2/align_ctc.py    FORCE-ALIGN the caption words to the mix (Whisper timings are ~130 ms early)
captions.py        word-timed from words_ctc.json, suppressed under text graphics, typo correction map
caption_sync_check.py  THE SUBTITLE GATE on the delivered file (qc check 20)
a2/watch.py        THE GATE: per-frame scan + a consecutive-frame strip at every boundary
qc.py              20 checks (generic; per-cut numbers in qc.json). Check 15 = the watch pass
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

⚠ The older per-video QC script in `reference/` still runs and still has rows this gate has not
absorbed yet (the watch pass is Phase 3 of `Handoffs/handoff-20260911-video-quality-engine.md`;
**framing landed in the shared gate 2026-09-12** — the five `framing:` rows, Step 5 rule 14).
**Run both until Phase 3 lands.**

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

Only then run `reference/qc.py <delivered.mp4> --build-dir <build>`, which is **20 checks**.

> **⚠ THIS FILE NOW EXISTS (2026-09-09).** Until Phase 0 of the video-quality programme, this SKILL.md
> referenced `reference/qc.py` five times and described its check list — and **the file was not there.**
> The only gate on disk was `qc_ad2v2.py`, a per-ad fork with `TARGET = 276.109167` and
> `V = 'ad2v2_vertical_9x16.mp4'` compiled in, unusable on any other cut. A SKILL.md that asserts a
> check nothing performs is worse than no check: it reads as covered. `qc.py` is the generic gate;
> per-cut numbers go in a `qc.json` beside the build (see its docstring), and **a check whose input is
> missing is NOT MEASURED, which FAILS** — declare a genuine non-applicability in `qc.json`'s `skip`,
> with the reason, where a reader can audit it. `qc_ad2v2.py` stays as the reproducible Ad-2 record.

The checks (16 = audio integrity, 18 = the `_shared/audio` gate stamp on this exact file):

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
file is silent** (per-second RMS scan; run it on review copies too) · **20 captions synchronised — on the DELIVERED file, at the instant each word is spoken, the word lit is that word (≥ 97 %, no run of three misses) and no highlighted word sits outside speech (`caption_sync_check.py`; Dan, 2026-09-08)** · **17 the audio is
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

17. **Snap every raw seek to the frame grid.** `-ss <arbitrary fraction> -i RAW` plus a cfr output rate
    duplicates the FIRST frame of a segment whenever the seek phase is past half a frame — the re-audit
    counted a duplicated frame right after 9 of 29 cuts (4 of 29 in the earlier base): a 33 ms hold on the
    incoming frame, invisible, but a defect class. `src = round(src_in*FPS)/FPS + 0.0002` in the conform
    (`build_base_pic.py`) lands every seek on a frame. Shipped on Ad 2 V2 unfixed, deliberately: the
    re-render cost an hour for nothing a viewer could see.

18. ⚠⚠ **`fps=4` SAMPLING IS ~0.2 s LATE. THE CROP TRACK MUST LIVE ON FRAME INDICES.** The re-audit
    measured a 726 px/s whip just before the 21.05 s cut "while he is static": the 4 fps torso sample
    labelled 21.00 s had been taken from a frame AFTER the cut, so the track switched to the incoming pose
    two frames early and the crop left him before the cut. Sample with `select='eq(n,…)+…'` at exact
    indices (every 7th frame PLUS the last frame before and the first frame of every picture segment),
    store `n` with `x` (`measure_torso2.py`, `facetrack4.py`), and interpolate in frame time inside the
    segment only (`render.py _x_at`). Result: landing error 0 px at both sides of every cut, and the
    self-test still proves the expression. Cap the slope at 170 px/s source (~300 on the phone).
19. **Ask the auditor to re-audit, and expect a "does not ship".** The first re-audit of the picture-cut
    rebuild found two narrow mechanical faults (duplicated first frames at 11 cuts, the whip above) that
    every gate had passed and that I had declared fixed. Its scripts (`audit_v3/p1_landing3.py`,
    `p1_pananalyse3.py`) are reusable; `landing_check.py` is the builder-side version now run before
    delivery: torso at n0−1 / n0 / n0+2 on the DELIVERED file for every cut, and `diff(n0→n0+1) ≥ 0.5`.

20. **A step breakpoint goes HALF A FRAME before the cut, with explicit values.** A pair at
    (c − 1/FPS, c) is written into the expression with 4 decimals, which can land it a hair AFTER the
    cut frame — so the cut frame itself still evaluated to the outgoing crop: one mis-framed frame at
    every cut (−86 px on the phone at 84.48 s, found only by `landing_check.py` on the delivered file).
    Pair = (c − 0.5/FPS − 2 ms → x(n0−1), c − 0.5/FPS + 2 ms → x(n0)), and the self-test now evaluates
    every cut frame and the frame before it against the track. **And `setpts=N/FR/TB` in the conform** —
    snapping the seek alone did not stop the duplicated first frame (the roll's pts are not on k/FPS);
    rewriting the timestamps did (0 duplicates at 32 cuts, from 10).

21. ⚠⚠ **WHISPER'S WORD TIMESTAMPS ARE NOT CAPTION TIMINGS. FORCE-ALIGN, THEN GATE THE DELIVERED FILE.**
    Dan, 2026-09-08, on the V2 vertical: *"the subtitles are not matching what's said … the highlighted
    word … very confusing and makes the ad look unprofessional"* — the most serious note on an otherwise
    approved build. Measured: Whisper `small`'s word starts on his mix (voice + bed) run **128 ms early on
    average, sd 152, p90 +295 ms; 289 of 875 words more than 150 ms off** against a CTC forced alignment
    (`align_ctc.py`: torchaudio `WAV2VEC2_ASR_BASE_960H` + `forced_align`, per Whisper segment with 0.6 s
    padding, the same words with the FIX map applied, digits spelled out). The karaoke highlight then lit
    the wrong word. Whisper is the source of the WORDS only; `captions.py` reads `words_ctc.json`.
    **The gate (`caption_sync_check.py`, qc check 20) measures the DELIVERED file end to end:** the olive
    highlighted word is tracked per frame in the caption band, every on-screen onset is matched to the
    aligned word start (PASS: p95 ≤ 120 ms, max ≤ 250 ms), and any word lit while the speech band is
    within 6 dB of the floor fails the build. The rejected file read p95 190 / max 339 ms with 35 words
    lit during silence. Also print the disagreement against a second transcription (Whisper `medium`) —
    if the two Whispers agree with each other and not with the alignment, the alignment is wrong, not them.
22. **Dan's 2026-09-08 picture notes, for the next build's defaults:** a before photo's stomach must stay in
    frame (`oy` toward the bottom, gentler push), a multi-person photo is centred on Dan (`ox`), an "after"
    beat wants THREE different shots (0.8 s each) rather than one, an app card that starts from an upload
    must reach the FINALISED after picture before it ends, a repeated app clip gets a DIFFERENT person's
    before/after (asset library `01 Before and After Images/male2-*`, composited into the app's scanning
    box: `build_scan_male2.py`), and a meal-tracker card ends on the calories broken down AND logged —
    recorded from the real app with Playwright (`record_meal.py`: iPhone emulation, `set_input_files`,
    `showMacroScreen()`, screenshots per state; `logMeal` works for guests via localStorage).

23. ⚠ **AN APP SCREEN WITH A DIFFERENT PERSON IS A REAL GENERATION, NEVER A COMPOSITE.** Dan rejected a
    before photo pasted into the old scanning recording within minutes ("just overlaid … make it look like a
    real generation"). `record_gen_male2.py` runs the live site's generate flow with the other person's photo
    under Playwright (iPhone emulation), records the app's own loader with a CDP screencast (`Page.startScreencast`,
    ~54 fps but CSS pixels — 390 px wide; upscale ×2 with lanczos, the dpr-3 screenshots carry the static
    screens), handles the app's "Which future you?" chooser (click the first "Keep this one"), and captures
    the result screen AFTER-ONLY by hiding the before column and the body-fat row in the live DOM
    (`grid-template-columns:1fr`, `display:none`) so the compliant screen is the app's own rendering. One real
    generation costs ~$0.10 and a fresh Playwright context has free generations. Never use the chooser or the
    pair result in an ad (both are before/after layouts).
24. **The plate cache key must include the media's ASPECT.** A new phone media at the same path with a
    different shape reused the old plate: the hole was the old aspect, the media was cover-cropped into it,
    and 40 px of UI vanished at each side — the third cache-key lesson in this skill (index, media spec,
    now aspect). If a hole is sized from a file, hash what sizes it.

12. **Delivery goes beside his file under the `/editor-deliveries` convention — `title | editor | aspect |
    number`, lowercase, single-spaced pipes:** `Muhammad Ad Videos/<ad folder>/<title> | claude | 9x16 | ad N.mp4`
    + `<title> | REVIEW 540p 9x16 | ad N.mp4` + `<title> | REVIEW 480p 9x16 phone | ad N.mp4` + `<title> | AB audio
    his-vs-ours | ad N.mp4` + the gate stamp beside the master + `notes-vertical-v2.md` + `recipe-vertical-v2/`.
    (The un-suffixed `… | claude | 9x16.mp4` name the first delivery used was renamed by that skill on 2026-09-03;
    a second delivery under the old name made a duplicate master — `deliver.py` now writes the convention.)

## [A6] Zeeshan's Ad 1 (2026-09-10) — a 24 fps editor, a quiet dynamic mix, and a compositor

Build dir `/Volumes/Extreme/_edit_work/ad1-zee-vert/` (recipe beside the master in `Zeeshan Ad Videos/this picture got
me abs - ad 1/recipe-vertical/`). Thirteen lessons, every one measured on this build:

1. **Probe the reference's frame rate; never assume 29.97.** Zeeshan cut the 29.97 roll on a **24 fps** timeline, so
   the vertical is 24 fps and frame n is his frame n (5,980 frames). `caption_sync_check.py` had `FPS = 30000/1001`
   compiled in and pulls frames BY INDEX -- on a 24 fps master it would have sampled the caption band 25 % late by the
   end. It now probes the delivered file (corpus re-run: PASS).
2. **Picture EDL, frame-exact, from two instruments reconciled.** Per-frame matching of his frames against the raw
   (256x144 gray caches, his fitted framing via `warpAffine`, NCC over head+torso) finds his talking-head frames
   exactly (3,571 at r >= 0.90) but its raw index JITTERS +-0.2 s in low-motion stretches (the mouth is a few pixels).
   So every segment's **offset comes from the dense acoustic profile** (r 0.99, +-1 ms) and only the **cut frame from the
   picture crossover** at each audio join (`zedl.py`). Result: 23 picture segments, every picture cut within +-4 frames
   of its audio join (his J/L cuts).
3. **Talk ranges need bridging AND trimming.** A one-frame flash or a zoom-ramp frame falls under any match threshold,
   so gaps <= 12 frames inside talk are bridged -- which then lets a range run one frame past his hard cut into an
   insert, so every segment is trimmed at his talk->insert cut frames (`zedl3.py`). ⚠ **A flash frame belongs to the
   shot whose picture it is**: extending the incoming segment back onto a flash that was the OUTGOING shot's last frame
   overlapped two segments and made the conform 5,981 frames.
4. **When his talking head is the raw at framing 1.0, fit his grade as a 3D LUT from pixel correspondences** (`zlut.py`:
   33^3 bins, median of his RGB per raw-RGB bin, overlays rejected by the median). Per-channel curves could not fit him:
   the centre-box fit left the fridge 21 levels too red, the wide fit put skin 9 off. The LUT: skin / tank / door within
   2-4 levels; a residual ~5 % less red on his fridge highlights is spatial and was accepted. Measure his vignette first:
   his was flat (0.96-1.03), which is what made a whole-frame fit legitimate.
5. **Tag every intermediate BT.709 and give fillers the same tags.** A graded conform with no colour tags, stream-copy
   concatenated with untagged black fillers, is two different H.264 parameter sets in one file. Set the matrices
   explicitly (`scale=in_color_matrix=bt709` / `out_color_matrix=bt709`) and tag every segment identically.
6. ⚠ **[REJECTED BY DAN 2026-09-10 -- Step 4 and lesson 26; kept as history, do not repeat] A quiet, dynamic
   reference mix needs a true-peak limiter.** His master: -23.5 LUFS, -1.7 dBTP, LRA 5.9 -- +9.9 dB
   of constant gain. The 48 kHz limiter held the samples at -1.4 and the true peak still read -0.3 dBTP; **new opt-in
   `voice_chain.py --oversample 4`** runs the limiter at 192 kHz. And the AAC encode matters: 192k/256k overshot to
   -0.8/-0.7, **320k landed -1.2 dBTP** -- the masters are muxed at 320k (`zmux.py`). The window is narrow: loudness
   >= -14.8 (qc 4) against a deepest shave <= 4.5 dB (gain_flatness); `--target -14.4` landed -14.7 with a 4.29 dB shave
   (cutdown: +9.7 dB, 2.70 dB). **LRA measured on the delivered files: 5.9 -> 4.1 LU (the cutdown's windows 4.9 -> 3.7)**
   -- a 1.8 LU loss, past the ~0.8 LU rule of thumb in Step 4. That is a FINDING, reported to Dan with the A/B, not
   excused: there is no smaller lift inside the gate, and the result still reads more dynamic than the pinned approved
   reference (LRA 3.5; speech spread 8.0 dB vs 8.2). If Dan hears it as squashed, the fix is his call on the -14 target
   for quiet masters, never a looser gate.
7. **Translate his card language by its logic, not its look.** In 16:9 he cards the media that does not fill his frame
   (portrait photos). In 9:16 the landscape clips are the ones that do not, so they go in HIS black-bordered card on
   HIS field (1280x720 -> 1000 wide: a sharp DOWNSCALE, never the 2.7x crop), while portrait and high-res media fill the
   frame. The mirror of his rule reads as his style and costs no resolution.
8. **Lift from his render what our library does not have -- and inspect the crop edge at full resolution.** His
   phone-on-marble, hand-holding-phone and anatomy clips are not in the asset library; lifted from his 4K render with the
   window clear of his burned label and CTA bar. The first hand-phone crop still carried the TOPS of his "AI" glyphs in
   its bottom-right corner, invisible on a contact sheet. His SECOND phone beat is the first beat's 111 frames played
   1:1 then held (r = 1.000 frame for frame) with his CTA bar burned in -- reuse the first instance, never the second.
9. **A Python frame compositor instead of an ffmpeg filter graph** (`zrender.py`). Per-frame crop straight from
   `crop.json`, overlays composited on their measured frames, captions from the SAME caption states the sync gate reads,
   his flashes as a screen blend on their exact frames, frame count asserted. Every trap in [A2]-[A5] that came from
   expressing per-frame state as filter expressions (crop-expression order, overlays gated not shifted, index-keyed plate
   caches, truncated plates) cannot occur. ~13 fps at 1080x1920; a `--stills` mode renders chosen frames for review first.
10. **The hair standard on a roll with no headroom.** This 8/14 roll puts his hair 19-45 px below its OWN top edge, so
    `y0 = hold min hair top - 4 % of the crop height` clamps to the source top in most holds and the phone shows 44-77 px
    of headroom. The delivered-frame gate (`zhairgate.py`, the website gate's two tests rebuilt for this geometry and
    scaled x1920/1080) declares holds at y0 = 0 as source-limited -- auditable -- while the hair floor still gates every
    frame. Measure the hair top RELATIVE to what is above it: a fixed luma threshold climbed to y = 0 on the dim wall.
11. **Cutdown edges only ever move AWAY from the words.** Snapping a start forward onto the pool card cut "You're"; now
    the picture keeps the card and the AUDIO LEADS it by 5 frames (a J-cut, taken from the previous range's silent tail,
    so the total stays exact). Ends snap to his PICTURE cuts as well as beat edges (one frame past a picture cut leaks a
    one-frame shot). A seam with talk on both sides flips FAR<->NEAR **only when both sides would otherwise be the same
    level** (lesson 21). His mix had no bed (30-120 Hz +4.9 dB in the gaps; a bed reads ~+12), so the cutdown cuts HIS
    mix at the same windows with 4 ms raised-cosine joins.
12. **Process traps, again.** `pkill -f "python3 zbase.py"` did not match the framework Python, two conforms raced and
    wrote a 5,981-frame base -- kill by PID. Never name a module after the stdlib: a local `zlib.py` broke PIL's import of
    `zlib` in every script in the directory. A code statement pasted after a `#` comment silently dropped the AI label.
13. **His email-capture screen (188.75-190.33) became the app's AFTER IMAGE ALONE in his black-bordered card, under his
    "Final Result AI" label -- with an AI label on the result image**, which his had not: the standing rule is ours. The
    first build cropped the screen above the form and it still read as that screen (lesson 19c).
14. ⚠ **A caption's held last word must stop at the next muted graphic and at every cutdown seam.** The "hold the last
    word up to 0.8 s" rule (lesson A5.21) had no other stop, so on this master **10 caption lines ran 0.23-0.91 s into
    graphics that mute them** -- "the game." sat on the app screen, "can generate" on the title card, "In" under the
    checklist header -- and in the cutdown the last line of each range rode across the seam. Only the consecutive-frame
    strips showed it; `caption_sync_check.py` samples each word at its own time and cannot. `captions.py` now clips every
    hold at the next mute start and the next `beats.SEAMS`.
15. **A cutdown must drop a text overlay whose START lies in dropped material.** His 1:35 lower third outlives its
    sentence by 1.2 s, so the range that began there printed "If You Saw Yourself With Abs, You'd Be MOTIVATED" over
    "And right now you can generate…". Only overlays that start inside a range survive (the persistent CTA bar is the
    exception).
16. ⚠ **[REJECTED BY DAN 2026-09-10 -- lesson 26; kept as history: gate his image against HIS, never sum it]
    An editor's mix that sits ON the L/R line fails the shared gate after AAC -- sum it to centre, never relax the
    row.** His mix read L/R +0.970 against the gate's +0.97 and the AAC encode took ours to +0.968. It was not the
    two-mic fault (both channels carry the lav at the same instant, 0.92 each, lag 0.04 ms, equal level) -- a faint
    stereo difference. **New opt-in `voice_chain.py --mono-sum`** (finish-only) sums to centred mono before the constant
    gain: L/R +1.000, provenance 0.9989, and the dropped side sits ~18 dB under the voice. Corpus re-run: PASS.
17. ⚠ **A green highlight over green-toned footage is unreadable to the eye AND to the sync gate -- fix the picture,
    not the gate.** The cutdown failed check 20 at 96.0 % (97 needed) and three of its four misses were words burned
    correctly but invisible to the detector: over his phone-on-marble clip the goal photo's pool deck and neon shorts put
    6,400-7,500 green pixels in the caption band, 3,600-4,300 of them within 40 levels of the lime highlight. The
    tempting fix -- teach the gate the build's exact highlight colour -- was **measured and ruled out before any edit**:
    no tolerance separates the word from that background. The real fix is a legibility one: a soft dark gradient behind
    the caption band on those beats (`scrim=True`, 0 -> 0.65 over y 1200-1370), which puts the background under both the
    eye's and the detector's threshold while the lit word stays full colour. The fourth miss was genuine 24 fps
    quantisation (a 40 ms "it" spans less than one frame) and stays inside the 97 % allowance.
18. **Run `qc.py` from INSIDE the build directory, and make generated build modules resolve files next to themselves.**
    Run from the parent, the cutdown's generated `beats.py` opened `cut_timeline.json` against the caller's cwd and
    failed to import (3b, 9, 12 NOT MEASURED) -- and `centering.py`'s `sys.path.insert(0, '.')` then imported the
    MASTER's beat sheet, so check 17 "passed" the cutdown against the master's timeline. A green row that measured the
    wrong file is worse than a red one; `zcut_build.py` now writes paths relative to `__file__`.
19. ⚠ **An independent audit found four defects that had passed `qc.py` 20/20, the watch pass and every gate -- the
    first delivery was withdrawn before Dan saw it.** Each was mechanical; each is now a rule:
    (a) **an overlay cache settles on its LAST element.** `overlay_img()` froze the problem lower third 0.45 s in; its
    subtitle draws on at 1.83 s, so "No Time, No Motivation." showed for 3 frames of 4.96 s. No watch boundary fell
    inside the lower third, so **every overlay's sub-element in-times (subtitles, checklist items, an end card's second
    line) are watch boundaries now** (`a6/watch_zee_ad1.py`). ⚠ Gap: the cutdown's generated `beats.py` carries only frame
    numbers (`m0/m1`), not the master's spec fields, so its end card's second line is not a boundary there -- this build
    confirmed it from the frozen-run split instead (53.92 s = 51.875 + 49/24). Carry the spec into `cut_timeline.json`
    next time; (b) **label by the asset index, not by eye** -- the crude-photoshop gag is filed
    under "04 AI-GENERATED CLIPS" and ran 7 s full-frame unlabelled; (c) **a banned screen is banned by its look, not
    just its form** -- cropping the email screen above the form left its heading and confetti, still recognisably that
    screen; take the photo's own pixels (`after_still.png`) or record the current product; (d) **measure every text
    cue on his frames, the end card's second line included** (his 5942; ours cued 5973 and showed it for 7 frames).
20. **"Alternating across visible joins" means visible IN HIS CUT.** Zeeshan pose-matched five splices: his render's
    frame-to-frame change at the join was 1.1-2.3x the change around it, against >= 4.3x at every real cut. A zoom at
    those turned his seamless splices into visible ones -- the very technique that separates the human editors from us
    (memory `muhammad-trial-edit-analysis`). `zcrop.py` reads his 256x144 cache, calls a join visible above 3x, and
    carries the level (and the hair-anchored y0, from the group's minimum hair) across the rest.
21. **Choose the level a talk run opens on by drift, and flip a cutdown seam only when the levels match.** The crop
    deliberately does not chase a lean; magnified at NEAR, one lean (99.9-100.6 s) walked the cutdown to -132 px for
    1.0 s. `zcrop.py` tries both parities per run and keeps the one with the shortest sustained > 60 px stretch (FAR on
    a tie; his punch-ins forced NEAR); `zcut_build.py` flips an incoming hold only when the seam would otherwise join two
    holds of the same level -- here the new parity made that seam a zoom cut on its own.
22. **A beat that prints no words keeps its captions -- the hook above all.** The split (Dan above, the door photo
    below) was muted, so a muted viewer read "...it's not even real." then "I was 200 pounds." with no "I generated this
    picture with AI". The door card now sits between Dan and the caption band -- and at 0.87x instead of a soft 1.45x
    blow-up.
23. **Settle a disputed caption word acoustically, not by majority or grammar.** Whisper small heard "a specific
    equipment", Whisper medium "the". The CTC negative log-likelihood of each full transcript under the aligner's own
    wav2vec2 (19.1 for "a" vs 34.7 for "the"; greedy decode "A") showed the caption was right.
24. ⚠ **A cache keyed on a sequence number serves stale pictures the moment the sequence changes.** `captions.py` drew
    a state image only when `c{n:05d}.png` did not exist; unmuting one beat regrouped every caption after it, and the
    re-run silently reused the previous run's images -- "I was 200 pounds." burned over "I generated this picture"
    while `list.txt` timed it perfectly. Test stills caught it before a render. State files are now named by their
    CONTENT (`md5(line text | lit word | CAP_Y)`), in the build and in `reference/captions.py`.
25. ⚠ **`qc.py` check 17 measured a PREVIOUS render.** It reused `centering/m` whenever the folder existed, so the
    first master's "2/28 beyond 70px" came from a 14 s test render (28 samples at 2 fps; the 249 s master has ~290),
    and the re-rendered cutdown repeated its first render's numbers to the pixel. The independent audit's own 589-frame
    measurement is what actually cleared that master. Check 17 now reuses the cache only when `centering/source.key`
    (path | size | mtime) matches the file it is grading. **Any gate that caches per-file work must key the cache on
    the file** -- same class of bug as lesson 24.
26. ⚠⚠ **Dan rejected the delivered verticals' AUDIO (2026-09-10): "What the fuck happened to the audio? Zishan's
    audio sounds much better. This is an awful mistake which can't happen again."** Lessons 6 and 16 processed
    Zeeshan's finished mix to pass OUR rows -- +9.9 dB into a 4x-oversampled limiter for -14 LUFS, a mono sum for L/R
    >= 0.98 -- rows his own mix FAILS (-23.5 LUFS, L/R 0.970). Every check it met was level-normalised (provenance
    0.9989) or target-based (LUFS, L/R, a 4.5 dB one-sided shave allowance), so it passed `qc.py` 20/20 while the
    loudness range fell 5.9 -> 4.1 LU -- measured, written up as a "trade-off", shipped anyway. **The fix is
    structural: the editor's audio ships untouched (Step 4), and `audio_gate.py --verbatim` + `qc.json
    "audio_mode": "verbatim"` gate his level, dynamics and stereo image against HIS.** The re-delivery's full length
    carries his audio stream bit for bit (md5 5051f4f4...), its cutdown his cut mix encoded with no filter; both
    rejected files are corpus entries the verbatim rows fail three ways, and his own export is the approved anchor.
    The A/B sent with that delivery also played the pinned MUHAMMAD reference as "his" -- `--ab` in verbatim mode now
    plays the editor's own mix.

## [A7] Muhammad's Ad 5 (2026-09-10) — a processed mix, a 29.97 editor, and two audits that found what the gates could not

Build dir `/Volumes/Extreme/_edit_work/ad5-vert/`, scripts in `reference/a7/`. Every lesson below was paid for on this build;
the first independent audit returned "does not ship" with nine findings after 20/20 gates, the re-audit found two more.

1. **A processed editor mix needs GCC-PHAT to lock against the raw.** Muhammad's EQ'd / de-reverbed / compressed mix
   correlated 0.61 (median) with the raw lav waveform, against Zeeshan's untreated 0.99; `zedl.py`'s r > 0.85 run threshold
   then found 10 audio runs of 65. PHAT whitening (`zprofile2.py`) locks 1,718 of 2,341 windows, 3.3 ms within-run jitter.
2. **His text-left / Dan-right screens need a RIGHT-HALF framing template.** The centre template sits over his text panel,
   the fit reads r 0.2, and the EDL calls a 17 s window beat "insert" — base black. `zfit_right.py` re-fits every sample
   under 0.80 with x 150–252 and records the template box on the sample; zpic2/zedl score with it.
3. ⚠ **An ODD-width raw frame from ffmpeg on yuv420p SHEARS silently.** A 817-px card hole → `crop=817:…` is rounded to 816
   by the chroma subsampling, the raw pipe delivers 816×h×3 bytes per frame, and a reader that reads 817×h×3 tears every
   frame diagonally with an alternating brightness — the watch scan called it "jumps", the strips showed a 3-frame flicker.
   `format=rgb24` first in the chain, EVEN hole sizes, and the reader raises on a short read.
4. **Recover his flash strength from HIS luma trace, per side of the cut.** A guessed envelope with one base level washed
   ten frames near-white; k = (his − base) / (255 − base) with the outgoing side's last frame and the incoming side's
   settled level as bases reproduces his 3-pulse light leak frame for frame (`beats.py _flash_windows`).
5. ⚠ **A plate cache that "settles" before its last element drops that element.** The bullets plate settled 1.6 s after
   the last bullet; "COMPLETELY FREE" typed on 1.2 s later and never appeared. The audit caught it; the settle time now
   includes every sub-element (same class as A6.19a).
6. **Type-on speed scales to the overlay's duration**: a 0.83 s Day chip with a 0.75 s type-on never finished its line.
7. **Size Dan's window from the BOTTOM safe edge (1660), not from the top**: `h = 1660 − 60 − 74 − text_h − 24`. The old
   150 px allowance put three-bullet builds at y 1795.
8. ⚠ **Every lift from his render must be checked for HIS burned text, at full resolution.** The cooking clip carried his
   lower third in its bottom fifth (ours drew the same words underneath — "duplicated lower third"), the laptop dad his
   AI label. Inset the window with `crop=` (still a downscale) and prefer the clean library source where one exists
   (the stressed dad = `ai_busydad_kitchen.mp4` at 1:1, matched by NCC).
9. **His cut can sit ON the flash peak**: the salad-guy lift started at the beat (4458) and showed five frames of his
   16:9 bullets screen inside our card before his cut at 4463. Start the lift on his cut frame and let the flash ride.
10. **A lift must cover its beat; play it slower rather than holding the last frame.** Two held tails (0.2 s and 0.3 s)
    came from lifts a few frames short; `rate=` on the reader (setpts) fills the beat with no freeze.
11. ⚠ **The hair detector must walk UP from inside the hair.** A dim wall above the bright fridge above his head sat below
    the hair/forehead midpoint, and the top-down search read the hair top at y = 0 on half the samples (the delivered-frame
    gate FAILED a correct crop). `zhairgate2.py` / `zhair_ad5.py` walk up from the mask top while rows stay hair-dark.
12. **A time-based `-ss` seek lands on the WRONG frame on these masters** (measured: a frame ~1 s away, which read as
    "hair cut at the top" and cost an hour). Extract by index: `-vf "select='eq(n,N)'" -fps_mode passthrough`.
13. **NEAR holds anchor on the HEAD.** The audited torso anchor centred the shoulders while a 53 px head lean read as 122
    px off at the 2.3× NEAR magnification. `zcrop_ad5.py` tracks 0.4·torso + 0.6·head for NEAR, torso for FAR. And a
    punch-in whose head lean exceeds 60 px for ~0.8 s at NEAR is DEMOTED to FAR (skill A6.21: never chase a lean).
14. **His punch-in starts ON his picture cut when the fit puts it within 8 frames**: a cut then a push 0.2 s later reads as a
    naked cut plus a zoom (re-audit N2). Snap punch edges to the EDL.
15. **The join-visibility ratio cannot tell a pose snap at 1.1 from a pose-matched splice at 1.0** — six joins the audit
    read as naked sat at ratios 1.1–1.5 while the four it called invisible sat at 1.0–1.2. Lower VIS_K to 1.8, then let the
    audit's eye decide the rest (`FORCE_VISIBLE`); a level change hides a snap that the ratio cannot see.
16. **Cutdown L-cut tails**: a word that ends 1–4 frames past his picture cut ("…future self." under the title card's first
    frames) is finished over the next range's first frames instead of being clipped (`zcutdown_ad5.py`), and the
    generated cut beats carry the full spec so window bodies and mutes survive into `cut/`.
17. **The watch scan's "unexplained jump" inside an app card is the recording's own screen change** on his time map —
    report it, do not chase it.
18. **Two audits, not one.** The re-audit of the "fixed" render found two new defects the fixes had introduced (a lift's
    in-point, a punch start that missed the cut). Budget the second audit; it is where the last real defects are.

## [A8] Muhammad's Ad 4 (2026-09-11) — a sibling build's revisions, small phones, his pace, and moving a level change

Build dir `/Volumes/Extreme/_edit_work/ad4-vert/`, scripts in `reference/a8_ad4/` (its README maps each script to its step:
the a7 pipeline + `g8.py` / `render8.py`). Audit 1 returned "does not ship" with ten findings after the gates and a
211-strip watch pass; audit 2 verified eight of nine fixes and found four more. Every one is a rule below.

1. **Step 0b's first draft lied on a clean export** (fixed in the committed `hd_vs_draft.py`): it counted clipping on a
   `-ac 1 -ar 16000` decode, and ffmpeg's stereo→mono downmix lifts a correlated mix ~2.3 dB — 8,810 "clipped" samples in an
   HD with ZERO samples ≥ 0.999 natively. Before stopping on an export fault, re-measure it independently.
2. **Read `git log` for new standing rules at the start AND before the first render.** Dan's Ad 5 round-1 revisions landed
   20 minutes into this build (every real after picture full-bleed portrait + "Real picture of me — not AI-generated").
   Reproducing Muhammad literally would have shipped his two landscape stills in cards.
3. **A phone ~300 px wide at 1920 cannot be matched at 640.** The matcher locked on one frame (r 0.50, constant t) while his
   phone scrolled. Full-res crops + a multi-scale template search (`zmatch4c.py`): r 0.67–0.94, monotonic. Take coordinates
   off the FULL-RES frame — a contact-sheet tile's local x × 3 put the first crop 240 px off the phone.
4. **A clip beside the editor's own label needs a FIXED box** (his tag swallowed the hole detector: r 0.2 → 0.55–0.60), and
   **a low-motion clip's time map is linear per shot**: the NCC jitter + running maximum made 13 frozen runs of 8–20 frames.
5. **Reproduce the editor's own AI label device, ON from the first frame.** His "AI-generated video" tag + dashed arrow
   (Dan-approved) points DOWN in 9:16; typed on, it left the clip unlabelled for 5 frames. The card fades up over 10 frames
   with the tag already on — his entrance.
6. **Every text reveal at HIS pace.** g5's reveals typed 3–6× slower than his: a 1.5 s "AI can read the label" was readable
   for 6 frames. His line is complete 4–8 frames after the tab, his bullets in ~6, tails in 1–2, his title card's headline by
   +15 and sub by +25. `g8.py`: LT_GROW 0.15, LT_HEAD 0.06, LT_STAG 0.10, LT_TYPE 0.25, BUL_TYPE 0.30, TAIL_TYPE 0.25, and
   a faster `title_card` (audit 2 caught the title card still at the old pace — it is a text reveal too). Cue an overlay at
   his FIRST letter, not at the olive tab's first detection.
7. **A window beat ends ON his cut.** His window wipes out over ~8 frames and his take change sits inside the wipe (1267,
   5905): ending at the wipe's start left a 3-frame shot of the old take; ending after his cut showed his pose jump inside
   our window.
8. **Move a level change WITH its beat edge, as a pair.** When W4's end moved onto his cut (5912 → 5905) the level change
   stayed at the old edge: 7 FAR frames, then a punch on continuous footage (audit 2). Mark the new edge `FORCE_VISIBLE` and
   the old one `FORCE_INVISIBLE` — the group count is unchanged, so no other hold moves. Merging the groups instead changes
   the parity of the free run back to the previous fixed punch and re-levels every hold in between. Diff `zoom_per_frame`
   before and after: here only 5905–5911 changed.
9. **A visible join INSIDE his punch-in is a naked jump cut in ours** (3925: he hid it with a punch-OUT; our punch range
   forced NEAR both sides) — end the punch range on that cut. Joins his render reads as invisible (ratio 1.1–1.6) can still
   jump at 2.3× (2937 a blink, 3543 hands): `FORCE_VISIBLE` after the audit's eye, as in A7.15. The reverse: a join 3–6
   frames from a beat edge (1267, 6508) is `FORCE_INVISIBLE`, or it leaves a sliver at another level or y0.
10. **The hair floor is met by the level, not by headroom that does not exist.** This roll puts the hair 22 px under its own
    top; a 9-frame FAR opening read 34 px on the phone (floor 36). NEAR magnifies it to ~50, so the hook opens on NEAR.
11. **Rebuild an approved screen from the recording's own pixels:** his download screen = the page header + the after image
    enlarged to the screen width at 40.5 % down, the email form out of frame (Dan r2/r3); the photo's box came from its EDGE
    gradients (threshold detectors failed on the page's grey card). **A phone mockup takes the MEDIA's aspect** — a 9:16
    recording cover-cropped into a 19.5:9 phone loses ~9 % of list text per side.
12. **Captions: settle words acoustically, read the greedy decode, merge Whisper's hyphen splits.** CTC NLL picked "name it"
    and "can't"; the greedy decode "TOP" settled "tub" where "tone"/"tongue"/"tube" scored within 0.5; "abs" over "ads" is
    below CTC's resolution (meaning decides); "my supplements that workouts" won two acoustic tests against Whisper-medium's
    "supplement stack" — kept, flagged for Dan's ear. "science -based" was two tokens → FIX `('science', '-based'):
    ('science-based', '')`. ⚠ **`align_ctc.py` reads its own previous `words_ctc.json`**, so a FIX change is silently
    ignored (here it asserted 728 vs 731) — move `words_ctc.json` aside before re-aligning.
13. **Cutdown seams:** a range never ends inside a strobe's RISE (two brightening frames, then a hard cut, read as a flicker at
    two seams — `zcutdown.py` ends it at the strobe's first flashed frame), and **the last seam flips the OUTGOING hold** —
    the ending was his walk-out, and at NEAR Dan's face left the right edge (`zcut_build.py`).
14. **`zcut_build.py` generated a cut/beats.py with Ad 5's caption-mute kinds hard-coded** (new kinds would have run captions
    under the cutdown's graphics — the sets now come from the master's beats), and read `his_mix.wav` as int16 (a float WAV is
    silently misread — it asserts 16-bit stereo). A range that opens mid-sentence capitalises its first word.
15. **Near-static media freezes in our gate even when his does not** (0.93× card downscale of a slow clip): video cards carry
    a 4 % push, title cards 8 %.
16. **The editor's export can miss Dan's true-peak rule by a hair.** Muhammad's V4 HD peaks at −0.90 dBTP against −1.0 (the
    draft Dan approved read −0.2). Verbatim mode gates TP absolutely, so the stamp FAILS and `deliver4.py` refuses the
    masters; his audio is not ours to trim (Step 4) — report it, deliver review copies, and let Dan choose (accept, or a −1.0
    re-export from the editor, then a 5-minute re-mux).
17. **Load:** at a 1-minute load average of 60–220 (three sessions building), the compositor ran at ~2 fps against ~12 quiet.

## [A9] Ad 5 round 1 (2026-09-11) — the real-picture label, and a fix that was worse than the defect

Dan approved the Ad 5 vertical's picture and asked for three revisions: every real after picture full-bleed and
PORTRAIT, the new "Real picture of me — not AI-generated" label on each, audio untouched. Build dir
`/Volumes/Extreme/_edit_work/ad5-vert/`; `reference/zpick.py` is the tool it added. Two independent audits, both
returning DOES NOT SHIP the first time, on two different things — and the second one was a fix *I* had introduced.

1. **A LANDSCAPE still can never be full-bleed in 9:16 — it is not a crop decision, it is a different picture.** His
   1.22:1 and 1.49:1 photo-shoot stills keep a head and throw the body away. When the standing rule says every after
   picture is full-bleed, those get REPLACED, and the replacements come from the same shoot so the run still reads as
   his. Four distinct shots in a four-shot reveal, as he had.
2. ⚠ **A finished, retouched, Dan-approved photo can still be composed OFF-CENTRE, and a centred cover crop inherits
   it.** `studio-white-23` puts its subject 218 px left of the photo's own frame centre: rendered full-bleed that is
   **torso −122 / head −96 px** on the phone, and the cut to the next studio shot popped him 118 px. Nothing upstream
   sees this — the beat sheet is right, the asset is "final". **Measure every full-bleed still's rendered crop with
   `rc/personmask` + `anchor.py` BEFORE the render** and pass an `ox` per media; here `ox=0.02` (the window slid to the
   photo's left edge) gave torso −26 / head 0 against the neighbour's +14 / +20. Found by the audit, not by any gate.
3. **Pick pictures on the RENDERED 9:16 crop, with the push windows drawn on it** (`reference/zpick.py`): portrait
   filter, cover crop, the tightest push (z 1.05) outlined, the real-picture chip composited where it will sit. Skill
   rule 12's "verify before rendering" is otherwise a sentence nobody executes when there are 176 candidates.
4. ⚠⚠ **A bright photo behind the burned caption band is a legibility regression — and the obvious cure is worse than
   the defect.** Full-bleed photos put the OLIVE lit word on red Muay Thai shorts (background luma 74 against the
   olive's 125), pale water (76) and a white studio backdrop (98–110). A6.17 says fix the picture, not the gate, so the
   first fix was a full-width gradient, 0 → 0.50 alpha, held to the frame bottom. It is invisible on the six dark
   photos — and on a WHITE CYCLORAMA it paints a mid-grey fog across a backdrop that has no floor line or shadow to
   explain it. The re-audit read it at 1:1 and called it a rendering fault; it refused the build over it. **The device
   that works on every background is a caption-LOCAL black plate sized to the caption image's own alpha bbox**
   (`g5.caption_plate`, with a `min_w` so a one-word line does not get a cramped box), in the same chip language as the
   AI and real-picture labels: it reads as design on white, it disappears on a frame that prints no caption, and it
   costs none of the picture. Do not weaken the gradient instead — at 0.25 the olive on white is back under threshold.
   ⚠ And the gate can fail on this too, for its own reasons: see 10.
5. **Order two stills so the big luma step lands on the EXIT, not the entry.** Cutting from his dim room into a
   near-white frame was the largest non-flash luma jump in the film and read for a beat like one of his light leaks.
   Entering on the grey seamless and exiting on the white one moves that step to a cut INTO darkness, which cannot be
   mistaken for a leak. Measured: entry 79.6 → 87.8, exit 134.5 → 78.6.
6. **A8.13 again, and it shipped inside a build Dan had already approved:** the cutdown's second range ended TWO frames
   into one of his light leaks (luma 100.8 → 143.0, 142.9 → 53.9) because his peak frame belongs to the next beat and
   was never carried — two brightening frames, then a hard cut, a flicker. `zcutdown.py` now pulls any range end that
   sits inside a strobe back to the strobe's FIRST flashed frame. **Dan's approval of a cut is not evidence its seams
   are clean** — he is watching the film, not the seams.
7. ⚠⚠ **TWO GATE SCRIPTS WRITING THE SAME `/tmp` PATH. With two builds running, one graded the other's file.**
   `caption_sync_check.py` wrote `/tmp/_cs.wav`; a sibling session's extraction overwrote it between this run's write
   and its read, and test B measured THIS file's word list against a 276-second file's audio — 8 phantom "words lit
   outside speech" on a file whose audio had not changed by a byte. Per-process `mkdtemp`, removed at exit. **Any gate
   that stages work on disk must stage it per process** — the same class as A6.25 (a cache keyed on anything but the
   file it is grading) and worse, because a green row that measured the wrong file is what ships a defect.
8. **When a cutdown CHANGES LENGTH, a frame-by-frame diff against the previous cutdown is meaningless after the first
   seam** — everything downstream is shifted and the "changed spans" report is noise. Verify **cut frame → master
   frame** through `cut_plan.json` instead: every frame must match the master within encoder noise, except the one
   range where `zcut_build.py` deliberately flips the hold FAR↔NEAR (its log names it: "seam flip APPLIED").
10. ⚠ **A GATE CAN SAMPLE A WORD ON A FRAME WHERE THE WORD IS PHYSICALLY UNREADABLE — AND THAT IS THE INSTRUMENT
    FAILING, NOT THE BUILD.** `caption_sync_check.py` grades each word on ONE frame, 40 % into it. Inside the editor's
    light-leak strobe the caption band is washed toward white for a few frames at a time: measured on Ad 5's cutdown,
    "when" (frames 212–215, inside his 209–220 leak) carries 96 qualifying pixels at 212 and **zero** at 214–215, and
    the heuristic landed on a washed one — 96.1 % on a correct cutdown, a FAIL. The caption image is IDENTICAL across a
    word's own span, so the gate now tries up to five frames inside that span, **least-washed first**, and grades the
    first that reads. **That is a strictly better measurement of the same word, not a looser bound** — a word lit
    wrongly is lit wrongly on every frame of its span — and the 97 % threshold was not touched. A word readable on no
    frame of its span is still a miss and still reported. Run the corpus after any change here; it passed 19/19.
11. ⚠⚠ **TWO SESSIONS EDITING THE SAME SHARED GATE WILL CLOBBER EACH OTHER, SILENTLY.** A fix committed to
    `reference/caption_sync_check.py` was overwritten an hour later by a concurrent session's rewrite of the same file
    (a good rewrite — full-resolution band, exact highlight colour, dense-blob centroid — which simply did not have the
    earlier change in it). It was only noticed because `qc.py` runs the SKILL's copy while the build chain runs the
    BUILD's copy, and the two disagreed on the same file. **When you touch a shared gate while other builds are running:
    diff the skill's copy against the build's before you trust either, re-apply rather than rewrite, and say so in the
    coordination file.** A build copy that has drifted from the skill copy is its own defect class.
12. **Re-render the whole master rather than splicing the changed spans.** Three full renders on a loaded machine cost
   ~15 minutes each and the gray-trace diff then PROVES the change set — on all three rounds it came back as exactly
   the intended spans. A spliced render cannot make that claim, and A4.0aa is what splicing costs when it goes wrong.

## [A10] The first SQUARE (Ad 2, 2026-09-11) — a 1:1 re-layout of an APPROVED vertical

Build dir `/Volumes/Extreme/_edit_work/ad2-sq/`, tools in `reference/a10_sq/` (its README maps each
script to its step). Rules: `Handoffs/handoff-20260911-square-ads-00-shared-rules.md`. The audit
returned **"does not ship"** with four findings after `qc.py` scored 20/20 and every sub-gate passed;
fixing the first exposed a fifth. Every lesson below is measured on this build.

1. ⚠⚠ **A FULL-HEIGHT WINDOW IN A 1080-TALL FRAME IS ALWAYS 1.00x, WHATEVER ITS WIDTH.** The crop is
   1080 tall and the window is 1080 tall, so the magnification is fixed and a NARROWER window shows
   LESS of the subject, not a wider shot. The editor's own 16:9 split gets away with a full-height
   window only because his is 945 px of 1920 (49 % of his frame); at 496 px of 1080 the same
   construction put Dan's head at **81 % of the window width**. Size any window beside other content
   from the MAGNIFICATION you want and derive the height: `win_h = win_w*1080/(win_w/mag)`.
   And check the balance against HIS: his Dan-head-to-phone-width ratio is 0.55; the square read 0.33
   at the vertical's own 0.60x, because the phone takes 47 % of a 1:1 frame against 22 % of his 16:9.
2. ⚠⚠ **A 9:16 DEFAULT PASSED BY THE CALLER SURVIVES A FIX TO THE FUNCTION'S OWN DEFAULT.**
   `render.py` had `y_bottom=spec.get('y_bottom', 1600)`. Changing `overlay_lower_third`'s default to
   a square value did nothing, so a lower third was drawn at y 1447-1600 in a 1080-tall frame --
   **entirely off frame for 4.3 s** -- and because a lower third MUTES the captions that beat carried
   **no words on screen at all**. Its overlay `.mov` had EMPTY ALPHA. `qc.py` 20/20, the watch scan,
   the caption gate and the safe-area measurements all passed on it. **Grep the renderer for every
   literal that encodes the old frame's geometry, not just the library.**
3. ⚠ **A LABEL CHIP AND A LOWER THIRD ON THE SAME BEAT MUST BE MEASURED AGAINST EACH OTHER.** With the
   bar above finally visible, the AI-GENERATED chip sat 46 px UNDER it. Two elements both left on
   their defaults collide the moment the frame changes shape.
4. ⚠ **CHECK A STILL AT THE PUSH'S END, NOT ONLY AT FRAME 0.** `still_chain` starts at zoom 1.0, so a
   frame-0 contact sheet shows the LOOSEST framing a beat ever has. A 1:1 cover crop of a 4:5 photo
   takes 10 % of its height at the start and **12.8 % by the end** -- off the top of his head on a
   photo a frame-0 sheet had cleared. `a10_sq/sqstills.py` renders frame 0; **`sqstill_end.py` renders
   both ends** -- use it on every full-bleed still.
5. **Which stills survive a 1:1 crop is a MEASUREMENT, not a rule.** On this ad the two portraits at
   0.73-0.75 lost their heads and went into his card; the three after pictures (0.67 portrait and two
   landscapes) kept head and waist and stayed full-bleed. Contact-sheet the rendered crop of every
   one before building, and card the ones that fail -- carding is also his own language for media
   that does not fill his frame.
6. **The concat demuxer's trailing `file` line repeats THAT image.** Written as the last caption state
   it re-showed the final lit word for 7 frames past its own end -- a word stamped across the closing
   CTA pill. Write the BLANK. (The approved 9:16 carries the identical overprint.)
7. **The square is the format that shows MORE of his frame, not less.** A 1080 px window of a 1920 px
   clip has 840 px of freedom against 9:16's 1312, but it is 472 px WIDER -- it held a sign the
   vertical had cut in half. And the talking head is a PURE CROP at 1.00x, so the `unsharp` the
   vertical needs for its 1.78x upscale is removed (measured: Laplacian energy 0.92-0.96 of the
   conform, no halos). Attach a sharpen only where the chain actually resamples.
8. **Sizing, in this order:** the caption band sits at CAP_Y 880 and cards must END above it (64-848,
   against the vertical's 1180) -- which still runs a phone 44 % wider than his own 16:9 card does.
   Window type comes DOWN (46/50 -> 40/44) until no beat clamps: at the vertical's sizes the
   four-bullet beat asked 440 px of type and left Dan 444, a silent overflow past the bottom safe
   line. Margins 100 and SYMMETRIC: the in-feed reserve is on the right only, but an asymmetric text
   column in a square reads as mis-centred type, and the measured cost of 76 -> 100 was ONE extra
   wrapped line in the whole ad.
9. **Audio: copy the APPROVED VERTICAL's stream and assert its md5 before writing the file**
   (`a10_sq/muxsq.py`). Ad 2's vertical carries his mix plus the one constant +5.2 dB Dan approved, so
   `--verbatim` against his raw export would FAIL on the very sound he said yes to: the mode is
   `reference-mix`, exactly as the vertical's own stamp reads, and the md5 is the real guarantee.
10. ⚠ **A GATE SHARED BY THREE CONCURRENT SESSIONS CAN CHANGE UNDER A RUNNING BUILD.**
   `caption_sync_check.py` moved from half to full resolution mid-build. On olive-graded material
   that regresses: the grade sits inside +-22 of the accent colour, so the exact mask matched 13,347
   px where the lit word is ~1,200 and the heaviest column run landed on the background. Twelve words
   were reported as misses and **all twelve are correct and legible on the delivered frame.** Report
   it, record it in the gate file, do not tune it -- and never assume the instrument that graded your
   last render is the one grading this one.

## [S1] THE SQUARE (1:1) TRANSLATION — Ad 1, 2026-09-11

Dan's Google Ads rep asked for a **1:1 version of every finalized ad**: a Demand Gen video ad
serves across YouTube in-feed, Shorts, Discover and Gmail, and Google fills each placement from
the aspect ratios the ad carries. The shared rules are
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md`; this section is what building the
first one actually cost. Build dir `/Volumes/Extreme/_edit_work/ad1-sq/` (`sqlib.py` +
`sqassets.py` + `render.py` + `sqmux.py` + `sqcutdown.py`, the attempt-3 pipeline re-laid-out).

1. **A square is a re-layout of the APPROVED VERTICAL, not a third recovery of the editor's cut.**
   Copy the vertical's build dir, keep its beat sheet, EDL, grade, flashes, pushes, lower thirds
   and SFX unchanged, and change only the geometry — plus whatever standing rules have landed
   since. The whole build is then a day, not a week. Do NOT copy the whole dir: Ad 1's vertical
   is 65 GB of caches. The 2.8 GB that matter are the scripts, the JSON, `base.mp4`, the assets,
   `_flash/final/` and `ref_audit/his.wav`.

2. **The audio is the approved vertical's AAC stream, COPIED, with the md5 asserted at the mux**
   (`sqmux.py`), so the square sounds exactly like the cut Dan approved. The cutdown cuts that
   same mix at the seams with 4 ms raised-cosine joins and encodes it once at 320k with no filter.
   ⚠ The vertical's own `cutdown.py` rebuilt the music bed and ran two-pass `loudnorm` — the class
   of thing Dan rejected on 2026-09-10. Delete that path when you copy the dir; do not run it.

3. ⚠⚠ **CHOOSE THE WINDOW'S CROP BY MAGNIFICATION, NOT BY "FIT THE ROOM IN".** The first cut of
   the stacked (text-below) layout sized Dan's window from the text and then filled it with the
   whole 1920-wide frame. Two things went wrong at once and neither is visible in the code: Dan
   came out **a third of the size he is in Muhammad's own frame**, and because the crop was the
   full source width the face track's x **clamps to 0**, so he sat at one edge of the window with
   an empty doorway beside him. The fix is two numbers: the crop is sized so the on-screen
   magnification matches HIS (a 16:9 frame shown 1080 wide is the source × 0.5625), and the crop
   width is **capped** (1400 px here) so the track keeps ~260 px of travel. Verify by rendering
   the window beats and looking — the statistics upstream were all green.

4. **The talking head at 1:1 is the source at 1.00× — the square's one free advantage.** A
   1080×1080 crop of a 1920×1080 conform needs no upscale at all, against the vertical's 1.78×
   (608×1080 → 1080×1920), and it amplifies the subject's lean 1.78× LESS. Measured on the
   delivered Ad 1 square: median +(-1) px, sd 33, 9 of 192 talk samples beyond 70 px, **zero**
   sustained runs. The same track in the vertical is magnified nearly twice as far.

5. **Decide full-bleed vs full-height by LOOKING at the 1:1 crop of every asset, never by the
   aspect ratio.** What a 1:1 crop takes off a standing photo of a person is their head or their
   shorts, and which one is not predictable from the number: of Ad 1's assets, three landscape and
   portrait stills survived a 1:1 cover crop whole while four portraits lost his head entirely.
   Contact-sheet them all first (`_sq/media_1to1.jpg`) and record the decision per media key with
   its reason (`sqassets.py`). A 2:3 portrait that cannot be full-bleed goes **full HEIGHT on his
   field** — that is the square's "vertical and full screen".

6. **A 1:1 frame HAS the width to keep the editor's own left/right split for portrait media.**
   Muhammad's product beat is phone LEFT / Dan RIGHT and the square keeps it exactly. ⚠ Check his
   render, not the handoff: the Ad 1 handoff said "Dan left, phone right" and his frames say the
   opposite.

7. **But the TEXT screens cannot keep it.** Beside Dan, a 1:1 text column is ~620 px, which puts
   his 48 px type at 27 px. Those go stacked (Dan above, text below) with a type ladder that steps
   down only as far as it must, and an assert that FAILS the build if the block ever ends below
   the safe line.

8. ⚠ **A LABEL BURNED IN FOR A 9:16 FRAME BECOMES TOO SMALL AT FULL HEIGHT IN A SQUARE.** The
   hook's goal clip carries its own AI-GENERATED chip, measured at x 186..896 of 1080×1920; shown
   at full height in a 1:1 frame it lands 411 px wide — 38 % of the frame against the ~68 % the
   skill asks for. Adding a second chip beside it is two labels. **Draw ours OVER it, and assert
   the coverage in code** (`chip_png(..., cover_box=...)` raises if our box does not contain the
   burned one).

9. **The square is where an old build meets the standing rules it predates.** Ad 1's vertical was
   approved before the "Real picture of me — not AI-generated" rule (2026-09-11) and before the
   photoshop gag's missing AI label (A6.19b) was known — and its beat sheet had no label mechanism
   at all outside the olive card. Re-read `git log` for standing rules at the start of a square
   build, walk every beat against them, and put each addition in the notes as a difference from
   the file Dan approved.

10. ⚠ **THE CUTDOWN PLAN MUST BE IN FRAMES, NOT SECONDS.** The last range's `src1` is `beats.DUR`
    (232.768 s) while 6,976 frames is 232.7659 s, so the selection asked for one frame more than
    the master holds and came out a frame short — with every duration check still green. Each
    range takes exactly the frames that exist between its two frame indices.

11. ⚠ **`wave` CANNOT READ ffmpeg's `pcm_s24le`** (WAVE_FORMAT_EXTENSIBLE, tag 65534) — it raises
    outright, and a float WAV it would read SILENTLY WRONG (A8.14). Decode the editor's mix with
    the same tool that wrote it.

12. **A green highlight over green-toned footage is unreadable, and the fix is the picture**
    (A6.17 again, on a new cut). The square's caption band lands lower in the frame than the
    vertical's (81 % down vs 73 %), which on this ad put it straight across the **neon
    yellow-green stripe of his shorts** in the hook: 16,500–18,400 pixels within 90 levels of the
    olive highlight, three consecutive words lit invisibly, `caption_sync_check.py` failing the
    build on the run at 98.4 % overall. A soft dark bed behind the band (0 → 0.55, ramped, drawn
    into every caption state under the text) fixes the eye and the gate together. **Put the scrim
    parameters in the caption cache key** or the re-run silently serves the previous pictures
    (A6.24).

13. ⚠ **NEVER OVERWRITE THE FILE AN AUDIT IS READING.** The independent audit was launched on the
    master, then the master was re-muxed at the same path for the caption fix — killing the mux
    mid-write left the auditor reading a truncated file. Render a revision to a NEW name, or
    launch the audit only after the file is final. (The skill already budgets two audits; this is
    a reason to keep them strictly sequential.)

14. **Re-align the captions when you re-lay-out an old build.** Ad 1's approved vertical timed its
    captions from Whisper's own word timestamps. Measured against a CTC forced alignment on the
    same mix: Whisper's starts run **+129 ms early on average (sd 91, p90 +237), and 214 of 761
    words are more than 150 ms off** — the fault Dan rejected on 2026-09-08. The square's captions
    come from `align_ctc.py` and score 98.4 % on the delivered-file gate.

16. ⚠⚠ **A RANGE MAP MUST CLAMP A SPAN, NEVER DROP IT.** The cutdown's caption mutes are the
    master's suppressed spans mapped through `cut_plan.json`. Mapping the two ends
    independently and discarding the span when EITHER end falls outside a range threw away
    **both CTA pills' mutes** -- each pill starts inside a kept range and ends just past it --
    and the delivered cutdown printed "below to see yourself" straight across "With Abs". That
    is the A4.7 defect, reintroduced by a helper. A span maps to its INTERSECTIONS with the
    ranges, clamped. The same bug dropped both pills from the generated cut beat sheet, so
    nothing downstream could notice either. **No gate in the set caught it** -- it was found by
    mapping the master's overlays by hand and looking at the frames.

17. ⚠ **A HELD CAPTION'S STOPS BELONG TO THE FILE BEING RENDERED.** `captions.render()`
    recomputed its hard stops from the beat sheet, which in a cutdown is the MASTER's
    timeline -- times that do not exist in the cut. So even with the mutes fixed, the held
    last word of the group before the pill still rode across it. The caller passes its own
    stops (`stops=[a for a, b in mute] + seams`).

18. ⚠ **A GENERATED BEAT SHEET IS PYTHON, NOT JSON.** `json.dumps` writes `false` and `null`,
    which are not Python names, so `cut/beats.py` raised `NameError: name 'false' is not
    defined` on import -- and `qc.py` reports an unimportable beat sheet as NOT MEASURED,
    which is a FAILURE, not a skip. Emit `repr()`.

19. **Measure the "longest static stretch" bound off HIS cut before trusting it.** Ad 1's
    square inherited `max_static: 16.0` from the old vertical's config, where it had been
    copied rather than measured. Measured with the same instrument: **his 16:9 final holds
    16.5 s at 27.39-43.88**, ours 16.7 s on the same passage (the approved 9:16 reads 15.3 s
    because its detector places the preceding cut 1.4 s later). The bound is his number, so
    the check fails by 0.2 s and that is reported -- **never raised to go green**.

20. ⚠⚠ **IN A SELECTION CUTDOWN, A6.15 IS A PICTURE PROBLEM, NOT A BEAT-SHEET PROBLEM.** The
    cutdown selects intervals out of the FINISHED master, so his lower thirds and CTA pills are
    already in the pixels. A range that opens part-way through one inherits words belonging to a
    sentence the cutdown no longer contains -- Ad 1's range 5 opened at 91.02 inside his
    86.90-91.85 lower third and printed "If you saw yourself with abs, you'd be MOTIVATED" over
    "And right now, you can generate...". The generated cut beat sheet was CORRECT (it drops an
    overlay whose start was cut away), which is exactly why nothing caught it. **Assert it
    structurally** (`assert_no_orphan_overlay`): no range may start inside an overlay whose own
    start lies in dropped material. The fix here was to open the range at 91.85 instead -- the
    lower third's end, which is also the bullets screen's start, and the bullets print those very
    words. It cost "And right now," (0.83 s) and the seam capitalisation makes the line read.

21. ⚠ **A GATE MUST CLASSIFY FRAMES BY THE RENDERER'S CUMULATIVE FRAME PLAN, NOT BY SECONDS.**
    Converting each beat's t0/t1 to frames independently disagrees with a cumulative plan by a
    frame at a boundary, so the hair gate graded a PHOTO as a talking-head frame: the towel
    picture's dark trees above his head read 0.89 on the detector-free test against a 0.20 bound
    -- a FAIL on a frame the gate should never have looked at. Build the frame set the way the
    renderer does, and keep a 2-frame guard either side of every edge.

22. ⚠⚠ **A SELECTION CUTDOWN IS WHERE THE SQUARE'S REAL DEFECTS WERE, AND EVERY GATE PASSED THEM.**
    The Ad 1 square's 0:59 was cleared by `qc.py`, the watch pass, the hair gate, the caption gate,
    the landing check AND `_shared/deliver/gate.py` before the independent audit returned DOES NOT
    SHIP. Tools and the full write-up: `reference/a11_sq_ad1/`. The four, each waiting for the next
    square: **(a)** `-ss f"{t:.4f}"` drops a frame whenever the rounding lands above that frame's own
    pts — 4 of 9 ranges started one frame late, which flashed a third photo for one frame at a seam,
    dropped the peak frame of a light leak and ran the picture **33 ms ahead of the audio over 23.6 s
    of 49 s**, with every count green because the counts were right and the CONTENT was shifted. Seek
    half a frame early and **assert each range's first and last frame against the master on the
    pixels**. **(b)** Range edges come from the CTC alignment, never Whisper (it clipped the onset of
    "You're" and cut "changes." 118 ms early): floor a start, ceil an end, **round an edge that
    snapped onto a beat boundary** — a boundary is one frame index and both sides must use the same
    number. **(c)** Three things conspire to delete the first word after a seam: the range map must
    CLAMP a straddling word, `groups()`' 0.15 s mute slack must be clipped at `beats.SEAMS` (the CTA
    pill ending on the seam was muting the next range's first word), and that clip needs a **1 ms
    tolerance** because a span clamped to a range edge and the seam are two different float sums,
    1e-5 apart. It belongs in `groups()`, because `caption_sync_check.py` re-derives its grouping
    from that same function. **(d)** ⚠ **The cutdown's mute list and word list were each derived
    TWICE** — by the builder from the in-memory plan, and by `sqcut_build.py` from `cut_plan.json`'s
    5-decimal numbers. They agreed to a few milliseconds, and one word fell on opposite sides of the
    mute line: the render burned 103 caption states, the gate re-derived 104 and reported three
    misses on captions that are correct on the frame. Written once now, read by both. **Any number a
    gate re-derives instead of reading is a number that can disagree with the render.**
23. **The concat demuxer's trailing `file` line is RENDERED — write the BLANK.** [S1].6 was recorded
    on Ad 2 and never applied in code, so the last caption state re-showed its lit word past its own
    planned end: "six pack abs," printed across the closing CTA pill's "With Abs" for 7 frames, in
    the Ad 1 square master AND its cutdown, while `cap/list.txt` ended correctly at the pill's own
    mute start. ⚠ **The APPROVED 9:16 verticals of Ad 1 and Ad 2 carry the same overprint** — a
    caption rebuild plus a mux fixes them, with no re-render.
24. **Two copies of the delivered file share one name** (the build root's and the one the gate chain
    copies into `cut/`). Check mtime and md5 before believing a frame pulled from `cut/`: three
    extractions in this build were of a stale copy, and one looked exactly like a defect that had
    already been fixed.

22. ⚠ **A `pgrep -f` WAIT LOOP MATCHES ITS OWN SHELL AND NEVER EXITS.**
    `until ! pgrep -f "qc_corpus/run.py" > /dev/null; do sleep 45; done` never finishes: the
    loop's own command line CONTAINS that string, so pgrep always finds at least one match --
    itself. Five of these ran for 18 hours on this build, long after their jobs were done, and
    they are what a user sees in the background-task list. Wait on something that cannot
    match the waiter: a sentinel file, a marker line in the log, or the PID captured with `$!`.
    (Related, and separately paid for: **never `pgrep -f "python3 X.py"`** -- these scripts run
    under the framework Python, whose command line reads `Python X.py`, so that wait matches
    nothing and the next step races the build. And **never put a step that must fail the chain
    behind a pipe**: `cmd | tail` returns tail's status, so `set -e` never sees the failure --
    that is how a mux failed and the rest of the chain silently graded the previous file.)

15. **Gates that must be rebuilt for 1:1, not reused:** the hair gate's bound is the standard's
    **fraction** of frame height (36/1920 = 1.875 % → 20 px of 1080), `centering.py` samples
    270×270, `caption_sync_check.py` must read the build's own `CAP_Y` (hard-coded at 1385 for
    9:16 it reads 505 px below a square build's captions and finds no highlight at all — a gate
    measuring empty field would FAIL a correct build), and `watch.py`'s strips are square.

## Standing content rules that override the reference

The reference editor does not know Dan's ad rules. Check every beat you are reproducing:

- **NO side-by-side before/after, ever, in a paid ad.** Muhammad's 0:03 card is exactly
  that (heavier Dan left, goal phone right, arrow between). **Cut it sequentially instead** —
  the before photo, then the goal phone.
- **NEVER show the email-capture screen**, and never the app's "Meet the new you"
  before/after screen. In the product recording `clip_109_replacement.mp4` those start at
  **26 s and 29 s** — the usable window is **0–25 s**. Assert it in QC.
- **A before and after picture are the SAME PERSON** (Dan, 2026-09-12: *"don't mix before-and-after pictures… That doesn't really make sense if you change the person."*). Never pair one person's before with another's after — in an app recording, a result screen, a card or a thumbnail. If that person's after does not exist, generate it for THEM through the live product (a real generation, never a composite) or change the before so the pair matches. ⚠ The only real app recording in the asset library uploads a man who is NOT Dan, so every phone demo cut from it inherits this.
- **Dan's REAL after pictures carry a burned label: "Real picture of me — not AI-generated"** (Dan, 2026-09-11: viewers were taking his real photos for AI). Every real photo-shoot or studio picture of Dan shown as a result gets it for its full duration, in the same chip style as the AI label. AI images of Dan keep "AI-GENERATED". The two labels are mutually exclusive: every picture of Dan's physique carries exactly one of them.
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
