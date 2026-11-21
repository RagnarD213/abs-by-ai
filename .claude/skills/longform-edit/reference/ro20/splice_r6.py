"""RO-20C round 6 (copy of splice_r4.py writing into round6/V, with films_r6 loaded so the excuse clips are in the plan): rebuild changed film parts of one video from an already rendered part, re-rendering only the keyframe windows that changed.
usage: splice_r4.py V OLD_PART_FILE OLD_F0 OLD_F1 'a:b,a:b,...'
  OLD_PART_FILE  the rendered .v.mp4 that covered film frames OLD_F0..OLD_F1 (stream-copied where nothing changed)
  dirty          film-frame windows whose picture changed (re-rendered); new part edges are dirty automatically when they are not keyframes
Writes every film part of the video's current layout that lies inside OLD_F0..OLD_F1 as round4/V/parts/NN_film.mp4.v.mp4 (+ .base.mp4)."""
import sys, os, json, subprocess, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import films_r6 as F6, build as Bd, composite as HC
F = F6.F
V, OLD, OF0, OF1, DIRTY = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
FPS = Bd.FPS; FF = Bd.FF; FP = FF.replace("ffmpeg", "ffprobe"); D = f"{F.W}/round6/{V}"; WK = os.environ.get("SPLICE_DIR", f"{D}/splice"); os.makedirs(WK, exist_ok=True)
kf = [round(float(x.split(",")[0])*FPS) + OF0 for x in subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey", "-show_entries", "frame=pts_time",
      "-of", "csv=p=0", OLD], capture_output=True, text=True).stdout.split() if x.split(",")[0]]
kf = sorted(set(kf)) + [OF1]
def kprev(f): return kf[max(0, bisect.bisect_right(kf, f) - 1)]
def knext(f): return kf[min(len(kf) - 1, bisect.bisect_left(kf, f))]
clips = [(Bd.fr(i["t0"]), Bd.fr(i["t1"])) for i in Bd.R if i["kind"] == "clip"]
dirty = [tuple(map(int, w.split(":"))) for w in DIRTY.split(",") if w]
def render(x, y, out):
    if not os.path.exists(out) or F.probe_frames(out) != y - x:
        tmp = out[:-6]                                    # render_picture writes <name>.v.mp4
        Bd.render_picture(x/FPS, y/FPS, tmp, x, y, Bd.segments(x, y), HC.Compositor(F.MAN))
    return out
def build_part(s, e, out):
    win = [(s, knext(s))] if s not in kf else []
    win += [(kprev(e), e)] if e not in kf else []
    win += [(kprev(a), knext(b)) for a, b in dirty if a < e and b > s]
    win = [(max(s, a), min(e, b)) for a, b in win if min(e, b) > max(s, a)]
    for _ in range(5):                                    # a render window never starts inside a clip (its reader starts at the clip's first frame)
        win = [(min(a, kprev(next((c0 for c0, c1 in clips if c0 < a < c1), a))) if any(c0 < a < c1 for c0, c1 in clips) else a, b) for a, b in win]
        win = [(max(s, a), b) for a, b in win]
    win.sort(); merged = []
    for a, b in win:
        if merged and a <= merged[-1][1]: merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else: merged.append((a, b))
    chunks, t = [], s
    for a, b in merged:
        if t < a: chunks.append(("copy", t, a))
        chunks.append(("render", a, b)); t = b
    if t < e: chunks.append(("copy", t, e))
    files = []
    for k, (kind, a, b) in enumerate(chunks):
        f = f"{WK}/{os.path.basename(out)[:-6]}_{k:02d}_{kind}_{a}_{b}.v.mp4"
        if kind == "render": render(a, b, f)
        else:
            assert a in kf and (b in kf or b == OF1), (a, b)
            if not os.path.exists(f):
                cuts = [c for c in (a - OF0, b - OF0) if 0 < c < OF1 - OF0]; idx = 1 if a > OF0 else 0
                for z in range(3):
                    try: os.remove(f"{WK}/_seg{z}.mp4")
                    except OSError: pass
                subprocess.run([FF, "-v", "error", "-y", "-i", OLD, "-map", "0:v", "-c", "copy", "-f", "segment", "-segment_frames", ",".join(map(str, cuts)),
                                "-reset_timestamps", "1", f"{WK}/_seg%d.mp4"], check=True)
                os.replace(f"{WK}/_seg{idx}.mp4", f)
        assert F.probe_frames(f) == b - a, (f, F.probe_frames(f), b - a)
        files.append(f)
    txt = out + ".txt"; open(txt, "w").write("".join(f"file '{x}'\n" for x in files))
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", out], check=True)
    assert F.probe_frames(out) == e - s
    base = out[:-6] + ".base.mp4"; bt = base + ".txt"                 # the presenter render before graphics, for the watch pass
    open(bt, "w").write("".join(f"file '{Bd.render_seg(sg)}'\n" for sg in Bd.segments(s, e)))
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", bt, "-c", "copy", base], check=True)
    print("part", os.path.basename(out), e - s, "frames:", [(c[0], c[1], c[2]) for c in chunks], flush=True)
for k, (p, a, b) in enumerate(F.layout(V)):
    if p[0] == "film" and OF0 <= p[1] and p[2] <= OF1:
        build_part(p[1], p[2], f"{D}/parts/{k:02d}_film.mp4.v.mp4")
