"""RO-37 prep: lav wav per roll (48 kHz mono, measured lav channel 0) and medium.en word timestamps (shared speech.transcribe, cached)."""
import sys, json, subprocess, os
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{P}/.claude/skills/_shared/cut")
import speech
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; FF = f"{P}/Media/video_edit/bin/ffmpeg"
RD = "/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content"
for r in ["C1893", "C1894", "C1895", "C1897"]:
    src = f"{RD}/{r}.MP4"
    if not os.path.exists(f"{W}/lav_{r}.wav"):
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", src, "-map", "0:a:0", "-af", "pan=mono|c0=c0", "-ar", "48000", "-c:a", "pcm_s16le", f"{W}/lav_{r}.wav"], check=True)
    words = speech.transcribe(src, model="medium.en", amap="0:a:0", af="pan=mono|c0=c0")[0]
    json.dump(words, open(f"{W}/words_{r}.json", "w"))
    print(r, len(words), "words", flush=True)
