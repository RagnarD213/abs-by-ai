# Green-screen backgrounds: the template for reaction and commentary videos

**Dan, 2026-10-24 (RO-24 round 2, after two mockup sheets):** *"I like all of these except for number 5, the TV studio build.
What I'm thinking is I would like you to cycle through all of these options where it's appropriate in the video... right
after the intro clip, the floating cards, or the pictures scrolling through... When we find clips throughout the video,
occasionally put me to the side while the clip plays in the background. The numbers, I feel like, are appropriate when we
mention the numbers... always keeping the background visually interesting, always changing up the background... establishing
a template for making these visually interesting."* Earlier, same review: *"we can't just have a white background the whole time."*

Binds every green-screen reaction or commentary video, Claude and Codex (memory `green-screen-background-cycle`). First film:
"Reacting To Celebrity Ozempic Transformations" (RO-24), round 3 (recipe: `longform-edit/reference/ro24/round3/`). Mockups Dan
approved: `/Volumes/Expansion/_edit_work/RO-24/round3/mock/background_options.jpg` and `background_options_2.jpg`.

Status: **built 2026-10-25, shown to Dan in RO-24 round 3; not yet locked by Dan.** Record his verdict here when it comes.

**Scope (2026-10-25):** green-screen long-form commentary and reaction films with several backgrounds. Reaction SHORTS keep
the locked Bill Maher Codex R5 format (VIDEO-RULES, "Reaction videos: the locked format"); this template does not replace it.
Codex owns green-screen editing from 2026-10-25 (same section): Codex uses this module as is, through the same plan format.

## The types (Dan's numbers from the mockups)

| # | type | what is behind Dan | Dan | use it when |
|---|---|---|---|---|
| 1 | `soft` | their clip (muted) or a photo, blurred, darkened, navy-tinted | centre (W/T) | commentary; a left-third card is up; a stretch under 2.5 s |
| 2 | `corner` | their clip full screen, muted, still rolling after it played with sound | lower-right corner, talking | right after their clip played |
| 2b | `side` | their clip full screen behind (zoomed so they sit left), a little softer on his side | right (W/T) | "occasionally" while a clip exists (at most one in four segments) |
| 3 | `wall` | a wall of photos scrolling slowly, alternate columns up and down, darkened | centre | right after the intro (after the cards) |
| 4 | `panel` | their before / after pair, name, weight lost + medication (HyperFrames) | right | he talks about how their body changed |
| 6 | `cards` | tilted photo cards with white borders drifting on the Soft Blue field | centre | right after the intro; a person's photos when he talks about how they look |
| 7 | `bigtype` | the number and the drug, huge and faint, sliding in (HyperFrames) | right | he says a number no lower third already shows |
| 8 | `set` | the realistic studio set (one Codex plate per film); its TV plays their clip or shows a pair | right | longer commentary |

Not 5 (the flat built TV wall): Dan rejected it. Full-screen items (the clip with its own sound, photo scenes, cards, B-roll)
sit between background segments and are not backgrounds.

**Placement** (`gsbg.affine`, output pixels, from the house-key plate 2880x1620): centre W = the plate scaled 2/3; centre T =
round 2's tight window (0.74 of the width, hair 4 % of the window below the top); right W = W moved +346 px (round 2's S
framing); right T = the tight scale with his head centre at x 1330; corner W/T = scale 0.48 / 0.65 (1.35x apart, the
same step as W/T; 0.56 / 0.64 read as a jump cut in the RO-24 R3 review) with the head centre at x 1580 / 1505 and the hair
top at y 490 / 400, lower right as in Dan's approved mockup 2. Every shot keeps
one fixed placement (horizontal footage stays still); the round's W/T alternation at every cut is kept, so a cut still changes
the framing. Where the camera's own frame edge lands on screen (right, corner) his alpha gets a 22 px soft edge.

**Camera-locked types** (`soft`, `set`): a tight cut zooms the background with him, as a real camera would (`gsbg.camera`).
The others are screen graphics and stay put.

