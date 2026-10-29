"""RO-24 round 4 subtitles (.srt sidecar, organic long-form: nothing burned in): Dan's words on the film timeline
(round 3 film_words_r3.json, the timeline the round 4 film uses unchanged) plus the six interview clips' own words, mapped
from each clip's source time to where it plays. Cue rules from RO-28's finish.py (gap 0.45 s, 84 chars, 5.5 s, sentence
ends; balanced two-line wrap at 45). -> final/RO24_R4.srt"""
import json, re, pathlib, sys
R4 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round5'); R3 = R4.parent / 'round3'   # round 5: R4 names the round 5 folder; R3 = R4.parent / 'round3'
# words heard on the DELIVERED audio (Whisper small, cached by the file's sha256): Dan and the six clips, in sync with
# what plays (round 4 review F4: the intended-word list missed "Why", "But most of the headlines left out", ...)
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/cut'); import speech
MAN = {m['id']: m for m in json.load(open(R4 / 'film_manifest_r5.json'))}
CL = [(n[2:], m['a'], m['b']) for n, m in MAN.items() if n.startswith('C_')]
heard, _ = speech.transcribe(str(R4 / 'final/RO24_R5_MASTER.mp4'), 'small')
W = []
for x in heard:
    w = x['w'].strip()
    if not w: continue
    c = next((n for n, a, b in CL if a <= (x['t'] + x['e']) / 2 < b), None)
    W.append(dict(w=w, t0=round(x['t'], 3), t1=round(x['e'], 3), **({'clip': c} if c else {})))
# inside each interview clip, its own source transcript (Whisper on the delivered mix misses Tracy's Tonight Show audio and
# Meghan's narrator under music; review 2 item 1), mapped from clip seconds to where the clip plays and cut where it ends
INS = json.load(open(R3 / 'clips/inserts.json'))
W = [w for w in W if not w.get('clip')]
for n, a0, b0 in CL:
    I = INS[n]
    for x in json.load(open(R3 / I['src'].replace('.mp4', '.words.json'))):
        t0 = a0 + x['t0'] - I['a']; t1 = a0 + x['t1'] - I['a']
        if t0 >= a0 - 0.05 and t1 <= b0 + 0.05:
            W.append(dict(w=x['w'], t0=round(t0, 3), t1=round(t1, 3), clip=n))
W.sort(key=lambda x: x['t0'])
for i, w in enumerate(W[:-1]):                           # percent signs Whisper drops
    nx = ' '.join(x['w'] for x in W[i + 1:i + 3]).lower()
    if w['w'] == '100' and nx.startswith('her own'): w['w'] = '100%'
    if w['w'] == '14' and nx.startswith('of their'): w['w'] = '14%'
M = []                                                   # Whisper splits "GLP" / "-1." and "1" / ".5mg": glue them back
for w in W:
    if M and w['w'][:1] in "-.'%," and w['t0'] - M[-1]['t1'] < 0.3 and w.get('clip') == M[-1].get('clip'):
        M[-1] = dict(M[-1], w=M[-1]['w'] + w['w'], t1=w['t1'])
    else: M.append(dict(w))
