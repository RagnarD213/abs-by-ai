#!/usr/bin/env python3
"""RO-21 "What Every Body Fat Percentage Looks Like (On Me)" round 1: full-screen B-roll inserts.

Rebuilds every /Volumes/Expansion/_edit_work/RO-21/broll/<ID>.mp4 from round1/plan_r1.json (item film in/out a, b)
and round1/film_words.json (cut words). Re-run after film times shift: the frame counts and cut frames follow.

  python3 broll_r1.py                  build every item (encodes go through the render queue wrapper)
  python3 broll_r1.py B03 B07          build only these
  python3 broll_r1.py --measure [IDs]  before/after stats per piece (median luma, black share, median saturation)
  python3 broll_r1.py --stills [IDs]   before/after still pairs per piece into broll/_stills/
  python3 broll_r1.py --sheet          SHEET.jpg: one row per item, middle frame of each piece, labelled
  python3 broll_r1.py --check          frame count / fps / size / tags of every built file

Output: 1920x1080, 30000/1001, exactly round((b-a)*30000/1001) frames, libx264 CRF 14 high, yuv420p, bt709 tags, no audio.
Every non-Color-C source is decoded as BT.709 TV range into RGB (format=gbrp) and graded there (RO-28 lesson 24).
"""
import json, os, subprocess, sys, math
from fractions import Fraction

W = "/Volumes/Expansion/_edit_work/RO-21"
PROJ = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
FF = f"{PROJ}/Media/video_edit/bin/ffmpeg"            # render-queue wrapper (full encodes)
FFR = f"{PROJ}/Media/video_edit/bin/ffmpeg.real"      # few-frame grabs only
FP = f"{PROJ}/Media/video_edit/bin/ffprobe"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage"
DAN = f"{LIB}/dan-filmed"
ST = f"{W}/stock"
R1015 = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop"
OUT = f"{W}/broll"
FPS = Fraction(30000, 1001)

def lib(cid):
    import glob
    h = sorted(glob.glob(f"{LIB}/*/{cid}_*") + glob.glob(f"{LIB}/*/*/{cid}_*"))
    assert h, cid
    return h[0]

# ---------------------------------------------------------------- grades (RGB, after BT.709 decode)
# Each grade: colorlevels (black point / per-channel white balance), master curve, temperature, saturation.
def grade(lo=0.0, hi=(1.0, 1.0, 1.0), curve=None, temp=None, sat=0.0, vib=0.0):
    f = []
    r, g, b = hi
    if lo or hi != (1.0, 1.0, 1.0):
        f.append(f"colorlevels=rimin={lo}:gimin={lo}:bimin={lo}:rimax={r}:gimax={g}:bimax={b}")
    if curve:
        f.append(f"curves=master='{curve}'")
    if temp:
        f.append(f"colortemperature=temperature={temp}:pl=1")
    if sat:   # linear saturation about BT.709 luma (huesaturation measured as a no-op on gbrp here)
        k = 1.0 + sat; wr, wg, wb = 0.2126 * (1 - k), 0.7152 * (1 - k), 0.0722 * (1 - k)
        f.append(f"colorchannelmixer=rr={wr+k:.4f}:rg={wg:.4f}:rb={wb:.4f}:gr={wr:.4f}:gg={wg+k:.4f}:gb={wb:.4f}:"
                 f"br={wr:.4f}:bg={wg:.4f}:bb={wb+k:.4f}")
    if vib:
        f.append(f"vibrance=intensity={vib}")
    return ",".join(f)

