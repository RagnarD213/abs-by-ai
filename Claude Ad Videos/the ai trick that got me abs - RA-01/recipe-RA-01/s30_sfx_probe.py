#!/usr/bin/env python3
"""Plan section 6 asks for transition SFX from `_shared/sfxlib.py` on card ins. This build has
none. Before recording that as a deviation, MEASURE what adding them would do to the one gate row
that is already failing (`artifacts`, spectral flux).

Builds the SFX bed the plan describes -- a whoosh on each full card in, a pop on each of the three
rapid after-photo ins -- runs it through the SAME voice chain as an `--extra` track, and measures
flux over the gate's own window. Writes sfx_probe.json. Changes no delivered file.
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
SH = f"{ROOT}/.claude/skills/_shared/audio"
FF = f"{ROOT}/Media/video_edit/bin/ffmpeg"
sys.path.insert(0, SH)
sys.path.insert(0, f"{ROOT}/.claude/skills/_shared")
import common as C          # noqa: E402
import sfxlib               # noqa: E402

W = "/Volumes/Extreme/_edit_work/ra01"
TMP = f"{W}/fluxdiag"
SR = C.SR
os.makedirs(TMP, exist_ok=True)

TL = json.load(open(f"{W}/timeline_9x16.json"))
cards = [i for i in TL["items"] if i["kind"] == "card"]
# the three rapid after photographs get a pop; every other card in gets a whoosh
POP = {"after_1", "after_2", "after_3"}
dur = TL["items"][-1]["b"]
track = np.zeros(int(dur * SR) + SR, np.float32)
placed = []
for c in cards:
    if c["a"] <= 0.001:                     # the hook card is frame 0; nothing to transition from
        continue
    y = sfxlib.pop(freq=980) * 0.35 if c["name"] in POP else sfxlib.whoosh() * 0.30
    i0 = int(c["a"] * SR)
    track[i0:i0 + len(y)] += y.astype(np.float32)
    placed.append({"card": c["name"], "t": round(c["a"], 3),
                   "sfx": "pop" if c["name"] in POP else "whoosh"})

sfx_wav = f"{TMP}/sfx_track.wav"
wv = wave.open(sfx_wav, "w"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes()); wv.close()
print(f"{len(placed)} one-shot(s): " + ", ".join(f"{p['card']}@{p['t']}s {p['sfx']}" for p in placed))

mix_sfx = f"{TMP}/mix_with_sfx.wav"
subprocess.run([sys.executable, f"{SH}/voice_chain.py", "--in", f"{W}/cut_audio.wav",
                "--out", mix_sfx, "--bed", "/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3",
                "--bed-db", "-32", "--extra", sfx_wav, "--work", f"{TMP}/work_sfx"], check=True)

STAMP = json.load(open(f"{W}/master_9x16.mp4.audio_gate.json"))
W0, W1 = STAMP["window"]
BOUND = STAMP["reference"] and None
ref_flux = [r for r in STAMP["rows"] if r["key"] == "artifacts"][0]["text"]


def art(path):
    out = f"{TMP}/_p_{os.path.basename(path)}"
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-map", "0:a:0", "-ac", "1",
                    "-ar", str(SR), "-c:a", "pcm_s16le", out], check=True)
    w = wave.open(out)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    w.close()
    return C.artifacts(x[int(W0 * SR):int(W1 * SR)])


a_now = art(f"{W}/mix.wav")
a_sfx = art(mix_sfx)
d = json.load(open(f"{W}/flux_diagnosis.json"))
bound = d["bound_flux"]
print(f"\nbound (gate stamp): {ref_flux}")
print(f"  mix as delivered (no SFX)  flux {a_now['flux']:.4f}  swirl {a_now['swirl']:.4f}")
print(f"  same mix WITH the SFX      flux {a_sfx['flux']:.4f}  swirl {a_sfx['swirl']:.4f}")
print(f"  delta                      flux {a_sfx['flux'] - a_now['flux']:+.4f}")

json.dump({"placed": placed, "window": [W0, W1], "bound_flux_local_remeasure": bound,
           "gate_row_text": ref_flux,
           "mix_no_sfx": a_now, "mix_with_sfx": a_sfx,
           "delta_flux": round(a_sfx["flux"] - a_now["flux"], 5),
           "delta_swirl": round(a_sfx["swirl"] - a_now["swirl"], 5)},
          open(f"{W}/sfx_probe.json", "w"), indent=1)
print(f"\nwrote {W}/sfx_probe.json")
