"""Round 6 (Dan: "the mic is blown out when I turn my head down ... fix that audio so that it sounds as normal as possible").
Roll C1576, 65.45 to 69.00 s: he turns his head down onto the lav for the overhead triceps demo. Measured: 7 dB hotter than the
seconds around it in every band, peaks pinned at the recorder's ceiling (-0.4 dBFS). The roll's second channel is digital
silence, so there is no other microphone to patch from. Repair on the lav itself, inside the stretch only:
a spline declip (rebuilds the flattened peaks; ffmpeg's adeclip left them flat), a gentle low shelf (his chest is nearer the capsule), then the level down to the
neighbours' speech level while he is speaking (unity in the pauses), with 50 ms ramps at both ends. No gate, no denoise, no compressor.
Writes lav.round6.wav = lav.wav with ONLY those samples replaced (build.py reads it when RO06_LAV is set). usage: audiofix6.py"""
import wave, json, subprocess, numpy as np
W = "/Volumes/Extreme/_edit_work/ro06"; SR = 48000; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
g0 = json.load(open(f"{W}/rolls.json"))["C1576"]["f0"]
A, Bq = 65.45, 69.00; PAD = 1.0; RAMP = 0.05
def rd(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).copy()
L = rd(f"{W}/lav.wav"); base = int(round(g0/FPS*SR))
i0 = base + int((A - PAD)*SR); i1 = base + int((Bq + PAD)*SR); seg = L[i0:i1]
o = wave.open(f"{W}/round6/audio/seg_in.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(seg.tobytes()); o.close()
def voiced_rms(x):
    x = x.astype(np.float64)/(32768 if x.dtype == np.int16 else 1); n = int(0.05*SR); r = np.array([np.sqrt((x[i:i+n]**2).mean()) for i in range(0, len(x)-n, n)]); return 20*np.log10(np.sqrt((r[r > 10**(-30/20)]**2).mean()))
ref = np.concatenate([L[base + int(52*SR):base + int(63.5*SR)], L[base + int(70.5*SR):base + int(82*SR)]])
def declip(x):
    """ffmpeg's adeclip left these peaks flat (checked on the waveform: runs of up to 24 samples pinned at +0.955 / -0.944). Rebuild them: every sample
    within 1.5 % of either ceiling (and one neighbour each side) is treated as lost and replaced by a cubic spline through the samples that survived;
    a rebuilt peak is never lower than the ceiling it was cut at, and never more than 2.2x it."""
    from scipy.interpolate import CubicSpline
    hi, lo = x.max(), x.min(); bad = (x >= hi*0.985) | (x <= lo*0.985); bad = bad | np.roll(bad, 1) | np.roll(bad, -1)
    idx = np.arange(len(x)); y = x.copy(); y[bad] = CubicSpline(idx[~bad], x[~bad])(idx[bad])
    up = bad & (x > 0); dn = bad & (x < 0)
    y[up] = np.clip(y[up], np.minimum(x[up], hi*0.985), 2.2*hi); y[dn] = np.clip(y[dn], 2.2*lo, np.maximum(x[dn], lo*0.985))
    return y, int(bad.sum())
x0 = seg.astype(np.float64)/32768; dc, nbad = declip(x0)
import scipy.signal as sg
bz, az = sg.butter(1, 300/(SR/2)); low = sg.filtfilt(bz, az, dc); d = dc - low*(1 - 10**(-2/20))      # a 2 dB low shelf at 300 Hz, zero phase (his chest is nearer the capsule)
a, b = int(PAD*SR), len(seg) - int(PAD*SR)
gain_db = voiced_rms(ref) - voiced_rms(d[a:b]) - 1.5; gain_db = float(np.clip(gain_db, -10.0, 0.0))   # 1.5 dB under the plain match: after the voice chain's EQ the stretch still read 2.6 dB hot against its neighbours
m = np.zeros(len(seg)); r = int(RAMP*SR); m[a:b] = 1; m[a-r:a] = np.linspace(0, 1, r); m[b:b+r] = np.linspace(1, 0, r)
# The pool and insect noise did not get louder when he turned his head, only his voice did. So the gain comes down with the VOICE and returns to
# unity in the pauses inside the stretch (first listen: with one flat gain the background dropped 6 dB for those seconds and came back).
# va = how much voice is present: the level over 20 ms, 0 below -40 dBFS, 1 above -28, held up 120 ms so the dips between syllables do not open it.
n20 = int(0.02*SR); env = np.sqrt(np.convolve(d*d, np.ones(n20)/n20, "same")) ; edb = 20*np.log10(env + 1e-9)
va = np.clip((edb + 40)/12.0, 0, 1); hold = int(0.12*SR)
from scipy.ndimage import maximum_filter1d, uniform_filter1d
va = uniform_filter1d(maximum_filter1d(va, hold), int(0.06*SR))
gl = 10**(gain_db*va/20.0)
fixed = d*gl; x = seg.astype(np.float64)/32768
out = np.where(m > 0, x*(1-m) + fixed*m, x)
res = np.clip(np.round(out*32768), -32768, 32767).astype(np.int16)
changed = np.nonzero(res != seg)[0]; assert changed.min() >= a - r and changed.max() < b + r
N = L.copy(); N[i0:i1] = res
assert (N[:i0 + a - r] == L[:i0 + a - r]).all() and (N[i0 + b + r:] == L[i0 + b + r:]).all()
o = wave.open(f"{W}/lav.round6.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(N.tobytes()); o.close()
o = wave.open(f"{W}/round6/audio/seg_out.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(res.tobytes()); o.close()
rep = dict(roll="C1576", local_s=[A, Bq], global_samples=[int(i0 + a - r), int(i0 + b + r)], gain_db=round(gain_db, 2), neighbours_voiced_rms_db=round(voiced_rms(ref), 1),
           before_voiced_rms_db=round(voiced_rms(seg[a:b]), 1), after_voiced_rms_db=round(voiced_rms(res[a:b]), 1),
           before_peak_db=round(20*np.log10(np.abs(seg[a:b]).max()/32768), 2), after_peak_db=round(20*np.log10(np.abs(res[a:b]).max()/32768), 2),
           declip_peak_db=round(20*np.log10(np.abs(d[a:b]).max()), 2), samples_changed=int(len(changed)), samples_total=int(len(L)),
           samples_rebuilt=nbad, chain="cubic-spline declip of every sample at the ceiling, zero-phase 2 dB low shelf at 300 Hz, gain down with the voice only (unity in the pauses, so the background noise stays level), 50 ms ramps at both ends")
json.dump(rep, open(f"{W}/round6/audio/audiofix.json", "w"), indent=1); print(json.dumps(rep, indent=1))
