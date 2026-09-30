"""RO-10 visual plan. Every item is anchored to the words Dan says (phrase -> output time via words_out.json).
Kinds built from the approved HyperFrames templates (hyperframes/from_plan.py): lt (Motivation lower third, parts land on
their words), scene/fact (before / fact card), l3 (3A side list, items land on their words), cycle (4-step loop card).
Kinds that stay softblue.py: title (full-screen way card), scene/recap, phone (app demo beside Dan). clip = full-frame
cutaway (Pexels / library), hard cuts. start = phrase whose first word starts the item; end = phrase whose last word
ends it (or dur). Inside a template item every time is a phrase too (resolved by from_plan.py)."""
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
ST = "/Volumes/Extreme/_edit_work/ro10/stock"
PH = "/Volumes/Extreme/_edit_work/ro10/assets"
PLAN = [
 # ---------------- hook (on camera; no AI opener, see What I decided)
 dict(id="G01", kind="lt", start="Most people overcomplicate", end="than you are right now", topic="THE REAL REASON",
      point="Carbs, Insulin, Seed Oils? No. It's CALORIES.",
      parts=[["Carbs, Insulin, Seed Oils?", "argue about carbs"], ["No. It's CALORIES.", "it just comes down"]]),
 # ---------------- the proof
 dict(id="C01", kind="clip", start="a nutrition professor at Kansas State", end="for 10 weeks", src=[f"{ST}/p8844683.mp4@8.0"],
      note="junk food laid out (chips, cola, chocolate); no person eating"),
 dict(id="G02", kind="scene", scene="fact", start="but he kept it under", end="eating less calories", photo=f"{PH}/cookies.jpg",
      eyebrow=["1,800 CAL A DAY", "but he kept it"], headline=[["27 lb", "27"], ["LOST", "pounds"]], count={"value": "27", "from": 0, "dur": 0.55},
      detail=["Cholesterol got BETTER.", "cholesterol"], sweep="junk food", push=1.06, drift=-8),
 dict(id="C02", kind="clip", start="Stanford put 609 people", end="for a full year", src=[f"{ST}/p8768892.mp4@0.3"],
      note="salad bowl set on a table, overhead (a diet)"),
 dict(id="G03", kind="lt", start="Both groups lost", end="ended up eating less calories", topic="STANFORD 2018: 609 PEOPLE",
      point="Low Carb Or Low Fat: SAME Weight Loss.",
      parts=[["Low Carb Or Low Fat:", "Both groups lost"], ["SAME Weight Loss.", "same amount"]]),
 dict(id="C03", kind="clip", start="where scientists controlled every bite", end="every bite people ate", tail=0.4, src=[f"{ST}/p8863360.mp4@1.0"],
      note="lab scientist (controlled feeding studies)"),
 dict(id="C04", kind="clip", start="researchers took people who swore", end="calories per day", src=[f"{ST}/p6771504.mp4@2.0"],
      note="hand writing a food log beside a phone"),
 dict(id="G04", kind="scene", scene="fact", start="When they measured it", end="completely normal", photo=f"{PH}/foodlog.jpg",
      eyebrow=["NEJM, 1992", "When they measured"], headline=[["47% MORE", "47"]], count={"value": "47", "from": 0, "dur": 0.6},
      detail=["than they thought they ate.", "than they thought"], sweep="metabolisms", push=1.06, drift=-8),
 # ---------------- way 1
 dict(id="T1", kind="title", start="Number one, take", dur=2.4, step=1, headline="Get On A GLP-1\nMedication"),
 dict(id="C05", kind="clip", start="It works because it turns your appetite down", end="fewer calories", src=[f"{ST}/p6824226.mp4@1.0"]),
 dict(id="G05", kind="lt", start="In a big clinical trial", end="their body weight", topic="THE BIG CLINICAL TRIAL",
      point="Highest Dose: About 20% Of Body Weight LOST.",
      parts=[["Highest Dose:", "highest dose"], ["About 20% Of Body Weight LOST.", "about 20"]]),
 dict(id="G06", kind="lt", start="about 1", end="something I barely", topic="MY EXPERIENCE",
      point="1.5 mg A Week. Eating Less Got EASY.",
      parts=[["1.5 mg A Week.", "about 1"], ["Eating Less Got EASY.", "Eating less went"]]),
 # ---------------- way 2
 dict(id="T2", kind="title", start="here's the second one. Know", dur=2.4, step=2, headline="Know Your\nCalorie Number"),
 dict(id="G07", kind="lt", start="take the body weight you want", end="calories a day", topic="YOUR STARTING NUMBER",
      point="Goal Weight x 12. 180 lb Goal = About 2,100 CAL A DAY.",
      parts=[["Goal Weight x 12.", "take the body weight"], ["180 lb Goal = About 2,100 CAL A DAY.", "180"]]),
 dict(id="G08", kind="cycle", start="Then weigh yourself", end="easier to follow", title="Your Weekly Loop", hue="teal", direction="cw",
      boxes=["Set a number", "Weigh daily", "Weekly average", "Lower it a bit"],
      reveal={"TL": "Then weigh", "TR": "weigh yourself every", "BR": "look at your average", "BL": "lower your number"},
      close="keep going", pulse="real number", drift=-12),
 # ---------------- way 3
 dict(id="T3", kind="title", start="So number three", dur=2.4, step=3, headline="Track Your Calories\nWith AI"),
 dict(id="C06", kind="clip", start="You used to need a food scale", end="nobody stuck with it", src=["B0017"]),
 dict(id="C07", kind="clip", start="With AI you just take a picture", end="in just a few seconds", src=[f"{ST}/p8907615.mp4@0.5"]),
 dict(id="P01", kind="phone", start="We have a free one", end="tracker you like", src=["B0038"], note="real AbsByAI meal-log screen in the approved phone, Dan beside it"),
 # ---------------- way 4
 dict(id="T4", kind="title", start="Let's talk about the next one", dur=2.4, step=4, headline="Fast Until\n2 PM"),
 dict(id="G09", kind="l3", start="Here's what I do", end="dinner in the evening", heading="How I Eat",
      points=["Nothing until 2 PM", "Big salad first", "Real dinner at night"],
      reveal=["I don't eat anything", "break my fast", "I eat dinner"]),
 dict(id="G10", kind="lt", start="If you eat breakfast", end="go to bed hungry", topic="YOUR 2,000 CALORIES",
      point="Eat All Day: 1,200 Gone By 2 PM. Tiny DINNER.",
      parts=[["Eat All Day: 1,200 Gone By 2 PM.", "If you eat breakfast"], ["Tiny DINNER.", "dinner has to be tiny"]]),
 dict(id="C08", kind="clip", start="So you can sit down with your family", end="a real meal", tail=0.6, src=[f"{ST}/p6304835.mp4@1.0"]),
 # ---------------- way 5
 dict(id="T5", kind="title", start="Number 5 goes together", dur=2.4, step=5, headline="Drink Black Coffee\nWhile You Fast"),
 dict(id="C09", kind="clip", start="I drink 2-4 cups", end="food until 2", tail=1.3, src=[f"{ST}/p19157857.mp4@2.0"]),
 dict(id="G11", kind="lt", start="It has to be black coffee", end="breaks your fast", topic="KEEP IT BLACK",
      point="Cream And Sugar: Up To 200 CAL A CUP.",
      parts=[["Cream And Sugar:", "Cream and sugar"], ["Up To 200 CAL A CUP.", "add 200"]]),
 # ---------------- way 6
 dict(id="T6", kind="title", start="Here's the next one, and almost", dur=2.4, step=6, headline="Start Every Meal\nWith A Salad"),
 dict(id="C10", kind="clip", start="They gave people a big", end="as they wanted", src=[f"{ST}/p3189049.mp4@2.0", f"{ST}/p8481268.mp4@3.0"],
      note="salad tossed at a dinner table, then a man eating his main course"),
 dict(id="G12", kind="scene", scene="fact", start="Those people ate about", end="any less full", photo=f"{PH}/salad.jpg",
      eyebrow=["PENN STATE STUDY", "Those people"], headline=[["12% FEWER", "12"]], count={"value": "12", "from": 0, "dur": 0.5},
      detail=["calories, and just as full.", "didn't feel"], sweep="whole meal", push=1.06, drift=-8),
 dict(id="C11", kind="clip", start="broth-based soup", end="broth-based soup", tail=0.9, src=[f"{ST}/p6645713.mp4@6.0"]),
 # ---------------- way 7
 dict(id="T7", kind="title", start="Number seven", dur=2.4, step=7, headline="Snack On Protein,\nNot Carbs"),
 dict(id="C12", kind="clip", start="Chips, crackers", end="keep eating them", src=[f"{ST}/p10973447.mp4@0.5"]),
 dict(id="G13", kind="l3", start="So keep protein snacks around", end="grams of protein", heading="Protein Snacks",
      points=["Beef jerky", "Sardines", "Greek yogurt, cottage cheese", "Deli turkey"],
      reveal=["beef jerky", "sardines", "Greek yogurt", "deli turkey"]),
 # ---------------- way 8
 dict(id="T8", kind="title", start="And then finally, number eight", dur=2.4, step=8, headline="Stop Drinking\nLiquid Calories"),
 dict(id="C13", kind="clip", start="they got it as jelly beans", end="jelly beans", tail=0.5, pad_to_next=True, src=[f"{ST}/p8670642.mp4@1.0"]),
 dict(id="C14", kind="clip", start="they got it as soda", end="as soda", tail=0.5, src=[f"{ST}/p12511820.mp4@0.5"]),
 dict(id="G14", kind="lt", start="When they ate the jelly beans", end="and they gained weight", topic="PURDUE: SAME 450 CALORIES",
      point="Jelly Beans: No Gain. Soda: GAINED WEIGHT.",
      parts=[["Jelly Beans: No Gain.", "didn't gain weight"], ["Soda: GAINED WEIGHT.", "When they drank the soda"]]),
 dict(id="G15", kind="l3", start="That means soda", end="filling them up", heading="Liquid Calories",
      points=["Soda", "Juice, sweet tea", "Starbucks drinks", "Beer"],
      reveal=["soda juice", "juice", "the coffee drinks", "and beer"]),
 # ---------------- wrap
 dict(id="C15", kind="clip", start="sell you books and supplements", end="you don't need", src=[f"{ST}/p7615429.mp4@9.0"]),
 dict(id="G16", kind="scene", scene="recap", start="Know your number, track it", end="far, far easier", eyebrow="THE 8 WAYS",
      headline="8 Ways To Eat Less Calories",
      items=["Get on a GLP-1", "Know your number", "Track it with AI", "Fast until 2 PM",
             "Drink black coffee", "Start with a salad", "Snack on protein", "Don't drink calories"]),
]
