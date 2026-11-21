from pathlib import Path
import json,sys
HF=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes');sys.path.insert(0,str(HF));import vertical as V
out=Path('/Volumes/Extreme/_edit_work/SL-13/round2/build/A/hf');c=json.loads((out/'configs/protein-study.json').read_text())[0];c['id']='protein-study-v2';c['eyebrow']['s']='MCMASTER, 2016'
for row,y,t in zip(c['rows'],[420,585,750,915],[1.64,3.94,7.44,8.84]):row.update(y=y,t=t)
V.build([(HF/'title-card/title-card.template.htm',c,())],out,render=True,snap=10.5)
