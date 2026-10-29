"""RO-37 builder: edl.json pieces -> shots (T/W alternate at every cut, long pieces split at word gaps) -> per-segment ffmpeg
renders (presenter via frames.graph; full-screen clips via the library master + tune curve + name chip) -> concat base ->
voice (lav pieces, 40 ms crossfades, chosen EQ through voice_chain) -> HyperFrames overlays (composite.py) -> draft.
usage: build.py shots | field <dur> | range <t0> <t1> <out.mp4>"""
import sys, os, json, subprocess, glob, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import frames as F
W = F.W; FF = F.FF; FPS = F.FPS; SR = 48000; P = F.P
def fr(t): return int(round(t * FPS))
def run(c): subprocess.run(c, check=True)
CHIP_FONT = "/Volumes/Expansion/_edit_work/RO-37/round1/assets/Poppins-Bold.ttf"

def words(roll):
    d = json.load(open(f"{W}/words_{roll}.json"))
    return d[0] if isinstance(d, list) and d and isinstance(d[0], list) else d

def make_shots(edl, max_len=9.0, min_len=3.0):
    """One shot per piece; a piece longer than max_len is split at its widest word gaps (>= 0.18 s) into runs of
    min_len..max_len, so the picture changes size at least every ~9 s. Framing alternates T/W from the opening W."""
    shots, o = [], 0
    for p in edl:
        ws = [w for w in words(p["roll"]) if p["in"] <= w["t"] and w["e"] <= p["out"] + 0.05]
        cuts = [p["in"]]
        while p["out"] - cuts[-1] > max_len:
            cand = [((b["t"] - a["e"]), (a["e"] + b["t"]) / 2) for a, b in zip(ws, ws[1:])
                    if cuts[-1] + min_len <= (a["e"] + b["t"]) / 2 <= cuts[-1] + max_len and p["out"] - (a["e"] + b["t"]) / 2 >= min_len]
            if not cand: break
            g, t = max(cand); cuts.append(round(t, 3))
        cuts.append(p["out"])
        for k, (a, b) in enumerate(zip(cuts, cuts[1:])):
            n = fr(b - a)
            shots.append(dict(id=f"{p['id']}.{k}", roll=p["roll"], src0=a, src1=b, out_f0=o, out_f1=o + n, reframe=k > 0))
            o += n
    for i, s in enumerate(shots): s["framing"] = "W" if i % 2 == 0 else "T"
    return shots

def lt_framing(shots, R, min_rem=1.2):
    """A lower third sits across the panel's waist on the upright W picture (round-1 self-check: it covered the abs), so every
    lower third plays on the close-up: a W shot under one is split at the lower third's in/out (a zoom cut on a word start,
    the size changes 2x) and the middle becomes T. A W remnant shorter than min_rem joins the T part."""
    lts = sorted((fr(r["t0"]) - 2, fr(r["t1"]) + 2) for r in R if r["kind"] == "lt" and r.get("t1"))
    out = []
    for s in shots:
        parts = [dict(s)]
        if s["framing"] == "W":
            for a, b in lts:
                nxt = []
                for p in parts:
                    if p["framing"] != "W" or b <= p["out_f0"] or a >= p["out_f1"]: nxt.append(p); continue
                    cuts = [p["out_f0"], max(p["out_f0"], a), min(p["out_f1"], b), p["out_f1"]]
                    if cuts[1] - cuts[0] < fr(min_rem): cuts[1] = cuts[0]
                    if cuts[3] - cuts[2] < fr(min_rem): cuts[2] = cuts[3]
                    for k, (x, y) in enumerate(zip(cuts, cuts[1:])):
                        if y <= x: continue
                        q = dict(p, out_f0=x, out_f1=y, src0=round(p["src0"] + (x - p["out_f0"]) / FPS, 4), framing="T" if k == 1 else "W")
                        q["reframe"] = p["reframe"] if x == p["out_f0"] else True
                        nxt.append(q)
                parts = nxt
        out += parts
    for i, s in enumerate(out): s["src1"] = round(s["src0"] + (s["out_f1"] - s["out_f0"]) / FPS, 4)
    m = []                                      # same-take close-ups back to back are one continuous shot (no cut)
    for s in out:
        if m and s["reframe"] and s["framing"] == m[-1]["framing"] and s["roll"] == m[-1]["roll"]:
            m[-1]["out_f1"] = s["out_f1"]; m[-1]["src1"] = round(m[-1]["src0"] + (m[-1]["out_f1"] - m[-1]["out_f0"]) / FPS, 4)
        else: m.append(dict(s))
    for a, b in zip(m, m[1:]):                  # a take join between two close-ups: the later one goes tighter (T2)
        if a["framing"] == "T" and b["framing"] == "T" and not b["reframe"]: b["framing"] = "T2"
    for i, s in enumerate(m): s["id"] = f"{s['id'].split('~')[0]}~{i}"
    return m

