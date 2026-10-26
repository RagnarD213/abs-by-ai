import sys,json,subprocess,shutil,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R=Path(__file__).resolve().parents[1]
ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/hyperframes'))
import hfbuild as H,vertical as V
srcs={x['t']:x for x in json.loads((R/'sources.json').read_text())}
M=json.loads((R/'parent/measure.json').read_text())
REV=R/'review';(REV/'stills').mkdir(exist_ok=True);(REV/'context').mkdir(exist_ok=True)
TITLES={'A':['How To Do A Standing','Stomach Vacuum'],'B':['Stop Holding Your Breath','During Stomach Vacuums'],'C':['Start With One','20-Second Vacuum']}
FULL={'A':'How To Do A Standing Stomach Vacuum','B':'Stop Holding Your Breath During Stomach Vacuums','C':'Start With One 20-Second Vacuum Every Morning'}
ITEMS=[
 dict(id='A-title',short='A',t=390,topic=None,point=None,cap='do it in',note='Title and wider presenter crop. The full film keeps its approved colour and voice.'),
 dict(id='A-step1',short='A',t=450,topic='STEP 1',point='Relax Before You Draw In',cap='consciously slump',note='The deliberate slump is shown as the starting position, not the finished exercise.'),
 dict(id='A-step2',short='A',t=455,topic='STEP 2',point='Draw In And Hold',cap='suck it in',note='Keep the whole draw-in visible; do not zoom into the belly.'),
 dict(id='A-step3',short='A',t=470,topic='STEP 3',point='Use Time, Not Guesswork',cap='20 second sets',note='A compact timer instruction. The original long-form graphic is rebuilt, not sliced.'),
 dict(id='B-title',short='B',t=490,topic=None,point=None,cap='hold their breath',note='This is the original warning, not the new opening. B still needs its studio pickup.'),
 dict(id='B-breaths',short='B',t=505,topic='DURING THE HOLD',point='Small Breaths Through Your Nose',cap='taking little breaths',note='The actual breathing demonstration stays visible.'),
 dict(id='B-recover',short='B',t=580,topic='BETWEEN SETS',point='Recover With Deep Breaths',cap='deep belly breaths',note='A separate recovery cue accompanies the rest instruction.'),
 dict(id='C-title',short='C',t=556,topic=None,point=None,cap='first thing when',note='Title and wider crop. Opening picture will be the active exercise, then this presenter shot.'),
 dict(id='C-routine',short='C',t=566,topic='BUILD UP GRADUALLY',point='One Set, Then Two, Then Three',cap='two sets of',note='Progression is the useful takeaway; a minute of rest stays in the speech.'),
]

def geometry(t,near=False):
    sh=srcs[t]['shot'];a,b=sh['src_f0']/(30000/1001),sh['src_f1']/(30000/1001)
    rows=[x for x in M[sh['piece']] if a-.3<=x[0]<=b+.3] or M[sh['piece']]
    arr=np.asarray(rows);tops=np.sort(arr[:,1]);med=np.median(tops);good=tops[tops>=med-36] if (tops<med-36).mean()<.15 else tops
    top=float(good.min());cx=float(np.median(arr[:,2]));h=(672 if near=='tight' else 840) if near else 1040
    y=max(0,min(1080-h,round(top-.04*h)));w=round(h*1080/1610);x=round(max(0,min(1920-w,cx-w/2)))
    return [x,y,w,h]

def title(S):
    cfg=dict(id='TITLE-'+S,dur=6,drift=-2,canvas=[1080,310],line_px=68,accent=[64,52,8],eyebrow=dict(x=88,y=38,px=30,s='STOMACH VACUUM'),lines=[])
    while max(H.text_w(s,cfg['line_px']) for s in TITLES[S])>952:cfg['line_px']-=2
    cfg['lines']=[dict(x=64,y=86+i*96,s=s) for i,s in enumerate(TITLES[S])]
    scenes=[(R/'recipe/title-band.template.htm',cfg,())]
    V.build(scenes,R/'hf',snap=2,check=True)
    return R/'hf/stills'/f'TITLE-{S}.png'

def graphic(it):
    c=dict(id=it['id'],a=0,b=6,topic=it['topic'],topic_case='preserve',parts=[[it['point'],.25]],top_y=(1370 if it['id'] in ['A-step3','B-recover','C-routine'] else 1130),drift=-4)
    scenes,meta=V.lt_scenes(c);assert meta['lines']<=2
    V.build(scenes,R/'hf',snap=2,check=True)
    return R/'hf/stills'/f"{it['id']}.png",meta

def crop(t,near=False):
    im=Image.open(R/'source'/f'clean-{t}.png').convert('RGB');x,y,w,h=geometry(t,near)
    return im.crop((x,y,x+w,y+h)).resize((1080,1610),Image.Resampling.LANCZOS)

def caption(im,text,top=1412):
    d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86)
    x=(1080-d.textlength(text,font=font))/2
    d.text((x,top),text,font=font,fill='white',stroke_width=7,stroke_fill='black')

titles={S:title(S) for S in TITLES}
for it in ITEMS:
    im=Image.new('RGB',(1080,1920));im.paste(crop(it['t'],it['id'] in ['B-recover','C-title']),(0,310));im.paste(Image.open(titles[it['short']]).convert('RGB'),(0,0))
    if it['topic']:
        p,meta=graphic(it);ov=Image.open(p).convert('RGBA')
        im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB');it['graphic']=meta
    it['cap_top']=1650 if it['id'] in ['A-step3','B-recover','C-title','C-routine'] else 1412;caption(im,it['cap'],it['cap_top']);p=REV/'stills'/f"{it['id']}.jpg";im.save(p,quality=95)
    it['file']='stills/'+p.name;it['crop']=geometry(it['t'],it['id'] in ['B-recover','C-title']);it['source']=srcs[it['t']]
    print('STILL',it['id'],it['crop'],flush=True)
    if it['id'].endswith('title') and it['short'] != 'C':
        im=Image.new('RGB',(1080,1920));im.paste(crop(it['t'],'tight' if it['short']=='C' else True),(0,310));im.paste(Image.open(titles[it['short']]).convert('RGB'),(0,0));caption(im,it['cap'],1500 if it['short']=='C' else 1412);im.save(REV/'stills'/f"{it['short']}-near.jpg",quality=95)
(R/'items.json').write_text(json.dumps(ITEMS,indent=2))
thumbs=[]
for it in ITEMS:
    im=Image.open(REV/it['file']);im.thumbnail((270,480));thumbs.append((it['id'],im.copy()))
sheet=Image.new('RGB',(810,520*3),'#101d2d');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(thumbs):x=i%3*270;y=i//3*520;sheet.paste(im,(x,y));d.text((x+8,y+488),name,fill='white')
sheet.save(REV/'all-assets.jpg',quality=95)
