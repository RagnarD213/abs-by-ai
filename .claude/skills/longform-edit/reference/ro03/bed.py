"""RO-03 music bed: the cleared trip-hop track (Pixabay 10091, already live under the V4 workout section and V5), low
under Dan's voice and up in the three holds (Muhammad's bed swells in his sets and drops under speech). bed_full.wav is
built once on the film timeline; build.py slices it per render range and hands it to the shared voice chain, which ducks
it under the voice."""
import json, os, subprocess, sys, wave
import numpy as np
W = "/Volumes/Extreme/_edit_work/ro03"; SR = 48000; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
TRACK = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/music beds/rhythmical-melodic-syncopation-triphop-130bpm-pixabay-10091.mp3"
BED_DB = float(os.environ.get("RO03_BED_DB", "-16.5"))      # level under his voice, before the chain's own ducking
SWELL = float(os.environ.get("RO03_SWELL", "25.5"))         # dB up in the holds
OFFSET = float(os.environ.get("RO03_BED_OFFSET", "0"))
def build():
    S = json.load(open(f"{W}/shots.json")); M = json.load(open(f"{W}/marks.json")); total = S[-1]["out_f1"]/FPS; N = int(round(total*SR))
    b = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{OFFSET}", "-i", TRACK, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    m = np.frombuffer(b, np.float32).reshape(-1, 2); assert len(m) >= N, "track shorter than the film: never loop without a crossfade"
    bed = m[:N].copy(); env = np.ones(N, np.float32); up = 10**(SWELL/20)
    for f0, beep in zip(M["flashes"], M["beeps"]):                      # up from the cut into the set to just after the beep
        i, j = int(f0/FPS*SR), int((beep+0.5)*SR); r0, r1 = int(0.5*SR), int(1.2*SR)
        env[i:j] = up; env[i:i+r0] = np.linspace(1, up, r0); env[j:j+r1] = np.maximum(env[j:j+r1], np.linspace(up, 1, r1))
    bed *= env[:, None]; bed *= 10**(-SWELL/20)                         # headroom: the swell tops out at the track's own level
    fi = int(0.8*SR); bed[:fi] *= np.linspace(0, 1, fi)[:, None]; fo = int(2.5*SR); bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
    w = wave.open(f"{W}/bed_full.wav", "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(bed, -1, 1)*32767).astype("<i2").tobytes()); w.close(); print("bed", round(total, 2), "s, swell", SWELL, "dB")
def slice_bed(t0, dur, out):
    if not os.path.exists(f"{W}/bed_full.wav"): build()
    w = wave.open(f"{W}/bed_full.wav"); w.setpos(int(round(t0*SR))); x = w.readframes(int(round(dur*SR))); w.close()
    o = wave.open(out, "w"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes(x); o.close()
if __name__ == "__main__": build()
