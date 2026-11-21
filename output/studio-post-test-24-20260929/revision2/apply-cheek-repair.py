from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import json
r=Path(__file__).resolve().parent.parent
original=Image.open(r/'assets/studio-blue-11-photo.jpg').convert('RGB')
repair=Image.open(r/'revision2/cheek-repaired.png').convert('RGB').resize((135,130),Image.Resampling.LANCZOS)
layer=original.copy();layer.paste(repair,(520,245))
mask=Image.new('L',original.size)
ImageDraw.Draw(mask).ellipse((600,295,611,316),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1.5))
fixed=Image.composite(layer,original,mask)
fixed.save(r/'assets/studio-blue-11-photo-r2.png')
box=ImageChops.difference(original,fixed).getbbox()
assert box[0]>=590 and box[1]>=285 and box[2]<=622 and box[3]<=327,box
(r/'revision2/cheek-repair.json').write_text(json.dumps({'source':'assets/studio-blue-11-photo.jpg','output':'assets/studio-blue-11-photo-r2.png','changed_pixel_bbox':box,'method':'Codex subscription spot repair composited only within a feathered cheek mask; every pixel outside the recorded bounds is unchanged.'},indent=2))
out=Image.new('RGB',(800,520),'white')
for j,im in enumerate([original,fixed]):out.paste(im.crop((545,260,645,390)).resize((400,520)),(400*j,0))
out.save(r/'revision2/cheek-before-after.jpg')
print('Localized repair:',box)
