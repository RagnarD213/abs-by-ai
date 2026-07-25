import base64, io, json, requests, os
from PIL import Image

BASE = "https://absbyai.com"
TOKEN = open(os.path.join(os.path.dirname(__file__), ".demotoken")).read().strip()
H = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/"


def data_url(path, size=None):
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# Insert oldest-first so the last one ends up on top of the gallery (ordered id DESC).
PAIRS = [
    # gym male: our own proof pair
    (ROOT + "public/img/proof/male-before.webp",
     ROOT + "public/img/proof/male-after.webp",
     {"condition": "moderate", "intensity": "max"}),
    # heavier beach male: source photo + Dan's chosen candidate E
    (ROOT + "public/img/proof/male2-before.webp",
     ROOT + "app-store-assets/hero-candidates/E-chosen-flux-heavier.jpg",
     {"condition": "heavier", "intensity": "max"}),
]

for before, after, settings in PAIRS:
    body = {"before": data_url(before), "after": data_url(after), "settings": settings}
    r = requests.post(BASE + "/api/transformations", headers=H, json=body, timeout=120)
    print(os.path.basename(before), r.status_code, r.text[:200])

r = requests.get(BASE + "/api/transformations", headers=H, timeout=60)
items = r.json()["transformations"]
print("\ngallery now:", len(items), "cards")
for t in items:
    print(" id", t["id"], "hero", t["is_hero"], "settings", t["settings"])
