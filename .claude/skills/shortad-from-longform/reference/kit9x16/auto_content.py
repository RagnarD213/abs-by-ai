#!/usr/bin/env python3
"""WRITE content.json FROM THE EDITOR'S MASTER, with no editing session.

content.json is the one sheet the kit was told by hand: WHAT graphic appears WHEN (beat kind, times, bullet text,
which picture, real/AI label). This script derives it from what we already have -- the editor's finished 16:9
master, Dan's raw roll(s) and our own asset libraries -- by measurement, and escalates whatever it is not sure of.

  python3 auto_content.py --build B --master his.mp4 --words m.whisper.json [--ai gemini|none] [--ledger L]

Needs (from the edit recovery, kit_recover.py / skill Step 1): B/auto/frames.npz (auto_measure.py), the master.
Writes: B/content.json, B/assets.py (the media map), B/assets_auto/ (portrait crops lifted from the master),
        B/auto_content_report.json (every entry with its evidence and confidence, every escalation).
Exit 0 = complete, 3 = escalations (the sheet is written but the job goes to the normal /shortad-from-longform path).

How (no model in the normal case):
 1. WHERE: per frame, how much of the master agrees with Dan's graded raw picture (auto_measure.py). Talk agrees
    ~98 %, an insert ~15 %, a bullets window has its text half dead and Dan's half alive. Runs -> spans; hard cuts
    (isolated scene-change spikes) split an insert into its shots; his flash transitions (a burst of spikes) put
    the boundary at the burst's centre.
 2. KIND: panel tokens (measurements.json: field, olive card) + Apple Vision text on the span's frames.
    Text on olive with no picture -> title; text beside live Dan -> window; a picture -> step 4 decides card/bleed.
 3. WORDS: Apple Vision (vision_ocr.swift), read on several frames of the span; a line counts only when two
    frames agree. Cross-checked against the transcript (graphics paraphrase the spoken line). "Al" -> "AI".
 4. PICTURES: ORB features + RANSAC homography against the libraries in auto_sources.json. A matched still is used
    CLEAN (bleed if it is portrait or >= 1440 tall, else card); its label comes from the library it lives in, and
    must agree with the label the editor burned into the master. Motion is lifted from the master into the olive
    card (skill Step 5 rule 3). A physique still with no provenance escalates.
 5. OVERLAYS: text read over live Dan in the lower frame -> a lower third, or the CTA pill when it reads like one;
    their in/out frames from the cell agreement under the text box.
"""
import argparse
import difflib
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_calls  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")
OCR_BIN = os.path.expanduser("~/.cache/kit9x16/vision_ocr")
OCR_SRC = os.path.join(HERE, "vision_ocr.swift")
CACHE = os.path.expanduser("~/.cache/kit9x16")

# ---- calibrated on Ad 10 (AV-07) and Ad 1 (the approved vertical), 2026-09-28. See README "auto_content".
T_TALK = 0.50          # whole-frame cell agreement at/above which Dan's graded raw picture is on screen
T_INSERT = 0.45        # below which the editor covered him
WIN_DEAD, WIN_LIVE = 0.25, 0.75   # a window: one side's agreement below DEAD, the other's above LIVE
CUT_SPIKE = 12.0       # scene-change score (mean |d| on 64x36 grey) of a hard cut
MIN_SHOT = 6           # frames: shorter runs are a flash or a transition, absorbed
OCR_EVERY = 5          # frames between Vision reads
LT_TOP = 0.55          # an overlay's text box starts below this fraction of the frame height
MATCH_MIN_INLIERS = 25
OLIVE = np.array([91, 97, 57], np.float32)
REAL_RX = re.compile(r"real\s+picture|not\s+a[il]\W*generated", re.I)
AI_RX = re.compile(r"^\W*a[il]\W*generated\W*$", re.I)
CTA_RX = re.compile(r"image\s+of\s+yourself|with\s+abs|tap\s+the\s+button", re.I)
NAME_AI = re.compile(r"(^|[^a-z])(ai|goal|generated|gag|veo|kling|seedream|flux)([^a-z]|$)", re.I)
NAME_REAL = re.compile(r"before|original|photoshoot|photo-shoot|shoot|photo-\d", re.I)


# ============================================================================ small helpers
def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def fix_ocr(s):
    s = s.replace("Al-", "AI-").replace("-Al", "-AI").replace("’", "'")
    s = re.sub(r"\bAl\b", "AI", s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("'", "")).strip()


