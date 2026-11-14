"""DS-41 R1 prep: edit list, audio and film-time word map for ONE version.   python3 prep.py scripted|offcuff [--no-audio]
Writes <version>/edl.json, words_out.json, lav.wav, voice-<name>.wav, clip-finished.wav.
(Adapted from DS-36 Fat Shaming R1, same roll C1730, same set, mic and day.)

Shared opening (identical in both versions, Bill Maher Codex R5 sequence). The clip: JRE Clips "Kevin James on Cheat Days and
Losing 60lbs After Fasting for 41 Days" (tX5ZQ8rfHzY), the two pieces Dan's shoot doc names (0:41-0:49, 0:58-1:07), one camera:
  C1  clip 41.40-47.78  "You could work out like six days a week and just have one day to eat what you want." full screen (fixed
                        portrait window on Kevin James), Dan keyed lower left at 0.40.
  C2  clip 58.25-65.90  "Because your one day is gonna destroy everything. And he said, and I remember this, he goes, you can't
                        outwork a bad diet. And he was right." in the titled panel (Dan large, still watching).
  The full-screen -> panel layout change sits ON the clip's own edit (C1|C2), so the skip inside the quote is never a jump cut.
  Dan's real reaction: his FIRST viewing, roll = clip + 1566.872 (lav cross-correlation, 10 windows agree to 2 ms). He looks up
  at the lens and opens both hands on "destroy everything", then grins. (He replayed piece 2 at roll = clip + 1595.967 with a
  hand on the laptop; not used.)
  Then the response starts in the same panel layout (clip continues silently from 65.90, same camera to 82.5) and the field follows.

Talk pieces: every cut sits in a measured pause (audio/takes_db10ms.npy, medium.en words audio/*_words.json, spot pass
audio/spots.json). Pause trims happen only at a shot change (zoom cut, layout change, card or cutaway), never as a naked jump.
"""
from pathlib import Path
import json, subprocess, sys, os, re
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
CLIP = W/'src/kevin_full.mkv'
ROLL_MINUS_CLIP = 1566.872
VERSION = sys.argv[1]; assert VERSION in ('scripted', 'offcuff')
O = W/VERSION; O.mkdir(exist_ok=True); (O/'audio').mkdir(exist_ok=True)
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)
def fr(t): return int(round(t*FPS))

