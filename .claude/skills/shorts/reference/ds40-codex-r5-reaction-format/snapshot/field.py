from pathlib import Path
import sys
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W=Path(__file__).parent
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V
scene,_=V.media_card_scene('G00',20.02,16/9)
tpl,cfg,assets=scene;cfg['hole']=[0,0,0,0];cfg['radius']=0
V.build([(tpl,cfg,assets)],W/'hf',render=True,snap=1)
