# RO-14 "Why You're Not Losing Weight" (9/23 C1708): round 1 recipe (Claude Opus 5.5, 2026-10-14)

One 13:53 talk roll on the 9/23 studio set, cut to 8:27. Starts from RO-17's round 2 recipe (`../ro17/`); only the files that differ or
are new are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/RO-14/round1/` (never commit media; the repo is public).
Review page: port 8964.

Order: `roll_sidecar.py build` (lav map, small-model takes) -> lav.wav (dual-mono pan) -> medium.en words (`whisper_words.py`, needs the
project ffmpeg on PATH or it dies with "No such file or directory: 'ffmpeg'") -> Gemini verbatim listen in four 190 s chunks -> `env.py`
level strips at every restart -> `edl.py` -> `shots.py` -> `assemble_audio.py` -> `patch_words.py` -> `words_src_out.py` -> `plan.py` ->
`resolve.py` -> `from_plan.py` dry run (fit) -> `chain_r1.sh` (hair_pre, crop_y, voice fit, graphics render, stills, first minute,
audio gate, hair, context for every item, checks) -> `page_extra.py` + `page.py`.

What is new here:
- **`env.py`: a 20 ms level strip of the lav** (`' '` under -50 dB, `.` -40, `:` -30, `#` louder) with a time ruler. Medium.en folds a
  restart into ONE stretched word (`told` 4.0 s, `can` 4.7 s, `she's` 2.5 s, `and` 3.0 s): the strip shows the silence and the second
  attempt's onset inside it, which is where the piece starts (hand override in `edl.py`, 80 ms before the onset).
- **`patch_words.py`: the words of the second attempt are lost inside the stretched word**, so a phrase like "I was 200 pounds" does not
  resolve and the SRT would be wrong. It re-transcribes each folded region with medium.en and replaces the overlapping words; Whisper
  drops the region's first word, which is added by hand from the strip (`words.json` marks every patched word).
- **gfx: `week_card`** (the weekday deficit bars going down, then the weekend bars going up, each on its word, a running total that
  counts back to zero), `study_card` bars from the plan, and `recap_card` items on their words, with an optional picture bled in on the
  right (a three-item list alone on the field looked empty) and five items laid out 3 + 2.
- **`resolve.py`: two cutaways less than 0.5 s apart after a length cap** close up (the later one starts where the first ends), or three
  frames of Dan flash between them; and `reveal_days` / `reveal_items` resolve like the swap card's rows.
- **`crop_y.py`** writes RO-17's per-shot hair lift as a script (lowest hair top in the shot minus 4 % of the crop height; lift only).

Traps this round paid for:
1. **Every take of the intro says "five hidden reasons"; the video gives four.** Cutting the word "five" on measured troughs (-52 and
   -47 dB) still sounded choppy: a blind Gemini listen scored the edited clip 2/10 against 10/10 for the original. A stressed word mid-
   phrase cannot come out. Fix: a pickup on the next shoot list, laid under a full-screen card so it needs no picture.
2. **Medium.en and Gemini disagreed on which "30 days of honest tracking" copy was clean.** Gemini's timestamps in that chunk were off by
   seconds; medium.en's word times showed the re-said copy swapped words ("you will be actually able"). Trust word-level times for
   which copy, Gemini for where restarts and noises are.
