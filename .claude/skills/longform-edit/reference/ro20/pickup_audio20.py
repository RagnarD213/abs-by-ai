#!/usr/bin/env python3
"""RO-20 round 3: Dan's re-recorded audio pickups (Yeti, rec_mic) cut to the chosen takes and matched to the film voice.
For each pickup: the take(s) with a 0.15 s lead, 70 Hz high-pass, a smoothed long-term spectrum match to the film's treated voice
(third octave, boosts capped at +8 dB, cuts at -12 dB), a gentle compressor only as far as the film's own speech spread, level matched to the film's
active speech level, peaks held under -2 dBFS. Writes round3/pickups/P#.voice.wav (48 k mono) + words_P#.json (for pickups20.py)
and prints the before/after numbers. usage: pickup_audio20.py"""
import json, wave, os, numpy as np
from scipy.signal import welch, firwin2, fftconvolve, butter, sosfiltfilt
W = "/Volumes/Extreme/_edit_work/ro20"; SR = 48000
D = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/ro20-pickups/rerecord_20261012"
OUT = f"{W}/round3/pickups"
T = json.load(open(f"{D}/pickups_rerecord.transcript.json"))["words"]
# last clean take of each pickup (2026-10-13 recording). P3: take 2's first line reads "That's worth a cut" to Whisper twice, so the
# first sentence is take 1's and the rest is take 2 (the join sits in the pause before "Now you have the money").
TAKES = {"P1": [(17.96, 29.34)], "P2": [(46.92, 60.60)], "P3": [(67.98, 68.95), (92.94, 111.02)], "P4": [(136.14, 153.18)]}
TAIL = {"P1": 0.45, "P2": 0.45, "P3": 5.4, "P4": 0.45}          # P3 ends video 2: room for YouTube's end screen
FIXW = {"bawler.": "baller.", "bawler": "baller", "absbyai.com.": "AbsByAI.com."}
def rd(p, a=None, b=None):
    w = wave.open(p); assert w.getframerate() == SR and w.getsampwidth() == 2; c = w.getnchannels()
    if a is not None: w.setpos(int(a*SR))
    n = w.getnframes() if a is None else int((b-a)*SR)
    return np.frombuffer(w.readframes(n), np.int16).reshape(-1, c)[:, 0].astype(np.float64)/32768      # the film voice is the same voice on both channels
def wr(p, x):
    o = wave.open(p, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(x, -1, 1)*32767).astype("<i2").tobytes()); o.close()
