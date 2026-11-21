"""RO-11 round 3 review media: the seven section cards with a picture on the right (titles.py), as settled stills and as
moving context clips (3 s of speech either side) through the film's own renderer. plan_resolved.json is NOT rewritten this
round (it is locked until Dan approves the cards): the photo fields are merged onto the title items in memory.
usage: round3.py stills | context [IDS...] | contextB T1 | frames"""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro11/recipe")
import build as Bd, gfx as G, titles as T
W = "/Volumes/Extreme/_edit_work/ro11"; OUT = f"{W}/round4"; FF = Bd.FF
REC = "frame"                                  # the recommended layout
TI = [it for it in Bd.R if it["kind"] == "title"]
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
def patch(layout_for):
    for it in Bd.R:
        if it["kind"] == "title": it.update(T.item(it["id"], layout_for(it["id"])))
def review_copy(path, name):
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "22", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", name], check=True)
def context(it, tag=""):
    os.makedirs(f"{OUT}/context", exist_ok=True)
    a, b = max(0.0, it["t0"] - 3.0), min(Bd.S[-1]["out_f1"] / Bd.FPS, it["t1"] + 3.0)
    out = f"{OUT}/context/{it['id']}{tag}-context.mp4"
    Bd.render_range(a, b, out); review_copy(out, f"{OUT}/context/{it['id']}{tag}-context - REVIEW 540p.mp4")
    json.dump(dict(id=it["id"], t0=a, t1=b, card=[it["t0"], it["t1"]]), open(out + ".t0.json", "w"))

if __name__ == "__main__":
    what = sys.argv[1]; only = set(sys.argv[2:])
    if what == "stills":
        os.makedirs(f"{OUT}/stills", exist_ok=True); rows = []
        for it in TI:
            dur = it["t1"] - it["t0"]; tl = dur - 0.2
            for lay in ("frame", "bleed"):
                x = T.item(it["id"], lay)
                G.title_card(tl, it["step"], it["headline"], x["photo"], x["label"], lay, x["chip"]).save(f"{OUT}/stills/{it['id']}_{lay}.jpg", quality=92)
            G.title_card(tl, it["step"], it["headline"]).save(f"{OUT}/stills/{it['id']}_before.jpg", quality=92)
            c = T.TITLES[it["id"]]
            rows.append(dict(id=it["id"], t0=it["t0"], t1=it["t1"], step=it["step"], headline=it["headline"], what=c["what"], licence=c["licence"],
                             url=c.get("url"), label=c["label"], src=os.path.basename(c["src"]),
                             before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], it["t1"]), after=speech(it["t1"], it["t1"] + 5)))
            print(it["id"], round(it["t0"], 2), round(dur, 2), flush=True)
        json.dump(rows, open(f"{OUT}/stills.json", "w"), indent=1)
    elif what == "context":
        patch(lambda k: REC)
        for it in TI:
            if only and it["id"] not in only: continue
            context(it)
    elif what == "contextB":
        patch(lambda k: "bleed")
        for it in TI:
            if it["id"] in only: context(it, "B")
    elif what == "frames":
        # entrance and exit, read off the rendered clips: last frame before the card, its first 6 frames, settle, last, first after
        from PIL import Image
        os.makedirs(f"{OUT}/checks", exist_ok=True)
        for it in TI:
            for tag in ("", "B"):
                p = f"{OUT}/context/{it['id']}{tag}-context.mp4"
                if not os.path.exists(p): continue
                t0 = json.load(open(p + ".t0.json"))["t0"]; f0 = Bd.fr(it["t0"]) - Bd.fr(t0); f1 = Bd.fr(it["t1"]) - Bd.fr(t0)
                pick = [f0 - 1, f0, f0 + 3, f0 + 6, f0 + 10, f0 + 15, f0 + 22, f1 - 1, f1]
                sel = "+".join(f"eq(n\\,{n})" for n in pick)
                d = f"{OUT}/checks/{it['id']}{tag}"; os.makedirs(d, exist_ok=True)
                subprocess.run([FF, "-v", "error", "-y", "-i", p, "-vf", f"select='{sel}',scale=640:360", "-vsync", "0", f"{d}/%02d.png"], check=True)
                ims = [Image.open(f"{d}/{i + 1:02d}.png") for i in range(len(pick))]
                sh = Image.new("RGB", (640 * 3, 360 * 3))
                for k, im in enumerate(ims): sh.paste(im, ((k % 3) * 640, (k // 3) * 360))
                sh.save(f"{OUT}/checks/{it['id']}{tag}_entrance.jpg", quality=85); print(it["id"] + tag, pick, flush=True)
