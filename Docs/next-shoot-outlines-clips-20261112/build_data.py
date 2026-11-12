"""Builds clips.json for the Next Shoot Outlines clip review page (2026-11-12). Run, then page.py."""
import json, os
def it(t, v, vid, segs, src, views, words, what, lesson, note=None, take=None):
    d = {"t": t, "v": v, "id": vid, "segs": segs, "src": src, "views": views, "words": words, "what": what,
         "pts": ([f"My take: {take}"] if take else []) + [f"Lesson: {lesson}"]}
    if note: d["note"] = note
    return d
def sec(sid, heading, sub, label, items):
    return {"id": sid, "heading": heading, "sub": sub, "label": label, "pick": True, "reply_label": sid.upper(), "items": items}
S = []
S.append(sec("b06", "B06 Smaller Plates (reaction Short)", "No big celebrity on video says it. This is the real source of the line you remember: the Profit First author.", "Reaction Short", [
 it("Profit First Author Says Get Smaller Plates. He's Right.", "right", "-8O2Rw8moHs", [[358, 372]], "TEDx Talks, Mike Michalowicz, \"Profit first is better for entrepreneurs than G.A.A.P.\"", "79K views",
    "Starts on \"he said what we need to do for health is get smaller plates\". Ends on \"with his wooden teeth\".",
    "Mike Michalowicz, author of Profit First, repeats what a fitness expert told him: smaller plates. He uses it as the analogy for his money system.",
    "buy smaller plates; the same portion looks like a meal.", "Not a household name. Alternate if you want a celebrity: Wendy Williams, Entertainment Tonight KyiVs3iS-P0 (not yet checked).")]))
S.append(sec("d15", "D15 Should You Train to Failure?", "Cutler confirmed. No clip of Clavicular saying to leave one rep in the tank was found; the closest is below.", "Long reaction", [
 it("Jay Cutler Never Trained To Failure", "plain", "VW9hnJL9UZE", [[0, 7]], "Renaissance Periodization, \"Jay Cutler Never Trained to Failure\"", "680K views",
    "Starts on \"Jay Cutler was on a podcast\". Ends on \"I never trained to failure ever in my career\".",
    "Dr. Mike sets it up, then Cutler's own line.", "failure depends on who you are; Cutler's failure is real failure."),
 it("Greg Doucette Mocks Clavicular's Training", "plain", "YN_NYiW0a6E", [[556, 566]], "Greg Doucette, \"Juicing My Pants Reviewing Clavicular's Workout\"", "317K views",
    "Starts on \"Bro goes to the gym, does sets of four, maybe five reps\". Ends on \"only trains once a month\".",
    "Doucette's words about Clavicular, not Clavicular's own. Stand-in until a real Clavicular clip is found.",
    "most guys who think they hit failure have five reps left.", "Not Clavicular speaking. Tell me if you know where he said it.")]))
d04 = [("JxgwVez4DuM", 587, 593, "Squat stuck at the bottom, he ends face down under the bar", "leg press: the sled stops, nothing lands on you"),
 ("JxgwVez4DuM", 307, 314, "Loaded bar off the floor drags him over backward", "leg press and hamstring curl"),
 ("JxgwVez4DuM", 348, 355, "Bench with no collars: plate slides, bar tips, he's pinned", "chest press machine"),
 ("JxgwVez4DuM", 382, 387, "Bench bar tilts and the plates slide", "chest press machine or chest flies"),
 ("JxgwVez4DuM", 356, 363, "Deadlift with hips too low, then he collapses", "hamstring curl, glute bridge machine, T-bar row"),
 ("JxgwVez4DuM", 172, 181, "Snatch: bar crashes down behind him", "lat pulldown and side laterals"),
 ("LRr17X-hlwA", 60, 72, "Red onesie squat collapse, plates spill", "leg press and glute bridge machine"),
 ("LRr17X-hlwA", 1023, 1035, "Heavy squat bailed in the rack", "leg press"),
 ("LRr17X-hlwA", 275, 287, "Loaded bar crashes down and bounces", "leg press and hamstring curl")]
