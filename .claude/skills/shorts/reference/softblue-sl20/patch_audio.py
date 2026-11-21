#!/usr/bin/env python3
"""SL-18: apply plans.PATCH (a repair of the film's own join) to build/S/audio.wav and his_mix.wav. usage: patch_audio.py S"""
import json, sys, wave, numpy as np
import plans as P
S = sys.argv[1]; d = f"build/{S}"; T = json.load(open(f"{d}/timeline.json")); SR = 48000
def out_t(film):
    for s in T["seg"]:
        if s["a"] - 1e-6 <= film <= s["b"] + 1e-6: return s["o0"] + film - s["a"]
    raise ValueError(film)
for name in ("audio.wav", "his_mix.wav"):
    w = wave.open(f"{d}/{name}"); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, 2); w.close()
    for p in P.PATCH.get(S, []):
        if "fadein" in p:                               # the incoming side of a join starts with a step: ramp it in from silence over p["fadein"] s
            o = int(round(out_t(p["film"]) * SR)); n = int(round(p["fadein"] * SR)); x[o:o + n] *= np.linspace(0, 1, n)[:, None]
            print(S, name, f"faded in {n} samples at output {o / SR:.3f} s"); continue
        if "duck" in p:                                 # soften a short mouth click: gain p["gain"] over p["duck"] s with p["fade"] s ramps
            o = int(round(out_t(p["film"]) * SR)); n = int(round(p["duck"] * SR)); k = int(p["fade"] * SR)
            g = np.full(n, p["gain"]); g[:k] = np.linspace(1, p["gain"], k); g[n - k:] = np.linspace(p["gain"], 1, k); x[o:o + n] *= g[:, None]
            print(S, name, f"ducked {n} samples at output {o / SR:.3f} s to {p['gain']}"); continue
        if "mute" in p:                                 # fade a stretch of the film's own audio down to silence (no new samples)
            o = int(round(out_t(p["film"]) * SR)); n = int(round(p["mute"] * SR)); k = int(p["fade"] * SR)
            g = np.zeros(n); g[:k] = np.linspace(1, 0, k); x[o:o + n] *= g[:, None]
            print(S, name, f"faded {n} samples at output {o / SR:.3f} s"); continue
        sw = wave.open(p["src"]); assert sw.getframerate() == SR and sw.getnchannels() == 2
        n = int(round(p["dur"] * SR)); sw.setpos(int(round(p["src_t"] * SR))); y = np.frombuffer(sw.readframes(n), "<i2").astype(np.float32).reshape(-1, 2)
        o = int(round(out_t(p["film"]) * SR)); seg = x[o:o + n].copy()
        g = np.ones(n); fi = int(p["fin"] * SR); fo = int(p["fout"] * SR); g[:fi] = np.linspace(0, 1, fi); g[n - fo:] = np.linspace(1, 0, fo)
        x[o:o + n] = y * g[:, None] + seg * (1 - g[:, None])
        print(S, name, f"patched {n} samples at output {o / SR:.3f} s from {p['src']} {p['src_t']}")
    ow = wave.open(f"{d}/{name}", "w"); ow.setnchannels(2); ow.setsampwidth(2); ow.setframerate(SR); ow.writeframes(np.clip(x, -32768, 32767).astype("<i2").tobytes()); ow.close()
