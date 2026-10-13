#!/usr/bin/env python3
"""SL-07 batch builder (Soft Blue shorts, from softblue-sl03 by way of SL-06). Run from /Volumes/Extreme/_edit_work/sl07 :
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
WORK = "/Volumes/Extreme/_edit_work/sl07"
sys.path.insert(0, WORK); sys.path.insert(0, HERE)
import lib, plans as P
B = lib.B
FPS = 30000 / 1001; FPSS = "30000/1001"; SR = 48000
LF = "/Volumes/Extreme/_edit_work/ro16/"      # read only: RO-16 round 3 master build
W, H, DROP = 1080, 1920, 310
PIC_H = H - DROP
WIN = {"full": (724, 1080), "mid": (604, 900)}
def D(S): d = f"{WORK}/build/{S}"; os.makedirs(d, exist_ok=True); return d
def fr(t): return int(round(t * FPS))
def A_pieces():
    """the film's audio and picture map: RO-16 is one roll (C1710); shots.json (round 3) gives each continuous raw frame range
    and the film frame range it plays at (master audio against the lav through this map: lag 0.0 ms at 9 points)."""
    Sh = json.load(open(LF + "shots.json"))
    return [{"at": s["out_f0"] / FPS, "end": s["out_f1"] / FPS, "in": s["src_f0"] / FPS, "out": s["src_f1"] / FPS, "roll": lib.ROLL} for s in Sh]
def head(S):
    """seconds of recorded pickup before the first film piece (VIDEO-RULES 2026-10-11); 0 when the short opens on a film line."""
    p = P.PICKUP.get(S)
    if not p or os.path.exists(f"{WORK}/{p['wav'][:-4]}.PLACEHOLDER"): return 0.0     # not recorded yet: the short opens on the film line
    w = wave.open(f"{WORK}/{p['wav']}"); return w.getnframes() / w.getframerate()

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
    seg, off = [], head(S)
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
    if o < seg[0]["o0"] - 1e-9: return None          # inside the pickup: no film picture, a cover must be there
    for s in seg:
        if s["o0"] - 1e-9 <= o < s["o1"]: return s["pa"] + (o - s["o0"]) * (s["pb"] - s["pa"]) / (s["o1"] - s["o0"])
    s = seg[-1]; return s["pb"]
def joins(seg):
    """audio joins on the output timeline (a real discontinuity in film time)."""
    return ([round(seg[0]["o0"], 4)] if seg[0]["o0"] > 0 else []) + [round(s["o0"], 4) for i, s in enumerate(seg) if i and abs(s["a"] - seg[i - 1]["b"]) > 1e-6]

def text(S):
    """plans.TEXT without the pickup's piece while the pickup is not recorded."""
    t = P.TEXT[S]
    return t.split(" | ", 1)[1] if (S in P.PICKUP and head(S) == 0.0) else t
