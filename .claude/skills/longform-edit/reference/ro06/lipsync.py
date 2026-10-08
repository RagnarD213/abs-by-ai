"""RO-06 round 4: sync the client's lips to Dan's own impression (no new voice). Trims a Veo take to its slot at native
frame rate (never slowed or held), cuts the slot's audio from the first minute's untreated voice track on the same output
frames the build uses, and runs sync/lipsync-2-pro on Replicate with active_speaker on.
usage: lipsync.py <A1|A2> <take.mp4> <offset s> <tag> [temperature=0.5] [x:y:w:h face crop: sync only that window, composite back]
Writes round4/motion/<tag>.mp4 (silent picture, slot length) + <tag>.json; appends the cost to ledger.json."""
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_motion as GM
W = GM.W; M = GM.M; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
VOICE = f"{W}/round3/first-minute/DRAFT - RO-06 round 3 - first minute.mp4.untreated.wav"       # md5 fbf7798364cf1f0592144e03827a3b8a
MODEL = "sync/lipsync-2-pro"; USD_S = 0.08325
def fr(t): return int(round(t*FPS))
def uri(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
if __name__ == "__main__":
    cid, take, off, tag = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    temp = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5; crop = sys.argv[6] if len(sys.argv) > 6 else None
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    it = next(r for r in json.load(open(f"{W}/plan_resolved.json")) if r["id"] == cid)
    f0, f1 = fr(it["t0"]), fr(it["t1"]); n24 = -(-(f1-f0)*24*1001//30000); dur = n24/24.0       # whole 24 fps frames covering the slot
    trim = f"{M}/{tag}.trim.mp4"; wav = f"{M}/{tag}.wav"
    vf = "format=yuv420p" if not crop else "crop={2}:{3}:{0}:{1},format=yuv420p".format(*crop.split(":"))
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{off:.4f}", "-i", take, "-frames:v", str(n24), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", trim], check=True)
    w = wave.open(VOICE); sr = w.getframerate(); w.setpos(int(round(f0/FPS*sr))); pcm = w.readframes(int(round(dur*sr))); w.close()
    o = wave.open(wav, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(pcm); o.close()
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"video": uri(trim, "video/mp4"), "audio": uri(wav, "audio/wav"), "sync_mode": "cut_off", "temperature": temp, "active_speaker": True}}).encode()
    print("trim", n24, "frames", round(dur, 3), "s;", round(os.path.getsize(trim)/1e6, 1), "MB", flush=True)
    p = GM.call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = GM.call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    usd = round(dur*USD_S, 3) if p["status"] == "succeeded" else 0.0
    if p["status"] == "succeeded":
        raw = f"{M}/{tag}.sync-raw.mp4"; urllib.request.urlretrieve(o, raw)
        if crop:                                                 # composite the synced face window back over the untouched take
            x, y, cw, ch = crop.split(":")
            subprocess.run([FF, "-v", "error", "-y", "-ss", f"{off:.4f}", "-i", take, "-i", raw, "-filter_complex", f"[1:v]scale={cw}:{ch}[f];[0:v][f]overlay={x}:{y}:shortest=1,format=yuv420p",
                            "-frames:v", str(n24), "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], check=True)
        else: subprocess.run([FF, "-v", "error", "-y", "-i", raw, "-an", "-c:v", "copy", out], check=True)
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "take": take, "offset": off, "seconds": dur, "usd": usd,
               "temperature": temp, "crop": crop, "audio": [round(f0/FPS, 4), round(f0/FPS+dur, 4)], "voice": VOICE, "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), p.get("metrics"), "| spent so far: $", GM.ledger(dict(tag=tag, what=f"{MODEL} {dur:.2f}s", usd=usd, id=p["id"], status=p["status"])))
