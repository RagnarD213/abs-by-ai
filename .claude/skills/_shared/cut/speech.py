#!/usr/bin/env python3
"""Shared plumbing for the cut module: words, the measured envelope, gaps, and transcription.

⚠ NOTHING IN HERE DECIDES ANYTHING. The junk detectors are in junk.py, take selection in takes.py,
and every bound a delivery is held to lives in `_shared/deliver/formats.py`. This module only knows
how to read speech out of a file.

Four word formats reach this module and all of them collapse to ONE shape, sorted by onset:

    {"w": " word", "t": start_s, "e": end_s, "p": probability_or_None}

  * a Whisper result          {"segments": [{"words": [{"word", "start", "end", "probability"}]}]}
  * a roll sidecar            {"words": [{"word", "start", "end", "probability"}]}
  * a tight-cuts file         {"words": [{"w", "t", "e"}]}       (ad-edit / website-video plans)
  * a shorts words.json       {"chunks": [{"text", "timestamp": [t, e]}]}

THE ENVELOPE. 20 ms RMS in dBFS at 16 kHz mono. Every measurement here is against the file's OWN
speech level, never a constant: the spray-tan lav sits at −19 dB RMS, a finished master at −14 LUFS,
and the same absolute threshold means different things on the two.

GAPS are the silencedetect-equivalent the original `gaps.json` files were built from
(`_edit_work/silences.py`: noise=−30 dB, d=0.10 on the lav wav). Reproduced here as frames below
min(−30 dBFS, speech level − 13 dB) for ≥ 0.10 s, so junkscan's 0.55 s and fixonsets' 0.25 s keep
the meaning they were calibrated with.

TRANSCRIPTION goes through `ad-edit/reference/whisper_chunked.py` -- the only runner that gets a
COMPLETE transcript of a roll full of retakes (overlapping windows, condition_on_previous_text=False)
-- and is cached by the media file's sha256 under Media/_cache/asr/ (git-ignored). It waits for a
build slot first: the two-concurrent-build cap in `_shared/VIDEO-RULES.md` applies to transcription.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(os.path.dirname(SKILLS))
CACHE = os.path.join(REPO, "Media", "_cache", "asr")
CHUNKED = os.path.join(SKILLS, "ad-edit", "reference", "whisper_chunked.py")

SR = 16000
HOP_S = 0.02
HOP = int(SR * HOP_S)


def _find(tool):
    for p in (os.path.join(REPO, "Media/video_edit/bin", tool),
              f"/Volumes/Extreme/_edit_work/bin/{tool}",
              shutil.which(tool) or ""):
        if p and os.path.exists(p):
            return p
    raise SystemExit(f"{tool} not found: looked in Media/video_edit/bin, the Extreme SSD and $PATH")


FF = _find("ffmpeg")
FP = _find("ffprobe")
# whisper's own loader shells out to a bare `ffmpeg`; a gate run from a plain shell has none on
# $PATH (FileNotFoundError: 'ffmpeg' inside junk:repeated_take, 2026-09-24). Put ours first.
os.environ["PATH"] = os.path.dirname(FF) + os.pathsep + os.environ.get("PATH", "")


# ---------------------------------------------------------------------------- words
def norm(s):
    return re.sub(r"[^a-z0-9']", "", str(s).lower())


def load_words(src):
    """Any of the four word formats -> the one shape, sorted by onset. `src` is a path or a dict."""
    d = json.load(open(src)) if isinstance(src, str) else src
    out = []
    if isinstance(d, dict) and "segments" in d:
        for s in d["segments"]:
            ws = s.get("words", [])
            if isinstance(ws, str):                       # a stringified list (some exports)
                import ast
                ws = ast.literal_eval(ws)
            for x in ws:
                out.append(dict(w=x["word"], t=float(x["start"]), e=float(x["end"]),
                                p=x.get("probability")))
    elif isinstance(d, dict) and "words" in d:
        for x in d["words"]:
            if "start" in x:
                out.append(dict(w=x["word"], t=float(x["start"]), e=float(x["end"]),
                                p=x.get("probability")))
            else:
                out.append(dict(w=x["w"], t=float(x["t"]), e=float(x["e"]), p=x.get("p")))
    elif isinstance(d, dict) and "chunks" in d:
        for x in d["chunks"]:
            t, e = x["timestamp"]
            out.append(dict(w=x["text"], t=float(t), e=float(e if e is not None else t), p=None))
    elif isinstance(d, list):
        for x in d:
            out.append(dict(w=x.get("w", x.get("word")), t=float(x.get("t", x.get("start"))),
                            e=float(x.get("e", x.get("end"))), p=x.get("p", x.get("probability"))))
    else:
        raise SystemExit("unrecognised word file: expected segments / words / chunks")
    out = [w for w in out if norm(w["w"])]
    out.sort(key=lambda w: (w["t"], w["e"]))
    return out


def words_in(words, t0, t1):
    return [w for w in words if w["e"] > t0 and w["t"] < t1]


def text_of(words):
    return " ".join(norm(w["w"]) for w in words if norm(w["w"]))


# ---------------------------------------------------------------------------- audio
def wav16k(media, out, amap=None, af=None, ss=None, dur=None):
    """Decode any media to 16 kHz mono PCM16 (what Whisper and the envelope both want)."""
    cmd = [FF, "-nostdin", "-v", "error", "-y"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", media, "-map", amap or "0:a:0"]
    if af:
        cmd += ["-af", af]
    cmd += ["-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", out]
    subprocess.run(cmd, check=True)
    return out


def pcm(media, amap=None, af=None):
    cmd = [FF, "-nostdin", "-v", "error", "-i", media, "-map", amap or "0:a:0"]
    if af:
        cmd += ["-af", af]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def envelope(a):
    """20 ms RMS in dBFS. Index i covers [i*0.02, (i+1)*0.02)."""
    n = len(a) // HOP
    if n == 0:
        return np.zeros(0)
    fr = a[:n * HOP].reshape(n, HOP)
    return 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)


def speech_level(db):
    """Median dB of the loudest 40 % of frames -- the file's own speaking level."""
    if len(db) == 0:
        return -60.0
    return float(np.median(db[db >= np.percentile(db, 60)]))


