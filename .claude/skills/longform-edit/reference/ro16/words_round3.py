"""Round 3 word list. The two join fixes must not move anything else, so the words are NOT re-transcribed: every round-2
word keeps its source time (round3-plan/before/words_out.json) and is re-mapped onto the new shots.json. Three words are
fixed by hand from medium.en on the windows alone (verify_asr.py 572.84:576 and 1071:1073.4): the first "Most guys" is cut,
the fluent second one (which Whisper had folded into one long "do") is written in, and "benefits." ends on its real "s".
Run instead of words_out.py: edl.py -> shots.py -> assemble_audio.py -> words_round3.py -> resolve.py."""
import json
W="/Volumes/Extreme/_edit_work/ro16"; FPS=30000/1001
S=json.load(open(f"{W}/shots.json")); B=json.load(open(f"{W}/round3-plan/before/words_out.json"))
def to_out(s):
    for sh in S:
        a=sh["src_f0"]/FPS; b=sh["src_f1"]/FPS
        if a-0.02<=s<=b+0.02: return sh["out_f0"]/FPS+(min(max(s,a),b)-a)
    return None
src=[]
for w in B:
    if w["w"] in ("Most","guys") and 570.9<w["src0"]<571.8: continue            # the abandoned first copy (cut)
    if w["w"]=="do" and 571.7<w["src0"]<571.8:                                   # the folded second copy
        src += [("Most",572.88,573.24),("guys",573.24,573.52),("do",573.52,573.678)]; continue
    if w["w"]=="benefits." and 1072.4<w["src0"]<1072.6: src.append((w["w"],w["src0"],1073.16)); continue
    src.append((w["w"],w["src0"],w["src1"],w))
out=[]
for row in src:
    w,s0,s1=row[:3]; o0=to_out(s0); o1=to_out(s1)
    # between the two joins the shift is exactly 30 frames = 1.001 s: carry the round-2 time so no 1 ms rounding moves a graphic by a frame
    if len(row)>3 and 572.84<=s0 and s1<1072.9 and row[3]["t0"] is not None and row[3]["t1"] is not None: o0=row[3]["t0"]-1.001; o1=row[3]["t1"]-1.001
    out.append(dict(w=w, src0=round(s0,3), src1=round(s1,3), t0=None if o0 is None else round(o0,3), t1=None if o1 is None else round(o1,3)))
json.dump(out,open(f"{W}/words_out.json","w"),indent=0)
print(len(out),"words (round 2:",len(B),");",sum(1 for x in out if x["t0"] is None),"unmapped (round 2:",sum(1 for x in B if x["t0"] is None),")")
