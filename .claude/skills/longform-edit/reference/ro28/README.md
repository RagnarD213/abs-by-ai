# RO-28 "Why Zepbound Improves Your Health Even If You're Ripped" (10/15 C1771): round 1 recipe (Claude Opus 5.5, 2026-10-20)

First Claude film on the **10/15 studio set** (dark green backdrop, two cyan tubes, desk; Codex cut RO-25/26/27 there). One 10:18 roll,
cut to 6:26. Starts from RO-18's round 1 recipe (`../ro18/`); only the files that differ are kept here. Work dir (Extreme was full, 66 GB):
`/Volumes/Expansion/_edit_work/ro28/round1/` (`/Volumes/Extreme/_edit_work/ro28` links to it). Never commit media.

## The set (measured)
- Lav left channel only (`pan=mono|c0=c0`); room tone for joins C1771 51.0-54.3 s (-54.9 dB, steady).
- **Hair top: 84 px from the top of the 4K frame at its highest** (person mask every 0.5 s of the whole roll, `framing/hair_roll.json`,
  verified on a native frame). So W2 (3552x1998 @144) sits at y 0-21 and T2 (2704x1521 @568) at y 9-42 per shot (4.5 % + 6 px), never the
  RO-25 y 80 / 50 (RO-27 R1's clipped-hair rejection came from fixed y). `framing/crops.json` + `crop_y.json`; `frames.py` reads both.
- No room to slide the crop left under a side card (Dan's left edge sits at x 978-1180 of 3840): `build.all_segments` cards take W2 + wall
  stretch only.
- Colour options: A Rich Balanced (the approved RO-25 grade, recommended), B RO-27's Richer, C A + warm skin (`frames.GRADES`).
- Voice: RO-27's "warm bass" EQ (Dan's 10-20 pick on this set) came first in 11 blind Gemini listens (5.7) over warm bass + 3 dB at 120 Hz
  (5.5), untreated (5.0, room heard 7/11) and the chain default (3.7). `audio_options28.py`, `listen_trials.py`.

## Traps this round paid for
1. **The render queue: wrap the whole HyperFrames pass as ONE `renderq.py run --group` step.** `from_plan.py --render` alone queued each of
   27 graphics separately (#23 in line for the first one); the wrapped job got its slot once (after 112 min on a busy night) and rendered all
   27. Once a group is running, its next wrapped step is near the head of the line.
2. **Lower-third topics come out UPPERCASE unless every `lt` item carries `topic_case="preserve"`** (16:9 template default is upper;
   VIDEO-RULES 2026-10-16 says title case, never auto caps). Caught on the stills; 14 lower thirds re-rendered.
3. **Side-list headings wrap past about 13 characters at this size** ("Abs Lower Your Risk / Of", "What It Helps / Prevent"). from_plan's fit
   check does not cover l3 headings; read the stills.
4. **Fact-card copy limits (before-card, 16:9):** eyebrow about 20 characters at 64 px, headline about 15 at 84 px, detail about 30 at 46 px.
   from_plan asserts them; a count needs the headline to START with the number, and the phrase must match the token ("58%" not "58").
5. **`patch_words.py` region edges drop real words** that start just before the region ("diabetes", "by"); re-add by hand (`word_fixes.py`)
   and print film-time sentences after every patch.
6. **Pexels 9902352 ("man taking pill with water"): the drinking shot reads as red wine.** Use its first seconds (pill in an open palm).
   Library B0015's tube rack carries a brand name ("A-PRF").
7. **Dan's 10/15 pool B-roll is a wide shot (Dan about a quarter of the frame): crop the source window** (`crop=(w, h, x, y)` on a clip item,
   `gfx.clip_vf`), keeping headroom above his hair (person-mask box per roll in `framing/broll/`). Jump rope and squats need the whole body.
8. **A Gemini whole-cut junk listen called a natural 0.6 s pause inside "72% ... of American adults" an unnatural join.** It was one
   continuous take (level strip); check the EDL before cutting on a listener's word.

## Round 2 traps (2026-10-21)
9. **Motion spec boxes must be in the TAKE's pixels.** Codex frames are 1672x941, Flow takes 1920x1080; clipcheck failed every take until the
   boxes were scaled (x1920/1672, y1080/941) into `motion/*.take.spec.json`.
10. **A prop resting on a moving body (laptop on a lap) is not "still".** It rides his breathing and fails a still box by 5-9 px; drop it from
    `still`, note why, and have the reviewer check it by eye.
11. **Regenerate after a reviewer FAIL, never argue it.** A1 t1/t2 (both people looked into the lens, plastic face) and A5 t2 (startled, late
    wave) failed; tighter prompts (A1b, A5b: "never looks at the camera", "smug from the first frame") passed first time.
12. **from_plan's lower-third fit check missed a too-long point** ("...Even If You're Already Ripped", 1759 px of 1632) and the render died.
    Count before rendering; shorten or shrink.
13. **Copying a round folder and sed-ing `round1` -> `round2` makes from_plan re-render every before-card** (the photo path is in the
    config, so its hash changes) though nothing visible changed. Before queueing hours of scene cards, diff the configs with the folder
    name masked; if identical, reuse the previous round's renders (`round2/logs/hf_r2.log`).
14. **Expansion's 3-slot drive cap sat full for hours** with other editors' long jobs. A graphics pass can run with `--out` on the internal
    scratch (`renderq.py scratch`) and rsync back (`recipe/hf_r2_int.sh`); unchanged renders are recognized there too. Use `GATE_PRIORITY=1`
    only while Dan waits on the result.
15. **Never stretch a short AI take to fit a line.** Repeats during motion stutter, a slowed still stretch reads frozen, 1.25x reads rushed;
    four retimes of A5c failed review. Generate takes whose usable natural stretch is at least the slot length (Quality model was calmer than
    Fast here), and check the background objects too: A5d t1 failed only on a lamp drifting 5.5 px during the gesture.
16. **Start-frame-only generation avoids an end frame's baked-in expression** (A1's approved END had an open-mouth gasp the reviewer
    called cartoonish); the takes then drift toward the camera late, so pick the range before that.

