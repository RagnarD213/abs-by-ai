"""Calibrate the house key on 2-3 s excerpts at a piece's hardest moments, in the render queue's QUICK lane.

    python3 calibrate.py --code RECIPE_DIR --src CLIP.MP4 --t0 T0 --dur D --out CAL_DIR [--watch watch.json]
                         [--at SECONDS ...] [--len 2.5] [--n 3] [--pick-only]
                         [--stage1 "python3 stage1_key.py {t0} {dur} {out}"]
                         [--srcprep "python3 srcprep.py {t0} {n} {out}"]
                         [--stage15 "python3 stage15_temporal.py {c1} {src} {out} {watch}"]

Why (Handoffs/handoff-20261021-render-throughput-plan.md, 1b): RO-24 re-keyed whole clips three times while it tuned
plate, crop and hold-out boxes, 40-75 minutes a run, about 6 of one day's 8.5 key hours. Tune here instead, then key
the whole piece exactly once (keyonce.py) and gate that one run.

What it does
1. Finds the hardest moments with one low-resolution pass over the piece (hardware decode): the frames where the most
   edge pixels change (fast hands, hair, turns: the motion peaks) and the frame where the tracked hold-out has the
   most to do (the watch's grey band low in the frame; or the middle of the longest --watch box range). --at adds
   or replaces picks by time in the piece. Windows never overlap.
2. Keys each excerpt with the recipe's OWN stage 1 and stage 1.5 (the command templates; RO-24 style recipes that
   take frame numbers use {f0} and {nf}). Each excerpt is keyed R=3 frames wider on both sides, so its frames see
   the same temporal neighbours as in the full run: what you judge here is what the full key will produce there.
   Each excerpt's seek is checked against the low-resolution pass, so it starts on exactly the full run's frame.
3. Writes CAL_DIR/sheet.jpg (each excerpt: start, peak and end frames over the pale and pink key-check fields plus
   the matte) and CAL_DIR/calibration.json (picks, frame numbers in the piece, commands, seconds per stage).

Judge the sheet; change plate, crop rows or boxes in the recipe; re-run (seconds to a few minutes) until it is right.
Then key the piece once. Never re-key a full clip to try a setting.
"""
import argparse, json, os, shlex, subprocess, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
sys.path.insert(0, str(SHARED / "renderq"))
import renderq  # noqa: E402

FF = str(SHARED.parents[2] / "Media/video_edit/bin/ffmpeg")
FFPROBE = str(SHARED.parents[2] / "Media/video_edit/bin/ffprobe")
R = 3                              # stage 1.5 neighbours each side (stage15_temporal.R)
DEFAULTS = dict(stage1="python3 stage1_key.py {t0} {dur} {out}",
                srcprep="python3 srcprep.py {t0} {n} {out}",
                stage15="python3 stage15_temporal.py {c1} {src} {out} {watch}")
PALE, PINK = np.array([0.86, 0.89, 0.93], np.float32), np.array([0.95, 0.25, 0.62], np.float32)


def probe(src):
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,start_time:stream_side_data=rotation", "-of", "json", src],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    num, den = map(int, s["r_frame_rate"].split("/"))
    w, h = s["width"], s["height"]
    rot = next((abs(int(d.get("rotation", 0))) for d in s.get("side_data_list", []) if "rotation" in d), 0)
    if rot in (90, 270):
        w, h = h, w
    return num / den, w, h, float(s.get("start_time") or 0)


