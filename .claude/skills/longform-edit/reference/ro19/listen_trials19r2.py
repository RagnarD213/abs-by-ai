"""RO-19 round 2: the blind voice ranking as a CROSS-CHECK only (Dan picks by ear). N trials, fresh letters and send order each
time, all options in audio/opts2/options.json. First a speech check on one option (Dan, 2026-10-11: an audition clip starts on speech).
usage: listen_trials19r2.py check | N [seed]"""
import sys, os, json, random, shutil, subprocess, re, collections
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/audio/opts2"
keys = sorted(json.load(open(f"{O}/options.json")))
def ask(q, clips, d):
    os.makedirs(d, exist_ok=True); open(f"{d}/q.txt", "w").write(q)
    r = subprocess.run(["python3", f"{W}/recipe/gemini_listen.py", f"{d}/q.txt"] + clips, capture_output=True, text=True, env=dict(os.environ, GM="gemini-3.1-pro-preview"))
    open(f"{d}/answer.txt", "w").write(r.stdout + r.stderr); return r.stdout
if sys.argv[1] == "check":
    print(ask("Listen to this clip. Answer with JSON only: {\"first_words\": \"<the first eight words spoken>\", \"speech_starts_within_first_second\": true|false, "
              "\"longest_silence_seconds\": n, \"continuous_speech\": true|false, \"seconds_of_speech\": n}", [f"{O}/W1-light.mp3"], f"{O}/check")); sys.exit()
N = int(sys.argv[1]); seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 200; n = len(keys)
Q = (f"You are a dialogue mixer. Clip _reference.mp3 is a voice mix the client likes (a different video, for tone only). The {n} other clips are the SAME 31 seconds "
     "of one talking-head take recorded in a kitchen, level matched, processed in different ways. You are not told what was done to each. Listen to each fully. Score each 1-10 for how good it "
     "sounds as a finished YouTube voice (room echo, harshness, sibilance, boominess, hiss, chopped word endings, thinness, underwater or swirly processing all count against it). "
     'Answer with JSON only: {"scores": {"<clip file name>": {"score": n, "room": true|false, "boomy": true|false, "processed": true|false, "fault": "..."}}, "ship": "<clip file name>"}')
res = collections.defaultdict(list); ships = collections.Counter()
for i in range(N):
    rng = random.Random(seed0 + i); d = f"{O}/trial{seed0+i}"; os.makedirs(d, exist_ok=True)
    letters = rng.sample("ABCDEFGHJKLMNPQRSTUVWXYZ", n); m = dict(zip(letters, rng.sample(keys, n)))
    for L, k in m.items(): shutil.copy(f"{O}/{k}.mp3", f"{d}/clip_{L}.mp3")
    shutil.copy(f"{O}/_reference.mp3", f"{d}/_reference.mp3"); json.dump(m, open(f"{d}/map.json", "w"))
    out = ask(Q, [f"{d}/_reference.mp3"] + [f"{d}/clip_{L}.mp3" for L in rng.sample(letters, n)], d)
    try:
        j = json.loads(re.search(r"\{.*\}", out.split("USAGE")[0], re.S).group(0))
        for name, v in j["scores"].items():
            L = re.search(r"clip_([A-Z])", name).group(1); res[m[L]].append((v["score"], v.get("room"), v.get("boomy"), v.get("processed")))
        L = re.search(r"clip_([A-Z])", j["ship"]).group(1); ships[m[L]] += 1
        print(i, {m[re.search(r'clip_([A-Z])', nm).group(1)]: v["score"] for nm, v in j["scores"].items()}, "ship", m[L], flush=True)
    except Exception as e: print(i, "parse failed", e, out[:200], flush=True)
for k in keys:
    v = res[k]
    if v: print(f"{k:22s} mean {sum(s[0] for s in v)/len(v):.1f}  scores {[s[0] for s in v]}  room heard {sum(1 for s in v if s[1])}/{len(v)}  boomy {sum(1 for s in v if s[2])}/{len(v)}  processed {sum(1 for s in v if s[3])}/{len(v)}  shipped {ships[k]}")
json.dump({k: res[k] for k in keys}, open(f"{O}/trials_{seed0}.json", "w"))
