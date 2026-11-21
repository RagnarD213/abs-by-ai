from build import *
from scipy.ndimage import maximum_filter
m=json.loads((OUT/'manifest.json').read_text());src=np.array(Image.open(SOURCE).convert('RGB'));rows=[]
head=(535,635,850,1010);absbox=(385,1010,635,1215)
for r in m['outputs']:
 p=Path(r['path']);im=Image.open(p);a=np.asarray(im);txt=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')));safe=np.zeros((H,W),bool)
 for x0,y0,x1,y1 in [head,absbox]:safe[y0:y1,x0:x1]=True
 coll=int(((maximum_filter(txt,size=31)>0)&safe).sum());changes=int(np.any(a[620:]!=src[620:],axis=2).sum());protected_changes=int((np.any(a!=src,axis=2)&safe).sum())
 row=dict(choice=r['choice'],platform=r['platform'],sha256=sha(p),size=list(im.size),mode=im.mode,changed_pixels_below620=changes,changed_head_abs_pixels=protected_changes,text_vs_head_abs15px_margin=coll,passed=changes==0 and protected_changes==0 and coll==0 and im.size==(W,H) and im.mode=='RGB')
 if r['platform']=='youtube':
  q=p.with_suffix('.jpg');row.update(jpeg_sha256=sha(q),jpeg_bytes=q.stat().st_size);row['passed'] &= q.stat().st_size<2000000
 rows.append(row)
(OUT/'cover-checks.json').write_text(json.dumps({'all_passed':all(x['passed'] for x in rows),'head_box':head,'abs_box':absbox,'checks':rows,'visual_review':'Pending direct inspection'},indent=2));print(json.dumps({'all_passed':all(x['passed'] for x in rows),'checks':rows},indent=2))
