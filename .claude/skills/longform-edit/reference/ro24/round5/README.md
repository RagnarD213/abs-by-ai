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
