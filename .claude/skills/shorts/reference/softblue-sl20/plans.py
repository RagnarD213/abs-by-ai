"""SL-20: three Shorts from RO-20 "Why You Should Invest More In Your Health" as data. Film seconds are on the APPROVED RO-20 round 4
master (16:11.6, sha 41e0949a, Dan finalized 2026-10-20). Picture: the film's own graphics-free base.mp4 (same frames and clock).
Dan's picks 2026-11-05: C (online dating, Short 1), B (relationship; Dan titled it "Why being fat destroys your relationship" and chose B
over D when asked), G (money does you no good if you're dead). Titles are Dan's own words.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the master's own mix (snap.py, 10 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq + ai (chip xy, u))
        Every cover is the film's own approved cutaway at the film's own in-point (plan_resolved.json src@start), except G's B0214.
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken (the film's corrected words), ` | ` at each audio piece join; `shown{spoken}` for the aligner"""
CL = "/Volumes/Expansion/_edit_work/SL-20/clips/"           # copies; never read from another session's build folder at render time
DISC = {}
MASTER_CUTS = []                            # the film's presenter-segment boundaries are all in silence.json joins (layout.json)
Y0 = {"full": 0, "mid": 0}                  # roll C1511 framed the top of his hair at the frame edge (RO-20 round 1, reported unfixable): no headroom to give
KEEP = 0.90
TRIM = {"B": [(102.80, 103.30, 0, 0.37)]}      # R1b (reviewer B): the 0.63 s pause after "right now" (102.75-103.38, under the Cb01 cutaway) keeps 0.33 s
SEG = {
 # C: picture join 201.401 (shot date1.0r1); "Now" onset 201.43 (-36 dB), no dip between "Now" and "in" (201.68 -14 dB), so "Now" stays.
 # "paramount." ends 211.6, silence 211.71-212.01. "If" onset 225.75 (silence 225.37-225.74). "nothing." ends 273.11, room to 273.47, "So," 273.50.
 "C": [[201.405, 211.90], [225.55, 255.795], [256.21, 273.40]],      # R1b (reviewer C): "make such a, such a huge": the repeat "such a" (255.80-256.20, its "s" from 255.80) is cut; "huge" from 256.21 (dip to -39 dB)
 # B: "So" (99.26) decays by 99.78 (-49 dB), "let's" 99.89: the Short opens on "Let's say". "you." ends 139.01 (silence to 139.64).
 # "So if you're married": quiet 173.00-173.16 (-40 to -54 dB), "So" 173.22 (kept: it runs into "if"). "health." ends 180.85; next word 181.18.
 "B": [[99.79, 139.40], [173.08, 174.00], [174.24, 181.00]],      # R1b (reviewer B): the half-started "or" (174.03-174.18) between "married" and "and" is cut in its two dips (-37 dB at 174.00, -39 at 174.24)
 # G: "make." ends 710.67 (silence to 711.01), "A" 711.07. "health." ends 767.58, silence to 767.99 ("Now" after it).
 "G": [[710.85, 739.41], [739.51, 767.85]],      # R1c (reviewer G): piece 1 runs to 739.41 (-57 dB, just before the "b-") so the pause after "work," is 0.41 s; the end is 767.85 ("health." ends 767.58), before the film's camera cut at 767.876 (a last-frame flash)      # R1b (reviewer G): a 60 ms half-started "b-" (739.42-739.48, -9 dB) before "just being slaves" is cut in the silences either side
}
PICKUP = {}
PATCH = {}
WORDFIX = {"C": [("a", 40.72, 40.56, 40.65)]}      # R1c: CTC put "a" (film 255.59-255.71, before the 255.795 join) after the join; measured levels
NAME = {"C": "invest-short1_dont-bother-dating-unless-youre-ripped",
        "B": "invest-short2_why-being-fat-destroys-your-relationship",
        "G": "invest-short3_you-cant-afford-to-not-work-out"}
TITLE = {"C": ("ONLINE DATING", ["Don't Bother Dating", "Unless You're Ripped"]),
         "B": ("RELATIONSHIPS", ["Why Being Fat Destroys", "Your Relationship"]),
         "G": ("MONEY AND HEALTH", ["You Can't Afford To", "NOT Work Out"])}
