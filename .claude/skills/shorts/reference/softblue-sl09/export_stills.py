#!/usr/bin/env python3
"""SL-09 round 1 (SFL R2): one still per title band, crop level, clip, phone screen, scene and key-point bar of a short, on
its real frame (the same Short class the renderer uses, so a still IS the frame the short shows), plus a 540p context clip of
each item with about 3 s either side, cut from the delivered short's REVIEW copy (PRE-RENDER-APPROVAL: "Play it moving, in context").
  export_stills.py S..   -> review/stills/<S>_<nn>_<id>.jpg (+ _sm.jpg), review/context/<S>_<id>-context - REVIEW 540p.mp4, review/items_<S>.json"""
import json, os, sys, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import cv2, batch as Bt, plans as P
Bt.cv2 = cv2
import composite as Cm
R = Bt.WORK + "/review"; FPS = Bt.FPS
KIND = {"clip": "clip", "psolo": "phone", "hf": "graphic"}
def run(S, review_copy):
    os.makedirs(R + "/stills", exist_ok=True); os.makedirs(R + "/context", exist_ok=True)
    s = Bt.Short(S); C = Cm.Compositor(s.man, wh=(Bt.W, Bt.H)) if s.man else None
    words = json.load(open(f"{s.d}/words.json")); say = lambda a, b: " ".join(w["w"] for w in words if a - 0.05 <= w["t"] < b)
    want = [(int(1.2 * FPS), "title", "title", 0.0, s.N / FPS, "Title band, on screen for the whole short: " + P.TITLE[S][0] + " / " + " ".join(P.TITLE[S][1]))]
    seen = set()
    for sh in s.shots:
        a, b = sh["f0"] / FPS, sh["f1"] / FPS; n = sh["f1"] - sh["f0"]
        if sh["kind"] == "talk":
            w = sh.get("win", "full")
            if w not in seen:
                seen.add(w); want.append((sh["f0"] + min(n - 1, int(1.0 * FPS)), f"crop-{w}", "crop", a, b,
                                          f"You on camera, {'wider' if w == 'full' else 'closer'} crop ({Bt.WIN[w][0]} x {Bt.WIN[w][1]} of Zeeshan's frame, from its top row)"))
        else:
            c = sh["cover"]; kind = KIND.get(sh["kind"], "clip")
            if sh["kind"] == "clip": note = c.get("note") or (os.path.basename(c["src"]) if c["src"] != P.MASTER else f"Zeeshan's own footage at {int(c['t'] // 60)}:{c['t'] % 60:04.1f} of the film")
            elif sh["kind"] == "psolo": note = f"your real Oura app recording from the film ({int(c['t'] // 60)}:{c['t'] % 60:04.1f}), in our phone frame"
            else: note = "our moving Soft Blue scene"
            want.append((sh["f0"] + n // 2 if sh["kind"] != "hf" else sh["f1"] - int(0.6 * FPS), c["id"], kind, a, b, note))
    for m in s.man: want.append((Bt.fr(m["b"] - 0.7), m["id"], "bar", m["a"], m["b"], f"{m['topic']}: " + " / ".join(p[0] for p in m["parts"])))
    items = []
    for k, (i, gid, kind, a, b, note) in enumerate(sorted(want, key=lambda x: (x[3] if x[2] != "title" else -1, x[0]))):
        i = min(max(i, 0), s.N - 1); f, sh = s.picture(i); f = s.finish(f, sh, i, C)
        name = f"{S}_{k:02d}_{gid}"; im = Image.fromarray(f); im.save(f"{R}/stills/{name}.jpg", quality=92); im.resize((540, 960), Image.LANCZOS).save(f"{R}/stills/{name}_sm.jpg", quality=88)
        ctx = None
        if kind not in ("title", "crop"):
            c0, c1 = max(0.0, a - 3.0), min(s.N / FPS, b + 3.0); ctx = f"context/{S}_{gid}-context - REVIEW 540p.mp4"
            subprocess.run([Bt.lib.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{c0:.3f}", "-i", review_copy, "-t", f"{c1 - c0:.3f}", "-c:v", "libx264", "-crf", "22",
                            "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/{ctx}"], check=True)
        items.append(dict(short=S, id=gid, kind=kind, img=name, a=round(a, 2), b=round(b, 2), at=round(i / FPS, 2), note=note, ctx=ctx,
                          during=say(a, b), before=say(max(0, a - 4), a), after=say(b, b + 4)))
    s.close(); json.dump(dict(short=S, total=s.N / FPS, title=P.TITLE[S], name=P.NAME[S], items=items), open(f"{R}/items_{S}.json", "w"), indent=1)
    print(S, len(items), "stills", flush=True)
if __name__ == "__main__":
    REV = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/oura-ring-review REVIEW"      # deliver.py's REV (a plain import would load the shared deliver package)
    for S in sys.argv[1:]: run(S, f"{REV}/{P.NAME[S]} - REVIEW 540p.mp4")
