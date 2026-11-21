"""RO-20 round 2: the new full-screen Soft Blue Light pieces Dan asked for on the round 1 page, as pre-rendered plan clips
(1920x1080, 29.97, BT.709) and stills.
  date     Cb11: the library AI dating-app clip A0089 (heavier profile, no matches, lean profile, matches) lifted out of its
           drawn phone into the approved iPhone shell, text on the right landing on his words, AI-GENERATED chip.
  diagram  Cb12: Dan's own diagram (ten women, ten men, every arrow at the top few men) with the "winner take all" text beside it.
  series   the three-part card that sits under the audio pickups (stills now; its motion is timed to the real recordings).
  levels   the three-levels card for video 3's first seconds (still now).
usage: cards20.py date|diagram [--stills]   |   cards20.py stills"""
import sys, os, json, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import softblue as B, gfx as G
W = "/Volumes/Extreme/_edit_work/ro20"; OUT = f"{W}/round2/cards"; ST = f"{W}/round2/stills"; FPS = 30000/1001; FF = B.FF; U = 2.0
WO = json.load(open(f"{W}/words_out.json"))
def fr(t): return int(round(t*FPS))
def item(cid): return next(r for r in json.load(open(f"{W}/plan_resolved.json")) if r["id"] == cid)
def word_t(phrase, after):
    """output time of the first word of a phrase (same matcher as resolve.py)"""
    import resolve as RS
    i, _ = RS.find(phrase, after); return RS.WO[i]["t0"]
def writer(path):
    return subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "12", "-preset", "medium",
                             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", path], stdin=subprocess.PIPE)
