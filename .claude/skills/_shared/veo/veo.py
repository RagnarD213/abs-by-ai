#!/usr/bin/env python3
"""Subscription-first Veo motion: one job file per video, generated on Dan's Google AI Pro credits in Flow by a background
sub-agent, with the paid Replicate API only when Dan says rush (or approves paying after the credits run out).

Rule and runbook: README.md and FLOW-RUNBOOK.md beside this file. Built 2026-10-17 (Dan: "Default to the subscription; switch to
the paid API only when I say rush, accelerate, or as fast as possible. If the subscription credits run out, ask me before paying.")

usage:
  veo.py route [--said "Dan's words"]                 prints flow or api (api only on rush / accelerate / as fast as possible)
  veo.py add JOBDIR ID --start S.png [--end E.png] --prompt-file P.txt [--seconds 8] [--aspect 16:9] [--model fast]
             [--takes 1] [--skip-gate "why"]          adds a clip to JOBDIR/veo/job.json; approved frames only (framecheck)
  veo.py status JOBDIR                                 table of every clip, its route, takes and timings
  veo.py mark JOBDIR ID submitted|failed|skipped [--note ...] [--credits-left N]   the Flow agent records progress
  veo.py collect JOBDIR ID --from PATH_OR_URL [--credits-left N]   files a finished Flow take as JOBDIR/veo/<ID>-flow-tN.mp4
  veo.py credits [--set N]                             last known Flow credit balance and the spend log
  veo.py api JOBDIR ID (--rush "Dan's words" | --paid-ok "Dan's words")   paid Replicate Veo 3.1 Fast for one clip
"""
import argparse, base64, hashlib, io, json, os, re, shutil, subprocess, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.expanduser("~/.absbyai-veo-ledger.jsonl")     # account-wide: Claude and Codex on this Mac share it
PICKS = os.path.expanduser("~/.absbyai-video-model-picks.jsonl")  # Dan's picks between models, read by the monthly model watch
RUSH = re.compile(r"\b(rush|rushed|rushing|accelerate|accelerated|as fast as possible|asap)\b", re.I)
CREDITS = {"lite": 10, "fast": 20, "quality": 100, "omni": 12}  # Flow per generation, Pro rates 2026-10-17 (Ultra since 10-20 may be lower; the live popover wins)
API_MODEL, API_USD_S = "google/veo-3.1-fast", 0.10            # Replicate, 1080p, no audio


def _find(tool):
    for p in (os.path.join(REPO, "Media/video_edit/bin", tool), f"/Volumes/Extreme/_edit_work/bin/{tool}", shutil.which(tool) or ""):
        if p and os.path.exists(p):
            return p
    raise SystemExit(f"{tool} not found")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def jpath(jobdir):
    return os.path.join(os.path.abspath(jobdir), "veo", "job.json")


def load(jobdir):
    p = jpath(jobdir)
    return json.load(open(p)) if os.path.exists(p) else {"job": os.path.basename(os.path.abspath(jobdir)), "clips": []}


def save(jobdir, J):
    p = jpath(jobdir); os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"; json.dump(J, open(tmp, "w"), indent=1); os.replace(tmp, p)


def update(jobdir, fn):
    """re-read job.json under a lock, apply fn(J), save: two `api` runs at once each wrote back the copy they loaded
    minutes earlier, and the second dropped the first one's take (SL-09 R4, 2026-10-20)."""
    import fcntl
    os.makedirs(os.path.dirname(jpath(jobdir)), exist_ok=True)
    with open(jpath(jobdir) + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX); J = load(jobdir); r = fn(J); save(jobdir, J)
    return r


def clip(J, cid):
    for c in J["clips"]:
        if c["id"] == cid:
            return c
    raise SystemExit(f"{cid}: not in the job (veo.py add first)")


def log(entry):
    with open(LEDGER, "a") as f:
        f.write(json.dumps({"when": now(), **entry}) + "\n")


