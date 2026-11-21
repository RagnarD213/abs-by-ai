"""RO-24 round 4 retime: Tracy Morgan's Tonight Show insert ends right after "I gained 40 pounds." (clip second 22.444)
instead of on the start of his next sentence ("Yeah, I gained 40. I", independent review ROUND-4-REVIEW F1). The insert
loses its last CUT frames; everything after it moves earlier by exactly that many frames. Nothing else changes.

Writes round4/: edl_r4.json, film_words_r4.json, audio/film_voice_r4.wav (the cut samples removed, a 60 ms cosine fade on
the clip's new tail), retime_r4.json {at_frame, cut_frames}. r4_t(t) maps a round 3 film second to round 4."""
import json, wave, pathlib, numpy as np
R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3'); R4 = R3.parent / 'round4'
FPS = 30000 / 1001; SR = 48000
E = json.load(open(R3 / 'edl_r3.json')); it = E['items']
k = next(i for i, x in enumerate(it) if x['kind'] == 'insert' and x['clip'] == 'tracy')
NEW_N = 334                                    # 11.3 s + 334 frames = 22.444 s in the source: after "pounds." (22.16), before "You," (22.72)
CUT = it[k]['n'] - NEW_N; AT = it[k]['o0'] + NEW_N          # film frames [AT, AT + CUT) of round 3 are removed
def r4_f(f): return f if f < AT else (AT if f < AT + CUT else f - CUT)
def r4_t(t): return t if t < AT / FPS else max(AT / FPS, t - CUT / FPS)

if __name__ == '__main__':
    it[k] = dict(it[k], n=NEW_N, o1=AT)
    for x in it[k + 1:]: x['o0'] -= CUT; x['o1'] -= CUT
    E['note'] = (E.get('note', '') + f' | round 4: Tracy insert ends after "I gained 40 pounds." ({CUT} frames off its tail; later items {CUT} frames earlier)').strip()
    json.dump(E, open(R4 / 'edl_r4.json', 'w'), indent=1)
    W = json.load(open(R3 / 'film_words_r3.json'))
    W4 = [dict(w, t0=round(r4_t(w['t0']), 3), t1=round(r4_t(w['t1']), 3)) for w in W if not (AT / FPS <= w['t0'] < (AT + CUT) / FPS)]
    json.dump(W4, open(R4 / 'film_words_r4.json', 'w'), indent=1)
    with wave.open(str(R3 / 'audio/film_voice_r3.wav')) as r:
        p = r.getparams(); assert p.framerate == SR and p.sampwidth in (2, 3, 4), p
        raw = r.readframes(p.nframes)
    dt = {2: np.int16, 4: np.int32}[p.sampwidth]
    a = np.frombuffer(raw, dt).reshape(-1, p.nchannels).astype(np.float64)
    s0, s1 = int(round(AT / FPS * SR)), int(round((AT + CUT) / FPS * SR))
    fade = int(0.06 * SR); a[s0 - fade:s0] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fade)))[:, None]
    b = np.concatenate([a[:s0], a[s1:]]).round().astype(dt)
    (R4 / 'audio').mkdir(exist_ok=True)
    with wave.open(str(R4 / 'audio/film_voice_r4.wav'), 'w') as w:
        w.setparams(p); w.writeframes(b.tobytes())
    json.dump(dict(at_frame=AT, cut_frames=CUT, at_s=round(AT / FPS, 4), cut_s=round(CUT / FPS, 4), new_frames=it[-1]['o1'],
                   voice_samples=len(b), voice_s=round(len(b) / SR, 4)), open(R4 / 'retime_r4.json', 'w'), indent=1)
    print(open(R4 / 'retime_r4.json').read())
