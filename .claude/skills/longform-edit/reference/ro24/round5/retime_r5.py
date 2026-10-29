"""RO-24 round 5 retime: the pause after "...and why you should too." at the 7 DAYS A WEEK big type (round 4 film 5:44.9 to
5:45.9; Dan, 2026-10-28: "when there's 2:50 remaining ... there's a slight pause. I want you to remove that and make that
transition smooth"). Speech ends at 344.85 and restarts at 345.90 across the picture cut at frame 10364 (345.812); the last
CUT frames of the shot before that cut are silence (-50 dB) and go, leaving about 0.40 s between the two lines.
Picture EDL, words, voice and every later time move earlier by exactly CUT whole frames (round 4's retime_r4.py method).

Writes round5/: edl_r5.json, film_words_r5.json, audio/film_voice_r5.wav (from round 4's film_voice_r4b.wav, a 10 ms
equal-power crossfade at the join), retime_r5.json. r5_t(t) / r5_f(f) map round 4 film seconds / frames to round 5."""
import json, wave, pathlib, numpy as np
R4 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round4'); R5 = R4.parent / 'round5'
FPS = 30000 / 1001; SR = 48000
CUT = 19; AT = 10364 - CUT                      # round 4 film frames [AT, AT + CUT) = 345.179 to 345.812 s are removed
def r5_f(f): return f if f < AT else (AT if f < AT + CUT else f - CUT)
def r5_t(t): return t if t < AT / FPS else max(AT / FPS, t - CUT / FPS)

if __name__ == '__main__':
    E = json.load(open(R4 / 'edl_r4.json')); it = E['items']
    k = next(i for i, x in enumerate(it) if x['o0'] < AT < x['o1'])
    assert it[k]['o1'] == AT + CUT and it[k]['kind'] == 'shot', it[k]
    it[k] = dict(it[k], n=it[k]['n'] - CUT, o1=AT)
    for x in it[k + 1:]: x['o0'] -= CUT; x['o1'] -= CUT
    E['note'] = (E.get('note', '') + f' | round 5: pause after "why you should too." trimmed ({CUT} silent frames off the end of piece '
                 f'{it[k]["piece"]}; later items {CUT} frames earlier)').strip()
    json.dump(E, open(R5 / 'edl_r5.json', 'w'), indent=1)
    W = json.load(open(R4 / 'film_words_r4.json'))
    assert not any(AT / FPS <= w['t0'] < (AT + CUT) / FPS for w in W), 'a word inside the removed span'
    json.dump([dict(w, t0=round(r5_t(w['t0']), 3), t1=round(r5_t(w['t1']), 3)) for w in W], open(R5 / 'film_words_r5.json', 'w'), indent=1)
    with wave.open(str(R4 / 'audio/film_voice_r4b.wav')) as r:
        p = r.getparams(); assert p.framerate == SR and p.sampwidth == 2, p
        a = np.frombuffer(r.readframes(p.nframes), np.int16).reshape(-1, p.nchannels).astype(np.float64)
    s0, s1 = int(round(AT / FPS * SR)), int(round((AT + CUT) / FPS * SR)); x = int(0.010 * SR)
    th = np.linspace(0, np.pi / 2, x)[:, None]
    seam = a[s0 - x:s0] * np.cos(th) + a[s1 - x:s1] * np.sin(th)          # equal-power crossfade, both sides room tone
    b = np.concatenate([a[:s0 - x], seam, a[s1:]]).round().clip(-32768, 32767).astype(np.int16)
    with wave.open(str(R5 / 'audio/film_voice_r5.wav'), 'w') as w:
        w.setparams(p); w.writeframes(b.tobytes())
    rms = lambda s: 20 * np.log10(np.sqrt((s[:, 0] / 32768) ** 2).mean() + 1e-9)
    json.dump(dict(at_frame=AT, cut_frames=CUT, at_s=round(AT / FPS, 4), cut_s=round(CUT / FPS, 4), new_frames=it[-1]['o1'],
                   voice_samples=len(b), voice_s=round(len(b) / SR, 4), removed_dbfs=round(float(rms(a[s0:s1])), 1)),
              open(R5 / 'retime_r5.json', 'w'), indent=1)
    print(open(R5 / 'retime_r5.json').read())
