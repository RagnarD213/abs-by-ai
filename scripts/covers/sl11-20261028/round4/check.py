from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parents[4];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';R=B/'round4'
m=json.loads((R/'manifest.json').read_text());r2=json.loads((B/'round2/manifest.json').read_text());prior=json.loads((B/'round2/quality-checks.json').read_text())['checks'];rows=[]
for x in m['outputs']:
 p=P/x['path'];im=Image.open(p);base=Image.open(P/x['base_path']).convert('RGB');end=x['photo_start_y'];tm=np.array(Image.open(p.with_name(p.stem+'-text-mask.png')))>0
 original=next(q for q in r2['outputs'] if q['short']==x['short'] and q['design']==1 and q['platform']==x['platform'])
 pm=np.array(Image.open((P/original['path']).with_name((P/original['path']).stem+'-person-mask.png')).convert('L'))>127
 faces=next(q for q in prior if q['short']==x['short'] and q['design']==1 and q['platform']==x['platform'])['faces']
 facehits=[int(tm[b:d,a:c].sum()) for a,b,c,d in [f['expanded_face_and_hair'] for f in faces]]
 y,xx=np.where(tm);actual_bbox=[int(xx.min()),int(y.min()),int(xx.max()+1),int(y.max()+1)]
 # Every non-text header pixel must be plain gradient, excluding antialiased type only.
 grad=np.zeros((end,1080,3),np.uint8)
 for yy in range(end):
  t=yy/max(1,end-1);grad[yy,:,:]=[round(v*(1-t)+w*t) for v,w in zip((5,14,29),(14,37,59))]
 checks={'rgb_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],'photo_pixels_identical':np.array_equal(np.array(im)[end:],np.array(base)[end:]),'text_clear_of_face_hair':not any(facehits),'text_clear_of_body':not (tm&pm).any(),'text_above_photo':actual_bbox[3]<=end-10,'text_safe_band':actual_bbox[1]>=(240 if x['platform']=='instagram' else 50),'top_line_full_width':x['text'][0]['bbox'][2]-x['text'][0]['bbox'][0]==1020,'top_font_enlarged':x['text'][0]['size']>x['text'][0]['old_size'],'lower_fonts_about_5pct_larger':all(1.04<=t['size']/t['old_size']<=1.06 for t in x['text'][1:]),'no_decorative_lines':np.array_equal(np.array(im)[:end][~tm[:end]],grad[~tm[:end]]),'jpeg_under_2MB':(P/x['jpeg_path']).stat().st_size<2_000_000}
 rows.append({'short':x['short'],'platform':x['platform'],'checks':{k:bool(v) for k,v in checks.items()},'text_bbox':actual_bbox,'passed':bool(all(checks.values()))})
result={'status':'PASS' if len(rows)==6 and all(q['passed'] for q in rows) else 'FAIL','files':len(rows),'method':'Exact photo pixel comparison, text/body/face masks, header-only gradient proof, text dimensions and file checks. Silent still-image inspection only.','checks':rows}
(R/'quality-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['status']=='PASS'
