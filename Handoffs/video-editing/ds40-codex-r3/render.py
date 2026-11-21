import cv2,numpy as np,subprocess,sys,time,json
from pathlib import Path
from key_v3 import key,stabilize,composite
from grade import grade
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';D.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R3 ten-second render');cv2.setNumThreads(2)
bg=np.load(W/'screen.npy');maker=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
def decoder(name):
 return subprocess.Popen([F,'-v','error','-i',str(W.parent/'round2/review/media'/f'{name}.mp4'),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
def encoder(name,w,h):
 return subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-crf','16','-preset','fast','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(W/f'{name}-picture.mp4')],stdin=subprocess.PIPE)
decs=[decoder('balanced'),decoder('dark')];encs=[encoder('wide',1080,1920),encoder('dark',1080,1920),encoder('hair',1500,900)]
cache={};stats=[];t=time.time();previous=None
# Full replacement above y=960, smooth handover above the forehead. All pixels
# below native y=1120 and outside x350:1850 reuse decoded R2 exactly pre-encode.
y=np.arange(400,1300,dtype=np.float32)[:,None];blend=np.broadcast_to(np.clip((1120-y)/160,0,1),(900,1500));blend=cv2.resize(blend,(750,450),interpolation=cv2.INTER_AREA)[:,:,None]
for i in range(300):
 lo=max(0,i-2);hi=min(300,i+3)
 for j in range(lo,hi):
  if j not in cache:cache[j]=key(np.load(W/'native'/f'{j:03}.npy').astype('float32')/65535,bg)
 for j in list(cache):
  if j<lo:del cache[j]
 items=[cache[j] for j in range(lo,hi)];cur=cache[i];a=stabilize(items,i-lo,maker)
 originals=[];outs=[]
 for z,c in zip(decs,[[.84,.87,.89],[.08,.1,.13]]):
  raw=z.stdout.read(1080*1920*3);assert len(raw)==1080*1920*3
  old=np.frombuffer(raw,'uint8').reshape(1920,1080,3).copy();originals.append(old)
  # Match the existing encoded reference field, avoiding a rectangular tint seam.
  field=np.median(old[20:180,20:160].reshape(-1,3),axis=0)/255
  new=composite(cur,a,bg,field,grade);new=cv2.resize(new,(750,450),interpolation=cv2.INTER_AREA)*255
  out=old.copy();out[200:650,175:925]=np.clip(old[200:650,175:925]*(1-blend)+new*blend+.5,0,255).astype('uint8');outs.append(out)
 for e,out in zip(encs[:2],outs):e.stdin.write(out.tobytes())
 hair=np.concatenate([np.concatenate([originals[0][200:650,175:925],outs[0][200:650,175:925]],1),np.concatenate([originals[1][200:650,175:925],outs[1][200:650,175:925]],1)])
 for text,pos in [('Previous R2 | Light',(20,35)),('Revised R3 | Light',(770,35)),('Previous R2 | Dark',(20,485)),('Revised R3 | Dark',(770,485))]:cv2.putText(hair,text,pos,cv2.FONT_HERSHEY_SIMPLEX,.65,(185,100,40),2)
 encs[2].stdin.write(hair.tobytes())
 # Transparent-hair stability diagnostic at output resolution, same region and
 # correspondence for both keys. This is a comparative measurement, not a gate.
 newa=cv2.resize(a,(750,450),interpolation=cv2.INTER_AREA)
 olda=1-np.mean((originals[0][200:650,175:925].astype(np.float32)-originals[1][200:650,175:925])/255/np.array([.76,.77,.76]),axis=2)
 gray=cv2.resize(cur['gray'],(750,450));spatial=blend[:,:,0]
 if previous is not None:
  yy,xx=np.mgrid[:450,:750].astype('float32');flow=maker.calc(gray,previous[0],None);mx=xx+flow[:,:,0];my=yy+flow[:,:,1]
  pg=cv2.remap(previous[0],mx,my,cv2.INTER_LINEAR).astype(np.float32)
  mask=(newa>.08)&(newa<.95)&(spatial>.99)&(abs(pg-gray)<10)
  row={'frame':i,'pixels':int(mask.sum())}
  for name,aa,pr in [('r2',olda,previous[1]),('r3',newa,previous[2])]:
   wa=cv2.remap(pr,mx,my,cv2.INTER_LINEAR);row[name+'_alpha_residual_mean']=float(np.mean(abs(wa-aa)[mask]))
  stats.append(row)
 previous=(gray,olda,newa)
 if i in [0,30,60,150,240,255,270,299]:
  cv2.imwrite(str(D/f'wide-{i:03}.jpg'),outs[0][:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,97]);cv2.imwrite(str(D/f'hair-{i:03}.jpg'),hair[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,97])
 if i%30==0:print(i,round(time.time()-t,1),flush=True)
for e in encs:e.stdin.close();assert e.wait()==0
for z in decs:assert z.wait()==0
(W/'measurements.json').write_text(json.dumps(stats,indent=2));print('RENDER DONE',flush=True)
