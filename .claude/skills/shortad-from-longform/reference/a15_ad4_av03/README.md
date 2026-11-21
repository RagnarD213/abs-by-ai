# a15_ad4_av03: Ad 4 in 9:16 and 1:1, full length and 59 s, from ONE compositor (AV-03 + AS-02, 2026-10-03/04)

Build dir `/Volumes/Extreme/_edit_work/AV-03/` (a lean copy of `ad4-vert/`: scripts, JSON, sources; no caches). The lessons
are SKILL.md section [A15]. What each script is for:

| step | script |
|---|---|
| picture EDL on HIS picture frames (2-frame acoustic bias, cuts on his picture cuts, micro trims, closing slow-down) | `zedl9.py`, then `zbase.py` (proves base frame n = raw n + d) |
| which raw frame his frame shows, read off his face (mouth, pose; `--abs` adds position) | `zlips.py`; `zmatch9.py` is the whole-frame version that FAILED under his punch ramp |
| face centre at every measured sample (the crop lands on his face) | `zface.py` |
| crop: land then hold, re-land only at visible cuts, insert returns and window edges; eased punches from his fit | `zcrop.py`, `zcrop_sq.py` |
| BT.709 grade chain (the Ad 3 method) | `zlut.py` in a12_ad3, `zgrade2.py --post`, `zgrade3.py`, `zgrade4.py` (not needed here) |
| ONE compositor for both aspects (`--aspect 1x1` re-points g5/g8 geometry) | `render9.py`, `beats.py`, `g5.py`, `g8.py` |
| labels by measurement (first settled + last frame, one size and spot per run) | `zlabel9.py` |
| square captions | `zcaps_sq.py` |
| plan for the shared gate, bound to the delivered sha | `plan9.py`, `ztranscribe9.py`, `zneg9.py` |
| chains | `chain_all.sh` (four renders), `chain_round2.sh` (+ scans), `gates9.sh` / `gates9b.sh`, `finalize9.sh` |
| carry judged watch verdicts across pixel-identical images | `zcarry9.py` |
| review page (four files, decisions, every re-laid shot in both aspects, one docked player) | `page9.py` |
| delivery | `deliver9.py` |
