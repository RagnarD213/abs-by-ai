#!/usr/bin/env python3
"""RO-20 round 3: the four audio pickups (P1 end of video 1, P2 start of video 2, P3 end of video 2, P4 start of video 3) as
full-screen picture segments. A pickup has no camera picture, so every frame is a clip, the three-part card or the three-levels
card, following the picture list Dan approved (round2/pickups/pickups_doc.html), row by row.

Driven ONLY by a per-pickup word-times file. No time is typed anywhere in this file: every cue is a phrase looked up in
    WORDS.json = {"duration": seconds, "words": [{"w": "In", "t0": 0.12, "t1": 0.30}, ...]}
and the build stops, printing the phrase, when a cue phrase is not in the words.

usage:
  pickups20.py P1|P2|P3|P4 WORDS.json OUT.mp4 [--audio VOICE.wav] [--sheet SHEET.jpg] [--full-open] [--start S]
               [--j1 PATH] [--j1-in S] [--allow-dup] [--dry]
  pickups20.py sheet P# WORDS.json OUT.mp4 SHEET.jpg      contact sheet of an existing render (one frame per cue, cue + 0.4 s)
  pickups20.py placeholders                                round3/pickups/placeholder_words_P#.json from the old recording
  pickups20.py selftest                                    the settled card against the approved stills' own drawing code

Output: 1920x1080, 30000/1001 fps, BT.709 tagged, libx264 crf 14, exactly round(duration * fps) frames. OUT.mp4.cues.json lists
every cue as built (words, time, what shows, source, in and out).

P2: Dan chose the camera open (video 2 starts on camera with his own take of the first line), so the segment STARTS at
"In the last video". If the words file still holds the first line, the segment starts in the gap before "In the last video"
(--start S overrides) and --audio is cut at the same point. --full-open builds the other shape (B0450, the bar cash, the heart
monitor under the first line).

Rules this file enforces: a clip is never slowed or frozen (a slot longer than its clip takes an earlier in-point, and past that
the picture cuts to the card early or the window leaves); every clip of Dan goes through its grade (gfx.clip_vf reads
round2/broll_grades.json); every AI clip carries the AI-GENERATED chip, placed off the faces; no source twice inside one video
(checked against the plan clips inside that video's ranges in round2-plan/videos.json and against the other pickup of that video).

The three-part card: series_rows() and window() below are COPIES of cards20.series_card (cards20.py is locked), split in two so
the rows can change state on a word (0.3 s ease, no bounce) and the picture window can come and go by itself. `selftest`
proves the settled frame is the approved still's frame. The three-levels card is cards20.levels_card itself, unchanged."""
import sys, os, re, json, time, subprocess, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter

W = "/Volumes/Extreme/_edit_work/ro20"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FPS = 30000/1001; U = 2.0
OLD_TRANSCRIPT = f"{REPO}/Media/longform-raw/ro20-pickups/pickups_all_takes.transcript.json"
PRESENTER = f"{W}/round1/first-minute/DRAFT - RO-20 round 1 - first minute.mp4"      # the look D reference brollgrade20.py measures

def load_json(path, tries=8):
    """Another helper rewrites the timeline files while this runs: re-read on a half-written file."""
    err = None
    for _ in range(tries):
        try:
            with open(path) as f: return json.load(f)
        except (ValueError, OSError) as e: err = e; time.sleep(0.6)
    raise SystemExit(f"cannot read {path}: {err}")
def _imports():
    err = None
    for _ in range(8):                                     # cards20 reads words_out.json when it is imported
        try:
            import softblue as B, gfx as G, cards20 as C; return B, G, C
        except (ValueError, OSError) as e: err = e; time.sleep(0.6)
    raise SystemExit(f"cannot import the recipe modules: {err}")
B, G, C = _imports()
FF = B.FF; FP = FF.replace("ffmpeg", "ffprobe")
def fr(t): return int(round(t*FPS))

# ------------------------------------------------------------------ the words file and the cue lookup
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
class Words:
    def __init__(self, path):
        d = load_json(path); self.path = path; self.dur = float(d["duration"])
        self.w = [x for x in d["words"] if norm(x["w"])]; self.n = [norm(x["w"]) for x in self.w]
        self.S = "".join(self.n); self.at = {}; self.end = {}; c = 0
        for i, s in enumerate(self.n): self.at[c] = i; c += len(s); self.end[c] = i
        assert self.w and self.w[-1]["t1"] <= self.dur + 1e-3, "duration is shorter than the last word"
    def text(self, i0=0, i1=None): return " ".join(x["w"].strip() for x in self.w[i0:i1])
    def find(self, alts, after=0):
        """First and last word index of the phrase, searching from word `after`. Case, punctuation and word breaks do not count
        ("six-pack" = "six pack", "$10,000" = "$10 ,000", "AbsByAI.com" = "absbyai .com"). `alts` are the wordings Dan may have
        used, most exact first. If none is there letter for letter, the closest run of words is taken when it is close enough
        (a transcript mishearing), and said out loud."""
        c0 = sum(len(s) for s in self.n[:after])
        for a in alts:
            p = norm(a); pos = self.S.find(p, c0)
            while pos >= 0:
                if pos in self.at and pos + len(p) in self.end: return self.at[pos], self.end[pos + len(p)], a, "exact"
                pos = self.S.find(p, pos + 1)
        best = (0, None)
        for a in alts:
            p = norm(a); m = len(a.split())
            if m < 3: continue                              # a one or two word phrase is never guessed
            for n in range(max(2, m - 2), m + 3):
                for i in range(after, len(self.n) - n + 1):
                    r = difflib.SequenceMatcher(None, p, "".join(self.n[i:i + n])).ratio()
                    if r > best[0] + 1e-9: best = (r, (i, i + n - 1, a))
        if best[1] and best[0] >= 0.74:
            i0, i1, a = best[1]; return i0, i1, a, f"CLOSEST ({best[0]:.2f}): heard \"{self.text(i0, i1 + 1)}\""
        return None
