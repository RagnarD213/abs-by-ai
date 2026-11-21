#!/usr/bin/env python3
"""Container rows: is this the file we said we were delivering, all of it, at the right shape."""
import os

from .. import common as C
from ..common import Row, unmeasured


def size(key, pr, cfg, plan, video):
    want = cfg["size"]
    return Row(key, pr["size"] == want, f'frame size {pr["size"]} (want {want})',
               dict(got=pr["size"], want=want))


def fps(key, pr, cfg, plan, video):
    want = cfg["fps"]
    return Row(key, pr["fps_str"] == want, f'frame rate {pr["fps_str"]} (want {want})',
               dict(got=pr["fps_str"], want=want))


def codec(key, pr, cfg, plan, video):
    vok = pr["codec"] == cfg["vcodec"]
    aok = (pr["acodec"] == cfg["acodec"] and pr["asr"] == cfg["asr"]
           and pr["ach"] == cfg["achannels"])
    return Row(key, vok and aok,
               f'{pr["codec"]} / {pr["acodec"]} {pr["asr"]} Hz {pr["ach"]} ch '
               f'(want {cfg["vcodec"]} / {cfg["acodec"]} {cfg["asr"]} Hz {cfg["achannels"]} ch)',
               dict(vcodec=pr["codec"], acodec=pr["acodec"], sr=pr["asr"], ch=pr["ach"]))


def duration(key, pr, cfg, plan, video):
    """container:duration -- the VIDEO STREAM against the cut this one reproduces.

    ⚠ The target comes from the plan or from a reference cut, never from the container. See the
    warning in common.probe: a truncated picture reads back as the full length on the container.
    """
    tgt = plan.get("target_seconds")
    if tgt is None and plan.get("reference_cut"):
        ref = plan["reference_cut"]
        if os.path.exists(ref):
            tgt = C.probe(ref)["vdur"]
    if tgt is None:
        return unmeasured(key, "the plan gives neither `target_seconds` nor a readable "
                               "`reference_cut`, so there is nothing to check the length against")
    tol = cfg["tolerance_s"]
    got = pr["vdur"]
    return Row(key, abs(got - tgt) <= tol,
               f"video stream {got:.3f}s vs target {tgt:.3f}s (tolerance {tol}s)",
               dict(duration=round(got, 3), target=round(tgt, 3), tolerance=tol))


def frames(key, pr, cfg, plan, video):
    """container:frames -- every planned frame present. A truncated beat is silent otherwise."""
    want = plan.get("target_frames")
    if want is None:
        return unmeasured(key, "the plan gives no `target_frames`; put the beat sheet's own frame "
                               "count there so a truncated beat cannot pass as a rounding error")
    got = C.count_frames(video)
    if got is None:
        return unmeasured(key, "ffprobe could not count frames on this file")
    return Row(key, got == want, f"{got} frames present, {want} planned",
               dict(frames=got, planned=want))
