"""SL-18: two Shorts from RO-25 "I'm 41. I Wasted My Life." as data. Film seconds are on the APPROVED RO-25 R7 master
(11:51.144, sha 6045ac0e, Dan finalized 2026-10-17). Dan's picks 2026-10-20: B (Adderall) with a decisive opening line ("If I say
'Stop taking Adderall' that would be the best starting line"), D (dating) opening on "If you're in your 20s, stop chasing women",
first story sentence cut, more depth at the end on why to build your value before dating.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the master's own mix (snap.py, 10 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq + ai (chip xy, u) + speed)
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken, ` | ` at each audio piece join; `shown{spoken}` where the aligner needs the spoken form"""
STOCK = "/Volumes/Expansion/_edit_work/SL-18/clips/"          # copies; never read from another session's build folder at render time
DISC = {}
MASTER_CUTS = [36.103, 38.071, 52.986]      # the master's internal picture cuts (scene detection, 2026-10-20) not already in the edit map
Y0 = {"full": 0, "mid": 0}                  # measured per shot after `track` (SHOTS y0 overrides); the full window keeps all the master's headroom
KEEP = 0.90
TRIM = {}
SEG = {
 # B: "If" from 149.42 after the dip to -35 dB at 149.40 that ends the dropped "So"; "wait." ends 157.16 (silence 157.22).
 # "I" 33.68 (silence 33.55-33.61); "productivity." decays by 52.70, breath to 52.87, silence from 52.88. "When" 67.94 (silence 67.58-68.04);
 # "quit." ends 102.60 (silence 102.63; the film's picture join at 102.903 is after the out point).
 "B": [[149.475, 157.48], [33.58, 52.88], [67.60, 102.80]],      # R1g (reviewers R1f, check): the film says "So if" as one run; no start gives a clean "If" (from 149.32 the first 50 ms is the vowel of "So"; "if" is a fragment 10-20 dB down at 149.42-149.47). The Short opens on "you're" (149.48), captioned as the challenge it now is: "You're on Adderall or any ADHD drug? Quit today." Dan's own suggested opener ("Stop taking Adderall") needs a studio pickup: offered on the review page
 # D: "If" 370.64 (silence 370.25-370.83); "today." ends 381.70 (silence 381.73). "What" in silence 348.02-348.12; "instead." ends 370.22
 # (silence 370.25). "The" in silence 381.83-382.29; "today." ends 410.58 (silence 410.63-410.83).
 "D": [[370.30, 381.73], [347.66, 370.29], [381.84, 410.82]],      # R1e: no overlapping film ranges (P2 to 370.55 re-used the hook's own lead-in 370.30-370.55); the pause before "The reality" comes from P3 starting in the silence 381.83-382.29 instead (0.52 s in all); P3 runs to 410.82 so "today." lands (reviewer R1d)      # R1b (reviewer): P2 from 347.66 (silence 347.62-347.76) keeps his breath before "What"; P2 to 370.55 inside the silence before the hook's "If" (370.64): the two joins had 0.12 and 0.17 s, his pauses run 0.4-0.6 s
}
PICKUP = {}
# R1b (reviewer D): the film's own false-start cut at film 386.786 removed the end of "rich" (about 120 ms of the "ch"; every Whisper run
# heard "ripped and ripped"). The film's processed full-roll mix (RO-25 round7 audio/baseline/full-Bass-2.wav, on the round-1 cut-map clock,
# film = original - 18.755 before the join, r 0.9998) still has it at original 405.541-405.695: it replaces the room tone of the next take
# for those 154 ms (film 386.786-386.940, silence before "And" at 386.96), 5 ms in, 20 ms crossfade back. patch_audio.py applies it to
# audio.wav AND his_mix.wav (the audio gate's verbatim reference), so the gate still proves the rest is the film's mix untouched.
PATCH = {"D0": [], "B": [dict(film=78.800, duck=0.040, gain=0.2, fade=0.005),      # R1f (reviewer): a 30 ms mouth click before "So you take more" (-31 dB from -60, the largest sample step in the file; the approved film has it too), softened 14 dB
       dict(film=52.70, src="master_audio.wav", src_t=52.88, dur=0.18, fin=0.05, fout=0.04)],      # R1d (reviewer): the fade went to digital zero for 121 ms; now the exhale crossfades into the film's own room tone (52.88-53.06)      # R1c: after "productivity." the film carries a soft voiced exhale (52.70-52.86, -25 to -33 dB) that leads into the next sentence in the film; alone before the graph cut the delivered transcript heard it as a word ("activity"): faded out over 60 ms, then room level
         "D": [dict(film=374.564, mute=0.010, fade=0.010), dict(film=374.574, fadein=0.008),      # R1f (reviewer): the incoming take also starts with a one-sample step: ramp it in over 8 ms
       dict(film=355.150, mute=0.072, fade=0.060), dict(film=355.222, fadein=0.006),      # R1g (reviewer): "value," is still voiced (-20 dB) when the film's cut stops it at 355.21: a 60 ms decay from 355.15 instead of a 6 ms one at the join      # R1f (reviewer): the film's join at 355.222 (in the pause after "value,", not in its edit map) repeats 14 ms and steps; fade out and in over 6 ms (the approved film has the click)
            # R1e (reviewer): the tail of "value." stops in one sample step at the film's own join 374.574 (the approved film has it too): a 10 ms fade-out into the join
       dict(film=386.786, src="full-Bass-2.wav", src_t=405.541, dur=0.154, fin=0.005, fout=0.020)]}
