"""Round-1 stills: every graphic/clip on its real graded frame at a representative moment + context speech."""
import sys, json, os
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro16/recipe")
import frames as F, gfx as G
W = "/Volumes/Extreme/_edit_work/ro16"; OUT = f"{W}/round1/stills"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json")); WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
CLIPTS = {}
rows = []
only = set(sys.argv[1:])
for it in R:
    if only and it["id"] not in only: continue
    t1 = it["t1"] or it["t0"] + 3
    if it["kind"] in ("l3",): t = (it.get("reveal_t") or [it["t0"]])[-1] + .6
    elif it["kind"] in ("scene", "title"): t = min(t1 - .15, it["t0"] + 2.6)
    elif it["kind"] == "lt": t = it["t0"] + 2.0
    else: t = (it["t0"] + t1) / 2
    fr = "W2" if it["kind"] in ("l3", "phone") else F.shot_at(t)["framing"]
    frame = F.frame_at(t, fr)
    clip = None
    if it["kind"] in ("clip", "phone") and it.get("src"):
        src = G.src_path(it["src"][0]); clip = G.clip_frame(src, G.src_start(it["src"][0]) + 1.0, it.get("zoom", 1.0)) if it["kind"] == "clip" else G.clip_frame(src, 5.0).resize((574, 1080))
        if it["kind"] == "phone":
            import subprocess
            p = subprocess.run([G.FF, "-v", "error", "-ss", "5", "-i", src, "-frames:v", "1", "-vf", "format=rgb24", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            from PIL import Image; import io; clip = Image.open(io.BytesIO(p)).convert("RGB")
    if it["kind"] == "ai": 
        from PIL import Image
        clip = Image.open(f"{W}/aiframes/A-start.png").convert("RGB").resize((1920, 1080))
    im = G.paint(frame, t, [it], fr, clip)
    im.save(f"{OUT}/{it['id']}.jpg", quality=90)
    rows.append(dict(id=it["id"], kind=it["kind"], t0=it["t0"], t1=it["t1"], still_t=round(t, 2), framing=fr,
                     before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1 + 5),
                     copy={k: it[k] for k in ("topic", "point", "heading", "points", "headline", "eyebrow", "detail", "label", "items") if k in it},
                     src=it.get("src"), note=it.get("note")))
    print(it["id"], flush=True)
if not only: json.dump(rows, open(f"{W}/round1/stills.json", "w"), indent=1)