def cmd_audio(S):
    seg, total = timeline(S); d = D(S)
    w = wave.open(f"{WORK}/master_audio.wav"); assert w.getframerate() == SR and w.getnchannels() == 2
    parts, raw = [], []
    hd = head(S)
    if hd:                                              # the treated pickup (pickup.py: fitted voice + the film's bed, already faded at its tail)
        pw = wave.open(f"{WORK}/{P.PICKUP[S]['wav']}"); assert pw.getframerate() == SR and pw.getnchannels() == 2
        x = np.frombuffer(pw.readframes(pw.getnframes()), "<i2").astype(np.float32).reshape(-1, 2) / 32768
        parts.append(x); raw.append(x.copy())
    for i, s in enumerate(seg):
        n0 = int(round(s["a"] * SR)); n = int(round((s["o1"] - hd) * SR)) - int(round((s["o0"] - hd) * SR))
        w.setpos(n0); x = np.frombuffer(w.readframes(n), "<i2").astype(np.float32).reshape(-1, 2) / 32768
        raw.append(x.copy())
        first = i == 0 or abs(s["a"] - seg[i - 1]["b"]) > 1e-6; last = i == len(seg) - 1 or abs(seg[i + 1]["a"] - s["b"]) > 1e-6
        if first: k = int(0.015 * SR); x[:k] *= np.linspace(0, 1, k)[:, None]
        if last: k = int((0.04 if i == len(seg) - 1 else 0.015) * SR); x[-k:] *= np.linspace(1, 0, k)[:, None]
        parts.append(x)
    for name, xs in (("audio.wav", parts), ("his_mix.wav", raw)):
        o = wave.open(f"{d}/{name}", "w"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
        o.writeframes((np.clip(np.concatenate(xs), -1, 1) * 32767).astype("<i2").tobytes()); o.close()
    json.dump(dict(seg=seg, total=total, frames=fr(total), joins=joins(seg), head=hd), open(f"{d}/timeline.json", "w"), indent=1)
    # RO-16's mix has no music bed (pauses sit 36 dB under speech in the master, 5 dB over the dry lav's: the expander's floor)
    print(S, f"{total:.2f} s, {fr(total)} frames; joins:", "  ".join(f"{j:.2f}" for j in joins(seg)))

# ------------------------------------------------------------------ words: CTC alignment of the caption text
def tokens(S):
    """[(shown, spoken, piece index)] from plans.TEXT"""
    out = []
    for pi, part in enumerate(text(S).split(" | ")):
        for tok in part.split():
            m = re.match(r"^(.*?)\{(.*)\}(.*)$", tok)
            shown, spoken = (m.group(1) + m.group(3), m.group(2)) if m else (tok, tok)
            out.append((shown, spoken, pi))
    # `{two words}` was split by whitespace: rejoin
    fixed, buf = [], None
    for part_i, part in enumerate(text(S).split(" | ")):
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
    toks = tokens(S); hd = T.get("head", 0.0)
    # the SEG pieces (plans.TEXT ' | ') are the audio joins that are not pause trims; a pickup is piece 0
    pj = [hd]; acc = hd
    for a, b in P.SEG[S]:
        acc += (b - a) - sum((t[1] - t[0]) - (t[3] if len(t) > 3 else P.KEEP) for t in P.TRIM.get(S, []) if a < t[0] and t[1] < b); pj.append(acc)
    out = []
    spans = ([(0.0, hd)] if hd else []) + list(zip(pj[:-1], pj[1:]))
    assert len(spans) == len(text(S).split(" | ")), (S, "TEXT pieces", len(text(S).split(" | ")), "audio pieces", len(spans))
    for pi, (t0, t1) in enumerate(spans):
        ws = [t for t in toks if t[2] == pi]
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
        if out[k][0]["p"] == out[k - 1][-1]["p"] and len(out[k - 1]) > 2 and nz(out[k][0]["w"]) in [nz(x["w"]) for x in out[k - 1]] \
           and not re.search(r"[.!?]$", out[k - 1][-1]["w"]):      # never carry a sentence's last word into the next sentence's cue (SL-07 A: "happens. So if I was")
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
    ot = lambda x: T.get("head", 0.0) if x == "head" else float(x[1:]) if isinstance(x, str) else film2out(seg, x)      # "o47.4" = an output time (inside a pause trim)
    covers = [(ot(c["a"]), ot(c.get("nohead", c["b"]) if (c["b"] == "head" and not T.get("head")) else c["b"]), c) for c in P.COVERS[S]]   # nohead: where the opening cover ends while the pickup is not recorded
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
            c = cv[2]; key = ("scene" if c.get("scene") else "clip", c["id"], 0); roll = c["id"]
            raw = c.get("t", 0.0) + (o - cv[0]) * c.get("speed", 1)      # clip time (or scene-local time)
            for a_, b_ in c.get("skip", []):                                # leave a stretch of the clip out (a screen recording's own messy transition): the picture jumps inside the clip
                if raw >= a_: raw += b_ - a_
            if c.get("phone"):
                a_ = next(a for a in A if a["at"] - 1e-6 <= f < a["end"]); camt = a_["in"] + (f - a_["at"]); key = ("phone", c["id"], round((camt - f) * 10))
        else:
            assert f is not None, (S, "the pickup is not covered at", round(o, 2))
            a = next((a for a in A if a["at"] - 1e-6 <= f < a["end"]), None)
            if a is None: a = max((a for a in A if a["at"] <= f), key=lambda a: a["at"])      # a gap in the long-form's audio map: the take runs on
            raw = a["in"] + (f - a["at"]); roll = a["roll"]; key = ("talk", a["roll"], round((raw - f) * 10), sum(i >= c for c in cutf), sum(o >= j for j in T["joins"]))      # one shot per continuous run of the roll
        if cur is None or cur["key"] != key:
            cur = dict(key=key, kind=key[0], roll=roll, f0=i, raw=[], cam=[]); rows.append(cur)
        cur["raw"].append(raw)
        if key[0] == "phone": cur["cam"].append(camt)
    for r in rows:                                    # the long-form's audio map can step a take back a few ms at one of its own joins
        if r["kind"] != "talk": continue             # (C1548 at film 524.07: 20 ms): the same source frame would show twice (reviewer r3a/r3b,
        off = 0.0                                     # S4 0:34.60). Carry the step forward so the picture stays one continuous run.
        for j in range(1, len(r["raw"])):
            r["raw"][j] += off; dlt = r["raw"][j] - r["raw"][j - 1]
            if 1 / FPS - 0.03 < dlt < 1 / FPS - 0.002: r["raw"][j] += 1 / FPS - dlt; off += 1 / FPS - dlt
    shots = []
    for k, r in enumerate(rows):
        sh = dict(idx=k, kind=r["kind"], roll=r["roll"], f0=r["f0"], f1=r["f0"] + len(r["raw"]), raw0=round(r["raw"][0], 4), raw1=round(r["raw"][-1], 4), raw=[round(x, 4) for x in r["raw"]])
        if r["kind"] == "phone": sh.update(clip=sh["raw"], raw=[round(x, 4) for x in r["cam"]], raw0=round(r["cam"][0], 4), raw1=round(r["cam"][-1], 4), roll=lib.ROLL, cid=r["roll"])
        shots.append(sh)
    # a few-frame sliver (a piece edge that runs a hair past a join) folds into its neighbour
    keep = []
    for sh in shots:
        if sh["f1"] - sh["f0"] < 8 and keep and sh["kind"] == "talk" and keep[-1]["kind"] == "talk":
            p = keep[-1]; n = sh["f1"] - sh["f0"]; step = (p["raw"][-1] - p["raw"][-2]) if len(p["raw"]) > 1 else 1 / FPS
            p["raw"] += [round(p["raw"][-1] + step * (j + 1), 4) for j in range(n)]; p["f1"] = sh["f1"]; p["raw1"] = p["raw"][-1]
        elif sh["f1"] - sh["f0"] < 8 and not keep and sh["kind"] == "talk": sh["_fold_next"] = True; keep.append(sh)
        else:
            if keep and keep[-1].get("_fold_next"):
                q = keep.pop(); n = q["f1"] - q["f0"]; sh["raw"] = [round(sh["raw"][0] - (n - j) / FPS, 4) for j in range(n)] + sh["raw"]; sh["f0"] = q["f0"]; sh["raw0"] = sh["raw"][0]
            keep.append(sh)
    for k, sh in enumerate(keep):
        sh["idx"] = k; sh.update(P.SHOTS[S].get(k, {}))
        if sh["kind"] == "talk" and "win" not in sh and not sh.get("auto"):      # default: a real size step at every same-camera join
            pv = keep[k - 1] if k else None
            sh["win"] = ("mid" if pv["win"] == "full" else "full") if (pv and pv["kind"] == "talk" and pv["f1"] == sh["f0"]) else "full"
        if sh["kind"] != "talk": sh["cover"] = next(c for c in P.COVERS[S] if c["id"] == sh.get("cid", sh["roll"]))
    # `auto` talking shots become steady holds (plan_holds)
    if any(sh.get("auto") for sh in keep) and os.path.exists(f"{d}/words.json"):
        bars = set()
        for b in bar_times(S): bars.update(range(fr(b["a"]), fr(b["b"]) + 1))
        out = []
        for sh in keep:
            if not sh.get("auto") or sh["kind"] != "talk": out.append(sh); continue
            pv = out[-1] if out else None; prev = None
            if pv and pv["kind"] == "talk" and pv["roll"] == sh["roll"] and pv.get("win") and pv["f1"] == sh["f0"]:
                prev = (pv["win"], 0.0)
            if len(roll_track(d, sh["roll"])) < 2: print(S, f"shot {sh['idx']}: no track yet; run track, then plan again"); out.append(sh); continue
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
        if sh["kind"] not in ("talk", "phone"): continue
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
            med = float(np.median([r["fx"] for r in inside])); m_ = 45                    # centre on his median position, as long as his whole face (+45 px) stays inside
            c0 = min(max(med, hi + m_ - cw / 2), lo - m_ + cw / 2) if hi - lo + 2 * m_ <= cw else (lo + hi) / 2
            return np.clip(np.full(n, c0), cw / 2, 1920 - cw / 2)
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
        ts = []
        for _, ph in b["parts"]: ts.append(words[find_phrase(words, ph, ts[-1] if ts else 0.0)]["t"])      # each line lands at or after the line before it
        out.append(dict(id=b["id"], topic=b["topic"], parts=[[l, round(t, 3)] for (l, _), t in zip(b["parts"], ts)], a=round(ts[0] + b["a"], 3), b=round(min([ts[-1] + b["b"], T["total"] - 0.12] + [j - 0.04 for j in T["joins"] if j > ts[0]]), 3)))   # never across a piece join
    for k in range(len(out) - 1):                       # one bar at a time: a bar leaves before the next one arrives
        out[k]["b"] = round(min(out[k]["b"], out[k + 1]["a"] - 0.25), 3)
    return out
def cmd_gfx(S, snap_only=False):
    import vertical as V, hfbuild as Hf, lt
    V.B.lower_third_default_box = lt._shifted
    d = D(S); man = []
    for c in bar_times(S):
        scenes, meta = V.lt_scenes(dict(c, drift=-4)); assert meta["lines"] <= 2, (S, c["id"], "wraps to", meta["lines"], "lines")
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
    def __init__(self, path, vf, wh, rate, pre=(), cplx=False): self.path, self.vf, self.wh, self.rate, self.pre, self.cplx = path, vf, wh, rate, list(pre), cplx; self.p = None; self.n = None; self.last = None
    def open(self, n):
        self.close()
        self.p = subprocess.Popen([lib.FF, "-nostdin", "-v", "error"] + self.pre + ["-ss", f"{max(0, (n - 0.3) / self.rate):.4f}", "-i", self.path, "-filter_complex" if self.cplx else "-vf", self.vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE); self.n = n
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
def cam(roll, x0, x1):
    """the raw 4K roll through the film's grade, cropped to the strip of columns [x0, x1) (1920-space) this short's windows use.
    Windows are cut from 4K (a 724 window is 1448 px wide for a 1080 px picture: no upscale)."""
    X, Wd = x0 * 2, (x1 - x0) * 2
    vf = (f"crop={Wd}:2160:{X}:0,scale={Wd}:2160:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,"
          f"lut3d=file='{lib.LUT}':interp=tetrahedral,scale=out_color_matrix=bt709:out_range=pc,format=rgb24")
    return Seq(f"{lib.RAWD}/{roll}.MP4", vf, (Wd, 2160), FPS)
def clip_box(c):
    """where a cover clip sits: (x, y, w, h) on the 1080x1920 canvas. fill = the whole picture area (default, VIDEO-RULES
    'fill the frame'); square / whole = a card on the field, with the reason written in plans.py."""
    fit = c.get("fit", "fill")
    if fit == "fill": return (0, DROP, W, PIC_H)
    if fit == "square": return (0, c.get("y", DROP + 40), W, W)
    if fit == "whole": return (0, c.get("y", DROP + 200), W, 608)
    if fit == "stack2": return (0, DROP, W, PIC_H)
    if fit == "span":                                  # a card as tall as the subject's sideways travel allows: columns span=(a, b) of a 16:9 clip, full height, full width
        a, b_ = c["span"]; return (0, c.get("y", DROP), W, min(PIC_H, int(round(W * 1080 / ((b_ - a) * 1920) / 2) * 2)))
    raise ValueError(fit)
def clip_seq(c):
    """a stock / library / AI clip conformed to its box: scaled to cover it, cropped on the subject (fx, fy = where the crop
    sits, 0..1), then colour corrected toward the film (c['eq'], an ffmpeg filter chain measured in grade.py)."""
    x, y, w, h = clip_box(c); fx, fy = c.get("fx", 0.5), c.get("fy", 0.5); z = c.get("zoom", 1.0)
    if c.get("fit") == "stack2":                       # left half on top, right half under it, each scaled to the full width; a 2 px glass line between
        hh = h // 2; fy = c.get("fy", 0.3)
        half = lambda xx: f"crop=iw/2:ih:{xx}:0,scale={w}:-2:flags=lanczos,crop={w}:{hh}:0:(ih-{hh})*{fy}"
        vf = (f"fps={FPSS},scale=in_color_matrix=bt709,split[a][b];[a]{half(0)}[t];[b]{half('iw/2')}[u];[t][u]vstack" + ("," + c["eq"] if c.get("eq") else "") + f",drawbox=0:{hh - 1}:{w}:2:color=0x4070A0,format=rgb24")
        return Seq(c["src"], vf, (w, h), FPS, cplx=True)
    if c.get("fit") == "span":
        a, b_ = c["span"]
        return Seq(c["src"], f"fps={FPSS},crop=iw*{b_ - a:.4f}:ih:iw*{a:.4f}:0,scale={w}:{h}:flags=lanczos:in_color_matrix=bt709" + ("," + c["eq"] if c.get("eq") else "") + ",format=rgb24", (w, h), FPS)
    vf = (("hflip,vflip," if c.get("rot") == 180 else "") + f"fps={FPSS},scale={round(w * z)}:{round(h * z)}:force_original_aspect_ratio=increase:flags=lanczos:in_color_matrix=bt709,"
          f"crop={w}:{h}:(iw-{w})*{fx}:(ih-{h})*{fy}" + ("," + c["eq"] if c.get("eq") else "") + ",format=rgb24")
    return Seq(c["src"], vf, (w, h), FPS)

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

PHONE_XY = (14, 322); DAN_BOX = (612, 345, 440, 1190); SCR_WH = (518, 982)
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
def chip_png(text, xy, size=23, u=2):
    """the AI-GENERATED chip (softblue.disclosure: the same solid rounded chip the film uses), as an RGBA layer + its box."""
    base = Image.new("RGB", (W, H), (0, 0, 0)); a = Image.new("RGB", (W, H), (255, 255, 255))
    B.disclosure(base, text, xy, u, anchor="lt", size=size); B.disclosure(a, text, xy, u, anchor="lt", size=size)
    x = np.asarray(base).astype(np.int16); y = np.asarray(a).astype(np.int16)
    al = 255 - (y - x).max(2).clip(0, 255); rgba = np.dstack([np.where(al[..., None] > 0, (x * 255 // np.maximum(al[..., None], 1)).clip(0, 255), 0), al]).astype(np.uint8)
    ys, xs = np.where(al > 0); return rgba, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)

class Short:
    def __init__(self, S):
        self.S = S; d = self.d = D(S); self.T = json.load(open(f"{d}/timeline.json")); self.N = self.T["frames"]
        self.shots = json.load(open(f"{d}/shots.json")); self.track = json.load(open(f"{d}/track.json")) if os.path.exists(f"{d}/track.json") else {}
        self.cues = json.load(open(f"{d}/cues.json"))
        # the Soft Blue field drifts (GRAPHICS-STANDARDS: "restrained drifting blue light"): keyframes every 0.5 s, blended per frame
        tsig = hashlib.sha256(json.dumps(P.TITLE[S]).encode()).hexdigest()[:10]
        kf = os.path.join(d, f"field_keys_{tsig}.npy"); nk = int(self.N / FPS / 0.5) + 2
        if os.path.exists(kf) and np.load(kf, mmap_mode="r").shape[0] == nk: self.keys = np.load(kf)
        else:
            ks = []
            for k in range(nk):
                bg = lib.canvas(k * 0.5); lib.band(bg, *P.TITLE[S]); ks.append(np.asarray(bg))
            self.keys = np.stack(ks); np.save(kf, self.keys)
        self.base = self.keys[0]
        self.cams = {}; self.clips = {}
        self.plan_windows()
        f = B.font(30); xy = (64, 1800)
        o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(o); dd.text((xy[0] + 2, xy[1] + 2), "AbsByAI.com", font=f, fill=(0, 0, 0, 140)); dd.text(xy, "AbsByAI.com", font=f, fill=(244, 250, 255, 170))
        if P.DISC.get(S):                                                          # a small on-screen disclaimer where a short needs one
            fd = B.font(24, bold=False); disc = P.DISC[S]; wd = B.text_w(disc, fd)
            dd.text((W - 64 - wd + 2, 1806), disc, font=fd, fill=(0, 0, 0, 140)); dd.text((W - 64 - wd, 1804), disc, font=fd, fill=(244, 250, 255, 170))
        self.wm = (np.asarray(o), (60, 1796, W - 60, 1850))
        # captions: one RGBA state per cue, at the caption top of the shot it starts in
        os.makedirs(f"{d}/cap", exist_ok=True); self.caps = []
        for i, c in enumerate(self.cues):
            sh = self.shot_at(min(fr(c["a"]), self.N - 1)); top = sh.get("cap", 1412)
            im = cap_png(c["lines"], top); p = f"{d}/cap/cue{i:03d}.png"; im.save(p); bb = im.getbbox()
            f0_, f1_ = fr(c["a"]), fr(c["b"])
            for s2 in self.shots[1:]:                        # a cut inside the cue's last 10 frames: the cue ends on the cut (reviewers 10-13: captions trailed 2 to 4 frames past cuts)
                if f0_ + 8 < s2["f0"] < f1_ <= s2["f0"] + 10: f1_ = s2["f0"]      # a cue lingers at most 0.30 s (9 frames) after its last word
            self.caps.append(dict(f0=f0_, f1=f1_, arr=np.asarray(im), box=bb, png=p, top=top))
        man = f"{d}/hf/manifest.json"; self.man = json.load(open(man)) if os.path.exists(man) else []
        self.ph = None
        if P.PICKUP.get(S, {}).get("placeholder") and self.T.get("head"):
            o2 = Image.new("RGB", (W, 100), (0, 0, 0)); bx_ = B.disclosure(o2, "PLACEHOLDER AUDIO: studio pickup 10/17", (W - 40, 10), 2, anchor="rt", size=17)
            self.ph = (np.asarray(o2), int(bx_[0]), fr(self.T["head"]))
        self.chips = {}
        import scenes; self.scenes = scenes
    def shot_at(self, i): return next(sh for sh in self.shots if sh["f0"] <= i < sh["f1"])
    def key(self, sh): return f"{sh['roll']}:{sh['raw0']:.2f}:{sh['raw1']:.2f}"
    def plan_windows(self):
        xs = []
        for sh in self.shots:
            if sh["kind"] not in ("talk", "phone"): continue
            trk = self.track.get(self.key(sh)) or [r for r in roll_track(self.d, sh["roll"]) if sh["raw0"] - 0.5 <= r["t"] <= sh["raw1"] + 0.5]
            if sh["kind"] == "phone": ch = sh.get("dh", 1080); cw = round(ch * DAN_BOX[2] / DAN_BOX[3]); sh.setdefault("y0", 0); sh.setdefault("cap", 1640)
            else: cw, ch = WIN[sh.get("win", "full")]; sh.setdefault("y0", P.Y0[sh.get("win", "full")])
            sh["cw"], sh["ch"] = cw, ch; sh["path"] = window_path(sh, trk, cw)
            xs += [float(sh["path"].min()) - cw / 2, float(sh["path"].max()) + cw / 2]
        if xs: self.strip = (max(0, int(min(xs)) // 2 * 2 - 2), min(1920, (int(max(xs)) + 3) // 2 * 2))
    def fidx(self, sh, raw):
        """source frame index. floor(x + 0.25), unless this take's phase sits on that boundary (the 4-decimal raw times then
        jitter across it and one source frame shows twice: reviewer r3a, S2 0:31.37 and S4 0:34.60): then floor(x + 0.5)."""
        if "_off" not in sh:
            ph = (sh["raw"][0] * FPS + 0.25) % 1; sh["_off"] = 0.25 if 0.1 < ph < 0.9 else 0.5
        return int(np.floor(raw * FPS + sh["_off"]))
    def picture(self, i, graphics=True):
        sh = self.shot_at(i); j = i - sh["f0"]; raw = sh["raw"][j]; roll = sh["roll"]
        u = i / FPS / 0.5; k = int(u); w = u - k
        frame = (self.keys[k].astype(np.float32) * (1 - w) + self.keys[k + 1].astype(np.float32) * w + 0.5).astype(np.uint8)
        if sh["kind"] == "talk":
            if roll not in self.cams: self.cams[roll] = cam(roll, *self.strip)
            src = self.cams[roll].get(self.fidx(sh, raw)); cw, ch = sh["cw"], sh["ch"]
            x = int(round((sh["path"][j] - cw / 2 - self.strip[0]) * 2)); y = sh["y0"] * 2
            frame[DROP:] = cv2.resize(src[y:y + ch * 2, x:x + cw * 2], (W, PIC_H), interpolation=cv2.INTER_AREA)
        elif sh["kind"] == "clip":
            c = sh["cover"]
            if c["id"] not in self.clips: self.clips[c["id"]] = clip_seq(c)
            bx, by, bw, bh = clip_box(c); frame[by:by + bh, bx:bx + bw] = self.clips[c["id"]].get(int(np.floor(raw * FPS + 0.25)))
            if graphics and c.get("ai"):
                x0_, y0_ = c["ai"][:2]; reg = Image.fromarray(frame[y0_ - 10:y0_ + 90, 0:W])            # the film's own chip (softblue.disclosure), drawn on the frame
                B.disclosure(reg, "AI-GENERATED", (x0_, 10), c["ai"][2] if len(c["ai"]) > 2 else 2, anchor="lt"); frame[y0_ - 10:y0_ + 90, 0:W] = np.asarray(reg)      # default size: the chip's own proportions (size 30 sat on its bottom edge, reviewers 10-13)
        elif sh["kind"] == "phone":                         # the approved shorts phone demo: phone beside Dan on the field (GRAPHICS-STANDARDS)
            c = sh["cover"]
            if "shell" not in self.__dict__:
                self.shell = np.asarray(phone_shell())
                m = Image.new("L", (DAN_BOX[2], DAN_BOX[3]), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, DAN_BOX[2] - 1, DAN_BOX[3] - 1), 28, fill=255); self.dmask = np.asarray(m)[..., None].astype(np.float32) / 255
            if c["id"] not in self.clips:                  # the app recording, its own status bar cropped off (RO-12 phone_frame), fitted inside the shell's screen
                self.clips[c["id"]] = Seq(c["src"], f"fps={FPSS}," + c.get("vf", f"crop=660:1330:0:104,scale=-2:{SCR_WH[1]}:flags=lanczos,pad={SCR_WH[0]}:{SCR_WH[1]}:(ow-iw)/2:0:color=0xF8FAFC") + ",format=rgb24", SCR_WH, FPS)
            px, py = PHONE_XY; box = (px, py, px + 624, py + 1290); full = np.zeros((H, W, 4), np.uint8); full[py:py + 1290, px:px + 624] = self.shell; over_box(frame, full, box)
            scr = self.clips[c["id"]].get(int(np.floor(sh["clip"][j] * FPS + 0.25)))
            if c.get("round"):                              # a recording that carries its own rounded bezel: its corner wedges take the page's own colour, so the page is a plain rectangle like any other
                if "smask" not in self.__dict__ or self.smask[0] != c["round"]:
                    mm = Image.new("L", SCR_WH, 0); ImageDraw.Draw(mm).rounded_rectangle((0, 0, SCR_WH[0] - 1, SCR_WH[1] - 1), c["round"], fill=255); self.smask = (c["round"], np.asarray(mm)[..., None].astype(np.float32) / 255)
                r_ = c["round"]; hh_, ww_ = scr.shape[:2]; out_ = scr.astype(np.float32); m_ = self.smask[1]
                for ys_, xs_, sy_, sx_ in ((slice(0, r_), slice(0, r_), 3, r_ + 6), (slice(0, r_), slice(ww_ - r_, ww_), 3, ww_ - r_ - 7),
                                           (slice(hh_ - r_, hh_), slice(0, r_), hh_ - 4, r_ + 6), (slice(hh_ - r_, hh_), slice(ww_ - r_, ww_), hh_ - 4, ww_ - r_ - 7)):
                    bg_ = np.median(scr[sy_ - 2:sy_ + 3, sx_ - 3:sx_ + 4].reshape(-1, 3), 0).astype(np.float32)      # each wedge takes the colour of the page edge right beside it, frame by frame
                    out_[ys_, xs_] = bg_ * (1 - m_[ys_, xs_]) + out_[ys_, xs_] * m_[ys_, xs_]
                scr = (out_ + 0.5).astype(np.uint8)
            if c.get("darkfill") and scr[4:40, 20:SCR_WH[0] - 20].mean() < 45:      # a black screen in the recording (the iPhone camera): the WHOLE phone screen goes black, not a black box inside a white one (reviewers, 10-13)
                if "scrmask" not in self.__dict__:
                    mm = Image.new("L", (W, H), 0); ImageDraw.Draw(mm).rounded_rectangle((px + 38, py + 36, px + 38 + 538, py + 36 + 1200), 65, fill=255); self.scrmask = np.asarray(mm) > 127
                frame[self.scrmask] = (0, 0, 0)
                scr = scr.copy(); k_ = (SCR_WH[0] - 488) // 2; scr[:, :k_ + 1] = 0; scr[:, SCR_WH[0] - k_ - 1:] = 0      # the white side padding of the fitted recording (488 px wide in a 518 px screen)
            frame[py + 114:py + 114 + SCR_WH[1], px + 48:px + 48 + SCR_WH[0]] = scr
            if roll not in self.cams: self.cams[roll] = cam(roll, *self.strip)
            src = self.cams[roll].get(self.fidx(sh, raw)); cw, ch = sh["cw"], sh["ch"]
            x = int(round((sh["path"][j] - cw / 2 - self.strip[0]) * 2)); y = sh["y0"] * 2
            dn = cv2.resize(src[y:y + ch * 2, x:x + cw * 2], (DAN_BOX[2], DAN_BOX[3]), interpolation=cv2.INTER_AREA).astype(np.float32)
            bx, by = DAN_BOX[0], DAN_BOX[1]; reg = frame[by:by + DAN_BOX[3], bx:bx + DAN_BOX[2]].astype(np.float32)
            frame[by:by + DAN_BOX[3], bx:bx + DAN_BOX[2]] = (reg * (1 - self.dmask) + dn * self.dmask + 0.5).astype(np.uint8)
        else:                                               # a rebuilt film graphic that fills the picture area
            im = self.scenes.SCENES[sh["cover"]["scene"]](raw, sh["cover"], i / FPS)
            frame[DROP:] = np.asarray(im) if graphics else frame[DROP:]
        return frame, sh
    def finish(self, frame, sh, i, C=None):
        if C is not None: frame = np.ascontiguousarray(C.apply(frame, i))
        wm, box = self.wm; over_box(frame, wm, box)
        if self.ph is not None and i < self.ph[2]: frame[330:420, self.ph[1] - 4:W - 36] = self.ph[0][6:96, self.ph[1] - 4:W - 36]      # only while the placeholder pickup plays
        for c in self.caps:
            if c["f0"] <= i < c["f1"]: over_box(frame, c["arr"], c["box"])
        return frame
    def close(self):
        for c in list(self.cams.values()) + list(self.clips.values()): c.close()

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