WORDFIX = {"B": [], "D": [("at", 25.7, 25.50, 25.58)]}      # CTC loses the first word at the file head (score 0): "If" is 149.42-149.48 on the 10 ms levels after the dropped "So"
NAME = {"B": "short1_why-adhd-meds-backfire-long-term", "D": "short2_build-your-value-before-you-date"}
TITLE = {"B": ("ADHD MEDICATION", ["Why ADHD Meds", "Backfire Long Term"]),
         "D": ("DATING IN YOUR 20S", ["Build Your Value", "Before You Date"])}
BRIGHT = "eq=gamma=1.2:saturation=1.05"      # Dan's overcast pool rolls (curls B0031): SL-07's approved lift (skin 77 against the presenter's 94)
GRAPH = "/Volumes/Expansion/_edit_work/SL-18/graph/proj/B_graph.mov"
COVERS = {
 "B": [dict(id="desk", a=33.58, b=38.21, src=STOCK + "DESK.mp4", t=0.0, fx=0.73, ai=(40, 336, 1.6)),        # the film's approved P01 AI clip (1-DESK r6 take6), frames 0-111: one pill, then water. Frame-reviewer R1 FAIL on 0-140: the glass comes back as full as it started after a long drink (back in view from frame 112), so the clip ends at 111 and Dan is on camera from 38.21 ("early 30s."). Covers the master's cut at 36.10 and 38.07
       dict(id="graph", a=67.60, b=89.16, src=GRAPH, t=0.45, fx=0.5, fy=0.0),      # t 0.45: the graph scene starts 0.45 s before the cut (config a 67.15), so its header is already drawing on the first frame (reviewer R1: 8 blank frames)
       dict(id="graph_z", a=89.16, b=94.32, src=GRAPH, t=0.45 + 21.56, zoom=1.4, fx=0.98, fy=0.72),      # R1g (gate style:static_run: 35.2 s with no picture change, max 30): a 1.4x zoom CUT onto the zigzag on "This cycle just keeps going until you need Adderall just to function..."; segments 5-8 draw inside it
       dict(id="graph_b", a=94.32, b=102.80, src=GRAPH, t=0.45 + 26.72, fx=0.5, fy=0.0)],      # cut back to the whole graph on "Eventually"
 "D": [dict(id="curls", a=374.574, b=376.10, src=STOCK + "B0031.mp4", t=0.0, fx=0.5, eq=BRIGHT),             # "Build your body,": Dan's real curls from his first rep (SL-07); starts ON the film's false-start join 374.574, hiding it
       dict(id="money", a=376.10, b=376.70, src=STOCK + "B0213.mp4", t=0.5, fx=0.08),                       # "your money,": hands counting dollars (Pexels, used in RO-19 SL-15); ends before "and your skills." (reviewer R1d: skills over money stock), Dan on camera for that
       dict(id="pool", a=377.70, b=381.73, src=STOCK + "A0061.mp4", t=28 / 24, fit="span", span=(0.24, 0.81), pre="crop=iw:ih-6:0:3", ai=(632, 336, 1.6)),     # "The women will come later, and they'll be far better": A0061 frames 28-124 (frame-reviewer R1: from 124 the heads drop and smear); a card: the two heads are 785-860 px apart (R2); span 0.24-0.81 holds both (R3 PASS). pre: the source's 3 black rows off
       dict(id="app2", a=353.02, b=355.42, src=STOCK + "A0089.mp4", t=179 / 29.97, speed=0.83, fit="tall", ar=962 / 1880, pre="crop=962:1880:60:21", round=58, ai=(377, 322, 1.6)),   # R1e: the dating-app mock (frames 179-238, a static UI screen at 0.83x, then its own tap ring on the Matches tab at 232-238) lands the lean profile on "got in a better shape, and built my own value,". No push-in (reviewer R1d: it lost the side bezel); "No new matches" dropped (it said the opposite of "once I'd made more money"). Cropped 6 px inside the bezel, corners rounded to the phone's own radius (R1d: white crescents)
       dict(id="app3", a=355.42, b=358.24, src=STOCK + "A0089.mp4", t=239 / 29.97, speed=0.92, fit="tall", ar=962 / 1880, pre="crop=962:1880:60:21", round=58, ai=(377, 322, 1.6)),   # the full Matches list (frames 239-317, 0.92x) on "I'd be able to attract far higher quality women."
       dict(id="date", a=358.24, b=361.71, src=STOCK + "DATEA.mp4", t=0.0, fit="whole", y=460, ai=(40, 336, 1.6)),     # R2 (Dan, 2026-10-22: "this clip doesn't really make sense split screen... use it horizontally"): the film's DATE-A whole 16:9 card (both people need the full width), y 460-1068, clear of the captions; ends in the dip after "relationships"
       dict(id="squats", a=367.70, b=370.29, src=STOCK + "B0464.mp4", t=0.0, fx=0.45, eq=BRIGHT),      # R1e: "I would have put that time into building myself instead.": Dan's real bodyweight squats on the lawn (B0464, slow orbit); breaks up 30 s of talking head (reviewer R1d)
       dict(id="abwheel", a=403.46, b=407.70, src=STOCK + "B0030.mp4", t=0.9, speed=1.25, fit="span", span=(0.13, 0.88))],   # "If you stay on point with your workouts, nutrition, and your work over the next 10 years,": SL-07's approved ab wheel card; ends in the gap before "you'll". A0085 meal prep was dropped (its source cuts the man's hair and dissolves into a second take at frame 63)
}
SPLIT = {"B": [["I'm not a doctor", 0.0]],      # no step under the B key point (40.8-50.9): a bar sits on one steady full window          # size steps inside one continuous take, in the pause before each phrase
         "D": [["If I had known", 0.0], ["But it's tough", 0.0]]}      # R1b: no step at "But take it": the key point sits on that one full window
