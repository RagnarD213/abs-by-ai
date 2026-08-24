#!/usr/bin/env python3
"""Output-timeline model: words, beats and the 5 ms RMS envelope of the clean voice.

Everything downstream (pause removal, insert planning, graphics, captions) works in
OUTPUT seconds, so this is built once and imported.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import segmap

B  = Path("/Volumes/Extreme/_edit_work/abwheel")
R2 = B / "r2"
FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
HOP = 0.005

ROWS, TOTAL = segmap.build()
EDL = json.load(open(B / "edl.json"))

def load_words():
    """Whisper words per roll, mapped onto output time via the segment map."""
    cache = {}
    out = []
    for r in ROWS:
        s = r["source"]
        if s not in cache:
            wh = json.load(open(B / f"{s}.whisper.json"))
            cache[s] = [w for seg in wh["segments"] for w in seg.get("words", [])]
        for w in cache[s]:
            if r["start"] - 0.02 <= w["start"] < r["end"]:
                a = r["out_start"] + (w["start"] - r["start"])
                b = r["out_start"] + (min(w["end"], r["end"]) - r["start"])
                out.append({"t": round(a, 3), "e": round(b, 3),
                            "w": w["word"].strip(), "beat": r["beat"]})
    out.sort(key=lambda w: w["t"])
    return out

def envelope():
    p = R2 / "audio" / "env.json"
    if p.exists():
        d = json.load(open(p)); return np.array(d["db"]), d["hop"]
    raw = subprocess.run([FF, "-v", "error", "-i", str(R2/"audio"/"voice_raw.wav"),
                          "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(float)
    n = int(HOP * 48000); m = len(a) // n
    r = np.sqrt((a[:m*n].reshape(-1, n) ** 2).mean(1) + 1e-14)
    db = 20 * np.log10(r + 1e-12)
    json.dump({"hop": HOP, "db": [round(float(x), 2) for x in db]}, open(p, "w"))
    return db, HOP

WORDS = load_words()
BEATS = [{"beat": r["beat"], "a": r["out_start"],
          "b": round(r["out_start"] + r["dur"], 4), "source": r["source"]} for r in ROWS]

def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"

if __name__ == "__main__":
    db, hop = envelope()
    print(f"TOTAL {mmss(TOTAL)}  {len(WORDS)} words  "
          f"{len(WORDS)/TOTAL*60:.0f} wpm   (reference cut: 1315 words / 418.1 s = 189 wpm)\n")
    print(f"{'beat':26s} {'out':>16s} {'dur':>7s} {'words':>6s} {'wpm':>5s} {'speech%':>8s}")
    for bt in BEATS:
        ws = [w for w in WORDS if bt["a"] <= w["t"] < bt["b"]]
        d = bt["b"] - bt["a"]
        spoken = sum(w["e"] - w["t"] for w in ws)
        print(f"{bt['beat']:26s} {mmss(bt['a']):>7s}-{mmss(bt['b']):>7s} {d:7.2f} "
              f"{len(ws):6d} {len(ws)/d*60:5.0f} {100*spoken/d:7.1f}%")
    # dead air measured as gaps BETWEEN words (what the handoff's 192 s figure counts)
    gaps = [(a["e"], b["t"]) for a, b in zip(WORDS, WORDS[1:]) if b["t"] - a["e"] >= 0.25]
    head = [(0.0, WORDS[0]["t"])] if WORDS[0]["t"] >= 0.25 else []
    tail = [(WORDS[-1]["e"], TOTAL)] if TOTAL - WORDS[-1]["e"] >= 0.25 else []
    allg = head + gaps + tail
    print(f"\ndead air >=0.25 s between words: {sum(b-a for a,b in allg):.1f}s "
          f"({100*sum(b-a for a,b in allg)/TOTAL:.0f}%) in {len(allg)} gaps")
    for a, b in sorted(allg, key=lambda g: -(g[1]-g[0]))[:12]:
        print(f"   {mmss(a)} - {mmss(b)}  {b-a:6.2f}s")
