"""Stage 1 (approved keylib, unchanged maths) on C1726: key at 4K, premultiplied area-downscale to 2880x1620, cache float16 RGBA.
    python3 stage1_16.py F0 NFRAMES OUT_CACHE [X0 X1 PLATE]   (box in 4K px: the cache then holds only that box, at output scale)
Per-source calibration only: the C1726 plate, the watch search band (the watch is never above source row 900 here; the
portrait set used 2600), no garbage rows (the screen fills the whole frame) and no bottom crop (no laptop)."""
import numpy as np, sys, os, time, cv2
from multiprocessing import Pool
from scipy import ndimage as ndi
import keylib
from common16 import frames, WORK, OW, OH
F0, N, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
X0, X1 = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 3840)
PLATE = sys.argv[6] if len(sys.argv) > 6 else "plate"
assert X0 % 4 == 0 and X1 % 4 == 0
_pl = None
def plate_full(shape):
    """the full-frame plate at 4K, sliced to the processing box (same plate pixels as an uncropped run)"""
    global _pl
    if _pl is None:
        q = np.load(f"{WORK}/{PLATE}_q.npy")
        full = np.stack([ndi.zoom(q[..., c], (2160 / q.shape[0], 3840 / q.shape[1]), order=1) for c in range(3)], -1).astype(np.float32)
        _pl = np.ascontiguousarray(full[:, X0:X1])
    assert _pl.shape[:2] == shape[:2], (_pl.shape, shape)
    return _pl
keylib.plate_full = plate_full
keylib.watch_holdout.__defaults__ = (900, 70, 0.70)       # y_min, pad, dark_ratio
def done(i):
    """resume after a stop: a frame already cached (and readable) is not keyed again"""
    try: np.load(f"{OUT}/f{i:04d}.npy", mmap_mode="r").shape; return True
    except Exception: return False
def work(args):
    i, P = args
    if done(i): return i
    P = np.ascontiguousarray(P[:, X0:X1])
    a, Sc = keylib.key(P)
    A = a[..., None]
    Fp = np.clip(P - (1 - A) * Sc, 0, None) * np.clip(A * 25, 0, 1)
    Fp, _ = keylib.despill(Fp)
    ow = (X1 - X0) * 3 // 4
    Fd = cv2.resize(Fp, (ow, OH), interpolation=cv2.INTER_AREA)       # premultiplied area average = the anti-aliasing
    ad = cv2.resize(a.astype(np.float32), (ow, OH), interpolation=cv2.INTER_AREA)
    np.save(f"{OUT}/f{i:04d}.npy", np.concatenate([Fd, ad[..., None]], -1).astype(np.float16))
    return i
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); cv2.setNumThreads(2); t = time.time(); n = 0
    with Pool(int(os.environ.get("WORKERS", "4"))) as pool:
        for r in pool.imap(work, enumerate(frames(F0, N)), chunksize=1):
            n += 1
            if n % 30 == 0: print(n, "frames", round(time.time() - t), "s", flush=True)
    print("stage1 done", n, round(time.time() - t), "s"); assert n == N, f"keyed {n} of {N}"