S.append(sec("d04", "D04 Worst Gym Mistakes", "Silent fail clips. Each card: the fail, then the machine that makes it impossible.", "Long reaction",
 [it(f"Fail {n}: {w}", "wrong", v, [[a, b]], "FailArmy" if v == "JxgwVez4DuM" else "FailArmy 2.0", "3M views" if v == "JxgwVez4DuM" else "502K views",
     "No speech: check by eye.", w + ".", fix) for n, (v, a, b, w, fix) in enumerate(d04, 1)]))
d05 = [("ZwJJuy_IQYU", 180, 196, "Bikman, Diary Of A CEO Clips", "864K views", "for every six pounds of fat a person was losing", "including muscle and bone", "Muscle loss: 40% of the weight lost is lean mass.", "half true; lift every day and eat protein first."),
 ("nlC7rDjnfnw", 132, 151, "Jillian Michaels, Club Random", "134K views", "you can't get off of it ever", "yo-yo dieting on crack", "You'll gain it all back.", "true if you quit cold; stay on a low dose."),
 ("zpyibQvpjcw", 68, 89, "Jillian Michaels, NewsNation", "75K views", "You can lose weight by eating less", "vision problems", "Fix your diet instead, plus side effects.", "I fixed my diet and still sat at 190 for a year."),
 ("nlC7rDjnfnw", 80, 93, "Jillian Michaels, Club Random", "134K views", "now we're 18 months into it and you will plateau", "let me Google that for you", "It stops working.", "it's a dial: raise the dose a step and eat a little less."),
 ("qX9nQ40mSMY", 41, 57, "RFK Jr.", "62K views", "the EU is right now investigating", "makes you want to do everything less", "It makes you want to do everything less.", "true, and that's the point: less alcohol, less sugar."),
 ("qX9nQ40mSMY", 59, 80, "RFK Jr.", "62K views", "we're spending $1600 a month on this drug", "$3 trillion a year", "Cost.", "price it the way you buy it."),
 ("zpyibQvpjcw", 843, 861, "Calley Means, NewsNation", "75K views", "this is on the box, a lifetime drug", "lifetime recurring annuity", "It's a lifelong drug.", "true, and fine: a low dose for life."),
 ("ZwJJuy_IQYU", 473, 489, "Bikman, Diary Of A CEO Clips", "864K views", "you also are not interested as much in exercise", "drinking with the boys", "You'll stop wanting to exercise.", "wrong for me: seven days a week."),
 ("qX9nQ40mSMY", 111, 126, "RFK Jr.", "62K views", "in Denmark they do not recommend it", "so addicted to drugs", "Eat better instead of taking a drug.", "the drug is what made eating better stick."),
 ("zpyibQvpjcw", 359, 380, "Jillian Michaels, NewsNation", "75K views", "we can facilitate 15% weight loss", "diarrhea, constipation", "It's cheating.", "a tool is not cheating.")]
S.append(sec("d05", "D05 Arguments Against Zepbound", "Each card is one objection. Note: three Jillian Michaels clips; you passed on her once as boring.", "Long reaction",
 [it(f"Objection {n}: {o}", "wrong", v, [[a, b]], src, vw, f"Starts on \"{f}\". Ends on \"{l}\".", o, les) for n, (v, a, b, src, vw, f, l, o, les) in enumerate(d05, 1)]))
d07 = [("jYY4FDzf4p0", 52, 64, "there's a few things that matter", "don't do it for a day", "If you can't do it for a decade, don't do it for a day.", "right", "pick habits you can keep for ten years."),
 ("fxyhIXZ6Yog", 82, 94, "here's step three, you multiply your weight", "means 200 grams of protein", "One gram of protein per pound.", "wrong", "about 0.6 grams per pound is enough."),
 ("fxyhIXZ6Yog", 58, 72, "let's say I'm a 200 lb guy", "2,000 calories", "Cutting calories = body weight x 10.", "plain", "your verdict."),
 ("fxyhIXZ6Yog", 149, 167, "here's the magic of how this works", "that's 880 calories", "Hit protein first, the rest is free.", "plain", "eat the protein first at every meal."),
 ("fxyhIXZ6Yog", 200, 213, "I eat the same breakfast and lunch every day", "grab a Quest Bar at the airport", "Same breakfast and lunch every day.", "right", "decide your meals before you're hungry."),
 ("jYY4FDzf4p0", 268, 278, "if you don't track what you eat", "you don't even have data", "Track what you eat.", "right", "weigh in every morning."),
 ("jYY4FDzf4p0", 106, 121, "I eat two pounds of meat a day", "dessert in excess of my calories", "Two pounds of meat a day, dessert on top.", "plain", "your verdict."),
 ("jYY4FDzf4p0", 129, 139, "training has been progressive overload", "almost two decades", "Progressive overload on machines.", "right", "machines and cables, not barbells.")]
