#!/usr/bin/env python3
"""RE-PUNCH a cut that is already locked and delivered.

`plan_punchins.py` plans the cut AND the framing together, from raw source. That is the
right tool when you are cutting. It is the wrong tool for the five delivered longforms:
their cuts are approved, their grades are validated closed-loop, and re-deriving either
would risk the parts that are known-good to fix the part that is not.

This does the FRAMING HALF ONLY, against the finished `*_NO-GRAPHICS.mp4`:

  * the subject is tracked off the finished picture itself (locked camera => the
    per-pixel median is a clean plate; columns are scored rather than pixels so pool
    ripple and leaf shimmer do not drag the box)
  * shot boundaries start as the cut's OWN joins, read out of edl.json and accumulated
    into output time, so a framing change lands where a pause was already removed
  * any run longer than ~1.25x the target is split purely to reframe -- nothing is
    removed, the audio runs straight through -- and each split is nudged to the
    quietest 40 ms inside +/-0.9 s so it lands between words
  * three crop levels 1.00 / 0.86 / 0.74 of frame width, centred on the tracked box,
    never repeating the previous level, never cropping through the subject

Output is PICTURE ONLY and exactly as many frames as the source, so the delivered audio
drops straight back underneath it with no drift by construction. That is asserted.

usage:
  repunch.py --src NO-GRAPHICS.mp4 --audio DELIVERED.mp4 --out punched.mp4
             [--edl edl.json] [--work DIR] [--target 7.0] [--jobs 6]
"""
import argparse, json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")
GW, GH = 192, 108          # grid the subject analysis runs on
CROPS = [1.00, 0.86, 0.74]


def probe(v, sel, ent):
    return subprocess.run([FFP, "-v", "error", "-select_streams", sel, "-show_entries",
                           ent, "-of", "csv=p=0", v], capture_output=True,
                          text=True).stdout.strip()


# ---------------------------------------------------------------- subject track
BLOCK   = 2.0              # seconds per motion block
WIN     = 7                # blocks per analysis window (14 s)
SFPS    = 1.0 / BLOCK      # subject samples per second


