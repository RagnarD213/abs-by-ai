#!/usr/bin/env python3
"""QC v3. Adds to qc_v2: the v3 revision joints re-transcribed from the FINISHED
render, a phrase-level (3-5 word shingle) repeat scan over the whole finished
transcript, the SRT text gate, and zoom-contrast frame pairs.
Usage: python3 qc_v3.py ../roughcuts/INVEST_HEALTH_v3.mp4"""
import json, subprocess, sys, wave, struct, re, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = Path(sys.argv[1])
edl = json.load(open(HERE / "edl.json"))
ranges = edl["ranges"]
offs = []; acc = 0.0
for r in ranges:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc

def src_to_out(t):
    for r, o in zip(ranges, offs):
        if r["start"] - 0.5 <= t <= r["end"] + 0.5:
            return o + max(0.0, min(t, r["end"]) - r["start"])
    return None

def sh(*a, **k):
    return subprocess.run(list(a), capture_output=True, text=True, **k)

fails = []
def check(ok, msg):
    print(f"[{'OK' if ok else 'FAIL'}] {msg}")
    if not ok: fails.append(msg)

dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(VIDEO)).stdout.strip())
check(abs(dur - TOTAL) < 2.5, f"duration {dur:.2f}s vs plan {TOTAL:.2f}s")

proc = sh("ffmpeg", "-hide_banner", "-nostats", "-i", str(VIDEO),
          "-af", "loudnorm=print_format=json", "-vn", "-f", "null", "-")
m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', proc.stderr)
lufs = float(m.group(1)) if m else None
check(lufs is not None and abs(lufs + 14) <= 1.2, f"loudness {lufs} LUFS")

# ---- splices: fail only above the file's own natural ceiling ----
wav = HERE / "_qc3_audio.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1",
                "-ar", "48000", "-c:a", "pcm_s16le", str(wav)], check=True)
wf = wave.open(str(wav), "rb"); sr = wf.getframerate(); n = wf.getnframes()
samples = struct.unpack(f"<{n}h", wf.readframes(n)); wf.close()
def max_jump(c, win=0.004):
    a = max(1, int((c - win) * sr)); b = min(n - 1, int((c + win) * sr))
    return max(abs(samples[i] - samples[i - 1]) for i in range(a, b))
random.seed(7)
ctrls = sorted(max_jump(random.uniform(5, TOTAL - 5)) for _ in range(120))
med = ctrls[len(ctrls)//2] or 1; ceil = ctrls[-1] * 1.25
bad = [(o, max_jump(o)) for o in offs[1:] if 0.05 < o < dur - 0.05 and max_jump(o) > ceil]
check(not bad, "splices: %d/%d joins above the control ceiling %s"
      % (len(bad), len(offs) - 1, " ".join(f"{o:.0f}s({j/med:.1f}x)" for o, j in bad[:6])))

# ---- artificial mid-speech splits ----
# The gap-only version of this test (adjacent ranges closer than 0.20s) is a
# STRUCTURAL proxy: render.py's 30ms fade-out + fade-in leaves an amplitude
# notch, and max-sample-to-sample-jump can't see a dip. But the proxy is not the
# defect. On v3 it flagged bars-clubs->entertainment and outsource->maid-laundry;
# a 2ms RMS envelope put their notches at 14.0 and 19.6 dB below the local
# median, INSIDE the control distribution (12.4-20.9 dB over 5 random non-join
# points), and re-transcribing both from the finished render returned clean
# continuous speech. So: report every close pair, but only FAIL when the notch
# is deeper than the file's own natural ceiling. (Same lesson as the splice
# metric and the circular cut-cleanliness metric — verify the metric first.)
def notch_db(o, half=0.20, step_s=0.002):
    p = HERE / "_qc3_dip.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{o-half:.3f}", "-i", str(VIDEO),
                    "-t", f"{2*half:.3f}", "-vn", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(p)], check=True)
    w = wave.open(str(p)); nn = w.getnframes()
    sm = struct.unpack(f"<{nn}h", w.readframes(nn)); w.close()
    st = int(step_s * 48000); e = []
    for i in range(0, nn - st, st):
        ch = sm[i:i + st]
        import math as _m
        e.append(20 * _m.log10((sum(x * x for x in ch) / len(ch)) ** 0.5 / 32768 + 1e-9))
    return sorted(e)[len(e)//2] - min(e)

close = [(i + 1, a["beat"], b["beat"]) for i, (a, b) in enumerate(zip(ranges, ranges[1:]))
         if 0 <= b["start"] - a["end"] < 0.20]
if close:
    random.seed(11)
    # 6 controls is NOT enough — the notch ceiling swung 18.4 -> 165.9 dB between
    # seeds at N=6 vs N=50. Use 40 and fail on the p90, not the max.
    ctrl_notch = sorted(notch_db(random.uniform(60, TOTAL - 60)) for _ in range(40))
    ceil_notch = ctrl_notch[int(0.9 * len(ctrl_notch))]
    deep = []
    for idx, A, B in close:
        d = notch_db(offs[idx])
        print(f"    close pair {A} -> {B} @ {offs[idx]:.2f}s: notch {d:.1f} dB "
              f"(control ceiling {ceil_notch:.1f} dB)")
        if d > ceil_notch: deep.append((A, B, round(d, 1)))
    check(not deep, f"mid-speech fade notches above the control ceiling: {deep}")
else:
    check(True, "artificial mid-speech splits: none")

# ---- SRT text gate ----
srt = VIDEO.with_suffix(".srt")
if srt.exists():
    body = srt.read_text()
    check("GOP" not in body, f"SRT contains 'GOP' ({body.count('GOP')} hits)")
    for pat in ("Terzepetide", "Tersepityde", "reditrutide", "osepic", "Aura ring"):
        check(pat not in body, f"SRT contains unfixed spelling {pat!r}")
else:
    check(False, f"SRT missing at {srt}")

# ---- zoom contrast: adjacent ranges must alternate punch-in ----
import PIL.Image as I
def frame(t, p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(VIDEO),
                    "-frames:v", "1", p], check=True)
    return I.open(p)