**Light match on the set (8):** Dan 12 % dimmer and a touch cooler, a blue rim on his edges facing the set's blue lamps (left)
and a warm rim facing its floor lamp (right), a 1.3 px depth-of-field blur on the set. The set is an AI picture, so it carries
the AI-GENERATED chip (top left) while it is on screen (`ai_label: false` in a segment turns it off if Dan says so). Its TV
shows 2-4 steady stretches of 3 s or more (a TV flipping every second reads as busy). The set plate is one Codex image for the whole film (RO-24: `round3/mock/set_plate.png`, TV screen measured as the
largest near-black rectangle, `SET` in the film's assembler).

## The rules (`planner.py`)

1. The background changes only on a picture cut, about every 8 to 20 seconds (whole shots grouped; a short tail joins the
   segment before it).
2. The type follows what he says, in this order: a left-third card is up → 1; right after the intro → 6, then 3; right after
   a clip played with its sound → 2 (the clip keeps rolling, he reacts from the corner); he says a number no lower third
   shows → 7; he talks about how someone's body changed → 4; a clip exists → 2b occasionally, else 8 or 1; otherwise 8 or 1.
3. Never the same type twice in a row.
4. No photo or pair repeated where it can be avoided (the planner hands out the least-used first; credited photos go where a
   credit line shows, uncredited agency photos only in walls, cards and the set's TV).
5. Muted footage behind Dan comes from clean, STEADY windows of the person's clip: no burned-in quote box, chyron, product
   shot or transition behind him, and no flashing red-carpet cameras (a whole-frame pulse 6-16 times a second behind him read
   as strobing in the RO-24 R3 review). Download the full source video; set window edges on scene detection; scan each window
   for brightness jumps (more than 8/255 between frames, under about 1 a second); keep the logo/bug off him with the zoom.
7. Photos: every tile and card unique where the pool allows. The wall builds only the tiles that come on screen during the
   segment (it scrolls a little slower rather than add a row it cannot fill uniquely) and deals them so any unavoidable repeat
   lands in a far column. A wall or card set right before a person's own photo scene leaves that person out, and a wall right
   after a card set leaves out those cards.
9. Footage behind the corner keeps the source's logo bug out of Dan's corner (zoom, and out_focus that crops the bottom).
8. Big type lands on the words: `line_times` (film seconds) per line; the drug can show from the cut, the number on the number.
6. Overrides: the editor's calls where the rules allow two answers go in the film's `bg_overrides.json`, each with its why;
   the plan records "(editor's override)".

## Plan format (`bg_plan.json`)

```json
{"segments": [
 {"id": "BG04", "t0": 73.81, "t1": 84.72, "type": "panel", "person": "Sharon Osbourne", "why": "...",
  "pair": {"photos": ["before.jpg", "after.jpg"], "years": ["2021", "2025"], "credits": ["...", "..."], "crop_k": 6.0},
  "name": "Sharon Osbourne", "stat": "42 lb, Ozempic", "mov": "bg/BG04.mov"},
 {"id": "BG05", "type": "side", "clip": {"src": "clips/src/sharon_full.mp4", "windows": [[52.0, 57.9], [66.0, 71.9]],
  "zoom": 1.22, "focus": [0.47, 0.42], "out_focus": [0.33, 0.44]}},
 {"id": "BG06", "type": "bigtype", "lines": ["2.5 MG", "OR LESS"]},
 {"id": "BG07", "type": "set", "clip": {"src": "...", "windows": [[6.0, 7.9], [36.0, 37.8]]}},
 {"id": "BG01", "type": "cards", "photos": ["...6 photos..."]},
 {"id": "BG02", "type": "wall", "photos": ["...about 24..."]}]}
```
Times are film seconds; paths resolve against the plan's folder. `clip.windows` play one after another and loop.

## Files

- `gsbg.py`: the presenter placement (`affine`, `visible`, `Presenter`: ffmpeg crops, premultiplies and scales the plate
  straight to its screen rect, unpremultiplied here so the grade sees true colour), the locked grade and light wrap
  (`compose`, from comp16), and the types (`make_background(seg, ctx).frame(i, cam)`).
- `hfbg.py` + `templates/panel.template.htm`, `templates/bigtype.template.htm`: the two text types as opaque HyperFrames
  renders (moving field included). Big type is drawn on a canvas: it is a deliberately faint texture, so the readable-text
  contrast check does not apply to it.
- `planner.py`: the rules above, `FACTS.json` -> `bg_plan.json`.

## Applying it to a film (RO-24 round 3 is the worked example)

1. Key once (house key, `chroma-key/README.md`); keep the plates. Never re-key for a background change.
2. Write the film's facts (shots on the final timeline, full-screen inserts, who he talks about, numbers, transformations,
   clip windows, photo pools): RO-24 `recipe/facts_r3.py`. Run `planner.py`, read every line of its output, put the editor's
   calls in the overrides.
3. `hfbg.py PLAN OUT --only <panel and bigtype ids> --snap`, look, then `--render` (through the render queue).
4. One still per segment through the real assembler before any long render (RO-24 `recipe/stills_r3.py`: one plate frame
   each, about 2 minutes for ten). Fix placement there.
5. Render the section through the queue (`renderq.py run --group <JOB> -- bash chain.sh`). The assembler measures the hair
   top on every rendered presenter frame against the background it drew (>= 20 px, VIDEO-RULES 2026-10-20) and skips the
   plate decode under full-screen items.

## Cost (measured 2026-10-25 on RO-24, a busy Mac)

The plate decode dominates: FFV1 16-bit 2880x1620 costs about 0.45 core-seconds a frame. The RO-24 2:50 preview (3,042
presenter frames, 2,069 under full-screen items) rendered at 2.9 frames a second in one heavy slot on a Mac running four other
edits (29 min). A fix to a few background stretches re-composes only those (`assemble_r3.py --reuse OLD --redo BG03,BG05`:
everything else is copied from the earlier render) at 5.7 frames a second. Looks are tested on stills and 10-15 s windows
(`--g0/--g1`), never on a full render. HyperFrames backgrounds render at about 7 s per second of screen time.

Trap (2026-10-25): a 1-frame-per-2-s contact sheet made with the `fps` filter can show a frame up to a second later than its
label, so muted-footage windows picked from it started on the wrong shot (an Ozempic box behind Dan instead of Sharon). Pick
windows from ffmpeg scene detection (`select='gt(scene,0.25)',showinfo`) and check the first and last frame of each window.
