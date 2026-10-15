"""Print a 20 ms lav level strip over [a,b]: one char per 20 ms (' ' < -50 dB, '.' < -40, ':' < -30, '#' louder), with a time ruler."""
import sys, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/RO-14/round1"; SR = 48000
wv = wave.open(f"{W}/lav.wav"); A = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
def strip(a, b):
    out = []
    for t in np.arange(a, b, 0.02):
        x = A[int(t*SR):int((t+0.02)*SR)]; d = 20*np.log10(np.sqrt(np.mean(x*x))+1e-9)
        out.append(" " if d < -50 else "." if d < -40 else ":" if d < -30 else "#")
    s = "".join(out)
    for k in range(0, len(s), 100):
        print(f"{a+k*0.02:8.2f} |{s[k:k+100]}|")
for arg in sys.argv[1:]:
    a, b = map(float, arg.split("-")); print("==", arg); strip(a, b)