CLIP_SEGS = [('C1', 41.68, 47.78), ('C2', 58.55, 65.90)]
PANEL_SILENT_FROM = 65.90
# id, roll in, roll out. Piece 1 plays over the silent panel.
TALK = {
    'scripted': [
        # false start cut ("Okay, Kevin James's... Alright," 1670.9-1674.0):
        # "Kevin James's trainer sounds like a smart guy and he is right about this. Let's talk about why."
        ('P1', 1674.055, 1678.80),
        # "So, let's say you cut 500 calories a day for 6 days. At the end of those 6 days, you're down about 3,000 calories. But one
        # big cheat day can easily put you in a 3,000 calorie surplus. So you did six days of hard work and you're right back where
        # you started."   ('surplus' ends on its s at 1690.30; 'So' starts 1690.63)
        ('P2', 1679.08, 1694.54),
        # "The math behind cheat days simply doesn't work. And if you haven't lost any weight while doing cheat days, this is the reason why."
        ('P3', 1694.79, 1701.90),
        # "If you want a treat, that's fine. Just fit it inside that day's calories. But you can't ever have a day where you just eat
        # any high calorie food you want without tracking."
        ('P4', 1702.18, 1710.90),
        # "Remember, ripped guys occasionally have a cheat meal. Fat guys diet all week and then have a cheat day and then make zero
        # progress."   ('progress' ends on its s at 1718.78)
        ('P5', 1711.30, 1718.84),
        # "If you're ready to start losing your belly fat, subscribe to my channel for more workout and nutrition tips."
        ('P6', 1719.15, 1724.08)],
    'offcuff': [
        # "Okay," cut (1730.9-1731.0): "Kevin James and his trainer are absolutely right about this. One single cheat day can outweigh
        # six days of hard dieting and I'll explain why with math."
        ('P1', 1731.18, 1740.49),
        # "So let's say you diet for six days, you have a 500 calorie deficit in each day, 3,000 calorie total deficit."
        ('P2', 1740.50, 1747.52),
        # "On that one cheat day, you can"   (repeat cut: the first "easily," 1749.39-1749.92)
        ('P3', 1747.53, 1749.33),
        # "easily have a 3,000 calorie or more surplus if you're not tracking."
        ('P4', 1750.10, 1754.69),
        # "So guys, this concept of a cheat day does not work mathematically."
        ('P5', 1754.70, 1758.76),
        # restart cut ("If you have a cheat day, even if you're dieting hard all," 1759.0-1761.45):
        # "if you have a cheat day, even if you're dieting hard all the other six days, then you're not going to lose any weight most likely."
        ('P6', 1762.33, 1767.86),
        # "So I would say just make it one cheat meal and not a cheat day. And whether you're doing a cheat meal or cheat day, if you
        # don't follow my advice, track your calories,"
        ('P7', 1767.87, 1777.60),
        # restart cut ("and you'll find if you're actually tracking your calories, and" 1777.65-1780.22, the second "and" is drawn out
        # and followed by a 0.65 s stall): "you'll find if you're actually tracking your calories while you're going hog wild for an
        # entire day, you're eating 6,000, 7,000, 8,000 calories in one day, and you'll realize why you can never do that again."
        ('P8', 1780.865, 1791.70),   # (in-point stays in the 20 ms dip between his in-breath and "You'll")
        # "So no cheat days, make it a cheat meal only, and still track when you cheat."
        ('P9', 1791.71, 1795.70),
        # his second read of the subscribe line (last clean take; the first is 1796.05-1798.37):
        # "Subscribe to my channel for more workout and nutrition tips."
        ('P10', 1800.94, 1803.80)],
}[VERSION]
# the talk take is keyed only where Dan is on screen (run_key.sh, key_subs.json): [name, roll start, seconds]
_subs = json.load(open(Path(__file__).resolve().parent/'key_subs.json'))
KEY = dict(watchA=1608.00, watchB=1624.92, T=[[k, a, d] for k, (a, d) in _subs.items() if k[0] == dict(scripted='S', offcuff='O')[VERSION]])
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
           clip=dict(file=str(CLIP), segs=segs, frames=CLIP_FRAMES, layout_cut_film=segs[1]['film0'], roll_minus_clip=ROLL_MINUS_CLIP, panel_silent_from=PANEL_SILENT_FROM),   # the clip simply continues, silent, from its last spoken frame (one camera, no repeat of the quote)
           pieces=pieces, key=KEY)
(O/'edl.json').write_text(json.dumps(edl, indent=1))

# Voice: the exact voice Dan approved on this set, mic and day (DS-44B Hormozi off-cuff R2 = DS-40 Claude house EQ fitted on
# C1730 + a half bass lift, expander on), level matched to -14.1 LUFS by the shared chain. Balanced kept as the A/B alternative.
E_EQ = ('highpass=f=70,equalizer=f=110:t=q:w=1.3:g=-5.89,equalizer=f=194:t=q:w=1.3:g=+0.46,equalizer=f=316:t=q:w=1.3:g=+1.95,'
        'equalizer=f=490:t=q:w=1.3:g=+2.44,equalizer=f=735:t=q:w=1.3:g=+1.63,equalizer=f=1122:t=q:w=1.3:g=+1.21,'
        'equalizer=f=1755:t=q:w=1.3:g=+1.12,equalizer=f=2775:t=q:w=1.3:g=+0.55,equalizer=f=4387:t=q:w=1.3:g=-3.65,'
        'treble=g=-1.65:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+1.5')
