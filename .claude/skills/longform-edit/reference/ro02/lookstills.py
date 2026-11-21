import os, sys, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro02"; O = f"{W}/round1/look"
import frames as F
S = F.S; FPS = F.FPS
def t_of(shot_id, frac=0.5):
    s = next(x for x in S if x["id"] == shot_id); return (s["out_f0"]+(s["out_f1"]-s["out_f0"])*frac)/FPS
MOM = [("hook", "hook.0r0", 0.3), ("cloud", "types.2", 0.5), ("demo", "steps.0r0", 0.75)]
for name, sid, fr in MOM:
    t = t_of(sid, fr)
    for look in ("A", "B"):
        F.LOOK = look
        for fm in ("F", "N"):
            F.frame_at(t, fm).save(f"{O}/{name}-{look}-{fm}.jpg", quality=93)
    F.frame_at(t, "N", look=False).save(f"{O}/{name}-raw-N.jpg", quality=93)
    print(name, sid, round(t, 2), "gamma", F.gamma(F.shot_at(t)))
ims = [[f"{O}/{n}-{k}.jpg" for k in ("raw-N", "A-N", "B-N", "A-F")] for n, _, _ in MOM]
sh = Image.new("RGB", (4*640, 3*360))
for j, row in enumerate(ims):
    for i, f in enumerate(row): sh.paste(Image.open(f).resize((640, 360)), (i*640, j*360))
sh.save(f"{W}/tmp/look_sheet.jpg", quality=88)
