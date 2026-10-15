"""BootsTAPIR (Google DeepMind, offline PyTorch TAPIR) for clipcheck.py: the licence-clean tracker. Code (vendored in
vendor/tapnet, torch files only) and checkpoint are Apache 2.0, so it may run on commercial work; CoTracker3 is CC BY-NC.
The checkpoint (bootstapir_checkpoint_v2.pt, 219 MB) downloads to ~/.cache/framecheck on first use.
Same call as cotracker_mps.track: frames uint8 RGB (T, H, W, 3); queries (N, 3) of (t, x, y) in those pixels.
"""
import os, sys
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CKPT = os.path.expanduser("~/.cache/framecheck/bootstapir_checkpoint_v2.pt")
URL = "https://storage.googleapis.com/dm-tapnet/bootstap/bootstapir_checkpoint_v2.pt"
RES = 512                # BootsTAPIR is best at 512 x 512 (tapnet README)
POINT_BUDGET = 64 * 700  # frames x points per call
_model = {}


def model():
    if "m" not in _model:
        import mps_ops; mps_ops.patch()
        sys.path.insert(0, os.path.join(HERE, "vendor"))
        from tapnet.torch import tapir_model
        if not os.path.exists(CKPT):
            import urllib.request
            os.makedirs(os.path.dirname(CKPT), exist_ok=True); urllib.request.urlretrieve(URL, CKPT + ".part"); os.replace(CKPT + ".part", CKPT)
        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        m = tapir_model.TAPIR(pyramid_level=1, extra_convs=True)
        m.load_state_dict(torch.load(CKPT, map_location="cpu")); _model["m"] = m.to(dev).eval(); _model["dev"] = dev
    return _model["m"], _model["dev"]


def track(frames, queries):
    import cv2
    m, dev = model()
    T, H, W, _ = frames.shape
    v = np.stack([cv2.resize(f, (RES, RES), interpolation=cv2.INTER_AREA) for f in frames]).astype(np.float32) / 255 * 2 - 1
    V = torch.from_numpy(v)[None].to(dev)
    q = np.asarray(queries, np.float32); sx, sy = RES / W, RES / H
    qq = np.stack([q[:, 0], q[:, 2] * sy, q[:, 1] * sx], 1)            # TAPIR wants (t, y, x)
    step = max(64, POINT_BUDGET // T); trs, vss = [], []
    for i in range(0, len(qq), step):
        with torch.no_grad():
            o = m(V, torch.from_numpy(qq[i:i + step])[None].to(dev))
        vis = (1 - torch.sigmoid(o["occlusion"][0])) * (1 - torch.sigmoid(o["expected_dist"][0])) > 0.5   # N T
        trs.append(o["tracks"][0].permute(1, 0, 2).cpu().numpy()); vss.append(vis.T.cpu().numpy())
        del o
        if dev == "mps":
            torch.mps.empty_cache()
    tr = np.concatenate(trs, 1); tr[..., 0] /= sx; tr[..., 1] /= sy
    return tr, np.concatenate(vss, 1)
