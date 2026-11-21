#!/usr/bin/env python3
"""gen_motion.py ID:DUR[:take] ... -> takes/<ID>_t<take>.mp4 from round3 aiframes, refuses pairs without gate+review PASS."""
import sys, subprocess, json, os, time
from concurrent.futures import ThreadPoolExecutor
ROOT = "/Volumes/Extreme/_edit_work/RO-17/round3"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, REPO + "/.claude/skills/_shared/framecheck")
VEO = REPO + "/.claude/skills/ai-clip-ideas/reference/gen-veo-keyframes.js"
RATE = 0.15

def one(spec):
    parts = spec.split(":"); i, dur = parts[0], int(parts[1]); take = parts[2] if len(parts) > 2 else "1"
    pf = parts[3] if len(parts) > 3 else f"{ROOT}/motion/prompts/{i}.txt"
    from gate import require_pass
    s, e = f"{ROOT}/aiframes/{i}-start.png", f"{ROOT}/aiframes/{i}-end.png"
    require_pass(s, e)
    out = f"{ROOT}/motion/takes/{i}_t{take}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    for attempt in range(8):                      # a 429 on submit is refused before any charge: wait and resubmit
        r = subprocess.run(["node", VEO, "--start", s, "--end", e, "--prompt-file", pf, "--out", out, "--duration", str(dur)],
                           capture_output=True, text=True)
        if "HTTP 429" not in r.stderr: break
        time.sleep(20 + 10 * attempt)
    ok = r.returncode == 0 and os.path.exists(out)
    charged = "submitted" in r.stdout
    rec = dict(id=i, take=take, dur=dur, usd=dur * RATE if charged else 0.0, ok=ok, out=out, prompt=pf, secs=round(time.time() - t0),
               err=r.stderr[-300:] if not ok else "")
    with open(f"{ROOT}/motion/spend.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)
    return rec

if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex: list(ex.map(one, sys.argv[1:]))
    tot = sum(json.loads(l)["usd"] for l in open(f"{ROOT}/motion/spend.jsonl"))
    print("Veo spend so far (charged even on failure, assumed):", round(tot, 2))
