"""DS-36 R1 prep: edit list, audio and film-time word map for ONE version.   python3 prep.py scripted|offcuff [--no-audio]
Writes <version>/edl.json, words_out.json, lav.wav, voice-<name>.wav, clip-finished.wav.
(Adapted from DS-43 Terry Crews R2, same roll C1730, same set, mic and day.)

Shared opening (identical in both versions, Bill Maher Codex R5 sequence):
  C1  clip 355.30-358.30  "Fat shaming doesn't need to end. Needs to make a comeback." full screen (fixed portrait window on
                          Bill, face x 948 of 1920, one camera), Dan keyed lower left at 0.40.
  C2  clip 359.92-370.98  "Some amount of shame is good ... Shame is the first step in reform." in the titled panel (Dan large,
                          still watching). Cut out at the layout change: 358.30-359.92 (studio-audience murmur, no speech).
  Dan's real reaction: roll = clip + 182.812 (lav cross-correlation, 5 windows agree to 2 ms).
  Then the response starts in the same panel layout (clip continues silently from 370.98) and the field section follows.

Talk pieces: every cut sits in a measured pause (audio/takes_db10ms.npy, medium.en words audio/*_words.json, spot pass
audio/spots.json). Pause trims happen only at a shot change (zoom cut, layout change or cutaway), never as a naked jump.
"""
from pathlib import Path
import json, subprocess, sys, os, re
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
CLIP = W/'src/maher_full.mkv'
ROLL_MINUS_CLIP = 182.812
VERSION = sys.argv[1]; assert VERSION in ('scripted', 'offcuff')
O = W/VERSION; O.mkdir(exist_ok=True); (O/'audio').mkdir(exist_ok=True)
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)
def fr(t): return int(round(t*FPS))

