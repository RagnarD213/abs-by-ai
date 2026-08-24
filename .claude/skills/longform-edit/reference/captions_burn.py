#!/usr/bin/env python3
"""Burned captions, word-timed from the FINAL VOICE, never from estimated windows.

Burned in, not an .srt sidecar. The skill's "SRT, not burned in" rule was decided for
the meal-prep split-screen tutorial, where captions fought the app UI in the left 570 px;
it is not a rule about talking-head content, and this video ships both.

Placement cooperates with the graphics:
  * FULL-SCREEN CARDS (title, endcard) -> captions SUPPRESSED. The card carries its own
    headline; a caption on top is two texts saying different things.
  * everything else keeps captions, including over B-roll -- the viewer still needs the
    words, and the reference edit's captions run over its stock too.
MarginV is set so the caption band sits BELOW the inset window (which ends at y=933) and
below the section-label band (796-884), and clear of the corner watermark.
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spec

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
os.environ["PATH"] = os.path.dirname(FF) + os.pathsep + os.environ.get("PATH", "")
VOICE = "audio/voice_tight.wav"
TX    = "final.whisper.json"
MV    = 62

SUPPRESS = [(a, a + d) for a, d, k, _, _ in spec.G if k in ("title", "endcard")]

# Whisper mishears in this transcript, checked against what Dan actually says
CORRECT = {r"\bab wheel\b": "ab wheel", r"\bAbwheel\b": "ab wheel",
           r"\bab\s*-\s*wheel\b": "ab wheel",
           r"\brectus abdominis\b": "rectus abdominis",
           r"\btransverse abdominis\b": "transverse abdominis",
           r"absbyai\s*\.\s*com": "AbsByAI.com", r"\babs by ai\b": "AbsByAI",
           r"\bsix pack\b": "six-pack",
           # re-transcription errors, found by diffing the final audio against the
           # source rolls (99.26% word overlap -- these two are the only real misses)
           r"\bscammed\b": "scams",
           r"\bgo a little bit further\b": "go a little bit farther"}

def transcribe():
    if os.path.exists(TX): return
    wav = "_cap16k.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", VOICE, "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", wav], check=True)
    import whisper
    m = whisper.load_model("small.en")
    json.dump(m.transcribe(wav, word_timestamps=True, language="en"), open(TX, "w"))

def overlaps(a, b, spans, slack=0.10):
    return any(not (b <= s - slack or a >= e + slack) for s, e in spans)

def build():
    raw = [w for s in json.load(open(TX))["segments"] for w in s.get("words", [])]
    ws = []
    for w in raw:
        t = w["word"]
        if ws and re.match(r"^\s*[.,!?%]", t):
            ws[-1]["word"] = ws[-1]["word"].rstrip() + t.strip(); ws[-1]["end"] = w["end"]
        else:
            ws.append({"word": t, "start": w["start"], "end": w["end"]})
    # Chunk on PHRASE boundaries, not on a word count. A fixed 5-word cap produced
    # "I'll show you why you" / "need to be buying an", which is two broken phrases.
    # Break on sentence punctuation, on a real pause, or when the line would get too
    # long to read at this size -- whichever comes first.
    MAXCH, PAUSE = 40, 0.26
    chunks, cur = [], []
    def flush():
        nonlocal cur
        if cur: chunks.append(cur); cur = []
    def width(c, extra=""):
        return len(" ".join(w["word"].strip() for w in c) + (" " + extra if extra else ""))
    for w in ws:
        t = w["word"].strip()
        if cur and (w["start"] - cur[-1]["end"] >= PAUSE or width(cur, t) > MAXCH):
            flush()
        cur.append(w)
        if re.search(r"[.?!…]$", t): flush()
        elif t.endswith(",") and width(cur) >= 22: flush()
    flush()
    # An orphan -- one short word left alone, usually because the chunk before it was
    # suppressed over a full-screen card -- reads as a mistake. Fold it into a neighbour.
    merged = []
    for c in chunks:
        txt = " ".join(w["word"].strip() for w in c)
        if merged and len(c) <= 2 and len(txt) <= 6 and \
           c[0]["start"] - merged[-1][-1]["end"] < 0.5 and width(merged[-1], txt) <= MAXCH + 8:
            merged[-1].extend(c)
        else:
            merged.append(list(c))
    chunks = merged
    def t2ass(t):
        h, m = int(t // 3600), int(t % 3600 // 60)
        s, cs = int(t % 60), min(99, round(t % 1 * 100))
        return "%d:%02d:%02d.%02d" % (h, m, s, cs)
    events, dropped, last_dropped = [], 0, False
    for i, c in enumerate(chunks):
        a = c[0]["start"]; b = c[-1]["end"] + 0.15
        if i + 1 < len(chunks): b = min(b, chunks[i + 1][0]["start"])
        if b - a < 0.3: b = a + 0.3
        if overlaps(a, b, SUPPRESS): dropped += 1; last_dropped = True; continue
        txt = " ".join(w["word"].strip() for w in c)
        # A mid-sentence fragment arriving straight out of a full-screen card reads as
        # a mistake -- the viewer saw "...and I'll", then the card, then "to be using
        # it." Drop the tail rather than show half a sentence.
        if last_dropped and txt[:1].islower():
            dropped += 1; continue
        last_dropped = False
        txt = re.sub(r"\s+([.,!?%])", r"\1", txt)
        for k, v in CORRECT.items(): txt = re.sub(k, v, txt, flags=re.I)
        txt = re.sub(r"\babs\b", "abs", txt, flags=re.I)     # Dan: always lowercase
        txt = re.sub(r"\s{2,}", " ", txt).strip()
        events.append(f"Dialogue: 0,{t2ass(a)},{t2ass(b)},Cap,,0,0,{MV},,{txt}")
    style = ("Style: Cap,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,"
             f"100,100,0,0,1,4,2,2,180,180,{MV},1")
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n"
            "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, "
            "Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,"
            " Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
            " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"{style}\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL,"
            " MarginR, MarginV, Effect, Text\n")
    open("cap.ass", "w").write(head + "\n".join(events) + "\n")
    longest = max(len(e.split(",,")[-1]) for e in events)
    print(f"{len(events)} cues, {dropped} suppressed over full-screen cards, "
          f"longest line {longest} chars")
    # an .srt is shipped as well, for the YouTube upload
    with open("captions.srt", "w") as f:
        n = 0
        for i, c in enumerate(chunks):
            a = c[0]["start"]; b = c[-1]["end"] + 0.15
            if i + 1 < len(chunks): b = min(b, chunks[i + 1][0]["start"])
            if b - a < 0.3: b = a + 0.3
            txt = " ".join(w["word"].strip() for w in c)
            txt = re.sub(r"\s+([.,!?%])", r"\1", txt)
            for k, v in CORRECT.items(): txt = re.sub(k, v, txt, flags=re.I)
            n += 1
            def srt(t): return "%02d:%02d:%02d,%03d" % (t//3600, t%3600//60, t%60, round(t%1*1000))
            f.write(f"{n}\n{srt(a)} --> {srt(b)}\n{txt}\n\n")
    print(f"captions.srt: {n} cues")

if __name__ == "__main__":
    steps = sys.argv[1:] or ["tx", "build"]
    if "tx" in steps: transcribe()
    if "build" in steps: build()
