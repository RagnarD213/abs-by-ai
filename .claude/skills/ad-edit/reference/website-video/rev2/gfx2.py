#!/usr/bin/env python3
"""Website video REV 2 -- the reduced graphics set, styled on MUHAMMAD'S measured system.

Dan on rev 1 (2026-09-02): "a graphic on the left and a huge amount of black space ... just a
bunch of text, generic ... horrible. Graphics sparingly. When we do put in a graphic it can't
have black space over half of the screen." So rev 2 keeps the six lower thirds from rev 1
(gfx/name,num1,flyblind,num2,num3,cancel -- untouched, Dan did not mention them) and rebuilds
everything else on his measured card system (pv/mh_*.png, pixel-scanned 2026-09-02):

  field   near-black olive (10,11,5) with a faint 72 px grid and a vignette
  plate   olive (66,76,37)->(80,89,49), 1476x924 for photos / 1497x764 for titles -- the plate
          fills ~75 % of the frame width, which is why his cards never read as "one small
          element on black"
  photo   fit inside the plate with a 28 px inset, rounded 22 px; AI tag sits on the photo's
          bottom-right corner (his 160 s frame)
  title   ~142 px oblique ExtraBold caps at 0.88 leading, subtitle ~52 px, all inside the plate

The phone for the macro-tracker beat is NOT a card: Dan asked for it next to him in the camera
scene, so gfx2 only builds its rounded mask + hairline/shadow plate and layout2.py overlays
the real recording through them.

  python3 gfx2.py               # everything not cached      FORCE=1 rebuilds
  python3 gfx2.py NAME ...      # just those
"""
import importlib.util, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
spec=importlib.util.spec_from_file_location("ml",f"{SK}/motionlib.py")
ml=importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats as B
W,H=1920,1080; FPS=30000/1001
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF=f"{L}/00 ASSETS USED IN THE REFERENCE AD"
G=f"{HERE}/gfx"; os.makedirs(G,exist_ok=True)

GOAL   = f"{L}/01 Before and After Images/dan by pool - AI GOAL IMAGE.png"
BEFOREP= f"{REF}/02_BEFORE-PICTURE_dan-200lb.png"
TODAYP = [f"{REF}/04_SHOT1_photoshoot-smiling-trees.png", f"{REF}/05_SHOT2_photoshoot-flag.jpg",
          f"{REF}/06_SHOT3_photoshoot-towel-smile.jpg",  f"{REF}/07_SHOT4_photoshoot-standing.jpg"]

# ---- his measured tokens -------------------------------------------------------
FIELD=(10,11,5); GRIDC=(24,26,12); VIG=(4,5,2)
PL_TL=(66,76,37); PL_BR=(80,89,49)
OLIVE=(140,152,88)                       # hairlines only
PHOTO_BOX=[243,78,1719,1002]             # 1476x924
TITLE_BOX=[211,158,1708,922]             # 1497x764
INSET=28; PHOTO_R=22; PLATE_R=40

def grid_field():
    im=Image.new("RGB",(W,H),FIELD); d=ImageDraw.Draw(im)
    for x in range(0,W,72): d.line([(x,0),(x,H)],fill=GRIDC,width=1)
    for y in range(0,H,72): d.line([(0,y),(W,y)],fill=GRIDC,width=1)
    v=Image.new("L",(W,H),0); ImageDraw.Draw(v).ellipse([-W*0.25,-H*0.25,W*1.25,H*1.25],fill=255)
    v=v.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(im,Image.new("RGB",(W,H),VIG),v).convert("RGBA")
_FIELD=None
def field():
    global _FIELD
    if _FIELD is None: _FIELD=grid_field()
    return _FIELD

def plate(box,rad=PLATE_R):
    x0,y0,x1,y1=box; w,h=x1-x0,y1-y0
    yy,xx=np.mgrid[0:h,0:w]; t=(0.55*xx/w+0.75*yy/h)/1.3
    g=np.zeros((h,w,3),np.float32)
    for c in range(3): g[:,:,c]=PL_TL[c]*(1-t)+PL_BR[c]*t
    im=Image.fromarray(g.astype(np.uint8))
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=rad,fill=255)
    out=Image.new("RGBA",(W,H),(0,0,0,0)); out.paste(im,(x0,y0),m)
    return out

def rounded(img,rad):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,img.size[0]-1,img.size[1]-1],radius=rad,fill=255)
    out=img.convert("RGBA"); out.putalpha(m); return out

PREVIEW=os.environ.get("PREVIEW_T")
def _frames(n):
    """PREVIEW_T=<sec> renders ONE frame to pv/g2_<name>.png instead of encoding (lesson 60:
    preview on a real frame at native resolution before any render)"""
    if PREVIEW: return [max(0,min(n-1,int(round(float(PREVIEW)*FPS))))]
    return range(n)
def _emit(frames,name):
    if PREVIEW: frames[0].save(f"{HERE}/pv/g2_{name}.png"); print(f"  preview pv/g2_{name}.png"); return
    ml.encode(frames,f"{G}/{name}.mov")