COLOR_C = None   # Oct 23 gym masters: finalized Color C, used exactly as they are
GRADES = {
    "COLOR_C": COLOR_C,
    # Dan's pool B-roll (graded to RO-28's approved pool range: real contrast and colour, never a gamma lift alone)
    "POOL_SHADE_0708": grade(lo=0.02, hi=(0.95, 0.98, 1.0), curve="0/0 0.25/0.25 0.5/0.56 0.75/0.81 1/1", sat=0.10),
    "POOL_SUN_0708":   grade(lo=0.06, curve="0/0 0.5/0.47 1/1", sat=0.12),
    "POOL_1015":       grade(lo=0.04, curve="0/0 0.25/0.23 0.75/0.77 1/1", sat=0.05),
    "POOL_0828":       grade(lo=0.015, curve="0/0 0.25/0.235 0.75/0.78 1/1", sat=0.05),
    "POOL_1015_KB":    grade(curve="0/0 0.1/0.09 0.3/0.36 0.6/0.68 1/1", sat=0.05),
    # stock: light per-clip corrections toward neutral whites, healthy contrast, natural colour
    "STOCK_SCALE":     grade(curve="0/0 0.25/0.23 0.75/0.77 1/1"),
    "STOCK_COLA":      grade(curve="0/0 0.1/0.1 0.5/0.55 1/1"),
    "STOCK_OJ":        grade(curve="0/0 0.25/0.24 0.75/0.77 1/1"),
    "STOCK_FRAPPE":    grade(temp=6000, curve="0/0 0.25/0.23 0.75/0.77 1/1"),
    "STOCK_MILK":      grade(curve="0/0 0.5/0.47 1/0.98", sat=0.15),
    "STOCK_COCONUT":   grade(lo=0.03, curve="0/0 0.5/0.48 1/1", sat=0.15),
    "STOCK_STEAK":     grade(lo=0.03, curve="0/0 0.25/0.22 0.75/0.78 1/1", sat=0.15),
    "STOCK_SALMON":    grade(curve="0/0 0.25/0.24 0.5/0.53 0.75/0.78 1/1", sat=0.10),
    "STOCK_CHIPS":     grade(curve="0/0 0.25/0.30 0.5/0.58 0.75/0.82 1/1", sat=0.05),
    "STOCK_SARDINES":  grade(lo=0.03, curve="0/0 0.5/0.46 1/0.98", sat=0.15),
    "STOCK_EGG":       grade(lo=0.03, curve="0/0 0.25/0.23 0.75/0.78 1/1", sat=0.15),
    "STOCK_COCKTAILS": grade(curve="0/0 0.25/0.25 0.5/0.53 1/1"),
    "STOCK_MEALPREP":  grade(curve="0/0 0.25/0.24 0.75/0.77 1/1"),
    "STOCK_SLEEP":     grade(temp=8000, curve="0/0 0.5/0.5 1/1", sat=-0.10),
}

# ---------------------------------------------------------------- the table
# piece: (label, cut word or None for the item start, lead seconds (cut earlier by), source, source in, crop w:h:x:y or None, grade key)
ITEMS = {
 "B01": [("scale",       None,      0,    lib("B0502"),                     0.40, None,                  "STOCK_SCALE")],
 "B02": [("squats",      None,      0,    lib("B0460"),                     0.00, "1664:936:70:40",    "POOL_SHADE_0708"),
         ("push-ups",    "push",    0.26, lib("B0461"),                     1.25, None,                  "POOL_SUN_0708"),
         ("plank",       "planks",  0,    f"{R1015}/C1752.MP4",             6.00, "2560:1440:300:640",   "POOL_1015")],
 "B03": [("soda",        None,      0,    f"{ST}/1_cola-pour-ice_px8518236.mp4",      1.00, None, "STOCK_COLA"),
         ("juice",       "juice",   0.14, f"{ST}/1_oj-pour_px6739355.mp4",            2.00, None, "STOCK_OJ"),
         ("sweet coffee","sweet",   0,    f"{ST}/1_frappe-whipped-pool_px12646080.mp4", 10.0, None, "STOCK_FRAPPE"),
         ("milk",        "milk",    0,    f"{ST}/1_milk-bottle-pour_px855303.mp4",    4.00, None, "STOCK_MILK"),
         ("coconut water","coconut",0,    f"{ST}/1_coconut-straw_px17194540.mp4",     5.00, None, "STOCK_COCONUT")],
 "B05": [("KB deadlift front", None, 0,   lib("B0431"),                     1.00, None,                  "POOL_0828"),
         ("KB deadlift side",  "They", 0, f"{R1015}/C1743.MP4",             4.67, "3200:1800:0:200",   "POOL_1015_KB"),
         ("KB deadlift front 2", "You", 0, lib("B0431"),                    3.75, None,                  "POOL_0828")],
 "B06": [("steak and eggs", None,   0,    f"{ST}/3_steak-eggs-plate_px40047451.mp4",  2.00, None, "STOCK_STEAK")],   # salmon dropped 2026-10-29: at review size it read as a pizza
 "B07": [("cardio bike", None,      0,    lib("B0566"),                     4.00, None, "COLOR_C"),
         ("leg press",   "leg",     0,    lib("B0621"),                     4.00, None, "COLOR_C"),
         ("incline DB press", "upper", 0, lib("B0697"),                     4.00, "3200:1800:0:180", "COLOR_C"),
         ("decline med-ball sit-up", "ab", 0, lib("B0616"),                 4.33, None, "COLOR_C")],
 "B08": [("chips",       None,      0,    f"{ST}/4_chips-bowl-hands_px4710996.mp4",   0.00, "2780:1564:80:0", "STOCK_CHIPS"),
         ("sardines",    "Sardines",0,    f"{ST}/4_sardines-tin_px6398604.mp4",       4.50, None, "STOCK_SARDINES"),
         ("peeled egg",  "packed",  0,    f"{ST}/4_peeled-egg_px6288311.mp4",         6.00, None, "STOCK_EGG")],
 "B09": [("cocktails",   None,      0,    f"{ST}/5_cocktails-bar_px8942658.mp4",      0.00, None, "STOCK_COCKTAILS"),
         ("meal prep",   "meal",    0,    f"{ST}/5_mealprep-containers_px6894099.mp4", 2.00, None, "STOCK_MEALPREP")],
 "B10": [("man sleeping", None,     0,    f"{ST}/6_man-sleeping-warm_px19919759.mp4", 4.00, None, "STOCK_SLEEP")],
 "B11": [("cable crunch", None,     0,    lib("B0574"),                     1.50, None, "COLOR_C"),
         ("leg raise",   "leg",     0,    lib("B0584"),                     1.00, None, "COLOR_C")],
}