W = M
total = max(m['b'] for m in MAN.values())
FIX = [(r' ([.,%?!])', r'\1'), (r'(\d) \.(\d)', r'\1.\2'), (r' -(\w)', r'-\1'), (r'GLP -1', 'GLP-1'), (r'\bozempic\b', 'Ozempic'), (r'Ozenpik', 'Ozempic'),
       (r'old zempic', 'Ozempic'), (r'Monjaro', 'Mounjaro'), (r'[Zz]ebbound|[Zz]etbound', 'Zepbound'), (r'get this gone', 'get this gaunt'),
       (r'over fat', 'overfat'), (r'\b(\d(?:\.\d)?)mg\b', r'\1 mg'), (r'sixpackabs\s*\.com', 'SixPackAbs.com'), (r'\bout ate\b', 'out-ate'),
       (r'ozempic phase', 'Ozempic face'), (r'Ozempic phase', 'Ozempic face'), (r'\bOsborne?\b', 'Osbourne'), (r'\bManjaro\b', 'Mounjaro'),
       (r"\bI'll eat (o|O)zimpic", 'I out-ate Ozempic'), (r'\b[Oo]zimpic\b', 'Ozempic'), (r'\b[Oo]zempik\b', 'Ozempic'), (r'\bGLP ?-?1\b', 'GLP-1'), (r'\bZep ?(bown|hbound|hound|bound)s?\b', 'Zepbound'), (r'\bZep\b(?! ?bound)', 'Zepbound'),
       (r'\b[Oo]s[ae]m[bp]ic\b', 'Ozempic'), (r'\b[Oo]zympics?\b', 'Ozempic'), (r'\b[Zz]et[Bb]ound\b', 'Zepbound'), (r'\bthat bound\b', 'Zepbound'), (r'\bZepbound-Bound\b', 'Zepbound'), (r'\bZepbound[- ]bound\b', 'Zepbound'), (r'\bMegan Trainor\b', 'Meghan Trainor'), (r'\bMegan\b', 'Meghan'), (r'\b[Zz]ap ?down\b', 'Zepbound'), (r"And I'm like, I was like, shriveling", "And I'm like, I can't. I was like, shriveling"), (r'^took myself off the medications', 'I took myself off the medications'), (r'^Tracy Morgan said on the Tonight Show', 'And Tracy Morgan said it on The Tonight Show'), (r'\b5 to 4, to 3, to 2\b', '5 to 4, 4 to 3, 3 to 2'), (r'\bover eat\b', 'overeat'), (r"\bThe Osbourne's alum\b", 'The Osbournes alum'), (r"\band I had my son's like\b", "and my son's like"), (r'\bHow you stay in the shape these days\?', 'How you staying in shape these days?')]
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s
cues, cur = [], []
def flush():
    global cur
    if cur: cues.append([cur[0]['t0'], cur[-1]['t1'], fix(' '.join(w['w'] for w in cur))]); cur = []
for w in W:
    if cur:
        gap = w['t0'] - cur[-1]['t1']; txt = ' '.join(x['w'] for x in cur + [w])
        if gap >= 0.45 or len(txt) > 84 or w['t1'] - cur[0]['t0'] > 5.5 or w.get('clip') != cur[-1].get('clip'): flush()
    cur.append(w)
    if w['w'][-1:] in '.?!' and (cur[-1]['t1'] - cur[0]['t0']) > 1.2: flush()
flush()
k = 1                                                    # a 1-2 word orphan after an unfinished sentence joins the cue before it
while k < len(cues):
    a0, b0, t = cues[k]; pa, pb, pt = cues[k - 1]
    if len(t.split()) <= 2 and pt.rstrip()[-1:] not in '.?!' and a0 - pb < 1.0 and len(pt) + len(t) < 92:
        cues[k - 1] = [pa, b0, pt + ' ' + t]; del cues[k]
    else: k += 1
def wrap(s):
    if len(s) <= 45: return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        a, b = ' '.join(ws[:k]), ' '.join(ws[k:]); m = max(len(a), len(b))
        if best is None or m < best[0]: best = (m, a + '\n' + b)
    return best[1]
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; ms = min(999, int(round((s - int(s)) * 1000)))
    return f'{h:02d}:{m:02d}:{int(s):02d},{ms:03d}'
out = []
for i, (a, b, s) in enumerate(cues):
    if s and s[0].islower() and (i == 0 or cues[i - 1][2].rstrip()[-1:] in '.?!'): s = s[0].upper() + s[1:]
    b = max(b, a + 0.9)
    if i + 1 < len(cues): b = min(b, cues[i + 1][0] - 0.02)
    b = min(b, total - 0.05)
    out.append(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n')
txt = '\n'.join(out); assert '—' not in txt
(R4 / 'final/RO24_R5.srt').write_text(txt)
print(len(cues), 'cues; longest line', max(len(l) for c in out for l in c.split('\n')[2:]), 'chars')