def gap_threshold(db):
    """silencedetect noise=-30dB on a −19 dB lav, made relative: min(−30, speech − 13)."""
    return min(-30.0, speech_level(db) - 13.0)


def gaps_from_envelope(db, thr=None, min_s=0.10):
    """[[start, end], ...] runs below `thr` lasting ≥ min_s. The measured silence, which VALIDATES
    every word boundary Whisper claims (longform-edit Step 3)."""
    if thr is None:
        thr = gap_threshold(db)
    quiet = db < thr
    out, i, n = [], 0, len(quiet)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * HOP_S >= min_s:
                out.append([round(i * HOP_S, 3), round(j * HOP_S, 3)])
            i = j
        else:
            i += 1
    return out


def gap_at(gaps, t):
    for g0, g1 in gaps:
        if g0 < t < g1:
            return (g0, g1)
        if g0 > t:
            break
    return None


# ---------------------------------------------------------------------------- build cap
def active_builds():
    """The other sessions' renders, transcriptions and gates (VIDEO-RULES: cap is TWO)."""
    try:
        sys.path.insert(0, SKILLS)
        from _shared.rolls import roll_sidecar as RS
        return RS.active_builds()
    except Exception:                                        # noqa: BLE001
        out = subprocess.run(["ps", "-Ao", "pid=,command="], capture_output=True, text=True).stdout
        pat = re.compile(r"ffmpeg|whisper|render\.py|gate\.py|qc_style", re.I)
        me = os.getpid()
        return [l for l in out.splitlines()
                if pat.search(l) and not l.strip().startswith(str(me))]


