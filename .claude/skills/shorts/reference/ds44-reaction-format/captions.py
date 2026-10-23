"""DS-44 R1 captions (the approved DS-28 / DS-31 / DS-33 style: Arial Bold 86, outline 7, shadow 3; chunker: at most 3 words and
17 characters a cue, no lone trailing word, break on , . ? ! or a gap > 0.6 s, a cue under 0.26 s merges, cues never cross a
picture or audio join) + the mix: the clip's own sound under the clip and the transition, then the chosen voice.
Two placements: "Clip" (MarginV 630, bottom at y 1290) while the clip fills the frame and Dan sits small in the bottom-left
corner (his head from y ~1450), "Default" (MarginV 420, the approved position) once he is full size."""
from pathlib import Path
import json, re, subprocess, sys
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
VOICE = sys.argv[1] if len(sys.argv) > 1 else 'house_bass15'
edl = json.load(open(W/'edl.json')); out = json.load(open(W/'words_out.json')); shots = json.load(open(W/'shots.json'))
joins = sorted(set([p['film0'] for p in edl['pieces']] + [s['film0'] for s in edl['clip']['segs'][1:]] + [s['a'] for s in shots[1:]]))
TALK0 = edl['pieces'][0]['film0']
head = open('/Volumes/Extreme/_edit_work/ds28/round3/captions.ass').read().split('[Events]')[0]
head = head.replace('Style: Default,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,2,70,70,420,1',   # R2: Default lowered to MarginV 320 (bottom 1600) so G02 can sit under Dan's chin
                    'Style: Default,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,2,70,70,320,1\n'
                    'Style: Clip,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,2,70,70,660,1')   # R2: bottom 1260, clear of the larger corner Dan (hair from y ~1288)
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
    if w['w'][-1] in '.?!,' or nxt is None or nxt['t0'] - w['t1'] > 0.6 or (nxt and any(w['t0'] < j <= nxt['t0'] for j in joins)) \
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
# a lone short word (under 0.45 s) joins the next cue, else the previous one, when the pair fits a line (20 characters at
# Arial Bold 86 on the 940 px caption width) and no join or speaker change sits between them ("Yes," "Right," "200")
k = 0
while k < len(chunks):
    c = chunks[k]
    if len(c) == 1 and c[0]['t1'] - c[0]['t0'] < 0.45:
        for nb in (k + 1, k - 1):
            if 0 <= nb < len(chunks) and L(chunks[min(k, nb)] + chunks[max(k, nb)]) <= 20 and chunks[nb][0]['speaker'] == c[0]['speaker'] \
               and not any(min(c[0]['t0'], chunks[nb][0]['t0']) < j <= max(c[0]['t0'], chunks[nb][0]['t0']) for j in joins):
                a_, b_ = sorted((k, nb)); chunks[a_:b_ + 1] = [chunks[a_] + chunks[b_]]; k = a_; break
        else: k += 1
    else: k += 1
def ts(x): cs = round(x*100); return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'
lines = []
for j, c in enumerate(chunks):
    a = c[0]['t0']; b = c[-1]['t1'] + 0.12
    if j + 1 < len(chunks): b = min(max(b, a + 0.30), chunks[j+1][0]['t0'])
    for jn in joins:
        if a < jn < b and jn - a < 0.06: a = int(jn*100 + 0.999)/100                # a word starting a hair before a cut: the cue starts on the cut
        elif a < jn < b: b = int(jn*100)/100 - 0.01        # ends on the frame before the join, never on the next shot's first frame
    text = ' '.join(x['w'].rstrip(',') for x in c)
    if j == 0 or chunks[j-1][-1]['w'][-1] in '.?!' or c[0]['speaker'] != chunks[j-1][-1]['speaker']: text = text[0].upper() + text[1:]
    style = 'Clip' if a < TALK0 else 'Default'
    lines.append(f'Dialogue: 0,{ts(a)},{ts(b)},{style},,0,0,0,,{text}')
(W/'captions.ass').write_text(head + '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(lines) + '\n')
# the mix: the clip's sound from 0 (it fades out over the transition), the voice from the transition's start (room tone under the move)
ms = int(round(edl['tr']['film0']*1000))
subprocess.run([F, '-v', 'error', '-y', '-i', str(W/'clip-finished.wav'), '-i', str(W/f'voice-{VOICE}.wav'), '-filter_complex',
                f'[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo,adelay={ms}|{ms}[b];'
                f'[a][b]amix=inputs=2:normalize=0:duration=longest[o]', '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', str(W/f'mix-{VOICE}.wav')], check=True)
subprocess.run([F, '-v', 'error', '-y', '-i', str(W/'clip-original.wav'), '-i', str(W/'lav.wav'), '-filter_complex',
                f'[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo,adelay={ms}|{ms}[b];'
                f'[a][b]amix=inputs=2:normalize=0:duration=longest[o]', '-map', '[o]', '-c:a', 'pcm_s24le', '-ar', '48000', str(W/'mix-untreated.wav')], check=True)
print('CAPTIONS', len(lines), 'cues; mix', VOICE)
