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
AT = {'sharon': 785,    # 26.193: the cut after "...what not to do." (voice -38 dB; "Sharon" starts 26.20)
      'fatjoe': 3508,   # 117.050: "...did it the right way." / "Fat Joe was" (-45 dB), inside P3
      'amy': 5468,      # 182.449: "Next up is Amy Schumer." / "Amy Schumer lost" (-53 dB), inside P4
      'meghan': 7021,   # 234.267: "...someone who got it right." / "Meghan Trainor took" (-44 dB), inside P5
      'oprah': 8759,    # 292.259: "...the weight came back." / "Oprah stopped" (-47 dB), on P6's last frame
      'tracy': 9026}    # 301.168: "...a lifetime thing." / "And Tracy Morgan said it" (-52 dB), Dan on camera
ORDER = sorted(AT, key=AT.get)


def shift_f(f):
    """old film frame -> new film frame (a frame at an insert point plays after the clip)."""
    return f + sum(INS[n]['frames'] for n in ORDER if AT[n] <= f)


def shift_t(t):
    return shift_f(int(round(t * FPS))) / FPS + (t - round(t * FPS) / FPS)


def main():
    E = json.load(open(R2 / 'edl_film_pic.json'))
    # ---- picture: split shots at insert points, put the inserts in
    items, g = [], 0
    pend = list(ORDER)
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
            if n > 0: items.append(dict(kind='shot', piece=p['id'], key=p['key'], src0=a, n=n, framing=sh['framing'], join=si == 0 and a == sh['f0']))
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
    for w in W: w['t0'] = round(shift_t(w['t0']), 3); w['t1'] = round(shift_t(w['t1']), 3)
    json.dump(W, open(R3 / 'film_words_r3.json', 'w'))
    # ---- audio: his voice, cut at each insert frame, the clip's sound in between
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(R2 / 'audio/film_voice_A.wav'), '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'])
    v = np.frombuffer(raw, '<i2').reshape(-1, 2)
    sm = lambda f: int(round(f * SR * 1001 / 30000))
    parts, last = [], 0
    for nm in ORDER:
        c = sm(AT[nm]); parts.append(v[last:c]); last = c
        raw = subprocess.check_output([FF, '-v', 'error', '-i', str(R3 / INS[nm]['wav']), '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'])
        a = np.frombuffer(raw, '<i2').reshape(-1, 2); want = sm(INS[nm]['frames'])
        a = a[:want] if len(a) >= want else np.concatenate([a, np.zeros((want - len(a), 2), '<i2')])
        parts.append(a)
    parts.append(v[last:])
    out = np.concatenate(parts)
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
