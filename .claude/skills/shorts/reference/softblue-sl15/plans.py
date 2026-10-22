"""SL-15: two Shorts from RO-19 "Spray Tanning Guide: How To Looksmax With A Spray Tan" as data. Film seconds are on the RO-19
round 4 master (18:46.46, sha b4b30999). Dan's picks 2026-10-18 ("Let's do A and C"): A = Short 1 (airs Fri Oct 30), C = Short 2.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py + 20 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq + ai (chip xy, u)
        + speed, or scene=<name in scenes.py> for a real-photo display rebuilt for the vertical picture area)
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets (copy from the film's approved Ga03/Ga05/Gc12/Gc13)
text    the captions as spoken, ` | ` at each audio piece join (spellings from the film's corrected .srt; Bryan Johnson)"""
STOCK = "/Volumes/Extreme/_edit_work/SL-15/clips/"          # copies; never read from another session's build folder at render time
DISC = {}
Y0 = {"full": 0, "mid": 0}        # C1512: the camera framed his hair at the top row on every shot (shot_framing hair_min 0): keep all the head the source has
KEEP = 0.90
TRIM = {}
SEG = {
 # A: "If" starts 26.04 (film splice 25.99); "defined" decays to -52 dB at 54.96; "the main reason" from 59.72 after the breath; "pale" ends 62.74; "and this is" after a 0.3 s breath; "defined." ends
 # 92.92, film splice 93.19. (Piece 2 keeps his "But": 59.18-59.36 is the end of "did", the breath follows, "But" is 59.79-59.92; the delivered
 # transcript heard it, so the caption carries it: "But the main reason why is that I was too pale.")
 "A": [[26.01, 54.96], [59.72, 62.76], [67.40, 93.15]],
 # C: the leading "So" ends at 594.30 (the dip to -35 dB at 594.36 before "the"); an "Um" at 604.84-605.16 before "For those of you
 # guys" is cut (the beach clip covers that join; 0.46 s pause kept); "cancer." ends 641.80, silence to 642.38
 # Round 2 review (VIDEO-RULES 2026-10-20, stumbles): "why he, uh, takes an umbrella": "he" ends 625.56 (dip to -36 dB), the "uh" is
 # 625.62-625.96, silence 626.04-626.26, "takes" from 626.30. Cut 625.58-626.08: "why he takes", 0.22 s between them; the join is a size step.
 "C": [[594.36, 604.70], [605.22, 625.58], [626.08, 642.30]],
}
PICKUP = {}
WORDFIX = {}      # round 1 pinned "takes" onto the "uh" before it (Whisper with a disfluency prompt: "he, uh, takes"); the "uh" is now cut, so CTC stands
NAME = {"A": "short1_why-you-look-less-ripped-in-photos", "C": "short2_get-a-tan-without-sun-damage"}
EYE = "SPRAY TANNING"          # the eyebrow stays in CAPITALS (Dan, 2026-10-20, VIDEO-RULES eyebrow exception); typed, never uppercased in code
TITLE = {"A": (EYE, ["Why You Look Less", "Ripped In Photos"]), "C": (EYE, ["Get A Tan Without", "Sun Damage"])}
LIFT = "eq=gamma=1.2"
DARK = "eq=gamma=1.35:saturation=1.08"     # stock that reads darker than the presenter frames (VIDEO-RULES 2026-10-11; SL-07 value)            # the film's own lift on the studio-photographer stock (plan_resolved Cc08 fx gamma 1.2)
COVERS = {
 "A": [dict(id="photographer", a=26.01, b=28.42, src=STOCK + "p7326269.mp4", t=0.3, fx=0.93),      # the opener (first 5 seconds): "look good in photos"; the film's Ca03. fx 0.93: the photographer aiming at the camera (at 0.5 the window showed the blurred back of his subject)
       dict(id="tinder", a=28.42, b=32.56, src=STOCK + "p6833576.mp4", t=0.5, fx=0.30, eq=DARK),     # the film's Ca01: dating-app profile photos. fx 0.30 puts the phone and hand in frame (at 0.5 the phone was cut at the left edge); DARK: median brightness 0.29 against Dan's 0.42 (reviewer r2)
       dict(id="shoot", a=39.58, b=42.45, src=STOCK + "p31512200.mp4", t=0.3, fx=0.5, eq=LIFT),   # the film's Cc08 (studio shoot): "the first couple of photo shoots I did"
       dict(id="mirror", a=46.05, b=48.64, src=STOCK + "B0223.mp4", t=0.0, fy=0.4),      # round 2b review: library B0223 (real stock, native 9:16) over "myself in the mirror and I'm like, man, I'm looking good": a man checks himself in a gym mirror. Dan leans 620 px side to side on that line; the crop swung at 300 px/s to follow him
       dict(id="pale", a=48.64, b=54.96, scene="photo1", photo="pale4_single", t=0.0),          # the film's P02 (Dan's round 4 pick), a real photo: covers the join to "The main reason"
       dict(id="bodybuilders", a=69.20, b=75.10, src=STOCK + "p38627614.mp4", t=0.3, fx=0.5),    # the film's Ca02
       dict(id="pair", a=89.60, b=93.15, scene="pair", before="pale2_side", after="tan2_side", reveal=1.35)],      # singular label until the after card arrives (reviewer r2)   # the film's P05 before and after: "put a spray tan on it"
 "C": [dict(id="appointment", a=594.36, b=597.78, src=STOCK + "A4.mp4", t=0.0, speed=1.05, fx=0.42, ai=(714, 336, 1.6)),      # chip top right (chipplace: 0 overlap with any person; at top left it sat on his hair, reviewer r2)      # the opener: the film's approved appointment clip (A4), frames 0-85 at 1.05x (frame-reviewer FAIL from frame 86: his hair and stubble change by themselves); fx 0.42 = source window x 502-1226, the man and the spray gun
       dict(id="beach", a=601.83, b=604.70, src=STOCK + "p7892918.mp4", t=0.5, fx=0.5),          # the film's Cc12
       # the film's approved A1 over "looks like an ultra pale vampire,". clipcheck FAILED the take's middle (f100-110: the open umbrella turns see-through and ghosts over him
       # while he holds a closed one), so the short shows f7-f49 (pale, cowering, the tan cloud rolling in) then f146-f182 (golden, sunglasses, thumbs up)
       dict(id="vampire", a=612.38, b=613.28, src=STOCK + "A1.mp4", t=5 / 24, fx=0.42, ai=(40, 552, 1.6)),      # round 2b review: only the pale opening, f5-f26, over "ultra pale vampire," (from f28 the cloud reaches him and he tans: contradicts "he stays pale"; at f0-f3 the chip touched his raised hand: frame-reviewer). fx 0.42 = source x 502-1226
       # round 2 review: the tanned vampire2 shot (f146-182) is OUT: over "this is the reason why" (he stays pale) it showed the opposite of the line.
       # The pale shot ends at 613.55 and Dan comes back on camera in the pause before "this".
       dict(id="sunscreen", a=628.73, b=633.72, src=STOCK + "B0233.mp4", t=1.0, fx=0.5),         # the film's Cc13
       dict(id="clinic", a=633.72, b=636.80, src=STOCK + "B0208.mp4", t=1.0, fx=0.25)],          # the film's Cc14. fx 0.25: the client's face and the specialist's gloved hand at her cheek (both faces span 67 % of the width; at 0.5 her face was cut at the edge)
}
SPLIT = {
 "A": [["The reason for that", 0.0], ["Definition on camera", 0.0], ["If you're just super", 0.0], ["Even if you're", 0.0]],
 "C": [["If you ever notice", 0.0], ["he only goes out", 0.0]]      # the "uh" cut (a join) is the size step before "takes",
}
SHOTS = {"A": {2: dict(win="mid"), 3: dict(win="full"), 7: dict(cap=1650), 11: dict(win="mid"), 12: dict(win="full"), 13: dict(win="mid"), 14: dict(win="full")},      # bars G1 (#3) and G2 (#12) on the wide window; #7 the real photo: captions at y 1650 over his shorts, not across his abs (round 2b review)
         "C": {}}
