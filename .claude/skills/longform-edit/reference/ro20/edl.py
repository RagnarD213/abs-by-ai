"""RO-20 "Why You Should Invest More In Your Health" edit decision list (8/3 kitchen roll C1511, one 68:51 take off an outline).
Pieces are anchored on PHRASES in the medium.en word list (words.json, global timeline of mkglobal.py, with the verified
windows of word_patches.json), not on typed times: (id, roll, first words, last words, roll-local hint, script beat, why).
Edges are then snapped to the measured lav envelope. Optional 8th/9th fields: measured roll-local out / in that override the snap.
The list is generated from takesel/takeplan.py by takesel/gen_pieces.py (edit the plan, then regenerate)."""
import json, re, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro20"
FPS = 30000/1001
ROLLS = json.load(open(f"{W}/rolls.json"))
WORDS = json.load(open(f"{W}/words.json"))["words"]
THR = -43.0   # C1511 lav: room mode -60 dB (quiet pauses -62..-56), speech median -25 dB inside words, word tails reach -43 about 0.1 s after the word (measured on lav.wav)
PIECES = [
 ("intro", "C1511", "Alright, so let's talk about why", "wrong way to think.", 2.9,
  "Alright, so let's talk about why you need to be investing more in your health no ... happy with that. But that is totally the wrong way to think.",
  "only take of the opening and the excuse run, up to 'But that is totally the wrong way to think.'"),
 ("halo1", "C1511", "If you care about money, if", "is the halo effect.", 74.1,
  "If you care about money, if money is your most important priority in life, then you need to be prioritizing your looks. And the reason for that is the halo effect.",
  "take 3 of 3 of 'If you care about money ...', the last and clean (takes at 34.2 s and 44.5 s; 'Let me silence my notifications' sits between them)"),
 ("halo2", "C1511", "It has been scientifically proven that", "on how you look.", 91.9,
  "It has been scientifically proven that people are more likely to think you're intelligent, that you're ... going to have a better personality purely based on how you look.",
  "only take. 'Okay so let's talk about the halo effect.' (88.3 to 91.4 s) left out: he named the halo effect 6 s earlier, twice"),
 ("halo3", "C1511", "even very technical, even very intelligent", "to get that partnership.", 109.7,
  "even very technical, even very intelligent people that you do business with are gonna be judging ... who you can trust, and you're more likely to get that partnership.",
  "second start of 'even very technical, even very intelligent people' (the first stopped at 'do businesses,')"),
 ("rel1", "C1511", "So Let's say that you're in", "in the long term.", 177.8,
  "So Let's say that you're in a relationship right now and you're getting a little bit ... money on your relationship, and to maintain that in the long term.",
  "second take of the relationship example (the first stopped at 170 s when he asked about a plane)", None, 177.76),
 ("date1", "C1511", "And, obviously, if you are single,", "apps or meeting online.", 274.0,
  "And, obviously, if you are single, looking better makes a tremendous, tremendous difference. It is impossible ... over 70% of people are meeting on dating apps or meeting online.",
  "only take"),
 ("date2", "C1511", "In the modern online dating environment", "top 10 of looks,", 298.1,
  "In the modern online dating environment looks are paramount. The reason for this is in the ... nothing. So, you need to break into that top 10% of looks,",
  "second run at 'In the modern online dating environment' (the first, 294.8 to 296.3 s, he abandoned; it was hidden in a 5.5 s Whisper word). Ends on 'So, you need to break into that top 10% of looks,': the EARLIER take of that clause on purpose, because in the retake he says 'top 80% of looks', a slip for the top 10% he named 30 s before", 367.07, 298.06),
 ("date4", "C1511", "Otherwise your personality, your money, none", "really going to matter.", 373.3,
  "Otherwise your personality, your money, none of it is really going to matter.",
  "last take of 'Otherwise your personality, your money, none of it is really going to matter.'"),
 ("prod1", "C1511", "Alright let's talk about the second", "be a good thinker.", 388.3,
  "Alright let's talk about the second reason you need to invest more in your health. Productivity. ... not gonna be productive and you're not gonna be a good thinker.",
  "only take"),
 ("prod2", "C1511", "It's gonna be hard for you", "this strains your productivity.", 427.1,
  "It's gonna be hard for you to grind if you're not in peak physical condition. And I'm gonna show you a few ways that this strains your productivity.",
  "retake of 'It's gonna be hard for you to grind' (the first trailed off at 'if you're always thinking about')"),
 ("prod3", "C1511", "First of all, let's talk about", "going to Taco Bell.", 441.4,
  "First of all, let's talk about the immediate effects. Let's say before you even get in ... can eat for lunch every day rather than going to Taco Bell.",
  "only take; ends before 'The first day you do this, you're going to experience increased productivity', which he corrected ('Actually ... I'm going to do that take one more time')"),
 ("prod4", "C1511", "Now, the first few days you", "time of the day.", 469.2,
  "Now, the first few days you do this, it might take a little bit of getting ... afternoon is going to become your most productive time of the day.",
  "his retake: the first few days productivity dips, then it gets better"),
 ("prod5", "C1511", "Here's another reason why looking good", "resulting from being overweight.", 500.1,
  "Here's another reason why looking good and being in great health improves your productivity. As you ... all kinds of prescription medications, arthritis, joint problems resulting from being overweight.",
  "only take. The next sentence, 'There's all kinds of problems that you have to deal with if you don't take care of your health' (525.2 to 532.8 s, said one and a half times), is left out whole: 'all kinds of' problems and medications came 6 s earlier"),
 ("prod6", "C1511", "So a lot of people think,", "is incredibly time consuming.", 533.5,
  "So a lot of people think, oh, well I'm just not going to spend that hour ... the time in the doctor's office and this is incredibly time consuming.",
  "only take"),
 ("prod7", "C1511", "When you have problems that require", "that long term thinking,", 555.6,
  "When you have problems that require you to go to the doctor you have to spend ... would be in better shape today. So engage that long term thinking,",
  "only take, up to 'So engage that long term thinking,'"),
 ("prod8", "C1511", "Sacrifice a few days or a", "yourself for doing that", 607.8,
  "Sacrifice a few days or a few weeks of productivity for the long term and a few years from now You will be thanking yourself for doing that",
  "second run of 'sacrifice a few days or a few weeks of productivity ...' (the first stopped at 'a few years from')"),
 ("mind1", "C1511", "The third reason why you have", "to be unhealthy too.", 624.3,
  "The third reason why you have to invest more in your health is that being in ... body is unhealthy then your mind is going to be unhealthy too.",
  "only take"),
 ("mind2", "C1511", "Now if you develop mental health", "your money once again.", 666.8,
  "Now if you develop mental health problems then that's going to be very expensive to fix ... is gonna be expensive Draining your time and your money once again.",
  "only take"),
 ("mind3", "C1511", "This medication is probably gonna make", "people are trapped in.", 696.7,
  "This medication is probably gonna make you fat being fat is gonna make your mental health ... and an ongoing spiral of failure that many people are trapped in.",
  "retake of 'This medication is probably gonna make you fat' (the first stumbled on 'gonna make you make')"),
 ("mind4", "C1511", "I don't want you to get", "that in a minute.", 716.5,
  "I don't want you to get trapped in that. That's the reason why you need to ... therapy and medication. And I'll go more into that in a minute.",
  "retake of 'I don't want you to get trapped in that' (the first stopped at 'your health your first,')"),
 ("cost1", "C1511", "The fourth reason why you need", "you do have insurance.", 738.3,
  "The fourth reason why you need to invest more in your health is that even if ... more you are going to pay, even if you do have insurance.",
  "only take"),
 ("cost2", "C1511", "So many people waste their life", "they're not even successful.", 767.2,
  "So many people waste their life dedicating every waking moment to money. The lawyer who's working ... life trying to fix these problems and usually they're not even successful.",
  "only take"),
 ("cost3", "C1511", "Giving you an example I know", "much much better investment.", 811.1,
  "Giving you an example I know somebody personally in my life who's made a lot of ... 401k instead put it into your health. A much much better investment.",
  "only take"),
 ("dead1", "C1511", "Now here's the final point that", "good if you're dead", 920.7,
  "Now here's the final point that I want to make. A lot of people think oh ... guys to remember money doesn't do you any good if you're dead",
  "only take, to 'money doesn't do you any good if you're dead'. 'Money does you no good if you're dead.' (936.5 to 938.0 s) left out: the same sentence re-said at once"),
 ("dead2", "C1511", "if You have millions of dollars,", "think that they will.", 944.5,
  "if You have millions of dollars, and you just pass it on to your heirs You ... gonna benefit from this, but I really don't think that they will.",
  "second, complete version of 'If you have millions of dollars and you just pass it on to your heirs' (the first, 938.3 to 943.5 s, ended 'as all')"),
 ("dead3", "C1511", "both sides of my family, both", "of neglecting your health.", 986.3,
  "both sides of my family, both sets of grandparents, my extended family started suing each other ... of money behind and you die prematurely because of neglecting your health.",
  "last take of 'Both sides of my family, both sets of grandparents ...'. The sentence before it, 'Both sides of my family had inheritance fights where people started suing each other over the inheritance' (973.2 to 979.1 s), is left out: this take says the same thing in full"),
 ("dead4", "C1511", "Now maybe you're watching this and", "it doesn't really matter.", 1006.7,
  "Now maybe you're watching this and saying I'm in my 20s or 30s right now. I ... in the world, but if you're visually impaired, it doesn't really matter.",
  "only take"),
 ("dead5", "C1511", "Let's say like many overweight people", "like an old person.", 1063.0,
  "Let's say like many overweight people do you develop joint problems. Everything you do is gonna ... you're just gonna stay on the first floor like an old person.",
  "only take"),
 ("dead6", "C1511", "Let's say the kids come first.", "a pile of money.", 1093.5,
  "Let's say the kids come first. If you become debilitated by disease because you wanted to ... of them than someone who's debilitated leaving them a pile of money.",
  "starts on 'Let's say the kids come first.' The sentence before it (1088.4 to 1093.4 s) is left out: he is walking back into frame and off centre while saying it (Dan's flag on the old edit)", None, 1093.49),
 ("dead7", "C1511", "Let's say your wife or girlfriend", "little bit more money.", 1111.7,
  "Let's say your wife or girlfriend is your first priority. Again, she would far rather have ... to take care of, but who has a little bit more money.",
  "only take"),
 ("dead8", "C1511", "So I really wanna stress this", "makes you more money.", 1127.8,
  "So I really wanna stress this point, guys. Money does you no good if you're dead ... in the long run, investing in your health makes you more money.",
  "only take"),
 ("broke1", "C1511", "All right, so hopefully now I've", "on the wrong things.", 1174.0,
  "All right, so hopefully now I've got you convinced. You need to be spending more money ... do have the money, you're just spending it on the wrong things.",
  "only take"),
 ("broke2", "C1511", "Now, obviously one way to find", "to maximize your fitness.", 1207.0,
  "Now, obviously one way to find this money is just to make a little bit more ... than enough money to buy everything you need to maximize your fitness.",
  "only take"),
 ("keep1", "C1511", "Alright so before we go into", "on delicious healthy food.", 1226.5,
  "Alright so before we go into what to cut, I want to tell you the things ... be spending the most that you can afford on delicious healthy food.",
  "only take"),
 ("keep2", "C1511", "Number two your mattress your sleep", "need for our health.", 1255.0,
  "Number two your mattress your sleep is going to be important so anything that affects your ... in order to get the money that we need for our health.",
  "only take"),
 ("sac1", "C1511", "Okay, so let's talk about what", "that make you fat.", 1306.1,
  "Okay, so let's talk about what we should sacrifice in order to get better health. So, ... better health is sacrificing spending money on things that make you fat.",
  "only take"),
 ("sac2", "C1511", "If you sacrifice spending money on", "gonna tell you why.", 1325.5,
  "If you sacrifice spending money on something that makes you fat, you're killing two birds with ... need some entertainment, but you don't. And I'm gonna tell you why.",
  "only take"),
 ("sac3", "C1511", "I'm not telling you to sacrifice", "isn't a permanent sacrifice.", 1370.5,
  "I'm not telling you to sacrifice going to the bar or going to the club forever, ... make some extra money so that way this isn't a permanent sacrifice.",
  "only take", 1398.46, None),
 ("sac4", "C1511", "Bars and clubs are the number", "to get in shape.", 1420.9,
  "Bars and clubs are the number one thing that sacrifice because you're drinking alcohol usually in ... sacrifice that for multiple reasons if you want to get in shape.",
  "take 2 of 2 of 'Bars and clubs are the number one thing to sacrifice', the last and complete (take 1 at 1411.8 s stopped after 'you're consuming the alcohol itself')"),
 ("rest1", "C1511", "Here's the next thing you need", "yourself. And here's why.", 1464.5,
  "Here's the next thing you need to sacrifice. Eating at restaurants. A lot of people I ... while. but you don't need a treat for yourself. And here's why.",
  "only take"),
 ("rest2", "C1511", "When you're going to restaurants, they", "home to that extent.", 1488.8,
  "When you're going to restaurants, they don't care about your long -term fitness goals. They only ... would never load up your own food at home to that extent.",
  "only take"),
 ("rest3", "C1511", "Now, obviously we can combat this", "very short term sacrifice.", 1522.0,
  "Now, obviously we can combat this somewhat with abs by AI. We're not just leaving those ... option. And this is going to be a very short term sacrifice.",
  "only take"),
 ("junk1", "C1511", "The next thing you need to", "can on your health.", 1570.6,
  "The next thing you need to sacrifice is the junk food, the chips, the candy, the ... food until you're spending all the money you can on your health.",
  "only take"),
 ("vac1", "C1511", "The final thing you need to", "me tell you why.", 1612.3,
  "The final thing you need to sacrifice if you're not spending everything you need to on ... deserve a break once you're ripped. And let me tell you why.",
  "only take"),
 ("vac2", "C1511", "When you go on vacation, the", "health habits dialed in.", 1631.3,
  "When you go on vacation, the usual rules of working out and eating for most people ... when you're ripped and when you have your health habits dialed in.",
  "only take"),
 ("vac3", "C1511", "Furthermore, sacrificing just one vacation for", "get tremendous, tremendous results.", 1676.8,
  "Furthermore, sacrificing just one vacation for the year frees up $5 ,000, $10 ,000, $15 ,000 ... of money in your health, you're going to get tremendous, tremendous results.",
  "only take"),
 ("ther1", "C1511", "And here's one more thing that", "therapy and the medication.", 1694.7,
  "And here's one more thing that you should sacrifice that's going to be a little bit ... easier even if you have to sacrifice the therapy and the medication.",
  "only take; his 'I'm not a psychologist, this is not medical advice' stays"),
 ("ther2", "C1511", "Now again I'm not telling you", "of the higher priority.", 1740.8,
  "Now again I'm not telling you you've got to sacrifice that permanently I'm just telling you ... can reinvest in that once you've taken care of the higher priority.",
  "only take"),
 ("more1", "C1511", "So, things that make you fat,", "reducing your car payment.", 1766.1,
  "So, things that make you fat, psychiatric medication, junk food, going to the club, these are ... subscriptions, your Netflix. You should be thinking about reducing your car payment.",
  "only take"),
 ("more2", "C1511", "You should be thinking about not", "dates until you're ripped.", 1798.3,
  "You should be thinking about not spending any further money on clothing until you're ripped. You should be thinking about not going on any expensive dates until you're ripped.",
  "only take"),
 ("more3", "C1511", "again, sacrifices temporarily. It'll just be", "in a couple months.", 1810.7,
  "again, sacrifices temporarily. It'll just be for a few months, and you'll be so glad you did once you're there in a couple months.",
  "second run of 'Again, sacrifices temporarily' (the first stopped at 'It's only gonna be for,')"),
 ("home1", "C1511", "All right. So let me walk", "life depends on it.", 1843.6,
  "All right. So let me walk you through it. I'll walk you through every level of ... get this basic home workout setup because my life depends on it.",
  "only take"),
 ("home2", "C1511", "So I'm going to link to", "that stuff right now.", 1885.4,
  "So I'm going to link to another video where I show you this in more detail. ... don't even watch the rest, go and buy that stuff right now.",
  "second start of 'So I'm going to link to another video' (the first drifted off at 'the type of things'). Ends at 'go and buy that stuff right now.': the two sentences after it ('steal this stuff from the store if you have to ...') he replaced himself after the cameraman's question"),
 ("home3", "C1511", "Now I'm saying you need this", "the most important thing.", 1939.0,
  "Now I'm saying you need this stuff, your life depends on it. So even if you ... endorsing stealing, I'm just saying your life is the most important thing.",
  "his retake of the ending ('let me do another take like that'): the last take"),
 ("food1", "C1511", "Here's the next thing that you", "the standard American diet.", 1978.6,
  "Here's the next thing that you need to invest in if you're broke. Basic healthy food. ... going to save you money compared to eating the standard American diet.",
  "only take. 2001.5 to 2009.7 s left out: an aside to the cameraman about junk food prices, with the cameraman answering"),
 ("food2", "C1511", "if you're broke right now, you", "eating the standard diet.", 2013.0,
  "if you're broke right now, you don't need to go luxury or organic. You can get ... and it will save you money compared to eating the standard diet.",
  "only take; the stand-alone 'So,' before it (2011.9 s, then a 0.7 s pause) is left out: it made a 0.8 s shot"),
 ("food3", "C1511", "So, no matter how broke you", "to buy junk food.", 2056.6,
  "So, no matter how broke you are, you're buying that home workout setup and you are ... Start thinking instead, I don't have enough money to buy junk food.",
  "only take"),
 ("mid1", "C1511", "Okay, so now that I told", "that money can buy.", 2089.3,
  "Okay, so now that I told y 'all brokies what you need to buy, let me ... if you're middle class is the best protein that money can buy.",
  "only take"),
 ("prot1", "C1511", "So, for me personally, my favorite", "feel like a sacrifice.", 2113.1,
  "So, for me personally, my favorite protein is wild -caught Alaskan sockeye salmon, cost about $20 ... gonna feel like a privilege. It's not gonna feel like a sacrifice.",
  "only take"),
 ("prot2", "C1511", "Now, I hear you middle class", "out your health spending.", 2170.4,
  "Now, I hear you middle class people thinking like, oh, Dan, I don't have the money ... retirement account, middle class people, unless you're maxing out your health spending.",
  "only take"),
 ("matt1", "C1511", "Number two thing you middle class", "a better mattress immediately.", 2269.5,
  "Number two thing you middle class people need to spend more money on is your mattress. ... money, cash out your retirement account and buy a better mattress immediately.",
  "only take"),
 ("matt2", "C1511", "If you buy a better mattress,", "definitely worth the investment.", 2315.8,
  "If you buy a better mattress, you're going to immediately begin getting a little bit better ... that small improvement in your sleep is definitely, definitely worth the investment.",
  "only take"),
 ("matt3", "C1511", "So, what mattress should you buy?", "like a normal mattress.", 2349.2,
  "So, what mattress should you buy? Now, there is some preference to this. Some people have ... gel grid. It's not a set of springs like a normal mattress.",
  "only take", 2374.8, None),
 ("matt4", "C1511", "And this has a few advantages", "lasts about 7 years.", 2376.7,
  "And this has a few advantages over a regular mattress. Springs wear out over time, especially ... can last 20 years. A regular mattress only lasts about 7 years.",
  "only take"),
 ("matt5", "C1511", "The Purple Mattress has another important", "years old spring mattress.", 2416.8,
  "The Purple Mattress has another important benefit which is that it absorbs fluids to a much ... bit more if you're sleeping on a filthy, years old spring mattress.",
  "only take"),
 ("matt6", "C1511", "So, clean up your hygiene, make", "mattress money can buy.", 2480.5,
  "So, clean up your hygiene, make it a little bit less disgusting, get sick less, have less back pain, sleep more, and just spend everything you can on the best mattress money can buy.",
  "only take"),
 ("gym1", "C1511", "The next thing you have to", "has the best people.", 2498.7,
  "The next thing you have to invest in is a gym membership at the best gym ... matter as much. I mean the gym which has the best people.",
  "only take"),
 ("gym2", "C1511", "Now why is a gym membership", "work out from home?", 2516.8,
  "Now why is a gym membership important when you can just work out from home?",
  "only take"),
 ("gym3", "C1511", "There's a couple reasons why it's", "the most ripped people.", 2525.5,
  "There's a couple reasons why it's worth making the investment in a good gym membership. First ... the best equipment. Go for the gym with the most ripped people.",
  "take 2 of 2 of 'There's a couple reasons why it's worth making the investment in a good gym membership' (same words as take 1 at 2520.7 s; the last take)"),
 ("sleep1", "C1511", "Here's the next thing you middle", "data with no subscription.", 2664.0,
  "Here's the next thing you middle class guys need to be investing in, a sleep tracker. ... month and get better data than have worse data with no subscription.",
  "only take"),
 ("sleep2", "C1511", "So, if you don't have anything", "need to get that.", 2708.2,
  "So, if you don't have anything to track your sleep right now, you need to get that.",
  "only take. The next sentence, 'Your three options are the Oura Ring, my preferred option, the Whoop.' (2712.2 to 2716.4 s), is left out: it introduces the Oura Ring again 26 s after he did (Dan's flag on the old edit)"),
 ("sleep3", "C1511", "The Whoop is a thin wearable,", "than any wrist tracker.", 2716.7,
  "The Whoop is a thin wearable, significantly less bulky and more comfortable than the Apple Watch ... shown that the finger is significantly more accurate than any wrist tracker.",
  "only take"),
 ("sleep4", "C1511", "So, if you have the money,", "a ring at night", 2767.4,
  "So, if you have the money, do what I do. Apple watching the day or a ring at night",
  "only take; 'So,' is on the lav 0.4 s before Whisper puts it (in measured)", None, 2767.28),
 ("sleep5", "C1511", "Or if you're a little shorter", "done at all times.", 2774.7,
  "Or if you're a little shorter on funds, the whoop gets the job done at all times.",
  "second start of 'or if you're a little shorter on funds' (the first 'or if you're' stopped; Whisper had folded the restart into one 1.8 s word, and the old edit kept both)"),
 ("glp1", "C1511", "All right, here's the next thing", "happens to your productivity.", 2784.2,
  "All right, here's the next thing you need to be putting your money into. GLP, weight ... couple months, you will be shocked at what happens to your productivity.",
  "only take"),
 ("glp2", "C1511", "When you're on these GLPs, it", "on the appropriate dose.", 2856.4,
  "When you're on these GLPs, it reduces the food noise so much. Now, even for me, ... don't feel hungry when you're fasting, when you're on the appropriate dose.",
  "only take"),
 ("glp3", "C1511", "Terezepatide also reduces your desire to", "anything in the net.", 2894.5,
  "Terezepatide also reduces your desire to waste money on things like alcohol, on things like going ... break even and it won't really cost you anything in the net.",
  "only take"),
 ("glp4", "C1511", "And again, if you have a", "your finances as well.", 2944.4,
  "And again, if you have a savings account, if you have retirement savings, if you have ... live a great life and that will benefit your finances as well.",
  "only take"),
 ("trt1", "C1511", "Here's the next thing you middle", "absolutely changed their life.", 2966.8,
  "Here's the next thing you middle class guys need to buy. TRT. Now, I haven't started ... people who have gone on TRT and it absolutely changed their life.",
  "only take"),
 ("trt2", "C1511", "Now, again, this isn't very expensive", "have an immediate payoff.", 2984.8,
  "Now, again, this isn't very expensive when you consider the benefits, but when some people see ... and immediate investment in your health that's gonna have an immediate payoff.",
  "only take"),
 ("trt3", "C1511", "And think about the long term", "having to work less?", 3014.5,
  "And think about the long term as Well what effect is it going to have getting ... more productive and getting more work done while having to work less?",
  "only take"),
 ("trt4", "C1511", "Now if you're a man in", "and make it happen.", 3033.3,
  "Now if you're a man in your 40s and 50s, if you've been tested and you ... sacrificed aside from the necessities we mentioned before and make it happen.",
  "only take"),
 ("supp1", "C1511", "Here's the final thing you need", "to be investing in", 3056.1,
  "Here's the final thing you need to be investing in",
  "EARLIER take on purpose: 'Here's the final thing you need to be investing in', cut before 'if,'. The retake runs straight into 'if you're middle class', which Dan cut from the old edit, and has no gap to cut it at; this take has a measured 80 ms gap after 'in'", 3058.19, None),
 ("supp2", "C1511", "supplements. Now, I personally take 10", "very expensive at all.", 3062.5,
  "supplements. Now, I personally take 10 supplements per day. I'm spending a lot of money on ... buy even if you're middle class that aren't very expensive at all.",
  "only take"),
 ("supp3", "C1511", "The first supplement that you need", "and start living better", 3077.9,
  "The first supplement that you need to buy is a fish oil or Omega supplement. This ... vitamin D and then save yourself some money and start living better",
  "only take. 'So go and buy yourself some vitamin D if you're middle class' (3167.5 to 3172.1 s, with a false start) left out: it repeats the sentence before it"),
 ("supp4", "C1511", "Now the third thing I think", "sacrificing something not essential.", 3182.1,
  "Now the third thing I think everybody needs is a magnesium supplement. Studies show that about ... you can afford to do that by just sacrificing something not essential.",
  "only take"),
 ("rich1", "C1511", "Alright so that's what you middle", "10 grand a month.", 3233.9,
  "Alright so that's what you middle class guys should be buying. So now let's talk about ... to you guys who are making more than 10 grand a month.",
  "only take"),
 ("rich2", "C1511", "anyone making more than $10 ,000", "workout every single time.", 3251.6,
  "anyone making more than $10 ,000 per month should be considering spending money on what I'm ... what it took so I got a great workout every single time.",
  "second start ('Anyone spending more than 10 grand a month should be considering,' was the slip: spending for making)"),
 ("rich3", "C1511", "Now if you're a baller if", "benefits to doing this.", 3316.1,
  "Now if you're a baller if you have very limited time if you're working all the ... to your own music. There's a lot of benefits to doing this.",
  "only take"),
 ("rich4", "C1511", "now, those of you guys who", "also a gym membership.", 3362.4,
  "now, those of you guys who are ballers, I want you to consider doing what I'm ... the money for it, home gym and then also a gym membership.",
  "second 'now' (the first, at 3360.3 s, stood alone before a pause)"),
 ("chef1", "C1511", "Here is the next thing that", "doing higher value work.", 3415.7,
  "Here is the next thing that you need if you're making more than $10 ,000 a ... focus on your health or you focus on doing higher value work.",
  "second start (the first said 'if you're ripped')"),
 ("chef2", "C1511", "so what I do every other", "right here in Austin,", 3451.1,
  "so what I do every other week is I have a meal prep service called Clean Eats, great meal prep service right here in Austin,",
  "EARLIER take on purpose: 'so what I do every other week is I have a meal prep service called Clean Eats, great meal prep service right here in Austin'. The last take (3461.0 s) drops 'what I do every other week', which the later line 'I am still cooking every other week' leans on", 3457.0, None),
 ("chef3", "C1511", "For about $120 per week, I", "service is worth it.", 3465.5,
  "For about $120 per week, I can get a week's worth of meals that I eat. ... So making that investment in a meal prep service is worth it.",
  "only take"),
 ("chef4", "C1511", "Now for me, I am still", "the way to go.", 3506.6,
  "Now for me, I am still cooking every other week for now because I'm high maintenance, ... that. But if you're a real baller, that's the way to go.",
  "only take", 3524.32, None),
 ("chef5", "C1511", "that's the way that the guys", "make eating healthy easy.", 3526.5,
  "that's the way that the guys I know who are multi -millionaires and ripped, that's the ... foods with premium protein. That is how you make eating healthy easy.",
  "second start of 'that's the way that the guys I know' ('That's the guys,' was the stumble)"),
 ("maid1", "C1511", "The next thing that you need", "time into working out", 3548.1,
  "The next thing that you need if you're rich is someone to take care of other ... if you got the money invest that extra time into working out",
  "second start (the first stopped at 'someone to take care of.')"),
 ("coach1", "C1511", "Now the final thing you should", "if you're a multimillionaire.", 3595.4,
  "Now the final thing you should consider if you're a real baller is a personal trainer ... of money, then it can be worth it if you're a multimillionaire.",
  "only take"),
 ("beyond1", "C1511", "So that is what you need", "little bit more speculative.", 3695.5,
  "So that is what you need to be spending your money on if you are a ... benefit. Once we get beyond this, it's a little bit more speculative.",
  "only take"),
 ("beyond2", "C1511", "So, if you want to invest", "may improve your health.", 3742.3,
  "So, if you want to invest beyond this, there are things like expensive red light therapy ... on supplements and peptides and other things which may improve your health.",
  "only take"),
 ("beyond4", "C1511", "Now what I recommend for you", "Brian Johnson's YouTube channel", 3779.1,
  "Now what I recommend for you guys who want to invest Millions in your health and want to take your health to the next level is to check out Brian Johnson's YouTube channel",
  "the last take of the Bryan Johnson recommendation. His first run at it (3768.7 to 3777.9 s: 'Now, if you guys wanna go beyond this, then this is a little bit beyond the scope of this video. But what I recommend for those of you guys who ...') he abandoned and restarted from 'Now'; it would also be the third 'if you want to go beyond this' in 45 s"),
 ("beyond5", "C1511", "So, Brian Johnson is a guy", "Brian Johnson level stuff.", 3798.7,
  "So, Brian Johnson is a guy who's dedicated to this idea of living forever and spending ... mega baller, and then you can consider the Brian Johnson level stuff.",
  "second 'So,' (the first, at 3793.3 s, stood alone)"),
 ("sum1", "C1511", "All right, so let's summarize everything", "you should be buying.", 3839.6,
  "All right, so let's summarize everything and wrap this video up. You need to be spending ... laid out the whole list of things that you should be buying.",
  "only take"),
 ("sum2", "C1511", "You should be investing $500 to", "your hands on it.", 3897.0,
  "You should be investing $500 to $1000 in your health every month buying the things on ... health if there's any way you can get your hands on it.",
  "retake of 'You should be investing $500 to $1000 in your health every month' (the first ended on a slip, 'on those lips')"),
 ("sum3", "C1511", "for those of you guys making", "and make it happen.", 3924.2,
  "for those of you guys making more than $10 ,000 a month, a home gym, a ... So if you've got the money, spend it and make it happen.",
  "second start (the first stopped at 'a home gym,')"),
 ("cta", "C1511", "Alright guys, that's today's video. If", "in the next video.", 4062.3,
  "Alright guys, that's today's video. If you want to get started building your dream body and ... you for watching guys, and I'll see you in the next video.",
  "take 2 of 2 of the close, the last and clean, one unbroken run (take 1, 3966 to 4046 s, has three restarts inside it)"),
]
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def find(roll, phrase, after, last=False):
    """index range (i, j) of the phrase's words in WORDS for this roll, first match starting at or after `after` (global s)"""
    toks = [norm(x) for x in phrase.split() if norm(x)]
    idx = [k for k, w in enumerate(WORDS) if w["roll"] == roll and norm(w["word"])]
    for a in range(len(idx)):
        if WORDS[idx[a]]["start"] < after - 0.6: continue
        k = a; ok = True
        for t in toks:
            acc = ""
            while k < len(idx) and len(acc) < len(t):
                acc += norm(WORDS[idx[k]]["word"]); k += 1
            if acc != t: ok = False; break
        if ok: return idx[a], idx[k-1]
    raise ValueError(f"phrase not found: {roll} {phrase!r} after {after:.1f}")
