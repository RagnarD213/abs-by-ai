"""RO-20C round 6: sync an excuse-voice character's lips to Dan's own recording of the line (no new voice), the lipsync20.py
method (sync/lipsync-2-pro on Replicate, active_speaker on, temperature 0.5) with the audio cut from the round 4 master's
untreated voice twin on the video's own timeline.
usage: lipsync_r6.py TAKE.mp4 TAKE_OFFSET_S VIDEO_T0 VIDEO_T1 TAG
Writes round6/lipsync/<TAG>.mp4 (silent picture, slot length at 24 fps) + <TAG>.json; appends the cost to round6/lipsync/ledger.json."""
import base64, json, os, subprocess, sys, time, urllib.request, wave
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VOICE = "/Volumes/Extreme/_edit_work/ro20/round4/v3/untreated.wav"     # master timeline, 48 kHz mono
OUT = "/Volumes/Extreme/_edit_work/ro20/round6/lipsync"
MODEL = "sync/lipsync-2-pro"; USD_S = 0.08325


def uri(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()


def call(req):
    for k in range(6):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception as e:
            if k == 5: raise
            print("retry", e, flush=True); time.sleep(10)


if __name__ == "__main__":
    take, off, t0, t1, tag = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    os.makedirs(OUT, exist_ok=True); out = f"{OUT}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    n24 = int(round((t1 - t0) * 24)); dur = n24 / 24.0
    trim, wav = f"{OUT}/{tag}.trim.mp4", f"{OUT}/{tag}.wav"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{off:.4f}", "-i", take, "-frames:v", str(n24), "-vf", "format=yuv420p", "-an", "-c:v", "libx264",
                    "-crf", "10", "-preset", "slow", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", trim], check=True)
    w = wave.open(VOICE); sr = w.getframerate(); w.setpos(int(round(t0 * sr))); pcm = w.readframes(int(round(dur * sr))); w.close()
    o = wave.open(wav, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(pcm); o.close()
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"video": uri(trim, "video/mp4"), "audio": uri(wav, "audio/wav"), "sync_mode": "cut_off", "temperature": 0.5,
                                 "active_speaker": True}}).encode()
    print(tag, "trim", n24, "frames", dur, "s", flush=True)
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    usd = round(dur * USD_S, 3) if p["status"] == "succeeded" else 0.0
    if p["status"] == "succeeded":
        o = p["output"]; o = o[0] if isinstance(o, list) else o
        raw = f"{OUT}/{tag}.sync-raw.mp4"; urllib.request.urlretrieve(o, raw)
        subprocess.run([FF, "-v", "error", "-y", "-i", raw, "-an", "-c:v", "copy", out], check=True)
    rec = dict(id=p["id"], status=p["status"], error=p.get("error"), model=MODEL, take=take, offset=off, video=[t0, t1], seconds=dur, usd=usd,
               voice=VOICE, when=time.strftime("%F %T"))
    json.dump(rec, open(f"{OUT}/{tag}.json", "w"), indent=1)
    lp = f"{OUT}/ledger.json"; L = json.load(open(lp)) if os.path.exists(lp) else []; L.append(dict(tag=tag, usd=usd, status=p["status"], id=p["id"]))
    json.dump(L, open(lp, "w"), indent=1)
    print(tag, p["status"], p.get("error"), "usd", usd, "| ledger total $", round(sum(x["usd"] for x in L), 3))
