# D01 independent START/END frame review

Reviewed the 1024 × 1536 originals at full resolution before reading the gate, then inspected 3× crops and made fresh pixel measurements. Coordinates below use the full stacked image. Scratch evidence: `/private/tmp/claude-501/framereview/D01-end/`. Only the two images, spec, and gate evidence informed this review.

**A. Object realism: PASS.** Both frames contain one fork with four tines, one open tin, one held sardine piece, one held chip, one chip bowl, and one cracker plate. Tin at approximately (586,485), bowl at (445,1308), and plate at (635,1340) have coherent rims, food, and support; no extra unsupported object appears.

**B. Contact: PASS.** Each frame has four visible hands total and zero visible feet, with all four intended hand contacts retained: fork grip near (325,292), tin grip near (640,521), chip pinch near (429,1010), and resting hand near (813,1310). Fresh template matches place the fork hand, chip hand, resting hand and both named elbows at (0,0) px displacement; END teeth meet the fish near (477,282) and the chip near (470,1008).

**C. Body line: PASS.** Both seated torsos and supported arms retain the same position; top torso box (370,390)-(680,568) and bottom torso box (370,1110)-(700,1225) match at (0,0) px with correlations 0.985 and 0.985. Head crowns move down about 39 px on top and 30 px below, with a plausible neck bow toward the food rather than torso sliding; both men are shirtless in all four panels and the lean upper / heavier lower physiques remain intact.

**D. Anatomy: PASS.** There are two arms per man in both frames, no added limb, and no reversed joint; the arms themselves remain fixed. Approximate projected upper-arm / forearm lengths are top right 250/208 px, top left 244/147 px, bottom right 252/222 px and bottom left 230/67 px (last forearm strongly foreshortened); unchanged shoulder/elbow/wrist contours and 0–1 px anchor shifts imply under 2% change, below the 8% failure threshold. These are screen-space measurements, not inferred anatomical bone lengths; no full-body detector was used to certify the stacked image.

**E. Continuity START to END: FAIL.** All nine spec still boxes independently match at 0–1 px displacement, correlations 0.929–0.997, and the remaining static field has only 0.350% of pixels with any RGB channel difference greater than 20 (mean absolute difference 2.26/255). However, the gate misses the stationary fork/food inside the generously allowed head rectangles: sardine texture box (456,290)-(481,318) moves (-2,+13) px with 0.922 correlation, while its hand stays at (0,0); fork bowl bottom near (424,287) becomes approximately (424,293), with outer tines about 9–14 px lower. The held chip also drops: its yellow lower edge at x=455 and x=460 changes y=1032 to y=1038, while its pinch hand stays fixed; see `fork-detail-pair.png`, `start-fork-grid.png`, `end-fork-grid.png`, and `chip-detail-pair.png`.

**F. Hands and props: FAIL.** At 3×, each hand reads as a normal five-digit hand; the top tin-holding thumb is partly occluded by the tin, rather than an extra or missing exposed digit. Each prop remains singular and all intended hands hold it, but the supposedly unchanged fork and food do not retain their positions: fish 13 px down and held chip lower edge 6 px down, with the hands fixed. The sardine shift involves its unbitten lower half, so it cannot be explained by removal of a bite at the mouth.

**G. Expression and intent: PASS.** Both START faces smile toward camera; both END faces look down with open mouths at their food. Approximate mouth centers move from (515,214) to (480,295) on top and (509,954) to (477,1017) below, so a silent viewer reads two men beginning to eat; END shows an initial bite, not completed chewing.

**H. AI slop: FAIL.** There is no conspicuous doubled hand, warped torso, garment change, vacated-head residue, or background seam in the 3× head/hand crops. The fork itself changes geometry while its handle/grip stay fixed: its bowl/tine assembly lowers around 6–14 px, and the sardine below it shifts 13 px; this is a visible utensil/food wobble rather than a rigid stationary prop. Evidence: `fork-detail-pair.png` and the two coordinate-grid crops.

**I. Animate test: FAIL.** The roughly 81 px top and 63 px lower mouth descent is a plausible beginning of a seated bite over the specified 2.30 seconds, with no need for body-size change or a limb passing through an object. But interpolating these endpoints would require the held fork/food to move or deform despite the required fixed hands and stationary props; the head-to-food action is close, but these endpoints do not satisfy that explicit motion requirement. A frame-pair review cannot certify the eventual video's in-between motion.

Must change:
1. Preserve the START fork shaft, bowl, all four tines, and unbitten sardine piece at their exact START coordinates; move only the upper head/neck/mouth to meet them. Do not shift the sardine's lower half down 13 px.
2. Preserve the START held chip outline and position, including lower edge y=1032 at x=455–460; move only the lower head/neck/mouth to make contact. Do not lower the chip 6 px.

VERDICT: FAIL
