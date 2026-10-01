# HyperFrames templates (Soft Blue Light motion layer)

HyperFrames renders our GRAPHICS as transparent ProRes 4444 overlays; the cut, grade, audio chain, gates and delivery
stay in our own pipeline. Setup, pinned version (0.8.97), PATH note and CLI commands: `Media/hyperframes/README.md`.
Research and decision: `Docs/HYPERFRAMES_RESEARCH.md`. Style lock: [../SOFTBLUE.md](../SOFTBLUE.md),
[../GRAPHICS-STANDARDS.md](../GRAPHICS-STANDARDS.md).

| Template | Status | Use for |
|---|---|---|
| [`cycle/`](cycle/) | **Approved by Dan 2026-09-30** (C1652 pilot) | a 4-step loop / vicious or virtuous cycle, and its reversal |
| [`lower-third/`](lower-third/) | **Approved by Dan 2026-09-30** (RO-16 G04 sample) | Motivation lower third; parts land on words; optional counter bar (long way vs short way) |
| [`before-card/`](before-card/) | **Approved by Dan 2026-09-30** (RO-16 G02 sample) | full-screen photo + glass fact card on the live field; number count-up |
| [`side-list/`](side-list/) | **Approved by Dan 2026-09-30** (RO-16 G20 sample) | the 3A left card; items land on their words |

Round-2 samples, beat sheet, bases, compositor and review page: `Media/hyperframes/round2-templates/`
(`BEATS.md`, `bases.py`, `composite.py`, `clearance.py`, `page.py`); heavy media in `/Volumes/Extreme/_edit_work/hyperframes-r2/`.
Shared plumbing for the three: [`hfbuild.py`](hfbuild.py) (make_scene, lint + check, render; text placement matches PIL).
Whole-video pass: [`from_plan.py`](from_plan.py) (plan + words -> configs -> renders), [`composite.py`](composite.py)
(compositor), [`checks.py`](checks.py) (clearance, face, fill). See "One graphics pass for any video" below.

Round 2 (lower third, before card, side list) approved by Dan 2026-09-30: "All three approved." Each `build.py`
docstring has its config format; the approved configs are the `example-ro16-*.json` beside it.

## One graphics pass for any video (2026-09-30, first used on RO-10)

1. **`from_plan.py`** reads the video's resolved plan (`plan_resolved.json`: items with `t0`/`t1` and their copy) and its
   mapped words (`words_out.json`: `w`, `t0`, `t1` on the film timeline), and writes one config per template scene, then
   renders them: `python3 from_plan.py --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render`.
   Kinds: `lt`, `scene` + `scene: "fact"`, `l3`, `cycle`; every other kind is ignored (it stays `softblue.py`). Inside an
   item every time is a PHRASE Dan says (`parts: [["7 MONTHS.", "seven months"]]`, `reveal: ["beef jerky", ...]`), resolved to
   its first word's start. Field list in the docstring. It asserts the copy fits (the lower third and the fact card are
   one-line nowrap layouts) before rendering, skips a scene whose config and template are unchanged, and writes
   `hf/manifest.json` (what the compositor needs) and `hf/BEATS.md` / `beats.json` (the beat sheet for the review page).
   Side-card edges snap to a shot join within 0.7 s; do the same snap in the video's own resolve so both agree.
2. **`composite.py`** composites every overlay into the film in RGB. In a video's per-frame render loop:
   `C = Compositor(json.load(open("hf/manifest.json")))`, then `frame = C.apply(frame, g)` where `g` is the film frame index
   (an opaque fact card replaces the frame). It decodes renders as BT.601 and bases by their own tags, blurs the base
   inside a lower third's `_mask` alpha (GaussianBlur 14), and replaces exactly `fr(b) - fr(a)` frames for an opaque scene.
   CLI for a finished base: `composite.py manifest.json --base base.mp4 --base-t0 <s> --out out.mp4`. Proven against
   round 2: it reproduces the approved G04 composite at 69 dB.
3. **`checks.py`** verifies a rendered composite (the film or a context clip): Vision person mask right of every side card
   (clearance), Vision face box above every lower third (`facebox.swift`, compiled on first use to `~/.cache/absbyai/`),
   and the card fill as the compositor decodes it (10,38,72 +/- 2, alpha 232) with the composite reading beside it (the
   91 % card lets about 3 levels of footage through, which is correct). Reproduces round 2: G20 78 px clearance.

**Framing under side cards (RO-10 recipe `build.py all_segments`).** A global W/T alternation cannot place side cards:
fix one card's exit and the next shot flips too. Solve the whole film instead (dynamic programming over every picture
segment, 2 options each): a join is a jump when the two framings are within 1.2x in size (W2/W2, and W4S/T2), unless a
full-screen item covers one side; cards prefer W4S (the W4 crop slid left inside the 4K frame) and fall back to W2 + wall
stretch where the slide would force a jump.

## Dan's verdict on the pilot (2026-09-30)

*"This is looking significantly better than the graphics that we're using. This really shows me the potential. This is
approved."* On layout: *"it's a little bit better the way you did it because of the content of the graphic. It's a
little bit empty when it's full screen, but this... does make a lot of sense in the left third graphic."*
So: a diagram of four short items goes in the LEFT-THIRD card with Dan on camera beside it, not a full-screen scene.

## The cycle template