def ratio(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def ensure_ocr():
    if not os.path.exists(OCR_BIN) or os.path.getmtime(OCR_BIN) < os.path.getmtime(OCR_SRC):
        os.makedirs(CACHE, exist_ok=True)
        run(["swiftc", "-O", OCR_SRC, "-o", OCR_BIN])


def ocr(paths):
    ensure_ocr()
    out = {}
    for i in range(0, len(paths), 200):
        r = subprocess.run([OCR_BIN] + paths[i:i + 200], capture_output=True, text=True, check=True)
        for line in r.stdout.splitlines():
            d = json.loads(line)
            out[d["image"]] = [dict(text=fix_ocr(x["text"]), box=x["box"]) for x in d["lines"] if x["text"].strip()]
    return out


def load_words(path):
    d = json.load(open(path))
    W = []
    if isinstance(d, dict) and "segments" in d:
        for s in d["segments"]:
            for w in s.get("words", []):
                if w["word"].strip():
                    W.append((w["word"].strip(), float(w["start"]), float(w["end"])))
    else:
        for w in d:
            W.append((w.get("w") or w.get("word", "").strip(), float(w.get("t", w.get("start"))), float(w.get("e", w.get("end")))))
    return W


def spoken(W, t0, t1):
    return " ".join(w for w, a, b in W if b >= t0 and a <= t1)


def best_spoken_match(text, W, t0, t1, pad=4.0):
    """How well a graphic's line matches what is said around it: best ratio over word windows of similar length."""
    ws = [w for w, a, b in W if b >= t0 - pad and a <= t1 + pad]
    n = max(1, len(norm(text).split()))
    best, where = 0.0, ""
    for L in range(max(1, n - 2), n + 4):
        for i in range(0, max(1, len(ws) - L + 1)):
            cand = " ".join(ws[i:i + L])
            r = ratio(text, cand)
            if r > best:
                best, where = r, cand
    return round(best, 3), where


def repair_with_speech(text, W, t0, t1):
    """Restore apostrophes Vision drops ("don t") from the transcript's own spelling."""
    words = {norm(w).replace(" ", ""): w.strip(",.?!") for w, a, b in W if b >= t0 - 6 and a <= t1 + 6 and "'" in w}
    def fix(m):
        key = (m.group(1) + m.group(2)).lower()
        return words.get(key, m.group(0))
    text = re.sub(r"\b(\w+) (t|s|re|ve|ll|d|m)\b", fix, text)
    hy = {w.lower().strip(",.?!").replace("-", " "): w.strip(",.?!") for w, a, b in W if b >= t0 - 6 and a <= t1 + 6 and "-" in w}
    for plain, hyph in hy.items():
        text = re.sub(r"\b" + re.escape(plain) + r"\b", hyph, text, flags=re.I)
    return text


def sentence_case(s):
    if s.isupper():
        s = s.lower()
        s = s[0].upper() + s[1:]
        s = re.sub(r"\bi\b", "I", s)
        s = re.sub(r"\bi'm\b", "I'm", s)
        s = re.sub(r"\bai\b", "AI", s)
    return s


def probe_wh(path):
    o = subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x",
                        path], capture_output=True, text=True).stdout.strip().split("\n")[0]
    try:
        w, h = (int(x) for x in o.split("x")[:2])
        return w, h
    except Exception:
        im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return (im.shape[1], im.shape[0]) if im is not None else (0, 0)


# ============================================================================ 1. WHERE
def frame_states(D):
    frac, cells = D["frac"], D["cells"]
    left = (cells[:, :, 0:7] > 0.5).mean(axis=(1, 2))
    right = (cells[:, :, 9:16] > 0.5).mean(axis=(1, 2))
    st = np.full(len(frac), "talk", dtype=object)
    st[frac < T_INSERT] = "insert"
    st[(frac >= T_INSERT) & (frac < T_TALK)] = "talk?"
    winR = (left < WIN_DEAD) & (right > WIN_LIVE)
    winL = (right < WIN_DEAD) & (left > WIN_LIVE)
    st[winR] = "window"
    st[winL] = "windowL"
    # "talk?" (between the two thresholds) joins whichever neighbour it sits next to
    for n in range(len(st)):
        if st[n] == "talk?":
            st[n] = st[n - 1] if n else "talk"
    return st, left, right


def runs_of(st):
    out, s = [], 0
    for n in range(1, len(st) + 1):
        if n == len(st) or st[n] != st[s]:
            out.append([st[s], s, n])
            s = n
    return out


def absorb_short(runs, minf=MIN_SHOT):
    changed = True
    while changed and len(runs) > 1:
        changed = False
        for i, r in enumerate(runs):
            if r[2] - r[1] < minf:
                j = i - 1 if i > 0 else i + 1
                if i > 0 and i + 1 < len(runs) and (runs[i + 1][2] - runs[i + 1][1]) > (runs[i - 1][2] - runs[i - 1][1]) \
                        and runs[i + 1][0] == r[0]:
                    j = i + 1
                if j < i:
                    runs[j][2] = r[2]
                else:
                    runs[j][1] = r[1]
                del runs[i]
                changed = True
                break
        # merge equal neighbours
        m = [runs[0]]
        for r in runs[1:]:
            if r[0] == m[-1][0]:
                m[-1][2] = r[2]
            else:
                m.append(r)
        runs = m
    return runs


