# REV1 item 5 -- Dan: "there shouldn't be more than 30 seconds without a clip or
# some kind of graphic... I'd rather have a little bit too much and eliminate
# them than not enough."
#
# Times are OUTPUT seconds on the rev1 cut (18:53.31). Existing J2 chips already
# cover 26 windows; these fill every gap between them. Kinds:
#   clip   full-frame stock cutaway (Pexels, free licence, $0)   -> pre-rendered MP4
#   card   J2 fact card, full frame                              -> PNG overlay
#   photo  before/after panel from build_photos.py               -> PNG overlay
# STOCK[key] = (pexels_id_prefix_of_filename, seek_seconds_into_the_clip)

STOCK = {
 "photog":      ("12331347_photographer-camera", 2.0),
 "mirror":      ("6547791_mirror-flex",          1.5),
 "lighting":    ("33940049_studio-lighting-rig",  0.6),   # REV2 recast
 "stage":       ("28029794_physique-stage",      12.0),   # REV2 recast
 "bbflex":      ("5319758_bodybuilder-flex",     3.0),
 "gym":         ("5319433_gym-workout",          4.0),
 "shoot1":      ("3917517_photog-model-blonde",   3.0),   # REV2 recast
 "dating":      ("6833576_dating-app",           3.0),
 "wedarch":     ("34506426_wedding-archway",     1.5),
 "laptop":      ("8519534_man-laptop",            2.0),   # REV2 recast
 "maps":        ("6258206_phone-maps",           1.0),
 "bts":         ("33191906_bts-photoshoot",      1.0),
 "money3":      ("4524511_counting-money3",      4.0),
 "shootcouple": ("33940041_softbox-setup",        1.5),   # REV2 recast
 "cardread":    ("11158789_card-reader",         1.5),
 "aerosol":     ("6950943_aerosol-spray",        0.4),
 "bodycream":   ("12220106_body-cream",          6.0),
 "wedchurch":   ("31010685_wedding-church",      0.15),
 "sunarm":      ("7467141_sunscreen-arm",        2.0),
 "shoulder":    ("7467132_lotion-on-mans-back",   1.5),   # REV2 - Dan: applied to someone's BACK
 "gloves":      ("7820111_beautician-gloves",    6.0),
 "consult":     ("4824010_cosmetologist-talk",   8.0),
 "money2":      ("5466769_counting-money2",      2.0),
 "towel":       ("19919757_towel-bathroom",      2.0),
 "salon":       ("8830118_hairdresser",          2.0),
 "device":      ("4824011_cosmetologist-device", 1.0),
 "sheets":      ("7607770_bed-sheets",           3.0),
 "showerhead":  ("15887131_shower-head",         2.0),
 "loofah":      ("7250838_loofah-scrub",         2.0),
 "showerdrop":  ("9166287_shower-drops",         6.0),
 "brush":       ("8955751_makeup-brush",         6.0),
 "soap":        ("9474176_soap-bars",            1.5),
 "redhead":     ("10210876_redhead-portrait",    3.0),
 "beachsleep":  ("8731175_beach-sleeping",       1.5),
 "swim":        ("6012511_man-swimming",         4.0),
 "pool":        ("4114689_pool-dip",             1.5),
 "paddle":      ("10070229_paddleboard",         2.0),
 "boat":        ("2711208_motorboat",            4.0),
 "sun":         ("3637063_sun-blue-sky",         1.0),
 "umbrella":    ("7539035_umbrella-dock",        2.0),
 "beachaerial": ("19735225_beach-aerial",        4.0),
 "mole":        ("5701568_mole-check",           8.0),
 "manface":     ("7299500_elderly-face",          2.0),   # REV2 - Dan: older, sun-damaged skin
 "sunbathe":    ("992677_man-sunbathing",        0.6),
 "freckmacro":  ("7298115_wrinkled-forehead",     2.0),   # REV2 recast - leathery, weathered
 "lab":         ("8771135_man-microscope",        3.0),   # REV2 recast
 "bills":       ("5466780_hundred-bills",        2.0),
 "freckvid":    ("8724227_freckled-video",       8.0),
 "freckwoman":  ("8055996_freckled-woman",       1.5),
 "lotion":      ("7117543_applying-lotion",      6.0),
 "cashvert":    ("6326861_counting-cash",        3.0),
 "meals":       ("5866259_healthy-meals",        1.0),
 "creditcard":  ("8465178_credit-card",          2.0),
 "hairspray":   ("9785834_hairspray-finger",     1.0),
 "lips":        ("8056004_freckled-lips",        1.5),
 "containers":  ("7250804_food-containers",      2.0),
 "vlog":        ("6332248_vlog-recording",       1.5),
 "handshake":   ("7643473_handshake",            1.0),
 "runway":      ("19862866_fashion-model",       6.0),
 "posing":      ("9441682_photographer-model",    2.0),   # REV2 recast
 "brideglaugh": ("34503193_wedding-kiss-outdoor", 1.5),   # REV2 recast
 "goldlight":   ("8770369_sunlight-posing",      2.0),
 "photogf":     ("7570995_posing-coaching",       4.0),   # REV2 recast
}

