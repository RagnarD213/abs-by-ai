"""DS-43 R1 prep: edit list, audio and film-time word map for ONE version.   python3 prep.py scripted|offcuff [--no-audio]
Writes <version>/edl.json, words_out.json, lav.wav, voice-<name>.wav, clip-finished.wav.

Shared opening (identical in both versions, Bill Maher Codex R5 sequence):
  C1  clip 0.00-4.30   Terry's hook "My first meal is at 2 p.m. and then I eat from 2 to 10." full screen (fixed portrait window
                       on him; his burned "My first meal" text sits left of the window), Dan keyed lower left at 0.40.
                       The clip's own blur transition starts at 4.32.
  C2  clip 8.40-19.82  "Over the last five years ... but then I don't eat." in the titled panel (Dan large, still watching).
                       The clip's title photo ("How intermittent fasting keeps Terry Crews in shape") and its blur run to 9.2:
                       Terry is already speaking over them, so the panel opens on that shot. The cut lands 0.06 s after "eat.".
                       Cut out: 4.30-8.40 (title card, no speech).
  Dan's real reaction: one full play on the roll, roll = clip + 1984.799 (lav cross-correlation, 5 windows agree to 1 ms).
  Then the response starts in the same panel layout (clip continues silently from 19.82) and the field section follows.

Talk pieces: every cut sits in a measured pause (audio/takes_db10ms.npy, medium.en words audio/*_words.json, spot passes
audio/spots.json). Pause trims happen only at a shot change (zoom cut, layout change or cutaway), never as a naked jump.
"""
from pathlib import Path
import json, subprocess, sys, os, re
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
CLIP = W/'src/terry_full.mkv'
ROLL_MINUS_CLIP = 1984.799
VERSION = sys.argv[1]; assert VERSION in ('scripted', 'offcuff')
O = W/VERSION; O.mkdir(exist_ok=True); (O/'audio').mkdir(exist_ok=True)
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)
def fr(t): return int(round(t*FPS))

CLIP_SEGS = [('C1', 0.00, 4.30), ('C2', 8.40, 19.82)]
# id, roll in, roll out. Piece 1 plays over the silent panel (one continuous piece, no cut inside it).
TALK = {
    'scripted': [
        # "Terry Crews is smart as fuck. ... And it's going to work for you too."  ("All right," 2024.02-2024.97 cut: a slate)
        ('P1', 2025.03, 2034.24),
        # "I've been doing fasting for about 10 years, ... my first meal at 2."  (0.70 s pause -> layout change to the field)
        ('P2', 2034.62, 2040.18),
        # "Fasting until 2 is actually easy ... until about 2."
        ('P3', 2040.36, 2054.30),
        # "And what I love the most about fasting ... calories for the day."  (SPOT 1 decides the 'I ... love' hesitation)
        ('P4', 2055.86, 2062.90),
        # second read (spot pass audio/spot_restart.json; first read "If you're not fasting, then ... dinner to" 2063.18-2067.50 cut):
        # "If you're not fasting, then you'll probably have to eat a small, low calorie dinner to hit your calories. If you think
        # fasting will make you lose muscle mass, watch that Terry Crews video again and shut the fuck up."  (enters 50 ms before
        # the onset at 2068.45; the 'and And' of the first pass was one 'and': spot pass audio/spots.json)
        ('P5', 2068.40, 2078.60),
        # "And if you wanna learn how to get started with intermittent fasting, subscribe to my channel."  ("Because if you wanna…" cut)
        ('P6', 2080.60, 2084.62)],
    'offcuff': [
        # "Terry Crews is smart as fuck. He knows what you're doing. And this video ... to watch."  ("All right," cut)
        ('P1', 2099.17, 2107.22),
        # "So Terry Crews, obviously, fitness professional ... in his 50s now."  (0.66 s pause trimmed at the layout change)
        ('P2', 2107.56, 2117.22),
        # "He's doing this with intermittent fasting ... work for you too."
        ('P3', 2117.24, 2123.37),
        # "And I've heard a lot of people out there saying, Dan, ... Get that out of your head."
        ('P4', 2123.66, 2140.80),
        # restart cut: "Fasting is great because you can," (2141.32-2143.06) -> "fasting is great because your body adapts ... easy."
        ('P5', 2144.14, 2148.86),
        # "Fasting also lets you eat a big dinner ... much harder."
        ('P6', 2149.18, 2158.78),
        # "So try fasting and I know you're gonna love the results."
        ('P7', 2159.06, 2161.72),
        # "If you want to learn how to get started with intermittent fasting, subscribe to my channel."  (SPOT 4: the pause in "to")
        ('P8', 2163.02, 2166.62)],
        # R1 independent review: every off-cuff join ends before Dan's in-breath and starts in the quiet just before speech
        # (P2 keeps the 'S' of 'So' at 2107.62; P5 starts after the roll's click at 2144.10)
}[VERSION]
KEY = dict(watchF=1984.40, T=dict(scripted=2024.80, offcuff=2098.90)[VERSION])
XF = 0.010            # 10 ms crossfade at every voice join, each inside a measured dip

