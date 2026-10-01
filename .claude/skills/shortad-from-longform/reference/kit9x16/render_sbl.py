#!/usr/bin/env python3
"""RENDER THE 9:16 PICTURE OF A SHEET BUILD (Soft Blue Light). Run inside the build dir, like render.py.

Talk and full-bleed beats are render.py's own (the same crop track, push schedule and segment cache). What changes
is every graphic: none of vlib's olive plates, lower thirds, CTA pill or flash is drawn. Instead

  `hf` beats      the HyperFrames full-screen render for that beat (sbl_graphics.py), decoded BT.601 -> BT.709
  `card` beats    the picture scaled into the media-card plate's hole, the plate (field, frame, chip) laid over it
  overlays        lower thirds (glass: the footage under the strip is blurred inside the mask pass), side cards, CTAs:
                  composited in RGB by _shared/hyperframes/composite.py, each file decoded by its own matrix

  python3 render_sbl.py [--selftest] [--only i,j] [--range A B --out preview.mp4 [--exact]]

--range renders only the beats that overlap those film seconds and writes a picture-only preview of exactly that span
(whole beats), for the first-minute and in-context review clips. Without it: picture.mp4, the full film.
"""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, ".")
HERE_SHARED = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
for _p in ("vignette.png", "vignette_soft.png"):                 # the sheet's grade is the look: no added vignette
    if not os.path.exists(_p):
        Image.new("RGB", (1080, 1920), (255, 255, 255)).save(_p)
import render as R  # noqa: E402  (talk / bleed segments, crop track, seek rules, caches)
import beats  # noqa: E402

KIT = os.path.dirname(os.path.realpath(__file__)) if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "sbl_graphics.py")) \
    else json.load(open("kit_path.json"))["kit"]
sys.path.insert(0, os.path.abspath(os.path.join(KIT, "..", "..", "..", "_shared", "hyperframes")))
import composite as HC  # noqa: E402

FF, FPS, VW, VH = R.FF, R.FPS, R.VW, R.VH
HF_IN = "scale=in_color_matrix=bt601:in_range=tv:out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int"
PLATES = json.load(open("hf/plates.json")) if os.path.exists("hf/plates.json") else {}


def fsha(p):
    st = os.stat(p)
    return [st.st_size, st.st_mtime_ns]


def render_segment(i, b, nfr, t0):
    if b["kind"] not in ("hf", "card"):
        return R.render_segment(i, b, nfr, t0)
    pl = PLATES.get(str(i))
    if not pl or not os.path.exists(pl["mov"]):
        raise SystemExit(f"beat {i} ({b['kind']} {b.get('gid') or b.get('media')}): its HyperFrames render is missing -- run sbl_graphics.py")
    out = f"out/s{i:03d}.mp4"; man = out + ".sig"
    sig = json.dumps(dict(b=b, n=nfr, plate=fsha(pl["mov"]), hole=pl.get("hole"), v="sbl-1",
                          media=(repr(R.MEDIA[b["media"]]) if b["kind"] == "card" else None)), sort_keys=True, default=str)
    if os.path.exists(out) and os.path.getsize(out) > 20000 and os.path.exists(man) and open(man).read() == sig:
        return
    common = R.COMMON(nfr, out)
    if b["kind"] == "hf":
        R.run([FF, "-v", "error", "-y", "-i", pl["mov"], "-vf", f"{HF_IN},format=yuv420p,tpad=stop_mode=clone:stop=-1"] + common)
    else:
        x0, y0, x1, y1 = pl["hole"]; w, h = x1 - x0, y1 - y0
        key = b["media"]
        o = dict(R.media_opts(key)); amt = o.pop("amt", 0.04)
        chain = R.still_chain(w, h, nfr, amt=amt, **o) if R.MEDIA[key][0] == "img" else \
            "setpts=PTS-STARTPTS," + R.media_prefix(key) + R.cover_chain(w, h, **o)
        R.run([FF, "-v", "error", "-y"] + R.media_input(key, nfr) + ["-i", pl["mov"], "-filter_complex",
              f"color=black:s={VW}x{VH}:r=30000/1001[bg];[0:v]{chain}[m];[bg][m]overlay={x0}:{y0}[u];"
              f"[1:v]{HF_IN},format=yuva444p,tpad=stop_mode=clone:stop=-1[p];[u][p]overlay=0:0:format=auto,format=yuv420p"] + common)
    open(man, "w").write(sig)