def bursts(cut, thr=CUT_SPIKE):
    """His flash transitions: >= 3 spikes within 12 frames -> (first, last, centre) frame."""
    idx = np.where(cut >= thr)[0]
    out, cur = [], []
    for n in idx:
        if cur and n - cur[-1] > 4:
            if len(cur) >= 3:
                out.append((cur[0], cur[-1]))
            cur = []
        cur.append(n)
    if len(cur) >= 3:
        out.append((cur[0], cur[-1]))
    return [(a, b, (a + b) // 2) for a, b in out]


def isolated_spikes(cut, lo, hi, thr=CUT_SPIKE):
    out = []
    for n in range(lo + 1, hi):
        c = cut[n]
        if c < thr:
            continue
        nb = [cut[m] for m in (n - 2, n - 1, n + 1, n + 2) if lo <= m < hi and m != n]
        if not nb or c >= 2.5 * max(nb):
            out.append(n)
    return out


def snap_boundary(n, cut, B, lo=8):
    for a, b, c in B:
        if a - lo <= n <= b + lo:
            return c, "flash-burst centre"
    win = range(max(1, n - 3), min(len(cut), n + 4))
    m = max(win, key=lambda k: cut[k])
    return (m, "hard cut") if cut[m] >= CUT_SPIKE else (n, "agreement edge")


# ============================================================================ 4. PICTURES
def name_prov(path):
    b = os.path.basename(path)
    if NAME_AI.search(b.replace("_", " ").replace("-", " ")):
        return "ai"
    if NAME_REAL.search(b):
        return "real"
    return None


class Library:
    def __init__(self, sources_path):
        S = json.load(open(sources_path))
        self.orb = cv2.ORB_create(nfeatures=1500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        files = []
        for si, src in enumerate(S["sources"]):
            d = src["dir"]
            if not os.path.isdir(d):
                continue
            it = [os.path.join(d, f) for f in os.listdir(d)] if src.get("top_only") else \
                [os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs]
            for p in sorted(it):
                if not os.path.isfile(p) or any(x in p for x in S["exclude_substrings"]) or os.path.basename(p).startswith("."):
                    continue
                ext = os.path.splitext(p)[1].lower()
                typ = "img" if ext in S["still_ext"] else "vid" if ext in S["video_ext"] else None
                if typ:
                    prov = src["prov"]
                    if prov == "by-name":
                        prov = name_prov(p)
                    files.append((p, typ, prov, si))
        self.files = files
        sig = hashlib.md5(json.dumps([(p, os.path.getmtime(p), si) for p, _, _, si in files]).encode()).hexdigest()[:12]
        self.cache = os.path.join(CACHE, f"libindex_{sig}.npz")
        self._load()

    def _feat(self, img, maxside=1000):
        h, w = img.shape[:2]
        s = maxside / max(h, w)
        if s < 1:
            img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
        kp, des = self.orb.detectAndCompute(g, None)
        pts = np.float32([k.pt for k in kp]) if kp else np.zeros((0, 2), np.float32)
        return pts, des

    def _load(self):
        if os.path.exists(self.cache):
            z = np.load(self.cache, allow_pickle=True)
            self.entries = list(z["entries"])
            return
        os.makedirs(CACHE, exist_ok=True)
        entries = []
        for p, typ, prov, si in self.files:
            if typ == "img":
                im = cv2.imread(p, cv2.IMREAD_COLOR)
                if im is None:
                    continue
                pts, des = self._feat(im)
                if des is not None:
                    entries.append(dict(path=p, typ=typ, prov=prov, si=si, t=0.0, pts=pts, des=des, w=im.shape[1], h=im.shape[0]))
            else:
                cap = cv2.VideoCapture(p)
                fps = cap.get(cv2.CAP_PROP_FPS) or 30
                n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
                step = max(1, int(round(fps)))
                for f in range(0, min(n, int(fps * 90)), step):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
                    ok, im = cap.read()
                    if not ok:
                        break
                    pts, des = self._feat(im)
                    if des is not None:
                        entries.append(dict(path=p, typ=typ, prov=prov, si=si, t=f / fps, pts=pts, des=des, w=im.shape[1], h=im.shape[0]))
                cap.release()
        np.savez(self.cache, entries=np.array(entries, dtype=object))
        self.entries = entries

    @staticmethod
    def _coverage(H, e, qsize):
        """Fraction of the query picture covered by the matched library picture (its corners projected back).
        ~1 = the picture IS the library file; well under 1 = it sits inside something else (a phone's app screen)."""
        try:
            Hi = np.linalg.inv(H)
        except np.linalg.LinAlgError:
            return 0.0
        sc = min(1.0, 1000 / max(e["w"], e["h"]))
        w, h = e["w"] * sc, e["h"] * sc
        quad = cv2.perspectiveTransform(np.float32([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]]), Hi).reshape(-1, 2)
        qw, qh = qsize
        rect = np.float32([[0, 0], [qw, 0], [qw, qh], [0, qh]])
        try:
            area, _ = cv2.intersectConvexConvex(quad.astype(np.float32), rect)
        except cv2.error:
            return 0.0
        return float(max(0.0, area) / (qw * qh))

    def match(self, img):
        qp, qd = self._feat(img)
        hq, wq = img.shape[:2]
        sq = min(1.0, 1000 / max(hq, wq))
        qsize = (wq * sq, hq * sq)
        if qd is None or len(qp) < 20:
            return []
        res = []
        for e in self.entries:
            if e["des"] is None or len(e["des"]) < 20:
                continue
            m = self.bf.knnMatch(qd, e["des"], k=2)
            good = [a for a, b in (x for x in m if len(x) == 2) if a.distance < 0.75 * b.distance]
            if len(good) < 12:
                continue
            src = np.float32([qp[g.queryIdx] for g in good]); dst = np.float32([e["pts"][g.trainIdx] for g in good])
            H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 6.0)
            inl = int(mask.sum()) if mask is not None else 0
            cov = self._coverage(H, e, qsize) if H is not None and inl >= 12 else 0.0
            res.append((inl, e["path"], e["typ"], e["prov"], e["t"], e["w"], e["h"], e.get("si", 0), cov))
        res.sort(key=lambda r: -r[0])
        # the same picture often lives in two files (the library's and a reference-ad copy, a jpg and a png): among
        # matches within 10 % of the best, the LARGEST file wins (the clean full-resolution original), then the
        # earlier source in auto_sources.json
        if res:
            top = res[0][0]
            tied = [r for r in res if r[0] >= 0.9 * top]
            rest = [r for r in res if r[0] < 0.9 * top]
            tied.sort(key=lambda r: (-(r[5] * r[6]), r[7]))
            provs = {r[3] for r in tied if r[3] in ("real", "ai")} if top >= MATCH_MIN_INLIERS else set()
            if len(provs) > 1:                       # two copies of one picture disagree on real vs AI
                tied = [r[:3] + ("conflict",) + r[4:] for r in tied]
            elif provs and tied[0][3] not in provs:  # a copy with no provenance inherits its twin's
                tied = [r[:3] + (next(iter(provs)),) + r[4:] for r in tied]
            res = tied + rest
        # one row per file, best frame
        seen, out = set(), []
        for r in res:
            if r[1] not in seen:
                seen.add(r[1]); out.append(r)
        return out[:5]


# ============================================================================ frames of the master
def grab(master, t, out, w=1920):
    if not os.path.exists(out):
        run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.4f}", "-i", master, "-frames:v", "1",
             "-vf", f"scale={w}:-2:in_color_matrix=bt709:in_range=tv", out])
    return out


