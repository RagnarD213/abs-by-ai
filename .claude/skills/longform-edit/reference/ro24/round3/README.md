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
  muted footage behind Dan (steady Sharon windows of the E! video: 12.4-16.8, 54.6-58.8, 88.5-91.8, 118.95-124.4 s; 66-71 strobes).
- HyperFrames `check` fails deliberately faint big type on contrast: it is a texture, drawn on a canvas.
- The plate decode (FFV1 16-bit 2880x1620) is about 0.45 core-seconds a frame and dominates every render.

Round 3 review loop (2026-10-25): the first independent review (FIX FIRST) caught a strobing red-carpet window, a source wipe at a
window's first frames, a 1.14x corner W/T step that read as a jump cut, a split on round 2's join crossfade ("Sharon" chopped),
digital silence at a clip head, and a credit under Dan's shoulder. Fixes: windows on scene detection + a flicker scan,
corner 1.35x, the insert one frame earlier with the next take's pre-roll frame in its slot (`PREROLL`) and room tone over the
clip's silent head (`ROOMTONE_HEAD`), credit wrapped at 600 px. `assemble_r3.py --reuse OLD --redo BG03,...` re-composes only
changed background segments; `hair_corner_r3.py` measures the corner layout the main hair scan cannot see.
