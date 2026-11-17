"""Exact same-size meal composite for the selected cover, preserving Dan's pixels."""
from pathlib import Path
import hashlib,json,uuid
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
P=Path('/Volumes/Extreme/_edit_work/DS-108-setup')
Q=P/'cover-r2'
src=Image.open(P/'google/g2.jpg').convert('RGB')
points=[(463,1047),(469,1043),(477,1047),(481,1040),(491,1030),(503,1024),(516,1023),(527,1027),(534,1023),(542,1017),(551,1015),(555,1005),(568,1000),(580,1004),(587,1009),(590,1017),(600,1014),(611,1008),(619,1014),(623,1023),(626,1030),(637,1029),(645,1033),(651,1042),(654,1056),(655,1065),(651,1071),(655,1080),(657,1094),(650,1101),(636,1107),(625,1108),(613,1114),(596,1118),(581,1121),(563,1122),(549,1119),(537,1117),(528,1110),(522,1104),(511,1101),(501,1098),(489,1095),(478,1090),(470,1084),(468,1075),(467,1068),(461,1062)]
mask=Image.new('L',src.size);ImageDraw.Draw(mask).polygon(points,fill=255)
# Fine gaps between the broccoli crowns reveal brown tabletop in the source.
# Exclude that backdrop instead of carrying brown wedges onto the white plate.
rgb=np.asarray(src).astype(np.int16);yy,xx=np.indices(rgb.shape[:2])
wood_gap=(xx>529)&(yy<1034)&(yy>995)&(rgb[:,:,0]>65)&(rgb[:,:,0]>rgb[:,:,1]+4)
matte=np.asarray(mask).copy();matte[wood_gap]=0
mask=Image.fromarray(matte).filter(ImageFilter.GaussianBlur(.45))
dx,dy=-348,0
shifted=Image.new('L',src.size);shifted.paste(mask,(dx,dy))
food=Image.new('RGB',src.size);food.paste(src,(dx,dy))
result=src.copy()
shadow=Image.new('RGBA',src.size)
ImageDraw.Draw(shadow).ellipse((112,1082,316,1129),fill=(25,17,7,25))
shadow=shadow.filter(ImageFilter.GaussianBlur(6))
result=Image.alpha_composite(result.convert('RGBA'),shadow).convert('RGB')
result.paste(food,(0,0),shifted)
# Proof is on lossless pixels before the paired JPEG exports, no food rescaling.
a=np.asarray(src);b=np.asarray(result);core=np.asarray(mask)==255
ys,xs=np.where(core);assert np.array_equal(a[ys,xs],b[ys+dy,xs+dx])
assert np.array_equal(a[:980],b[:980]),'Face/body/hands above plates changed'
assert np.array_equal(a[990:1140,430:705],b[990:1140,430:705]),'Original small plate changed'
out=Q/'identical-meal-source.png';tmp=out.with_name('identical-meal-source.'+uuid.uuid4().hex+'.png');result.save(tmp);tmp.replace(out)
mask.save(Q/'meal-mask.png')
receipt={'source_sha256':hashlib.sha256((P/'google/g2.jpg').read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'method':'One original photographic meal cutout translated without resizing onto the original empty large plate; original small plate retained. Subpixel mask edge and local contact shadow only.','translation':[dx,dy],'food_scale':1.0,'identical_opaque_food_pixels':int(core.sum()),'exact_core_pixel_match':True,'face_body_hands_above_plates_pixel_identical':True,'original_small_plate_pixel_identical':True,'generated_edit_disposition':'Retained but not used: matching ingredients, differing grain/broccoli shape and slight quantity drift failed the exact-meal requirement.','film_changed':False}
p=Q/'meal-identity-proof.json';tmp=p.with_name('meal-identity-proof.'+uuid.uuid4().hex+'.json');tmp.write_text(json.dumps(receipt,indent=2)+'\n');tmp.replace(p)
zoom=result.crop((25,975,710,1160)).resize((1370,370));zoom.save(Q/'same-meal-detail.jpg',quality=97)
print(json.dumps({'same_food_core_pixels':receipt['identical_opaque_food_pixels'],'scale':1.0,'source_face_unchanged':True,'file':str(out)}))