def wait_for_build_slot(label, quiet=False):
    said = False
    while len(active_builds()) >= 2:
        if not said and not quiet:
            print(f"WAIT {label}: two other builds are active; not taking a third slot", flush=True)
            said = True
        time.sleep(20)


# ---------------------------------------------------------------------------- transcription
def sha256(path, cap=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 22)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def cached_words_path(media, model, amap=None, af=None):
    key = sha256(media) + (f".{norm(amap or '')}{norm(af or '')}" if (amap or af) else "")
    return os.path.join(CACHE, f"{key}.{model}.words.json")


def transcribe(media, model="small", amap=None, af=None, force=False, quiet=False):
    """Chunked Whisper over the media's audio, cached by the media's sha256.

    Returns (words, source) where source is 'cache:<path>' or 'whisper:<model>'. The chunked runner
    is the ad-edit one -- one implementation of the overlapping-window transcript, not a fork.
    """
    if not os.path.exists(CHUNKED):
        raise SystemExit(f"whisper runner not on disk: {CHUNKED}")
    cp = cached_words_path(media, model, amap, af)
    if os.path.exists(cp) and not force:
        return load_words(cp), f"cache:{cp}"
    wait_for_build_slot(f"Whisper {model} on {os.path.basename(media)}", quiet)
    os.makedirs(CACHE, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cut-asr-") as tmp:
        wav = wav16k(media, os.path.join(tmp, "a.wav"), amap, af)
        out = os.path.join(tmp, "whisper.json")
        env = os.environ.copy()
        env["PATH"] = os.path.dirname(FF) + os.pathsep + env.get("PATH", "")
        env.setdefault("FF", FF)
        r = subprocess.run(["nice", "-n", "10", sys.executable, CHUNKED, wav, out, model],
                           capture_output=True, text=True, env=env)
        if r.returncode != 0 or not os.path.exists(out):
            raise SystemExit(f"whisper_chunked failed on {media}:\n{(r.stdout + r.stderr)[-2000:]}")
        words = load_words(out)
    json.dump({"words": [dict(word=w["w"], start=w["t"], end=w["e"], probability=w["p"])
                         for w in words],
               "source": os.path.abspath(media), "model": model, "amap": amap, "af": af,
               "when": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
              open(cp, "w"))
    return words, f"whisper:{model}"


_MODELS = {}


def _model(name):
    if name not in _MODELS:
        import whisper
        _MODELS[name] = whisper.load_model(name)
    return _MODELS[name]


def retranscribe_span(wav, t0, t1, model="medium.en"):
    """The isolated re-transcription every stretched-word / repeat flag is verified with
    (ad-edit lesson 56, longform-edit junk rule 2): 4 s of audio alone, no prior context, so a
    restart Whisper stitched shut in the full pass has nowhere to hide.

    Returns words in FILE time. ⚠ The window must extend ~1.5 s past the span of interest:
    truncating Whisper's audio at the join drops the final word (longform-edit Step 3).
    """
    t0 = max(0.0, t0)
    with tempfile.TemporaryDirectory(prefix="cut-span-") as tmp:
        clip = os.path.join(tmp, "s.wav")
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t",
                        f"{t1 - t0:.3f}", "-i", wav, "-ac", "1", "-ar", str(SR), clip], check=True)
        # ⚠ default temperature FALLBACK, not a pinned 0.0: pinned, a 7.6 s clip holding a 1.46 s
        # pause came back as three words ("work just fine.") and Dan's 4:00 restart read
        # "not confirmed" (2026-09-24). The fallback ladder is what recovers the rest of the clip.
        r = _model(model).transcribe(clip, word_timestamps=True, language="en", verbose=False,
                                     condition_on_previous_text=False)
    out = []
    for s in r["segments"]:
        for x in s.get("words", []):
            out.append(dict(w=x["word"], t=round(x["start"] + t0, 3), e=round(x["end"] + t0, 3),
                            p=x.get("probability")))
    return [w for w in out if norm(w["w"])]


def media_duration(media):
    out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of",
                          "csv=p=0", media], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return None
