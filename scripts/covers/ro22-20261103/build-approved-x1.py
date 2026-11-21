from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import hashlib,json,datetime

W=Path('/Volumes/Extreme/_edit_work/RO-22/setup/thumbnails/revision2')
SOURCE=W.parent/'choices/originals/real-04a2609ea8f3.jpg'
im=Image.open(SOURCE).convert('RGB')
assert im.size==(1280,720)
original=im.copy()
d=ImageDraw.Draw(im)
d.rectangle((0,0,1279,195),fill='#17222e')
copy=['How Fat Loss','Looksmaxxes Your Face']
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Impact.ttf',84)
boxes=[]
for n,line in enumerate(copy):
    b=d.textbbox((0,0),line,font=font)
    width=b[2]-b[0]
    assert width<=1190
    x=(1280-width)//2-b[0];y=12+n*82-b[1]
    d.text((x,y),line,font=font,fill='white' if n==0 else '#6ce8f6')
    boxes.append(d.textbbox((x,y),line,font=font))
assert max(b[3] for b in boxes)<=184
assert ImageChops.difference(original.crop((0,196,1280,720)),im.crop((0,196,1280,720))).getbbox() is None
png=W/'X1-revised.png';jpeg=W/'X1-revised.jpg'
im.save(png)
im.save(jpeg,quality=97,subsampling=0)
assert jpeg.stat().st_size<2_000_000
receipt={'date':'2026-11-03','owner':'01a197ed-ea42-71a0-9d71-d64adc2d2be8','message_id':'01a1a1f2-034d-7003-ab6b-c0fa0ff36704','dan_words':'Let\'s go with X1 but change the text to "How Fat Loss Looksmaxxes Your Face"\n','pick':'X1','status':'REVISED_IMAGE_PENDING_DAN_APPROVAL','copy':' '.join(copy),'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'real_photo_model_trial_excluded':True,'picture_and_layout_preserved':True,'decoded_pixels_below_header_identical_in_PNG':True,'new_AI_generation':0,'paid_api_spend':0,'text_boxes':boxes,'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [png,jpeg]],'installed':False,'uploaded_for_distribution':False,'scheduled':False}
(W/'REVISION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Revised X1 built; photo/layout pixels unchanged in PNG. JPEG under2MB. Pending exact-image approval.')
