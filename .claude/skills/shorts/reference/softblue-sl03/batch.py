#!/usr/bin/env python3
"""SL-03 round 2 batch builder (Soft Blue shorts). Run from /Volumes/Extreme/_edit_work/sl03 :
  batch.py audio S..   cut the MASTER's mix (15 ms de-click fades), write r2/S/audio.wav + his_mix.wav + timeline.json
  batch.py words S..   CTC-align plans.TEXT to the cut audio -> r2/S/words.json, cues.json
  batch.py plan  S..   the shot table (one row per picture shot) -> r2/S/shots.json
  batch.py track S..   face / hair track per talking shot (Vision, 4 fps) -> r2/S/track.json
  batch.py gfx   S..   key-point bars (HyperFrames lower third, content + glass mask) -> r2/S/hf/manifest.json
  batch.py proof S..   stills of every shot's window (start, middle, end) and every bar at its settled moment
  batch.py render S..  the short: r2/S/<name>.mp4 (+ source_picture.mp4 without graphics for the watch pass)
Picture: RAW rolls through the long-form's grade-B luts; talking shots follow the long-form's own audio map, so lip
sync is the roll's own. Audio: cut only. Look: GRAPHICS-STANDARDS.md, "Soft Blue shorts standard"."""
import json, os, re, subprocess, sys, wave, pathlib, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/Volumes/Extreme/_edit_work/sl03"
sys.path.insert(0, WORK); sys.path.insert(0, HERE)
import lib, plans as P
B = lib.B
FPS = 30000 / 1001; FPSS = "30000/1001"; SR = 48000
LF = "/Volumes/Extreme/_edit_work/ro05-fable/round4/full/"
W, H, DROP = 1080, 1920, 310
PIC_H = H - DROP
WIN = {"full": (724, 1080), "mid": (604, 900)}
PHONE_XY = (14, 322); DAN_BOX = (612, 345, 440, 1190); PHONE_ALONE_X = 228
def D(S): d = f"{WORK}/r2/{S}"; os.makedirs(d, exist_ok=True); return d
def fr(t): return int(round(t * FPS))
def A_pieces():
    A = json.load(open(LF + "timeline.json"))["A"]
    for a in A: a["end"] = a["at"] + (a["out"] - a["in"])
    return A

# ------------------------------------------------------------------ timeline: audio cuts and the picture's film time
def timeline(S):
    """audio ranges kept (film), and per output frame the film time the PICTURE shows (faster across a trimmed pause)."""
    cuts = []                                   # (film a, film b, picture film a, picture film b)
    for a, b in P.SEG[S]:
        cur = a
        for tr in P.TRIM.get(S, []):
            s, e = tr[0], tr[1]
            if a < s and e < b:
                keep = tr[3] if len(tr) > 3 else P.KEEP
                h = keep / 2; m = (s + e) / 2
                if len(tr) > 2 and tr[2] and (e - s) / keep > tr[2]:      # speed capped: the picture skips the middle (a size step hides it)
                    cuts.append((cur, s, cur, s)); cuts.append((s, s + h, s, s + h * tr[2])); cuts.append((e - h, e, e - h * tr[2], e))
                else:
                    cuts.append((cur, s, cur, s)); cuts.append((s, s + h, s, m)); cuts.append((e - h, e, m, e))
                cur = e
        cuts.append((cur, b, cur, b))
    seg, off = [], 0.0
    for a, b, pa, pb in cuts:
        seg.append(dict(a=a, b=b, pa=pa, pb=pb, o0=off, o1=off + (b - a))); off += b - a
    return seg, off
def film2out(seg, t):
    for s in seg:
        if s["a"] - 1e-6 <= t <= s["b"] + 1e-6 and s["a"] == s["pa"] and abs((s["b"] - s["a"]) - (s["pb"] - s["pa"])) < 1e-6: return s["o0"] + t - s["a"]
    for s in seg:
        if s["pa"] - 1e-6 <= t <= s["pb"] + 1e-6: return s["o0"] + (t - s["pa"]) * (s["o1"] - s["o0"]) / (s["pb"] - s["pa"])
    raise ValueError(f"film {t} not in the short")
def out2film_pic(seg, o):
    for s in seg:
        if s["o0"] - 1e-9 <= o < s["o1"]: return s["pa"] + (o - s["o0"]) * (s["pb"] - s["pa"]) / (s["o1"] - s["o0"])
    s = seg[-1]; return s["pb"]
def joins(seg):
    """audio joins on the output timeline (a real discontinuity in film time)."""
    return [round(s["o0"], 4) for i, s in enumerate(seg) if i and abs(s["a"] - seg[i - 1]["b"]) > 1e-6]

def cmd_audio(S):
    seg, total = timeline(S); d = D(S)
    w = wave.open(f"{WORK}/master_audio.wav"); assert w.getframerate() == SR and w.getnchannels() == 2
    parts, raw = [], []
    for i, s in enumerate(seg):
        n0 = int(round(s["a"] * SR)); n = int(round(s["o1"] * SR)) - int(round(s["o0"] * SR))
        w.setpos(n0); x = np.frombuffer(w.readframes(n), "<i2").astype(np.float32).reshape(-1, 2) / 32768
        raw.append(x.copy())
        first = i == 0 or abs(s["a"] - seg[i - 1]["b"]) > 1e-6; last = i == len(seg) - 1 or abs(seg[i + 1]["a"] - s["b"]) > 1e-6
        if first: k = int(0.015 * SR); x[:k] *= np.linspace(0, 1, k)[:, None]
        if last: k = int((0.04 if i == len(seg) - 1 else 0.015) * SR); x[-k:] *= np.linspace(1, 0, k)[:, None]
        parts.append(x)
    for name, xs in (("audio.wav", parts), ("his_mix.wav", raw)):
        o = wave.open(f"{d}/{name}", "w"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
        o.writeframes((np.clip(np.concatenate(xs), -1, 1) * 32767).astype("<i2").tobytes()); o.close()
    json.dump(dict(seg=seg, total=total, frames=fr(total), joins=joins(seg)), open(f"{d}/timeline.json", "w"), indent=1)
    # the bed under each join: how far the music jumps there (bed.wav is the long-form's music stem on the same clock)
    bw = wave.open(LF + "bed.wav"); bsr, bch = bw.getframerate(), bw.getnchannels()
    def lvl(t):
        bw.setpos(max(0, int((t - 0.15) * bsr))); x = np.frombuffer(bw.readframes(int(0.3 * bsr)), "<i2").astype(np.float32) / 32768
        return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-7)
    js = [(seg[i - 1]["b"], s["a"], s["o0"]) for i, s in enumerate(seg) if i and abs(s["a"] - seg[i - 1]["b"]) > 1e-6]
    print(S, f"{total:.2f} s, {fr(total)} frames; joins:", "  ".join(f"{o:.2f}s bed {lvl(a):.0f}->{lvl(b):.0f} dB" for a, b, o in js))

