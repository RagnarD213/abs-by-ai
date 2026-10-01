#!/usr/bin/env python3
"""RO-12 builder. Locked 9/23 look (WV-01): W2 3552:1998:144:162 / T2 2608:1466:616:184 on the 4K source, grade-C.cube (BT.709,
tetrahedral), audio B = voice_chain with WV-01's fitted EQ + bass=g=0.9 at 150 Hz, no dereverb. Soft Blue Light graphics.
Structure borrowed from RO-05 round 4 (Dan approved 2026-09-29): title_scene, bloom flash, bed loop, chunked 2-worker picture.

usage: build.py timeline            -> out/timeline.json (+ prints shots, joins, coverage)
       build.py stills [IDS...]     -> check/stills/<ID>.jpg (every graphic on its real frame)
       build.py picture [--from S --to S --name N]   -> out/PICTURE.mp4 (or a window, for the first-minute check)
       build.py audio               -> out/voice_raw.wav, out/bed.wav, out/RO12.mp4 (voice chain muxed on PICTURE)"""
import sys, os, json, subprocess, math, hashlib
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{ROOT}/.claude/skills/_shared")
import softblue as S
import edl, plan
W = "/Volumes/Extreme/_edit_work/ro12"; OD = f"{W}/out"
FF = f"{ROOT}/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001; FPSS = "30000/1001"; SR = 48000
LUT = "/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube"
CROP = {"W": "3552:1998:144:162", "T": "2608:1466:616:184"}
LAV = f"{W}/audio/lav.wav"
def fr(t): return int(round(t*FPS))
def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode: print("FAIL", " ".join(map(str, cmd))[:400]); print(r.stderr.decode()[-1500:]); sys.exit(1)
    return r

# ================================================================== timeline
def blocks():
    """Merge source-contiguous pieces (gap < 1 s, a natural pause) into blocks; each block length is frame-quantised so picture
    and audio share exact boundaries. Consecutive blocks are cuts."""
    P = edl.pieces(); B = []
    for p in P:
        if B and 0 <= p["in"] - B[-1]["out"] < 1.0: B[-1]["out"] = p["out"]; continue
        B.append(dict(p))
    f = 0
    for b in B:
        n = int(round((b["out"] - b["in"])*FPS)); b["out"] = b["in"] + n/FPS; b["f0"] = f; b["f1"] = f + n; f += n
    return B

def s2o(B, t, side="in"):
    """source seconds -> output seconds (a time in a dropped gap snaps to the next kept block's start)."""
    for b in B:
        if b["in"] - 1e-6 <= t <= b["out"] + 1e-6: return b["f0"]/FPS + (t - b["in"])
    nxt = [b for b in B if b["in"] > t]
    if not nxt: return B[-1]["f1"]/FPS
    return nxt[0]["f0"]/FPS

SIDE = ("l3", "phone")        # side layouts: Dan shifted right for the whole shot, entering and leaving on cuts
def resolve(B):
    items = []
    for it in plan.ITEMS:
        it = dict(it); it["o0"] = s2o(B, it["t0"]); it["o1"] = s2o(B, it["t1"])
        for k in ("item_t", ):
            if k in it: it["o_items"] = [s2o(B, x) for x in it[k]]
        if it["kind"] == "beforenow": it["o_now"] = s2o(B, it["t_now"])
        if it["kind"] == "ramp": it["o_steps"] = [(lab, s2o(B, x)) for lab, x in it["steps"]]
        if it["kind"] == "recap": it["o_items"] = [s2o(B, x) for _, x in it["items"]]
        it["f0"], it["f1"] = fr(it["o0"]), fr(it["o1"])
        items.append(it)
    # review r1 B1/B2/S6: a sliver (< 0.5 s) of presenter between two covering pieces flashes on screen -> the earlier piece
    # runs to the next one (full-frame or side layout); a sliver before a block cut is closed the same way.
    cov = sorted([i for i in items if i["kind"] in FULL + SIDE], key=lambda i: i["f0"])
    for x, y in zip(cov, cov[1:]):
        if 0 < y["f0"] - x["f1"] < 20: x["f1"] = y["f0"]; x["o1"] = x["f1"]/FPS
    cuts = [b["f0"] for b in B[1:]]
    for x in cov:
        nxt = [c for c in cuts if 0 < c - x["f1"] < 20]
        if nxt and x["kind"] in FULL: x["f1"] = nxt[0]; x["o1"] = x["f1"]/FPS
    return items