def load_plan():
    plan = {it["id"]: it for it in json.load(open(f"{W}/round1/plan_r1.json"))}
    words = json.load(open(f"{W}/round1/film_words.json"))
    return plan, words

def norm(w): return "".join(ch for ch in w.lower() if ch.isalnum())

def word_time(words, a, b, key):
    for x in words:
        if a - 0.01 <= x["t0"] < b and norm(x["w"]) == norm(key):   # exact word ("you" must not match "your")
            return x["t0"]
    raise SystemExit(f"cut word {key!r} not found in {a}-{b}")

def layout(iid):
    """-> (a, b, total frames, [(piece, start_frame, n_frames)])"""
    plan, words = load_plan()
    it = plan[iid]; a, b = it["a"], it["b"]
    N = round((b - a) * FPS)
    starts = []
    for p in ITEMS[iid]:
        lab, key, lead = p[0], p[1], p[2]
        starts.append(0 if key is None else round((word_time(words, a, b, key) - lead - a) * FPS))
    out = []
    for i, p in enumerate(ITEMS[iid]):
        s = starts[i]; e = starts[i + 1] if i + 1 < len(starts) else N
        assert e > s, (iid, p[0])
        out.append((p, s, e - s))
    return a, b, N, out

def chain(p, gkey, raw=False):
    """filter chain for one piece, ending in RGB gbrp (graded unless raw)."""
    _, _, _, src, sin, crop, _ = p
    c = f"crop={crop}," if crop else ""
    vf = (f"{c}scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos:in_color_matrix=bt709:in_range=tv,"
          f"crop=1920:1080,format=gbrp")
    g = GRADES.get(gkey)
    if g and not raw:
        vf += "," + g
    return vf

def build(iid):
    a, b, N, pieces = layout(iid)
    args = [FF, "-y", "-v", "error"]
    fc = []
    for k, (p, s, n) in enumerate(pieces):
        dur = n / FPS + 0.5
        args += ["-ss", f"{p[4]:.3f}", "-t", f"{float(dur):.3f}", "-i", p[3]]
        fc.append(f"[{k}:v]{chain(p, p[6])},fps=30000/1001,trim=end_frame={n},setpts=PTS-STARTPTS[v{k}]")
    cat = "".join(f"[v{k}]" for k in range(len(pieces)))
    fc.append(f"{cat}concat=n={len(pieces)}:v=1:a=0,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,"
              f"setsar=1,trim=end_frame={N}[out]")
    out = f"{OUT}/{iid}.mp4"
    args += ["-filter_complex", ";".join(fc), "-map", "[out]", "-an", "-r", "30000/1001", "-frames:v", str(N),
             "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
             "-movflags", "+faststart", out]
    subprocess.run(args, check=True)
    return out

