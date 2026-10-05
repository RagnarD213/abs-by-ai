# RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat" (8/14 poolside, C1614-C1629): round 1 recipe (Claude Opus 5.5, 2026-10-03)

First long-form in this recipe family cut from MANY rolls, outdoors, from a 1080p source. Round 1 is the cut and the
look only (colour, framing, sound); graphics and clips join in round 2 from `../ro13/` (`plan.py`, `resolve.py`,
`gfx.py`, `stills.py`, the plan loop in its `build.py`). Work dir and media: `/Volumes/Extreme/_edit_work/ro02/`.

Order: lav per roll from each roll sidecar's measured filter -> `edl.py` (pieces carry their roll) -> `verify_asr.py`
on every splice -> `shots.py` -> `assemble_audio.py` -> `asr_assembled.py` (medium.en) -> `words_out.py` ->
`measure.py` (where he is) -> `skin.py` (how bright he is) -> `grade.py` (colour cubes) -> `frames.py` ->
`lookstills.py` -> `build.py range` -> `hair_first.py` -> `page.py`.

What is new against RO-10/11/13:
- `edl.py`: `(id, roll, in, out, ...)`; the voice threshold is measured per roll (room floor + 10 dB), because the pool,
  the waterfall and traffic put the floor near -55 dB where the studio sat at -65.
- `frames.py`: no fixed crops. FAR (x1.45) and NEAR (x1.80) are placed per shot from `measure.json`: centred on his
  head, top edge 50 / 40 source px above the highest his hair gets in that shot. Fixed inside a shot.
- `grade.py`: the approved poolside colour (Codex organic colour v1: per-channel LUT, matrix, tone curve) is pointwise,
  so it bakes into a 3D cube for `lut3d`. `pre_gamma` is the per-shot exposure trim.
- `build.py`: sizes alternate at every join; the opening size is chosen so the forced shot (the live set, FAR) falls on
  its own turn.