def composite(src, out, g0, n, skip=0):
    """Overlays onto `src` in RGB; writes `out` tagged BT.709. `src` frame `skip` is film frame g0; n frames are written."""
    man = json.load(open("hf/manifest.json")) if os.path.exists("hf/manifest.json") else []
    man = [m for m in man if HC.fr(m["a"]) < g0 + n and HC.fr(m["b"]) > g0]
    for m in man:
        for k in ("mov", "mask"):
            if m.get(k) and not os.path.exists(m[k]):
                raise SystemExit(f"overlay {m['id']}: {m[k]} is missing -- run sbl_graphics.py")
    C = HC.Compositor(man, wh=(VW, VH))
    trim = f"trim=start_frame={skip},setpts=PTS-STARTPTS," if skip else ""
    dec = subprocess.Popen([FF, "-v", "error", "-i", src, "-vf", trim + "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-framerate", "30000/1001", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-video_track_timescale", "30000", "-an", out],
                           stdin=subprocess.PIPE)
    size = VW * VH * 3
    for k in range(n):
        buf = dec.stdout.read(size)
        if len(buf) < size:
            raise SystemExit(f"{src}: short read at frame {k} of {n}")
        g = g0 + k
        if C.active(g):
            buf = np.ascontiguousarray(C.apply(np.frombuffer(buf, np.uint8).reshape(VH, VW, 3), g)).tobytes()
        enc.stdin.write(buf)
    enc.stdin.close(); enc.wait(); dec.kill(); dec.stdout.close(); dec.wait()
    if enc.returncode:
        raise SystemExit("compositor encode failed")


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        R.selftest(); return
    P, _ov = R.plan()
    starts, prev = [], 0
    for b, n in P:
        starts.append(prev); prev += n
    only = set(int(x) for x in args[args.index("--only") + 1].split(",")) if "--only" in args else None
    rng = (float(args[args.index("--range") + 1]), float(args[args.index("--range") + 2])) if "--range" in args else None
    if rng:
        only = {i for i, (b, n) in enumerate(P) if b["t0"] < rng[1] and b["t1"] > rng[0]}
    R.selftest(verbose=False)
    for i, (b, nfr) in enumerate(P):
        if only is not None and i not in only:
            continue
        render_segment(i, b, nfr, b["t0"])
        print(f"{i:3d} {b['kind']:6s} {nfr:5d}f  {b.get('media') or b.get('gid') or ''}", flush=True)
    if only is not None and not rng:
        return
    idx = sorted(only) if rng else list(range(len(P)))
    lst = f"out/list_rng_{idx[0]}_{idx[-1]}.txt" if rng else "out/list.txt"
    with open(lst, "w") as f:
        for i in idx:
            f.write(f"file s{i:03d}.mp4\n")
    raw = f"out/_rng_raw_{idx[0]}_{idx[-1]}.mp4" if rng else "picture_raw.mp4"
    R.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw])
    g0 = starts[idx[0]]; n = sum(P[i][1] for i in idx)
    out = args[args.index("--out") + 1] if "--out" in args else "picture.mp4"
    skip = 0
    if rng and "--exact" in args:                                 # exactly the asked seconds, not whole beats
        fa, fb = max(g0, round(rng[0] * FPS)), min(g0 + n, round(rng[1] * FPS))
        skip, g0, n = fa - g0, fa, fb - fa
    composite(raw, out, g0, n, skip)
    if rng:
        json.dump(dict(g0=g0, frames=n, t0=g0 / FPS, t1=(g0 + n) / FPS), open(out + ".range.json", "w"))
    print(out, "done:", n, "frames from film frame", g0)


if __name__ == "__main__":
    main()
