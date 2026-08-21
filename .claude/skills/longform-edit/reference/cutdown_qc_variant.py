#!/usr/bin/env python3
"""QC for a cut-down variant. The full v3 gate plus the one check a cut-down
actually needs: EVERY new joint re-transcribed from the FINISHED render.

  duration vs plan | integrated loudness | splice discontinuity vs the file's own
  control ceiling | mid-speech fade notches vs a 40-control p90 | SRT text gate |
  chips on/off separation | per-joint re-transcription (word-presence, the only
  check that sees a clipped trailing fricative) | phrase-shingle repeat scan |
  contact sheets at every new joint.

Usage: python3 qc_variant.py cons|sub30
"""
import json, math, random, re, struct, subprocess, sys, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
V = sys.argv[1]
NAME = "INVEST_HEALTH_conservative" if V == "cons" else "INVEST_HEALTH_sub30"
D = HERE / V
VIDEO = D / "out" / f"{NAME}.mp4"
SRT = D / "out" / f"{NAME}.srt"
TMP = D / "_qc"; TMP.mkdir(exist_ok=True)
SHEETS = D / "_qc_sheets"; SHEETS.mkdir(exist_ok=True)

edl = json.load(open(D / "edl.json"))
ranges = edl["ranges"]
offs, acc = [], 0.0
for r in ranges:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc
JOINTS = json.load(open(D / "new_joints.json"))["joints"]

def sh(*a):
    return subprocess.run(list(a), capture_output=True, text=True)

fails, warns = [], []
def check(ok, msg):
    print(f"[{'OK' if ok else 'FAIL'}] {msg}")
    if not ok: fails.append(msg)

print(f"=== QC {V}: {VIDEO.name} ===")
dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(VIDEO)).stdout.strip())
# Per-segment frame rounding at 29.97 accumulates over the concat, so the
# tolerance scales with the range count (~0.016 s/range measured on v3) instead
# of being a flat 2.5 s that a 163-range cut-down would trip for no reason.
tol = max(2.5, 0.04 * len(ranges))
check(abs(dur - TOTAL) < tol,
      f"duration {dur:.2f}s ({dur/60:.2f} min) vs plan {TOTAL:.2f}s "
      f"(drift {dur-TOTAL:+.2f}s, tolerance {tol:.1f}s over {len(ranges)} ranges)")
if V == "sub30":
    check(dur < 1800, f"sub30 hard gate: {dur:.2f}s < 30:00")

proc = sh("ffmpeg", "-hide_banner", "-nostats", "-i", str(VIDEO),
          "-af", "loudnorm=print_format=json", "-vn", "-f", "null", "-")
m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', proc.stderr)
lufs = float(m.group(1)) if m else None
tp = re.search(r'"input_tp"\s*:\s*"(-?[\d.]+)"', proc.stderr)
check(lufs is not None and abs(lufs + 14) <= 1.2,
      f"loudness {lufs} LUFS (true peak {tp.group(1) if tp else '?'} dBTP)")

# ---- splices: fail only above the file's own natural ceiling ----
wav = TMP / "audio.wav"
if not wav.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1",
                    "-ar", "48000", "-c:a", "pcm_s16le", str(wav)], check=True)
wf = wave.open(str(wav), "rb"); sr = wf.getframerate(); n = wf.getnframes()
samples = struct.unpack(f"<{n}h", wf.readframes(n)); wf.close()
def max_jump(c, win=0.004):
    a = max(1, int((c - win) * sr)); b = min(n - 1, int((c + win) * sr))
    return max(abs(samples[i] - samples[i - 1]) for i in range(a, b))
random.seed(7)
ctrls = sorted(max_jump(random.uniform(5, TOTAL - 5)) for _ in range(120))
med = ctrls[len(ctrls) // 2] or 1
ceil = ctrls[-1] * 1.25
bad = [(o, max_jump(o)) for o in offs[1:] if 0.05 < o < dur - 0.05 and max_jump(o) > ceil]
check(not bad, "splices: %d/%d joins above the control ceiling %s"
      % (len(bad), len(offs) - 1, " ".join(f"{o:.0f}s({j/med:.1f}x)" for o, j in bad[:8])))

# ---- artificial mid-speech splits: measure the notch, don't trust the proxy ----
def notch_db(o, half=0.20, step_s=0.002):
    p = TMP / "dip.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{o-half:.3f}", "-i", str(VIDEO),
                    "-t", f"{2*half:.3f}", "-vn", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(p)], check=True)
    w = wave.open(str(p)); nn = w.getnframes()
    sm = struct.unpack(f"<{nn}h", w.readframes(nn)); w.close()
    st = int(step_s * 48000); e = []
    for i in range(0, nn - st, st):
        ch = sm[i:i + st]
        e.append(20 * math.log10((sum(x * x for x in ch) / len(ch)) ** 0.5 / 32768 + 1e-9))
    return sorted(e)[len(e) // 2] - min(e)
close = [(i + 1, a["beat"], b["beat"]) for i, (a, b) in enumerate(zip(ranges, ranges[1:]))
         if a["source"] == b["source"] and 0 <= b["start"] - a["end"] < 0.20]
if close:
    random.seed(11)
    ctrl_notch = sorted(notch_db(random.uniform(60, TOTAL - 60)) for _ in range(40))
    ceil_notch = ctrl_notch[int(0.9 * len(ctrl_notch))]
    deep = []
    for idx, A, B in close:
        d = notch_db(offs[idx])
        print(f"    close pair {A} -> {B} @ {offs[idx]:.2f}s: notch {d:.1f} dB "
              f"(control p90 {ceil_notch:.1f} dB)")
        if d > ceil_notch: deep.append((A, B, round(d, 1)))
    check(not deep, f"mid-speech fade notches above the control p90: {deep}")
else:
    check(True, "artificial mid-speech splits: none")

# ---- SRT text gate ----
if SRT.exists():
    body = SRT.read_text()
    check("GOP" not in body, f"SRT contains 'GOP' ({body.count('GOP')} hits)")
    for pat in ("Terzepetide", "Tersepityde", "reditrutide", "osepic", "Aura ring"):
        check(pat not in body, f"SRT contains unfixed spelling {pat!r}")
    cues = body.strip().split("\n\n")
    longest = max((len(l) for c in cues for l in c.split("\n")[2:]), default=0)
    check(longest <= 50, f"SRT longest caption line {longest} chars")
else:
    check(False, f"SRT missing at {SRT}")

# ---- chips on/off ----
import PIL.Image as I
chips = json.load(open(D / "chip_timings.json"))
def region_mean(t):
    p = TMP / "f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(VIDEO),
                    "-frames:v", "1", str(p)], check=True)
    im = I.open(p).convert("L").crop((110, 790, 900, 920))
    return sum(im.getdata()) / (im.width * im.height)