def shell(im, content, ox):
    """The approved WV-01 iPhone shell (same geometry as gfx.iphone / ro06 phone_demo.shell): the status area takes the app's own
    top colour and the space under the content its bottom colour."""
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((91+ox, 34, 573+ox, 1062), 68, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    def rr(box, fill, r, outline=None, width=1): ImageDraw.Draw(im).rounded_rectangle((box[0]+ox, box[1], box[2]+ox, box[3]), r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    p = ImageOps.contain(content, (432, 920), Image.Resampling.LANCZOS); a = np.asarray(p)
    top = tuple(int(v) for v in np.median(np.concatenate([a[:6, :10], a[:6, -10:]], 1).reshape(-1, 3), 0))
    bot = tuple(int(v) for v in np.median(a[-6:].reshape(-1, 3), 0))
    scr = Image.new("RGB", (448, 1000), top); d = ImageDraw.Draw(scr)
    d.rectangle((0, 65 + p.height, 448, 1000), fill=bot)
    if p.width < 448:
        x0 = (448 - p.width)//2; scr.paste(p.crop((0, 0, 1, p.height)).resize((x0, p.height)), (0, 65)); scr.paste(p.crop((p.width-1, 0, p.width, p.height)).resize((448 - x0 - p.width, p.height)), (x0 + p.width, 65))
    scr.paste(p, ((448 - p.width)//2, 65))
    ink = (25, 32, 40) if sum(top) > 380 else (240, 243, 246)
    d.text((30, 14), "9:41", font=B.font(17), fill=ink)
    for i in range(4): d.rounded_rectangle((352+i*6, 30-i*3, 355+i*6, 35), 1, fill=ink)
    d.rounded_rectangle((391, 22, 418, 34), 3, outline=ink, width=2); d.rectangle((419, 26, 422, 30), fill=ink); d.rectangle((394, 25, 413, 31), fill=ink)
    d.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); d.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); d.ellipse((280, 29, 284, 33), fill=(34, 60, 82))
    d.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32) if sum(bot) > 380 else (235, 238, 242))
    m = Image.new("L", (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(scr, (102+ox, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    return im
def eyebrow(im, x, y, s, t):
    if t > .05:
        a = B.ease(t, .55); B.rr(im, (x, y + 8, x + 8 + 70*a, y + 16), B.CYAN, 3); B.text(im, (x, y + 30), s, 30, B.CYAN)
def lines(im, x, y, rows, px, maxw, gap=1.2):
    """rows: [(text, colour, local time since it landed)]; each rises 26 px as it lands; long rows wrap. Returns the y under the block."""
    f = B.font(px)
    for s, col, tt in rows:
        for ln in B.wrap(s, f, maxw):
            if tt > 0: B.text(im, (x, y + (1 - B.ease(tt, .55))*26), ln, px, col)
            y += px*gap
    return y

# ------------------------------------------------------------------ Cb11: the dating-app clip in the phone shell
A89 = None
SCREEN = (80, 150, 1000, 1820)                    # A0089's own screen inside its drawn phone, under its status bar, down to its tab bar
SEG = [(0.0, 1.9), (2.0, 5.9), (6.0, 7.9), (8.0, 10.6)]   # heavier profile, "No new matches!", lean profile, the matches list (source seconds)
def a89():
    global A89
    if A89 is None:
        x0, y0, x1, y1 = SCREEN
        raw = subprocess.run([FF, "-v", "error", "-i", G.lib_path("A0089"), "-vf", f"crop={x1-x0}:{y1-y0}:{x0}:{y0},scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        A89 = np.frombuffer(raw, np.uint8).reshape(-1, y1-y0, x1-x0, 3)
    return A89
TAB = 1556                                        # row (inside SCREEN) where A0089's dark tab bar starts
def a89_screen(f):
    """One A0089 frame re-laid for the taller approved shell: the page at the top, its own page colour under it, the tab bar at the very bottom."""
    a = a89()[f]; w = a.shape[1]; H = round(w*920/432); c = np.empty((H, w, 3), np.uint8); c[:] = a[TAB-4, 4]
    c[:TAB] = a[:TAB]; tb = a[TAB:]; c[H-len(tb):] = tb
    return Image.fromarray(c)
def date_times():
    it = item("Cb11"); t0 = fr(it["t0"])/FPS; n = fr(it["t1"]) - fr(it["t0"])
    lean = word_t("and I got in really good shape", it["t0"]) - t0; hit = word_t("it 10x my matches", it["t0"]) - t0
    end = n/FPS; c3 = max(hit - 0.45, end - 2.6); c2 = max(lean, c3 - 1.9); c1 = max(min(1.9, c2 - 0.6), c2 - 3.9)
    cut = [0.0, c1, c2, c3, end]          # screen changes: no matches, lean profile on "I got in really good shape", matches just before "10x"; no screen runs past its own source length
    for i, (a, b) in enumerate(SEG): assert cut[i+1] - cut[i] <= b - a + 1e-6, ("screen", i, "would be held past its source", cut[i+1] - cut[i], b - a)
    l1 = word_t("I'm someone who was in decent", it["t0"]) - t0
    return n, cut, l1, hit
def date_frame(k, n, cut, l1, hit):
    t = k/FPS; im = B.field(t); F = a89()
    s = max(i for i in range(4) if t >= cut[i]); src = SEG[s][0] + (t - cut[s])
    im = shell(im, a89_screen(min(len(F) - 2, int(src*29.97))), 330)
    x = 1010; y = 330
    eyebrow(im, x, y, "DAN'S RESULT", t)
    lines(im, x - 4, y + 100, [("Decent Shape To Great Shape:", B.WHITE, t - l1), ("10x The Matches.", B.CYAN, t - hit)], 68, 820)
    B.disclosure(im, "AI-GENERATED", (1866, 54), U, anchor="rt")
    return im

# ------------------------------------------------------------------ Cb12: Dan's diagram, full screen
DIAG = f"{W}/round1/dan-dating-diagram.png"
PINK = (184, 52, 120); BLUE = (47, 168, 219)
_D = {}
def diagram_panel():
    if "p" not in _D:
        d = Image.open(DIAG).convert("RGBA"); h = 880; w = round(d.width*h/d.height); d = d.resize((w, h), Image.Resampling.LANCZOS)
        P = Image.new("RGBA", (w + 120, h + 130), (0, 0, 0, 0)); dr = ImageDraw.Draw(P)
        dr.rounded_rectangle((0, 0, P.width - 1, P.height - 1), 30, fill=(246, 250, 253, 255), outline=(118, 183, 222, 255), width=3)
        P.alpha_composite(d, (60, 96))
        f = B.font(34)
        dr.text((60 + 22 - B.text_w("10 Women", f)/2 + 40, 32), "10 Women", font=f, fill=PINK)
        dr.text((60 + w - 30 - B.text_w("10 Men", f)/2 - 22, 32), "10 Men", font=f, fill=BLUE)
        _D["p"] = P
    return _D["p"]
def diagram_times():
    it = item("Cb12"); t0 = fr(it["t0"])/FPS; n = fr(it["t1"]) - fr(it["t0"])
    return n, word_t("The bottom 80", it["t0"]) - t0
def diagram_frame(k, n, bottom):
    t = k/FPS; im = B.field(t); P = diagram_panel(); q = B.ease(t, .6)
    L = P.copy()
    if q < 1: L.putalpha(L.getchannel("A").point(lambda a: round(a*q)))
    x0 = 150; y0 = (1080 - P.height)//2 + round((1 - q)*48)
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((x0 + 12, y0 + 18, x0 + P.width + 12, y0 + P.height + 18), 30, fill=(0, 2, 12, round(120*q)))
    im = Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(L, (x0, y0)); im = im.convert("RGB")
    x = x0 + P.width + 100; card = (x - 54, 286, 1800, 794); B.glass(im, card, t, U, 18)
    eyebrow(im, x, 326, "ONLINE DATING", t)
    y = lines(im, x - 4, 424, [("Winner Take All", B.CYAN, t - .25)], 100, card[2] - x - 40)
    lines(im, x - 2, y + 26, [("The Top Guys Take Everything.", B.WHITE, t - .7), ("The Bottom 80% Get NOTHING.", B.WHITE, t - bottom)], 54, card[2] - x - 40, gap=1.36)
    return im

# ------------------------------------------------------------------ the three-part card under the pickups
PARTS = ["Why Spend More On Your Health", "What To Cut To Find The Money", "What To Buy At Every Income Level"]
def series_card(t, lit=None, tag=None, done=(), window=None, ai=False, t_lit=0.0):
    """lit: the row (0..2) that is lit, with its tag ("Next Video", "This Video", "Last Video"); done: rows that carry a tick;
    window: a 1920x1080 PIL frame shown in the picture window on the right (None = empty frame); ai: AI-GENERATED chip in the window."""
    im = B.field(t)
    eyebrow(im, 110, 146, "A 3-PART SERIES", t)
    if t > .2: B.text(im, (106, 222 + (1 - B.ease(t - .2, .55))*26), "Invest In Your Health", 66)
    y = 370; rh = 168; gap = 26
    for i, s in enumerate(PARTS):
        tt = t - .3 - i*.14
        if tt <= 0: y += rh + gap; continue
        yo = y + (1 - B.ease(tt, .55))*30; box = (110, yo, 940, yo + rh); on = (i == lit and t >= t_lit)
        B.glass(im, box, t, U, 16)
        if on: B.rr(im, box, None, 32, B.CYAN, 4)
        cx, cy = 190, yo + rh/2; d = ImageDraw.Draw(im)
        if i in done:
            d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=B.GOOD); d.line((cx - 17, cy + 1, cx - 5, cy + 14, cx + 19, cy - 13), fill=(5, 13, 28), width=8, joint="curve")
        else:
            d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), outline=B.CYAN if on else (110, 150, 185), width=4)
            f = B.font(44); d.text((cx - B.text_w(str(i + 1), f)/2, cy - 31), str(i + 1), font=f, fill=B.CYAN if on else (150, 180, 205))
        col = B.WHITE if (on or lit is None) else (156, 178, 198)
        f = B.font(40); ls = B.wrap(s, f, 640); ty = yo + rh/2 - len(ls)*25
        for ln in ls: B.text(im, (262, ty), ln, 40, col); ty += 50
        if on and tag:
            f2 = B.font(24); tw = B.text_w(tag.upper(), f2); bx = (940 - tw - 52, yo - 20, 940 - 16, yo + 24)
            B.rr(im, bx, B.CYAN, 22); ImageDraw.Draw(im).text((bx[0] + 18, bx[1] + 7), tag.upper(), font=f2, fill=(5, 13, 28))
        y += rh + gap
    wx, wy, ww, wh = 1010, 407, 800, 450
    if t > .45:
        q = B.ease(t - .45, .6); pad = 14
        L = Image.new("RGBA", (ww + 2*pad + 30, wh + 2*pad + 30)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((pad + 10, pad + 16, pad + ww + 10, pad + wh + 16), 30, fill=(0, 2, 12, 120)); L = L.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((0, 0, ww + 2*pad, wh + 2*pad), 26, fill=(42, 80, 113, 255), outline=(118, 183, 222, 150), width=2)
        if window is not None:
            p = ImageOps.fit(window, (ww, wh)); m = Image.new("L", (ww, wh)); ImageDraw.Draw(m).rounded_rectangle((0, 0, ww - 1, wh - 1), 16, fill=255); L.paste(p, (pad, pad), m)
        if q < 1: L.putalpha(L.getchannel("A").point(lambda a: round(a*q)))
        im.paste(L, (wx - pad, round(wy - pad + (1 - q)*40)), L)
        if ai and window is not None and q >= 1: B.disclosure(im, "AI-GENERATED", (wx + ww - 14, wy + 14), U, anchor="rt", size=17)
    return im

# ------------------------------------------------------------------ the three-levels card (video 3, first seconds)
PH = f"{W}/stock/photos"
LEVELS = [("Dead Broke", "A Home Setup Under $100", f"{PH}/pexels-8033019-ab-roller-and-black-dumbbells-on-yoga-mat.jpg"),
          ("Middle Class", "$500 To $1,000 A Month", f"{PH}/pexels-4663250-cooked-fish-with-green-vegetable-on-white-plate.jpg"),
          ("Over $10,000 A Month", "Home Gym, Meal Prep, Maid", f"{PH}/pexels-36777945-modern-home-gym-interior.jpg")]
def levels_card(t, lands=(0.4, 1.3, 2.3)):
    im = B.field(t)
    eyebrow(im, 110, 136, "WHAT TO BUY FOR YOUR HEALTH", t)
    if t > .2: B.text(im, (106, 212 + (1 - B.ease(t - .2, .55))*26), "At Every Income Level", 66)
    tw, th, gap = 540, 338, 40
    for i, (a, b, ph) in enumerate(LEVELS):
        tt = t - lands[i]
        if tt <= 0: continue
        x = 110 + i*(tw + gap); B.photo_card(im, ph, (x, 370, tw, th), tt, fit=True, u=U)
        if tt > .25:
            box = (x - 6, 370 + th + 44, x + tw + 6, 370 + th + 44 + 190); B.glass(im, box, t, U, 16)
            B.text(im, (x + 26, box[1] + 30), a, 44); f = B.font(34)
            yy = box[1] + 100
            for ln in B.wrap(b, f, tw - 40): B.text(im, (x + 26, yy), ln, 34, B.CYAN); yy += 44
    return im

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(ST, exist_ok=True); what = sys.argv[1]; stills = "--stills" in sys.argv
    if what == "date":
        n, cut, l1, hit = date_times(); print("Cb11", n, "frames; screens at", [round(c, 2) for c in cut], "text at", round(l1, 2), round(hit, 2))
        if stills:
            for nm, tt in (("a", cut[1] - .3), ("b", cut[2] - .3), ("c", cut[3] - .2), ("d", n/FPS - .3)): date_frame(int(tt*FPS), n, cut, l1, hit).save(f"{ST}/Cb11-{nm}.png")
        else:
            e = writer(f"{OUT}/Cb11-dating.mp4")
            for k in range(n + 12): e.stdin.write(date_frame(min(k, n - 1) if k >= n else k, n, cut, l1, hit).tobytes())
            e.stdin.close(); e.wait()
    if what == "diagram":
        n, bottom = diagram_times(); print("Cb12", n, "frames; 'The Bottom 80%' at", round(bottom, 2))
        if stills: diagram_frame(n - 8, n, bottom).save(f"{ST}/Cb12-diagram.png"); diagram_frame(int((bottom - .2)*FPS), n, bottom).save(f"{ST}/Cb12-diagram-early.png")
        else:
            e = writer(f"{OUT}/Cb12-diagram.mp4")
            for k in range(n + 12): e.stdin.write(diagram_frame(k, n, bottom).tobytes())
            e.stdin.close(); e.wait()
    if what == "stills":
        def cf(src, ts): return G.clip_frame(G.src_path(src) if not src.startswith("/") else src, ts)
        S = f"{W}/stock"; M = f"{W}/round2/motion"
        series_card(6, 1, "Next Video", done=(0,), window=cf(f"{S}/pexels-8942658-camera-focus-of-colorful-beverages.mp4", 3.0)).save(f"{ST}/SC-P1-next-is-2.png")
        series_card(6, 2, "Next Video", done=(0,), window=cf(f"{M}/A3-t1.mp4", 5.2), ai=True).save(f"{ST}/SC-P1-then-3.png")
        series_card(6, 0, "Last Video", window=cf(f"{S}/pexels-6520321-ambulance-on-the-road.mp4", 1.0)).save(f"{ST}/SC-P2-last-was-1.png")
        series_card(6, 1, "This Video", done=(0,), window=cf(f"{S}/pexels-5981290-a-woman-recording-her-receipts-in-a-planner.mp4", 3.0)).save(f"{ST}/SC-P2-this-is-2.png")
        series_card(6, 2, "Next Video", done=(0, 1), window=cf("A0037", 1.0), ai=True).save(f"{ST}/SC-P3-next-is-3.png")
        series_card(6, 2, "This Video", done=(0, 1), window=cf(f"{S}/pexels-8942658-camera-focus-of-colorful-beverages.mp4", 3.0)).save(f"{ST}/SC-P4-this-is-3.png")
        levels_card(6).save(f"{ST}/LV-P4-three-levels.png")
        print("stills ->", ST)
