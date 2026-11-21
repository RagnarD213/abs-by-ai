#!/usr/bin/env python3
"""Remove backgrounds from finished photos -> full-res transparent PNG cutouts.

The proven Abs By AI recipe (validated 2026-08-31 on the studio shoot):
  1. Downscale a COPY to 2048 long edge and send that to Replicate BiRefNet
     (851-labs/background-remover). The model only ever produces a MASK.
  2. Upscale the returned ALPHA ONLY back to full res (LANCZOS) and apply it
     to the ORIGINAL pixels — the subject is never re-rendered, so there is
     zero identity/edit risk on retouched finals.
  3. Contract the alpha edge ~2px (MinFilter(5) + GaussianBlur(1)) to kill
     the 1-2px bright halo left by backdrop light wrap (worst on white).

Usage:
  python3 removebg.py IMG [IMG...] --out DIR [--contract 2] [--sheet] [--force]

  --out       output directory (created if missing)
  --contract  edge contraction in px: 0=raw, 2=default, 3=aggressive
  --sheet     also write a <base>_SHEET.jpg QC sheet per image
              (original | checker | magenta overview + auto 1:1 zooms)
  --force     rebuild even if the output PNG already exists (default: skip)

Cost: ~$0.002/image. Token comes from ~/.absbyai-secrets.env — read with a
grep, NOT `source` (a line in that file silently breaks shell sourcing).
"""
import argparse, io, json, os, sys, time, urllib.request

API = "https://api.replicate.com/v1"
MODEL = "851-labs/background-remover"


def token():
    p = os.path.expanduser("~/.absbyai-secrets.env")
    for line in open(p):
        if line.startswith("REPLICATE_API_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"')
    sys.exit("REPLICATE_API_TOKEN not found in ~/.absbyai-secrets.env")


def api(path, tok, data=None, raw=None, ctype=None):
    req = urllib.request.Request(API + path)
    req.add_header("Authorization", "Bearer " + tok)
    # Replicate's edge 403s the default Python-urllib user agent
    req.add_header("User-Agent", "absbyai-removebg/1.0")
    body = None
    if raw is not None:
        body, req.headers["Content-Type"] = raw, ctype
    elif data is not None:
        body = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, body) as r:
        return json.load(r)


def latest_version(tok):
    # Fetch the FULL hash — never reconstruct it from a truncated prefix.
    return api(f"/models/{MODEL}", tok)["latest_version"]["id"]


def upload(tok, jpeg_bytes, name):
    bnd = "----removebg%d" % int(time.time() * 1000)
    body = (
        (f"--{bnd}\r\nContent-Disposition: form-data; name=\"content\"; "
         f"filename=\"{name}\"\r\nContent-Type: image/jpeg\r\n\r\n").encode()
        + jpeg_bytes + f"\r\n--{bnd}--\r\n".encode()
    )
    return api("/files", tok, raw=body,
               ctype=f"multipart/form-data; boundary={bnd}")["urls"]["get"]


def predict(tok, version, image_url, timeout=180):
    pred = api("/predictions", tok, data={"version": version,
                                          "input": {"image": image_url}})
    t0 = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > timeout:
            raise RuntimeError("prediction timed out: " + pred["id"])
        time.sleep(3)
        pred = api("/predictions/" + pred["id"], tok)
    if pred["status"] != "succeeded":
        raise RuntimeError(f"prediction {pred['status']}: {pred.get('error')}")
    out = pred["output"]
    return out[0] if isinstance(out, list) else out


