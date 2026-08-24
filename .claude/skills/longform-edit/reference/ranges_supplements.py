SRC_PATH = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1514.MP4"
# black point 0.054 -> crush; same gentle S-curve. WB deviation 0.008 = neutral.
GRADE = "curves=all='0/0 0.054/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'"
RANGES = [
 (37.74, 53.20, "intro"),                      # take 3 of 3
 (115.24, 156.10, "how-to-decide"),            # take 2, after "one more take of that"
 (159.64, 221.40, "youre-not-smart-enough"),   # ends before crew chatter
 (244.60, 266.10, "dont-trust-influencers"),
 (268.66, 274.15, "chatgpt-beats-nothing"),
 (299.28, 312.75, "i-built-a-tool"),           # drops two false starts
 (319.06, 336.60, "how-to-use-it"),            # drops "So, if you're a member of..."
 (368.06, 414.95, "ag1-and-the-ai-veto"),
 (418.56, 443.05, "why-i-still-take-it"),      # drops crew chatter 449-493
 (493.60, 524.75, "ag1-benefits"),
 (527.04, 532.65, "vitamin-d-a"),
 (535.80, 565.45, "vitamin-d-b"),              # drops the doubled "70% are deficient"
 (583.62, 608.10, "vitamin-d-dose"),
 (616.52, 645.65, "post-workout-food"),
 (649.08, 655.72, "protein-first-a"),
 (666.30, 670.40, "protein-first-b"),          # drops two restarts + "Synthesis."
 (673.04, 683.30, "seeds-and-almonds"),
 (686.56, 715.05, "fish-oil-and-thorne"),
 (720.64, 747.80, "fish-oil-benefits"),
 (751.96, 773.90, "fish-oil-is-proven"),
 (782.68, 790.62, "curcumin-a"),
 (797.34, 817.10, "curcumin-b"),               # drops the repeated "thorn bran" line
 (820.18, 833.70, "curcumin-concentration"),
 (838.86, 843.00, "curcumin-cheap-option"),    # second take
 (849.40, 852.05, "ginger-a"),
 (860.64, 886.90, "ginger-b"),                 # drops the Huberman repeat
 (903.50, 952.25, "glucosamine"),              # third take
 (958.32, 972.35, "skin-intro-a"),
 (977.04, 990.90, "skin-intro-b"),             # drops "I don't agree with him on anything"
 (1000.00, 1046.65, "b6-zinc-dim"),
 (1070.50, 1102.60, "testosterone-booster"),
 (1107.86, 1132.10, "ashwagandha-and-zinc"),
 (1138.48, 1163.30, "the-post-workout-drink"),
 (1168.90, 1239.00, "aminos-vs-whey"),         # drops "that I actually recommend" false start
 (1243.02, 1263.65, "magnesium"),
 (1265.96, 1270.50, "collagen-a"),
 (1274.32, 1282.35, "collagen-b"),
 (1288.66, 1300.00, "collagen-c"),             # drops the doubled "seven day a week grind"
 (1306.32, 1311.65, "collagen-brand"),
 (1318.38, 1345.10, "electrolytes-and-recap"),
 (1348.02, 1373.45, "deep-sleep-a"),
 (1379.86, 1388.90, "deep-sleep-b"),
 (1399.18, 1415.25, "creatine-a"),
 (1419.84, 1447.40, "creatine-b"),
 (1455.40, 1477.50, "this-is-too-much"),
 (1488.34, 1537.70, "my-biggest-mistake"),     # drops "I started getting real into fitness after..."
 (1548.72, 1591.20, "the-big-three"),          # second take
 (1598.32, 1612.20, "step-2-muscle-a"),
 (1618.72, 1623.45, "step-2-muscle-b"),
 (1635.98, 1648.35, "step-3-greens"),
 (1681.74, 1702.25, "step-4-skin"),            # drops two false starts
 (1722.66, 1734.05, "step-5-test-booster"),
 (1740.12, 1764.65, "never-buy-preworkout"),
 (1784.54, 1793.45, "never-buy-fat-burners"),  # third take
 (1801.64, 1826.15, "stimulants-and-appetite"),
 (1834.50, 1864.00, "wrap-start-small"),
 (1872.16, 1904.65, "supplements-are-5-percent"),
 (1910.16, 1939.60, "the-ironing-analogy"),
 (1949.52, 1957.60, "keep-it-in-perspective"),
 (1964.76, 1971.45, "thanks"),                 # drops "I hope it could..." false start
 (1977.70, 1996.25, "verify-with-ai"),
 (2183.22, 2257.00, "outro"),                  # final CTA take (2 earlier ones dropped)
]