BAL = 'highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
# R1 review (audio gate, voice alone): the scripted take is bright at 3.5/5.5 kHz (about 25 'shame/shaming' sibilants), the off-cuff
# take is thin at 900 Hz and bright at 3.5 kHz. A per-take match to his reference voice, measured with audio_gate --reference-rows-only:
# scripted 1.55/4.18 -> 0.99/1.83, off the cuff 1.17/3.55 -> 1.15/2.29 (limits 1.2/2.5), no processing-damage or comb row raised.
TAKE_EQ = {'scripted': ',equalizer=f=3500:t=q:w=1.0:g=-1.0,equalizer=f=5500:t=q:w=1.0:g=-0.5,equalizer=f=900:t=q:w=1.0:g=1.0', 'offcuff': ',equalizer=f=3500:t=q:w=2.0:g=-1.2,equalizer=f=6000:t=q:w=1.5:g=2.0,equalizer=f=150:t=q:w=1.0:g=1.0'}[VERSION]   # DS-41: fitted only if the voice-alone gate rows ask for it (see notes)
VOICES = {'house_bass15': dict(eq=E_EQ + TAKE_EQ, expander=True), 'balanced': dict(eq=BAL, expander=False)}

if '--no-audio' not in sys.argv:
    parts = []
    for i, p in enumerate(pieces):
        last = i == len(pieces) - 1
        d = p['duration'] + (0 if last else XF)
        af = 'pan=mono|c0=c0' + (f",afade=t=out:st={d-0.03}:d=0.03" if last else '')   # R1 review: a 60 ms fade ate the final 's' of 'videos'
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
        d = s['frames']/FPS; p = O/'audio'/f"clip-{s['id']}.wav"; fo = 0.10 if s is segs[-1] else 0.04
        if s is segs[0]:
            ff(['-ss', s['clip_in'], '-i', CLIP, '-t', d, '-map', '0:a:0', '-af', f'pan=mono|c0=0.5*c0+0.5*c1,aresample=48000,apad,atrim=duration={d},'
                f'afade=t=in:d=0.015,afade=t=out:st={d-fo}:d={fo}', '-ar', 48000, '-c:a', 'pcm_s24le', p])   # R1 review: 100 ms tail fade into Dan's quieter room
        else:
            # review 2: the two pieces ran together (50 ms). Piece 2's picture starts 0.22 s before "your"; its own sound (the end of a
            # "'cause he's" false start) is held out until 58.765 and a room-tone bed at the clip's measured floor (about -60 dB) fills the gap
            # (review 2, build 6: pink noise read 10 dB bright at 1-2 kHz against Kevin's room; brown noise high-passed at 60 Hz matches its bands within about 3 dB)
            HOLD = 0.215
            ff(['-ss', s['clip_in'], '-i', CLIP, '-f', 'lavfi', '-i', f'anoisesrc=color=brown:amplitude=0.0033:duration={HOLD + 0.03}:sample_rate=48000,highpass=f=60', '-t', d, '-filter_complex',
                f'[0:a:0]pan=mono|c0=0.5*c0+0.5*c1,aresample=48000,apad,atrim=duration={d},afade=t=in:st={HOLD}:d=0.015,afade=t=out:st={d-fo}:d={fo}[v];'
                f'[1:a]afade=t=in:d=0.02,afade=t=out:st={HOLD}:d=0.03[n];[v][n]amix=inputs=2:normalize=0:duration=first[o]', '-map', '[o]', '-ar', 48000, '-c:a', 'pcm_s24le', p])
        cparts.append(p)
    (O/'audio'/'clip.txt').write_text(''.join(f"file '{p}'\n" for p in cparts))
    ff(['-f', 'concat', '-safe', 0, '-i', O/'audio'/'clip.txt', '-c', 'copy', O/'audio'/'clip-raw.wav'])
    # DS-43 method (two gentle compressors at 4x rate, no limiter: DS-33 lesson), then plain gain to about the voice level,
    # capped so the peak stays under -1.5 dBFS. Measured values: audio/clip-level.json.
    ff(['-i', O/'audio'/'clip-raw.wav', '-af', 'aresample=192000,acompressor=threshold=0.05:ratio=3:attack=10:release=200:knee=6,'
        'acompressor=threshold=0.1:ratio=10:attack=0.02:release=30:knee=3,aresample=48000', '-c:a', 'pcm_s24le', O/'clip-original.wav'])   # Real Time's mix: PLR 17 -> 12.9, lands at -14.5 LUFS (R5 clip -14.2)
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
dw = json.load(open(W/f'audio/{VERSION}_words.json'))
spots = json.load(open(W/'audio/spots.json')) if (W/'audio/spots.json').exists() else {}
DW_FIX = json.load(open(W/f'audio/{VERSION}_wordfix.json')) if (W/f'audio/{VERSION}_wordfix.json').exists() else {}
# DW_FIX: {"drop": [t,...], "text": {"t": "word"}, "add": [[w, t, e]]}  (keys: word start rounded to 2 dp)
drop = set(DW_FIX.get('drop', [])); text = DW_FIX.get('text', {})
dw = [dict(x, w=text.get(f"{round(x['t'], 2):.2f}", x['w'])) for x in dw if round(x['t'], 2) not in drop]
dw += [dict(w=w, t=t, e=e, fixed=True) for w, t, e in DW_FIX.get('add', [])]   # hand-measured times: never snapped
dw.sort(key=lambda x: x['t'])
# R1 gate (captions:sync): Whisper stretches some word starts back into the pause before them ('And here's how' sat 0.6 s early).
# Snap each word's start to the lav's speech onset (first 10 ms bin over -42 dB inside the word) when it is more than 0.12 s later.
_db = np.load(W/'audio/takes_db10ms.npy'); _T0 = float(open(W/'audio/takes_db10ms.t0').read())
for x in dw:
    i0, i1 = int((x['t'] - _T0)*100), int((x['e'] - _T0)*100)
    if 0 <= i0 < i1 <= len(_db) and not x.get('fixed'):
        hit = np.where(_db[i0:i1] > -42)[0]
        if len(hit) and hit[0]/100 > 0.12: x['t'] = round(_T0 + (i0 + hit[0])/100 - 0.03, 3)
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in dw:
        if w['e'] <= a or w['t'] >= b or (min(w['e'], b) - max(w['t'], a)) < 0.5*(w['e'] - w['t']): continue
        out.append(dict(w=w['w'], t0=round(max(w['t'], a) - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['t'], piece=p['id'], speaker='dan', fixed=bool(w.get('fixed'))))
FIX = {'6packabs': 'SixPackAbs', 'sixpackapps': 'SixPackAbs', 'sixbackapps': 'SixPackAbs', 'sixpackabs': 'SixPackAbs'}   # spelled as in his script
for w in out:
    k_ = w['w'].lower().rstrip('.,')
    if k_ in FIX: w['w'] = FIX[k_]
k = 0
while k < len(out) - 1:          # "3" ",000" -> "3,000" (Whisper splits the number); any token that starts with punctuation joins the previous word
    if out[k + 1]['w'][:1] in ',.%' and out[k]['piece'] == out[k + 1]['piece']:
        out[k]['w'] += out[k + 1]['w']; out[k]['t1'] = out[k + 1]['t1']; del out[k + 1]
    else: k += 1
k = 0
while k < len(out) - 1:          # "over" "fat" -> "overfat" (his script's word, R1 review)
    if out[k]['w'].lower() == 'over' and out[k + 1]['w'].lower().startswith('fat') and out[k]['piece'] == out[k + 1]['piece'] and out[k]['speaker'] == 'dan':
        out[k]['w'] = 'overfat' + out[k + 1]['w'][3:]; out[k]['t1'] = out[k + 1]['t1']; del out[k + 1]
    else: k += 1
k = 0
while k < len(out) - 1:          # "sixpackabs" ".com" -> one word
    if out[k + 1]['w'].startswith('.com') and out[k]['piece'] == out[k + 1]['piece']:
        out[k]['w'] += out[k + 1]['w']; out[k]['t1'] = out[k + 1]['t1']; del out[k + 1]
    else: k += 1
(O/'words_out.json').write_text(json.dumps(out, indent=1))
print('PREP', VERSION, 'frames', TOTAL, round(TOTAL/FPS, 3), 's; clip', CLIP_FRAMES, [(p['id'], p['frames']) for p in pieces], len(out), 'words')
