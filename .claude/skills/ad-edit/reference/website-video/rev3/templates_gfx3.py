#!/usr/bin/env python3
"""Ad 3 -- every animated graphic to an alpha MOV. Palette: motionlib.J2AD (paid-ad
locked style: BLACK field, olive/dark-green headers, WHITE body).

Every element animates (lesson 19); alpha rides on QTRLE MOV. Nothing static.
  python3 gfx3.py            # all (cached on disk)
  python3 gfx3.py NAME ...   # just those      FORCE=1 to rebuild
"""
import importlib.util, os, sys
from PIL import Image, ImageDraw
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec=importlib.util.spec_from_file_location("ml",f"{SK}/motionlib.py")
ml=importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats3 as B
PAL=ml.J2AD
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF=f"{L}/00 ASSETS USED IN THE REFERENCE AD"
SHOOT=f"{L}/06 Dan Photo Shoot Stills"
G=f"{HERE}/gfx"; os.makedirs(G,exist_ok=True)

GOAL   = f"{REF}/01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png"
BEFOREP= f"{REF}/02_BEFORE-PICTURE_dan-200lb.png"
# The cue asks for 3-5 best shots from the photo shoot on "this is what I look like today".
TODAY_SHOTS=[f"{REF}/04_SHOT1_photoshoot-smiling-trees.png",
             f"{REF}/05_SHOT2_photoshoot-flag.jpg",
             f"{REF}/06_SHOT3_photoshoot-towel-smile.jpg",
             f"{REF}/07_SHOT4_photoshoot-standing.jpg"]
tag_f=ml.font(30,"ExtraBold"); cap_f=ml.font(44,"Bold"); pop_f=ml.font(104,"ExtraBold")
def _tag(im,xy,text="AI-GENERATED",f=None):
    ml.chip(im,xy,text,f or tag_f,(10,12,8,240),(255,255,255,255),radius=8)
def _drift(lay, t, dur, amt=0.055, out=False):
    """Ken Burns on a finished card layer.

    card_in scales its content 0.90 -> 1.00 across a 0.42 s entrance and then HOLDS. The
    watch pass measured 2.4 s, 2.8 s, 3.2 s, 5.8 s and 8.7 s dead-frozen on the photo and
    CTA cards -- which is exactly Dan's ad-1 rev-1 note 1, "static photos are never left
    static". PIL resizes the whole layer per frame, so the CONTENT interpolates smoothly
    instead of stepping the way ffmpeg zoompan does on integer crop offsets (lesson 7).
    k never drops below 1.0, so the field edge is never exposed.
    """
    k = (1.0 + amt) - amt * (t / dur) if out else 1.0 + amt * (t / dur)
    return ml.scale_about(lay, k)

def _skip(n):
    if os.path.exists(f"{G}/{n}.mov") and os.environ.get("FORCE")!="1":
        print(f"  [cached] {n}"); return True
    return False

# ---- statements / lower thirds -------------------------------------------------
def g_lower3a():
    if _skip("lower3a"): return
    ml.lower_third_bar(f"{G}/lower3a.mov",
        ["Human personal trainers","are obsolete."],
        B.LOWER3A[1]-B.LOWER3A[0], pal=PAL, size=42, lead_size=46)
def g_notprice():
    """The one 'stop and read this' beat -- bar stays the reserved brand RED."""
    if _skip("notprice"): return
    ml.lower_third_bar(f"{G}/notprice.mov",
        ["A human trainer cannot do this for you.","Not at any price."],
        B.NOTPRICE[1]-B.NOTPRICE[0], pal=PAL, size=38, lead_size=46, bar_color=PAL.hot)
def g_num1():
    if _skip("num1"): return
    ml.lower_third_bar(f"{G}/num1.mov", ["1 — They are expensive","$70 to $200 an hour"],
        B.NUM1[1]-B.NUM1[0], pal=PAL, size=40, lead_size=46)
def g_num3():
    if _skip("num3"): return
    ml.lower_third_bar(f"{G}/num3.mov", ["3 — Science, not bro-science",
        "Most trainers never read the research"], B.NUM3[1]-B.NUM3[0],
        pal=PAL, size=38, lead_size=46)
def g_num4():
    if _skip("num4"): return
    ml.lower_third_bar(f"{G}/num4.mov", ["4 — It is there every workout",
        "A human trainer sees you once a week"], B.NUM4[1]-B.NUM4[0],
        pal=PAL, size=38, lead_size=46)