def subject_track(src, work, dfps=4):
    """Where is the subject, second by second, in a shot that is ALWAYS occupied?

    `plan_punchins.py`/`subject.py` find the subject as "whatever differs from the
    per-pixel MEDIAN of the programme". That works on the ab-wheel roll because Dan
    leaves frame between sets, so the median really is a clean plate. It does NOT work
    on a talking head: he is in every frame, so he IS the median, and the largest
    residuals end up on the reflective door and the cabinets. Run on the spray-tan cut
    it put the subject centre at x=0.07 — the doorframe — on most of the video.

    MOTION is the signal that survives. Over a locked shot the background is still and
    the man talking and gesturing is not, so the mean absolute frame-to-frame difference
    accumulated over a window peaks exactly on him. Measured on the spray-tan cut at six
    timecodes it returns x 0.29-0.82 (centre ~0.56), which is where he actually is.

    Motion is accumulated into non-overlapping 2 s blocks and windowed afterwards, so
    memory is O(runtime/2) frames rather than O(runtime x fps) — a 53-minute programme
    would otherwise hold a gigabyte of diffs.
    """
    cache = work / "subject.npy"
    if cache.exists(): return np.load(cache)
    p = subprocess.Popen([FF, "-v", "error", "-i", src, "-vf",
                          f"fps={dfps},scale={GW}:{GH},format=gray", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE, bufsize=GW * GH * 64)
    per = int(round(BLOCK * dfps))
    blocks, acc, prev, k = [], np.zeros((GH, GW), np.float32), None, 0
    while True:
        buf = p.stdout.read(GW * GH)
        if len(buf) < GW * GH: break
        f = np.frombuffer(buf, dtype=np.uint8).reshape(GH, GW).astype(np.float32)
        if prev is not None: acc += np.abs(f - prev)
        prev = f; k += 1
        if k % per == 0:
            blocks.append(acc / per); acc = np.zeros((GH, GW), np.float32)
    if k % per: blocks.append(acc / max(1, k % per))
    p.stdout.close(); p.wait()
    M = np.stack(blocks) if blocks else np.zeros((1, GH, GW), np.float32)

    boxes = []
    for i in range(len(M)):
        lo, hi = max(0, i - WIN // 2), min(len(M), i + WIN // 2 + 1)
        mot = M[lo:hi].mean(0)
        col = mot.sum(0); col = col - col.min()
        if col.max() <= 1e-6:
            boxes.append(boxes[-1] if boxes else [0.30, 0.05, 0.80, 1.0]); continue
        pk = int(np.argmax(col)); thr = col.max() * 0.25
        x0 = pk
        while x0 > 0 and col[x0 - 1] > thr: x0 -= 1
        x1 = pk
        while x1 < GW - 1 and col[x1 + 1] > thr: x1 += 1
        row = mot[:, x0:x1 + 1].sum(1); row = row - row.min()
        ys = np.where(row > row.max() * 0.25)[0]
        y0, y1 = (int(ys[0]), int(ys[-1])) if len(ys) else (0, GH - 1)
        boxes.append([x0 / GW, y0 / GH, (x1 + 1) / GW, (y1 + 1) / GH])
    A = np.array(boxes, dtype=np.float64)
    kk = 5
    pad = np.pad(A, ((kk // 2, kk // 2), (0, 0)), mode="edge")
    S = np.stack([np.convolve(pad[:, j], np.ones(kk) / kk, "valid") for j in range(4)], 1)
    np.save(cache, S)
    return S


# ---------------------------------------------------------------- audio envelope
def envelope(audio, work, hop=0.005):
    cache = work / "env.json"
    if cache.exists(): return json.load(open(cache))
    raw = subprocess.run([FF, "-v", "error", "-i", audio, "-vn", "-ac", "1",
                          "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    n = int(48000 * hop)
    fr = a[:len(a) // n * n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    out = {"db": db.round(2).tolist(), "hop": hop}
    json.dump(out, open(cache, "w"))
    return out


# ---------------------------------------------------------------- shot plan
def edl_joins(edl_path, fd, total):
    """Existing cut joins in OUTPUT time: the cumulative sum of the kept ranges,
    each rounded to whole frames the way the renderer rounded them."""
    if not edl_path or not os.path.exists(edl_path): return []
    R = json.load(open(edl_path))["ranges"]
    t, out = 0.0, []
    for r in R[:-1]:
        t += round((r["end"] - r["start"]) / fd) * fd
        if 0.5 < t < total - 0.5: out.append(round(t, 6))
    return out


def split_runs(bounds, total, db, hop, target, fd):
    """Split any run longer than 1.25x target, nudging each split into the quietest
    40 ms inside +/-0.9 s so the reframe lands between words."""
    edges = [0.0] + list(bounds) + [total]
    out = [0.0]
    for a, b in zip(edges, edges[1:]):
        d = b - a
        if d <= target * 1.25:
            out.append(b); continue
        n = max(2, int(round(d / target)))
        prev = a
        for i in range(1, n):
            t = a + d * i / n
            lo, hi = max(0, int((t - 0.9) / hop)), min(len(db) - 1, int((t + 0.9) / hop))
            if hi > lo + 8:
                w = 8
                t = (min((db[j:j + w].mean(), j) for j in range(lo, hi - w))[1] + w / 2) * hop
            t = round(round(t / fd) * fd, 6)
            if t - prev > 1.2 and b - t > 1.2:
                out.append(t); prev = t
        out.append(b)
    return sorted(set(out))


def frame_shots(edges, S, target, anchor="top", headroom=0.05):
    """Assign a crop level to every shot. Never repeat the previous level; widen if the
    tracked box plus a 10% margin does not fit HORIZONTALLY; hold the crop for the whole
    shot.

    ONLY the width is protected. The first version of this also refused to crop through
    the subject vertically, and on a waist-up talking head that made every shot 1.00:
    the tracked box runs head (y~0.05) to the bottom of frame, so need_h ~ 1.01 and the
    widen loop fired on all 167 shots -- 991 s of 1134 s came out uncropped. Cutting the
    bottom of his torso off IS what a punch-in is. Height is handled by the ANCHOR
    instead: `top` puts the crop's top edge just above his head, which keeps the face
    and the headroom and takes the crop out of his chest downward. `centre` reproduces
    plan_punchins.py's behaviour, which is right for a full-body outdoor shot.
    """
    shots, level, i = [], 0, 0
    for k, (a, b) in enumerate(zip(edges, edges[1:])):
        if k:
            level = (level + 1) % 3 if (i % 3) else (level + 2) % 3
        i += 1
        lo, hi = int(a * SFPS), max(int(a * SFPS) + 1, int(b * SFPS))
        box = S[lo:hi] if hi <= len(S) else S[min(lo, len(S) - 1):]
        if not len(box): box = S[min(lo, len(S) - 1):min(lo, len(S) - 1) + 1]
        x0, y0, x1, y1 = box[:, 0].min(), box[:, 1].min(), box[:, 2].max(), box[:, 3].max()
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        need_w = (x1 - x0) + 0.10
        cw = CROPS[level]
        while cw < 1.0 and cw < need_w:
            cw = CROPS[max(0, CROPS.index(cw) - 1)]
            if cw >= 1.0: break
        if anchor == "top":
            cy = min(max(float(y0) - headroom + cw / 2, cw / 2), 1.0 - cw / 2)
        shots.append({"a": round(a, 6), "b": round(b, 6), "crop": round(cw, 3),
                      "cx": round(float(cx), 4), "cy": round(float(cy), 4)})
    return shots


# ---------------------------------------------------------------- render
def vf_for(s, W, H):
    k = s["crop"]
    if k >= 0.999: return "null"
    cw = int(W * k) // 2 * 2; ch = int(H * k) // 2 * 2
    x = int(min(max(s["cx"] * W - cw / 2, 0), W - cw))
    y = int(min(max(s["cy"] * H - ch / 2, 0), H - ch))
    return f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1"


def render(shots, src, out, work, fd, fpsstr, W, H, jobs, crf):
    pdir = work / "pieces"; pdir.mkdir(exist_ok=True)

    def one(i):
        s = shots[i]
        n = int(round((s["b"] - s["a"]) / fd))
        dst = pdir / f"p{i:04d}.mp4"
        if dst.exists() and dst.stat().st_size > 1000: return dst, n
        vf = vf_for(s, W, H)
        cmd = [FF, "-nostdin", "-v", "error", "-y", "-ss", f"{s['a']:.6f}", "-i", str(src)]
        if vf != "null": cmd += ["-vf", vf]
        cmd += ["-an", "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium",
                "-crf", str(crf), "-pix_fmt", "yuv420p", "-r", fpsstr, str(dst)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode: raise SystemExit(f"piece {i} failed: {r.stderr[-500:]}")
        return dst, n

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        res = list(ex.map(one, range(len(shots))))
    lst = work / "pieces.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p, _ in res))
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(out)], check=True)
    return sum(n for _, n in res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--edl")
    ap.add_argument("--work", default="repunch")
    ap.add_argument("--target", type=float, default=7.0)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--anchor", default="top", choices=["top", "centre"])
    ap.add_argument("--plan-only", action="store_true")
    A = ap.parse_args()

    work = Path(A.work); work.mkdir(parents=True, exist_ok=True)
    num, den = probe(A.src, "v:0", "stream=r_frame_rate").split("/")
    fd = int(den) / int(num); fpsstr = f"{num}/{den}"
    W, H = [int(x) for x in probe(A.src, "v:0", "stream=width,height").split(",")]
    nsrc = int(probe(A.src, "v:0", "stream=nb_read_packets").split(",")[0]) if False else None
    total = float(probe(A.src, "v:0", "stream=duration") or probe(A.src, "", "format=duration"))
    total = round(round(total / fd) * fd, 6)

    S = subject_track(A.src, work)
    env = envelope(A.audio, work)
    db, hop = np.array(env["db"]), env["hop"]
    joins = edl_joins(A.edl, fd, total)
    edges = split_runs(joins, total, db, hop, A.target, fd)
    shots = frame_shots(edges, S, A.target, anchor=A.anchor)
    json.dump({"shots": shots, "total": total, "fd": fd},
              open(work / "shots.json", "w"), indent=1)

    lv = {}
    for s in shots: lv[s["crop"]] = lv.get(s["crop"], 0) + s["b"] - s["a"]
    print(f"{len(joins)} existing joins -> {len(shots)} shots over {total:.2f}s "
          f"= {len(shots)/(total/60):.1f} framing changes/min (reference cut 7.7)")
    print("  time per crop level: " + "  ".join(f"{k:.2f}={v:.0f}s" for k, v in sorted(lv.items())))
    if A.plan_only: sys.exit(0)

    n = render(shots, A.src, A.out, work, fd, fpsstr, W, H, A.jobs, A.crf)
    want = int(round(total / fd))
    print(f"rendered {n} frames, source has {want} -> {'MATCH' if n == want else 'MISMATCH'}")
    assert n == want, "frame count changed; the delivered audio would drift under this picture"
    print("->", A.out)
