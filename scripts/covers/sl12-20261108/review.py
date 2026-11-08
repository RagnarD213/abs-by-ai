"""Build a source-blind, paired cover review. Originals remain private.

Rerunning retains the existing neutral labels, so Dan's picks never drift.
"""
from pathlib import Path
import json, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[3]
WORK=Path('/Volumes/Extreme/_edit_work/SL-12/setup')
PAGE=Path('/Volumes/Extreme/_edit_work/SL-12/round1/asset-review/setup')
BLIND=ROOT/'.claude/skills/_shared/blind-image/blind.py'
TITLES={'A':'Lift Weights On Weight Loss Medication','B':'How Much Protein Do You Need?'}
PAGE.mkdir(parents=True,exist_ok=True)

def run(*args):subprocess.run(['python3',str(BLIND),*map(str,args)],check=True)

for short in 'AB':
    setdir=WORK/'blind'/short
    if not (setdir/'.blind-key.json').exists():
        for ident in ['c1','c2','c3','c4','c5','g1','g2','g3']:
            args=['add',setdir,'--source','codex' if ident[0]=='c' else 'google',
                  '--file',WORK/'layouts'/short/'instagram'/(ident+'.png'),'--note',ident]
            if ident=='c5':args+=['--not-comparison']
            run(*args)
        run('build',setdir,'--kind','cover','--video',TITLES[short]+' (SL-12 '+short+')','--shot',short)
    key=json.loads((setdir/'.blind-key.json').read_text())
    sheet=Image.new('RGB',(4*540,2*595),'#101820');dr=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',30)
    for n,(label,row) in enumerate(key['labels'].items()):
        ident=row['note'];x=n%4*540;y=n//4*595
        dr.text((x+12,y+4),short+' '+label,fill='white',font=font)
        for j,platform in enumerate(['instagram','youtube']):
            source=WORK/'layouts'/short/platform/(ident+'.png')
            im=Image.open(source).convert('RGB')
            dest=PAGE/f'{short}-{label}-{platform}.jpg';im.save(dest,quality=94)
            if platform=='instagram':
                # Exact profile crop, displayed first; full file remains linked.
                im.crop((0,240,1080,1680)).save(PAGE/f'{short}-{label}-grid.jpg',quality=94)
            thumb=im.copy();thumb.thumbnail((270,480));sheet.paste(thumb,(x+j*270,y+45))
            dr.text((x+j*270+5,y+535),platform.title(),fill='#cdd8e3')
    sheet.save(PAGE/(short+'-choices.jpg'),quality=95)

header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keep Your Muscle: Cover Choices</title>
<style>*{box-sizing:border-box}body{margin:0;background:#0b121a;color:#edf4fc;font:16px/1.5 system-ui}main{max-width:1250px;margin:auto;padding:20px}h1{font-size:26px;line-height:1.12;margin:4px 0 10px}h2{font-size:25px;line-height:1.2}p{max-width:760px}.hold{border-left:4px solid #f7ce48;background:#1b2430;padding:12px 16px}.nav{position:sticky;top:0;background:#0b121aee;padding:12px 0;z-index:2;display:flex;gap:10px}.nav a,.overview{color:#8bd9ff}section{scroll-margin-top:68px;margin-top:32px}.grid{display:grid;grid-template-columns:1fr;gap:20px}.card{padding:14px;background:#17212e;border:1px solid #304257;border-radius:14px}.card h3{font-size:24px;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}.pair img{display:block;width:100%;height:auto}.pair a{color:#b6d5ed;font-size:13px;text-decoration:none}.caption{margin:8px 0;font-size:14px;color:#b6c8da}.card small{display:block;color:#aebed0;margin-top:8px}a:hover{text-decoration:underline}img{border-radius:6px}@media(min-width:900px){main{padding:32px}.grid{grid-template-columns:1fr 1fr}}
</style><main><h1>Keep Your Muscle<br>Cover Choices</h1>
<p>Pick one label for each: <b>A X3, B X6</b>, for example. Tap a picture to enlarge.</p>
<p class="hold"><b>Publishing held.</b> Both wait until the parent is confirmed public on or after December 6.</p>
<nav class="nav"><a href="#A">A: Lifting</a><a href="#B">B: Protein</a></nav>'''
body=header
for short in 'AB':
    body+=f'<section id="{short}"><h2>{short}: {TITLES[short]}</h2><p><a class="overview" href="{short}-choices.jpg">View all eight together</a></p><div class="grid">'
    for i in range(1,9):
        label=f'X{i}'
        body+=f'''<article class="card"><h3>{short} {label}</h3><div class="pair"><div><p class="caption">Instagram profile tile</p><a href="{short}-{label}-instagram.jpg"><img loading="lazy" src="{short}-{label}-grid.jpg" alt="{short} {label} Instagram profile crop"><small>Open full Instagram cover</small></a></div><div><p class="caption">YouTube cover</p><a href="{short}-{label}-youtube.jpg"><img loading="lazy" src="{short}-{label}-youtube.jpg" alt="{short} {label} YouTube cover"></a></div></div></article>'''
    body+='</div></section>'
body+='<p>Reply with one label for A and one for B. The videos stay approved; this review is for covers.</p></main></html>'
(PAGE/'index.html').write_text(body)
# Reuse this job's existing service and port. The finalized editing review stays in round3.
(PAGE.parent/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=setup/"><a href="setup/">Keep Your Muscle cover choices</a>')
print('Review built:',PAGE)
