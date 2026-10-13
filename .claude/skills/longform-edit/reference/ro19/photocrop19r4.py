"""RO-19 round 4 photo crop (Dan's round 3 note, 2026-10-13). Writes NEW files only (photos/pale4_single.jpg, photos/crops_r4.json).
pale4_single: the single pale photo at 0:48. Dan: "the picture at 49 seconds, change it to this picture here" (his attachment: round4-plan/dan-pick-P02.jpg,
  804x978). It is Photos asset 77D35A5F (1 April, 14:50:50, 2865x3486, exported with sips + exif_transpose to src/pale_r4_pick.jpg; grey correlation with his
  attachment 0.997, same colour). His explicit pick: used as he sent it, not swapped and not re-tinted. It is a smaller copy of the camera frame taken the
  same second (asset 5AC50078, holds it 1:1 at offset 759, 1247, match 0.989) and is warmer than that frame (chest skin 216/156/118 against 214/168/136):
  said on the page in one line. Cropped the way round 3's single was: head top from the person mask, navel row 1858 read off a ruled close-up, 0.06 above
  the hair, 0.45 below the navel, 4:5, so his abs read at the same size as on the card it replaces.
usage: photocrop19r4.py"""
import json, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19/photos"
src, wb, KT, KB = "pale_r4_pick", 1858, 0.06, 0.45
im = Image.open(f"{W}/src/{src}.jpg").convert("RGB"); m = np.asarray(Image.open(f"{W}/mask_r4/{src}.mask.png").convert("L").resize(im.size)) > 127
rows = np.nonzero(m.sum(1) > im.width*0.01)[0]; top = int(rows[0]); D = wb - top; yc = top + int(0.45*D); cx = float(np.median(np.nonzero(m[yc])[0]))
h = (1 + KT + KB)*D; w = 0.8*h; y0 = max(0, top - KT*D); x0 = min(max(0, cx - w/2), im.width - w); assert y0 + h <= im.height + 1 and w <= im.width
im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1200, 1500), Image.LANCZOS).save(f"{W}/pale4_single.jpg", quality=93)
out = {"pale4_single": dict(src=src, asset="77D35A5F", head_top=top, landmark=wb, D=int(D), cx=int(cx), crop=[int(x0), int(y0), int(w), int(h)],
                            margin_above_hair=round((top - y0)/D, 3), upscale=round(1200/w, 3))}
json.dump(out, open(f"{W}/crops_r4.json", "w"), indent=1); print(json.dumps(out, indent=1))
