"""Locked-design recap: original typography/card pixels; live Soft Blue Light field and specular accents.
Config: id, a/b, approved_card path, heading, points (audit text), reveal (film seconds), rows (pixel boxes).
Uses shared HyperFrames 0.8.97. Full-screen opaque. Does not change approved text or geometry.
"""
import sys,json,pathlib,hashlib
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]));import hfbuild as H
HERE=pathlib.Path(__file__).resolve().parent

def scene(c,out):
    im=Image.open(c["approved_card"]).convert("RGB");assert im.size==(1920,1080)
    cfg=dict(c,dur=round(c["b"]-c["a"],6),times=[round(t-c["a"],6) for t in c["reveal"]])
    d=H.make_scene(HERE/"recap-card.template.htm",cfg,out)
    # Extract the approved glyphs without carrying the old opaque background over the live field.
    x=np.array(im.crop((0,0,1920,215)));alpha=np.uint8(np.clip((x[:,:,0].astype(float)-28)/18,0,1)*255)
    rgba=Image.fromarray(np.dstack([x,alpha]));rgba.save(d/"assets/heading.png")
    for i,box in enumerate(c["rows"]):
        x0,y0,x1,y1=box;p=im.crop(box).convert("RGBA");a=np.array(p)
        # Remove only the old 181x4 cyan accent. The moving accent has identical dimensions and colour.
        a[1:5,107:288,:3]=a[6:7,107:288,:3];p=Image.fromarray(a)
        mask=Image.new("L",p.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,p.width-1,p.height-1),56,fill=255)
        p.putalpha(mask);p.save(d/"assets"/f"row{i}.png")
    return d
if __name__=="__main__":
    cfgs=json.load(open(sys.argv[1]));out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
    for c in cfgs:
        d=scene(c,out);H.lint_check(d)
        if "--render" in sys.argv:H.render(d,out/(c["id"]+".mov"))
