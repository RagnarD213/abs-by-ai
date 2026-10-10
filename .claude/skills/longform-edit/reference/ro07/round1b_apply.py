"""RO-07 round 1b: apply Dan's 2026-10-09 notes to plan.py and record them word for word in round2-plan/decisions.json."""
import json
W = "/Volumes/Extreme/_edit_work/ro07"
s = open(f"{W}/recipe/plan.py").read()
if 'B0448@4.0", "B0456' not in s:
    a = s.index(' dict(id="C01", kind="clip"'); b = s.index(' dict(id="G01", kind="lt"')
    s = s[:a] + ''' dict(id="C01", kind="clip", start="Today I'm going to show you why", end="In today's video I'm going to show you why", tail=0.1, src=["B0448@4.0", "B0456@1.0", "B0453@0.3"], **DAN,
      note="OPENER, round 1b (Dan: better clips where he looks ripped): his fast correct jump rope, handstand push-ups, decline push-ups on the handles. Real footage, his voice runs underneath. Kettlebell deadlifts have no horizontal cut in the library yet"),
''' + s[b:]
    a = 'dict(id="G01", kind="lt", start="In today\'s video", end="twice per week"'
    assert a in s; s = s.replace(a, 'dict(id="G01", kind="lt", start="5 minute workout done every day", end="twice per week"')
    a = s.index(' dict(id="A1", kind="clip"'); b = s.index(' dict(id="G02", kind="lt"'); s = s[:a] + s[b:]
    a = s.index('note="NEW AI CLIP (frames for approval): a man heads for his front door'); b = s.index('"),', a)
    s = s[:a] + 'note="NEW AI CLIP, round 1b END frame (Dan: the glove comes from outside, much larger, and knocks him down): he opens the front door and a giant cartoon boxing glove on a spring shoots in from outside at the right edge and knocks him flat' + s[b:]
    open(f"{W}/recipe/plan.py", "w").write(s)
Q = '"'
D = dict(job="RO-07", round_shown="round 1 (2026-10-09, page localhost:8857)", recorded="2026-10-09", items=[
 dict(id="look-colour", path="grades.json option C (first minute)", verdict="rejected",
      words="This color looks awful. How do I see the color options in the video? Which one is in the first minute?",
      scope="colour of the first minute (option C)", next="moving comparison of C, B and two new brighter options D, E on round 1b; Dan picks"),
 dict(id="audio", path="round1/first-minute/DRAFT - RO-07 round 1 - first minute.mp4", sha256_16="59ff56f27d4bfe3f", verdict="rejected",
      words="Also, the audio sounds really bad. Give me a few audio options to fix this in the next round.",
      scope="voice sound of the first minute (fitted EQ + expander)", next="four level-matched auditions on round 1b; the pick becomes a voice_chain flag"),
 dict(id="C01", verdict="approved-with-notes",
      words="I like the idea of using workout clips in the beginning, but I don't like the ones you use. The pushup one is kind of weird. It's on my back, and the lighting isn't the best. The same thing with the tower row: the lighting isn't the best. I want you to use the jump rope clip, the one where I'm doing the correct reps, skipping over the rope quickly, not the one where I'm skipping slowly, and not the ones where I'm jumping over 2 ft. I want you to choose some exercise clips where I'm looking ripped and better, like: the handstand pushup clip, the decline pushup clip, kettlebell deadlifts. Give me some better clips in the beginning.",
      scope="opener concept approved; clips replaced", next="rebuilt with B0448, B0456, B0453; shown on round 1b"),
 dict(id="A1", verdict="rejected", words="Eliminate clip A1. I don't feel like that gets across the idea or adds any value.",
      scope="clip removed from the film", next="removed from plan.py; no motion, no spend"),
 dict(id="G02", verdict="approved-with-notes",
      words=f"In the graphic at 41 seconds, there's no space between the question mark and {Q}no{Q}. Add in the space between the question mark and {Q}no{Q}.",
      scope="spacing only", next="lower-third template fixed for every multi-part lower third (PART_GAP, commit b49eca7); G02 re-rendered"),
 dict(id="A2", path="aiframes/A2-start.png, aiframes/A2-end.png", sha256_16=["745e2c402911844d", "be605c2bac335679"], verdict="approved",
      words="Start n frames for A2 are approved. That's looking good.", scope="start and end frames", next="generate motion (one Veo 3.1 Fast take)"),
 dict(id="A3", path="aiframes/A3-start.png", sha256_16="39e6fa6a07794e3f", verdict="approved-with-notes",
      words=f"I don't like A3: {Q}Life punches you in the face.{Q} I feel like that's a little weird for the coming out of the gym bag. I want to change A3 to 2. He's walking out. The start frame looks good, but change the end frame to where he walks out the door rather than the boxing glove coming out of his gym bag. A giant cartoon boxing glove comes from outside on that spring and then punches him in the face and then knocks him down. The glove is larger. It comes from outside rather than the gym bag at the right edge of the frame, and it's much larger than the current glove. It knocks him down. Looks cartoonish and funny",
      scope="START frame approved; END frame rejected and redescribed", next="new END frame for approval; no motion until it is approved"),
], motion_authorized=["A2"], new_frames_before_motion=["A3 (new END frame)"], removed=["A1"])
json.dump(D, open(f"{W}/round2-plan/decisions.json", "w"), indent=1); print("plan updated; decisions recorded:", len(D["items"]))
