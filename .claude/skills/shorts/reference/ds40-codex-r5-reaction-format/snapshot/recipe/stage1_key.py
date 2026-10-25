"""Stage 1: key every frame of the sample at 4K, downscale premultiplied fg + alpha to output scale, cache.

Speed (2026-10-21, Handoffs/results-20261021-cheap-key.md): RENDERQ_CORES workers (the render queue's allowance,
default 4; WORKERS overrides), one cv2/BLAS thread each, frames sent to workers as the decoder's 16-bit words (half
the bytes of float32; converted in the worker with the same expression as common.frames), each cache file written
under a temporary name and renamed, so a killed run never leaves a half-written frame for stage 1.5 to read."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np, sys, time, subprocess, cv2
from multiprocessing import Pool
from scipy import ndimage as ndi
from common import frames, FF, SRC, W, H, DEC
from keylib import key, despill, _blockmean
T0, DUR = float(sys.argv[1]), float(sys.argv[2])
OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
Y_GARBAGE = 480        # source rows above this are never Dan (screen top edge); hair top >= 628 in this take
Y_BOTTOM = 3840        # laptop line (tilted, 3515 right .. 3660 left); crop above it
S = 0.5                # source -> output scale (2160 -> 1080)
CORES = int(os.environ.get("WORKERS") or os.environ.get("RENDERQ_CORES") or 4)

def frames_u16(t0, dur=None, src=SRC):
    """common.frames(t0, dur) without the float conversion: (H, W, 3) uint16 words, converted in the worker."""
    cmd = [FF, "-v", "error", "-ss", f"{t0:.3f}", "-i", src]
    if dur: cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vf", DEC, "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W*H*6)
    n = W*H*3*2
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint16).reshape(H, W, 3)
    p.wait()

def init():
    cv2.setNumThreads(1)

def save(path, arr):
    d, f = os.path.split(path); tmp = os.path.join(d, ".tmp_" + f)
    np.save(tmp, arr); os.replace(tmp, path)

def work(args):
    i, P = args
    if os.path.exists(f"{OUT}/f{i:04d}.npy"):   # already keyed (resume after an interrupted run; files are written
        return i                                 # whole, then renamed, so an existing one is complete)
    if P.dtype == np.uint16:
        P = P.astype(np.float32) / 65535.0        # = common.frames
    a, Sc = key(P)
    a[:Y_GARBAGE] = 0
    A = a[..., None]
    Fp = np.clip(P - (1 - A) * Sc, 0, None) * np.clip(A * 25, 0, 1)
    Fp, _ = despill(Fp)
    Fp = Fp[:Y_BOTTOM]; a = a[:Y_BOTTOM]
    h, w = a.shape
    # premultiplied area downscale x0.5 (exact 2x2 average)
    Fd = _blockmean(Fp, 2)                # = reshape(h2, 2, w2, 2, 3).mean((1, 3)), bit-identical
    ad = _blockmean(a, 2)
    save(f"{OUT}/f{i:04d}.npy", np.concatenate([Fd, ad[..., None]], -1).astype(np.float16))
    return i
if __name__ == "__main__":
    t = time.time()
    with Pool(CORES, initializer=init) as pool:
        n = 0
        for r in pool.imap(work, enumerate(frames_u16(T0, dur=DUR)), chunksize=1):
            n += 1
            if n % 30 == 0: print(n, "frames", round(time.time() - t), "s", flush=True)
    print("done", n, round(time.time() - t), "s")
    assert n > 0, "no frames keyed"
