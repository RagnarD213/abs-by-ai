"""RO-21 round 1 EDL: draft take list (plan/edl_draft.json) -> cut points placed on word edges (medium.en words, small-model
words where medium merged takes) and validated on the lav's quietest 10 ms inside the gap. Writes round1/edl_r1.json
(pieces with src in/out, film in/out, frame exact) and round1/film_words.json (Dan's words on the film timeline)."""
import json, numpy as np, subprocess
B = '/Volumes/Expansion/_edit_work/RO-21'; FPS = 30000 / 1001
P = json.load(open(f'{B}/plan/edl_draft.json'))
WM = json.load(open(f'{B}/audio/words_medium.json'))
WS = [dict(w=w['word'].strip(), t0=w['start'], t1=w['end']) for w in json.load(open(
    '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1724.roll/words.json'))['words']]
SMALL_ONLY = [(399.0, 415.0), (421.9, 432.6)]          # medium.en merged the two "63 degrees" takes here; the small model kept them apart
raw = subprocess.run(['/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real', '-v', 'error', '-i',
                      f'{B}/audio/lav_full.wav', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.float32); hop = 160
env = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same')[::hop]) + 1e-9)   # 10 ms RMS, dBFS
def quiet(a, b):
    i0, i1 = int(a * 100), max(int(a * 100) + 1, int(b * 100))
    k = i0 + int(np.argmin(env[i0:i1])); return k / 100, float(env[k])
def words(a, b):
    use_small = any(s0 <= a < s1 for s0, s1 in SMALL_ONLY)
    W = WS if use_small else WM
    return [w for w in W if w['t0'] >= a - 0.35 and w['t0'] < b - 0.05], ('small' if use_small else 'medium')
MERGE = 0.7                            # a source gap shorter than this between kept pieces is kept (no time removed, no cut)
spans = []
for k, p in enumerate(P):
    ws, src = words(p['t0'], p['t1'])
    if p['t0'] == 204.42: ws = [w for w in WM if 204.0 <= w['t0'] < 228.0]          # ends on "mat." (227.98)
    w0, w1 = ws[0]['t0'], ws[-1]['t1']
    i, li = quiet(w0 - 0.30, w0 - 0.04)
    o, lo = quiet(w1 + 0.04, w1 + 0.30)
    if spans and w0 - spans[-1]['w1'] < MERGE + 0.2 and i - spans[-1]['o'] < MERGE:
        L = spans[-1]; L.update(o=o, lo=lo, w1=w1, last=ws[-1]['w'], ws=L['ws'] + ws, note=L['note'] + ' | ' + p['note'])
    else:
        spans.append(dict(i=i, li=li, o=o, lo=lo, w1=w1, first=ws[0]['w'], last=ws[-1]['w'], ws=ws, src=src, note=p['note']))
OVR = {0: dict(o=62.98), 1: dict(i=66.05)}   # Gemini listen 2026-10-28 (twice): the 0/1 join cut a breath in half; end take 1 right
                                             # after "abs." (before its breath) and start take 2 on its own whole inhale, just after a lip click
for k, v in OVR.items(): spans[k].update(v)
out, film, t = [], [], 0.0
for k, s in enumerate(spans):
    fi, fo = round(s['i'] * FPS), round(s['o'] * FPS); n = fo - fi
    out.append(dict(k=k, src_in=fi / FPS, src_out=fo / FPS, f_in=fi, f_out=fo, film_in=t, film_out=t + n / FPS,
                    first=s['first'], last=s['last'], in_db=round(s['li'], 1), out_db=round(s['lo'], 1), words_from=s['src'], note=s['note']))
    seen = set()
    for w in s['ws']:
        if w['t0'] in seen: continue
        seen.add(w['t0'])
        film.append(dict(w=w['w'], t0=round(t + w['t0'] - fi / FPS, 3), t1=round(t + w['t1'] - fi / FPS, 3), src_t0=w['t0']))
    t += n / FPS
json.dump(out, open(f'{B}/round1/edl_r1.json', 'w'), indent=1)
json.dump(film, open(f'{B}/round1/film_words.json', 'w'), indent=1)
for e in out: print(f"{e['k']:2d} {e['src_in']:7.2f}-{e['src_out']:7.2f} film {e['film_in']:6.2f}-{e['film_out']:6.2f} {e['in_db']:6.1f}/{e['out_db']:6.1f} {e['first']} .. {e['last']}")
print('film length', round(t, 2), 's =', round(t / 60, 2), 'min')