def _skip(n):
    if PREVIEW: return False
    if os.path.exists(f"{G}/{n}.mov") and os.environ.get("FORCE")!="1":
        print(f"  [cached] {n}"); return True
    return False

def fade_env(t,dur,in_dur=0.50,out_dur=0.40,hold=False):
    a=ml.ease_out_cubic(t/in_dur) if in_dur>0 else 1.0
    if hold or t<=dur-out_dur: return a
    return a*(1-ml.ease_in_cubic((t-(dur-out_dur))/out_dur))

# ---- photo cards ------------------------------------------------------------------
tag_f=ml.font(30,"ExtraBold"); disc_f=ml.font(26,"Medium")
def fitted(path):
    """photo fit-contained inside the plate inset, returned with its box"""
    img=ml.oriented(Image.open(path)).convert("RGB")
    bw,bh=PHOTO_BOX[2]-PHOTO_BOX[0]-2*INSET,PHOTO_BOX[3]-PHOTO_BOX[1]-2*INSET
    k=min(bw/img.width,bh/img.height); w,h=int(img.width*k),int(img.height*k)
    x=PHOTO_BOX[0]+(PHOTO_BOX[2]-PHOTO_BOX[0]-w)//2; y=PHOTO_BOX[1]+(PHOTO_BOX[3]-PHOTO_BOX[1]-h)//2
    return img,(x,y,w,h)