def ledger():
    return [json.loads(l) for l in open(LEDGER)] if os.path.exists(LEDGER) else []


def stage(src, dst):
    """Flow upload copy: JPEG q95, long side <= 1920, so a START+END pair stays far under the 10 MB upload limit."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    if max(im.size) > 1920:
        k = 1920 / max(im.size); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=95)
    return dst


def probe(p):
    out = subprocess.run([_find("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", p], capture_output=True, text=True)
    d = json.loads(out.stdout or "{}"); s = (d.get("streams") or [{}])[0]
    n, _, m = (s.get("r_frame_rate") or "0/1").partition("/")
    return {"w": s.get("width"), "h": s.get("height"), "fps": round(int(n) / int(m or 1), 3),
            "seconds": round(float(d.get("format", {}).get("duration", 0)), 2)}


# ---------------------------------------------------------------------------- commands
def cmd_route(a):
    rush = bool(os.environ.get("VEO_RUSH")) or bool(a.said and RUSH.search(a.said))
    print("api" if rush else "flow")
    print(("rush: Dan asked for speed, the paid API is allowed (it still counts against the per-video budget)" if rush else
           "default: Flow on the Google AI Pro subscription, run by the flow-veo background agent"), file=sys.stderr)


def cmd_add(a):
    J = load(a.jobdir)
    if any(c["id"] == a.id for c in J["clips"]):
        raise SystemExit(f"{a.id} is already in the job; pick a new id (A1b) for a materially different clip")
    if a.model == "quality" and not a.dan_asked:   # Dan, 2026-10-25: Quality only when he names it (48 Quality clips ate two-thirds of 10-20..23 credits)
        raise SystemExit("Veo Quality costs 10x Fast and is used only when Dan asks for it by name. "
                         "Use --model fast, or pass --dan-asked \"<his exact words>\".")
    if not a.skip_gate and a.end:
        sys.path.insert(0, os.path.join(HERE, "..", "framecheck"))
        from gate import require_pass
        require_pass(a.start, a.end)        # same refusal as every motion generator: approved, gated, reviewed frames only
    up = os.path.join(os.path.dirname(jpath(a.jobdir)), "upload"); os.makedirs(up, exist_ok=True)
    prompt = open(a.prompt_file).read().strip()
    neg = open(a.negative_file).read().strip() if a.negative_file else None
    c = {"id": a.id, "start": os.path.abspath(a.start), "start_sha256": sha(a.start),
         "end": os.path.abspath(a.end) if a.end else None, "end_sha256": sha(a.end) if a.end else None,
         "upload_start": stage(a.start, f"{up}/{a.id}-start.jpg"), "upload_end": stage(a.end, f"{up}/{a.id}-end.jpg") if a.end else None,
         "prompt": prompt, "negative": neg, "seconds": a.seconds, "aspect": a.aspect, "model": a.model, "takes": a.takes,
         "dan_asked": a.dan_asked,
         "gate": f"skipped: {a.skip_gate}" if a.skip_gate else ("framecheck PASS" if a.end else "single frame, no pair gate"),
         "route": "flow", "status": "queued", "added": now(), "outputs": [], "events": []}
    J["clips"].append(c); save(a.jobdir, J)
    print(f"{a.id} queued for Flow ({a.model}, {a.seconds}s, {a.aspect}, {a.takes} take(s), ~{CREDITS[a.model] * a.takes} credits)")


def cmd_status(a):
    J = load(a.jobdir)
    print(f"job {J['job']}  ({jpath(a.jobdir)})")
    for c in J["clips"]:
        outs = ", ".join(f"{os.path.basename(o['file'])} {o['w']}x{o['h']} {o['seconds']}s" for o in c["outputs"]) or "-"
        t = ""
        if c.get("submitted") and c["outputs"]:
            t0 = time.mktime(time.strptime(c["submitted"], "%Y-%m-%d %H:%M:%S"))
            t1 = time.mktime(time.strptime(c["outputs"][-1]["collected"], "%Y-%m-%d %H:%M:%S"))
            t = f"  {int(t1 - t0)}s submit->file"
        print(f"  {c['id']:6} {c['route']:4} {c['status']:9} {c['model']:7} {c['seconds']}s {c['aspect']:5} | {outs}{t}")
    led = [e for e in ledger() if "credits_left" in e]
    if led:
        print(f"Flow credits last seen: {led[-1]['credits_left']} ({led[-1]['when']})")


def _credits(J, c, n, why):
    if n is not None:
        log({"job": J["job"], "clip": c["id"], "event": why, "credits_left": n})


def cmd_mark(a):
    J = load(a.jobdir); c = clip(J, a.id)
    c["status"] = a.state; c["events"].append({"when": now(), "state": a.state, "note": a.note})
    if a.state == "submitted":
        c["submitted"] = now()
    save(a.jobdir, J); _credits(J, c, a.credits_left, a.state)
    if a.state == "submitted":
        log({"job": J["job"], "clip": c["id"], "event": "flow-generation", "model": c["model"], "credits": CREDITS[c["model"]]})
    print(f"{a.id}: {a.state}")


def framediff(video, at, image):
    """Mean absolute grey difference (0-255) between one frame of the take and an image, both at 64x36."""
    from PIL import Image
    raw = subprocess.run([_find("ffmpeg"), "-v", "error", "-sseof" if at < 0 else "-ss", str(abs(at) if at >= 0 else at), "-i", video,
                          "-frames:v", "1", "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    ref = Image.open(image).convert("L").resize((64, 36), Image.BILINEAR).tobytes()
    if len(raw) != len(ref):
        return 999.0
    return round(sum(abs(x - y) for x, y in zip(raw, ref)) / len(ref), 1)


def framecheck(c, out):
    """Flow's picker re-sorts while uploads finish, so a click can land on the wrong frame (2026-10-17: A1 went out with the
    END frame in both slots). The take must OPEN on START, and closer to START than to END. The closing frame is reported but
    only warns: Veo drifts off the END frame in its last frames (RO-20's good API take closed 24.2 from END, 25.2 from START)."""
    s0, e1 = framediff(out, 0, c["start"]), (framediff(out, -0.25, c["end"]) if c["end"] else None)
    s1 = framediff(out, -0.25, c["start"]); e0 = framediff(out, 0, c["end"]) if c["end"] else None
    ok = s0 < 25 and (e0 is None or s0 < e0)
    warn = e1 is not None and e1 >= s1
    return {"open_vs_start": s0, "open_vs_end": e0, "close_vs_end": e1, "close_vs_start": s1, "ok": ok,
            **({"warn": "closes no nearer END than START: look at the ending"} if warn else {})}


def cmd_collect(a):
    J = load(a.jobdir); c = clip(J, a.id)
    d = os.path.dirname(jpath(a.jobdir)); n = len(c["outputs"]) + 1
    while os.path.exists(f"{d}/{a.id}-flow-t{n}.mp4"):
        n += 1                                              # never overwrite a take
    out = f"{d}/{a.id}-flow-t{n}.mp4"
    if re.match(r"https?://", a.src):
        urllib.request.urlretrieve(a.src, out)
    else:
        shutil.copy2(os.path.expanduser(a.src), out)
    meta = probe(out)
    if not meta["w"] or meta["seconds"] < 1:
        os.remove(out); raise SystemExit(f"{a.src} is not a playable video ({meta})")
    fc = framecheck(c, out)
    c["outputs"].append({"file": out, "sha256": sha(out), "collected": now(), "frames": fc, **meta})
    c["status"] = ("done" if len(c["outputs"]) >= c["takes"] else "submitted") if fc["ok"] else "wrong-frames"
    save(a.jobdir, J); _credits(J, c, a.credits_left, "collected")
    print(f"{a.id} take {n}: {out}  {meta['w']}x{meta['h']} {meta['fps']}fps {meta['seconds']}s  frames {fc}")
    if not fc["ok"]:
        raise SystemExit(f"{a.id}: the take does not open on START / close on END. Wrong frame picked in Flow: resubmit with "
                         f"the right frames (search the exact file name, check the preview name before Add to prompt)")


def cmd_credits(a):
    if a.set is not None:
        log({"event": "balance", "credits_left": a.set}); print(f"recorded {a.set}"); return
    L = ledger(); bal = [e for e in L if "credits_left" in e]
    print(f"last known Flow balance: {bal[-1]['credits_left']} at {bal[-1]['when']}" if bal else "no balance recorded yet")
    month = time.strftime("%Y-%m")
    gen = [e for e in L if e.get("event") == "flow-generation" and e["when"].startswith(month)]
    api = [e for e in L if e.get("event") == "api-generation" and e["when"].startswith(month)]
    print(f"{month}: {len(gen)} Flow generations, ~{sum(e['credits'] for e in gen)} credits; "
          f"{len(api)} paid API takes, ${sum(e['usd'] for e in api):.2f}")


def cmd_api(a):
    """The paid path. Only on Dan's rush words, or after he approved paying because the credits ran out; both are recorded."""
    words = a.rush or a.paid_ok
    if a.rush and not RUSH.search(a.rush):
        raise SystemExit("--rush needs Dan's words containing rush / accelerate / as fast as possible")
    J = load(a.jobdir); c = clip(J, a.id)
    d = os.path.dirname(jpath(a.jobdir)); n = len(c["outputs"]) + 1
    while os.path.exists(f"{d}/{a.id}-api-t{n}.mp4") or os.path.exists(f"{d}/{a.id}-api-t{n}.mp4.part"):
        n += 1                                       # never overwrite a take another run is writing or already wrote
    out = f"{d}/{a.id}-api-t{n}.mp4"; open(out + ".part", "w").close()
    from PIL import Image

    def uri(p):
        buf = io.BytesIO(); im = Image.open(p).convert("RGB")
        im.resize((1920, 1080) if c["aspect"] == "16:9" else (1080, 1920), Image.LANCZOS).save(buf, "PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    for k in ("start", "end"):
        if c[k] and sha(c[k]) != c[k + "_sha256"]:
            raise SystemExit(f"{c[k]} changed since it was approved")
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
             if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    inp = {"prompt": c["prompt"], "image": uri(c["start"]), "duration": c["seconds"], "resolution": "1080p",
           "aspect_ratio": c["aspect"], "generate_audio": False}
    if c["end"]:
        inp["last_frame"] = uri(c["end"])
    if c["negative"]:
        inp["negative_prompt"] = c["negative"]

    def call(req):
        for k in range(6):
            try:
                return json.load(urllib.request.urlopen(req, timeout=120))
            except urllib.error.HTTPError as e:
                body = e.read().decode()[:300]
                if e.code in (429, 500, 502, 503) or "E005" in body:
                    time.sleep(15 * (k + 1)); continue
                raise SystemExit(f"HTTP {e.code}: {body}")
        raise SystemExit("gave up after 6 tries")
    t0 = time.time()
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{API_MODEL}/predictions",
                                    data=json.dumps({"input": inp}).encode(), headers=H))
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    usd = c["seconds"] * API_USD_S if p["status"] == "succeeded" else 0.0
    log({"job": J["job"], "clip": c["id"], "event": "api-generation", "usd": usd, "why": words, "id": p["id"], "status": p["status"]})
    if p["status"] != "succeeded":
        if os.path.exists(out + ".part"): os.remove(out + ".part")
        raise SystemExit(f"{a.id}: {p['status']} {p.get('error')}")
    o = p.get("output"); urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, out)
    rec = {"file": out, "sha256": sha(out), "collected": now(), "usd": usd, "why": words, "wall_s": int(time.time() - t0), **probe(out)}

    def add(J2):
        c2 = clip(J2, a.id); c2["route"] = "api"; c2["outputs"].append(rec); c2["status"] = "done"
    update(a.jobdir, add)
    if os.path.exists(out + ".part"): os.remove(out + ".part")
    print(f"{a.id}: {out} (${usd:.2f}, {int(time.time() - t0)}s)")


