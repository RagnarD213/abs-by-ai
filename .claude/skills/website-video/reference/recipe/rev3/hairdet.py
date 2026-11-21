#!/usr/bin/env python3
"""THE hair-top detector for the website video (ad-edit lesson 107): one module, three callers
(hairtrack.py on the 4K base, hairtrack_refine.py on the punched picture, qc_frame.py on the master).

Rev 3 anchored every crop to the HAIRLINE (first row of skin at r>120) minus a 40-px guess, and cut the
top of Dan's hair in 23 of 26 holds. Measured on the 4K base (probe4k / det3, 2026-09-08):
  * the door panel behind his head is (33,38,36), luma 36-37, row-mean sd 0.5 -- constant for the whole video
  * his hair is luma 20-30; the hair band (hair top -> skin) is 53-78 px of 4K when he is upright
  * the relaxed skin test (r>g+10, r>55, g>b) fires 56-68 px below the true hair top; the old r>120 fired ~60 px lower still
Detector, in 4K pixel units:
  1 per-column header luma from rows 100-180 (the door panel above the head); a pixel is HAIR-DARK when it is 5 levels
    darker than ITS OWN column's header, so the door's dark grooves never count as hair
  2 skin start = first row >= 40 where >= 50 % of the 160-px band is relaxed skin
  3 head centre = median x of the hair-dark pixels 8-48 rows above the skin start (second pass, so a sideways lean or
    the wood frame in the band cannot pull the band off the crown)
  4 walk UP from the skin start over the band's hair-dark fraction: keep the last row with >= 20 % hair-dark, stop after
    12 consecutive rows below that (the hairline transition and the sheen at the crown are tolerated). Hair top = last.
  5 valid only when the climb is 50-110 px: a shorter climb stopped INSIDE the hair (reads LOW, the dangerous direction),
    a longer one started on something that was not his forehead. Invalid samples are discarded, never used.
The delivered-scale callers crop the head region, resize it to 4K scale and run the SAME function; the per-column
header comes from the base's static column profile (hairtrack.json "hdr_col"), mapped through the crop.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BAND=80; T_DROP=5.0; FRAC=0.20; GAP=12; CLIMB=(50,110); SKIN_FRAC=0.5; TOP_MARGIN=40
def detect(im, cx_guess=1980, X0=0, hdr_col=None, hdr_rows=(100,180)):
    """im: HxWx3 int array (a 4K-scale crop whose column 0 is 4K x = X0). hdr_col: optional 4K-indexed
    per-column header luma (from hairtrack.json) -- when the frame has no door panel above the head
    (delivered frames), the caller passes the base's profile. Returns a dict; 'hair' is None on a miss."""
    H,W,_=im.shape
    r,g,b=im[...,0],im[...,1],im[...,2]; Y=0.299*r+0.587*g+0.114*b
    c=int(cx_guess-X0)
    if hdr_col is None:
        hc=np.median(Y[hdr_rows[0]:hdr_rows[1]],axis=0)
    else:
        xs=np.arange(W)+X0; hc=np.interp(xs,np.arange(len(hdr_col)),hdr_col)
    lo,hi=max(0,c-BAND),min(W,c+BAND)
    header=float(np.median(hc[lo:hi]))
    T=np.minimum(hc-T_DROP,header-T_DROP)
    dark=(Y<T[None,:])
    skin=((r>g+10)&(r>55)&(g>b))
    frac=skin[:, lo:hi].mean(1)
    rows=np.where(frac[TOP_MARGIN:]>=SKIN_FRAC)[0]
    if len(rows)==0: return dict(header=round(header,1),skin=None,hair=None,cx=None,climb=None,valid=False,why="no skin")
    s=int(rows[0]+TOP_MARGIN)
    ys,xs=np.where(dark[max(0,s-48):max(0,s-8), max(0,c-300):min(W,c+300)])
    cx=int(np.median(xs))+max(0,c-300) if len(xs)>50 else c
    lo,hi=max(0,cx-BAND),min(W,cx+BAND)
    df=dark[:, lo:hi].mean(1)
    y=s-1; gap=0; last=None
    while y>0:
        if df[y]>=FRAC: last=y; gap=0
        else:
            gap+=1
            if gap>GAP: break
        y-=1
    if last is None: return dict(header=round(header,1),skin=s,hair=None,cx=cx+X0,climb=0,valid=False,why="no hair run")
    hair=int(last); climb=s-hair; ok=CLIMB[0]<=climb<=CLIMB[1]
    return dict(header=round(header,1),skin=s,hair=hair,cx=cx+X0,climb=climb,valid=bool(ok),
                why=None if ok else ("climb too short (stopped inside the hair)" if climb<CLIMB[0] else "climb too long"))
def stretch(a):
    a=a.astype(float); lo,hi=np.percentile(a,1),np.percentile(a,99)
    return np.clip((a-lo)/(hi-lo+1e-6)*255,0,255).astype(np.uint8)
def proof_sheet(items,out,TW=560,TH=340,cols=4,grid0=None):
    """items: [(label, im (np HxWx3 at 4K scale), X0, det dict, y_line, y_line2)]: NATIVE-scale crops of the head,
    contrast-stretched, 50-px grid labelled in 4K rows, the hair line (green) and the skin line (cyan). This is the sheet
    a human looks at before anything renders (lesson 107: 480-px tiles hid a 90-px error)."""
    rows=(len(items)+cols-1)//cols
    sh=Image.new("RGB",(TW*cols,(TH+22)*rows),(0,0,0)); d=ImageDraw.Draw(sh)
    try: fnt=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",16)
    except Exception: fnt=ImageFont.load_default()
    for i,(lab,im,x0abs,dd) in enumerate(items):
        cx=(dd.get("cx") or 1980)-x0abs; xs=max(0,cx-TW//2); y0=max(0,(dd.get("hair") or 220)-100)
        crop=im[y0:y0+TH, xs:xs+TW]
        tile=Image.fromarray(stretch(crop.astype(np.uint8))); td=ImageDraw.Draw(tile)
        for gy in range((y0//50+1)*50,y0+TH,50):
            td.line([(0,gy-y0),(TW,gy-y0)],fill=(255,0,0) if gy%100==0 else (120,0,0),width=1); td.text((2,gy-y0-14),str(gy),fill=(255,255,0),font=fnt)
        if dd.get("hair") is not None: td.line([(0,dd["hair"]-y0),(TW,dd["hair"]-y0)],fill=(0,255,0),width=2)
        if dd.get("skin") is not None: td.line([(0,dd["skin"]-y0),(TW,dd["skin"]-y0)],fill=(0,255,255),width=1)
        X=(i%cols)*TW; Yy=(i//cols)*(TH+22)
        sh.paste(tile,(X,Yy+22)); d.text((X+4,Yy+3),lab,fill=(255,255,0),font=fnt)
    sh.save(out,quality=90); return out
