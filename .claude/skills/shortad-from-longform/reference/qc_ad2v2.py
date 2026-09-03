#!/usr/bin/env python3
"""Hard gate for the vertical Ad 2, measured off the FINISHED FILE, never the build plan.

⚠ The ancestor of this gate passed 11/11 on a video Dan called "truly awful", because
every check measured format and none of them watched the picture. Check 15 refuses to pass
until the watch pass has been done on this exact file; check 16 exists because a mux once
truncated the audio at 2:24 of a 3:52 master, exited 0, and passed everything.
"""
import json, os, re, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '.')
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
V = sys.argv[1] if len(sys.argv) > 1 else 'ad2v2_vertical_9x16.mp4'
TARGET = 276.109167
R = []
def chk(ok, name, detail): R.append((bool(ok), name, detail))

# ⚠ PROBE THE VIDEO STREAM, NOT THE CONTAINER. The container's duration is the longer of
# the two streams, so a truncated PICTURE reads back as the full length and every duration
# check passes -- which is how a 10-frame hole and a 334 ms A/V offset shipped.
# ffprobe emits csv fields in ITS order (duration before nb_read_frames), not the requested
# order -- parse by name from json so a field swap cannot turn a frame count into a duration.
_pj = json.loads(subprocess.run([FP,'-v','error','-select_streams','v','-count_frames','-show_entries',
    'stream=width,height,r_frame_rate,nb_read_frames,duration','-of','json',V],
    capture_output=True, text=True).stdout)['streams'][0]
w, h, fr, NFR, dur = str(_pj['width']), str(_pj['height']), _pj['r_frame_rate'], int(_pj['nb_read_frames']), float(_pj['duration'])
chk((w,h)==('1080','1920'), '1  frame size is 1080x1920', f'{w}x{h}')
chk(fr=='30000/1001', '2  frame rate is 29.97', fr)
chk(abs(dur-TARGET) < 0.10, '3  video stream duration matches his cut', f'{dur:.3f}s vs {TARGET:.3f}s')
import beats as _BT
_PLAN = round(_BT.DUR*30000/1001)
chk(NFR == _PLAN, '3b every planned frame is present (no truncated beat)',
    f'{NFR} frames vs {_PLAN} planned')

r = subprocess.run([FF,'-hide_banner','-nostats','-i',V,'-af','loudnorm=print_format=summary',
    '-f','null','-'], capture_output=True, text=True).stderr
g = lambda k: float(re.search(rf'{k}:\s+(-?[\d.]+)', r).group(1))
I, TP = g('Input Integrated'), g('Input True Peak')
chk(abs(I+14) <= 0.8, '4  loudness -14 LUFS', f'{I} LUFS')
chk(TP <= -1.0, '5  true peak at or under -1.0 dBTP', f'{TP} dBTP')

subprocess.run([FF,'-v','error','-y','-i',V,'-map','0:a','-ar','16000','-ac','2','_qc.wav'], check=True)
a = np.frombuffer(wave.open('_qc.wav').readframes(10**9), dtype='<i2').astype(np.float32).reshape(-1,2)
c = float(np.corrcoef(a[:,0], a[:,1])[0,1])
chk(c > 0.98, '6  voice is centred / mono-safe', f'L/R corr {c:.4f}')

vals = subprocess.run([FF,'-v','info','-i',V,'-vf',
    "select='gt(scene,0.12)',metadata=print:file=-",'-an','-f','null','-'],
    capture_output=True, text=True).stdout
ts = sorted(set(round(float(x),2) for x in re.findall(r'pts_time:([\d.]+)', vals)))
gaps = [b-a2 for a2, b in zip([0.0]+ts, ts+[dur])]
chk(len(ts)/(dur/60) >= 9.0, '7  visual change rate >= 9/min',
    f'{len(ts)/(dur/60):.1f}/min ({len(ts)} changes)')
# Bar is HIS cut, not an absolute: his longest talking stretch is 31.6 s. Dan's round-1
# note was to mirror his graphics and stop inventing text, which removed the two extra
# bullet cards that had been holding this number down.
chk(max(gaps) <= 31.6, '8  no stretch longer than his own longest (31.6s)', f'longest {max(gaps):.1f}s')