# ------------------------------------------------------------------ words: CTC alignment of the caption text
def tokens(S):
    """[(shown, spoken, piece index)] from plans.TEXT"""
    out = []
    for pi, part in enumerate(P.TEXT[S].split(" | ")):
        for tok in part.split():
            m = re.match(r"^(.*?)\{(.*)\}(.*)$", tok)
            shown, spoken = (m.group(1) + m.group(3), m.group(2)) if m else (tok, tok)
            out.append((shown, spoken, pi))
    # `{two words}` was split by whitespace: rejoin
    fixed, buf = [], None
    for part_i, part in enumerate(P.TEXT[S].split(" | ")):
        for m in re.finditer(r"(\S*?\{[^}]*\}\S*|\S+)", part):
            tok = m.group(1); mm = re.match(r"^(.*?)\{(.*)\}(.*)$", tok)
            fixed.append((mm.group(1) + mm.group(3), mm.group(2), part_i) if mm else (tok, tok, part_i))
    return fixed
def cmd_words(S):
    import torch, torchaudio, scipy.signal as ss
    d = D(S); T = json.load(open(f"{d}/timeline.json")); seg = T["seg"]
    w = wave.open(f"{d}/his_mix.wav"); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, 2).mean(1) / 32768
    a16 = ss.resample_poly(x, 16000, SR).astype(np.float32)
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H; model = bundle.get_model().eval(); L = {c: i for i, c in enumerate(bundle.get_labels())}
    toks = tokens(S); bounds = [0.0] + T["joins"] + [T["total"]]
    # the SEG pieces (plans.TEXT ' | ') are the audio joins that are not pause trims
    pj = [0.0]; acc = 0.0
    for a, b in P.SEG[S]:
        acc += (b - a) - sum((t[1] - t[0]) - (t[3] if len(t) > 3 else P.KEEP) for t in P.TRIM.get(S, []) if a < t[0] and t[1] < b); pj.append(acc)
    out = []
    for pi in range(len(P.SEG[S])):
        ws = [t for t in toks if t[2] == pi]; t0, t1 = pj[pi], pj[pi + 1]
        seg16 = torch.from_numpy(a16[int(t0 * 16000):int(t1 * 16000)]).unsqueeze(0)
        ids, owner = [], []
        for k, (_, spoken, _) in enumerate(ws):
            n = re.sub(r"[^A-Z' ]", "", re.sub(r"[-]", " ", spoken).upper()).strip()
            for ch in n.replace(" ", "|"):
                ids.append(L[ch]); owner.append(k)
            ids.append(L["|"]); owner.append(-1)
        ids, owner = ids[:-1], owner[:-1]
        with torch.inference_mode(): em, _ = model(seg16); em = torch.log_softmax(em, -1)
        ali, sc = torchaudio.functional.forced_align(em, torch.tensor([ids], dtype=torch.int32), blank=0)
        spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp()); ratio = seg16.shape[1] / em.shape[1] / 16000
        per = {}
        for ti, sp in enumerate(spans):
            k = owner[ti]
            if k < 0: continue
            a, b = t0 + sp.start * ratio, t0 + sp.end * ratio
            per.setdefault(k, [a, b, []]); per[k][1] = b; per[k][2].append(float(sp.score))
        for k, (shown, spoken, _) in enumerate(ws):
            assert k in per, (S, shown)
            out.append(dict(w=shown, t=round(per[k][0], 3), e=round(per[k][1], 3), p=pi, score=round(float(np.mean(per[k][2])), 2)))
    for i in range(1, len(out)):                                    # onsets monotonic
        if out[i]["t"] < out[i - 1]["t"] + 0.02: out[i]["t"] = round(out[i - 1]["t"] + 0.02, 3)
        out[i]["e"] = max(out[i]["e"], out[i]["t"] + 0.05)
    json.dump(out, open(f"{d}/words.json", "w"), indent=0)
    low = [f"{o['w']}@{o['t']:.2f}({o['score']})" for o in out if o["score"] < 0.35]
    print(S, len(out), "words aligned; low-confidence:", " ".join(low) or "none")
    cmd_cues(S)

def find_phrase(words, phrase, after=0.0):
    nz = lambda s: re.sub(r"[^a-z0-9$%]", "", s.lower())
    want = [nz(x) for x in phrase.split()]
    for i in range(len(words) - len(want) + 1):
        if words[i]["t"] >= after and all(nz(words[i + j]["w"]) == want[j] for j in range(len(want))): return i
    raise ValueError(f"phrase not found: {phrase!r}")

ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def cap_lines(text, size=86, maxw=960):
    f = ImageFont.truetype(ARIAL, size); d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    if d.textlength(text, font=f) <= maxw: return [text]
    ws = text.split(); best = None
    for k in range(1, len(ws)):
        a, b = " ".join(ws[:k]), " ".join(ws[k:]); m = max(d.textlength(a, font=f), d.textlength(b, font=f))
        if best is None or m < best[0]: best = (m, [a, b])
    assert best[0] <= 1040, text
    return best[1]