def frames_db(x, n=480):
    f = x[:len(x)//n*n].reshape(-1, n); return 20*np.log10(np.sqrt((f**2).mean(1)) + 1e-9)
def active(x):
    r = frames_db(x); thr = np.percentile(r, 95) - 25; m = np.repeat(r > thr, 480); return x[:len(m)][m]
def act_db(x): a = active(x); return 10*np.log10(np.mean(a**2))
def spread(x):
    r = frames_db(x, 4800); r = r[r > np.percentile(r, 95) - 25]; return np.percentile(r, 90) - np.percentile(r, 10)
BANDS = 1000*2.0**(np.arange(-11, 12)/3.0)                         # 79 Hz .. 12.7 kHz, third octaves
def ltas(x):
    f, p = welch(active(x), SR, nperseg=8192)
    return np.array([10*np.log10(p[(f >= c/2**(1/6)) & (f < c*2**(1/6))].mean()) for c in BANDS])
def match_fir(g_db):
    g = np.convolve(np.pad(g_db, 1, mode="edge"), [0.25, 0.5, 0.25], "valid"); g = np.clip(g, -12, BOOST)                         # cuts may go deeper than boosts (the Yeti carries far more below 110 Hz and above 10 kHz than the treated lav)
    g = g - np.where(BANDS < 260, LOWCUT, 0.0)                         # pass 2: the listener still heard the pickup as boomier. Final: room -16 dB, boost cap 0.75, 1 dB off below 260 Hz, 1 dB under the film level, film room tone under it. More room (-10) and less bass (2.5) did not change the listener's verdict, so the setting stays near the best of the five-way comparison
    fr = np.concatenate([[0, 60], BANDS, [16000, SR/2]]); gn = np.concatenate([[g[0], g[0]], g, [g[-1], g[-1]]])
    return firwin2(4097, fr, 10**(gn/20), fs=SR), g
BOOST = float(os.environ.get("BOOST", "0.75"))     # 2026-10-13: +1.5 dB boost cap and room at -16 dB sat between the two best of five in a blind listen (cuts only with -18: "slightly thinner"; +3 with -14: "slightly boomier")
def decay(x, lag=0.064):
    """median level drop (dB) from the last loud 8 ms frame of a word to `lag` later, at word ends followed by a pause"""
    r = frames_db(x, 384); top = np.percentile(r, 95); k = int(round(lag/0.008)); out = []
    for i in range(2, len(r) - 40):
        if r[i] > top - 14 and r[i+1] < r[i] and max(r[i+12:i+30]) < top - 30 and r[i-1] > top - 18: out.append(r[i] - r[i+k])
    return float(np.median(out)) if out else float("nan"), len(out)
def room_ir(rt60=0.32, pre=0.008, seed=7):
    rng = np.random.default_rng(seed); n = int(0.5*SR); t = np.arange(n)/SR; ir = rng.standard_normal(n)*np.exp(-6.9*t/rt60)
    ir = sosfiltfilt(butter(2, [250, 5000], "bp", fs=SR, output="sos"), ir); ir /= np.sqrt((ir**2).sum())
    return np.concatenate([np.zeros(int(pre*SR)), ir])
def add_room(x, wet_db, ir=None):
    ir = room_ir() if ir is None else ir; w = fftconvolve(x, ir)[:len(x)]; return x + w*10**(wet_db/20)
LOWCUT = float(os.environ.get("LOWCUT", "1.0")); TRIM = float(os.environ.get("TRIM", "-1.0"))
def film_tone(film, n):
    """the kitchen's own room tone (the quietest 0.4 s of the film voice reference), looped with crossfades to n samples, at its own level"""
    k = int(0.4*SR); r = np.array([np.sqrt((film[i:i+k]**2).mean()) for i in range(0, len(film)-k, 2400)]); i = int(np.argmin(r))*2400; t = film[i:i+k].copy()
    x = int(0.05*SR); out = np.zeros(n + k); pos = 0; w = np.ones(k); w[:x] = np.linspace(0, 1, x); w[-x:] = np.linspace(1, 0, x)
    while pos < n: out[pos:pos+k] += (t if (pos//(k-x)) % 2 == 0 else t[::-1])*w; pos += k - x
    return out[:n], 20*np.log10(r.min() + 1e-9)
def compress(x, thr_db, ratio, att=0.005, rel=0.12):
    e = np.abs(x); env = np.zeros_like(e); a, r = np.exp(-1/(att*SR)), np.exp(-1/(rel*SR)); v = 0.0
    for i in range(len(e)):
        c = a if e[i] > v else r; v = c*v + (1-c)*e[i]; env[i] = v
    lv = 20*np.log10(env + 1e-9); over = np.maximum(lv - thr_db, 0); return x*10**(-(over*(1-1/ratio))/20)
def limit(x, ceil_db=-2.0):
    c = 10**(ceil_db/20); n = 96; pk = np.abs(x); mx = np.array([pk[max(0, i-n):i+n].max() for i in range(0, len(x), 48)]); mx = np.repeat(mx, 48)[:len(x)]
    g = np.minimum(1.0, c/np.maximum(mx, 1e-9)); g = np.convolve(g, np.ones(96)/96, "same"); return np.clip(x*np.minimum(g, 1.0), -c, c)
if __name__ == "__main__":
    film = np.concatenate([rd(f"{W}/voice/film_voice.wav", a, b) for a, b in ((840, 900), (905, 965), (1380, 1420), (1421, 1481))])
    F_lt, F_act, F_sp = ltas(film), act_db(film), spread(film)
    F_crest = 20*np.log10(np.percentile(np.abs(active(film)), 99.9)) - F_act
    print(f"film voice: active {F_act:.1f} dB, spread {F_sp:.1f} dB, crest(p99.9) {F_crest:.1f} dB, peak {20*np.log10(np.abs(film).max()):.1f}")
    raw = rd(f"{D}/pickups_rerecord_48k_mono.wav"); sos = butter(2, 70, "hp", fs=SR, output="sos")
    allsp = np.concatenate([raw[int(a*SR):int(b*SR)] for r in TAKES.values() for a, b in r]); allsp = sosfiltfilt(sos, allsp)
    Fd, nF = decay(film); cand = [(w, decay(add_room(allsp, w))[0]) for w in (-30, -24, -20, -17, -14, -11, -8)]
    WET = float(os.environ.get("WET", "-16"))            # chosen by ear (blind listen), the decay metric below does not separate the options
    print(f"word-end decay over 64 ms: film {Fd:.1f} dB ({nF} word ends), pickup dry {decay(allsp)[0]:.1f}; with room at", " ".join(f"{w}:{d:.1f}" for w, d in cand), "-> room at", WET, "dB")
    allsp = add_room(allsp, WET)
    h, g = match_fir(F_lt - ltas(allsp) - (F_act - act_db(allsp)))        # shape only: the level difference is taken out first
    print("match EQ per third octave (dB, 79 Hz to 12.7 kHz):", " ".join(f"{v:+.1f}" for v in g))
    rep = {}
    for pid, rng in TAKES.items():
        pieces, words, at = [], [], 0.0
        for k, (a, b) in enumerate(rng):
            ws = [w for w in T if a - 0.01 <= w["t0"] < b]
            lead = 0.15 if k == 0 else (ws[0]["t0"] - prev_end)/2 if False else 0.10
            end = ws[-1]["t1"] + (TAIL[pid] if k == len(rng)-1 else 0.12)
            s0 = a - lead; x = raw[int(s0*SR):int(min(end, s0 + 600)*SR)].copy()
            if len(x) < int((end - s0)*SR): x = np.concatenate([x, np.zeros(int((end - s0)*SR) - len(x))])
            n = int(0.010*SR); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
            if k == len(rng)-1 and TAIL[pid] > 1:                          # long tail: only his room after the last word, faded out over the first second
                i0 = int((ws[-1]["t1"] + 0.25 - s0)*SR); f = int(1.0*SR); x[i0:i0+f] *= np.linspace(1, 0, f); x[i0+f:] = 0
            for w in ws: words.append(dict(w=FIXW.get(w["w"], w["w"]), t0=round(at + w["t0"] - s0, 3), t1=round(at + w["t1"] - s0, 3)))
            pieces.append(x); at += len(x)/SR
        x = np.concatenate(pieces); x = sosfiltfilt(sos, x); pre = dict(active=act_db(x), spread=spread(x))
        y = fftconvolve(add_room(x, WET), h, "same")
        best = y
        if spread(y) > F_sp + 0.7:                                        # only compress as far as the film's own spread
            thr = np.percentile(frames_db(active(y)), 60)
            for ratio in (1.3, 1.6, 2.0, 2.5):
                z = compress(y, thr, ratio); best = z
                if spread(z) <= F_sp + 0.7: break
        y = best
        for _ in range(4): y = limit(y*10**((F_act + TRIM - act_db(y))/20), -2.0)   # level to the film's active speech level (pass 2: 1 dB under), peaks under -2 dBFS
        tone, tl = film_tone(film, len(y)); y = y + tone                    # the film's own room tone under the pickup, so the floor does not drop at the join
        wr(f"{OUT}/{pid}.voice.wav", y)
        json.dump(dict(duration=round(len(y)/SR, 3), words=words, takes=rng, source=f"{D}/pickups_rerecord_48k_mono.wav"), open(f"{OUT}/words_{pid}.json", "w"), indent=0)
        err = ltas(y) - F_lt - (act_db(y) - F_act)
        rep[pid] = dict(seconds=round(len(y)/SR, 2), active_before=round(pre["active"], 1), active_after=round(act_db(y), 1), spread_before=round(pre["spread"], 1), spread_after=round(spread(y), 1),
                        peak=round(20*np.log10(np.abs(y).max()), 1), tone_err_mean=round(float(np.abs(err).mean()), 2), tone_err_max=round(float(np.abs(err).max()), 2), text=" ".join(w["w"] for w in words))
        print(pid, {k: (float(v) if not isinstance(v, str) else v[:60]) for k, v in rep[pid].items()}); print("   residual per band:", " ".join(f"{v:+.1f}" for v in err))
    json.dump(dict(film=dict(active=F_act, spread=F_sp, crest=F_crest), eq_db=list(map(float, g)), pickups=rep), open(f"{OUT}/pickup_audio_report.json", "w"), indent=1)
