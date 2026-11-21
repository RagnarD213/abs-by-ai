# a7 — Muhammad's Ad 5 vertical (2026-09-10): the tools behind SKILL.md lessons [A7]

Build dir `/Volumes/Extreme/_edit_work/ad5-vert/` (recipe beside the master in `Muhammad Ad Videos/every diet youve tried
failed for the same reason - ad 5/recipe-vertical/`). The a6 pipeline (Zeeshan, 24 fps) re-run on a 29.97 editor with a
processed mix, Muhammad's J2 design system, and a Python compositor with per-beat renderers:

| step | script | what changed against a6 |
|---|---|---|
| profile | `zprofile2.py` | GCC-PHAT weighted xcorr: his EQ'd/de-reverbed mix locks at 0.61 with plain correlation, 0.75 with PHAT, 3 ms jitter |
| framing | `zfit_right.py` | a second template on the RIGHT half for his text-left / Dan-right window screens; each sample records its template box |
| EDL clean | `zedl3.py` | clips segments to the beat sheet's talk/window beats, extends edges over his flash frames, asserts coverage |
| vignette | `zvig.py` | his radial falloff measured AFTER the LUT, applied on the conform in source coordinates |
| graphics | `g5.py` | Muhammad's tokens as per-frame PIL functions: note+title, bullets window, lower thirds, Day chips, CTA pill, why card, title card, lock screen, phone mockups |
| beats | `beats.py` | 56 beats; flash strength per frame recovered from HIS luma trace on each side of the cut |
| picture | `render5.py` | compositor at 29.97 with cardv (his 16:9 clips in his card, crop insets, rate), window bodies, slow pushes on settled cards |
| crop | `zcrop_ad5.py` | NEAR holds anchor on the head (0.4 torso + 0.6 head); punch edges snapped to his cuts; a punch whose head lean runs > 60 px for ~0.8 s at NEAR is demoted to FAR; audit-judged pose snaps forced visible |
| hair | `zhair_ad5.py`, `zhairgate2.py` | the hair top walks UP from inside the hair (a dim wall over the bright fridge fooled the midpoint search into y = 0) |
| assets | `zassets5.py`, `zmatch5.py` | the app recording on his time map; his result screen (goal image alone) rebuilt |
| cutdown | `zcutdown_ad5.py`, `zcut_build_ad5.py` | L-cut tails for a word that ends past his picture cut; the generated cut beats carry the full spec |
| delivery | `deliver5.py` | both masters + review copies + A/B + stamps + recipe under the editor-deliveries convention |