def cmd_pick(a):
    """Record which model's take Dan chose when he compared takes of the SAME shot made by different models."""
    models = [m.strip() for m in a.compared.split(",") if m.strip()]
    if a.winner != "same" and a.winner not in models:
        raise SystemExit(f"--winner must be one of {models} or 'same'")
    e = {"when": now(), "video": a.video, "shot": a.shot, "compared": models, "winner": a.winner,
         "blind": not a.not_blind, "dan_words": a.words, "kind": a.kind}
    with open(PICKS, "a") as f:
        f.write(json.dumps(e) + "\n")
    print(f"recorded: {a.shot} -> {a.winner}")


def cmd_picks(a):
    """Running scorecard of Dan's model picks."""
    rows = [json.loads(l) for l in open(PICKS)] if os.path.exists(PICKS) else []
    if a.since: rows = [r for r in rows if r["when"][:10] >= a.since]
    score = {}
    for r in rows:
        for m in r["compared"]:
            s = score.setdefault(m, {"compared": 0, "won": 0, "tied": 0})
            s["compared"] += 1
            if r["winner"] == m: s["won"] += 1
            elif r["winner"] == "same": s["tied"] += 1
    print(f"{len(rows)} picks{' since ' + a.since if a.since else ''} ({PICKS})")
    for m, s in sorted(score.items(), key=lambda kv: -kv[1]["won"]):
        print(f"  {m:24s} won {s['won']:3d}  tied {s['tied']:3d}  of {s['compared']:3d} compared")


