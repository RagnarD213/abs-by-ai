"""RO-24 round 2: the whole-film timeline from the round 1 take list (best take of every line, edges on the measured lav envelope).

  python3 edl_film.py            -> round2/edl_film.json (assemble16 format) + round2/film_words.json (words in film seconds)

0. Restarts inside a kept take (Gemini listen + lav envelope, round 2): the first attempt is cut out, from the quietest 40 ms of
   the pause before it to the quietest 40 ms of the pause before the clean restart (RESTARTS, source seconds).
1. Long pauses inside a take: silence is measured on the lav (20 ms RMS more than 20 dB under the take's speech level, so a word
   Whisper stretched over a pause is caught too). Any silence over 0.85 s keeps 0.45 s; the cut sits on the quietest 40 ms at
   each end of the removed stretch. Every such cut is a jump, so it always switches framing.
2. Reframe-only cuts at sentence ends (a word ending . ? !, then at least 0.12 s of silence), on the quietest 40 ms of that gap:
   the first candidate at least 4.5 s into the shot; if none comes by 11 s, any word gap of 0.08 s or more.
3. Framing alternates W / T at every cut and at every take join, so no join is a same-size jump.
"""
import json, subprocess, numpy as np
W = '/Volumes/Expansion/_edit_work/RO-24'
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
FPS = 30000 / 1001; SR = 48000
P = json.load(open(f'{W}/round1/edl_full_takes.json'))['pieces']
# round 2 join fixes from the seam scan + per-join listening + the lav envelope (source frames; take numbers are 1-based):
EDGE = {6: dict(f1=24221),      # "lost about 33." ended 0.12 s into its own decay (-39 dB): end in silence (-51 dB)
        14: dict(f0=30331),     # "Number two": start on the soft breath before it, not 0.12 s ahead of a hard onset
        15: dict(f0=30810),     # "If you can't do that": 0.9 s of dead air after the join, keep 0.3 s before the word
        9: dict(f1=26058),      # "...is mandatory.": the word's tail was still decaying (-37 dB) at the cut; end it in silence
        10: dict(f1=26269)}     # "...taking the drug.": end before the mouth sound and in-breath 60 ms ahead of the old cut
for k, v in EDGE.items(): P[k - 1].update(v)
# takes 7 and 8 are one stretch of the roll ("...start on a low dose." / "Now here's someone"): the 0.5 s cut between them split
# the breath before "Now". Join them into one take: the natural pause and breath stay.
P[6]['f1'] = P[7]['f1']; P[6]['t_out'] = P[7]['t_out']; P[6]['tail'] = P[7]['tail']; MERGED = P.pop(7)
R = json.load(open(f'{W}/round2/key_ranges.json'))
words = json.load(open(f'{W}/round1/audio/words_src.json'))
x = np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-i', f'{W}/round1/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']), np.float32)
HOP = 480                                                   # 10 ms
def rms_db(a, b):
    seg = x[int(a * SR):int(b * SR)]; n = len(seg) // HOP
    fr = seg[:n * HOP].reshape(n, HOP); e = np.sqrt(np.convolve((fr ** 2).mean(1), np.ones(2) / 2, 'same'))
    return 20 * np.log10(e + 1e-9)
def quiet(a, b):
    """centre (s) of the quietest 40 ms inside [a, b]"""
    seg = x[int(a * SR):int(b * SR)]; w = 1920
    if len(seg) <= w: return (a + b) / 2
    e = np.convolve(seg ** 2, np.ones(w) / w, 'valid'); return a + (int(np.argmin(e)) + w / 2) / SR
fr = lambda t: int(round(t * FPS))
RESTARTS = [((682.10, 682.94), (684.60, 685.08), '"But most of the headlines left" said twice (Gemini, round 2)'),
            ((784.60, 785.20), (786.80, 787.70), '"They started with Ozempic, they" restarted (Gemini, round 2)')]