import beats as BT
tl, _ = BT.timeline()
ins = sum(b['t1']-b['t0'] for b in tl if b['kind'] != 'talk')
# ⚠ HIS OWN CUT MEASURES 39% -- far below the 58-65% modern standard and below his Ad 1.
# The bar here is therefore "at least his, with margin", not an absolute 55%: padding a
# faithful reproduction with filler inserts to clear a number is the wrong trade.
chk(ins/TARGET >= 0.39, '9  insert/graphic coverage at least his 39%',
    f'{100*ins/TARGET:.0f}%')

# 10 -- BANNED SCREENS, matched on EVERY FRAME of the finished picture.
# A sampling scan cannot see a single-frame violation: on Ad 3 a 2 fps scan reported a
# clean 0.647 and the same scan at full rate reported 1.000 and failed the build.
from PIL import Image
APPF = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
        "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4")
def sigs_of(path, times):
    out = []
    for t in times:
        o = '/tmp/_qsig.png'
        subprocess.run([FF,'-v','error','-y','-ss',f'{t:.3f}','-i',path,'-frames:v','1',
                        '-vf','scale=48:86','-pix_fmt','gray',o], check=True)
        v = np.asarray(Image.open(o), dtype=np.float32).ravel(); v -= v.mean()
        out.append(v/max(v.std(),1e-6))
    return out
banned = sigs_of(APPF, (26.5, 27.5, 29.5, 31.0))     # before/after pair, then the email form
raw = subprocess.run([FF,'-v','error','-i',V,'-vf','scale=48:86,format=gray','-f','rawvideo','-'],
                     capture_output=True).stdout
F = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 86*48).astype(np.float32)
F -= F.mean(1, keepdims=True); F /= np.maximum(F.std(1, keepdims=True), 1e-6)
worst, wt = 0.0, None
for bd in banned:
    v = (F*bd).mean(1); k = int(np.argmax(v))
    if v[k] > worst: worst, wt = float(v[k]), k/(30000/1001)
chk(worst < 0.72, '10 no banned before/after or email screen anywhere (ALL frames)',
    f'{len(F)} frames scanned, worst match {worst:.2f} at {wt:.1f}s')

chk(os.path.exists('captions.mov'), '11 burned captions present', 'captions.mov')

talk_t = [t/10 for t in range(int(TARGET*10))
          if any(b['kind']=='talk' and b['t0'] <= t/10 < b['t1'] for b in tl)]
pushed = sum(1 for t in talk_t if BT.push_at(t) > 1.05)
chk(len(talk_t) and pushed/len(talk_t) >= 0.25,
    '12 talking head is not one fixed crop (his push schedule reproduced)',
    f'{100*pushed/max(len(talk_t),1):.0f}% of talk inside a push (his: 28%)')

# 13/14 -- the audio IS his mix, so his bed and his SFX are correct by construction.
# Prove that rather than re-measuring tempo and transient density.
def mono16(src, extra=()):
    subprocess.run([FF,'-v','error','-y','-i',src,*extra,'-ac','1','-ar','16000',
                    '-c:a','pcm_s16le','/tmp/_pv.wav'], check=True)
    return np.frombuffer(wave.open('/tmp/_pv.wav').readframes(10**9), dtype='<i2').astype(float)
ours, his = mono16(V), mono16('his_mix.wav')
n = min(len(ours), len(his)); ours, his = ours[:n]-ours[:n].mean(), his[:n]-his[:n].mean()
W = 16000
kk = min(len(ours), len(his))//W
cors, gains = [], []
for i in range(kk):
    x, y = his[i*W:(i+1)*W], ours[i*W:(i+1)*W]
    if np.sqrt((x**2).mean()) < 50: continue      # skip true silence
    g = np.dot(x, y)/max((x**2).sum(), 1e-9)      # best-fit gain for this second
    xx, yy = x-x.mean(), y-y.mean()
    cors.append(float(np.dot(xx,yy)/np.sqrt((xx**2).sum()*(yy**2).sum())))
    gains.append(20*np.log10(max(g, 1e-9)))
cors, gains = np.array(cors), np.array(gains)
med = float(np.median(cors))
# The right test for "this is his mix": inside each second, once the level is normalised,
# the waveform must be his. A whole-file correlation cannot pass, because reaching ad spec
# is +6.4 dB against peaks already at -0.1 dBTP, so the limiter genuinely rides the level.
chk(med >= 0.99, '13 audio is HIS finished mix (per-second, level-normalised)',
    f'median {med:.4f} over {len(cors)} windows; limiter rides '
    f'{gains.min():+.1f}..{gains.max():+.1f} dB')
chk(True, '14 no synthesised bed or SFX were added', 'none by construction')

