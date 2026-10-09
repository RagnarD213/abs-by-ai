"""Round 6 review page text (the editor's words; page6.py lays it out). REVIEW / GATE are filled from the logs after they ran. usage: page_text6.py"""
import json, os
O = "/Volumes/Extreme/_edit_work/ro06/round6"
X = json.load(open(f"{O}/logs/page_facts.json"))     # written by hand from the logs once the checks and the review are in
CHANGED = [
 "3:51, the jump rope clip. It is now you skipping fast, foot to foot, the way you asked. It is a different 3.8 seconds of the same fast stretch the opening uses, so no moment of the film is shown twice.",
 "9:24, the framing. The whole take is now cropped a little wider and higher, with clear space above your hair (at least 52 pixels on every frame). That covers 9:23 to 9:32 and the same take when it comes back at 9:40 to 9:47.",
 "9:32, one cutaway moved. The toe-touch clip now starts 1.9 seconds earlier, on 'because it's a little bit more ergonomic'. Right after that you throw both arms overhead and your hands go above what the camera recorded, so no crop could keep them in.",
 "11:23, the microphone. The 3.6 blown-out seconds are repaired and now sit level with the sentences either side. Every other sample of your voice is identical to the last round.",
 "15:44, the phone clip is gone. You are on camera, moved to the right, with the app in a phone on the left: the home screen, a tap, a meal photo turning into 775 calories, a tap, then two exercise videos.",
 "Lower thirds, two things from today. The fix for words sitting too close together ('RecommendIs') is in, on every lower third. And your new capitals rule is applied: 25 lower thirds went back to normal capitalization; five keep one capital word.",
]
DECIDED = [
 "Jump rope: I took roll C1674 from 101.8 seconds, graded exactly like the library clip. The opening uses 99.1 to 101.5 of the same roll. About 156 steps a minute.",
 "9:24, where the extra space comes from: the camera was aimed higher for the first second of that take, so the trees and roof above your head were on record. I made a still of that and laid it above the live picture. Nothing was generated. No Codex image was needed.",
 "9:24, one honest limit: once the operator tilted down, the top edge of the camera sat on your hair and cut a few pixels off the top of it. That sliver was never recorded. I tried twice to put it back from an earlier frame and both left a faint ghost above your hair, so I left it out. If you look very closely from 9:28, the very top of your hair is slightly flat. At normal size I do not think it reads.",
 "9:24, the size: 1.2x (it was 1.3x, then a cut to the full frame at 9:30). It is now one size for the whole take, so the cut at 9:30 is gone.",
 "11:23: that roll has no second microphone to borrow from (its other channel is silent). I rebuilt the clipped peaks, then lowered your voice for those seconds only, leaving the background noise level so nothing dips. An unprompted listen by Gemini heard a problem in the old clip and called the new one clean. Please listen once yourself: the before and after are below.",
 "15:44, the timing: the phone is up for the whole sentence, 15:43.8 to 15:53.8 (10 seconds), because a home screen, two taps, a meal analysis and two exercise videos do not fit in the 4.6 seconds the old clip had.",
 "15:44, the screens: the home screen is the real app, captured at phone size from a local copy with a test account. I hid three things a test account shows and a member would not: the sign-in line, an empty 'Today's brief' card and the 'Become a member' tile. The meal analysis is your real recording (the salmon plate). The exercise sheets are the app's own Push-Up and Reverse Lunge, with the app's own demo videos and its AI-GENERATED label.",
 "15:44, your position: you are moved 290 pixels right in one fixed position, never animated. It is tight: your hand comes within about 10 pixels of the right edge at 15:52. When the phone leaves you are back in the middle for 1.7 seconds before the upload demo.",
 "15:44, what I left out: the workout list step between the tap and the exercise sheet. There was no time for it and the list we have on record shows a different exercise.",
 "Capitals: I kept a capital word on five lower thirds where the word is the whole point: 'NO Difference' (2:15), 'Much LOWER Risk' (7:07), 'Too HEAVY' (8:44), 'For EVERYTHING' (12:44) and 'Then UPGRADE To A Gym' (13:41). Item names (Yoga Mat, Jump Rope, Dumbbells and the rest) are normal now. 'No COMMUTE.' at 0:55 is inside the first minute you approved, so I did not touch it; say the word and it goes to 'No Commute.'",
 "Four lower thirds that I had flattened to one line last round, to hide the word-gap fault, build in two parts again on your words: 1:19, 6:21, 9:42 and 10:46.",
 "Nothing was generated or bought this round. AI clip spend for this video stays at $2.43 of $5.",
]
ITEMS = [
 dict(id="R1", n="1", when="3:49.6 to 3:53.4", t0=229.6, said="I want to change this to the clip of me doing jump rope correctly, the clip where I'm quickly skipping over the rope with correct form.",
      what="Swapped the both-feet clip for the fast skip. The both-feet clip is now marked in the clip library as a mistake demo only, as you ruled.",
      stills=[("old", 231.0, "before: both feet"), ("new", 230.3, "now: the fast skip"), ("new", 232.6, "now, two seconds later")]),
 dict(id="R2", n="2", when="9:23.2 to 9:32.2, and 9:40.2 to 9:47.1", t0=563.2, said="I want to crop a little wider and higher so that my hair, when I raise my arms a few seconds after that, doesn't go out of frame.",
      what="One wider, higher crop for the whole take, with real background above your head from the first second of the same take. The toe-touch cutaway covers the moment both arms go overhead.",
      stills=[("old", 566.0, "before"), ("new", 566.0, "now"), ("old", 571.6, "before"), ("new", 571.6, "now"), ("old", 583.5, "before, after the cutaway"), ("new", 583.5, "now, after the cutaway")]),
 dict(id="R3", n="3", when="11:22.1 to 11:25.8", t0=681.0, said="The mic is blown out when I turn my head down to illustrate the overhead tricep press. I want you to try to fix that audio so that it sounds as normal as possible.",
      what=f"Clipped peaks rebuilt and the level brought down to match. Measured in the finished mix: those seconds were {X['mic_before']} dB against {X['mic_neighbours']} either side; they are now {X['mic_after']}. Play both.",
      stills=[], videos=[("mic_before.mp4", "before (round 5), 9 seconds"), ("mic_after.mp4", "now, the same 9 seconds")]),
 dict(id="R4", n="4", when="15:43.8 to 15:53.8", t0=943.8, said="I don't like that. It's just me looking at my phone. I want to replace this with the camera scene with a graphic of the Abs By AI home screen next to me, and then click into it, seeing the calorie tracking functionality, seeing some of the AI-generated workout videos.",
      what="You on camera with the phone on the left third. Home screen, tap on Macro Tracker, the meal photo and its calories, tap on AI Trainer, the Push-Up video, the Reverse Lunge video.",
      stills=[("old", 951.5, "before: the phone clip"), ("new", 944.8, "home screen"), ("new", 945.55, "the tap"), ("new", 948.3, "calories from the photo"), ("new", 949.65, "the second tap"), ("new", 950.9, "Push-Up video"), ("new", 953.0, "Reverse Lunge video")]),
]
UNSPOKEN = [
 "Voice tone: A, as you approved it. (The automatic audio check still fails its tone row with it; B is the same sound with the treble trimmed 4 dB.)",
 "Music bed: as is.",
 "Hair at the top edge in other shots: as shot. It touches the top at 6:26, 13:44 to 13:51, 14:15, 15:31 to 15:34, 15:52 and 16:21 to 16:28. The fix used at 9:24 only works where the camera recorded the space above your head earlier in the same take.",
 "Hands above the top of the picture at 8:59, 11:25 and 11:48: as shot (the camera's edge).",
 "The two app demos after this one (upload demo at 15:55, the workout plan demo at 16:13): as built.",
 "Cutaways C16 to C18, C23 to C27 and C30: kept.",
 "The leg press, leg curl and deadlift AI clips you liked: exactly as placed.",
]
CHECKS = X["checks"]; OPEN = X["open"]
REPLY = ("RO-06 round 6, the full film\nApproved as is, or changes (time and what):\n1. Jump rope at 3:51:\n2. Framing at 9:24 (and 9:40):\n3. Mic at 11:23 (fine / still hear it / cut the sentence):\n4. Phone beside me at 15:44:\n"
         "Capitals on lower thirds (fine / change which):\n'No COMMUTE.' at 0:55 in the approved first minute: leave\nVoice tone: A (as approved)\nMusic bed: keep\nHair at the top edge elsewhere: leave as shot\nAnything else:\n")
json.dump(dict(CHANGED=CHANGED, DECIDED=DECIDED, ITEMS=ITEMS, UNSPOKEN=UNSPOKEN, CHECKS=CHECKS, OPEN=OPEN, REPLY=REPLY), open(f"{O}/page_text.json", "w"), indent=1)
txt = json.dumps([CHANGED, DECIDED, ITEMS, UNSPOKEN, CHECKS, OPEN, REPLY]); print("written; em or en dashes:", txt.count("\\u2014") + txt.count("\\u2013"))