# REV2 (2026-08-22) recast 12 clips toward the target demographic - white or
# Asian men 30-50 - and re-picked the female-featuring clips. Two of Dan's swaps
# are specific: 4:01 is now someone actually applying to another person's BACK,
# and 11:05 is an older face with real sun damage instead of a young freckled
# one. Replaced sources are marked "REV2 recast" in STOCK above; the rev-1 list
# is kept as inserts_rev1.py.bak.

# (start_out, duration, kind, key, note)
INSERTS = [
 # ---- ITEM 1: "here on the left ... and here on the right" (off by 0:11.36)
 # intro_both CONTAINS intro_left, so the left panel holds at full opacity and
 # the two-up fades in ON TOP of it. Cross-fading them instead would dip the
 # left photo out and back in around 7.0s.
 (  3.50, 3.80, "photo", "intro_left",  'L panel only; "here on the left"'),
 (  6.95, 4.25, "photo", "intro_both",  '+ R panel; "and here on the right"'),

 # ---- cameras flatten you
 ( 37.20, 4.20, "clip", "photog",     "cameras tend to flatten your definition"),
 ( 45.60, 4.00, "clip", "mirror",     "looking at myself in the mirror"),
 ( 57.20, 4.00, "clip", "lighting",   "the lighting and what the photographer did"),
 ( 68.90, 4.40, "clip", "stage",      "fitness models and bodybuilders spray tan"),
 ( 75.20, 4.00, "clip", "bbflex",     "going very dark increases definition"),
 ( 88.00, 3.60, "clip", "gym",        "even if you're muscular"),
 ( 95.80, 3.20, "clip", "shoot1",     "if you're doing a photo shoot"),
 ( 99.30, 3.00, "clip", "dating",     "if you're doing dating pictures"),
 (102.80, 3.40, "clip", "wedarch",    "an important event such as a wedding"),

 # ---- I asked my AI
 (128.00, 4.20, "clip", "laptop",     "uploaded my pictures into my AI"),
 (141.20, 4.40, "clip", "maps",       "AI found a studio a few miles away"),
 (153.60, 5.00, "card", "askai",      "go to Claude / ChatGPT / Gemini"),
 (159.40, 3.40, "clip", "bts",        "find me the three best options"),

 # ---- what I paid
 (173.00, 4.20, "clip", "money3",     "$80 base + $20 contouring"),
 (178.40, 5.20, "card", "cost",       "about $100 altogether"),
 (185.20, 4.00, "clip", "shootcouple","important for my social media"),
 (196.50, 4.00, "clip", "cardread",   "about $50 if you skip the contouring"),

 # ---- DIY options
 (209.90, 3.60, "clip", "aerosol",    "aerosol do-it-yourself at home tans"),
 (213.80, 3.60, "clip", "bodycream",  "tanning wipes you use at home"),
 (223.50, 3.10, "clip", "wedchurch",  "on a date or for a wedding"),   # source is only 3.32s
 (230.00, 3.80, "clip", "sunarm",     "just your arms and your face"),
 (241.00, 4.40, "clip", "shoulder",   "someone who can spray your back"),
 (251.50, 4.20, "clip", "gloves",     "I recommend going professional"),

 # ---- the appointment (78s gap, the biggest)
 (266.50, 4.00, "clip", "consult",    "strip down to your briefs"),
 (274.00, 5.40, "card", "briefs",     "briefs, not boxers"),
 (288.00, 4.20, "clip", "money2",     "you're spending the money on this"),
 (297.00, 4.00, "clip", "towel",      "briefs I was comfortable destroying"),
 (313.00, 4.20, "clip", "salon",      "a woman who's going to be assessing you"),
 (324.90, 5.00, "card", "rededicate", "it makes you train harder"),
 (334.50, 4.00, "clip", "device",     "these people are professionals"),

 # ---- drying time
 (352.00, 5.40, "card", "drying",     "8 hours vs 24 hours"),
 (362.50, 4.20, "clip", "consult2",   "what my tanning specialist told me"),
 (377.00, 4.40, "clip", "sheets",     "you'll destroy your sheets"),
 (383.50, 4.00, "clip", "showerhead", "shower before you get into bed"),

 # ---- the first shower
 (399.50, 5.40, "card", "firstshower","no soap, no washcloth, no scrubbing"),
 (407.00, 4.20, "clip", "loofah",     "scrubbing off that layer of dead cells"),
 (414.50, 4.20, "clip", "showerdrop", "a bunch of brown water comes off"),
 (421.00, 4.20, "clip", "brush",      "the cosmetic makeup they used"),

 # ---- ongoing care
 (440.00, 5.60, "card", "ongoing",    "no washcloths / no acids"),
 (450.00, 4.20, "clip", "soap",       "be gentle with the soap you use"),

 # ---- how long it lasts
 (486.00, 4.20, "clip", "redhead",    "very pale people going much darker"),
 (503.00, 4.40, "clip", "beachsleep", "naturally more tan skin lasts longer"),

 # ---- water is the enemy
 (520.00, 4.00, "clip", "swim",       "the pool, the lake, the beach"),
 (534.20, 2.60, "clip", "pool",       "I have a pool I go in all the time"),
 (536.90, 2.80, "clip", "paddle",     "I go paddle boarding all the time"),
 (539.80, 3.00, "clip", "boat",       "boating"),

 # ---- ITEM 3: three before/after pairs, ~5.8s each
 # the three pairs OVERLAP by 0.30s and cross-dissolve into each other; a gap
 # between them would flash Dan back on screen for a third of a second.
 (564.20, 6.10, "photo", "pair_a",    "pair 1 - standing front"),
 (570.00, 6.10, "photo", "pair_b",    "pair 2 - hands at hips"),
 (575.80, 6.20, "photo", "pair_c",    "pair 3 - double biceps"),

 # ---- sun damage (111s gap, the second biggest)
 (607.00, 4.20, "clip", "sun",        "the sun is more damaging than people think"),
 (614.50, 5.20, "card", "bryan",      "off-peak hours only, umbrella in the sun"),
 (627.00, 4.20, "clip", "umbrella",   "he takes an umbrella out with him"),
 (636.50, 5.40, "card", "cancer",     "skin cancer is one of the most common"),
 (643.50, 4.20, "clip", "beachaerial","if you go out in the sun a lot"),
 (648.50, 4.20, "clip", "mole",       "sun damage goes beyond your skin"),
 (665.00, 4.20, "clip", "manface",    "it also makes you look older"),
 (671.50, 4.20, "clip", "sunbathe",   "people who live in Florida"),
 (679.50, 4.20, "clip", "freckmacro", "visibly more leathery and wrinkled"),
 (693.50, 4.20, "clip", "lab",        "your cells would function younger"),
 (708.00, 4.20, "clip", "bills",      "if you have the money and value how you look"),

 # ---- if you're pale / go subtle
 (724.50, 4.40, "clip", "freckvid",   "if you're a ginger, translucent white skin"),
 (731.00, 4.20, "clip", "freckwoman", "sunburn, freckles and blemishes"),
 (754.00, 5.00, "card", "subtle",     "a little darker than you are now"),
 (761.50, 4.20, "clip", "lotion",     "going subtle makes it last longer"),
 (768.50, 5.20, "card", "darkonpale", "dark on pale = 3-4 days"),

 # ---- the money con
 (789.50, 4.20, "clip", "cashvert",   "$50 to $100 per tan"),
 (797.50, 4.20, "clip", "meals",      "gym membership or meal prep service"),
 (806.00, 5.80, "card", "order",      "spend in this order"),
 (819.50, 4.20, "clip", "creditcard", "funds to buy all that easily"),

 # ---- the orange con
 (847.50, 4.20, "clip", "hairspray",  "more orange if it's not done well"),
 (860.00, 5.00, "card", "orange",     "cheap = orange, premium = natural"),

 # ---- who should
 (896.50, 4.20, "clip", "lips",       "your skin looks translucent"),
 (905.50, 4.00, "clip", "cardread2",  "invest a little money in that spray tan"),
 (913.00, 4.00, "clip", "bodycream2", "at least do the wipes or the spray"),

 # ---- who should not / appearance pays
 (929.00, 4.40, "clip", "containers", "meal prep, gym membership, the essentials"),
 (936.50, 4.20, "clip", "bbflex2",    "once you have the body to show off"),
 (943.50, 4.20, "clip", "vlog",       "if you're an influencer"),
 (949.00, 3.60, "clip", "handshake",  "dealing with clients in person"),
 (953.00, 3.40, "clip", "runway",     "an industry such as fashion"),
 (956.60, 3.40, "clip", "salon2",     "or hair dressing"),
 (960.50, 4.00, "clip", "money2b",    "it will pay dividends"),
 (968.00, 5.60, "card", "whofor",     "who it's for"),
 (981.00, 4.20, "clip", "brideglaugh","a special occasion like a wedding"),
 (990.00, 4.00, "clip", "posing",     "shooting photos or a special event"),

 # ---- maximize the shoot
 (1013.50, 4.20, "clip", "goldlight", "good light, never noon"),
 (1023.00, 4.20, "clip", "photogf",   "a good photographer and a good camera"),
 (1055.50, 4.20, "clip", "shoot1b",   "take pictures like a professional"),
 (1066.50, 4.20, "clip", "wedarch2",  "weddings, photo shoots, video shoots"),

 # ---- outro / CTA
 (1084.50, 5.60, "card", "step1",     "upload a shirtless photo"),
 (1093.50, 5.60, "card", "realyou",   "the real you, not a head on a stock body"),
 (1106.50, 5.60, "card", "trainer",   "AI personal trainer"),
 (1114.50, 5.60, "card", "nutrition", "AI nutritionist"),
 (1124.00, 6.00, "card", "cta2",      "absbyai.com"),
]

# Clips deliberately used a SECOND time, far apart (>10 min). Aliased so the
# renderer can give each use its own seek point and duration.
ALIASES = {
 "consult2":   ("device",    2.5),
 "cardread2":  ("cardread",  5.0),
 "bodycream2": ("bodycream",20.0),
 "bbflex2":    ("bbflex",   12.0),
 "salon2":     ("salon",     5.5),
 "money2b":    ("money2",    7.0),
 "shoot1b":    ("bts",       2.7),
 "wedarch2":   ("wedarch",   5.5),
}
