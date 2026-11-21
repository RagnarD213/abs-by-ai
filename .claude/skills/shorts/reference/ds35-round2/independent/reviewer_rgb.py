from pathlib import Path
import os,sys,json,subprocess,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
cv2.setNumThreads(1)
W=Path('/Volumes/Expansion/_edit_work/DS-35/round2');v=sys.argv[1];out=W/'independent'/v;out.mkdir(exist_ok=True,parents=True);q=W/'qa'/v
p=json.loads((q/'plan.json').read_text());e=json.loads((W/v/'edl.json').read_text());L=json.loads((W/v/'r2-layout.json').read_text());FPS=30000/1001
sys.path.insert(0,str(W/'recipe'));import clip_ds35 as C
FF='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg';video=W/'review/media'/('dad-bod-r2-'+v+'.mp4')
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
proc=subprocess.Popen([FF,'-v','error','-i',str(video),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
rows=[];diff=[];prev=None;proof=[];thumbs=[];ca,cb=L['comparison']
for g in range(e['total_frames']):
 b=proc.stdout.read(1080*1920*3);assert len(b)==1080*1920*3,(g,len(b));im=np.frombuffer(b,np.uint8).reshape(1920,1080,3);small=cv2.resize(im,(90,160));
 diff.append(float(np.mean(np.abs(small.astype(float)-prev))) if prev is not None else None);prev=small.astype(float)
 if g%15==0:thumbs.append((g,Image.fromarray(im).resize((162,288))))
 if ca<=g<cb or any(round(a*FPS)<=g<round(b*FPS) for a,b in p['covered'] if a>16.0 and abs(a-ca/FPS)>.001):continue
 if g<284:
  c=next(c for c in e['clip']['segs'] if c['n0']<=g<c['n0']+c['frames']);t=c['clip_in']+(g-c['n0'])/FPS
  expected=C.view(26.02+(g-69)/FPS,camera_t=26.02) if 67<=g<69 else C.view(t)
  y0=1280;x0=0;roi=im[y0:1920,:432];exp=(expected[y0:1920,:432]*255).astype(np.uint8);mask=(np.max(abs(roi.astype(np.int16)-exp.astype(np.int16)),axis=2)>32).astype(np.uint8);kind='corner'
 elif g<ca:
  if g<469:c=next(c for c in e['clip']['segs'] if c['n0']<=g<c['n0']+c['frames']);t=c['clip_in']+(g-c['n0'])/FPS
  else:t=e['tr']['clip_in']+(g-469)/FPS
  exp=cv2.resize(C.frame(t),(1080,608),interpolation=cv2.INTER_AREA)*255;y0=92;x0=0;roi=im[92:700];mask=(np.max(abs(roi.astype(np.float32)-exp),axis=2)>32).astype(np.uint8);kind='panel'
 else:
  y0=0;x0=0;roi=im[:850];r,gg,bb=[roi[:,:,i].astype(np.int16) for i in range(3)];mask=((r-bb>-12)&(r-gg>-15)&(np.max(roi,axis=2)<110)).astype(np.uint8);kind='field'
 mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8));n,lab,st,ct=cv2.connectedComponentsWithStats(mask,8)
 ids=[i for i in range(1,n) if st[i,4]>80 and (kind!='panel' or st[i,1]+st[i,3]>=606)]
 if not ids:rows.append(dict(g=g,t=g/FPS,kind=kind,valid=False));continue

 if kind in ['field','corner']:
  ids=[i for i in ids if st[i,4]>400 and (kind!='field' or st[i,1]<450)]
  if not ids:rows.append(dict(g=g,t=g/FPS,kind=kind,valid=False));continue
  k=min(ids,key=lambda i:st[i,1])
 else:k=max(ids,key=lambda i:st[i,4])
 xx,yy,ww,hh,ar=map(int,st[k]);hy=y0+yy
 # Head horizontal centre: the top120px of the isolated hair component; source-independent actual RGB.
 ys,xs=np.where((lab==k)&(np.indices(lab.shape)[0]<yy+(100 if kind=='corner' else 150)))
 cx=float((xs.min()+xs.max())/2+x0);rows.append(dict(g=g,t=g/FPS,kind=kind,valid=True,hair_top=hy,head_x=cx,bbox=[xx+x0,hy,ww,hh]))
 if g in [0,68,284,417,425,485,507,616,755,849,902,1078,1133,1237,1239,1287,1352,1551,1609,1662,1702]:
  pth=out/f'calibration-{g:04d}.png';pi=Image.fromarray(im.copy());draw=ImageDraw.Draw(pi);draw.line((0,hy,1080,hy),fill='lime',width=2);draw.line((cx,hy,cx,hy+160),fill='yellow',width=2);pi.save(pth);proof.append(str(pth))
assert proc.stdout.read(1)==b'';assert proc.wait()==0
valid=[r for r in rows if r['valid']];full=[r for r in valid if r['kind']=='field'];a=np.array([r['head_x']-540 for r in full]);bad=[];start=None
for i,r in enumerate(full+[None]):
 flag=r is not None and abs(r['head_x']-540)>60
 if flag and (start is None or r['g']!=full[i-1]['g']+1):
  if start is not None and i-start>=30:bad.append([full[start]['t'],full[i-1]['t']+1/FPS])
  start=i
 elif not flag and start is not None:
  if i-start>=30:bad.append([full[start]['t'],full[i-1]['t']+1/FPS])
  start=None
stats=dict(frames=len(diff),valid=len(valid),invalid=[r for r in rows if not r['valid']],per_kind={k:dict(n=len(rr),min_hair=min(x['hair_top'] for x in rr),max_hair=max(x['hair_top'] for x in rr)) for k in ['corner','panel','field'] if (rr:=[x for x in valid if x['kind']==k])},field_head_offset=dict(n=len(a),median=float(np.median(a)),median_abs=float(np.median(abs(a))),p95_abs=float(np.percentile(abs(a),95)),max_abs=float(max(abs(a))),sd=float(np.std(a)),over60_fraction=float(np.mean(abs(a)>60)),over60_runs_1s=bad),frame_diff=dict(min=min(x for x in diff[1:]),median=float(np.median(diff[1:])),black_frames=[]))
(out/'rgb-analysis.json').write_text(json.dumps(dict(video_sha256=sha(video),method='Sequential native1080x1920 decoded RGB, allframe90x160 motion scan. Actual RGB hair components calibrated independently: opening residual vs independently decoded native source view in real corner ROI; panel residual vs actual native source16:9 component with connected hair reaching panel bottom; SoftBlue field color separation (neutral-dark vs blue), no source alpha or geometry rows used.',calibration=proof,stats=stats,rows=rows,frame_diff=diff),indent=1))
for s in range(0,len(thumbs),40):
 seq=thumbs[s:s+40];sheet=Image.new('RGB',(8*162,5*310));draw=ImageDraw.Draw(sheet)
 for i,(g,thumb) in enumerate(seq):x=i%8*162;y=i//8*310;sheet.paste(thumb,(x,y+22));draw.text((x,y),f'{g/FPS:.3f} f{g}',fill='white')
 sheet.save(out/f'chronological-{s//40:02d}.jpg')
print(json.dumps(stats,indent=2))
