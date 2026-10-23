"""DS-44 R1 prep: edit list, audio (lav pieces, voice options, the clip's own sound), film-time word map.

Clip: The Iced Coffee Hour, "Alex Hormozi's advice on weight control" (YouTube 37mqHjJOS50), downloaded 1080p 24 fps as
src/hormozi_140-220.mkv (YouTube 140-220 s; CLIP TIMES BELOW ARE SECONDS INTO THAT FILE). Reaction-clips doc window 2:51-3:10
("I'll ask you a better question: why aren't you 200 pounds heavier?" .. "you just stop at the wrong point").
Built from the camera cut into Hormozi at 30.17 ("Why aren't you 200 pounds heavier?" 30.78) to the end of "...you just stop
at the wrong point." (50.86), tightened at two camera changes so the Short stays under 66 s:
  C1 30.20-32.93  Hormozi asks the question (cut before the 0.67 s wide shot of the hosts)
  C2 35.60-40.40  the caller thinks, "Probably because I can't eat that much." / "So you do know how to stop?"
                  (removes 2.7 s of the 4.7 s silence after the question; keeps 1 s of the caller's thinking beat)
  C3 41.45-51.00  "Yes, I believe so." / "Right, so here's what's interesting... you just stop at the wrong point."
                  (removes 1.05 s of the 2 s pause before "Yes")
  TR 51.00-51.53  the clip shrinks away while Dan grows from the corner (16 frames), before the camera cut at 51.59
Camera cuts in the file (scene > 0.25): 30.17 32.96 33.63 38.88 40.55 43.42 51.59. Every edit is a change of camera.
Dan watching (corner): C1730 roll time = clip time + 2162.270 (lav picked up the laptop; cross-correlation, 2 windows agree).
Talk, C1730 scripted take (medium.en re-check, take_s_medium.json; energy measured at every cut):
  A 2268.18-2305.66  "This is a critical insight from Alex Hormozi..." .. "...at the rate you want."
                      The line was read twice; the first read (2257-2265.7) broke off at "fans have," -> the second read.
                      Speech starts 2268.46 (whisper's doubled "this, this" at 2267.86 is room tone).
  B 2307.96-2316.00  "and if you need help stopping eating at a healthy point, try taking Zepbound to make that easy.
                      Subscribe to my channel for more exercise and nutrition insights like this."
                      The first "And if you need help stopping eating," (2306.02-2307.40) was abandoned -> the restart.
                      A click at 2307.92 sits before the in point.
"""
from pathlib import Path
import json, subprocess, sys, os, re
import numpy as np
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); A = R/'.claude/skills/_shared/audio'; FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
CLIP = W/'src/hormozi_140-220.mkv'
ROLL_MINUS_CLIP = 2162.270
def ff(x): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, x)), check=True)
def fr(t): return int(round(t*FPS))

CLIP_SEGS = [('C1', 30.20, 32.32), ('C2', 36.12, 40.40), ('C3', 41.45, 50.45)]
# build 4 (delivery gate junk:dead_air 1.44 s at the clip -> Dan handover): "wrong point." ends at clip 50.30 by energy (whisper
# said 50.86), so C3 now ends at 50.45, and read 1 starts 0.15 s before "This" (2257.23): silence about 0.83 s.
# build 2 (delivery gate junk:dead_air, 2.06 s > 1.0 s): the silence after "Why aren't you 200 pounds heavier?" is cut to 0.92 s
# at the same camera change (C1 out 0.41 s after the question, C2 in 0.51 s before the caller's answer). Build 1 was
# C1 30.20-32.93, C2 35.60-40.40 (BUILD1_SEGS below converts the clip words transcribed on build 1's timeline).
BUILD1_SEGS = [('C1', 30.20, 32.93), ('C2', 35.60, 40.40), ('C3', 41.45, 51.00)]
TR_FRAMES = 16
# build 3 (independent review 1): Dan looked down at the laptop through "This is a" in read 2. The line now opens on READ 1,
# eyes on camera ("This is a critical insight", 2257.15-2258.85, speech from 2257.38), and joins read 2 at "from Alex Hormozi"
# (2270.07): both cuts sit in the -50 dB dip between "insight" and "from". The transition's sound is read 1's own room tone
# right before it (2256.62-2257.15, -50..-61 dB): build 2's room tone at 2267.10 carried a hiss/exhale (review defect 2).
TALK = [('A0', 2257.23, 2258.85), ('A', 2270.07, 2305.66), ('B', 2307.96, 2316.00)]
KEY = {'watch': 2192.30, 'A0': 2256.90, 'A': 2268.00, 'B': 2307.80}          # key piece starts (recipe/run_key.sh)

