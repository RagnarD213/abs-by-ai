# RO-37 "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time" (10/23 pool rolls C1893-C1897): round 1 recipe (Claude Opus 5.5, 2026-10-29)

First long-form cut from **portrait** footage (Sony 4K S-Cinetone filmed upright, 2160x3840 after rotation; 10/23 pool set).
Scripts here are copies; the live ones are in `/Volumes/Expansion/_edit_work/RO-37/round1/recipe/` (Expansion, never commit media).
RO-38 (same day, same set) can start from this.

## Presentation of portrait footage in a 16:9 film (Dan picks in round 1)
- **T** = full-frame 16:9 window of the upright picture, 2160x1215 (hair to chest), 4 % headroom above the shot's highest hair.
  It is necessarily a close-up: 2160 is the whole source width.
- **T2** = tighter close-up 1728x972 centred on the body (1.25x), used only where a take join falls under a lower third.
- **W** = the whole upright picture hair to waistband (2160x2640) as a rounded 864x1000 panel at y 40, on (a) the moving Soft
  Blue field (`softblue.field`, rendered once to `field.mp4` for the film clock, 0.07 s/frame) or (b) the same picture blurred,
  darkened, navy-tinted (the locked green-screen "soft" numbers). Centre, or x 936 while a 3A side list is up; the panel
  EASES across (overlay x expression, 14 frames) when a list comes or goes inside one shot.
- (c) close-up only was offered; it never shows the physique.
- Framing alternates W/T at every cut (long pieces split at word gaps, 3-9 s runs).

## Traps this round paid for
1. **A lower third over the W panel sits across his waist and abs.** Every lower third plays on the close-up: `build.lt_framing`
   splits a W shot at the lower third's in/out (zoom cut on a word start) and makes the middle T; same-take T/T runs merge; a
   take join between two T shots becomes T2. `build.jumps()` must print [].
2. **Whisper word edges vs measured onsets:** medium.en put "Second," at 6.80-6.82 while the voice starts 6.40 (quiet S); the
   snap walk started after it and clipped the word. Re-transcribe the ASSEMBLED voice and print every join (`asr_check.py`):
   it caught a clipped "tomorrow", a clipped "Second", a doubled "working" and a repeated "in my experience". Fix with
   explicit in/out overrides read off a 50 ms level strip.
3. **Word mapping by midpoint drops edge words** ("If", "Second,") and then plan anchors fail; map by overlap (`words_out.py`).
4. **`pgrep -f "<pattern>"` inside `bash -c '... <pattern> ...'` matches its own command line**, so a "wait until X ends"
   waiter never ends. Wait on a file (`until [ -s file ]`) or a log line instead.
5. **Hair check on the panel:** measure against the panel's top edge (y 40), and ignore stray mask specks in the trees (take
   the first of 4 consecutive rows with >= 12 mask px). Result: closest 36 px.
6. **10/23 gym library masters read darker than the sunny pool**: `broll_tune.py` lifts midtones per window (DS-76 curve,
   blacks kept) to median >= 55 / black <= 20 %.
7. **Don't reuse the same library clip in the opening montage and later**: the montage uses B0575/B0623/B0681, the
   machine cutaways B0566/B0621/B0678/B0648.
8. **The pool set's voice:** Dan picked A Natural Warmth on DS-84, DS-47 and DS-76. 10 blind Gemini listens preferred the
   untreated lav (C 6.5 vs A 3.9) but swung 3-9 on the same clip; shown to Dan as A (his pick) vs C (listener).
9. **review_server refuses a page whose linked file is outside the served folder**: copy option media into `review/`.
10. **Internal full-length render for context clips** (`ctx_chain.sh`): never delivered; cuts every item +/- 4 s and its still.

## Round 1 verdict (Dan, 2026-10-29): the boxed panel is rejected; the CUTOUT is approved
Dan: "This looks weird with the boxed-in thing" ... then on the 20 s test: "Yes, this cutout works. I think we should edit the
video this way." Method (`cutout_test.py`): graded 4K frame -> 1152x2048 JPEG -> BiRefNet (Replicate `851-labs/background-remover`,
~$0.002 a frame, 8 threads) -> alpha back to 2160x3840 (LANCZOS) on the ORIGINAL pixels -> 3-frame temporal median on the alpha
-> composite with a soft dark drop shadow. Wide: scale 0.394, body centre x 1400, hair top y 44. Corner over a gym clip:
scale 0.20, centre x 1640, hair top y 560. Hair edge steady over consecutive frames; hands/watch solid. Apple Vision's
mask works too but is softer. The full-frame close-up "is a little bit too close": use it rarely.
Treat cut-out portrait footage like green screen: the locked long-form background template (`_shared/greenscreen-bg/`).