segs = []; n = 0
for sid, a, b in CLIP_SEGS:
    k = fr(b - a); segs.append(dict(id=sid, clip_in=a, frames=k, n0=n, film0=n/FPS)); n += k
CLIP_FRAMES = n
pieces = []
for pid, a, b in TALK:
    k = fr(b - a); pieces.append(dict(id=pid, key='T', source=SRC, start=a, frames=k, duration=k/FPS, n0=n, film0=n/FPS)); n += k
TOTAL = n
edl = dict(version=VERSION, fps='30000/1001', speed=1.0, total_frames=TOTAL, total_seconds=TOTAL/FPS,
           clip=dict(file=str(CLIP), segs=segs, frames=CLIP_FRAMES, roll_minus_clip=ROLL_MINUS_CLIP, panel_silent_from=25.20),   # after the clip's own repeat of the hook (19.9-23.7 s) and its subtitle card (to 25.1 s); cache src/clip_silent_24fps.npy
           pieces=pieces, key=KEY)
(O/'edl.json').write_text(json.dumps(edl, indent=1))

# Voice: the exact voice Dan approved on this set, mic and day (DS-44B Hormozi off-cuff R2 = DS-40 Claude house EQ fitted on
# C1730 + a half bass lift, expander on), level matched to -14.1 LUFS by the shared chain. Balanced kept as the A/B alternative.
E_EQ = ('highpass=f=70,equalizer=f=110:t=q:w=1.3:g=-5.89,equalizer=f=194:t=q:w=1.3:g=+0.46,equalizer=f=316:t=q:w=1.3:g=+1.95,'
        'equalizer=f=490:t=q:w=1.3:g=+2.44,equalizer=f=735:t=q:w=1.3:g=+1.63,equalizer=f=1122:t=q:w=1.3:g=+1.21,'
        'equalizer=f=1755:t=q:w=1.3:g=+1.12,equalizer=f=2775:t=q:w=1.3:g=+0.55,equalizer=f=4387:t=q:w=1.3:g=-3.65,'
        'treble=g=-1.65:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+1.5')
BAL = 'highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
VOICES = {'house_bass15': dict(eq=E_EQ, expander=True), 'balanced': dict(eq=BAL, expander=False)}

