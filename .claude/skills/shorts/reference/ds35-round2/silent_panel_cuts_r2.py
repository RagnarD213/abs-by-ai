from pathlib import Path
import json,numpy as np,cv2
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1]
if (W/'silent-panel-native-cuts.json').exists():
 print('Existing exact native-cut analysis reused');raise SystemExit()
O=W.parent/'round1';cache=next(c for c in json.loads((O/'src/clip-caches.json').read_text()) if c['a']==134);m=np.load(cache['file'],mmap_mode='r');out=W/'proofs/silent-panel-native';out.mkdir(exist_ok=True);rows=[]
for candidate in [134.709,136.1688,139.1301]:
 k=round((candidate-cache['frame0_pts'])*cache['fps']);scores=[]
 for j in range(max(1,k-3),min(len(m),k+5)):
  a=m[j-1,::12,::12].astype(float);b=m[j,::12,::12].astype(float);scores.append((float(np.abs(a-b).mean()),j))
 score,j=max(scores);t=cache['frame0_pts']+j/cache['fps'];g=469+int(np.ceil((t-131.21303333333333)*(30000/1001)-1e-7));p=out/f'{j:03d}.jpg';im=np.concatenate([m[j-1],m[j]],axis=1);Image.fromarray(im).save(p,quality=96);rows.append(dict(candidate=candidate,exact_source_after_pts=t,native_cache_index=j,source_file=cache['file'],source_cache_first_pts=cache['frame0_pts'],native_fps=cache['fps'],output_after_frame=g,output_after_seconds=g/(30000/1001),neighbour_scores=scores,pair=str(p),inspected=False))
(W/'silent-panel-native-cuts.json').write_text(json.dumps(rows,indent=2));print(json.dumps([{k:r[k] for k in ['exact_source_after_pts','output_after_frame','pair']} for r in rows],indent=2))