FULL = ("insert", "title", "beforenow", "ramp", "week", "recap", "photo")
def word_starts(a, b):
    import words
    return [w["s"] for i, w in enumerate(words.WORDS) if a + 0.5 < w["s"] < b - 0.5 and i and w["s"] - words.WORDS[i-1]["e"] >= 0.25]

def shots(B, items):
    """Presenter shots: split every block at sentence starts into 6.5-13 s shots; framing alternates W/T at every split.
    A side layout (3A card, phone) is its own W shot: boundaries sit exactly on its first and last frame, so Dan's fixed
    shift starts and ends on a cut (review r1 S7), never mid-shot."""
    side = sorted([i for i in items if i["kind"] in SIDE], key=lambda i: i["f0"])
    out = []
    for b in B:
        cands = [t for t in word_starts(b["in"], b["out"])]
        cuts = [b["in"]]; last = b["in"]
        while True:
            ok = [t for t in cands if last + 6.5 <= t <= last + 13.0 and t < b["out"] - 3.0]
            if not ok:
                later = [t for t in cands if t > last + 13.0 and t < b["out"] - 3.0]
                if later: ok = [later[0]]
                else: break
            last = ok[0] if len(ok) == 1 else min(ok, key=lambda t: abs(t - (last + 9.0))); cuts.append(last)
        fb = [b["f0"] + int(round((c - b["in"])*FPS)) for c in cuts] + [b["f1"]]
        # side windows inside this block: drop boundaries inside them (and within 12 frames of their edges), add their edges
        for it in side:
            if it["f1"] <= b["f0"] or it["f0"] >= b["f1"]: continue
            fb = [f for f in fb if not (it["f0"] - 12 < f < it["f1"] + 12) or f in (b["f0"], b["f1"])]
            fb += [f for f in (it["f0"], it["f1"]) if b["f0"] + 12 < f < b["f1"] - 12]
        fb = sorted(set(fb))
        for f0, f1 in zip(fb, fb[1:]):
            out.append(dict(f0=f0, f1=f1, block=B.index(b), **{"in": b["in"] + (f0 - b["f0"])/FPS, "out": b["in"] + (f1 - b["f0"])/FPS}))
    # review r1: no presenter sliver (< 15 frames) beside a full-frame piece. A split moves onto the piece's edge; at a block cut
    # (source discontinuity, cannot move) the piece is stretched to the cut instead.
    blk = set(b["f0"] for b in B)
    full_its = [i for i in items if i["kind"] in FULL]
    for i in range(1, len(out)):
        f = out[i]["f0"]
        for it in full_its:
            if 0 < it["f0"] - f < 20 or 0 < f - it["f1"] < 20:
                if f in blk:
                    if 0 < it["f0"] - f < 20: it["f0"] = f; it["o0"] = f/FPS
                    else: it["f1"] = f; it["o1"] = f/FPS
                else:
                    g = it["f0"] if 0 < it["f0"] - f < 20 else it["f1"]
                    if out[i-1]["f0"] + 15 < g < out[i]["f1"] - 15: out[i-1]["f1"] = out[i]["f0"] = g
    for sh in out:
        b = B[sh["block"]]; sh["in"] = b["in"] + (sh["f0"] - b["f0"])/FPS; sh["out"] = b["in"] + (sh["f1"] - b["f0"])/FPS
    for sh in out:
        sh["forced"] = any(it["f0"] <= sh["f0"] + 12 and sh["f1"] - 12 <= it["f1"] for it in side)
    # framing: forced shots are W; each run of free shots between them alternates starting and ending on T (so both
    # neighbouring cuts change framing). A run with the wrong parity gets its longest shot split at a sentence start.
    def runs():
        r, cur = [], []
        for i, sh in enumerate(out):
            if sh["forced"]:
                if cur: r.append(cur); cur = []
            else: cur.append(i)
        if cur: r.append(cur)
        return r
    for _ in range(20):
        changed = False
        for run in runs():
            before = run[0] > 0 and out[run[0]-1]["forced"]; after = run[-1] + 1 < len(out) and out[run[-1]+1]["forced"]
            if before and after and len(run) % 2 == 0:
                k = max(run, key=lambda i: out[i]["f1"] - out[i]["f0"]); sh = out[k]; b = B[sh["block"]]
                ws = [w for w in word_starts(sh["in"], sh["out"]) if sh["in"] + 2.5 < w < sh["out"] - 2.5]
                if not ws: raise SystemExit(f"cannot fix framing parity near {sh['f0']/FPS:.2f}")
                mid = (sh["in"] + sh["out"])/2; w = min(ws, key=lambda x: abs(x - mid)); f = b["f0"] + int(round((w - b["in"])*FPS))
                new = dict(sh); new["f0"] = f; sh["f1"] = f
                for x in (sh, new): x["in"] = b["in"] + (x["f0"] - b["f0"])/FPS; x["out"] = b["in"] + (x["f1"] - b["f0"])/FPS
                out.insert(k + 1, new); changed = True; break
        if not changed: break
    for run in runs():
        after = run[-1] + 1 < len(out) and out[run[-1]+1]["forced"]
        before = run[0] > 0 and out[run[0]-1]["forced"]
        if before: seq = ["T", "W"]
        elif after: seq = ["T", "W"] if len(run) % 2 == 1 else ["W", "T"]
        else: seq = ["W", "T"]
        for j, i in enumerate(run): out[i]["fr"] = seq[j % 2]
    for sh in out:
        if sh["forced"]: sh["fr"] = "W"
    bad = [out[i]["f0"] for i in range(1, len(out)) if out[i]["fr"] == out[i-1]["fr"]]
    if bad: raise SystemExit(f"same framing across a cut: {bad}")
    return out

