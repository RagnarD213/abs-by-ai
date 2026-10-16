# RO-17 "3 Healthy Foods That Made Me Fat" (9/23 C1713): round 2 recipe (Claude Opus 5.5, 2026-10-14)

One 11:10 talk roll on the 9/23 studio set, re-edited from scratch to the current standard (the 09-25 queue-pilot draft was
discarded). Starts from RO-13's WORKING recipe on the SSD (`/Volumes/Extreme/_edit_work/ro13/recipe/`) plus RO-11's `gfx.py` and
`titles.py` (section cards with a picture on the right). Only the files that differ are kept here. Work dir and media:
`/Volumes/Extreme/_edit_work/RO-17/round2/` (never commit media; the repo is public). Review page: port 8877.

Order: lav (`pick_lav` map from the roll sidecar) -> medium.en words on the roll (`whisper_words.py`) -> Gemini verbatim listen in
four 190 s chunks (`gemini_listen.py`, `GM=gemini-3.1-pro-preview`, about $0.15 a chunk) -> `edl.py` (last clean take, reason per
piece) -> level envelope at every edge -> `shots.py` -> `assemble_audio.py` -> `hair_pre.py` -> voice fit (`voice_chain.py` on the
whole assembled voice) -> `words_src_out.py` -> `plan.py` -> `resolve.py` -> `from_plan.py` (dry run for fit, then `--render`) ->
`chain_r2.sh` (stills, first minute, audio gate, hair, context for every item, page).

What is new here:
- **`words_src_out.py`: no second ASR pass.** The roll's medium.en words are mapped straight onto the film through `shots.json`.
  A word is kept when 0.08 s (or 60 %) of it lies inside a shot: a midpoint test dropped six join words whose Whisper start sat a hair
  before the cut ("And the third one", "You only get"), and a zero-length word ("Number" before "2, hard boiled eggs") needs its own
  case or a phrase that starts on it never resolves.
- **`hair_pre.py` + per-shot crop lift (`framing/crop_y.json`, `frames.crop(framing, shot)`).** On C1713 Dan stands closer to camera
  at times; the locked T2 crop would have left 12 px above his hair on the opening. Measured every 0.5 s on the source, the crop is
  lifted per shot only where his hair would sit under 4 % of the crop height (never lowered). The segment cache key carries the crop.
- **`review_media.py context_all`: a context clip for EVERY item** (graphics, clips, AI slots), rendered as merged blocks so no frame
  renders twice, each item cut from its block. The blocks are render units only, never joined or shown as a film.
- **`gfx.swap_card`:** the closing throw-out / replace-with card, each row landing on its word (`reveal_left` / `reveal_right`
  resolved by `resolve.py`). `gfx.clip_vf(..., grade)`: a per-clip ffmpeg eq for flat stock (B-roll colour rule, 10-11).
- **`page.py`:** the player floats at the right on a screen 1500 px wide or more; every AI pair shows its name and its context rows
  (when, line before, line under in bold, after, what you see, fallback, cost) per Dan's 10-13 note.

Traps this round paid for:
1. **Eight Codex image jobs at once hit 429 Too Many Requests**; five came back empty. Two at a time with a 90 s retry
   (`aiframes/run_queue.sh`) never failed.
2. **An edited end frame can add furniture.** One can and done's first end frame had a coffee table that was not in the start frame
   and his hand on his stomach (cause-and-effect and belly rules). Say "do not add any furniture or objects" and "hands well away from
   his body" in every end-frame edit.
3. **A stock clip named for the food is not enough; look at what is in it.** Every "snacking at a desk" clip on Pexels shows chips;
   Dan names trail mix there, so those lines got an AI clip or stayed on camera. The one chips clip sits under "Carbs and sugar are
   addictive", where no food is named.
4. **A brand on a stock photo next to a put-down.** The only coconut-water carton photo showed a brand beside "it's sugar water"; the
   carton is a Codex still, unbranded, labelled AI-GENERATED.
5. **Bass lift on this lav:** the lowest band already read 6.2 dB against the reference 5.4 (the "reads full" case), but three blind
   listens ranked +3 dB first every time and never called it boomy, so the standard +3 dB stayed. The gate's tone row fails on it
   (max 3.33 dB), the known mismatch.
6. **The machine was over the two-build cap from other sessions** (load 185). HyperFrames with two workers spawns 12 Chrome
   capture workers; `buildcap.py` does not count them. Use one worker when anyone else is rendering.
7. **Lower thirds whose first part lands 3 s or more after the strip appears** were caught from `hf/BEATS.md` with a small script
   (first-part delay per lower third) before rendering; re-anchor the start on the part's own phrase.

The independent check of the round 2 page (29 findings, all fixed or explained before Dan saw it) added these:
8. **W4S on C1713 shows the backdrop's edge**: two orange spring clamps and a strip of wall at the 4K frame's left edge. A mirrored
   paint-out left visible rectangles; cropping 4 % in (`W4S = 2690x1513 @ 110,183`) is clean and the side cards keep 85 px or more
   of clearance (they had 127-178).
9. **A reframe-only join under a side card** made Dan change size under a static card. `build.all_segments` now skips reframe
   joins (continuous source) inside a card window; framing changes only on the card's own in and out.
