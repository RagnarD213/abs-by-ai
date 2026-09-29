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
FACE_BIN = os.path.expanduser("~/.cache/kit9x16/vision_face")
FACE_SRC = os.path.join(HERE, "vision_face.swift")
OCR_SRC = os.path.join(HERE, "vision_ocr.swift")
CACHE = os.path.expanduser("~/.cache/kit9x16")

# ---- calibrated on Ad 10 (AV-07) and Ad 1 (the approved vertical), 2026-09-28. See README "auto_content".
T_TALK = 0.50          # whole-frame cell agreement at/above which Dan's graded raw picture is on screen
T_INSERT = 0.45        # below which the editor covered him
WIN_DEAD, WIN_LIVE = 0.25, 0.75   # a window: one side's agreement below DEAD, the other's above LIVE
WIN_HEAD = 0.88                   # ... or Dan's head box on the live side matching at/above this (NCC)
WIN_SOFT = 0.20                   # ... or above SOFT for most of 15 frames (the window's own push)
CUT_SPIKE = 12.0       # scene-change score (mean |d| on 64x36 grey) of a hard cut
MIN_SHOT = 6           # frames: shorter runs are a flash or a transition, absorbed
OCR_EVERY = 5          # frames between Vision reads
LT_TOP = 0.55          # an overlay's text box starts below this fraction of the frame height
MATCH_MIN_INLIERS = 25
OLIVE = np.array([91, 97, 57], np.float32)
REAL_RX = re.compile(r"real\s+picture|not\s+a[il]\W*generated", re.I)
_AI_RX = re.compile(r"(^|[^a-z])a[il][\s-]?generated([^a-z]|$)", re.I)


class _AILabel:
    """A burned AI tag is a short CHIP ("AI-GENERATED", "[AI-generated]", "AI-generated Video"); an app screen's
    sentence that mentions AI-generated images is UI text, not a label (Ad 10 122.8 s)."""
    @staticmethod
    def search(t):
        return _AI_RX.search(t) if len(t.split()) <= 3 else None


AI_RX = _AILabel()
# screens banned from a paid ad on sight: the email-capture form and the in-app BEFORE/AFTER split (AGENTS.md,
# skill [A2]): a picture that reads like one escalates; the kit never ships it
BANNED_RX = re.compile(r"enter\s+your\s+e-?mail|your\s+e-?mail|e-?mail\s+address|get\s+my\s+download|meet\s+the\s+new\s+you", re.I)
CTA_RX = re.compile(r"image\s+of\s+yourself|^\W*with\s+abs\W*$|tap\s+the\s+button", re.I | re.M)
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


