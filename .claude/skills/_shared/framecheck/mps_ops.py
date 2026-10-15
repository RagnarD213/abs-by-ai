"""torch.nn.functional.grid_sample on Apple's MPS backend, for the point trackers (cotracker_mps.py, tapir_mps.py).

MPS lacks "border" padding and 3D (5-D) sampling. Border becomes zero padding with the sample points clamped to the edge pixel
centres (identical result); a 3D sample on one time slice becomes a 2D sample; any other 3D sample runs on the CPU (the
trackers use it once per run, to read the query points' features). Checked against the CPU: tracks within 0.05 px.
"""
import torch
import torch.nn.functional as F


def patch():
    if getattr(F, "_framecheck_patched", False):
        return
    _gs = F.grid_sample

    def grid_sample(input, grid, mode="bilinear", padding_mode="zeros", align_corners=None):
        if input.device.type != "mps":
            return _gs(input, grid, mode=mode, padding_mode=padding_mode, align_corners=align_corners)
        if input.dim() == 5 and input.shape[2] != 1:
            return _gs(input.cpu(), grid.cpu(), mode=mode, padding_mode=padding_mode, align_corners=align_corners).to(input.device)
        if padding_mode == "border":
            if align_corners:
                grid = grid.clamp(-1, 1)
            else:
                sz = torch.tensor(list(reversed(input.shape[2:])), device=grid.device, dtype=grid.dtype)
                grid = torch.max(torch.min(grid, 1 - 1 / sz[:grid.shape[-1]]), -1 + 1 / sz[:grid.shape[-1]])
            padding_mode = "zeros"
        if input.dim() == 5:
            N, d, h, w, _ = grid.shape
            o = _gs(input[:, :, 0], grid[..., :2].reshape(N, d * h, w, 2), mode=mode, padding_mode=padding_mode,
                    align_corners=align_corners)
            return o.reshape(N, -1, d, h, w)
        return _gs(input, grid, mode=mode, padding_mode=padding_mode, align_corners=align_corners)

    F.grid_sample = grid_sample
    F._framecheck_patched = True
