"""RO-11 opener motion: approved C-start.png -> C-end.png (first + last frame), Veo 3.1 through Replicate.
usage: gen_motion.py <tag> [duration=6] [model=google/veo-3.1-fast] [prompt file=motion_C.txt]  (a <prompt file minus .txt>.neg.txt beside it is sent as the negative prompt)
Writes aiframes/<tag>.mp4 + <tag>.json (prediction id, model, seconds, prompt). Never import this file (RO-12 trap 12)."""
import base64, json, os, sys, time, urllib.request

W = "/Volumes/Extreme/_edit_work/ro11/aiframes"
EXPECT = {"C-start.png": "969fa7ab19451c6f146b2ea3008e59ec2c1ad110436c67eb3a01322269552c5b",
          "C-end.png": "0edd9b753853e9efe1c2066cd983516b210cc0d158a007b66f7f1088f66a29d0"}


def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def main():
    import hashlib
    tag = sys.argv[1]
    dur = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    model = sys.argv[3] if len(sys.argv) > 3 else "google/veo-3.1-fast"
    out = f"{W}/{tag}.mp4"
    assert not os.path.exists(out), f"{out} exists: pick a new tag, never overwrite a take"
    for f, h in EXPECT.items():          # only the frames Dan approved (decisions.json)
        assert hashlib.sha256(open(f"{W}/{f}", "rb").read()).hexdigest() == h, f
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
             if l.startswith("REPLICATE_API_TOKEN=")][0]
    pf = sys.argv[4] if len(sys.argv) > 4 else "motion_C.txt"
    prompt = open(f"{W}/{pf}").read().strip()
    nf = f"{W}/{pf[:-4]}.neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    body = json.dumps({"input": {"prompt": prompt, "image": b64(f"{W}/C-start.png"), "last_frame": b64(f"{W}/C-end.png"),
                                 "duration": dur, "resolution": "1080p", "aspect_ratio": "16:9",
                                 "generate_audio": False, **({"negative_prompt": neg} if neg else {})}}).encode()
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    p = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://api.replicate.com/v1/models/{model}/predictions", data=body, headers=H)))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(10)
        p = json.load(urllib.request.urlopen(urllib.request.Request(p["urls"]["get"], headers=H)))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded":
        urllib.request.urlretrieve(o, out)
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": model,
               "duration": dur, "prompt": prompt, "prompt_file": pf, "negative_prompt": neg, "start": "C-start.png", "end": "C-end.png", "when": time.strftime("%F %T")},
              open(f"{W}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), p.get("metrics"))


if __name__ == "__main__":
    main()
