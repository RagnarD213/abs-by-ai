SRC_PATH = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1512.MP4"
# black point 0.079 -> crush; gentle S-curve. NO white-balance shift: the warm
# tone IS the spray tan, which is the subject of the video.
GRADE = "curves=all='0/0 0.079/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'"
RANGES = [
 (135.85, 161.45, "intro"),                 # take 4, clean restart (takes 1-3 dropped)
 (193.65, 262.05, "why-cameras-flatten"),
 (273.75, 295.20, "use-cases"),
 (305.60, 330.15, "ai-picked-studio-a"),
 (333.70, 357.20, "ai-picked-studio-b"),    # drops "for people in my local," restart
 (368.30, 406.50, "what-i-paid"),
 (414.50, 428.70, "diy-options-a"),
 (434.90, 456.20, "diy-options-b"),         # drops "These type of things..." false start
 (459.25, 483.20, "diy-helper"),            # self-correction kept (no clean internal cut)
 (489.30, 565.05, "the-appointment"),
 (568.85, 578.00, "theyre-professionals"),
 (584.50, 612.85, "drying-time"),
 (618.85, 635.95, "dont-sleep-in-it"),
 (638.85, 678.70, "first-shower"),          # zero-length cluster inside: kept contiguous
 (689.60, 721.70, "ongoing-care"),          # drops "Now, after this," false start
 (728.20, 753.90, "how-long-it-lasts"),
 (757.00, 782.95, "pale-fades-faster"),
 (791.75, 836.50, "water-is-the-enemy"),    # drops the repeated "in my normal life"
 (858.70, 892.00, "before-after-photos"),   # PHOTO INSERT
 (916.90, 960.40, "pro-no-sun-damage"),
 (976.60, 1001.35, "sun-damage-facts-a"),   # drops fumbled first take at 965
 (1005.00, 1050.90, "sun-damage-facts-b"),  # drops "So sun damage, even though." false start
 (1061.60, 1076.05, "most-important-reason"),
 (1082.40, 1111.45, "if-youre-pale"),
 (1118.50, 1153.65, "go-subtle"),
 (1172.40, 1217.30, "con-money"),
 (1238.30, 1250.30, "con-self-apply"),
 (1256.10, 1285.20, "con-orange"),          # stumble kept (no clean internal cut)
 (1288.45, 1307.70, "con-wears-off"),
 (1324.30, 1349.80, "who-vampires"),        # drops the aborted question
 (1355.90, 1365.35, "who-strapped"),        # second take; drops "So that way the clothes,"
 (1372.50, 1391.55, "who-not-poor"),
 (1405.10, 1422.80, "who-appearance-pays"),
 (1431.30, 1436.20, "pays-dividends"),      # drops the fashion/hairdressing repeat
 (1452.40, 1474.55, "most-of-you-middle"),
 (1482.00, 1500.30, "what-i-recommend"),
 (1515.00, 1540.50, "maximize-lighting"),
 (1544.25, 1552.15, "get-a-pump"),
 (1556.05, 1563.35, "shoot-fasted"),
 (1569.60, 1581.25, "practice-posing"),
 (1583.75, 1599.90, "summary"),
 (1777.45, 1838.20, "outro"),               # final take (3 earlier outros dropped)
]
