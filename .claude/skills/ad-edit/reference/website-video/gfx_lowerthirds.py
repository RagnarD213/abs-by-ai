#!/usr/bin/env python3
"""Website video -- every graphic to an alpha QTRLE MOV. Palette: motionlib.J2AD (the
locked paid-ad system: black field, olive accent, white body) so the video that plays
right after the ad lands looks like the same brand.

TRUST brief: every element still animates (a frozen card reads as cheap), but the
motion is slow -- gentle drifts, no pops, no flashes -- and the copy is Dan's own words.
  python3 gfx.py            # all (cached on disk)      FORCE=1 to rebuild
  python3 gfx.py NAME ...   # just those
"""
import importlib.util, os, sys
from PIL import Image, ImageDraw
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
spec=importlib.util.spec_from_file_location("ml",f"{SK}/motionlib.py")
ml=importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats as B
PAL=ml.J2AD
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF=f"{L}/00 ASSETS USED IN THE REFERENCE AD"; SHOOT=f"{L}/06 Dan Photo Shoot Stills"
G=f"{HERE}/gfx"; os.makedirs(G,exist_ok=True)

GOAL   = f"{L}/01 Before and After Images/dan by pool - AI GOAL IMAGE.png"
BEFOREP= f"{REF}/02_BEFORE-PICTURE_dan-200lb.png"
POOLP  = f"{SHOOT}/photo-223_FINAL_PRIMARY.jpg"
TODAYP = [f"{SHOOT}/photo-158_FINAL_PRIMARY.jpg", f"{SHOOT}/photo-172_FINAL_PRIMARY.jpg"]
tag_f=ml.font(30,"ExtraBold"); cap_f=ml.font(44,"Bold")
def _tag(im,xy,text="AI-GENERATED",f=None):
    ml.chip(im,xy,text,f or tag_f,(10,12,8,240),(255,255,255,255),radius=8)
def _drift(lay, t, dur, amt=0.045, out=False):
    """slow Ken Burns on a finished layer -- never below 1.0 so the field edge never shows"""
    k = (1.0 + amt) - amt * (t / dur) if out else 1.0 + amt * (t / dur)
    return ml.scale_about(lay, k)
def _skip(n):
    if os.path.exists(f"{G}/{n}.mov") and os.environ.get("FORCE")!="1":
        print(f"  [cached] {n}"); return True
    return False
def _lt(name, lines, beat, lead=44, size=38, **kw):
    if _skip(name): return
    ml.lower_third_bar(f"{G}/{name}.mov", lines, beat[1]-beat[0], pal=PAL, size=size,
                       lead_size=lead, in_dur=0.40, out_dur=0.32, **kw)

# ---- lower thirds (Dan stays full frame) ---------------------------------------
def g_name():     _lt("name",     ["Dan Rose","Founder, Abs by AI"], B.NAME, lead=46, size=36)
def g_num1():     _lt("num1",     ["1 — AI tracks your macros for you","Just take a picture of your food"], B.NUM1)
def g_flyblind(): _lt("flyblind", ["You don't have to fly blind anymore","Track with AI, lose belly fat more easily"], B.FLYBLIND)
def g_num2():     _lt("num2",     ["2 — A workout program built for you","Designed from your own pictures"], B.NUM2)
def g_num3():     _lt("num3",     ["3 — A nutrition plan built for you","From your fat-loss and muscle-gain goals"], B.NUM3)
def g_cancel():   _lt("cancel",   ["Cancel with two taps","You won't be charged a dime"], B.CANCEL)

# ---- photographs (full-frame cards) ---------------------------------------------
disc_f=ml.font(26,"Medium")
def _disc(lay):
    ImageDraw.Draw(lay).text((1880,1046),"Results are not guaranteed.",font=disc_f,fill=(150,156,140),anchor="rm")
def _photo_card(name, path, beat, maxw=1180, maxh=900, out=False, tag=False, caption=None, disclaimer=False):
    if _skip(name): return
    dur=beat[1]-beat[0]
    img=ml.oriented(Image.open(path)).convert("RGB")
    lay,box=ml.photo_on_field(img,maxw,maxh,centre=(960,530 if not caption else (430 if tag else 470)))
    if tag: _tag(lay,(box[0],box[3]+26))
    if caption:
        ImageDraw.Draw(lay).text((960,box[3]+(130 if tag else 70)),caption,font=cap_f,fill=PAL.ink_soft,anchor="mm")
    if disclaimer: _disc(lay)
    ml.card_in(f"{G}/{name}.mov",dur,lambda im,t: im.alpha_composite(_drift(lay,t,dur,0.045,out=out)),
               pal=PAL,in_dur=0.50,out_dur=0.36)
def g_pool():   _photo_card("pool",  POOLP,  B.POOL, maxh=980, disclaimer=True)
def g_before(): _photo_card("before",BEFOREP,B.BEFORE, caption="Me, out of shape")
def g_solved(): _photo_card("solved",GOAL,   B.SOLVED, maxh=800, tag=True, caption="The goal image I generated of myself", out=True)
def g_today():
    """two real shoot photos in SEQUENCE (never side by side), slow drift alternating"""
    if _skip("today"): return
    dur=B.TODAY[1]-B.TODAY[0]; n=len(TODAYP); step=dur/n
    lays=[]
    for p in TODAYP:
        lay,_=ml.photo_on_field(ml.oriented(Image.open(p)).convert("RGB"),1180,980,centre=(960,530)); _disc(lay); lays.append(lay)
    def build(im,t):
        i=min(int(t/step),n-1); lt=t-i*step
        p=ml.ease_out_cubic(lt/0.30)
        im.alpha_composite(ml.with_alpha(_drift(lays[i],lt,step,0.050,out=bool(i%2)),p))
    ml.card_in(f"{G}/today.mov",dur,build,pal=PAL,in_dur=0.50,out_dur=0.36)

