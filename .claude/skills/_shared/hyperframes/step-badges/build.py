"""Step badges (Soft Blue Light HyperFrames): round glass number badges that land beside items, keep drifting, exit with the
scene. First use SL-06 R7 short C (the injection kit flat lay). Not yet approved by Dan as a template (shown in context there).
  python3 build.py config.json OUT_DIR [--render out.mov]
Config: {"id": "...", "dur": 2.84, "canvas": [1080, 1920], "r": 52, "badges": [[cx, cy, "1", at_seconds], ...]}"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import hfbuild as H
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
d = H.make_scene(pathlib.Path(__file__).with_name("step-badges.template.htm"), cfg, out)
H.lint_check(d)
if "--render" in sys.argv: H.render(d, sys.argv[sys.argv.index("--render") + 1])
print("scene", d)
