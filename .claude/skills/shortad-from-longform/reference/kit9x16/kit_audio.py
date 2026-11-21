#!/usr/bin/env python3
"""FROM-RAW AUDIO for a kit build: the lav track of each roll (pick_lav.py decides which track, per file),
conformed to the audio EDL, through the ONE shared voice chain (EQ fitted to the pinned reference), with a
music bed at his level and his ~22 ms tick at graphic ENTRANCES only (never on a flash, never on a
footage cut) -- then the shared finish. The gate (audio_gate.py) judges the delivered file, not this.

  python3 kit_audio.py --build DIR --raw ROLL [--rolls rolls.json] --edl edl_final.json --bed music.mp3
                       [--bed-db -19] [--tick his_tick.wav] [--tick-db -12]

Writes voice_raw.wav (the conformed lav, untreated), audio_final.wav (the finished mix) and the voice
chain's sidecars beside it. Length-locked to the picture plan (beats.json dur).
"""
import argparse
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
SHARED_AUDIO = os.path.join(REPO, ".claude/skills/_shared/audio")
sys.path.insert(0, SHARED_AUDIO)
FPS = 30000 / 1001
SR = 48000


def load_edl(path):
    E = json.load(open(path))
    out = []
    for i, s in enumerate(E):
        if "cut_in" in s:
            out.append(dict(i=i, cut_in=float(s["cut_in"]), cut_out=float(s["cut_out"]), src_in=float(s["src_in"]), roll=s.get("roll")))
        else:
            a, b = s["out_seconds"]
            out.append(dict(i=i, cut_in=float(a), cut_out=float(b), src_in=float(s["src_in"]), roll=s.get("roll")))
    return out


def pcm(src, ss, dur, amap, af):
    cmd = [FF, "-v", "error", "-ss", f"{ss:.6f}", "-t", f"{dur:.6f}", "-i", src, "-map", amap, "-af", af,
           "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)


def write_wav(path, x):
    w = wave.open(path, "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    w.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--rolls")
    ap.add_argument("--edl", required=True)
    ap.add_argument("--bed")
    ap.add_argument("--bed-db", type=float, default=-38.0)   # HIS bed level, measured (kit9x16 from-raw Ad 1, 2026-09-17): the gate's floor row wants the bed 28-35 dB under the voice like his; -19 read 14/23/16, -30 read 20/28/22, the treated voice alone 42/48/38 -- the bed is the whole floor, and -38 lands on his 28/35/28
    ap.add_argument("--tick")
    ap.add_argument("--tick-db", type=float, default=-12.0)
    a = ap.parse_args()
    os.chdir(a.build)
    import common as AC                                  # _shared/audio/common.py: load_source reads pick_lav's JSON
    rolls = json.load(open(a.rolls)) if a.rolls else {}
    E = load_edl(a.edl)
    J = json.load(open("beats.json"))
    total = int(round(float(J["dur"]) * SR))
    # 1. the conformed lav: per roll, pick_lav's JSON decides the track; refuse a roll without one
    voice = np.zeros(total, np.float32)
    n_prev = 0
    for s in E:
        src = rolls.get(s["roll"], a.raw) if s.get("roll") else a.raw
        L = AC.load_source(src)
        if not L:
            raise SystemExit(f"no audio_source.json beside {src}: run _shared/audio/pick_lav.py on it first")
        n0 = int(round(s["cut_in"] * SR))
        n1 = int(round(s["cut_out"] * SR))
        x = np.array(pcm(src, s["src_in"], (n1 - n0) / SR + 0.05, L["map"], L["filter"])[: n1 - n0])   # a copy: pcm() hands back a read-only frombuffer view, and the join ramp writes into it
        if len(x) < n1 - n0:
            x = np.pad(x, (0, n1 - n0 - len(x)))
        # 4 ms raised-cosine joins so a trim never clicks
        k = int(0.004 * SR)
        if n0 > 0 and k < len(x):
            r = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
            x[:k] *= r
            voice[n0 - k:n0] *= r[::-1] if n0 - k >= 0 else 1
        voice[n0:n1] = x
        n_prev = n1
    write_wav("voice_raw.wav", voice)
    # 2. ticks at graphic ENTRANCES only (lower thirds, CTAs, plates and cards opening) -- his count, his rule
    extra = None
    if a.tick:
        sys.path.insert(0, os.getcwd())
        import beats as B
        tl, ov = B.timeline()
        ents = [o["t0"] for o in ov if o["kind"] in ("lt", "cta")] + \
               [b["t0"] for i, b in enumerate(tl) if b["kind"] in ("window", "title", "stmt", "card", "winmedia") and (i == 0 or tl[i - 1]["kind"] != b["kind"])]
        flashes = [x + 0.11 for x, _ in B.FLASHES]
        ents = [t for t in ents if not any(abs(t - f) < 0.3 for f in flashes)]     # never on a flash
        t = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", a.tick, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                         capture_output=True).stdout, np.float32)
        g = 10 ** (a.tick_db / 20)
        sfx = np.zeros(total, np.float32)
        for e in ents:
            n0 = int(e * SR)
            m = min(len(t), total - n0)
            if m > 0:
                sfx[n0:n0 + m] += t[:m] * g
        write_wav("sfx.wav", sfx)
        extra = "sfx.wav"
        json.dump(dict(entrances=[round(x, 3) for x in ents], count=len(ents), per_s=round(float(J["dur"]) / max(1, len(ents)), 1)),
                  open("sfx_plan.json", "w"), indent=1)
        print(f"{len(ents)} ticks, one per {float(J['dur']) / max(1, len(ents)):.1f} s (his: one per ~11 s)")
    # 3. the one voice chain
    cmd = [sys.executable, os.path.join(SHARED_AUDIO, "voice_chain.py"), "--in", "voice_raw.wav", "--out", "audio_final.wav",
           "--frame-lock", "picture.mp4" if os.path.exists("picture.mp4") else "base.mp4"]
    if a.bed:
        cmd += ["--bed", a.bed, "--bed-db", str(a.bed_db)]
    if extra:
        cmd += ["--extra", extra]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.run(cmd, check=True)
    print("audio_final.wav written; gate it on the delivered file with _shared/audio/audio_gate.py")


if __name__ == "__main__":
    sys.exit(main())
