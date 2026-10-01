import sys, pathlib
SH = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
sys.path.insert(0, str(SH)); import softblue as B
from PIL import Image
out = pathlib.Path(__file__).resolve().parent / "labels"; out.mkdir(exist_ok=True)
for name, s in (("AI-GENERATED", "AI-GENERATED"), ("REAL-PICTURE", "Real picture of me, not AI-generated")):
    for pos, y in (("top", 96), ("below-top-graphic", 336)):
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        box = B.disclosure(im, s, xy=(60, y), u=1.75, size=23)
        im.save(out / f"label_{name}_{pos}.png")
    c = im.crop(tuple(int(v) for v in (box[0], box[1], box[2] + 1, box[3] + 1))); c.save(out / f"label_{name}_chip-only.png")
print(sorted(p.name for p in out.iterdir()))
