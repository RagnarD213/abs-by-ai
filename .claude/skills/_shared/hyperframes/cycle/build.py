"""Soft Blue Light CYCLE card (HyperFrames): a 4-step loop in the left-third card, Dan beside it.
Approved by Dan 2026-09-30 (C1652 pilot: "significantly better than the graphics that we're using").

Usage:
    python3 build.py config.json OUT_DIR [--render]

config.json is a list of scenes. Every time is the WORD's start in the finished film (from mapped-words.json);
build.py converts to scene-relative seconds. Two scene kinds:

  {"id": "down", "kind": "build", "a": 272.0384, "b": 286.0858, "title": "The downward spiral", "hue": "red",
   "direction": "cw", "boxes": ["TL", "TR", "BR", "BL" copy in that order],
   "reveal": {"TL": 272.41, "BR": 276.69, "TR": 278.59, "BL": 279.71},   # each box lands on its word
   "close": 281.55, "pulse": 281.97, "drift": 12}

  {"id": "turn", "kind": "flip", "a": 289.3891, "b": 297.1969, "title": "Turn the spiral around",
   "old_title": "The downward spiral", "hue": "teal", "direction": "ccw",
   "old_boxes": [the red scene's boxes, TL TR BR BL], "boxes": [the opposites, same corners],
   "title_swap": 289.55, "flip": {"TL": 290.11, "BL": 290.97, "BR": 292.51, "TR": 293.65},
   "close": 295.29, "pulse": 295.73, "drift": -12}

direction "cw" loops TL>TR>BR>BL, "ccw" loops TL>BL>BR>TR. hue: "red" (B.BAD, a bad loop) or "teal" (a good loop).
drift: px the diagram sinks (+) or rises (-) over the scene. Each scene becomes OUT_DIR/<id>/ (its own HyperFrames
project; lint rejects two roots in one folder). --render writes OUT_DIR/<id>.mov (ProRes 4444, alpha, 29.97).
"""
import json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
VERSION = "0.8.97"
FONT = ROOT / "Media/codex-video-trial/assets/fonts/Poppins-Bold.ttf"
BIN = ROOT / "Media/video_edit/bin"


def rel(t, a):
    return round(t - a, 3)


def scene_cfg(s):
    a = s["a"]
    c = dict(id=s["id"], dur=round(s["b"] - a, 3), direction=s["direction"], title=s["title"], hue=s["hue"],
             boxes=s["boxes"], close=rel(s["close"], a), pulse=rel(s["pulse"], a), drift=s.get("drift", 0))
    if s["kind"] == "build":
        c["reveal"] = {k: rel(v, a) for k, v in s["reveal"].items()}
    else:
        c.update(old_title=s["old_title"], old_boxes=s["old_boxes"], title_swap=rel(s["title_swap"], a),
                 flip={k: rel(v, a) for k, v in s["flip"].items()})
    return c


def package_json(name):
    cmd = lambda v: f"npx --yes hyperframes@{VERSION} {v}"
    return json.dumps(dict(name=name, private=True, type="module",
                           scripts=dict(dev=cmd("preview"), check=cmd("check"), render=cmd("render"))), indent=2)


def main():
    cfg_path, out = sys.argv[1], pathlib.Path(sys.argv[2])
    render = "--render" in sys.argv
    tpl = (HERE / "cycle.template.htm").read_text()
    env = dict(os.environ, PATH=f"{BIN}:{os.environ['PATH']}", HYPERFRAMES_SKIP_SKILLS="1")
    for s in json.load(open(cfg_path)):
        c = scene_cfg(s)
        d = out / c["id"]; (d / "assets").mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(tpl.replace("__CFG__", json.dumps(c, indent=2))
                                      .replace("__ID__", c["id"]).replace("__DUR__", str(c["dur"])))
        (d / "package.json").write_text(package_json(c["id"]))
        (d / "hyperframes.json").write_text(json.dumps({"paths": {"assets": "assets"}}, indent=2))
        font = d / "assets/Poppins-Bold.ttf"
        if not font.exists(): font.write_bytes(FONT.read_bytes())
        npx = ["npx", "-y", f"hyperframes@{VERSION}"]
        for step in (["lint"], ["check"]):
            r = subprocess.run(npx + step, cwd=d, env=env, capture_output=True, text=True)
            ok = r.returncode == 0 and " 0 error" in (r.stdout + r.stderr).replace("0 errors", " 0 error")
            print(c["id"], step[0], "ok" if ok else "FAILED");
            if not ok: print(r.stdout[-3000:], r.stderr[-2000:]); sys.exit(1)
        if render:
            subprocess.run(npx + ["render", "--format", "mov", "--fps", "30000/1001", "-o", str((out / f"{c['id']}.mov").resolve())],
                           cwd=d, env=env, check=True)
            print(c["id"], "rendered", out / f"{c['id']}.mov")


if __name__ == "__main__":
    main()
