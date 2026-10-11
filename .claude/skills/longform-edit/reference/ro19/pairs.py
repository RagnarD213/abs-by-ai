"""RO-19 photo scenes (Soft Blue Light, softblue.py): Dan's real before / after tan pictures, and three portraits from the
pool shoot. Each plan clip item that carries `pair=[before, after]` (+ optional `reveal="phrase he says"`: the after picture
comes up on that phrase) or `portraits=[a, b, c]` is rendered to gfx/<id>.mp4, an opaque insert as long as its slot. The plan
points the item's src at that file. Crops: photos/<name>.jpg (head to thigh, person mask, made once by the crop step).
usage: pairs.py [IDS...] | still ID out.png [t]"""
import sys, os, json, re
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import softblue as B
from PIL import ImageDraw
W = "/Volumes/Extreme/_edit_work/ro19"; PH = f"{W}/photos"; OUT = f"{W}/gfx"; os.makedirs(OUT, exist_ok=True)
LABEL = "Real pictures of me. Not AI-generated."
def tab(im, cx, y, s, u, t, delay):
    """caption tab under a photo: glass pill, white title-case text"""
    q = B.ease(t - delay)
    if q <= 0: return
    f = B.font(0.031 * im.size[1], True); tw = B.text_w(s, f); bw, bh = tw + 0.03 * im.size[0], 0.056 * im.size[1]
    box = (cx - bw / 2, y, cx + bw / 2, y + bh)
    B.glass(im, box, t, u, radius=16)
    ImageDraw.Draw(im).text((cx - tw / 2, y + 0.009 * im.size[1]), s, font=f, fill=B.WHITE)
def scene_pair(t, w, h, before, after, reveal=0.6, caps=("Before The Tan", "After The Tan")):
    im = B.field(t, w, h); u = B.unit(w, h)
    pw, ph = 0.3146 * w, 0.3146 * w * 1.25; gap = 0.05 * w; x0 = (w - 2 * pw - gap) / 2; y0 = 0.04 * h
    for i, (p, d) in enumerate(((before, 0.0), (after, reveal))):
        x = x0 + i * (pw + gap)
        B.photo_card(im, f"{PH}/{p}.jpg", (x, y0, pw, ph), t, d, fit=True, u=u)
        tab(im, x + pw / 2, y0 + ph + 0.030 * h, caps[i], u, t, d + 0.15)
    B.disclosure(im, LABEL, (w / 2, y0 + ph + 0.108 * h), u, anchor="mt", size=19)
    return im
def scene_three(t, w, h, photos):
    return B.scene_portraits(t, w, h, [f"{PH}/{p}.jpg" for p in photos], LABEL)
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def when(words, phrase, lo, hi):
    toks = [norm(x) for x in phrase.split() if norm(x)]; ws = [x for x in words if lo - 0.5 <= x["t0"] <= hi]
    for i in range(len(ws)):
        if [norm(x["w"]) for x in ws[i:i + len(toks)]] == toks: return ws[i]["t0"]
    raise SystemExit(f"reveal phrase not found: {phrase!r}")
if __name__ == "__main__":
    R = json.load(open(f"{W}/plan_resolved.json")); WO = [x for x in json.load(open(f"{W}/words_out.json")) if x["t0"] is not None]
    if len(sys.argv) > 1 and sys.argv[1] == "still":
        it = next(r for r in R if r["id"] == sys.argv[2]); t = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
        im = scene_pair(t, 1920, 1080, *it["pair"], reveal=0.6) if it.get("pair") else scene_three(t, 1920, 1080, it["portraits"])
        im.convert("RGB").save(sys.argv[3]); sys.exit()
    only = set(sys.argv[1:])
    for it in R:
        if not (it.get("pair") or it.get("portraits") or it.get("photo")) or (only and it["id"] not in only): continue
        dur = it["t1"] - it["t0"] + 0.6
        if it.get("pair"):
            rv = when(WO, it["reveal"], it["t0"], it["t1"]) - it["t0"] if it.get("reveal") else 0.6
            fn = lambda t, it=it, rv=rv: scene_pair(t, 1920, 1080, *it["pair"], reveal=max(0.3, rv))
        elif it.get("photo"):
            fn = lambda t, it=it: B.scene_photo(t, 1920, 1080, f"{PH}/{it['photo']}.jpg", "Real picture of me. Not AI-generated.")
        else:
            fn = lambda t, it=it: scene_three(t, 1920, 1080, it["portraits"])
        B.render_scene(f"{OUT}/{it['id']}.mp4", dur, fn); print("rendered", it["id"], round(dur, 2), "s", flush=True)
