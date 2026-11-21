#!/usr/bin/env python3
"""RO-20 round 3b: blind join listen. For each pickup treatment (round3b/opts/<opt>/P#.voice.wav) build the three join clips Dan will hear
(video 2 open: film > P2 > film; video 3 open: P4 tail > film; video 1 end: film > P1 > sign-off), then ask a blind listener, N times with fresh
letters and order, how noticeable the voice change is at each join. usage: join_listen20b.py N [seed]"""
import sys, os, json, random, subprocess, re, collections, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3b/listen"; C = f"{W}/round3/context"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OPTS = ["chain", "match", "raw"]; SR = 48000
def film(p, a=None, b=None):
    cmd = [FF, "-v", "error"] + (["-ss", str(a)] if a is not None else []) + ["-i", p] + (["-t", str(b)] if b is not None else []) + ["-ac", "1", "-ar", "48000", "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(float)/32768
def rd(p): w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)/32768
def dur(p): return float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def fade(x, n=576): x = x.copy(); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n); return x
def mp3(x, out):
    subprocess.run([FF, "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-b:a", "160k", out], input=(np.clip(x, -1, 1)*32767).astype("<i2").tobytes(), check=True)
def build():
    os.makedirs(O, exist_ok=True)
    v2o = film(f"{C}/v2open-context.mp4"); v2o = v2o[-int(7*SR):]; v2f = film(f"{C}/v2film-context.mp4", 0, 7)
    v3f = film(f"{C}/v3film-context.mp4", 0, 8); v1e = film(f"{C}/v1end-context.mp4"); v1e = v1e[-int(7*SR):]; so = film(f"{C}/v1-signoff.mp4", 0, 7)
    for o in OPTS:
        p = {k: rd(f"{W}/round3b/opts/{o}/{k}.voice.wav") for k in ("P1", "P2", "P4")}
        mp3(np.concatenate([fade(v2o), fade(p["P2"]), fade(v2f)]), f"{O}/{o}_v2open.mp3")
        mp3(np.concatenate([fade(p["P4"][-int(10*SR):]), fade(v3f)]), f"{O}/{o}_v3open.mp3")
        mp3(np.concatenate([fade(v1e), fade(p["P1"]), fade(so)]), f"{O}/{o}_v1end.mp3")
Q = ("You are a dialogue mixer checking audio pickups. Each clip below is ONE spoken passage by one man in which part was recorded on a different day "
     "in a different room and inserted (in some clips the insert is in the middle, in some at the start). All clips of one passage are the same words, "
     "treated different ways. Listen to each clip fully. For each clip, find where the recording changes and score how NOTICEABLE the change is to an "
     "ordinary viewer, 1 (cannot hear any change) to 10 (obviously a different recording). Describe in a few words what changes (tone, room, level, "
     "noise, closeness). Answer with JSON only: "
     '{"scores": {"<clip file name>": {"noticeable": n, "change_at_seconds": [..], "what": "..."}}, "least_noticeable": "<clip file name>"}')
def trial(join, seed):
    rng = random.Random(seed); d = f"{O}/{join}_t{seed}"; os.makedirs(d, exist_ok=True); letters = rng.sample("ABCDEFGHJK", len(OPTS)); m = dict(zip(letters, rng.sample(OPTS, len(OPTS))))
    for L, k in m.items(): subprocess.run(["cp", f"{O}/{k}_{join}.mp3", f"{d}/clip_{L}.mp3"], check=True)
    open(f"{d}/q.txt", "w").write(Q); order = [f"{d}/clip_{L}.mp3" for L in rng.sample(letters, len(letters))]
    r = subprocess.run(["python3", f"{W}/recipe/gemini_listen.py", f"{d}/q.txt"] + order, capture_output=True, text=True, env=dict(os.environ, GM="gemini-3.1-pro-preview"))
    open(f"{d}/answer.txt", "w").write(r.stdout + r.stderr); json.dump(m, open(f"{d}/map.json", "w"))
    j = json.loads(re.search(r"\{.*\}", r.stdout.split("USAGE")[0], re.S).group(0))
    sc = {m[re.search(r"clip_([A-Z])", n).group(1)]: v for n, v in j["scores"].items()}
    return sc, m[re.search(r"clip_([A-Z])", j["least_noticeable"]).group(1)]
if __name__ == "__main__":
    build(); N = int(sys.argv[1]); s0 = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    res = collections.defaultdict(list); best = collections.Counter()
    for join in ("v2open", "v3open", "v1end"):
        for i in range(N):
            try:
                sc, b = trial(join, s0 + i); best[b] += 1
                for k, v in sc.items(): res[k].append((join, v["noticeable"], v.get("what", "")))
                print(join, i, {k: v["noticeable"] for k, v in sc.items()}, "least:", b, flush=True)
            except Exception as e: print(join, i, "failed", e, flush=True)
    for k in OPTS:
        v = res[k]; print(f"{k:6s} mean noticeable {np.mean([s for _, s, _ in v]):.1f}  {[s for _, s, _ in v]}  least-noticeable picks {best[k]}")
        for j, s, w in v: print(f"    {j} {s}: {w}")
    json.dump(dict(res=res, best=best), open(f"{O}/result_{s0}.json", "w"), indent=1)