# ---------------------------------------------------------------- measurement / stills / sheet
def grab(p, t, gkey, raw=False, w=480, h=270):
    vf = chain(p, gkey, raw) + f",scale={w}:{h}:flags=area"
    for _ in range(3):
        r = subprocess.run([FFR, "-v", "error", "-ss", f"{t:.3f}", "-i", p[3], "-frames:v", "1", "-vf", vf,
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        if len(r.stdout) == w * h * 3:
            return r.stdout
    raise RuntimeError(f"grab failed {p[3]} @{t}: {r.stderr[-300:]}")

def stats_rgb(buf_list, w, h):
    import numpy as np
    arr = np.concatenate([np.frombuffer(b, np.uint8).reshape(h * w, 3) for b in buf_list]).astype(np.float32)
    R, G, B = arr[:, 0], arr[:, 1], arr[:, 2]
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    mx, mn = arr.max(1), arr.min(1)
    S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    return dict(med=float(np.median(Y)), black=float((Y < 16).mean()), sat=float(np.median(S)),
                rgb=tuple(round(float(v), 1) for v in arr.mean(0)))

def measure_piece(p, n, raw):
    ts = [p[4] + (n / FPS) * f for f in (0.1, 0.3, 0.5, 0.7, 0.9)]
    return stats_rgb([grab(p, float(t), p[6], raw) for t in ts], 480, 270)

def fmt(s): return f"med {s['med']:.0f} black {s['black']*100:.1f}% sat {s['sat']:.2f} rgb {s['rgb']}"

def measure(ids):
    res = {}
    for iid in ids:
        a, b, N, pieces = layout(iid)
        for p, s, n in pieces:
            before = measure_piece(p, n, True); after = measure_piece(p, n, False)
            res[f"{iid}/{p[0]}"] = dict(before=before, after=after, grade=p[6])
            print(f"{iid} {p[0]:<24} {p[6]:<16} BEFORE {fmt(before)}\n{'':>44} AFTER  {fmt(after)}")
    json.dump(res, open(f"{OUT}/_measure.json", "w"), indent=1)

def stills(ids):
    from PIL import Image
    os.makedirs(f"{OUT}/_stills", exist_ok=True)
    for iid in ids:
        a, b, N, pieces = layout(iid)
        for p, s, n in pieces:
            t = float(p[4] + (n / FPS) / 2)
            im0 = Image.frombytes("RGB", (960, 540), grab(p, t, p[6], True, 960, 540))
            im1 = Image.frombytes("RGB", (960, 540), grab(p, t, p[6], False, 960, 540))
            o = Image.new("RGB", (1920, 540)); o.paste(im0, (0, 0)); o.paste(im1, (960, 0))
            o.save(f"{OUT}/_stills/{iid}_{p[0].replace(' ', '-')}.jpg", quality=85)

def sheet():
    from PIL import Image, ImageDraw, ImageFont
    ids = list(ITEMS)
    TW, TH, LW = 480, 270, 150
    maxp = max(len(v) for v in ITEMS.values())
    o = Image.new("RGB", (LW + maxp * TW, len(ids) * (TH + 24)), (24, 24, 24))
    d = ImageDraw.Draw(o)
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17); big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    except Exception: font = big = None
    for r, iid in enumerate(ids):
        a, b, N, pieces = layout(iid)
        y = r * (TH + 24)
        d.text((10, y + 10), iid, fill="yellow", font=big)
        d.text((10, y + 50), f"{a:.2f}-{b:.2f}", fill="white", font=font)
        d.text((10, y + 72), f"{N} fr", fill="white", font=font)
        f = f"{OUT}/{iid}.mp4"
        for k, (p, s, n) in enumerate(pieces):
            mid = (s + n // 2) / FPS
            buf = subprocess.run([FFR, "-v", "error", "-ss", f"{float(mid):.4f}", "-i", f, "-frames:v", "1",
                                  "-vf", f"scale={TW}:{TH}:in_color_matrix=bt709:in_range=tv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                 capture_output=True, check=True).stdout
            im = Image.frombytes("RGB", (TW, TH), buf)
            x = LW + k * TW
            o.paste(im, (x, y))
            bn = os.path.basename(p[3]); src = bn.split("_")[0] if "/dan-filmed/" in p[3] or "/stock/lifestyle" in p[3] else (bn.rsplit("_", 1)[-1][:-4] if "_px" in bn else bn)
            d.text((x + 4, y + TH + 2), f"{k+1}. {p[0]} | {src} @{p[4]:.2f} | {n/float(FPS):.2f}s", fill="white", font=font)
    o.save(f"{OUT}/SHEET.jpg", quality=85)
    print(f"{OUT}/SHEET.jpg", o.size)

def check():
    for iid in ITEMS:
        a, b, N, _ = layout(iid)
        f = f"{OUT}/{iid}.mp4"
        r = subprocess.run([FP, "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,r_frame_rate,nb_read_frames,pix_fmt,color_space,color_transfer,color_primaries,color_range,profile",
                            "-of", "json", f], capture_output=True, text=True)
        s = json.loads(r.stdout)["streams"][0]
        aud = subprocess.run([FP, "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
        ok = int(s["nb_read_frames"]) == N and s["width"] == 1920 and s["height"] == 1080 and s["r_frame_rate"] == "30000/1001" and not aud
        print(iid, "OK " if ok else "BAD", N, s, "audio" if aud else "")

if __name__ == "__main__":
    a = sys.argv[1:]
    ids = [x for x in a if not x.startswith("--")] or list(ITEMS)
    if "--measure" in a: measure(ids)
    elif "--stills" in a: stills(ids)
    elif "--sheet" in a: sheet()
    elif "--check" in a: check()
    else:
        for iid in ids:
            print("build", iid, build(iid), flush=True)
