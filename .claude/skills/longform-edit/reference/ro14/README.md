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