SHOTS = {"B": {}, "D": {3: dict(win="mid", y0=0), 5: dict(win="mid", y0=0), 10: dict(y0=24), 12: dict(win="mid", y0=0), 13: dict(win="mid", y0=22)}}      # R1e indices. WIDE master shots (#3, #5, #12: face 218-220 px) take the mid window and CLOSE ones (face 284-296) the full window, so his face is a similar size in every shot (reviewer R1c: one shot much wider); #10 and #13 are close shots in the mid window for a real size step (1.2x and 1.32x). y0 = measured hair top minus 46 px, floor 0
BARS = {
 "B": [dict(id="G1", topic="KEY POINT", parts=[["A Short-Term Boost", "turned me into"], ["Long-Term Damage", "But in the long term"]], a=-0.2, b=4.6)],      # R1d (reviewer): line 2 lands on "But in the long term" and holds about 4.5 s (it was readable 1.27 s); eyebrows in capitals (Dan 2026-10-20, GRAPHICS-STANDARDS)
 "D": [dict(id="G1", topic="KEY POINT", parts=[["Every Year You Build,", "build your value so"], ["Your Options Get Better", "get better women later"]], a=-0.2, b=2.1)],      # R1d (reviewer): distill, not echo (R1b repeated the title, R1c repeated his words)
}
TEXT = {
 "B": "You're on Adderall or any ADHD{a d h d} drug? Quit today. I'm not a doctor, so talk to yours about the safest way to come off it. But don't wait. | "
      "I took Vyvanse{vivance}, Adderall, and Adderall XR{ex ar} for about 5{five} years in my late 20s{twenties} and early 30s{thirties}. When I first took it, I thought it turned me into Superman. "
      "I was more productive than I'd ever been. I made more money than I ever had made before. But in the long term, it had a huge, permanent, negative impact on my health and my productivity. | "
      "When you take Adderall, you get more productive for a few hours. But there's a downside. You don't sleep as well that night and you don't get proper nutrition, so you're less productive the next day. "
      "So you take more Adderall and you're more productive than normal again. Just not as productive as the first time. With more long-term use, your sleep and nutrition take an even bigger hit. "
      "This cycle just keeps going until you need Adderall just to function the way you used to without it. Eventually, even on a high dose, you're not as productive as you were before you ever took it. "
      "In the end, the long-term effects get so bad that you have to quit.",
 "D": "If you're in your 20s{twenties}, stop chasing women and build your value. Build your body, your money, and your skills. The women will come later, and they'll be far better than the ones you'd settle for today. | "
      "What I didn't realize is that once I got into my late 30s{thirties} and 40s{forties}, once I'd made more money, got in a better shape, and built my own value, I'd be able to attract far higher quality women. "
      "So I spent a huge amount of time on dating apps and relationships at the exact moment that my value was at its lowest. If I had known the women I could attract once my value was higher, I would have put that time into building myself instead. | "
      "The reality is that dating is always going to be a struggle for you until you're ripped and rich. And there simply isn't any magic technique that you can use to make women attracted to you despite being overweight and broke. "
      "But it's tough to sacrifice the woman you could have now because you might not believe you'll be able to build your value so you can get better women later. But take it from an older man. You will. "
      "If you stay on point with your workouts, nutrition, and your work over the next 10{ten} years, you'll be able to attract far better women than you can today.",
}