# ---- chapter cards -------------------------------------------------------------
def g_whycard():
    if _skip("whycard"): return
    ml.title_card(f"{G}/whycard.mov","Why AI beats\na human trainer",
        "Four reasons, including me", B.WHYCARD[1]-B.WHYCARD[0], pal=PAL,
        band=PAL.deep, band_ink=(255,255,255), size=124, sub_size=58)
def g_howcard():
    if _skip("howcard"): return
    ml.title_card(f"{G}/howcard.mov","How AI personal\ntraining works",
        "From your photo to your first workout", B.HOWCARD[1]-B.HOWCARD[0], pal=PAL,
        band=PAL.deep, band_ink=(255,255,255), size=118, sub_size=56)

# ---- bullet panels -------------------------------------------------------------
def g_costcard():
    if _skip("costcard"): return
    c0=B.COSTCARD[0]
    ml.bullets_build(f"{G}/costcard.mov","Spend it on this",
        [(round(B.at("on meal prep",after=c0-0.5)-c0,3),"Meal prep."),
         (round(B.at("quality food",after=c0-0.5)-c0,3),"Quality food."),
         (round(B.at("or a home gym",after=c0-0.5)-c0,3),"A home gym setup.")],
        B.COSTCARD[1]-c0, panel_w=980, pal=PAL, head_color=PAL.accent)
def g_planbul():
    if _skip("planbul"): return
    p0=B.PLANBUL[0]
    ml.bullets_build(f"{G}/planbul.mov","Built around you",
        [(round(B.at("any injuries you have",after=p0-0.5)-p0,3),"Any injuries you have."),
         (round(B.at("the equipment you actually own",after=p0-0.5)-p0,3),"The equipment you actually own."),
         (round(B.at("how many days a week",after=p0-0.5)-p0,3),"How many days a week you can train.")],
        B.PLANBUL[1]-p0, panel_w=980, pal=PAL, head_color=PAL.accent)
def g_adapts():
    if _skip("adapts"): return
    a0=B.ADAPTS[0]
    ml.bullets_build(f"{G}/adapts.mov","Your plan adapts",
        [(round(B.at("If it's too difficult",after=a0-0.5)-a0,3),"Too hard? The AI tones it down."),
         (round(B.at("If it's too easy",after=a0-0.5)-a0,3),"Too easy? It cranks it up."),
         (round(B.at("Didn't sleep well",after=a0-0.5)-a0,3),"Slept badly? It adjusts for that too.")],
        B.ADAPTS[1]-a0, panel_w=980, pal=PAL, head_color=PAL.accent)
def g_tailor():
    if _skip("tailor"): return
    t0=B.TAILOR[0]
    ml.bullets_build(f"{G}/tailor.mov","It reads your body",
        [(0.30,"Your strong body parts."),
         (round(B.at("and your lagging body parts",after=t0-0.5)-t0,3),"Your lagging body parts."),
         (round(B.at("And it tailors your program",after=t0-0.5)-t0,3),"Trained toward your goal picture.")],
        B.TAILOR[1]-t0, panel_w=980, pal=PAL, head_color=PAL.accent)
def g_brocard():
    if _skip("brocard"): return
    ml.title_card(f"{G}/brocard.mov","Bro-science\nfrom 2015","Picked up in the gym, passed along as fact",
        B.BROCARD[1]-B.BROCARD[0], pal=PAL, band=PAL.deep, band_ink=(255,255,255),
        size=118, sub_size=52)

# ---- photographs ---------------------------------------------------------------
def g_before():
    """His real 200 lb before picture, ALONE, with the number popped. Never beside the
    after -- that is the banned pattern (Dan's #1 compliance rule)."""
    if _skip("before"): return
    dur=B.BEFORE[1]-B.BEFORE[0]
    img=ml.oriented(Image.open(BEFOREP)).convert("RGB")
    lay,box=ml.photo_on_field(img,820,760,centre=(960,410))
    def build(im,t):
        im.alpha_composite(_drift(lay,t,dur,0.060))          # in
        ml.pop_text(im,t-(dur*0.46),"200 POUNDS",pop_f,(960,box[3]+105),
                    color=PAL.ink,accent=PAL.hot)
    ml.card_in(f"{G}/before.mov",dur,build,pal=PAL)
def g_goalimg():
    """The AI future-self image ALONE, tag ON SCREEN per the cue."""
    if _skip("goalimg"): return
    dur=B.GOALIMG[1]-B.GOALIMG[0]
    img=ml.oriented(Image.open(GOAL)).convert("RGB")
    lay,box=ml.photo_on_field(img,980,880,centre=(960,452))
    _tag(lay,(box[0],box[3]+30))
    ImageDraw.Draw(lay).text((960,box[3]+150),"The goal image I generated",
                             font=cap_f,fill=PAL.ink_soft,anchor="mm")
    ml.card_in(f"{G}/goalimg.mov",dur,
               lambda im,t: im.alpha_composite(_drift(lay,t,dur,0.055,out=True)),pal=PAL)
