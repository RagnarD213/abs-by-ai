# a8_ad4 — Muhammad's Ad 4 vertical (2026-09-11): the tools behind SKILL.md lessons [A8]

Build dir `/Volumes/Extreme/_edit_work/ad4-vert/` (recipe beside the master in `Muhammad Ad Videos/stop wasting money on
supplements - ad 4/recipe-vertical/`). The a7 pipeline (zprofile2 → zfit/zfit_right → zpic2 → zedl → zedl3 → zlut → zbase →
zvig → zmeasure → zhair → zcrop → align_ctc → captions → render → zmux → gates) re-run on raw roll C1594, plus:

| step | script | what changed against a7 |
|---|---|---|
| media maps | `zmatch4.py`, `zmatch4b.py`, `zmatch4c.py` | NCC of his frames against every source at 640; a FIXED box for a clip beside his own label (the robot); full-res crops + a multi-scale template search for the ~300 px phones beside Dan (results / safety) |
| assets | `zassets4.py` | every asset rendered on HIS time map, one frame per beat frame; the robot map strictly linear per shot (no plateaus); the download screen rebuilt from the recording's own pixels (header + the photo by its edge gradients, email form out of frame) |
| graphics | `g8.py` | g5 (Dan-approved on Ad 5) + his numbered lower third, bullets with one or two olive tails, his "AI-generated video" tag + arrow, the real-picture chip, and every text reveal at HIS pace (LT_GROW/LT_HEAD/LT_STAG/LT_TYPE, BUL_TYPE, TAIL_TYPE, title card) |
| picture | `render8.py` | new kinds: robot (fades up with the tag on), shot/bleed with the real label, app/phonecard/dl (a phone taking the media's aspect), window body `phonev` (Dan above, the audit phone below); 4 % push on video cards, 8 % on title cards |
| crop | `zcrop.py` | his six punch-ins (clipped to talk, ended on a visible cut inside them), FORCE_VISIBLE / FORCE_INVISIBLE pairs that move a level change onto a beat edge without changing the group count |
| cutdown | `zcutdown.py`, `zcut_build.py` | a range never ends inside a strobe's rise; the last seam flips the OUTGOING hold (the ending is his walk-out); the caption-mute sets come from the master's beats; `his_mix.wav` asserted 16-bit stereo; first word of a range capitalised |
| beats / captions | `beats_ad4.py`, `captions_ad4.py` | the Ad 4 beat sheet (every deviation logged at the top) and the caption FIX map settled by CTC |
| chains | `chain_m1.sh`, `chain_c1.sh` | master render + every gate; the cutdown render + every gate from inside `cut/` |
| delivery | `deliver4.py` | refuses a file without a PASS audio stamp — on this build the editor's own export failed the true-peak row by 0.1 dB, so the masters waited for Dan's call |