out = []; film_words = []; g = 0; framing = 'T'; cuts_log = []
for pi, p in enumerate(P):
    a, b = p['f0'] / FPS, p['f1'] / FPS
    db = rms_db(a, b); speech = np.percentile(db, 80); sil = db < speech - 20
    # silences (10 ms frames) longer than 0.85 s -> keep 0.45 s
    kept = [(a, b)]
    for (qa, qb), (ra, rb), why in RESTARTS:              # restarts first: the first attempt goes
        if a < qa < b:
            c0, c1 = quiet(qa, qb), quiet(ra, rb)
            kept = [y for sa, sb in kept for y in ([(sa, c0), (c1, sb)] if sa < c0 < sb else [(sa, sb)])]
            cuts_log.append((round(c0, 2), 'restart', round(c1 - c0, 2)))
    segs = []
    for ka, kb in kept:                                   # then long silences, only inside what is kept
        s0 = ka; i0 = int((ka - a) * SR / HOP); i1 = int((kb - a) * SR / HOP); i = i0
        while i < i1:
            if sil[i]:
                j = i
                while j < i1 and sil[j]: j += 1
                dur = (j - i) * HOP / SR
                if dur > 0.85 and i > i0 and j < i1:
                    t_sil0, t_sil1 = a + i * HOP / SR, a + j * HOP / SR
                    cut0 = quiet(t_sil0 + 0.18, t_sil0 + 0.32); cut1 = quiet(t_sil1 - 0.20, t_sil1 - 0.08)
                    segs.append((s0, cut0)); s0 = cut1; cuts_log.append((round(t_sil0, 2), round(dur, 2)))
                i = j
            else: i += 1
        segs.append((s0, kb))
    for si, (sa, sb) in enumerate(segs):
        f0, f1 = (p['f0'] if si == 0 else fr(sa)), (p['f1'] if si == len(segs) - 1 else fr(sb))
        framing = 'W' if framing == 'T' else 'T'                                  # every take join / pause cut switches size
        ws = [w for w in words if w['t0'] >= f0 / FPS - .05 and w['t1'] <= f1 / FPS + .05]
        shots = [{'f0': f0, 'framing': framing}]; last = f0 / FPS
        for k, w in enumerate(ws[:-1]):
            nxt = ws[k + 1]; gap = nxt['t0'] - w['t1']; since = w['t1'] - last
            sentence = w['w'].rstrip('"”\'').endswith(('.', '?', '!')) and gap >= 0.12
            mins = 3.0 if g / FPS + w['t1'] - f0 / FPS < 30 else 4.5      # the hook cuts faster (round 1's first 30 s)
            if (sentence and since >= mins) or (since >= 11 and gap >= 0.08):
                if (f1 / FPS) - nxt['t0'] < 2.5: continue                          # no shot shorter than 2.5 s at the end
                t = quiet(w['t1'], nxt['t0']); framing = 'W' if framing == 'T' else 'T'
                shots.append({'f0': fr(t), 'framing': framing}); last = t
        rk = [r for r in R if r['f0'] <= f0 and f1 <= r['f0'] + r['n']]
        assert rk, ('no key range covers', f0, f1)
        key = f"{W}/round2/key/{rk[0]['name']}.mkv"
        if pi == 0 and si == 0:          # the hook keeps round 1's independently checked cut plan (5 shots, 3.6-7.6 s)
            shots = [{'f0': 16088, 'framing': 'W'}, {'f0': 16267, 'framing': 'T'}, {'f0': 16375, 'framing': 'W'},
                     {'f0': 16537, 'framing': 'T'}, {'f0': 16765, 'framing': 'W'}]; framing = 'W'
        out.append({'id': f'P{len(out) + 1:02d}', 'take': pi + 1, 'f0': f0, 'f1': f1, 'key': key,
                    'text': (ws[0]['w'] + ' ... ' + ws[-1]['w']) if ws else '', 'shots': shots})
        for w in ws:
            film_words.append({'w': w['w'], 't0': round(g / FPS + w['t0'] - f0 / FPS, 3), 't1': round(g / FPS + w['t1'] - f0 / FPS, 3),
                               'src': w['t0'], 'piece': out[-1]['id']})
        g += f1 - f0
json.dump({'note': 'RO-24 round 2 whole film: round 1 take list, pauses over 0.85 s kept at 0.45 s, W/T switch at every cut and join',
           'pieces': out}, open(f'{W}/round2/edl_film.json', 'w'), indent=1)
json.dump(film_words, open(f'{W}/round2/film_words.json', 'w'))
nsh = sum(len(p['shots']) for p in out)
print(f'{len(out)} pieces, {nsh} shots, {g} frames = {g / FPS:.1f} s ({g / FPS / 60:.2f} min); pause cuts: {len(cuts_log)} {cuts_log[:12]}')
lens = [((p['shots'][i + 1]['f0'] if i + 1 < len(p['shots']) else p['f1']) - s['f0']) / FPS for p in out for i, s in enumerate(p['shots'])]
print('shot length s: min %.1f p50 %.1f max %.1f' % (min(lens), np.median(lens), max(lens)))
