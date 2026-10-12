"""RO-19 round 3 photo crops (Dan's round 2 notes, 2026-10-12). Writes NEW files only (photos/pale3_*.jpg, photos/crops_r3.json).
pale3_down: the pale half of pair 1 from the UNTINTED original. Dan: "this is actually a tan filter on that photo. The original was significantly more
  pale. Find the original". The card he approved was cut from a 2417x3348 filtered copy (Photos asset C60DD02A). The frame taken the same second
  (asset 99501C7F, 4284x5712, exported from Photos with originals on, src/pale_r3_down.jpg) holds that copy 1:1 at offset (695, 1476) (template match
  0.998; chest skin 228/162/129 against the filtered 229/143/103), so the approved crop box is reused shifted by that offset: same framing, same body
  scale against the tanned half, only the tint is gone.
pale3_single: the single pale photo at 0:48. Dan: "use a picture where I'm pale, but I still have defined abs ... the one where I'm standing on the
  driveway". Driveway set, 14:50:13 (asset 06D979F4, src/pale_r3_drive.jpg): the frame of the set with the clearest abs and his eyes open. Head top from
  the person mask, navel row 3750 read off a ruled close-up, the same margins as round 2's single (0.06 above the hair, 0.45 below the navel).
usage: photocrop19r3.py"""
import json, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19/photos"
R2 = json.load(open(f"{W}/crops_r2.json")); OFF = json.load(open(f"{W}/mask_r3/down_offset.json"))
out = {}
x, y, w, h = R2["pale2_down"]["crop"]; im = Image.open(f"{W}/src/pale_r3_down.jpg").convert("RGB")
box = (x + OFF["ox"], y + OFF["oy"], x + OFF["ox"] + w, y + OFF["oy"] + h); assert box[2] <= im.width and box[3] <= im.height
im.crop(box).resize((1200, 1500), Image.LANCZOS).save(f"{W}/pale3_down.jpg", quality=93)
out["pale3_down"] = dict(src="pale_r3_down", asset="99501C7F", crop=[box[0], box[1], w, h], same_box_as="pale2_down", offset=[OFF["ox"], OFF["oy"]], match=OFF["match"])
src, wb, KT, KB = "pale_r3_drive", 3750, 0.06, 0.45
im = Image.open(f"{W}/src/{src}.jpg").convert("RGB"); m = np.asarray(Image.open(f"{W}/mask_r3/{src}.mask.png").convert("L").resize(im.size)) > 127
rows = np.nonzero(m.sum(1) > im.width*0.01)[0]; top = int(rows[0]); D = wb - top; yc = top + int(0.45*D); cx = float(np.median(np.nonzero(m[yc])[0]))
h = (1 + KT + KB)*D; w = 0.8*h; y0 = max(0, top - KT*D); x0 = min(max(0, cx - w/2), im.width - w); assert y0 + h <= im.height + 1 and w <= im.width
im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1200, 1500), Image.LANCZOS).save(f"{W}/pale3_single.jpg", quality=93)
out["pale3_single"] = dict(src=src, asset="06D979F4", head_top=top, landmark=wb, D=int(D), cx=int(cx), crop=[int(x0), int(y0), int(w), int(h)])
json.dump(out, open(f"{W}/crops_r3.json", "w"), indent=1); print(json.dumps(out, indent=1))
