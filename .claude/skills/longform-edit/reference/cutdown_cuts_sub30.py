#!/usr/bin/env python3
"""SUB-30 cut-down: the conservative list PLUS a second aggressive pass.
The three approved levers are here in full — therapy & psych meds dropped
wholesale (L1), the mattress-fluids riff dropped (L2), the COVID shed story
dropped (L3) — and every other section is compressed to the handoff's beat-map
target. Outline points are kept wherever a clean sentence boundary allows it."""
from cuts_cons import CUTS as CONS
EXTRA = [
    # 1 intro + halo
    (21.22,   27.70,  "x1-make-money-priority"),
    (97.86,  101.55,  "x1-funnier-personality", (8, 0)),
    # 2 job / partnership — negative direction only
    (145.24, 155.80,  "x2-partnership-positive"),
    # 3 relationship
    (190.98, 194.75,  "x3-doesnt-care-about-me"),
    (251.78, 268.10,  "x3-married-wrap"),
    # 4 dating
    (274.20, 280.25,  "x4-tremendous-difference"),
    (325.20, 329.05,  "x4-never-see-personality", (0, 0)),
    (364.24, 377.80,  "x4-top10-button"),
    # 5 productivity
    (393.40, 402.95,  "x5-logic-guys-use", (0, 8)),
    (469.22, 483.40,  "x5-first-few-days-block"),
    # 6 doctor time-cost
    (533.42, 542.20,  "x6-no-time-commitment"),
    # 7 long-term thinking
    (593.40, 614.60,  "x7-longterm-tail"),
    # 8 mental health
    (634.22, 641.00,  "x8-common-sense"),
    (670.84, 679.40,  "x8-psychologist-weekly"),
    (718.10, 730.30,  "x8-priority-retake"),
    # 9 bad health is expensive
    (747.36, 763.95,  "x9-insurance-block"),
    (789.94, 794.80,  "x9-heart-cancer"),
    # 10 diabetes story
    (829.98, 836.00,  "x10-insulin-logistics"),
    (851.50, 858.05,  "x10-one-less-toe"),
    (872.78, 884.60,  "x10-go-back-in-time"),
    (884.60, 894.95,  "x10-too-late"),
    # 11 money-dead + inheritance
    (923.12, 930.90,  "x11-mediocre-health-setup"),
    (944.32, 951.45,  "x11-pass-it-on"),
    # 12 not-dead-but-sick
    (1006.66, 1017.90, "x12-twenties-hook"),
    (1026.64, 1039.95, "x12-friend-example-vacations"),
    (1070.50, 1073.55, "x12-again-those-vacations"),
    (1138.56, 1148.90, "x12-not-only-avoid"),
    # 13 brokie pivot
    (1180.30, 1184.30, "x13-in-a-minute", (0, 0)),
    # 14 never-cut list
    (1267.85, 1272.10, "x14-luxury-crib", (0, 0)),
    (1284.16, 1293.40, "x14-everything-else-table"),
    # 15 bars & clubs
    (1360.58, 1366.05, "x15-entertainment-beat"),
    (1381.07, 1391.30, "x15-redirect-money"),
    (1450.92, 1458.35, "x15-30-rack"),
    # 16 restaurants — the AbsByAI plug (1522-1565) stays untouched
    (1469.28, 1479.00, "x16-credit-card-objection"),
    (1498.12, 1505.60, "x16-google-review"),
    # 17 junk food
    (1592.30, 1598.70, "x17-once-twice-three-times", (0, 0)),
    # 18 vacations
    (1635.56, 1644.90, "x18-my-routine", (8, 0)),
    (1665.90, 1672.60, "x18-enjoy-eventually", (0, 0)),
    # 19 LEVER 1 — therapy & psychiatric medication, dropped wholesale
    (1694.14, 1753.80, "L1-therapy-and-psych-meds"),
    # 20 sacrifice recap
    (1810.54, 1817.15, "x20-temporary-retake"),
    # 21 brokie tier
    (1843.70, 1848.50, "x21-walk-you-through"),
    (1946.84, 1961.65, "x21-steal-hypothetical"),
    (1982.40, 1994.45, "x21-cant-afford-food"),
    (2012.34, 2017.20, "x21-no-luxury-organic"),
    (2034.72, 2049.40, "x21-skip-the-rice"),
    (2064.10, 2068.90, "x21-rice-and-beans", (0, 0)),
    # 22 premium protein + 401k
    (2127.48, 2138.55, "x22-filet-mignon"),
    (2170.38, 2180.80, "x22-cant-afford-salmon"),
    (2202.80, 2215.15, "x22-omega-balance"),
    (2215.15, 2224.00, "x22-heart-dividends"),
    # 23 mattress + purple; LEVER 2 — the fluids riff dropped
    (2287.48, 2302.20, "x23-broken-mattress"),
    (2315.08, 2332.35, "x23-mattress-benefits"),
    (2376.42, 2398.60, "x23-springs-indentations"),
    (2416.57, 2490.00, "L2-fluids-and-hygiene"),
    # 24 gym membership
    (2529.67, 2545.80, "x24-afford-equipment"),
    (2619.99, 2628.80, "x24-most-ripped-people"),
    # 25 sleep tracker
    (2677.40, 2686.55, "x25-oura-subscription", (0, 8)),
    (2722.90, 2728.60, "x25-whoop-preference"),
    (2753.95, 2757.95, "x25-wrist-reason3"),
    # 26 GLP-1
    (2799.20, 2807.65, "x26-price-tag-setup"),
    (2823.73, 2836.10, "x26-crunch-time-tail"),
    (2879.23, 2888.65, "x26-fasting-hungry"),
    (2901.75, 2915.05, "x26-terz-eliminate"),
    # 27 TRT
    (2984.57, 2993.30, "x27-not-expensive", (8, 0)),
    (3014.11, 3019.80, "x27-think-long-term"),
    # 28 supplements
    (3064.50, 3077.50, "x28-ten-supplements"),
    (3105.87, 3108.90, "x28-workout-recovery"),
    (3121.03, 3126.40, "x28-older-darker-skin"),
    (3141.51, 3147.20, "x28-liquid-dropper"),
    (3149.57, 3156.70, "x28-best-cheapest-form"),
    (3187.07, 3195.80, "x28-magnesium-stat"),
    (3204.13, 3208.10, "x28-magnesium-benefits"),
    # 29 home gym; LEVER 3 — the COVID shed story dropped
    (3268.50, 3274.65, "x29-separate-structure", (0, 0)),
    (3274.20, 3300.90, "L3-covid-shed-story"),
    (3328.21, 3342.50, "x29-pays-for-itself"),
    (3345.57, 3356.60, "x29-shirtless-music"),
    (3373.39, 3399.75, "x29-both-worlds-tail"),
    # 30 meal prep / chef
    (3469.17, 3481.50, "x30-price-comparison"),
    (3487.50, 3490.95, "x30-professional-chefs"),
    (3506.57, 3512.50, "x30-still-cooking"),
    (3533.21, 3537.50, "x30-eating-healthy-easy"),
    # 31 outsource chores
    (3566.15, 3574.40, "x31-shouldnt-be-doing"),
    # 32 trainer & nutritionist
    (3603.51, 3608.45, "x32-last-thing-reason"),
    (3608.45, 3619.75, "x32-lowest-roi"),
    (3646.97, 3650.85, "x32-money-no-object"),
    # 33 mega-baller + Bryan Johnson
    (3705.00, 3718.80, "x33-mega-baller-intro"),
    (3759.63, 3765.45, "x33-thousands-per-month"),
    (3823.30, 3834.45, "x33-dont-get-distracted", (0, 0)),
    # 34 summary
    (3843.29, 3846.55, "x34-too-cheap"),
    (3854.99, 3865.25, "x34-club-bar-alcohol"),
    (3935.20, 3941.95, "x34-mega-bowler", (0, 0)),
    (3949.50, 3959.70, "x34-immortal", (0, 0)),
    # 35 outro — untouched (conversion)
]
CUTS = sorted(CONS + EXTRA, key=lambda c: c[0])