def lowres(src, t0, dur=None, nframes=None, w=0, h=0):
    """1/8-size RGB frames from a seek exactly like the stage scripts' (-ss before -i)."""
    sw, sh = max(2, w // 8 // 2 * 2), max(2, h // 8 // 2 * 2)
    vf = f"scale={sw}:{sh}:in_color_matrix=bt709:in_range=tv:out_range=pc:flags=area,format=rgb24"
    cmd = [FF, "-v", "error", "-ss", t0, "-i", src] + (["-t", dur] if dur else []) + \
          (["-frames:v", str(nframes)] if nframes else []) + ["-vf", vf, "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = sw * sh * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(sh, sw, 3)
    p.wait()


def thumb(f):
    g = f.astype(np.float32).mean(-1)
    h, w = g.shape[0] // 4 * 4, g.shape[1] // 4 * 4
    return g[:h, :w].reshape(h // 4, 4, w // 4, 4).mean((1, 3))


def seek_for(src, t0, p0, e0, fps, thumbs, w, h):
    """The seek string (3 decimals, as the stage scripts format it) whose first two frames are the piece's frames
    e0 and e0+1. Two traps (found 10-21): a seek more than half a frame before the first frame makes ffmpeg's
    constant-rate raw output repeat that frame, shifting every later frame by one; and frame-time arithmetic alone
    does not say which frame a seek lands on. So try seeks a little before the predicted frame and keep the one
    whose pictures match the low-resolution pass, which decoded the piece from t0 exactly as the full key will."""
    if e0 == 0:
        return f"{t0:.3f}"                                     # the full run's own seek: identical frames
    want = [thumbs[k] for k in (e0, e0 + 1) if k < len(thumbs)]
    for d in (-0.25, -0.15, -0.35, -1.25, 0.75, -0.05, -0.45):   # p0: the first frame's time (ffprobe)
        t = f"{p0 + (e0 + d) / fps:.3f}"
        got = [thumb(f) for f in lowres(src, t, nframes=len(want), w=w, h=h)]
        if len(got) == len(want) and all(np.abs(g - x).mean() < 0.05 for g, x in zip(got, want)):
            return t
    raise SystemExit(f"calibrate: no seek lands on piece frame {e0} without a repeated frame; check --t0 and the source")


def analyse(src, t0, dur, fps, w, h):
    """Per-frame scores on a 1/8-size decode: edge change (motion peaks) and hold-out band area, plus a small
    picture of every frame (to check where excerpt seeks land)."""
    edge, hold, thumbs, prev = [], [], [], None
    for f8 in lowres(src, f"{t0:.3f}", dur=f"{dur:.3f}", w=w, h=h):
        thumbs.append(thumb(f8))
        f = f8.astype(np.float32) / 255
        sh = f.shape[0]
        ex = f[..., 1] - np.maximum(f[..., 0], f[..., 2])
        m = np.clip((0.14 - ex) / 0.08, 0, 1)                   # soft "not screen" (plate.py calls ex > 0.10 screen)
        edge.append(0.0 if prev is None else float((np.abs(m - prev) > 0.25).sum()))
        prev = m
        lo = f[int(sh * 0.68):]                                  # hold-out zone: low in the frame (wrist, desk)
        mx, mn = lo.max(-1), lo.min(-1)
        Y = 0.2126 * lo[..., 0] + 0.7152 * lo[..., 1] + 0.0722 * lo[..., 2]
        hold.append(float((((mx - mn) < 0.07) & (Y > 0.25) & (Y < 0.62)).sum()))
    return np.array(edge), np.array(hold), thumbs


def pick(edge, hold, L, n, watch, at, fps, nframes):
    """Window centres (frame numbers in the piece), hardest first, no overlap, all inside the piece: --at picks,
    then the tracked hold-out, then the motion peaks."""
    lo, hi = L // 2, nframes - (L - L // 2)
    if hi < lo:
        return [(nframes // 2, "whole piece (shorter than an excerpt)")]
    picks = []

    def free(c):
        return all(abs(c - p) >= L for p, _ in picks) and lo <= c <= hi

    def place(c, why):
        c = int(np.clip(c, lo, hi))
        for d in range(0, nframes):                            # nearest free spot
            for x in (c - d, c + d):
                if free(x):
                    picks.append((x, why)); return

    for t in at or []:
        if len(picks) < n:
            place(round(t * fps), f"--at {t:g} s")
    k = np.ones(max(1, L // 3)) / max(1, L // 3)
    if len(picks) < n:
        if watch and watch.get("ranges"):
            f0, f1 = max(((r[0], r[1]) for r in watch["ranges"]), key=lambda r: r[1] - r[0])
            place((f0 + f1) // 2, f"tracked hold-out box frames {f0}-{f1}")
        elif hold.max() > 0:
            place(int(np.argmax(np.convolve(hold, k, mode="same"))), "hold-out band peak")
    sm = np.convolve(edge, k, mode="same")                    # sustained motion, not a single noisy frame
    for c in np.argsort(-sm):
        if len(picks) >= n:
            break
        if free(int(c)):
            picks.append((int(c), f"motion peak ({sm[c]:.0f} edge px changing)"))
    return picks


def run(cmd, cwd, log):
    t = time.time()
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    log.append(dict(cmd=cmd, s=round(time.time() - t, 1), rc=r.returncode))
    if r.returncode:
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-4000:])
        raise SystemExit(f"calibrate: failed: {cmd}")
    return r.stdout


def tile(c15, i, W=240):
    d = np.load(f"{c15}/f{i:04d}.npy").astype(np.float32)
    Fp, a = d[..., :3], d[..., 3:]
    out = []
    for bg in (PALE, PINK):
        out.append(np.clip(Fp + (1 - a) * bg, 0, 1))
    out.append(np.repeat(a, 3, -1))
    from PIL import Image
    ims = [Image.fromarray((x * 255 + 0.5).astype(np.uint8)) for x in out]
    h = int(ims[0].height * W / ims[0].width)
    return [im.resize((W, h), Image.Resampling.LANCZOS) for im in ims]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--code", required=True, help="the recipe folder (its stage scripts run from there)")
    ap.add_argument("--src", required=True); ap.add_argument("--t0", type=float, required=True)
    ap.add_argument("--dur", type=float, required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--watch"); ap.add_argument("--at", type=float, nargs="*")
    ap.add_argument("--plate", help="plate_out.npy stage 1.5 reads (default: RECIPE_DIR/plate_out.npy)")
    ap.add_argument("--len", type=float, default=2.5); ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--pick-only", action="store_true", help="print the picks and stop")
    for k, v in DEFAULTS.items():
        ap.add_argument("--" + k, default=v)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    watch = json.load(open(a.watch)) if a.watch else None
    fps, w, h, st = probe(a.src)
    nframes = int(round(a.dur * fps))
    L = max(2 * R + 1, int(round(a.len * fps)))
    n0 = int(np.ceil((a.t0 - st) * fps - 1e-6))               # source frame number of the piece's frame 0 (ffmpeg -ss
                                                              # input seek: the first frame at or after t0)
    log, rec = [], dict(src=a.src, t0=a.t0, dur=a.dur, fps=fps, frames=nframes, excerpt_frames=L, excerpts=[])
    with renderq.slot(f"chroma-key calibrate {Path(a.src).name}", pool="quick"):
        t = time.time()
        edge, hold, thumbs = analyse(a.src, a.t0, a.dur, fps, w, h)
        rec["analyse_s"] = round(time.time() - t, 1)
        picks = pick(edge, hold, L, a.n, watch, a.at, fps, len(edge) or nframes)
        for c, why in picks:
            print(f"pick: piece frame {c} ({c / fps:.2f} s into the piece): {why}")
        if a.pick_only:
            return
        os.environ["MIN_FRAMES"] = "0"                         # stage 1.5's partial-cache guard, for excerpts
        for k, (c, why) in enumerate(picks):
            # judged span c - L//2 .. +L, keyed R frames wider each side (not past the piece's own ends: there the
            # full run has no neighbours either)
            j0 = c - L // 2; j1 = j0 + L
            e0 = max(0, j0 - R); ne = min(nframes, j1 + R) - e0
            d = out / f"x{k + 1}"
            for sub in ("c1", "c15"):
                subprocess.run(["rm", "-rf", str(d / sub)])
            d.mkdir(exist_ok=True)
            plate = Path(a.plate or Path(a.code) / "plate_out.npy")
            f = dict(t0=seek_for(a.src, a.t0, st + n0 / fps, e0, fps, thumbs, w, h), dur=f"{ne / fps:.4f}", n=ne, nf=ne, f0=n0 + e0, out="",
                     c1=str(d / "c1"), src=str(d / "src_u8.npy"), watch="")
            wj = None
            if watch:                                          # the boxes, renumbered to the excerpt's frames
                wj = {"ranges": [[r[0] - e0, r[1] - e0] + list(r[2:]) for r in watch.get("ranges", [])
                                 if r[1] >= e0 and r[0] < e0 + ne]}
                json.dump(wj, open(d / "watch.json", "w")); f["watch"] = str(d / "watch.json")
            ts = time.time()
            run(a.stage1.format(**dict(f, out=str(d / "c1"))), a.code, log)
            got = len(list((d / "c1").glob("f*.npy")))
            if got < ne:
                raise SystemExit(f"calibrate: stage 1 keyed {got} of {ne} frames for excerpt {k + 1}")
            for extra in sorted((d / "c1").glob("f*.npy"))[ne:]:
                extra.unlink()
            t1 = time.time() - ts
            run(a.srcprep.format(**dict(f, out=str(d / "src_u8.npy"))), a.code, log)
            pl = d / "plate_out.npy"
            if not pl.exists():
                src_plate = plate if plate.exists() else None
                if src_plate is None:
                    raise SystemExit(f"calibrate: no plate_out.npy in {a.code} (stage 1.5 reads it beside src_u8.npy)")
                pl.symlink_to(src_plate.resolve())
            ts2 = time.time()
            run(a.stage15.format(**dict(f, out=str(d / "c15"))).rstrip(), a.code, log)
            t15 = time.time() - ts2
            rec["excerpts"].append(dict(k=k + 1, why=why, centre_piece_frame=c, first_piece_frame=j0,
                                        judged_frames=[j0 - e0, j0 - e0 + L - 1], keyed_from_piece_frame=e0, keyed_frames=ne,
                                        seek=f["t0"], stage1_s=round(t1, 1), stage15_s=round(t15, 1),
                                        watch=wj, dir=str(d)))
            print(f"excerpt {k + 1}: piece frames {j0}-{j1 - 1}, stage 1 {t1:.0f} s, stage 1.5 {t15:.0f} s",
                  flush=True)
    # contact sheet: start, centre and end of each judged span; pale, pink, matte
    from PIL import Image, ImageDraw
    rows = []
    for x in rec["excerpts"]:
        tiles = []
        a0, a1 = x["judged_frames"]
        for j in (a0, (a0 + a1) // 2, a1):
            tiles += tile(f"{x['dir']}/c15", j)
        tw, th = tiles[0].size
        row = Image.new("RGB", (tw * len(tiles), th + 28), (20, 20, 24))
        for q, im in enumerate(tiles):
            row.paste(im, (q * tw, 28))
        ImageDraw.Draw(row).text((8, 6), f"excerpt {x['k']}: piece frames {x['first_piece_frame']}-"
                                 f"{x['first_piece_frame'] + L - 1} ({x['why']}); each frame: pale, pink, matte",
                                 fill=(230, 230, 230))
        rows.append(row)
    sheet = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (20, 20, 24))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    sheet.save(out / "sheet.jpg", quality=90)
    rec["log"] = log
    json.dump(rec, open(out / "calibration.json", "w"), indent=1)
    print(f"sheet: {out / 'sheet.jpg'}\nrecord: {out / 'calibration.json'}")


if __name__ == "__main__":
    main()