## Round 3 traps (2026-10-22)
17. **A film with Dan on camera under half its runtime (47% here) leaves every framing row NOT MEASURED** ("palette never settles"):
    the programme-median palette is not his scene. Declare `talking_head_windows` (uncovered punch pieces, full-frame rect) with
    `evidence_contract` {version 2, video_sha256 of the exact master} in `finish.py`.
18. **A take join under a side card is a jump cut when the card forces one framing.** With the card on the left and Dan right of
    centre, a T2-size crop slid left in 4K (`T2R` = 2704x1521 @ x145) keeps him ~300 px clear; `allow_t2=True` on that card lets the
    framing solver use it (`build.all_segments`).
19. **A side card ending one frame before a clip leaves a 1-frame presenter flash** (`cut:min_segment`); resolve.py now starts the
    clip on the card's end when the gap is under 0.2 s.
20. **Full-film true peak read -0.7 dBTP** though the first minute read -1.9: finish with a 4x-oversampled limiter
    (`declick.py`). The tone row fails on the approved warm bass (known; RO-14 and RA-15 shipped the same way).
21. Flow takes on this set: start+end frames on Fast worked for A2/A3 (people talk less when the END pose is fixed); the trims that
    passed are A2 t1 f36-187, A3 t3 f90-187 (t3 smears at 188).

## Round 4 traps (2026-10-23/24)
22. **Measure a B-roll grade through the build path (`gfx.clip_frame`), never on a hand-built test chain.** The build applies the grade
    to the decoded YUV frame before `format=rgb24`; my test chain converted to RGB first, so a grade that measured 9% black / median 69
    rendered at 5.5% / 75 (washed out), and the one before it crushed to 25% black. Target the film's own approved pool clips
    (C01/C05/C12: 10-17% black, saturation .27-.38, median 55-71); C07 passed at 11% / .39 / 61 (`POOL_SHADE`).
23. **A "click" on an audio join can be a 0.2 s breath, not the next word's onset** (6:17.5: burst 377.51-377.71, "Thank" at 377.87).
    Read 5 ms levels across 0.5 s before deciding; fill a breath with room tone (`roomfill.py`), blend only a ~10 ms tick (`declick.py`).
