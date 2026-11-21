#!/usr/bin/env python3
"""Pull the lav per C1663's own audio_source.json, write the working wavs and the 5 ms envelope."""
import json, subprocess, os, sys, wave
import numpy as np
P = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
ROLL = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1663.MP4"
SRC = json.load(open(ROLL + ".audio_source.json"))
assert SRC["verdict"] == "dual-mono", SRC["verdict"]
MAP, FILT = SRC["map"], SRC["filter"]
print("lav pull:", MAP, FILT)
for out, sr in (("lav.wav", 48000), ("lav16.wav", 16000)):
    subprocess.run([f"{P}/ffmpeg", "-nostdin", "-v", "error", "-y", "-i", ROLL,
                    "-map", MAP, "-af", FILT, "-ar", str(sr), "-ac", "1",
                    "-c:a", "pcm_s16le", out], check=True)
    print("wrote", out)
w = wave.open("lav.wav"); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768.0
HOP = 0.005; N = int(HOP*sr); n = len(a)//N
db = 20*np.log10(np.sqrt((a[:n*N].reshape(n, N)**2).mean(1))+1e-12)
json.dump({"hop": HOP, "sr": sr, "db": [round(float(x), 2) for x in db]}, open("env.json", "w"))
print(f"env.json {n} frames, {n*HOP:.1f}s  floor p5={np.percentile(db,5):.1f} dB  p95={np.percentile(db,95):.1f} dB")