def drifted(img,box,k):
    """Ken Burns from a SUPERSAMPLED source (lesson 7): resize the full-res photo to k x the
    box and centre-crop, so the drift is smooth and never shows the plate through an edge"""
    x,y,w,h=box; sw,sh=int(round(w*k)),int(round(h*k))
    big=img.resize((sw,sh),Image.LANCZOS)
    return rounded(big.crop(((sw-w)//2,(sh-h)//2,(sw-w)//2+w,(sh-h)//2+h)),PHOTO_R)
def _tag(im,box):
    x,y,w,h=box
    ml.chip(im,(x+w-16-ml.text_size("AI-GENERATED",tag_f)[0]-36,y+h-16-52),"AI-GENERATED",tag_f,
            (18,18,18,235),(255,255,255,255),radius=8)
def _disc(im):
    ImageDraw.Draw(im).text((PHOTO_BOX[2],1044),"Results are not guaranteed.",font=disc_f,fill=(150,156,140),anchor="rm")

def photo_card(name,items,dur,tag=False,disclaimer=False,hold=False):
    """items = [(path, seconds), ...] shown in SEQUENCE inside one plate; each photo drifts
    slowly (alternating in/out) and hands over with a short crossfade -- never side by side"""
    if _skip(name): return
    prep=[(fitted(p),d) for p,d in items]
    pl=plate(PHOTO_BOX); fld=field()
    frames=[]; n=max(1,int(round(dur*FPS)))
    starts=np.cumsum([0]+[d for _,d in items])
    for i in _frames(n):
        t=i/FPS; env=fade_env(t,dur,hold=hold)
        im=Image.new("RGBA",(W,H),(0,0,0,0))
        im.alpha_composite(ml.with_alpha(fld,env))
        con=Image.new("RGBA",(W,H),(0,0,0,0)); con.alpha_composite(pl)
        j=min(int(np.searchsorted(starts,t,side="right")-1),len(prep)-1); lt=t-starts[j]; d=prep[j][1]
        (img,box)=prep[j][0]
        k=1.0+0.045*(lt/d) if j%2==0 else 1.045-0.045*(lt/d)
        ph=drifted(img,box,k); a=ml.ease_out_cubic(lt/0.30) if j>0 else 1.0
        if j>0 and a<1.0:                          # crossfade from the previous photo
            (img0,box0)=prep[j-1][0]; con.alpha_composite(drifted(img0,box0,1.045 if (j-1)%2==0 else 1.0),(box0[0],box0[1]))
        con.alpha_composite(ml.with_alpha(ph,a),(box[0],box[1]))
        if tag: _tag(con,box)
        if disclaimer: _disc(con)
        s=0.97+0.03*ml.ease_out_cubic(t/0.50)
        im.alpha_composite(ml.with_alpha(ml.scale_about(con,s),env))
        frames.append(im)
    _emit(frames,name)

def g_before(): photo_card("before",[(BEFOREP,B.BEFORE[1]-B.BEFORE[0])],B.BEFORE[1]-B.BEFORE[0])
def g_today():
    dur=B.TODAY[1]-B.TODAY[0]; each=dur/len(TODAYP)
    photo_card("today",[(p,each) for p in TODAYP],dur,disclaimer=True)
def g_solved(): photo_card("solved",[(GOAL,B.SOLVED[1]-B.SOLVED[0])],B.SOLVED[1]-B.SOLVED[0],tag=True)

# ---- title cards (his 45 s card, measured) ---------------------------------------
def title_card(name,lines,sub,dur,hold=False,max_size=142,max_w=1100):
    if _skip(name): return
    lines=[l.upper() for l in lines]
    size=max_size
    while size>80 and max(ml.text_size(l,ml.font(size,"ExtraBold"))[0] for l in lines)>max_w: size-=4
    fH=ml.font(size,"ExtraBold"); fS=ml.font(52,"Medium")
    LH=int(size*0.88); widths=[ml.text_size(l,fH)[0] for l in lines]
    cap=max(ml.ink_bottom(l,fH) for l in lines)
    subl=ml.wrap(sub,fS,max_w) if sub else []; LHS=int(52*1.22)
    hb=(len(lines)-1)*LH+cap; sb=(len(subl)*LHS) if subl else 0
    block=hb+(74+sb if subl else 0)
    x0,y0,x1,y1=TITLE_BOX; top=y0+((y1-y0)-block)//2
    pl=plate(TITLE_BOX); fld=field()
    frames=[]; n=max(1,int(round(dur*FPS)))
    for i in _frames(n):
        t=i/FPS; env=fade_env(t,dur,hold=hold)
        im=Image.new("RGBA",(W,H),(0,0,0,0)); im.alpha_composite(ml.with_alpha(fld,env))
        con=Image.new("RGBA",(W,H),(0,0,0,0))
        p=ml.ease_out_cubic(t/0.40)
        if p>0.01:
            ph=(y1-y0)*p; cy=(y0+y1)/2
            con.alpha_composite(plate([x0,int(cy-ph/2),x1,int(cy+ph/2)]))
        y=top
        for li,l in enumerate(lines):
            q=ml.ease_out_cubic((t-0.20-li*0.10)/0.40)
            if q<=0.02: y+=LH; continue
            tw=widths[li]; x=(W-tw)/2
            gl=Image.new("RGBA",(W,H),(0,0,0,0))
            ImageDraw.Draw(gl).text((x,y),l,font=fH,fill=(255,255,255),anchor="lt")
            gl=ml.oblique(gl,10.0,pivot_y=y+cap/2)
            cut=x+tw*ml.ease_out_expo((t-0.20-li*0.10)/0.5)+size*0.3
            m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rectangle([0,0,cut,H],fill=255)
            gl.putalpha(Image.composite(gl.getchannel("A"),Image.new("L",(W,H),0),m))
            con.alpha_composite(gl); y+=LH
        if subl:
            y=top+hb+74
            for si,l in enumerate(subl):
                q=ml.ease_out_cubic((t-0.55-si*0.08)/0.40)
                if q>0.01:
                    lay=Image.new("RGBA",(W,H),(0,0,0,0)); tw=ml.text_size(l,fS)[0]
                    ImageDraw.Draw(lay).text(((W-tw)/2,y+(1-q)*12),l,font=fS,fill=(236,240,226),anchor="lt")
                    con.alpha_composite(ml.with_alpha(lay,q))
                y+=LHS
        im.alpha_composite(ml.with_alpha(ml.scale_about(con,1.0+0.022*(t/dur)),env))
        frames.append(im)
    _emit(frames,name)

def g_trial(): title_card("trial",["Try Abs by AI","free for 7 days"],"Everything in the app. No charge for a week.",B.TRIAL[1]-B.TRIAL[0])
def g_price(): title_card("price",["$19.99","per month"],"A fraction of what a human trainer would charge you",B.PRICE[1]-B.PRICE[0])
def g_cta():   title_card("cta",["Try Abs by AI","for free"],"Tap the button below to get started",B.CTA[1]-B.CTA[0],hold=True)

# ---- the phone PiP (mask + plate; layout2.py overlays the real recording) ----------
PIP_BOX=[150,130,583,950]                # 433x820 -- his phones measure ~475x922; iOS corner ~44
PIP_R=44
def g_pip():
    x0,y0,x1,y1=PIP_BOX; w,h=x1-x0,y1-y0
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=PIP_R,fill=255)
    m.save(f"{G}/pip_mask.png")
    pl=Image.new("RGBA",(W,H),(0,0,0,0))
    pl.alpha_composite(ml.drop_shadow((W,H),PIP_BOX,PIP_R,blur=34,spread=12,opacity=150,offset=(0,14)))
    hole=Image.new("L",(W,H),255); ImageDraw.Draw(hole).rounded_rectangle(PIP_BOX,radius=PIP_R,fill=0)
    pl.putalpha(Image.composite(pl.getchannel("A"),Image.new("L",(W,H),0),hole))
    ImageDraw.Draw(pl).rounded_rectangle([x0-2,y0-2,x1+1,y1+1],radius=PIP_R+2,outline=OLIVE+(255,),width=3)
    pl.save(f"{G}/pip_plate.png"); print("  pip mask + plate")

BUILDERS={n[2:]:f for n,f in sorted(globals().items()) if n.startswith("g_")}
if __name__=="__main__":
    for name in (sys.argv[1:] or list(BUILDERS)):
        print(name); BUILDERS[name]()
    print("gfx2 done")
