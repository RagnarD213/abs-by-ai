# Colour audit, round 3 (2026-10-22)

Dan: "anytime you use a screenshot in these carousels, it's properly color corrected and looking optimal before you put
it in." Every footage still in the 22 posts below was traced to its source and judged next to the approved jump rope
slides (`template-r1-mockups/C1-the-fix-02/03.jpg`) and the workout-05 slides. Regraded stills were made with
`reference/grade_still.py` (approved S-Log3 LUT for log rolls, then the finishing pass) and written as `*-graded*.jpg`
beside the old file; the content file points at the new one. Old files are kept.

Root causes found: (1) R2 stills pulled straight from raw S-Log3 rolls with no LUT (fix-07 cover and mistake, fix-08 fix)
and only brightened by `enhance.py`; (2) the 8/28 blue-mat rolls C1679-C1683 and Zeeshan's arms master: low sun left
skin orange and the body in shade; (3) the 7/8 welcome roll C0223-007 (fix-06) was graded but dark (overcast).

Rolls: `C02xx-0xx` = 7/8 welcome shoot (S-Log3, LUT e0.70), `C1672-C1685` = 8/28 shoot (S-Log3; blue mat e1.30 + cool,
hard sun e1.15), `C1584` = 8/3 (Rec.709), `C17xx` = 10/15 (Rec.709), `AM` = Zeeshan arms master (graded edit),
`B####` = clip library (already LUT-graded).

| post | slide | source | verdict | why |
|---|---|---|---|---|
| fix-02-towel-row | cover, mistake, fix, cues | C0229-008 @ 197.8 / 198.5 / 209.0 / 212.0 (LUT e0.70 in R1) | kept | bright, natural, approved; finishing pass tested, no visible gain |
| fix-03-deadlift-look-up | cover, mistake, fix, cues | C0228-005 @ 112.2 / 131.2 / 136.6 / 139.4 (LUT e0.70) | kept | same as fix-02 |
| fix-04-kettlebell-between-legs | cover, mistake, fix, cues | C0228-005 @ 64.8 / 64.2 / 74.6 / 74.0 (LUT e0.70 + enhance) | kept | bright and natural already |
| fix-05-toe-touch | cover | C1682 @ 111.6 (b130) | regraded | backlit, body dark; Dan asked for brighter |
| fix-05-toe-touch | mistake | C1682 @ 108.6 | regraded | same |
| fix-05-toe-touch | fix | C1682 @ 70.0 | regraded | same, skin orange |
| fix-05-toe-touch | cues | studio-blue-53 studio photo | n/a | finished photo |
| fix-06-v-sit-twist | cover, mistake, fix, cues | C0223-007 @ 367.8 / 366.2 / 345.2 / 325.0 | regraded | dark and grey (overcast); approved post but it failed the bar |
| fix-07-plank-butt-up | cover | C1683 @ 105.60 | regraded | was raw S-Log3 + enhance only; Dan: "still looks very dark" |
| fix-07-plank-butt-up | mistake | C1683 @ 115.25 | regraded | was raw S-Log3 |
| fix-07-plank-butt-up | fix | C1683 @ 79.0 | regraded | dark, orange skin |
| fix-07-plank-butt-up | cues | C1683 @ 124.0 | regraded | orange skin |
| fix-08-push-up | cover | C1680 @ 148.4 | regraded | orange skin, shade |
| fix-08-push-up | mistake | C1680 @ 151.7 | regraded | same |
| fix-08-push-up | fix | C1680 @ 64.0 | regraded | was raw S-Log3, washed out (Dan) |
| fix-08-push-up | cues | studio-white-13 studio photo | n/a | finished photo |
| fix-09-bicep-curl-swing | cover | C1584 @ 87.1 (8/3, Rec.709) | regraded | shaded and flat (finish pass from source) |
| fix-09-bicep-curl-swing | mistake, fix, cues | AM @ 187.0 / 203.8 / 200.0 | regraded | orange skin from the edit's grade |
| fix-10-side-lateral-elbows | cover, mistake | AM @ 284.2 | regraded | orange skin |
| fix-10-side-lateral-elbows | fix, cues | C1676 @ 13.5 / 8.0 (h115) | regraded | flat grey and dark; approved post but it failed the bar |
| workout-02-five-minutes | squat | B0464 @ 6.57 | kept | bright and vivid; finish pass made it duller |
| workout-02-five-minutes | push-up | B0546 @ 3.55 | regraded | orange skin |
| workout-02-five-minutes | Spiderman plank | B0455 @ 2.82 | regraded | dark, orange (B0455 is on the reads-dark list) |
| workout-03-kettlebell | cover | C1743 @ 19.0 (new, 10/15) | new, graded | Dan: a real kettlebell deadlift rep on the intro slide |
| workout-03-kettlebell | deadlift | B0431 @ 1.7 | regraded | orange face, hot |
| workout-03-kettlebell | goblet squat, push-up | C1750 @ 11.47, C1744 @ 13.72 | kept | bright 10/15 Rec.709; finish pass made them duller |
| workout-04-home-arms | curl, lateral, tricep | B0432 @ 6.9, B0450 @ 1.51, C1754 @ 14.64 | kept | bright and natural; no gain from the finish pass |
| workout-05-commercial-break | push-up, squat, plank | B0547 @ 3.44, B0475 @ 4.19 (GoPro), C1752 @ 3.19 | kept | approved reference, queued |
| workout-06-ab-rounds | toe touch, V-sit, Spiderman | B0003 @ 1.41, C1748 @ 12.95, B0468 @ 3.94 | kept | bright and natural |
| workout-07-lower-abs | reverse crunch | C1747 @ 4.0 | kept | bright; finish pass washed it out |
| workout-07-lower-abs | toe touch | C1741 @ 33.0 (new, 10/15) | new, graded | Dan: more extended toe touch (legs straight up, arms reaching) |
| workout-08-v-taper | lateral | B0450 @ 5.53 | kept | bright and natural |
| workout-08-v-taper | vacuum | thumbnail photo | n/a | finished photo |
| workout-09-ab-wheel | levels 1-3 | B0427 @ 2.75 / 3.75 / 4.75 | regraded | orange skin and a hot yellow sun streak on his back (`--glare`) |
| workout-09-ab-wheel | cover | thumbnail photo | n/a | finished photo |
| receipts-02-metabolism | all | personal and studio photos, cutouts | n/a | no footage stills |
| receipts-04-light-weights | cover | C1676 @ 25.1 (h115, new) | new, graded | Dan: side laterals on the intro (was curl B0432 @ 7.2) |
| receipts-04-light-weights | tips | C1676 @ 6.6 (h115, new) | new, graded | old tips still was the same rep as the new cover |
| receipts-05-too-old | all | studio photos, AI images | n/a | no footage stills (cover is now a Codex aged image) |
| receipts-06-sleep | all | AI images, studio photo (removed) | n/a | no footage stills |
| receipts-11-carbs-at-night | all | AI images, cutout | n/a | no footage stills |

Tool notes: `grade_still.py --src ROLL --t SEC [--crop x,y,w,h --size WxH]` picks the base grade from the roll name;
`--still FILE` runs the finishing pass only. The finishing pass helps footage that is dark, shaded, flat or orange; on
stills that already look bright and saturated (10/15 rolls in sun, most library clips) it tends to mute them, so
compare and keep the original when it is already good.
