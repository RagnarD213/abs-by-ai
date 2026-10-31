"""RO-37 round 3 subtitles (.srt sidecar, nothing burned in): the words heard on the delivered audio (Whisper small, cached by sha256),
cue rules from RO-24 R5 (gap 0.45 s, 84 chars, 5.5 s, sentence ends; balanced two-line wrap at 45)."""
import json, re, sys
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/cut'); import speech
heard, _ = speech.transcribe('final/RO37_R3_MASTER.mp4', 'small')
W = [dict(w=x['w'].strip(), t0=round(x['t'], 3), t1=round(x['e'], 3)) for x in heard if x['w'].strip()]
M = []
for w in W:
    if M and w['w'][:1] in "-.'%," and w['t0'] - M[-1]['t1'] < 0.3: M[-1] = dict(M[-1], w=M[-1]['w'] + w['w'], t1=w['t1'])
    else: M.append(dict(w))
W = M; total = 475.075
FIX = [(r'about 80 of beginners', 'about 80% of beginners'), (r'before when and you', 'before when you'), (r'to my channel and go to', 'to my channel, go to'), (r'locked in, That', 'locked in, that'),
       (r'still a struggle$', 'still a struggle,'), (r'every day So why', 'every day. So why'), (r'long term\. Next only', 'long term. Next, only'), (r'every day becomes a struggle\.$', 'every day becomes a struggle?'),
       (r'only workout for', 'only work out for'), (r'cable crunchers', 'cable crunches'), (r'weeks 2-4', 'weeks two to four'), (r'working out longer If you', 'working out longer. If you'), (r'stops you for coming', 'stops you from coming'), (r'same exercise as every day', 'same exercises every day'), (r"gonna going to do", 'gonna do'), (r'going gonna do', 'gonna do'),
       (r'you train But', 'you train. But'), (r'still a struggle don', "still a struggle, don"), (r'you guys You want', 'you guys. You want'), (r'for an hour But', 'for an hour. But'),
       (r'^Working out longer if you', 'working out longer. If you'), (r'a day You', 'a day. You'), (r'don\'t add more I know', "don't add more. I know"), (r'6[- ]?[Pp]ack[Aa]pps?\s*\.?\s*com', 'SixPackAbs.com'), (r' ([.,%?!])', r'\1'), (r'6[- ]?[Pp]ack[Aa]bs\s*\.?\s*com', 'SixPackAbs.com'), (r'[Ss]ix[- ]?[Pp]ack[Aa]bs\s*\.\s*com', 'SixPackAbs.com')]
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
open('final/RO37_R3.srt','w').write(txt)
print(len(cues), 'cues; longest line', max(len(l) for c in out for l in c.split('\n')[2:]), 'chars')
