#!/usr/bin/env python3
"""THE 1:1 SQUARE OF A SOFT BLUE LIGHT VERTICAL BUILD (first built for Ad 6, AS-04, 2026-10-02).

A square is a re-layout of the locked vertical, never a new edit: the same beat sheet, picture cuts, face track, push
schedule, flashes, caption states and audio stream. Only the geometry changes. Reads the vertical build B (which must
have reached `mux`) and writes everything into its own folder Q; nothing in B is touched.

  python3 sq_render.py fit      --build B --out Q [--copy Q/sq_copy.json]   every picture: fill or card, crop, label
  python3 sq_render.py graphics --build B --out Q                           every graphic and card plate at 1080x1080
  python3 sq_render.py picture  --build B --out Q [--range A B]             the film (or a span) -> Q/picture.mp4
  python3 sq_render.py mux      --build B --out Q --vertical V.mp4 --name "<title> | claude | 1x1 | ad N"

THE RULE (Dan, 2026-10-02, VIDEO-RULES top section): a clip or photo FILLS the square. It goes in a card on the field
only for a reason: filling would cut something that matters, it is a phone screen, or a required label has no clear
spot. Every card's reason is written to Q/sq_fit.json and printed.

THE COPY FILE (editorial, Q/sq_copy.json): {"pictures": {"<media key>": {"fit": "fill", "start": 0.25} |
{"fit": "fill", "oy": 0.8} | {"fit": "card", "reason": "..."}, ...}}.
`start` is the left edge of the 1:1 window as a fraction of a 16:9 clip's width (the window is 0.5625 wide). An
editor's lift that carries his burned AI chip (x 0.05..0.24) takes start <= 0.04 (his chip whole, ours not added) or
start >= 0.245 (his chip out, ours placed by measurement): never half of it, never both ("his_chip": true marks the
first case). Without an entry: a phone and a still photo go in a card, a clip fills from its centre.

Geometry: the talking head is a 1080x1080 window of the 1080p conform at 1.00x (no upscale), on the vertical's own
track centre, with the vertical's push schedule. Lower thirds, the 3A card and the CTA sit at the bottom
(hyperframes/square.py). Captions are the vertical's own states moved to y 880, lifted above a side card, paused under
a lower third or a CTA. A card under running captions ends above y 848.
"""
import argparse, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image

HERE = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16'   # Ad 10 build-local copy: the kit folder, for the shared imports
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".claude/skills/_shared/hyperframes"))
sys.path.insert(0, os.path.join(REPO, ".claude/skills/_shared"))
import square as SQM  # noqa: E402
import composite as CP  # noqa: E402
SQ = SQM.SQ
FF, FPS = CP.FF, CP.FPS
S = 1080
WIN = S / 1920                                   # the 1:1 window of a 16:9 clip, as a fraction of its width
CAP_Y, LIFT_GAP, LIFT_MIN = 880, 150, 560
REAL, AI = "Real picture of me - not AI-generated", "AI-GENERATED"
PUSH_UP = 85.0                                   # render.py: his punch recentres 85 px up in the 1080 source


def run(c, **k): subprocess.run(c, check=True, **k)


