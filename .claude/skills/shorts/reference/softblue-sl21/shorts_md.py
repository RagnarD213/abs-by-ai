#!/usr/bin/env python3
"""Write Short-form video content/whattocut-SHORTS.md (in/out, title, parent, clips, key point, transcript) from plans.py + build data."""
import json, os, re, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P
W = "/Users/danielrose/Projects/_edit_work/SL-21"; OUT = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
L = ["# whattocut-SHORTS.md: SL-21 What To Cut SFL R1", "",
     "Parent: RO-20B \"What To Cut To Afford Getting In Shape\", round 4 master sha256 88a6314f43424b28312dacdc1775b73ae7d17c8bf45212f6ffdc2bfccd86dec1 (Dan finalized 2026-10-20). "
     "Picture from the film's graphics-free base.mp4 (same frames and clock), audio verbatim from the master. Parent YouTube release: Fri Dec 11, 2026 (kitchen film); "
     "these Shorts air only after it is public (kitchen Shorts go to February per the 10-28 calendar; the handoff's Mon Nov 30 date is retired).",
     "Dan's picks 2026-11-13: A, D, E as recommended, titles as proposed. No covers made here (setup makes them). No AI clips in any of the three (ai_generated: false at setup).", ""]
for n, S in enumerate(("A", "D", "E"), 1):
    T = json.load(open(f"{W}/build/{S}/timeline.json")); f = f"{OUT}/{P.NAME[S]}.mp4"
    L += [f"## Short {n}: {' '.join(P.TITLE[S][1])} ({S})", f"File: `Short-form video content/{P.NAME[S]}.mp4` ({T['total']:.2f} s, {T['frames']} frames)" + (f", sha256 {sha(f)}" if os.path.exists(f) else ""),
          "Film in/out: " + ", ".join(f"{a:.3f}-{b:.3f}" for a, b in P.SEG[S]),
          "Cutaways (film times): " + "; ".join(f"{c['id']} {c['a']}-{c['b']}" for c in P.COVERS[S]),
          "Key point: " + " / ".join(l for l, _ in P.BARS[S][0]["parts"]), "AI clips (set ai_generated: true at setup): none", "", "Transcript:",
          "> " + re.sub(r"\s+", " ", re.sub(r"\{[^}]*\}", "", P.TEXT[S]).replace(" | ", " ").replace(" / ", " ").replace("_", " ")), ""]
open(f"{OUT}/whattocut-SHORTS.md", "w").write("\n".join(L)); print("written", len(L), "lines")
