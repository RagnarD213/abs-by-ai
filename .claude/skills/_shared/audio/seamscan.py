#!/usr/bin/env python3
"""Audio seam / onset scan for a delivered film (VIDEO-RULES, "Audio joins are smooth before anything ships", 2026-10-20).

usage: seamscan.py FILM.wav [--joins joins.json] [--out report.json]
  FILM.wav: mono 48 kHz PCM extracted from the exact delivered file (audio-only ffmpeg, no queue).
  joins.json: every audio seam in seconds, from the assembly map (cumulative samples / rate), not the gate's list.
Flags per join: CLICK (sample discontinuity), FLOOR-JUMP (room tone >5 dB), MID-SPEECH (speech runs into and
out of the cut), HARD-START (speech begins on the first frame after the cut), LONG-PAUSE. Also global clicks,
hard onsets and dead air. Every flag is a candidate for a 5 s listen, not a verdict. Built on RO-25, 2026-10-20.
Finds: (1) clicks / sample discontinuities, (2) hard speech onsets (speech that starts
with no attack, as after a cut), (3) room-tone / level jumps at joins, (4) dead air.
"""
import sys, json, wave, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('wav')
ap.add_argument('--joins', help='json list of join times in seconds')
ap.add_argument('--out')
a = ap.parse_args()

w = wave.open(a.wav)
sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
if w.getnchannels() > 1:
    x = x.reshape(-1, w.getnchannels()).mean(axis=1)
dur = len(x) / sr

def db(v): return 20*np.log10(max(v, 1e-9))

# 10 ms RMS envelope
hop = int(sr*0.010)
nf = len(x)//hop
env = np.sqrt((x[:nf*hop].reshape(nf, hop)**2).mean(axis=1))
env_db = 20*np.log10(np.maximum(env, 1e-9))
# speech threshold: relative to the loud part of the file
loud = np.percentile(env_db, 90)
speech_thr = loud - 22.0     # speech-ish
quiet_thr = loud - 40.0      # room tone / silence

report = {'file': a.wav, 'duration': dur, 'loud_p90_db': float(loud), 'speech_thr_db': float(speech_thr)}

# ---- 1. clicks: first-difference spikes vs local median
d = np.abs(np.diff(x))
win = int(sr*0.05)
# local median of |diff| per 50 ms block
nb = len(d)//win
blk = d[:nb*win].reshape(nb, win)
med = np.median(blk, axis=1) + 1e-6
mx = blk.max(axis=1)
ratio = mx/med
clicks = []
for i in np.where(ratio > 25)[0]:
    j = i*win + int(blk[i].argmax())
    t = j/sr
    if mx[i] < 0.02:  # ignore tiny spikes in near-silence
        continue
    clicks.append({'t': round(t,3), 'ratio': round(float(ratio[i]),1), 'jump': round(float(mx[i]),4)})
# merge within 30 ms
m=[]
for c in clicks:
    if m and c['t']-m[-1]['t'] < 0.03:
        if c['ratio']>m[-1]['ratio']: m[-1]=c
    else: m.append(c)
report['clicks'] = m

# ---- 2. hard onsets: quiet (<= quiet_thr for >= 120 ms) then speech level within 1 frame (10 ms)
onsets=[]
i=12
while i < nf-3:
    if env_db[i] >= speech_thr and env_db[i-1] < quiet_thr+6 and (env_db[i-12:i-1] < quiet_thr+6).all():
        # rise within 10 ms from quiet to speech: hard start
        # measure sub-frame: first 2 ms of this frame vs its last 2 ms
        seg = x[i*hop:(i+1)*hop]
        a2 = np.sqrt((seg[:int(sr*0.002)]**2).mean()); b2 = np.sqrt((seg[-int(sr*0.002):]**2).mean())
        onsets.append({'t': round(i*hop/sr,3), 'from_db': round(float(env_db[i-1]),1), 'to_db': round(float(env_db[i]),1),
                       'first2ms_db': round(db(a2),1), 'attack_ms': 10 if db(a2) > speech_thr-6 else None})
        i += 20
    i += 1
