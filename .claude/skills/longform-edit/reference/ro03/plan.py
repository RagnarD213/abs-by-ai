"""RO-03 "The Vacuum: Workout Only" visual plan, round 1. CONTENT (LFC). Modelled on the workout sections of Muhammad's
ab wheel cut: a label on screen through every set, one form cue per set, Dan talking in the rests, a size change inside
each set, his flash into each set, music up in the sets. All graphics are Soft Blue Light.
Times: a phrase Dan says (resolved on words_out.json), or ("hold", n, seconds) = seconds after hold n starts.
HyperFrames (from_plan.py): lt (Motivation lower third). gfx.py: wtitle (title chip), work (set / rest countdown chip),
clip (full-frame cutaway, hard cuts)."""
W = "/Volumes/Extreme/_edit_work/ro03"
HOLD_SRC = 35.08; BEEP_SRC = 55.08; SECS = 20; REST = 30          # C1625: the hold starts 20 s before the phone timer's beep (RO-02 K1)
SETS = ["set1", "set2", "set3"]
FLASH_INTO = ["set1.0", "set2.0", "set3.0"]                       # Muhammad's silent bloom flash on the cut into each set
PLAN = [
 dict(id="C00", kind="clip", start="Alright", end="I'm going to time", end_at_start=True, lead=-0.07, src=[f"{W}/assets/vacuum_teaser.mp4@0.5"],
      note="the first 3 seconds: the hold done correctly (this film's own live set, the clip RO-02 used as its teaser), his first line under it"),
 dict(id="T00", kind="wtitle", t0=0.0, end_shot="intro.0", eyebrow="FOLLOW ALONG", headline="The Vacuum Workout", detail="3 sets of 20 seconds. Rest 30 seconds.",
      note="title chip, top left, over the opening clip and his intro line"),
 dict(id="K00", kind="work", start_shot="set1.0", end_shot="set3.1", note="one chip, top left, from the first set to the last beep: SET n OF 3 with the 20-second countdown, then REST with the 30-second countdown. RO-02's approved countdown chip with a set line added."),
 dict(id="G01", kind="lt", t0=("hold", 1, 3.0), t1=("hold", 1, 9.6), topic="FORM CUE", point="Suck It In As HARD As You Can.", parts=[["Suck It In As HARD As You Can.", ("hold", 1, 3.0)]]),
 dict(id="G02", kind="lt", start="it's important that you take", end="next set", topic="KEY POINT",
      point="Between Sets, Take DEEP Belly Breaths.", parts=[["Between Sets,", "it's important"], ["Take DEEP Belly Breaths.", "deep belly"]]),
 dict(id="G03", kind="lt", t0=("hold", 2, 9.4), t1=("hold", 2, 16.0), topic="FORM CUE", point="Belly Button THROUGH Your Spine.", parts=[["Belly Button THROUGH Your Spine.", ("hold", 2, 9.4)]]),   # on the far half of set 2: on the near framing the strip would sit across his waist
 dict(id="G04", kind="lt", start="you want to take short", end="breathe normally", topic="KEY POINT",
      point="Take SHORT BREATHS Through Your Nose.", parts=[["Take SHORT BREATHS Through Your Nose.", "you want to take short"]]),
 dict(id="G05", kind="lt", t0=("hold", 3, 2.0), t1=("hold", 3, 8.6), topic="LAST SET", point="Keep Pulling In. This Should Be HARD.", parts=[["Keep Pulling In.", ("hold", 3, 2.0)], ["This Should Be HARD.", ("hold", 3, 3.6)]]),
 dict(id="G06", kind="lt", start="What I recommend", end="just that one set", tail=0.0, topic="KEY POINT",
      point="Beginners: Start With ONE Set Every Morning.", parts=[["Beginners:", "What I recommend"], ["Start With ONE Set Every Morning.", "do 20 seconds"]]),
]
