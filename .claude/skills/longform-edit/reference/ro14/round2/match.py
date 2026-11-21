"""Match the 10/15 pickup (C1722 lav, left) to the 9/23 film voice (C1708 lav) before the film's own chain:
a smooth linear-phase EQ fitted from the two long-term active-speech spectra (1/3 octave, 80 Hz to 16 kHz), then a gain
so the active-speech RMS matches. Writes pickup/pickup_matched.wav (48k mono, the take 342.20 to 351.20 s) + match.json."""
import wave, numpy as np, json
SR = 48000; FPS = 30000/1001; W = "/Volumes/Extreme/_edit_work/RO-14/round2"
def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
L = load(f"{W}/lav.wav"); P = load(f"{W}/pickup/c1722_300_355.wav")
S = json.load(open(f"{W}/shots.json"))
def out2src(t):
    g = t*FPS; s = next(s for s in S if s['out_f0'] <= g < s['out_f1']); return (s['src_f0']+g-s['out_f0'])/FPS
# film reference: the opening minute's speech around the splice (same take family, same energy)
film = np.concatenate([L[int(out2src(a)*SR):int(out2src(b)*SR)] for a, b in ((5.0, 10.0), (10.3, 16.0), (26.1, 28.9), (29.5, 40.0), (40.0, 52.0))])
A0, A1 = 342.10, 351.70
pk = P[int((A0-300)*SR):int((A1-300)*SR)]
def frames(x, n=int(0.02*SR)):
    fr = x[:len(x)//n*n].reshape(-1, n); return fr, 20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
def active(x):
    fr, db = frames(x); return fr[db > np.percentile(db, 95) - 25].ravel()   # relative: level-independent
def floor(x):
    fr, db = frames(x); return float(np.percentile(db, 5))
def spec(x, N=8192):
    f = np.fft.rfftfreq(N, 1/SR); acc = np.zeros(len(f))
    for i in range(0, len(x)-N, N//2): acc += np.abs(np.fft.rfft(x[i:i+N]*np.hanning(N)))**2
    return f, acc
fa, pa = active(film), active(pk)
f, a = spec(fa); _, b = spec(pa)
cs = 1000*2**(np.arange(-14, 13)/3)                      # 1/3-octave centres ~ 40 Hz .. 16 kHz
cs = cs[(cs >= 80) & (cs <= 16000)]
diff = []
for c in cs:
    m = (f >= c/2**(1/6)) & (f < c*2**(1/6))
    diff.append(10*np.log10(a[m].sum()/a.sum()) - 10*np.log10(b[m].sum()/b.sum()))
def bands(x):
    _, c = spec(x); return np.array([10*np.log10(c[(f >= c0/2**(1/6)) & (f < c0*2**(1/6))].sum()/c.sum()) for c0 in cs])
ref = np.array(diff)
N = 4097; fg = np.fft.rfftfreq(N-1, 1/SR); tot = np.zeros(len(cs)); y = pk.copy()
rms = lambda x: 20*np.log10(np.sqrt((x**2).mean()))
for it in range(4):                                       # fit, measure the residual on the result, refit (content differs)
    res = bands(fa) - bands(active(y)) if it else ref
    tot = np.clip(tot + np.convolve(np.pad(res, 1, mode='edge'), [0.25, 0.5, 0.25], 'valid'), -30, 12)
    g_db = np.interp(np.log10(np.maximum(fg, 1)), np.log10(cs), tot, left=tot[0], right=tot[-1])
    h = np.fft.irfft(10**(g_db/20)); h = np.roll(h, (N-1)//2)*np.hanning(N-1)
    y = np.convolve(pk, h, mode='same').astype(np.float32)
sm = tot
g = rms(fa) - rms(active(y)); y *= 10**(g/20)
pk_peak = 20*np.log10(np.abs(y).max())
o = wave.open(f"{W}/pickup/pickup_matched.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
o.writeframes((np.clip(y, -1, 1)*32767).astype('<i2').tobytes()); o.close()
# check: residual band difference after the match
_, c2 = spec(active(y)); res = []
for c in cs:
    m = (f >= c/2**(1/6)) & (f < c*2**(1/6)); res.append(10*np.log10(a[m].sum()/a.sum()) - 10*np.log10(c2[m].sum()/c2.sum()))
info = dict(take=[A0, A1], eq_db={str(int(c)): round(float(v), 1) for c, v in zip(cs, sm)}, gain_db=round(float(g), 2),
            residual_db={str(int(c)): round(float(v), 1) for c, v in zip(cs, res)}, film_rms=round(float(rms(fa)), 2),
            film_floor_db=round(floor(film), 1), pickup_floor_raw_db=round(floor(pk), 1), pickup_floor_matched_db=round(floor(y), 1),
            peak_dbfs=round(float(pk_peak), 2))
json.dump(info, open(f"{W}/pickup/match.json", "w"), indent=1); print(json.dumps(info))
# round 2 pass 2 (blind Gemini listen on the rendered test: "duller/thinner, energy drops"; measured on that render, film around the
# splice minus pickup: 630 Hz -2.4, 1.6 kHz +2.3, 10 kHz +2.1, active level +0.4 dB): applied with ffmpeg to pickup_matched_v1.wav ->
# pickup_matched.wav: equalizer=f=630:t=q:w=1.0:g=-2.4, equalizer=f=1600:t=q:w=1.0:g=2.3, highshelf=f=8000:g=2.0, volume=-0.5dB
# pass 3 (2026-10-20): volume -0.5 dB dropped (rendered test: pickup -16.9 dB active vs film -16.4 / -15.9). Blind Gemini A/B was found
# unreliable on this question: with the SAME original clip on both sides it still "found" a splice at 0:08, so the join is judged on
# measurement: 1/3-octave distance pickup vs film 2.3 / 3.3 dB, film vs film 4.1 dB. Room-reverb and brighter-EQ variants changed nothing.
