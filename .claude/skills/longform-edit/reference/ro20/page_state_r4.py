"""RO-20 round 4: the review page's content (what is new in each film, by timestamp on the delivered film) -> round4/page_state.json.
Times come from each video's layout.json (film time -> video time), never typed by hand."""
import json, sys, os
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001
def lay(v): return json.load(open(f"{W}/round4/{v}/layout.json"))
def fmap(v, t):
    f = t*FPS
    for P in lay(v)["parts"]:
        p = P["part"]
        if p[0] == "film" and p[1] <= f < p[2]: return (f - p[1] + P["out"][0])/FPS
    raise SystemExit(f"{v}: film {t} not in the video")
def pk(v, pid): return next(P["out"][0]/FPS for P in lay(v)["parts"] if P["part"][0] == "pickup" and P["part"][1] == pid)
def part_at(v, i): return lay(v)["parts"][i]["out"][0]/FPS
def mm(t): return f"{int(t//60)}:{t % 60:04.1f}"
def rng(a, b): return f"{mm(max(0, a))} to {mm(b)}"
def row(at, what, a=None, b=None): return dict(at=mm(at), what=what, watch=rng(at - 4 if a is None else a, at + 6 if b is None else b))
def length(v): return mm(lay(v)["frames"]/FPS)
R = {i["id"]: i for i in json.load(open(f"{W}/plan_resolved.json"))}
V1 = [
 row(fmap("v1", 122.42), "AI poolside clip: its AI label moved to the top left (it sat on the passing man's face)."),
 row(fmap("v1", 142.72), "Stomach-vacuum pose clip removed (a still hands-on-hips hold with a light stand in frame); you stay on camera."),
 row(fmap("v1", 345.111), "Wide shot from here to 5:52.6: the camera's own recording skips a frame at 5:45.1, and the zoom cut hides it."),
 row(fmap("v1", 469.98), "Stock shot of the man on the couch brightened and slightly warmed (it read dark and very blue)."),
 row(part_at("v1", 1), "0.37 s of the pause after \"...too.\" trimmed (you looked down at your hands before the cut)."),
 row(part_at("v1", 2), "The split: \"And I'll go more into that in a minute.\" is out (it pointed at video 2)."),
 row(fmap("v1", R["Cc04"]["t0"] + (R["Cc04"]["t1"] - R["Cc04"]["t0"])/2), "Heart-monitor stock colour corrected like everywhere else it appears."),
 row(fmap("v1", 639.04), "Brain-scan tablet stock brightened."),
 row(fmap("v1", 887.99), "Clip of you standing by the pool holding the ab roller removed (the library rejected it on 10-16 as a standing shot); you stay on camera. This is inside the ending you approved in round 3b."),
 row(pk("v1", "P1"), "Pickup P1 (studio lav, treatment A). It now plays at the same level as your kitchen voice; the round 3b clip played it about 3 dB quieter because of how that clip was joined."),
 row(part_at("v1", 4), "Your on-camera sign-off; the sentence ends on \"filled with motivation.\" at " + mm(part_at("v1", 4) + 27.86) + ".", None, part_at("v1", 4) + 32),
]
V2 = [
 row(0.0, "Opens on camera: \"You need to be spending more money on your health...\" (as approved).", 0, 14),
 row(pk("v2", "P2"), "Pickup P2. Same level change as video 1's pickup (now level with your kitchen voice)."),
 row(fmap("v2", 932.315), "Handstand push-up clip removed: the \"Cut The Waste, Fund Your Fitness\" key point covered your head at the bottom of every rep. This was in the first minute you approved; say \"put it back\" if you prefer it."),
 row(fmap("v2", 1111.71), "Beer-can stock removed (near black even after a lift); you stay on camera."),
 row(fmap("v2", R["Cd11"]["t0"]), "Smoking-pan stock brightened."),
 row(fmap("v2", 1302.84), "Front-pose clip by the pool removed (your 10-14 rule names it); the next take starts wide so there is no jump."),
 row(fmap("v2", 1356.56), "Side-pose clip removed (also named in the 10-14 rule); you stay on camera under the key point."),
 row(fmap("v2", R["Cd28"]["t0"]), "Couple-on-the-sofa stock brightened and warmed (it read dim and blue)."),
 row(pk("v2", "P3"), "Pickup P3 and the ending screens, as approved; silent room at the end for YouTube's end screen.", None, lay("v2")["frames"]/FPS),
]
V3 = [
 row(0.0, "Pickup P4 opens the video (level now matches your kitchen voice).", 0, 22),
 row(part_at("v3", 1), "New: 0.3 s of the roll before \"All right.\" so the first word is no longer clipped."),
 row(fmap("v3", 43041/FPS), "Squat clip now ends before your head leaves the top of the frame; you are on camera for the rest of the sentence."),
 row(fmap("v3", 46910/FPS), "The \"Two Buys\" lower third now enters after the push-up clip (it covered your face at the bottom of the rep)."),
 row(part_at("v3", 3), "0.6 s of silent pause trimmed after \"...my life depends on it.\" (you looked down before the cut)."),
 row(fmap("v3", 43714/FPS), "Curl clip now ends before you stand still with your eyes shut at the end of the set."),
 row(fmap("v3", 1614.5), "Dark stock lifted here and at about the bedroom (5:57), gyms (8:56, 9:58), dumbbell racks (9:37, 10:16), vitamin D bottle (17:33) and trainer (24:15) shots."),
 row(fmap("v3", 57782/FPS), "Bed B-roll now starts on \"So,\" so your turn to the side in that pause is covered; the black-and-white bedroom clip (about 8:01) is out and you are on camera."),
 row(fmap("v3", 59363/FPS), "Dumbbell-rack clip holds 3 frames longer over an off-centre take start."),
 row(fmap("v3", 1977.52), "AI clip: only the leg-press shot is kept. The leg-curl shot had a pad floating with no machine arm; you are on camera for \"a leg curl machine\"."),
 row(fmap("v3", R["Ge32"]["t0"]) + 2.15, "Lower third: the empty lead before its main line is shortened (also at about 15:05, 18:38 and 18:54)."),
 row(part_at("v3", 4), "0.4 s of silent pause trimmed after \"...at all times.\" (eyes dropped to the floor)."),
 row(fmap("v3", 2419.78), "Medicine-ball V-up clip removed: the key point covered your abs; you stay on camera."),
 row(fmap("v3", 2628.23), "Wide-to-tight zoom cut over a frame skip in the camera's own recording."),
 row(fmap("v3", 76180/FPS), "AI home-gym clip now ends before its dumbbells briefly double."),
 row(part_at("v3", 5), "A silent look-down before a zoom cut trimmed (0.33 s) after \"...real baller.\""),
 row(fmap("v3", 90001/FPS), "Zoom cut moved 0.7 s later so it no longer lands in the middle of a head turn."),
 row(lay("v3")["frames"]/FPS - 0.6, "New: 0.6 s of your held smile after the last word, so the film does not end on the word.", lay("v3")["frames"]/FPS - 8, lay("v3")["frames"]/FPS),
]
S = dict(videos=[
  dict(n=1, title="Why You Should Invest More In Your Health", length=length("v1"), review="r4/video 1 - REVIEW 540p.mp4", vlc="Invest In Your Health LFC R4 - video 1 full film.mp4", changes=V1),
  dict(n=2, title="What To Cut To Afford Getting In Shape", length=length("v2"), review="r4/video 2 - REVIEW 540p.mp4", vlc="Invest In Your Health LFC R4 - video 2 full film.mp4", changes=V2),
  dict(n=3, title="What To Buy For Your Health At Every Income Level", length=length("v3"), review="r4/video 3 - REVIEW 540p.mp4", vlc="Invest In Your Health LFC R4 - video 3 full film.mp4", changes=V3)])
json.dump(S, open(f"{W}/round4/page_state.base.json", "w"), indent=1)
for v in S["videos"]:
    print(v["n"], v["length"]); [print("  ", c["at"], c["what"][:90]) for c in v["changes"]]
