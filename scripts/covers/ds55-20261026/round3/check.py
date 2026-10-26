from build import *
import subprocess
from scipy.ndimage import maximum_filter
PM=Path.home()/'.cache/absbyai/personmask/personmask'
ABS={1:(400,640,720,995),2:(385,1010,635,1215),3:(400,740,695,1055)}
HEAD={1:(460,325,775,640),2:(535,635,850,1010),3:(465,380,800,700)}
m=json.loads((OUT/'manifest.json').read_text());rows=[];pairs=[];colour=[]
for k in [1,2,3]:
 a=Image.open(OUT/'sources'/f'{k}-original.png').convert('RGB');b=Image.open(OUT/'sources'/f'{k}-picture.png').convert('RGB')
 for label,im in [('original',a),('warm',b)]:
  hsv=np.asarray(im.convert('HSV')).astype(float);v=np.asarray(im).astype(float);box=ABS[k];skin=v[box[1]:box[3],box[0]:box[2]]
  colour.append({'choice':k,'version':label,'median_saturation':float(np.median(hsv[:,:,1])),'mean_saturation':float(hsv[:,:,1].mean()),'torso_mean_red_over_blue':float((skin[:,:,0].mean()+1)/(skin[:,:,2].mean()+1)),'black_pixel_share':float((v.mean(2)<16).mean())})
 box=HEAD[k]
 for label,im in [('Original',a),('Warm retouch',b)]:
  crop=im.crop(box);crop.thumbnail((270,300));pairs.append((f'{k}: '+label,crop))
for r in m['outputs']:
 p=Path(r['path']);im=Image.open(p);pic=p.with_name(p.stem+'.picture.png');pm=p.with_name(p.stem+'.person-mask.png');res=subprocess.run([str(PM),str(pic),str(pm)],capture_output=True,text=True,check=True);faces=json.loads(res.stdout)['faces']
 txt=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')));gm=np.array(Image.open(p.with_name(p.stem+'.graphic-mask.png')))
 protected=Image.new('L',(W,H));dd=ImageDraw.Draw(protected);dd.rectangle(ABS[r['choice']],fill=255);dd.rectangle(HEAD[r['choice']],fill=255);protected=np.array(protected)>0
 collisions=int(((maximum_filter(txt,size=31)>0)&protected).sum());gcollisions=int(((gm>16)&protected).sum())
 row=dict(choice=r['choice'],platform=r['platform'],sha256=sha(p),size=list(im.size),mode=im.mode,faces=faces,text_vs_head_abs_pixels_including15px=collisions,graphic_vs_head_abs_pixels_above6percent_alpha=gcollisions,full_screen_picture=True,passed=im.size==(W,H) and im.mode=='RGB' and len(faces)==1 and collisions==0 and gcollisions==0)
 if r['platform']=='youtube':
  q=p.with_suffix('.jpg');row.update(jpeg_sha256=sha(q),jpeg_bytes=q.stat().st_size);row['passed'] &= q.stat().st_size<2000000
 rows.append(row)
sheet=Image.new('RGB',(6*285,350),'#152333');dd=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(pairs):sheet.paste(im,(i*285+5,35));dd.text((i*285+8,8),label,fill='white')
sheet.save(OUT/'face-comparison.jpg',quality=95)
(OUT/'cover-checks.json').write_text(json.dumps({'all_passed':all(r['passed'] for r in rows),'checks':rows,'colour_measurements':colour,'head_boxes':HEAD,'abs_boxes':ABS,'protected_boxes':'Manually calibrated against full-resolution sources and final pictures. Direct face/hair/abs and image inspection required.','visual_review':'pending'},indent=2))
print(json.dumps({'all_passed':all(r['passed'] for r in rows),'checks':[{'choice':x['choice'],'platform':x['platform'],'text_collisions':x['text_vs_head_abs_pixels_including15px'],'graphic_collisions':x['graphic_vs_head_abs_pixels_above6percent_alpha'],'faces':len(x['faces']),'passed':x['passed']} for x in rows],'colour':colour},indent=2))