def cmd_cues(S):
    d = D(S); words = json.load(open(f"{d}/words.json")); T = json.load(open(f"{d}/timeline.json"))
    cues, cur = [], []
    def flush():
        if cur: cues.append(list(cur)); cur.clear()
    for i, w in enumerate(words):
        ends = bool(re.search(r"[.!?]$", w["w"])); n = len(" ".join(x["w"] for x in cur)) + len(w["w"])
        if cur and (w["p"] != cur[-1]["p"] or w["t"] - cur[-1]["e"] > 0.6 or (len(cur) >= 4 and not (ends and n <= 30)) or (n > 24 and not (ends and n <= 30))): flush()
        cur.append(w)
        if re.search(r"[.!?:]$", w["w"]) or (re.search(r",$", w["w"]) and len(cur) >= 2): flush()
    flush()
    # a one-word tail joins its neighbour when it fits
    out = []
    for c in cues:
        if out and len(c) == 1 and out[-1][-1]["p"] == c[0]["p"] and c[0]["t"] - out[-1][-1]["e"] < 0.4 and len(out[-1]) < 4 \
           and not re.search(r"[.!?]$", out[-1][-1]["w"]) and len(" ".join(x["w"] for x in out[-1])) + len(c[0]["w"]) <= 32: out[-1].extend(c)
        else: out.append(c)
    k = 0                                       # a lone word that does not end a sentence leads into the next cue
    while k + 1 < len(out):
        c, nx = out[k], out[k + 1]
        if len(c) == 1 and not re.search(r"[.!?,]$", c[0]["w"]) and nx[0]["p"] == c[0]["p"] and nx[0]["t"] - c[0]["e"] < 1.5 and len(nx) <= 4: out[k:k + 2] = [c + nx]
        else: k += 1
    # a cue never opens on a word the cue before it also says ("start doing what I'm | doing right here"): the gate, and a
    # reader, pair it with the first occurrence. Move the boundary one word earlier.
    nz = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    for k in range(1, len(out)):
        if out[k][0]["p"] == out[k - 1][-1]["p"] and len(out[k - 1]) > 2 and nz(out[k][0]["w"]) in [nz(x["w"]) for x in out[k - 1]]:
            out[k].insert(0, out[k - 1].pop())
    res = []
    for i, c in enumerate(out):
        a = c[0]["t"]; e = c[-1]["e"] + 0.30
        if i + 1 < len(out): e = min(e, out[i + 1][0]["t"]) if out[i + 1][0]["t"] - c[-1]["e"] > 0.30 else out[i + 1][0]["t"]
        for j in T["joins"]:
            if a < j < e: e = j
        e = min(e, T["total"] - 0.02); a = max(0.0, a - 0.03)
        if res and res[-1]["b"] > a: res[-1]["b"] = round(a, 3)
        if i + 1 < len(out): e = min(e, out[i + 1][0]["t"] - 0.03)
        txt = " ".join(x["w"] for x in c)
        if i == 0 or out[i - 1][-1]["p"] != c[0]["p"] or re.search(r"[.!?]$", out[i - 1][-1]["w"]): txt = txt[0].upper() + txt[1:]
        res.append(dict(a=round(a, 3), b=round(max(e, a + 0.2), 3), text=txt, lines=cap_lines(txt)))
    json.dump(res, open(f"{d}/cues.json", "w"), indent=0)
    print(S, len(res), "cues;", sum(len(r["lines"]) == 2 for r in res), "two-line")

# ------------------------------------------------------------------ shots
def cmd_plan(S, quiet=False):
    d = D(S); T = json.load(open(f"{d}/timeline.json")); seg = T["seg"]; N = T["frames"]; A = A_pieces()
    ot = lambda x: float(x[1:]) if isinstance(x, str) else film2out(seg, x)      # "o47.4" = an output time (inside a pause trim)
    covers = [(ot(c[0]), ot(c[1]), c) for c in P.COVERS[S]]
    rows, cur = [], None
    W_ = json.load(open(f"{d}/words.json")); cutf = []
    for k_, c_ in enumerate(seg[1:], 1):                                # a capped pause trim jumps in picture: always a shot change there
        if abs(c_["pa"] - seg[k_ - 1]["pb"]) > 1e-6 and abs(c_["a"] - seg[k_ - 1]["b"]) > 1e-6 and c_["pa"] != c_["a"]: cutf.append(fr(c_["o0"]))
    for ph, dt in P.SPLIT.get(S, []):                                  # a size step inside one continuous take, in the pause before a phrase
        if isinstance(ph, (int, float)): cutf.append(fr(ph)); continue   # or a picture-only step at an output time (audio untouched)
        k = find_phrase(W_, ph); assert W_[k]["t"] - W_[k - 1]["e"] >= 0.08, (S, ph, "no pause before it", W_[k]["t"] - W_[k - 1]["e"])
        cutf.append(fr((W_[k - 1]["e"] + W_[k]["t"]) / 2 + dt))
    for i in range(N):
        o = (i + 0.5) / FPS; f = out2film_pic(seg, o)
        cv = next((c for c in covers if fr(c[0]) <= i < fr(c[1])), None)
        if cv:
            c = cv[2]; key = ("broll", c[2], c[0]); roll = c[2]
            raw = c[3] + ((o - cv[0]) if isinstance(c[0], str) else (f - c[0])) * c[5]
        else:
            a = next((a for a in A if a["at"] - 1e-6 <= f < a["end"]), None)
            if a is None: a = max((a for a in A if a["at"] <= f), key=lambda a: a["at"])      # a gap in the long-form's audio map: the take runs on
            raw = a["in"] + (f - a["at"]); roll = a["roll"]; key = ("demo" if a["roll"] == P.DEMO_ROLL else "talk", a["roll"], round((raw - f) * 10), sum(i >= c for c in cutf))      # one shot per continuous run of the roll
        if cur is None or cur["key"] != key:
            cur = dict(key=key, kind=key[0], roll=roll, f0=i, raw=[]); rows.append(cur)
        cur["raw"].append(raw)
    shots = []
    for k, r in enumerate(rows):
        sh = dict(idx=k, kind=r["kind"], roll=r["roll"], f0=r["f0"], f1=r["f0"] + len(r["raw"]), raw0=round(r["raw"][0], 4), raw1=round(r["raw"][-1], 4), raw=[round(x, 4) for x in r["raw"]])
        shots.append(sh)
    # a few-frame sliver (a piece edge that runs a hair past a join) folds into its neighbour
    keep = []
    for sh in shots:
        if sh["f1"] - sh["f0"] < 8 and keep and sh["kind"] != "broll":
            p = keep[-1]; n = sh["f1"] - sh["f0"]; step = (p["raw"][-1] - p["raw"][-2]) if len(p["raw"]) > 1 else 1 / FPS
            p["raw"] += [round(p["raw"][-1] + step * (j + 1), 4) for j in range(n)]; p["f1"] = sh["f1"]; p["raw1"] = p["raw"][-1]
        elif sh["f1"] - sh["f0"] < 8 and not keep: sh["_fold_next"] = True; keep.append(sh)
        else:
            if keep and keep[-1].get("_fold_next"):
                q = keep.pop(); n = q["f1"] - q["f0"]; sh["raw"] = [round(sh["raw"][0] - (n - j) / FPS, 4) for j in range(n)] + sh["raw"]; sh["f0"] = q["f0"]; sh["raw0"] = sh["raw"][0]
            keep.append(sh)
    for k, sh in enumerate(keep):
        sh["idx"] = k; sh.update(P.SHOTS[S].get(k, {}))
        if sh["kind"] == "broll": sh.update(cx=next(c[4] for c in P.COVERS[S] if c[2] == sh["roll"] and abs(c[3] - sh["raw0"]) < 1.0))
    # `auto` talking shots become steady holds (plan_holds)
    if any(sh.get("auto") for sh in keep) and os.path.exists(f"{d}/words.json"):
        bars = set()
        for b in bar_times(S): bars.update(range(fr(b["a"]), fr(b["b"]) + 1))
        out = []
        for sh in keep:
            if not sh.get("auto"): out.append(sh); continue
            pv = out[-1] if out else None; prev = None
            if pv and pv["kind"] == "talk" and pv["roll"] == sh["roll"] and pv.get("win") and pv["f1"] == sh["f0"]:
                prev = (pv["win"], 0.0)
            hs = plan_holds(sh, roll_track(d, sh["roll"]), bars, prev)
            assert hs, f"{S} shot {sh['idx']}: no steady holds fit; give it keys or follow"
            for j0, j1, w, c in hs:
                h = {k: v for k, v in sh.items() if k not in ("auto", "raw")}
                h.update(f0=sh["f0"] + j0, f1=sh["f0"] + j1, raw=sh["raw"][j0:j1], raw0=sh["raw"][j0], raw1=sh["raw"][j1 - 1], win=w, hold=True)
                if c is None:
                    h.update(follow=True, lead=0.0, sigma=0.9, margin=90)
                    pv2 = out[-1] if out else None
                    if pv2 and pv2.get("hold") and pv2["f1"] == h["f0"] and "cx" in pv2 and pv2["roll"] == h["roll"] and abs(pv2["raw1"] - h["raw0"]) < 0.1:
                        rws = roll_track(d, sh["roll"]); x = float(np.interp(h["raw0"], [r["t"] for r in rws], [r["fx"] for r in rws]))
                        h["start_c"] = x - (x - pv2["cx"]) * (WIN[w][0] / WIN[pv2["win"]][0])
                else:
                    h.update(cx=round(c))
                    pv2 = out[-1] if out else None
                    if pv2 and pv2.get("follow") and pv2["f1"] == h["f0"] and pv2["win"] == w: pv2["end_c"] = round(c); h["seamless"] = True
                out.append(h)
        keep = out
        for k, sh in enumerate(keep): sh["idx"] = k
    json.dump(keep, open(f"{d}/shots.json", "w"))
    if not quiet:
        words = json.load(open(f"{d}/words.json")) if os.path.exists(f"{d}/words.json") else []
        for sh in keep:
            a, b = sh["f0"] / FPS, sh["f1"] / FPS; ws = " ".join(w["w"] for w in words if a <= w["t"] < b)
            ext = {k: v for k, v in sh.items() if k not in ("idx", "kind", "roll", "f0", "f1", "raw0", "raw1", "raw")}
            print(f"{S} #{sh['idx']:<2} {sh['kind']:<5} {a:6.2f}-{b:6.2f} {sh['roll']} {sh['raw0']:7.2f}-{sh['raw1']:7.2f} {ext} | {ws[:60]} ... {ws[-30:]}")
    return keep