COVERS = {
 "C": [dict(id="Cb08", a=203.38, b=211.90, src=CL + "Cb08.mp4", t=1.0, fx=0.40),          # film Cb08, R1b: held to 211.90 over "looks are paramount" (reviewer C: he looks at the floor and jerks his head up there); (Pexels): over a man's shoulder, his thumb flicking women's photos on a dating app
       dict(id="Cb10", a=233.07, b=238.36, src=CL + "Cb10.mp4", t=3.5, fx=0.5),           # film Cb10 (Pexels): a woman on her couch flicks through profiles, screen to camera ("they swipe left on you")
       dict(id="Cb10b", a=254.40, b=257.31, src=CL + "Cb10.mp4", t=12.0, fx=0.62),      # R1c (reviewer C): he says "is going to make such a" with eyes shut and head down (film 254.4-255.8); the film's Cb10 stock (a later, unused stretch) covers it and the "such a | huge" join, straight into Cb11
       dict(id="Cb11", a=257.31, b=264.97, src=CL + "Cb11.mp4", t=0.0,      # R1b: 1x (never slowed, VIDEO-RULES 2026-10-08); runs to frame 229: frames 223-235 are the same static Matches screen as reviewed frame 224 (max pixel difference 2)
                 # R1b: from the silence before "and I know this" (no lone "and" caption); 0.975x keeps it inside the reviewed frames 0-224
            fit="tall", ar=480 / 1030, pre="crop=480:1030:415:25", ai=(377, 322, 1.6)),   # film Cb11 card: A0089 (AI dating app) in the approved shell; the phone alone, shown whole above the captions (the card's text panel is 16:9-only)
       dict(id="Cb12", a=268.25, b=273.40, src=CL + "Cb12.mp4", t=0.5,      # R1b: from the silence before "The guys" and 0.5 s into the card (its diagram already in; reviewer C: a one-frame "The" over an empty box)
            fit="tall", ar=600 / 1020, pre="crop=600:1020:145:30")],                       # film Cb12 card: Dan's own winner-take-all diagram (ten women, ten men), shown whole
 "B": [dict(id="Cb01", a=101.20, b=105.18, src=CL + "Cb01.mp4", t=0.5 + (101.20 - 99.166),      # R1b: from "in a relationship" (reviewer B: "right now" was split across two captions at the cut)
            fit="span", span=(0.50, 0.90)),    # film Cb01 (Pexels): a wife sets a plate in front of her husband (span 0.50-0.90 holds both; a centred fill crop lost her); the Short opens on Dan (2.3 s) and cuts to it on "right now"
       dict(id="Cb02", a=122.42, b=124.87, src=CL + "A0032.mp4", t=0.0, fit="whole", y=460, ai=(40, 336, 1.6)),   # film Cb02, library AI A0032: the wife's eyes follow a fit man past the table. A whole 16:9 card: the source is 848x480 (a fill crop would be a 3.4x blow-up) and the story needs all three people
       dict(id="Cb03", a=124.87, b=129.56, src=CL + "Cb03.mp4", t=0.87,      # R1b: from the silence before "Those are the reasons" (reviewer B: a lone "that's" caption at the old cut 126.00)
            fx=0.5),           # film Cb03 (Pexels): a woman's hands slide her wedding ring off
       dict(id="Cb06", a=176.00, b=181.00, src=CL + "B0485.mp4", t=1.0, fit="whole", y=560, eq="curves=all='0/0 0.15/0.07 0.5/0.46 1/1',eq=saturation=1.2"),      # R1c (reviewer B): whole 16:9 card (the handheld drift cut the mother out of the span crop), above the captions; graded toward the film (it had no blacks and weak colour)
                # R1b: library stock B0485 (used in RO-10, RO-08): a family at dinner, the father serving salad. Replaces A0072: its clean frames (6-143) are 0.23 s short of the slot, and a clip is never slowed or held to fill one (VIDEO-RULES 2026-10-08)
       ],   # (A0072 was here in R1: frame-reviewer 2026-11-05 passed frames 6-143 only; greens appear on a plate at 146-148)
 "G": [dict(id="B0214", a=724.00, b=729.45, src=CL + "B0214.mp4", t=0.3, fx=0.5, eq="eq=saturation=0.55")      # R1b (reviewer G): the stock read orange, saturation 0.73 against Dan's 0.21-0.36
           ,       # NEW (library stock, used in My First Spray Tan): hands pass a fan of hundred-dollar bills, on "If you have millions of dollars, and you just pass it on to your heirs"; runs into Cc12 (B-roll share 30 %+)
       dict(id="Cc12", a=729.45, b=736.336, src=CL + "B0535.mp4", t=0.5 + 0.355, fx=0.5),       # film Cc12 from 729.45 (after "at all.", so no caption straddles the clip-to-clip cut), library stock B0535: a worn-out man slumps on his desk ("Your life was a total waste if you spent it all working")
       dict(id="Cc13", a=754.50, b=761.427, src=CL + "Cc13.mp4", t=0.446,      # R1b: from 754.50 (reviewer G: one frame of the next master shot flashed before it at 754.554)
            fit="span", span=(0.10, 0.90))],     # film Cc13 (Pexels): a woman pushes papers to two lawyers (the family lawsuits)
}
SPLIT = {"C": [], "B": [], "G": []}
# Windows: the film's own wide (face about 250-285 px) and close (330-390 px) cameras keep their native 1.3x difference in the
# full window, so every master W/T cut stays a real size step; where two same-size shots meet, one goes to the mid window (1.2x punch-in).
# Every key-point bar sits on one steady FULL window (C #6, B #8, G #6): in the mid window his chin reaches the bar's top.
SHOTS = {"C": {0: dict(win="full"), 2: dict(win="full"), 4: dict(win="full"), 5: dict(win="full"), 6: dict(win="mid"), 9: dict(win="full")},      # R1c indices; R1d: #6 mid (gate cut:jump_cut: he leans in at the end of wide #5, face 284-308 px, against close #6 at about 341: 1.14x, under the 1.15x size step)
         "B": {0: dict(win="full"), 2: dict(win="full"), 3: dict(win="full"), 4: dict(win="mid"), 7: dict(win="mid"), 8: dict(win="full"), 9: dict(win="mid"), 10: dict(win="full")},
         "G": {0: dict(win="mid"), 1: dict(win="full"), 4: dict(win="full"), 5: dict(win="mid"), 6: dict(win="full"), 7: dict(win="full"), 9: dict(win="full")}}      # G: R1c indices (part 3 cuts corrected)
