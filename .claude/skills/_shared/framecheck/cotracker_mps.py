"""CoTracker3 (Meta, offline model) on this Mac's GPU, for clipcheck.py.

Two ops CoTracker uses are missing on Apple's MPS backend: grid_sampler_3d and "border" padding. With
PYTORCH_ENABLE_MPS_FALLBACK=1 every iteration round-trips to the CPU. mps_ops.py and the sample_features5d below replace
both with exact 2D equivalents (tracks identical to the CPU run within 0.05 px, visibility identical, 2026-10-14).
A second limit: memory. GPU memory grows with frames x points (64 x 650: 7.8 GB, 96 x 650: 12 GB, 64 x 1300: 13.4 GB) and
the Mac shares it with every render other sessions run; past the free memory it swaps and a 6 s take ran 8 minutes (and once
never finished). So clipcheck samples a take down to MAX_FRAMES and tracks the points in batches of POINT_BUDGET / frames.

Install once: pip3 install --user "git+https://github.com/facebookresearch/co-tracker.git"; the checkpoint
(facebook/cotracker3, scaled_offline.pth, 100 MB) downloads from Hugging Face on first use.
Licence: CoTracker3 code and weights are CC BY-NC 4.0 (non-commercial); see README, "Licences".
"""
import torch
import torch.nn.functional as F

MAX_FRAMES = 64
POINT_BUDGET = 40000     # frames x points per batch: about 6 GB
_model = {}


def _patch():
    import cotracker.models.core.cotracker.cotracker3_online as on
    from cotracker.models.core.model_utils import bilinear_sampler
    if getattr(on, "_framecheck_patched", False):
        return

    def sample_features5d(input, coords):
        # input B T C H W, coords B R1 R2 3 (t, x, y) -> B R1 R2 C, linear in t, one 2D sample per time slice used
        B, T, C, H, W = input.shape; _, R1, R2, _ = coords.shape
        c = coords.reshape(B, R1 * R2, 3); out = torch.zeros(B, R1 * R2, C, device=input.device, dtype=input.dtype)
        t = c[..., 0].clamp(0, T - 1); t0 = t.floor().long(); w1 = t - t0.float(); t1 = (t0 + 1).clamp(max=T - 1)
        for b in range(B):
            for ti in torch.unique(torch.cat([t0[b], t1[b]])).tolist():
                for tt, w in ((t0[b], 1 - w1[b]), (t1[b], w1[b])):
                    sel = (tt == ti) & (w > 0)
                    if sel.any():
                        f = bilinear_sampler(input[b, ti][None], c[b, sel, 1:][None, :, None, :])[0, :, :, 0].T
                        out[b, sel] += f * w[sel][:, None]
        return out.view(B, R1, R2, C)

    import mps_ops; mps_ops.patch()          # grid_sample: border padding and 3D samples on MPS
    on.sample_features5d = sample_features5d
    on._framecheck_patched = True


def model():
    if "m" not in _model:
        _patch()
        from cotracker.predictor import CoTrackerPredictor
        from huggingface_hub import hf_hub_download
        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        _model["m"] = CoTrackerPredictor(checkpoint=hf_hub_download("facebook/cotracker3", "scaled_offline.pth")).to(dev)
        _model["dev"] = dev
    return _model["m"], _model["dev"]


def track(frames, queries):
    """frames: uint8 RGB (T, H, W, 3), already small (the model works at 384x512); queries: (N, 3) array of (t, x, y) in those
    pixels. Returns tracks (T, N, 2) in the same pixels and visibility (T, N) bool (CoTracker's > 0.9)."""
    import numpy as np
    m, dev = model()
    V = torch.from_numpy(np.ascontiguousarray(frames)).permute(0, 3, 1, 2)[None].float().to(dev)
    queries = np.asarray(queries, np.float32); step = max(64, POINT_BUDGET // len(frames)); trs, vss = [], []
    for i in range(0, len(queries), step):
        with torch.no_grad():
            tr, vis = m(V, queries=torch.from_numpy(queries[i:i + step])[None].to(dev))
        trs.append(tr[0].cpu().numpy()); vss.append(vis[0].cpu().numpy())
        del tr, vis
        if dev == "mps":
            torch.mps.empty_cache()
    return np.concatenate(trs, 1), np.concatenate(vss, 1)
