#!/usr/bin/env python3
"""DS-05 Why Having Abs Beats Being A Fat Millionaire: five cover choices (2026-10-14), two layouts each.
Mix per VIDEO-RULES (2026-10-13): A real pool photo, B real studio cutout on a Codex scene, C AI image of Dan,
D and E Codex's own designs. Reuses the type layouts of the Muhammad batch builder (scripts/covers/muhammad-batch-20261013).
Codex plates live in <review>/assets/gen as ds-05-{studio,c,d,e}.png."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'muhammad-batch-20261013'))
import build as b
b.R=b.P/'Short-form video content/covers/review/ds05-20261014'
b.COPY={'ds-05':('ABS VS MONEY',['WHY ABS BEAT','A FAT MILLIONAIRE'],'ds-05_why-having-abs-beats-being-a-fat-millionaire','Why Having Abs Beats Being A Fat Millionaire')}
b.ORDER=['ds-05']
b.POOL={'ds-05':('photo-276',(0.0790,0.7794,0.1169,0.9719))}
b.STUDIO={'ds-05':'studio-blue-175'}
b.KIND={'A':'Pool photo','B':'Studio photo on topic scene','C':'AI image of Dan: yellow band','D':'Codex choice 1: headline at the bottom','E':'Codex choice 2: two panels'}
_plate=b.plate
def plate(k,which,gradient):
 """E: Codex's black strip sits at y 833-1084, narrower than the type band (812-1108), so the rich man's feet and
 Dan's hair touched the band. Slide the top panel up 50 px and the bottom panel down 50 px to widen the strip."""
 im,p=_plate(k,which,gradient)
 if which!='e':return im,p
 out=b.Image.new('RGBA',(b.W,b.H),(0,0,0,255));out.paste(im.crop((0,50,b.W,833)),(0,0));out.paste(im.crop((0,1084,b.W,b.H-50)),(0,1134))
 return out,p
b.plate=plate
if __name__=='__main__':b.build(['ds-05'])
