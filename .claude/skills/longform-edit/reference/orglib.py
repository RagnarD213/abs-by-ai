#!/usr/bin/env python3
"""Muhammad-organic design system (measured off his ab-wheel round-2 render).
All components render RGBA PNG frame sequences at 29.97fps for overlay.

Tokens (measured):
  FIELD (10,11,5) near-black olive field; faint grid pitch ~72px lines (24,26,12)
  OLIVE text on white pill: (118,134,66);  pill white: (250,251,250)
  plate gradient: (141,152,97) light -> (84,93,55) dark
  Font: Poppins (Bold / SemiBold / BoldItalic)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os, math

A=os.path.dirname(os.path.abspath(__file__))+'/assets'
FIELD=(10,11,5)
GRIDC=(26,28,14)
OLIVE=(118,134,66)
OLIVE_DARK=(84,93,55)
OLIVE_LIGHT=(141,152,97)
PILLW=(250,251,250)
FPS=30000/1001

def font(sz,weight='Bold',italic=False):
    name=f"Poppins-{weight}{'Italic' if italic else ''}.ttf"
    return ImageFont.truetype(f"{A}/{name}",sz)

def rr(draw,box,rad,fill):
    draw.rounded_rectangle(box,radius=rad,fill=fill)

# ---------- grid field (title cards, glow cards)
def grid_field(w=1920,h=1080):
    im=Image.new('RGB',(w,h),FIELD)
    d=ImageDraw.Draw(im)
    for x in range(0,w,72):
        d.line([(x,0),(x,h)],fill=GRIDC,width=1)
    for y in range(0,h,72):
        d.line([(0,y),(w,y)],fill=GRIDC,width=1)
    # soft vignette darken corners
    v=Image.new('L',(w,h),0)
    dv=ImageDraw.Draw(v)
    dv.ellipse([-w*0.3,-h*0.3,w*1.3,h*1.3],fill=60)
    v=v.filter(ImageFilter.GaussianBlur(200))
    im=Image.composite(im,Image.new('RGB',(w,h),(4,5,2)),v.point(lambda p:255-p+195))
    return im

def deco(draw,w=1920,h=1080):
    c=(210,214,196)
    # corner L brackets
    L=64; th=3; m=48
    for (x,y,sx,sy) in [(m,m,1,1),(w-m,m,-1,1),(m,h-m,1,-1),(w-m,h-m,-1,-1)]:
        draw.line([(x,y),(x+sx*L,y)],fill=c,width=th)
        draw.line([(x,y),(x,y+sy*L)],fill=c,width=th)
    # plus marks
    for (x,y) in [(120,190),(w-120,190),(120,h-190),(w-120,h-190)]:
        draw.line([(x-10,y),(x+10,y)],fill=c,width=2)
        draw.line([(x,y-10),(x,y+10)],fill=c,width=2)
    # dotted rows top
    for i in range(12):
        draw.rectangle([560+i*16,44,564+i*16,48],fill=c)
    for i in range(12):
        draw.rectangle([w-560-i*16,44,w-556-i*16,48],fill=c)
    # dot columns sides
    for i in range(8):
        draw.rectangle([210,330+i*26,214,334+i*26],fill=c)
        draw.rectangle([w-214,330+i*26,w-210,334+i*26],fill=c)
    # carousel dots bottom
    for i in range(9):
        x=w//2-80+i*20
        if i==4: draw.ellipse([x-4,h-56,x+4,h-48],fill=c)
        else: draw.ellipse([x-2.5,h-54.5,x+2.5,h-49.5],fill=(120,122,108))

def plate(w,h,rad=42):
    """olive gradient plate with soft inner sheen"""
    g=np.zeros((h,w,3),np.float32)
    for y in range(h):
        for c in range(3):
            pass
    yy,xx=np.mgrid[0:h,0:w]
    t=(0.55*xx/w+0.75*yy/h)/1.3
    for c in range(3):
        g[:,:,c]=OLIVE_LIGHT[c]*(1-t)+OLIVE_DARK[c]*t
    im=Image.fromarray(g.astype(np.uint8))
    mask=Image.new('L',(w,h),0)
    rr(ImageDraw.Draw(mask),[0,0,w-1,h-1],rad,255)
    out=Image.new('RGBA',(w,h),(0,0,0,0))
    out.paste(im,(0,0),mask)
    return out

# ---------- typewriter text helpers
def type_states(text,tfont,color,shadow=None):
    """list of RGBA images, one per revealed char count, drawn at baseline;
    trailing 3 chars of the reveal get graded alpha (soft typewriter fade)."""
    states=[]
    for k in range(len(text)+1):
        pass
    return states

def draw_text_reveal(im,xy,text,tfont,color,reveal,align_center_x=None):
    """draw text with per-char alpha: chars < reveal-3 full, then fade."""
    d=ImageDraw.Draw(im)
    asc,desc=tfont.getmetrics()
    x,y=xy
    if align_center_x is not None:
        tw=tfont.getlength(text)
        x=align_center_x-tw/2
    for i,ch in enumerate(text):
        if i>=reveal: break
        a=255
        if i>=reveal-3:
            a=int(255*(reveal-i)/3)
        d.text((x,y+asc),ch,font=tfont,fill=color+(a,),anchor='ls')
        x+=tfont.getlength(ch)
    return im

# ---------- pill components (each returns list of (RGBA frame, dur_frames) or a
# function frame(t) -> RGBA)

def pill_two_line(line1,line2=None,style='white',w=1920,h=1080,y0=64,
                  size1=86,size2=64,pop_t=0.25,type_cps=28):
    """His top-center pill: line1 pops/slides in with the pill; line2 typewrites.
    style 'white' (white pill, olive text, olive tab) or 'olive' (olive pill, white text).
    Returns frame(t)->RGBA and total intro duration."""
    f1=font(size1,'Bold'); f2=font(size2,'SemiBold')
    asc1,_=f1.getmetrics()
    pad=56
    w1=f1.getlength(line1); w2=f2.getlength(line2) if line2 else 0
    pw=int(max(w1,w2))+2*pad
    ph=int(size1*1.5+(size2*1.35 if line2 else 0)+24)
    tab=104
    total_w=tab+8+pw if style=='white' else pw
    x0=(w-total_w)//2
    def frame(t):
        im=Image.new('RGBA',(w,h),(0,0,0,0))
        d=ImageDraw.Draw(im)
        # pop scale-in
        k=min(1.0,t/pop_t)
        k=1-(1-k)**3
        cw,chh=int(total_w*(0.85+0.15*k)),int(ph*(0.85+0.15*k))
        cx,cy=x0+(total_w-cw)//2,y0+(ph-chh)//2
        a=int(255*min(1.0,t/0.12))
        if style=='white':
            tabim=Image.new('RGBA',(w,h),(0,0,0,0))
            rr(ImageDraw.Draw(tabim),[cx,cy,cx+int(tab*cw/total_w),cy+chh],22,OLIVE+(a,))
            rr(ImageDraw.Draw(tabim),[cx+int((tab+8)*cw/total_w),cy,cx+cw,cy+chh],24,PILLW+(a,))
            im=Image.alpha_composite(im,tabim)
            tx0=x0+tab+8+pad; tcol=OLIVE
        else:
            p=plate(cw,chh,rad=26)
            if a<255:
                p.putalpha(p.getchannel('A').point(lambda v:v*a//255))
            im.alpha_composite(p,(cx,cy))
            tx0=x0+pad; tcol=(255,255,255)
        if t>pop_t*0.4:
            ty=y0+14
            im=draw_text_reveal(im,(tx0,ty),line1,f1,tcol,10**6,
                                align_center_x=x0+(tab+8 if style=='white' else 0)+(pw)//2)
            if line2:
                reveal=int(max(0,(t-pop_t-0.05))*type_cps)
                im=draw_text_reveal(im,(tx0,ty+int(size1*1.42)),line2,f2,tcol,reveal,
                                    align_center_x=x0+(tab+8 if style=='white' else 0)+(pw)//2)
        return im
    return frame,ph

def thin_bar(text,w=1920,y0=36,size=34,type_cps=30):
    """small white bar, olive text, typewriter; top-center."""
    f=font(size,'SemiBold')
    pad=30
    tw=f.getlength(text)
    bw=int(tw)+2*pad+46; bh=int(size*1.75)
    x0=(w-bw)//2
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        a=int(255*min(1.0,t/0.15))
        d=ImageDraw.Draw(im)
        rr(d,[x0,y0,x0+bw,y0+bh],14,PILLW+(a,))
        rr(d,[x0+10,y0+10,x0+34,y0+bh-10],7,OLIVE+(a,))
        reveal=int(max(0,t-0.1)*type_cps)
        im=draw_text_reveal(im,(x0+46+pad,y0+int(bh*0.16)),text,f,OLIVE,reveal)
        return im
    return frame,bh

def num_chip(num,text,w=1920,x0=95,y0=940,size=56):
    """olive numbered square + white pill, bottom-left; slides in from left."""
    f=font(size,'Bold'); fn=font(int(size*0.92),'Bold')
    pad=36
    tw=f.getlength(text)
    sq=int(size*1.65)
    bw=int(tw)+2*pad; bh=sq
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        k=min(1.0,t/0.3); k=1-(1-k)**3
        dx=int((1-k)*-220)
        a=int(255*min(1.0,t/0.15))
        d=ImageDraw.Draw(im)
        rr(d,[x0+dx,y0,x0+dx+sq,y0+sq],10,OLIVE+(a,))
        asc,_=fn.getmetrics()
        d.text((x0+dx+sq//2,y0+sq//2),num,font=fn,fill=(255,255,255,a),anchor='mm')
        rr(d,[x0+dx+sq+10,y0,x0+dx+sq+10+bw,y0+bh],10,PILLW+(a,))
        reveal=int(max(0,t-0.25)*30)
        im=draw_text_reveal(im,(x0+dx+sq+10+pad,y0+int(bh*0.12)),text,f,OLIVE,reveal)
        return im
    return frame,bh

def stack_panel(items,w=1920,x0=60,y0=200,size=44,per_item=0.9):
    """frosted panel with white mini-pills appearing one at a time (typewriter)."""
    f=font(size,'SemiBold')
    pad=26
    iw=int(max(f.getlength(s) for s in items))+2*pad+56
    ih=int(size*1.7)
    gap=22
    pw=iw+2*34; phh=len(items)*(ih+gap)-gap+2*34
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        d=ImageDraw.Draw(im)
        a=int(160*min(1.0,t/0.2))
        rr(d,[x0,y0,x0+pw,y0+phh],26,(245,247,240,int(a*0.45)))
        for i,s in enumerate(items):
            ts=t-0.15-i*per_item
            if ts<=0: continue
            aa=int(255*min(1.0,ts/0.12))
            yy=y0+34+i*(ih+gap)
            rr(d,[x0+34,yy,x0+34+24,yy+ih],7,OLIVE+(aa,))
            rr(d,[x0+34+30,yy,x0+34+iw,yy+ih],9,PILLW+(aa,))
            reveal=int(max(0,ts-0.05)*26)
            im=draw_text_reveal(im,(x0+34+30+pad,yy+int(ih*0.14)),s,f,OLIVE,reveal)
        return im
    return frame,phh

def title_card(lines,hl_line=None,w=1920,h=1080):
    """full-frame dark grid field + brackets + olive plate + italic caps wiping in
    with motion blur; hl_line index gets a white highlight box."""
    base=grid_field(w,h)
    deco(ImageDraw.Draw(base))
    pw,phh=1500,740
    px,py=(w-pw)//2,165
    pl=plate(pw,phh)
    f=font(78,'Bold',italic=True)
    def frame(t):
        im=base.convert('RGBA').copy()
        pa=int(255*min(1.0,t/0.2))
        p=pl.copy()
        if pa<255: p.putalpha(p.getchannel('A').point(lambda v:v*pa//255))
        im.alpha_composite(p,(px,py))
        n=len(lines)
        total_h=n*112
        ty=py+phh//2-total_h//2
        for i,ln in enumerate(lines):
            ts=t-0.25-i*0.22
            if ts<=0: continue
            k=min(1.0,ts/0.30)
            txt=Image.new('RGBA',(w,200),(0,0,0,0))
            dt=ImageDraw.Draw(txt)
            if hl_line==i:
                tw=f.getlength(ln)
                bx=(w-tw)/2
                aa=int(255*k)
                rr(dt,[bx-24,28,bx+tw+24,142],10,(255,255,255,aa))
                dt.text((w/2,42+font(78,'Bold',italic=True).getmetrics()[0]-42+42),ln,
                        font=f,fill=OLIVE_DARK+(aa,),anchor='ms')
            else:
                dt.text((w/2,120),ln,font=f,fill=(255,255,255,int(255*k)),anchor='ms')
            if k<1.0:
                blur=int((1-k)*22)
                if blur>0: txt=txt.filter(ImageFilter.GaussianBlur((blur,0)))
            im.alpha_composite(txt,(0,ty+i*112-60))
        return im
    return frame

def glow_card_plate(hole_w=1660,hole_h=880,w=1920,h=1080,cy=None):
    """dark grid field with a rounded transparent hole + soft glow ring.
    Returns RGBA plate; media composited UNDER it."""
    base=grid_field(w,h).convert('RGBA')
    cx=(w-hole_w)//2
    cy=(h-hole_h)//2 if cy is None else cy
    # glow ring: blurred rounded rect painted BEFORE hole cut
    glow=Image.new('RGBA',(w,h),(0,0,0,0))
    rr(ImageDraw.Draw(glow),[cx-8,cy-8,cx+hole_w+8,cy+hole_h+8],36,(224,232,180,180))
    glow=glow.filter(ImageFilter.GaussianBlur(22))
    base.alpha_composite(glow)
    # cut the hole
    mask=Image.new('L',(w,h),255)
    rr(ImageDraw.Draw(mask),[cx,cy,cx+hole_w,cy+hole_h],28,0)
    base.putalpha(mask)
    return base,(cx,cy,hole_w,hole_h)

def ffwd_glyph(w=1920):
    """two white chevrons, top-right, subtle pulse."""
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        d=ImageDraw.Draw(im)
        a=int(200+40*math.sin(t*6))
        x0,y0=1770,64
        for k in range(2):
            xx=x0+k*44
            d.polygon([(xx,y0),(xx+34,y0+26),(xx,y0+52)],fill=(255,255,255,a))
        return im
    return frame

def cta_pill(text,y0=940,size=54,w=1920,style='olive'):
    f=font(size,'Bold')
    pad=44
    tw=f.getlength(text)
    bw=int(tw)+2*pad; bh=int(size*1.75)
    x0=(w-bw)//2
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        d=ImageDraw.Draw(im)
        a=int(255*min(1.0,t/0.15))
        if style=='olive':
            p=plate(bw,bh,rad=16)
            if a<255: p.putalpha(p.getchannel('A').point(lambda v:v*a//255))
            im.alpha_composite(p,(x0,y0))
            col=(255,255,255)
        else:
            rr(d,[x0,y0,x0+bw,y0+bh],16,PILLW+(a,)); col=OLIVE
        reveal=int(max(0,t-0.1)*24)
        im=draw_text_reveal(im,(x0+pad,y0+int(bh*0.14)),text,f,col,reveal)
        return im
    return frame,bh

def price_pill(pre,amount,w=1920,y0=930,size=52):
    """'You can buy it for' pill + big amount snapping in."""
    f=font(size,'SemiBold'); fa=font(int(size*1.9),'Bold')
    pad=40
    tw=f.getlength(pre); aw=fa.getlength(amount)
    bw=int(tw+aw)+2*pad+36; bh=int(size*2.2)
    x0=(w-bw)//2
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        a=int(255*min(1.0,t/0.15))
        p=plate(bw,bh,rad=18)
        if a<255: p.putalpha(p.getchannel('A').point(lambda v:v*a//255))
        im.alpha_composite(p,(x0,y0))
        d=ImageDraw.Draw(im)
        d.text((x0+pad,y0+bh//2),pre,font=f,fill=(255,255,255,a),anchor='lm')
        if t>0.5:
            k=min(1.0,(t-0.5)/0.18)
            sz=int(size*1.9*(1.6-0.6*k))
            fa2=font(sz,'Bold')
            aa=int(255*k)
            d.text((x0+pad+tw+36+aw/2,y0+bh//2),amount,font=fa2,fill=(255,244,200,aa),anchor='mm')
        return im
    return frame,bh

def ai_label(w=1920,x0=1416,y0=140):
    f=font(30,'Bold')
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        d=ImageDraw.Draw(im)
        a=int(230*min(1.0,t/0.2))
        rr(d,[x0,y0,x0+300,y0+54],10,(20,20,20,a))
        d.text((x0+150,y0+27),"AI GENERATED",font=f,fill=(255,255,255,a),anchor='mm')
        return im
    return frame

def subscribe_anim(w=1920,y0=920):
    """white bar bottom-center: thumbs-up + red SUBSCRIBE -> grey SUBSCRIBED + bell;
    a cursor clicks it."""
    fb=font(34,'Bold')
    bw,bh=560,110
    x0=(w-bw)//2
    def frame(t):
        im=Image.new('RGBA',(w,1080),(0,0,0,0))
        d=ImageDraw.Draw(im)
        a=int(255*min(1.0,t/0.2))
        rr(d,[x0,y0,x0+bw,y0+bh],20,(255,255,255,a))
        # thumb icon (vector)
        tx,ty=x0+70,y0+bh//2
        d.rounded_rectangle([tx-26,ty-2,tx-12,ty+20],radius=3,fill=(60,60,64,a))
        d.rounded_rectangle([tx-10,ty-4,tx+26,ty+20],radius=6,fill=(60,60,64,a))
        d.rounded_rectangle([tx-6,ty-22,tx+6,ty+2],radius=5,fill=(60,60,64,a))
        clicked=t>2.0
        col=(224,226,229,a) if clicked else (212,32,32,a)
        label="SUBSCRIBED" if clicked else "SUBSCRIBE"
        rr(d,[x0+140,y0+22,x0+430,y0+bh-22],12,col)
        d.text((x0+285,y0+bh//2),label,font=fb,fill=(70,70,70,a) if clicked else (255,255,255,a),anchor='mm')
        # bell (vector)
        bx,by=x0+490,y0+bh//2
        d.pieslice([bx-16,by-18,bx+16,by+14],180,360,fill=(60,60,64,a))
        d.rectangle([bx-16,by-2,bx+16,by+6],fill=(60,60,64,a))
        d.ellipse([bx-5,by+8,bx+5,by+16],fill=(60,60,64,a))
        # cursor moves in and clicks at t=2.0
        if 0.6<t<3.2:
            k=min(1.0,(t-0.6)/1.2)
            cxp=int(x0+680-(k*400)); cyp=int(y0+170-k*90)
            press=1.0 if 1.95<t<2.15 else 0.0
            szc=int(38-6*press)
            d.polygon([(cxp,cyp),(cxp+szc*0.62,cyp+szc*0.4),(cxp+szc*0.28,cyp+szc*0.45),
                       (cxp+szc*0.42,cyp+szc*0.85),(cxp+szc*0.3,cyp+szc*0.9),
                       (cxp+szc*0.16,cyp+szc*0.5),(cxp,cyp+szc*0.7)],fill=(20,20,20,a),
                      outline=(255,255,255,a))
        # confetti burst after click
        if 2.0<t<3.0:
            rng=np.random.RandomState(7)
            for i in range(26):
                ang=rng.uniform(0,2*math.pi); sp=rng.uniform(120,420)
                tt=t-2.0
                px=x0+280+math.cos(ang)*sp*tt
                py=y0+40+math.sin(ang)*sp*tt+200*tt*tt
                cc=[(240,80,60),(250,200,60),(90,180,90),(80,140,240)][i%4]
                aa=int(a*max(0,1-tt))
                d.rectangle([px,py,px+8,py+8],fill=cc+(aa,))
        return im
    return frame

def encode_seq(frame_fn,dur,out,w=1920,h=1080,fps=FPS):
    """render frame(t) sequence to a qtrle mov with alpha via png pipe."""
    import subprocess
    n=int(round(dur*fps))
    cmd=["ffmpeg","-nostdin","-v","error","-f","image2pipe","-framerate","30000/1001",
         "-i","-","-c:v","qtrle","-y",out]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(n):
        im=frame_fn(i/fps)
        im.save(p.stdin,format='PNG')
    p.stdin.close(); p.wait()
    return out
