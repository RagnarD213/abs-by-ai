# RO-24 round 5 recipe (Celebrity Ozempic: Dan's round 4 notes on the locked template)

Round 5 = round 4's film plus Dan's notes: AI motion for A1/A3/A4/A6/A8 (Flow), new A7 frames, Amy Schumer's abs photo (P8),
the G06 study card with drug names and quit bars, and the pause at 7 DAYS A WEEK. Work dir `/Volumes/Expansion/_edit_work/RO-24/round5/`.

Order:
1. `retime_r5.py`: 19 silent frames off the end of the shot before the cut at round 4 frame 10364 (the pause after "why you
   should too."). Writes `edl_r5.json`, `film_words_r5.json`, `audio/film_voice_r5.wav` (10 ms equal-power seam), `r5_t()`.
2. `facts_r5.py`: round 4's manifest and bg plan moved through `r5_t` (the planner is NOT re-run: every background is
   approved), G06 from `round5/hf/gfx/build_custom.py` (study card gains a `quit` block: short bars on a 0-100 % track),
   P8 from `round5/hf/photos_r5.py` (layout `boxed`: a hand-set crop for a photo with no face), AI inserts from `ai_inserts.json`.
3. AI motion: `veo.py add` per clip, the `flow-veo` agent, then `takespec_r5.py` (round 4 specs are in 1672x941 START pixels;
   Flow takes are 1920x1080: scale every box, set `camera: locked`), `clipcheck.py --frames A:B`, a fresh `frame-reviewer`
   per take, `ai_r5.py` (require_pass, retime to the slot, round 2's AI-GENERATED chip).
4. `assemble_r5.py` / `chain_r5.sh` (full render), `run_checks_r5.sh` (audio gate with round 4's untreated baseline copied
   beside the master, srt, context clips, negscan, gate plan, watch), a fresh `ra-reviewer`, `page_r5.py`.

Traps met:
- Flow credits ran out after 3 clips (36 credits; a Fast clip costs 10 on Ultra). Read `veo.py credits` before queuing and
  plan the order (hook first). Flow refused A1 shot 2's START frame ("Failed to upload") three times: try PNG or the API.
- A take can pass clipcheck and its frame-reviewer and still fail the film review on meaning: A4's man grins at the pasta and
  the bowl ends in front of him, which reads as "about to eat it" over "he stays away from the pasta". Brief the take reviewer
  with the line and ask "does it show the line", and write the prompt so the action is unambiguous (head shake, push to the
  far edge, let go). The approved END frame itself was ambiguous, so the remake runs START-only.
- A7 frames (four reviews): box composites swap the background inside the box (trees, clouds) and leave rectangles of
  sharper texture; use tight Apple Vision person masks (`personmask` on an enlarged crop when a person is motion-blurred or
  against foliage), ONE shared softened background for both frames, the hole where the other frame's man stands grown before
  its feather (a short feather leaked a ghost shoe), rim clamps only where a halo exists (it smeared hair elsewhere), never a
  blur patch over a logo. Regenerate START from END with every identity detail spelled out (hair, shoes, both shirts), then
  measure garment colour on both frames and match in code.
- The audio gate's `do_no_harm` row needs `<master>.audio_untreated.json`; when the voice is the previous round's track
  retimed, copy that round's baseline beside the new master.
- A gate plan built from a manifest edited after the render fails (`covering()` finds no item): build it from the manifest
  the render used, or re-render first.
- A1 shot 2 (hand rises to a hollow cheek): Veo could not draw the hand's path from START to END in 7 takes (ear, temple,
  eye, fist, hair, a turn to profile). Redesign as a HELD pose: START-only from the approved END frame, prompt "almost no
  movement, like a held photograph", plus an "Avoid:" list naming each fault (Flow has no negative field: veo.py
  `--negative-file`, the flow-veo agent appends it). Even then 3 of 4 takes rubbed the cheek or turned; take 1 was clean on
  frames 0-59 only. Prescreen with a face+hand crop strip (every 10 frames) before clipcheck: clipcheck tracks only camera
  and background, never hands or faces. `ai_r5.py` takes optional `cuts` (film seconds) so each shot is retimed to its own
  slot: the shot cut sits in the pause before the line it illustrates.
- `veo.py add <dir>` appends `veo/`: pass the folder ABOVE the job (`round5/ai`), or takes land in a nested `veo/veo/`.
- The frame gate refuses START=END from one gated frame (no reviewed pair stamp); START-only is accepted.
- Outcome: the held pose also failed (23 Flow takes in all: hand to eye, temple or chin, mouths opening, a sealed-lips
  prompt did not stop it). Shot 2 ships as the gated, reviewed END still with a slow push-in (`ai_r5.py` shot
  `['still', png, zoom_end, fx, fy]`, which checks the frame stamp and the review file). Stop at about 8 takes per shot and
  fall back to the still rather than burning credits on the same pose.
- The AI chip sits top-left; a side-list card (G12) over an AI insert (A8) covered it and the chip ghosted through the card's
  91 % fill (caught as a `fill` row in the graphics checks). Before rendering, list every manifest item overlapping each AI
  insert; move the chip with `chip_x` (1400 = top-right) in `clips_override.json`.
- Never ship a frame altered only to get it through Flow (the A1 face swap): once motion is abandoned, the still is Dan's
  approved frame, byte for byte. A different face is a new frame and needs his approval again (review M1, render 2).
- AI inserts play at real speed: size the slot to the take (A8: 40 source frames = 50 film frames), never stretch the
  take to the slot (0.925x was caught as a repeated frame every 4 frames).
- Presenter seek after an insert: `gsbg.Presenter` seeks with `-ss (k0-0.5)/FPS`, which can land one frame late after an
  insert splits a presenter run (render 2: picture one frame ahead of the voice for 184 frames after A8). `assemble_r5.py`
  now reads on from the last presenter run's start and skips frames instead of seeking. Check: decode both masters to
  192x108 grey and search the best offset per frame against the previous round; every run outside the changes must sit
  at the same offset as the sound.