class Build:
    """The vertical build, read-only."""
    def __init__(self, B, Q):
        self.B, self.Q = os.path.abspath(B), os.path.abspath(Q)
        os.makedirs(self.Q, exist_ok=True)
        os.chdir(self.B); sys.path.insert(0, self.B)
        import render as R, beats
        self.R, self.beats = R, beats
        self.MEDIA = R.MEDIA
        self.P, _ = R.plan()                     # [(beat, frames)] : the vertical's own frame grid
        # sq_copy "beat_frames": {"<picture index>": frames}: re-cut the boundary between two pictures on the square. Ad 10: the editor's
        # beach clip ends at full frame 5169 and his phone screen starts 10 frames before the vertical's card grid says, so the beach
        # beat is 91 frames and the phone card starts at 5170 (the vertical's own cut), never a frozen beach picture under the speech
        _cp0 = os.path.join(self.Q, "sq_copy.json")
        _bf = (json.load(open(_cp0)) if os.path.exists(_cp0) else {}).get("beat_frames", {})
        if _bf:
            _pics = [i_ for i_, (b_, k_) in enumerate(self.P) if b_["kind"] in ("card", "bleed")]
            for pi_, fr_ in _bf.items():
                i_ = int(pi_); b_, k_ = self.P[i_]; self.P[i_] = (b_, int(fr_))
        # sq_copy "extra_pushes": [[a1, a2, b1, b2], ...]: a square-only punch-in laid on a pause splice that the vertical's
        # 608 px window hides and the 1080 px square window shows (the same recipe as the vertical's own pushes)
        _cp = os.path.join(self.Q, "sq_copy.json")
        for row_ in (json.load(open(_cp)) if os.path.exists(_cp) else {}).get("extra_pushes", []):
            beats.PUSHES.append(tuple(row_))
        self.starts, n = [], 0
        for b, k in self.P:
            self.starts.append(n); n += k
        self.N = n
        cp = os.path.join(self.Q, "sq_copy.json")
        self.copy = (json.load(open(cp)) if os.path.exists(cp) else {}).get("pictures", {})
        self.copy_gfx = (json.load(open(cp)) if os.path.exists(cp) else {}).get("graphics", {})
        # sq_copy "media": {"key": ["vid", path, start, ...]}: a square-only source for one picture. The vertical's
        # renderer multiplies the editor's soft vignette onto full-frame clips, so a clip pre-compensated for it there
        # (Ad 6's plank) must be the plain graded file here, where no vignette is applied
        for k_, v_ in ((json.load(open(cp)) if os.path.exists(cp) else {}).get("media", {})).items():
            R.MEDIA[k_] = tuple(v_)
        fp = os.path.join(self.Q, "sq_fit.json")
        self.fit = json.load(open(fp)) if os.path.exists(fp) else {}

    def pictures(self):
        return [(i, b, k, self.starts[i]) for i, (b, k) in enumerate(self.P) if b["kind"] in ("card", "bleed")]

    def opts(self, key):
        s = self.MEDIA[key]
        return dict(s[4]) if len(s) > 4 and isinstance(s[4], dict) else {}

    def src_wh(self, key):
        p = self.MEDIA[key][1]
        if self.MEDIA[key][0] == "img":
            from PIL import ImageOps
            return ImageOps.exif_transpose(Image.open(p)).size
        o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0:s=x", p], capture_output=True, text=True).stdout.strip().split("\n")[0]
        w, h = (int(x) for x in o.split("x")[:2]); return w, h

    def decide(self, b):
        """fill or card for one picture beat, with the crop and (for a card) the reason."""
        key = b["media"]; c = dict(self.copy.get(key, {}))
        w, h = self.src_wh(key); ar = w / h
        lab = {"real": REAL, "ai": AI}.get(b.get("label_kind"))
        if not c:
            if b.get("phone"):
                c = dict(fit="card", reason="a phone screen: it stays whole")
            elif self.MEDIA[key][0] == "img":
                c = dict(fit="card", reason="a portrait photo: a square window would cut his head or his abs" if ar < 0.9
                         else "a wide photo: a square window would cut its sides")
            else:
                c = dict(fit="fill")
        if c["fit"] == "fill":
            if ar > 1.0:
                st = c.get("start", (1 - WIN) / 2)
                c["ox"], c["oy"] = round(st / (1 - WIN), 4), 0.5
            else:
                c["ox"], c["oy"] = 0.5, c.get("oy", 0.5)
            if c.get("his_chip"):
                lab = None                                           # his burned chip is whole inside the window: never both
        else:
            assert c.get("reason"), f"{key}: a card needs its reason (Dan, 2026-10-02: no boxes without a reason)"
            c["ar"] = self.opts(key).get("ar_sq") or (ar if not self.opts(key).get("ar") else ar)   # the WHOLE picture, its own shape
        c["label"] = lab; c["caps"] = b.get("caps") is not False; c["phone"] = bool(b.get("phone"))
        return c

    def media_chain(self, key, w, h, nfr, ox, oy):
        R = self.R
        if self.MEDIA[key][0] == "img":
            # a 3.8 % push over 3 s moves about half a pixel per frame: zoompan rounds that to whole pixels and the picture steps every
            # other frame (the independent review saw 15 fps judder on the AI pool picture). Pushed at 2x and scaled down, the steps are
            # half as big and land on every frame.
            return R.media_input(key, nfr), R.still_chain(2 * w, 2 * h, nfr, amt=0.04, ox=ox, oy=oy) + f",scale={w}:{h}:flags=lanczos"
        # sq_copy "trim_bars": N: the editor's AI lifts carry N px of black at the top and the bottom of the 1080p frame (measured
        # 4 px on every AI clip of Muhammad's master); cropped off, never stretched (kit README, Ad 6 lessons)
        tb = int((self.copy.get(key) or {}).get("trim_bars", 0))
        trim = f"crop=iw:ih-{2 * tb}:0:{tb}," if tb else ""
        return R.media_input(key, nfr), "setpts=PTS-STARTPTS," + R.media_prefix(key) + trim + R.cover_chain(w, h, ox=ox, oy=oy)

    def media_frames(self, key, w, h, nfr, ox=0.5, oy=0.5):
        """nfr RGB frames of the picture, cover-cropped to w x h exactly as the vertical times it (start, rate, push)."""
        ins, chain = self.media_chain(key, w, h, nfr, ox, oy)
        p = subprocess.Popen([FF, "-v", "error"] + ins + ["-vf", chain + ",scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                              "-r", "30000/1001", "-frames:v", str(nfr), "-f", "rawvideo", "-"], stdout=subprocess.PIPE, cwd=self.B)
        size = w * h * 3; last = None
        # sq_copy "hold_from": N: a lift of the editor's master whose frames from N on belong to the NEXT shot (the master's own
        # cut falls before the beat's last frame); the picture holds its frame N-1 from there
        hold = (self.copy.get(key) or {}).get("hold_from")
        for k_ in range(nfr):
            buf = p.stdout.read(size)
            if hold is not None and k_ >= hold: yield last; continue
            if len(buf) == size: last = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
            if last is None: raise SystemExit(f"{key}: no frames")
            yield last                                                # a clip that ends early holds its last frame
        p.kill(); p.stdout.close(); p.wait()


# ------------------------------------------------------------------------------------------------ fit + labels
def cmd_fit(X):
    """Decide every picture, then place our chip on every labelled FILL by measuring the person on its square frames
    (kit_labels' own search and with-the-chip validation, on a 1080x1080 canvas). A fill whose chip has no clear spot
    becomes a card, with that as its reason."""
    import kit_labels as L
    L.SBL = True; L.VW = L.VH = S; L.TOP_SAFE = 64; L.PERSON_ONLY = True
    out = {}
    for i, b, nfr, g0 in X.pictures():
        key = b["media"]; c = X.decide(b)
        if c["fit"] == "fill" and c["label"]:
            L.CHIP_BOTTOM_MAX = 836 if c["caps"] else 1010
            d = os.path.join(X.Q, "labels", f"{i:03d}_{key}"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
            vid = os.path.join(d, "fill.mp4")
            enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S}x{S}", "-r", CP.FPSS, "-i", "-",
                                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
            for f in X.media_frames(key, S, S, nfr, c["ox"], c["oy"]): enc.stdin.write(f.tobytes())
            enc.stdin.close(); enc.wait()
            idxs = sorted(set(list(range(0, nfr, 3)) + [nfr - 1]))
            os.chdir(X.Q)
            fs, ms = L.masks_for(vid, idxs, os.path.join("labels", f"_m_{i:03d}"))
            union = np.any(ms, axis=0)
            got, tried = None, []
            if union.sum() < 2000:                                    # nobody in the picture (food, hands): top left, above the captions
                w_, h_ = L.chip_dims(c["label"], 1, 40)
                got = dict(x=40, y=64, lines=1, size=40, w=w_, h=h_, note="no person in the picture")
            else:
                hb = L.head_box(union)
                allc = [q for q in L.candidates(c["label"], union, hb) if q["x"] + q["w"] <= S - 60]
                # sq_copy "prefer": [[x, y, lines, size], ...]: placements measured on an earlier build are tried first,
                # under the same validation (the segmenter's verdict on one spot flips between near-identical renders)
                pref = []
                for x_, y_, ln_, sz_ in c.get("prefer") or []:
                    w_, h_ = L.chip_dims(c["label"], ln_, sz_)
                    pref.append(dict(cls="P", lines=ln_, size=sz_, x=x_, y=y_, w=w_, h=h_))
                # one line for the AI chip, up to three for the real-picture chip; bigger type first within a class
                for q in pref + [q for q in allc if q["cls"] == "A"][:6] + [q for q in allc if q["cls"] == "B"][:12] + [q for q in allc if q["cls"] == "C"][:12]:
                    contact = L.validate(c["label"], q, list(fs), f"sq{i:03d}")
                    tried.append([q["cls"], q["size"], q["x"], q["y"], contact])
                    if contact == 0: got = q; break
                    if q.get("contact_at_2x_verify_px", 1) == 0 and got is None: got = dict(q, note="clear at 16 px; contact only at the 24 px margin")
            os.chdir(X.B)
            if got:
                png = os.path.join(X.Q, "labels", f"chip_{i:03d}_{key}.png")
                L.chip_at(c["label"], got["x"], got["y"], got.get("lines", 1), got["size"]).save(png)
                c.update(chip_png=png, chip_box=[got["x"], got["y"], got["w"], got["h"]], chip_size=got["size"], chip_note=got.get("note"))
            else:
                c = dict(fit="card", reason="the required label has no clear spot on the filled frame (the person fills it)", label=c["label"],
                         caps=c["caps"], phone=False, ar=X.src_wh(key)[0] / X.src_wh(key)[1], tried=tried[:10])
            shutil.rmtree(os.path.join(X.Q, "labels", f"_m_{i:03d}"), ignore_errors=True)
            os.remove(vid)
        out[str(i)] = dict(c, media=key, t0=b["t0"], t1=b["t1"])
        print(f"{i:3d} {b['t0']:7.2f} {key:12s} {c['fit']:4s} {('label ' + str(c.get('chip_box'))) if c.get('chip_png') else (c.get('reason') or ('his burned chip' if X.copy.get(key, {}).get('his_chip') else ''))}", flush=True)
    json.dump(out, open(os.path.join(X.Q, "sq_fit.json"), "w"), indent=1)
    n = sum(1 for v in out.values() if v["fit"] == "fill")
    print(f"{n} of {len(out)} pictures fill the square; {len(out) - n} cards -> sq_fit.json")


# ------------------------------------------------------------------------------------------------ graphics
def cmd_graphics(X):
    """Every graphic of the film at 1080x1080 from the vertical's own configs and times, and one plate per card."""
    hf = os.path.join(X.Q, "hf")
    sheet = json.load(open(os.path.join(X.B, "sbl_sheet.json")))
    J = json.load(open(os.path.join(X.B, "beats.json")))
    kt = {m["id"]: (m["a"], m["b"]) for m in json.load(open(os.path.join(X.B, "hf", "manifest.json")))}
    for b in J["beats"]:
        if b.get("kind") == "hf": kt[b["gid"]] = (b["t0"], b["t1"])
    man = []
    for g in sheet["graphics"]:
        ta, tb = kt.get(g["id"], (g["t0"], g["t1"]))
        # sq_copy "graphics": {"L12": {"a": 130.915}}: a square-only start or end for one graphic. A lower third sits
        # at the BOTTOM of a square, so one that arrives over a tall card (the phone held up, Ad 6 2:08) would force
        # the card small; starting it with the next picture keeps the card large
        ov = X.copy_gfx.get(g["id"], {})
        ta, tb = float(ov.get("a", ta)), float(ov.get("b", tb))
        g = dict(g, t0=ta, t1=tb, config=dict(g["config"], a=ta, b=tb))
        if ov and g["config"].get("parts"):               # a part whose word is before the new start rises as the graphic lands
            g["config"]["parts"] = [[p_[0], max(float(p_[1]), ta + 0.35)] if len(p_) > 1 else p_ for p_ in g["config"]["parts"]]
        if g["template"] == "before-card" or g["template"].startswith("softblue:"):
            g["config"]["a"], g["config"]["b"] = CP.fr(ta) / FPS, CP.fr(tb) / FPS
        scenes, meta = SQ.scenes_for(g)
        SQ.build(scenes, hf, render=True)
        m = dict(id=g["id"], template=g["template"], a=ta, b=tb, mov=os.path.join(hf, "renders", g["id"] + ".mov"), **meta)
        if meta["kind"] == "glass": m["mask"] = os.path.join(hf, "renders", g["id"] + "_mask.mov")
        man.append(m); print(g["id"], g["template"], meta["kind"], flush=True)
    json.dump(man, open(os.path.join(X.Q, "manifest.json"), "w"), indent=1)
    plates = {}
    # a card under a bottom graphic (lower third, CTA, side card) ends above it, chip included: the "MY LOCK SCREEN"
    # lower third sat over the phone card's AI chip (Ad 6 square judge 2, 2:08). Back-to-back cards of ONE clip share
    # the smallest such end, or the card shrinks in one frame while the same shot plays on (judge 2, round 2, 2:07.995)
    ends, runs, prev = {}, [], None
    for i, b, nfr, g0 in X.pictures():
        if X.fit[str(i)]["fit"] != "card": prev = None; continue
        ov = [m["box"][1] for m in man if m["kind"] in ("glass", "overlay") and m.get("box") and m["a"] < b["t1"] and m["b"] > b["t0"]]
        ends[i] = (min(ov) - 24) if ov else None
        same = prev is not None and abs(prev[1]["t1"] - b["t0"]) < 0.05 and X.MEDIA[prev[1]["media"]][1] == X.MEDIA[b["media"]][1]
        if same: runs[-1].append(i)
        else: runs.append([i])
        prev = (i, b)
    for run in runs:
        es = [ends[i] for i in run if ends[i] is not None]
        for i in run:
            ends[i] = min(es) if es else None
    for i, b, nfr, g0 in X.pictures():
        c = X.fit[str(i)]
        if c["fit"] != "card": continue
        gid = f"sqcard_{i:03d}_{b['media']}"
        over = [ends[i]] if ends[i] is not None else []
        keep = SQM.CARD_END
        if over:
            SQM.CARD_END = over[0]
        try:
            scene, hole = SQM.media_card_scene(gid, nfr / FPS + 0.2, c["ar"], label=c["label"], kicker="AbsByAI.com" if c["phone"] else None,
                                               caps=c["caps"] or bool(over))
        finally:
            SQM.CARD_END = keep
        SQ.build([scene], hf, render=True)
        plates[str(i)] = dict(mov=os.path.join(hf, "renders", gid + ".mov"), hole=hole, chip=scene[1].get("chip"))
        print(gid, hole, flush=True)
    json.dump(plates, open(os.path.join(X.Q, "plates.json"), "w"), indent=1)


# ------------------------------------------------------------------------------------------------ the picture
def cmd_picture(X, rng=None, out=None, cut=False):
    """The film (or --range span) -> Q/picture.mp4. cut=True: the <=0:59 cutdown -> Q/cut_picture.mp4, the same frames the
    vertical cutdown took (B/cut_plan.json, frame for frame) drawn the square way, under the vertical cutdown's own
    caption track (B/cut/captions.mov: re-grouped at the seams, so no caption carries a word the cut removed)."""
    R, beats = X.R, X.beats
    man = json.load(open(os.path.join(X.Q, "manifest.json")))
    plates = json.load(open(os.path.join(X.Q, "plates.json")))
    g0, g1 = (CP.fr(rng[0]), min(X.N, CP.fr(rng[1]))) if rng else (0, X.N)
    if cut:
        cp_ = json.load(open(os.path.join(X.B, "cut_plan.json")))
        assert all(not r.get("hold") for r in cp_["ranges"]), "a held range: not drawn by the square cut yet"
        FRAMES = [r["n0"] + k for r in cp_["ranges"] for k in range(r["frames"])]
    else:
        FRAMES = list(range(g0, g1))
    man_ = man if cut else [m for m in man if CP.fr(m["a"]) < g1 and CP.fr(m["b"]) > g0]
    C = CP.Compositor(man_, wh=(S, S))
    cards = [(m["a"], m["b"], m["box"][1]) for m in man if m["kind"] == "overlay"]
    glass = [(CP.fr(m["a"]), CP.fr(m["b"])) for m in man if m["kind"] == "glass"]
    FL = [(CP.fr(a), CP.fr(b)) for a, b in getattr(beats, "FLASHES", [])]
    _fl = {}

    def flash(frame, g):
        import vlib
        for f0, f1 in FL:
            if f0 <= g < f1:
                if (f0, f1) not in _fl:
                    fr_, _ = vlib.overlay_flash((f1 - f0) / FPS)
                    _fl[(f0, f1)] = [np.asarray(x.resize((S, S)))[..., 3:4].astype(np.float32) / 255 for x in fr_]
                al = _fl[(f0, f1)][min(g - f0, len(_fl[(f0, f1)]) - 1)]
                frame = (frame.astype(np.float32) * (1 - al) + np.array([244, 250, 255], np.float32) * al + 0.5).astype(np.uint8)
        return frame

    def talk(bf, g):
        """The 1080 window of the conform: the vertical's track centre, its push (smoothstep, recentred up), at 1.00x base."""
        # THE CUT'S OWN FRAME: a picture cut's time sits between frames (88.3968 s = frame 2649.26), and the conform
        # shows the new shot from frame round(cut * FPS). Sampled at g / FPS, that first frame read the OUTGOING shot's
        # crop and zoom, a one-frame twitch after the cut (59.09, 82.05, 86.35, 88.39 s, Ad 6 square judge 1). The
        # time is clamped into the segment the frame belongs to by rounding.
        t = g / FPS
        for sa, sb in SEGF:
            if sa[0] <= g < sb[0]:
                t = min(max(t, sa[1] + 1e-4), sb[1] - 1e-4)
                break
        z = beats.push_at(t)
        cx = R._x_at(t) + R.CROP_W / 2
        w = S / z
        x0 = min(1920 - w, max(0.0, cx - w / 2))
        y0 = max(0.0, (1080 - w) / 2 - PUSH_UP * (z - 1) / max(1e-6, beats.PUSH_Z - 1))
        if z <= 1.0005:
            xi = int(round(x0)); return np.ascontiguousarray(bf[:, xi:xi + S])
        return np.asarray(Image.fromarray(bf).resize((S, S), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + w)))

    # sq_copy "mute_caption_frames": [[a, b], ...] (full-film frames, inclusive): the vertical's caption layer still carries the last frames of a
    # line over a picture change; where the square's new card starts first, the line is not drawn (the phone card at 2:52.5 had "years younger."
    # printed over its first five frames)
    _cpm = os.path.join(X.Q, "sq_copy.json")
    MUTE_F = [tuple(r_) for r_ in (json.load(open(_cpm)) if os.path.exists(_cpm) else {}).get("mute_caption_frames", [])]
    CAPS = os.path.join(X.B, "cut", "captions.mov") if cut else os.path.join(X.B, "captions.mov")
    caps = CP.reader(CAPS, start=0 if cut else g0, n=len(FRAMES), rgba=True, wh=(1080, 1920))
    _bs = {"it": None, "next": None}

    def base_frame(g):                            # sequential reads, re-opened where the cut jumps
        if _bs["next"] != g:
            _bs["it"] = CP.reader(os.path.join(X.B, "base.mp4"), start=g, wh=(1920, 1080))
        _bs["next"] = g + 1
        return next(_bs["it"])
    out = out or os.path.join(X.Q, "cut_picture.mp4" if cut else "picture.mp4")
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S}x{S}", "-framerate", "30000/1001", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "12", "-preset", "medium",
                            "-profile:v", "high", "-maxrate", "12M", "-bufsize", "24M", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-video_track_timescale", "30000", "-an", out], stdin=subprocess.PIPE)
    pics = {i: (b, n, s) for i, b, n, s in X.pictures()}
    SEGF = [((int(round(sa * FPS)), sa), (int(round(sb * FPS)), sb)) for sa, sb in R._SEGS]   # picture segments by frame
    NOCAP = np.zeros((1920, 1080, 4), np.uint8)
    CAP_N = int(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries',
                                'stream=nb_read_packets', '-of', 'csv=p=0', CAPS], capture_output=True, text=True).stdout.strip() or 0)
    cur = None                                     # (beat index, media iterator, plate iterator, fit, chip rgba)
    cap_states = []                                # what the square actually drew: [g, y] per captioned frame (for the plan)
    bi = 0; prev_g = None
    for k_out, g in enumerate(FRAMES):
        bi = max(i for i, s0 in enumerate(X.starts) if s0 <= g)
        if prev_g is not None and g != prev_g + 1:
            cur = None                             # a seam: the picture iterators restart where the next range opens
        prev_g = g
        bf = base_frame(g); cf = next(caps, None)
        if cf is None:                             # the caption track ends at its last caption (the closing button has none)
            if k_out < CAP_N: raise SystemExit(f'captions.mov stopped at frame {g} of {CAP_N}: was it rewritten during the render?')
            cf = NOCAP
        t = g / FPS
        pic = bi in pics
        if pic:
            if cur is None or cur[0] != bi:
                b, n, s = pics[bi]; c = X.fit[str(bi)]; skip = g - s
                if c["fit"] == "fill":
                    it = X.media_frames(b["media"], S, S, n, c["ox"], c["oy"]); pl = None
                    chip = np.asarray(Image.open(c["chip_png"]).convert("RGBA")) if c.get("chip_png") else None
                else:
                    x0, y0, x1, y1 = plates[str(bi)]["hole"]
                    it = X.media_frames(b["media"], x1 - x0, y1 - y0, n, 0.5, 0.0 if X.MEDIA[b["media"]][0] == "img" else 0.5)
                    pl = CP.reader(plates[str(bi)]["mov"], rgba=True, wh=(S, S)); chip = None
                for _ in range(skip):
                    next(it); pl and next(pl)
                cur = (bi, it, pl, c, chip)
            _, it, pl, c, chip = cur
            mf = next(it)
            if c["fit"] == "fill":
                fr_ = mf if chip is None else CP.over(mf, chip)
            else:
                x0, y0, x1, y1 = plates[str(bi)]["hole"]
                bg = np.zeros((S, S, 3), np.uint8); bg[y0:y1, x0:x1] = mf
                fr_ = CP.over(bg, next(pl))
        else:
            fr_ = talk(bf, g)
        fr_ = C.apply(np.ascontiguousarray(fr_), g)
        # captions: the vertical's own caption states at the square line; lifted above a side card; paused under glass
        al = cf[..., 3]
        if al.max() > 8 and not any(a_ <= g < b_ for a_, b_ in glass) and not C.opaque(g) and not any(a_ <= g <= b_ for a_, b_ in MUTE_F):
            rows = np.where(al.max(axis=1) > 8)[0]
            band = cf[rows[0]:rows[-1] + 1]
            # LIFTED EXACTLY WHEN THE VERTICAL LIFTED IT. The vertical decides per caption line (captions.py CAP_LIFTS),
            # so a line never moves while it is on screen. Deciding per frame from the card's own times moved a word up
            # mid-word where the card arrived ("seconds." hop at 2:42.7; the cutdown's captions:sync read the second
            # half 472 ms late). The vertical's lifted line sits well above its normal one (row 1067 against 1400+).
            if rows[0] < 1250 and cards:
                cy = min(cards, key=lambda c_: 0.0 if c_[0] <= t < c_[1] else min(abs(t - c_[0]), abs(t - c_[1])))[2] - LIFT_GAP
            else:
                cy = CAP_Y
            if cy >= LIFT_MIN and cy + band.shape[0] <= S:
                yy = int(cy)
                reg = fr_[yy:yy + band.shape[0]].astype(np.float32); al_ = band[..., 3:4].astype(np.float32) / 255
                fr_ = fr_.copy(); fr_[yy:yy + band.shape[0]] = (reg * (1 - al_) + band[..., :3].astype(np.float32) * al_ + 0.5).astype(np.uint8)
                cols = np.where(band[..., 3].max(axis=0) > 8)[0]
                cap_states.append([k_out if cut else g, yy, int(rows[0]), int(cols[0]), int(cols[-1]) + 1, int(band.shape[0])])
        enc.stdin.write(np.ascontiguousarray(flash(fr_, g)).tobytes())
        if k_out % 600 == 0: print(f"frame {k_out} / {len(FRAMES)}", flush=True)
    enc.stdin.close(); enc.wait()
    if enc.returncode: raise SystemExit("encode failed")
    if not rng:
        json.dump(cap_states, open(os.path.join(X.Q, "cap_drawn_cut.json" if cut else "cap_drawn.json"), "w"))
    print(out, "done:", len(FRAMES), "frames")


