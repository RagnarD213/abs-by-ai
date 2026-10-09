"""Round 5 music bed (Dan: "add a quiet bed"): Pixabay `acoustic_bg` (Pixabay Content Licence, no attribution), the bed of
the approved RO-05 round 4 and RO-12 films. Same builder as RO-12 (seamless equal-power loop over the track body, 10 dB of
headroom, 1 s in, 2.5 s out). The chain ducks it under the voice (voice_chain --bed). usage: bed.py TOTAL_SECONDS OUT.wav"""
import sys, subprocess, wave, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; SR = 48000
TRACK = "/Volumes/Extreme/_edit_work/abwheel/r2/music/acoustic_bg.mp3"; BED_PRE = -10.0; BED_OFFSET = 87.0
def build_bed(total_s, out):
    b = subprocess.run([FF, "-nostdin", "-v", "error", "-i", TRACK, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    m = np.frombuffer(b, np.float32).reshape(-1, 2)[int(0.5*SR):int(135.5*SR)]
    L = len(m); xf = 3*SR; th = np.linspace(0, np.pi/2, xf)[:, None]; fin, fout = np.sin(th), np.cos(th)
    off = int(BED_OFFSET*SR); N = int(round(total_s*SR)); M = N + off
    bed = np.zeros((M, 2), np.float32); pos = 0
    while pos < M:
        seg = m.copy()
        if pos > 0: seg[:xf] *= fin
        seg[-xf:] *= fout
        e = min(M, pos + L); bed[pos:e] += seg[:e-pos]; pos += L - xf
    bed = bed[off:off + N].copy(); bed *= 10**(BED_PRE/20)
    fi = int(1.0*SR); bed[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(2.5*SR); bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
    assert np.abs(bed).max() < 1.0
    w = wave.open(out, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(bed, -1, 1)*32767).astype("<i2").tobytes()); w.close()
if __name__ == "__main__": build_bed(float(sys.argv[1]), sys.argv[2]); print("bed", sys.argv[2])
