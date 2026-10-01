"""Composite HyperFrames renders into a film, in RGB. Generalised from Media/hyperframes/round2-templates/composite.py.

Three rules (README, "Rules that bit"):
  1. Decode each file by its own matrix: HyperFrames renders are UNTAGGED BT.601 limited range, our bases are tagged
     BT.709. An overlay=format=auto in YUV mixes the two (the 3A navy reads 7,37,75 instead of 10,38,72).
  2. The lower third's glass: blur the base (GaussianBlur 14) inside the `_mask` render's alpha, then lay the content
     render (tint, hairline, text, bar) on top.
  3. An opaque scene (before card) replaces exactly fr(b) - fr(a) frames.

Two ways in:
  * API, inside a video's own per-frame RGB render loop (in place of the PIL paint for these four kinds):
        C = Compositor(json.load(open("OUT/manifest.json")))
        if C.opaque(g): frame = C.apply(None, g)          # the scene IS the frame
        else:           frame = C.apply(frame, g)         # overlays on the graded base (numpy HxWx3 uint8)
    g is the frame index on the film timeline (round(t * 30000/1001)). Readers open lazily and restart on a jump.
  * CLI, on a finished base file:
        python3 composite.py manifest.json --base base.mp4 --base-t0 <film s of base frame 0> --out out.mp4 [--audio a.wav]
"""
import argparse, json, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000 / 1001; FPSS = "30000/1001"; WH = (1920, 1080)


def fr(t): return int(round(t * FPS))


_MAT = {}
def matrix(path):
    """The file's decode matrix: untagged (HyperFrames) = BT.601, tagged bt709 = BT.709. Cached; retried, because a
    loaded machine can hand back an empty ffprobe answer."""
    if path in _MAT: return _MAT[path]
    for _ in range(5):
        r = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=color_space", "-of", "json", path], capture_output=True, text=True)
        st = json.loads(r.stdout or "{}").get("streams")
        if st: break
        import time; time.sleep(1)
    else:
        raise RuntimeError(f"ffprobe could not read {path}: {r.stderr[-300:]}")
    cs = st[0].get("color_space") or "bt470bg"
    _MAT[path] = {"bt709": "bt709", "bt470bg": "bt601", "smpte170m": "bt601"}.get(cs, "bt709")
    return _MAT[path]


def reader(path, start=0, n=None, rgba=False, wh=None):
    """Frames of `path` from frame index `start`, decoded by the file's own matrix."""
    ch = 4 if rgba else 3
    wh = wh or WH                                  # 1920x1080, or the vertical's 1080x1920 (Compositor(manifest, wh=))
    vf = f"scale=in_color_matrix={matrix(path)}:in_range=tv,format={'rgba' if rgba else 'rgb24'}"
    if start: vf = f"trim=start_frame={start},setpts=PTS-STARTPTS," + vf
    cmd = [FF, "-v", "error", "-i", path, "-vf", vf]
    if n: cmd += ["-frames:v", str(n)]
    p = subprocess.Popen(cmd + ["-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = wh[0] * wh[1] * ch; done = False
    try:
        while True:
            b = p.stdout.read(size)
            if len(b) < size: done = True; break
            yield np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], ch)
    finally:
        if not done: p.kill()                 # closed early (a still, a seek): stop ffmpeg quietly
        p.stdout.close(); p.wait()


def over(dst, ov):
    a = ov[..., 3:4].astype(np.float32) / 255
    return (dst.astype(np.float32) * (1 - a) + ov[..., :3].astype(np.float32) * a + 0.5).astype(np.uint8)


def glass(base, mask_rgba, band, radius=14):
    y0, y1 = band
    m = mask_rgba[y0:y1, :, 3:4].astype(np.float32) / 255
    if not m.any(): return base
    bl = np.asarray(Image.fromarray(np.ascontiguousarray(base[y0:y1])).filter(ImageFilter.GaussianBlur(radius)), np.float32)
    out = base.copy()
    out[y0:y1] = (base[y0:y1].astype(np.float32) * (1 - m) + bl * m + 0.5).astype(np.uint8)
    return out


class _Track:
    def __init__(self, path, g0, n, rgba, wh=None):
        self.path, self.g0, self.n, self.rgba, self.wh = path, g0, n, rgba, wh
        self.it, self.next_g = None, None

    def frame(self, g):
        if self.it is None or g != self.next_g:
            self.it = reader(self.path, g - self.g0, self.g0 + self.n - g, self.rgba, self.wh)
        self.next_g = g + 1
        f = next(self.it, None)
        assert f is not None, f"{self.path}: no frame {g - self.g0} of {self.n} (render shorter than its slot)"
        return f


class Compositor:
    def __init__(self, manifest, wh=None):
        self.items = []
        for m in manifest:
            g0, g1 = fr(m["a"]), fr(m["b"]); n = g1 - g0
            it = dict(m, g0=g0, g1=g1, ov=_Track(m["mov"], g0, n, True, wh))
            if m["kind"] == "glass": it["mk"] = _Track(m["mask"], g0, n, True, wh)
            self.items.append(it)

    def active(self, g): return [it for it in self.items if it["g0"] <= g < it["g1"]]
    def opaque(self, g): return any(it["kind"] == "opaque" for it in self.active(g))
    def card(self, g): return next((it for it in self.active(g) if it["kind"] == "overlay"), None)

    def apply(self, frame, g):
        act = self.active(g)
        op = [it for it in act if it["kind"] == "opaque"]
        if op:
            frame = np.ascontiguousarray(op[-1]["ov"].frame(g)[..., :3])
        for it in act:
            if it["kind"] == "overlay": frame = over(frame, it["ov"].frame(g))
        for it in act:                                              # lower thirds last: they sit over a side card
            if it["kind"] == "glass":
                frame = over(glass(frame, it["mk"].frame(g), it.get("band", (760, 1080))), it["ov"].frame(g))
        return frame


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest"); ap.add_argument("--base", required=True); ap.add_argument("--base-t0", type=float, required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--audio")
    A = ap.parse_args()
    C = Compositor(json.load(open(A.manifest))); g_base = fr(A.base_t0)
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-"]
    if A.audio: cmd += ["-i", A.audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k"]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", A.out]
    e = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, f in enumerate(reader(A.base)):
        e.stdin.write(np.ascontiguousarray(C.apply(f, g_base + i)).tobytes())
    e.stdin.close(); e.wait()
    print("composited", A.out, flush=True)


if __name__ == "__main__":
    main()