def turned_until(master, t, A, span=0.6):
    """Dan's head TURNED AWAY at a return from a picture (Vision face yaw > 25 deg on the first frames) that faces
    the camera again within `span` s: -> the time he faces camera (the picture before holds until then), else None.
    His Ad 10 window opened on a 0.35 s look to the side; the hand-built AV-07 held the food shot over it and three
    judges read our copy of it as visual junk (155.86 s)."""
    if not os.path.exists(FACE_BIN) or os.path.getmtime(FACE_BIN) < os.path.getmtime(FACE_SRC):
        os.makedirs(CACHE, exist_ok=True)
        run(["swiftc", "-O", FACE_SRC, "-o", FACE_BIN])
    d = os.path.join(A, "yaw", f"{t:.3f}")
    os.makedirs(d, exist_ok=True)
    if not glob.glob(os.path.join(d, "*.jpg")):
        run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", master, "-t", f"{span + 0.1:.2f}",
             "-vf", "fps=15,scale=960:-2:in_color_matrix=bt709:in_range=tv", os.path.join(d, "%03d.jpg")])
    files = sorted(glob.glob(os.path.join(d, "*.jpg")))
    r = subprocess.run([FACE_BIN] + files, capture_output=True, text=True)
    yaws = []
    for line in r.stdout.splitlines():
        f = json.loads(line)["faces"]
        yaws.append(abs(f[0]["yaw"]) if f else None)
    if len(yaws) < 3 or yaws[0] is None or yaws[0] < 25 or (yaws[1] or 0) < 25:
        return None
    for i, y in enumerate(yaws):
        if y is not None and y < 12:
            return round(t + i / 15.0, 3)
    return None


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
    near = [w.strip(",.?!\"") for w, a, b in W if b >= t0 - 6 and a <= t1 + 6]
    # a word the editor typed without its apostrophe ("Its") or split in two ("Chat GPT") takes the spoken spelling
    apo = {w.replace("'", "").replace("’", "").lower(): w for w in near if "'" in w or "’" in w}
    toks = text.split(" ")
    out_t, i = [], 0
    while i < len(toks):
        if i + 1 < len(toks):
            joined = (toks[i] + toks[i + 1]).lower()
            hit = next((w for w in near if w.lower() == joined and len(w) > 4), None)
            if hit:
                out_t.append(hit if toks[i][:1].isupper() == hit[:1].isupper() else hit[:1].swapcase() + hit[1:])
                i += 2
                continue
        t_ = toks[i]
        core = t_.strip(",.?!").lower()
        if core in apo and core not in ("its",) or (core == "its" and "it's" in apo.values()):
            rep = apo.get(core, "it's")
            rep = rep[:1].upper() + rep[1:] if t_[:1].isupper() else rep
            t_ = t_.replace(t_.strip(",.?!"), rep)
        out_t.append(t_)
        i += 1
    text = " ".join(out_t)
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
    rb, bx = D["r_box"], D["box"]
    # ... or the text side is dead and Dan's HEAD box on the other side matches his raw picture closely (his window
    # can hold a pushed or shifted crop that lowers the cell agreement: Ad 1 14-22 s; a photo card's box reads ~0.56)
    winR = ((left < WIN_DEAD) & (right > WIN_LIVE)) | ((left < 0.15) & (bx == 1) & (rb >= WIN_HEAD))
    winL = ((right < WIN_DEAD) & (left > WIN_LIVE)) | ((right < 0.15) & (bx == 2) & (rb >= WIN_HEAD))
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
                    elif prov == "by-name-else-real":            # a build's own asset folder: AI files are named so
                        prov = "ai" if name_prov(p) == "ai" else "real"
                    files.append((p, typ, prov, si))
        self.files = files
        self.curated = {si for si, src in enumerate(S["sources"]) if src.get("curated_crop")}
        sig = hashlib.md5(json.dumps([(p, os.path.getmtime(p), si, pv) for p, _, pv, si in files]).encode()).hexdigest()[:12]   # provenance in the key: a rule change must re-index
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

    def _fit(self, r, gq):
        """How far the library picture, warped onto his frame, is from his frame where they differ MOST: the 98th
        percentile of 24x24-block mean |difference| after a level match (grey levels; identical copies ~2-5)."""
        path, typ, t, w, h, H = r[1], r[2], r[4], r[5], r[6], r[10]
        if H is None:
            return 99.0
        if typ == "img":
            im = cv2.imread(path, cv2.IMREAD_COLOR)
        else:
            cap = cv2.VideoCapture(path); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, im = cap.read(); cap.release()
            im = im if ok else None
        if im is None:
            return 99.0
        sc = min(1.0, 1000 / max(im.shape[:2]))
        g = cv2.cvtColor(cv2.resize(im, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        try:
            Hi = np.linalg.inv(H)
        except np.linalg.LinAlgError:
            return 99.0
        wq, hq = gq.shape[1], gq.shape[0]
        warped = cv2.warpPerspective(g, Hi, (wq, hq), flags=cv2.INTER_LINEAR, borderValue=0)
        valid = cv2.warpPerspective(np.full_like(g, 255), Hi, (wq, hq), flags=cv2.INTER_NEAREST, borderValue=0) > 0
        valid = cv2.erode(valid.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        if valid.sum() < 500:
            return 99.0
        wb = cv2.GaussianBlur(warped, (0, 0), 2.0).astype(np.float32)
        a = gq[valid]; b = wb[valid]
        # his grade and compression change levels, not shapes: match b's levels to a's (least squares), then look
        # for the WORST 24x24 block. An edited belly lives in a few blocks; a whole-frame score dilutes it.
        A = np.vstack([b, np.ones_like(b)]).T
        gain, off = np.linalg.lstsq(A, a, rcond=None)[0]
        diff = np.zeros_like(gq); diff[valid] = np.abs(gq[valid] - (gain * wb[valid] + off))
        bs = 24
        worst = []
        for y in range(0, gq.shape[0] - bs + 1, bs):
            for x in range(0, gq.shape[1] - bs + 1, bs):
                vm = valid[y:y + bs, x:x + bs]
                if vm.mean() > 0.9:
                    worst.append(float(diff[y:y + bs, x:x + bs][vm].mean()))
        return float(np.percentile(worst, 98)) if worst else 99.0

    @staticmethod
    def _lib_coverage(H, e, qsize):
        """Fraction of the LIBRARY picture that his frame shows. A tighter crop of the same photo reads ~1; the
        uncropped original he did not use reads less (Ad 10 8.8 s: the full photo-180 jpg shows the Speedo he
        cropped away; the png he used is the crop)."""
        sc = min(1.0, 1000 / max(e["w"], e["h"]))
        w, h = e["w"] * sc, e["h"] * sc
        qw, qh = qsize
        quad = cv2.perspectiveTransform(np.float32([[[0, 0]], [[qw, 0]], [[qw, qh]], [[0, qh]]]), H).reshape(-1, 2)
        rect = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        try:
            area, _ = cv2.intersectConvexConvex(quad.astype(np.float32), rect)
        except cv2.error:
            return 0.0
        return float(max(0.0, area) / (w * h))

    def shows(self, img, path):
        """How much of ONE library picture this frame shows (0..1): the uploaded photo on a scrolling app screen. Its
        own detector (3000 points, the file at 720 px): on an app screen the library-wide 1500 points all go to the
        UI text and a 200 px photo gets none (Ad 10 122.8 s read 0 on a frame that shows it whole)."""
        if not hasattr(self, "_shows"):
            self._shows, self._orb3 = {}, cv2.ORB_create(nfeatures=3000)
        if path not in self._shows:
            L = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            sc = 720 / max(L.shape)
            L = cv2.resize(L, (int(L.shape[1] * sc), int(L.shape[0] * sc)), interpolation=cv2.INTER_AREA)
            self._shows[path] = (L.shape,) + self._orb3.detectAndCompute(L, None)
        (lh, lw), kl, dl = self._shows[path]
        q = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
        kq, dq = self._orb3.detectAndCompute(q, None)
        if dq is None or dl is None or len(kq) < 20:
            return 0.0
        m = self.bf.knnMatch(dq, dl, k=2)
        good = [a for a, b in (x for x in m if len(x) == 2) if a.distance < 0.75 * b.distance]
        if len(good) < 12:
            return 0.0
        H, mask = cv2.findHomography(np.float32([kq[g.queryIdx].pt for g in good]),
                                     np.float32([kl[g.trainIdx].pt for g in good]), cv2.RANSAC, 6.0)
        if H is None or int(mask.sum()) < 15:
            return 0.0
        h, w = q.shape[:2]
        quad = cv2.perspectiveTransform(np.float32([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]]), H).reshape(-1, 2)
        try:
            area, _ = cv2.intersectConvexConvex(quad.astype(np.float32), np.float32([[0, 0], [lw, 0], [lw, lh], [0, lh]]))
        except cv2.error:
            return 0.0
        return float(max(0.0, area) / (lw * lh))

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
            lcov = self._lib_coverage(H, e, qsize) if H is not None and inl >= 12 else 0.0
            res.append((inl, e["path"], e["typ"], e["prov"], e["t"], e["w"], e["h"], e.get("si", 0), cov, lcov, H))
        res.sort(key=lambda r: -r[0])
        # the same picture often lives in two files (the library's and a reference-ad copy, a jpg and a png): among
        # matches within 10 % of the best, the LARGEST file wins (the clean full-resolution original), then the
        # earlier source in auto_sources.json
        if res:
            top = res[0][0]
            # the same picture in several files: every match with half the best inliers that covers his picture
            tied = [r for r in res if r[0] >= 0.5 * top and r[8] >= 0.5] or [res[0]]
            rest = [r for r in res if r not in tied]
            # ⚠ NEAR-DUPLICATES ARE NOT THE SAME PICTURE. The library holds AI-edited variants of Dan's real photos
            # ("01_LIGHT_plus8lb" = the real deckchair photo with 8 lb painted on): same feature points, different
            # body. So the candidates are ranked by their PIXELS after alignment (NCC against his frame); only files
            # within 0.02 of the best fit count as copies of one picture, and provenance is shared only among those.
            gq = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(img, (int(qsize[0]), int(qsize[1])), interpolation=cv2.INTER_AREA),
                                               cv2.COLOR_BGR2GRAY), (0, 0), 2.0).astype(np.float32)
            fits = []
            for r in tied[:8]:
                fits.append(self._fit(r, gq))
            fits += [99.0] * (len(tied) - len(fits))
            tied = [r + (f,) for r, f in zip(tied, fits)]
            fits_img = [f for r, f in zip(tied, fits) if r[2] == "img"]
            best_fit = min(fits_img) if fits_img else min(fits)    # the worst block's mean |difference|, grey levels (lower = closer)
            same = [r for r in tied if r[2] == "vid" or r[11] <= best_fit * 1.3 + 1.5]   # a clip is sampled at 1 fps: its fit is timing, not content
            others = [r for r in tied if r not in same]
            # of the copies (pixel fit only EXCLUDES a different picture; as a ranking it favours blurry re-saves):
            # the curated library first (auto_sources.json order: a re-saved doc copy in an old ad folder lost the
            # 27.1 s chip placement), then the file he actually showed (all of it on screen: the cropped png over the
            # uncropped jpg), then the largest (clean full resolution)
            same.sort(key=lambda r: (r[7], -(r[9] >= 0.85), -(r[5] * r[6])))   # "on screen" is a yes/no at 85 %, so the bigger file of a tie wins
            provs = {r[3] for r in same if r[3] in ("real", "ai")} if top >= MATCH_MIN_INLIERS else set()
            if len(provs) > 1:                       # two copies of one picture disagree on real vs AI
                same = [r[:3] + ("conflict",) + r[4:] for r in same]
            elif provs and same[0][3] not in provs:  # a copy with no provenance inherits its identical twin's
                same = [r[:3] + (next(iter(provs)),) + r[4:] for r in same]
            tied = same + sorted(others, key=lambda r: r[11])
            rest = [r + (None,) for r in rest]
            res = tied + rest
        # a Dan-APPROVED crop of the matched photo (head and stomach framed, Ad 1 attempt 3 item 8) replaces the full
        # photo when all of it lies inside his picture: Ad 8 16.2 s put the 4:3 original in a card that cut his head
        # and hid his stomach, the framing Dan had already rejected on Ad 1
        if res and res[0][2] == "img" and res[0][7] not in getattr(self, "curated", ()):
            cur = [r for r in res if r[7] in self.curated and r[2] == "img" and r[0] >= max(20, 0.25 * res[0][0]) and r[9] >= 0.85]
            if cur:
                c = max(cur, key=lambda r: r[0])
                res = [c[:3] + (res[0][3] if res[0][3] in ("real", "ai") else c[3],) + c[4:]] + [r for r in res if r is not c]
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

    def split_shots(n0, n1):
        cuts = [n0] + isolated_spikes(cut, n0, n1) + [n1]
        for b0, b1, c in B_:
            if n0 + MIN_SHOT < c < n1 - MIN_SHOT and not any(abs(c - x) < MIN_SHOT for x in cuts):
                cuts.append(c)
        cuts = sorted(set(cuts))
        shots = [[cuts[i], cuts[i + 1]] for i in range(len(cuts) - 1)]
        merged = []
        for s_ in shots:
            if merged and s_[1] - s_[0] < MIN_SHOT:
                merged[-1][1] = s_[1]
            elif not merged and s_[1] - s_[0] < MIN_SHOT and len(shots) > 1:
                shots[1][0] = s_[0]
            else:
                merged.append(s_)
        return merged

    def side_words(n0, n1, kind):
        ws = set()
        for n in sorted(O):
            if n0 <= n < n1:
                for l in O[n]:
                    if (l["box"][2] < 1280 * 0.58) if kind != "windowL" else (l["box"][0] > 1280 * 0.42):
                        ws |= set(norm(l["text"]).split())
        return ws

    def last_side_words(n0, n1, kind):
        """The panel's words on the shot's LAST read that has any: a type-on reads 'INTODAY'S E P' first."""
        for n in sorted((n for n in O if n0 <= n < n1), reverse=True):
            ws = set()
            for l in O[n]:
                if (l["box"][2] < 1280 * 0.58) if kind != "windowL" else (l["box"][0] > 1280 * 0.42):
                    ws |= set(norm(l["text"]).split())
            if len(ws) >= 2:
                return ws
        return set()

    # every insert run -> its shots; a SHOT that carries the same panel words as the window beside it is that
    # window (his window's Dan crop can drift off the raw picture for a second or two, and his window slides in
    # over a flash: Ad 1 13.7-14.8 s). The panel's words decide, not the picture agreement.
    S_ = []
    for r in R:
        if r[0] == "insert":
            for k_, (s0, s1) in enumerate(split_shots(r[1], r[2])):
                S_.append(["insert", s0, s1, r[3] if k_ == 0 and len(r) > 3 else "his cut inside an insert"])
        else:
            S_.append(list(r))
    changed = True
    while changed:
        changed = False
        for i, r in enumerate(S_):
            if r[0] != "insert":
                continue
            for j in (i - 1, i + 1):
                if 0 <= j < len(S_) and S_[j][0] in ("window", "windowL"):
                    a_, b_ = last_side_words(r[1], r[2], S_[j][0]), side_words(S_[j][1], S_[j][2], S_[j][0])
                    if len(a_) >= 2 and len(a_ & b_) >= 0.6 * len(a_):
                        r[0] = S_[j][0]; changed = True
                        break
        m_ = [S_[0]]
        for r in S_[1:]:
            if r[0] == m_[-1][0] and r[0] != "insert":
                m_[-1][2] = r[2]
            else:
                m_.append(r)
        S_ = m_
    # consecutive insert shots form one insert group (the app-demo and entrance rules look across the group)
    R = []
    for r in S_:
        if r[0] == "insert" and R and R[-1][0] == "insert" and R[-1][2] == r[1]:
            R[-1][2] = r[2]; R[-1][4].append([r[1], r[2]])
        elif r[0] == "insert":
            R.append(["insert", r[1], r[2], r[3] if len(r) > 3 else "", [[r[1], r[2]]]])
        else:
            R.append(r)

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
            # a window run can hold several plates back to back (Ad 1: the app window, then the statement): split
            # it at his hard cuts / flash centres, then describe each plate
            cuts_w = [n0] + isolated_spikes(cut, n0, n1) + [c for _, _, c in B_ if n0 + MIN_SHOT < c < n1 - MIN_SHOT] + [n1]
            # ... and where the panel's words change completely between two reads (a new plate, no cut under it)
            prev_r = None
            for n, lines in samples_in(n0, n1):
                ws = set(norm(" ".join(l["text"] for l in lines if (l["box"][2] < 1280 * 0.58) == (kind == "window"))).split())
                if len(ws) >= 3:
                    # a new plate unless one read's words are mostly inside the other's (a reveal ADDS words; one
                    # shared "your" between an app screen and a bullet header is not the same plate, Ad 8 190.9 s)
                    if prev_r and len(ws & prev_r[1]) < 0.5 * min(len(ws), len(prev_r[1])):
                        lo, hi = prev_r[0], n
                        cuts_w.append(max(range(lo + 1, hi + 1), key=lambda q: cut[q]))
                    prev_r = (n, ws)
            cuts_w = sorted(set(cuts_w))
            plates = []
            for i in range(len(cuts_w) - 1):
                if plates and cuts_w[i + 1] - cuts_w[i] < 3 * MIN_SHOT:
                    plates[-1][1] = cuts_w[i + 1]
                else:
                    plates.append([cuts_w[i], cuts_w[i + 1]])
            for p0, p1 in plates:
                ent, ev_, e_ = describe_window(master, frames_dir, D, O, W, p0, p1, kind, T, cell_mean, media, prep, left, right)
                ev_["boundary"] = how0 if p0 == n0 else "his cut inside the window run"
                # consecutive plates that share their text are ONE plate: a cut on Dan's side under an unchanged or
                # still-revealing panel (his bullets type on one by one). Only a panel whose words change is new.
                prev = beats[-1] if beats and abs(beats[-1]["t1"] - ent["t0"]) < 0.05 else None
                if prev is not None and prev.get("kind") in ("window", "stmt", "winmedia") and \
                        (same_plate(prev, ent) or (ent["kind"] != "winmedia" and not text_key(ent))):
                    keep_new = len(text_key(ent) or "") > len(text_key(prev) or "")
                    if keep_new and prev["kind"] == ent["kind"]:
                        for k_ in ("bullets", "header", "parts"):
                            if k_ in ent:
                                prev[k_] = ent[k_]
                    prev["t1"] = ent["t1"]
                    esc.extend(x for x in e_ if "no readable" not in x["what"])     # an empty read inside a merged plate is not a plate
                    continue
                beats.append(ent)
                rep_beats.append(dict(entry=ent, confidence=ev_.pop("confidence"), evidence=ev_))
                for x in e_:
                    x["_plate"] = id(ent)
                esc.extend(e_)
            # a plate that was empty on its own and filled by a merge is fine
            esc[:] = [x for x in esc if not ("no readable" in x["what"] and any(id(b) == x.get("_plate") and
                                                                                   (b.get("bullets") or b.get("parts")) for b in beats))]
            continue

        # ---- an insert group: his shots
        merged = [list(x) for x in run_[4]]
        # a card's ENTRANCE (a short, fast-moving first shot straight out of talk: the phone zooming in blurred) is
        # not content: the beat starts when the picture has landed; the kit draws its own entrance
        if len(merged) > 1 and merged[0][1] - merged[0][0] < 18 and float(np.median(cut[merged[0][0] + 1:merged[0][1]])) > 5.0:
            merged = merged[1:]
        run_beats, trans = [], []
        for s0, s1 in merged:
            beat, ev = describe_shot(master, A, frames_dir, D, O, W, s0, s1, fps, T, lambda: lib_get(), AI, esc, media, prep, B)
            if beat:
                beats.append(beat); run_beats.append((beat, ev))
                rep_beats.append(dict(entry=beat, confidence=ev.pop("confidence"), evidence=ev))
            elif ev.get("transition"):
                trans.append((T(s0), T(s1)))
                rep_beats.append(dict(entry=dict(kind="transition", t0=T(s0), t1=T(s1)), confidence="high", evidence=ev,
                                      dropped="a transition: its time goes to the picture beside it"))
        for a_, b_ in trans:                          # the picture it leads into takes it; out of a picture it is talk
            nxt = next((bt for bt, _ in run_beats if abs(bt["t0"] - b_) < 0.02), None)
            prv = next((bt for bt, _ in run_beats if abs(bt["t1"] - a_) < 0.02), None)
            if nxt is not None:
                nxt["t0"] = a_
        # an APP DEMO stays in one layout: a clean still between phone shots of the same insert is a card too
        if any(ev_.get("phone") for _, ev_ in run_beats):
            for b_, ev_ in run_beats:
                if b_["kind"] == "bleed":
                    b_["kind"] = "card"; ev_["layout"] = "card: part of an app-demo sequence"
            # the photo he UPLOADS stays on the app's next screen (the form shows it large): a phone screen right after
            # a real-labelled upload screen, with no label of its own, keeps the label (three judges, Ad 10 122.8 /
            # 173.9 s: "a real photo of Dan shown for ~2.8 s with no chip")
            for (pb, pe), (b_, ev_) in zip(run_beats[:-1], run_beats[1:]):
                if pe.get("phone") and ev_.get("phone") and pb.get("label_kind") in ("real", "ai") and not b_.get("label_kind") \
                        and not ev_.get("burned_label"):
                    # ... but only while the photo is ON the screen: the form scrolls it away (Ad 10 round 4 judge,
                    # 124.4 / 175.2 s: "Real picture of me" under a form with no photo). The screen is sampled every
                    # 3rd frame against the uploaded file; where it is gone the clip splits and the rest has no chip.
                    up = (pe.get("matches") or [{}])[0].get("file")
                    shown = []
                    if up:
                        hole = ev_.get("hole")
                        for n in range(int(round(b_["t0"] * fps)), int(round(b_["t1"] * fps)), 3):
                            fp_ = grab(master, n / fps, os.path.join(frames_dir, f"up{n:06d}.png"))
                            im_ = cv2.imread(fp_)
                            if hole:
                                im_ = im_[max(0, hole[1]):hole[3], max(0, hole[0]):hole[2]]
                            shown.append((n, lib_get().shows(im_, up) >= 0.35))
                    # runs of on / off, a run under 12 frames joins the one before it (no chip flicker)
                    runs = []
                    for n, v in shown:
                        if runs and runs[-1][2] == v:
                            runs[-1][1] = n + 3
                        else:
                            runs.append([n, n + 3, v])
                    for i in range(len(runs) - 1, 0, -1):
                        if runs[i][1] - runs[i][0] < 12:
                            runs[i - 1][1] = runs[i][1]; del runs[i]
                    k = 0
                    while k < len(runs) - 1:
                        if runs[k][2] == runs[k + 1][2]:
                            runs[k][1] = runs[k + 1][1]; del runs[k + 1]
                        else:
                            k += 1
                    if not up or all(v for _, _, v in runs):
                        b_["label_kind"] = pb["label_kind"]; b_["caps"] = False
                        ev_["label"] = f"{pb['label_kind']} label: the uploaded photo stays on this app screen"
                        continue
                    if not any(v for _, _, v in runs):
                        ev_["label"] = "no label: the uploaded photo is not on this app screen"
                        continue
                    q = next((q_ for q_ in prep if q_["beat"] is b_), None)
                    if q is None:
                        b_["label_kind"] = pb["label_kind"]; b_["caps"] = False
                        continue
                    # split the clip where the photo comes and goes; each piece keeps his picture frame-exact
                    t1_all, c1_all = b_["t1"], q["c1"]
                    parts = [b_]
                    for r0, _, _ in runs[1:]:
                        ts = T(r0)
                        prev_b = parts[-1]
                        nb = {k_: v_ for k_, v_ in b_.items() if k_ != "label_kind"}
                        key2 = f"auto_{r0:05d}"
                        nb["t0"] = ts; nb["media"] = key2; nb["caps"] = False
                        out2 = os.path.join("assets_auto", f"{key2}.mp4")
                        prep.append(dict(q, out=out2, beat=nb, c0=max(q["c0"], ts), c1=c1_all))
                        media[key2] = ("vid", out2, 0.0)
                        prev_b["t1"] = ts
                        parts.append(nb)
                    parts[-1]["t1"] = t1_all
                    for i_, q_ in enumerate([x for x in prep if any(x["beat"] is p_ for p_ in parts)]):
                        q_["c1"] = min(c1_all, q_["beat"]["t1"])
                    for p_, (r0, r1, v) in zip(parts, runs):
                        p_["caps"] = False
                        if v:
                            p_["label_kind"] = pb["label_kind"]
                        else:
                            p_.pop("label_kind", None)
                    ev_["label"] = (f"{pb['label_kind']} label only while the uploaded photo is on screen; the screen is split at "
                                    + ", ".join(f"{p_['t0']:.3f}" for p_ in parts[1:]))
                    at = beats.index(b_)
                    for j_, p_ in enumerate(parts[1:]):
                        beats.insert(at + 1 + j_, p_)
                        rep_beats.append(dict(entry=p_, confidence="high", evidence=dict(ev_, source="split from the app screen before it at the photo's edge")))

    # ---- 5. overlays over live Dan: lower thirds and the CTA pill
    ov = []
    for n in sorted(O):
        if st[n] not in ("talk",):
            continue
        L = [l for l in O[n] if l["box"][1] > 720 * LT_TOP and cell_mean(n, l["box"]) < 0.5]
        if L:
            L = sorted(L, key=lambda l: (round(((l["box"][1] + l["box"][3]) / 2) / 30), l["box"][0]))
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

    ctas.sort(key=lambda x: x["t0"])
    # ---- the kit's grammar asks for template cta.count pills (his measured range); a master with fewer gets the
    #      missing ones AT HIS OWN MEASURED POSITIONS (Ad 1: 0.43 and 0.77 of the runtime, the last one runs to the
    #      end), each on a sentence start inside plain talk, clear of every graphic. Recorded as a deviation.
    TPL = json.load(open(os.path.join(HERE, "template.json")))["cta"]
    added_ctas = []
    need = int(TPL.get("count", 3)) - len(ctas)
    if need > 0:
        busy = [(b["t0"], b["t1"]) for b in beats] + [(o["t0"], o["t1"]) for o in lts + ctas]
        starts = [W[i][1] for i in range(1, len(W)) if W[i][1] - W[i - 1][2] >= 0.12 or W[i - 1][0][-1:] in ".?!,"]
        for frac in (0.43, 0.77):
            if need <= 0:
                break
            target = frac * dur
            if any(abs(c["t0"] - target) < 15 for c in ctas):
                continue
            cands = [t for t in starts if all(t + TPL["dur_s"] + 0.3 < a_ or t - 0.3 > b_ for a_, b_ in busy)
                     and all(st[int(q * fps)] == "talk" for q in np.arange(t, t + TPL["dur_s"], 0.1) if int(q * fps) < N)]
            cands = [t for t in cands if abs(t - target) <= 20]
            if cands:
                t0 = min(cands, key=lambda t: abs(t - target))
                c = dict(t0=round(t0, 3), t1=round(t0 + TPL["dur_s"], 3))
                ctas.append(c); added_ctas.append(c); busy.append((c["t0"], c["t1"])); need -= 1
        ctas.sort(key=lambda x: x["t0"])
        for c in added_ctas:
            rep_beats.append(dict(entry=dict(kind="cta", **c), confidence="high",
                                  evidence=dict(source="added by the kit's grammar (template cta.count): not in his master")))

    beats.sort(key=lambda b: b["t0"])
    # a return to Dan that opens on him TURNED AWAY: the picture before holds until he faces the camera
    for i, b_ in enumerate(beats[:-1]):
        nxt = beats[i + 1]
        if b_["kind"] in ("card", "bleed") and (nxt["kind"] in ("window", "windowL") and abs(nxt["t0"] - b_["t1"]) < 0.05):
            tt = turned_until(master, b_["t1"], A)
            if tt and tt < nxt["t1"] - 0.5:
                rep_beats.append(dict(entry=dict(kind="hold", t0=b_["t1"], t1=tt), confidence="high",
                                      evidence=dict(why="his head is turned away as the window opens (face yaw > 25 deg)")))
                b_["t1"] = tt; nxt["t0"] = tt
    for i, b_ in enumerate(beats):
        if b_["kind"] in ("card", "bleed"):
            nxt_t0 = beats[i + 1]["t0"] if i + 1 < len(beats) else dur
            if nxt_t0 - b_["t1"] > 0.3:              # a return to plain talk
                tt = turned_until(master, b_["t1"], A)
                if tt and tt < nxt_t0:
                    rep_beats.append(dict(entry=dict(kind="hold", t0=b_["t1"], t1=tt), confidence="high",
                                          evidence=dict(why="his head is turned away as the talk resumes (face yaw > 25 deg)")))
                    b_["t1"] = tt
    # an insert ENTRANCE that ended up as its own beat (the blurred phone zooming in, < 0.5 s, fast) followed at once
    # by the landed picture: it is not content (the kit draws its own entrance)
    evs = {id(r["entry"]): r for r in rep_beats}
    keep = []
    for i, b_ in enumerate(beats):
        r_ = evs.get(id(b_))
        nxt = beats[i + 1] if i + 1 < len(beats) else None
        if b_["kind"] in ("card", "bleed") and b_["t1"] - b_["t0"] < 0.6 and r_ and r_["evidence"].get("motion", 0) > 5.0 \
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
    for c in added_ctas:
        C["deviations"].append([f"CTA {c['t0']:.2f}", "his master has fewer CTA pills than the kit's measured range; "
                                "this one is added at his Ad 1 position on a sentence start in plain talk"])
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


