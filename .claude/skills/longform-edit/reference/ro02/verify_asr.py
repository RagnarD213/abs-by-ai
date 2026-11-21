"""Re-transcribe short lav windows alone (medium.en, word timestamps) to settle cut points. usage: verify_asr.py ROLL:t0:t1 ..."""
import sys, subprocess, whisper
W = "/Volumes/Extreme/_edit_work/ro02"; m = whisper.load_model("medium.en")
for spec in sys.argv[1:]:
    roll, a, b = spec.split(":"); a = float(a); b = float(b)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b-a), "-i", f"{W}/lav/{roll}.wav", f"{W}/_v.wav"], check=True)
    r = m.transcribe(f"{W}/_v.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
    print(spec, " ".join(f"{w['word'].strip()}[{w['start']+a:.2f}-{w['end']+a:.2f}]" for s in r["segments"] for w in s["words"]), flush=True)
