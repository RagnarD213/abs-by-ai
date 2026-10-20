"""Stage 1: key every frame of the sample at 4K, downscale premultiplied fg + alpha to output scale, cache."""
import numpy as np, sys, os, time
from multiprocessing import Pool
from scipy import ndimage as ndi
from common import frames
from keylib import key, despill
T0, DUR = float(sys.argv[1]), float(sys.argv[2])
OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
Y_GARBAGE = 480        # source rows above this are never Dan (screen top edge); hair top >= 628 in this take
Y_BOTTOM = 3490        # laptop line (tilted, 3515 right .. 3660 left); crop above it
S = 0.5                # source -> output scale (2160 -> 1080)
def work(args):
    i, P = args
    a, Sc = key(P)
    a[:Y_GARBAGE] = 0
    A = a[..., None]
    Fp = np.clip(P - (1 - A) * Sc, 0, None) * np.clip(A * 25, 0, 1)
    Fp, _ = despill(Fp)
    Fp = Fp[:Y_BOTTOM]; a = a[:Y_BOTTOM]
    h, w = a.shape
    # premultiplied area downscale x0.5 (exact 2x2 average)
    h2, w2 = h // 2, w // 2
    Fd = Fp[:h2*2, :w2*2].reshape(h2, 2, w2, 2, 3).mean((1, 3))
    ad = a[:h2*2, :w2*2].reshape(h2, 2, w2, 2).mean((1, 3))
    np.save(f"{OUT}/f{i:04d}.npy", np.concatenate([Fd, ad[..., None]], -1).astype(np.float16))
    return i
if __name__ == "__main__":
    t = time.time()
    with Pool(4) as pool:
        n = 0
        for r in pool.imap(work, enumerate(frames(T0, dur=DUR)), chunksize=1):
            n += 1
            if n % 30 == 0: print(n, "frames", round(time.time() - t), "s", flush=True)
    print("done", n, round(time.time() - t), "s")
    assert n > 0, "no frames keyed"