# R2 (Dan, 2026-11-05: "cut D2, D4 and D5, keep D1 and D6, cut the pauses, and cut Bill's line 'We shame them out of littering'"):
#   C1 'Fat shaming doesn't need to end. Needs to make a comeback.' (ends in silence at 358.30)
#   C2 the audience murmur from 359.50 (60 ms fade-in; it runs straight into 'Some') .. 'seat belts.' (365.45, before 'We' 365.47)
#   C3 'Shame is the first step in reform.' from 368.88 (quiet before 'Shame' 368.94); 'We shame them out of littering and most of
#      them out of racism.' (365.45-368.88) is cut, at a zoom cut on Dan watching (PW1 -> PW2)
CLIP_SEGS = [('C1', 355.30, 358.30), ('C2', 359.86, 365.45), ('C3', 368.88, 370.98)]   # R2 review: C2 starts just before the 'S' of 'Some' (359.90); no murmur left
CLIP_FADE_IN = {'C2': 0.02}
LAYOUT_CUT = None   # the full-screen -> panel change is the C1/C2 join
# id, roll in, roll out. Piece 1 plays over the silent panel (one continuous piece; the panel -> field change is a cut inside it).
TALK = {
    'scripted': [
        # "Bill Maher is right here. Fat shaming is good. Being over fat is a serious failure of character."  (slate before it cut)
        ('P1', 572.80, 579.45),
        # "And someone who is over fat should feel a deep sense of healthy shame."
        ('P2', 579.70, 583.85),
        # "Shame works, but fat shaming other people is a pointless waste of energy."
        ('P3', 584.22, 588.05),
        # restart cut: "Instead, you should be fat shaming. yourself if you want to instead you should be fat sha-" (588.05-595.58) ->
        # "instead you should be fat shaming yourself if you get above your goal weight. Here's how. First weigh yourself every
        # morning and if you get more than three pounds over your goal weight force yourself to feel a deep sense of shame and
        # disappointment that you let yourself down."
        ('P4', 595.42, 609.98),
        # "Then lock in and focus on cutting your calories until you're back at the goal."
        ('P5', 610.18, 614.02),
        # "Second start doing standing vacuums in the mirror every morning."
        ('P6', 614.50, 617.86),
        # "This will force you to look at yourself shirtless for a few minutes every day, increasing the healthy shame you feel if you get too fat."
        ('P7', 618.18, 625.05),
        # "And vacuums will actually make your belly bulge out less."
        ('P8', 625.42, 628.08),
        # "Subscribe and go to sixpackabs.com for all my newest videos."
        ('P9', 628.38, 631.45)],
    'offcuff': [
        # "Bill Maher is right. ... But there's no need for you to be fat shaming other people. That's just cruel and there's no point
        # to doing it. Because those people aren't going to change anyway."   (D1 kept, Dan R2)
        ('P1', 646.66, 655.92),
        # "Instead, you should be fat shaming yourself. And here's how to do it: weigh in every single morning."  (starts before his breath)
        ('P2', 655.98, 662.38),   # R2 build 3 review: ~0.25 s pause before 'If' again (tail sits under the scale cutaway)
        # "If you get more than three pounds above your goal weight, make yourself feel a deep sense of healthy shame."
        ('P3a', 666.95, 672.80),
        # D2 cut ("That is good." 672.99-673.48):  "That's what's gonna get you back on track."  ('That's' 673.82)
        ('P3b', 673.70, 675.50),
        # "Feel that shame when you're only a little bit over your goal weight rather than 20 or 30 pounds,"  (mouth click at 678.346 faded)
        ('P4a', 678.33, 682.68),
        # R2 review: 682.59-682.66 is the 's' of 'pounds' (kept); the pause cut takes only the breath gap 682.70-682.93 and keeps the
        # spoken 'and' (683.01).  Was: the drawn-out 'and' (682.61-682.66) and its gaps go:  "then use that shame as motivation to lock in, get your diet
        # handled, get your workouts handled,"  ('th' from 682.80)
        ('P4b', 682.93, 689.10),
        # D4 cut ("and make sure you get back to goal weight as soon as possible." 689.08-691.84): "Shame can be healthy,"  (from his breath)
        ('P4c', 691.88, 693.30),
        # D5 cut ("shame can be good," 693.51-694.32): "and shame can literally save your life if it's shame about belly fat. You should be
        # ashamed if you let yourself down, but don't be ashamed forever and just not do anything about it."
        ('P4d', 694.52, 703.80),
        # "Use that shame as motivation, as a fuel you'll need to get back on track, and then you'll start feeling good about yourself for
        # the rest of your life. So subscribe and go to sixpackabs.com for all my latest videos."   (D6 kept, Dan R2)
        ('P5', 707.46, 717.19)],
}[VERSION]
KEY = dict(watchF=537.50, T=dict(scripted=572.40, offcuff=646.40)[VERSION])
XF = 0.010            # 10 ms crossfade at every voice join, each inside a measured dip
# R2 (Dan: under 60 s through cuts and acceleration): his reply plays SPEED x faster, pitch kept (ffmpeg atempo); Bill's clip stays 1x.
# 53.87 s of reply / 1.13 = 47.67 s + 11.05 s of clip = 58.7 s.
SPEED = 1.12 if VERSION == 'offcuff' else 1.0
# R2 review: breaths back at three joins (P3a 666.85-672.80, P3b from 673.70, P4c from 691.88 on the rise of 'sh'), the 's' of
# 'pounds' kept, C2 tightened: 54.22 s of reply / 1.12 = 48.41 + 10.69 s of clip = 59.1 s. The HF 'swirl' rise of a faster voice is
# the speech rate itself: Praat PSOLA, an artifact-free speech stretch, raises it the same 10-11 %; atempo measured no worse.

segs = []; n = 0
for sid, a, b in CLIP_SEGS:
    k = fr(b - a); segs.append(dict(id=sid, clip_in=a, frames=k, n0=n, film0=n/FPS)); n += k
CLIP_FRAMES = n
pieces = []
for pid, a, b in TALK:
    k = fr((b - a)/SPEED); pieces.append(dict(id=pid, key='T', source=SRC, start=a, src_end=b, speed=SPEED, frames=k, duration=k/FPS, n0=n, film0=n/FPS)); n += k
