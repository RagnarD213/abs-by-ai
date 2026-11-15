#!/usr/bin/env python3
"""Check the content map against what Dan actually says on camera.

    announcements.py "/Volumes/Extreme/<shoot>" ["/Volumes/Expansion/Abs By AI Raw Footage/<shoot>"]
    announcements.py "<shoot dir>" --gaps map.json      # also print what is said between mapped segments

For every roll with a Whisper sidecar (`<clip>.roll/words.json`, built by roll_sidecar.py) it prints each
spoken announcement ("this video is ...", "this ad is ...", "this is now ...", or a bare script code such
as L01 / S05 / A15 / B08 / C01) with its time and the words around it. Compare these against the audio map
and the queue rows before registering jobs: on the 11/13 shoot this caught four start times that were a
few seconds off and confirmed that the VSL roll held nothing else.
With --gaps it prints the transcript between consecutive mapped segments, so you can confirm every gap is
crew chat, framing or a break and that no filmed take was missed.
"""
import argparse, json, os, re


def words(dirs, clip):
    for d in dirs:
        p = os.path.join(d, f"{clip}.roll", "words.json")
        if os.path.exists(p):
            j = json.load(open(p))
            ws = j["words"] if isinstance(j, dict) and "words" in j else j
            return [(float(w.get("start", w.get("s", 0))), (w.get("word") or w.get("w") or w.get("text") or "").strip())
                    for w in ws]
    return None


def mmss(t):
    return f"{int(t)//60}:{int(t)%60:02d}"


def secs(s):
    p = [int(x) for x in str(s).split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--gaps")
    a = ap.parse_args()
    clips = sorted({os.path.splitext(f)[0] for d in a.dirs if os.path.isdir(d) for f in os.listdir(d)
                    if f.upper().endswith(".MP4") and not f.startswith("._")})
    code = re.compile(r"^[lsabcd]\d\d$")
    gm = json.load(open(a.gaps)) if a.gaps else {}
    for c in clips:
        t = words(a.dirs, c)
        if t is None:
            print(f"== {c}: NO SIDECAR (build it with roll_sidecar.py before relying on this roll)")
            continue
        print(f"== {c}: {len(t)} words, last at {mmss(t[-1][0]) if t else '0:00'}")
        low = [w.lower().strip(".,!?\"'") for _, w in t]
        last = -99
        for i in range(len(low) - 2):
            hit = ((low[i] in ("video", "ad") and low[i + 1] == "is") or
                   (low[i] == "this" and low[i + 1] == "is" and low[i + 2] == "now") or code.match(low[i]))
            if hit and t[i][0] - last > 4:
                last = t[i][0]
                print(f"  {mmss(t[i][0])}  " + " ".join(w for _, w in t[max(0, i - 3):i + 12]))
        if c in gm:
            seg = gm[c].get("segments", gm[c]) if isinstance(gm[c], dict) else gm[c]
            seg = sorted(seg, key=lambda s: secs(s["start"]))
            for x, y in zip(seg, seg[1:]):
                a0, b0 = secs(x["end"]), secs(y["start"])
                if b0 - a0 >= 3:
                    said = " ".join(w for s, w in t if a0 <= s < b0)
                    print(f"  GAP {mmss(a0)}-{mmss(b0)}: {said[:300] or '(silence)'}")


if __name__ == "__main__":
    main()
