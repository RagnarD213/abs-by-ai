"""Repeat the blind voice ranking N times with fresh random letters and send order, ask for JSON scores, and average per
treatment. One Gemini listen swung 2 to 9 on the same clip between two runs (RO-20), so a single ranking decides nothing."""
import sys, os, json, random, shutil, subprocess, re, collections
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/audio/opts"; N = int(sys.argv[1]); seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
keys = sorted(json.load(open(f"{O}/options.json")))
Q = ("You are a dialogue mixer. Clip _reference.mp3 is a voice mix the client likes (a different video, for tone only). The five other clips are the SAME 31 seconds "
     "of one talking-head take, level matched, processed five ways. You are not told what was done to each. Listen to each fully. Score each 1-10 for how good it "
     "sounds as a finished YouTube voice (echo, harshness, sibilance, boominess, hiss, chopped word endings, thinness all count against it). "
     'Answer with JSON only: {"scores": {"<clip file name>": {"score": n, "room": true|false, "chopped": true|false, "fault": "..."}}, "ship": "<clip file name>"}')
res = collections.defaultdict(list); ships = collections.Counter()
for i in range(N):
    rng = random.Random(seed0 + i); d = f"{O}/trial{seed0+i}"; os.makedirs(d, exist_ok=True)
    letters = rng.sample("ABCDEFGHJKLMN", 5); m = dict(zip(letters, rng.sample(keys, 5)))
    for L, k in m.items(): shutil.copy(f"{O}/{k}.mp3", f"{d}/clip_{L}.mp3")
    shutil.copy(f"{O}/_reference.mp3", f"{d}/_reference.mp3"); open(f"{d}/q.txt", "w").write(Q)
    order = [f"{d}/clip_{L}.mp3" for L in rng.sample(letters, 5)]
    r = subprocess.run(["python3", f"{W}/recipe/gemini_listen.py", f"{d}/q.txt", f"{d}/_reference.mp3"] + order, capture_output=True, text=True, env=dict(os.environ, GM="gemini-3.1-pro-preview"))
    open(f"{d}/answer.txt", "w").write(r.stdout + r.stderr); json.dump(m, open(f"{d}/map.json", "w"))
    try:
        j = json.loads(re.search(r"\{.*\}", r.stdout.split("USAGE")[0], re.S).group(0))
        for name, v in j["scores"].items():
            L = re.search(r"clip_([A-Z])", name).group(1); res[m[L]].append((v["score"], v.get("room"), v.get("chopped")))
        L = re.search(r"clip_([A-Z])", j["ship"]).group(1); ships[m[L]] += 1
        print(i, {m[re.search(r'clip_([A-Z])', n).group(1)]: v["score"] for n, v in j["scores"].items()}, "ship", m[L], flush=True)
    except Exception as e: print(i, "parse failed", e, r.stdout[:200], r.stderr[:200], flush=True)
for k in keys:
    v = res[k]
    if v: print(f"{k:24s} mean {sum(s for s,_,_ in v)/len(v):.1f}  scores {[s for s,_,_ in v]}  room heard {sum(1 for _,r,_ in v if r)}/{len(v)}  chopped {sum(1 for _,_,c in v if c)}/{len(v)}  shipped {ships[k]}")
json.dump({k: res[k] for k in keys}, open(f"{O}/trials_{seed0}.json", "w"))
