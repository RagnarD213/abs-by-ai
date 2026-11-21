"""RO-24 round 4 (from round 3's photos_r3.py): photo scenes P4-P7. Round 3's note: the photo scenes of the first three minutes, rebuilt from round 2's build_photos.py (same template, same
frame, push and chip) with Dan's round 2 notes: every person gets their weight lost and medication in his approved wording,
and before / after pairs wherever the person lost weight. P0 now shows all six people.

  python3 photos_r3.py [--only P0,P3] [--render] [--force] [--snap]

Times are on the round 3 timeline (film_words_r3.json, edl_r3.json). Writes photo_assets/, configs/, projects/<id>/,
renders/<id>.mov, stills/raw/<id>-n.png, and photos_manifest.json (kind opaque) + plan_photos_r4.json.
"""
import argparse, hashlib, json, pathlib, re, subprocess, sys
from PIL import Image, ImageOps
HERE = pathlib.Path(__file__).resolve().parent; R3 = HERE.parent.parent / 'round3'; R2 = R3.parent / 'round2'
sys.path.insert(0, "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H                                    # noqa: E402
import from_plan as FP                                 # noqa: E402
FPS = 30000 / 1001
TPL = R3 / "hf/templates/photo-scene/photo-scene.template.htm"
W = FP.Words(str(HERE.parent / "film_words_r4.json"))   # round 4 timeline (Tracy retime)
STAT = {"Sharon Osbourne": "42 lb, Ozempic", "Fat Joe": "200 lb, Ozempic", "Amy Schumer": "50 lb, Mounjaro",
        "Meghan Trainor": "60 lb, Mounjaro", "Oprah Winfrey": "Down to 155 lb, GLP-1", "Tracy Morgan": "On Ozempic, gained 40 lb"}
META = {pathlib.Path(x["file"]).stem: dict(x, root=R2 / "photos") for x in json.load(open(R2 / "photos/photos.json"))}
META.update({pathlib.Path(x["file"]).stem: dict(x, root=R3 / "photos") for x in json.load(open(R3 / "photos/photos_r3.json"))})
# on-screen credits for the round 3 photos (photographer / agency as printed where the photo was found)
CREDIT3 = {"sharon_before_2019_million_little_pieces": "Getty Images", "sharon_before_2021_the_talk_set": "CBS via Getty Images",
           "sharon_after_2025_villa_park_announcement": "Samir Hussein/Getty Images for Live Nation UK",
           "amy_before_2023_good-foundation-carnegie-hall": "Getty Images for Good+Foundation",
           "amy_before_2024_variety-power-of-women": "George Chinsee/Variety via Getty Images", "amy_after_2026_lorne-premiere": "Cindy Ord/WireImage",
           "meghan_before_2020_tommynow-london-fashion-week": "Mike Marsland/WireImage", "oprah_before_2022_tiff-sidney-premiere": "Getty Images",
           "oprah_before_2023_wes-moore-reception": "Maryland GovPics (CC BY 2.0)", "fatjoe_before_2002_mtv-trl-times-square": "Dimitrios Kambouris/WireImage",
           "fatjoe_after_2026_espy-awards": "AP Photo/Yuki Iwamura", "tracy_after_2025_snl50-red-carpet": "Evan Agostini/Invision/AP",
           "meghan_before_2019_star-wars-premiere-london": "hawtcelebs.com"}


def path(stem):
    return META[stem]["root"] / META[stem]["file"]


def credit(stem):
    if stem in CREDIT3: return CREDIT3[stem]
    m = META[stem]; s = m["outlet_or_author"]
    if s.startswith("Wikimedia Commons:"):
        return s.split(":", 1)[1].strip() + (f" ({m['licence']})" if m.get("licence") else "")
    mm = re.search(r"\(photo: (.*)\)\s*$", s)
    s = mm.group(1) if mm else s
    return re.sub(r",\s*id\s*\d+", "", s).strip()


_FB = {}
def facebox(stem):
    if stem not in _FB:
        r = subprocess.run([str(pathlib.Path.home() / ".cache/absbyai/facebox"), str(path(stem))], capture_output=True, text=True, check=True).stdout
        _FB[stem] = [int(v) for v in r.strip().split("\t")[1].split()]
    return _FB[stem]


def crop(stem, aspect, k=None, top=0.55, x_bias=0.0):
    im = Image.open(path(stem)); iw, ih = im.size
    fx0, fy0, fx1, fy1 = facebox(stem); fh = fy1 - fy0; cx = (fx0 + fx1) / 2 + x_bias * fh
    if k is None:
        h = min(ih, iw / aspect); wd = h * aspect; y0 = 0 if h >= ih else max(0, min(ih - h, fy0 - 0.6 * fh))
    else:
        h = min(ih, k * fh, iw / aspect); wd = h * aspect; y0 = max(0, min(ih - h, fy0 - top * fh))
    x0 = max(0, min(iw - wd, cx - wd / 2))
    return [round(x0), round(y0), round(x0 + wd), round(y0 + h)]


def asset(stem, box, disp_w, disp_h, out):
    im = ImageOps.exif_transpose(Image.open(path(stem))).convert("RGB").crop(tuple(box))
    scale = min(1.0, 1.6 * disp_w / im.width)
    if scale < 1: im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    im.save(out, quality=92)
    return out


CHIP_PX, CHIP_H, CHIP_PAD, CHIP_R = 34, 58, 28, 18
STAT_PX, CITE_PX = 44, 22
BELOW = 22 + CHIP_H + 6 + round(STAT_PX * 1.4) + 4 + 31          # chip, the stat line, the credit


def chip(s, cx, y):
    wd = round(H.text_w(s, CHIP_PX, False) + 2 * CHIP_PAD)
    return dict(s=s, x=round(cx - wd / 2), y=y, w=wd, h=CHIP_H, r=CHIP_R, px=CHIP_PX, pad=CHIP_PAD, pt=round((CHIP_H - CHIP_PX * 1.4) / 2))


def stat(s, cx, y):
    return dict(s=s, x=round(cx - H.text_w(s, STAT_PX) / 2), y=y, px=STAT_PX)


def cite(s, cx, y):
    return dict(s=s, x=round(cx - H.text_w(s, CITE_PX, False) / 2), y=y, px=CITE_PX)


def year(s, x, y):
    px_, h, pad = 30, 50, 18
    return dict(s=s, x=x, y=y, w=round(H.text_w(s, px_) + 2 * pad), h=h, r=14, px=px_, pad=pad, pt=round((h - px_ * 1.4) / 2))


def under(shot, name, credits, y_bottom):
    """name chip, weight + medication, credit, centred under the photos"""
    y = y_bottom + 22
    shot["chip"] = chip(name, 960, y); y += CHIP_H + 6
    shot["stat"] = stat(STAT[name], 960, y); y += round(STAT_PX * 1.4) + 4
    cr = list(dict.fromkeys(credits))
    shot["cite"] = cite(("Photo: " if len(cr) == 1 else "Photos: ") + ", ".join(cr), 960, y)
    for s in (shot["chip"]["s"], shot["stat"]["s"], shot["cite"]["s"]): assert "—" not in s and s.strip() == s


def single(sid, stem, name, aspect=2 / 3, k=6.5, ph=760, push=1.06, top=0.55):
    box = crop(stem, aspect, k, top); a = (box[2] - box[0]) / (box[3] - box[1])
    pw = round(ph * a)
    if pw > 1400: pw = 1400; ph = round(pw / a)
    y = round((1080 - (ph + BELOW)) / 2); x = round((1920 - pw) / 2)
    src = asset(stem, box, pw, ph, HERE / "photo_assets" / f"{sid}.jpg")
    fx0, fy0, fx1, fy1 = facebox(stem); oy = ((fy0 + fy1) / 2 - box[1]) / (box[3] - box[1]); ox = ((fx0 + fx1) / 2 - box[0]) / (box[2] - box[0])
    shot = dict(photos=[dict(src=f"assets/{sid}.jpg", x=x, y=y, w=pw, h=ph, push=push, origin=f"{ox * 100:.0f}% {oy * 100:.0f}%")])
    under(shot, name, [credit(stem)], y + ph)
    return shot, [(src, f"{sid}.jpg")], dict(stem=[stem], crop=[box], name=name, stat=STAT[name])


def pair(sid, stems, years, name, aspect, k, ph=700, gap=64, push=1.05, top=0.55, x_bias=(0.0, 0.0)):
    """then / now: two photos the same size, the face the same size in both; year chips in the frames"""
    boxes = [crop(s, aspect, k, top, xb) for s, xb in zip(stems, x_bias)]
    pw = round(ph * aspect); x0 = round((1920 - (2 * pw + gap)) / 2)
    y = round((1080 - (ph + BELOW)) / 2)
    photos, assets = [], []
    for i, (s, bx, yr) in enumerate(zip(stems, boxes, years)):
        pid = f"{sid}_{i}"; x = x0 + i * (pw + gap)
        assets.append((asset(s, bx, pw, ph, HERE / "photo_assets" / f"{pid}.jpg"), f"{pid}.jpg"))
        fx0, fy0, fx1, fy1 = facebox(s); oy = ((fy0 + fy1) / 2 - bx[1]) / (bx[3] - bx[1]); ox = ((fx0 + fx1) / 2 - bx[0]) / (bx[2] - bx[0])
        photos.append(dict(src=f"assets/{pid}.jpg", x=x, y=y, w=pw, h=ph, push=push, origin=f"{ox * 100:.0f}% {oy * 100:.0f}%",
                           year=year(yr, x + 18, y + ph - 50 - 18)))
    shot = dict(photos=photos)
    under(shot, name, [credit(s) for s in stems], y + ph)
    return shot, assets, dict(stem=list(stems), crop=boxes, name=name, years=list(years), stat=STAT[name])


def w(phrase, lo):
    return round(W.at(phrase, lo - 1.0, lo + 6.0, phrase), 3)


def scenes():
    """round 4: P4-P7 rebuilt as pairs with Dan's approved stat line (round 2 showed one recent photo each). P0-P3 are round 3's."""
    S = []
    S.append(dict(id="P4", name="Amy Schumer, before and after", t0=round(6739 / FPS + 0.0005, 4), t1=round(6809 / FPS + 0.0005, 4),
                  shots=[dict(t=0.0, enter="rise", layout="pair", args=dict(stems=("amy_before_2024_variety-power-of-women", "amy_after_2026_lorne-premiere"),
                                                                           years=("2024", "2026"), name="Amy Schumer", aspect=2 / 3, k=6.5))],
                  why="in on the cut before 'Next up is Amy Schumer'; her 2024 / 2026 pair (P0 showed 2023 / 2025) with 50 lb, Mounjaro; out where her Howard Stern clip starts"))
    S.append(dict(id="P5", name="Meghan Trainor, before and after", t0=round(8792 / FPS + 0.0005, 4), t1=round(8854 / FPS + 0.0005, 4),
                  shots=[dict(t=0.0, enter="rise", layout="pair", args=dict(stems=("meghan_before_2019_star-wars-premiere-london", "meghan_recent_slim_2025_the_paper_premiere"),
                                                                           years=("2019", "2025"), name="Meghan Trainor", aspect=2 / 3, k=6.5))],
                  why="in on the cut before 'Now here's someone who got it right' (round 3 had it 0.9 s, after the clip insert moved its start); "
                      "her 2019 / 2025 pair (P0 showed 2020 / 2025, her panel keeps 2020 / 2025 Baby2Baby) with 60 lb, Mounjaro; out where her ET clip starts"))
    S.append(dict(id="P6", name="Oprah Winfrey, before and after", t0=round(10933 / FPS + 0.0005, 4), t1=round(11090 / FPS + 0.0005, 4),
                  shots=[dict(t=0.0, enter="rise", layout="pair", args=dict(stems=("oprah_before_2022_tiff-sidney-premiere", "oprah_recent_2025_abt_gala"),
                                                                           years=("2022", "2025"), name="Oprah Winfrey", aspect=2 / 3, k=6.5))],
                  why="in on the cut before 'Alright, so this last group is the most important one'; her 2022 / 2025 pair (P0 showed one 2024 photo) "
                      "with Down to 155 lb, GLP-1; out where her clip starts"))
    S.append(dict(id="P7", name="Tracy Morgan", t0=round(12133 / FPS + 0.0005, 4), t1=round(12256 / FPS + 0.0005, 4),
                  shots=[dict(t=0.0, enter="rise", layout="single", args=dict(stem="tracy_recent_2026_tribeca_closeup", name="Tracy Morgan", k=6.5))],
                  why="straight out of his Tonight Show clip (round 3 left a 0.7 s flash of Dan between them) under 'And Tracy Morgan said it on "
                      "The Tonight Show, I out ate Ozempic'; one recent photo (he gained weight, so no pair) with On Ozempic, gained 40 lb; out on the cut before 'I've gained 40 pounds'"))
    return S


def build_scene(sc):
    a, b = sc["t0"], sc["t1"]
    shots, assets, used = [], [], []
    for k, s in enumerate(sc["shots"]):
        sid = f"{sc['id']}_{k}"
        fn = single if s["layout"] == "single" else pair
        shot, ass, u = fn(sid, **s["args"])
        shot.update(t=round(s["t"] - a if s["t"] >= a else s["t"], 3), enter=s["enter"])
        shots.append(shot); assets += ass; used.append(dict(u, t=round(a + shot["t"], 3)))
    shots[0]["t"] = 0.0
    return dict(id=sc["id"], dur=round(b - a, 3), drift=-6, shots=shots), assets, used


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--render", action="store_true")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--snap", action="store_true")
    A = ap.parse_args(); only = set(A.only.split(",")) if A.only else None
    for d in ("photo_assets", "configs", "renders", "stills/raw"): (HERE / d).mkdir(parents=True, exist_ok=True)
    man_p = HERE / "photos_manifest.json"; man = {m["id"]: m for m in json.load(open(man_p))} if man_p.exists() else {}
    plan_p = HERE / "plan_photos_r4.json"; plan = {m["id"]: m for m in json.load(open(plan_p))} if plan_p.exists() else {}
    for sc in scenes():
        if only and sc["id"] not in only: continue
        cfg, assets, used = build_scene(sc)
        (HERE / "configs" / f"{sc['id']}.json").write_text(json.dumps([cfg], indent=1))
        d = H.make_scene(TPL, cfg, HERE / "projects", assets); H.lint_check(d)
        sha = hashlib.sha256((json.dumps(cfg, sort_keys=True) + TPL.read_text() + "".join(pathlib.Path(s).read_bytes().hex()[:4096] for s, _ in assets)).encode()).hexdigest()[:16]
        mov = HERE / "renders" / f"{sc['id']}.mov"; stamp = HERE / "renders" / f"{sc['id']}.cfg.sha"
        if A.snap:
            ts = [round(min(cfg["dur"] - 0.05, (s["t"] + (cfg["shots"][i + 1]["t"] if i + 1 < len(cfg["shots"]) else cfg["dur"])) / 2 + 0.25), 2) for i, s in enumerate(cfg["shots"])]
            for o in (d / "snapshots").glob("*.png"):
                try: o.unlink()
                except FileNotFoundError: pass
            shots = sorted(x for x in H.snapshot(d, ts) if not x.name.startswith("._"))
            for i, x in enumerate(shots[:len(ts)]): Image.open(x).save(HERE / "stills/raw" / f"{sc['id']}-{i}.png")
        if A.render:
            if not A.force and stamp.exists() and stamp.read_text() == sha and mov.exists():
                print(sc["id"], "unchanged, render kept", flush=True)
            else:
                if mov.exists(): mov.unlink()
                H.render(d, mov); stamp.write_text(sha)
        man[sc["id"]] = dict(id=sc["id"], template="local:photo-scene", a=sc["t0"], b=sc["t1"], mov=str(mov), kind="opaque")
        plan[sc["id"]] = dict(id=sc["id"], name=sc["name"], kind="photo", t0=sc["t0"], t1=sc["t1"], shots=used, why=sc["why"])
        print(f"{sc['id']:4s} {sc['t0']:8.3f} - {sc['t1']:8.3f}  {len(cfg['shots'])} shot(s)", flush=True)
    json.dump(sorted(man.values(), key=lambda m: m["a"]), open(man_p, "w"), indent=1)
    json.dump(sorted(plan.values(), key=lambda m: m["t0"]), open(plan_p, "w"), indent=1)


if __name__ == "__main__":
    main()
