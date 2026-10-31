"""Round 4 subtitles: round 3's reviewed file with its timing moved across the two new cuts (no words change, nothing burned in)."""
import json, re
R3 = "/Volumes/Expansion/_edit_work/RO-37/round3/final/RO37_R3.srt"; OUT = "/Volumes/Expansion/_edit_work/RO-37/round4/final/RO37_R4.srt"
(c1, n1), (c2, n2) = json.load(open("/Volumes/Expansion/_edit_work/RO-37/round4/cuts4.json"))
def m(t):
    if t >= c2 + n2: return t - n1 - n2
    if t >= c2: return c2 - n1
    if t >= c1 + n1: return t - n1
    return min(t, c1)
def ps(s): h, mi, x = s.split(":"); a, b = x.split(","); return int(h) * 3600 + int(mi) * 60 + int(a) + int(b) / 1000
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
out = []; prev = 0
for b in open(R3).read().strip().split("\n\n"):
    i, tt, *txt = b.split("\n"); a, e = [m(ps(x)) for x in tt.split(" --> ")]
    a = max(a, prev + .02) if prev else a; e = max(e, a + .4); prev = e
    out.append(f"{i}\n{ts(a)} --> {ts(e)}\n" + "\n".join(txt) + "\n")
open(OUT, "w").write("\n".join(out)); print(len(out), "cues, last ends", ts(prev))
