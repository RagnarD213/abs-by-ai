#!/usr/bin/env python3
"""RA-12: round1/gfx_sheet.json = the plan's overlays (CTA x2, the KEY POINT lower third) + A1, the shared Soft Blue analysis card
(Dan 2026-10-14, the standard for every video), its rows landing on the words that start their clause."""
import json, re, os
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).strip()
def word_t(ph, after=0.0):
    toks = norm(ph).split(); seq = [norm(w["w"]) for w in W]
    for i in range(len(W) - len(toks) + 1):
        if W[i]["t"] >= after and seq[i:i + len(toks)] == toks: return round(W[i]["t"], 3)
    raise KeyError(ph)
A1 = next(c for c in B["cards"] if c["name"] == "A1"); a, b = A1["beat"]
G = [dict(id=g["id"], template=g["template"], t0=g["t0"], t1=g["t1"], config=g["config"]) for g in B["overlays"]]
G.append({"id": "A1", "template": "analysis-card", "t0": a, "t1": b, "config": {
    "photo": "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/example pictures/dan by pool.png", "label": "AI-GENERATED",
    "reveal": [word_t("exactly how much fat", a), word_t("you have to lose", a), word_t("gain muscle", a)],
    "band": ["YOUR PERSONAL PLAN", word_t("to make your dream", a)], "a": a, "b": b}})
G.sort(key=lambda g: g["t0"])
os.makedirs("round1", exist_ok=True)
json.dump({"graphics": G}, open("round1/gfx_sheet.json", "w"), indent=1)
for g in G: print(g["id"], g["template"], g["t0"], g["t1"], json.dumps(g["config"])[:160])