S.append(sec("d07", "D07 Hormozi's Fitness Rules", "One rule per card.", "Long reaction",
 [it(f"Rule {n}: {r}", v2, v, [[a, b]], "Alex Hormozi" if v == "fxyhIXZ6Yog" else "MoreMozi", "738K views" if v == "fxyhIXZ6Yog" else "19K views", f"Starts on \"{f}\". Ends on \"{l}\".", r, les) for n, (v, a, b, f, l, r, v2, les) in enumerate(d07, 1)]))
d08 = [(12, 23, "And then I looked around and I saw so many bodybuilders", "they didn't have fitness", "Bodybuilders with muscle who get winded doing simple things."),
 (0, 12, "When I was a younger man, I was super into bodybuilding", "a shoulder day", "He used to train body-part splits."),
 (34, 48, "and so you want to train in a way", "you want general fitness", "Over 40, train for your next 40 years."),
 (44, 58, "We're going to train the whole body using a pair of dumbbells", "which you absolutely need", "The circuit: six exercises back to back."),
 (261, 276, "You would rest for 2 minutes maybe", "50 reps on each of those motions", "Five rounds, about 30 minutes, about 300 reps."),
 (300, 320, "Point of showing you this workout is", "No gym needed", "Training for longevity, no gym needed."),
 (321, 336, "And so, the message here is that fitness", "in your own life", "His close: get it in, do the work.")]
S.append(sec("d08", "D08 Bodybuilder's Circuit (Fit Father Project)", "One video, about 41K views. Pick the moments you want to react to.", "Long reaction",
 [it(f"Moment {n}: {w}", "plain", "VwTeS5voWP4", [[a, b]], "Fit Father Project, Dr. Baldi", "41K views", f"Starts on \"{f}\". Ends on \"{l}\".", w, "your verdict on this point.") for n, (a, b, f, l, w) in enumerate(d08, 1)]))
d09 = [("The Rock", "-aWeIZxfT4E", 91, 104, "Tonight Show", "1.9M views", "I'm into pancakes. I'm into sushi", "you got to give it a shot", "Cheat meal: pancakes and sushi together.", "a cheat day wrecks a normal guy's week."),
 ("Mark Wahlberg", "zwDw9ptpk_o", 146, 163, "Men's Health", "2.9M views", "I learned the hard way", "eating at the right times", "Trained twice a day, 8 meals, then switched to fasting.", "skip breakfast."),
 ("Jason Momoa", "2rsyrVlZGP0", 150, 164, "Men's Health", "417K views", "My also my guilty breakfast", "That's the banger", "Buttery spaghetti, eggs and caviar for breakfast.", "real food, no shakes, but not this."),
 ("Bryan Johnson", "foa9ZhtyrfM", 41, 56, "Bryan Johnson", "1.3M views", "we've identified what the clinically relevant dose is", "in history", "Every calorie has to fight for its life.", "make every calorie earn its place."),
 ("Erling Haaland", "FV0B26YYCqA", 2, 20, "Aventura Australia (narrator, not Haaland)", "361K views", "This Norwegian football superstar", "massive tomahawk steaks", "6,000 calories of heart, liver, raw milk, steak.", "elite athletes only."),
 ("Michael Phelps", "2-6tagN27Q4", 8, 24, "Mashable Deals", "2.2M views", "when I was in high school", "it was brutal for me", "8,000 to 10,000 calories a day.", "you don't swim five hours a day."),
 ("Jennifer Aniston", "lLqtWLL5pXw", 90, 110, "adamtanswell (talk show re-upload)", "793K views", "intermittent fasting. Yeah, that's the no breakfast", "sixteen hours", "No breakfast, 16 hour fast.", "fast until 2 PM."),
 ("Arnold Schwarzenegger", "jFk-L7Wcg0g", 134, 152, "Men's Health", "27M views", "Now I eat more, you know, like oatmeal", "the only way you get big and strong", "He backed off meat and animal protein.", "your verdict."),
 ("Tom Brady", "XIPbMNnH2mI", 98, 115, "KPIX CBS News Bay Area", "211K views", "those electrolytes in there", "yeah, probably more", "Half your body weight in ounces of water.", "your water habit."),
 ("Henry Cavill", "lN10c2AGSFo", 51, 63, "Entertainment Tonight (2013)", "12K views", "well I had a couple of breaks without shooting", "an enormous pizza", "After a harsh cut, a whole apple pie and a huge pizza.", "a crash diet ends in a binge.")]
