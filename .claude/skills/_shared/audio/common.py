#!/usr/bin/env python3
"""ONE set of audio measurements for every video skill. Numpy only (no scipy on this Mac).

Every function here is the SAME code the approved gates used, so the numbers a session
quotes today are the numbers the previous session quoted:
  analyse()   10-band tone / voice-over-floor / dryness  -- ad-edit voice_ref_check.py
  edt()       early decay time                            -- shorts spray-tan audiogate.py
  comb_ripple() spectral ripple of a two-mic sum          -- longform chan_analyse.py
  xcorr()     inter-channel lag + polarity                -- chan_analyse.py (FFT, not O(n^2))

Why this file exists (2026-09-02): nineteen audio scripts across five skills, six of them
byte-identical copies, three pairs sharing a filename with different behaviour. A fix landed
in one and not the others, and three longforms shipped comb-filtered. Import from here.
"""
import hashlib, json, os, re, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))   # _shared/audio -> skills -> .claude -> repo
SR = 48000
EDGES = [80, 150, 250, 400, 600, 900, 1400, 2200, 3500, 5500, 9000]      # the gate's 10 bands
CENTRES = [int(round((lo * hi) ** 0.5)) for lo, hi in zip(EDGES, EDGES[1:])]
FLOOR_BANDS = ((80, 250), (250, 1000), (1000, 4000))
STAMP_VERSION = 1


def _first(*cands):
    for c in cands:
        if c and os.path.exists(c): return c
    return None

FF = _first(os.path.join(REPO, "Media/video_edit/bin/ffmpeg"), "/Volumes/Extreme/_edit_work/bin/ffmpeg")
FFP = _first(os.path.join(REPO, "Media/video_edit/bin/ffprobe"), "/Volumes/Extreme/_edit_work/bin/ffprobe")
if not FF or not FFP:
    raise SystemExit("ffmpeg/ffprobe not found at Media/video_edit/bin or /Volumes/Extreme/_edit_work/bin")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path, stream=None):
    """format duration, or a specific stream's ('a:0' / 'v:0')."""
    if stream:
        r = sh([FFP, "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration",
                "-of", "csv=p=0", path]).stdout.strip().split("\n")[0]
        if r and r != "N/A": return float(r)
    r = sh([FFP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    if not r.stdout.strip():
        raise SystemExit(f"ffprobe cannot read {path}: {(r.stderr or 'no duration').strip()[:200]} (still being written?)")
    return float(r.stdout.strip())


def probe_audio(path):
    """[{index(among audio streams), channels, codec, sample_rate}] for every audio stream."""
    out = sh([FFP, "-v", "error", "-select_streams", "a", "-show_entries",
              "stream=index,channels,codec_name,sample_rate", "-of", "json", path]).stdout
    st = json.loads(out or "{}").get("streams", [])
    return [dict(a=i, index=s.get("index"), channels=int(s.get("channels", 0)),
                 codec=s.get("codec_name"), sample_rate=int(s.get("sample_rate", 0) or 0))
            for i, s in enumerate(st)]


def has_video(path):
    return bool(sh([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_type",
                    "-of", "csv=p=0", path]).stdout.strip())


def pcm(path, af="anull", ss=None, dur=None, ac=1, sr=SR, amap=None):
    """float64 samples; shape (n,) for ac=1 else (n, ac). `amap` = '0:a:1' to pick a stream."""
    cmd = [FF, "-nostdin", "-v", "error"]
    if ss is not None: cmd += ["-ss", str(ss)]
    if dur is not None: cmd += ["-t", str(dur)]
    cmd += ["-i", path]
    if amap: cmd += ["-map", amap]
    else: cmd += ["-map", "0:a:0"]
    cmd += ["-af", af, "-ac", str(ac), "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    if ac > 1: a = a[: len(a) // ac * ac].reshape(-1, ac)
    return a


def ebur(path, af="anull", amap=None):
    """(I LUFS, true peak dBTP, LRA LU) of the whole file through `af`."""
    cmd = [FF, "-nostdin", "-nostats", "-hide_banner", "-i", path]
    cmd += ["-map", amap or "0:a:0", "-af", f"{af},ebur128=peak=true", "-f", "null", "-"]
    p = sh(cmd).stderr
    g = lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)", p)[-1])
    return g("I"), g("Peak"), g("LRA")


# ------------------------------------------------------------------ measurements
def frames(x, N, hop):
    n = (len(x) - N) // hop
    if n <= 0: return np.zeros((0, N))
    idx = np.arange(N)[None, :] + (np.arange(n) * hop)[:, None]
    return x[idx]


def analyse(a):
    """voice_ref_check.py verbatim: speech = top 40 % RMS frames, quiet = bottom 8 %, 2048-pt.
    returns (10 band levels, mean-removed dB), (voice-over-floor per FLOOR_BANDS, dB),
            dryness (median level drop 64 ms after a word ends, dB), speech spread p90-p10 dB"""
    N = 2048; hop = 1024
    fr = frames(a, N, hop)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms + 1e-12)
    sp = rms > np.percentile(rms, 60); nz = rms < np.percentile(rms, 8)
    win = np.hanning(N); f = np.fft.rfftfreq(N, 1 / SR)
    S = (np.abs(np.fft.rfft(fr[sp] * win, axis=1)) ** 2).mean(0)
    Sn = (np.abs(np.fft.rfft(fr[nz] * win, axis=1)) ** 2).mean(0)
    bands = np.array([10 * np.log10(S[(f >= lo) & (f < hi)].mean() + 1e-15) for lo, hi in zip(EDGES, EDGES[1:])])
    bands -= bands.mean()
    floor = np.array([10 * np.log10(S[(f >= lo) & (f < hi)].mean() / (Sn[(f >= lo) & (f < hi)].mean() + 1e-15))
                      for lo, hi in FLOOR_BANDS])
    drops = [db[i - 1] - db[min(i + 3, len(db) - 1)] for i in range(1, len(db) - 5)
             if sp[i - 1] and not sp[i] and db[i - 1] > np.percentile(db, 50)]
    dry = float(np.median(drops)) if drops else float("nan")
    spread = float(np.percentile(db[sp], 90) - np.percentile(db[sp], 10)) if sp.any() else float("nan")
    return bands, floor, dry, spread


def edt(x):
    """audiogate.py verbatim: ms to fall 20 dB after a speech offset (median over offsets).
    Reverb lives INSIDE the words, so no level/spectrum/gap check can see it; this can."""
    fr = frames(x, 512, 128)
    e = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    p90 = np.percentile(e, 90); o = []
    for i in range(1, len(e) - 40):
        if e[i] > p90 - 4 and e[i + 3] < e[i] - 4:
            s = e[i:i + 40]; b = np.nonzero(s < s[0] - 20)[0]
            if len(b): o.append(b[0] * 128 / SR * 1000)
    return float(np.median(o)) if o else float("nan")


def comb_ripple(sig, sr=SR):
    """chan_analyse.py: std-dev of the speech spectrum (300-6 kHz) after removing its broad tilt.
    A two-mic sum 7-8 ms apart is a comb with notches every ~130 Hz; this is what an EQ cannot
    flatten and what a 10-band tone check smooths over."""
    N = 1024
    fr = frames(sig, N, 512)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-15)
    sp = rms > np.percentile(rms, 70)
    S = np.abs(np.fft.rfft(fr[sp] * np.hanning(N), axis=1)).mean(0) + 1e-12
    f = np.fft.rfftfreq(N, 1 / sr); band = (f > 300) & (f < 6000)
    db = 20 * np.log10(S[band]); sm = np.convolve(db, np.ones(9) / 9, "same")
    return float(np.std((db - sm)[5:-5]))


