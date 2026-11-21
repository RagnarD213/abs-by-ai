"""RO-05 graphic layers, built on the approved Codex/Muhammad primitives (06-organic-r4/muhammad_graphics.py).
Every function returns (full_frame_flag, [dict(image, start_offset, motion)])."""
import sys,re
R4="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/06-organic-r4"
sys.path.insert(0,R4)
import muhammad_graphics as MG
from PIL import Image,ImageDraw
W,H=1920,1080;OL=MG.M_OLIVE;WHITE=MG.WHITE;INK=MG.INK;DARK=(19,25,21,236);ACC=(205,216,171,255)
def blank():return Image.new('RGBA',(W,H))

def _bar(label,x,y,tab=None,n=44,tabw=96,h=110,maxw=1500,rich=False):
    """white bar with an olive tab (Muhammad lower third). Returns (base_im, label_im, bar_right)."""
    f=MG.font(n);lw=_rich_len(label,n) if rich else f.getlength(label)
    ww=min(maxw,max(560,int(lw)+tabw+84))
    im=blank();d=ImageDraw.Draw(im)
    d.rounded_rectangle((x+tabw-22,y+8,x+ww,y+h-8),12,fill=WHITE)
    d.rounded_rectangle((x,y,x+tabw,y+h),12,fill=OL);d.rectangle((x+tabw//2,y,x+tabw,y+h),fill=OL)
    if tab:MG.text(im,(x+tabw/2,y+h/2),tab,40 if len(tab)<=2 else 24,style='Bold',anchor='mm')
    li=blank()
    if rich:_rich(li,(x+tabw+26,y+h/2),label,n,maxw=ww-tabw-50)
    else:MG.text(li,(x+tabw+26,y+h/2),label,n,INK,maxw=ww-tabw-50)
    return im,li,x+ww

def _rich_len(s,n):
    return sum(MG.font(n,'Bold' if seg.isupper() and any(c.isalpha() for c in seg) else 'SemiBold').getlength(seg) for seg in re.split(r'(\s+)',s))
def _rich(im,xy,s,n,maxw):
    """Dan's KEY POINT format: FULL-CAPS words carry the punch (Bold olive-dark), the rest SemiBold ink."""
    while _rich_len(s,n)>maxw and n>26:n-=1
    x,y=xy;d=ImageDraw.Draw(im)
    for seg in re.split(r'(\s+)',s):
        caps=seg.isupper() and any(c.isalpha() for c in seg) and len(seg.strip(':'))>1
        f=MG.font(n,'Bold' if caps else 'SemiBold');d.text((x,y),seg,font=f,fill=((84,96,38,255) if caps else INK),anchor='lm');x+=f.getlength(seg)

def xy(pos,ww,hh,top_y=56):
    """tl / tr / bl / br / bottom(centre) / right(split-screen column). Measured per graphic by place.py."""
    if pos=='right':return 640,800
    if pos in('top','tl'):return 70,top_y
    if pos=='tr':return 1850-ww,top_y
    if pos=='bl':return 70,915-hh
    if pos=='br':return 1850-ww,915-hh
    return (W-ww)//2,915-hh
def lower(text,pos='bottom',tab=None,keypoint=False,n=44,top_y=56):
    tabw=132 if keypoint else 96
    label=text
    f=MG.font(n);lw=_rich_len(label,n) if keypoint else f.getlength(label);ww=min(1560 if pos!='right' else 1220,max(560,int(lw)+tabw+84))
    x,y=xy(pos,ww,110,top_y)
    im,li,_=_bar(label,x,y,None,n,tabw,110,1560 if pos!='right' else 1220,rich=keypoint)
    if keypoint:
        d=ImageDraw.Draw(im);f=MG.font(25,'Bold')
        d.multiline_text((x+tabw/2,y+55),'KEY\nPOINT',font=f,fill=WHITE,anchor='mm',align='center',spacing=2)
    elif tab:MG.text(im,(x+tabw/2,y+55),tab,40,style='Bold',anchor='mm')
    return False,[dict(image=im,start=0,motion='fade'),dict(image=li,start=.16,motion='wipe-wide' if pos!='top' else 'wipe')]

def solid(text,pos='bottom',top_y=56):
    """solid olive pill (topic / CTA)."""
    im=blank();li=blank();d=ImageDraw.Draw(im);n=48;ww=int(MG.font(n).getlength(text))+120
    x,y=xy(pos,ww,110,top_y)
    d.rounded_rectangle((x,y,x+ww,y+110),14,fill=OL,outline=(205,216,171,120),width=2)
    MG.text(li,(x+ww/2,y+55),text,n,WHITE,anchor='mm')
    return False,[dict(image=im,start=0,motion='fade'),dict(image=li,start=.14,motion='fade')]

def ingredient(num,name,sub=None,pos='tl',top_y=56):
    """numbered ingredient card with the app's per-salad figure on a dark sub-bar; position measured per graphic."""
    ww=min(1100,max(560,int(MG.font(44).getlength(name))+96+84));subw=int(MG.font(28,'Regular').getlength(sub))+44+74 if sub else 0
    x,y=xy(pos,max(ww,subw),110+(60 if sub else 0),top_y)
    im,li,right=_bar(name,x,y,num,44,96,110,1100)
    out=[dict(image=im,start=0,motion='fade'),dict(image=li,start=.16,motion='wipe')]
    if sub:
        s=blank();d=ImageDraw.Draw(s);f=MG.font(28,'Medium') if False else MG.font(28,'Regular')
        sw=int(f.getlength(sub))+44;d.rounded_rectangle((x+74,y+116,x+74+sw,y+116+54),10,fill=DARK)
        MG.text(s,(x+96,y+143),sub,28,ACC,style='Regular')
        out.append(dict(image=s,start=.45,motion='fade'))
    return False,out

def speed(factor):
    im=blank();d=ImageDraw.Draw(im);x1,y=1850,56;w=176;x0=x1-w
    d.rounded_rectangle((x0,y,x1,y+72),12,fill=DARK,outline=(205,216,171,110),width=2)
    for k in (0,1):
        ax=x0+26+k*26;d.polygon([(ax,y+20),(ax,y+52),(ax+24,y+36)],fill=ACC)
    MG.text(im,(x0+118,y+37),f'{factor}x',34,WHITE,style='Bold',anchor='mm')
    return False,[dict(image=im,start=0,motion='fade')]

def title(lines):
    return MG.layers(dict(kind='title',text=lines,a=0.0))[0] or True, MG.layers(dict(kind='title',text=lines,a=0.0))[1]

def left_list(title_text,items,reveals_rel,subtitle=None):
    g=dict(kind='left-list',text=title_text,items=items,reveals=reveals_rel,a=0.0)
    if subtitle:g['subtitle']=subtitle
    return MG.layers(g)

def endcard():
    im=MG.gradient();d=ImageDraw.Draw(im)
    MG.text(im,(960,400),'See Yourself With Abs',54,(235,240,220,255),style='SemiBold',anchor='mm')
    f=MG.font(150,'BoldItalic');tw=f.getlength('Free At');d.rounded_rectangle((960-tw/2-40,470,960+tw/2+40,650),24,fill=(25,31,18,255))
    MG.text(im,(960,560),'Free At',150,WHITE,style='BoldItalic',anchor='mm')
    MG.text(im,(960,715),'AbsByAI.com',60,WHITE,style='SemiBold',anchor='mm')
    return True,[dict(image=im,start=0,motion='fade')]
