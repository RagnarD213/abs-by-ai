#!/usr/bin/env python3
"""THE REFERENCE, PINNED BY FINGERPRINT.

Muhammad's `this picture got me abs | muhammad | 16x9.mp4` is what Dan names every time he
rejects audio. On 2026-09-02 he moved it into a subfolder and every gate that hardcoded the
path crashed with "No such file" -- and the older reference two chains used (`Daniel HQ
Fitness AD Video v3 HD.mp4`) is not on disk anywhere. So the reference lives HERE, as a mono
48 kHz FLAC of his audio plus a committed fingerprint (sha256 of the FLAC and the measured
bands / floor / EDT / LUFS), and `resolve()` refuses to run on anything that does not match.

  python3 reference.py pin [<path to the .mp4>]   # (re)build the FLAC + fingerprint
  python3 reference.py                            # resolve + print the fingerprint
"""
import glob, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

RDIR = os.path.join(C.HERE, "reference")
FLAC = os.path.join(RDIR, "muhammad_16x9_voice.flac")
META = os.path.join(RDIR, "reference.json")
NAME = "this picture got me abs | muhammad | 16x9.mp4"
WINDOW = (20.0, 120.0)          # the gate's window on the reference, always


def find_mp4():
    hits = glob.glob(os.path.join(C.REPO, "Muhammad Ad Videos", "**", NAME), recursive=True)
    return hits[0] if hits else None


def measure(path, amap=None):
    """the fingerprint: everything the gate compares against, on the 20-140 s window."""
    x = C.pcm(path, ss=WINDOW[0], dur=WINDOW[1], amap=amap)
    bands, floor, dry, spread = C.analyse(x)
    I, TP, LRA = C.ebur(path, amap=amap)
    return dict(bands=[round(float(b), 3) for b in bands], floor=[round(float(v), 3) for v in floor],
                dryness=round(dry, 3), spread=round(spread, 3), edt_ms=round(C.edt(x), 2),
                comb_ripple=round(C.comb_ripple(x), 3), lufs=round(I, 2), tp=round(TP, 2), lra=round(LRA, 2))


def pin(src=None):
    src = src or find_mp4()
    if not src: raise SystemExit(f"cannot find '{NAME}' under Muhammad Ad Videos/ -- pass the path")
    os.makedirs(RDIR, exist_ok=True)
    subprocess.run([C.FF, "-nostdin", "-y", "-v", "error", "-i", src, "-map", "0:a:0", "-ac", "1",
                    "-ar", str(C.SR), "-c:a", "flac", "-compression_level", "8", FLAC], check=True)
    m = measure(FLAC)
    m.update(name=NAME, sha256=common_sha(FLAC), duration=round(C.duration(FLAC), 3), source=src,
             window=list(WINDOW), version=C.STAMP_VERSION)
    json.dump(m, open(META, "w"), indent=1)
    print(f"pinned {FLAC}\n  sha256 {m['sha256'][:16]}…  {m['duration']} s  I {m['lufs']} LUFS  "
          f"EDT {m['edt_ms']} ms  dryness {m['dryness']} dB  spread {m['spread']} dB")
    return m


def common_sha(p): return C.sha256(p)


def resolve(strict=True):
    """returns (path to the mono reference audio, fingerprint dict). Regenerates the FLAC from
    the .mp4 if it is missing; refuses if what it finds does not match the pinned fingerprint."""
    if not os.path.exists(META):
        raise SystemExit("reference/reference.json missing -- run `python3 reference.py pin`")
    meta = json.load(open(META))
    if os.path.exists(FLAC) and C.sha256(FLAC) == meta["sha256"]:
        return FLAC, meta
    src = find_mp4()
    if not src: raise SystemExit("reference FLAC missing/changed and the .mp4 is not on disk")
    tmp = FLAC + ".regen.flac"
    subprocess.run([C.FF, "-nostdin", "-y", "-v", "error", "-i", src, "-map", "0:a:0", "-ac", "1",
                    "-ar", str(C.SR), "-c:a", "flac", "-compression_level", "8", tmp], check=True)
    m = measure(tmp)
    drift = max(abs(a - b) for a, b in zip(m["bands"], meta["bands"]))
    ok = drift < 0.3 and abs(m["edt_ms"] - meta["edt_ms"]) < 3 and abs(m["lufs"] - meta["lufs"]) < 0.3
    if not ok:
        os.remove(tmp)
        raise SystemExit(f"the .mp4 on disk does NOT match the pinned reference (band drift {drift:.2f} dB, "
                         f"EDT {m['edt_ms']} vs {meta['edt_ms']}) -- refusing to gate against it")
    os.replace(tmp, FLAC)
    print(f"reference FLAC regenerated from {src} (fingerprint matches)")
    return FLAC, meta


if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "pin": pin(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        p, m = resolve(); print(p); print(json.dumps({k: v for k, v in m.items() if k != "bands"}, indent=1))