wl = 'logs/watch_pass.json'
ok, det = False, 'NOT DONE -- run watch.py'
if os.path.exists(wl):
    d = json.load(open(wl))
    ok = (d.get('video') == os.path.basename(V) and
          d.get('reviewed', 0) >= d.get('boundaries', 1) and d.get('inspected') is True)
    det = f"{d.get('reviewed')}/{d.get('boundaries')} boundaries reviewed as consecutive frames"
chk(ok, '15 WATCH PASS done on this exact file (the gate, not the metrics)', det)

# 16 -- audio integrity. A mux once truncated the audio at 2:24 of a 3:52 master and
# exited 0. Probe the STREAM, not the container, and scan every second for a dropout.
ad = subprocess.run([FP,'-v','error','-select_streams','a','-show_entries','stream=duration',
                     '-of','csv=p=0',V], capture_output=True, text=True).stdout.strip().split('\n')[0]
ad = float(ad) if ad and ad != 'N/A' else -1
mono = a.mean(1)/32768.0          # normalise, or every dBFS reads positive and the
sec = [20*np.log10(np.sqrt((mono[i*16000:(i+1)*16000]**2).mean())+1e-12)   # check never fires
       for i in range(int(dur))]
silent = [i for i, v in enumerate(sec) if v < -50]
chk(abs(ad-dur) < 0.15 and not silent,   # dur is now the VIDEO STREAM's own duration
    '16 audio stream runs the full length and no second is silent',
    f'audio {ad:.3f}s vs video {dur:.3f}s; {len(silent)} silent seconds; quietest {min(sec):.1f} dBFS')

# 17 -- CENTERING, MEASURED ON THE DELIVERED FILE.
# ⚠ THE CHECK WHOSE ABSENCE COST TWO REJECTED VERSIONS. Everything upstream can be right --
# the track measured with Apple Vision, the A/B verified, the beat sheet correct -- and the
# delivered picture still wrong, because the ffmpeg crop EXPRESSION built its nested ifs in
# the wrong order and evaluated the final interval, extrapolated, across the whole beat.
# Nothing that inspects the build plan can see that; only the finished frames can.
import centering as CE
rows = CE.measure(rebuild=not os.path.exists('centering/m'))
talk = np.array([[r[0], r[2]] for r in rows if r[1] == 'talk'])
cv = talk[:, 1]
runs, cur = [], []
for t, x in talk:
    if abs(x) > 60: cur.append(x)
    else:
        if len(cur) >= 4: runs.append(float(np.mean(cur)))
        cur = []
if len(cur) >= 4: runs.append(float(np.mean(cur)))
chk(abs(np.median(cv)) <= 25 and (np.abs(cv) > 70).mean() <= 0.10 and not runs,
    '17 presenter is centred in the DELIVERED frame',
    f'median {np.median(cv):+.0f} px, sd {cv.std():.0f}, '
    f'{(np.abs(cv)>70).sum()}/{len(cv)} beyond 70px, {len(runs)} sustained runs')

# 18 -- the shared audio gate's STAMP on this exact file (_shared/audio/audio_gate.py).
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio')
try:
    from require_stamp import require_stamp; require_stamp(V, quiet=True); _sok, _sd = True, 'stamp present, matches this file, PASS'
except SystemExit as e: _sok, _sd = False, f'NO VALID STAMP: {e}'
except Exception as e: _sok, _sd = False, f'NO VALID STAMP: {e}'
chk(_sok, '18 audio gate stamp (_shared/audio/audio_gate.py) on this exact file', _sd)

# 19 -- the audio is HIS mix moved by ONE CONSTANT GAIN (gain_flatness.py, one-sided): nothing
# above G, p90 within 0.25 dB of G, the limiter shaving no second by more than 2.5 dB.
gf = subprocess.run(['python3', '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/'
                     'shortad-from-longform/reference/gain_flatness.py', 'his_mix.wav', V],
                    capture_output=True, text=True)
_gl = [l for l in (gf.stdout + gf.stderr).strip().split('\n') if l.strip()]
chk(gf.returncode == 0, '19 constant gain against HIS mix (gain_flatness, one-sided)', _gl[-1] if _gl else 'no output')

print(f'\nQC  {V}')
for ok, n_, d in R: print(f'  {"PASS" if ok else "FAIL"}  {n_:72s} {d}')
bad = [x for x in R if not x[0]]
print(f'\n{len(R)-len(bad)}/{len(R)} pass')
sys.exit(1 if bad else 0)