def jumps(shots, R):
    """Joins between two same-size framings (W/W or T/T) that no full-screen clip covers (should be none, or only reframes of one take)."""
    clips = [(fr(r["t0"]), fr(r["t1"])) for r in R if r["kind"] == "clip" and r.get("t1")]
    return [(round(b["out_f0"] / FPS, 2), a["framing"], b["reframe"]) for a, b in zip(shots, shots[1:])
            if a["framing"] == b["framing"] and not any(x <= b["out_f0"] < y for x, y in clips)]

VOICES = {
    "A": ("Natural Warmth", "highpass=f=70,equalizer=f=140:t=q:w=1:g=1.5,equalizer=f=450:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.5:g=-0.5,equalizer=f=120:t=q:w=0.8:g=1.5"),
    "B": ("Fuller Bass", "highpass=f=70,equalizer=f=140:t=q:w=1:g=1.5,equalizer=f=450:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.5:g=-0.5,equalizer=f=120:t=q:w=0.8:g=3"),
    "C": ("Original Mic, Matched Volume", "anull"),
    "D": ("Automatic Reference Match", None),
}
VOICE_KEY = os.environ.get("RO37_VOICE", "A")
NOEXP = "Dry outdoor lav; keep natural word tails (same as the approved DS-84/DS-76 pool set)."

def lav(roll):
    wv = wave.open(f"{W}/lav_{roll}.wav"); return np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32) / 32768

def assemble_audio(shots, out_wav, xf=0.04):
    """Sample-exact to the picture: shot k fills samples [round(f0/FPS*SR), round(f1/FPS*SR)). At a join between two
    pieces (not a reframe of one take) both sides run 20 ms past the join and crossfade over 40 ms (DS-76 lesson)."""
    L = {}; n_tot = round(shots[-1]["out_f1"] / FPS * SR); y = np.zeros(n_tot + SR, np.float32); h = round(xf / 2 * SR)
    for i, s in enumerate(shots):
        if s["roll"] not in L: L[s["roll"]] = lav(s["roll"])
        a, b = round(s["out_f0"] / FPS * SR), round(s["out_f1"] / FPS * SR)
        join_in = i > 0 and not s["reframe"]; join_out = i + 1 < len(shots) and not shots[i + 1]["reframe"]
        pa, pb = a - (h if join_in else 0), b + (h if join_out else 0)
        s0 = round(s["src0"] * SR) - (a - pa)
        seg = L[s["roll"]][max(0, s0): max(0, s0) + (pb - pa)].copy()
        seg = np.pad(seg, (0, (pb - pa) - len(seg)))
        g = np.ones(len(seg), np.float32)
        if join_in: g[:2 * h] = np.linspace(0, 1, 2 * h)
        if join_out: g[-2 * h:] = np.linspace(1, 0, 2 * h)
        y[max(0, pa):pb] += (seg * g)[max(0, -pa):]
    y = y[:n_tot]
    o = wave.open(out_wav, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes()); o.close()

def voice(raw, out, key=None):
    k = key or VOICE_KEY; eq = VOICES[k][1]
    cmd = ["python3", f"{P}/.claude/skills/_shared/audio/voice_chain.py", "--in", raw, "--pull", "anull", "--out", out,
           "--work", out + ".work", "--no-expander-because", NOEXP]
    if eq: cmd += ["--eq", eq]
    run(cmd)

def field(dur, out):
    """The moving Soft Blue Light field, film clock, as a video (input for W segments with bg field)."""
    sys.path.insert(0, f"{P}/.claude/skills/_shared"); import softblue as SB
    n = fr(dur) + 2
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "30000/1001",
                          "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(SB.field(i / FPS, 1920, 1080).convert("RGB").tobytes())
    p.stdin.close(); p.wait()

def chip_png(text, out):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(CHIP_FONT, 44); w = int(f.getlength(text)) + 64
    im = Image.new("RGBA", (w, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 79], 24, fill=(6, 17, 30, 235), outline=(64, 112, 153, 255), width=2)
    d.text((32, 40), text, font=f, fill=(244, 250, 255, 255), anchor="lm"); im.save(out); return out

ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-r", "30000/1001", "-an"]

def render_presenter(shot, f0, f1, px, out, bg="field"):
    """Frames [f0, f1) of the film inside this shot."""
    n = f1 - f0; ts = shot["src0"] + (f0 - shot["out_f0"]) / FPS
    cmd = [FF, "-nostdin", "-v", "error", "-y", "-ss", f"{ts:.4f}", "-i", F.ROLLS[shot["roll"]], "-loop", "1", "-framerate", "30000/1001", "-i", F.ensure_mask()]
    if shot["framing"] == "W" and bg == "field": cmd += ["-ss", f"{f0 / FPS:.4f}", "-i", f"{W}/field.mp4"]
    a, b = shot["src0"], shot["src1"]
    cmd += ["-filter_complex", F.graph(shot["framing"], shot["roll"], a, b, bg, px), "-map", "[v]", "-frames:v", str(n)] + ENC + [out]
    run(cmd)

