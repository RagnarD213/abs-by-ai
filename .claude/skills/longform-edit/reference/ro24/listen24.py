"""RO-24 blind voice ranking, repeated N times with fresh letters and send order (RO-20: one Gemini listen swung 2 to 9).
Reference: the Bill Maher R3 sample Dan approved 2026-10-20 (Balanced voice, same lav and room), for tone only."""
import sys, os, json, random, shutil, subprocess, re, collections
W = '/Volumes/Expansion/_edit_work/RO-24/round1'; O = f'{W}/audio/opts'; N = int(sys.argv[1]); seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
keys = sorted(json.load(open(f'{O}/options.json'))['options'])
Q = ("You are a dialogue mixer. Clip _reference.mp3 is a finished voice mix the client approved (a different video recorded with the same "
     "microphone in the same room), for tone only. The other clips are the SAME 26 seconds of one talking-head take, level matched, processed "
     f"{len(keys)} ways. You are not told what was done to each. Listen to each fully. Score each 1-10 for how good it sounds as a finished "
     "YouTube voice (room echo, harshness, sibilance, boominess, muddiness, hiss, chopped word endings, thinness all count against it). "
     'Answer with JSON only: {"scores": {"<clip file name>": {"score": n, "room": true|false, "chopped": true|false, "fault": "..."}}, "ship": "<clip file name>"}')
res = collections.defaultdict(list); ships = collections.Counter()
for i in range(N):
    rng = random.Random(seed0 + i); d = f'{O}/trial{seed0+i}'; os.makedirs(d, exist_ok=True)
    letters = rng.sample('ABCDEFGHJKLMN', len(keys)); m = dict(zip(letters, rng.sample(keys, len(keys))))
    for L, k in m.items(): shutil.copy(f'{O}/{k}.mp3', f'{d}/clip_{L}.mp3')
    shutil.copy(f'{O}/_reference.mp3', f'{d}/_reference.mp3'); open(f'{d}/q.txt', 'w').write(Q)
    order = [f'{d}/clip_{L}.mp3' for L in rng.sample(letters, len(keys))]
    r = subprocess.run(['python3', f'{W}/recipe/gemini_listen.py', f'{d}/q.txt', f'{d}/_reference.mp3'] + order, capture_output=True, text=True,
                       env=dict(os.environ, GM='gemini-3.1-pro-preview'))
    open(f'{d}/answer.txt', 'w').write(r.stdout + r.stderr); json.dump(m, open(f'{d}/map.json', 'w'))
    try:
        j = json.loads(re.search(r'\{.*\}', r.stdout.split('USAGE')[0], re.S).group(0))
        for name, v in j['scores'].items():
            L = re.search(r'clip_([A-Z])', name).group(1); res[m[L]].append((v['score'], v.get('room'), v.get('chopped'), v.get('fault')))
        L = re.search(r'clip_([A-Z])', j['ship']).group(1); ships[m[L]] += 1
        print(i, {m[re.search(r'clip_([A-Z])', n).group(1)]: v['score'] for n, v in j['scores'].items()}, 'ship', m[L], flush=True)
    except Exception as e: print(i, 'parse failed', e, r.stdout[:200], r.stderr[:200], flush=True)
summary = {}
for k in keys:
    v = res[k]
    if v:
        summary[k] = dict(mean=round(sum(s for s, *_ in v) / len(v), 2), scores=[s for s, *_ in v], room=sum(1 for _, r, _, _ in v if r),
                          chopped=sum(1 for _, _, c, _ in v if c), shipped=ships[k], faults=[f for *_, f in v])
        print(f"{k:18s} mean {summary[k]['mean']:.1f} scores {summary[k]['scores']} room {summary[k]['room']}/{len(v)} chopped {summary[k]['chopped']}/{len(v)} shipped {ships[k]}")
json.dump(summary, open(f'{O}/trials_{seed0}.json', 'w'), indent=1)
print('LISTEN DONE')
