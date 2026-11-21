"""RO-02 visual plan, round 2. Every item is anchored to the words Dan says (phrase -> output time via words_out.json).
HyperFrames templates (hyperframes/from_plan.py): lt (Motivation lower third), scene/fact (fact card), l3 (3A side list).
gfx.py (Soft Blue Light, PIL): opener (two AI panels + red X), title (PART n OF 6), scene/recap, anat (two-muscle diagram
in the 3A card), count (20-second hold countdown), url (AbsByAI.com chip). clip = full-frame cutaway, hard cuts."""
DEMO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.mp4"
V4 = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/YouTube Long Form Video Content/V4 + V5 - The Ultimate 1 Minute Ab Workout - UPLOADED/V4 - 1 Minute Ab Workout That Hits All 4 Ab Muscle Groups (At Home) - UPLOADED.mp4"
PH = "/Volumes/Extreme/_edit_work/ro02/assets"
KP = "KEY POINT"
PLAN = [
 # ---------------- hook
 dict(id="O01", kind="opener", start="If you have belly fat", end="stop doing all", end_at_start=True,
      title=["Stop Doing Ab Exercises", "If You Have Belly Fat"], labels=dict(A="CRUNCHES", B="SIT-UPS"),
      x_ph=dict(A="Stop doing crunches", B="stop doing sit ups"),
      note="Dan's opener: Soft Blue Light graphic, two AI clips (A crunches, B sit-ups), a red X on each as he says it. Ends on the cut to him at 'stop doing all those ab exercises'."),
 dict(id="G01", kind="lt", start="Gaining muscle on your abs", end="bulge out more", topic=KP,
      point="Ab Exercises Build Muscle UNDER The Fat.", parts=[["Ab Exercises Build Muscle", "Gaining muscle"], ["UNDER The Fat.", "putting muscle onto"]]),
 dict(id="C01", kind="clip", start="the vacuum, the only ab exercise", end="shrink your waist", tail=0.3, src=["/Volumes/Extreme/_edit_work/ro02/assets/vacuum_teaser.mp4@0.5"],
      note="four seconds of this film's own live set (C1625, same colour and framing as the set at 8:52). The library clip B0428 is in shade and read dark beside this film."),
 # ---------------- why ab exercises do not burn belly fat
 dict(id="T1", kind="title", start="So let's talk about why", dur=2.4, step=1, headline="Why Ab Exercises\nDo Not Burn Belly Fat"),
 dict(id="C02", kind="clip", start="they want an ab workout", end="from their stomach", tail=0.25, src=[V4 + "@1.0"],
      note="his own toe-touch crunches, from the finished 1 Minute Ab Workout export (0:01)"),
 dict(id="G02", kind="scene", scene="fact", start="The way that it works", end="specifically from your abs", photo=f"{PH}/crunch.jpg",
      label="Real picture of me. Not AI-generated.",
      eyebrow=["YOU BURN FAT", "The way that it works"], headline=[["EVENLY,", "burns it evenly"], ["ALL OVER", "entire body"]],
      detail=["Spot reduction is a myth.", "no such thing"], sweep="specifically from", push=1.06, drift=-8),
 # ---------------- the muscle
 dict(id="T2", kind="title", start="When you're training your abs, you're training", dur=2.4, step=2, headline="The Muscle That\nShrinks Your Waist"),
 dict(id="AN1", kind="anat", start="a muscle group in your abs", end="still have belly fat", heading="Your 2 Ab Muscles",
      stage_ph=["rectus abdominis", "transverse abdominis"],
      rows=[["Six Pack Muscle", "The visible front. Crunches train it."], ["Deep Waist Muscle", "A hidden sleeve. The vacuum trains it."]],
      note="new kind: a drawn two-muscle diagram in the 3A card; the six pack lights on 'rectus abdominis', the deep belt on 'transverse abdominis'"),
 dict(id="G03", kind="lt", start="Now the vacuum has been used", end="tiny waist", topic=KP,
      point="Bodybuilders Have Used It Since THE 1960s.", parts=[["Bodybuilders Have Used It", "has been used"], ["Since THE 1960s.", "since the 60s"]]),
 dict(id="G04", kind="lt", start="Just as important", end="making yourself aware", topic=KP,
      point="The Mirror Is HALF The Exercise.", parts=[["The Mirror Is HALF The Exercise.", "Just as important"]]),
 # ---------------- why the standing vacuum
 dict(id="T3", kind="title", start="So there are three types", dur=3.05, step=3, headline="Why The Standing Vacuum"),
 dict(id="L1", kind="l3", start="your knees", end="is the standing vacuum", heading="3 Types Of Vacuums",
      points=["Kneeling", "Hands And Knees", "Standing"], reveal=["your knees", "hands and knees", "the one that I recommend"]),
 dict(id="L2", kind="l3", start="The standing vacuum also has", end="It's super easy", heading="Why Standing",
      points=["Do it anywhere", "No equipment", "Takes a few minutes"], reveal=["do it anywhere", "any equipment", "it just takes"]),
 dict(id="C03", kind="clip", start="is like a real life AI", dur=10.15, src=[DEMO + "@0"],
      note="the approved demo of Dan generating his goal picture (Ad 14 R3 g17), exact sequence and AI-GENERATED label"),
 # ---------------- how to do it
 dict(id="T4", kind="title", start="so let's talk about how to do the vacuum", dur=2.4, step=4, headline="How To Do It"),
 dict(id="L3", kind="l3", start="The first step is you want to do it in the mirror", end="is a real good time", heading="Before You Start",
      points=["In a mirror", "Shirtless", "Empty stomach"], reveal=["in the mirror", "do it shirtless", "empty stomach"]),
 dict(id="G05", kind="lt", start="It's not optimal", end="push yourself as much", topic=KP,
      point="Do It On An EMPTY STOMACH.", parts=[["Do It On An EMPTY STOMACH.", "It's not optimal"]]),
 dict(id="G07", kind="lt", start="going to consciously slump", end="The next step", end_at_start=True, topic="STEP 1",
      point="Slump. Let Your Stomach OUT.", parts=[["Slump.", "consciously slump"], ["Let Your Stomach OUT.", "bulge out"]]),
 dict(id="G08", kind="lt", start="consciously suck", end="as much as possible", topic="STEP 2",
      point="Suck It In As HARD As You Can.", parts=[["Suck It In", "consciously suck it in"], ["As HARD As You Can.", "really working"]]),
 dict(id="G09", kind="lt", start="you want to use a timer", end="every set of your vacuums", topic="STEP 3",
      point="Use A Timer. Hold 20 SECONDS.", parts=[["Use A Timer.", "use a timer"], ["Hold 20 SECONDS.", "20 second sets"]]),
 dict(id="G06", kind="lt", start="you want to take short breaths", end="breathe normally", topic=KP,
      point="Take SHORT BREATHS Through Your Nose.", parts=[["Take SHORT BREATHS Through Your Nose.", "take short breaths"]]),
 # ---------------- a live set
 dict(id="T5", kind="title", start="so now I'll show you what a set", dur=2.4, step=5, headline="A Live Set"),
 dict(id="K1", kind="count", shot="set.0", secs=20, beep_src=55.08, note="new kind: 20-second countdown chip, top left, ends on his phone timer's beep"),
 # ---------------- your routine
 dict(id="T6", kind="title", start="Let's say you're a beginner", dur=2.4, step=6, headline="Your Routine"),
 dict(id="L5", kind="l3", start="What I recommend is first thing", end="When you're resting", end_at_start=True, heading="The Routine",
      points=["1 set of 20 seconds", "Then 2 sets", "Then 3 sets", "Rest 1 minute between"],
      reveal=["20 seconds of a timed", "two sets", "three sets", "give yourself a minute to rest in between. When"]),
 # ---------------- takeaway + ending
 dict(id="S1", kind="scene", scene="recap", start="Crunches and sit ups do not target", end="from anywhere", tail=0.4, eyebrow="THE TAKEAWAY",
      headline="If You Have Belly Fat", items=["Stop the ab exercises for now", "Fat burns evenly, all over", "Total body workouts + nutrition", "Vacuums every morning"]),
 dict(id="U1", kind="url", start="go to absbyai", end="you can generate a picture"),
 dict(id="C04", kind="clip", start="you can generate a picture", dur=10.15, src=[DEMO + "@0"],
      note="the approved demo again, as he describes generating the picture"),
 dict(id="U2", kind="url", start="So go to", end="getting in shape", tail=0.6),
]