Traps this build paid for:
- **The roll sidecars' whisper-small words are fine for finding takes and wrong for cutting.** It timed a 3 s stop
  inside one word (`for[16.48-19.30]`), put "You" 1.3 s early, and merged a restart in the ending ("That means your
  waist will get... That means your waist will get smaller"). medium.en on the ASSEMBLED cut found that restart. Read
  the assembled transcript end to end before building anything.
- **medium.en alone on a window that is mostly silence invents a sentence** ("in the next video."). Keep verify windows
  on speech, 3 to 6 s.
- **The person mask grows a stray blob on the chimney cap**, 40 px above his hair. Take the largest connected blob.
- **Clouds.** Raw torso-skin luma runs 0.275 to 0.54 across the kept pieces (0.37 to 0.52 on the rolls the colour was
  approved on). One fixed gamma per shot pulls it into 0.38 to 0.50; capped at 0.75 to 1.15. Sun and cloud still differ
  in warmth; that is the light, not the grade.
- **A tightened pause can leave a 1.2 s shot.** `shots.py KEEP` lists pauses that stay (also the teaching pause where
  he shows the nose breath).
- **`grep render` in a `ps` check matches every app's "Renderer" helper.** Grep for the script name.

## Round 2 (2026-10-04): graphics, clips, opener frames, first minute

Order: `frames.py` (half headroom, bottoms held) -> `asr_assembled.py` -> `words_out.py` -> `plan.py` -> `resolve.py` ->
`cardclear.py` -> `from_plan.py` (no `--render` first) -> `round2_chain.sh` (renders, `stills.py`, `review_media.py first`,
`hair_first.py`, audio gate, `review_media.py context|verify`) -> `page_extra.py` -> `page.py`. `softblue.py` is the pinned
copy from `ro13/recipe/`. `page.py` here is now the round 2 page; round 1's is in git history.

What is new against RO-13:
- `build.py`: one solver for a multi-roll film with two sizes. Segments split at shot joins and card edges; two on-camera
  segments either side of a cut must differ (F / N); the live set is forced F; a left card prefers F.
- `frames.crop(card=True)`: a 1080p outdoor source has no wall to stretch and no 4K room, but the F / N windows are
  1276 and 1032 px wide inside 1920, so the window slides left and his head lands at x 1336 of the output.
- `gfx.py`: `opener` (title, two 16:9 AI panels, a red X on each on the heard word, AI chip top left of each panel),
  `anat_card` (drawn torso in the 3A card, each muscle lights on its word), `countdown` (ends on the phone timer's beep,
  found as the 3 kHz onset in the lav), `recap_card` two by two.
- `resolve.py`: `x_ph` / `stage_ph` phrases -> times; `shot=` items live on one shot.

Traps this round paid for:
- **Check a side list over every piece before rendering it** (`cardclear.py`). The step-by-step demo failed by 144 px;
  it became three lower thirds.
- **HyperFrames on an exFAT drive stores each captured frame as a 1 MB file.** A 31 s side list wanted 7.8 GB. Point
  `hf/renders` at the internal disk (symlink).
- **A two-part lower third dropped the space before a part starting with T.** One part fixed it; look at every still.
- **A library clip can be the wrong look.** B0428 (shade, wide) read dark beside this film; the film's own live set won.
- A zsh glob with no match aborts the whole `rm` line, and everything after `&&` with it. Use `find ... -exec`.

## Round 3 (2026-10-04): opener motion and the full film

Order: re-hash `round3-plan/decisions.json` -> Veo 3.1 fast, first and last frame, 4 s each
(`ai-clip-ideas/reference/gen-veo-keyframes.js`, prompts `opener_motion_A.txt` / `_B.txt`) -> contact sheets of every
fourth frame, cropped on the man -> `aiframes/A.mp4`, `B.mp4` (forward then reversed, 30000/1001, 6.8 s) ->
`build.opener_frames` reads them at panel size -> `round3_render.sh` (`dupscan.py`, `clipscan.py`,
`build.render_range(0, total)`) -> `finish_chain.sh` -> reviewer -> delivery gate.

What is new:
- `build._opener_clip`: each panel's clip is decoded once at 850 x 478 and indexed by the film frame. It asserts the clip
  is long enough; it never holds a frame.
- Crunches came back as up, down, up inside 4 s, so the loop is the whole clip then the whole clip reversed. The sit-up
  reaches the top at about 2.3 s and then sits still, so its loop is frames 0 to 62, reversed, then forward again.
- `finish.py`: chapters are the six PART cards plus the recap; the opener's two AI chips are checked at their drawn
  position with a chip rendered at the opener's scale (1.5).
- `round3`, `cache` and `hf/renders` are symlinks to `~/.cache/absbyai/` (the Extreme drive had 2 GB free).

Traps this round paid for:
- **Two Veo submissions in the same second: the second gets HTTP 429.** Submit one, wait a few seconds, submit the next.
- **zsh does not split an unquoted variable into arguments.** Encoder flags go in an array (`"${ENC[@]}"`).
- A start frame's logo (the N on the shoe) is painted out on a COPY (`B-start-clean.png`); the approved file keeps its hash.
- **A restart the transcriber swallows.** medium.en on the assembled cut gave "with belly ... fat" with 3.5 s between
  two words: that gap WAS the first attempt of "However, I see very, very few people with", heard twice on the film. Any
  gap over 1.5 s between two words inside a sentence gets its own 6 s re-listen and a level read before the first minute
  is shown. The independent reviewer found this one on the finished audio; it cost a second full build.
- **A new EDL piece needs rows in `measure.json` and `skin.json`** (keyed by piece). A piece split off an existing one
  copies its parent's rows.
- **The default peak ceiling left -0.80 dBTP after the AAC encode; -4.0 then failed tone.** `--tp -2.8 --oversample 4`
  passed both (in `build.py`).
- **`round3` is a symlink, so `../recipe` from inside it resolves under `~/.cache`.** Chain scripts use absolute paths.
- **The hair check must take the largest mask blob** (the chimney cap read as hair at 0 px on the far framing).
- The delivery gate fails seven rows on this film (see the delivery notes): the silent live set and the poolside
  far/near framing meet studio bounds. Reported, not tuned.
