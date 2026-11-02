from pathlib import Path
WORK = "/Volumes/Extreme/_edit_work/SL-13/round1"
STOCK=WORK+"/clips/"
DISC={}; PICKUP={}; WORDFIX={}; KEEP=.90; TRIM={}; SPLIT={}; SHOTS={"A":{3:dict(win="mid")}}
Y0={"full":68,"mid":76}
SEG={"A":[[318.35,367.38],[376.10,384.78]]}
NAME={"A":"calories-dont-matter-short1_eat-protein-first"}
TITLE={"A":("FAT LOSS",["Eat Protein First To Keep","Muscle While Losing Fat"])}
COVERS={"A":[
 dict(id="protein-open",a=318.35,b=322.20,src=STOCK+"p38757135.mp4",t=1.0,fx=.50),
 dict(id="bread",a=332.85,b=334.37,src=STOCK+"p5116397.mp4",t=3.0,fx=.50),
 dict(id="study",a=351.85,b=363.55,src=WORK+"/build/A/hf/renders/protein-study-v2.mov",t=0,fx=.5,matrix="bt601"),
 dict(id="eggs",a=376.10,b=380.33,src=STOCK+"eggs-parent.mp4",t=0,fx=.5)
]}
BARS={"A":[
 dict(id="G1",topic="CALORIES BURNED DIGESTING",parts=[["Protein: 20–30%","your body burns"],["Carbs: 5–10%","With carbs"]],a=-.15,b=1.8),
 dict(id="G2",topic="EVERY MEAL",parts=[["Protein First.","Get your protein"],["Then Fit In Your Carbs.","then fit your carbs"]],a=-.1,b=3.0)
]}
TEXT={'A': "Let me give you two reasons why protein matters outside of calories. The first one is that your body burns about 20-30%{twenty to thirty percent} of the calories in protein just digesting it. With carbs, it's 5-10%{five to ten percent}. So 200{two hundred} calories of chicken and 200{two hundred} calories of bread aren't the same thing once they're inside your body. The second reason is muscle. Researchers at McMaster University put two groups of young men on the same brutal diet with the same hard workouts for four weeks. The only difference was protein. One group ate twice as much as the other. The high protein group lost about 10.5{ten point five} pounds of fat and they gained 2.5{two point five} pounds of muscle. The lower protein group lost about 8{eight} pounds of fat and they didn't gain any muscle at all. Those were the same calories and the high protein guys ended up with a completely different body. | So every meal you eat needs a big serving of meat, fish or eggs. Get your protein in first then fit your carbs into whatever calories you have left."}