on = [region_mean(c["start"] + 3.0) for c in chips[:6]]
off = [region_mean(c["end"] + 3.0) for c in chips[:6] if c["end"] + 3.0 < dur]
sep_up = min(on) > max(off) + 5
sep_dn = max(on) < min(off) - 5
check(sep_up or sep_dn,
      f"chips on/off separated (on {min(on):.0f}-{max(on):.0f} vs off {min(off):.0f}-{max(off):.0f})")

# ---- contact sheets at every new joint ----
for j in JOINTS:
    t = j["out_t"]
    if t < 1.5 or t > dur - 1.5: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t-1.2:.2f}", "-i", str(VIDEO),
                    "-t", "2.4", "-vf", "fps=1,scale=480:-1,tile=3x1",
                    str(SHEETS / f"joint_{t:.0f}s.jpg")], check=True)
print(f"contact sheets for {len(JOINTS)} new joints -> {SHEETS}")

# ---- re-transcribe EVERY new joint from the FINISHED render ----
import whisper
model = whisper.load_model("small")
def norm(x): return re.sub(r"[^a-z0-9]", "", x.lower())
print(f"\nre-transcribing {len(JOINTS)} new joints (window ends 6s PAST the join):")
joint_flags = []
for j in JOINTS:
    t = j["out_t"]
    a = max(0.0, t - 4.0)
    snip = TMP / "snip.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(VIDEO),
                    "-t", "10", "-vn", "-ac", "1", "-ar", "16000", str(snip)], check=True)
    txt = model.transcribe(str(snip), fp16=False, language="en")["text"].strip()
    got = norm(txt)
    lhs = j["join"].split("]|[")[0].split(); rhs = j["join"].split("]|[")[1].split()
    lastw = norm(lhs[-1]) if lhs else ""
    firstw = norm(rhs[0]) if rhs else ""
    miss = [w for w in (lastw, firstw) if w and w not in got]
    tag = "" if not miss else f"   <-- CHECK: {miss} not in re-transcription"
    if miss: joint_flags.append((t, j["beats"], miss, txt))
    print(f"  {t:8.1f}s {j['beats'][:38]:40s} :: {txt[:110]}{tag}")
print(f"\n{len(joint_flags)} joints to eyeball of {len(JOINTS)}")

# ---- phrase repeat scan over the FINISHED transcript ----
print("\nphrase repeat scan (3-5 word shingles, +/-30s) on the finished render:")
full = TMP / "full16k.wav"
if not full.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1",
                    "-ar", "16000", str(full)], check=True)
res = model.transcribe(str(full), fp16=False, language="en", word_timestamps=True)
words = [(w["word"].strip().lower().strip(".,!?"), w["start"])
         for s in res["segments"] for w in s.get("words", [])]
words = [w for w in words if w[0]]
json.dump([{"t": t, "w": w} for w, t in words], open(TMP / "words.json", "w"))
hits = {}
for N in (5, 4, 3):
    seen = {}
    for i in range(len(words) - N):
        key = " ".join(w for w, _ in words[i:i + N]); t = words[i][1]
        for prev in seen.get(key, []):
            if 0 < t - prev <= 30:
                hits.setdefault(key, set()).add((round(prev, 1), round(t, 1)))
        seen.setdefault(key, []).append(t)
final = []
for k in sorted(hits, key=lambda k: -len(k.split())):
    if not any(k in kk for kk in (x[0] for x in final)):
        final.append((k, sorted(hits[k])))
for k, pairs in final:
    print(f"  {k!r} -> {pairs[:3]}")
print(f"({len(final)} phrase repeats to eyeball)")

json.dump({"joint_flags": [{"t": t, "beats": b, "missing": m, "text": x}
                           for t, b, m, x in joint_flags]},
          open(D / "qc_joint_flags.json", "w"), indent=1)
print("\n" + (f"QC {V} PASSED" if not fails else f"QC {V} FAILURES: " + "; ".join(fails)))
