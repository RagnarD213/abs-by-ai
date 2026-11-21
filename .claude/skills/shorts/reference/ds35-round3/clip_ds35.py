"""Native 23.976 source sampling and fixed speaker crops per original camera shot.
Relocate the actual celebrity photo pixels, because the portrait crop excludes the original insets.
"""
from pathlib import Path
import json,numpy as np,cv2,sys
from PIL import Image
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W/'recipe'));import house_composite as H
CS=json.loads((W/'src/clip-caches.json').read_text());MAPS={}
# Native boundary pairs inspected in native-camera-pairs-A/B.jpg; fixed windows throughout each original shot.
CAMS=[dict(a=17.0,b=18.018,cx=1030,h=1080),dict(a=18.018,b=19.352666666666664,cx=1040,h=1080),dict(a=19.352666666666664,b=26.0,cx=824,h=1080),
 dict(a=26.0,b=28.57020833333333,cx=900,h=1080),dict(a=28.57020833333333,b=31.114416666666664,cx=1200,h=720),dict(a=31.114416666666664,b=33.36666666666666,cx=900,h=1080),dict(a=33.36666666666666,b=36.0,cx=1200,h=720),
 dict(a=124.0,b=127.21041666666666,cx=1170,h=1080),dict(a=127.21041666666666,b=130.33854166666666,cx=1200,h=1080),dict(a=130.33854166666666,b=134,cx=820,h=1080),dict(a=134,b=145,cx=950,h=1080)]
def frame(t):
 c=next(c for c in CS if c['a']<=t<c['b']);key=c['file']
 if key not in MAPS:MAPS[key]=np.load(key,mmap_mode='r')
 k=int(np.floor((t-c['frame0_pts'])*c['fps']+1e-6));assert -1<=k<c['frames'],(t,k,c)
 return np.asarray(MAPS[key][max(0,k)]).astype(np.float32)/255

def view(t,include_inset=True,camera_t=None):
 ct=t if camera_t is None else camera_t
 c=next(c for c in CAMS if c['a']<=ct<c['b']);h=c['h'];w=h*9/16;x=c['cx']-w/2
 f=frame(t);out=cv2.warpAffine(f,np.array([[1080/w,0,-x*1080/w],[0,1920/h,0]],np.float32),(1080,1920),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
 if include_inset:
  if 26<=ct<35.70233333333333:
   photo=np.asarray(Image.open(W/'assets/Seth-source-inset.png').convert('RGB')).astype(np.float32)/255
   hh=430*photo.shape[0]/photo.shape[1];out=H.draw_card(out,photo,[608,1340,430,hh],r=10,shadow=.5)
  elif 124.0<=ct<130.33854166666666:
   photo=np.asarray(Image.open(W/'assets/Daniel-source-inset.png').convert('RGB')).astype(np.float32)/255
   hh=430*photo.shape[0]/photo.shape[1];out=H.draw_card(out,photo,[608,1390,430,hh],r=10,shadow=.5)
 return np.clip(out,0,1)

if __name__=='__main__':
 for name,t,roi in [('Seth',32.7,[1408,744,1655,1065]),('Daniel',126,[417,741,737,1063])]:
  f=frame(t);x0,y0,x1,y1=roi;im=Image.fromarray(H.u8(f[y0:y1,x0:x1]));im.save(W/'assets'/f'{name}-source-inset.png')
 (W/'clip-camera-plan.json').write_text(json.dumps(CAMS,indent=1))
 # Actual source-aligned watching calibration frame 10 under matching clip time.
 a=json.loads((W/'key/cal_watch/calibration.json').read_text())['excerpts'][0];start=float(a['seek']);i=10;t=start+i/(30000/1001)-291.467375
 out=view(t);d=np.load(Path(a['dir'])/'c15'/f'f{i:04d}.npy').astype(np.float32);H.LOOK='A_natural';fp,al=H.feather(d[...,:3],d[...,3]);out=H.place(out,fp,al,.40*1080/1620,0,1152)
 Image.fromarray(H.u8(out)).save(W/'stills/opening-Seth-real-synced-proof.png')
 sheet=Image.new('RGB',(4*270,3*480),(9,12,20))
 times=[17.5,18.3,19.38,26.4,27.8,29.5,32.7,34.7,125.4,128.4,130.7]
 from PIL import ImageDraw
 d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  im=Image.fromarray(H.u8(view(t))).resize((270,480));sheet.paste(im,(i%4*270,i//4*480));d.text((i%4*270+8,i//4*480+8),str(t),fill='red',stroke_width=1)
 sheet.save(W/'stills/speaker-crop-proof.jpg')