segs = []; n = 0
for sid, a, b in CLIP_SEGS:
    k = fr(b - a); segs.append(dict(id=sid, clip_in=a, frames=k, n0=n, film0=n/FPS)); n += k
CLIP_FRAMES = n
tr = dict(id='TR', clip_in=CLIP_SEGS[-1][2], frames=TR_FRAMES, n0=n, film0=n/FPS); n += TR_FRAMES
pieces = []
for pid, a, b in TALK:
    k = fr(b - a); pieces.append(dict(id=pid, source=SRC, start=a, frames=k, duration=k/FPS, n0=n, film0=n/FPS)); n += k
TOTAL = n
edl = dict(fps='30000/1001', total_frames=TOTAL, total_seconds=TOTAL/FPS, clip=dict(file=str(CLIP), segs=segs, frames=CLIP_FRAMES,
           roll_minus_clip=ROLL_MINUS_CLIP), tr=tr, pieces=pieces, key=KEY)
(W/'edl.json').write_text(json.dumps(edl, indent=1))

O = W/'audio'; O.mkdir(exist_ok=True)
# Voice options (both level matched by the chain to -14.1 LUFS):
#  E = the exact voice Dan picked for Bill Maher Fat 90-Year-Old on this set, mic and day (house EQ fitted on that take
#      + a half bass lift, +1.5 dB at 120 Hz, expander on; DS-40 decisions.json, 2026-10-20). Recommended.
#  BAL = "Balanced" (Codex's Bill Maher R3 voice, used on Ronaldo Ab Belt R1), no expander.
E_EQ = ('highpass=f=70,equalizer=f=110:t=q:w=1.3:g=-5.89,equalizer=f=194:t=q:w=1.3:g=+0.46,equalizer=f=316:t=q:w=1.3:g=+1.95,'
        'equalizer=f=490:t=q:w=1.3:g=+2.44,equalizer=f=735:t=q:w=1.3:g=+1.63,equalizer=f=1122:t=q:w=1.3:g=+1.21,'
        'equalizer=f=1755:t=q:w=1.3:g=+1.12,equalizer=f=2775:t=q:w=1.3:g=+0.55,equalizer=f=4387:t=q:w=1.3:g=-3.65,'
        'treble=g=-1.65:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+1.5')
BAL = 'highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
VOICES = {'house_bass15': dict(eq=E_EQ, expander=True), 'balanced': dict(eq=BAL, expander=False)}
ROOM = (2267.10, 2267.10 + TR_FRAMES/FPS)          # room tone under the transition (measured -48..-60 dB, no speech)
XF = 0.04                                          # A -> B: 40 ms crossfade in room tone (DS-33 lesson: no hole after a breath)

