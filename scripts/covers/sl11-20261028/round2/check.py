from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json,hashlib,subprocess,numpy as np
P=Path(__file__).resolve().parents[4];R=P/'Short-form video content/covers/review/sl11-vacuum-20261028/round2';PM=Path.home()/'.cache/absbyai/personmask/personmask'
m=json.loads((R/'manifest.json').read_text());res=[]
for row in m['outputs']:
 p=P/row['path'];pic=p.with_name(p.stem+'-picture.png');mp=p.with_name(p.stem+'-person-mask.png');data=json.loads(subprocess.run([str(PM),str(pic),str(mp)],capture_output=True,text=True,check=True).stdout);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'-text-mask.png')))>0;pm=np.array(Image.open(mp).convert('L'))>127;hits=[]
 for f in data['faces']:
  x,y,x1,y1=f;h=y1-y;w=x1-x;bb=[max(0,x-w//5),max(0,y-h//2),min(1080,x1+w//5),min(1920,y1+h//5)];a,b,c,d=bb;hits.append({'face':f,'expanded_face_and_hair':bb,'text_pixels':int(tm[b:d,a:c].sum())})
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 safe=all(25<=b[0]<b[2]<=1055 and (240 if row['platform']=='instagram' else 50)<=b[1]<b[3]<=(1620 if row['platform']=='instagram' else 1850) for b in row['text_bounds'])
 d={'short':row['short'],'design':row['design'],'platform':row['platform'],'sha256':row['sha256'],'rgb_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'text_band_safe':safe,'faces':hits,'text_person_pixels':int((tm&pm).sum()),'jpeg_under_2MB':(P/row['jpeg_path']).stat().st_size<2_000_000};d['passed']=d['rgb_1080x1920'] and safe and bool(hits) and not any(h['text_pixels'] for h in hits) and d['jpeg_under_2MB'];res.append(d);print(row['short'],row['design'],row['platform'],d['passed'],'body pixels',d['text_person_pixels'],flush=True)
(R/'quality-checks.json').write_text(json.dumps({'status':'PASS' if len(res)==18 and all(d['passed'] for d in res) else 'FAIL','files':len(res),'checks':res},indent=2));print('ALL',len(res),all(d['passed'] for d in res))
