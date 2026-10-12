# 53:04 to 54:05 on the cut timeline (3184.31 to 3244.81 s)  VIDEO 1's OWN SIGN-OFF, appended after the 53 minute film (round 3,
# 2026-10-12). It is the roll's other complete closing take (C1511 3974.2 to 4046.8 s, pieces v1so1 to v1so4), so video 1 ends on
# camera the way video 3 does. Nothing here belongs to video 2 or video 3: video 3 still ends at 3184.225 s.
# The items mirror the approved close of video 3 (p07_cta.py: Gh01 to Gh05 and the self-generation demo P01), re-worded to what he
# says in THIS take. Lower thirds are signposts (a product feature list in the CTA is allowed). No AbsByAI.com mark graphic.
# P03 is the same approved Soft Blue phone card file as P01 (sunglasses photo to pool goal). Its beats land on his words here:
# photo on "upload a picture of yourself", the form on "describe your dream physique", generating on "click a few buttons",
# the result on "and bam". It ends on the join where the stray "Not," was cut, so that join is never seen.
# The second sentence ends on "you'll be filled with motivation.": his next three words ("to make you happen", a slip) are cut.
# He names an "AI trainer" here (not "personal trainer") and a "sleep tracker" as well as the sleep coach: the labels follow him.
RO6 = "/Volumes/Extreme/_edit_work/ro06"
PART = [
 dict(id="Gi01", kind="lt", start="If you wanna take the first step", end="go to absbyai .com", tail=0.2, topic="YOUR FIRST STEP",
      point="See Yourself With Ripped Six-Pack Abs.", parts=[["See Yourself With Ripped Six-Pack Abs.", "If you wanna take the first"]]),
 dict(id="P03", kind="clip", start="you can upload a picture of yourself", end="of your dream physique", tail=0.1, src=[f"{RO6}/round5/phone/P01-softblue.mp4@0.0"],
      people="dan", physique=True, label="AI-GENERATED", label_in_picture=True,
      note="the approved self-generation demo (your sunglasses photo to the pool goal) in the Soft Blue phone card, the same file as P01 in video 3's close and the last two videos"),
 dict(id="Gi02", kind="lt", start="Once you see how amazing you look", end="filled with motivation", tail=0.0, topic="WHY IT WORKS",
      point="Seeing Yourself With Abs Builds Motivation.", parts=[["Seeing Yourself With Abs Builds Motivation.", "Once you see how amazing"]]),
 dict(id="Gi03", kind="lt", start="We have an AI trainer", end="customized workout program", tail=0.2, topic="AI TRAINER",
      point="A Customized Workout Program.", parts=[["A Customized Workout Program.", "We have an AI trainer"]]),
 dict(id="Gi04", kind="lt", start="An AI nutritionist which will design", end="your food preferences", tail=0.2, topic="AI NUTRITIONIST",
      point="A Custom Meal Plan Built On Foods You Like.", parts=[["A Custom Meal Plan Built On Foods You Like.", "An AI nutritionist which will"]]),
 dict(id="Gi05", kind="lt", start="We have an AI sleep tracker", end="much much more", tail=0.3, topic="AI SLEEP COACH",
      point="Plus An AI Sleep Tracker And Much More.", parts=[["Plus An AI Sleep Tracker And Much More.", "We have an AI sleep tracker"]]),
]
