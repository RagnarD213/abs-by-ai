# The $17 Ab Wheel Beats Every Crunch -- 8/14 shoot, rolls C1630-C1633.
# Every cut carries a comment saying what it removes.
SHOOT = ("/Volumes/Seagate 4TB/abs by ai 8:14 shoot | teleprompter ads, "
         "indoor talking content, outdoor workout content | jeff chagrin | dan rose")
SOURCES = {b: f"{SHOOT}/{b}.MP4" for b in ("C1630", "C1631", "C1632", "C1633")}

# Outdoor, bright daylight, WB neutral (dev 0.002-0.016), exposure already good
# (median lum 0.52-0.55) and highlights ALREADY clipping ~6% -- so this grade
# crushes the milky blacks ONLY and holds mids/highlights near identity.
# Crush point = that roll's own measured black point (longform-edit Step 6).
def crush(blk):
    return (f"curves=all='0/0 {blk}/0.005 0.30/0.294 0.55/0.550 0.85/0.848 1/1'")
GRADES = {"C1630": crush(0.112), "C1631": crush(0.108),
          "C1632": crush(0.108), "C1633": crush(0.104)}

RANGES = [
 # ---------- INTRO (C1630: three takes; take 3 is LATER but NOT fluent --
 # it stalls 1.3s on "sold" and drops the plural in "infomercials are scams",
 # so later-take-wins does not apply. Take 2 is clean end to end.)
 ("C1630",  55.10,  75.98, "intro"),

 # ---------- WHY THE AB WHEEL (C1631)
 # A -30dB silence starts at 25.70, but the trailing "-es" of "crunches" is an
 # unvoiced fricative sitting BELOW that threshold -- speech really runs to 25.99
 # (measured at -45dB). The stretched-last-word rule put the out at 25.75 and the
 # finished render said "crunch". rawout past the fricative.
 ("C1631",   3.74,  26.05, "why-1-constant-tension", "rawout"),  # PiP insert here
 ("C1631",  45.68,  67.34, "why-2-progression"),        # drops 18s reposition
 ("C1631",  81.10, 113.26, "why-3-all-ab-muscles"),     # + total-body point
 ("C1631", 126.78, 142.20, "why-4-cheap-and-small", "rawout"),  # "home." tail is not
                                                        # silent until 142.13 -- a word-end
                                                        # out at 140.98 would clip it

 # ---------- HOW TO DO IT (C1631)
 ("C1631", 155.76, 158.30, "to-the-floor"),             # drops crew: "angles are good"
 ("C1631", 164.60, 221.92, "form-back-and-arms"),       # mat / flat back / locked arms
 ("C1631", 236.90, 249.74, "pace-why"),                 # take 1 has the TEACHING...
 ("C1631", 267.34, 288.12, "pace-demo"),                # ...take 2 has the DEMOS; keeps
                                                        # the 6.2s silent proper-pace demo

 # ---------- THE PROGRESSION (C1632, one clean take)
 ("C1632",   1.90,  55.82, "progression-levels"),       # beginner -> intermediate -> nose down
 ("C1632",  68.26,  93.06, "standing-variation"),       # drops 12s wall reposition

 # ---------- THE LIVE WORKOUT (C1633)
 ("C1633",  20.36,  32.22, "live-how-many-reps"),       # take 2; drops take 1 ("am I in frame")
 ("C1633",  37.84,  44.52, "live-three-sets"),          # drops the "three VACUUMS" misspeak
 ("C1633",  75.00, 143.64, "set-1", "rawin"),           # silent set + "that's my first set"
 ("C1633", 154.38, 206.62, "set-2"),                    # drops crew chatter 66-74
 ("C1633", 212.72, 228.44, "glasses-and-pump"),         # the sunglasses aside + "feeling the pump"
 ("C1633", 231.28, 288.26, "set-3"),                    # lead-in + set + out-of-breath reaction

 # ---------- OUTRO + CTA (C1633: five takes; take 5 is the last AND fully
 # fluent AND the only one carrying subscribe + CTA + sign-off in one run.
 # Take 4 (417-437) contains a Whisper degenerate cluster and a doubled line.)
 ("C1633", 450.52, 488.24, "outro-cta"),                # drops the duplicated sign-off at 490
]
