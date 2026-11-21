"""Stage 1 (DS-44): key every frame at 4K with the house key (DS-40 Claude R2 keylib, unchanged maths), then downscale the
PREMULTIPLIED foreground and alpha to 0.75 scale (1620 wide) and cache them.
Only change from the approved stage1_key.py: the output scale. R2 cached at 0.5 (exact 2x2 average); a Short needs a wide
AND a tight window of Dan (zoom cuts), so the cache is kept at 0.75 and the window is area-resized to 1080 later. The
premultiplied area resize is the same anti-aliasing at a different ratio. Resumes: frames already cached are skipped.
    python3 stage1_key.py T0 DUR OUT
"""
import numpy as np, sys, os, time, cv2
from multiprocessing import Pool
from common import frames
from keylib import key, despill
T0, DUR = float(sys.argv[1]), float(sys.argv[2])
OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
Y_GARBAGE = 480        # source rows above this are never Dan (screen top edge); hair top 628-744 on this set (measured again below)
Y_BOTTOM = int(os.environ.get("Y_BOTTOM", "3490"))   # laptop line (crop above it); 3840 = keep the laptop (R2 standard reaction layout)
S = 0.75               # source -> cache scale (2160 -> 1620)
OW, OH = int(2160 * S), int(round(Y_BOTTOM * S))      # 1620 x 2618
cv2.setNumThreads(1)
def work(args):
    i, P = args
    if os.path.exists(f"{OUT}/f{i:04d}.npy"):
        return i
    a, Sc = key(P)
    a[:Y_GARBAGE] = 0
    A = a[..., None]
    Fp = np.clip(P - (1 - A) * Sc, 0, None) * np.clip(A * 25, 0, 1)
    Fp, _ = despill(Fp)
    Fp = np.ascontiguousarray(Fp[:Y_BOTTOM]); a = np.ascontiguousarray(a[:Y_BOTTOM])
    Fd = cv2.resize(Fp, (OW, OH), interpolation=cv2.INTER_AREA)
    ad = cv2.resize(a, (OW, OH), interpolation=cv2.INTER_AREA)
    np.save(f"{OUT}/f{i:04d}.npy", np.concatenate([Fd, ad[..., None]], -1).astype(np.float16))
    return i
if __name__ == "__main__":
    t = time.time()
    with Pool(int(os.environ.get("WORKERS", "4"))) as pool:
        n = 0
        for r in pool.imap(work, enumerate(frames(T0, dur=DUR)), chunksize=1):
            n += 1
            if n % 60 == 0: print(n, "frames", round(time.time() - t), "s", flush=True)
    print("done", n, round(time.time() - t), "s")
    assert n > 0, "no frames keyed"
