# Lead editor items that sit inside the other parts' stretches (each is found anywhere in the film by its own words, so this
# file does not have to be in film order): the new AI clips (frames for approval, motion only after Dan approves them), the real
# photo scenes, and the closing call to action. ROUND 2 (Dan's round 1 notes, 2026-10-11): P04 / P05 are two new same-pose pairs (arms down, side pose)
# cropped to one body scale by photocrop.py; A1 to A4 have finished motion (round2/motion, the src and trims live in plan_resolved.json, patched by hand: the
# ai() items below are the round 1 placeholders); A5 (frames) replaces the stock doctor Cc16; Cb02 (library B0437, Dan on his phone) is removed. No AbsByAI.com mark graphic (Dan, 2026-10-01).
RO6 = "/Volumes/Extreme/_edit_work/ro06"
PH = dict(people="dan", physique=True, label="Real pictures of me. Not AI-generated.", label_in_picture=True)
def ai(i, start, end, note, tail=0.1): return dict(id=i, kind="clip", start=start, end=end, tail=tail, frames=[f"{AI}/{i}-start.png", f"{AI}/{i}-end.png"], pending=True, anywhere=True, **AIL, **OTHER, note=note)
PART = [
 dict(id="P03", kind="clip", start="I decided to go expensive because", end="for my social media,", tail=0.6, src=[f"{W}/gfx/r2/P03.mp4@0"], anywhere=True,
      portraits=["tan_13", "tan_223", "tan_17"], **PH,
      note="Three of his real pictures from the pool photo shoot the tan was for, as three portraits on the Soft Blue field"),
 ai("A4", "So it's actually very quick.", "in about 10 minutes.",
    "THE APPOINTMENT, new AI clip (frames for approval), played straight: a man stands in a pop-up tanning tent while the specialist sprays him; as the mist passes over him his skin goes from untanned to an even golden tan. Pexels has no footage of a real spray tan", tail=0.25),
 ai("A3", "That means that you're going to", "sleep with your tan on.",
    "DESTROY YOUR SHEETS, new AI clip (frames for approval), a gag: a tanned man asleep in spotless white sheets; cut to morning, he pulls back the duvet and finds a brown print of his whole body on the sheet and stares at it"),
 dict(id="P04", kind="clip", start="I'm going to show you a few pictures,", end="what I looked like after.", tail=0.15, src=[f"{W}/gfx/r2/P04.mp4@0"], anywhere=True,
      pair=["pale2_down", "tan2_down"], **PH,
      note="Before and after, hands at his hips: the pale earlier shoot on the left, the pool shoot after the tan on the right"),
 dict(id="P05", kind="clip", start="Keep in mind the lighting was", end="for the second shoot.", tail=0.15, src=[f"{W}/gfx/r2/P05.mp4@0"], anywhere=True,
      pair=["pale2_side", "tan2_side"], **PH,
      note="Before and after, in the same teal shorts by the pool: flexing in the pale earlier shoot on the left, standing in the pool after the tan on the right"),
 dict(id="Gp01", kind="lt", start="However, even taking those factors into", end="a significant difference.", tail=0.3, topic="MY TAKE", anywhere=True,
      point="Better Light, Leaner, And The Tan Still Mattered", parts=[["Better Light, Leaner,", "even taking those factors"], ["And The Tan Still Mattered", "the tan really made"]]),
 dict(id="Gp02", kind="lt", start="And if you value how you", end="investing $50 to $100.", tail=0.3, topic="YOU BE THE JUDGE", anywhere=True,
      point="Is That Difference Worth $50 To $100?", parts=[["Is That Difference Worth", "if that difference would be"], ["$50 To $100?", "$50"]]),
 ai("A2", "You don't need to go full", "than you are right now.",
    "TOO MUCH TAN, new AI clip (frames for approval), a gag: a pale man in a tanning tent smiles hopefully as the specialist starts spraying; he comes out bright traffic cone orange and stares at his arms while she winces. No real person is pictured"),
 ai("A1", "Number one, vampires, people out", "you have no choice.",
    "VAMPIRES, new AI clip (frames for approval), a gag: a chalk white vampire in a cape cowers under a black umbrella on a sunny beach; a mist of spray tan drifts over him and he ends up golden, in sunglasses, umbrella closed, thumbs up"),
 dict(id="Gz01", kind="lt", start="If you guys wanna take the first", end="go to absbyai", tail=0.2, topic="YOUR FIRST STEP", anywhere=True,
      point="See What You'd Look Like With Abs", parts=[["See What You'd Look Like With Abs", "If you guys wanna take"]]),
 dict(id="P06", kind="clip", start="you're gonna upload a picture of yourself", end="you've always wanted.", tail=0.2, src=[f"{RO6}/round5/phone/P01-softblue.mp4@0.0"], anywhere=True,
      people="dan", physique=True, label="AI-GENERATED", label_in_picture=True,
      note="the approved self-generation demo (your sunglasses photo to the pool goal) in the Soft Blue phone card, the same file as the last three videos"),
 dict(id="Gz02", kind="lt", start="Not someone else with your head", end="with your dream physique.", tail=0.3, topic="KEY POINT", anywhere=True,
      point="The REAL You, Not Your Head On Someone Else", parts=[["The REAL You,", "the real you"], ["Not Your Head On Someone Else", "with your dream"]]),
 dict(id="Gz03", kind="lt", start="Once you see how good you", end="to make it happen.", tail=0.3, topic="WHY IT WORKS", anywhere=True,
      point="Seeing Your Goal Body Builds Motivation", parts=[["Seeing Your Goal Body Builds Motivation", "Once you see how good"]]),
 dict(id="Gz04", kind="lt", start="We have an AI personal trainer,", end="program to get there.", tail=0.2, topic="AI PERSONAL TRAINER", anywhere=True,
      point="A Workout Program Built From Your Photo", parts=[["A Workout Program Built From Your Photo", "We have an AI personal trainer"]]),
 dict(id="Gz05", kind="lt", start="We have an AI nutritionist,", end="get you to your goal.", tail=0.2, topic="AI NUTRITIONIST", anywhere=True,
      point="A Meal Plan Built On Foods You Like", parts=[["A Meal Plan Built On Foods You Like", "We have an AI nutritionist"]]),
]