def timeline():
    B = blocks(); items = resolve(B); SH = shots(B, items)
    total = B[-1]["f1"]
    json.dump(dict(blocks=B, items=items, shots=SH, total_frames=total), open(f"{OD}/timeline.json", "w"), indent=1)
    return B, items, SH, total

# ================================================================== graphics
def title_scene(t, eyebrow, headline, w=1920, h=1080):
    """RO-05 round 3/4 section title (approved 2026-09-29): cyan eyebrow, slim cyan accent, headline lines rise staggered 0.2 s."""
    im = S.field(t, w, h); u = S.unit(w, h)
    lines = headline.split("\n"); size = 60
    while size > 40 and max(S.text_w(l, S.font(size*u)) for l in lines) > w - 150*u - 100*u: size -= 2
    lh = 80*u*size/60
    y0 = (h - (40*u + len(lines)*lh))/2; x = 150*u
    S.rr(im, (x - 36*u, y0 + 6*u, x - 28*u, y0 + 40*u + len(lines)*lh - 10*u), S.CYAN, 4*u)
    if t > 0.1: S.text(im, (x, y0), eyebrow, 20*u, S.CYAN)
    for i, ln in enumerate(lines):
        q = S.ease(t - 0.25 - i*0.2)
        if q > 0: S.text(im, (x, y0 + 40*u + i*lh + (1 - q)*22*u), ln, size*u)
    return im

def beforenow(t, it):
    im = S.field(t); u = 2
    tn = it["o_now"] - it["o0"]
    for k, (path, cx, lab, d) in enumerate([(plan.BEFORE, 520, "BEFORE", 0.0), (plan.NOW, 1370, "NOW", tn)]):
        if t < d: continue
        mw, mh = (660, 760) if k == 0 else (860, 760)
        pw, ph = S.photo_size(path, mw, mh); x, y = cx - pw/2, 190
        S.photo_card(im, path, (x, y, pw, ph), t, delay=d, u=u)
        if t > d + 0.2: S.text(im, (x, 108), lab, 40, S.CYAN)
    if t > 0.3:
        S.disclosure(im, "Real pictures of me. Not AI-generated.", (960, 990), u, anchor="mt")
    return im

