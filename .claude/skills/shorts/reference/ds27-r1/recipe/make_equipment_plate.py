from pathlib import Path
import sys,os,json
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1]
os.environ['GATE_GROUP']='DS-27'
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'))
import vertical as V
scene,hole=V.media_card_scene('EQUIPMENT',6,16/9,kicker='My Home Workout Setup',max_w=1080)
print('HOLE',hole,flush=True)
V.build([scene],W/'hf-equipment',render=True,snap=3)
(W/'equipment-hole.json').write_text(json.dumps(hole))