if '--no-audio' not in sys.argv:
    parts = []
    for i, p in enumerate(pieces):
        last = i == len(pieces) - 1
        d = p['duration'] + (0 if last else XF)
        af = 'pan=mono|c0=c0' + (f",afade=t=out:st={d-0.06}:d=0.06" if last else '') + (',afade=t=in:d=0.006' if i == 0 else '')
        ff(['-ss', p['start'], '-i', SRC, '-t', d, '-map', '0:a:0', '-af', af, '-ar', 48000, '-c:a', 'pcm_s24le', O/'audio'/f"lav-{p['id']}.wav"])
        parts.append(O/'audio'/f"lav-{p['id']}.wav")
    ins = []; fc = ''; prev = '0:a'
    for i in range(1, len(parts)):
        ins += ['-i', parts[i]]; fc += f'[{prev}][{i}:a]acrossfade=d={XF}:c1=tri:c2=tri[x{i}];'; prev = f'x{i}'
    fc += f'[{prev}]apad,atrim=duration={(TOTAL - CLIP_FRAMES)/FPS:.6f}[lav]'
    ff(['-i', parts[0]] + ins + ['-filter_complex', fc, '-map', '[lav]',
        '-ar', 48000, '-c:a', 'pcm_s24le', O/'lav.wav'])
    for name, v in VOICES.items():
        cmd = [sys.executable, str(A/'voice_chain.py'), '--in', str(O/'lav.wav'), '--out', str(O/f'voice-{name}.wav'), '--work', str(O/'audio'/f'chain-{name}'),
               '--eq', v['eq'], '--target', '-14.1', '--tp', '-1.5', '--oversample', '4']
        if not v['expander']:
            cmd += ['--no-expander-because', 'Balanced as used on Ronaldo Ab Belt R1 (same set, mic and day): no expander, to keep complete word tails.']
        subprocess.run(cmd, check=True)
    # the clip's sound: the picture's segments, 15 ms fades (both edits sit in pauses), folded to centred mono, plain gain to
    # about the voice level, capped so the peak stays under -1.5 dBFS (no limiter: DS-33 artifacts lesson)
    cparts = []
    for s in segs:
        d = s['frames']/FPS; p = O/'audio'/f"clip-{s['id']}.wav"
        ff(['-ss', s['clip_in'], '-i', CLIP, '-t', d, '-map', '0:a:0', '-af', f'pan=mono|c0=0.5*c0+0.5*c1,aresample=48000,apad,atrim=duration={d},'
            f'afade=t=in:d=0.015,afade=t=out:st={d-0.015}:d=0.015', '-ar', 48000, '-c:a', 'pcm_s24le', p])
        cparts.append(p)
    (O/'audio'/'clip.txt').write_text(''.join(f"file '{p}'\n" for p in cparts))
    ff(['-f', 'concat', '-safe', 0, '-i', O/'audio'/'clip.txt', '-c', 'copy', O/'audio'/'clip-raw.wav'])
    # Business Insider's mix is peaky (I -20.9, peak -0.6: PLR 20), so plain gain capped at -1.5 dBFS left the clip 7 LU under
    # Dan and the film at -15.2 LUFS. Two gentle compressors at 4x rate (slow body, then a fast peak stage; no limiter, DS-33
    # lesson) bring PLR to about 14, so the clip lands near -15.8 LUFS beside Dan's -14.3.
    ff(['-i', O/'audio'/'clip-raw.wav', '-af', 'aresample=192000,acompressor=threshold=0.1:ratio=3:attack=10:release=200:knee=6,'
        'acompressor=threshold=0.18:ratio=6:attack=0.3:release=40:knee=4,aresample=48000', '-c:a', 'pcm_s24le', O/'clip-original.wav'])
    meas = subprocess.run([F, '-hide_banner', '-i', str(O/'clip-original.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas)[-1]); pk = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', meas)[-1])
    g = min(-14.5 - I, -1.5 - pk)
    ff(['-i', O/'clip-original.wav', '-af', f'volume={g:.2f}dB', '-c:a', 'pcm_s24le', '-ar', 48000, O/'clip-finished.wav'])
    (O/'audio'/'clip-level.json').write_text(json.dumps(dict(I_lufs=I, peak_dbfs=pk, gain_db=round(g, 2)), indent=1))
    (O/'audio-options.json').write_text(json.dumps(VOICES, indent=1))

# ---- words on the film timeline
out = []
def clip_to_film(c):
    for x in segs:
        if x['clip_in'] - 1e-6 <= c < x['clip_in'] + x['frames']/FPS: return x['film0'] + (c - x['clip_in'])
    return None
for w in json.load(open(W/'audio/clip_words.json')):
    n0, n1 = clip_to_film(w['t'] + 1e-3), clip_to_film(min(w['e'], w['t'] + 5) - 1e-3)
    if n0 is None or n1 is None: continue
    seg = next(x for x in segs if x['film0'] - 1e-6 <= n0 < x['film0'] + x['frames']/FPS)
    out.append(dict(w=w['w'], t0=round(n0, 3), t1=round(n1, 3), src=None, piece=seg['id'], speaker='clip'))
# "2 p .m." -> one word "2 p.m."; whisper split it
k = 0
while k < len(out) - 1:
    if out[k]['w'] == 'p' and out[k + 1]['w'].startswith('.m'):
        out[k - 1]['w'] = out[k - 1]['w'] + ' p' + out[k + 1]['w']; out[k - 1]['t1'] = out[k + 1]['t1']; del out[k:k + 2]
    else: k += 1
dw = json.load(open(W/f'audio/{VERSION}_words.json'))
spots = json.load(open(W/'audio/spots.json')) if (W/'audio/spots.json').exists() else {}
DW_FIX = json.load(open(W/f'audio/{VERSION}_wordfix.json')) if (W/f'audio/{VERSION}_wordfix.json').exists() else {}
# DW_FIX: {"drop": [t,...], "text": {"t": "word"}, "add": [[w, t, e]]}  (keys: word start rounded to 2 dp)
drop = set(DW_FIX.get('drop', [])); text = DW_FIX.get('text', {})
dw = [dict(x, w=text.get(f"{round(x['t'], 2):.2f}", x['w'])) for x in dw if round(x['t'], 2) not in drop]
dw += [dict(w=w, t=t, e=e) for w, t, e in DW_FIX.get('add', [])]
dw.sort(key=lambda x: x['t'])
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in dw:
        if w['e'] <= a or w['t'] >= b or (min(w['e'], b) - max(w['t'], a)) < 0.5*(w['e'] - w['t']): continue
        out.append(dict(w=w['w'], t0=round(max(w['t'], a) - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['t'], piece=p['id'], speaker='dan'))
for w in out:
    if w['w'].lower().strip('.,') == 'cruz': w['w'] = 'Crews' + w['w'][4:]
(O/'words_out.json').write_text(json.dumps(out, indent=1))
print('PREP', VERSION, 'frames', TOTAL, round(TOTAL/FPS, 3), 's; clip', CLIP_FRAMES, [(p['id'], p['frames']) for p in pieces], len(out), 'words')
