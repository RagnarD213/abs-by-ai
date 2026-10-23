# RO-24 round 2: STOPPED at Dan's request (2026-10-22, "stop work on this task so I can render other things")

Nothing of RO-24 is running or queued (renderq status readback: 0 entries). Resume only when Dan says.

## Keys (approved DS-40 Claude R2 key, RIM 4)
Done (plates in key/): R01 R02 R03 R04a R04b R05 R06 R10 (the whole first minute and takes 4-6, 10).
Partial, stage 1 caches kept: R07 (481 of 999 frames), R12 (1570 of 2734). stage1_16.py now skips cached frames.
Not started: R09 R11 R13 R14 R15 R16.
Resume: renderq.py run --group RO-24 -- bash recipe/ds40key/resume2_laneA.sh   (R07 R09 R11 R13 R15)
        renderq.py run --group RO-24 -- bash recipe/ds40key/resume2_laneB.sh   (R12 R14 R16)
Lane A peaked at 28.9 GB (stage 1 at 4K, 5 workers): consider WORKERS=3 if the Mac is busy.

## Graphics and photo scenes (hf/)
Rendered and checked (17 of 22): G01-G05, G07, G09, G10, G11, G14 and photo scenes P0, P1, P3-P7. Not rendered: G06, G08,
G12, G13 (render_long.sh) and P2 (hf/build_photos.py --render --only P2; killed 5 s into its render). The agent records the exact remaining commands at the top of
hf/GRAPHICS-REPORT.md. manifest.json lists items whose .mov does not exist yet: do not assemble before they render.

## Ready, not run
B-roll inserts done (broll/B1.mp4, B2.mp4, broll_manifest.json). Voice final (audio/film_voice_A.wav). Timeline final (edl_film.json,
edl_film_pic.json with S framing under the two side cards). Next after keys + graphics: recipe/chain_r2fm.sh (first minute, checks,
key comparisons and measures), recipe/ctx_r2.py (context clips), then the page and an independent review.