# ---- bullet panels (left, Dan in the right column) ------------------------------
def _bul(name, heading, items, beat):
    if _skip(name): return
    # lesson 55: bullets_build draws the heading on ONE line; it must fit panel_w - 2*PAD
    hw=ml.text_size(heading.upper(),ml.font(68,"ExtraBold"))[0]
    assert hw<=980-2*int(980*0.095), f"{name}: heading {hw}px too wide for the 980 panel: {heading!r}"
    a0=beat[0]; out=[]
    for ph,txt in items:
        try: t=round(B.at(ph,after=a0-0.5)-a0,3)
        except KeyError: t=0.30
        out.append((max(0.30,t),txt))
    ml.bullets_build(f"{G}/{name}.mov",heading,out,beat[1]-a0,panel_w=980,pal=PAL,
                     head_color=PAL.accent,head_size=68,body_size=58,in_dur=0.50,out_dur=0.34)
def g_tellai():
    _bul("tellai","Tell the AI about",
         [("workout histories","Your workout history"),("your injuries","Your injuries"),
          ("the equipment you have","The equipment you have"),("your lifestyle constraints","Your lifestyle constraints")],
         B.TELLAI)
def g_trylist():
    _bul("trylist","Try everything, free",
         [("the macro tracker","The macro tracker"),("the AI workout program","The AI workout program"),
          ("the AI nutrition plan","The AI nutrition plan"),("everything in the app","Everything in the app")],
         B.TRYLIST)
def g_mealbul():
    """the second half of the MEALPLAN beat: the plan works around..."""
    if _skip("mealbul"): return
    a0=B.MEALBUL[0]
    _bul("mealbul","Made to fit your life",
         [("any allergies","Works around your allergies"),("religious restrictions","And religious restrictions"),
          ("based on your lifestyle","Built around your lifestyle"),("how much time","And how much time you have")],
         B.MEALBUL)

# ---- full-frame statement cards -------------------------------------------------
def _card(out,dur,headline,sub,size=96,sub_size=48,hold=False):
    fH,fS=ml.font(size,"ExtraBold"),ml.font(sub_size,"Medium")
    lines=ml.wrap(headline,fH,1480); subl=ml.wrap(sub,fS,1300) if sub else []
    LH,LHS=int(size*0.98),int(sub_size*1.2)
    block=len(lines)*LH+(46+len(subl)*LHS if subl else 0)
    top=(ml.H-block)//2
    green=Image.new("RGBA",(ml.W,ml.H),PAL.deep+(255,))
    def build(im,t):
        im.alpha_composite(green)
        tl=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); y=top
        for i,l in enumerate(lines):
            p=ml.ease_out_cubic((t-0.16-i*0.12)/0.50)
            if p<=0.01: y+=LH; continue
            lay=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); w,_=ml.text_size(l,fH)
            ImageDraw.Draw(lay).text(((ml.W-w)/2,y+(1-p)*14),l,font=fH,fill=(255,255,255),anchor="lt")
            tl.alpha_composite(ml.with_alpha(lay,p)); y+=LH
        if subl:
            y+=46
            for i,l in enumerate(subl):
                p=ml.ease_out_cubic((t-0.62-i*0.10)/0.45)
                if p<=0.01: y+=LHS; continue
                lay=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); w,_=ml.text_size(l,fS)
                ImageDraw.Draw(lay).text(((ml.W-w)/2,y),l,font=fS,fill=(226,234,210),anchor="lt")
                tl.alpha_composite(ml.with_alpha(lay,p)); y+=LHS
        im.alpha_composite(_drift(tl,t,dur,0.030))
    # hold=True: the card never fades out -- the video ENDS on it (the site's button sits below)
    ml.card_in(out,dur,build,pal=PAL,in_dur=0.50,out_dur=(0.0 if hold else 0.36))
def g_trial():
    if _skip("trial"): return
    _card(f"{G}/trial.mov",B.TRIAL[1]-B.TRIAL[0],"Try Abs by AI free for 7 days","Everything in the app. No charge for a week.")
def g_price():
    if _skip("price"): return
    _card(f"{G}/price.mov",B.PRICE[1]-B.PRICE[0],"$19.99 per month","A fraction of what a human trainer would charge you",size=120)
def g_cta():
    if _skip("cta"): return
    _card(f"{G}/cta.mov",B.CTA[1]-B.CTA[0],"Try Abs by AI for free","Tap the button below to get started",hold=True)

# ---- plates + tags -------------------------------------------------------------
def g_plates():
    """panels get rounded corners from a PLATE (lesson 22) + an olive hairline"""
    def plate(box,radius=30):
        im=ml.panel_plate(box,radius=radius,pal=PAL); d=ImageDraw.Draw(im)
        d.rounded_rectangle([box[0]-4,box[1]-4,box[2]+3,box[3]+3],radius=radius+4,
                            outline=PAL.accent+(255,),width=4)
        return im
    # LEFT-column phone panels; Dan stays in the right column (x>=980)
    plate([203,30,723,1050]).save(f"{G}/plate_app.png")     # 520x1020 phone recording
    plate([193,30,733,1050]).save(f"{G}/plate_shot.png")    # 540x1020 tall screenshots (900 wide sources)
    t=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); _tag(t,(0,0)); t.crop(t.getbbox()).save(f"{G}/tag.png")
    print("  plates + tags")

BUILDERS={n[2:]:f for n,f in sorted(globals().items()) if n.startswith("g_")}
if __name__=="__main__":
    for name in (sys.argv[1:] or list(BUILDERS)):
        print(name); BUILDERS[name]()
    print("gfx done")
