# 44:38 to 52:00  Over $10,000 a month (meal prep or chef, maid and laundry), real ballers (human trainer and
# nutritionist), beyond the list (red light, peptides, Bryan Johnson), summary. The closing call to action (52:00 on) is
# NOT planned here: the lead editor builds it with the approved app demo.
#
# NEEDS A PICTURE:
#   45:04 to 45:15 "I have a meal prep service called Clean Eats, great meal prep service right here in Austin": his real
#     Clean Eats meals (the containers in his fridge, or the delivery bag). Cg03 covers it with a library stock clip of a
#     man unpacking a meal delivery bag; a real shot of his own order would replace it.
#   49:07 to 49:10 "expensive red light therapy machines": no red light panel in the library, and the Pexels index for
#     "red light therapy" has nothing usable (flowers, a facial, a DJ booth). He stays on camera; Gg15 names it.
#   49:21 to 49:27 "spending thousands per month on supplements and peptides": Cg15 is a stock pill organizer. His own
#     supplement shelf would be better if the supplements chapter has not already used it (B0002).
#
# AI IDEAS:
#   46:25 "oh I got such a busy schedule, I'm a lawyer Dan, I don't have time to work out": EXCUSE VOICE with the lips
#     synced to his recording. A lawyer in a suit says it to camera in his law office while ironing his own shirt on the
#     desk, a basket of laundry on the law books. Earns a slot: it is a voice, and the picture shows the very point of
#     the section (he has the money, he is doing his own chores).
#   45:28 "You're gonna be eating the regular protein just like the peasants": obviously unreal gag. Medieval peasants in
#     a hut solemnly open black plastic meal prep containers of plain chicken and rice. Earns a slot: a joke line with no
#     literal picture, and the meal prep chapter is otherwise all straight stock.
#
# SPECIAL:
#   49:27 to 49:45 Bryan Johnson (a real named person, "check out Brian Johnson's YouTube channel", "a guy who's
#     dedicated to this idea of living forever"). No picture chosen. Gg16 is a text-only lower third with his name spelled
#     "Bryan Johnson" (the ASR writes "Brian"): keep, restyle or cut it, and decide whether his channel is shown. He is
#     named again at 50:10, 51:37 and 51:55 with nothing on screen.
#   45:06 Clean Eats is a real Austin business he names: no logo or site was used.
#   Caption fixes seen in the words: 46:45 "laundry service made" is "maid"; 47:44 "from a video loan" is "video alone".
#   Section labels: he does not number the over $10,000 items (first thing, next thing, next thing, final thing), so
#     Gg01 and Gg06 carry the topic OVER $10,000 A MONTH with no "N OF 4". Match it to the home gym part if that numbers.
#   Summary: one fresh clip only (Cg16, an older man running on a beach). The other recap lines stay on Dan with lower
#     thirds so no picture from an earlier chapter repeats.
PART = [
 # ---- 44:38 Over $10,000 a month: a meal prep service or a personal chef
 dict(id="Cg01", kind="clip", start="A meal prep service or", end="a personal chef", tail=0.55,
      src=["B0018@1.0", stock("pexels-39877491-chef-preparing-ingredient-in-modern-kitchen.mp4", 0.3)], **OTHER,
      note="two shots on the two things he names. Library stock: a prep line scooping food into rows of takeout containers (meal prep service). Pexels stock (new): a chef in a striped apron tastes from a pot (personal chef)"),
 dict(id="Gg01", kind="lt", start="A meal prep service or", end="a personal chef", tail=0.6, topic="OVER $10,000 A MONTH",
      point="A Meal Prep Service Or A Personal Chef", parts=[["A Meal Prep Service", "A meal prep service or"], ["Or A Personal Chef", "even better, a personal chef"]]),
 dict(id="Cg02", kind="clip", start="if you're spending time on cooking", end="then you're wasting your time", tail=0.1, src=["B0312@5.1"], **OTHER,
      note="library stock, never used before: a home cook at the stove cracks eggs into a frying pan, from the second egg on so the hands are in frame (spending time on cooking)"),
 dict(id="Gg02", kind="lt", start="having someone else do that", end="doing higher value work", tail=0.5, topic="KEY POINT",
      point="Pay Someone To Cook. Your Time Is Worth More.", parts=[["Pay Someone To Cook.", "having someone else do that"], ["Your Time Is Worth More.", "while you focus on your"]]),
 dict(id="Cg03", kind="clip", start="meal prep service called Clean", end="worth of meals that I eat", tail=0.1, src=["B0503@0.5"], **OTHER,
      note="library stock: a man unpacks a meal delivery bag on his kitchen counter and lifts out the boxes (his week of delivered meals). See NEEDS A PICTURE: his real Clean Eats order would replace it"),
 dict(id="Gg03", kind="lt", start="about $120 per week", end="if I'm buying chicken", topic="MEAL PREP SERVICE",
      point="$120 A Week. Cooking It Costs $80 To $120.", parts=[["$120 A Week.", "about $120 per week"], ["Cooking It Costs $80 To $120.", "between 80 and $120"]]),
 dict(id="Cg04", kind="clip", start="It's professional chefs making this", end="300 to 500 calories", tail=0.1, src=["B0019@2.0", "B0062@0.0"], **OTHER,
      note="two library stock shots: gloved hands fork salad into a takeout box (professional chefs making this stuff), then hands portion chicken and vegetables into a row of meal prep containers (portioned out)"),
 dict(id="Gg04", kind="lt", start="It's portioned out, so each", end="to track your calories", tail=0.4, topic="KEY POINT",
      point="Portioned Meals Make Calories Easy To Track.", parts=[["Portioned Meals", "It's portioned out, so each"], ["Make Calories Easy To Track.", "far easier and more accurate"]]),
 dict(id="Cg05", kind="clip", start="Now for me, I am", end="I like the premium proteins", tail=0.1, src=["B0469@0.5", "B0441@0.5"], **DAN,
      note="Dan's own kitchen B-roll (8/3 shoot), never used before: he slices a cucumber on the board, then seals glass meal containers in purple gloves (he still cooks every other week)"),
 dict(id="Cg06", kind="clip", start="the guys I know who are", end="with premium protein", tail=0.1,
      src=[stock("pexels-8627105-bald-man-preparing-food.mp4", 1.0), stock("pexels-4064770-a-person-frying-a-chicken-meat.mp4", 2.0)], **OTHER,
      note="Pexels stock (new), two shots: a chef in whites works at his board, then chicken breasts are turned in a pan (a full-time personal chef making food with premium protein)"),
 dict(id="Gg05", kind="lt", start="They got a full -time", end="eating healthy easy", tail=0.5, topic="KEY POINT",
      point="A Full Time Chef Makes Eating Healthy Easy.", parts=[["A Full Time Chef", "They got a full -time"], ["Makes Eating Healthy Easy.", "That is how you make"]]),
 # ---- 46:15 Over $10,000 a month: a maid and a laundry service
 dict(id="Cg07", kind="clip", start="someone to take care of other", end="you need for working out", tail=0.1,
      src=[stock("pexels-6195525-people-in-overalls-cleaning-dining-area.mp4", 3.5)], **OTHER,
      note="Pexels stock (new): a cleaner in red overalls mops the floor of a bright home while a second cleaner works behind her"),
 dict(id="Gg06", kind="lt", start="someone to take care of other", end="you need for working out", tail=0.5, topic="OVER $10,000 A MONTH",
      point="A Maid And A Laundry Service", parts=[["A Maid And A Laundry Service", "someone to take care of other"]]),
 # round 2 (Dan, 2026-10-11): "Just eliminate the lawyer who has no time clip altogether." A4 removed; he stays on camera.
 dict(id="Cg08", kind="clip", start="yet they don't have a maid", end="their house for themselves", tail=0.1,
      src=[stock("pexels-7640950-a-man-washing-the-dishes-while-talking-to-his-wife.mp4", 2.0), stock("pexels-6961718-a-person-folding-denim-jeans.mp4", 0.5)], **OTHER,
      note="Pexels stock (new), two shots of doing it yourself: a man washes the dishes at his kitchen sink, then hands fold jeans onto a stack. The lawyer voice just before it stays on camera"),
 dict(id="Gg07", kind="lt", start="If you're rich, you shouldn't", end="the time to work out", tail=0.5, topic="KEY POINT",
      point="No Time To Work Out? Stop Doing Chores.", parts=[["No Time To Work Out? Stop Doing Chores.", "If you're rich, you shouldn't"]]),
 dict(id="Cg09", kind="clip", start="a month laundry service made", end="made no more laundry", tail=0.1,
      src=[stock("pexels-8756696-workers-working-in-a-laundry-facility.mp4", 4.5)], **OTHER,
      note="Pexels stock (new): a worker at a commercial laundry pulls linen out of a cart beside the big washers (laundry service)"),
 dict(id="Cg10", kind="clip", start="if you got the money invest", end="extra time into working out", tail=0.1, src=["B0450@0.3"], **DAN,
      note="Dan's own B-roll (8/28 shoot), never used before: standing dumbbell lateral raises by the pool, front-on, from the first rep (invest that extra time into working out)"),
 # ---- 46:54 Real ballers: a human personal trainer and nutritionist
 dict(id="Cg11", kind="clip", start="personal trainer and a nutritionist", end="human personal trainer or nutritionist", tail=0.1,
      src=[stock("pexels-6892966-a-man-doing-a-biceps-workout-while-being-supervised-by-his-instructor.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a trainer stands at an older man's shoulder and watches his dumbbell curls"),
 dict(id="Gg08", kind="lt", start="personal trainer and a nutritionist", end="human personal trainer or nutritionist", tail=0.8, topic="REAL BALLERS",
      point="A Human Personal Trainer And Nutritionist", parts=[["A Human Personal Trainer And Nutritionist", "personal trainer and a nutritionist"]]),
 dict(id="Gg09", kind="lt", start="you shouldn't be buying a personal", end="on this list so far", tail=0.4, topic="KEY POINT",
      point="Buy It Last. Lowest Return On The List.", parts=[["Buy It Last.", "you shouldn't be buying a personal"], ["Lowest Return On The List.", "the lowest return on investment"]]),
 dict(id="Gg10", kind="lt", start="Number one, talking to a human", end="those details of form", tail=0.8, topic="REASON 1 OF 2",
      point="Accountability And In Person Form Coaching", parts=[["Accountability", "Number one, talking to a human"], ["And In Person Form Coaching", "having someone to show you"]]),
 dict(id="Cg12", kind="clip", start="And working out with somebody", end="from a video loan", tail=0.1,
      src=[stock("pexels-3209241-a-man-assisting-a-woman-in-using-the-flat-pulldown-weights-equipment-in-a-gym.mp4", 1.0), stock("pexels-12188782-man-exercising-with-personal-trainer.mp4", 2.0)], **OTHER,
      note="Pexels stock (new), two shots: a trainer stands over a client and guides her pulldown (working out with somebody every workout), then another trainer steadies a client's elbow through an overhead extension (those details of form)"),
 dict(id="Cg13", kind="clip", start="somebody in that top 1", end="workout and nutrition program", tail=0.1,
      src=[stock("pexels-5449996-woman-using-digital-tablet.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a nutritionist in a white coat writes a plan on a tablet behind a table of vegetables (a customized nutrition program)"),
 dict(id="Gg11", kind="lt", start="somebody in that top 1", end="what AI can do", tail=0.5, topic="REASON 2 OF 2",
      point="The Top 1% Can Build A Better Plan Than AI.", parts=[["The Top 1%", "somebody in that top 1"], ["Can Build A Better Plan Than AI.", "could build you a customized"]]),
 dict(id="Gg12", kind="lt", start="if you're paying 200, 300", end="someone who's truly elite", tail=0.6, topic="KEY POINT",
      point="$200 To $400 An Hour Buys Someone Elite.", parts=[["$200 To $400 An Hour", "if you're paying 200, 300"], ["Buys Someone Elite.", "you're getting someone who's"]]),
 # ---- 48:21 Beyond the list: red light, peptides and Bryan Johnson
 dict(id="Gg13", kind="lt", start="guys who are the mega", end="investing as much as you can", tail=0.3, topic="BEYOND THE LIST",
      point="For The Mega Ballers And True Believers", parts=[["For The Mega Ballers", "guys who are the mega"], ["And True Believers", "truly believers in this idea"]]),
 dict(id="Gg14", kind="lt", start="I will have to say that", end="significantly more limited", tail=0.6, topic="KEY POINT",
      point="Past This List, The Evidence Gets Thin.", parts=[["Past This List, The Evidence Gets Thin.", "I will have to say that"]]),
 dict(id="Gg15", kind="lt", start="things like expensive red light", end="that you could buy", tail=0.3, topic="MORE SPECULATIVE",
      point="Red Light Therapy, Peptides, Growth Hormone", parts=[["Red Light Therapy,", "things like expensive red light"], ["Peptides,", "exotic peptides like"], ["Growth Hormone", "growth hormone, things like"]]),
 dict(id="Cg14", kind="clip", start="There are exotic peptides like", end="that you could buy", tail=0.1,
      src=[stock("pexels-8534418-vials-on-the-table.mp4", 0.5)], **NONE,
      note="Pexels stock (new): small glass vials with metal caps on a lab bench under blue light, no labels readable (peptides, growth hormone)"),
 dict(id="Cg15", kind="clip", start="You could be spending thousands", end="which may improve your health", tail=0.1,
      src=[stock("pexels-8581288-a-person-organizing-her-medicine.mp4", 6.0)], **OTHER,
      note="Pexels stock (new): top-down, hands sort piles of pills into a weekly pill organizer (thousands a month on supplements)"),
 dict(id="Gg16", kind="lt", start="check out Brian Johnson's YouTube", end="idea of living forever", tail=0.5, topic="TO GO FURTHER",
      point="Bryan Johnson's YouTube Channel", parts=[["Bryan Johnson's YouTube Channel", "check out Brian Johnson's YouTube"]]),
 dict(id="Gg17", kind="lt", start="just stick to what's on the", end="until you're a mega baller", tail=0.3, topic="KEY POINT",
      point="Handle The Basics Before The Exotic Stuff.", parts=[["Handle The Basics", "just stick to what's on the"], ["Before The Exotic Stuff.", "Don't worry about the exotic"]]),
 # ---- 50:11 Summary: stop being cheap with your health (recap lower thirds on Dan, one fresh clip)
 dict(id="Gg18", kind="lt", start="You are being too cheap", end="is literally killing you", tail=0.6, topic="SUMMARY",
      point="Being CHEAP With Your Health Is Killing You.", parts=[["Being CHEAP With Your Health", "You are being too cheap"], ["Is Killing You.", "is literally killing you"]]),
 dict(id="Gg19", kind="lt", start="Going to the club, going", end="improve your health right away", tail=0.3, topic="RECAP: SACRIFICE",
      point="The Club, The Bar, The Alcohol", parts=[["The Club,", "Going to the club, going"], ["The Bar,", "going to the bar"], ["The Alcohol", "alcohol, all these kind"]]),
 dict(id="Gg20", kind="lt", start="still going on expensive dates", end="on the table to chop", tail=0.5, topic="ALSO ON THE TABLE",
      point="Expensive Dates, Movies And Netflix", parts=[["Expensive Dates,", "still going on expensive dates"], ["Movies", "and the movies"], ["And Netflix", "and Netflix, all that"]]),
 dict(id="Gg21", kind="lt", start="you need a basic home workout", end="on welfare right now", tail=0.3, topic="IF YOU'RE BROKE",
      point="A Basic Home Workout Setup And Healthy Food", parts=[["A Basic Home Workout Setup", "you need a basic home workout"], ["And Healthy Food", "and healthy food"]]),
 dict(id="Gg22", kind="lt", start="You should be investing $500", end="the things on this list", tail=0.5, topic="IF YOU'RE MIDDLE CLASS",
      point="Invest $500 To $1,000 A Month In Your Health.", parts=[["Invest $500 To $1,000 A Month", "You should be investing $500"], ["In Your Health.", "in your health every month"]]),
 dict(id="Gg23", kind="lt", start="Stop saving money, stop putting", end="that money into your health", tail=0.5, topic="KEY POINT",
      point="Your Health Comes Before Your Savings.", parts=[["Your Health Comes Before Your Savings.", "Stop saving money, stop putting"]]),
 dict(id="Gg24", kind="lt", start="a home gym, a maid service", end="you can make in your health", tail=0.3, topic="OVER $10,000 A MONTH",
      point="Home Gym, Maid, Meal Prep, Laundry Service", parts=[["Home Gym,", "a home gym, a maid service"], ["Maid,", "a maid service"], ["Meal Prep,", "a meal prep service"], ["Laundry Service", "a laundry service, these"]]),
 dict(id="Gg25", kind="lt", start="a personal trainer, a nutritionist", end="really help a lot too", tail=0.3, topic="MEGA BALLERS",
      point="A Personal Trainer And A Nutritionist", parts=[["A Personal Trainer", "a personal trainer, a nutritionist"], ["And A Nutritionist", "a nutritionist, or Brian"]]),
 dict(id="Gg26", kind="lt", start="Remember, money doesn't do you", end="as long as possible", tail=0.3, topic="KEY POINT",
      point="Spend Your Money On Living Longer.", parts=[["Spend Your Money On Living Longer.", "Remember, money doesn't do you"]]),
 dict(id="Cg16", kind="clip", start="If you have millions, you", end="as long as possible", tail=0.1,
      src=[stock("pexels-8637373-elderly-man-running-on-the-shore.mp4", 9.0)], **OTHER,
      note="Pexels stock (new), the one fresh clip of the summary: a grey-haired man in running kit runs barefoot along the shoreline (prolong your life as long as possible)"),
]
