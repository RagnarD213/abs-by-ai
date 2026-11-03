from pathlib import Path
WORK = "/Volumes/Extreme/_edit_work/SL-13/round2"
STOCK=WORK+"/clips/"
DISC={}; PICKUP={}; WORDFIX={}; KEEP=.90; TRIM={}; SPLIT={}; SHOTS={"A":{3:dict(win="mid")}}
Y0={"full":68,"mid":76}
SEG={"A":[[318.35,367.38],[376.10,384.78]]}
NAME={"A":"calories-dont-matter-short1_eat-protein-first"}
TITLE={"A":("FAT LOSS",["Eat Protein First To Keep","Muscle While Losing Fat"])}
COVERS={"A":[
 dict(id="protein-open",a=318.35,b=322.20,src=STOCK+"p38757135.mp4",t=1.0,fx=.50),
 dict(id="bread",a=332.85,b=334.37,src=STOCK+"p5116397.mp4",t=3.0,fx=.50),
 dict(id="study",a=351.85,b=363.55,src=WORK+"/build/A/hf/renders/protein-study-r2.mov",t=0,fx=.5,matrix="bt601"),
 dict(id="eggs",a=376.10,b=380.33,src=STOCK+"eggs-parent.mp4",t=0,fx=.5)
]}
BARS={"A":[
 dict(id="G1",topic="CALORIES BURNED DIGESTING",parts=[["Protein: 20–30%","your body burns"],["Carbs: 5–10%","With carbs"]],a=-.15,b=1.8),
 dict(id="G2",topic="EVERY MEAL",parts=[["Protein First.","Get your protein"],["Then Fit In Your Carbs.","then fit your carbs"]],a=-.1,b=3.0)
]}
TEXT={'A': "Let me give you two reasons why protein matters outside of calories. The first one is that your body burns about 20-30%{twenty to thirty percent} of the calories in protein just digesting it. With carbs, it's 5-10%{five to ten percent}. So 200{two hundred} calories of chicken and 200{two hundred} calories of bread aren't the same thing once they're inside your body. The second reason is muscle. Researchers at McMaster University put two groups of young men on the same brutal diet with the same hard workouts for four weeks. The only difference was protein. One group ate twice as much as the other. The high protein group lost about 10.5{ten point five} pounds of fat and they gained 2.5{two point five} pounds of muscle. The lower protein group lost about 8{eight} pounds of fat and they didn't gain any muscle at all. Those were the same calories and the high protein guys ended up with a completely different body. | So every meal you eat needs a big serving of meat, fish or eggs. Get your protein in first then fit your carbs into whatever calories you have left."}

# R2 selected B/C, source-silence boundaries protect the full opening and final words.
SEG.update({'B': [[258.14, 302.2], [305.5, 313.78]], 'C': [[494.87, 522.1], [528.82, 560.52]]})
SHOTS.update({"B":{},"C":{}})
NAME.update({'B': 'calories-dont-matter-short2_eat-less-without-counting', 'C': 'calories-dont-matter-short3_keep-your-steps-up'})
TITLE.update({'B': ('FAT LOSS', ['Eat Less Without Counting', 'Every Calorie']), 'C': ('FAT LOSS', ['Keep Your Steps Up', 'While You Diet'])})
TEXT.update({'B': "Researchers at the University of Illinois gave a group of obese adults one rule. They could only eat inside a 4{four} or 6{six} hour window each day. Nobody counted calories, and nobody told them what to eat. After two months, they were eating about 550{five hundred fifty} fewer calories a day without even trying. And they lost about 3%{three percent} of their body weight compared to the group that ate whenever they wanted. Then they ran a bigger study for a full year. One group fasted until noon every single day and never counted a single calorie. Another group counted every calorie they ate. The fasting group ate about 425{four hundred twenty five} fewer calories per day and they lost about 10{ten} pounds more than the people who changed nothing. They did just as well as the calorie counters. | When you've got fewer hours to eat, you eat less and you don't have to fight yourself all day to do it. That's one more reason why I fast until 2{two} every day.", 'C': "The Mayo Clinic overfed a group of people by a thousand calories a day for eight weeks. Everybody got the same extra food. But the fat they gained was wildly different. One person gained less than a pound of fat. Another person gained over nine pounds. That's a ten times difference from the same extra calories. So what was the difference? It was how much they moved around during the day. I don't mean exercise. I mean walking, standing, taking the stairs, and even fidgeting. | When you cut your calories, your body quietly makes you move less. You sit more, you take the elevator, and you don't even notice it happening. That can cancel out a big piece of your deficit. So here's what I would do. Set a minimum number of steps per day and hit it no matter what. I would say 8–10K{eight to ten thousand} is a good target for most of you guys. Walk after dinner, take your phone calls on your feet, and park at the back of the parking lot. Work at a standing desk. It all adds up and it protects your deficit you're working so hard for."})
COVERS.update({'B': [{'id': 'eating-window', 'a': 258.14, 'b': 264.14, 'src': '/Volumes/Extreme/_edit_work/SL-13/round2/build/B/hf/renders/eating-window.mov', 't': 0, 'matrix': 'bt601'}, {'id': 'fasting-fact', 'a': 269.84, 'b': 276.21, 'src': '/Volumes/Extreme/_edit_work/SL-13/round2/build/B/hf/renders/fasting-fact.mov', 't': 0, 'matrix': 'bt601'}, {'id': 'fasting-compare', 'a': 291.26, 'b': 302.2, 'src': '/Volumes/Extreme/_edit_work/SL-13/round2/build/B/hf/renders/fasting-compare.mov', 't': 0, 'matrix': 'bt601'}], 'C': [{'id': 'stairs-open', 'a': 494.87, 'b': 499.87, 'src': '/Volumes/Expansion/_edit_work/ro11/stock/p8550877.mp4', 't': 1, 'fx': 0.5, 'eq': 'eq=brightness=0.015:saturation=1.03'}, {'id': 'movement-fact', 'a': 504.04, 'b': 512.39, 'src': '/Volumes/Extreme/_edit_work/SL-13/round2/build/C/hf/renders/movement-fact.mov', 't': 0, 'matrix': 'bt601'}, {'id': 'steps-list', 'a': 539.57, 'b': 556.6, 'src': '/Volumes/Extreme/_edit_work/SL-13/round2/build/C/hf/renders/steps-list.mov', 't': 0, 'matrix': 'bt601'}]})
BARS.update({"B":[],"C":[]})

COVERS["B"][0]["b"]=267.14

# Native C opening proof: keep the stair walker in-frame from the first useful step.
COVERS["C"][0]["fx"]=0.20

# Internal QA repair: approved closer window for the middle B presenter section.
SHOTS["B"][3] = dict(win="mid")

# Source-projected headroom from the failed gate: 71px full => 67px mid at y84.
SHOTS["B"][3] = dict(win="mid", y0=84)