def render_clip(it, f0, f1, out):
    import broll_tune as BT
    cid, s0 = it["src"].split("@")[0], float(it["src"].split("@")[1])
    g = json.load(open(f"{W}/broll/grade.json")).get(f"{cid}@{s0}", {})
    path = g.get("path") or BT.path(cid); vf = g.get("vf", "")
    ts = s0 + (f0 - fr(it["t0"])) / FPS; n = f1 - f0
    chain = f"[0:v]{F.DEC},{vf + ',' if vf else ''}scale=1920:1080:flags=lanczos,format=yuv420p[c]"
    cmd = [FF, "-nostdin", "-v", "error", "-y", "-ss", f"{ts:.4f}", "-i", path]
    if it.get("chip"):
        cp = chip_png(it["chip"], f"{W}/broll/chip_{it['id']}.png"); cmd += ["-loop", "1", "-i", cp]
        chain += ";[c][1:v]overlay=64:952:format=auto,format=yuv420p[v]"
    else: chain += ";[c]null[v]"
    cmd += ["-filter_complex", chain, "-map", "[v]", "-frames:v", str(n)] + ENC + [out]
    run(cmd)

def segments(shots, R, f0, f1):
    """Picture segments of [f0, f1): ('clip', item) where a full-screen clip is up, else ('pres', shot, px)."""
    clips = [(fr(r["t0"]), fr(r["t1"]), r) for r in R if r["kind"] == "clip" and r.get("t1")]
    cards = [(fr(r["t0"]), fr(r["t1"])) for r in R if r["kind"] in ("l3",) and r.get("t1")]
    cuts = {f0, f1} | {s["out_f0"] for s in shots} | {a for a, b, _ in clips} | {b for a, b, _ in clips} | {a for a, b in cards} | {b for a, b in cards}
    cuts = sorted(c for c in cuts if f0 <= c <= f1); out = []
    for a, b in zip(cuts, cuts[1:]):
        c = next((r for x, y, r in clips if x <= a < y), None)
        if c: out.append(("clip", a, b, c)); continue
        sh = next(s for s in shots if s["out_f0"] <= a < s["out_f1"])
        px = "right" if any(x <= a < y for x, y in cards) else "center"
        out.append(("pres", a, b, sh, px))
    # a W segment that starts where a card starts or ends, inside the same shot as the segment before it, slides
    for k in range(1, len(out)):
        p, q = out[k - 1], out[k]
        if p[0] == "pres" and q[0] == "pres" and p[3]["id"] == q[3]["id"] and q[3]["framing"] == "W" and p[4] != q[4]:
            out[k] = ("pres", q[1], q[2], q[3], ("slide", p[4], q[4], 14))
    # a T shot cannot hold a side card: under a card the shot is W (right)
    out = [(o[0], o[1], o[2], dict(o[3], framing="W"), o[4]) if o[0] == "pres" and o[4] == "right" and o[3]["framing"] == "T" else o for o in out]
    return out

def render_range(t0, t1, out, R=None):
    shots = json.load(open(f"{W}/shots.json")); R = R if R is not None else json.load(open(f"{W}/plan_resolved.json"))
    f0, f1 = fr(t0), fr(t1); d = out + ".segs"; os.makedirs(d, exist_ok=True); lst = []
    for k, sg in enumerate(segments(shots, R, f0, f1)):
        p = f"{d}/{k:04d}.mp4"
        if sg[0] == "clip": render_clip(sg[3], sg[1], sg[2], p)
        else: render_presenter(sg[3], sg[1], sg[2], sg[4], p)
        lst.append(p)
    open(f"{d}/list.txt", "w").write("".join(f"file '{p}'\n" for p in lst))
    run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt", "-c", "copy", out])

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "shots":
        sh = make_shots(json.load(open(f"{W}/edl.json"))); json.dump(sh, open(f"{W}/shots.json", "w"), indent=1)
        print(len(sh), "shots,", round(sh[-1]["out_f1"] / FPS, 1), "s")
    elif cmd == "ltframing":
        R = json.load(open(f"{W}/plan_resolved.json")); sh = lt_framing(make_shots(json.load(open(f"{W}/edl.json"))), R)
        json.dump(sh, open(f"{W}/shots.json", "w"), indent=1); print(len(sh), "shots; same-size joins:", jumps(sh, R))
    elif cmd == "field": field(float(sys.argv[2]), f"{W}/field.mp4")
    elif cmd == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
