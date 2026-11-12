# Handoff: Next shoot outlines (35 picked ideas + the Tesla crash video)

**Date:** 2026-11-12
**Project:** Abs By AI (YouTube channel content)
**Business goal this serves:** marketing performance (organic reach and subscribers), feeding app adoption
**Category:** CONTENT, not ads. 11 long videos (LFC), 9 Shorts (SFC), 9 reaction Shorts (SFC), 7 long reactions (LFC).
**Suggested task name:** `Next Shoot Outlines`

## Objective

Write a detailed outline for each of the 36 videos below, in Dan's outline style, in ONE Google Doc he can edit. He will change the outlines, and only then are scripts written (scripts are a later task, not this one). Dan, 2026-11-12: "Go ahead and write out all the detailed outlines for each of these. I will modify as necessary, then we'll write out the scripts."

The whole shoot is green screen. Nothing may need outdoor or new gym filming.

## Current State

- Research is done: [Next Shoot Research Brief](https://claude.ai/artifact/JdZV2BrhWaHxkWKgDKJqAm), files in `Research/Shoot Research Claude 2026-11-12/` (README there lists the data traps).
- Two AIs each wrote an idea list. They were merged into one blind, shuffled pick page with new IDs (A = long videos, B = Shorts, C = reaction Shorts, D = long reactions): https://claude.ai/artifact/U1FQh89tUpYwrAAet8mnqb and, with clips that play in the page, http://127.0.0.1:11832/ .
- Dan picked 34 by ID and added D15 in his notes, so 35, plus one new video (the Tesla crash). His changes to seven ideas are quoted under each idea below.
- Nothing has been outlined yet. Only the skeletons below exist.
- **The blind test is still closed.** Dan has not asked for the scorecard. Do not say or write which AI wrote any idea, in chat, in the Doc or in a file name. When he asks, count his picks per AI from `Research/Shoot Research Claude 2026-11-12/blind/key.json` and follow memory `blind-claude-vs-codex-idea-picks`.

## Key Decisions Already Made (Dan, 2026-11-12)

- **100% green screen.** Exercise points use the finished October 23 gym clips (`Docs/OCTOBER23_SHARED_EDITOR_ACCESS.md`), never new filming. Any beat in a skeleton that needs an outdoor or gym take (for example "film three endings of your own curl") is rewritten for green screen with existing clips, props held on camera, or on-screen graphics.
- **About two thirds built for US viewers**: food and supplement claims with a number, "why" explainers, personal stories, reactions to names Americans know.
- **No app or AI content.** "Let's kill all AI content. I feel like it's established that doesn't work." The one exception is the Tesla video, which he asked for by name.
- **No natty-or-not or "exposed" reactions** in this batch.
- **Supplements in general only.** "I don't want to be perceived as a pitch." Never mention or lead toward his own supplement line.
- **GLP-1** topics are fine where he picked them (C02, C31, D05).
- **He selects what he wants; nothing is "killed"** (memory `review-pages-select-not-kill`). Any page that asks him to choose uses Select or Pick buttons.
- Execute his changes exactly as given. Do not soften his positions (memory `claude-softens-strong-language`), and do not add warnings or compliance notes.

## Detailed Plan

1. **Read the rules first** (all short): `.claude/skills/_shared/WRITING-RULES.md`, `.claude/skills/_shared/HOOKS.md`, `.claude/skills/_shared/DAN-VOICE.md`, `.claude/skills/_shared/voice/outlines.md`, and memory entries `video-outline-style`, `hooks-need-most-effort`, `no-staccato-fragments`, `shorts-reason-to-watch`, `shorts-open-with-pickup`, `reaction-clip-criteria`, `reaction-shorts-clip-first`, `dan-personal-facts-for-scripts`, `personal-facts-only-when-relevant`. Skills that own the formats: `/shortsideas` (Short idea shape and his title templates), `/reaction-clips` (clips, review page), `/scriptfromoutline` (what a long outline must give the script, including the no-warm-up rule).
2. **Do the lookups** (a cheaper model or subagents can do these; see the model section):
   - **B06:** find the famous person who said to buy smaller plates, and a real clip of them saying it. Dan thinks it may be a personal finance person making an analogy. Candidates to check, all unverified: Alex Hormozi, Ramit Sethi, Dave Ramsey, James Clear, Tim Ferriss, Naval Ravikant, Scott Galloway. Use `/reaction-clips` tools (`reference/yt.py`). If no clip of a famous person exists, say so and offer the closest real clip; do not invent a quote.
   - **B38 and A21:** the evidence for a lower protein number. Dan wants a figure such as 0.5 or 0.6 grams per pound where results are not much different. Start with the Morton 2018 meta-analysis (benefit levels off around 1.6 g per kg of body weight, about 0.73 g per pound) and the studies that compare lower intakes. Give the number, what "not a huge difference" means in the study's own terms, and the source link. His own number on record is 0.8 g per pound of LEAN mass (about 115 g for a 200-pound man at 28% body fat, which is about 0.58 g per pound of body weight, so his number already sits in that range: check the math and use it).
   - **C02:** trial numbers for semaglutide against tirzepatide and retatrutide (average weight loss, with the trial names), and whether retatrutide is approved yet as of this month. Note that Dan made a Short titled "Clavicular Recommends Retatrutide. He's Wrong." (DS-69): read that script so this outline does not contradict it, and mark the point `[DAN: ...]` if the two conflict.
   - **D15:** find a clip of Clavicular saying to leave one rep in the tank, and confirm the Jay Cutler clip (`VW9hnJL9UZE` near 0:04).
   - **Long reactions (D04, D05, D07, D08, D09, D10):** find candidate moments for each (10 to 15 seconds each, his clip rules), enough for the outline: about 6 to 10 per video.
   - **Number checks** marked "(check)" in the brief and ideas doc: the metabolism study (Pontzer, Science, 2021), the 1965 pedometer origin of 10,000 steps, calorie and protein figures on labels and menus, the social-network obesity study for A47 (Christakis and Fowler, 2007). Put the source link beside each number in the outline.
3. **Write the outlines**, in this order so the cheap ones land first: the 11 long videos (10 picks + Tesla), the 9 Shorts, the 9 reaction Shorts, then the 7 long reactions.
   - **Long video outline:** title; three hook takes (the first sentence must stop a stranger and be concrete; no warm-up after it, point one within about 20 seconds); one credibility line; each numbered point with its claim, the why, Dan's own number or example, and what is on the green screen behind him (photo, study card, label, clip); the close; three moments that could be cut as Shorts; a list of what is needed from Dan as `[DAN: ...]`.
   - **Short outline:** title in one of his templates; three hook takes; the beats as real specifics (foods, numbers, products named); bottom line; what is on screen. Fits 176 to 185 spoken words when scripted, so three beats, not five.
   - **Reaction Short outline:** the clip (id, seconds, first and last words), Dan's verdict as the first sentence after the clip, his take, the lesson the viewer can do tomorrow, bottom line. The clip plays first and is never repeated.
   - **Long reaction outline:** the target and the judge in the title; the clip list in order, each with Dan's verdict and one lesson; the close.
   - Never invent a habit, number or opinion for Dan. Use only what is on record or in his notes below; mark every gap `[DAN: ...]`.
4. **New clips go on one review page before they are relied on** (clips-first rule): B06, D15's Clavicular clip and the long-reaction candidates, built with `/reaction-clips` (`page.py`, now Select buttons), served with `review_server.py`, tested silently. The nine C clips are already chosen by Dan and need no second look.
5. **Deliver** one Google Doc titled "Next Shoot Outlines" (create it from HTML through the Drive connector so headings and lists survive; set link sharing to anyone with the link can view), sections in the order A, Tesla, B, C, D, each outline headed by its ID and title. Then in chat: the Doc link, the clip review page address, the list of `[DAN]` questions grouped by video, and the two wrap-up boxes. Stop there; do not script.

## The picks, with Dan's changes

### Long videos (10)

**A15 · I'm 41. If I Were 25 Again, This Is Exactly How I'd Get In Shape.**

- Open: I did this wrong for 15 years. If I were 25 again I'd do five things, in this order, and I'd have had abs before 30.
- Get lean first and never bulk; use machines and cables from day one instead of barbell ego lifts.
- Fifteen minutes every morning instead of 90 minutes three times a week; fix drinks and snacks before anything else; weigh in daily.
- What I'd ignore: splits, bulking season, most supplements. It worked at 40, so it is not too late for you either.
- Evidence: Organic: Wasted My Life

**A16 · I Ranked 15 "Healthy" Foods From Actually Healthy To Basically Candy**

- Open: Granola has more calories per cup than ice cream. I ranked 15 foods with a health halo, and most of them belong in the candy aisle.
- Basically candy: granola, acai bowls, dried fruit, trail mix, smoothies. The label number for each.
- Fine in small amounts: peanut butter, hummus, oat milk. Actually healthy: eggs, sardines, plain Greek yogurt.
- What I eat instead of each loser, and a ten-second label rule.
- Evidence: Peer: Healthy Hamesha 5.0×

**A17 · Bulking Is A Scam For Men Over 35**

- Open: After 35, most of what you gain on a "bulk" is fat. You are not bulking. You are getting fat with a plan.
- Where bulking came from: young lifters, many of them on drugs. What changes after 35.
- If you are skinny-fat: get lean first.
- How to add muscle without adding fat. Nobody ever regretted getting lean first.
- Evidence: Peer: Doctor Mike Diamonds 5.2×
- **DAN'S CHANGE:** New title: "Why Bulking Is a Scam, Not Just for People Over 35." Dan's points, in his words: (1) "When you build the habit of eating more, it's not that easy to break it when you want to cut again." (2) "You'll look better if you're leaner, even if you have less muscle." (3) "If you get lean first, it'll be better than getting big first and then trying to cut." (4) "The health risks of doing too much bulking and not being lean, like more wear and tear in your joints, more stress on your organs, etc."

**A18 · 7 Fitness Rules That Are Completely Made Up**

- Open: 10,000 steps a day came from a 1965 Japanese ad for a pedometer. Nobody tested it. Here are six more rules somebody made up.
- 10,000 steps, breakfast as the most important meal (a cereal slogan), eight glasses of water.
- One gram of protein per pound, six small meals, the fat-burning zone, no food after 7 PM.
- For each: where it came from on screen, what is true, and what I do.
- Evidence: Peer: Fledge Fitness 105.1×

**A21 · You Don't Need 200 Grams Of Protein. Here's The Real Number.**

- Open: The "one gram per pound" rule was written for 250-pound bodybuilders. It is the reason you think you can't eat enough protein.
- Where one gram per pound came from, and my number: 0.8 grams per pound of lean mass.
- The math for a 200-pound man at 28% body fat: about 115 grams. What that looks like in eggs, chicken, sardines.
- When more helps, why you do not need powder, and how to get your own number in ten seconds.
- Evidence: Peer: Fledge Fitness 105.1×

**A28 · Your Metabolism Didn't Slow Down At 40. This Did.**

- Open: A study of more than 6,000 people found that metabolism stays flat from age 20 to 60. So it is not why you got fat at 40.
- The study on screen, then what actually changed: you move less, you drink more, portions grew, you sleep worse.
- Me at 38 and 200 pounds as the example.
- The order to fix them in. This is good news, because all four are fixable.
- Evidence: Peer: Cory Armstrong Fitness 63.3×

**A29 · I'm 41. 6 Brutal Truths About Getting Lean After 40.**

- Open: Truth number one: nobody is coming to help you, and your doctor is not going to tell you that you are fat.
- Your doctor won't say it; you cannot out-train your drinks and snacks; alcohol costs you double after 40.
- Injuries end more diets than hunger does, so train safe; you will have to disappoint some people.
- It takes a year, not 12 weeks. It is still worth it.
- Evidence: Peer: KristianKfitness 504.5×; Peer: Old Dog Fitness 5.8×

**A38 · I'm 41. 7 Mistakes That Kept Me At 200 Pounds Until I Was 38.**

- Open: I was 200 pounds at 38 and I thought I was doing everything right. I was making seven mistakes, and most guys my age make at least five of them.
- The food mistakes: drinks I thought were healthy, "healthy" snacks like trail mix and dried fruit, and drinks that taste good.
- The routine mistakes: training at night and eating late, never weighing in, long workouts a few days a week.
- The last one: sitting at 190 for a year before getting help. Then the one mistake to fix this week.
- Evidence: Organic: Wasted My Life; Peer: KristianKfitness 504.5×

**A47 · The People Around You Are Keeping You Fat**

- Open: If your wife, your friends and your coworkers are overweight, you probably will be too. The research on this is brutal.
- The study on screen, and how it happens: shared meals, shared drinks, and what starts to look normal.
- What I did about it, and what to say when someone pushes food or a drink on you.
- The upgrade: one lean friend. You end up as the average of the people you eat with.
- Evidence: Peer: Dad Who Got Fit 658.9×

**A51 · Eat This, Not That: 10 Fast Food Chains Ranked For Fat Loss**

- Open: One order at Chipotle is 1,300 calories. Another, from the same line, is 500 with twice the protein. I ranked ten chains by how easy it is to stay lean there.
- The rule is protein per calorie. Bottom tier: the trap order at each chain and why nothing saves it.
- Middle and top tiers: one good order at each, with the menu and the numbers on screen.
- Three swaps that work anywhere (no drink calories, no sauce, double protein), then the number one chain and my order.
- Evidence: Peer: Noel Deyzel 6.4×


### Shorts (9)

**B05 · The Best Protein Snack Costs $2 And Comes In A Can**

- Open: The best protein snack in the store costs about $2, needs no fridge, and almost nobody buys it.
- Sardines: about 23 grams of protein and 190 calories. Next to a protein bar: same protein, fewer calories, a third of the price.
- How I eat them. Stop paying extra for protein in a wrapper.
- Evidence: Organic: Supplements Are Only 3%

**B06 · Guess Which Plate Has the Larger Serving of Pasta**

- Open: Put pasta on two different-sized plates. The portions look different; invite the guess.
- Slide each serving onto the same plate, then tare and weigh them on camera.
- Reveal that you plated the same cooked weight twice. Use a familiar plate if you rely on eyeballing portions.
- Evidence: Organic: Top 10 Abs Tips at 40; Peer: Paul Revelia 4.8×
- **DAN'S CHANGE:** Becomes a REACTION Short on green screen. Dan: "I want to talk about how the solution is to buy smaller plates. Also, some type of famous person said this: that you should buy smaller plates. I'm not sure exactly who. It might have been some kind of personal finance person making an analogy, but find the famous person who said that. I want to make this a reaction video, a reaction short, done on green screen, talking about how buying smaller plates will make you eat less." Find the person and a real clip first (clips-first rule), show Dan the clip, then outline around it.

**B08 · Your Metabolism Is Not The Reason You're Fat**

- Open: Scientists measured the metabolism of more than 6,000 people. From age 20 to 60, it does not slow down.
- So what did change since you were 25: you move less, you drink more, the portions grew. At 38 I blamed mine too; I was 200 pounds.
- The first two things to fix. It is not your age, so you can fix it.
- Evidence: Organic: I Was 200 Pounds At 38

**B10 · Diet Soda Won't Make You Fat**

- Open: Diet soda has zero calories, and zero calories cannot make you fat. The internet has this one backwards.
- What happens in trials when people swap sugar drinks for diet ones, and where the scare came from.
- My rule is zero liquid calories. A diet soda beats a regular one by 140 calories every time.
- Evidence: Organic: Supplements Are Only 3%

**B14 · The Treadmill Is Lying To You About Calories**

- Open: The treadmill says you burned 400 calories. It is wrong, and you are about to eat all of it back in one protein bar.
- Cardio machines overestimate, and the elliptical is the worst. Thirty minutes of cardio is one snack.
- What moves the scale is drinks and snacks. You cannot outrun your mouth.
- Evidence: Organic: Supplements Are Only 3%

**B21 · Top 3 Fast Food Orders When You're Cutting**

- Open: You can eat fast food every day and still get abs, if you order these three things.
- Three real orders, each with its calories and protein on screen.
- Order for protein, skip the drink and the sauce.
- Evidence: Peer: Noel Deyzel 6.4×

**B22 · Top 3 Most Overrated Supplements**

- Open: Americans spend tens of billions a year on supplements. These three are the biggest waste of it.
- Number three, number two, number one, each with what it promises and what it does.
- Supplements are 3% of your results.
- Evidence: Organic: Supplements Are Only 3%; Peer: Talking With Docs 155.7×

**B29 · Pre-Workout Is Just Expensive Coffee**

- Open: Pre-workout costs $1.50 a scoop for the caffeine in a 30 cent cup of coffee, plus an itch.
- The one ingredient doing the work is caffeine. The tingle is beta-alanine; it feels like something, and it is not your workout getting better.
- What I have before the gym instead. Keep the $40 a month.
- Evidence: Organic: Supplements Are Only 3%
- **DAN'S CHANGE:** New title: "Why I Quit Pre-Workout." Dan: "I was very dependent on pre-workout. I thought my workouts were so much better. I went on a vacation to Hawaii, and I forgot my pre-workout. I started doing all the workouts anyway, thinking I'd lift less, and I actually lifted more. Basically, pre-workout just makes you feel like you're performing better, but if you write down how much weight you're lifting and essentially you're measuring performance, you'll find out it's not actually improving your performance at all. The action step is to record your weight and reps when you're on pre-workout and not, and you'll see it's not improving performance."

**B38 · You Don't Need 1 Gram Of Protein Per Pound**

- Open: "One gram of protein per pound" was a rule for 250-pound bodybuilders. For you it is too high by about 80 grams.
- My number: 0.8 grams per pound of lean mass, not body weight. A 200-pound man at 28% body fat needs about 115 grams, not 200.
- What 115 looks like: eggs, a chicken thigh, a can of sardines, one more serving. A target you can hit beats one you quit.
- Evidence: Peer: Fledge Fitness 105.1×
- **DAN'S CHANGE:** Dan: "I also want to include an explanation: if you went down to 0.6 g/lb, then it wouldn't be a huge difference. Essentially, do some research into this and give another number where there wouldn't be a huge difference, even if you went down to, say, 0.5 or 0.6 g." Research the evidence and give the lower number with its source.


### Reaction Shorts (9)

**C01 · Alex Hormozi Says You're Not Hungry, You're Bored. He's Right.**

- Open: Alex Hormozi has a one-second test for hunger. Would you eat a plain chicken breast right now?
- He's right. Real hunger will eat protein. Boredom wants chips.
- Keep protein ready to grab. I swapped chips, trail mix and dried fruit for hard boiled eggs and sardines. If you don't want those, you're not hungry. If you don't want the egg, you don't want food.
- Clip (already cued, Dan has watched it): `A9TMIcajf8A` at 13:03 to 13:20. The Iced Coffee Hour Clips: Alex Hormozi's advice on weight control | OPENING UP (Part 2). https://www.youtube.com/watch?v=A9TMIcajf8A&t=783s

**C02 · Gabriel Iglesias Lost 15 Pounds His First Week On Ozempic, Then Stalled. Here's Why.**

- Open: Gabriel Iglesias dropped 15 pounds his first week on Ozempic. Then it stopped.
- That first drop is mostly water and less food in your gut. Real fat loss on it is slower, and it keeps going if you keep the diet.
- Judge it by the month, not the week. I went from 192 to 181 in two months, then 181 to 175 the month after. A stall in week two isn't the drug failing. It's normal.
- Clip (already cued, Dan has watched it): `0tSEjiisVI4` at 5:43 to 5:53, then 6:32 to 6:40. PowerfulJRE: Gabriel Iglesias on Weight Loss and Almost Being an Ozempic Spokesperson. https://www.youtube.com/watch?v=0tSEjiisVI4&t=343s
- **DAN'S CHANGE:** Dan: "I want to talk about how it was a mistake for him to just give up after not seeing success with Ozempic. I want to talk about how he should have upgraded to Tirzepatide or Gliquidotide, both of which are substantially more effective. If the person has not gotten good results with Ozempic, just realize that there are upgraded versions of this that are way better." "Gliquidotide" is read as retatrutide (dictation); Dan was told this reading and has not corrected it yet. Keep the existing clip.

**C03 · Ronnie Coleman Squatted 300 Pounds Two Weeks After A Herniated Disc. He's Wrong.**

- Open: Ronnie Coleman squatted 300 pounds two weeks after herniating a disc. Now his whole spine is fused.
- Heavy barbell squats are the riskiest way to build your legs, and you don't need them.
- Stop doing squats. The leg press builds the same legs without a bar on your spine. I do one leg exercise per workout: leg press, hamstring curls or the glute bridge machine. Train for the body you want at 60.
- Clip (already cued, Dan has watched it): `Q-RnElujInY` at 6:07 to 6:15, then 9:36 to 9:42. JRE Clips: Ronnie Coleman Details His 13 Post Bodybuilding Sugeries | Joe Rogan. https://www.youtube.com/watch?v=Q-RnElujInY&t=367s

**C09 · The Rock Built A Gym That Travels With Him So He Has No Excuses. You Don't Need One.**

- Open: The Rock hauls a 45,000-pound gym on 18-wheelers to every movie set so he never has an excuse.
- A home gym doesn't kill excuses. It makes skipping easier, because nothing gets you out the door.
- I own a $20,000 home gym, and I still drive to a real gym every morning. Leaving the house is what makes it happen. Don't buy a gym. Go to one.
- Clip (already cued, Dan has watched it): `OBUNP9eruRc` at 0:31 to 0:37, then 0:45 to 0:53. The Late Late Show with James Corden: Dwayne Johnson Travels with a 45,000-Pound Gym. https://www.youtube.com/watch?v=OBUNP9eruRc&t=31s

**C19 · Ryan Crowley Tore His Pec On Flat Bench With Larry Wheels Spotting. Stop Doing Flat Bench.**

- Open: Ryan Crowley tore his pec on a flat bench press with one of the strongest men alive spotting him.
- A spotter can't save you. Flat bench puts your shoulders and pecs in the worst position in the gym.
- Stop doing flat bench press. It's one of the stupidest exercises in the gym. Use the chest press machine or chest flies instead. Build your chest without betting your shoulder on every rep.
- Clip (already cued, Dan has watched it): `3NLMjbjvEMc` at 0:17 to 0:29, then 0:42 to 0:47. Larry Wheels: DEVASTATING CAREER THREATENING INJURY.. https://www.youtube.com/watch?v=3NLMjbjvEMc&t=17s

**C21 · Alex Hormozi Says Planet Fitness Makes Money Off Members Who Never Show Up. He's Right.**

- Open: Alex Hormozi says Planet Fitness is built for the 92 percent of members who never come.
- He's right, and it's not just Planet Fitness. A membership you don't use is a donation.
- Train first thing in the morning, every day, before the day can talk you out of it. Since I moved my workout to the morning I'm less stressed and I eat less junk at night. Be the member they lose money on.
- Clip (already cued, Dan has watched it): `BFTDW_Bppbg` at 0:08 to 0:14, then 0:36 to 0:50. Acquisitioncom: Alex Hormozi Reveals Planet Fitness EVIL GENIUS Business Model. https://www.youtube.com/watch?v=BFTDW_Bppbg&t=8s

**C25 · Herschel Walker Still Does 3,500 Sit-Ups A Day. He's Wrong.**

- Open: Herschel Walker says he does 3,500 sit-ups a day. You need two sets.
- Thousands of easy reps don't build abs. Abs are a muscle. Train them like one, heavy enough that rep 10 is hard.
- Cable crunches. One warm-up set of 12 to 15, then two hard sets of 6 to 10. That's my ab work at the gym. Stop counting to 3,500. Make 10 hard.
- Clip (already cued, Dan has watched it): `uPBO8T3a9sg` at 1:13 to 1:23. TMZSports: Herschel Walker Still Does 3,500 Sit-Ups Daily, Offers to Train Trump! | TMZ Sports. https://www.youtube.com/watch?v=uPBO8T3a9sg&t=73s

**C31 · Bill Maher Says We Gave Up On Diet And Exercise For Ozempic. He's Wrong.**

- Open: Bill Maher thinks taking Ozempic means giving up on diet and exercise. I take it, and I train every single day.
- It's not one or the other. A low dose turns the hunger down. You still do the work.
- If you take it, lift every day and eat your protein, so the weight you lose is fat, not muscle. I'm on 1.5 mg a week and I train seven days a week. The shot is the tool. The gym still matters.
- Clip (already cued, Dan has watched it): `pcWeT-eI8hY` at 1:12 to 1:29. PowerfulJRE: Bill Maher on Obesity Being Treated as a Disease. https://www.youtube.com/watch?v=pcWeT-eI8hY&t=72s

**C35 · Kumail Nanjiani Says The Diet Is The Hardest Part. He's Right.**

- Open: Kumail Nanjiani got shredded for Marvel. He says the workouts got easy. The diet never did.
- He's right. Training is one hour of your day. Food is a decision every hour.
- Take the decisions away. I buy meal prep, about $8 to $9 a meal, so what I eat is decided before I'm hungry. Make the diet boring and it gets easy.
- Clip (already cued, Dan has watched it): `W_9jPRA0_Jc` at 5:44 to 5:57. Jimmy Kimmel Live: Kumail Nanjiani Has Pizza & Cake for First Time in a Year. https://www.youtube.com/watch?v=W_9jPRA0_Jc&t=344s


### Long reactions (7, D15 added from Dan's notes)

**D04 · Rating The Worst Gym Mistakes On The Internet**

- Open: Play the first fail and freeze just before it goes wrong. Say what is about to happen.
- Each fail: the clip, and what went wrong in one sentence.
- The safe version of each, shown with my own gym clips.
- The pattern: almost every fail is a barbell or an ego lift. The machines that make these impossible.
- Starting clips (exact moments not yet picked): `JxgwVez4DuM` (FailArmy: Best Workout Fails | 100% Morons); `LRr17X-hlwA` (FailArmy 2.0: Gym Fails So Bad It Hurts 😭)
- Evidence: Peer: trainer winny 6.4×; Peer: Larry Wheels Reacts 107.5×

**D05 · I'm On Zepbound. Reacting To The Loudest Arguments Against It.**

- Open: Play the strongest objection first and answer it in one word: true, half true or wrong.
- Each objection: the clip, then the verdict and why.
- My own numbers: 192 to 175, 1.5 mg a week, muscle kept.
- Who should not take it.
- Starting clips (exact moments not yet picked): `nlC7rDjnfnw` (Club Random Podcast: Jillian Michaels on Ozempic); `zpyibQvpjcw` (NewsNation: Jillian Michaels makes case against Ozempic use | Dan Abrams); `ZwJJuy_IQYU` (The Diary Of A CEO Clips: The Hidden DANGERS of Weight Loss Injections They DON'T Tell)
- Evidence: Organic: Hormozi reaction; Peer: Barrick Health 99.9×

**D07 · Alex Hormozi's Fitness Rules, Rated By A Guy Who Got Abs At 40**

- Open: Play one Hormozi rule and answer it in the first sentence: "He's right" or "He's wrong".
- Six to eight of his rules, one clip each, each with a verdict.
- My version of each rule.
- Where a businessman's rules beat a trainer's.
- Starting clips (exact moments not yet picked): `fxyhIXZ6Yog` (Alex Hormozi: The Alex Hormozi Diet (REVEALED)); `RpqSy5V1fFQ` (Alex Hormozi: My Unconventional Diet Explained in 15min); `jYY4FDzf4p0` (MoreMozi: What Is My Fitness Routine?)
- Evidence: Organic: Hormozi reaction

**D08 · A Bodybuilder Gave Up Body-Part Days. Does His Circuit Solve the Right Problem?**

- Open: Open on the Fit Father coach describing muscular men getting winded. Ask which kind of fitness his story actually tested.
- Map his circuit on screen and follow one round: what challenges the muscles, what raises breathing demand, what is mostly transition?
- Contrast it with an ordinary strength session plus a separate walk. Compare both for a man with the same weekly time budget.
- Let two viewers pick different winners: the man chasing strength and the man who wants stairs to feel easier.
- Starting clips (exact moments not yet picked): `VwTeS5voWP4` at 0:12 (Fit Father Project - Fitness For Busy Fathers: I Used To Train Arm Day, Leg Day, Shoulder Day (Now I Do THI); `VwTeS5voWP4` at 2:40 (Fit Father Project - Fitness For Busy Fathers: I Used To Train Arm Day, Leg Day, Shoulder Day (Now I Do THI)
- Evidence: Organic: Hormozi reaction + Top 10 Abs Tips at 40; Peer: Fit Father Project - Fitness For Busy Fathers 6.4×

**D09 · I'm 41 With Abs. I Rated 10 Celebrity Diets.**

- Open: Open on the most extreme plate, The Rock's cheat meal, and give the verdict in the first sentence.
- Each celebrity gets a 10 to 15 second clip, a score out of 10 for "would this work for a normal guy", and one thing worth stealing.
- Sort them: works only if you train four hours a day, or works for anyone.
- The winner, what it shares with how I eat, and the three things every lean celebrity does.
- Starting clips (exact moments not yet picked): `VO-xaqyHe_Y` (Men's Health: Everything Dwayne "The Rock" Johnson Eats In A Day | Eat Lik); `-aWeIZxfT4E` (The Tonight Show Starring Jimmy Fallon: Dwayne Johnson Eats Cheat Meals Late at Night and Alone Like); `WWE_yoRmMbU` (TB12 Sports: Tom Brady Explains the TB12 Diet); `FV0B26YYCqA` (Aventura Australia: Erling Haaland's Primal Diet Is INSANE (6,000+ Calories))
- Evidence: Organic: Hormozi reaction; Peer: Renaissance Periodization 10.4×

**D10 · Planet Fitness Is The Most Hated Gym In America. Reacting To The Hate.**

- Open: Open on the lunk alarm going off, then ask whether the hate is deserved.
- Each complaint with one clip: the lunk alarm, pizza night, no barbells.
- A verdict on each, and what a normal guy can build there with machines alone.
- The gym you will actually go to beats the one with the best equipment.
- Starting clips (exact moments not yet picked): `5-jIV3R2v5I` (SunnyV2: How Planet Fitness Became Hated By The World); `0ZsljkuN9Es` (Will Tennyson: I Trained At World's Most Hated Gym For A Week); `PUJ4J2BQgCM` (Joe Bartolozzi: Why Everyone Hates Planet Fitness.); `jiuY-FTZzlc` (Aaron McKinney: Lunk Alarm at planet fitness)
- Evidence: Organic: Hormozi reaction; Ads: Stopped Deadlifting at 40
- **DAN'S CHANGE:** Dan reverses the idea's verdict: "I want to talk about why Planet Fitness is hated for a reason. Planet Fitness is the worst gym in America. It's full of losers, and I want to talk about how the people you train around are more important than the quality of the equipment or the environment you're in. And I want to talk about why I train at House of Gainz, a bodybuilding gym, primarily for this reason: to be around better people."

**D15 · Jay Cutler Says He Never Trained to Failure. What Did He Mean by "Failure"?**

- Open: Open on the Mr. Olympia winner saying he never trained to failure; cut before the commentator answers.
- Play Hybrid Calisthenics' definition, then film three endings of your own light curl: tired, last clean rep, and a rep that needs body swing.
- Replay the final two seconds of each. Ask which evidence would tell a stranger whether another clean rep was possible.
- Give a practical stopping rule for a controlled isolation set and explain why it doesn't automatically apply to a heavy barbell set.
- Starting clips (exact moments not yet picked): `VW9hnJL9UZE` at 0:04 (Renaissance Periodization: Jay Cutler Never Trained to Failure); `eJGYjxl1yPk` at 0:06 (Hybrid Calisthenics: Are you actually training to "failure"?)
- Evidence: Organic: Hormozi reaction + Deadlift Trick; Peer: Renaissance Periodization 4.6×
- **DAN'S CHANGE:** Modified. Dan: title "Should You Train to Failure? It Depends Who You Are." "I want to show a clip of Jay Cutler saying he never trains to failure, and then Clavicular saying that you should leave one rep in the tank. Essentially, I want to talk about how failure is different for different people. Clearly, Jay Cutler is training at a higher level of intensity, and if he goes to failure, then he's actually at failure. Whereas if Clavicular goes to failure, then he probably has five more reps in the tank." His recommendations: "For women and for people who are very new to training, you should go beyond failure and do two reps after you think you failed. Those reps are spotted and assisted. Most likely, you're not getting any assistance. You just think you're at failure." and "For people who know how to genuinely go to failure, meaning that the spotter had to help you with the last reps, it's no longer necessary to do the spotted reps. You can just go to failure or leave one rep in the tank." Summary in his words: "going to failure depends on who you are, because for a lot of people, their definition of failure actually means they got five reps left in the tank."

### One more video Dan added (not from the pick list): the Tesla crash

Default it to a long video (he said "a video"); say so in the Doc so he can switch it to a Short. Dan's brief, in his words:

- "I crashed my Tesla because I didn't trust FSD."
- "I briefly say what happened: a car pulled in front of me without the turn signal."
- "The 18-wheeler hit me from behind while the clips are playing on screen."
- "Talk about how, if I just trusted FSD, I could have pulled over to the left or maybe gone a little more forward and probably avoided this accident."
- "Next time, if I feel like I'm going to crash in FSD, I'm going to trust the system a little bit more."
- "The lesson should be that driving while being blind in every direction except for one (which is what we're doing when we're manually driving) isn't safe."
- "By upgrading to FSD, not only are you saving tons of time, but you're removing the number one risk of dying early for people who are healthy and conscious of their health like us."
- "Using FSD and trusting FSD is now a health issue. If you really care about your health, you need to be using FSD."
- He also said: "I crashed my Tesla because I unnecessarily intervened and pressed the brake when I saw a car pull in front of me with no turn signal. Then an 18-wheeler hit me from behind."

Context and footage (from the Codex task that filed his insurance claim). Everything is in `~/Documents/Insurance Claims/2026-10-24/` on this Mac:

- `accident-narrative.txt`: what happened, in Dan's words to the insurer. October 24, 2026, about 3:30 PM.
- `claim-attachments/2026-10-24_15-29-29-front.mp4` and `2026-10-24_15-29-29-back.mp4`: the front and rear dashcam minute. The impact is about 43 seconds into the rear clip. `claim-attachments/Tesla_front_camera_collision_2026-10-24.mp4` is a smaller copy of the front view.
- `dashcam-candidates/` and `dashcam-candidates-earlier/`: the minutes before and after, front and rear. `dashcam-decrypted/inspection/` has still frames and contact sheets, useful for choosing moments without playing video.
- `claim-attachments/accident-photo-01.jpg` to `-14.jpg`: photos of the damage.
- `claim-working-record.json`: the claim's state.
- Watch the clips (silently) before outlining, and write the outline around what they actually show: when the other car moves over, when Dan brakes, where the truck is, and whether the left lane was open.
- Keep private details out of the outline, the Doc and every repo file: other people's names, the trucking company, claim and police numbers, the exact location. The folder holds all of them. This repo is public.
- Facts to check and cite in the outline: what the leading causes of death are for adults under 45 (for the "number one risk of dying early" line), and Tesla's published crash rates with and without FSD. Use the real figures.
- The claim for this crash is still open (board entry "TeslaEstimates", Codex). Write the outline exactly as Dan asked. When the video is released relative to the claim is his call; he has been told once.

## Things to Avoid / Lessons Learned

- Do not reveal authorship of any idea (see Current State).
- Do not re-open settled choices: the picks, his title changes, his reversed verdict on Planet Fitness, green screen only.
- Skeleton beats written as camera tests ("weigh it on camera", "film two reps") need a green screen version, not a filming day.
- Three picked Shorts share a topic with a picked long video (B08 with A28, B38 with A21, B21 with A51). Outline both; give the Short the single sharpest point and keep the rest for the long video, so they do not repeat each other.
- YouTube caption downloads were rate limited on 2026-11-12 (HTTP 429). `yt.py` search still works; for transcripts use the browser transcript panel method in `/reaction-clips`.
- The clip player ignores start times with half seconds; use whole seconds.
- GitHub pushes are blocked by a merge conflict from other sessions in `AI_COORDINATION.md`, `Docs/DAN_DECISIONS.md` and `Handoffs/README.md`. `safe-push.sh` commits locally and stops; that is expected until someone hand-merges those three files.
- The status board is at its 2,500 word limit. Do not add an entry unless you remove words from your own.

## Relevant Files & Locations

- This handoff: `Handoffs/handoff-20261112-next-shoot-outlines.md`
- Blind list data (no author info): `Research/Shoot Research Claude 2026-11-12/blind/cards.json`. Private author key: `.../blind/key.json` (do not open it until Dan asks for the scorecard).
- Pick pages: https://claude.ai/artifact/U1FQh89tUpYwrAAet8mnqb and http://127.0.0.1:11832/ (re-serve with `python3 .claude/skills/_shared/review_server.py 11832 "Research/Shoot Research Claude 2026-11-12/blind/local"` if it has been retired).
- Research brief: https://claude.ai/artifact/JdZV2BrhWaHxkWKgDKJqAm . Evidence tables: `Research/Shoot Research Claude 2026-11-12/evidence/`.
- Existing videos, so outlines do not repeat one: `Handoffs/video-editing/jobs.json` (titles of every long video and Short already filmed or queued).
- Reaction clip tools and rules: `.claude/skills/reaction-clips/`.
- Tesla crash folder: `~/Documents/Insurance Claims/2026-10-24/`.
- The `Research/` folder is not in the repo, so this handoff runs in a local session on this Mac, not in the cloud.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Opus 5.5, high effort, for the whole task. |
| **If Claude usage is high / approaching a limit** | Still Claude Opus 5.5, high effort, for writing the outlines. Send the lookups in step 2 (clip finding, protein and drug trial numbers, number checks) to Sonnet 5.5 subagents, and split the task in two sittings if needed: long videos and Shorts first, reactions second. |

This is writing in Dan's voice, which stays on Claude regardless of usage (project routing: Opus 5.5 high for writing; Codex does not write his copy). Fable is not needed.

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20261112-next-shoot-outlines.md` in full and carry it out. It asks for detailed outlines, in my outline style, for 36 green screen videos I picked for my next shoot (35 picks plus the Tesla crash video), delivered in one Google Doc I can edit. My changes to seven of the ideas are quoted in the handoff and must be followed exactly. Start with step 1 (read the writing, hook and voice rules), then the lookups in step 2, then write the outlines in the order given. Do not write scripts, and do not tell me which AI wrote which idea until I ask for the scorecard. Name this task "Next Shoot Outlines".