BARS = {
 "A": [dict(id="G1", topic="KEY POINT", parts=[["Cameras Flatten", "cameras tend"], ["Your Definition", "to flatten"]], a=-0.2, b=1.6),
       dict(id="G3", topic="THE MAIN REASON", parts=[["I Was Too Pale", "the main reason"]], a=-0.2, b=3.0),      # round 2d review: the film's Ga04 (its "For A Fitness Shoot" half was cut with its words); lands on "the main reason", leaves at the join
       dict(id="G2", topic="KEY POINT", parts=[["Definition On Camera", "Definition on camera"], ["Is All About CONTRAST", "is all about"]], a=-0.2, b=1.6)],
 "C": [dict(id="G1", topic="THE BIGGEST PRO", parts=[["You Get The Tan", "get tan while"], ["WITHOUT The Sun Damage", "avoiding sun damage"]], a=-0.2, b=1.5),
       dict(id="G2", topic="BRYAN JOHNSON", parts=[["He Stays Pale To Avoid", "trying to avoid cancer"], ["Cancer And Skin Damage", "avoid skin damage"]], a=-0.2, b=1.9)],
}
TEXT = {
 "A": "If you guys want to look good in photos, especially if you want some good photos for Instagram or for your dating profile, then spray tanning can be especially important. The reason for that is that cameras tend to flatten your definition. Now I had this experience the first couple of photo shoots I did, but after I started getting in shape this most recent time, I was looking at myself in the mirror and I'm like, man, I'm looking good. But then I take a picture of myself in the photo shoot and I'm like, oh, I don't look anywhere near as defined. | But the main reason why is that I was too pale. | And this is the reason why if you look at all fitness models and bodybuilders, they're spray tanning to such a huge extent, they're going very dark because a darker spray tan can tremendously increase your definition. Definition on camera is all about contrast. If you're just super pale and pasty and white, then there's not going to be that much contrast. Even if you're muscular, you're not going to look that defined. Take that same physique and put a spray tan on it and you'll look much more defined.",
 "C": "The most important pro of spray tanning, in my opinion, is that it enables you to get tan while avoiding sun damage. And the sun is a lot more damaging than people think. | For those of you guys who don't believe this, go and watch some of Bryan Johnson's videos on this topic. If you ever notice why the world's healthiest man looks like an ultra pale vampire, this is the reason why. He's trying to avoid cancer, he's trying to avoid skin damage, and that's the reason why he only goes out in the sun during off-peak hours, not in the bright sun in the noontime, and why he | takes an umbrella out with him when he goes out in the sun. Sun exposure is one of the most common causes of cancer. Skin cancer is one of the most common cancers and if you go out in the sun a lot getting that healthy looking tan, you're a lot more likely to get that kind of cancer.",
}