`python3 cycle/build.py config.json OUT_DIR --render` (config format in the file's docstring; the approved example is
`cycle/example-c1652.json`). Each scene becomes its own HyperFrames project, is linted and checked, then rendered to
`OUT_DIR/<id>.mov`. Reference build with base footage, composite and review page:
`Media/hyperframes/pilot-c1652-spiral/` (`BEATS.md`, `composite.py`, `page.py`, `base/build_shift.py`).

**Which words drive it** (all times are the word's start in the finished film, from `mapped-words.json`):
- `a` / `b`: the graphic's in and out. Put them on existing shot boundaries so the reframe (below) hides in a cut.
- `reveal` (build scene): each box lands on the word that names it, in speech order, not loop order.
  Arrows draw themselves automatically once both of their boxes are on screen (0.2 s after the later box, 0.3 s apart).
- `close`: the word that sums the loop up ("downward"); the last arrow draws. `pulse`: the next stressed word
  ("spiral"); one pulse, then a light travels the loop until the exit.
- `flip` (flip scene): each box turns over to its opposite on its word; `title_swap` is the first word of the turn.
- `hue`: `red` for a bad loop, `teal` for a good one. `direction`: `cw` or `ccw`; a reversal flips the direction.

**Geometry and colours** (ported from `softblue.py`): card x36 y42, 740 x 488 (3A is 716 wide; +24 px so a 22-character
title fits one line at 56 px), fill (10,38,72) at 0.91, border (99,176,224) at 0.706 2 px, radius 32, title LT_CYAN
Poppins Bold 56, white divider 3 px. Boxes 278 x 104, Poppins Bold 28, fill (6,20,40) at 0.96, 2 px hue border.
Red = B.BAD (235,64,64); teal (45,212,191). Arrows 4 px round caps, chevron heads.

**Easing values** (Nate Herk's table, kept quiet for Soft Blue Light):
| motion | value |
|---|---|
| card enter | fade + rise 24 px, `power2.out` 0.40 s |
| card exit | fade + drop 10 px, `power2.in` 0.33 s, ends exactly on the out cut |
| title words | rise 22 px, `expo.out` 0.42 s, 0.08 s stagger |
| divider | scaleX wipe, `power2.out` 0.45 s |
| box land | scale 0.88 + rise 18 px, `back.out(1.4)` 0.5 s |
| box flip | rotateX to 90 `power2.in` 0.17 s, swap, from -90 `back.out(1.4)` 0.42 s |
| arrow draw | stroke-dashoffset, `power2.inOut` 0.42 s; head pops `back.out(1.5)` 0.22 s |
| pulse | scale 1.045 + glow 34 px `power2.out` 0.22 s, settle `back.out(1.4)` / `sine.inOut` |
| travelling light | constant speed, 2.6 s per lap |
| always drifting | diagram sinks (bad) or rises (good) 12 px over the scene `sine.inOut`; specular line sweeps the top edge; soft light drifts inside the card |

## Placing Dan beside the card (the reframe)

Dan must sit right of the card with his arms clear. Do not stretch the wall (`shift_presenter`) when the roll has room:
slide the approved crop window LEFT inside the 4K frame, same size, same y, same grade, only while the card is up
(`base/build_shift.py` in the pilot: FAR x 239.7 to 0, NEAR x 327.7 to 117.5, both a 322 px move). Check every 10th
frame of the composite for hands crossing x = 776 (pilot minimum clearance about 120 px).

## Composite

The overlay is transparent, so the glass cannot blur the footage; the card is 91 % opaque, which makes that invisible.
`ffmpeg -i base.mov -i scene.mov -filter_complex "[1:v]setpts=PTS-STARTPTS+OFFSET/TB[o];[0:v][o]overlay=0:0:eof_action=pass:format=auto" ...`
where OFFSET is `a` minus the base clip's start. Verify frame alignment against the approved film on the untouched
frames (pilot: 43 dB PSNR).

## Rules that bit (HyperFrames 0.8.97)

- **Renders are UNTAGGED BT.601 limited range.** Decode them as BT.601 (`scale=in_color_matrix=bt601:in_range=tv`) or the
  navy shifts (3A fill reads 7,37,75 instead of 10,38,72). Our bases are tagged BT.709. `round2-templates/composite.py`
  composites in RGB with each file decoded by its own matrix; an `overlay=format=auto` in YUV mixes the two.
- **Glass over footage:** a transparent overlay cannot blur what is under it. `lower-third/` renders a second `_mask`
  pass (strip shape, white 92 %, same motion); the composite blurs the base (GaussianBlur 14) inside that alpha, then
  lays the content pass (tint 0.54, hairline, text) on top.
- **Match the source's own round trip.** RO-16's base goes through an H.264 yuv420p file before paint; decoding the grade
  straight to RGB came out 4.5 levels brighter (38 dB). Replicating the round trip gave 43.8 dB against the draft.
- **Reframe room:** slide the crop only where the 4K frame has room (RO-16 W4: 520 px, yes; W2: 144 px, no). Where it
  has none, keep that video's existing wall stretch rather than zooming in past the shoulders.
- Text: `line-height: 1.4` + `top: y` puts Poppins on PIL's baseline (ascent 1050 / descent 350). Measured within 4 px.

- One root composition per folder; a timed `.clip` wrapper with nested content warns. Plain divs + one paused timeline.
- `@font-face` to a file inside the project, or lint fails.
- `fromTo` for every initial state; finite `repeat` only; motion along a path = proxy object + `onUpdate`.
- `check` shows "0/0 text checks" on a transparent overlay; judge contrast on composite stills.
- Render speed about 5 to 6 s per second of 1080p overlay.
