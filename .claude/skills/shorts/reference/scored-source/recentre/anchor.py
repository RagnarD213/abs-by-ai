"""A stable horizontal anchor for the presenter.

The whole-mask centroid is unusable: his hands fly in and out of frame while he talks and
drag it 100-500px between adjacent frames. The torso is the part that does not move -- so
the anchor is the midpoint of the TALL columns (the head/torso block), and outstretched
arms are excluded by construction.
"""
import numpy as np

def anchors(mask):
    h, w = mask.shape
    cov = mask.sum(0).astype(float) / h
    if cov.max() < 0.05:
        return None
    on = np.where(cov >= 0.02)[0]
    if len(on) < 5:
        return None
    tall = np.where(cov >= 0.60 * cov.max())[0]      # the torso block
    if len(tall) < 3:
        tall = on
    ys, xs = np.nonzero(mask)
    y0, y1 = ys.min(), ys.max()
    head = xs[ys <= y0 + 0.18 * (y1 - y0)]           # head only
    return dict(
        torso=float((tall.min() + tall.max()) / 2 / w),
        head=float(np.median(head) / w) if len(head) else float((tall.min()+tall.max())/2/w),
        l=float(on.min() / w), r=float(on.max() / w),
        cen=float(xs.mean() / w),
    )