def snr(sig):
    """speech rms (top 30 % frames) over the quietest 5 %, dB."""
    fr = frames(sig, 1024, 512)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-15)
    sp = rms > np.percentile(rms, 70); nz = rms < np.percentile(rms, 5)
    return float(20 * np.log10(rms[sp].mean() / max(rms[nz].mean(), 1e-9)))


def xcorr(x, y, max_ms=20.0, sr=SR, seconds=20):
    """normalised cross-correlation of x against y within +/-max_ms.
    returns (peak corr with sign, lag in samples: positive = x LAGS y (x arrives later), zero-lag corr)"""
    n = min(len(x), len(y), sr * seconds)
    x = x[:n] - x[:n].mean(); y = y[:n] - y[:n].mean()
    den = np.sqrt((x ** 2).sum() * (y ** 2).sum()) or 1e-12
    N = 1 << int(np.ceil(np.log2(n * 2)))
    c = np.fft.irfft(np.fft.rfft(x, N) * np.conj(np.fft.rfft(y, N)), N)
    m = int(max_ms / 1000 * sr)
    cc = np.concatenate([c[-m:], c[:m + 1]]) / den
    lags = np.arange(-m, m + 1)
    k = int(np.argmax(np.abs(cc)))
    return float(cc[k]), int(lags[k]), float(c[0] / den)


def silent_seconds(mono, sr=SR, thresh_db=-60.0):
    n = len(mono) // sr
    if n == 0: return 0, 0
    fr = mono[: n * sr].reshape(n, sr)
    db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    return int((db < thresh_db).sum()), int((db < -50).sum())


def sha256(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""): h.update(b)
    return h.hexdigest()


def stamp_path(media):
    return media + ".audio_gate.json"


def source_json_path(media):
    return media + ".audio_source.json"


def analysis_window(path):
    """the gate's window: 20-140 s on anything long enough, else nearly the whole file."""
    d = duration(path)
    if d >= 150: return 20.0, 120.0
    return min(1.0, d * 0.02), max(1.0, d - 2.0)


def load_source(path_or_json):
    """read audio_source.json (from pick_lav) for a media file or a json path."""
    p = path_or_json if path_or_json.endswith(".json") else source_json_path(path_or_json)
    if not os.path.exists(p):
        raise SystemExit(f"no audio_source.json for {path_or_json} -- run pick_lav.py on it first "
                         f"(selection is measured per file, never assumed)")
    return json.load(open(p))
