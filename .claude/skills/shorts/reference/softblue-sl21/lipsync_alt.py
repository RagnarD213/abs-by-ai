"""SL-21 round 2: the same slot trim + voice slice through another lip sync model, for when sync/lipsync-2-pro barely opens the mouth.
usage: lipsync_alt.py kling|latent TAG_IN TAG_OUT     (reads round2/lipsync/<TAG_IN>.trim.mp4 + .wav, writes <TAG_OUT>.mp4 + .json)"""
import base64, json, os, subprocess, sys, time, urllib.request
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OUT = "/Users/danielrose/Projects/_edit_work/SL-21/round2/lipsync"
which, tin, tout = sys.argv[1:4]
MODEL = {"kling": "kwaivgi/kling-lip-sync", "latent": "bytedance/latentsync"}[which]
def uri(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
def call(req):
    for k in range(6):
        try: return json.loads(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.read()[:400]); raise
        except Exception as e:
            if k == 5: raise
            print("retry", e, flush=True); time.sleep(10)
trim, wav = f"{OUT}/{tin}.trim.mp4", f"{OUT}/{tin}.wav"; out = f"{OUT}/{tout}.mp4"; assert not os.path.exists(out)
small = f"{OUT}/{tout}.in.mp4"      # a lighter upload: same frames, crf 16
subprocess.run([FF, "-v", "error", "-y", "-i", trim, "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-an", small], check=True)
tok = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
H = {"Authorization": "Bearer " + tok, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
inp = ({"video_url": uri(small, "video/mp4"), "audio_file": uri(wav, "audio/wav")} if which == "kling"
       else {"video": uri(small, "video/mp4"), "audio": uri(wav, "audio/wav"), "guidance_scale": 1.5, "seed": 7})
if which == "latent":      # a community model: predictions go to /v1/predictions with its version id
    ver = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}", headers=H))["latest_version"]["id"]
    p = call(urllib.request.Request("https://api.replicate.com/v1/predictions", data=json.dumps({"version": ver, "input": inp}).encode(), headers=H))
else:
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=json.dumps({"input": inp}).encode(), headers=H))
print("submitted", p["id"], flush=True)
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
if p["status"] == "succeeded":
    o = p["output"]; o = o[0] if isinstance(o, list) else o
    raw = f"{OUT}/{tout}.raw.mp4"; urllib.request.urlretrieve(o, raw)
    subprocess.run([FF, "-v", "error", "-y", "-i", raw, "-an", "-c:v", "copy", out], check=True)
json.dump(dict(id=p["id"], status=p["status"], error=p.get("error"), model=MODEL, metrics=p.get("metrics"), when=time.strftime("%F %T")), open(f"{OUT}/{tout}.json", "w"), indent=1)
print(tout, p["status"], p.get("error"), p.get("metrics"))
