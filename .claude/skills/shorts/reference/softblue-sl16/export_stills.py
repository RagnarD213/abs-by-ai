#!/usr/bin/env python3
"""SL-07 round 1: one still per title, crop level, clip, rebuilt graphic and key-point bar of a short, on its real frame
(the same Short class the renderer uses, so a still IS the frame the short will show).
  export_stills.py S..   -> round1/stills/<S>_<nn>_<id>.jpg (+ _sm.jpg) and round1/items_<S>.json"""
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import cv2, batch as Bt, plans as P
Bt.cv2 = cv2
import composite as Cm
R = Bt.WORK + "/round1"; FPS = Bt.FPS
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def run(S):
    os.makedirs(R + "/stills", exist_ok=True)
    s = Bt.Short(S); C = Cm.Compositor(s.man, wh=(Bt.W, Bt.H)) if s.man else None
    words = json.load(open(f"{s.d}/words.json")); say = lambda a, b: " ".join(w["w"] for w in words if a - 0.05 <= w["t"] < b)
    want = []                                           # (frame, id, kind, a, b, note)
    seen = set(); first_talk = next((sh for sh in s.shots if sh["kind"] == "talk"), None)
    for sh in s.shots:
        a, b = sh["f0"] / FPS, sh["f1"] / FPS; n = sh["f1"] - sh["f0"]
        if sh["kind"] == "talk":
            w = sh.get("win", "full")
            if w not in seen:
                seen.add(w); want.append((sh["f0"] + min(n - 1, int(1.0 * FPS)), f"crop-{w}", "crop", a, b, f"Crop level: {'wide' if w == 'full' else 'closer'} ({Bt.WIN[w][0]} x {Bt.WIN[w][1]} of the camera frame)"))
        elif sh["kind"] == "clip":
            c = sh["cover"]; want.append((sh["f0"] + n // 2, c["id"], "clip", a, b, os.path.basename(c["src"]) + (" (AI, chip on)" if c.get("ai") else "") + ("" if c.get("fit", "fill") == "fill" else f" [{c['fit']}]")))
        elif sh["kind"] == "phone": want.append((sh["f0"] + n // 2, sh["cover"]["id"], "phone", a, b, f"app recording {os.path.basename(sh['cover']['src'])[:5]} in the approved phone shell, beside you"))
        else: want.append((sh["f1"] - int(0.4 * FPS), sh["cover"]["id"], "graphic", a, b, "film graphic rebuilt for vertical"))
    for m in s.man: want.append((Bt.fr(m["b"] - 0.7), m["id"], "bar", m["a"], m["b"], f"{m['topic']}: " + " / ".join(p[0] for p in m["parts"])))
    items = []
    for k, (i, gid, kind, a, b, note) in enumerate(sorted(want, key=lambda x: (x[3], x[0]))):
        i = min(max(i, 0), s.N - 1); f, sh = s.picture(i); f = s.finish(f, sh, i, C)
        name = f"{S}_{k:02d}_{gid}"; im = Image.fromarray(f); im.save(f"{R}/stills/{name}.jpg", quality=92); im.resize((540, 960), Image.LANCZOS).save(f"{R}/stills/{name}_sm.jpg", quality=88)
        items.append(dict(short=S, id=gid, kind=kind, img=name, a=round(a, 2), b=round(b, 2), at=round(i / FPS, 2), note=note, during=say(a, b), before=say(max(0, a - 4), a), after=say(b, b + 4)))
    s.close(); json.dump(dict(short=S, total=s.N / FPS, head=s.T.get("head", 0), title=P.TITLE[S], name=P.NAME[S], items=items), open(f"{R}/items_{S}.json", "w"), indent=1)
    print(S, len(items), "stills", flush=True)
if __name__ == "__main__":
    for S in sys.argv[1:]: run(S)
