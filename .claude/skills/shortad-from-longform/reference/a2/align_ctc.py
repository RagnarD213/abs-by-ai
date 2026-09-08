#!/usr/bin/env python3
"""FORCED ALIGNMENT of the caption words to his mix with a CTC acoustic model (wav2vec2, torchaudio).

Whisper's word timestamps come from attention-DTW and drift by 100-400 ms on a mix with a music
bed; the karaoke highlight then lights the wrong word. A CTC forced aligner places each KNOWN word
on the audio to ~20-40 ms. Aligned per Whisper segment (+0.6 s padding), so memory stays small.
Writes words_ctc.json = [{word, start, end, score}] in the caption word order."""
import json, re, sys, subprocess
import numpy as np, torch, torchaudio
sys.path.insert(0, '.'); import captions as C
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SR = 16000
subprocess.run([FF,'-v','error','-y','-i','his_mix.wav','-ac','1','-ar',str(SR),'-c:a','pcm_s16le','his_mix16.wav'], check=True)
import wave as _w
_f=_w.open('his_mix16.wav'); assert _f.getframerate()==SR
wav = torch.from_numpy(np.frombuffer(_f.readframes(_f.getnframes()), dtype='<i2').astype(np.float32)/32768.0)
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval()
labels = bundle.get_labels()          # ('-', '|', 'E', 'T', ...): blank, word-sep, letters
L = {c: i for i, c in enumerate(labels)}
NUM = {'6': 'SIX', '38': 'THIRTY EIGHT', '100': 'A HUNDRED', '2': 'TWO', '3': 'THREE', '5': 'FIVE', '10': 'TEN', '20': 'TWENTY'}
def norm(w):
    w = w.replace('6PackAbs.com', 'SIX PACK ABS DOT COM')
    w = re.sub(r"[^A-Za-z0-9' ]", ' ', w).upper()
    w = ' '.join(NUM.get(t, t) for t in w.split())
    w = re.sub(r'[0-9]+', lambda m: ' '.join(NUM.get(m.group(0), '')), w)
    return re.sub(r"[^A-Z' ]", '', w).strip()
words = C.load_words()                      # (word, whisper_start, whisper_end), FIX map applied
segs = json.load(open('ref.whisper.json'))['segments']
# assign each caption word to the whisper segment it came from (by time)
out = []
# Segment ownership by ORDER, not by a time window: a word whose Whisper time falls outside its own
# segment was aligned in the wrong audio window and landed hundreds of ms off (21 words on Ad 2 V2).
# The FIX map can drop a token ('6packabs' '.com' -> one word), so ownership is computed on the raw
# Whisper list and carried through the same FIX logic captions.py applies.
raw = [(w['word'].strip(), si) for si, s_ in enumerate(segs) for w in s_.get('words', []) if w['word'].strip()]
own = []
for i in range(len(raw)):
    hit = False
    for src, dst in C.FIX.items():
        k = len(src)
        if tuple(x[0] for x in raw[i:i+k]) == src:
            for j, word in enumerate(dst): raw[i+j] = (word, raw[i+j][1])
    own.append(raw[i][1])
seg_of = [si for (w, si) in raw if w]
assert len(seg_of) == len(words), (len(seg_of), len(words))
for si, s in enumerate(segs):
    sw = [(k, words[k]) for k in range(len(words)) if seg_of[k] == si]
    if not sw: continue
    a = max(0.0, s['start'] - 0.6); b = min(len(wav)/SR, s['end'] + 0.6)
    x = wav[int(a*SR):int(b*SR)]
    with torch.inference_mode():
        em, _ = model(x.unsqueeze(0))
    em = torch.log_softmax(em[0], dim=-1)
    toks = []; spans = []
    for k, w in sw:
        n = norm(w[0])
        if not n:
            spans.append(None); continue
        t = [L['|']] + [L[c] for c in n.replace(' ', '|') if c in L]
        spans.append((len(toks), len(toks) + len(t))); toks += t
    toks.append(L['|'])
    if len(toks) <= 1 or em.shape[0] < len(toks):
        for k, w in sw: out.append(dict(word=w[0], start=w[1], end=w[2], score=0.0, src='whisper'))
        continue
    ali, sc = torchaudio.functional.forced_align(em.unsqueeze(0), torch.tensor([toks]), blank=0)
    ali = ali[0].tolist(); sc = sc[0].exp().tolist()
    # frame index -> token index (collapse repeats/blanks): map each token position to its frame range
    fr = 0.02 * (x.shape[0]/SR) / max(1, em.shape[0]) * SR / SR   # frame duration ~20 ms
    fdur = (x.shape[0]/SR) / em.shape[0]
    tpos = []  # for each token position, (first frame, last frame)
    ti = 0; cur = None; first = {}; last = {}
    prev = None
    for f, tok in enumerate(ali):
        if tok == 0: prev = tok; continue
        if tok == prev and ti > 0 and toks[ti-1] == tok and (ti-1) in last and last[ti-1] == f-1:
            last[ti-1] = f; continue
        if ti < len(toks) and toks[ti] == tok:
            first[ti] = f; last[ti] = f; ti += 1
        else:
            if (ti-1) in last: last[ti-1] = f
        prev = tok
    for (k, w), sp in zip(sw, spans):
        if sp is None or (sp[0]+1) not in first:
            out.append(dict(word=w[0], start=w[1], end=w[2], score=0.0, src='whisper')); continue
        i0, i1 = sp[0] + 1, sp[1] - 1           # skip the leading '|'
        f0 = first.get(i0); f1 = last.get(i1, first.get(i1))
        if f0 is None or f1 is None:
            out.append(dict(word=w[0], start=w[1], end=w[2], score=0.0, src='whisper')); continue
        st = a + f0*fdur; en = a + (f1+1)*fdur
        scs = [sc[f] for f in range(f0, f1+1)]
        out.append(dict(word=w[0], start=round(st,3), end=round(en,3), score=round(float(np.mean(scs)),3), src='ctc'))
# A CTC slip on a tiny word can land it before its predecessor or after its successor (12 of 875 here even
# with exact segment ownership): re-place such a word evenly in the gap between its neighbours.
rep = 0
for i in range(1, len(out)-1):
    p, w, n = out[i-1], out[i], out[i+1]
    if w['start'] < p['end'] - 0.02 or w['start'] > n['start'] - 0.02:
        a, b = p['end'], n['start']
        if b - a < 0.06: b = a + 0.06
        dur = min(max(0.06, 0.4*(b-a)), b-a)
        w['start'] = round(a + 0.5*((b-a)-dur), 3); w['end'] = round(w['start']+dur, 3); w['src'] = 'repaired'; rep += 1
print(f'{rep} misplaced words re-placed between their neighbours')
json.dump(out, open('words_ctc.json','w'), indent=0)
ctc = [o for o in out if o['src']=='ctc']
print(f'{len(out)} words, {len(ctc)} CTC-aligned, {len(out)-len(ctc)} fell back to whisper')
d = np.array([o['start'] - w[1] for o, w in zip(out, words) if o['src']=='ctc'])
print(f'CTC start minus WHISPER start: mean {d.mean()*1000:+.0f} ms  sd {d.std()*1000:.0f}  p10 {np.percentile(d,10)*1000:+.0f}  p90 {np.percentile(d,90)*1000:+.0f}  |d|>150ms: {(np.abs(d)>0.15).sum()} of {len(d)}')
