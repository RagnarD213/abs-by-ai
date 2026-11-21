"""Complete B from the R1 approved compositor, header, moving card and untouched parent mix."""
from pathlib import Path
import sys,json,subprocess,os,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import packet as P
R=P.WORK.parent/'round2';OUT=R/'build';OUT.mkdir(exist_ok=True);P.OUT=OUT
q=dict(id='B-full-final5',header_id='B-full',header_ss=1.1,S='B',a=455.20,b=489.1,card=[458.1029,471.60446666666667],text="How much protein should you be aiming for? Studies have shown the optimal amount of protein to eat is about 0.8 grams of protein per pound of body weight. So let's say you're 200 pounds. That means aim for 160 grams of protein per day. So that basically means you're gonna be having three meals each with a larger than average serving of protein where you're making effort to get more protein in. And you're having a protein shake or protein heavy snack like chicken throughout the day. So I would say err on the side of eating more protein rather than less.")
owner=json.loads((R/'round-controller.json').read_text());assert owner['phase']=='complete' and owner['productionOwner']=='01a19c6e-4550-7283-a7cb-b9db7c442d0f'
# Fixed window per actual parent camera size; avoid recenter jumps at metadata-only shot rows.
P.cx_expr=lambda a,b: "if(lt(n,100),642.0,if(lt(n,897),577.0,562.0))"
P.preview(q,{'B':R.parent/'round1/asset-review/hf/renders/card-B-v2.mov'})
src=OUT/'B-full-final5-context.mp4';dest=R/'review/Keep Your Muscle - B - Daily Protein - R2.mp4'
if not dest.exists():shutil.copyfile(src,dest)
(OUT/'B-spec.json').write_text(json.dumps(q,indent=2)+'\n')
print('COMPLETE_B_RENDERED',dest,flush=True)
