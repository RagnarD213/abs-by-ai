from pathlib import Path
import json,sys
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
HF=ROOT/'.claude/skills/_shared/hyperframes';sys.path.insert(0,str(HF));import vertical as V
W=Path('/Volumes/Extreme/_edit_work/SL-13/round2')
p=W/'study-config.json'
if not p.exists():p=Path(__file__).parent/'study-config.json'
c=json.loads(p.read_text())[0]
assert c['id']=='protein-study-r2'
V.build([(HF/'title-card/title-card.template.htm',c,())],W/'build/A/hf',render=True,snap=10.5)
