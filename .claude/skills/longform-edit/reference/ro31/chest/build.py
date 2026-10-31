"""Chest diagram scene. usage: build.py config.json OUT [--render]. Times in the film clock, a/b the scene's edges."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H
def scene_cfg(s):
    a, b = s["a"], s["b"]
    P = []
    for p in s["panels"]:
        q = dict(p); q["t"] = max(0, H.rel(p["t"], a))
        q["calls"] = [dict(c, t=H.rel(c["t"], a)) for c in p.get("calls", [])]
        P.append(q)
    return dict(id=s["id"], dur=round(b - a, 3), eyebrow=s["eyebrow"], panels=P)
if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2])
    H.run_all([(HERE / "chest-diagram.template.htm", scene_cfg(s), ()) for s in (cfg if isinstance(cfg, list) else [cfg])], out, "--render" in sys.argv)
