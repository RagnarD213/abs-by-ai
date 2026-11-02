from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';F=str(R/'Media/video_edit/bin/ffmpeg');S='/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1719.MP4'
a=json.load(open(R/'Docs/DS28_APPROVED_COLOR_A_20261014.json'))['filter']
g={'A':a,'B':a.replace('0.25/0.35 0.5/0.61','0.25/0.39 0.5/0.66').replace('saturation=0.90','saturation=0.95'),'C':a.replace('0.25/0.35 0.5/0.61','0.25/0.32 0.5/0.57').replace('saturation=0.90','saturation=1.00')}
(W/'grades.json').write_text(json.dumps(g,indent=2))
for k,f in g.items():
 for t in [215,245]:
  p=Q/f'color-{k}-{t}.jpg'
  if not p.exists():subprocess.run([F,'-v','error','-nostdin','-y','-ss',str(t),'-i',S,'-frames:v','1','-vf',f'crop=1600:2844:300:700,scale=540:960:in_color_matrix=bt709:in_range=tv,{f}',str(p)],check=True)
out=Image.new('RGB',(1080,1352),'#102136');d=ImageDraw.Draw(out)
for i,k in enumerate(g):
 for j,t in enumerate([215,245]):
  out.paste(Image.open(Q/f'color-{k}-{t}.jpg').resize((360,640)),(i*360,36+j*658));d.text((i*360+10,10+j*658),k+': '+{'A':'Clean and balanced','B':'Brighter skin','C':'Deeper contrast'}[k],fill='white')
out.save(Q/'color-comparison.jpg',quality=94)
