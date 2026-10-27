"""RO-24 round 3 timeline: round 2's locked cut (edl_film_pic.json, film_voice_A.wav, the graphics) with the six interview
clips inserted where the script says [PLAY CLIP], each on a measured quiet frame of his voice. Nothing of round 2 is
re-cut: every old film frame keeps its picture and sound, shifted later by the clips before it.

Writes (round3/): edl_r3.json (picture: presenter shots and clip inserts, in order), timemap.json, film_words_r3.json,
audio/film_voice_r3.wav, manifest_r2_mapped.json (round 2's graphics on the new timeline; photo scenes that end on an
insert end there), facts.json (for the background planner).
"""
import json, subprocess, numpy as np, pathlib
R2 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round2'); R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3')
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
FPS = 30000 / 1001; SR = 48000
INS = json.load(open(R3 / 'clips/inserts.json'))
# old film frame where each clip goes (between the cue sentence and his next line; a quiet frame of the lav; inside the
# photo scene that introduces the person where there is one, so the insert hides the join)
AT = {'sharon': 784,    # 26.159: after "...what not to do." (voice -41 dB). Not 785 (the cut): round 2's 40 ms join crossfade
                        # into "Sharon" starts at 26.173, so a split there chopped its onset (R3 review F4/F5). The dropped P01
                        # frame's slot shows P02's plate pre-roll frame instead (PREROLL), so "Sharon" keeps its run-in.
      'fatjoe': 3508,   # 117.050: "...did it the right way." / "Fat Joe was" (-45 dB), inside P3
      'amy': 5468,      # 182.449: "Next up is Amy Schumer." / "Amy Schumer lost" (-53 dB), inside P4
      'meghan': 7021,   # 234.267: "...someone who got it right." / "Meghan Trainor took" (-44 dB), inside P5
      'oprah': 8759,    # 292.259: "...the weight came back." / "Oprah stopped" (-47 dB), on P6's last frame
      'tracy': 9026}    # 301.168: "...a lifetime thing." / "And Tracy Morgan said it" (-52 dB), Dan on camera
ORDER = sorted(AT, key=AT.get)
PREROLL = {'sharon': 'P02'}   # the frame after the insert comes from this piece's plate, one frame before its in-point


def shift_f(f):
    """old film frame -> new film frame (a frame at an insert point plays after the clip)."""
    return f + sum(INS[n]['frames'] for n in ORDER if AT[n] <= f)


def shift_t(t):
    return shift_f(int(round(t * FPS))) / FPS + (t - round(t * FPS) / FPS)


