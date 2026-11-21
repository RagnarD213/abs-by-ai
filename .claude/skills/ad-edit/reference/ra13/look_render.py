import json,sys,subprocess,os
from pathlib import Path
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];os.chdir(W);R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('RA-13 look comparison')
FF=str(R/'Media/video_edit/bin/ffmpeg');roll=json.load(open('source/roll.json'))['identity']['current_path']
variants={'A':('Existing Daylight', '1.15','eq=saturation=1.25'), 'B':('Brighter Natural','1.30','eq=saturation=1.12:gamma=1.03'),'C':('Warmer Contrast','1.15','eq=saturation=1.18:gamma=1.04:contrast=1.04,colorbalance=rm=0.018:bm=-0.006')}
meta={}
for code,(name,e,post) in variants.items():
 filt=f'scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709,lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e{e}.cube:interp=tetrahedral,{post}'
 meta[code]={'name':name,'filter':filt,'scope':'candidate, not approved'}
 for tm in (256,289):
  p=f'round1/stills/{code}-{tm}-full.png'
  subprocess.run([FF,'-v','error','-y','-ss',str(tm),'-i',roll,'-frames:v','1','-vf',filt,p],check=True)
print('LOOK OPTIONS READY',flush=True)
json.dump(meta,open('grade-options.json','w'),indent=2)