S.append(sec("d09", "D09 Celebrity Diets", "One celebrity per card. Pick the ten you want.", "Long reaction",
 [it(f"{c}: {w}", "plain", v, [[a, b]], src, vw, f"Starts on \"{f}\". Ends on \"{l}\".", w, les,
     note=("Narrator, not Haaland. " if c == "Erling Haaland" else "") + ("Check by eye that Aniston is speaking. " if c == "Jennifer Aniston" else "") or None)
  for (c, v, a, b, src, vw, f, l, w, les) in d09]))
d10 = [("5-jIV3R2v5I", 379, 393, "SunnyV2", "10.1M views", "by keeping the judgmental people away you only attract the insecure", "absolute peak performance", "Judgement free means you only attract the insecure.", "train where effort is normal."),
 ("PUJ4J2BQgCM", 83, 94, "Joe Bartolozzi", "Planet Fitness explainer", "part of the appeal of going to a gym", "pizza and donuts", "You go to a gym to train around other people.", "the people matter more than the equipment."),
 ("5-jIV3R2v5I", 352, 368, "SunnyV2", "10.1M views", "judgement free", "unless you're someone in shape", "Judgement free, unless you're in shape.", "the only one they judge is the guy trying."),
 ("dDusnIqziFI", 81, 94, "Papa Meat", "2.7M views", "Like every month they have a pizza day", "what is this?", "Monthly pizza day. It's Pizza Hut.", "pizza night tells you who the gym is for."),
 ("5-jIV3R2v5I", 463, 483, "SunnyV2", "10.1M views", "pizza at a gym", "meetings in a bar", "Pizza at a gym is like AA meetings in a bar.", "pick a gym that wants you to change."),
 ("PUJ4J2BQgCM", 95, 109, "Joe Bartolozzi", "Planet Fitness explainer", "we do not cater to bodybuilders", "four plates", "Leg press sign: no bodybuilders, four plates max.", "they told you who they want."),
 ("5-jIV3R2v5I", 167, 183, "SunnyV2", "10.1M views", "lunk alarm", "end by eye", "The lunk alarm.", "a siren for training hard."),
 ("dDusnIqziFI", 447, 460, "Papa Meat", "2.7M views", "kicked out", "end by eye", "Member kicked out for breathing hard and grunting.", "your verdict."),
 ("PUJ4J2BQgCM", 673, 690, "Joe Bartolozzi", "Planet Fitness explainer", "memberships", "never showing up", "A gym owner on memberships built on no-shows.", "be the member they lose money on.")]
S.append(sec("d10", "D10 Planet Fitness (your verdict: hated for a reason)", "Two clips per source video at most in the final cut.", "Long reaction",
 [it(w, "right", v, [[a, b]], src, vw, (f"Starts near \"{f}\". End by eye." if "by eye" in l else f"Starts near \"{f}\". Ends near \"{l}\"."), w, les, note=("End by eye." if "by eye" in l else None)) for (v, a, b, src, vw, f, l, w, les) in d10]))
data = {"title": "Next Shoot: New Clips To Select", "sub": "Clips found for the Next Shoot Outlines, 2026-11-12. Select the ones you want; anything you don't select is out.",
 "port": 11841, "decisions": ["<b>B06 smaller plates:</b> no celebrity on video says it; the Profit First author is the real source.",
  "<b>D15:</b> no Clavicular clip saying one rep in the tank was found; Doucette's stand-in is here.",
  "<b>The nine C reaction clips</b> are already chosen and are not on this page."],
 "sections": S, "reply_title": "NEXT SHOOT CLIP PICKS", "reply_help": "Tap Select on every clip you want. Anything you don't select is out."}
for s in S:
    for i in s["items"]:
        if i.get("note") is None: i.pop("note", None)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips.json")
json.dump(data, open(out, "w"), indent=1)
print("items", sum(len(s["items"]) for s in S))