def cmd_mux(X, vertical, name, cut=False):
    """The vertical's audio stream, copied bit for bit (md5 asserted), under the square picture."""
    out = os.path.join(X.Q, name + ".mp4")
    run([FF, "-v", "error", "-y", "-i", os.path.join(X.Q, "cut_picture.mp4" if cut else "picture.mp4"), "-i", vertical, "-map", "0:v", "-map", "1:a", "-c", "copy",
         "-movflags", "+faststart", out])
    md5 = lambda p: subprocess.run([FF, "-v", "error", "-i", p, "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    a, b = md5(vertical), md5(out)
    assert a == b and a, f"audio stream differs from the vertical's: {a} vs {b}"
    print(out, "audio", a)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["fit", "graphics", "picture", "mux"])
    ap.add_argument("--build", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--range", nargs=2, type=float); ap.add_argument("--to")
    ap.add_argument("--vertical"); ap.add_argument("--name")
    ap.add_argument("--cut", action="store_true", help="picture/mux: the <=0:59 cutdown (the vertical's cut_plan.json)")
    a = ap.parse_args()
    X = Build(a.build, a.out)
    if a.cmd == "fit": cmd_fit(X)
    elif a.cmd == "graphics": cmd_graphics(X)
    elif a.cmd == "picture": cmd_picture(X, a.range, a.to, a.cut)
    else: cmd_mux(X, a.vertical, a.name, a.cut)


if __name__ == "__main__":
    main()
