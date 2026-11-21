**SUPERSEDED 2026-10-24 by `handoff-20261024-ro24-celebrity-ozempic-round3.md` (Dan's round 2 reply). Do not execute.**

**LFC.** Task name: `Celebrity Ozempic LFC R3`.

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 3 handoff (written 2026-10-23 at the end of round 2)

**Waits for Dan's reply to the round 2 page (http://127.0.0.1:9125/).** Follow his answers exactly.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/_shared/framecheck/README.md` (AI frames), `.claude/skills/_shared/veo/README.md` (Flow first),
the round 2 recipe `.claude/skills/longform-edit/reference/ro24/round2/README.md` and `STATE.md`.

## Where things are (work dir `/Volumes/Expansion/_edit_work/RO-24/round2/`)
- Locked: key = Dan's approved DS-40 Claude R2 key ported to 16:9 (RIM 4 + faint-speck rule in write16), plates `key/R*.mkv` for the
  whole film; colour warm; voice A `audio/film_voice_A.wav` (crossfaded joins, every join level-checked); background depth.
- Timeline: `edl_film.json` (audio), `edl_film_pic.json` (picture: take 4 split, S framing under side cards, T either side of S).
- Graphics/photos/B-roll: `film_manifest.json` (hf/manifest.json 22 items + broll/broll_manifest.json); report `hf/GRAPHICS-REPORT.md`.
- Page and reviews: `review/index.html` (built by `recipe/page_r2.py`, served by `_shared/review_server.py 9125 .../round2/review`;
  re-run the server after every rebuild, it serves a cached copy), `review/INDEPENDENT-R2*.md`.
- Dan's decisions on the page: graphics OK/changes, photo scenes OK/changes (first 5 s montage or open on him), B2 at 4:15 (AI bench
  press A or stay on camera B), AI clip ideas A1-A8 (`ai_ideas.json`).

## Round 3 work
1. Apply his graphic/photo/B-roll answers (graphics: `hf/` templates and build scripts; B-roll: `recipe/broll24.py`).
2. AI clips he picks: start/end frame pairs with `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`, each pair
   through `_shared/framecheck/gate.py --verify` plus a fresh `frame-reviewer`, shown to Dan in context before any motion; then motion
   in Google Flow via the `flow-veo` agent; each take through `clipcheck.py --verify`.
3. Then the complete film: `recipe/assemble16.py edl_film_pic.json OUT --bg depth --grade warm --hf film_manifest.json` (+ AI clips as
   opaque manifest items), mux `audio/film_voice_A.wav`, delivery gate, watch pass, hair clearance (`hairclear16.py --skip-opaque`),
   graphics checks, edit sheet, independent review, SRT (Whisper fixes: Osempic/Ozenpik = Ozempic, Zebbound = Zepbound, Monjaro =
   Mounjaro, six pack abs .com = sixpackabs.com).

## Watch for
- The render queue is shared; Dan stopped this video twice for other work. Run at most two heavy lanes, WORKERS=3, and stop at once
  if he or the render-line check asks (finished frames are resumable: stage1_16 skips cached frames; stage15 takes ONLY=).
- The approved key strips green from the olive shorts (a little browner). Offered to keep the shorts' own colour if Dan wants.
- Long-form AI budget $15; Flow credits first.

## Model
Claude: Opus 5.5, high effort.

## Starter prompt
> Celebrity Ozempic LFC R3. Read `Handoffs/handoff-20261023-ro24-celebrity-ozempic-round3.md`, then Dan's round 2 reply, and execute round 3 of "Reacting To Celebrity Ozempic Transformations" (RO-24) with /longform-edit.
