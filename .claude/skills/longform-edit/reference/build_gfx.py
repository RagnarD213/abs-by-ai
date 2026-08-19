#!/usr/bin/env python3
"""J2 tactical graphics for the longform meal-prep video.
Constants lifted verbatim from .claude/skills/shorts/reference/band/assets.py"""
from PIL import Image, ImageDraw, ImageFont
import os
OUT="/tmp/sc/gfx"; W,H=1920,1080
BG=(13,14,11); OLIVE=(140,152,88); WHITE=(255,255,255)
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER='/System/Library/Fonts/Supplemental/Copperplate.ttc'
MANROPE='/Users/danielrose/Library/Fonts/Manrope.ttf'

def spaced(d,xy,text,font,fill,gap=5):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=font,fill=fill); x+=font.getlength(ch)+gap
    return x

def chip(key, eyebrow, title, x=620, y=812):
    """Lower-third chip: letter-spaced olive eyebrow over an olive-bordered box."""
    f_eye=ImageFont.truetype(COPPER,26); f_ttl=ImageFont.truetype(IMPACT,58)
    pad_x,pad_y=26,16
    tw=int(ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(title,font=f_ttl))
    ew=sum(f_eye.getlength(c)+5 for c in eyebrow)
    boxw=int(max(tw+pad_x*2, ew+pad_x*2)); boxh=58+pad_y*2
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    ebh=36
    d.rectangle([x,y-4,x+int(ew)+pad_x,y-4+ebh],fill=BG+(225,))
    spaced(d,(x+10,y),eyebrow,f_eye,OLIVE+(255,),5)
    top=y+40
    d.rectangle([x,top,x+boxw,top+boxh],fill=BG+(238,),outline=OLIVE+(255,),width=3)
    d.text((x+pad_x,top+pad_y-6),title,font=f_ttl,fill=WHITE+(255,))
    p=os.path.join(OUT,"chip_%s.png"%key); im.save(p); return p

def watermark():
    """AbsByAI.com - camel case, small, muted. Rip protection, per the J2 rule."""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(MANROPE,30)
    txt="AbsByAI.com"
    wid=f.getlength(txt)
    x0,y0=W-wid-46,H-62
    d.text((x0+2,y0+2),txt,font=f,fill=(0,0,0,150))
    d.text((x0,y0),txt,font=f,fill=(255,255,255,205))
    p=os.path.join(OUT,"wm.png"); im.save(p); return p

CHIPS=[
 ("intro","ABS BY AI // MACRO TRACKER","TRACK A WHOLE MEAL PREP"),
 ("s1","STEP 01","PHOTOGRAPH THE BATCH"),
 ("s2","STEP 02","SET YOUR SERVINGS"),
 ("s3","STEP 03","ADD THE CONTEXT"),
 ("s4","STEP 04","RUN THE ANALYSIS"),
 ("s5","STEP 05","ANSWER THE FOLLOW-UPS"),
 ("cal","PER SERVING","683 CALORIES"),
 ("s6","STEP 06","LOG ONE SERVING"),
]
for k,e,t in CHIPS: print("built",chip(k,e,t))
print("built",watermark())