def g_today():
    """3-5 best shots from the photo shoot, in SEQUENCE (never side by side), per the cue.
    Real photos of Dan need no label; only the generated image is tagged.

    Built here rather than with motionlib.photo_sequence because that one holds each
    photo perfectly still: the watch pass measured 0.87 s identical runs on all four,
    and Dan's ad-1 rev-1 note 1 is that a still is never left static. Each photo gets a
    Ken Burns drift, alternating in/out on consecutive images (rev-1 lesson 1)."""
    if _skip("today"): return
    dur=B.TODAY[1]-B.TODAY[0]; n=len(TODAY_SHOTS); step=dur/n
    lays=[]
    for i,path in enumerate(TODAY_SHOTS):
        lay,_box=ml.photo_on_field(ml.oriented(Image.open(path)).convert("RGB"),
                                   1180,930,centre=(960,516))
        lays.append(lay)
    def build(im,t):
        i=min(int(t/step),n-1)
        lt=t-i*step
        # quick cross-in so a photo change is a beat, not a snap
        p=ml.ease_out_cubic(lt/0.24)
        im.alpha_composite(ml.with_alpha(_drift(lays[i],lt,step,0.070,out=bool(i%2)),p))
    ml.card_in(f"{G}/today.mov",dur,build,pal=PAL)

# ---- CTAs ----------------------------------------------------------------------
def _cta_card(out,dur,headline,sub):
    fH,fS=ml.font(100,"ExtraBold"),ml.font(52,"Medium")
    lines=ml.wrap(headline,fH,1480); subl=ml.wrap(sub,fS,1300) if sub else []
    LH,LHS=int(100*0.98),int(52*1.2)
    block=len(lines)*LH+(46+len(subl)*LHS if subl else 0)
    top=(ml.H-block)//2
    green=Image.new("RGBA",(ml.W,ml.H),PAL.deep+(255,))
    def build(im,t):
        im.alpha_composite(green)
        tl=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); y=top
        for i,l in enumerate(lines):
            p=ml.ease_out_cubic((t-0.14-i*0.10)/0.42)
            if p<=0.01: y+=LH; continue
            lay=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); w,_=ml.text_size(l,fH)
            ImageDraw.Draw(lay).text(((ml.W-w)/2,y+(1-p)*18),l,font=fH,fill=(255,255,255),anchor="lt")
            tl.alpha_composite(ml.with_alpha(lay,p)); y+=LH
        if subl:
            y+=46
            for i,l in enumerate(subl):
                p=ml.ease_out_cubic((t-0.55-i*0.09)/0.4)
                if p<=0.01: y+=LHS; continue
                lay=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); w,_=ml.text_size(l,fS)
                ImageDraw.Draw(lay).text(((ml.W-w)/2,y),l,font=fS,fill=(226,234,210),anchor="lt")
                tl.alpha_composite(ml.with_alpha(lay,p)); y+=LHS
        im.alpha_composite(_drift(tl,t,dur,0.038))
    ml.card_in(out,dur,build,pal=PAL)
def g_cta1():
    if _skip("cta1"): return
    _cta_card(f"{G}/cta1.mov",B.CTA1[1]-B.CTA1[0],
        "Get your free AI image and your AI training plan","Tap the button below")
def g_cta2():
    if _skip("cta2"): return
    _cta_card(f"{G}/cta2.mov",B.CTA2[1]-B.CTA2[0],
        "Let your AI trainer make it real","Tap the button below to get started")

