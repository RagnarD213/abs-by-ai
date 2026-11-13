# RO-32 thumbnail 2 revised, 2026-11-13

Awaiting Dan’s approval of the exact revised file. No FINAL installation, metadata, upload, schedule or waitlist action performed.

## Pick with revision

> Let's go with number two, but I want to change the text to say "10 exercises I do every week" to be all in that large white font and to occupy the full stripe at the top.

Logged once via `blind.py pick` on `_round2-real`, `--chose "2"`, exact words, non-comparison real selection. Original label/key/hash preserved. This is not approval of the revised file. Pick record: `_round2-real/pick-2-with-revision.json`.

## Revised file

- File: `social media graphics/youtube/thumbnails/I'm 41. Here Are The 10 Exercises I Do Every Week/_round2-real/review/2-revised.jpg`
- SHA256: `a144e20a6ea4b003439516a61317b83b208aa82452b55b3156226ec0b06cf6e9`
- JPEG 1280x720, 474,224 bytes, under 2 MB.
- One white Anton headline: “10 Exercises I Do Every Week”. Font 105px; actual ink margins 38px left, 39px right; vertical center y78 in 156px stripe.
- Removed red age box and small blue subline. No AI generation or redraw. Original cyan rule and photo panels retained exactly.
- Pixel proof: `_round2-real/2-revised-pixel-proof.json`. JPEG DCT header-block replacement preserves decoded rows152–719 bit for bit. Cyan rule and all photo panels: maximum channel difference 0; changed pixels below stripe 0.
- Build: `_round2-real/build.py --revise-2`, using `jpeglib==1.0.2` from `_round2-real/requirements-jpeg.txt`. Dedicated interpreter: `/Users/danielrose/Projects/_edit_work/RO32-setup/jpeg-venv/bin/python`. Original build archived as `build.before-2-header-revision.py`. Other six original exports remain hash-identical.

## Checks and approval page

Visually inspected 390px phone export and 960px desktop export, browser at 390px and desktop. One line readable, evenly centered; photos/cyan rule unchanged. Served with `review_server.py` at http://127.0.0.1:9791/. Exact served image bytes match SHA256; page/image 200, range206; page script passes `node --check`. Approve/Select and Copy Reply tested, correct exact-file hash in reply; test choice cleared and reload shows unselected. No media players or speaker playback. Current page exposes only 2-revised; old six-choice page archived as `_round2-real/review-before-2-revision.html`.

Full QA: `_round2-real/2-revised-quality.json`. State and manifest record revised hash and pending approval. Original film unchanged.

## Next action

Stop for Dan’s explicit approval of 2-revised hash `a144e20a6ea4b003439516a61317b83b208aa82452b55b3156226ec0b06cf6e9`. Do not repeat the original pick log. Any further change requires a new checked revision and approval before FINAL installation. Only after revised-file approval and later setup resume, follow the handoff for metadata and shared Blotato/waitlist; preserve Jan29/30 release reservation.
