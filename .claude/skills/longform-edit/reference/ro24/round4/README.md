# RO-24 round 4 recipe (Celebrity Ozempic: whole film on the locked green-screen background template)

Round 4 put the whole 8:36 film on `_shared/greenscreen-bg/` (locked by Dan 2026-10-27), with all six interview clips, photo
scenes P4-P7 rebuilt as before/after pairs, G12/G14 polish, and start/end frames for AI clips A1, A3, A4, A6, A7, A8.
Work dir `/Volumes/Expansion/_edit_work/RO-24/round4/` (round 3's media linked in: `photos`, `clips`, `mock`).

Order:
1. `photos_r4.py` (P4-P7, from round 3's `photos_r3.py`); G12/G14 from round 2's `build_custom.py` / `from_plan.py` in `hf/gfx/`.
2. `retime_r4.py`: Tracy Morgan's insert ends after "I gained 40 pounds." (66 frames off its tail; everything after moves
   earlier). Writes `edl_r4.json`, `film_words_r4.json`, `audio/film_voice_r4.wav`; `r4_t()` maps round 3 seconds.
3. `audiofix_r4.py`: sub-6 ms click spikes bridged, two lip smacks replaced by room tone, clip exits faded after the last word
   (Meghan, Tracy) -> `film_voice_r4b.wav`.
4. `facts_r4.py` -> planner -> `hfbg.py` (panels, big type). Every later override carries its why; times after the retime go
   through `r4_t()`.
5. `stills_r4.py` on every changed segment, then `chain_r4.sh` (full film: picture, mux, 540p, hair, audio gate, graphics).
6. `srt_r4.py`: Dan's words from Whisper on the DELIVERED audio, each interview clip's words from its own source transcript.
7. `gateplan_r4.py` (+ `negscan_frames_r4.py`), `watch.py`, a fresh judge, the gate; `ctx_r4.py`, `page_r4.py`.

Traps met (four independent reviews; each fix below came from one):
- `assemble --reuse` darkens every copied frame about 1.65 luma levels per generation (decode/encode round trip). Previews
  only; the delivered file is a full render.
- Clip windows: a window that starts in the last ~1 s of a segment shows as a flash/scrap; a short window looped reads as a
  stutter; a window switch 2 frames before Dan's cut reads as a jump. Plan windows so every piece is >= ~2 s (>= 3 s on the
  set's TV) and no switch lands within ~0.3 s of a picture cut. When a person's clean footage is scarce (Fat Joe's Page Six
  video flashes or carries quote boxes almost everywhere; Meghan's ET has two long clean shots), use photos, cards or big
  type instead of reusing footage.
- Footage behind Dan: scan for flashes (whole-frame brightness jumps > 4/255) and gestures near his head (Oprah's fist pumps).
- Photo repeats: the planner's soft/set defaults reuse a person's photos; give each later segment its own photo and keep the
  wall's skip list in step. `person_crop` can pick a stranger's face on a red-carpet photo: check every card.
- The planner said "Dan to the side" under a left-third card but never set it: fixed in the shared planner (soft +
  card -> placement right). The soft type ignored the clip's zoom (ET bug showed through the blur): fixed in `gsbg.py`.
- Whisper on the delivered mix misses interview audio under music/laughter and misspells drug names; use the clip's own
  transcript inside clip spans and a fix table (`srt_r4.py`).
- AI frames: 6 clips took 1 to 6 reviewer rounds each (~110 Codex generations). What failed most: pasted people (rims,
  patch seams, size drift), objects that move by themselves, AI textures on denim/skin/shirts, clothing that changes between
  START and END. Build END first, START from END, lock the background only well away from people.