def ramp(t, it):
    im = S.field(t); u = 2; o0 = it["o0"]
    S.text(im, (150, 120), "THE STARTING RAMP", 40, S.CYAN)
    S.text(im, (150, 172), "Step Up Slowly To Avoid Side Effects", 84)
    for i, (lab, ot) in enumerate(it["o_steps"]):
        d = ot - o0
        if t < d: continue
        q = S.ease(t - d, .5)
        x0 = 150 + i*560; h = 200 + i*120; y1 = 900; y0 = y1 - h + (1 - q)*40
        S.glass(im, (x0, y0, x0 + 480, y1), t, u)
        S.text(im, (x0 + 40, y0 + 40), lab, 110, S.CYAN)
        S.text(im, (x0 + 44, y0 + 175), ["Start here", "Then", "Then"][i], 36, bold=False)
        if i:
            d_ = ImageDraw.Draw(im); ax = x0 - 70; ay = y1 - 60
            d_.polygon([(ax, ay - 22), (ax + 40, ay), (ax, ay + 22)], fill=S.CYAN)
    S.disclosure(im, plan.DISC, (1880, 990), u, anchor="rt", size=20)
    return im

def week(t, it):
    im = S.field(t); u = 2
    S.text(im, (150, 110), "HOW ONE WEEKLY SHOT WORKS", 40, S.CYAN)
    S.text(im, (150, 162), "Strongest Right After Your Shot, Fading By Day 7", 62)
    heights = [0.95, 1.0, 0.9, 0.78, 0.64, 0.5, 0.38]
    for i, hgt in enumerate(heights):
        q = S.ease(t - 0.4 - i*0.18, .5)
        if q <= 0: continue
        x0 = 170 + i*235; y1 = 900; hh = 520*hgt*q
        if hh < 60: continue
        S.glass(im, (x0, y1 - hh, x0 + 180, y1), t, u)
        S.rr(im, (x0 + 6, y1 - hh + 6, x0 + 174, y1 - hh + 18), S.CYAN, 6)
        S.text(im, (x0 + 30, y1 + 20), f"Day {i+1}", 38)
    if t > 0.4:
        S.text(im, (178, 900 - 520*0.95 - 70), "SHOT", 34, S.CYAN)
    return im

def recap(t, it):
    im = S.field(t); u = 2; o0 = it["o0"]
    S.text(im, (150, 96), "RECAP", 40, S.CYAN)
    S.text(im, (150, 148), "5 Tips To Get The Most Out Of A GLP-1", 76)
    S.glass(im, (150, 290, 1770, 990), t, u)
    for i, ((txt, _), ot) in enumerate(zip(it["items"], it["o_items"])):
        if t < ot - o0: continue
        y = 330 + i*128
        S.text(im, (200, y), f"{i+1}.", 64, S.CYAN); S.text(im, (290, y), txt, 64)
    return im

def ai_labels(im, t, split=True, pos="top"):
    # A0058 split screen: centred at the bottom on the split line, clear of both men (review r2 D: top corners touch hair)
    if pos == "bottom": S.disclosure(im, "AI-GENERATED", (960, 972), 2, anchor="mt")
    else: S.disclosure(im, "AI-GENERATED", (36, 36), 2, anchor="lt")
    if split and t > 2.2:
        for x, s, c in ((480, "Protein + Lifting", S.GOOD), (1440, "Low Protein", S.BAD)):
            f = S.font(40); tw = S.text_w(s, f); S.rr(im, (x - tw/2 - 26, 960, x + tw/2 + 26, 1030), (6, 17, 30), 20)
            S.rr(im, (x - tw/2 - 26, 960, x - tw/2 - 16, 1030), c, 4); S.text(im, (x - tw/2, 968), s, 40)
    return im

def bloom_frame(k, w=1920, h=1080):
    """Muhammad's silent bloom flash (RO-05 tools/build.py, measured off his ab-wheel HD master): double pulse around the cut."""
    env = {-5: (0.30, 0.45), -4: (1.0, 3.0), -3: (0.15, 0.45), -2: (0.80, 0.65), -1: (0.95, 0.80), 0: (0.85, 0.75),
           1: (0.90, 0.90), 2: (0.50, 0.70), 3: (0.25, 0.55), 4: (0.10, 0.45)}
    if k not in env: return None
    a, rad = env[k]
    yy, xx = np.mgrid[0:h:4, 0:w:4].astype(np.float32)
    d = np.sqrt(((xx - w*1.02)/(w*rad))**2 + ((yy - h*0.45)/(h*rad*1.2))**2)
    core = np.clip(1.0 - d, 0, 1)**1.3; fringe = np.clip(1.35 - d, 0, 1)**2.0
    col = np.stack([0.75*fringe + core, 0.85*fringe + core, fringe + core], -1).clip(0, 1)*a
    return np.array(Image.fromarray((col*255).astype(np.uint8)).resize((w, h), Image.BILINEAR), np.float32)/255

