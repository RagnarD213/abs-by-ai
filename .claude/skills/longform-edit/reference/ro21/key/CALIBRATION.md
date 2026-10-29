# RO-21 key calibration (C1724), 2026-10-28
House key (DS-40 Claude R2 maths) through the RO-24 16:9 port, fast shared keylib/stage 1.5, RIM=4, plate frames 3000+7000 at 1.5 fps.
Excerpts: CAL1 frames 4180-4279 (139.5 s, hands), CAL2 8980-9079 (299.6 s, hands). Renders: `CAL* pale/navy/pink.mp4`.
| | CAL1 | CAL2 | bar (DS-40 R2) |
|---|---|---|---|
| motion-compensated edge flicker (out/src) | 0.524 (worst 0.655) | 0.518 (worst 0.648) | below camera; R2 0.69 |
| hair, motion-compensated | 0.575 (worst 1.19) | 0.486 (worst 1.00) | R2 0.68 |
| dark rim on skin edges | 3.95 % | 4.58 % | at or below source (DS-40 source 8 %, R2 2.7 %) |
| floating specks | 0 | 1 (frame 87) | 0 |
| see-through (blue cast inside) | 4170 px / 100 fr, box at the glasses arm (x1008-1053 y99-265) | 5944 px, strip x1076-1145 | RO-24: head hits = glasses arm |
Verdict: settings carried from RO-24 (same set) hold; full key started with these inputs (keyonce stamps).
