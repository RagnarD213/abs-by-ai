"""Re-transcribe short lav windows alone (medium.en, word timestamps) to settle cut points. usage: verify_asr.py t0:t1 [t0:t1 ...]"""
import sys, subprocess, whisper
m = whisper.load_model("medium.en")
for spec in sys.argv[1:]:
    a, b = map(float, spec.split(":"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b-a), "-i", "/Volumes/Extreme/_edit_work/ro10/lav.wav", "/Volumes/Extreme/_edit_work/ro10/_v.wav"], check=True)
    r = m.transcribe("/Volumes/Extreme/_edit_work/ro10/_v.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
    print(spec, " ".join(f"{w['word'].strip()}[{w['start']+a:.2f}-{w['end']+a:.2f}]" for s in r["segments"] for w in s["words"]), flush=True)