report['hard_onsets'] = [o for o in onsets if o['attack_ms'] is not None]
report['fast_onsets_all'] = len(onsets)

# ---- 3. dead air: runs below quiet_thr+3 longer than 0.5 s
gaps=[]; run=0; start=None
for i in range(nf):
    if env_db[i] < quiet_thr+3:
        if run==0: start=i
        run+=1
    else:
        if run*0.010 >= 0.5: gaps.append({'t': round(start*0.010,2), 'len': round(run*0.010,2)})
        run=0
report['dead_air'] = gaps

# ---- 4. joins
def floor_db(seg):
    k = max(1, len(seg)//hop)
    e = np.sqrt((seg[:k*hop].reshape(k,hop)**2).mean(axis=1))
    return db(np.percentile(e, 10))
joins=[]
if a.joins:
    J = json.load(open(a.joins))
    for t in J:
        s = int(t*sr)
        if s < sr or s > len(x)-sr: continue
        pre = x[s-int(sr*0.25):s]; post = x[s:s+int(sr*0.25)]
        pre1 = x[s-sr:s]; post1 = x[s:s+sr]
        # discontinuity at the sample
        local = np.median(np.abs(np.diff(x[s-win:s+win]))) + 1e-6
        jump = float(abs(x[s]-x[s-1]))
        # first speech after the join
        fi = s//hop
        k = fi
        while k < nf and env_db[k] < speech_thr: k += 1
        onset_ms = (k-fi)*10
        # speech running INTO the join (cut mid-word?)
        kb = fi-1
        into = env_db[kb] >= speech_thr-3 if kb>=0 else False
        outof = env_db[fi] >= speech_thr-3
        joins.append({'t': round(t,3), 'level_pre_db': round(db(np.sqrt((pre**2).mean())),1),
                      'level_post_db': round(db(np.sqrt((post**2).mean())),1),
                      'floor_pre_db': round(floor_db(pre1),1), 'floor_post_db': round(floor_db(post1),1),
                      'sample_jump': round(jump,4), 'jump_ratio': round(jump/local,1),
                      'speech_into_join': bool(into), 'speech_out_of_join': bool(outof), 'first_speech_after_ms': onset_ms})
report['joins'] = joins

def fmt(t):
    m=int(t//60); s=t-60*m; return f"{m}:{s:05.2f}"
print(f"{a.wav}: {dur:.1f}s  loud p90 {loud:.1f} dB  speech thr {speech_thr:.1f}")
print(f"clicks (ratio>25): {len(m)}")
for c in sorted(m, key=lambda c:-c['ratio'])[:25]: print('  click', fmt(c['t']), {k:(round(float(v),4) if not isinstance(v,(int,bool)) else v) for k,v in c.items()})
print(f"hard onsets (speech within 2 ms of silence): {len(report['hard_onsets'])}")
for o in report['hard_onsets'][:40]: print('  onset', fmt(o['t']), {k:(round(float(v),1) if v is not None and not isinstance(v,(int,bool)) else v) for k,v in o.items()})
print(f"dead air >=0.5s: {len(gaps)}")
for g in gaps: print('  gap', fmt(g['t']), g)
if joins:
    print(f"joins: {len(joins)}")
    for j in joins:
        flags=[]
        if j['jump_ratio']>8 and j['sample_jump']>0.01: flags.append('CLICK')
        if abs(j['floor_pre_db']-j['floor_post_db'])>5: flags.append('FLOOR-JUMP')
        if j['speech_into_join'] and j['speech_out_of_join']: flags.append('MID-SPEECH')
        if j['speech_out_of_join'] and j['first_speech_after_ms']==0 and not j['speech_into_join']: flags.append('HARD-START')
        if j['first_speech_after_ms']>700: flags.append('LONG-PAUSE')
        print('  join', fmt(j['t']), ' '.join(flags) or '-', {k:(round(float(v),4) if not isinstance(v,(bool,int)) else v) for k,v in j.items()})
if a.out: json.dump(json.loads(json.dumps(report, default=float)), open(a.out,"w"), indent=1)
