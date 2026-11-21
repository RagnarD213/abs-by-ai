#!/usr/bin/env python3
"""CONSERVATIVE cut-down: remove repetition and belaboring only.
Every outline point in the beat map survives. Spans are approximate — every word
whose MIDPOINT falls inside a span is deleted; the edges are then resolved to
word/silence boundaries by cutlib.resolve_cut."""

# (approx_start, approx_end, label)
CUTS = [
    # 1 intro + halo — collapse the triple "halo effect" naming
    (17.44,   20.60,  "s1-vanity-double"),
    (73.28,   82.78,  "s1-halo-take3-restate"),
    (88.26,   91.15,  "s1-halo-relabel"),
    # 2 job / partnership
    (129.24,  134.55, "s2-women-aside"),
    # 3 relationship — keep the negative mirror, one positive line
    (194.70,  201.10, "s3-husband-funny-sex"),
    (209.36,  217.00, "s3-real-reason-restate"),
    (230.22,  241.05, "s3-positive-quotes"),
    # 4 dating — cut the real-world-vs-online mechanics
    (280.70,  286.00, "s4-impossible-understate"),
    (301.00,  316.55, "s4-realworld-mechanics"),
    (332.60,  340.30, "s4-top10-first-pass"),
    # 5 productivity + meal service
    (427.54,  430.35, "s5-grind-restate"),
    (452.95,  456.35, "s5-invest-money-repeat", (1, 0)),
    (472.36,  475.60, "s5-first-few-days-repeat"),
    # 6 doctor time-cost
    (505.08,  513.40, "s6-as-you-get-older"),
    (545.60,  549.14, "s6-time-consuming"),
    # 7 long-term thinking — appointment logistics to 2 items
    (562.02,  571.40, "s7-appointment-logistics"),
    # 8 mental-health spiral — one "trapped" pass
    (641.50,  645.85, "s8-not-ripped-restate"),
    (683.28,  688.20, "s8-med-expensive-restate"),
    (716.10,  719.65, "s8-trapped-second"),
    # 9 bad health is expensive
    (767.36,  772.00, "s9-waking-moment-garble"),
    # 10 diabetes story — doubled dollar figures + eye restatement only
    (844.60,  849.50, "s10-hospital-double"),
    (868.78,  872.30, "s10-severely-impaired"),
    # 11 money-dead + inheritance
    (920.74,  923.80, "s11-final-point-signpost"),
    (951.44,  954.85, "s11-spent-it-working"),
    # 12 not-dead-but-sick — keep stairs + kids
    (1041.24, 1062.85, "s12-vision-hypothetical"),
    (1111.72, 1125.25, "s12-wife-parallel"),
    # 13 brokie pivot — light touch
    (1210.90, 1213.50, "s13-option-open"),
    # 14 never-cut list — compress commentary, keep all 3 items
    (1240.00, 1244.85, "s14-doesnt-make-sense"),
    # 15 bars & clubs — one pass each
    (1305.94, 1311.10, "s15-opener-restate"),
    (1328.64, 1341.80, "s15-two-birds-and-spending-plan"),
    (1373.44, 1380.20, "s15-cant-afford-far-in-life"),
    (1390.60, 1397.10, "s15-extra-money-month-two"),
    (1441.90, 1451.70, "s15-not-as-much-back"),
    # 16 restaurants — the AbsByAI plug (1522-1565) is untouched
    (1493.34, 1498.10, "s16-restaurant-motives-restate", (2, 0)),
    (1478.40, 1485.20, "s16-treat-for-myself"),
    # 17 junk food
    (1599.00, 1602.95, "s17-cleared-out"),
    # 18 vacations — keep the 2-3 lb/week number, drop the 5-6 lb one
    (1619.42, 1622.50, "s18-know-you-wont-like"),
    (1647.96, 1660.05, "s18-five-six-pounds"),
    # 19 therapy & psych meds — every hedge kept
    (1730.66, 1737.95, "s19-positive-mirror"),
    # 20 sacrifice recap — compress, keep the items
    (1771.60, 1783.15, "s20-obvious-things-restate"),
    # 22 premium protein + 401k
    (2095.50, 2103.20, "s22-brokey-aside"),
    (2123.90, 2127.45, "s22-chicken-thighs-aside"),
    (2138.50, 2147.90, "s22-dollar-figure-list", (8, 0)),
    (2181.00, 2186.85, "s22-sacrifice-list-repeat"),
    (2195.24, 2202.80, "s22-grassfed-beef"),
    # 23 mattress + purple (+ fluids riff trimmed to ~30s)
    (2278.88, 2287.45, "s23-sleep-important-restate"),
    (2323.86, 2328.20, "s23-everything-improves"),
    (2393.50, 2398.18, "s23-no-matter-how-big"),
    (2437.50, 2468.40, "s23-fluids-riff-trim"),
    # 24 gym membership — best people, one osmosis pass
    (2519.99, 2523.72, "s24-couple-reasons"),
    (2546.40, 2555.20, "s24-equipment-list", (8, 0)),
    (2580.50, 2591.45, "s24-levels-to-this", (0, 0)),
    (2599.11, 2606.90, "s24-osmosis-restate"),
    # 25 sleep tracker — Apple Watch cons list to one line
    (2744.69, 2753.95, "s25-applewatch-reason2"),
    # 26 GLP-1
    (2814.60, 2817.60, "s26-wrong-way-restate"),
    (2839.00, 2844.90, "s26-sacrifice-list-3rd"),
    (2846.20, 2853.25, "s26-shocked-productivity"),
    (2869.35, 2875.30, "s26-food-noise-restate"),
    (2900.21, 2907.10, "s26-appealing-double"),
    (2934.57, 2938.68, "s26-break-even-hedge"),
    # 27 TRT
    (3020.75, 3027.88, "s27-what-effect-anaphora"),
    # 28 supplements — big three all kept
    (3108.00, 3112.70, "s28-get-omegas-double"),
    (3124.67, 3136.30, "s28-fair-skin"),
    (3146.67, 3149.50, "s28-show-on-screen"),
    (3155.80, 3165.68, "s28-vitd-tail-restate"),
    # 29 home gym + both worlds
    (3283.27, 3286.60, "s29-hybrid-line"),
    (3301.40, 3313.10, "s29-covid-tail"),
    (3343.61, 3347.20, "s29-workout-more-often"),
    (3349.15, 3350.05, "s29-wear-in-home-gym", (0, 0)),
    (3386.57, 3398.50, "s29-showing-someone-new"),
    # 30 meal prep / chef — Clean Eats + $120/wk kept
    (3514.29, 3520.55, "s30-making-videos"),
    # 31 outsource chores
    # 32 trainer & nutritionist — top-1% argument kept
    (3619.69, 3627.55, "s32-better-use-of-funds"),
    (3639.91, 3645.50, "s32-form-details"),
    (3674.57, 3678.15, "s32-paying-money-double"),
    # 33 mega-baller + Bryan Johnson (BJ beat survives)
    (3695.43, 3703.00, "s33-recap-transition"),
    (3730.97, 3737.35, "s33-proven-benefit-restate"),
    (3755.40, 3759.70, "s33-far-more-things"),
    (3768.73, 3772.99, "s33-beyond-scope"),
    # 34 summary — cut hardest, retention dies in recaps
    (3851.37, 3854.95, "s34-stop-right-now"),
    (3862.95, 3872.75, "s34-improve-right-away"),
    (3886.59, 3889.05, "s34-laid-out-list"),
    (3901.25, 3905.43, "s34-improve-life-tremendously"),
    (3942.07, 3945.88, "s34-rational-to-invest"),
    # 35 outro — untouched (conversion)
]
