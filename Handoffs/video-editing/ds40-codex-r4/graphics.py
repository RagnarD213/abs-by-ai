from pathlib import Path
import copy
import sys,json,math
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');HF=R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0,str(HF));import vertical as V
sys.path.insert(0,str(HF.parent));import buildcap
FONT=R/'Media/codex-video-trial/assets/fonts/Poppins-Bold.ttf'
def font(n):return ImageFont.truetype(str(FONT),n)
im=Image.new('RGB',(1008,1120),(9,27,48));d=ImageDraw.Draw(im)
def text(x,y,s,n=32,c='#F0F6FF',anchor='mm'):d.text((x,y),s,font=font(n),fill=c,anchor=anchor)
text(548,40,'Weight (lb)',34);text(75,103,'Height',25)
weights=list(range(120,281,20));heights=list(range(62,79,2))
cols={'Underweight':'#52647D','Normal':'#2E9B8C','Overweight':'#C3933E','Obese':'#B95462'}
table=[]
for j,lb in enumerate(weights):text(160+j*94,100,str(lb),29)
for i,h in enumerate(heights):
 y=173+i*81;text(66,y,f'{h//12}\'{h%12}"',30)
 for j,lb in enumerate(weights):
  bmi=lb*.45359237/(h*.0254)**2;cat='Underweight' if bmi<18.5 else 'Normal' if bmi<25 else 'Overweight' if bmi<30 else 'Obese'
  x=160+j*94;d.rounded_rectangle((x-43,y-36,x+43,y+36),radius=9,fill=cols[cat]);text(x,y,f'{bmi:.1f}',28)
  table.append({'height_inches':h,'weight_lb':lb,'bmi':round(bmi,4),'category':cat})
legend=[('Underweight','Below 18.5'),('Normal','18.5-24.9'),('Overweight','25-29.9'),('Obese','30+')]
for i,(cat,ran) in enumerate(legend):
 x=24+i*246;y=925;d.rounded_rectangle((x,y,x+228,y+104),radius=15,fill=cols[cat]);text(x+114,y+31,cat,23);text(x+114,y+77,ran,23)
text(504,1065,'CDC Adult BMI Categories',24,c='#A1B5CE')
im.save(W/'bmi-table.png');(W/'bmi-calculation.json').write_text(json.dumps({'source':'https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html','formula':'kg / metres squared','note':'Cells classified by unrounded BMI, numbers rounded to one decimal. Underweight cells in slate.','cells':table},indent=2))
# Actual phrase timing from the source word map, on the 18.018-second clip-first timeline.
start=1400.2322;opening=588/(30000/1001);shift=opening-18.018
to=lambda t:round(opening+t-start,6)
subscribe=opening+(1436.36-1400.2322)+(1445.06-1439.8)
cuts=[('G01',0,opening,'Source','Bill Maher | Real Time (HBO)',0),('G02',to(1413.26),to(1418.46),'Health','Treat Your Belly Fat As An Emergency',to(1414.18)),('G04',subscribe,opening+(1436.36-1400.2322)+(1448.9148-1439.8),'More Fitness Tips','Subscribe To The Channel',subscribe)]
out=W/'hf';allmeta=[]
import time
while not (W/'bill-original.wav').exists(): time.sleep(3)
buildcap.wait('Bill Maher R4 shared HyperFrames graphics')
for gid,a,b,topic,point,reveal in cuts:
 scenes,meta=V.lt_scenes({'id':gid,'a':a,'b':b,'topic':topic,'topic_case':'preserve','parts':[[point,max(a,reveal)]]})
 # Attribute the opening clip between its upper picture and Dan's lower reaction.
 if gid=='G01':
  delta=-495
  shifted=[]
  for tpl,cfg,assets in scenes:
   cfg=copy.deepcopy(cfg)
   cfg['strip'][1]+=delta;cfg['accent'][1]+=delta;cfg['topic']['y']+=delta;cfg['point_y']+=delta
   for part in cfg['parts']:part['y']+=delta
   shifted.append((tpl,cfg,assets))
  scenes=shifted
  meta['band']=[x+delta for x in meta['band']];meta['box'][1]+=delta;meta['box'][3]+=delta
 V.build(scenes,out,render=True,snap=1)
 allmeta.append({'id':gid,'a':a,'b':b,'template':'lower-third','mov':str(out/'renders'/f'{gid}.mov'),'mask':str(out/'renders'/f'{gid}_mask.mov'),**meta,'words':point})
a=to(1423.122);b=opening+(1436.36-1400.2322)+(1444.7099667-1439.8)
scene,hole=V.media_card_scene('G03',b-a,1008/1120,kicker='Find Your BMI',caps=False)
tpl,cfg,assets=scene;cfg['hole']=[36,240,1008,1120];cfg['kicker']={'x':64,'y':140,'px':54,'s':'Find Your BMI'}
V.build([(tpl,cfg,assets)],out,render=True,snap=1)
allmeta.append({'id':'G03','a':a,'b':b,'template':'media-card','mov':str(out/'renders/G03.mov'),'table':str(W/'bmi-table.png'),'hole':cfg['hole'],'words':'BMI Table: Height And Weight'})
(W/'graphics-manifest.json').write_text(json.dumps(sorted(allmeta,key=lambda x:x['a']),indent=2))
print('GRAPHICS COMPLETE',flush=True)
