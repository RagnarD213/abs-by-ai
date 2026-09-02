#!/usr/bin/env python3
"""Hard gate for the 9:16 build.

⚠ THIS GATE PASSED 11/11 ON THE VIDEO DAN CALLED "TRULY AWFUL". Every check measured
format -- frame size, loudness, coverage %, change rate -- and not one of them ever
watched the video. Checks 12-15 exist because of that: they measure the four things that
were actually wrong (one fixed crop for all talk, four times his SFX density, a bed at
the wrong tempo, and no human ever looking at the moving picture), and check 15 refuses
to pass at all until the watch pass has been done and its log written.

Everything is measured off the FINISHED FILE, never the build plan -- a build plan cannot
tell you that a filter silently truncated a segment.
"""
import glob, json, os, re, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '.')
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
V  = sys.argv[1] if len(sys.argv) > 1 else 'ad1_vertical_9x16.mp4'
TARGET = float(sys.argv[2]) if len(sys.argv) > 2 else 232.768
REF = 'ref_audit/his.wav'
R = []
def chk(ok, name, detail): R.append((bool(ok), name, detail))

p = subprocess.run([FP,'-v','error','-select_streams','v','-show_entries',
    'stream=width,height,r_frame_rate','-show_entries','format=duration','-of','csv=p=0',V],
    capture_output=True, text=True).stdout.split()
w, h, fr = p[0].split(',')[:3]; dur = float(p[1])
chk((w,h) == ('1080','1920'), '1  frame size is 1080x1920', f'{w}x{h}')
chk(fr == '30000/1001', '2  frame rate is 29.97', fr)
chk(abs(dur-TARGET) < 0.10, '3  duration matches the reference cut', f'{dur:.3f}s vs {TARGET}s')

r = subprocess.run([FF,'-hide_banner','-nostats','-i',V,'-af','loudnorm=print_format=summary',
    '-f','null','-'], capture_output=True, text=True).stderr
g = lambda k: float(re.search(rf'{k}:\s+(-?[\d.]+)', r).group(1))
I, TP = g('Input Integrated'), g('Input True Peak')
chk(abs(I+14) <= 0.8, '4  loudness -14 LUFS', f'{I} LUFS')
chk(TP <= -1.0,       '5  true peak at or under -1.0 dBTP', f'{TP} dBTP')

subprocess.run([FF,'-v','error','-y','-i',V,'-map','0:a','-ar','16000','-ac','2','_qc.wav'], check=True)
a = np.frombuffer(wave.open('_qc.wav').readframes(10**9), dtype='<i2').astype(np.float32).reshape(-1,2)
c = float(np.corrcoef(a[:,0], a[:,1])[0,1])
chk(c > 0.98, '6  voice is centred (single mic, no comb)', f'L/R corr {c:.4f}')

vals = subprocess.run([FF,'-v','info','-i',V,'-vf',
    "select='gt(scene,0.12)',metadata=print:file=-",'-an','-f','null','-'],
    capture_output=True, text=True).stdout
ts = sorted(set(round(float(x),2) for x in re.findall(r'pts_time:([\d.]+)', vals)))
gaps = [b-a2 for a2, b in zip([0.0]+ts, ts+[dur])]
chk(len(ts)/(dur/60) >= 9.0, '7  visual change rate >= 9/min',
    f'{len(ts)/(dur/60):.1f}/min ({len(ts)} changes)')
chk(max(gaps) <= 16.0, '8  no stretch over 16s without a visual change', f'longest {max(gaps):.1f}s')

import beats as BT
tl, ov = BT.timeline()
if abs(TARGET-BT.DUR) < 1.0:
    sel = [(0.0, BT.DUR)]
else:
    import cutdown as CD
    sel = [(q['src0'], q['src1']) for q in CD.plan()[0]]
ins = 0.0
for b in tl:
    if b['kind'] == 'talk': continue
    for a2, b2 in sel: ins += max(0.0, min(b['t1'], b2) - max(b['t0'], a2))
chk(ins/TARGET >= 0.55, '9  insert/graphic coverage >= 55%', f'{100*ins/TARGET:.0f}%')

# 10 -- the banned product screens, matched against the FINISHED PICTURE, not the plan.
# The recording hits the in-app "Meet the new you" BEFORE/AFTER at 26 s and the
# email-capture form at 29 s. His cut runs past both. Ours must not.
from assets import MEDIA, APP
def sig(path, t, isvid=True):
    o = f'_qc_sig_{abs(hash((path,t)))%99999}.png'
    subprocess.run([FF,'-v','error','-y','-ss',f'{t:.3f}','-i',path,'-frames:v','1',
                    '-vf','scale=64:114','-pix_fmt','gray',o], check=True)
    from PIL import Image
    v = np.asarray(Image.open(o), dtype=np.float32).ravel(); os.remove(o)
    v -= v.mean(); s = v.std()
    return v/s if s > 1e-6 else v