if __name__ == "__main__":
    P = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    S = P.add_subparsers(dest="cmd", required=True)
    s = S.add_parser("route"); s.add_argument("--said")
    s = S.add_parser("add"); s.add_argument("jobdir"); s.add_argument("id"); s.add_argument("--start", required=True)
    s.add_argument("--end"); s.add_argument("--prompt-file", required=True); s.add_argument("--negative-file")
    s.add_argument("--seconds", type=int, default=8, choices=(4, 6, 8, 10)); s.add_argument("--aspect", default="16:9", choices=("16:9", "9:16"))
    s.add_argument("--model", default="fast", choices=tuple(CREDITS)); s.add_argument("--takes", type=int, default=1)
    s.add_argument("--skip-gate"); s.add_argument("--dan-asked", help="Dan's exact words asking for Veo Quality (required for --model quality)")
    s = S.add_parser("status"); s.add_argument("jobdir")
    s = S.add_parser("mark"); s.add_argument("jobdir"); s.add_argument("id"); s.add_argument("state", choices=("submitted", "failed", "skipped"))
    s.add_argument("--note"); s.add_argument("--credits-left", type=int)
    s = S.add_parser("collect"); s.add_argument("jobdir"); s.add_argument("id"); s.add_argument("--from", dest="src", required=True)
    s.add_argument("--credits-left", type=int)
    s = S.add_parser("credits"); s.add_argument("--set", type=int)
    s = S.add_parser("api"); s.add_argument("jobdir"); s.add_argument("id"); g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--rush"); g.add_argument("--paid-ok")
    s = S.add_parser("pick"); s.add_argument("--video", required=True, help="recognizable title, e.g. 'Make Time Exercise (RO-18)'")
    s.add_argument("--shot", required=True); s.add_argument("--compared", required=True, help="comma list, e.g. veo-3.1-fast,omni-1.1-flash")
    s.add_argument("--winner", required=True, help="one of --compared, or same"); s.add_argument("--words", help="Dan's reason, verbatim")
    s.add_argument("--kind", default="work", choices=("work", "bakeoff")); s.add_argument("--not-blind", action="store_true")
    s = S.add_parser("picks"); s.add_argument("--since")
    a = P.parse_args()
    globals()["cmd_" + a.cmd](a)
