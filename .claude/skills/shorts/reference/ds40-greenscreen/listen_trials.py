"""DS-40 R1: blind voice ranking, repeated with fresh letters/order (adapted from ro20/listen_trials.py)."""
import sys, os, json, random, shutil, subprocess, re, collections
O = "/Volumes/Extreme/_edit_work/ds40/r1/audio/a30/opts"; R = "/Volumes/Extreme/_edit_work/ds40/r1/recipe"
N = int(sys.argv[1]); seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
keys = sorted(k[:-4] for k in os.listdir(O) if k.endswith(".mp3") and not k.startswith("_") and not k.startswith("."))
n = len(keys)
Q = (f"You are a dialogue mixer. Clip _reference.mp3 is a voice mix the client likes (a different video and microphone, for tone only). The {n} other clips are the SAME 31 seconds "
     "of one talking-head take, level matched, processed in different ways. You are not told what was done to each. Listen to each fully. Score each 1-10 for how good it "
     "sounds as a finished YouTube Shorts voice on a phone (echo, harshness, sibilance, boominess, muddiness, hiss, chopped word endings, thinness all count against it). "
     'Answer with JSON only: {"scores": {"<clip file name>": {"score": n, "room": true|false, "chopped": true|false, "boomy": true|false, "fault": "..."}}, "ship": "<clip file name>"}')
res = collections.defaultdict(list); ships = collections.Counter()
for i in range(N):
    rng = random.Random(seed0 + i); d = f"{O}/../trial{seed0+i}"; os.makedirs(d, exist_ok=True)
    letters = rng.sample("ABCDEFGHJKLMN", n); m = dict(zip(letters, rng.sample(keys, n)))
    for L, k in m.items(): shutil.copy(f"{O}/{k}.mp3", f"{d}/clip_{L}.mp3")
    shutil.copy(f"{O}/_reference.mp3", f"{d}/_reference.mp3"); open(f"{d}/q.txt", "w").write(Q)
    order = [f"{d}/clip_{L}.mp3" for L in rng.sample(letters, n)]
    r = subprocess.run(["python3", f"{R}/gemini_listen.py", f"{d}/q.txt", f"{d}/_reference.mp3"] + order, capture_output=True, text=True, env=dict(os.environ, GM="gemini-3.1-pro-preview"))
    open(f"{d}/answer.txt", "w").write(r.stdout + r.stderr); json.dump(m, open(f"{d}/map.json", "w"))
    try:
        j = json.loads(re.search(r"\{.*\}", r.stdout.split("USAGE")[0], re.S).group(0))
        for name, v in j["scores"].items():
            L = re.search(r"clip_([A-Z])", name).group(1); res[m[L]].append((v["score"], v.get("room"), v.get("chopped"), v.get("boomy")))
        L = re.search(r"clip_([A-Z])", j["ship"]).group(1); ships[m[L]] += 1
        print(i, {m[re.search(r'clip_([A-Z])', nm).group(1)]: v["score"] for nm, v in j["scores"].items()}, "ship", m[L], r.stdout.split("USAGE")[-1].strip(), flush=True)
    except Exception as e: print(i, "parse failed", e, r.stdout[:200], r.stderr[:200], flush=True)
for k in keys:
    v = res[k]
    if v: print(f"{k:16s} mean {sum(x[0] for x in v)/len(v):.1f}  scores {[x[0] for x in v]}  room {sum(1 for x in v if x[1])}/{len(v)}  chopped {sum(1 for x in v if x[2])}/{len(v)}  boomy {sum(1 for x in v if x[3])}/{len(v)}  shipped {ships[k]}")
json.dump({k: res[k] for k in keys}, open(f"{O}/../trials_{seed0}.json", "w"))
