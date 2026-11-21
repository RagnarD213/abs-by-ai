import sys, json, numpy as np
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RO-29/round2/recipe")
import gfx as G
from grades import GR
from PIL import Image, ImageDraw
P = json.load(open("/Volumes/Expansion/_edit_work/RO-29/round2/plan_resolved.json")); items = P if isinstance(P, list) else P["items"]
R1 = "/Volumes/Expansion/_edit_work/RO-29/round1/review/stills/"
ids = list(GR); S = Image.new("RGB", (1920, 1350)); n = 0
def stat(im):
    a = np.asarray(im.resize((480,270))).astype(float)/255; Y = .2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]; s=(a.max(2)-a.min(2))/(a.max(2)+1e-6)
    return f"Y {np.median(Y)*255:.0f} p90 {np.percentile(Y,90)*255:.0f} sat {np.median(s):.2f} blk {100*(Y<.06).mean():.0f}%"
ref = Image.open(R1+"G14.jpg").convert("RGB"); print("presenter", stat(ref))
for i in ids:
    it = next(x for x in items if x["id"] == i); sp = it["src"][0]; path = G.src_path(sp); t = G.src_start(sp) + 1.0
    a = G.clip_frame(path, t, it.get("zoom", 1.0), None, it.get("crop")); b = G.clip_frame(path, t, it.get("zoom", 1.0), GR[i], it.get("crop"))
    print(i, "before", stat(a), "| after", stat(b))
    for k, im in enumerate((a, b)):
        t_ = im.resize((480, 270)); ImageDraw.Draw(t_).text((6, 6), f"{i} {'raw' if k==0 else 'graded'}", fill=(255,255,0))
        S.paste(t_, ((n % 4)*480, (n//4)*270)); n += 1
S.save("/private/tmp/claude-501/-Users-danielrose-Projects-Claude-Projects-Abs-By-AI/d5812518-de65-4eb9-a91c-2ea7e4db3d0a/scratchpad/grades.jpg", quality=90)