BARS = {
 "C": [dict(id="G1", topic="KEY POINT", parts=[["Only The Top 10% Get Seen", "It's only once you"], ["Looks First, Personality Later", "women are even open"]], a=-0.2, b=2.6)],      # inside one shot (#6, 26.96-34.93): a bar never crosses a picture cut (SL-18)
 "B": [dict(id="G1", topic="KEY POINT", parts=[["Getting Fat Changes", "and because of that,"], ["How She Sees You", "she perceives all"]], a=-0.2, b=2.2)],
 "G": [dict(id="G1", topic="KEY POINT", parts=[["Money Can't Buy Health", "But that is just"], ["Health Comes First", "I just want you"]], a=-0.2, b=2.0)],      # R1b (reviewer G): on the WIDE opening shot #1 (full window): on the close shots the box reached his chin when he lowered his head
}
TEXT = {
 "C": "Now, in today's dating environment, over 70%{seventy percent} of people are meeting on dating apps or meeting online. In the modern online dating environment, looks are paramount. | "
      "If you're a little fat, if you look a little sloppy, especially if you combine that with other factors such as being short like myself, they swipe left on you, they never see your personality, they never see how much money you have, "
      "nothing matters except the way you look if you don't look good. It's only once you crack into that top 10%{ten percent} best looking guys in the world that women are even open to knowing what your personality is. "
      "So in the modern dating environment, losing even 5{five} or 10{ten} pounds is going to make such a | huge difference, and I know this because I'm someone who was in decent shape before and I got in really good shape, and it 10x{ten x} my matches. "
      "The modern dating environment is winner take all. The guys at the top are taking everything. The bottom 80%{eighty percent} are getting nothing.",
 "B": "Let's say that you're in a relationship right now and you're getting a little bit overweight. Now, your partner might not consciously say, hmm, my husband's getting a little fat and sloppy. I'm going to divorce him for getting fat. "
      "Instead, what she'll think is, oh, my husband just doesn't really care about me like he used to. My husband isn't as funny as he used to be. I'm just not enjoying sex with my husband as much as I used to. The spark, the chemistry isn't there. "
      "Those are the reasons that's going to pop into her mind for why she divorces you and leaves you lonely. However, if you look at the real reason a lot of the times, it's because you got fat, you got lazy, and because of that, she perceives all these negative traits about you. | "
      "So if you're married | and you're in a relationship right now, if your top priority is your family and your relationship, then you have to care about your health.",
 "G": "A lot of people think, oh, I can just deal with average or mediocre health if I just have a little bit more money. But that is just totally wrong thinking. I just want you guys to remember, money doesn't do you any good if you're dead. "
      "If you have millions of dollars, and you just pass it on to your heirs, you did not benefit from that at all. Your life was a total waste if you spent it all working and then you did not even live long enough to spend the money. "
      "Now, a lot of people justify a life of work, | just being slaves to their job or to their business, by saying, maybe I won't be around to spend all my money, but my children or whoever my heirs are, they're gonna benefit from this. But I really don't think that they will. "
      "Both sides of my family, both sets of grandparents, my extended family started suing each other and wasted more money on the legal fight than they inherited. "
      "This is probably what's going to happen to you if you leave a big pile of money behind and you die prematurely because of neglecting your health.",
}
