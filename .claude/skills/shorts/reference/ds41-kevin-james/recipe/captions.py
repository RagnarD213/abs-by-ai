"""DS-36 R1 captions (from DS-43 R2) (python3 captions.py scripted|offcuff [voice]; from DS-44B R2, Dan-approved on this set) (the approved DS-28 / DS-31 / DS-33 style: Arial Bold 86, outline 7, shadow 3; chunker: at most 3 words and
17 characters a cue, no lone trailing word, break on , . ? ! or a gap > 0.6 s, a cue under 0.26 s merges, cues never cross a
picture or audio join) + the mix: the clip's own sound under the clip and the transition, then the chosen voice.
Two placements: "Clip" (MarginV 630, bottom at y 1290) while the clip fills the frame and Dan sits small in the bottom-left
corner (his head from y ~1450), "Default" (MarginV 420, the approved position) once he is full size."""
from pathlib import Path
import json, re, subprocess, sys
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
VERSION = sys.argv[1]; O = W/VERSION
VOICE = sys.argv[2] if len(sys.argv) > 2 else 'house_bass15'
edl = json.load(open(O/'edl.json')); out = json.load(open(O/'words_out.json')); shots = json.load(open(O/('shots.json' if (O/'shots.json').exists() else 'shots-times.json')))
# R1 gate (captions:sync): cue starts follow the speech measured in the delivered film (caption_asr.json = that film's medium.en
# word times; the timeline does not change in an audio-only rebuild), wherever the two disagree by more than 0.15 s
if (O/'caption_asr.json').exists():
    import difflib
    A_ = json.load(open(O/'caption_asr.json'))['words']
    sm = difflib.SequenceMatcher(None, [x['w'].lower().strip('.,!?:') for x in out], [x['w'].lower().strip('.,!?:') for x in A_], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal': continue
        for k in range(i2 - i1):
            w_, a_ = out[i1 + k], A_[j1 + k]
            if w_['speaker'] == 'dan' and not w_.get('fixed') and 0.15 < abs(a_['t'] - w_['t0']) < 0.7:   # R1 review: a 1 s jump was a mismatched 'shame'
                w_['t0'] = round(a_['t'], 3); w_['t1'] = round(max(w_['t1'], w_['t0'] + 0.1), 3)
joins = sorted(set([p['film0'] for p in edl['pieces']] + [s['film0'] for s in edl['clip']['segs'][1:]] + [s['a'] for s in shots[1:]]))
TALK0 = edl['clip'].get('layout_cut_film') or edl['clip']['segs'][1]['film0']          # R5: captions move from the clip position to the default one at the panel cut
head = open(Path(__file__).resolve().parent/'captions_head.ass').read() + '\n'
# the approved DS-28/DS-31/DS-33 style as DS-43 R2 / DS-44B R2 used it on this set: Default MarginV 312 (bottom 1608), Clip MarginV 660
# (bottom 1260, clear of the corner Dan)
assert 'Style: Clip' in head
L = lambda c: len(' '.join(x['w'].rstrip(',') for x in c))
def split_clause(sent):
    cl = [[]]
    for w in sent:
        if cl[-1] and (len(cl[-1]) == 3 or L(cl[-1] + [w]) > 17): cl.append([])
        cl[-1].append(w)
    if len(cl) > 1 and len(cl[-1]) == 1 and L(cl[-2] + cl[-1]) <= 18 and len(cl[-2]) < 3: cl[-2:] = [cl[-2] + cl[-1]]
    elif len(cl) > 1 and len(cl[-1]) == 1 and len(cl[-2]) >= 2: cl[-1] = [cl[-2].pop()] + cl[-1]
    return cl
chunks = []; sent = []
for i, w in enumerate(out):
    sent.append(w); nxt = out[i+1] if i + 1 < len(out) else None
    if w['w'][-1] in '.?!,' or nxt is None or nxt['t0'] - w['t1'] > 0.6 or (nxt and any(w['t0'] + 0.02 < j <= nxt['t0'] + 0.06 for j in joins)) \
       or (nxt and nxt['speaker'] != w['speaker']):
        cl = split_clause(sent)
        j = 0
        while j < len(cl):
            if cl[j][-1]['t1'] - cl[j][0]['t0'] < 0.26 and len(cl) > 1:
                nbs = [x for x in (j + 1, j - 1) if 0 <= x < len(cl) and L(cl[j] + cl[x]) <= 18]
                if nbs:
                    a_, b_ = sorted((j, nbs[0])); cl[a_:b_+1] = [cl[a_] + cl[b_]]; continue
            j += 1
        chunks += cl; sent = []
# (DS-36: join tolerance 0.02 s, word times round to 1 ms) a lone short word (under 0.45 s) joins the next cue, else the previous one, when the pair fits a line (20 characters at
# Arial Bold 86 on the 940 px caption width) and no join or speaker change sits between them ("Yes," "Right," "200")
k = 0
while k < len(chunks):
    c = chunks[k]
    if len(c) == 1 and c[0]['t1'] - c[0]['t0'] < 0.80:   # DS-36: 0.80 (Whisper stretches a lone 'and', 'get', 'Instead' to 0.5-0.7 s)
        for nb in (k + 1, k - 1):
            if 0 <= nb < len(chunks) and L(chunks[min(k, nb)] + chunks[max(k, nb)]) <= 20 and chunks[nb][0]['speaker'] == c[0]['speaker'] \
               and not any(min(c[0]['t0'], chunks[nb][0]['t0']) < j <= max(c[0]['t0'], chunks[nb][0]['t0']) + 0.06 for j in joins):
                a_, b_ = sorted((k, nb)); chunks[a_:b_ + 1] = [chunks[a_] + chunks[b_]]; k = a_; break
        else: k += 1
    else: k += 1
# review 1: a cue on screen under 0.30 s cannot be read ("he goes" 0.16 s, "and I" 0.24 s): it joins a neighbour when the pair fits a line
k = 0
while k < len(chunks) - 1:
    c = chunks[k]; d = chunks[k+1][0]['t0'] - c[0]['t0']
    if d < 0.30:
        for nb in (k + 1, k - 1):
            if 0 <= nb < len(chunks) and L(chunks[min(k, nb)] + chunks[max(k, nb)]) <= 20 and chunks[nb][0]['speaker'] == c[0]['speaker'] \
               and not any(min(c[0]['t0'], chunks[nb][0]['t0']) < j <= max(c[0]['t0'], chunks[nb][0]['t0']) + 0.06 for j in joins):
                a_, b_ = sorted((k, nb)); chunks[a_:b_ + 1] = [chunks[a_] + chunks[b_]]; k = max(a_ - 1, 0); break
        else:
            # no neighbour has room: borrow the previous cue's last word when that leaves both readable ("and I remember" / "this he goes")
            pv = chunks[k-1] if k else None
            if pv and len(pv) >= 3 and pv[0]['speaker'] == c[0]['speaker'] and L([pv[-1]] + c) <= 20 and chunks[k+1][0]['t0'] - pv[-1]['t0'] >= 0.30 \
               and pv[-1]['t0'] - pv[0]['t0'] >= 0.30 and not any(pv[-1]['t0'] < j <= c[0]['t0'] + 0.06 for j in joins):
                chunks[k] = [pv.pop()] + c
            k += 1
    else: k += 1
def ts(x): cs = round(x*100); return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'
lines = []
for j, c in enumerate(chunks):
    a = c[0]['t0']; b = c[-1]['t1'] + 0.12
    if j + 1 < len(chunks): b = min(max(b, a + 0.30), chunks[j+1][0]['t0'])
    b = min(b, edl['total_frames']/FPS - 0.04)          # R1 gate: never past the last picture frame
    for jn in joins:
        if a < jn < b and jn - a < 0.06: a = int(jn*100 + 0.999)/100                # a word starting a hair before a cut: the cue starts on the cut
        elif a < jn < b and jn - a < 0.30 and b - jn > jn - a: a = int(jn*100 + 0.999)/100   # review 1: a 0.13 s flash before the cut; the cue starts on the cut instead
        elif a < jn < b: b = int(jn*100)/100 - 0.01        # ends on the frame before the join, never on the next shot's first frame
    text = ' '.join(x['w'].rstrip(',') for x in c)
    if j == 0 or chunks[j-1][-1]['w'][-1] in '.?!' or c[0]['speaker'] != chunks[j-1][-1]['speaker']: text = text[0].upper() + text[1:]
    if any(c_['a'] - 0.02 <= a < c_['b'] - 0.02 for c_ in shots if c_['kind'] == 'card'): continue   # DS-41 gate (captions:card_collision): no caption sits on a full-screen card; the card carries those lines
    style = 'Clip' if a < TALK0 else 'Default'
    lines.append(f'Dialogue: 0,{ts(a)},{ts(b)},{style},,0,0,0,,{text}')
(O/'captions.ass').write_text(head + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(lines) + '\n')
# the mix: the clip's sound from 0 (it fades out over the transition), the voice from the transition's start (room tone under the move)
ms = int(round(edl['clip']['frames']/FPS*1000))          # the voice starts on the first response frame
subprocess.run([F, '-v', 'error', '-y', '-i', str(O/'clip-finished.wav'), '-i', str(O/f'voice-{VOICE}.wav'), '-filter_complex',
                f'[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo,adelay={ms}|{ms}[b];'
                f'[a][b]amix=inputs=2:normalize=0:duration=longest[o]', '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', str(O/f'mix-{VOICE}.wav')], check=True)
subprocess.run([F, '-v', 'error', '-y', '-i', str(O/'audio'/'clip-raw.wav'), '-i', str(O/'lav.wav'), '-filter_complex',
                f'[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo,adelay={ms}|{ms}[b];'
                f'[a][b]amix=inputs=2:normalize=0:duration=longest[o]', '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', str(O/'mix-untreated.wav')], check=True)
print('CAPTIONS', len(lines), 'cues; mix', VOICE)
