from build import *
from scipy.ndimage import maximum_filter
m=json.loads((OUT/'manifest.json').read_text());rows=[];faces=[]
for r in m['outputs']:
 p=Path(r['path']);mask=p.with_name(p.stem+'.person-mask.png');pic=p.with_name(p.stem+'.picture.png')
 res=subprocess.run([str(PM),str(pic),str(mask)],capture_output=True,text=True,check=True);ff=json.loads(res.stdout)['faces']
 person=np.array(Image.open(mask).convert('L'))>127;text=maximum_filter(np.array(Image.open(p.with_name(p.stem+'.text-mask.png'))),size=31)>0
 n=int((person&text).sum());im=Image.open(p)
 rr=dict(choice=r['choice'],platform=r['platform'],sha256=sha(p),text_person_collision_px_15px_margin=n,faces=ff,size=list(im.size),mode=im.mode,passed=n==0 and len(ff)==1 and im.size==(W,H) and im.mode=='RGB')
 if r['platform']=='youtube':
  q=p.with_suffix('.jpg');rr['jpeg_bytes']=q.stat().st_size;rr['jpeg_sha256']=sha(q);rr['passed'] &= q.stat().st_size<2000000
  for box in ff:
   x0,y0,x1,y1=box;pad=round((x1-x0)*.25);face=im.crop((max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad)));face.thumbnail((260,300));faces.append((r['choice'],face))
 rows.append(rr)
sheet=Image.new('RGB',(len(faces)*280,360),'#152333');d=ImageDraw.Draw(sheet)
for i,(k,face) in enumerate(faces):sheet.paste(face,(i*280,40));d.text((i*280+8,10),'Choice '+str(k),fill='white')
sheet.save(OUT/'final-face-check.jpg',quality=95)
(OUT/'cover-checks.json').write_text(json.dumps({'all_passed':all(x['passed'] for x in rows),'rows':rows,'visual_review':'Pending direct inspection'},indent=2))
print(json.dumps({'all_passed':all(x['passed'] for x in rows),'rows':rows},indent=2))