def ocr_samples(master, A, N, fps):
    """Vision on every OCR_EVERY-th frame at 1280x720 -> {n: [lines]} (cached)."""
    cp = os.path.join(A, "ocr.json")
    if os.path.exists(cp):
        return {int(k): v for k, v in json.load(open(cp)).items()}
    d = os.path.join(A, "ocr_frames")
    os.makedirs(d, exist_ok=True)
    if not glob.glob(os.path.join(d, "*.jpg")):
        run([FF, "-nostdin", "-v", "error", "-y", "-i", master, "-an",
             "-vf", f"select='not(mod(n\\,{OCR_EVERY}))',scale=1280:720:in_color_matrix=bt709:in_range=tv",
             "-vsync", "0", "-q:v", "3", os.path.join(d, "%06d.jpg")])
    files = sorted(glob.glob(os.path.join(d, "*.jpg")))
    R = ocr(files)
    out = {}
    for i, f in enumerate(files):
        out[i * OCR_EVERY] = R.get(f, [])
    json.dump(out, open(cp, "w"))
    return out


def picture_bbox(img, text_boxes):
    """The picture inside his layout: not the dark field, not olive, not text. -> (x0, y0, x1, y1) or None."""
    h, w = img.shape[:2]
    s = 480 / w
    sm = cv2.resize(img, (480, int(h * s)), interpolation=cv2.INTER_AREA).astype(np.float32)
    rgb = sm[..., ::-1]
    field = rgb.max(axis=2) < 48
    olive = np.linalg.norm(rgb - OLIVE, axis=2) < 32
    m = (~field & ~olive).astype(np.uint8)
    for (x0, y0, x1, y1) in text_boxes:
        m[max(0, int(y0 * s) - 3):int(y1 * s) + 3, max(0, int(x0 * s) - 3):int(x1 * s) + 3] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n <= 1:
        return None, float(olive.mean()), 0.0, None
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    x, y, ww, hh, area = stats[i]
    frac = area / float(m.size)
    # the olive card's HOLE: everything inside the card's outline that is not olive (a phone's black bezel
    # included, which the picture mask drops as "field")
    hole = None
    if olive.mean() > 0.12:
        oc = cv2.morphologyEx(olive.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        k, lab2, st2, _ = cv2.connectedComponentsWithStats(oc)
        big = [j for j in range(1, k) if st2[j][cv2.CC_STAT_AREA] >= 0.01 * oc.size]
        if big:
            # the card outline is the union of its olive pieces: a phone as tall as the card splits it in two
            cx = min(st2[j][0] for j in big); cy = min(st2[j][1] for j in big)
            cx1 = max(st2[j][0] + st2[j][2] for j in big); cy1 = max(st2[j][1] + st2[j][3] for j in big)
            inner = (~olive[cy:cy1, cx:cx1]).astype(np.uint8)
            inner = cv2.morphologyEx(inner, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            k3, lab3, st3, _ = cv2.connectedComponentsWithStats(inner)
            if k3 > 1:
                q = 1 + int(np.argmax(st3[1:, cv2.CC_STAT_AREA]))
                hx, hy, hw, hh_ = st3[q][:4]
                hole = (int((cx + hx) / s), int((cy + hy) / s), int((cx + hx + hw) / s), int((cy + hy + hh_) / s))
    return (int(x / s), int(y / s), int((x + ww) / s), int((y + hh) / s)), float(olive.mean()), float(frac), hole


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--master", required=True)
    ap.add_argument("--words", required=True, help="his master's word timings (m.whisper.json)")
    ap.add_argument("--sources", default=os.path.join(HERE, "auto_sources.json"))
    ap.add_argument("--ai", default="none", help="leftover classifier: gemini | none")
    ap.add_argument("--ledger", help="AI call ledger (JSONL); default B/ai_ledger.jsonl")
    ap.add_argument("--out", help="default B/content.json")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    A = os.path.join(B, "auto")
    master = os.path.abspath(a.master)
    D = np.load(os.path.join(A, "frames.npz"))
    fps = float(D["fps"])
    N = len(D["frac"])
    dur = round(N / fps, 3)
    cut = D["cut"]
    W = load_words(a.words)
    AI = ai_calls.provider(a.ai, a.ledger or os.path.join(B, "ai_ledger.jsonl"))
    esc, rep_beats = [], []
    T = lambda n: float(round(float(n) / fps, 3))

    # ---- 1. spans
    st, left, right = frame_states(D)
    R = absorb_short(runs_of(list(st)))
    B_ = bursts(cut)
    O = ocr_samples(master, A, N, fps)
    frames_dir = os.path.join(A, "frames"); os.makedirs(frames_dir, exist_ok=True)

    # boundaries snapped to his cut / his flash centre
    for i in range(1, len(R)):
        n, how = snap_boundary(R[i][1], cut, B_)
        if R[i - 1][1] + MIN_SHOT <= n <= R[i][2] - MIN_SHOT:
            R[i - 1][2] = n; R[i][1] = n
        R[i].append(how)
    if R:
        R[0].append("start")

    def samples_in(n0, n1, pad=0):
        return [(n, O[n]) for n in sorted(O) if n0 + pad <= n < n1 - pad]

    def cell_mean(n, box, W_=1280, H_=720):
        x0, y0, x1, y1 = box
        j0, j1 = int(x0 / W_ * 16), max(int(x0 / W_ * 16) + 1, int(np.ceil(x1 / W_ * 16)))
        i0, i1 = int(y0 / H_ * 9), max(int(y0 / H_ * 9) + 1, int(np.ceil(y1 / H_ * 9)))
        return float(D["cells"][n, i0:i1, j0:j1].mean())

    lib = None
    beats, lts, ctas = [], [], []

    def lib_get():
        nonlocal lib
        if lib is None:
            lib = Library(a.sources)
        return lib

    media, prep = {}, []
    cta_top, cta_big = None, None

    # ---- 2-4. every non-talk run
    for run_ in R:
        kind, n0, n1 = run_[0], run_[1], run_[2]
        how0 = run_[3] if len(run_) > 3 else ""
        if kind == "talk":
            continue
        if kind in ("window", "windowL"):
            dead = slice(0, 7) if kind == "window" else slice(9, 16)
            S = samples_in(n0, n1)
            text_side = (lambda b: b[2] < 1280 * 0.55) if kind == "window" else (lambda b: b[0] > 1280 * 0.45)
            reads = []
            for n, lines in S:
                L = [l for l in lines if text_side(l["box"]) and cell_mean(n, l["box"]) < 0.5]
                reads.append((n, L))
            # the final state: the read with the most text in the last half, confirmed by another read
            tail = [r for r in reads if r[0] >= n0 + (n1 - n0) // 2] or reads
            best = max(tail, key=lambda r: sum(len(l["text"]) for l in r[1])) if tail else (n0, [])
            key = lambda L: [norm(l["text"]) for l in L]
            agree = sum(1 for r in reads if key(r[1]) == key(best[1]))
            lines = sorted(best[1], key=lambda l: l["box"][1])
            header, bullets = None, []
            hts = [l["box"][3] - l["box"][1] for l in lines]
            for l in lines:
                t_ = l["text"]
                glyph = bool(re.match(r"^[•▪■◾●\-–·]\s*", t_))
                clean = re.sub(r"^[•▪■◾●\-–·]\s*", "", t_)
                if not bullets and not glyph and (t_.isupper() or l["box"][1] < 150) and header is None:
                    header = sentence_case(clean) if clean.isupper() else clean
                    continue
                if glyph or not bullets:
                    bullets.append(clean)
                else:
                    prev_l = lines[lines.index(l) - 1]
                    gap = l["box"][1] - prev_l["box"][3]
                    if gap > 0.8 * (prev_l["box"][3] - prev_l["box"][1]):
                        bullets.append(clean)
                    else:
                        bullets[-1] = bullets[-1] + " " + clean
            bullets = [repair_with_speech(b, W, T(n0), T(n1)) for b in bullets]
            checks = [best_spoken_match(b, W, T(n0), T(n1)) for b in bullets]
            conf = "high" if agree >= 2 and bullets and min(c[0] for c in checks) >= 0.5 else "medium" if bullets else "low"
            ent = dict(kind="window", header=header, bullets=bullets, t0=T(n0), t1=T(n1))
            if kind == "windowL":
                ent["dan_side"] = "left"
            beats.append(ent)
            rep_beats.append(dict(entry=ent, confidence=conf, evidence=dict(
                frames=[n0, n1], boundary=how0, reads_agreeing=agree, read_frame=best[0],
                transcript_check=[dict(line=b, ratio=c[0], spoken=c[1]) for b, c in zip(bullets, checks)],
                left_agreement=round(float(left[n0:n1].mean()), 3), right_agreement=round(float(right[n0:n1].mean()), 3))))
            if not bullets:
                esc.append(dict(t0=T(n0), t1=T(n1), what="window with no readable bullets"))
            elif agree < 2 or min(c[0] for c in checks) < 0.3:
                esc.append(dict(t0=T(n0), t1=T(n1), what="window text not confirmed (reads disagree or no spoken match)",
                                bullets=bullets, checks=checks))
            continue

        # ---- an insert: split into his shots
        cuts = [n0] + isolated_spikes(cut, n0, n1) + [n1]
        for b0, b1, c in B_:
            if n0 + MIN_SHOT < c < n1 - MIN_SHOT and not any(abs(c - x) < MIN_SHOT for x in cuts):
                cuts.append(c)
        cuts = sorted(set(cuts))
        shots = [[cuts[i], cuts[i + 1]] for i in range(len(cuts) - 1)]
        merged = []
        for s in shots:
            if merged and s[1] - s[0] < MIN_SHOT:
                merged[-1][1] = s[1]
            elif not merged and s[1] - s[0] < MIN_SHOT and len(shots) > 1:
                shots[1][0] = s[0]
            else:
                merged.append(s)
        # a card's ENTRANCE (a short, fast-moving first shot straight out of talk: the phone zooming in blurred) is
        # not content: the beat starts when the picture has landed; the kit draws its own entrance
        if len(merged) > 1 and merged[0][1] - merged[0][0] < 15 and float(np.median(cut[merged[0][0] + 1:merged[0][1]])) > 5.0:
            merged = merged[1:]
        run_beats = []
        for s0, s1 in merged:
            beat, ev = describe_shot(master, A, frames_dir, D, O, W, s0, s1, fps, T, lambda: lib_get(), AI, esc, media, prep, B)
            if beat:
                beats.append(beat); run_beats.append((beat, ev))
                rep_beats.append(dict(entry=beat, confidence=ev.pop("confidence"), evidence=ev))
        # an APP DEMO stays in one layout: a clean still between phone shots of the same insert is a card too
        if any(ev_.get("phone") for _, ev_ in run_beats):
            for b_, ev_ in run_beats:
                if b_["kind"] == "bleed":
                    b_["kind"] = "card"; ev_["layout"] = "card: part of an app-demo sequence"

    # ---- 5. overlays over live Dan: lower thirds and the CTA pill
    ov = []
    for n in sorted(O):
        if st[n] not in ("talk",):
            continue
        L = [l for l in O[n] if l["box"][1] > 720 * LT_TOP and cell_mean(n, l["box"]) < 0.5]
        if L:
            L = sorted(L, key=lambda l: l["box"][1])
            ov.append((n, [l["text"] for l in L], [min(l["box"][0] for l in L), min(l["box"][1] for l in L),
                                                    max(l["box"][2] for l in L), max(l["box"][3] for l in L)]))
    # one overlay = consecutive reads whose text boxes overlap in height (a typewriter reveal reads "MyDaughte"
    # before "My Daughter Was Watching"; the text is not what ties the reads together, the place is)
    groups = []
    for n, lines, box in ov:
        txt = " / ".join(lines)
        if groups:
            g = groups[-1]
            ov_y = min(box[3], g["box"][3]) - max(box[1], g["box"][1])
            if n - g["n1"] <= 2 * OCR_EVERY and ov_y > 0.5 * min(box[3] - box[1], g["box"][3] - g["box"][1]):
                g["n1"] = n; g["reads"].append((n, txt, lines))
                g["box"] = [min(g["box"][0], box[0]), min(g["box"][1], box[1]), max(g["box"][2], box[2]), max(g["box"][3], box[3])]
                continue
        groups.append(dict(n0=n, n1=n, reads=[(n, txt, lines)], box=box))
    groups = [g for g in groups if g["n1"] - g["n0"] >= 2 * OCR_EVERY]      # a real overlay holds >= 10 frames
    for g in groups:
        texts = [r[1] for r in g["reads"]]
        L_ = max(len(norm(t)) for t in texts)
        full = [t for t in texts if len(norm(t)) >= 0.9 * L_]              # the revealed text, not a half-typed read
        mode = max(set(full), key=full.count)
        agree = texts.count(mode)
        lines = next(r[2] for r in g["reads"] if r[1] == mode)
        # in / out: walk from the reads to where the box stops disagreeing with Dan's raw picture
        a0, a1 = g["n0"], g["n1"]
        while a0 > 0 and cell_mean(a0 - 1, g["box"]) < 0.5 and st[a0 - 1] == "talk":
            a0 -= 1
        while a1 + 1 < N and cell_mean(a1 + 1, g["box"]) < 0.5 and st[a1 + 1] == "talk":
            a1 += 1
        is_cta = bool(CTA_RX.search(mode))
        ent = dict(t0=T(a0), t1=T(a1 + 1))
        conf = "high" if agree >= 2 else "low"
        if is_cta:
            ctas.append(ent)
            if len(lines) >= 2:
                cta_top, cta_big = cta_top or lines[0], cta_big or lines[-1]
        else:
            ent["lines"] = lines
            lts.append(ent)
        chk = best_spoken_match(mode, W, ent["t0"], ent["t1"])
        rep_beats.append(dict(entry=dict(kind="cta" if is_cta else "lower_third", **ent), confidence=conf,
                              evidence=dict(reads=len(texts), reads_agreeing=agree, box_1280=g["box"],
                                            transcript_check=dict(ratio=chk[0], spoken=chk[1]))))
        if agree < 2:
            esc.append(dict(t0=ent["t0"], t1=ent["t1"], what=f"{'CTA' if is_cta else 'lower third'} text read only once", text=mode))

    beats.sort(key=lambda b: b["t0"])
    # an insert ENTRANCE that ended up as its own beat (the blurred phone zooming in, < 0.5 s, fast) followed at once
    # by the landed picture: it is not content (the kit draws its own entrance)
    evs = {id(r["entry"]): r for r in rep_beats}
    keep = []
    for i, b_ in enumerate(beats):
        r_ = evs.get(id(b_))
        nxt = beats[i + 1] if i + 1 < len(beats) else None
        if b_["kind"] in ("card", "bleed") and b_["t1"] - b_["t0"] < 0.5 and r_ and r_["evidence"].get("motion", 0) > 5.0 \
                and nxt and abs(nxt["t0"] - b_["t1"]) < 0.05:
            if keep and abs(keep[-1]["t1"] - b_["t0"]) < 0.05:
                keep[-1]["t1"] = b_["t1"]              # out of another insert: that insert holds through it
                r_["dropped"] = "insert entrance animation, absorbed by the previous insert"
            else:
                r_["dropped"] = "insert entrance animation (out of talk)"
            media.pop(b_.get("media"), None)
            continue
        keep.append(b_)
    beats = keep
    kinds_seen = sorted({b["kind"] for b in beats})
    C = dict(
        source=f"auto_content.py from {os.path.basename(master)} (no editing session)",
        words=os.path.basename(a.words), dur=dur,
        cta_top=cta_top or "Get A FREE AI Image Of Yourself", cta_big=cta_big or "With Abs",
        no_caps_kinds=["cta", "stmt", "title", "window", "winmedia"],
        deviations=[
            ["all talking head", "Recovered from the raw roll with his picture EDL; his approved audio is untouched."],
            ["photos of Dan", "Where the library holds the clean original it replaces his frame (his burned label may cross the abs); the kit places its own label by measurement."],
            ["16:9 inserts", "His 16:9 motion inserts are shown in the olive card rather than upscaled to full-bleed 9:16."],
            ["captions", "Word-timed captions for muted feeds, suppressed under text plates and labelled pictures of Dan."],
        ],
        beats=beats, lower_thirds=sorted(lts, key=lambda x: x["t0"]), ctas=sorted(ctas, key=lambda x: x["t0"]),
    )
    out = a.out or os.path.join(B, "content.json")
    json.dump(C, open(out, "w"), indent=1)
    write_assets(B, master, media, prep)
    rep = dict(master=master, frames=N, fps=fps, beats=len(beats), lower_thirds=len(lts), ctas=len(ctas), kinds=kinds_seen,
               escalations=esc, complete=not esc, ai=AI.ledger.total(), entries=rep_beats,
               thresholds=dict(T_TALK=T_TALK, T_INSERT=T_INSERT, WIN_DEAD=WIN_DEAD, WIN_LIVE=WIN_LIVE, CUT_SPIKE=CUT_SPIKE,
                               MIN_SHOT=MIN_SHOT, OCR_EVERY=OCR_EVERY, MATCH_MIN_INLIERS=MATCH_MIN_INLIERS))
    json.dump(rep, open(os.path.join(B, "auto_content_report.json"), "w"), indent=1, default=str)
    print(f"auto_content: {len(beats)} beats ({', '.join(kinds_seen)}), {len(lts)} lower thirds, {len(ctas)} CTAs; "
          f"{len(esc)} escalation(s); AI {rep['ai']}")
    for e in esc:
        print("  ESCALATE", e)
    return 3 if esc else 0


def describe_shot(master, A, frames_dir, D, O, W, s0, s1, fps, T, lib_get, AI, esc, media, prep, B):
    """One insert shot -> a content beat (title / card / bleed) + its evidence."""
    samp = [(n, O[n]) for n in sorted(O) if s0 <= n < s1]
    all_text = [l for _, L in samp for l in L]
    burned = None
    if any(REAL_RX.search(l["text"]) for l in all_text):
        burned = "real"
    elif any(AI_RX.search(l["text"]) for l in all_text):
        burned = "ai"
    mid = s0 + int((s1 - s0) * 0.45)
    fp = grab(master, mid / fps, os.path.join(frames_dir, f"f{mid:06d}.png"))
    img = cv2.imread(fp)
    # the read nearest the middle, the text that is not a label chip
    near = min(samp, key=lambda x: abs(x[0] - mid)) if samp else (mid, [])
    text_lines = [l for l in near[1] if not REAL_RX.search(l["text"]) and not AI_RX.search(l["text"])]
    tb = [[v * 1.5 for v in l["box"]] for l in near[1]]                  # 1280 -> 1920
    bbox, olive_frac, pic_frac, hole = picture_bbox(img, tb)
    motion = float(np.median(D["cut"][s0 + 1:s1])) if s1 - s0 > 2 else 0.0
    words = sum(len(l["text"].split()) for l in text_lines)
    ev = dict(frames=[s0, s1], rep_frame=fp, olive=round(olive_frac, 3), picture_area=round(pic_frac, 3), motion=round(motion, 2),
              text=[l["text"] for l in text_lines], burned_label=burned)
    t0, t1 = T(s0), T(s1)

    # ---- a text plate (title)
    if words >= 3 and pic_frac < 0.03:
        lines = sorted(text_lines, key=lambda l: l["box"][1])
        hs = [l["box"][3] - l["box"][1] for l in lines]
        big = max(hs)
        caps = [l for l in lines if l["text"].isupper()]
        if caps and len(caps) < len(lines):            # his title card: CAPS headline, sentence-case sub
            head = [l["text"] for l in lines if l["text"].isupper()]
            sub = [l["text"] for l in lines if not l["text"].isupper()]
        else:
            head = [l["text"] for l, h in zip(lines, hs) if h >= 0.9 * big]
            sub = [l["text"] for l, h in zip(lines, hs) if h < 0.9 * big]
        # agreement across reads of the shot
        reads = [" ".join(l["text"] for l in L if not REAL_RX.search(l["text"])) for _, L in samp]
        full = " ".join(l["text"] for l in lines)
        agree = sum(1 for r in reads if norm(r) == norm(full))
        beat = dict(kind="title", headline=sentence_case(" ".join(head)), sub=" ".join(sub) or None, t0=t0, t1=t1)
        chk = best_spoken_match(full, W, t0, t1)
        ev.update(reads_agreeing=agree, transcript_check=dict(ratio=chk[0], spoken=chk[1]),
                  confidence="high" if agree >= 2 else "low")
        if agree < 2:
            esc.append(dict(t0=t0, t1=t1, what="title text not confirmed by a second read", text=full))
        return beat, ev

    # ---- a picture: find the clean original
    crop = img if bbox is None else img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    m = lib_get().match(crop) if crop.size else []
    ev["matches"] = [dict(file=r[1], inliers=r[0], typ=r[2], prov=r[3], t=round(r[4], 2), coverage=round(r[8], 3)) for r in m[:3]]
    top = m[0] if m and m[0][0] >= MATCH_MIN_INLIERS else None
    ui = [l["text"] for l in near[1] if not REAL_RX.search(l["text"]) and not AI_RX.search(l["text"])]
    tall = bbox is not None and (bbox[2] - bbox[0]) / max(1, bbox[3] - bbox[1]) < 0.75
    area = lambda b: max(1, (b[2] - b[0]) * (b[3] - b[1]))
    # a PHONE: the picture sits inside an app screen -- the card's hole is a tall shape clearly bigger than the
    # picture in it (the bezel and the app's own chrome), or the matched photo covers only part of the picture,
    # or nothing matches and it is a tall thing carrying UI text. A still that FILLS its hole is the photo itself.
    in_phone_hole = hole is not None and (hole[2] - hole[0]) / max(1, hole[3] - hole[1]) < 0.75 and \
        bbox is not None and area(bbox) < 0.8 * area(hole)
    phone = in_phone_hole or (tall and ((top is not None and top[8] < 0.6) or (top is None and len(ui) >= 1)))
    ev["hole"] = hole
    if phone and hole is not None:
        bbox = hole
    ev["phone"] = bool(phone)
    key = f"auto_{s0:05d}"
    beat = dict(t0=t0, t1=t1)
    prov = top[3] if top else None
    conf = "high"
    if prov == "conflict":
        esc.append(dict(t0=t0, t1=t1, what="two library copies of this picture disagree on real vs AI", files=[r[1] for r in m[:3]]))
        prov, conf = None, "low"
    if top and top[2] == "img" and not phone:
        w, h = top[5], top[6]
        beat["kind"] = "bleed" if (h > w or h >= 1440) else "card"
        media[key] = ("img", top[1], 0, 1.0, {"oy": 0.0})
        ev["source"] = "clean library still"
        label = prov if prov in ("real", "ai") else burned
        if prov in ("real", "ai") and burned and burned != prov:
            esc.append(dict(t0=t0, t1=t1, what=f"label conflict: library says {prov}, his burned label says {burned}", file=top[1]))
            conf = "low"
        if label is None:
            ans = AI.classify_picture(fp, "This is a frame of a fitness ad. Does the picture show a man's physique "
                                          "(bare torso/abs)? And is the picture a real photograph or AI-generated?",
                                      ["real_physique", "ai_physique", "real_other", "ai_other"])
            ev["ai_answer"] = ans
            if ans and ans.get("confidence", 0) >= 0.8 and ans["answer"].endswith("other"):
                label = "ai" if ans["answer"].startswith("ai") else None
            else:
                esc.append(dict(t0=t0, t1=t1, what="a picture with no provenance and no label (every physique picture needs exactly one)", file=top[1]))
                conf = "low"
        if label:
            beat["label_kind"] = label
            beat["caps"] = False
    else:
        beat["kind"] = "card"
        if phone:
            cx = (bbox[0] + bbox[2]) // 2
            x = int(min(max(cx - 304, 0), 1920 - 608))
            out = os.path.join("assets_auto", f"{key}.mp4")
            prep.append((out, t0, round(t1 - t0, 3), x))
            media[key] = ("vid", out, 0.0)
            ev["source"] = f"portrait crop of his master at x={x} (a phone)"
        else:
            media[key] = ("vid", master, t0)
            ev["source"] = "his master, lifted into the olive card"
        still = motion < 2.0
        ev["still"] = still
        if phone and top is not None and prov in ("real", "ai") and top[2] == "img":
            # the photo inside the app screen is a known picture of Dan: the kit's chip names it
            beat["label_kind"] = prov; beat["caps"] = False
            if burned and burned != prov:
                esc.append(dict(t0=t0, t1=t1, what=f"label conflict inside the phone: library {prov}, burned {burned}"))
                conf = "low"
            elif burned:
                beat.pop("label_kind")            # his own chip is already on this picture: never two
                ev["label"] = f"his burned {burned} label is carried in the lifted picture"
        elif burned:
            beat["caps"] = False
            ev["label"] = f"his burned {burned} label is carried in the lifted picture"
            if burned == "real" and still and not phone:
                esc.append(dict(t0=t0, t1=t1, what="a real physique still with no clean original: his burned label may cross the abs"))
                conf = "low"
        elif prov == "ai":
            beat["label_kind"] = "ai"; beat["caps"] = False
        elif prov is None:
            ans = AI.classify_picture(fp, "This is a frame of a fitness ad. Is the main picture AI-generated or a real "
                                          "photo/video? Does it show a man's bare torso/physique?",
                                      ["real_physique", "ai_physique", "real_other", "ai_other"])
            ev["ai_answer"] = ans
            if ans and ans.get("confidence", 0) >= 0.8:
                if ans["answer"].startswith("ai"):
                    beat["label_kind"] = "ai"; beat["caps"] = False
                elif ans["answer"] == "real_physique" and still:
                    esc.append(dict(t0=t0, t1=t1, what="a real physique still with no provenance"))
                    conf = "low"
            elif still and pic_can_be_dan(ev):
                esc.append(dict(t0=t0, t1=t1, what="an unmatched still with no label and no classifier answer"))
                conf = "low"
            else:
                conf = "medium"
    beat["media"] = key
    ev["confidence"] = conf
    ev["provenance"] = prov
    return beat, ev


def pic_can_be_dan(ev):
    return True


def write_assets(B, master, media, prep):
    os.makedirs(os.path.join(B, "assets_auto"), exist_ok=True)
    for out, t0, d, x in prep:
        p = os.path.join(B, out)
        if not os.path.exists(p):
            run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-t", f"{d:.4f}", "-i", master, "-an",
                 "-vf", f"crop=608:1080:{x}:0,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.25",
                 "-r", "30000/1001", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                 "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", p])
    with open(os.path.join(B, "assets.py"), "w") as f:
        f.write('#!/usr/bin/env python3\n"""Media map written by kit9x16/auto_content.py. Every entry cites its source in '
                'auto_content_report.json."""\n\n')
        f.write(f"MASTER = {master!r}\n\nMEDIA = {{\n")
        for k, v in media.items():
            vv = tuple(v)
            if vv[0] == "vid" and vv[1] == master:
                f.write(f"    {k!r}: ('vid', MASTER, {vv[2]!r}),\n")
            else:
                f.write(f"    {k!r}: {vv!r},\n")
        f.write("}\n")


if __name__ == "__main__":
    sys.exit(main())