TOTAL = n
edl = dict(version=VERSION, fps='30000/1001', speed=1.0, total_frames=TOTAL, total_seconds=TOTAL/FPS,
           clip=dict(file=str(CLIP), segs=segs, frames=CLIP_FRAMES, layout_cut_film=(fr(LAYOUT_CUT)/FPS if LAYOUT_CUT else None), roll_minus_clip=ROLL_MINUS_CLIP, panel_silent_from=370.98),   # the clip simply continues, silent, from its last spoken frame (one camera, no repeat of the quote)
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
TAKE_EQ = {'scripted': ',deesser=i=0.4:m=0.5:f=0.5,equalizer=f=3500:t=q:w=1.0:g=-1.5,equalizer=f=5500:t=q:w=1.0:g=-1.5',
           'offcuff': ',equalizer=f=900:t=q:w=1.4:g=+2.5,equalizer=f=3500:t=q:w=2.5:g=-3.5,equalizer=f=250:t=q:w=1.4:g=-1'}[VERSION]
VOICES = {'house_bass15': dict(eq=E_EQ + TAKE_EQ, expander=True), 'balanced': dict(eq=BAL, expander=False)}

if '--no-audio' not in sys.argv:
    parts = []
    for i, p in enumerate(pieces):
        last = i == len(pieces) - 1
        d = p['duration'] + (0 if last else XF)          # film seconds this piece fills (plus the crossfade overlap)
        sd = d*SPEED                                      # source seconds read
        af = 'pan=mono|c0=c0' + (f',atempo={SPEED}' if SPEED != 1 else '') + (f",apad,atrim=duration={d:.6f}" if SPEED != 1 else '') \
             + (f",afade=t=out:st={d-0.03}:d=0.03" if last else '')   # R1 review: a 60 ms fade ate the final 's' of 'videos'
        # R1 review build 6/7: a source mouth click 16-22 ms into off-cuff P4 (678.346, right after the S3/S4 cut); a 35 ms fade only softened it, so
        # removes it without touching 'Feel' (678.62). Timeline unchanged.
        if VERSION == 'offcuff' and p['id'] in ('P4', 'P4a'): af += ',afade=t=in:st=0.025:d=0.015'   # build 8: silent through the click (16-22 ms), full by 40 ms; breath at 70 ms + (',afade=t=in:d=0.006' if i == 0 else '')
        ff(['-ss', p['start'], '-i', SRC, '-t', sd + 0.05, '-map', '0:a:0', '-af', af, '-ar', 48000, '-c:a', 'pcm_s24le', O/'audio'/f"lav-{p['id']}.wav"])
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
            f"afade=t=in:d={CLIP_FADE_IN.get(s['id'], 0.015)},afade=t=out:st={d-(0.10 if s is segs[-1] else 0.015)}:d={0.10 if s is segs[-1] else 0.015}", '-ar', 48000, '-c:a', 'pcm_s24le', p])   # R1 review: 100 ms tail fade into Dan's quieter room
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
    a, b = p['start'], p['start'] + p['duration']*p['speed']
    for w in dw:
        if w['e'] <= a or w['t'] >= b or (min(w['e'], b) - max(w['t'], a)) < 0.5*(w['e'] - w['t']): continue
        out.append(dict(w=w['w'], t0=round((max(w['t'], a) - a)/p['speed'] + p['film0'], 3), t1=round((min(w['e'], b) - a)/p['speed'] + p['film0'], 3), src=w['t'], piece=p['id'], speaker='dan', fixed=bool(w.get('fixed'))))
FIX = {'6packabs': 'SixPackAbs', 'sixpackapps': 'SixPackAbs', 'sixbackapps': 'SixPackAbs', 'sixpackabs': 'SixPackAbs'}   # spelled as in his script
for w in out:
    k_ = w['w'].lower().rstrip('.,')
    if k_ in FIX: w['w'] = FIX[k_]
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
