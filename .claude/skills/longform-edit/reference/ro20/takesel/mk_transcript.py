"""cut_transcript.md from edl.json + shots.json + words_out.json: one block per piece (id, output range, roll range, kept
words as heard), a '## ' heading where the topic changes (takeplan.SECTIONS). Also prints the section list with output times."""
import json, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/takesel")
from takeplan import SECTIONS
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001
P = json.load(open(f"{W}/edl.json")); S = json.load(open(f"{W}/shots.json")); WO = json.load(open(f"{W}/words_out.json"))
def ms(t): t = int(t); return f"{t//60}:{t%60:02d}"
def mss(t): return f"{int(t//60)}:{t%60:05.2f}"
byp = {}
for s in S: byp.setdefault(s["piece"], []).append(s)
shot_piece = {s["id"]: s["piece"] for s in S}
words = {}
for w in WO: words.setdefault(shot_piece[w["shot"]], []).append(w["w"])
tot = S[-1]["out_f1"]/FPS
L = ["# RO-20 cut transcript: Why You Should Invest More In Your Health", "",
     f"Source: C1511.MP4 (68:51). Kept: {len(P)} pieces, {len(S)} shots, {ms(tot)} ({tot:.1f} s). Words are the medium.en words kept by `words_src_out.py` (words_out.json), in order. Output times are on the cut timeline (shots.json); roll times are seconds into C1511.", ""]
secs = []
for p in P:
    sh = byp[p["id"]]; o0 = sh[0]["out_f0"]/FPS; o1 = sh[-1]["out_f1"]/FPS
    if p["id"] in SECTIONS: L += [f"## {SECTIONS[p['id']]}", ""]; secs.append((o0, SECTIONS[p["id"]]))
    L += [f"**{p['id']}** | out {ms(o0)} to {ms(o1)} | roll {p['local_in']:.2f} to {p['local_out']:.2f} s ({mss(p['local_in'])} to {mss(p['local_out'])})", "", " ".join(words[p["id"]]).replace(" %", "%").replace(" ,000", ",000"), ""]
open(f"{W}/cut_transcript.md", "w").write("\n".join(L))
for t, title in secs: print(ms(t), title)
print("total", ms(tot), round(tot, 1))
