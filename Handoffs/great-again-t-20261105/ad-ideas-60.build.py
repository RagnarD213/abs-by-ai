#!/usr/bin/env python3
"""Builds the Great Again T ad ideas page (static HTML) from the idea data below."""
import html, sys, re

OUT = sys.argv[1]

CTA_QUIZ = "Tap the link, answer four quick questions, and the free video shows you the rest of the swaps."
CTA_VIDEO = "Tap the link and watch the free video. It covers the rest of the swaps and the nutrients behind them."
CTA_OFFER = "Tap the link and claim your free first month. Just cover shipping."
WHO = "Daniel Rose, founder of SixPackAbs.com. His channel helped over 4.4 million men. Show the photo from right before 40, then the abs he has now."

SRC = {
    "vshred": "V Shred",
    "testogreens": "TestoGreens",
    "nugenix": "Nugenix",
    "testreload": "Test Reload",
    "menerals": "Menerals",
}

def I(title, src, model, meta, beats, top=False, needs=None):
    return dict(title=title, src=src, model=model, meta=meta, beats=beats, top=top, needs=needs)

LONG = [
 dict(name="Testosterone-killing foods",
      proof="The most proven idea in the category. TestoGreens ($1.79M in the last 30 days) and V Shred (about $6.2M lifetime on Test Boost Max) both open on foods. Your VSL opens on foods too, so these ads hand off to it cleanly.",
      ideas=[
  I("Eat More Of This, Less Of This", ["vshred"],
    "V Shred’s food-hook quiz ads (one creative at $658K lifetime, another live for 149 days), laid out as the “do this, not that” table Healthy Back Institute uses. Same opening as your VSL, so the ad and the page match.",
    "Dan at the food table · Quiz, then the free video",
    [("Hook", "“If you want more testosterone, eat more of this, and less of this.” Dan points from egg whites to whole eggs, butter to olive oil, chicken breast to steak. Three swaps in ten seconds."),
     ("Promise", "Every swap is backed by a study, and he’ll prove one right now."),
     ("Proof", "The egg study. 30 men, 12 weeks, three whole eggs against six egg whites after every workout. The whole egg group got the bigger rise in testosterone, more strength and less body fat."),
     ("Not your fault", "For years guys were told to throw out the yolk. After 40, testosterone drops about 1% a year, and diet food speeds it up."),
     ("Who’s talking", WHO),
     ("Tease", "There are more swaps like this, including one diet food most guys eat every day."),
     ("CTA", CTA_QUIZ)], top=True),
  I("3 “Healthy” Foods That Are Killing Your Testosterone", ["vshred", "testogreens"],
    "The first line of V Shred’s VSL: “Are healthy foods destroying your testosterone?” TestoGreens opens the same way: the foods men think help their T are draining it.",
    "Dan at the food table · Quiz, then the free video",
    [("Hook", "“Are the healthy foods in your fridge killing your testosterone?” Egg whites, a protein bar and a dry chicken breast sit on the table. A red X lands on each."),
     ("Agitate", "These are the foods a guy eats when he’s trying to lose his gut. Build your diet around them and your testosterone pays for it."),
     ("Proof", "Pay off one in full. Very high-protein, low-carb diets: 27 studies, 309 men, a large drop in testosterone."),
     ("Not your fault", "“You’re not losing your edge because you stopped trying.” You followed the advice. The advice was wrong for men over 40."),
     ("Flip", "For every food that lowers testosterone, another does the opposite. Show the three swaps side by side, fast."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("The 1 “Diet” Food Killing Your Testosterone", ["vshred"],
    "V Shred’s VSL headline: “1 ‘Everyday’ Food Killing Your Testosterone.” It names one food, gives it about a minute, then pivots.",
    "Dan to camera with one prop · Quiz, then the free video",
    [("Hook", "Dan holds up a protein bar. “This is in almost every guy’s gym bag. And it could be crushing your testosterone.”"),
     ("Open loop", "It isn’t sugar. It isn’t beer. It’s the food you eat because you think it’s the healthy choice."),
     ("Reveal", "Protein bars and shakes in place of real carbs. In one study the same men had 26% higher testosterone on a high-carb diet than on a high-protein, low-carb one."),
     ("Swap", "Put the potato back on your plate, right next to the steak."),
     ("Bigger point", "“Most guys would never guess that.” A lot of what you’ve been told about healthy eating is flat out wrong for your testosterone."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)], top=True),
  I("Stop Throwing Out The Yolk", ["vshred"],
    "V Shred runs single-food versions of its quiz ad. “Eggs” is one of the creative names in VidTao.",
    "Dan in a kitchen · Quiz, then the free video",
    [("Hook", "Dan cracks an egg and starts to dump the yolk in the trash. He stops. “If you’re over 40, this is costing you testosterone.”"),
     ("Proof", "30 men, 12 weeks. Three whole eggs beat six egg whites for testosterone, strength and fat loss. Same protein."),
     ("Why", "The yolk is where the fat and the nutrients are. Throw it out and you throw out what your body uses to make testosterone."),
     ("Agitate", "Years of egg-white omelets, and the belly still grows a little every year."),
     ("Zoom out", "Eggs are one swap. There are more, and one of them will surprise you."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("The “Healthy” Breakfast That’s Lowering Your Testosterone", ["vshred"],
    "V Shred’s opening lines: foods in your fridge, your pantry, “maybe even in that clean smoothie you made this morning.”",
    "Dan with two breakfast plates · Quiz, then the free video",
    [("Hook", "Two breakfasts. Left: an egg-white omelet and a protein shake. Right: whole eggs and potatoes. “One of these is lowering your testosterone. It’s the one you think is healthy.”"),
     ("Proof 1", "Whole eggs beat egg whites for testosterone in a 12-week study of men who lift."),
     ("Proof 2", "The same men had 26% higher testosterone eating high carb than eating high protein, low carb."),
     ("Not your fault", "Every diet out there tells you to eat the plate on the left."),
     ("What it costs", "The belly that grows every year. The crash at two in the afternoon. The drive that isn’t what it was."),
     ("Tease", "That’s one meal. The free video covers what to cook with, which meat to buy and the nutrients behind all of it."),
     ("CTA", CTA_QUIZ)]),
  I("Stop Cooking With This", ["testogreens"],
    "TestoGreens’ top ad (3:43) ends on one instruction the viewer can act on tonight: “Get canola oil out of your kitchen immediately.”",
    "Dan walking through a kitchen · Quiz, then the free video",
    [("Hook", "Dan takes the butter out of the fridge. “If you’re a man over 40, stop cooking with this. Start cooking with this.” Extra virgin olive oil."),
     ("Proof", "60 men switched from butter to extra virgin olive oil. Three weeks later their testosterone was up about 17%. Same calories, same weight."),
     ("Kitchen clean-out", "He keeps going through the fridge and pantry. Egg whites, protein bars and dry chicken breast go in a box. Whole eggs, steak and potatoes stay."),
     ("Why now", "After 40 you lose about 1% of your testosterone a year. What’s in your kitchen can speed that up or fight it."),
     ("Who’s talking", WHO),
     ("Do this tonight", "Cook dinner in olive oil."),
     ("CTA", CTA_QUIZ)]),
  I("Your Low-Fat Diet Is Lowering Your Testosterone", ["vshred"],
    "V Shred’s “healthy foods” opening plus its reframe at 2:03: the rules changed and nobody told you.",
    "Dan at the food table · Quiz, then the free video",
    [("Hook", "Low-fat yogurt, skim milk and fat-free dressing on the table. “You bought these to lose your gut. They’re lowering your testosterone.”"),
     ("Proof", "When researchers pooled the diet studies, men on low-fat diets had lower testosterone than men eating more fat."),
     ("Why", "Fat is where the nutrients are that your body uses to make testosterone. Cut the fat and you cut the supply."),
     ("Not your fault", "Low-fat was the advice for thirty years. Just eating less fat doesn’t work for men our age."),
     ("Swaps", "Whole eggs, steak, olive oil."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("The Real Reason Oysters Work", ["menerals"],
    "The nutrient idea from your VSL (“the most important thing I want to teach you”), in the shape Menerals used for its “3 missing minerals” ads (about $1M lifetime).",
    "Dan at the food table · Quiz, then the free video",
    [("Hook", "A plate of oysters. “You’ve heard oysters are good for a man’s drive. It’s true. But there’s nothing magic about an oyster.”"),
     ("Reveal", "It’s the zinc. Your body cannot make testosterone without it."),
     ("Proof", "Scientists cut the zinc in healthy young men’s diets. In 20 weeks their testosterone crashed 73%."),
     ("Swap", "Ounce for ounce, sirloin steak has five times the zinc of chicken breast. Crab and pumpkin seeds work too."),
     ("Bigger idea", "Once you know the nutrients, you can pick the foods yourself. The next one is boron, and most guys have never heard of it."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("Answer These 4 Questions", ["vshred"],
    "V Shred’s quiz ads. Its quiz page took about $2.2M and is the version still running. “Take the quiz” is the call to action.",
    "Dan to camera, YES and NO buttons on screen · Quiz",
    [("Hook", "“Four questions. If you answer yes to even one, you need to see what’s on the next page.”"),
     ("Questions", "Your four quiz questions, read to camera, with a beat after each. A YES button lights up every time."),
     ("Pivot", "“If you said yes, here’s the first thing to change.”"),
     ("Proof", "One swap: less chicken breast, more steak. Five times the zinc, and your body can’t make testosterone without zinc."),
     ("Who’s talking", WHO),
     ("CTA", "Tap the link, answer them for real, and the video starts.")]),
 ]),
 dict(name="The transformation story",
      proof="TestoGreens’ top ad is a story about one man: “Your dad was fat, now he’s jacked. What did he change?” The strongest stretch of its VSL is the presenter’s own before and after, with real numbers. You have the real photos.",
      ideas=[
  I("“You Had A Gut At 39. What Did You Change?”", ["testogreens"],
    "TestoGreens’ top ad: “Your dad was fat, now he’s jacked. What did he change?” “He stopped eating the feminizing foods.” 3:43, one man’s story, ending on a kitchen tip.",
    "Dan plus a friend’s voice off camera · Quiz, then the free video",
    [("Hook", "The photo of Dan at 39, soft and puffy. A friend’s voice: “You had a gut at 39. Now you’ve got abs at 41. What did you change?” Dan: “I stopped eating the foods that lower testosterone.”"),
     ("The story", "Abs in his twenties. Then a flabby belly and man boobs right before 40. Same workouts. Eating “healthy.”"),
     ("The turn", "The fitness experts he worked with at SixPackAbs.com told him what it was: age-related testosterone decline. The research showed most of it came down to food."),
     ("What he changed", "Two swaps with their studies: whole eggs for egg whites, potatoes for protein shakes."),
     ("Result", "Abs better than he had in his twenties. Energy to work all day. His drive back."),
     ("Do this today", "Keep the yolks."),
     ("CTA", CTA_QUIZ)], top=True),
  I("This Was Me Right Before I Turned 40", ["testogreens"],
    "The origin story in TestoGreens’ VSL (failed an exam, tested at 216, now 931 at 56). The Nov 8 teardown called it the strongest part of either VSL. Yours is told with real photos.",
    "Dan to camera with his photos · Quiz, then the free video",
    [("Hook", "The three fat photos, full screen, shirtless one in the middle. “This was me right before I turned 40.”"),
     ("The twist", "“And I ran a fitness channel that helped over 4.4 million men.”"),
     ("The fall", "Soft, flabby belly. Man boobs. Puffy face. Tired all the time. His business and his love life both suffered."),
     ("He didn’t quit", "Same workouts and same healthy eating as his twenties. They just stopped working."),
     ("Discovery", "Age-related testosterone decline. And most of his problem came down to the foods he was eating."),
     ("After", "The after photos, full screen. “Abs better than I had in my twenties.”"),
     ("CTA", CTA_QUIZ)]),
  I("I Did Everything Right And Still Got Fat After 40", ["testogreens"],
    "TestoGreens: “I was following the playbook perfectly and still falling apart.” Problem hooks open 27% of its ads.",
    "Dan to camera, no props · Quiz, then the free video",
    [("Hook", "“I was working out. I was eating healthy. And I still got fat after 40.”"),
     ("Recognition", "The viewer’s version: the belly a little bigger every year, strength and stamina down, worn out after a normal day."),
     ("It isn’t effort", "Testosterone drops about 1% a year. Same effort, half the result."),
     ("The mistake", "The healthy foods he was eating were lowering his testosterone: egg whites, protein shakes, dry chicken breast."),
     ("Proof", "One study, on screen."),
     ("Result", "His before photo, then his after photo."),
     ("CTA", CTA_QUIZ)]),
  I("My Girlfriend Noticed Before I Did", ["testreload", "testogreens"],
    "Your green park-bench ads were titled “Fix This Hormone (That Helps You Attract Women).” TestoGreens presses the same nerve with wives who notice. The hook is a line from your own script.",
    "Dan to camera · Quiz, then the free video",
    [("Hook", "“My girlfriend noticed the difference before I did.”"),
     ("The honest part", "His drive wasn’t what it used to be. Or he still wanted it and his body was tapped out. “That one is brutal.”"),
     ("You’re not alone", "A lot of guys over 40 live with this every day and never say it out loud."),
     ("Cause", "Testosterone is the hormone that makes you a man, and you lose about 1% of it every year."),
     ("The fix starts with food", "One swap and its study."),
     ("Result", "“The best love life I’ve ever had.”"),
     ("CTA", CTA_QUIZ)]),
 ]),
 dict(name="Two people and a whiteboard",
      proof="Your own best. The Mark and Amy interview is the most-viewed green ad in the Test Reload archive: 1.62 million views, 7:18. A question in the first seconds, the presenter’s credentials at 0:28, the free video offered at 2:38.",
      ideas=[
  I("Which Of These Two Foods Boosts Testosterone?", ["testreload", "vshred"],
    "The Mark and Amy interview (green, 1.62M views), beat for beat, with food boards in place of the molecule boards. The food question is V Shred’s.",
    "Female interviewer plus Dan at a whiteboard · Free video",
    [("Hook", "The interviewer holds up two boards: egg whites and whole eggs. “One of these raises a man’s testosterone. Most men pick the wrong one.”"),
     ("Intro at 0:30", "“This is Daniel Rose, founder of SixPackAbs.com. His channel helped over 4.4 million men.”"),
     ("The exchange", "She guesses egg whites. He walks through the study at the whiteboard."),
     ("Round two", "Protein bar or baked potato? Same surprise."),
     ("Free video at 2:30", "He offers the rest of the swaps and the nutrients behind them."),
     ("Objections", "As in the original: “I’m too old.” “I don’t have time to work out more.” Short answers."),
     ("Close", "Age callout, then the link again.")], top=True),
  I("The Estrogen Molecule", ["testreload"],
    "A straight remake of your number one (green, 1.62M views): two molecule boards, a guessing question, the whiteboard explanation. You called this hook successful but somewhat boring, and the Nov 6 brief parked it. It is still your most-viewed ad.",
    "Female interviewer plus Dan at a whiteboard · Free video",
    [("Hook", "The interviewer holds two molecule boards that look almost the same. “One of these makes you a man. The other is estrogen. Can you tell which?”"),
     ("Intro at 0:30", "Dan’s name, SixPackAbs.com, 4.4 million men."),
     ("Explanation", "The two are a hair apart, and a man’s body turns one into the other. More of it as he ages and his belly grows."),
     ("Tie to the bottle", "Boron. In one study, a week of boron sent free testosterone up and estrogen down."),
     ("Free video at 2:30", "The foods and nutrients that keep testosterone high."),
     ("Objections", "Too old, no time, bad joints. Answered the way the original did."),
     ("Close", "Age callout, then the link again.")], top=True),
  I("“What Makes This Different From Every Other T Booster?”", ["testreload", "testogreens"],
    "The interview format of your top green ad, asking the question TestoGreens answers in its “why other boosters fail” section. Lead B in the Nov 6 creative brief.",
    "Female interviewer plus Dan, bottle in hand · Free first month",
    [("Hook", "The interviewer, skeptical: “There are a hundred testosterone boosters. What makes yours different?”"),
     ("Answer 1", "Tongkat ali. Many boosters have none. Others give you 100 or 200 milligrams. Great Again T has 400."),
     ("Answer 2", "Zinc. Many have none, or 10 to 20 milligrams. Great Again T has 50."),
     ("Answer 3", "14 ingredients, made in the USA in a GMP certified facility."),
     ("Show it", "Two tablets in his palm. Seven seconds a day."),
     ("Her last question", "“What does it cost to try?” The first month is free. Just cover shipping."),
     ("CTA", CTA_OFFER)]),
  I("Fix This Hormone", ["testreload"],
    "Your green park-bench ad with Mark and Brooke (long intro and short intro both green). The videos are private, so this takes only what the sheet shows: the title, a man and a woman on a bench, two intro lengths.",
    "A man and a woman on a bench · Free video",
    [("Hook", "A woman sits down next to a fit man over 40 and asks him a direct question about how he looks."),
     ("His answer", "One hormone. When it’s high, losing belly fat and gaining muscle get easier, and you have the energy and the drive."),
     ("When it’s low", "The belly, the exhaustion, the love life. He lists them plainly."),
     ("Why it falls", "About 1% a year, and the wrong foods push it down faster."),
     ("One swap", "Whole eggs for egg whites, with the study."),
     ("Free video", "The rest of the swaps."),
     ("Film two intros", "One long, one short. Both versions were green.")]),
  I("The Older Spokesman Opens, You Close", ["testreload", "testogreens"],
    "Older men (Mark, and Toby in his 60s) sold almost all of Test Reload. TestoGreens puts a fit older man in its ads and a different voice in its VSL. The Nov 10 funnel plan proposes this exact split.",
    "A fit man of 55 to 65 for the first 45 seconds, then Dan · Quiz, then the free video",
    [("Hook", "A fit man around 60 stands at the food table and does the three swaps. “Eat more of this, less of this.”"),
     ("His one line", "“At my age this matters more, not less.” He says nothing about results from the bottle."),
     ("Handoff", "“Daniel Rose founded SixPackAbs.com. Listen to him.” Cut to Dan."),
     ("Proof", "Dan gives the egg study."),
     ("Dan’s story", "The photo from right before 40, then the abs he has now."),
     ("CTA", CTA_QUIZ),
     ("The test", "Run it against “Eat More Of This, Less Of This” with the same body. One thing changes: the face in the first 45 seconds.")]),
 ]),
 dict(name="Men over 40",
      proof="Every winner names an age. Your green ads did too: the pool ad’s message (671K views), “How Men Over 40 Build Muscle Easily,” and the title of your old VSL.",
      ideas=[
  I("How Men Over 40 Build Muscle Easily", ["testreload"],
    "The title of a green Test Reload ad (the video is private). The body is your quiz question 3: more muscle without working out more.",
    "Dan to camera in a gym · Quiz, then the free video",
    [("Hook", "“If you’re over 40 and the gym stopped working, it’s not your workout.”"),
     ("Problem", "Same effort, half the results. You recover slower. The weights feel heavier."),
     ("Cause", "Testosterone, down about 1% every year."),
     ("Proof", "In the egg study the whole egg group gained more strength. In the tongkat ali trial, men aged 50 to 70 got stronger in 12 weeks."),
     ("Promise", "More muscle without working out any more than you do right now. Fix what you eat first."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("Men Over 40: Fight Aging And Lose Your Belly Fat", ["testreload", "nugenix"],
    "The public title of your old Test Reload VSL and both of its plug versions. Nugenix’s advertorial headline has the same shape: men over 50, their testosterone, their energy back.",
    "Dan to camera · Quiz, then the free video",
    [("Hook", "“Men over 40: if your belly gets a little bigger every year no matter what you do, watch this.”"),
     ("Why the belly", "When testosterone is low, losing belly fat and gaining muscle can feel impossible."),
     ("Stakes", "It’s more than looks. In an analysis of over 16,000 men, the guys with low testosterone were 35% more likely to die during the studies."),
     ("Good news", "Research shows you can raise it with a few simple food swaps."),
     ("One swap", "The potato and the protein shake."),
     ("Dan’s belly", "Before, then after."),
     ("CTA", CTA_QUIZ)]),
  I("Getting Older Doesn’t Mean Giving Up", ["testreload"],
    "Lead A in the Nov 6 creative brief, built on the message of your green pool ad (671K views): you’re not too old and it isn’t your fault. A whiteboard replaces the pool.",
    "Dan at a whiteboard · Quiz, then the free video",
    [("Hook", "The whiteboard says GETTING OLDER. Dan writes GIVING UP under it and crosses it out. “Getting older doesn’t mean you’ve stopped wanting to feel strong and be proud of your body.”"),
     ("The stereotype", "What a man over 40 is supposed to look like. Then Dan at 41."),
     ("Not your fault", "You didn’t get lazy. Your testosterone has been dropping every year."),
     ("What changed for him", "The foods. One swap with its study."),
     ("Hope", "It can be turned around. His before, then his after."),
     ("CTA", CTA_QUIZ)]),
  I("The Scene, The Rewind, The Explanation", ["testreload"],
    "The structure of both green pool ads: a short scene, the presenter interrupts and replays it, then a studio pitch. Pool, car and bikini are out. This scene costs nothing.",
    "A short breakfast scene, then Dan · Free video",
    [("Hook scene, 15 seconds", "A guy in his 40s at breakfast. Egg whites, a protein shake, a sigh, his belt out one more notch."),
     ("Interrupt", "Dan steps in. “Stop. Rewind that.” The scene plays again."),
     ("Commentary", "Freeze on the plate. “See this? This is why.”"),
     ("Contrast", "The tired 45-year-old everyone expects, then Dan at 41."),
     ("Free video early", "The pool ad made its offer at 0:58. Do the same."),
     ("Reassurance", "You’re not too old. You didn’t fail. Nobody told you."),
     ("Close", "Age callout, then the link again.")]),
 ]),
 dict(name="The hidden cause",
      proof="V Shred spends its first two minutes proving the viewer isn’t to blame: the frog study, four fast statistics, cortisol. Then it pivots to the foods that do the opposite.",
      ideas=[
  I("The Frog Study", ["vshred"],
    "V Shred’s shock proof in the first minute of its VSL: a chemical sprayed on the food supply turned male frogs into females. Then the pivot: some foods do the exact opposite.",
    "Dan to camera with the study on screen · Quiz, then the free video",
    [("Hook", "“A chemical sprayed on our food every day turned male frogs into females. They laid eggs.”"),
     ("So what", "It’s in the food and the water, and men’s testosterone has been falling for decades."),
     ("Not your fault", "The deck got stacked against you and nobody told you the rules changed."),
     ("Pivot", "Some things destroy testosterone. Some foods do the exact opposite."),
     ("One swap", "Whole eggs for egg whites, with the study."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)],
    needs="Add the frog paper (Hayes, 2010) to the studies list under the video."),
  I("4 Numbers Every Man Over 40 Should See", ["vshred"],
    "V Shred’s four-stat montage at 6:13: fast, one number per card. Built here from numbers already in your script.",
    "Dan to camera, one number per card · Quiz, then the free video",
    [("Hook", "“Four numbers. If you’re a man over 40, they explain what’s happening to your body.”"),
     ("1%", "The testosterone you lose every year."),
     ("35%", "How much more likely the men with low testosterone were to die, in an analysis of over 16,000 men."),
     ("42%", "The lower risk of type 2 diabetes for men with higher testosterone, across 43 studies."),
     ("26%", "How much higher testosterone was when the same men ate high carb instead of high protein, low carb."),
     ("The turn", "That last number is the one you control. It’s food."),
     ("CTA", CTA_QUIZ)]),
  I("It’s Not Your Fault You Got Soft After 40", ["vshred", "testreload", "nugenix"],
    "V Shred at 2:03: “You’re not losing your edge because you stopped trying.” Your pool ad makes the same promise, and so does Nugenix’s advertorial.",
    "Dan to camera · Quiz, then the free video",
    [("Hook", "“If you got soft after 40, it’s not because you got lazy.”"),
     ("You tried", "You stay active. You eat right. The belly grows anyway."),
     ("Real cause", "Age-related testosterone decline. About 1% a year."),
     ("Second cause", "Diet advice that lowers testosterone: egg whites, low fat, high protein and no carbs."),
     ("The fix is simple", "Food swaps. One, with its study."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("The Stress Hormone That’s Eating Your Testosterone", ["vshred"],
    "Cortisol is V Shred’s main mechanism and the subject of its 0:59 ad. It fits your bottle: tongkat ali cut cortisol 16% and raised testosterone 37% in four weeks.",
    "Dan to camera · Quiz, then the free video",
    [("Hook", "“There’s a hormone that fights your testosterone all day. And the diet you’re on is raising it.”"),
     ("Explain", "Cortisol and testosterone work against each other. When one goes up, the other goes down."),
     ("The food link", "On the high-protein, low-carb diet, the men’s cortisol was higher and their testosterone was lower."),
     ("The root", "Tongkat ali. In a four-week study it cut cortisol 16% and raised testosterone 37%."),
     ("What it feels like", "Tired, wired, a belly that won’t move."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)]),
  I("Your Doctor Says Your Testosterone Is “Normal”", ["testogreens", "vshred"],
    "An objection TestoGreens answers in its FAQ (“today’s normal range wasn’t normal a generation ago”). V Shred makes the same point in its stats. Question hooks open 32% of TestoGreens’ ads.",
    "Dan to camera · Quiz, then the free video",
    [("Hook", "“Did your doctor tell you your testosterone is normal? Normal for who?”"),
     ("The claim", "What counts as normal today would have been flagged as low a generation ago."),
     ("Recognition", "You can be normal on paper and still have the belly, the two o’clock crash and no drive."),
     ("Before anything drastic", "Start with what you eat."),
     ("One swap", "Steak for chicken breast. Five times the zinc."),
     ("Who’s talking", WHO),
     ("CTA", CTA_QUIZ)],
    needs="Find a study for the generational drop. Both competitors say it without one on screen."),
 ]),
 dict(name="The enemy",
      proof="TestoGreens sells against two things: TRT (“$600 to $1,000 a month”) and boosters that don’t work. Both set up what is in your bottle.",
      ideas=[
  I("Thinking About TRT? Watch This First.", ["testogreens"],
    "TestoGreens makes TRT its price anchor and answers “should I just go on TRT?” on camera. Your script’s version of the line: no needles, no prescription, no doctor’s waiting room.",
    "Dan to camera, bottle in hand · Free first month",
    [("Hook", "“Thinking about testosterone shots? Before you do, try this for 30 days.”"),
     ("What the needle costs", "Hundreds of dollars a month, the appointments, and it’s for life."),
     ("The step most guys skip", "Food. One swap with its study."),
     ("Then the roots", "Tongkat ali raised testosterone in men aged 50 to 70 who were low, in a 12-week trial."),
     ("Great Again T", "No needles. No prescription. Two tablets a day."),
     ("The offer", "Your first month is free. Just cover shipping."),
     ("CTA", CTA_OFFER)]),
  I("Why Most Testosterone Boosters Don’t Work", ["testogreens"],
    "TestoGreens’ “why other boosters fail” section, shot as the store-shelf scene already in your script: wrong ingredients, low doses, sketchy manufacturing.",
    "Dan with other brands’ bottles · Free first month",
    [("Hook", "Dan turns a generic booster over to the label. “Flip your testosterone booster over. I’ll show you why it isn’t working.”"),
     ("Problem 1", "No tongkat ali at all, or a token 100 to 200 milligrams."),
     ("Problem 2", "No zinc, or 10 to 20 milligrams."),
     ("Problem 3", "One or two ingredients, made overseas with no quality control."),
     ("So he made his own", "Great Again T: 400 milligrams of tongkat ali, 50 of zinc, 14 ingredients, made in the USA."),
     ("The offer", "Your first month is free. Just cover shipping."),
     ("CTA", CTA_OFFER)]),
  I("3 Roots Men Have Used For Centuries", ["vshred", "testogreens"],
    "V Shred’s “three pillars” ingredient section and TestoGreens’ line that the answer “isn’t found in a pharmacy, it’s found in nature.” These are the three roots in your script.",
    "Dan with the three roots on the table · Free first month",
    [("Hook", "Three roots on the table. “Men have used these three roots for centuries. You won’t find them in any grocery store.”"),
     ("Tongkat ali", "The king. 76 men with low testosterone took it for a month. At the start 35% had normal levels. After, over 90% did."),
     ("Panax ginseng", "In Chinese it means “man root.” Across six trials and 349 men, the men taking it were more than twice as likely to see their performance improve."),
     ("Maca", "Grown over 13,000 feet up in the Andes. In a 12-week trial it raised men’s desire."),
     ("The problem", "You can’t get these from regular food, and most supplements skimp on them."),
     ("Great Again T", "All three, with a full 400 milligrams of tongkat ali."),
     ("CTA", CTA_OFFER)]),
 ]),
]

SHORT = [
 dict(name="One food swap per ad",
      proof="V Shred’s quiz ads are single-food hooks. The creative names in VidTao include testokillingfoods, bread and eggs, and one has run 149 days. One food, one study, one tap.",
      ideas=[
  I("Stop Eating Egg Whites", ["vshred"],
    "V Shred’s single-food quiz ads. “Eggs” is one of its creative names.",
    "Dan at the food table · Quiz",
    [("Hook, first 3 seconds", "Dan holds up the egg-white carton. “If you’re a man over 40, stop eating these.”"),
     ("Swap", "He slides the whole eggs forward. “Eat these.”"),
     ("Proof on screen", "30 men, 12 weeks. Whole eggs beat egg whites for testosterone, strength and fat loss."),
     ("Why", "The yolk carries what your body uses to make testosterone."),
     ("CTA", CTA_QUIZ)], top=True),
  I("Put The Potato Back On Your Plate", ["vshred"],
    "V Shred’s “1 everyday food” idea at short length. This is the swap you called counterintuitive in the script contest.",
    "Dan with a protein bar and a baked potato · Quiz",
    [("Hook", "Protein bar in one hand, baked potato in the other. “One of these lowers your testosterone. It’s not the potato.”"),
     ("Proof on screen", "Same men, two diets, ten days each. Testosterone was 26% higher on high carb."),
     ("The twist", "The diet you went on to lose your gut is taking your testosterone down with it."),
     ("Swap", "Potato on the plate, right next to the steak."),
     ("CTA", CTA_QUIZ)]),
  I("Less Of This Meat, More Of This Meat", ["vshred"],
    "V Shred’s food-hook quiz ads. This is the third swap in your VSL’s first ten seconds.",
    "Dan at the food table · Quiz",
    [("Hook", "A dry chicken breast and a steak. “Eat less of this meat, and more of this meat.”"),
     ("Proof on screen", "Sirloin steak: five times the zinc of chicken breast."),
     ("Why zinc", "Your body can’t make testosterone without it. Cut zinc and testosterone crashed 73% in 20 weeks."),
     ("Tease", "That’s one swap. The others are just as easy."),
     ("CTA", CTA_QUIZ)]),
  I("Stop Cooking With This", ["testogreens"],
    "TestoGreens’ kitchen instruction (“get canola oil out of your kitchen”) at short length.",
    "Dan at a stove · Quiz",
    [("Hook", "A stick of butter over a hot pan. “Stop cooking with this.”"),
     ("Swap", "“Start cooking with this.” Extra virgin olive oil."),
     ("Proof on screen", "60 men made the switch. Three weeks later, testosterone was up about 17%."),
     ("Do it tonight", "Same dinner, different oil."),
     ("CTA", CTA_QUIZ)]),
  I("3 Swaps, 10 Seconds", ["vshred"],
    "V Shred’s quiz ads run on curiosity, with no explanation. This is your VSL’s opening cut as its own ad.",
    "Dan at the food table · Quiz",
    [("Hook", "“If you want more testosterone, eat more of this, and less of this.” All three swaps, no explanation."),
     ("One line of proof", "“Every one of these is backed by a study.”"),
     ("Who’s talking", "On-screen text only: Daniel Rose, SixPackAbs.com, 4.4 million men."),
     ("Open loop", "“I’ll show you why in a free video.”"),
     ("CTA", CTA_QUIZ)], top=True),
  I("Low-Fat Is Lowering Your T", ["vshred"],
    "V Shred’s “healthy foods” opening at short length.",
    "Dan at the food table · Quiz",
    [("Hook", "Low-fat yogurt in his hand. “You bought this to lose your gut. It’s lowering your testosterone.”"),
     ("Proof on screen", "Pooled diet studies: men on low-fat diets had lower testosterone."),
     ("Why", "Cut the fat and you cut what your body makes testosterone from."),
     ("Swap", "Whole eggs, steak, olive oil."),
     ("CTA", CTA_QUIZ)]),
  I("You Don’t Need Oysters", ["menerals"],
    "The nutrient idea from your VSL, in the Menerals mineral-ad shape.",
    "Dan at the food table · Quiz",
    [("Hook", "A plate of oysters. “Everybody says oysters boost testosterone. You don’t need them.”"),
     ("Reveal", "It’s the zinc."),
     ("Swap", "Steak, crab and pumpkin seeds are loaded with it too."),
     ("Proof on screen", "Cut zinc, and testosterone fell 73% in 20 weeks."),
     ("CTA", CTA_QUIZ)]),
  I("Left Or Right?", ["vshred"],
    "V Shred’s ads are quiz-style: the viewer answers before the reveal.",
    "Two plates and a countdown · Quiz",
    [("Hook", "Two plates. “Which one raises your testosterone? You’ve got three seconds.” A countdown on screen."),
     ("Reveal", "The one most guys get wrong: the whole eggs, or the potato."),
     ("Proof on screen", "One line from the study."),
     ("Tease", "There are more of these, and most men miss them."),
     ("CTA", CTA_QUIZ)]),
 ]),
 dict(name="The quiz question",
      proof="V Shred’s surviving funnel starts with easy yes questions. The ad asks one of them, and the page asks the rest.",
      ideas=[
  I("Would You Eat Them?", ["vshred"],
    "V Shred’s second quiz question, almost word for word: if certain foods would raise your testosterone, would you add them?",
    "Dan to camera, YES and NO buttons on screen · Quiz",
    [("Hook", "“If there were foods that naturally boost your testosterone, would you eat them?”"),
     ("The surprise", "“What if they were steak, whole eggs and potatoes?”"),
     ("One line of proof", "Studies back every one of them."),
     ("Who’s talking", "On-screen text only: Daniel Rose, SixPackAbs.com."),
     ("CTA", "Tap YES. Three more questions, then the free video.")], top=True),
  I("4 Questions, 30 Seconds", ["vshred"],
    "V Shred’s quiz ad, with your four questions.",
    "Dan to camera, questions on screen · Quiz",
    [("Hook", "“Men over 40: four questions, thirty seconds.”"),
     ("Questions", "All four, fast, on screen as he reads them."),
     ("The line", "“If you said yes to even one, you need to see this.”"),
     ("Promise", "The foods that naturally raise your testosterone, with the studies."),
     ("CTA", "Tap the link and answer them for real.")]),
  I("3 Signs Your Testosterone Is Dropping", ["vshred", "testogreens"],
    "The symptom lists in both VSLs: V Shred’s snooze button and 2 p.m. crash, TestoGreens’ “telltale signs.” Problem hooks open 27% of TestoGreens’ ads.",
    "Dan to camera · Quiz",
    [("Hook", "“Three signs your testosterone is dropping.”"),
     ("The signs", "Your belly gets a little bigger every year. You crash at two in the afternoon. Your drive isn’t what it used to be."),
     ("Why", "After 40 you lose about 1% a year."),
     ("Good news", "You can push it back up with food."),
     ("CTA", CTA_QUIZ)]),
 ]),
 dict(name="Reverse psychology",
      proof="V Shred’s live 0:59 ad opens backwards: “If you want to stay overweight, ignore cortisol.” Then the mechanism, then a free video with “no email needed.”",
      ideas=[
  I("If You Want Low Testosterone, Keep Eating Egg Whites", ["vshred"],
    "V Shred’s reverse hook, with the food from your VSL.",
    "Dan to camera · Quiz",
    [("Hook", "“If you want low testosterone, keep eating egg whites.”"),
     ("Proof on screen", "Whole eggs beat egg whites for testosterone in a 12-week study."),
     ("Turn", "“If you want it higher, eat the whole egg.”"),
     ("Tease", "That’s one swap out of several."),
     ("CTA", "Free video. No email needed.")]),
  I("How To Keep Your Gut After 40", ["vshred"],
    "V Shred’s reverse hook, as a list.",
    "Dan to camera · Quiz",
    [("Hook", "“Want to keep your gut after 40? Here’s how.”"),
     ("The list", "Throw out the yolks. Trade your potatoes for protein bars. Eat dry chicken breast every night."),
     ("Punchline", "“Do that, and your testosterone stays right where it is. Low.”"),
     ("Turn", "“Or do the opposite.”"),
     ("CTA", "Free video. No email needed.")]),
  I("If You Want To Stay Tired, Ignore Cortisol", ["vshred"],
    "The closest to V Shred’s actual 0:59 ad: reverse hook, the cortisol story, a free-video call to action.",
    "Dan to camera · Quiz",
    [("Hook", "“If you want to stay tired and soft after 40, ignore cortisol.”"),
     ("Explain", "Cortisol is your stress hormone, and it fights your testosterone. One goes up, the other goes down."),
     ("Proof on screen", "Tongkat ali, four weeks: cortisol down 16%, testosterone up 37%."),
     ("Tease", "The foods and the roots that bring it down are in a free video."),
     ("CTA", "Free video. No email needed.")], top=True),
 ]),
 dict(name="Two men talking",
      proof="Nugenix’s top YouTube ad (“SCHOOL,” $148K, 1:01) is two men trading lines. Your own archive says the face matters: older men sold almost all of Test Reload.",
      ideas=[
  I("“I Lost My Drive After 40”", ["nugenix"],
    "Nugenix “SCHOOL”: a misheard word (“I lost my driver” / “I lost my drive”), “most guys at 40 lose more than a golf game,” “what’d you do?”, the bottle, a free one.",
    "Dan plus a second man · Free first month",
    [("Hook", "Two guys at the gym. A misheard word turns into “I lost my drive and energy after I turned 40.” Write a new joke. Theirs is the golf driver."),
     ("The line", "“Most guys over 40 lose more than that. Energy, strength, stamina.”"),
     ("The exchange", "“Happen to you?” “Yeah.” “What’d you do?”"),
     ("The bottle", "Great Again T. 400 milligrams of tongkat ali. Made for men over 40."),
     ("CTA", CTA_OFFER)], top=True),
  I("Same 3 Swaps, Older Spokesman", ["testreload"],
    "The spokesman test from the Nov 10 funnel plan, at short length. Same words, different face.",
    "A fit man of 55 to 65 at the food table · Quiz",
    [("Hook", "A fit man around 60 does the three swaps. “Eat more of this, less of this.”"),
     ("One line of proof", "“Every one of these is backed by a study.”"),
     ("Handoff", "“Daniel Rose of SixPackAbs.com shows you why in a free video.”"),
     ("CTA", CTA_QUIZ),
     ("The test", "Run it against “3 Swaps, 10 Seconds.” One thing changes: the face.")]),
 ]),
 dict(name="The free bottle",
      proof="Nugenix ($400K in the last 30 days) leads with the offer: “Claim Your 14-Day Sample” ($108K). It sends these ads to a sample page, so these four need the free-month offer visible as soon as the page loads.",
      ideas=[
  I("Claim Your Free First Month", ["nugenix"],
    "Nugenix’s second-biggest ad: “Claim Your 14-Day Sample” ($108K lifetime).",
    "Dan to camera, bottle in hand · Free first month",
    [("Hook", "The bottle, held to camera. “Men over 40: your first month of Great Again T is free.”"),
     ("What it is", "400 milligrams of tongkat ali, 50 of zinc, 14 ingredients in all."),
     ("Who it’s for", "The belly, the energy, the drive."),
     ("The terms", "Just cover shipping. If you love it, it’s $67 a month. If you don’t, keep the bottle and you won’t be billed again."),
     ("CTA", CTA_OFFER)], top=True),
  I("See If You Qualify", ["nugenix"],
    "Nugenix’s funnel: a four-question “see if you qualify” quiz in front of the free sample.",
    "Dan to camera · Quiz, then the offer",
    [("Hook", "“Men over 40: see if you qualify for a free month of Great Again T.”"),
     ("How", "“Four questions. Thirty seconds.”"),
     ("First question on screen", "“Are you a man who wants to lose fat or build muscle?”"),
     ("What you get", "A full month’s supply. Just cover shipping."),
     ("CTA", "Tap the link and answer the four questions.")]),
  I("Why I’m Giving Away A Free Month", ["nugenix"],
    "Nugenix’s “try before you buy,” with the reason from your script: “Why am I spending my own money?”",
    "Dan to camera, bottle in hand · Free first month",
    [("Hook", "“I’m giving away a free month of my testosterone formula. Here’s why.”"),
     ("The reason", "Almost every man who tries Great Again T wants to keep taking it."),
     ("What’s in it", "A full 400 milligrams of tongkat ali. Most boosters have none."),
     ("The terms", "Cover shipping. Don’t like it? Keep the bottle and you won’t be billed again."),
     ("CTA", CTA_OFFER)]),
  I("$97 A Month. Or Free.", ["testogreens"],
    "TestoGreens’ price-drop sequence ($219.95, not $159, not $129, today $69), cut down to three steps.",
    "Dan with the store listing on screen · Free first month",
    [("Hook", "The store listing at $97. “This is $97 a month.”"),
     ("Why it costs that", "14 ingredients, 400 milligrams of tongkat ali, made in the USA."),
     ("The drop", "“You won’t pay $97 today. You won’t even pay $67.”"),
     ("The offer", "Your first month is free. Just cover shipping."),
     ("CTA", CTA_OFFER)]),
 ]),
 dict(name="One shocking number",
      proof="Bold-claim hooks open 23% of TestoGreens’ ads, and V Shred builds its first minutes on the frog study and four fast statistics.",
      ideas=[
  I("The Frog Study In 45 Seconds", ["vshred"],
    "V Shred’s shock proof, alone.",
    "Dan to camera with the study on screen · Quiz",
    [("Hook", "“A chemical sprayed on our food turned male frogs into females.”"),
     ("So what", "It’s in the food and water you had today."),
     ("Pivot", "Some foods do the exact opposite to your testosterone."),
     ("One example", "Whole eggs, steak, potatoes."),
     ("CTA", CTA_QUIZ)],
    needs="Add the frog paper (Hayes, 2010) to the studies list under the video."),
  I("1% A Year", ["vshred"],
    "The number both VSLs build on (V Shred at 4:07, and your script).",
    "Dan to camera with an age counter on screen · Quiz",
    [("Hook", "“After 30, a man loses about 1% of his testosterone every single year.” An age counter runs up: 30, 41, 50, 60."),
     ("What it feels like", "A little less strength, energy and drive every year."),
     ("It doesn’t stop", "Do nothing and it gets worse every year."),
     ("Good news", "Food can push it back up."),
     ("CTA", CTA_QUIZ)]),
  I("Cut One Mineral, Lose 73%", ["testogreens", "menerals"],
    "A bold-claim hook built on the zinc study in your script.",
    "Dan to camera · Quiz",
    [("Hook", "“Scientists cut one mineral out of healthy young men’s diets. In 20 weeks, their testosterone crashed 73%.”"),
     ("Reveal", "Zinc."),
     ("Where to get it", "Steak has five times the zinc of chicken breast. Oysters, crab and pumpkin seeds work too."),
     ("Tease", "Zinc is one of the nutrients that decide your testosterone. The free video covers the rest."),
     ("CTA", CTA_QUIZ)]),
 ]),
 dict(name="Before and after",
      proof="TestoGreens’ top ad is a transformation told in one question and one answer. You have the photos to do it for real.",
      ideas=[
  I("Same Guy. 39 And 41.", ["testogreens"],
    "TestoGreens’ transformation hook, with your photos.",
    "Dan’s photos, then Dan to camera · Quiz",
    [("Hook", "The before photo, full screen. “39.” Then the after photo, full screen. “41. Same guy.”"),
     ("What he didn’t do", "“I didn’t work out more.”"),
     ("What he did", "“I changed what I ate. Starting with eggs.”"),
     ("Who’s talking", "On-screen text only: Daniel Rose, SixPackAbs.com, 4.4 million men."),
     ("CTA", CTA_QUIZ)]),
  I("“What Did You Change?”", ["testogreens"],
    "TestoGreens’ top ad in 30 seconds: the question, the one-line answer, the tap.",
    "Dan plus a friend’s voice off camera · Quiz",
    [("Hook", "A friend’s voice over the before photo. “What did you change?”"),
     ("Answer", "“I stopped eating the foods that lower testosterone.”"),
     ("Out", "Egg whites, protein bars, dry chicken breast, flashed one at a time."),
     ("In", "Whole eggs, potatoes, steak."),
     ("CTA", CTA_QUIZ)]),
  I("Abs At 41 Without Working Out More", ["testogreens", "vshred"],
    "Your quiz question 3 as an ad, with the line from your script: “without working out any more than you do right now.”",
    "Dan’s photos, then Dan to camera · Quiz",
    [("Hook", "The after photo. “I got my abs back at 41 without working out more.”"),
     ("Before", "The before photo. “This was me right before 40.”"),
     ("The line", "“Same workouts. Different food.”"),
     ("One swap", "Whole eggs for egg whites."),
     ("CTA", CTA_QUIZ)]),
 ]),
 dict(name="What’s in the bottle",
      proof="Menerals ran “3 missing minerals” selfie ads to about $1M. The Nov 5 teardown found no big funnel leading with a full dose of tongkat ali, which makes 400 milligrams the hook only you can use.",
      ideas=[
  I("2 Minerals Your Testosterone Runs On", ["menerals"],
    "Menerals’ “3 missing minerals” ads, cut to the two minerals your script proves: zinc and boron.",
    "Dan, selfie style, in a kitchen · Free first month",
    [("Hook", "“Two minerals your testosterone runs on. Most guys never think about either one.”"),
     ("Zinc", "Cut it, and testosterone crashed 73% in 20 weeks."),
     ("Boron", "One week of it sent free testosterone up and estrogen down."),
     ("Where they are", "Steak and pumpkin seeds. Avocados and raisins."),
     ("CTA", "Or get both every day in two tablets. " + CTA_OFFER)]),
  I("400 Milligrams", ["vshred"],
    "V Shred’s label lists 200 mg of tongkat ali. TestoGreens and Nugenix have none. Yours has 400.",
    "Dan with the label in close-up · Free first month",
    [("Hook", "“Flip your testosterone booster over. Find tongkat ali. How many milligrams?”"),
     ("The answer", "“Most have none. Some have 100 or 200.”"),
     ("The label", "Close-up on Great Again T. “This has 400.”"),
     ("Why it matters", "Tongkat ali raised testosterone in men aged 50 to 70 who were low, in a 12-week trial."),
     ("CTA", CTA_OFFER)]),
  I("“Man Root”", ["vshred"],
    "V Shred’s “three pillars,” one line each, with the three roots from your script.",
    "Dan with the roots in hand · Free first month",
    [("Hook", "A ginseng root in his hand. “In Chinese, this is called man root.”"),
     ("Root two", "Tongkat ali, the king of natural testosterone boosters."),
     ("Root three", "Maca, grown over 13,000 feet up in the Andes."),
     ("The bottle", "“All three are in here.”"),
     ("CTA", CTA_OFFER)]),
  I("9 Out Of 10", ["testogreens"],
    "A bold-claim number hook, built on the tongkat ali study in your script.",
    "Dan to camera, bottle in hand · Free first month",
    [("Hook", "“76 men with low testosterone took one root every day for a month. At the start, about 1 in 3 had normal levels. A month later, 9 out of 10 did.”"),
     ("Reveal", "Tongkat ali."),
     ("The catch", "Most boosters have none, or 100 to 200 milligrams."),
     ("The bottle", "Great Again T has 400."),
     ("CTA", CTA_OFFER)]),
 ]),
]

def e(s):
    return html.escape(s, quote=True)

def render_group(groups, prefix):
    out = []
    n = 0
    for g in groups:
        cards = []
        for idea in g["ideas"]:
            n += 1
            code = f"{prefix}{n:02d}"
            tags = "".join(f'<span class="tag t-{s}">{e(SRC[s])}</span>' for s in idea["src"])
            beats = "".join(f"<li><b>{e(lbl)}.</b> {e(txt)}</li>" for lbl, txt in idea["beats"])
            top = '<span class="top">Closest to a proven winner</span>' if idea["top"] else ""
            needs = f'<p class="needs"><b>Before filming.</b> {e(idea["needs"])}</p>' if idea["needs"] else ""
            cards.append(
                f'<article class="idea" id="{code}" data-code="{code}" data-title="{e(idea["title"])}" '
                f'data-src="{" ".join(idea["src"])}" data-top="{1 if idea["top"] else 0}">'
                f'<div class="idea-head"><span class="code">{code}</span><h4>{e(idea["title"])}</h4>'
                f'<button type="button" class="pick" id="pick-{code}" aria-pressed="false">Pick</button></div>'
                f'<p class="model">{tags}{top}<span class="model-text">{e(idea["model"])}</span></p>'
                f'<p class="meta">{e(idea["meta"])}</p>'
                f'<ol class="beats">{beats}</ol>{needs}</article>')
        out.append(
            f'<section class="family"><div class="family-head"><h3>{e(g["name"])}</h3>'
            f'<p>{e(g["proof"])}</p></div>{"".join(cards)}</section>')
    return "".join(out), n

long_html, nl = render_group(LONG, "L")
short_html, ns = render_group(SHORT, "S")

# ---- checks -------------------------------------------------------------
assert nl == 30, nl
assert ns == 30, ns
for grp in (LONG, SHORT):
    for g in grp:
        for idea in g["ideas"]:
            assert 5 <= len(idea["beats"]) <= 7, (idea["title"], len(idea["beats"]))
            words = sum(len(t.split()) for _, t in idea["beats"])
            assert words <= 230, (idea["title"], words)

PAGE = r"""<title>Great Again T Ad Ideas</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;800&family=Inter:wght@400;600&display=swap">
<style>
/* Layout: one reading column. Proof first, then two lists (long, short) grouped by the proven concept each idea copies. */
:root{
  --bg:#f1f3f6; --surface:#ffffff; --ink:#131a22; --muted:#566373; --line:#d7dde5;
  --accent:#1d4e89; --accent-ink:#ffffff; --gold:#f2d675; --gold-ink:#3d2f00;
  --c-vshred:#b3261e; --c-testogreens:#2e6b3a; --c-nugenix:#1d4e89; --c-testreload:#8a5a00; --c-menerals:#0f6b6b;
  --display:"Archivo","Arial Narrow",Arial,sans-serif; --body:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0e1217; --surface:#171d25; --ink:#e7ebf0; --muted:#9ba7b5; --line:#2b3440;
  --accent:#8bb8ee; --accent-ink:#0e1217; --gold:#6b5410; --gold-ink:#fbe9a8;
  --c-vshred:#ff8a80; --c-testogreens:#86d39a; --c-nugenix:#8bb8ee; --c-testreload:#e6b655; --c-menerals:#6fd1d1;
  color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#0e1217; --surface:#171d25; --ink:#e7ebf0; --muted:#9ba7b5; --line:#2b3440;
  --accent:#8bb8ee; --accent-ink:#0e1217; --gold:#6b5410; --gold-ink:#fbe9a8;
  --c-vshred:#ff8a80; --c-testogreens:#86d39a; --c-nugenix:#8bb8ee; --c-testreload:#e6b655; --c-menerals:#6fd1d1;
  color-scheme:dark }
*{box-sizing:border-box}
[hidden]{display:none!important}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;margin:0}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.wrap{max-width:820px;margin:0 auto;padding-block:28px 120px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:28px}
h1,h2,h3,h4{font-family:var(--display);margin:0;text-wrap:balance;line-height:1.15}
p{margin:0}
.eyebrow{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:600}
h1{font-size:clamp(34px,7vw,52px);font-weight:800;letter-spacing:-.01em}
.lede{font-size:18px;max-width:62ch}
.top-block{display:flex;flex-direction:column;gap:12px}
h2{font-size:22px;font-weight:800}
.panel{display:flex;flex-direction:column;gap:14px}
.sources{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.sources div{display:grid;grid-template-columns:150px minmax(0,1fr);gap:4px 16px;padding:12px 0;border-bottom:1px solid var(--line)}
.sources dt,.sources .who{font-weight:600}
@media (max-width:560px){ .sources div{grid-template-columns:minmax(0,1fr)} }
.rules{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px;max-width:68ch}
details{border:1px solid var(--line);border-radius:6px;background:var(--surface)}
summary{cursor:pointer;padding:12px 14px;font-weight:600}
details .inner{padding:0 14px 14px;display:flex;flex-direction:column;gap:8px;color:var(--ink)}
details ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:baseline}
.controls{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:10px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:10px}
.seg{display:flex;gap:8px}
.seg button{flex:1 1 0;min-width:0;font:600 16px var(--body);padding:10px 12px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips button{font:600 13px var(--body);padding:6px 10px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer}
.chips button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.list{display:flex;flex-direction:column;gap:36px}
.list-head{display:flex;flex-direction:column;gap:6px}
.list-head p{color:var(--muted);max-width:68ch}
.family{display:flex;flex-direction:column;gap:14px}
.family-head{display:flex;flex-direction:column;gap:6px;padding-top:14px;border-top:3px solid var(--ink)}
.family-head h3{font-size:19px;font-weight:800;text-transform:uppercase;letter-spacing:.03em}
.family-head p{color:var(--muted);font-size:15px;max-width:70ch}
.idea{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:10px;min-width:0}
.idea-head{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:start}
.code{font:600 13px var(--body);font-variant-numeric:tabular-nums;color:var(--muted);padding-top:4px}
.idea h4{font-size:20px;font-weight:800}
.pick{font:600 13px var(--body);padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;white-space:nowrap}
.pick[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.model{font-size:14px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 8px;align-items:baseline}
.model-text{flex:1 1 100%}
.tag{font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ink);white-space:nowrap}
.tag::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;background:var(--muted)}
.t-vshred::before{background:var(--c-vshred)} .t-testogreens::before{background:var(--c-testogreens)}
.t-nugenix::before{background:var(--c-nugenix)} .t-testreload::before{background:var(--c-testreload)} .t-menerals::before{background:var(--c-menerals)}
.top{font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;background:var(--gold);color:var(--gold-ink);padding:2px 7px;border-radius:3px;white-space:nowrap}
.meta{font-size:13px;font-weight:600;color:var(--ink)}
.beats{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:6px}
.beats li{padding-left:2px}
.needs{font-size:14px;border-top:1px dashed var(--line);padding-top:8px;color:var(--muted)}
.empty{color:var(--muted);padding:12px 0}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:20;background:var(--ink);color:var(--bg);padding-top:10px;padding-bottom:calc(10px + env(safe-area-inset-bottom,0px));padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.bar-in{max-width:820px;margin:0 auto;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
.bar-in span{flex:1 1 140px;min-width:0;font-weight:600}
.bar button{font:600 14px var(--body);padding:8px 12px;border-radius:6px;border:1px solid var(--bg);background:transparent;color:var(--bg);cursor:pointer}
.bar button.primary{background:var(--bg);color:var(--ink)}
.bar textarea{flex:1 1 100%;min-height:72px;font:14px var(--body);border-radius:6px;border:0;padding:8px;background:var(--bg);color:var(--ink)}
</style>

<div class="wrap">
  <header class="top-block">
    <p class="eyebrow">SixPackAbs · Great Again T · November 10, 2026</p>
    <h1>60 Ad Ideas</h1>
    <p class="lede">30 long, 30 short. Each one copies an ad or a sales video that a testosterone advertiser has already put money behind, with your foods, your story and your bottle swapped in.</p>
  </header>

  <section class="panel" aria-labelledby="h-proof">
    <h2 id="h-proof">What every idea is copied from</h2>
    <div class="sources">
      <div><span class="who"><span class="dot" style="background:var(--c-testogreens)"></span>TestoGreens Max</span><span>$1.79M on YouTube in the last 30 days, 556 ads tested. Ads run 3:30 to 5:06. Top ad: “Your dad was fat, now he’s jacked. What did he change?”</span></div>
      <div><span class="who"><span class="dot" style="background:var(--c-vshred)"></span>V Shred Test Boost Max</span><span>About $6.2M lifetime, over 1,100 ads tested. “Testosterone-killing foods” quiz ads, one live for 149 days. Short ads cut to exactly 0:59.</span></div>
      <div><span class="who"><span class="dot" style="background:var(--c-nugenix)"></span>Nugenix Total-T</span><span>$400K in the last 30 days. Top ads: “SCHOOL” (1:01, $148K) and “Claim Your 14-Day Sample” ($108K).</span></div>
      <div><span class="who"><span class="dot" style="background:var(--c-testreload)"></span>Test Reload (yours)</span><span>The green rows in your archive: the Mark and Amy interview (1.62M views), the pool ad (671K views), the park bench, “How Men Over 40 Build Muscle Easily.”</span></div>
      <div><span class="who"><span class="dot" style="background:var(--c-menerals)"></span>Menerals</span><span>About $1M lifetime on “3 missing minerals” selfie-style ads.</span></div>
    </div>
    <ul class="rules">
      <li><b>The ad matches the page.</b> Every food, number and product fact comes from your final VSL script. Nothing new was added.</li>
      <li><b>Every ad ends the way theirs do.</b> Tap, answer four yes questions, watch the free video. Offer ads end on the free first month.</li>
      <li><b>Long</b> means 3:30 to 5:00. <b>Short</b> means 59 seconds or less, vertical.</li>
      <li><b>Some ideas share a body and change only the opening.</b> That is how the winners test: hundreds of hooks into one video.</li>
    </ul>
    <details id="left-out">
      <summary>Left out on purpose</summary>
      <div class="inner">
        <ul>
          <li>The red rows in your archive: 401(k) and retirement hooks, the valet and casino skits, “one household item,” “strange problem with my boyfriend,” the Obama voiceover, question ads with a static ending.</li>
          <li>Pool, car and bikini scenes. You ruled those out on November 6.</li>
          <li>Foods and nutrients that aren’t in your script or your bottle: soy (the studies show it doesn’t lower testosterone), vitamin D, magnesium, ashwagandha, DIM.</li>
          <li>V Shred’s chelated zinc argument. Your label is zinc oxide.</li>
          <li>Anything no testosterone advertiser is running.</li>
        </ul>
      </div>
    </details>
  </section>

  <div class="controls" id="controls">
    <div class="seg" role="group" aria-label="Format">
      <button type="button" id="view-long" data-view="long" aria-pressed="true">Long · 30</button>
      <button type="button" id="view-short" data-view="short" aria-pressed="false">Short · 30</button>
    </div>
    <div class="chips" role="group" aria-label="Filter by source">
      <button type="button" id="f-all" data-f="all" aria-pressed="true">All</button>
      <button type="button" id="f-top" data-f="top" aria-pressed="false">Closest to a winner</button>
      <button type="button" id="f-vshred" data-f="vshred" aria-pressed="false">V Shred</button>
      <button type="button" id="f-testogreens" data-f="testogreens" aria-pressed="false">TestoGreens</button>
      <button type="button" id="f-nugenix" data-f="nugenix" aria-pressed="false">Nugenix</button>
      <button type="button" id="f-testreload" data-f="testreload" aria-pressed="false">Test Reload</button>
      <button type="button" id="f-menerals" data-f="menerals" aria-pressed="false">Menerals</button>
    </div>
  </div>

  <section class="list" id="list-long" data-list="long">
    <div class="list-head">
      <h2>Long format, 3:30 to 5:00</h2>
      <p>The length TestoGreens runs (3:30 to 5:06). Your green Test Reload ads ran 4:45 to 7:18. Horizontal for YouTube, with the first 30 seconds doing the work.</p>
    </div>
    __LONG__
    <p class="empty" hidden>No long ideas match this filter.</p>
  </section>

  <section class="list" id="list-short" data-list="short">
    <div class="list-head">
      <h2>Short format, 59 seconds or less</h2>
      <p>Vertical. One idea per ad. The first two seconds are the thing being tested.</p>
    </div>
    __SHORT__
    <p class="empty" hidden>No short ideas match this filter.</p>
  </section>
</div>

<div class="bar" id="bar" hidden>
  <div class="bar-in">
    <span id="bar-count">0 picked</span>
    <button type="button" class="primary" id="bar-copy">Copy my picks</button>
    <button type="button" id="bar-clear">Clear</button>
    <textarea id="bar-text" readonly hidden aria-label="Your picks"></textarea>
  </div>
</div>

<script>
(function(){
  var KEY='gat-ad-ideas-picks-v1', view='long', filter='all', picks={};
  try{ var s=JSON.parse(localStorage.getItem(KEY)||'{}'); if(s&&typeof s==='object') picks=s; }catch(err){}
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(picks)); }catch(err){} }
  var lists={long:document.getElementById('list-long'), short:document.getElementById('list-short')};
  var ideas=[].slice.call(document.querySelectorAll('.idea'));
  var bar=document.getElementById('bar'), barCount=document.getElementById('bar-count'), barText=document.getElementById('bar-text');

  function apply(){
    Object.keys(lists).forEach(function(k){
      var list=lists[k]; list.hidden = (k!==view);
      var shown=0;
      [].slice.call(list.querySelectorAll('.family')).forEach(function(fam){
        var n=0;
        [].slice.call(fam.querySelectorAll('.idea')).forEach(function(el){
          var ok = filter==='all' || (filter==='top' ? el.dataset.top==='1' : (' '+el.dataset.src+' ').indexOf(' '+filter+' ')>-1);
          el.hidden=!ok; if(ok) n++;
        });
        fam.hidden = n===0; shown+=n;
      });
      list.querySelector('.empty').hidden = shown!==0;
    });
    [].slice.call(document.querySelectorAll('.seg button')).forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.view===view)); });
    [].slice.call(document.querySelectorAll('.chips button')).forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.f===filter)); });
  }
  function pickText(){
    return ideas.filter(function(el){ return picks[el.dataset.code]; })
      .map(function(el){ return el.dataset.code+' '+el.dataset.title; }).join('\n');
  }
  function paintPicks(){
    var n=0;
    ideas.forEach(function(el){
      var on=!!picks[el.dataset.code], b=el.querySelector('.pick');
      b.setAttribute('aria-pressed', String(on)); b.textContent = on ? 'Picked' : 'Pick'; if(on) n++;
    });
    bar.hidden = n===0;
    barCount.textContent = n+' picked';
    if(!barText.hidden) barText.value = pickText();
  }
  document.querySelector('.seg').addEventListener('click', function(ev){
    var b=ev.target.closest('button'); if(!b) return; view=b.dataset.view; apply();
    document.getElementById('controls').scrollIntoView({block:'start'});
  });
  document.querySelector('.chips').addEventListener('click', function(ev){
    var b=ev.target.closest('button'); if(!b) return; filter=b.dataset.f; apply();
  });
  document.addEventListener('click', function(ev){
    var b=ev.target.closest('.pick'); if(!b) return;
    var code=b.closest('.idea').dataset.code;
    if(picks[code]) delete picks[code]; else picks[code]=1;
    save(); paintPicks();
  });
  document.getElementById('bar-clear').addEventListener('click', function(){ picks={}; save(); barText.hidden=true; paintPicks(); });
  document.getElementById('bar-copy').addEventListener('click', function(){
    var btn=this, text='My ad picks:\n'+pickText();
    function fallback(){ barText.hidden=false; barText.value=text; barText.focus(); barText.select(); }
    try{
      navigator.clipboard.writeText(text).then(function(){
        btn.textContent='Copied'; setTimeout(function(){ btn.textContent='Copy my picks'; }, 1600);
      }, fallback);
    }catch(err){ fallback(); }
  });
  apply(); paintPicks();
})();
</script>
"""

page = PAGE.replace("__LONG__", long_html).replace("__SHORT__", short_html)

assert "—" not in page and "–" not in page, "dash found"
assert not re.search(r"\btrick", page, re.I), "the word trick found"
open(OUT, "w").write(page)
print("ok", nl, ns, len(page), "bytes")
