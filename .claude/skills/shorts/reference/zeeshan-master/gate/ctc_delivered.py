#!/usr/bin/env python3
"""speech_words for the gate: the DELIVERED file's audio, its own ASR transcript (gate/<S>_asr.json,
Whisper on the delivered mp3), re-timed by CTC forced alignment (torchaudio WAV2VEC2_ASR_BASE_960H)
in windows split at the ASR's own long gaps. Whisper's own word times smear onsets across pauses by
~400 ms on this mix (measured at 2.36 vs a real onset 2.80), which is why they are not used as timing.
Independent of the caption times, which come from the SOURCE Whisper pass + VAD onset correction.
usage: ctc_delivered.py S delivered.mp4"""
import json, re, sys, subprocess, numpy as np, torch, torchaudio, wave
S, video = sys.argv[1], sys.argv[2]
FF = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').FF))"]))
SR = 16000
wav16 = f'gate/{S}_deliv16.wav'
subprocess.run([FF, '-v', 'error', '-y', '-i', video, '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', wav16], check=True)
f = wave.open(wav16); audio = torch.from_numpy(np.frombuffer(f.readframes(f.getnframes()), '<i2').astype(np.float32) / 32768.0)
asr = [c for c in json.load(open(f'gate/{S}_asr.json'))['chunks'] if c['text'].strip()]
# Whisper sometimes stamps the LAST words before a music-only stretch with a bogus zero-length time
# at the end of the file (F: "workout, then do three or four rounds." all at 55.96-55.96). They are
# REAL words (the earlier version of this script dropped them and the gate then found the speech
# with no word under it). Re-time every zero-length word to follow the word before it, so it lands
# in that word's CTC window and the aligner places it on the audio.
n0 = sum(1 for c in asr if c['timestamp'][1] is not None and c['timestamp'][1] - c['timestamp'][0] < 0.01)
for i, c in enumerate(asr):
    if i and c['timestamp'][1] is not None and c['timestamp'][1] - c['timestamp'][0] < 0.01:
        p = asr[i - 1]['timestamp']
        c['timestamp'] = [round(p[1] + 0.02, 3), round(p[1] + 0.30, 3)]
print(f're-timed {n0} zero-length ASR word(s) to follow their predecessor')
json.dump({'chunks': asr}, open(f'gate/{S}_asr_clean.json', 'w'))
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval(); labels = bundle.get_labels(); L = {c: i for i, c in enumerate(labels)}
NUM = {'30': 'THIRTY', '2': 'TWO', '3': 'THREE', '4': 'FOUR', '10': 'TEN', '5': 'FIVE', '6': 'SIX', '15': 'FIFTEEN', '90': 'NINETY'}
def norm(w):
    w = re.sub(r"[^A-Za-z0-9' ]", ' ', w).upper()
    w = ' '.join(NUM.get(t, t) for t in w.split())
    return re.sub(r"[^A-Z' ]", '', w).strip()
# windows: break where the ASR shows >= 0.35 s between words, or every ~12 s
wins, cur = [], []
for i, c in enumerate(asr):
    if cur and (c['timestamp'][0] - cur[-1]['timestamp'][1] >= 0.35 or c['timestamp'][0] - cur[0]['timestamp'][0] > 12):
        wins.append(cur); cur = []
    cur.append(c)
if cur: wins.append(cur)
out = []
for wn in wins:
    t0 = max(0.0, wn[0]['timestamp'][0] - 0.6); t1 = min(len(audio) / SR, (wn[-1]['timestamp'][1] or wn[-1]['timestamp'][0]) + 0.6)
    while (t1 - t0) < 0.03 * sum(len(norm(c['text'])) + 1 for c in wn) + 0.5:   # CTC needs >= 1 frame (20 ms) per token; 30 ms per char is ample and only a one-word window grows
        t0 = max(0.0, t0 - 0.25); t1 = min(len(audio) / SR, t1 + 0.25)
    seg = audio[int(t0 * SR):int(t1 * SR)].unsqueeze(0)
    toks, owner = [], []
    for k, c in enumerate(wn):
        n = norm(c['text'])
        for j, ch in enumerate(n.replace(' ', '|')):
            if ch in L: toks.append(L[ch]); owner.append(k)
        toks.append(L['|']); owner.append(-1)
    toks = toks[:-1]; owner = owner[:-1]
    with torch.inference_mode():
        em, _ = model(seg); em = torch.log_softmax(em, -1)
    ali, sc = torchaudio.functional.forced_align(em, torch.tensor([toks], dtype=torch.int32), blank=0)
    ali = ali[0].tolist(); ratio = seg.shape[1] / em.shape[1] / SR
    # token spans
    spans = torchaudio.functional.merge_tokens(torch.tensor(ali), sc[0].exp())
    per = {}
    for ti, sp in enumerate(spans):
        k = owner[ti]
        if k < 0: continue
        a, b = t0 + sp.start * ratio, t0 + sp.end * ratio
        per.setdefault(k, [a, b]); per[k][1] = b
    for k, c in enumerate(wn):
        if k in per:
            out.append({'w': c['text'].strip(), 't': round(per[k][0], 3), 'e': round(per[k][1], 3), 'src': 'ctc'})
# the same measured-silence rule on the DELIVERED audio's own VAD (work/vad.py on the delivered file)
import sys; sys.path.insert(0, 'work'); from vadfix import vadfix
subprocess.run([FF, '-v', 'error', '-y', '-i', video, '-vn', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', f'gate/{S}_deliv48.wav'], check=True)
subprocess.run(['python3', 'work/vad.py', f'gate/{S}_deliv48.wav', f'gate/{S}_deliv_gaps.json'], check=True, capture_output=True)
print('delivered VAD moved', vadfix(out, json.load(open(f'gate/{S}_deliv_gaps.json'))), 'onsets out of silence')
json.dump(out, open(f'gate/{S}_speech_ctc.json', 'w'))
print(S, len(asr), 'asr words ->', len(out), 'aligned in', len(wins), 'windows')