def banned_reads(O, n0, n1):
    return [(n, l["text"]) for n in sorted(O) if n0 <= n < n1 for l in O[n] if BANNED_RX.search(l["text"])]


def olive_ring(img, hole, pad=40):
    """Share of his olive colour in a band just outside the hole: ~1 around his card, low around a picture that
    merely has grass or olive tones in it (Ad 8 150.4 s: a lawn read as his card and the clip was cut to a strip)."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = hole
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
    rgb = img[Y0:Y1, X0:X1][..., ::-1].astype(np.float32)
    mask = np.ones(rgb.shape[:2], bool)
    mask[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
    if not mask.any():
        return 0.0
    return float((np.linalg.norm(rgb - OLIVE, axis=2) < 32)[mask].mean())


def clean_range(D, s0, s1, fps):
    """The part of a shot that is HIS PICTURE ONLY: his flash / whip transitions sit at the shot's edges and the
    boundary is placed at a burst's centre, so the last frames before it are already his transition and his next
    shot (Ad 10 57.86 s: one frame of his talking head in the card). -> (c0, c1) seconds."""
    cut = D["cut"]
    B = bursts(cut)
    c0, c1 = s0, s1
    for a, b, c in B:
        if a - 3 <= s1 <= b + 3:
            c1 = min(c1, a - 1)
        if a - 3 <= s0 <= b + 3:
            c0 = max(c0, b + 2)
    # a single hard cut at the very edge: the first frame of his NEXT shot (or the last of the one before) got in
    # (Ad 8 122.09 s: one frame of his wide shot before the flash)
    while c1 - c0 > 8 and cut[min(c1 - 1, len(cut) - 1)] >= CUT_SPIKE:
        c1 -= 1
    while c1 - c0 > 8 and cut[min(c0 + 1, len(cut) - 1)] >= CUT_SPIKE:
        c0 += 1
    # a DISSOLVE edge (no hard cut within 2 frames, no burst): his next picture is already fading in over the last
    # frames (Ad 8 190.82 s: the next card's header smeared over the phone for 3 frames). Stop 4 frames early; the
    # last clean frame holds
    near = lambda n: float(np.max(cut[max(0, n - 2):min(len(cut), n + 3)])) if len(cut) else 0.0
    if c1 == s1 and c1 - c0 > 20 and near(s1) < CUT_SPIKE:
        c1 -= 4
    if c0 == s0 and c1 - c0 > 20 and near(s0) < CUT_SPIKE:
        c0 += 4
    if c1 - c0 < 6:                                   # nothing clean enough: keep the middle of the shot
        m = (s0 + s1) // 2
        c0, c1 = max(s0, m - 3), min(s1, m + 3)
    return c0 / fps, c1 / fps


def landed_range(A, c0, c1, fps, hole, src_w=1920):
    """Trim a lifted card clip to the frames where his picture has LANDED in its hole: while his card slides in (or
    out) the fixed crop shows his olive card background along one edge and a motion-blurred picture (Ad 8 58.59 /
    142.81 s: three frames of olive band down the left, judged a stutter). Read on the 256-wide master cache: the
    share of olive in each 2-px edge strip of the hole; an edge that is mostly olive means not landed yet."""
    p = os.path.join(A, "m256.rgb")
    if not os.path.exists(p):
        return c0, c1
    n_ = os.path.getsize(p) // (256 * 144 * 3)
    M = np.memmap(p, np.uint8, "r").reshape(n_, 144, 256, 3)
    s = 256 / src_w
    x0, y0, x1, y1 = [int(round(v * s)) for v in hole]
    x0, y0 = max(0, x0 + 1), max(0, y0 + 1)
    x1, y1 = min(255, x1 - 1), min(143, y1 - 1)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return c0, c1

    def strips(n):
        f = M[min(max(n, 0), n_ - 1)].astype(np.float32)
        return np.array([float((np.linalg.norm(st - OLIVE, axis=2) < 40).mean()) for st in
                         (f[y0:y1, x0:x0 + 2], f[y0:y1, x1 - 2:x1], f[y0:y0 + 2, x0:x1], f[y1 - 2:y1, x0:x1])])
    a, b = int(round(c0 * fps)), int(round(c1 * fps))
    mid = range(a + (b - a) // 4, b - (b - a) // 4, max(1, (b - a) // 16))
    base = np.median(np.array([strips(n) for n in mid]), axis=0)      # his picture's own olive tones (a lawn, a wall)
    band = lambda n: bool(((strips(n) > 0.5) & (strips(n) > base + 0.3)).any())
    k = 0
    while k < 20 and b - a > 12 and band(a):
        a += 1; k += 1
    k = 0
    while k < 20 and b - a > 12 and band(b - 1):
        b -= 1; k += 1
    return a / fps, b / fps


def text_key(b):
    if b.get("bullets"):
        return norm(" ".join(b["bullets"]))
    if b.get("parts"):
        return norm(" ".join(p[0] for p in b["parts"]))
    return None


def same_plate(a, b):
    """Two plates are one if they are the same kind and their words overlap (a reveal adds words, never replaces)."""
    if a.get("kind") != b.get("kind"):
        return False
    if a["kind"] == "winmedia":
        return True
    ka, kb = set((text_key(a) or "").split()), set((text_key(b) or "").split())
    if not ka or not kb:
        return True
    return len(ka & kb) >= 0.5 * min(len(ka), len(kb))


OLIVE_INK = lambda rgb: (rgb[..., 1] > rgb[..., 2] + 35) & (rgb[..., 0] > rgb[..., 2] + 20) & (rgb[..., 1] > 110)
WHITE_INK = lambda rgb: (rgb.min(axis=-1) > 150) & (rgb.max(axis=-1) - rgb.min(axis=-1) < 45)


def line_styles(img, line, scale=1.5):
    """-> [(word, "olive"|"white")] for one OCR line: the olive part of a two-colour line ("Chat GPT" in olive, "Or
    Any" in white on the same line) found from the columns' ink colour, words placed by character count."""
    x0, y0, x1, y1 = [int(v * scale) for v in line["box"]]
    crop = img[max(0, y0):y1, max(0, x0):x1][..., ::-1].astype(np.int32)
    words = line["text"].split()
    if crop.size == 0 or not words:
        return [(w, "white") for w in words]
    ol, wh = OLIVE_INK(crop).sum(axis=0), WHITE_INK(crop).sum(axis=0)
    total = len(line["text"])
    out, pos = [], 0
    for w in words:
        a_, b_ = pos / total, (pos + len(w)) / total
        c0, c1 = int(a_ * crop.shape[1]), max(int(a_ * crop.shape[1]) + 1, int(b_ * crop.shape[1]))
        out.append((w, "olive" if ol[c0:c1].sum() > 1.2 * wh[c0:c1].sum() else "white"))
        pos += len(w) + 1
    return out


def describe_window(master, frames_dir, D, O, W, n0, n1, kind, T, cell_mean, media, prep, left, right):
    """A plate beside live Dan -> window (bullets), stmt (styled statement) or winmedia (a phone/app beside him)."""
    esc = []
    fps = float(D["fps"])
    S = [(n, O[n]) for n in sorted(O) if n0 <= n < n1]
    text_side = (lambda b: b[2] < 1280 * 0.58) if kind == "window" else (lambda b: b[0] > 1280 * 0.42)
    reads = [(n, [l for l in lines if text_side(l["box"]) and cell_mean(n, l["box"]) < 0.5]) for n, lines in S]
    tail = [r for r in reads if r[0] >= n0 + (n1 - n0) // 2] or reads
    mx = max((sum(len(l["text"]) for l in r[1]) for r in tail), default=0)
    full = [r for r in tail if sum(len(l["text"]) for l in r[1]) >= 0.9 * mx] or [(n0, [])]
    # a read taken mid-animation misspells ("nelps otner"): of the full reads, the one closest to what he says
    t0_, t1_ = T(n0), T(n1)
    best = max(full, key=lambda r: best_spoken_match(" ".join(l["text"] for l in r[1]), W, t0_, t1_, pad=8.0)[0])
    key = lambda L: norm(" ".join(l["text"] for l in L))
    agree = sum(1 for r in reads if key(r[1]) and ratio(key(r[1]), key(best[1])) > 0.97)
    lines = sorted(best[1], key=lambda l: l["box"][1])
    rep_n = best[0]
    fp = grab(master, rep_n / fps, os.path.join(frames_dir, f"f{rep_n:06d}.png"))
    img = cv2.imread(fp)
    t0, t1 = T(n0), T(n1)
    ev = dict(frames=[n0, n1], reads_agreeing=agree, read_frame=rep_n, rep_frame=fp,
              left_agreement=round(float(left[n0:n1].mean()), 3), right_agreement=round(float(right[n0:n1].mean()), 3))
    # ---- winmedia: a PICTURE on the text side (a phone), its words small app chrome
    # the panel's width from the agreement map (dead columns), never a fixed share: a fixed 58 % took in a strip
    # of live Dan and the phone crop centred on him (Ad 8 183.4 s)
    colm = D["cells"][min(rep_n, len(D["cells"]) - 1)].mean(axis=0)
    if kind == "window":
        live = [j for j in range(16) if colm[j] > 0.6]
        x1_ = (min(live) if live else 9) * 120
        side, off_ = img[:, :max(240, x1_)], 0
    else:
        live = [j for j in range(16) if colm[j] > 0.6]
        x0_ = (max(live) + 1 if live else 7) * 120
        side, off_ = img[:, min(1680, x0_):], min(1680, x0_)
    tb = [[v * 1.5 for v in l["box"]] for l in lines]
    bbox, olive_frac, pic_frac, hole = picture_bbox(side, tb if kind == "window" else [])
    hts = [l["box"][3] - l["box"][1] for l in lines]
    small_text = not hts or np.median(hts) < 26
    if bbox is not None and pic_frac > 0.08 and small_text:
        cx = off_ + (bbox[0] + bbox[2]) // 2
        x = int(min(max(cx - 304, 0), 1920 - 608))
        mk = f"auto_{n0:05d}"
        out = os.path.join("assets_auto", f"{mk}.mp4")
        ent = dict(kind="winmedia", media=mk, t0=t0, t1=t1)
        c0, c1 = clean_range(D, n0, n1, fps)
        prep.append(dict(out=out, beat=ent, c0=c0, c1=c1, x=x))
        media[mk] = ("vid", out, 0.0)
        bad = banned_reads(O, n0, n1)
        if bad:
            esc.append(dict(t0=t0, t1=t1, what="a banned screen in his master (email capture / in-app before-after): trim or replace",
                            first_seen=T(bad[0][0]), text=bad[0][1]))
            ev["banned"] = bad[:3]
        ev.update(source=f"portrait crop of his master at x={x} (the phone beside Dan)", picture_area=round(pic_frac, 3),
                  ui_text=[l["text"] for l in lines], confidence="high")
        return ent, ev, esc
    glyphs = [bool(re.match(r"^[•▪■◾●\-–·]\s*", l["text"])) for l in lines]
    styled = lines and not any(glyphs) and len(lines) >= 2
    colours = []
    if styled:
        for l in lines:
            colours.append(line_styles(img, l))
        has_olive = any(c == "olive" for ws in colours for _, c in ws)
        styled = has_olive or (max(hts) > 1.3 * min(hts))
    if styled:
        # ---- stmt: parts in reading order, each "ink" (small), "olive" (his accent colour) or "big"
        small = min(hts)
        parts = []
        for l, ws in zip(lines, colours):
            h = l["box"][3] - l["box"][1]
            for w, c in ws:
                st_ = "olive" if c == "olive" else ("big" if h > 1.3 * small else "ink")
                if parts and parts[-1][1] == st_:
                    parts[-1][0] += " " + w
                else:
                    parts.append([w, st_])
        parts = [[repair_with_speech(p_, W, t0, t1), s_] for p_, s_ in parts]
        full = " ".join(p_ for p_, _ in parts)
        chk = best_spoken_match(full, W, t0, t1)
        ent = dict(kind="stmt", parts=parts, t0=t0, t1=t1)
        ev.update(transcript_check=dict(ratio=chk[0], spoken=chk[1]),
                  confidence="high" if agree >= 2 and chk[0] >= 0.5 else "low")
        if agree < 2 or chk[0] < 0.3:
            esc.append(dict(t0=t0, t1=t1, what="statement text not confirmed", text=full))
        return ent, ev, esc
    # ---- window: header + bullets
    header, bullets = None, []
    for i, l in enumerate(lines):
        t_ = l["text"]
        glyph = glyphs[i]
        clean = re.sub(r"^[•▪■◾●\-–·]\s*", "", t_)
        if not bullets and not glyph and (t_.isupper() or l["box"][1] < 150) and header is None:
            header = sentence_case(clean) if clean.isupper() else clean
            continue
        if glyph or not bullets:
            bullets.append(clean)
        else:
            prev_l = lines[i - 1]
            gap = l["box"][1] - prev_l["box"][3]
            if gap > 0.8 * (prev_l["box"][3] - prev_l["box"][1]):
                bullets.append(clean)
            else:
                bullets[-1] = bullets[-1] + " " + clean
    bullets = [repair_with_speech(b, W, t0, t1) for b in bullets]
    checks = [best_spoken_match(b, W, t0, t1) for b in bullets]
    ent = dict(kind="window", header=header, bullets=bullets, t0=t0, t1=t1)
    if kind == "windowL":
        ent["dan_side"] = "left"
    ev.update(transcript_check=[dict(line=b, ratio=c[0], spoken=c[1]) for b, c in zip(bullets, checks)],
              confidence="high" if agree >= 2 and bullets and min(c[0] for c in checks) >= 0.5 else "medium" if bullets else "low")
    if not bullets:
        esc.append(dict(t0=t0, t1=t1, what="window with no readable bullets"))
    elif agree < 2 or min(c[0] for c in checks) < 0.3:
        esc.append(dict(t0=t0, t1=t1, what="window text not confirmed (reads disagree or no spoken match)",
                        bullets=bullets, checks=checks))
    return ent, ev, esc


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
    # a TRANSITION, not content: his white flash, or the empty grid a card flies in over
    flash = float(img.mean()) > 185 and float(img.std()) < 40 and (s1 - s0) < 0.6 * fps      # a sunny beach is bright, not flat
    whip = (s1 - s0) < 0.4 * fps and motion > 20                                             # every frame a new picture
    if flash or whip or (pic_frac < 0.02 and words == 0 and olive_frac < 0.05):
        ev.update(transition=True, confidence="high", why="white flash" if flash else "whip/flash burst" if whip else "empty field")
        return None, ev
    bad = banned_reads(O, s0, s1)
    if bad:
        esc.append(dict(t0=t0, t1=t1, what="a banned screen in his master (email capture / in-app before-after): trim or replace",
                        first_seen=T(bad[0][0]), text=bad[0][1]))
        ev["banned"] = bad[:3]

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
    ev["matches"] = [dict(file=r[1], inliers=r[0], typ=r[2], prov=r[3], t=round(r[4], 2), coverage=round(r[8], 3),
                          shown=round(r[9], 3), fit=(round(r[11], 3) if len(r) > 11 and r[11] is not None else None)) for r in m[:3]]
    # a match counts when it is strong, or fair AND the library picture actually covers his (a 29-inlier "match" with
    # 0 % coverage is two unrelated gym pictures sharing texture: Ad 1 136.3 s)
    top = m[0] if m and (m[0][0] >= 40 or (m[0][0] >= MATCH_MIN_INLIERS and m[0][8] >= 0.3)) else None
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
        # full bleed is for a PHYSIQUE photo that is portrait or tall enough; a clothed family snapshot (Dan with his
        # daughter) goes in the card, where the cover crop cannot make the child the subject (both answer keys)
        tall_enough = h > w or h >= 1440
        phys = is_physique(AI, top[1], ev) if tall_enough else None
        beat["kind"] = "bleed" if tall_enough and phys is not False else "card"
        media[key] = ("img", top[1], 0, 1.0, {"oy": 0.0})
        ev["source"] = "clean library still"
        label = prov if prov in ("real", "ai") else burned
        if prov in ("real", "ai") and burned and burned != prov:
            esc.append(dict(t0=t0, t1=t1, what=f"label conflict: library says {prov}, his burned label says {burned}", file=top[1]))
            conf = "low"
        if label is None:
            if (phys if tall_enough else is_physique(AI, fp, ev)) is False:
                ev["label"] = "no label: not a physique picture, no provenance"
            else:
                esc.append(dict(t0=t0, t1=t1, what="a physique still with no provenance and no label (every physique picture needs exactly one)", file=top[1]))
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
            c0, c1 = clean_range(D, s0, s1, fps)
            prep.append(dict(out=out, beat=beat, c0=c0, c1=c1, x=x))
            media[key] = ("vid", out, 0.0)
            ev["source"] = f"portrait crop of his master at x={x} (a phone), his picture {c0:.3f}-{c1:.3f} s"
        else:
            out = os.path.join("assets_auto", f"{key}.mp4")
            c0, c1 = clean_range(D, s0, s1, fps)
            crop = None
            if hole is not None and olive_frac > 0.15 and area(hole) < 0.8 * img.shape[0] * img.shape[1] and olive_ring(img, hole) > 0.6:
                # his OWN card around the picture: lift only the picture inside it (a card inside our card read as a
                # nested panel, Ad 8 58.6 s), and his label/callout outside the hole goes with it -- so the burned
                # label only counts when it sits inside the hole
                hx0, hy0, hx1, hy1 = hole
                cw_, ch_ = (hx1 - hx0) // 2 * 2, (hy1 - hy0) // 2 * 2
                crop = (cw_, ch_, hx0, hy0)
                inside = [l for _, L in samp for l in L
                          if hx0 <= l["box"][0] * 1.5 and l["box"][2] * 1.5 <= hx1 and hy0 <= l["box"][1] * 1.5 and l["box"][3] * 1.5 <= hy1]
                burned = "real" if any(REAL_RX.search(l["text"]) for l in inside) else \
                    "ai" if any(AI_RX.search(l["text"]) for l in inside) else None
                ev["burned_label"] = burned
            if crop:
                c0, c1 = landed_range(A, c0, c1, fps, hole, img.shape[1])
            prep.append(dict(out=out, beat=beat, c0=c0, c1=c1, x=None, crop=crop))
            media[key] = ("vid", out, 0.0)
            ev["source"] = (f"his master {c0:.3f}-{c1:.3f} s (his transitions trimmed)"
                            + (f", the picture inside his card {crop}" if crop else "") + ", lifted into the olive card")
        still = is_still(B, D, s0, s1, bbox)
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
            beat["label_kind"] = "ai"
            if still:
                beat["caps"] = False                 # an AI picture held still (his goal image): the picture is the point
            elif top is not None and re.search(r"(^|[^a-z])dan([^a-z]|$)", os.path.basename(top[1]).lower()):
                beat["caps"] = False                 # an AI clip OF DAN is a labelled picture of Dan (Ad 8 58.6 / 142.8 s:
                                                     # captions ran under "fat Dan sees ripped Dan" beside its chip)
            ev["label"] = "AI label: the matched file lives in an AI-generated library"
        elif prov == "real":
            ev["label"] = "no label: real footage (the real-picture label is for still photos of his physique)"
        elif still:
            # REAL vs AI is never a model's call (a Flash classifier read three of Ad 1's AI clips as real at 0.95);
            # the model only answers "is this a physique?", and a physique still with no provenance escalates
            if is_physique(AI, fp, ev) is False:
                ev["label"] = "no label: a still that is not a physique picture, no provenance"
            else:
                esc.append(dict(t0=t0, t1=t1, what="a physique still with no provenance: which library file is it (real or AI)?"))
                conf = "low"
        else:
            ev["label"] = "carried as his approved master shows it: motion, no provenance, no label in his master"
            conf = "medium"
    beat["media"] = key
    ev["confidence"] = conf
    ev["provenance"] = prov
    return beat, ev


_PHYS = {}


def is_physique(AI, fp, ev):
    """The ONE picture question a model is asked: does it show a bare male torso? True / False / None (unsure)."""
    if fp in _PHYS:
        ev["ai_answer"] = _PHYS[fp]
        ans = _PHYS[fp]
        return None if not ans or ans.get("confidence", 0) < 0.8 else ans.get("answer") == "physique"
    ans = _PHYS[fp] = AI.classify_picture(fp, "This is a frame of a fitness ad. Does the main picture show a man's bare torso or "
                                  "physique (shirtless, abs or chest visible)?", ["physique", "not_physique"])
    ev["ai_answer"] = ans
    if not ans or ans.get("confidence", 0) < 0.8:
        return None
    return ans.get("answer") == "physique"


_MCACHE = {}


def is_still(B, D, s0, s1, bbox):
    """A still (a photo, maybe pushed in slowly) vs motion: align the shot's frames at 20 % and 80 % with an affine
    ECC fit on the 256x144 master cache; a still leaves almost nothing once the push is taken out."""
    path = os.path.join(B, "auto", "m256.rgb")
    if path not in _MCACHE:
        n = os.path.getsize(path) // (256 * 144 * 3)
        _MCACHE[path] = np.memmap(path, np.uint8, "r").reshape(n, 144, 256, 3)
    M = _MCACHE[path]
    a, b = s0 + int(0.2 * (s1 - s0)), s0 + int(0.8 * (s1 - s0))
    if b - a < 3:
        return True
    x0, y0, x1, y1 = (0, 0, 1920, 1080) if bbox is None else bbox
    sl = (slice(int(y0 / 7.5) + 2, max(int(y0 / 7.5) + 6, int(y1 / 7.5) - 2)), slice(int(x0 / 7.5) + 2, max(int(x0 / 7.5) + 6, int(x1 / 7.5) - 2)))
    g0 = cv2.cvtColor(np.ascontiguousarray(M[a]), cv2.COLOR_RGB2GRAY)[sl].astype(np.float32)
    g1 = cv2.cvtColor(np.ascontiguousarray(M[b]), cv2.COLOR_RGB2GRAY)[sl].astype(np.float32)
    if g0.size < 400:
        return True
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        _, warp = cv2.findTransformECC(g0, g1, warp, cv2.MOTION_AFFINE,
                                       (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5), None, 5)
    except cv2.error:
        return False
    w1 = cv2.warpAffine(g1, warp, (g1.shape[1], g1.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    m = 4
    res = float(np.abs(w1[m:-m, m:-m] - g0[m:-m, m:-m]).mean())
    return res < 5.0


def write_assets(B, master, media, prep):
    os.makedirs(os.path.join(B, "assets_auto"), exist_ok=True)
    for q in prep:
        if q["out"] not in [v[1] for v in media.values() if v[0] == "vid"]:
            continue                                  # its beat was dropped (an entrance)
        p = os.path.join(B, q["out"])
        b = q["beat"]
        dur = b["t1"] - b["t0"]
        clen = max(1 / 29.97, q["c1"] - q["c0"])
        # his clean picture fills the beat: stretched gently when it is a little short (AV-07's food shot), else
        # its first / last clean frame holds -- never his transition, never his next shot
        stretch = min(1.30, max(1.0, dur / clen))
        lead = max(0.0, q["c0"] - b["t0"]) if stretch * clen < dur else 0.0
        tail = max(0.25, dur - lead - stretch * clen + 0.25)
        vf = (f"crop=608:1080:{q['x']}:0," if q["x"] is not None else "") + \
             ("crop={}:{}:{}:{},".format(*q["crop"]) if q.get("crop") else "") + \
             f"setpts={stretch:.4f}*(PTS-STARTPTS),tpad=start_mode=clone:start_duration={lead:.3f}:stop_mode=clone:stop_duration={tail:.3f}"
        # FRAME-EXACT: seek half a frame early and take exactly the clean frames (a time seek + duration let his next
        # shot's first frame in: Ad 8 122.09 s, the vcutdown lesson)
        f0 = int(round(q["c0"] * 30000 / 1001)); nf = max(1, int(round(q["c1"] * 30000 / 1001)) - f0)
        run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{(f0 - 0.5) * 1001 / 30000:.6f}", "-i", master, "-an",
             "-vf", f"trim=end_frame={nf}," + vf, "-r", "30000/1001", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
             "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", p])
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