_lav = None
def lav():
    global _lav
    if _lav is None:
        wv = wave.open(f"{W}/lav.wav"); _lav = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    return _lav
def rms_db(t0, t1, sr=48000):
    a = lav()[int(t0*sr):int(t1*sr)]
    return 20*np.log10(np.sqrt(np.mean(a*a))+1e-9) if len(a) else -120
def _db(t, n=0.02): return rms_db(t, t+n)
def onset(w0, lo):
    """speech onset of the first kept word: Whisper folds a pause into a stretched word, so walk BACK from inside the word
    (its last 0.12 s) while the lav is loud; a dip under 60 ms is a stop consonant, not the edge. Never before `lo`."""
    t = max(w0["start"]+0.05, w0["end"]-0.12) if w0["end"]-w0["start"] > 0.45 else w0["start"]+0.10
    if _db(t) <= THR:
        while t < w0["end"] and _db(t) <= THR: t += 0.01
    quiet = 0.0
    while t > lo:
        if _db(t-0.02) > THR: quiet = 0.0
        else:
            quiet += 0.01
            if quiet >= 0.07: t += quiet; break
        t -= 0.01
    return max(lo, t-0.08)
def offset(w1, hi):
    """end of the last kept word: walk forward from near its end while the lav is loud (soft tails), then 0.12 s of room"""
    t = w1["end"]-0.15
    while t < min(hi, w1["end"]+0.55) and max(_db(t), _db(t+0.02), _db(t+0.04), _db(t+0.06)) > THR: t += 0.01
    return min(hi, max(t+0.12, w1["end"]+0.10))