# ================================================================== frame sources
def dec(cmd_args, n):
    p = subprocess.Popen([FF, "-v", "error"] + cmd_args + ["-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(1920*1080*3)
        if len(b) < 1920*1080*3:
            assert last is not None, cmd_args; yield last; continue
        last = np.frombuffer(b, np.uint8).reshape(1080, 1920, 3); yield last
    p.stdout.close(); p.wait()

def presenter(sh, fa, fb):
    """graded presenter frames for output frames [fa, fb) of shot sh"""
    t_in = sh["in"] + (fa - sh["f0"])/FPS
    vf = (f"crop={CROP[sh['fr']]},scale=1920:1080:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,"
          f"format=gbrpf32le,lut3d=file='{LUT}':interp=tetrahedral,scale=out_color_matrix=bt709:out_range=pc,format=rgb24")
    return dec(["-ss", f"{max(0, t_in - 2):.4f}", "-i", edl.SRC, "-ss", f"{min(2, t_in):.4f}", "-vf", f"fps={FPSS},{vf}"], fb - fa)

def insert_frames(it, fa, fb):
    t_in = it["off"] + (fa - it["f0"])/FPS
    vf = (f"fps={FPSS},scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos:in_color_matrix=bt709,"
          f"crop=1920:1080,format=rgb24")
    return dec(["-ss", f"{t_in:.4f}", "-i", it["src"], "-vf", vf], fb - fa)

SHIFT = dict(dx=300, c0=350, wall_w=500)     # softblue defaults = the WV-01 W2 shift on this same set and crop
BASE_ONLY = os.environ.get("RO12_BASE") == "1"      # graphic-free reference picture for the watch pass
SHIFTED = []    # forced (side-layout) shot frame ranges, set by render_range / compose
def paint(im, g, items, flashes, presenter_frame=False):
    if BASE_ONLY: return np.asarray(im)
    t = g/FPS
    if presenter_frame and any(a <= g < z for a, z in SHIFTED): im = S.shift_presenter(im, **SHIFT)
    for it in items:
        if not (it["f0"] <= g < it["f1"]): continue
        tt = t - it["o0"]; dur = it["o1"] - it["o0"]; k = it["kind"]
        if k == "lt": im = S.lower_third(im, tt, it["topic"], it["point"], dur=dur)
        elif k == "l3":
            items_vis = [x for x, ot in zip(it["items"], it["o_items"]) if t >= ot - 1e-6]
            if items_vis: im = S.left_third(im, 99, it["heading"], items_vis, dur=None)
            else: im = S.left_third(im, 99, it["heading"], [], dur=None)
            if it.get("disc"): S.disclosure(im, it["disc"], (36, 1010), 2, anchor="lt", size=18)
        elif k == "insert" and it.get("ai"): im = ai_labels(im, tt, it.get("ai_split", False), it.get("ai_pos", "top"))
        elif k == "phone": im = iphone(im, phone_frame(it, g))
    x = np.asarray(im)
    for f0 in flashes:
        b = bloom_frame(g - f0)
        if b is not None:
            xf = x.astype(np.float32)/255; x = ((1 - (1 - xf)*(1 - b))*255).astype(np.uint8)
    return x

_PH = {}
def phone_frame(it, g):
    """B0035 app recording (real capture, meal photo -> Analyze Meal -> logged; no banned screen). Its own status bar and Dynamic
    Island are cropped off (top 104 px) so the approved shell's single island is the only one."""
    if it["id"] not in _PH:
        n = it["f1"] - it["f0"] + 2
        p = subprocess.run([FF, "-v", "error", "-ss", f"{it['off']:.3f}", "-i", it["src"], "-frames:v", str(n), "-vf",
                            f"fps={FPSS},crop=660:1330:0:104,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
        fs = [Image.frombytes("RGB", (660, 1330), p[i*660*1330*3:(i+1)*660*1330*3]) for i in range(len(p)//(660*1330*3))]
        _PH[it["id"]] = fs
    fs = _PH[it["id"]]; return fs[min(len(fs) - 1, g - it["f0"])]

_SHD = {}
def iphone(im, content, ox=0):
    """RO-05 round 3/4 approved WV-01 iPhone shell (build_r3.iphone), unchanged."""
    from PIL import ImageFilter, ImageOps
    if ox not in _SHD:
        sh = Image.new('RGBA', im.size); ImageDraw.Draw(sh).rounded_rectangle((91+ox, 34, 573+ox, 1062), 68, fill=(0, 0, 0, 120))
        _SHD[ox] = sh.filter(ImageFilter.GaussianBlur(14))
    im = Image.alpha_composite(im.convert('RGBA'), _SHD[ox]).convert('RGB')
    def rr(box, fill, r, outline=None, width=1): ImageDraw.Draw(im).rounded_rectangle(tuple(v + (ox if i % 2 == 0 else 0) for i, v in enumerate(box)), r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    scr = Image.new('RGB', (448, 1000), (248, 250, 252)); p = ImageOps.contain(content, (432, 920), Image.Resampling.LANCZOS)
    scr.paste(p, ((448 - p.width)//2, 65)); d = ImageDraw.Draw(scr); d.text((30, 14), '9:41', font=S.font(17), fill=(23, 43, 59))
    for i in range(4): d.rounded_rectangle((352+i*6, 30-i*3, 355+i*6, 35), 1, fill=(25, 32, 40))
    d.rounded_rectangle((391, 22, 418, 34), 3, outline=(25, 32, 40), width=2); d.rectangle((419, 26, 422, 30), fill=(25, 32, 40)); d.rectangle((394, 25, 413, 31), fill=(25, 32, 40))
    d.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); d.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); d.ellipse((280, 29, 284, 33), fill=(34, 60, 82)); d.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32))
    m = Image.new('L', (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(scr, (102+ox, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    return im

def scene_frame(it, t):
    k = it["kind"]; tt = t - it["o0"]
    if k == "title": return title_scene(tt, it["eyebrow"], it["headline"])
    if k == "beforenow": return beforenow(tt, it)
    if k == "photo":
        im = S.scene_photo(tt, 1920, 1080, it["photo"], "Real picture of me. Not AI-generated.")
        if tt > 0.2: S.text(im, (110, 60), it["eyebrow"], 40, S.CYAN)
        return im
    if k == "ramp": return ramp(tt, it)
    if k == "week": return week(tt, it)
    if k == "recap": return recap(tt, it)

def render_range(fa, fb, out, TLd):
    items, SH = TLd["items"], TLd["shots"]
    SHIFTED[:] = [(x["f0"], x["f1"]) for x in SH if x["forced"]]
    flashes = [it["f0"] for it in items if it["id"] in plan.FLASH_AT]
    wr = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-",
                           "-vf", "scale=out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "14",
                           "-preset", "medium", "-g", "30", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"],
                          stdin=subprocess.PIPE)
    # piece list over [fa, fb): full-frame items win over presenter shots
    full = sorted([it for it in items if it["kind"] in FULL and it["f1"] > fa and it["f0"] < fb
                   and not (BASE_ONLY and it["kind"] != "insert")], key=lambda i: i["f0"])   # BASE: presenter under graphic scenes
    g = fa; n = 0
    while g < fb:
        cov = next((it for it in full if it["f0"] <= g < it["f1"]), None)
        if cov:
            e = min(cov["f1"], fb)
            src = insert_frames(cov, g, e) if cov["kind"] == "insert" else None
            for k in range(g, e):
                im = Image.fromarray(next(src)) if src else scene_frame(cov, k/FPS)
                wr.stdin.write(np.ascontiguousarray(paint(im, k, items, flashes)).tobytes()); n += 1
            g = e; continue
        sh = next(s for s in SH if s["f0"] <= g < s["f1"])
        nxt = min([sh["f1"], fb] + [it["f0"] for it in full if it["f0"] > g])
        for k, f in zip(range(g, nxt), presenter(sh, g, nxt)):
            act = any(it["f0"] <= k < it["f1"] for it in items) or any(-5 <= k - f0 <= 4 for f0 in flashes) or sh["forced"]
            x = paint(Image.fromarray(f), k, items, flashes, presenter_frame=True) if act else f
            wr.stdin.write(np.ascontiguousarray(x).tobytes()); n += 1
        g = nxt
    wr.stdin.close(); assert wr.wait() == 0 and n == fb - fa, (n, fb - fa)
    os.rename(out + ".tmp.mp4", out)

def _job(a):
    fa, fb, out = a
    if not os.path.exists(out): render_range(fa, fb, out, json.load(open(f"{OD}/timeline.json")))
    print("chunk", out, flush=True); return out

def picture(fa=None, fb=None, name="PICTURE"):
    TLd = json.load(open(f"{OD}/timeline.json")); tot = TLd["total_frames"]
    fa = 0 if fa is None else fa; fb = tot if fb is None else fb
    os.makedirs(f"{OD}/chunks", exist_ok=True)
    n = max(1, (fb - fa)//1800); step = (fb - fa + n - 1)//n
    jobs = [(a, min(fb, a + step), f"{OD}/chunks/{name}_{a:06d}_{min(fb, a+step):06d}.mp4") for a in range(fa, fb, step)]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(2) as ex: outs = list(ex.map(_job, jobs))
    lst = f"{OD}/{name}.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in outs))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OD}/{name}.mp4"])
    print("picture", name, fb - fa, "frames", flush=True)

# ================================================================== audio
def lav():
    b = run([FF, "-nostdin", "-v", "error", "-i", LAV, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]).stdout
    return np.frombuffer(b, np.float32)

def build_voice(B, out):
    x = lav(); N = int(round(B[-1]["f1"]/FPS*SR)); o = np.zeros(N, np.float32); fade = int(0.012*SR); ramp_ = np.linspace(0, 1, fade, dtype=np.float32)
    for b in B:
        i = int(round(b["in"]*SR)); at = int(round(b["f0"]/FPS*SR)); n = int(round((b["f1"] - b["f0"])/FPS*SR))
        seg = x[i:i+n].copy(); seg[:fade] *= ramp_; seg[-fade:] *= ramp_[::-1]
        e = min(N, at + len(seg)); o[at:e] += seg[:e-at]
    import wave
    w = wave.open(out, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(o, -1, 1)*32767).astype("<i2").tobytes()); w.close()

BED_PRE = -10.0; BED_OFFSET = 87.0
BED_TRIM = float(os.environ.get("RO12_BED_TRIM", "-10"))   # 2026-09-30: the lav needs +18.6 dB, which lifted the bed into the floor row; -10 dB measured
def build_bed(total_s, out, swells=()):
    """RO-05 round 4 build_bed_r4 (approved film): same track, seamless equal-power loop over the track body, headroom."""
    import wave
    b = run([FF, "-nostdin", "-v", "error", "-i", "/Volumes/Extreme/_edit_work/abwheel/r2/music/acoustic_bg.mp3", "-ac", "2", "-ar", "48000", "-f", "f32le", "-"]).stdout
    m = np.frombuffer(b, np.float32).reshape(-1, 2)[int(0.5*SR):int(135.5*SR)]
    L = len(m); xf = 3*SR; th = np.linspace(0, np.pi/2, xf)[:, None]; fin, fout = np.sin(th), np.cos(th)
    off = int(BED_OFFSET*SR); N = int(round(total_s*SR)); M = N + off
    bed = np.zeros((M, 2), np.float32); pos = 0
    while pos < M:
        seg = m.copy()
        if pos > 0: seg[:xf] *= fin
        seg[-xf:] *= fout
        e = min(M, pos + L); bed[pos:e] += seg[:e-pos]; pos += L - xf
    bed = bed[off:off + N].copy()
    env = np.ones(N, np.float32); up = 10**(6/20)
    for a, z in swells:
        i, j = int(a*SR), int(z*SR); r = int(0.4*SR)
        if j - i < 2*r: continue
        env[i:j] = up; env[i:i+r] = np.linspace(1, up, r); env[j-r:j] = np.linspace(up, 1, r)
    bed *= env[:, None]; bed *= 10**(BED_PRE/20)
    fi = int(1.0*SR); bed[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(2.5*SR); bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
    assert np.abs(bed).max() < 1.0
    w = wave.open(out, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(bed, -1, 1)*32767).astype("<i2").tobytes()); w.close()

# Audio B = the chain's FITTED EQ + bass=g=0.9 at 150 Hz (Dan's WV-01 choice). WV-01's curve was fitted to WV-01's own take and
# failed the tone row on C1706 (80 Hz +3.6, 5.5 kHz -4.5 vs Muhammad), so the fit is re-run on this roll (out/FIT.mp4.voice_chain.json).
EQ = json.load(open(f"{OD}/FIT.mp4.voice_chain.json"))["eq"] + ",bass=g=0.9:f=150:width_type=q:width=0.7"
def audio(picture_path=None, name="RO12"):
    TLd = json.load(open(f"{OD}/timeline.json")); B = TLd["blocks"]; total_s = TLd["total_frames"]/FPS
    pic = picture_path or f"{OD}/PICTURE.mp4"
    build_voice(B, f"{OD}/voice_raw.wav"); build_bed(total_s, f"{OD}/bed.wav")
    VC = f"{ROOT}/.claude/skills/_shared/audio/voice_chain.py"
    run(["python3", VC, "--in", f"{OD}/voice_raw.wav", "--video", pic, "--frame-lock", pic,
         "--bed", f"{OD}/bed.wav", "--bed-db", str(-40 - BED_PRE + BED_TRIM), "--eq", EQ, "--oversample", "4", "--tp", "-4.0",
         "--out", f"{OD}/{name}.mp4", "--work", f"{OD}/chain"])
    print("audio done", f"{OD}/{name}.mp4", flush=True)

if __name__ == "__main__":
    os.makedirs(OD, exist_ok=True); m = sys.argv[1]
    if m == "timeline":
        B, items, SH, total = timeline()
        print("blocks", len(B), "shots", len(SH), "frames", total, "=", round(total/FPS, 2), "s")
        for sh in SH: print(f"  shot {sh['f0']/FPS:7.2f}-{sh['f1']/FPS:7.2f} ({(sh['f1']-sh['f0'])/FPS:5.2f}) {sh['fr']} src {sh['in']:.2f}{' L3' if sh['forced'] else ''}")
        for it in items: print(f"  {it['id']:4s} {it['kind']:9s} {it['o0']:7.2f}-{it['o1']:7.2f} ({it['o1']-it['o0']:5.2f})")
        cov = sum(it["f1"] - it["f0"] for it in items if it["kind"] in FULL)/total
        print("full-frame coverage", round(cov*100, 1), "%")
    elif m == "picture":
        a = sys.argv.index("--from") if "--from" in sys.argv else None
        fa = fr(float(sys.argv[a+1])) if a else None
        b = sys.argv.index("--to") if "--to" in sys.argv else None
        fb = fr(float(sys.argv[b+1])) if b else None
        nm = sys.argv[sys.argv.index("--name")+1] if "--name" in sys.argv else "PICTURE"
        picture(fa, fb, nm)
    elif m == "audio":
        audio(*(sys.argv[2:4]))

def compose(g, TLd):
    """one finished output frame (for stills and spot checks)"""
    items, SH = TLd["items"], TLd["shots"]; flashes = [it["f0"] for it in items if it["id"] in plan.FLASH_AT]
    SHIFTED[:] = [(x["f0"], x["f1"]) for x in SH if x["forced"]]
    cov = next((it for it in items if it["kind"] in FULL and it["f0"] <= g < it["f1"]), None)
    if cov: im = Image.fromarray(next(insert_frames(cov, g, g + 1))) if cov["kind"] == "insert" else scene_frame(cov, g/FPS)
    else:
        sh = next(s for s in SH if s["f0"] <= g < s["f1"]); im = Image.fromarray(next(presenter(sh, g, g + 1)))
    return Image.fromarray(np.ascontiguousarray(paint(im, g, items, flashes, presenter_frame=cov is None)))

def stills(ids=None):
    TLd = json.load(open(f"{OD}/timeline.json")); os.makedirs(f"{W}/check/stills", exist_ok=True)
    for it in TLd["items"]:
        if ids and it["id"] not in ids: continue
        dur = it["o1"] - it["o0"]
        t = it["o0"] + (dur - 0.3 if it["kind"] in ("l3", "recap", "ramp", "beforenow", "week") else min(dur*0.6, 2.2))
        im = compose(fr(t), TLd); im.save(f"{W}/check/stills/{it['id']}.jpg", quality=88)
        print(it["id"], round(t, 2), flush=True)

if __name__ == "__main__" and sys.argv[1] == "stills":
    stills(sys.argv[2:] or None)