class Cues:
    """Named cue times, looked up in order: each search starts after the cue before it."""
    def __init__(self, words, pid): self.W = words; self.pid = pid; self.i = 0; self.t = {}; self.log = []
    def add(self, name, alts, edge="t0", optional=False):
        hit = self.W.find(alts, self.i)
        if hit is None:
            if optional: return None
            raise SystemExit(f"\n{self.pid}: CUE PHRASE NOT FOUND: \"{alts[0]}\" (also tried: {alts[1:]})\n"
                             f"  searched the words after word {self.i}: \"{self.W.text(self.i)}\"\n  words file: {self.W.path}\n")
        i0, i1, a, how = hit; t = self.W.w[i0]["t0"] if edge == "t0" else self.W.w[i1]["t1"]
        if edge == "t0": self.i = i0 + 1
        self.t[name] = t; self.log.append(dict(cue=name, doc=alts[0], matched=a, how=how, heard=self.W.text(i0, i1 + 1), word=i0, edge=edge, t=round(t, 3)))
        if how != "exact": print(f"  NOTE {self.pid} cue \"{alts[0]}\": {how}", flush=True)
        return t
    def __getitem__(self, k): return self.t[k]

# ------------------------------------------------------------------ sources
def dur(path): return float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
def plan_item(pred):
    return next((r for r in load_json(f"{W}/plan_resolved.json") if r.get("kind") == "clip" and pred(r)), None)
def plan_src(note_has, file_has, fallback):
    """A stock clip the film already uses ("stock, from video 1 / video 2"): the same file and crop as the plan item whose note says so."""
    it = plan_item(lambda r: note_has.lower() in r.get("note", "").lower() and any(file_has in s for s in r.get("src", [])))
    if not it: print(f"  NOTE: no plan clip with \"{note_has}\" in its note; using {os.path.basename(fallback)}"); return fallback, 0.0, None, None
    s = next(s for s in it["src"] if file_has in s); return G.src_path(s), G.src_start(s), it.get("crop"), it["id"]
# stock that reads dark gets a lift here, in RGB after the BT.709 decode, the same place the B-roll grades go (looked at beside a presenter still)
STOCK_GRADE = {"pexels-9564076": "curves=all='0/0 0.10/0.15 0.30/0.42 0.60/0.74 1/1'",          # a dim bar: lifted
               # the ECG strip is milky as delivered (its white paper sits at 0.62, its blacks at 0.23): stretched so the paper is white
               "B0275": "curves=all='0/0 0.22/0.10 0.42/0.42 0.56/0.72 0.64/0.90 1/1',eq=saturation=1.2"}