zoom_pairs = []
for idx in [3, 20, 45, 70, 95]:
    if idx + 1 >= len(offs): continue
    j = offs[idx + 1]
    if j < 2 or j > dur - 2: continue
    a = frame(j - 0.6, "/tmp/ihv3/zA.png"); b = frame(j + 0.6, "/tmp/ihv3/zB.png")
    a.save(f"/tmp/ihv3/zoom_{idx}_before.jpg"); b.save(f"/tmp/ihv3/zoom_{idx}_after.jpg")
    zoom_pairs.append((idx, j))
print("zoom frame pairs written to /tmp/ihv3 for", [z[0] for z in zoom_pairs])

# ---- v3 revision joints, re-transcribed from the FINISHED render ----
import whisper
model = whisper.load_model("small")
SPOTS = [
    ("v3-2 all-kinds-repeat", 524.4),
    ("v3-4a doubled-oura",    2711.9),
    ("v3-5 supplements",      3057.8),
    ("v3-6 bryan-johnson",    3800.4),
    ("v2 6:39 region",        520.0),
    ("v2 36:25 whoop",        2773.5),
]
print("\nrevision joints — transcribed from the finished video (±1.5s past the join):")
for label, st in SPOTS:
    ot = src_to_out(st)
    if ot is None:
        print(f"  {label}: not mapped (source time was cut)"); continue
    snip = HERE / "_qc3_snip.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, ot-4):.2f}", "-i", str(VIDEO),
                    "-t", "10", "-vn", "-ac", "1", "-ar", "16000", str(snip)], check=True)
    txt = model.transcribe(str(snip), fp16=False, language="en")["text"].strip()
    print(f"  {label:24s} out {ot:7.1f}s :: {txt}")

# ---- phrase-level repeat scan over the FINISHED transcript ----
print("\nphrase repeat scan (3-5 word shingles, +/-30s window) — full render transcript:")
full = HERE / "_qc3_16k.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1",
                "-ar", "16000", str(full)], check=True)
res = model.transcribe(str(full), fp16=False, language="en", word_timestamps=True)
words = [(w["word"].strip().lower().strip(".,!?"), w["start"])
         for s in res["segments"] for w in s.get("words", [])]
words = [w for w in words if w[0]]
json.dump([{"t": t, "w": w} for w, t in words], open(HERE / "_qc3_words.json", "w"))
hits = {}
for N in (5, 4, 3):
    seen = {}
    for i in range(len(words) - N):
        key = " ".join(w for w, _ in words[i:i + N])
        t = words[i][1]
        for prev in seen.get(key, []):
            if 0 < t - prev <= 30:
                hits.setdefault(key, set()).add((round(prev, 1), round(t, 1)))
        seen.setdefault(key, []).append(t)
# drop shorter shingles fully contained in a reported longer one
keys = sorted(hits, key=lambda k: -len(k.split()))
final = []
for k in keys:
    if not any(k in kk for kk in (x[0] for x in final)):
        final.append((k, sorted(hits[k])))
for k, pairs in final:
    print(f"  {k!r} -> {pairs[:3]}")
print(f"({len(final)} phrase repeats to eyeball — anaphora is deliberate, "
      f"re-INTRODUCTIONS of the same item are junk)")

print("\n" + ("QC v3 PASSED" if not fails else "QC v3 FAILURES: " + "; ".join(fails)))