# ------------------------------------------------------------------ track (Vision face box + person mask, 4 fps)
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
FB = os.path.expanduser("~/.cache/absbyai/facebox")
def cmd_track(S):
    import glob; from scipy import ndimage
    d = D(S); shots = json.load(open(f"{d}/shots.json")); res = {}
    old = json.load(open(f"{d}/track.json")) if os.path.exists(f"{d}/track.json") else {}
    for sh in shots:
        if sh["kind"] == "broll": continue
        key = f"{sh['roll']}:{sh['raw0']:.2f}:{sh['raw1']:.2f}"
        if key in old: res[key] = old[key]; continue
        td = f"{d}/trk/{sh['idx']}"; os.makedirs(td, exist_ok=True)
        for f in glob.glob(td + "/*.png") + glob.glob(td + "/m/*"): os.remove(f)
        t0, t1 = sh["raw0"] - 0.1, sh["raw1"] + 0.15
        subprocess.run([lib.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", f"{lib.RAWD}/{sh['roll']}.MP4", "-t", f"{t1 - t0:.3f}",
                        "-vf", "fps=6,scale=960:540:in_color_matrix=bt709:in_range=tv", f"{td}/f_%04d.png"], check=True)
        fs = sorted(f for f in glob.glob(td + "/f_*.png") if not os.path.basename(f).startswith("._"))
        subprocess.run([PM, td + "/m"] + fs, check=True, capture_output=True)
        fb = dict(l.split("\t") for l in subprocess.run([FB] + fs, capture_output=True, text=True).stdout.strip().split("\n"))
        rows = []
        for k, f in enumerate(fs):
            r = {"t": round(t0 + k / 6, 3)}
            m = np.array(Image.open(f"{td}/m/{os.path.basename(f)[:-4]}.mask.png")) > 127; lab, n = ndimage.label(m)
            if n:
                b = lab == (int(np.argmax(ndimage.sum(m, lab, range(1, n + 1)))) + 1); rr = np.where(b.sum(1) >= 20)[0]; c = np.where(b.any(0))[0]
                if len(rr): r.update(top=int(rr[0]) * 2, x0=int(c[0]) * 2, x1=int(c[-1]) * 2)
            v = fb.get(f, "none")
            if v not in ("none", "error"):
                x0, y0, x1, y1 = [int(q) * 2 for q in v.split()]; r.update(fx=(x0 + x1) // 2, fy0=y0, fy1=y1, fw=x1 - x0)
                if n:                                        # his HEAD at ear level (the face box stops short of his ears): mask extent, eyes to mid-face
                    ya, yb = max(0, y0 // 2), max(y0 // 2 + 2, (y0 + int(0.6 * (y1 - y0))) // 2); cols = np.where(b[ya:yb].any(0))[0]
                    if len(cols): r.update(hx0=int(cols[0]) * 2, hx1=int(cols[-1]) * 2)
            rows.append(r)
        res[key] = rows
        fx = [r["fx"] for r in rows if "fx" in r]
        print(S, f"#{sh['idx']}", key, "faces", len(fx), "/", len(rows), ("cx %d..%d fw %d bottom max %d top min %d" % (min(fx), max(fx), np.median([r["fw"] for r in rows if "fw" in r]), max(r["fy1"] for r in rows if "fx" in r), min(r["fy0"] for r in rows if "fx" in r))) if fx else "", flush=True)
        json.dump(res, open(f"{d}/track.json", "w"))
    json.dump(res, open(f"{d}/track.json", "w"))

def gauss(x, sigma):
    if sigma <= 0 or len(x) < 3: return x
    r = int(sigma * 3) + 1; k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    return np.convolve(np.pad(x, r, mode="edge"), k, mode="valid")
def window_path(sh, track, cw):
    """window centre x per output frame: steady where he is steady (a +-TOL deadband), following where the handheld camera or he moves."""
    n = sh["f1"] - sh["f0"]; raw = np.array(sh["raw"])
    if sh.get("keys"):
        ks = sorted(sh["keys"]); c = np.interp(raw, [k[0] for k in ks], [k[1] for k in ks]); c = gauss(c, 0.25 * FPS)
    elif "cx" in sh: c = np.full(n, float(sh["cx"]))
    else:
        rows = [r for r in track if "fx" in r]
        assert len(rows) >= 2, f"shot {sh['idx']}: no face track; give it cx or keys"
        inside = [r for r in rows if raw[0] - 0.2 <= r["t"] <= raw[-1] + 0.2] or rows
        lo = min(r["fx"] - r["fw"] / 2 for r in inside); hi = max(r["fx"] + r["fw"] / 2 for r in inside)
        if hi - lo <= cw - 20 and not sh.get("follow"):      # his whole face fits one window: a steady crop (Dan: steady per shot)
            return np.clip(np.full(n, (lo + hi) / 2), cw / 2, 1920 - cw / 2)
        if sh.get("lead") is not None:                # a close-up that must keep his whole face: centre on where he will be
            hr = [r for r in rows if "hx0" in r and r["hx1"] - r["hx0"] < cw + 200 and r["hx0"] < r["fx"] < r["hx1"]]
            if sh.get("head") and len(hr) >= 2:           # an extreme close-up: centre his HEAD (ears in), not his face box (reviewer, S4 0:08.8 / S5 0:03.2)
                tt = [r["t"] for r in hr]; hc = np.interp(raw + sh["lead"], tt, [(r["hx0"] + r["hx1"]) / 2 for r in hr])
                c = gauss(hc, sh.get("sigma", 0.2) * FPS)
                fxa = np.interp(raw, tt, [(r["hx0"] + r["hx1"]) / 2 for r in hr]); fwa = np.interp(raw, tt, [r["hx1"] - r["hx0"] for r in hr])
                m = sh.get("margin", 10)
                if float(np.max(fwa)) + 2 * m > cw: m = max(0.0, (cw - float(np.max(fwa))) / 2)     # the head nearly fills the window
            else:
                c = gauss(np.interp(raw + sh["lead"], [r["t"] for r in rows], [r["fx"] for r in rows]), sh.get("sigma", 0.2) * FPS)
                # his whole face stays inside the window before any smoothing wins (reviewer, S2 0:32.7): clamp, then a light re-smooth
                fxa = np.interp(raw, [r["t"] for r in rows], [r["fx"] for r in rows]); fwa = np.interp(raw, [r["t"] for r in rows], [r["fw"] for r in rows])
                m = sh.get("margin", 45)
            for _ in range(2):
                c = np.minimum(np.maximum(c, fxa + fwa / 2 + m - cw / 2), fxa - fwa / 2 - m + cw / 2); c = gauss(c, 0.15 * FPS)
            if sh.get("end_c") is not None:                # the walk ends: ease to the steady crop that follows, no cut
                k = min(n, int(1.0 * FPS)); w = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
                c[-k:] = c[-k:] * (1 - w) + sh["end_c"] * w
            if sh.get("start_c") is not None:              # after an in-take cut: start where his face was on screen, then ease onto him
                k = min(n, int(1.5 * FPS)); w = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
                c[:k] = sh["start_c"] * (1 - w) + c[:k] * w
            return np.clip(c, cw / 2, 1920 - cw / 2)
        f = gauss(np.interp(raw, [r["t"] for r in rows], [r["fx"] for r in rows]), 0.35 * FPS)
        fw = np.median([r["fw"] for r in rows])
        tol = sh.get("tol", float(min(np.clip((cw - fw) / 2 - 40, 15, cw * 0.13), cw * 0.045)))   # median face within the gate's 6 % of centre
        c = np.empty(n); c[0] = f[0]; c = np.empty(n); c[0] = f[0]     # a close-up gets a tight deadband: his face nearly fills the window
        if f.max() - f.min() <= 2 * tol: c[:] = (f.max() + f.min()) / 2
        else:
            for i in range(1, n): c[i] = min(max(c[i - 1], f[i] - tol), f[i] + tol)
            lead = c[0]; c = gauss(c, 0.45 * FPS); c[0:1] = c[0]
    return np.clip(c, cw / 2, 1920 - cw / 2)

def roll_track(d, roll):
    """every Vision sample this short has for a roll (track.json is keyed by shot; holds re-split shots)."""
    T = json.load(open(f"{d}/track.json")) if os.path.exists(f"{d}/track.json") else {}
    rows = sorted((r for k, v in T.items() if k.split(":")[0] == roll for r in v if "fx" in r), key=lambda r: r["t"])
    return rows
def plan_holds(sh, rows, bar_frames, prev=None, step=6, min_len=1.3, margin=45, cut_cost=40.0, centre_w=1.5, max_jump=70.0, follow_cost=400.0):
    """Split one continuous talking take into steady holds (Dan: steady crops; a real size step at every cut, and at a cut
    inside one take his face stays where it was on screen). Dynamic programme over cut points every `step` frames: each hold
    is FULL (724) or MID (604) and holds his whole face (+margin) on every sample; consecutive holds alternate size; cost =
    on-screen face jump at each cut + a fixed cost per cut + distance of his face from the centre. Frames under a key-point
    bar must be FULL. `prev` = (win, centre, face x) of the shot before when it is the same camera and take."""
    n = sh["f1"] - sh["f0"]; raw = np.array(sh["raw"]); G = list(range(0, n, step)) + [n]; m = len(G) - 1
    if len(rows) < 2: return None
    ts = [r["t"] for r in rows]; fx = np.interp(raw, ts, [r["fx"] for r in rows]); fw = np.interp(raw, ts, [r["fw"] for r in rows])
    lo_ = fx - fw / 2 - margin; hi_ = fx + fw / 2 + margin
    barred = np.array([sh["f0"] + i in bar_frames for i in range(n)])
    best = {}                                                    # (grid k, win, c) -> (cost, back)
    def interval(a, b, cw):
        L = hi_[G[a]:G[b]].max() - cw / 2; R = lo_[G[a]:G[b]].min() + cw / 2
        L = max(L, cw / 2); R = min(R, 1920 - cw / 2)
        return (L, R) if L <= R else None
    for b in range(1, m + 1):
        for a in range(0, b):
            if (G[b] - G[a]) / FPS < min_len and not (a == 0 and b == m): continue
            for w, (cw, ch) in WIN.items():
                if w == "mid" and barred[G[a]:G[b]].any(): continue
                iv = interval(a, b, cw)
                follow = iv is None
                if follow:                                   # no steady window holds him here: a slow follow, as a last resort
                    if w != "full": continue
                    iv = (fx[G[a]], fx[G[a]])
                s_ = 1080 / cw; med = float(np.median(fx[G[a]:G[b]])); ideal = min(max(med, iv[0]), iv[1])
                seg_fx = fx[G[a]:G[b]]; dur = (G[b] - G[a]) / FPS
                off = lambda c: (abs(med - c) + float(np.percentile(np.abs(seg_fx - c), 90))) / 2       # typical AND worst-case off-centre
                if a == 0:
                    c = ideal; cost = (follow_cost * dur) if follow else centre_w * off(c) * s_ * dur
                    if prev and prev[0] == w: continue
                    if prev: cost += abs((fx[0] - c) * s_ - prev[1]) * 0.5
                    ce = float(fx[G[b] - 1]) if follow else c
                    key = (b, w, round(ce))
                    if key not in best or best[key][0] > cost: best[key] = (cost, None, (a, b, w, None if follow else c))
                    continue
                for (kb, kw, kc), (pc, _, ph) in list(best.items()):
                    if kb != a: continue
                    if kw == w:                               # same size only where a follow eases to a stop (no cut at all)
                        if ph[3] is not None or follow or not (iv[0] - 200 <= kc <= iv[1] + 200): continue
                        c = min(max(kc, iv[0]), iv[1])                # the follow's last second eases onto c
                        cost = pc + 0.5 * abs(c - kc) * s_ + centre_w * off(c) * s_ * dur
                        key = (b, w, round(c))
                        if key not in best or best[key][0] > cost: best[key] = (cost, (kb, kw, kc), (a, b, w, float(c)))
                        continue
                    s1 = 1080 / WIN[kw][0]; x = fx[G[a]]; on = (x - kc) * s1     # his face on screen just before the cut
                    c = min(max(x - on / s_, iv[0]), iv[1])                   # keep it there after the cut if the hold allows
                    jump = abs((x - c) * s_ - on)
                    jcost = 3 * jump if jump <= max_jump else 3 * max_jump + 25 * (jump - max_jump)   # he must not slide across the cut
                    cost = pc + cut_cost + jcost + ((follow_cost * dur) if follow else centre_w * off(c) * s_ * dur)
                    ce = float(fx[G[b] - 1]) if follow else c
                    key = (b, w, round(ce))
                    if key not in best or best[key][0] > cost: best[key] = (cost, (kb, kw, kc), (a, b, w, None if follow else c))
    ends = [(v[0], k) for k, v in best.items() if k[0] == m]
    if not ends: return None
    k = min(ends)[1]; out = []
    while k:
        cost, back, hold = best[k]; out.append(hold); k = back
    return [(G[a], G[b], w, c) for a, b, w, c in reversed(out)]

# ------------------------------------------------------------------ graphics
def bar_times(S):
    d = D(S); words = json.load(open(f"{d}/words.json")); T = json.load(open(f"{d}/timeline.json")); out = []
    for b in P.BARS[S]:
        ts = [words[find_phrase(words, ph)]["t"] for _, ph in b["parts"]]
        out.append(dict(id=b["id"], topic=b["topic"], parts=[[l, round(t, 3)] for (l, _), t in zip(b["parts"], ts)], a=round(ts[0] + b["a"], 3), b=round(min([ts[-1] + b["b"], T["total"] - 0.12] + [j - 0.04 for j in T["joins"] if j > ts[0]]), 3)))   # never across a piece join
    return out
def cmd_gfx(S, snap_only=False):
    import vertical as V, hfbuild as Hf, lt
    V.B.lower_third_default_box = lt._shifted
    d = D(S); man = []
    for c in bar_times(S):
        scenes, meta = V.lt_scenes(dict(c, drift=-4)); assert meta["lines"] == 2, (S, c["id"], "wraps to", meta["lines"], "lines")
        assert meta["box"][1] >= 1128 and meta["box"][3] <= 1380, meta
        movs = []
        for tpl, cfg, assets in scenes:
            pd = Hf.make_scene(tpl, cfg, pathlib.Path(d) / "hf/proj", assets); mov = f"{d}/hf/{cfg['id']}.mov"; stamp = mov + ".cfg"
            sig = hashlib.sha256((json.dumps(cfg, sort_keys=True) + open(tpl).read()).encode()).hexdigest()
            if not (os.path.exists(mov) and os.path.exists(stamp) and open(stamp).read() == sig):
                Hf.lint_check(pd); Hf.render(pd, mov); open(stamp, "w").write(sig)
            movs.append(mov)
        man.append(dict(id=c["id"], kind="glass", a=c["a"], b=c["b"], mov=movs[0], mask=movs[1], band=meta["band"], box=meta["box"], topic=c["topic"], parts=c["parts"]))
        print(S, c["id"], c["a"], c["b"], c["parts"], meta["box"], flush=True)
    json.dump(man, open(f"{d}/hf/manifest.json", "w"), indent=1)

# ------------------------------------------------------------------ frame sources
class Seq:
    """sequential frame reader with restart on a jump: get(n) returns frame n of the stream (index at `rate`)."""
    def __init__(self, path, vf, wh, rate): self.path, self.vf, self.wh, self.rate = path, vf, wh, rate; self.p = None; self.n = None; self.last = None
    def open(self, n):
        self.close()
        self.p = subprocess.Popen([lib.FF, "-nostdin", "-v", "error", "-ss", f"{max(0, (n - 0.3) / self.rate):.4f}", "-i", self.path, "-vf", self.vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE); self.n = n
    def close(self):
        if self.p: self.p.kill(); self.p.stdout.close(); self.p.wait(); self.p = None
    def get(self, n):
        if self.last is not None and n == self.n - 1: return self.last
        if self.p is None or n < self.n or n > self.n + 90: self.open(n)
        size = self.wh[0] * self.wh[1] * 3
        while True:
            b = self.p.stdout.read(size)
            if len(b) < size: assert self.last is not None, (self.path, n); return self.last
            self.n += 1
            if self.n - 1 == n: self.last = np.frombuffer(b, np.uint8).reshape(self.wh[1], self.wh[0], 3); return self.last
def cam(roll):
    vf = f"scale=1920:1080:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb48le,lut3d=file='{lib.LUTS}/{roll}.cube':interp=tetrahedral,format=rgb24"
    return Seq(f"{lib.RAWD}/{roll}.MP4", vf, (1920, 1080), FPS)
SCR_WH = (518, 982)
def scr(): return Seq(lib.SCREEN, f"crop=1320:2500:0:175,scale={SCR_WH[0]}:{SCR_WH[1]}:flags=lanczos,format=rgb24", SCR_WH, 60.0)
def phone_shell():
    """the approved iPhone shell (RO-05 build_r2.iphone / round 1 P5_B) at 1.2x with an empty screen; content goes at (48,114) 518x982."""
    im = Image.new("RGBA", (660, 1090), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((91, 34, 573, 1062), 68, fill=(0, 0, 0, 120)); im = sh.filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(im)
    def rr(box, fill, r, outline=None, width=1): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    s = Image.new("RGB", (448, 1000), (248, 250, 252)); e = ImageDraw.Draw(s); e.text((30, 14), "9:41", font=B.font(17), fill=(23, 43, 59))
    for i in range(4): e.rounded_rectangle((352 + i * 6, 30 - i * 3, 355 + i * 6, 35), 1, fill=(25, 32, 40))
    e.rounded_rectangle((391, 22, 418, 34), 3, outline=(25, 32, 40), width=2); e.rectangle((419, 26, 422, 30), fill=(25, 32, 40)); e.rectangle((394, 25, 413, 31), fill=(25, 32, 40))
    e.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); e.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); e.ellipse((280, 29, 284, 33), fill=(34, 60, 82)); e.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32))
    m = Image.new("L", (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(s, (102, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    im = im.crop((70, 10, 590, 1085)); return im.resize((624, 1290), Image.LANCZOS)

def cap_png(lines, top, size=86):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(ARIAL, size); y = top
    for s in lines:
        w = d.textlength(s, font=f); x = (W - w) / 2
        d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
        d.text((x, y), s, font=f, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255)); y += int(size * 1.12)
    return im
def over_box(frame, rgba, box):
    x0, y0, x1, y1 = box; a = rgba[y0:y1, x0:x1, 3:4].astype(np.float32) / 255
    frame[y0:y1, x0:x1] = (frame[y0:y1, x0:x1].astype(np.float32) * (1 - a) + rgba[y0:y1, x0:x1, :3].astype(np.float32) * a + 0.5).astype(np.uint8)

class Short:
    def __init__(self, S):
        self.S = S; d = self.d = D(S); self.T = json.load(open(f"{d}/timeline.json")); self.N = self.T["frames"]
        self.shots = json.load(open(f"{d}/shots.json")); self.track = json.load(open(f"{d}/track.json")) if os.path.exists(f"{d}/track.json") else {}
        self.cues = json.load(open(f"{d}/cues.json"))
        # the Soft Blue field drifts (GRAPHICS-STANDARDS: "restrained drifting blue light"): keyframes every 0.5 s, blended per frame
        kf = os.path.join(d, "field_keys.npy"); nk = int(self.N / FPS / 0.5) + 2
        if os.path.exists(kf) and np.load(kf, mmap_mode="r").shape[0] == nk: self.keys = np.load(kf)
        else:
            ks = []
            for k in range(nk):
                bg = lib.canvas(k * 0.5); lib.band(bg, *P.TITLE[S]); ks.append(np.asarray(bg))
            self.keys = np.stack(ks); np.save(kf, self.keys)
        self.base = self.keys[0]
        wm = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(wm); f = B.font(30)
        self.shell = None; self.cams = {}; self.screen = None
        self.plan_windows()
        demo = any(sh["kind"] == "demo" for sh in self.shots)      # a phone short keeps the wordmark low throughout (captions sit low)
        for sh in self.shots:
            xy = (64, 1850) if demo else (64, 1800)
            sh["wm"] = xy
        self.wms = {}
        for xy in ((64, 1800), (64, 1850)):
            o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(o); dd.text((xy[0] + 2, xy[1] + 2), "AbsByAI.com", font=f, fill=(0, 0, 0, 140)); dd.text(xy, "AbsByAI.com", font=f, fill=(244, 250, 255, 170))
            self.wms[xy] = (np.asarray(o), (xy[0], xy[1], xy[0] + 260, xy[1] + 50))
        # captions: one RGBA state per cue, at the caption top of the shot it starts in
        os.makedirs(f"{d}/cap", exist_ok=True); self.caps = []
        for i, c in enumerate(self.cues):
            sh = self.shot_at(fr(c["a"])); top = sh.get("cap", 1612 if sh["kind"] == "demo" else 1412)
            im = cap_png(c["lines"], top); p = f"{d}/cap/cue{i:03d}.png"; im.save(p); bb = im.getbbox()
            self.caps.append(dict(f0=fr(c["a"]), f1=fr(c["b"]), arr=np.asarray(im), box=bb, png=p, top=top))
        man = f"{d}/hf/manifest.json"; self.man = json.load(open(man)) if os.path.exists(man) else []
    def shot_at(self, i): return next(sh for sh in self.shots if sh["f0"] <= i < sh["f1"])
    def key(self, sh): return f"{sh['roll']}:{sh['raw0']:.2f}:{sh['raw1']:.2f}"
    def plan_windows(self):
        for sh in self.shots:
            trk = self.track.get(self.key(sh)) or [r for r in roll_track(self.d, sh["roll"]) if sh["raw0"] - 0.5 <= r["t"] <= sh["raw1"] + 0.5]
            if sh["kind"] == "talk": cw, ch = WIN[sh.get("win", "full")]; sh["cw"], sh["ch"] = cw, ch; sh["path"] = window_path(sh, trk, cw)
            elif sh["kind"] == "broll": cw, ch = WIN["full"]; sh["cw"], sh["ch"] = cw, ch; sh["path"] = window_path(sh, trk, cw)
            elif sh.get("layout") != "phone":
                ch = sh.get("dh", 1080); cw = round(ch * DAN_BOX[2] / DAN_BOX[3]); sh["cw"], sh["ch"] = cw, ch; sh["path"] = window_path(sh, trk, cw)
    def picture(self, i, graphics=True):
        sh = self.shot_at(i); j = i - sh["f0"]; raw = sh["raw"][j]; roll = sh["roll"]
        if roll not in self.cams: self.cams[roll] = cam(roll)
        u = i / FPS / 0.5; k = int(u); w = u - k
        frame = (self.keys[k].astype(np.float32) * (1 - w) + self.keys[k + 1].astype(np.float32) * w + 0.5).astype(np.uint8)
        if sh["kind"] in ("talk", "broll"):
            src = self.cams[roll].get(int(np.floor(raw * FPS + 0.25))); cw, ch = sh["cw"], sh["ch"]; x = int(round(sh["path"][j] - cw / 2)); y = sh.get("dy", 0)
            frame[DROP:] = cv2.resize(src[y:y + ch, x:x + cw], (W, PIC_H), interpolation=cv2.INTER_LANCZOS4)
        else:
            if self.shell is None:
                self.shell = np.asarray(phone_shell()); self.screen = scr()
                m = Image.new("L", (DAN_BOX[2], DAN_BOX[3]), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, DAN_BOX[2] - 1, DAN_BOX[3] - 1), 28, fill=255); self.dmask = np.asarray(m)[..., None].astype(np.float32) / 255
            alone = sh.get("layout") == "phone"; px = PHONE_ALONE_X if alone else PHONE_XY[0]; py = PHONE_XY[1]
            box = (px, py, px + 624, py + 1290); full = np.zeros((H, W, 4), np.uint8); full[py:py + 1290, px:px + 624] = self.shell; over_box(frame, full, box)
            st = lib.screen_t(raw); frame[py + 114:py + 114 + SCR_WH[1], px + 48:px + 48 + SCR_WH[0]] = self.screen.get(int(np.floor(st * 60 + 0.25)))
            if not alone:
                src = self.cams[roll].get(int(np.floor(raw * FPS + 0.25))); cw, ch = sh["cw"], sh["ch"]; x = int(round(sh["path"][j] - cw / 2)); y = sh.get("dy", 0)
                dn = cv2.resize(src[y:y + ch, x:x + cw], (DAN_BOX[2], DAN_BOX[3]), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
                bx, by = DAN_BOX[0], DAN_BOX[1]; reg = frame[by:by + DAN_BOX[3], bx:bx + DAN_BOX[2]].astype(np.float32)
                frame[by:by + DAN_BOX[3], bx:bx + DAN_BOX[2]] = (reg * (1 - self.dmask) + dn * self.dmask + 0.5).astype(np.uint8)
        return frame, sh
    def finish(self, frame, sh, i, C=None):
        if C is not None: frame = np.ascontiguousarray(C.apply(frame, i))
        wm, box = self.wms[sh["wm"]]; over_box(frame, wm, box)
        for c in self.caps:
            if c["f0"] <= i < c["f1"]: over_box(frame, c["arr"], c["box"])
        return frame
    def close(self):
        for c in self.cams.values(): c.close()
        if self.screen: self.screen.close()

def cmd_proof(S):
    import composite as Cm
    s = Short(S); d = s.d; os.makedirs(f"{d}/proof", exist_ok=True); tiles = []
    C = Cm.Compositor(s.man, wh=(W, H)) if s.man else None
    want = []
    for sh in s.shots:
        n = sh["f1"] - sh["f0"]; want += [(sh["f0"] + 2, f"#{sh['idx']} in"), (sh["f0"] + n // 2, f"#{sh['idx']} mid"), (sh["f1"] - 3, f"#{sh['idx']} out")]
    for m in s.man: want.append((fr(m["b"] - 0.7), m["id"]))
    for i, lab in sorted(set(want)):
        i = min(max(i, 0), s.N - 1); f, sh = s.picture(i); f = s.finish(f, sh, i, C)
        im = Image.fromarray(f).resize((360, 640), Image.LANCZOS); dd = ImageDraw.Draw(im); dd.rectangle((0, 0, 200, 16), fill=(0, 0, 0)); dd.text((3, 2), f"{lab} {i / FPS:.2f}s {sh.get('win', '')}", fill=(255, 255, 0)); tiles.append(im)
    s.close(); cols = 9; rows = (len(tiles) + cols - 1) // cols
    for pg in range(0, rows, 2):
        sub = tiles[pg * cols:(pg + 2) * cols]; sheet = Image.new("RGB", (360 * cols, 640 * ((len(sub) + cols - 1) // cols)))
        for k, im in enumerate(sub): sheet.paste(im, ((k % cols) * 360, (k // cols) * 640))
        sheet.save(f"{d}/proof/proof_{pg // 2}.jpg", quality=82)
    print(S, "proof sheets:", (rows + 1) // 2)

def cmd_render(S):
    import composite as Cm
    s = Short(S); d = s.d; out = f"{d}/{P.NAME[S]}.mp4"; clean = f"{d}/source_picture.mp4"
    C = Cm.Compositor(s.man, wh=(W, H)) if s.man else None
    enc = lambda path, extra: subprocess.Popen([lib.FF, "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", FPSS, "-i", "-"] + extra + [
        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    e1 = enc(out, ["-i", f"{d}/audio.wav", "-map", "0:v", "-map", "1:a", "-c:a", "aac_at", "-b:a", "320k", "-crf", "16"])
    e2 = enc(clean, ["-crf", "20"])
    for i in range(s.N):
        f, sh = s.picture(i); e2.stdin.write(f.tobytes()); e1.stdin.write(s.finish(f, sh, i, C).tobytes())
        if i % 300 == 0: print(S, i, "/", s.N, flush=True)
    for e in (e1, e2): e.stdin.close(); e.wait()
    s.close(); print(S, "rendered", out, flush=True)

if __name__ == "__main__":
    import cv2
    sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
    cmd = sys.argv[1]
    for S in sys.argv[2:] or list(P.SEG): globals()["cmd_" + cmd](S)