# a wide shot in the 800 px window is punched in on its subject (source pixels: w, h, x, y); the grade is unchanged
WINDOW_CROP = {"B0032": (1280, 720, 320, 300), "B0207": (960, 540, 190, 170)}
class Use:
    """One use of a source: where it starts (pref, moved earlier if the slot needs more), the part that may be used [a, b], its label."""
    def __init__(self, name, src, pref=0.0, a=0.05, b=None, ai=False, chip="rt", crop=None, own_label=False, still=None, what=""):
        self.name = name; self.path = None if still else G.src_path(src); self.still = still; self.pref = pref; self.a = a; self.ai = ai; self.chip = chip
        self.crop = crop; self.own_label = own_label; self.what = what
        self.len = None if still else dur(self.path); self.b = None if still else (b if b is not None else self.len - 0.07)
        self.key = srckey(still or self.path)
        self.graded = None if still else (G.grade_for(self.path) or next((v for k, v in STOCK_GRADE.items() if k in self.path), None))
    def fit(self, n):
        """(in-point, frames it can play) for a slot of n frames: the preferred in-point, earlier if the slot is longer, never held."""
        if self.still: return 0.0, n
        t_in = max(self.a, min(self.pref, self.b - n/FPS)); return t_in, min(n, int((self.b - t_in)*FPS))
    def frames(self, t_in, n, size=None):
        if self.still:
            im = Image.open(self.still).convert("RGB"); im = ImageOps.fit(im, size or (1920, 1080), Image.Resampling.LANCZOS)
            for _ in range(n): yield im
            return
        vf = "fps=30000/1001," + G.clip_vf(1.0, self.path)                    # BT.709 decode, fill, his own B-roll grade
        vf = vf[:-len(",format=rgb24")]
        if ",format=gbrp" not in vf: vf += ",format=gbrp"                    # RGB before anything else touches it (README: the curves / BT.601 trap)
        if self.graded and not G.grade_for(self.path): vf += "," + self.graded
        if self.crop: vf = vf.replace("scale=1920:1080", "crop={}:{}:{}:{},scale=1920:1080".format(*self.crop), 1)
        w, h = size or (1920, 1080)
        if size: vf += f",scale={w}:{h}:flags=lanczos"
        vf += ",format=rgb24"
        p = subprocess.Popen([FF, "-v", "error", "-ss", f"{t_in:.3f}", "-i", self.path, "-frames:v", str(n), "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for i in range(n):
            buf = p.stdout.read(w*h*3)
            assert len(buf) == w*h*3, f"{self.name}: {os.path.basename(self.path)} ran out at frame {i} of {n} from {t_in:.2f} s (never hold a clip)"
            yield Image.frombytes("RGB", (w, h), buf)
        p.stdout.close(); p.wait()
def srckey(p):
    b = os.path.basename(p.split("@")[0])
    m = re.match(r"([AB]\d{4})(_|$)", b) or re.match(r"([A-Z]\d{1,2})-(t\d+|start|end|sync\d+|seg\d+)\.", b) or re.match(r"(pexels-\d+)", b)
    return m.group(1) if m else b

LIBNOTE = {"B0450": "Dan, dumbbell lateral raises by the pool", "B0275": "library stock, ECG strip printing", "B0032": "Dan, push-ups by the pool",
           "B0427": "Dan, ab wheel rollouts by the pool", "B0207": "library stock, hands counting dollar bills", "B0429": "Dan, front-on by the pool, hands on hips",
           "B0462": "Dan, walking lunges by the pool", "A0037": "library AI clip, the home gym"}
def lib(cid, pref, window=False, **k):
    if window and cid in WINDOW_CROP: k["crop"] = WINDOW_CROP[cid]
    return Use(cid, cid, pref, ai=cid.startswith("A"), what=LIBNOTE[cid] + (", punched in for the window" if k.get("crop") else ""), **k)
def sources(pid, opt):
    S = f"{W}/stock"; M = f"{W}/round2/motion"; u = {}
    def cocktails(pref=None):
        p, st, crop, iid = plan_src("three showy cocktails", "pexels-8942658", f"{S}/pexels-8942658-camera-focus-of-colorful-beverages.mp4")
        return Use("cocktails", p, st if pref is None else pref, crop=crop, what=f"stock, three showy cocktails on a bar (plan clip {iid}, video 2)")
    if pid == "P1":
        u["cocktails"] = cocktails()
        u["A2"] = Use("A2", f"{M}/A2-t1.mp4", 1.3, ai=True, what="approved AI clip, the brokie turning out his pockets")
        u["A3"] = Use("A3", f"{M}/A3-t1.mp4", 4.2, ai=True, what="approved AI clip, the cardboard box house guy swinging his kettlebell")
        u["A0037"] = lib("A0037", 0.6)
    if pid == "P2":
        j1 = opt["j1"]
        if os.path.exists(j1): u["J1"] = Use("J1", j1, opt["j1_in"], ai=True, chip="rb", what=f"AI clip, the fit guy getting the job in the boardroom ({os.path.basename(j1)})")
        else:
            if not opt.get("quiet"): print(f"  NOTE: {j1} does not exist yet; the boardroom picture is a STILL of aiframes/J1-end.png with the AI-GENERATED chip")
            u["J1"] = Use("J1", None, still=f"{W}/aiframes/J1-end.png", ai=True, chip="rb", what="STILL of aiframes/J1-end.png (the boardroom clip is not generated yet)")
        u["B0032"] = lib("B0032", 0.3, window=True); u["B0427"] = lib("B0427", 1.0, window=True)
        p, st, crop, iid = plan_src("ambulance drives off", "pexels-6520321", f"{S}/pexels-6520321-ambulance-on-the-road.mp4")
        u["ambulance"] = Use("ambulance", p, max(st, 0.3), crop=crop, what=f"stock, the ambulance (plan clip {iid}, video 1)")
        # the doc asks for scissors cutting a credit card in half (new stock). Pexels has no such clip (about 40 searches, 2026-10-12);
        # this is the picture Dan saw in this very window on the approved "This Video" still (cards20.py stills). Swap the path when a real one exists.
        u["cut"] = Use("receipts", opt.get("cut") or f"{S}/pexels-5981290-a-woman-recording-her-receipts-in-a-planner.mp4", 2.0,
                       what="stock, going through receipts and cash with a planner (stands in for the scissors and credit card: none on Pexels)")
        if opt["full_open"]:
            u["B0450"] = lib("B0450", 0.3); u["B0275"] = lib("B0275", 1.0)
            u["barcash"] = Use("barcash", f"{S}/pexels-9564076-man-leaving-money-at-the-bar.mp4", 15.6, a=13.2, b=27.5, what="stock (Pexels 9564076), a man counts out bills and puts them down on the bar beside his drink")
    if pid == "P3":
        u["B0207"] = lib("B0207", 0.5, window=True)
        u["A3"] = Use("A3", f"{M}/A3-t1.mp4", 4.2, ai=True, what="approved AI clip, the cardboard box house guy swinging his kettlebell")
        u["A0037"] = lib("A0037", 0.6)
        it = plan_item(lambda r: r.get("id") == "P01")
        src = it["src"][0] if it else "/Volumes/Extreme/_edit_work/ro06/round5/phone/P01-softblue.mp4@0.0"
        u["P01"] = Use("P01", src, G.src_start(src), a=0.0, b=dur(G.src_path(src)) - 0.04, own_label=True, what="the approved self-generation app demo (plan item P01), its own AI-GENERATED label inside")
    if pid == "P4":
        u["B0429"] = lib("B0429", 0.5); u["B0462"] = lib("B0462", 0.5); u["B0275"] = lib("B0275", 1.0); u["cocktails"] = cocktails()
    return u

# ------------------------------------------------------------------ no source twice inside one video
VIDEO = {"P1": "video1", "P2": "video2", "P3": "video2", "P4": "video3"}
def video_sources(pid, full_open):
    V = load_json(f"{W}/round2-plan/videos.json"); v = V[VIDEO[pid]]; rng = [p["range"] for p in v["parts"] if "range" in p]
    if VIDEO[pid] == "video2" and not full_open:           # the camera open is a piece of the film too
        for p in v["parts"]:
            m = re.search(r"film ([\d.]+) to ([\d.]+)", p.get("option", ""))
            if m: rng.append([float(m.group(1)), float(m.group(2))])
    used = {}
    for r in load_json(f"{W}/plan_resolved.json"):
        if r.get("kind") != "clip" or not any(r["t0"] < b and r["t1"] > a for a, b in rng): continue
        for s in list(r.get("src", [])) + list(r.get("frames", [])): used.setdefault(srckey(s), []).append(r["id"])
    return used, rng
def dupcheck(pid, uses, opt):
    used, rng = video_sources(pid, opt["full_open"]); bad = []
    for u in uses:
        if u.key in used: bad.append(f"{u.name} ({u.key}) is already in {VIDEO[pid]} as plan clip {used[u.key]}")
    for other in (p for p, v in VIDEO.items() if v == VIDEO[pid] and p != pid):
        ok = {x.key for x in sources(other, dict(opt, full_open=False, quiet=True)).values()}
        bad += [f"{u.name} ({u.key}) is also in {other}, the same video" for u in uses if u.key in ok]
    keys = [u.key for u in uses]; bad += [f"{k} is used twice inside {pid}" for k in sorted(set(keys)) if keys.count(k) > 1]
    print(f"  no-repeat check: {len(uses)} sources against {len(used)} sources in {VIDEO[pid]} ({', '.join(f'{a:.0f} to {b:.0f}' for a, b in rng)} s): " + ("clean" if not bad else "REPEATS"))
    if bad and not opt["allow_dup"]: raise SystemExit(f"\n{pid}: a source repeats inside one video:\n  " + "\n  ".join(bad) + "\n")

# ------------------------------------------------------------------ the three-part card (copied from cards20.series_card, split in two)
PARTS = C.PARTS
def series_rows(t, st):
    """The card without its picture window. st = dict(lit=row or None, tag=text or None, done=(rows that carry a tick)).
    Same geometry, colours and entrance as cards20.series_card; a row with no row lit anywhere is white, as there."""
    lit, tag, done = st["lit"], st["tag"], st["done"]
    im = B.field(t)
    C.eyebrow(im, 110, 146, "A 3-PART SERIES", t)
    if t > .2: B.text(im, (106, 222 + (1 - B.ease(t - .2, .55))*26), "Invest In Your Health", 66)
    y = 370; rh = 168; gap = 26
    for i, s in enumerate(PARTS):
        tt = t - .3 - i*.14
        if tt <= 0: y += rh + gap; continue
        yo = y + (1 - B.ease(tt, .55))*30; box = (110, yo, 940, yo + rh); on = (i == lit)
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
    return im
WX, WY, WW, WH, PAD = 1010, 407, 800, 450, 14               # the picture window (cards20.series_card)
_WIN = {}
def window(im, pic, q, rise, ai, chip):
    """The picture window: pic is an 800x450 frame; q fades it (in and out), rise moves it (in only). The AI chip sits inside the
    picture, top right, or bottom right when faces are along the top (the boardroom), and fades with it."""
    if q <= 0: return im
    if "base" not in _WIN:
        L = Image.new("RGBA", (WW + 2*PAD + 30, WH + 2*PAD + 30)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((PAD + 10, PAD + 16, PAD + WW + 10, PAD + WH + 16), 30, fill=(0, 2, 12, 120)); L = L.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((0, 0, WW + 2*PAD, WH + 2*PAD), 26, fill=(42, 80, 113, 255), outline=(118, 183, 222, 150), width=2)
        m = Image.new("L", (WW, WH)); ImageDraw.Draw(m).rounded_rectangle((0, 0, WW - 1, WH - 1), 16, fill=255); _WIN["base"] = L; _WIN["mask"] = m
    L = _WIN["base"].copy(); L.paste(pic, (PAD, PAD), _WIN["mask"])
    if ai: B.disclosure(L, "AI-GENERATED", (PAD + WW - 14, PAD + 14 if chip == "rt" else PAD + WH - 14 - 40*U), U, anchor="rt", size=17)
    if q < 1: L.putalpha(L.getchannel("A").point(lambda a: round(a*q)))
    im.paste(L, (WX - PAD, round(WY - PAD + rise)), L); return im

# ------------------------------------------------------------------ the timeline of one pickup
LIGHT = 0.9          # a card that comes in ON a cue lights its row once its rows have landed
WIN_IN, WIN_OUT, STATE = 0.45, 0.25, 0.30
def st(lit=None, tag=None, done=()): return dict(lit=lit, tag=tag, done=tuple(done))
def program(pid, WD, opt):
    """-> (frames, elements, cue log). Elements cover every frame once:
       dict(kind="clip", f0, f1, use, t_in) | dict(kind="levels", f0, f1, lands) | dict(kind="series", f0, f1, c0, events, wins)"""
    q = Cues(WD, pid); u = sources(pid, opt); start = 0.0; notes = []
    def A(name, *alts, **k): return q.add(name, list(alts), **k)
    if pid == "P1":
        A("card", "In the next video")
        A("cut", "what you should cut to find that money", "what you should cut", "what to cut")
        A("brokie", "even if you're a brokie right now", "even if you're a brokie", "even if you are a brokie", "even if you're a brokey", "even if you're broke", "even if")
        A("after", "In the video after that", "the video after that", "video after that")
        A("dead", "from dead broke", "dead broke")
        A("baller", "to mega baller", "to a mega baller", "to megaballer", "to baller", "mega baller")
        spec = [("series", 0.0, None, dict(events=[(0.0, st(done=(0,))), ("light", st(1, "Next Video", (0,))), (q["after"], st(2, None, (0,)))],
                 wins=[(q["cut"], q["brokie"], u["cocktails"]), (q["brokie"], q["after"], u["A2"]), (q["dead"], q["baller"], u["A3"]), (q["baller"], None, u["A0037"])]))]
    if pid == "P2":
        if opt["full_open"]:
            A("open", "You are being too cheap with your health", "You're being too cheap with your health", "being too cheap")
            A("cheap", "and your cheapness and wasting money on bullshit", "and your cheapness", "your cheapness", "Being cheap with your health", "wasting money on bullshit")
            A("kill", "is literally killing you", "literally killing you")
        A("card", "In the last video, I told you why you need to spend more", "In the last video")
        i_card = q.log[-1]["word"]
        if not opt["full_open"]:
            if opt["start"] is not None: start = opt["start"]
            elif i_card > 0:                                # the first line is in the words file: start in the gap before "In the last video"
                start = max(WD.w[i_card - 1]["t1"], q["card"] - 0.15)
                notes.append(f"the words file holds {i_card} words before \"In the last video\" (the first line, said on camera in video 2): the segment starts at {start:.3f} s of the words file")
        A("money", "makes you more money", "make you more money", "more money")
        A("prod", "and more productive", "more productive")
        A("bad", "bad health is ludicrously expensive", "bad health is", "bad health")
        A("this", "In this video, I'll tell you exactly what to cut", "In this video")
        A("so", "so you can spend more money on your health", "so you can spend", "spend more money on your health")
        card = ("series", q["card"] if opt["full_open"] else start, None, dict(events=[(None, st()), ("light", st(0, "Last Video")), (q["this"], st(1, "This Video", (0,)))],
                wins=[(q["money"], q["prod"], u["J1"]), (q["prod"], q["bad"], u["B0032"]), (q["bad"], q["this"], u["ambulance"]), (q["this"], q["so"], u["cut"]), (q["so"], None, u["B0427"])]))
        spec = ([("clip", 0.0, q["cheap"], u["B0450"]), ("clip", q["cheap"], q["kill"], u["barcash"]), ("clip", q["kill"], q["card"], u["B0275"])] if opt["full_open"] else []) + [card]
    if pid == "P3":
        A("card", "That's what to cut", "That is what to cut", "what to cut")
        A("now", "Now you have the money", "Now you have")
        A("next", "In the next video")
        A("dead", "from dead broke", "dead broke")
        A("baller", "to baller", "to mega baller", "to a baller", "baller")
        A("step", "To take the first step", "If you want to take the first step", "take the first step")
        A("goto", "go to AbsByAI.com", "go to abs by ai", "AbsByAI.com", "go to")
        A("free", "ripped six-pack abs, for free", "six-pack abs for free", "abs for free", "for free", edge="t1")
        A("thanks", "Thanks for watching guys", "Thank you for watching guys", "Thanks for watching", "Thank you for watching")
        # the demo covers "To take the first step ... for free." It is 11 s and is never slowed or held: when Dan takes longer than that,
        # it starts later (never past "go to AbsByAI.com") so the finished picture is up as he says "six-pack abs, for free", and the home
        # gym stays in the window until it starts. A demo that still ends before "Thanks for watching" cuts to the card when it finishes.
        d_len = (int((u["P01"].b - u["P01"].a)*FPS) - 1)/FPS; d0 = min(max(q["step"], q["free"] - d_len), max(q["step"], q["goto"])); d1 = min(q["thanks"], d0 + d_len)
        if d0 > q["step"] + 1/FPS: notes.append(f"\"To take the first step ... for free\" runs {q['thanks'] - q['step']:.1f} s and the demo is {d_len:.1f} s: the demo starts {d0 - q['step']:.2f} s after \"To take the first step\" (the home gym holds in the window until then)")
        if d1 < q["thanks"] - 1/FPS: notes.append(f"the demo ends {q['thanks'] - d1:.2f} s before \"Thanks for watching\": the three-part card comes back when it finishes")
        ev = [(0.0, st(done=(0,))), ("light", st(done=(0, 1))), (q["next"], st(2, "Next Video", (0, 1)))]
        spec = [("series", 0.0, d0, dict(events=ev, wins=[(q["now"], q["dead"], u["B0207"]), (q["dead"], q["baller"], u["A3"]), (q["baller"], d0, u["A0037"])])),
                ("clip", d0, d1, u["P01"]),
                ("series", d1, None, dict(events=ev, wins=[], same_card=True))]          # row 3 lit, right half and lower area empty for YouTube's end screen
    if pid == "P4":
        A("open", "Here's exactly what you should be buying for your health", "Here is exactly what you should be buying for your health", "exactly what you should be buying", optional=True)
        A("whether", "whether you're dead broke", "whether you are dead broke", "whether")
        q.i = q.log[-1]["word"]                             # "dead broke" is inside that phrase
        A("dead", "dead broke"); A("middle", "middle class")
        A("tenk", "making over $10,000 a month", "making over $10,000", "over $10,000 a month", "over $10,000", "$10,000")
        A("need", "You need to be spending more money on your health", "You need to be spending", "need to be spending")
        A("good", "money does you no good", "money does no good", "does you no good", "no good if you're dead")
        A("last", "The last video covered what to cut", "The last video covered", "The last video")
        A("spend", "Now let's spend it", "Now let us spend it", "Now let's", "let's spend it")
        # round 3 (Dan, 2026-10-13: "I don't really understand why I'm standing around before the clip, but the graphic itself looks good"):
        # the B0429 open is out; video 3 opens on the three-levels card from its first frame.
        spec = [("levels", 0.0, q["need"], dict(lands=(q["dead"], q["middle"], q["tenk"]))),
                ("clip", q["need"], q["good"], u["B0462"]), ("clip", q["good"], q["last"], u["B0275"]),
                ("series", q["last"], None, dict(events=[(None, st(done=(0,))), ("light", st(1, "Last Video", (0,))), (q["spend"], st(2, "This Video", (0, 1)))],
                 wins=[("card", None, u["cocktails"])]))]
    ts = [c["t"] for c in q.log if c["edge"] == "t0"]
    assert all(a < b for a, b in zip(ts, ts[1:])), f"{pid}: cue times are not in order: {[(c['cue'], c['t']) for c in q.log]}"
    # ---- to frames. Time zero of the segment is `start` of the words file.
    N = fr(WD.dur - start); F = lambda t: max(0, min(N, fr(t - start))); els = []; cur = 0; c0_first = None
    for kind, a, b, x in spec:
        f0 = cur; f1 = N if b is None else F(b)
        if f1 <= f0: notes.append(f"{kind} {getattr(x, 'name', '')} has no room ({a} to {b}) and is skipped"); continue
        if kind == "clip":
            t_in, n = x.fit(f1 - f0)
            if n < f1 - f0: notes.append(f"{x.name} can play {n/FPS:.2f} s of a {(f1 - f0)/FPS:.2f} s slot: the next picture comes in {(f1 - f0 - n)/FPS:.2f} s early (never slowed or held)"); f1 = f0 + n
            els.append(dict(kind="clip", f0=f0, f1=f1, use=x, t_in=t_in))
        elif kind == "levels":
            els.append(dict(kind="levels", f0=f0, f1=f1, lands=tuple(max(0.02, (F(t) - f0)/FPS) for t in x["lands"])))
        else:
            c0 = c0_first if x.get("same_card") else f0; c0_first = c0 if c0_first is None else c0_first
            ev = []
            for t, s in x["events"]:
                k = c0 if t in (None, 0.0) else (c0 + fr(LIGHT) if t == "light" else F(t)); ev.append((k, s))
            wins = []
            for wa, wb, use in x["wins"]:
                w0 = max(f0, c0 + fr(WIN_IN) if wa == "card" else F(wa)); w1 = f1 if wb is None else min(f1, F(wb))
                if w1 <= w0: continue
                t_in, n = use.fit(w1 - w0)
                if n < w1 - w0: notes.append(f"{use.name} can play {n/FPS:.2f} s of a {(w1 - w0)/FPS:.2f} s window slot: the window leaves when it ends (never slowed or held)")
                wins.append(dict(f0=w0, f1=w0 + n, use=use, t_in=t_in, slot_end=w1))
            for i, w in enumerate(wins):
                w["enter"] = i == 0 or wins[i - 1]["f1"] < w["f0"]
                w["exit"] = w["f1"] < f1 and not (i + 1 < len(wins) and wins[i + 1]["f0"] == w["f1"])
            els.append(dict(kind="series", f0=f0, f1=f1, c0=c0, events=ev, wins=wins))
        cur = f1
    assert els and els[0]["f0"] == 0 and els[-1]["f1"] == N and all(a["f1"] == b["f0"] for a, b in zip(els, els[1:])), "the pictures do not cover every frame"
    uses = [e["use"] for e in els if e["kind"] == "clip"] + [w["use"] for e in els if e["kind"] == "series" for w in e["wins"]]
    return dict(pid=pid, N=N, start=start, els=els, cues=q.log, notes=notes, uses=uses, q=q)

def describe(P):
    """The cue list as built, for the log, the .cues.json and the contact sheet."""
    rows = []; s0 = P["start"]; tl = lambda f: f/FPS
    cue_at = {fr(c["t"] - s0): c for c in P["cues"]}
    WDw = P["q"].W.w
    def cue_words(f):
        """the cue that lands on this frame, else the words being said then"""
        c = min((c for c in P["cues"] if c["edge"] == "t0"), key=lambda c: abs(fr(c["t"] - s0) - f))
        if abs(fr(c["t"] - s0) - f) <= 1: return c["heard"]
        t = f/FPS + s0; now = [w["w"].strip() for w in WDw if w["t1"] > t and w["t0"] < t + 0.8]
        if f > 0 and now: return ("(no cue; he is saying) " if WDw[0]["t0"] < t else "") + " ".join(now)
        return None
    for e in P["els"]:
        if e["kind"] == "clip":
            x = e["use"]; rows.append(dict(t=tl(e["f0"]), end=tl(e["f1"]), words=cue_words(e["f0"]) or "(segment start)", shows=f"FULL SCREEN: {x.what}", src=x.still or x.path, t_in=round(e["t_in"], 2), t_out=round(e["t_in"] + (e["f1"] - e["f0"])/FPS, 2), grade=x.graded, label="inside the clip" if x.own_label else None))
        if e["kind"] == "levels":
            rows.append(dict(t=tl(e["f0"]), end=tl(e["f1"]), words=cue_words(e["f0"]), shows="THREE-LEVELS CARD comes in"))
            for i, l in enumerate(e["lands"]): rows.append(dict(t=tl(e["f0"]) + l, words=cue_words(e["f0"] + fr(l)), shows=f"tile {i + 1} lands: {C.LEVELS[i][0]}: {C.LEVELS[i][1]}", settle=0.9))
        if e["kind"] == "series":
            for k, s in e["events"]:
                if k < e["f0"] - 1 or k >= e["f1"]: continue
                d = "ticks on " + ", ".join(f"row {i + 1}" for i in s["done"]) if s["done"] else "no ticks"
                l = f"row {s['lit'] + 1} lit" + (f" with the tag \"{s['tag']}\"" if s["tag"] else "") if s["lit"] is not None else "no row lit"
                rows.append(dict(t=tl(k), words=cue_words(k) or ("(rows have landed)" if k == e["c0"] + fr(LIGHT) else "(card)"), shows=f"THREE-PART CARD: {l}; {d}", settle=1.2 if k == e["c0"] else 0.5))
            if e["f0"] > e["c0"] and not any(e["f0"] <= k < e["f1"] for k, _ in e["events"]):
                rows.append(dict(t=tl(e["f0"]), end=tl(e["f1"]), words=cue_words(e["f0"]) or "(the demo has finished)", shows="THREE-PART CARD comes back, settled, no window (room for YouTube's end screen)", settle=1.0))
            for w in e["wins"]:
                x = w["use"]; rows.append(dict(t=tl(w["f0"]), end=tl(w["f1"]), words=cue_words(w["f0"]) or "(with the card)", shows=f"WINDOW: {x.what}" + (", AI-GENERATED chip " + ("top right" if x.chip == "rt" else "bottom right") if x.ai else ""),
                                               src=x.still or x.path, t_in=round(w["t_in"], 2), t_out=round(w["t_in"] + (w["f1"] - w["f0"])/FPS, 2), grade=x.graded, leaves_early=w["f1"] < w["slot_end"]))
    rows.sort(key=lambda r: r["t"]); return rows

# ------------------------------------------------------------------ render
def writer(path):
    return subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
def series_frame(e, k, readers):
    t = (k - e["c0"])/FPS; ev = [x for x in e["events"] if x[0] <= k]; kc, cur = ev[-1]
    im = series_rows(t, cur); p = B.ease((k - kc)/FPS, STATE) if len(ev) > 1 else 1.0
    if p < 1: im = Image.blend(series_rows(t, ev[-2][1]), im, p)
    for i, w in enumerate(e["wins"]):
        if not (w["f0"] <= k < w["f1"]): continue
        if id(w) not in readers: readers[id(w)] = w["use"].frames(w["t_in"], w["f1"] - w["f0"], (WW, WH))
        pic = next(readers[id(w)]); qi = B.ease((k - w["f0"] + 1)/FPS, WIN_IN) if w["enter"] else 1.0
        qo = B.ease((w["f1"] - k)/FPS, WIN_OUT) if w["exit"] else 1.0
        im = window(im, pic, min(qi, qo), (1 - qi)*40, w["use"].ai, w["use"].chip)
    return im
def frames(P):
    readers = {}
    for e in P["els"]:
        if e["kind"] == "clip": rd = e["use"].frames(e["t_in"], e["f1"] - e["f0"])
        for k in range(e["f0"], e["f1"]):
            if e["kind"] == "clip": yield next(rd)
            elif e["kind"] == "levels": yield C.levels_card((k - e["f0"])/FPS, e["lands"])
            else: yield series_frame(e, k, readers)
def busy():
    out = subprocess.run("ps -Ao pcpu,command | grep -E 'ffmpeg|whisper|render\\.py|gate\\.py|qc_style' | grep -v -E 'grep|Renderer'", shell=True, capture_output=True, text=True).stdout
    enc = [l for l in out.splitlines() if "libx264" in l or "whisper" in l or "render.py" in l or "gate.py" in l or "qc_style" in l]
    return len(enc), out
def render(pid, words, out, opt):
    WD = Words(words); print(f"{pid}: {words}: {len(WD.w)} words, {WD.dur:.2f} s", flush=True)
    P = program(pid, WD, opt); rows = describe(P)
    for n in P["notes"]: print("  NOTE", n)
    dupcheck(pid, P["uses"], opt)
    for r in rows:
        print(f"  {r['t']:6.2f}  \"{r['words']}\"  ->  {r['shows']}" + (f"  [{os.path.basename(r['src'])} {r['t_in']} to {r['t_out']} s" + (", graded" if r.get("grade") else "") + "]" if r.get("src") else "") + ("  LEAVES EARLY" if r.get("leaves_early") else ""))
    json.dump(dict(pickup=pid, words=os.path.abspath(words), duration=P["N"]/FPS, frames=P["N"], start_in_words_file=P["start"], full_open=opt["full_open"], cues=P["cues"], built=rows, notes=P["notes"]),
              open(out + ".cues.json", "w"), indent=1)
    if opt["dry"]: return P, rows
    while True:                                            # machine cap: never more than two video builds at once, across all sessions
        n, _ = busy()
        if n < 2: break
        print(f"  {n} builds are running; waiting", flush=True); time.sleep(20)
    tmp = out + ".v.mp4" if opt["audio"] else out; e = writer(tmp); n = 0
    for im in frames(P): e.stdin.write(im.tobytes()); n += 1
    e.stdin.close(); assert e.wait() == 0 and n == P["N"], (n, P["N"])
    if opt["audio"]:                                       # the voice as recorded, cut at the same point; the film's voice chain is the assembler's job
        subprocess.run([FF, "-v", "error", "-y", "-i", tmp, "-ss", f"{P['start']:.5f}", "-t", f"{P['N']/FPS:.5f}", "-i", opt["audio"], "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True); os.remove(tmp)
    print(f"built {out}: {P['N']} frames, {P['N']/FPS:.3f} s", flush=True)
    return P, rows

# ------------------------------------------------------------------ contact sheet: one frame per cue, at cue + 0.4 s
def grab(path, t, w=640, h=360):
    b = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:{h}:in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (w, h), b) if len(b) == w*h*3 else Image.new("RGB", (w, h), (90, 0, 0))
def sheet(pid, words, out, path, opt):
    cj = load_json(out + ".cues.json"); D = cj["duration"]; tiles = [("presenter, look D (the grades are judged against this)", grab(PRESENTER, 12.0))]
    for r in cj["built"]:
        t = min(D - 0.05, r["t"] + 0.4); tiles.append((f"{r['t']:.2f}+0.4 \"{r['words']}\" | {r['shows']}", grab(out, t)))
        if r.get("settle"): t2 = min(D - 0.05, r["t"] + 0.4 + r["settle"]); tiles.append((f"  ...settled, {t2:.2f} s", grab(out, t2)))
    tiles.append((f"last frame, {D:.2f} s", grab(out, D - 0.04)))
    cols = 3; w, h, lab = 640, 360, 44; S = Image.new("RGB", (cols*w, ((len(tiles) + cols - 1)//cols)*(h + lab)), (10, 14, 22)); d = ImageDraw.Draw(S); f = B.font(15, False)
    for i, (s, im) in enumerate(tiles):
        x, y = (i % cols)*w, (i//cols)*(h + lab); S.paste(im, (x, y + lab))
        for j, ln in enumerate(B.wrap(s, f, w - 12)[:2]): d.text((x + 6, y + 3 + j*19), ln, font=f, fill=(255, 255, 120))
    S.save(path, quality=90); print("sheet ->", path, len(tiles), "tiles")

# ------------------------------------------------------------------ placeholder word files from the old (unusable) recording
def placeholders():
    ws = load_json(OLD_TRANSCRIPT)["words"]; out = f"{W}/round3/pickups"; os.makedirs(out, exist_ok=True)
    fix = {"megamower.": ["mega", "baller."], "bower.": ["baller."]}                       # that transcript's mishearings of "mega baller" and "baller"
    def take(spans):
        """spans [(a, b)] of the old file, laid end to end from 0.15 s, 0.35 s between two spans"""
        res = []; at = 0.15
        for a, b in spans:
            sel = [w for w in ws if a - 0.01 <= w["t0"] and w["t1"] <= b + 0.01]; off = at - sel[0]["t0"]
            for w in sel:
                parts = fix.get(w["w"].strip(), [w["w"].strip()]); step = (w["t1"] - w["t0"])/len(parts)
                for i, p in enumerate(parts): res.append(dict(w=p, t0=round(w["t0"] + off + i*step, 3), t1=round(w["t0"] + off + (i + 1)*step, 3)))
            at = res[-1]["t1"] + 0.35
        return dict(duration=round(res[-1]["t1"] + 0.35, 3), words=res, note="PLACEHOLDER timings from the old, unusable recording (pickups_all_takes.transcript.json), last complete take; for proving the builder only")
    T = {"P1": [(69.7, 88.72)], "P2": [(189.08, 211.06)], "P3": [(283.1, 285.3), (225.06, 255.0)], "P4": [(303.0, 335.8)], "P2_fullopen": [(177.1, 211.06)]}
    for k, sp in T.items():
        d = take(sp); json.dump(d, open(f"{out}/placeholder_words_{k}.json", "w"), indent=1); print(k, d["duration"], "s:", " ".join(w["w"] for w in d["words"]))

def selftest():
    """The settled card here against cards20.series_card (the code behind the stills Dan approved): the rows must be the same pixels."""
    pic = G.clip_frame(f"{W}/stock/pexels-8942658-camera-focus-of-colorful-beverages.mp4", 3.0)
    for lit, tag, done, ai in ((1, "Next Video", (0,), False), (2, "Next Video", (0, 1), True), (0, "Last Video", (), False)):
        a = C.series_card(6.0, lit, tag, done=done, window=pic, ai=ai)
        b = window(series_rows(6.0, st(lit, tag, done)), ImageOps.fit(pic, (WW, WH)), 1.0, 0, ai, "rt")
        d = np.abs(np.asarray(a).astype(int) - np.asarray(b).astype(int)); print(f"lit {lit} tag {tag} done {done} ai {ai}: largest pixel difference {d.max()} (rows {d[:, :980].max()}, window {d[:, 980:].max()})")
        assert d.max() == 0, "the copied card has drifted from cards20.series_card"
    print("selftest passed: settled frames are identical to cards20.series_card")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"): print(__doc__); sys.exit(0)
    def flag(name, val=False):
        if name not in a: return None if val else False
        i = a.index(name); v = a[i + 1] if val else True; del a[i:i + (2 if val else 1)]; return v
    opt = dict(audio=flag("--audio", True), sheet=flag("--sheet", True), full_open=flag("--full-open"), allow_dup=flag("--allow-dup"), dry=flag("--dry"),
               j1=flag("--j1", True) or os.environ.get("RO20_J1", f"{W}/round3/motion/J1-t2.mp4"), j1_in=float(flag("--j1-in", True) or 4.0), cut=flag("--cut", True))
    s = flag("--start", True); opt["start"] = float(s) if s is not None else None
    if a[0] == "placeholders": placeholders()
    elif a[0] == "selftest": selftest()
    elif a[0] == "sheet": sheet(a[1], a[2], a[3], a[4], opt)
    else:
        assert a[0] in VIDEO and len(a) == 3, __doc__
        render(a[0], a[1], a[2], opt)
        if opt["sheet"] and not opt["dry"]: sheet(a[0], a[1], a[2], opt["sheet"], opt)
