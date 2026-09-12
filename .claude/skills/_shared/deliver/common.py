#!/usr/bin/env python3
"""Shared plumbing for the delivery gate: tool discovery, probing, decoding, and the Row type.

⚠ NOTHING IN HERE DECIDES ANYTHING. Bounds live in formats.py, next to the file and the date they
were measured on. Measurements live in checks/. This module only knows how to read a video.

⚠ ffmpeg is FOUND, never hardcoded. Seven of the seventeen gates this module replaces began
    FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
which is why `hairgate.py` could not run on a machine with the SSD unmounted and why `tailcheck.py`
and `verify_cover.py` were pinned to one project's path. A gate that only runs in one place is not
a gate.
"""
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# ⚠ FOUR levels, not three: this file sits at <repo>/.claude/skills/_shared/deliver/common.py.
# With three it resolved to <repo>/.claude, which made `_shared/audio/require_stamp.py`
# unimportable (audio:stamp read NOT MEASURED on every run) and quietly sent ffmpeg resolution
# past the repo's own build to the Extreme SSD's -- working by luck on this Mac and nowhere else.
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def _find(tool):
    """ffmpeg/ffprobe, in preference order: the repo's own build, the SSD's, then $PATH."""
    for p in (os.path.join(REPO, "Media/video_edit/bin", tool),
              f"/Volumes/Extreme/_edit_work/bin/{tool}",
              shutil.which(tool) or ""):
        if p and os.path.exists(p):
            return p
    raise SystemExit(f"{tool} not found: looked in Media/video_edit/bin, the Extreme SSD and $PATH")


FF = _find("ffmpeg")
FP = _find("ffprobe")


# ---------------------------------------------------------------------------- the row
class Row:
    """One check's result.

    ok is THREE-STATE and the third state is the point of this module:
        True   measured, inside the bound
        False  measured, outside the bound
        None   NOT MEASURED -- the input was missing, so nobody looked. This FAILS.

    `Row.na(...)` is the only way a check can legitimately not run, it requires a written reason,
    and the reason is printed on every run where a reader can audit it.
    """

    __slots__ = ("key", "ok", "detail", "value", "na_reason")

    def __init__(self, key, ok, detail, value=None, na_reason=None):
        # ⚠ bool() on purpose: numpy comparisons return np.bool_, and `np.True_ is True` is False,
        # so a row that passed was counted as neither passed nor failed until 2026-09-11.
        self.key, self.detail = key, detail
        self.ok = None if ok is None else bool(ok)
        self.value = value or {}
        self.na_reason = na_reason

    @classmethod
    def na(cls, key, reason):
        return cls(key, True, f"not applicable: {reason}", na_reason=reason)

    @property
    def passed(self):
        return self.ok is True

    @property
    def tag(self):
        if self.na_reason:
            return "n/a "
        if self.ok is None:
            return "????"
        return "PASS" if self.ok else "FAIL"


def unmeasured(key, why):
    """The input is missing, so the check did not run. 'Nobody looked' is not 'it is fine'."""
    return Row(key, None, f"NOT MEASURED -- {why}")


# ---------------------------------------------------------------------------- probing
def probe(video):
    """Video/audio stream facts, parsed BY NAME from json.

    ⚠ PROBE THE STREAM, NOT THE CONTAINER. The container's duration is the longer of the two
    streams, so a truncated PICTURE reads back as the full length and every duration check passes --
    which is how a 10-frame hole and a 334 ms A/V offset shipped (shortad-from-longform, 2026-09).
    ⚠ And parse json by key: ffprobe's csv output is in ITS field order, so a field swap can turn a
    frame count into a duration.
    """
    def _streams(kind, extra=()):
        out = subprocess.run([FP, "-v", "error", "-select_streams", kind, "-show_entries",
                              *extra, "-of", "json", video], capture_output=True, text=True).stdout
        try:
            return json.loads(out).get("streams", [])
        except json.JSONDecodeError:
            return []

    v = _streams("v", ("stream=width,height,r_frame_rate,duration,codec_name,pix_fmt,nb_frames",))
    a = _streams("a", ("stream=codec_name,sample_rate,channels,duration",))
    if not v:
        raise SystemExit(f"no video stream in {video}")
    v = v[0]
    num, den = (str(v["r_frame_rate"]).split("/") + ["1"])[:2]
    return dict(
        width=int(v["width"]), height=int(v["height"]),
        size=f'{v["width"]}x{v["height"]}',
        fps_str=str(v["r_frame_rate"]), fps=int(num) / max(int(den), 1),
        codec=v.get("codec_name"), pix_fmt=v.get("pix_fmt"),
        vdur=float(v["duration"]) if v.get("duration") not in (None, "N/A") else None,
        adur=float(a[0]["duration"]) if a and a[0].get("duration") not in (None, "N/A") else None,
        acodec=a[0].get("codec_name") if a else None,
        asr=int(a[0]["sample_rate"]) if a and a[0].get("sample_rate") else None,
        ach=int(a[0]["channels"]) if a and a[0].get("channels") else None,
        has_audio=bool(a),
    )


def count_frames(video):
    """The real frame count. Slow (it decodes), so only the rows that need it ask."""
    out = subprocess.run([FP, "-v", "error", "-select_streams", "v", "-count_frames",
                          "-show_entries", "stream=nb_read_frames", "-of", "json", video],
                         capture_output=True, text=True).stdout
    try:
        return int(json.loads(out)["streams"][0]["nb_read_frames"])
    except Exception:
        return None


# ---------------------------------------------------------------------------- decoding
def gray(video, fps, w, h, crop=None):
    """Decode the whole file once to an (N, h*w) uint8 array of gray frames."""
    import numpy as np
    vf = f"fps={fps},"
    if crop:
        vf += f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]},"
    vf += f"scale={w}:{h},format=gray"
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-vf", vf, "-an",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw[:n * w * h], dtype=np.uint8).reshape(n, h * w)


def rgb(video, fps, w, h):
    """Decode the whole file once to an (N, h*w, 3) uint8 array."""
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-vf", f"fps={fps},scale={w}:{h}",
                          "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    n = len(raw) // (w * h * 3)
    return np.frombuffer(raw[:n * w * h * 3], dtype=np.uint8).reshape(n, h * w, 3)


def pcm(src, ac=1, sr=48000, af=None):
    """Float32 PCM. ac=2 returns (N, 2)."""
    import numpy as np
    cmd = [FF, "-v", "error", "-i", src]
    if af:
        cmd += ["-af", af]
    cmd += ["-map", "0:a", "-ac", str(ac), "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return a.reshape(-1, ac) if ac > 1 else a


def loudness(src):
    """(integrated LUFS, true peak dBTP, LRA) from one ebur128 pass."""
    import re
    err = subprocess.run([FF, "-nostdin", "-hide_banner", "-nostats", "-i", src,
                          "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    def last(k, default=None):
        m = re.findall(rf"{k}:\s*(-?[\d.]+)", err)
        return float(m[-1]) if m else default
    return last("I"), last("Peak"), last("LRA")


# ---------------------------------------------------------------------------- small helpers
def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 22)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
