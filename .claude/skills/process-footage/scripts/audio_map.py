#!/usr/bin/env python3
"""Fast first map of what was filmed: extract each roll's audio and ask Gemini which video each stretch is.

    audio_map.py --shoot-dir "/Volumes/Extreme/11:13 dan rose fitness shoot - green screen" \
                 --out ~/process-footage/1113 [C1903 C1904 ...]   # default: every clip in the folder

Writes <out>/audio/<clip>.ogg (16 kHz mono Opus, about 10 MB an hour) and <out>/map.json:
{clip: {"segments": [{start, end, kind, title, first_words, complete_take, notes}], "summary", "_usage"}}.
Costs about $0.01 to $0.05 per hour of footage on Gemini Flash (logged in each entry's _usage); covered by
Dan's standing Gemini authorization. This map is a FIRST PASS: times are close, not frame-accurate. Confirm
it with `announcements.py` on the Whisper sidecars before registering queue jobs.
Why it exists (11/13 shoot): Whisper through the render queue ran slower than real time on 2 cores, so a
45-minute roll took over an hour; the Gemini audio pass mapped all 15 rolls in minutes.
"""
import argparse, base64, json, os, subprocess, sys, time, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
FF = os.environ.get("PF_FFMPEG") or os.path.join(ROOT, "Media/video_edit/bin/ffmpeg.real")
PROMPT = """This is the audio of one camera roll from a YouTube shoot. Dan Rose (fitness creator) reads scripts from a
teleprompter, usually announcing each one like "All right, this video is <title>" or "This ad is S01 ...", often with
a script code such as L01, S05, A15, B08 or C01. There may be retakes, crew chatter, teleprompter instructions,
reaction clips playing, and silence.
Return JSON only, one object: {"segments":[{"start":"MM:SS","end":"MM:SS","kind":"scripted video|ad|reaction|pickup|b-roll or silent|chatter/setup","title":"the video title and script code exactly as Dan announces it, or a short description","first_words":"first sentence of the best complete take","complete_take":true,"notes":"retakes, false starts, problems, anything an editor should know"}],"summary":"one sentence"}
Group all takes of the same video into one segment. Use times from the start of this audio file."""


def key():
    r = subprocess.run(["zsh", "-c", "grep '^GEMINI_API_KEY=' ~/.absbyai-secrets.env | cut -d= -f2- | tr -d '\"'"],
                       capture_output=True, text=True)
    k = r.stdout.strip()
    if not k:
        sys.exit("GEMINI_API_KEY not in ~/.absbyai-secrets.env (refresh it from Railway, see CLAUDE.md)")
    return k


def norm(p):
    if isinstance(p, list) and len(p) == 1 and isinstance(p[0], dict) and "segments" in p[0]:
        return p[0]
    return {"segments": p} if isinstance(p, list) else p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shoot-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=os.environ.get("CAT_MODEL", "gemini-3.8-flash"))
    ap.add_argument("clips", nargs="*")
    a = ap.parse_args()
    out = os.path.expanduser(a.out)
    os.makedirs(os.path.join(out, "audio"), exist_ok=True)
    clips = a.clips or sorted(os.path.splitext(f)[0] for f in os.listdir(a.shoot_dir)
                              if f.upper().endswith(".MP4") and not f.startswith("._"))
    mpath = os.path.join(out, "map.json")
    m = {k: norm(v) for k, v in json.load(open(mpath)).items()} if os.path.exists(mpath) else {}
    k = key()
    for c in clips:
        if c in m and m[c].get("segments"):
            print("have", c)
            continue
        ogg = os.path.join(out, "audio", c + ".ogg")
        if not os.path.exists(ogg):
            src = os.path.join(a.shoot_dir, c + ".MP4")
            subprocess.run(["nice", "-n", "10", FF, "-v", "error", "-y", "-i", src, "-vn", "-map", "0:a:0", "-ac", "1",
                            "-ar", "16000", "-c:a", "libopus", "-b:a", "24k", ogg], check=True)
        body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/ogg",
                                                         "data": base64.b64encode(open(ogg, "rb").read()).decode()}},
                                        {"text": PROMPT}]}],
                "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent?key={k}"
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
                r = json.load(urllib.request.urlopen(req, timeout=900))
                m[c] = norm(json.loads(r["candidates"][0]["content"]["parts"][0]["text"]))
                m[c]["_usage"] = r.get("usageMetadata")
                break
            except Exception as e:
                detail = getattr(e, "read", lambda: b"")().decode()[:300]
                print("retry", c, attempt, e, detail, flush=True)
                time.sleep(5)
        json.dump(m, open(mpath, "w"), indent=1)
        segs = m.get(c, {}).get("segments", [])
        print(f"== {c}: {m.get(c, {}).get('summary', 'NO RESULT')}")
        for s in segs:
            print(f"  {s.get('start')}-{s.get('end')} {s.get('kind')} | {s.get('title')} | complete={s.get('complete_take')}")


if __name__ == "__main__":
    main()
