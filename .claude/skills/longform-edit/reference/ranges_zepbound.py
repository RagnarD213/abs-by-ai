SRC_PATH = "/Volumes/Seagate 4TB/abs by ai 8:3 jeff chagrin shoot/main camera/C1513.MP4"
# black point 0.069 -> crush; same gentle S-curve. WB deviation 0.016 = neutral,
# so no colour-channel mixing.
GRADE = "curves=all='0/0 0.069/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'"
RANGES = [
 (72.40, 92.10, "intro"),                      # take 3 of 3
 (121.00, 140.05, "why-i-started"),
 (146.60, 191.85, "heard-about-it"),           # drops "I didn't take the medication myself" dup
 (192.25, 212.85, "my-old-thinking"),
 (221.55, 310.25, "the-data-changed-my-mind"),
 (315.15, 324.65, "anecdotes"),
 (331.25, 361.30, "started-recommending-it"),  # NOTE: ex-girlfriend injection line
 (364.15, 399.90, "30-pounds-math"),
 (408.70, 453.10, "even-ripped-people"),
 (455.90, 490.70, "my-diet-was-good"),
 (494.30, 573.60, "good-isnt-perfect"),
 (576.05, 616.90, "not-medical-advice"),       # ESSENTIAL disclaimer beat
 (621.15, 653.35, "old-vs-new-thinking"),
 (676.00, 775.00, "the-transformation"),       # 192 -> 181  [PHOTO INSERT]
 (775.00, 790.60, "alcohol-knockout"),
 (791.05, 803.95, "how-much-i-drank"),         # stumble kept (no clean internal cut)
 (804.50, 826.85, "blowouts-gone"),
 (838.80, 904.95, "sugar-carbs-productivity"),
 (916.60, 936.40, "if-youre-obese"),
 (938.65, 976.00, "if-youre-ripped"),
 (976.00, 991.65, "how-to-do-it"),
 (992.15, 1023.70, "where-to-get-it"),
 (1032.40, 1087.90, "compounded-vs-brand"),    # drops the circular first take
 (1093.80, 1123.70, "no-added-ingredients"),   # drops the "There's also a lot" dup
 (1129.30, 1140.40, "lily-direct"),
 (1145.10, 1188.10, "how-to-get-a-script"),    # drops "You just go to..." + dup
 (1191.90, 1208.05, "skip-the-membership-fees"),
 (1213.90, 1315.95, "oral-pen-or-needle"),
 (1329.30, 1456.20, "where-to-inject"),
 (1461.50, 1477.60, "which-day"),
 (1484.60, 1506.00, "why-thursday"),           # drops the "24 hours" restart
 (1509.40, 1519.50, "inject-thursday-7pm"),    # drops the "weekend" dup
 (1529.05, 1574.75, "my-side-effects"),
 (1586.90, 1613.60, "escalate-gradually"),     # drops "this is avoidable" false start
 (1616.10, 1622.40, "context-max-dose"),       # drops "the amount of," stumble
 (1626.70, 1642.55, "tiny-dose"),              # drops the "less than 10%" dup
 (1645.40, 1662.95, "dose-ladder"),
 (1665.90, 1699.25, "where-i-sit-now"),
 (1703.25, 1728.35, "digestion-improved"),
 (1733.35, 1757.70, "biggest-mistake"),
 (1777.10, 1829.20, "wont-damage-your-skin"),  # drops crew chatter 1766-1775
 (1836.20, 1888.05, "it-doesnt-hurt"),
 (1895.15, 1946.85, "dont-go-above-2.5"),
 (1952.30, 1962.15, "unless-youre-obese"),
 (1981.90, 2007.00, "ice-if-youre-scared"),
 (2007.00, 2050.85, "muscle-loss-is-the-risk"),
 (2060.60, 2096.35, "protein-target"),         # keeps take 2 (matches his 200lb->160g math)
 (2115.30, 2129.90, "wrap-obese-diabetes"),
 (2142.40, 2177.65, "wrap-20-30-lbs"),         # drops the near-identical first pass
 (2200.40, 2279.00, "outro"),                  # teases the masterclass video
]