if '--no-audio' not in sys.argv:
    pass   # audio only: run under renderq.py run --light
    A0_, A_, B_ = pieces; lead = TR_FRAMES/FPS
    # A0 carries the transition's room tone in front of it (continuous source, no join); A0 -> A and A -> B crossfade 40 ms in room tone
    ff(['-ss', A0_['start'] - lead, '-i', SRC, '-t', lead + A0_['duration'] + XF, '-map', '0:a:0', '-af', 'pan=mono|c0=c0,afade=t=in:d=0.04', '-ar', 48000, '-c:a', 'pcm_s24le', O/'lav-A0.wav'])
    ff(['-ss', A_['start'], '-i', SRC, '-t', A_['duration'] + XF, '-map', '0:a:0', '-af', 'pan=mono|c0=c0', '-ar', 48000, '-c:a', 'pcm_s24le', O/'lav-A.wav'])
    ff(['-ss', B_['start'], '-i', SRC, '-t', B_['duration'], '-map', '0:a:0', '-af', f"pan=mono|c0=c0,afade=t=out:st={B_['duration']-0.05}:d=0.05", '-ar', 48000, '-c:a', 'pcm_s24le', O/'lav-B.wav'])
    ff(['-i', O/'lav-A0.wav', '-i', O/'lav-A.wav', '-i', O/'lav-B.wav', '-filter_complex',
        f'[0:a][1:a]acrossfade=d={XF}:c1=tri:c2=tri[x];[x][2:a]acrossfade=d={XF}:c1=tri:c2=tri[o]', '-map', '[o]', '-ar', 48000, '-c:a', 'pcm_s24le', W/'lav.wav'])
    for name, v in ({} if '--clip-audio-only' in sys.argv else VOICES).items():
        cmd = [sys.executable, str(A/'voice_chain.py'), '--in', str(W/'lav.wav'), '--out', str(W/f'voice-{name}.wav'), '--work', str(O/f'chain-{name}'),
               '--eq', v['eq'], '--target', '-14.1', '--tp', '-1.5', '--oversample', '4']
        if not v['expander']:
            cmd += ['--no-expander-because', 'Balanced as used on Ronaldo Ab Belt R1 (same set, mic and day): no expander, to keep complete word tails.']
        subprocess.run(cmd, check=True)
    # the clip's sound: the same segments as the picture, 15 ms fades (every edit sits in a pause), folded to centred mono,
    # then the transition tail fading out. Plain gain (no limiter: DS-33 lesson, the artifacts row) to about the voice level,
    # capped so the peak stays under -1.5 dBFS.
    parts = []
    for s in segs + [tr]:
        d = s['frames']/FPS; p = O/f"clip-{s['id']}.wav"
        fade = f"afade=t=in:d=0.015,afade=t=out:st={d-0.015}:d=0.015" if s['id'] != 'TR' else f"afade=t=in:d=0.015,afade=t=out:st=0:d={d}"
        if s['id'] == 'C1': fade = f"afade=t=in:st=0.20:d=0.03,afade=t=out:st={d-0.015}:d=0.015"      # the caller's "Okay." tail (0.08-0.16) stays out
        ff(['-ss', s['clip_in'], '-i', CLIP, '-t', d, '-map', '0:a:0', '-af', f'pan=mono|c0=0.5*c0+0.5*c1,apad,atrim=duration={d},{fade}', '-ar', 48000, '-c:a', 'pcm_s24le', p])
        parts.append(p)
    (O/'clip.txt').write_text(''.join(f"file '{p}'\n" for p in parts))
    ff(['-f', 'concat', '-safe', 0, '-i', O/'clip.txt', '-c', 'copy', W/'clip-original.wav'])
    meas = subprocess.run([F, '-hide_banner', '-i', str(W/'clip-original.wav'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas)[-1]); pk = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', meas)[-1])
    g = min(-14.5 - I, -1.5 - pk)
    ff(['-i', W/'clip-original.wav', '-af', f'volume={g:.2f}dB', '-c:a', 'pcm_s24le', '-ar', 48000, W/'clip-finished.wav'])
    (O/'clip-level.json').write_text(json.dumps(dict(I_lufs=I, peak_dbfs=pk, gain_db=round(g, 2)), indent=1))
    (W/'audio-options.json').write_text(json.dumps(VOICES, indent=1))

# ---- words on the film timeline
FIX = {'hormonesy': 'Hormozi', 'hormozi': 'Hormozi', 'hormozi.': 'Hormozi.', 'hormozi,': 'Hormozi,', 'zepbound': 'Zepbound'}
def norm(w):
    k = w.lower()
    if k.strip('.,!?') in ('hormonesy', 'hormozi', 'hormozzi'): return 'Hormozi' + (w[-1] if w[-1] in '.,!?' else '')
    if k.strip('.,!?') == 'zepbound': return 'Zepbound' + (w[-1] if w[-1] in '.,!?' else '')
    return w
out = []
# clip words: medium.en on the clip's sound exactly as it plays in the film (audio/clip_film_words.json, film times).
# The caller's faint "Okay." tail in the first 0.2 s is faded out of the sound (see the clip audio) and left uncaptioned.
# "Right," is heard at 9.37-9.60 (energy burst 9.37-9.80) where whisper gave a zero-length "So": restored. Punctuation as spoken.
cw = json.load(open(W/'audio/clip_film_words.json'))         # transcribed on build 1's clip timeline
# word starts the delivered-audio ASR of build 1 measured later than whisper's stretched starts (captions:sync, my own 82-cue check)
CW_FIX = {('So', 5.64): 5.956, ('You', 11.54): 11.761, ("It's", 13.14): 13.401}
def b1_to_clip(t):
    f0 = 0.0
    for _, a_, b_ in BUILD1_SEGS:
        n = fr(b_ - a_)
        if t < f0 + n/FPS: return a_ + (t - f0)
        f0 += n/FPS
    return BUILD1_SEGS[-1][2] + (t - f0)
def clip_to_film(c):
    for x in segs + [tr]:
        if x['clip_in'] - 1e-6 <= c < x['clip_in'] + x['frames']/FPS: return x['film0'] + (c - x['clip_in'])
    return None
cw2 = []
for w in cw:
    t0 = CW_FIX.get((w['w'], round(w['t0'], 2)), w['t0'])
    c0, c1 = b1_to_clip(t0), b1_to_clip(w['t1'] - 1e-4) + 1e-4
    n0, n1 = clip_to_film(c0), clip_to_film(c1 - 1e-4)
    if n0 is None or n1 is None: continue
    cw2.append(dict(w=w['w'], t0=round(n0, 3), t1=round(n1 + 1e-4, 3)))
cw = cw2
FIXC = {'Yes.': 'Yes,', 'here\'s,': "here's"}
for w in cw:
    if w['w'] == 'Okay.' and w['t0'] < 0.3: continue
    if w['w'] == 'So' and abs(b1_to_clip(9.76) - 0) and abs(w['t0'] - clip_to_film(b1_to_clip(9.76))) < 0.05:
        r0, r1 = clip_to_film(b1_to_clip(9.37)), clip_to_film(b1_to_clip(9.60))
        out.append(dict(w='Right,', t0=round(r0, 3), t1=round(r1, 3), src=None, piece='C3', speaker='clip')); w = dict(w, w='so', t0=round(r1, 3))
    seg = next(x for x in segs + [tr] if x['film0'] - 1e-6 <= w['t0'] < x['film0'] + x['frames']/FPS)
    if w['w'] == 'stop.' and abs(w['t0'] - clip_to_film(b1_to_clip(6.80))) < 0.05: w = dict(w, w='stop?')          # Hormozi's question
    out.append(dict(w=FIXC.get(w['w'], w['w']), t0=w['t0'], t1=w['t1'], src=None, piece=seg['id'], speaker='clip'))
dw = json.load(open(W/'audio/take_s_medium.json'))
# medium.en stretched these word starts back over the pause before them; build 1's delivered-audio ASR put them later/earlier
DW_FIX = {2271.44: 2271.20, 2279.94: 2280.16, 2284.62: 2284.76, 2292.2: 2292.56}
dw = [dict(w, t=DW_FIX.get(round(w['t'], 2), w['t'])) for w in dw]
for p in pieces:
    a, b = p['start'], p['start'] + p['duration']
    for w in dw:
        if p['id'] == 'A0' and w['t'] > 2259.0: continue
        if p['id'] == 'B' and abs(w['t'] - 2307.66) < 0.02:      # "and": energy puts it at 2308.14-2308.28 (whisper 2307.66-2308.22)
            w = dict(w, t=2308.14, e=2308.28)
        if w['e'] <= a or w['t'] >= b or (min(w['e'], b) - max(w['t'], a)) < 0.5*(w['e'] - w['t']): continue
        out.append(dict(w=norm(w['w']), t0=round(max(w['t'], a) - a + p['film0'], 3), t1=round(min(w['e'], b) - a + p['film0'], 3), src=w['t'], piece=p['id'], speaker='dan'))
# A0's first word: speech starts 2257.38 (energy), medium.en put "This" at 2257.00; read 2's "from" starts 2270.15 (energy)
for w in out:
    if w['piece'] == 'A0' and w['w'] == 'This': w['t0'] = round(2257.38 - pieces[0]['start'] + pieces[0]['film0'], 3)
    if w['piece'] == 'A' and w['w'] == 'from' and w['src'] < 2270.2: w['t0'] = round(2270.15 - 2270.07 + pieces[1]['film0'], 3)
# numbers as digits for pounds (the captions read "2 pounds, not 20")
for w in out:
    if w['w'].lower().strip('.,') == 'two': w['w'] = '2' + w['w'][3:]
(W/'words_out.json').write_text(json.dumps(out, indent=1))
print('PREP', TOTAL, round(TOTAL/FPS, 3), 'clip', CLIP_FRAMES, 'tr', TR_FRAMES, [(p['id'], p['frames']) for p in pieces], len(out), 'words')