def checker(size, sq=24):
    import numpy as np
    from PIL import Image
    xx, yy = np.meshgrid(np.arange(size[0]) // sq, np.arange(size[1]) // sq)
    c = ((xx + yy) % 2 * 50 + 150).astype("uint8")
    return Image.fromarray(np.stack([c] * 3, -1))


def auto_zoom_spots(alpha, n=4, cs=500):
    """Pick QC crop centres automatically: the top of the subject (hair) plus
    the regions densest in soft-edge alpha — which is where keying is hardest
    (flyaways, enclosed holes, chains, glasses)."""
    import numpy as np
    a = np.array(alpha)
    ys, xs = np.nonzero(a > 128)
    spots = []
    if len(ys):
        top = ys.min()
        band = xs[ys < top + 80]
        spots.append(("hair/top", int(band.mean()), int(top + cs // 4)))
    soft = ((a > 10) & (a < 245)).astype(np.uint8)
    g = cs  # grid cell = crop size so picks don't overlap
    H, W = soft.shape
    cells = [(soft[y:y + g, x:x + g].sum(), x + g // 2, y + g // 2)
             for y in range(0, H - g, g) for x in range(0, W - g, g)]
    for s, cx, cy in sorted(cells, reverse=True):
        if len(spots) >= n:
            break
        if all(abs(cx - px) > g or abs(cy - py) > g for _, px, py in spots):
            spots.append((f"soft edge ({cx},{cy})", cx, cy))
    return spots


def build_sheet(orig, cut, path):
    from PIL import Image, ImageDraw
    s = 900 / cut.size[1]
    ow = round(cut.size[0] * s)
    small = cut.resize((ow, 900), Image.LANCZOS)
    osml = orig.resize((ow, 900), Image.LANCZOS)
    CS, W = 500, max(2050, ow * 3 + 60)
    sheet = Image.new("RGB", (W, 900 + CS + 90), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    x0 = (W - (ow * 3 + 40)) // 2
    sheet.paste(osml, (x0, 10))
    cb = checker(small.size); cb.paste(small, (0, 0), small)
    sheet.paste(cb, (x0 + ow + 20, 10))
    mg = Image.new("RGB", small.size, (255, 0, 255)); mg.paste(small, (0, 0), small)
    sheet.paste(mg, (x0 + 2 * (ow + 20), 10))
    for i, t in enumerate(["original", "cutout on checker", "cutout on magenta (fringe check)"]):
        d.text((x0 + i * (ow + 20), 918), t, fill=(255, 255, 255))
    for i, (label, cx, cy) in enumerate(auto_zoom_spots(cut.split()[-1])):
        c = cut.crop((cx - CS // 2, cy - CS // 2, cx + CS // 2, cy + CS // 2))
        bg = Image.new("RGB", (CS, CS), (255, 0, 255)); bg.paste(c, (0, 0), c)
        x = 10 + i * (CS + 10)
        sheet.paste(bg, (x, 950))
        d.text((x + 6, 950 + CS + 8), label + "  1:1", fill=(255, 255, 255))
    sheet.save(path, quality=90)


def process(path, out_dir, tok, version, contract, sheet, force):
    from PIL import Image, ImageFilter
    base = os.path.splitext(os.path.basename(path))[0].replace("_FINAL_PRIMARY", "")
    dest = os.path.join(out_dir, base + "_CUTOUT.png")
    if os.path.exists(dest) and not force:
        print(f"  skip (exists): {base}")
        return dest
    orig = Image.open(path).convert("RGB")
    w, h = orig.size
    sc = 2048 / max(w, h)
    buf = io.BytesIO()
    orig.resize((round(w * sc), round(h * sc)), Image.LANCZOS).save(
        buf, "JPEG", quality=92)
    url = upload(tok, buf.getvalue(), base + ".jpg")
    out_url = predict(tok, version, url)
    png = urllib.request.urlopen(out_url).read()
    model_out = Image.open(io.BytesIO(png)); model_out.load()
    if model_out.mode != "RGBA":
        raise RuntimeError(f"{base}: model returned {model_out.mode}, expected RGBA")
    alpha = model_out.split()[-1].resize(orig.size, Image.LANCZOS)
    if contract > 0:
        k = contract * 2 + 1          # 2px -> MinFilter(5), the validated default
        alpha = alpha.filter(ImageFilter.MinFilter(k)).filter(
            ImageFilter.GaussianBlur(contract / 2))
    cut = orig.copy(); cut.putalpha(alpha)
    cut.save(dest)
    # sanity: subject fraction should be plausible for a person shot
    import numpy as np
    frac = (np.array(alpha) > 128).mean()
    flag = "" if 0.10 < frac < 0.85 else "  <-- CHECK: odd subject fraction"
    print(f"  {base}: subject {frac:.1%} of frame -> {dest}{flag}")
    if sheet:
        build_sheet(orig, cut, os.path.join(out_dir, base + "_SHEET.jpg"))
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--contract", type=int, default=2)
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok = token()
    version = latest_version(tok)
    print(f"{MODEL} @ {version[:12]}…  contract={a.contract}px  n={len(a.images)}")
    fails = 0
    for p in a.images:
        try:
            process(p, a.out, tok, version, a.contract, a.sheet, a.force)
        except Exception as e:
            fails += 1
            print(f"  FAIL {os.path.basename(p)}: {e}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
