"""Convert local Whisper word-timestamp JSON -> ElevenLabs Scribe response shape.

video-use's transcribe_one() returns early when edit/transcripts/<stem>.json exists,
so writing this file means Scribe is never called. Schema consumed by
helpers/pack_transcripts.py: data["words"] = [{text,start,end,type,speaker_id}]
with type in {word, spacing, audio_event}.
"""
import json, sys

def convert(wpath, out, speaker="speaker_0"):
    r = json.load(open(wpath))
    words, prev_end = [], None
    for seg in r["segments"]:
        for w in seg.get("words", []):
            t = w["word"]
            s, e = float(w["start"]), float(w["end"])
            # emit an explicit spacing token for the gap, mirroring Scribe
            if prev_end is not None and s > prev_end:
                words.append({"text": " ", "start": prev_end, "end": s,
                              "type": "spacing", "speaker_id": speaker})
            words.append({"text": t.strip(), "start": s, "end": e,
                          "type": "word", "speaker_id": speaker,
                          "logprob": w.get("probability")})
            prev_end = e
    payload = {
        "language_code": r.get("language", "en"),
        "language_probability": 1.0,
        "text": r.get("text", "").strip(),
        "words": words,
    }
    json.dump(payload, open(out, "w"), indent=2)
    nw = sum(1 for w in words if w["type"] == "word")
    print(f"wrote {out}: {nw} words, {len(words)-nw} spacing, span "
          f"{words[0]['start']:.2f}-{words[-1]['end']:.2f}s")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
