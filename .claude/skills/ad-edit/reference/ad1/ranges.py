# AD 1 — "How AI Got Me Abs" — C1591 (8/14 shoot, teleprompter roll)
# Hook = TAKE 2 (slated master pass) pending Dan's pick from the take reel.
# Take-1 alternative for the hook: (3.66, 35.16).
SRC_PATH = "/Volumes/Seagate 4TB/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1591.MP4"
# black point 0.032 -> crush; mid lift for the dark night-kitchen look.
# NO WB shift: skin tone is prominent (tank top) — longform rule.
GRADE = "curves=all='0/0 0.032/0.005 0.25/0.315 0.50/0.60 0.80/0.875 1/1',eq=saturation=1.06"
RANGES = [
 (50.26, 82.84,  "hook"),           # "This picture got me abs" ... "for free." (TAKE 2)
 (83.68, 147.14, "conditioning1a"), # "Now, let's be honest" ... "...you lost your stomach fat."
                                    # (keeps the FIRST clean instance; 147.9-154.3 is a faltering
                                    #  re-attempt with 2s pauses — Dan's 1:33 junk note, cut)
 (154.30, 197.90, "conditioning1b"),# "You'd realize how much better..." thru CTA1, Listen block,
                                    # ends "...what you already know."
 (203.32, 307.96, "situation-product"), # 2nd "That's exactly the situation..." (stretched 1st word,
                                    # builder refines onset) thru CTA2, product detail,
                                    # ends "...equipment you actually have."
 (354.80, 376.24, "ending-pickup"), # clean pickup retake: "Your nutrition plan..." -> "tap the button below."
]
