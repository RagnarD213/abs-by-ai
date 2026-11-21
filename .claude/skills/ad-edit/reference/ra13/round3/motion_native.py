from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import landing
F=30000/1001;report=[];proof=json.load(open(O/'crop-quantization-proof.json'))
for r in json.load(open(O/'framing.json')):
 if r['format']!='9':continue
 n=np.arange(r['n']);tn=np.array(r['track']['n']);tx=np.array(r['track']['crop_center']);th=np.array(r['track']['head']);cw=r['crop'][0];left=np.empty(len(n))
 for j in range(len(tn)-1):
  a,b=tn[j],tn[j+1];m=(n>=a)&(n<b);left[m]=round(float(tx[j]-cw/2),4)+round(float(tx[j+1]-tx[j]),4)*(n[m]-a)/(b-a)
 left[n>=tn[-1]]=tx[-1]-cw/2;actual_left=np.rint(left);actual_center=actual_left+cw/2
 anchor=next(p for p in proof if p['name']==r['name']);assert actual_left[0]==anchor['best_integer_left'],(r['name'],actual_left[0],anchor)
 stats=landing.motion_stats(n,np.interp(n,tn,th),actual_center,[dict(n0=0,n1=r['n'])],cw,F)
 report.append(dict(name=r['name'],frames=r['n'],source0=r['src0'],crop_width=cw,source_pixel_space=[2160,3840],frame_rate=F,actual_first_crop_left=float(actual_left[0]),actual_first_crop_center=float(actual_center[0]),whole_head_anchor=r['exact_landing_head_x'],landing_error_source_px=round(float(actual_center[0]-r['exact_landing_head_x']),3),motion=stats))
out=dict(method='Native-frame coordinates from the actual FFmpeg crop expression, rounded to nearest integer source pixel. First-frame integer alignment verified against each independently graded source frame. Head offsets use dense 5 fps source whole-head masks interpolated per frame; finished first-frame masks are checked separately in native-proof/report.json.',registration_proof=str(O/'crop-quantization-proof.json'),rows=report)
(O/'motion-native.json').write_text(json.dumps(out,indent=2));print(json.dumps(report,indent=2))
