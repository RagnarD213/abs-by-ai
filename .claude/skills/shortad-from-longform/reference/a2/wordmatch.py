#!/usr/bin/env python3
"""Word-level DP alignment of our conformed voice against HIS cut's transcript.
The one check that proves the EDL: a missing word is a word he said and we did not."""
import json, re, sys
import numpy as np
n = lambda s: re.sub(r"[^a-z0-9]", '', s.lower())
def W(p):
    d = json.load(open(p))
    return [(n(w['word']), float(w['start']), float(w['end']))
            for s in d['segments'] for w in s.get('words', []) if n(w['word'])]
H = W('m.whisper.json'); O = W(sys.argv[1])
a = [x[0] for x in H]; b = [x[0] for x in O]
NA, NB = len(a), len(b)
D = np.zeros((NA+1, NB+1), dtype=np.int32); D[:, 0] = np.arange(NA+1); D[0, :] = np.arange(NB+1)
P = np.zeros((NA+1, NB+1), dtype=np.int8)
for i in range(1, NA+1):
    ai = a[i-1]; row = D[i-1]; cur = D[i]
    for j in range(1, NB+1):
        m = row[j-1] + (0 if ai == b[j-1] else 1); d1 = row[j]+1; d2 = cur[j-1]+1
        best = min(m, d1, d2); cur[j] = best
        P[i, j] = 0 if best == m else (1 if best == d1 else 2)
i, j = NA, NB; match = 0; miss = []
while i > 0 and j > 0:
    if P[i, j] == 0:
        if a[i-1] == b[j-1]: match += 1
        else: miss.append((H[i-1][1], a[i-1], b[j-1]))
        i -= 1; j -= 1
    elif P[i, j] == 1: miss.append((H[i-1][1], a[i-1], '(missing)')); i -= 1
    else: j -= 1
while i > 0: miss.append((H[i-1][1], a[i-1], '(missing)')); i -= 1
miss.sort()
gaps = [m for m in miss if m[2] == '(missing)']
print(f'his {NA} words, ours {NB}, matched {match} = {100*match/NA:.1f}%   absent {len(gaps)}')
for t, x, y in miss: print(f'  {t:7.2f}  his "{x}"  ->  ours "{y}"')