3. **Back-to-back lower thirds and signposts that read for under a second:** a "Leak #2" label whose point lands on its own words gets
   0.4 s before the next cutaway. Signposts land with the strip (part phrase = the item's start phrase); measure every lower third's
   last part to its fade from `hf/beats.json` before rendering.
4. **`buildcap.wait()` needs a label** (`wait('RO-14 x')`); called bare it raises and the next command runs anyway, taking a third slot.
   Two of my own waiters released at the same moment would also take two slots: chain your own heavy steps, do not queue them side by side.
5. **Pexels photo downloads:** `www.pexels.com/photo/<id>/download/` returns HTML to curl; use
   `images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?w=2400`.
6. **Plan colours from JSON are lists**; PIL wants tuples (`study_card` bars).
7. **The frame gate on waist-up AI frames (framecheck, first used here 2026-10-14).** Its `person` block always runs the leg-bone
   row, and on a frame with the legs out of shot (pose visibility under 0.15) that row measures nothing and fails. Leave `person`
   out and declare each person as a `may_change` box instead (the static row then checks the room); the frame reviewer judges the
   bodies. Declare props that legitimately move (a scale lifted, coins and shards, a plate slid) the same way, and put the things
   that must not move under `still` (the salad bowl, a candle, glasses, the pizza).
8. **The independent frame reviewers caught five faults in seven pairs that the gate passed** (each a fresh `frame-reviewer`):
   a donut in front of the taken one lost its top half; the salad changed into a different salad; the scale shrank to tablet size
   and his feet stood where it lay; a pizza slice came from a whole pizza, then from two odd gaps, then the hammer changed shape;
   the cake slid onto the salad's spot and shrank, and a fork appeared next to two spoons sharing one handle. Two were repaired in
   code by pasting START pixels back over a feathered mask (`ai-frame-prompts/A5-end.repair.txt`, `A6-end.repair.txt`; repaired
   frames still get a fresh gate and review); the rest were redrawn, and one whole pair was remade because the fault was in START.
   Write "the SAME <object>, the same size" and "nothing appears or vanishes" into every END prompt, and give a prop that will
   move a place to come from in START (the fork on the plate).
9. **`checks.py` side-card clearance can fail on a mask speck**: a 47 px blob at the frame's bottom edge (the light tube's base)
   read as the person's left edge, 440 px under the card. Open the flagged mask before acting; the person component was 226 px clear.

Round 2 (2026-10-20):
10. **The 10/15 pickup on the 9/23 film (`round2/recipe/pickup.py`, `round2/pickup/match.py`).** Same lav, different set: the 9/23
   voice measured about 20 dB darker above 5 kHz. Fix: an iterated 1/3-octave linear-phase match on active speech (threshold
   relative to each file's 95th percentile; an absolute -40 dB threshold biased the fit by 10 dB), level-matched, then the film's own
   chain. The window [16.62, 26.06) keeps the film's pauses, so the film length and every later item are unchanged; G02 starts on the
   pickup (`start_t`) and G01's render is simply cut at the card (manifest `b` only, no re-render).
11. **A blind Gemini A/B cannot judge a splice that sits at a script break.** With the SAME original clip on both sides it still
   "found" a different-day splice at the line break, 100 % confident. Judge pickup joins on measurement (pickup vs film distance
   against film vs film) and by ear; never by that listen alone.

Round 3 (2026-10-22, `round3/`):
12. **Veo/Omni cannot lift a scale off the floor cleanly.** About 30 takes across Veo Fast, Quality, Omni and paid failed the same beat:
   the foot sits inside the scale corner and the scale is lifted out through it, or the display doubles. A START-only prompt with "both
   feet a full foot behind the scale" did not help. Fix: two shots joined by a cut, the lift off screen (shot 1 ends on the grip,
   shot 2 cuts in on him already holding it). Plan any pick-up-from-the-floor gag this way from round 1.
13. **The approved START and END frames can show different-looking men.** Shot 2 generated from the END frame failed review at the cut
   (different face, hair, build). Make every shot of a multi-shot AI clip from the SAME frame (here the START frame), and use a later
   window of a take for the second shot.
14. **Veo 3.1 Fast creeps the camera 2-5 % over 8 s even with "locked off on a tripod"; Omni 1.1 Flash held it to 0-1 px.** For a
   locked-camera shot prefer Omni windows, or lock a Veo take with `round3/stabilize.py` (background similarity fit; align to the
   frame with the most head room; extend edge pixels only where the edge is plain wall, else an anchored zoom). Measure hair after it.
15. **A 1.35x cut-in on a 720p-upscaled AI take reads soft next to the wide shot**; 1.2x passed the reviewer.
16. **`build.py` writes the graphics-free base to `W/tmp_base.mp4`; `finish.py` declares `final/base.mp4` as the watch pass's
   `source_picture`.** Move it beside the master before the watch pass, or graphic presence reads NOT MEASURED (0/43).
