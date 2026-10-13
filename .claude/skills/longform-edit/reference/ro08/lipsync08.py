"""RO-08 round 2: sync an AI character's lips to Dan's own impression (no new voice), sync/lipsync-2-pro on Replicate ($0.08325 a second).
From the RO-06 round 4 / RO-20 scripts, with two additions: only a WINDOW round the face is sent (cropped, optionally turned upright and
enlarged) and it is laid back over the untouched take through a feathered mask, so nothing outside the face changes (the mask is trimmed to the synced frames: round 2 first left the last synced face pasted on the floor after the man had rolled away); and a segment of the
slot can be synced alone (a cheap test on a new face, or a stretch where the face is visible).
usage: lipsync08.py <plan id> <take.mp4> <take offset s> <tag>
env:  CROP=x:y:w:h (window in take pixels, even numbers; required)   ROT=cw|ccw|0 (turn the window so the face is upright before sending)
      LIPUP=2 (enlarge the window)   SEG=a:d (sync d seconds starting a seconds into the slot)   TEMP=0.5   ACTIVE=1   FEATHER=24
Writes round2/motion/<tag>.mp4 (silent, slot length, 24 fps: the take with the synced face laid in), <tag>.sync-raw.mp4 (what the model
returned: an upright face, the file lipmeasure20.py reads), <tag>.wav (the audio it was synced to) and <tag>.json (cost)."""
import base64, json, os, subprocess, sys, time, urllib.request, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_motion08 as GM
from PIL import Image, ImageFilter
W = GM.W; M = GM.M; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
VOICE = f"{W}/voice/film_voice.untreated.wav"          # the film's untreated voice, output frame 0 = film 0 (the track the build's chain reads)
MODEL = "sync/lipsync-2-pro"; USD_S = 0.08325
def fr(t): return int(round(t*FPS))
def uri(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
def run(c): subprocess.run(c, check=True)
ENC = ["-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
if __name__ == "__main__":
    cid, take, off, tag = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out) and not os.path.exists(f"{M}/{tag}.json"), f"{tag} exists: pick a new tag"
    x, y, cw, ch = map(int, os.environ["CROP"].split(":")); rot = os.environ.get("ROT", "0"); up = int(os.environ.get("LIPUP", "1")); fe = int(os.environ.get("FEATHER", "24"))
    it = next(r for r in json.load(open(f"{W}/plan_resolved.json")) if r["id"] == cid)
    f0, f1 = fr(it["t0"]), fr(it["t1"]); n24 = -(-(f1-f0)*24*1001//30000)                      # whole 24 fps frames covering the slot
    k0, nseg = 0, n24
    if os.environ.get("SEG"): sa, sd = (float(v) for v in os.environ["SEG"].split(":")); k0 = int(round(sa*24)); nseg = min(int(round(sd*24)), n24 - k0)
    dur = nseg/24.0; trim = f"{M}/{tag}.trim.mp4"; send = f"{M}/{tag}.send.mp4"; wav = f"{M}/{tag}.wav"; raw = f"{M}/{tag}.sync-raw.mp4"
    run([FF, "-v", "error", "-y", "-ss", f"{off:.4f}", "-i", take, "-frames:v", str(n24), "-vf", "format=yuv420p"] + ENC + [trim])
    fwd = {"cw": "transpose=1,", "ccw": "transpose=2,", "0": ""}[rot]; back = {"cw": "transpose=2,", "ccw": "transpose=1,", "0": ""}[rot]
    run([FF, "-v", "error", "-y", "-i", trim, "-vf", f"select='between(n,{k0},{k0+nseg-1})',setpts=N/24/TB,crop={cw}:{ch}:{x}:{y},{fwd}scale=iw*{up}:ih*{up}:flags=lanczos,format=yuv420p", "-r", "24"] + ENC + [send])
    w = wave.open(VOICE); sr = w.getframerate(); w.setpos(int(round((f0/FPS + k0/24.0)*sr))); pcm = w.readframes(int(round(dur*sr))); w.close()
    o = wave.open(wav, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(pcm); o.close()
    assert GM.spent() + dur*USD_S <= GM.CAP, "this sync would pass the cap Dan set"
    H = {"Authorization": "Bearer " + GM.token(), "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"video": uri(send, "video/mp4"), "audio": uri(wav, "audio/wav"), "sync_mode": "cut_off", "temperature": float(os.environ.get("TEMP", "0.5")),
                                 "active_speaker": os.environ.get("ACTIVE", "1") == "1"}}).encode()
    print(tag, "window", cw, ch, "rot", rot, "x", up, "| frames", k0, "to", k0+nseg, "of", n24, "|", round(dur, 3), "s", flush=True)
    p = GM.call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print(tag, "submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = GM.call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    usd = round(dur*USD_S, 3) if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "take": take, "offset": off, "seconds": dur, "usd": usd,
               "crop": [x, y, cw, ch], "rot": rot, "up": up, "seg_frames": [k0, k0+nseg], "audio": [round(f0/FPS + k0/24.0, 4), round(f0/FPS + k0/24.0 + dur, 4)], "voice": VOICE,
               "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    if p["status"] == "succeeded":
        urllib.request.urlretrieve(o, raw)
        m = Image.new("L", (cw, ch), 0); m.paste(255, (fe, fe, cw-fe, ch-fe)); m = m.filter(ImageFilter.GaussianBlur(fe/2)); mp = f"{M}/{tag}.mask.png"; m.save(mp)
        fc = (f"[1:v]fps=24,{back}scale={cw}:{ch}:flags=lanczos,format=yuv420p,setpts=PTS+{k0}/24/TB[f0];[2:v]format=gray,scale={cw}:{ch},trim=end_frame={nseg},setpts=PTS+{k0}/24/TB[mk];[f0][mk]alphamerge=shortest=1[f];"
              f"[0:v][f]overlay={x}:{y}:eof_action=pass:format=yuv420,format=yuv420p[v]")
        run([FF, "-v", "error", "-y", "-i", trim, "-i", raw, "-loop", "1", "-i", mp, "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n24), "-r", "24"] + ENC + [out])
    print(tag, p["status"], p.get("error"), p.get("metrics"), "| spent so far: $", GM.spent(), flush=True)