def main():
    E = json.load(open(R2 / 'edl_film_pic.json'))
    # ---- picture: split shots at insert points, put the inserts in
    items, g = [], 0
    pend = list(ORDER); pre = None
    for p in E['pieces']:
        for si, sh in enumerate(p['shots']):
            b = p['shots'][si + 1]['f0'] if si + 1 < len(p['shots']) else p['f1']
            a = sh['f0']; n = b - a
            while pend and g <= AT[pend[0]] < g + n:
                c = AT[pend[0]] - g
                if c > 0: items.append(dict(kind='shot', piece=p['id'], key=p['key'], src0=a, n=c, framing=sh['framing'], join=si == 0 and a == sh['f0']))
                nm = pend.pop(0); I = INS[nm]
                items.append(dict(kind='insert', clip=nm, mov=str(R3 / I['file']), n=I['frames']))
                a += c; n -= c; g += c
                if nm in PREROLL:                    # the rest of this shot gives its slots to the next piece's pre-roll
                    assert n <= 3, (nm, n); pre = (PREROLL[nm], n); g += n; n = 0
            if n > 0:
                it = dict(kind='shot', piece=p['id'], key=p['key'], src0=a, n=n, framing=sh['framing'], join=si == 0 and a == sh['f0'])
                if pre and pre[0] == p['id'] and si == 0:
                    it['src0'] -= pre[1]; it['n'] += pre[1]; it['preroll'] = pre[1]; pre = None
                items.append(it)
            g += n
    old_total = g
    o = 0
    for it in items: it['o0'] = o; o += it['n']; it['o1'] = o
    new_total = o
    assert new_total == old_total + sum(INS[n]['frames'] for n in ORDER)
    json.dump(dict(note='round 2 picture EDL with the six clip inserts; o0/o1 are new film frames', fps='30000/1001', items=items),
              open(R3 / 'edl_r3.json', 'w'), indent=1)
    json.dump(dict(at=AT, frames={n: INS[n]['frames'] for n in ORDER}, old_total=old_total, new_total=new_total,
                   new_at={n: shift_f(AT[n]) - INS[n]['frames'] for n in ORDER}), open(R3 / 'timemap.json', 'w'), indent=1)
    # ---- words
    W = json.load(open(R2 / 'film_words.json'))
    for w in W:
        late = any(0 <= AT[n] / FPS - w['t0'] < 0.1 and w['w'][:1].isupper() for n in ORDER)
        if late:
            n = next(n for n in ORDER if 0 <= AT[n] / FPS - w['t0'] < 0.1); d = INS[n]['frames'] / FPS
            w['t0'] = round(shift_t(AT[n] / FPS) + 0.02, 3); w['t1'] = round(shift_t(w['t1']) + (0 if w['t1'] * FPS >= AT[n] else d), 3)
        else:
            w['t0'] = round(shift_t(w['t0']), 3); w['t1'] = round(shift_t(w['t1']), 3)
    json.dump(W, open(R3 / 'film_words_r3.json', 'w'))
    # ---- audio: his voice, cut at each insert frame, the clip's sound in between
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(R2 / 'audio/film_voice_A.wav'), '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'])
    v = np.frombuffer(raw, '<i2').reshape(-1, 2)
    sm = lambda f: int(round(f * SR * 1001 / 30000))
    # Each clip's sound blends with his room tone at both edges instead of fading to silence (R3 re-check R2: a bed that
    # stopped dead in 10 ms with digital zero either side read as a chop). Room tone: a 300 ms speech-free stretch of take 1,
    # level-matched to his floor just before each insert; 10 ms crossfades into his own audio on both sides keep the
    # waveform continuous. Clip fade lengths fit the room before its first word and after its last (measured, ms).
    vf = v.astype(np.float32); L = int(0.30 * SR); hop = 480
    mono = vf.mean(1)
    rms = np.array([np.sqrt(np.mean(mono[k:k + L] ** 2)) for k in range(int(6.5 * SR), int(25.9 * SR) - L, hop)])
    k0 = int(6.5 * SR) + int(np.argmin(rms)) * hop; room = vf[k0:k0 + L]
    room = np.concatenate([room, room[::-1]])                  # mirrored loop: no seam click
    room_rms = np.sqrt(np.mean(room ** 2)) + 1e-9
    print('room tone from', round(k0 / SR, 3), 's')
    FADE = {'sharon': (150, 80), 'fatjoe': (250, 80), 'amy': (40, 120), 'meghan': (150, 150), 'oprah': (60, 150), 'tracy': (80, 30)}
    x10 = int(0.010 * SR)
    def eq(n):                                                 # equal-power 0 -> 1 over n samples
        return np.sin(np.linspace(0, np.pi / 2, max(1, n)))[:, None]
    parts, last = [], 0
    for nm in ORDER:
        c = sm(AT[nm]); parts.append(vf[last:c]); last = c
        raw = subprocess.check_output([FF, '-v', 'error', '-i', str(R3 / INS[nm]['wav']), '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'])
        a = np.frombuffer(raw, '<i2').reshape(-1, 2).astype(np.float32); want = sm(INS[nm]['frames'])
        a = a[:want] if len(a) >= want else np.concatenate([a, np.zeros((want - len(a), 2), np.float32)])
        floor = np.sqrt(np.mean(mono[c - int(0.06 * SR):c] ** 2)) + 1e-9
        floor = float(np.clip(floor, 32768 * 10 ** (-52 / 20), 32768 * 10 ** (-38 / 20)))
        rt = np.resize(room * (floor / room_rms), (want, 2))
        fi, fo = (int(ms * SR / 1000) for ms in FADE[nm])
        e = np.ones((want, 1), np.float32); e[:fi] = eq(fi) ** 2; e[want - fo:] = (eq(fo) ** 2)[::-1]   # S-curve: the bed eases in
        # and out (an equal-power sine reached -6 dB in a sixth of the fade and still read as an abrupt start, R3 final check D2)
        r = np.sqrt(np.clip(1 - e ** 2, 0, 1))                  # room tone where the clip is faded
        reg = a * e + rt * r
        w = eq(x10)
        reg[:x10] = vf[c:c + x10] * (1 - w ** 2) ** 0.5 + reg[:x10] * w                  # out of his audio
        reg[-x10:] = reg[-x10:] * (1 - w ** 2) ** 0.5 + vf[c - x10:c] * w                  # back into it
        parts.append(reg)
    parts.append(vf[last:])
    fixed = parts
    out = np.clip(np.concatenate(fixed), -32768, 32767).astype('<i2')
    (R3 / 'audio').mkdir(exist_ok=True)
    subprocess.run([FF, '-y', '-v', 'error', '-f', 's16le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s16le', str(R3 / 'audio/film_voice_r3.wav')],
                   input=out.tobytes(), check=True)
    print('audio', len(out) / SR, 's; picture', new_total / FPS, 's')
    # ---- round 2 graphics on the new timeline
    M = json.load(open(R2 / 'hf/manifest.json')) + json.load(open(R2 / 'broll/broll_manifest.json'))
    ends_on = {'P1': 'sharon', 'P3': 'fatjoe', 'P4': 'amy', 'P5': 'meghan', 'P6': 'oprah'}
    for m in M:
        a, b = m['a'], m['b']
        m['a_r2'], m['b_r2'] = a, b
        m['a'] = round(shift_t(a), 4)
        if m['id'] in ends_on:                       # the photo scene introduces the person and ends where their clip starts
            m['b'] = round(shift_f(AT[ends_on[m['id']]]) / FPS - INS[ends_on[m['id']]]['frames'] / FPS, 4)
        else:
            m['b'] = round(shift_t(b), 4)
    json.dump(M, open(R3 / 'manifest_r2_mapped.json', 'w'), indent=1)
    for m in M:
        if m['a_r2'] < 135: print(f"{m['id']:4s} {m['a_r2']:7.2f}-{m['b_r2']:7.2f} -> {m['a']:7.2f}-{m['b']:7.2f}")
    for nm in ORDER:
        s = (shift_f(AT[nm]) - INS[nm]['frames']) / FPS
        print(f'insert {nm:7s} old {AT[nm] / FPS:7.2f} -> new {s:7.2f}-{s + INS[nm]["dur"]:7.2f}')


if __name__ == '__main__':
    main()
