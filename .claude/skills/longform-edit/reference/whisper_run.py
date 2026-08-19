#!/usr/bin/env python3
"""Local Whisper transcription with WORD timestamps. Free; replaces ElevenLabs Scribe.

  ffmpeg -i src.MP4 -vn -ac 1 -ar 16000 -c:a pcm_s16le out.wav
  python3 whisper_run.py out.wav out.whisper.json

ffmpeg MUST be on PATH -- whisper shells out to it. Export PATH *into* any
nohup/background invocation or it dies with FileNotFoundError: 'ffmpeg'.
5:45 of audio transcribed in 41s on an M2 Pro with model 'small'.
Chunk into ~5-minute pieces only if a machine OOMs (the V3/V6 CUDA fix); not
needed on Apple silicon CPU.
"""
import sys, json, time, whisper

def main():
    src, out = sys.argv[1], sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "small"
    t0 = time.time()
    m = whisper.load_model(model)
    r = m.transcribe(src, word_timestamps=True, language="en", verbose=False)
    json.dump(r, open(out, "w"))
    nw = sum(len(s.get("words", [])) for s in r["segments"])
    print("done %.0fs segments=%d words=%d" % (time.time()-t0, len(r["segments"]), nw))

if __name__ == "__main__":
    main()