10. **Look at a stock clip's frames, not its title.** Pexels "woman checking dry fruits packaging" holds a wrapped loaf of bread;
    "nuts on a person palm" is out of focus and one kind of nut; a "man walking city" clip had readable convention-centre and shop
    signs; a big-box aisle had readable product tags. White powder under "electrolyte powder" reads as sugar.
11. **AI end frames: every object's change needs a visible cause inside the take.** A scoop and a sticker that must move to new
    places teleport; a measuring cup tips itself with no second hand; a knife vanishes when the hand that held it lifts a dome.
    Start the state that does not change already in place (the sticker on the jar), give every moving object a hand, keep
    utensils on the table, and frame a heavier man from the chest up so his stomach is never the centre.
12. **AI placeholder chips go where the action is not** (`chip=((54, 54), "lt")` on a plan item): top right covered the pouring
    hand on the opener and an executive's face.
13. **Lower thirds within 0.8 s of each other blink** (one fades, the next rises). Merge them or move one; the scan is in
    the resolve step's output (`back-to-back lower thirds`).
14. **The frame gate (`_shared/framecheck`, new 2026-10-14) on a talking-head film's AI pairs:** MediaPipe's person mask misses
    most of a person in a dark room or with several people, so the static row reads the people as moving background. Declare each
    person as a `may_change` box in the spec (`frame-specs/`), then `lockstill.py` with the same boxes. In zsh, build the
    `--box` arguments in Python: an unquoted `$BOXES` is one word and lockstill silently never runs.
15. **Frame reviewers catch what the gate cannot:** a cup that turns inside a still hand (twice, so A5 became a pour from an
    already-tipped cup: nothing rotates), a fork that shrank 35 % when set down, a fish appearing in an empty tin. Design pairs
    so every object either holds its pose or is visibly moved by a hand, and repair a single corner with Codex given the START
    as a size reference (`--image END --image START`).

## Round 3 (2026-10-15): AI motion, what it cost (scripts in `round3/`)
16. **Veo prints measuring marks on a glass measuring jug** mid-pour and they vanish again (2 of 2 takes); painting them out failed twice (faint ticks,
    a broken rim line, mushy glass). Prompting "a small, completely plain clear glass water pitcher, no markings, no numbers" fixed it (A3 take 4).
17. **Kling v3 holds hands and props steadier than Veo** (A5 raisins, A7 dome) and gets through Veo's E005 filter, but it pours through glass, outputs
    720p (about 3x softer upscaled; `prep_clips.py` adds a light unsharp) and costs about $1 a take.
18. **`clipcheck.py` cannot see gaze, fill levels, beam angles or markings**; every one of those was caught by the fresh frame reviewer. Budget one or
    two fails per clip, and when a clip keeps failing, use the clean part of a take (A1: 1.9 s of typing; A3: frames 0-84).
19. **429 on submit and E005 filter failures are not billed** (no `video_output_duration_seconds` in the prediction metrics); check before counting them.
20. **Hand-stamped replacement pieces read as stickers** (identical copies, wrong tint, over the bag edge). Edit a 4x crop of the area with Codex and paste
    it back into the approved frame (`aiframes/paste_box.py`).
21. **`pkill -f` matched the parent shell holding the same pattern** and killed a running generation; queue gate runs with `motion/after.sh`.

## Round 4 (2026-10-15): the last AI clip and the full film
22. **A busy four-beat action fits one 6 s Veo take when the prompt numbers the beats** (A10: bite and chew, fork into tin, tin onto the
    sofa back, hands behind head). One take, $0.90, passed the gate and a fresh reviewer; frames 4-101 fill the 4.06 s slot.
23. **A hand-off of a small prop at speed can drop it for 2 frames** (A10 f68-f69: the tin is gone under motion-blurred fingers, then
    fades in on the cushion). The reviewer measured it at 0.33 s inside a blurred move: a note under the playback-speed rule, not a
    retake. Ask for the prop's frames around any set-down in the reviewer brief; the gate's tracking did not flag it.
24. **The Extreme SSD filled to 0 bytes mid-render** (ffmpeg exit 228 = ENOSPC, the first attempt died silently). Render to the internal
    disk: `round3/final` is a link to `tmp/ro17_r4` in the project (mp4 git-ignored), `build.py` takes `RO17_BASE` for the base file,
    and `finish_chain.sh` uses absolute recipe paths because `..` from a linked dir resolves to the link target's parent.
25. **The independent review caught two things every gate passed** (round 4, first render): the AI chip that `prep_clips.py` places by
    heads only sat on the pouring hand of the opener (A3: chip to the top left), and A5's last 1.2 s was a held still after the pour
    (0.07 % of pixels changing): `max_len` 3.40 ends it on the last moving frame. Check chip corners against hands and the moving
    object, and trim every AI take's still tail, before the render. The re-review then caught the same chip fault on A5 (top right on
    the arm tipping the cup), and a third review the same on A10 (his raised arm under the chip in the last second, where no
    full-size corner is clear): 3 of 8 heads-only chip corners failed. A10 got a 3/4-size chip top left (`chip=((40,40),"lt",1.5)`,
    `gfx.ai_chip(u=)`, `finish.chip_png(u=)`). Mask every frame of a clip against the chip box plus a ring before the render.
