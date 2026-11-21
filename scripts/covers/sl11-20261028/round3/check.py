from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parents[4];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';R=B/'round3';m=json.loads((R/'manifest.json').read_text());old=json.loads((B/'round2/quality-checks.json').read_text())['checks'];rows=[]
for x in m['outputs']:
 p=P/x['path'];im=Image.open(p);base=Image.open(P/x['base_path']).convert('RGB');end=x['photo_start_y'];tm=np.array(Image.open(p.with_name(p.stem+'-text-mask.png')))>0
 prior=next(q for q in old if q['short']==x['short'] and q['design']==1 and q['platform']==x['platform'])
 faces=[]
 for f in prior['faces']:
  a,b,c,d=f['expanded_face_and_hair'];faces.append(int(tm[b:d,a:c].sum()))
 mp=(P/x['base_path']).with_name((P/x['base_path']).stem+'-person-mask.png');pm=np.array(Image.open(mp).convert('L'))>127
 y,xx=np.where(tm);actual_bbox=[int(xx.min()),int(y.min()),int(xx.max()+1),int(y.max()+1)]
 checks={'rgb_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],'all_photo_pixels_identical':np.array_equal(np.array(im)[end:],np.array(base)[end:]),'all_words_preserved':x['all_words_preserved'],'text_clear_of_face_and_hair':not any(faces),'text_clear_of_person':not (tm&pm).any(),'title_stays_above_photo':actual_bbox[3]<end-15,'text_safe_band':actual_bbox[1]>=(240 if x['platform']=='instagram' else 50),'jpeg_under_2MB':(P/x['jpeg_path']).stat().st_size<2_000_000}
 rows.append({'short':x['short'],'design':x['design'],'platform':x['platform'],'sha256':x['sha256'],'text_bbox':actual_bbox,'checks':{k:bool(v) for k,v in checks.items()},'passed':bool(all(checks.values()))})
(R/'quality-checks.json').write_text(json.dumps({'status':'PASS' if len(rows)==18 and all(q['passed'] for q in rows) else 'FAIL','files':len(rows),'method':'Exact PNG photo-pixel comparison plus text masks against the matching R2 Design 1 face/body positions, which have identical photo geometry. No new perceptual audio or film check.','checks':rows},indent=2))
sh=Image.new('RGB',(900,1260),'#152435');d=ImageDraw.Draw(sh)
for j,key in enumerate('abc'):
 for i,n in enumerate([1,2,3]):
  sh.paste(Image.open(R/key/'grid'/f'{n}.jpg'),(i*300+15,j*420+36));d.text((i*300+15,j*420+10),f'{key.upper()} - Header {n}',fill='white')
sh.save(R/'all-profile-crops.jpg',quality=96)
print('QA',len(rows),'files:',all(q['passed'] for q in rows));print([r for r in rows if not r['passed']])
