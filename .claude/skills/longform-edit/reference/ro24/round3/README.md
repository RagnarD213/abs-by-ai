# RO-24 round 3 recipe (Celebrity Ozempic, green-screen background template + interview clips)

The first film on the shared green-screen background template (`_shared/greenscreen-bg/`, Dan 2026-10-24). Round 2's cut, key,
colour, voice and graphics stay locked; round 3 adds the six interview clips (full screen with their own sound where the script
says [PLAY CLIP]), the backgrounds behind Dan, and before/after photo scenes with weight + medication. Work dir
`/Volumes/Expansion/_edit_work/RO-24/round3/`.

Order (each script's docstring has the detail):
1. `tx_clips.py`: word-timed transcripts of the downloaded clips (small.en), to set trims on the script's first/last words.
2. `clips_r3.py`: trims on measured quiet points (`--check` prints levels), 1080p 29.97 exact frames, a source chip, audio to
   -15 LUFS with 25 ms fades. Pictures stay as broadcast.
3. `timeline_r3.py`: inserts each clip at a quiet frame of his voice (inside the photo scene that introduces the person where
   there is one, so the insert hides the join), splits shots, shifts words / audio / graphics by whole frames; photo scenes that
   introduce a person end where their clip starts. Writes `edl_r3.json`, `timemap.json`, `film_voice_r3.wav`.
4. `photos_r3.py` (lives in `round3/hf/`): photo scenes with a stat line (Dan's approved wording) under the name chip; pairs for
   everyone who lost weight; only credited photos where a credit line shows.
5. `manifest_r3.py`: one compositor manifest (round 2 graphics mapped, round 3 photo scenes, the clips as opaque items).
6. `facts_r3.py` -> `planner.py facts.json bg_plan.json --overrides bg_overrides.json`, then `hfbg.py` for panel and big type.
7. `stills_r3.py OUT --only BG..`: one still per background through the real assembler (cheap), before any long render.
8. `chain_r3pv.sh` through the queue: `assemble_r3.py` (plates decoded once, composed at 1080p, plate decode skipped under
   full-screen items, hair measured on every rendered presenter frame), mux, 540p, `hair_r3.py`, audio gate, graphics checks.
9. `ctx_r3.py` (context clips per background, clip and photo scene, pair stills), `page_r3.py`.

Traps met:
- yt-dlp `--download-sections` on a long video can return audio only (format selector fell back): list formats, pick `137+ba`.
  Check every download has video. Dubbed-auto audio tracks exist on some videos: transcribe to confirm the language.
- News clips burn quote boxes and product shots over the person: download the WHOLE source video and pick clean windows for the
  muted footage behind Dan (Sharon: 52-58, 66-72, 88-92, 12-17.6 s of the E! video).
- HyperFrames `check` fails deliberately faint big type on contrast: it is a texture, drawn on a canvas.
- The plate decode (FFV1 16-bit 2880x1620) is about 0.45 core-seconds a frame and dominates every render.