# ---- plates + tags -------------------------------------------------------------
def g_plates():
    """A video panel gets rounded corners from a PLATE, not a mask (lesson 22), plus an
    olive hairline -- panel_plate's baked shadow is invisible on a (13,14,11) field."""
    def plate(box,radius=30):
        im=ml.panel_plate(box,radius=radius,pal=PAL); d=ImageDraw.Draw(im)
        d.rounded_rectangle([box[0]-4,box[1]-4,box[2]+3,box[3]+3],radius=radius+4,
                            outline=PAL.accent+(255,),width=4)
        return im
    plate([673,30,1247,1050]).save(f"{G}/plate_vert.png")    # 574x1020  9:16 clips
    plate([700,30,1220,1050]).save(f"{G}/plate_app.png")     # 520x1020  phone recordings
    plate([690,30,1230,1050]).save(f"{G}/plate_shot.png")    # 540x1020  900x2572 stills
    plate([328,40,1592,1040]).save(f"{G}/plate_wide.png")    # 1264x1000 the 1820x1440 archive clip
    plate([416,124,1504,936]).save(f"{G}/plate_demo.png")    # 1088x812  16:9 exercise demo
    # The after-alone app slice needs the email-capture form covered. Two separately
    # timed overlays (plate + cover) raced by ONE FRAME and the form was exposed at
    # 179.41 s -- caught by the watch pass's consecutive-frame strips, invisible to a
    # 2 fps scan. Baking the cover into the top plate makes it one layer and the race
    # cannot happen.
    pc = plate([700,30,1220,1050])
    _cover_into(pc, 700, 676)
    pc.save(f"{G}/plate_app_cover.png")
    t=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0)); _tag(t,(0,0)); t.crop(t.getbbox()).save(f"{G}/tag.png")
    tb=Image.new("RGBA",(ml.W,ml.H),(0,0,0,0))
    ml.chip(tb,(0,0),"AI-GENERATED",ml.font(45,"ExtraBold"),(10,12,8,240),(255,255,255,255),radius=10)
    tb.crop(tb.getbbox()).save(f"{G}/tag_big.png")
    print("  plates + tags")

def g_adaptmid():
    if _skip("adaptmid"): return
    a0=B.ADAPTMID[0]
    ml.bullets_build(f"{G}/adaptmid.mov","On the spot",
        [(0.30,"Tweaked your shoulder mid-week?"),
         (round(B.at("If you can't get to the gym",after=a0-0.5)-a0,3),
          "Stuck at home instead of the gym?")],
        B.ADAPTMID[1]-a0, panel_w=980, pal=PAL, head_color=PAL.accent)
def g_toolate():
    if _skip("toolate"): return
    ml.lower_third_bar(f"{G}/toolate.mov",
        ["By the time you see a human trainer","it is already too late to matter"],
        B.TOOLATE[1]-B.TOOLATE[0], pal=PAL, size=38, lead_size=44)
def g_gymq():
    if _skip("gymq"): return
    ml.lower_third_bar(f"{G}/gymq.mov",
        ["Any exercise question, answered","right there in the gym"],
        B.GYMQ[1]-B.GYMQ[0], pal=PAL, size=38, lead_size=44)

def _cover_into(im, ox, oy, W=520, Hh=374):
    d=ImageDraw.Draw(im)
    d.rectangle([ox,oy,ox+W-1,oy+Hh-1],fill=(10,12,8,255))
    d.rectangle([ox,oy,ox+W-1,oy+Hh-1],outline=PAL.accent+(255,),width=3)
    f1=ml.font(38,"ExtraBold"); f2=ml.font(25,"Medium")
    d.text((ox+W//2,oy+Hh//2-34),"AI-GENERATED",font=f1,fill=(255,255,255),anchor="mm")
    d.text((ox+W//2,oy+Hh//2+22),"Your future self, generated",font=f2,fill=PAL.ink_soft,anchor="mm")
    d.text((ox+W//2,oy+Hh//2+58),"from your own photo",font=f2,fill=PAL.ink_soft,anchor="mm")

def g_covers():
    """The oversized disclosure box that covers the app's email-capture form, whole,
    including its explainer text (Dan, ad-1 rev-2: never show an email ask in an ad).
    Dual purpose: it is also the AI-GENERATED disclosure on the after image above it."""
    W,Hh=520,374
    im=Image.new("RGBA",(W,Hh),(10,12,8,255))
    d=ImageDraw.Draw(im)
    d.rectangle([0,0,W-1,Hh-1],outline=PAL.accent+(255,),width=3)
    f1=ml.font(38,"ExtraBold"); f2=ml.font(25,"Medium")
    d.text((W//2,Hh//2-34),"AI-GENERATED",font=f1,fill=(255,255,255),anchor="mm")
    d.text((W//2,Hh//2+22),"Your future self, generated",font=f2,fill=PAL.ink_soft,anchor="mm")
    d.text((W//2,Hh//2+58),"from your own photo",font=f2,fill=PAL.ink_soft,anchor="mm")
    im.save(f"{G}/email_cover.png")
    print("  email_cover.png")

BUILDERS={n[2:]:f for n,f in sorted(globals().items()) if n.startswith("g_")}
if __name__=="__main__":
    for name in (sys.argv[1:] or list(BUILDERS)):
        print(name); BUILDERS[name]()
    print("gfx done")