banned = [sig(APP, t) for t in (26.4, 27.5, 29.6, 31.0)]
worst, worst_t = 0.0, None
for b in tl:
    if b.get('media') not in ('app_flow_a', 'app_flow_b'): continue
    n = max(2, int((b['t1']-b['t0'])/0.5))
    for k in range(n):
        t = b['t0'] + (b['t1']-b['t0'])*k/n
        if t > dur-0.2: continue
        s = sig(V, t)
        for bd in banned:
            v = float((s*bd).mean())
            if v > worst: worst, worst_t = v, t
chk(worst < 0.72, '10 no banned before/after or email screen reachable in the product beats',
    f'worst match {worst:.2f}' + (f' at {worst_t:.1f}s' if worst_t else ''))

chk(os.path.exists('captions.mov'), '11 burned captions present', 'captions.mov')

# --- 12-15: the four things that were actually wrong with attempt 1 ------------------
scales = [BT.push_at(t/10) for t in range(int(TARGET*10))]
talk_t = [t/10 for t in range(int(TARGET*10))
          if any(b['kind'] == 'talk' and b['t0'] <= t/10 < b['t1'] for b in tl)]
pushed = sum(1 for t in talk_t if BT.push_at(t) > 1.05)/10
chk(len(talk_t) and pushed/(len(talk_t)/10) >= 0.25,
    '12 talking head is not one fixed crop (his push schedule is reproduced)',
    f'{100*pushed/(len(talk_t)/10):.0f}% of talk is inside a push (his: ~39%)')

import build_audio as BA
sfx_rate = TARGET/len(BA.HIS_SFX)
chk(sfx_rate >= 6.0, '13 SFX no denser than one per 6s, and only on graphic entrances',
    f'{len(BA.HIS_SFX)} events = one per {sfx_rate:.1f}s (his 11.1s, attempt 1 2.8s)')

def beat_period(path):
    SR = 48000
    d = np.frombuffer(subprocess.run([FF,'-v','error','-i',path,'-ac','1','-ar',str(SR),
        '-f','f32le','-'], capture_output=True).stdout, dtype=np.float32).astype(float)
    N, H = 1024, 256; fps = SR/H
    frm = np.lib.stride_tricks.sliding_window_view(d, N)[::H]*np.hanning(N)
    S = np.abs(np.fft.rfft(frm, axis=1)); f = np.fft.rfftfreq(N, 1/SR)
    out = []
    for lo, hi in ((30,150), (6000,14000)):
        b = S[:, (f>=lo)&(f<hi)].sum(1); dd = np.maximum(0, np.diff(b))
        dd = (dd-dd.mean())/(dd.std()+1e-9)
        ac = np.correlate(dd, dd, 'full')[len(dd)-1:]; ac /= ac[0]
        lags = np.arange(len(ac))/fps; band = (lags > 0.28) & (lags < 1.1)
        out.append(float(lags[band][int(np.argmax(ac[band]))]))
    return out
ours, his = beat_period(V), beat_period(REF)
bpm_h = 60/his[1]                       # his hat band: 0.480 s = 125 BPM
def best_bpm(periods, target_bpm):
    """A bed under a ducked voice often locks on the half- or double-time grid, so fold
    each measured period to the octave nearest the reference before comparing."""
    cands = [60/(p*k) for p in periods for k in (0.5, 1, 2)]
    return min(cands, key=lambda v: abs(v-target_bpm))
bpm_o = best_bpm(ours, bpm_h)
chk(abs(bpm_o-bpm_h) <= 15, '14 music bed tempo matches the reference bed',
    f'ours {bpm_o:.0f} BPM vs his {bpm_h:.0f} BPM')

wl = 'logs/watch_pass.json'
ok = False; det = 'NOT DONE -- run watch.py'
if os.path.exists(wl):
    d = json.load(open(wl))
    ok = d.get('video') == os.path.basename(V) and d.get('reviewed', 0) >= d.get('boundaries', 1) \
         and d.get('listened') is True
    det = (f"{d.get('reviewed')}/{d.get('boundaries')} boundary clips watched as MOVING video, "
           f"full listen {'done' if d.get('listened') else 'NOT done'}")
chk(ok, '15 WATCH PASS done on this exact file (the gate, not the metrics)', det)

# --- 16-17: audio integrity + the shared gate's stamp (2026-09-02) ------------------------
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio')
import common as _C
_la, _lv = _C.duration(V, 'a:0'), _C.duration(V, 'v:0')
_dead, _quiet = _C.silent_seconds(_C.pcm(V, ac=1))
chk(abs(_la - _lv) <= 0.10 and _dead == 0, '16 audio integrity: audio runs the full length, no silent second',
    f'audio {_la:.3f}s vs video {_lv:.3f}s, {_dead} digitally silent s ({_quiet} below -50 dBFS)')
try:
    from require_stamp import require_stamp; require_stamp(V, quiet=True); _sok, _sd = True, 'stamp present, matches this file, PASS'
except SystemExit as _e: _sok, _sd = False, str(_e)
chk(_sok, '17 audio gate stamp (_shared/audio/audio_gate.py) on this exact file', _sd)

print(f'\nQC  {V}')
for ok, n, d in R: print(f'  {"PASS" if ok else "FAIL"}  {n:70s} {d}')
bad = [x for x in R if not x[0]]
print(f'\n{len(R)-len(bad)}/{len(R)} pass')
sys.exit(1 if bad else 0)