def pieces():
    out = []
    for row in PIECES:
        pid, roll, p_in, p_out, hint, txt, why = row[:7]; off = ROLLS[roll]["f0"]/FPS
        i0, i1 = find(roll, p_in, hint+off)
        if norm(p_out) and not norm(p_in).endswith(norm(p_out)): j0, j1 = find(roll, p_out, WORDS[i0]["start"])
        else: j1 = i1
        w0, w1 = WORDS[i0], WORDS[j1]
        prev_end = WORDS[i0-1]["end"] if i0 and WORDS[i0-1]["roll"] == roll else off
        prev_dur = (WORDS[i0-1]["end"]-WORDS[i0-1]["start"]) if i0 else 0
        lo = prev_end+0.02 if prev_dur <= 0.8 else w0["start"]-0.45            # rule 4: do not clamp to a stretched previous word
        nxt = WORDS[j1+1]["start"] if j1+1 < len(WORDS) and WORDS[j1+1]["roll"] == roll else (ROLLS[roll]["f0"]+ROLLS[roll]["n"])/FPS
        sa = onset(w0, max(off, lo)); sb = offset(w1, nxt-0.04 if nxt - w1["end"] > 0.10 else nxt+0.25)
        if len(row) > 7 and row[7] is not None: sb = row[7]+off
        if len(row) > 8 and row[8] is not None:
            if isinstance(row[8], str):
                _, a, b = row[8].split(":"); t = float(a)+off
                while t < float(b)+off and not (_db(t) > THR and _db(t+0.02) > THR and _db(t+0.04) > THR): t += 0.01
                sa = t-0.10
            else: sa = row[8]+off
        out.append(dict(id=pid, roll=roll, word_in=round(w0["start"], 3), word_out=round(w1["end"], 3), **{"in": round(sa, 3), "out": round(sb, 3)},
                        local_in=round(sa-off, 3), local_out=round(sb-off, 3), text=txt, why=why,
                        heard=" ".join(w["word"].strip() for w in WORDS[i0:j1+1])))
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    json.dump([dict(piece=p["id"], roll=p["roll"], source_in=p["local_in"], source_out=p["local_out"], script_beat=p["text"], why=p["why"]) for p in P],
              open(f"{W}/take_map.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P:
        h = p["heard"].split()
        print(f"{p['id']:5s} {p['roll']} {p['local_in']:8.2f} {p['local_out']:8.2f} {p['out']-p['in']:6.1f}s ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f})  {' '.join(h[:5])} ... {' '.join(h[-4:])}")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
