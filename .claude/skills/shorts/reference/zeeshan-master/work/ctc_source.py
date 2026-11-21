#!/usr/bin/env python3
"""Caption timing: CTC forced alignment (torchaudio WAV2VEC2_ASR_BASE_960H) of the SOURCE Whisper
words onto the master's own audio, inside every speech piece of every short. Whisper's word onsets
run 130-420 ms early in continuous speech on this mix (the gate's captions:sync row measured it on
short 2 against the delivered audio), so captions are timed from this instead. Writes
work/words_aligned.json in the same {chunks:[{text,timestamp}]} shape; words outside the pieces keep
their Whisper times. The gate still measures against a DIFFERENT pass: the delivered file's own ASR."""
import json, re, subprocess, wave, numpy as np, torch, torchaudio
FF = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').FF))"]))
SEGS = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./segments.js').SEGMENTS))"]))
SR = 16000
subprocess.run([FF, '-v', 'error', '-y', '-i', 'work/master48.wav', '-ar', str(SR), '-c:a', 'pcm_s16le', 'work/master16.wav'], check=True)
f = wave.open('work/master16.wav'); audio = torch.from_numpy(np.frombuffer(f.readframes(f.getnframes()), '<i2').astype(np.float32) / 32768.0)
words = json.load(open('work/words.json'))['chunks']
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval(); labels = bundle.get_labels(); L = {c: i for i, c in enumerate(labels)}
NUM = {'30': 'THIRTY', '2': 'TWO', '3': 'THREE', '4': 'FOUR', '10': 'TEN', '5': 'FIVE', '6': 'SIX', '15': 'FIFTEEN', '90': 'NINETY'}
def norm(w):
    w = re.sub(r"[^A-Za-z0-9' ]", ' ', w).upper()
    w = ' '.join(NUM.get(t, t) for t in w.split())
    return re.sub(r"[^A-Z' ]", '', w).strip()
done = {}
for s in SEGS:
    for p in s['pieces']:
        if p.get('music'): continue
        idx = [i for i, w in enumerate(words) if w['timestamp'][1] > p['start'] and w['timestamp'][0] < p['end']]
        # windows split at Whisper gaps >= 0.35 s or every ~12 s
        wins, cur = [], []
        for i in idx:
            if cur and (words[i]['timestamp'][0] - words[cur[-1]]['timestamp'][1] >= 0.35 or words[i]['timestamp'][0] - words[cur[0]]['timestamp'][0] > 12):
                wins.append(cur); cur = []
            cur.append(i)
        if cur: wins.append(cur)
        for wn in wins:
            t0 = max(p['start'] - 0.3, words[wn[0]]['timestamp'][0] - 0.5); t1 = min(p['end'] + 0.3, words[wn[-1]]['timestamp'][1] + 0.5)
            toks, owner = [], []
            for k, i in enumerate(wn):
                for ch in norm(words[i]['text']).replace(' ', '|'):
                    if ch in L: toks.append(L[ch]); owner.append(k)
                toks.append(L['|']); owner.append(-1)
            toks, owner = toks[:-1], owner[:-1]
            while (t1 - t0) < 0.03 * len(toks) + 0.5:
                t0 -= 0.2; t1 += 0.2
            seg = audio[int(t0 * SR):int(t1 * SR)].unsqueeze(0)
            with torch.inference_mode():
                em, _ = model(seg); em = torch.log_softmax(em, -1)
            ali, sc = torchaudio.functional.forced_align(em, torch.tensor([toks], dtype=torch.int32), blank=0)
            spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
            ratio = seg.shape[1] / em.shape[1] / SR
            per = {}
            for ti, sp in enumerate(spans):
                k = owner[ti]
                if k < 0: continue
                a, b = t0 + sp.start * ratio, t0 + sp.end * ratio
                per.setdefault(k, [a, b]); per[k][1] = b
            for k, i in enumerate(wn):
                if k in per: done[i] = [round(per[k][0], 3), round(per[k][1], 3)]
import sys; sys.path.insert(0, 'work'); from vadfix import vadfix
gaps = json.load(open('work/gaps.json'))
tmp = [{'t': done[i][0], 'e': done[i][1], 'i': i} for i in sorted(done)]
nv = vadfix(tmp, gaps)
for x in tmp: done[x['i']] = [x['t'], x['e']]
print(f'{nv} CTC onsets moved out of measured silence')
# A word CTC squeezes to < 50 ms against a pause ("be" 227.279-227.300 in "going to be... slightly") is
# really spoken from where the previous word ended, when no measured silence lies between them.
order = sorted(done)
nsq = 0
for a, b in zip(order, order[1:]):
    pe, (t, e) = done[a][1], done[b]
    # only when it is jammed against a measured pause (its end sits on a gap start); elsewhere a
    # 20 ms word is just a short word ("I", "a") and moving it made captions early
    if e - t < 0.05 and t - pe > 0.08 and any(abs(g0 - e) < 0.03 for g0, g1 in gaps) and not any(g0 < t and g1 > pe for g0, g1 in gaps):
        done[b] = [round(pe + 0.02, 3), e]; nsq += 1
print(f'{nsq} squeezed CTC words re-started at their predecessor\'s end')
# MEASURED overrides (source time), where CTC squeezed a word against the wrong side of a pause and
# the VAD speech bursts say otherwise. Each is checked against the delivered file's own CTC pass.
#   "position, [224.90-225.31 silence] and [225.31-225.56] my [225.75-] arms": CTC put "and" at
#   224.878-224.900 (20 ms, ending on the gap start) and "my" at 225.31; the delivered pass hears
#   "and" at 225.42 and "my" at 225.82.
MANUAL = {(224.878, 'and'): 225.31, (225.31, 'my'): 225.75}
for i in list(done):
    k = (round(done[i][0], 3), words[i]['text'].strip().rstrip(',.').lower())
    if k in MANUAL:
        done[i] = [MANUAL[k], max(done[i][1], MANUAL[k] + 0.1)]
        print('manual onset', k, '->', MANUAL[k])
out = []
moved = []
for i, w in enumerate(words):
    ts = done.get(i, w['timestamp'])
    if i in done: moved.append(ts[0] - w['timestamp'][0])
    out.append({'text': w['text'], 'timestamp': ts})
json.dump({'chunks': out}, open('work/words_aligned.json', 'w'))
m = np.array(moved)
print(f'{len(done)} words aligned; onset shift vs Whisper median {np.median(m)*1000:+.0f} ms, p10 {np.percentile(m,10)*1000:+.0f}, p90 {np.percentile(m,90)*1000:+.0f}')
