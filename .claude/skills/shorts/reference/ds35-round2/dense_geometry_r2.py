"""Every retained Dan matte posture through the ACTUAL R2 transforms, plus exact encoded worst proofs.
Supplemental evidence, never a private replacement for unchanged shared framing rows.
"""
from pathlib import Path
import sys,json,subprocess,numpy as np
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FPS=30000/1001;sys.path.insert(0,str(W/'recipe'));from qa_full_r2 import sha,video
v=sys.argv[1];d=W/v;q=W/'qa'/v;e=json.loads((d/'edl.json').read_text());L=json.loads((d/'r2-layout.json').read_text());shots=json.loads((d/'shots.json').read_text());crops=json.loads((d/'framing-frames.json').read_text());geo=json.loads((W/'panel-geometry.json').read_text())[v];heads={k:np.load(O/'framing-cache'/(k+'.npy')) for k in ['S','O1','O2','O3','CTA1','CTA2']};watch=np.load(W/'watch-hair-native.npy');ca,cb=L['comparison'];rows=[];holds=[]
for g in range(284,ca):
 if g<485:
  i=g-284;hy,hx=watch[i];s=2/3;x0,y0=geo['watch']['x'],geo['watch']['y'];name='watch';top=hy*s+y0;cx=hx*s+x0
 else:
  sh=shots[0];p=e['pieces'][0];k='S' if v=='scripted' else 'O1';hy,hx=heads[k][g-p['n0']];x,y,cw,ch=crops[sh['id']][g-sh['n0']];s=.82;top=hy*s+geo['response']['y'];cx=(hx-x)*1080/cw;name='response-panel'
 rows.append(dict(g=g,t=g/FPS,hold=name,hair_top_px=float(top),head_centre_x=float(cx),panel_overlap_px=float(700-top)))
for sh in shots:
 if sh['kind']=='photo':continue
 p=next(p for p in e['pieces'] if p['id']==sh['piece']);k=sh['key'];m=heads[k];lo=max(sh['n0'],cb);hi=sh['n1'];rr=[]
 for g in range(lo,hi):
  hy,hx=m[g-p['n0']];x,y,cw,ch=crops[sh['id']][g-sh['n0']]
  if sh['card']:
   cw=1000 if sh['size']=='T' else 1240;ch=cw*16/9;yy=float(m[sh['n0']-p['n0']:sh['n1']-p['n0'],0].min())-.035*ch;cx=x+sh['crop_w']/2;x=cx-cw/2;y=yy
  r=dict(g=g,t=g/FPS,hold=sh['id'],hair_top_px=float((hy-y)*1920/ch),head_centre_x=float((hx-x)*1080/cw),effective_crop=[x,y,cw,ch]);rows.append(r);rr.append(r)
 if rr:
  offsets=np.array([abs(r['head_centre_x']-540) for r in rr]);bad=offsets>60;runs=[];start=None
  for i,b in enumerate(list(bad)+[False]):
   if b and start is None:start=i
   elif not b and start is not None:
    if i-start>=FPS:runs.append([rr[start]['t'],rr[i-1]['t']+1/FPS,float(offsets[start:i].max())])
    start=None
  holds.append(dict(hold=sh['id'],frames=len(rr),min_hair_top_px=min(x['hair_top_px'] for x in rr),max_hair_top_px=max(x['hair_top_px'] for x in rr),median_abs_offset_px=float(np.median(offsets)),max_abs_offset_px=float(offsets.max()),offset_over60_runs_at_least1s=runs,worst_hair=min(rr,key=lambda x:x['hair_top_px']),worst_offset=rr[int(offsets.argmax())]))
proof=q/'geometry-proofs';proof.mkdir(exist_ok=True);picks={}
for h in holds:
 for x in [h['worst_hair'],h['worst_offset']]:picks[x['g']]=x
for name in ['watch','response-panel']:
 rr=[x for x in rows if x['hold']==name]
 for x in [min(rr,key=lambda x:x['hair_top_px']),max(rr,key=lambda x:x['hair_top_px'])]:picks[x['g']]=x
for g in sorted(picks):
 f=proof/f'g{g:04d}.png';subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-nostdin','-y','-ss',str(g/FPS),'-i',str(video(v)),'-frames:v','1','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24',str(f)],check=True);picks[g]['actual_encoded_native_proof']=str(f);picks[g]['proof_sha256']=sha(f)
rec=dict(video_sha256=sha(video(v)),scope='Dense source alpha posture transformed through exact R2 picture; actual encoded native worst proofs require visual inspection. Not independent RGB hair-detection clearance.',frames_measured=len(rows),all_transformed_frames=rows,holds=holds,panel_minimum_overlap=min(x['panel_overlap_px'] for x in rows if 'panel_overlap_px' in x),actual_encoded_proofs=list(picks.values()),early_corner_preservation='Same0.40/flush1152 transform on same accepted full-height key caches as R1; native encoded opening/boundary inspection still required.',source_matte_files=[dict(path=str(O/'framing-cache'/(k+'.npy')),sha256=sha(O/'framing-cache'/(k+'.npy'))) for k in heads],inspected=False)
(q/'dense-geometry.json').write_text(json.dumps(rec,indent=1));print('DENSE_SOURCE_GEOMETRY_AND_ENCODED_WORST_PROOFS',v,len(rows),len(picks),flush=True)
