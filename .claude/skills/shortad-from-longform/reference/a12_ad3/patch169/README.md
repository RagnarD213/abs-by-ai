# Patch one shot inside an editor's 16:9 card (Ad 3, 2026-09-14)

Order: `fit.py <dir>` (his frames H.npy, old story frames V.npy, time map J.npy; geometry by template match) →
`fit2.py` (ECC refine: scale 0.5177 at 683.07, 37.89) → `fit3.py` (10-term per-channel grade C_*.npy, held-out error) →
`matte2.py` (outside/band/label masks; window edge s·P+k, white label alpha) → `build_patch.py` (137 lossless frames from
the NEW story clip) → `encode.sh` (trim his file around the patch, x264 crf 12 BT.709, his audio stream-copied).
`kling_regen_shot.py` = batch 1 (rejected pick), `kling_regen_shot_calm.py` = batch 2 (keeper u2). `fog.py` = mirror
sharpness per 12 frames (weak: confounded by head motion — read the frames).
All paths are Ad 3's; `load.py` holds the time map and the decode (accurate_rnd — see SKILL.md A12.13 step 4).
