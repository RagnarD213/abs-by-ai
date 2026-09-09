#!/usr/bin/env python3
"""rev5 burned captions -- word-timed from the FINAL MIXED audio, never estimated windows.

Style is the locked ad spec: MadMuscles-style Arial Bold ~64 px, white with a black
outline, centred, low third. Dan keeps captions in this ad even though the reference edit
has none (his call, 2026-08-23).

Placement has to cooperate with the graphics, which the reference edit never had to solve
because it carries no captions:

  * FULL-SCREEN CARD beats -> captions are SUPPRESSED. The card already carries its own
    headline; a caption on top is two competing texts saying different things.
  * PANEL beats (the left-hand bullet panels) -> captions shift RIGHT into the video
    column so they never sit on the panel.
  * LOWER-THIRD beats -> captions LIFT above the chip (per-event MarginV, field 8).

  python3 captions5.py            # transcribe if needed, write cap.ass, burn
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats as B

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
# whisper shells out to a bare `ffmpeg`, so the static build has to be on PATH
os.environ["PATH"] = os.path.dirname(FF) + os.pathsep + os.environ.get("PATH", "")
HERE = os.path.dirname(os.path.abspath(__file__))
VIN  = os.environ.get("VIN",  f"{HERE}/nocap_audio.mov")
VOUT = os.environ.get("VOUT", f"{HERE}/website_video_16x9.mp4")
TX   = f"{HERE}/final.whisper.json"

# Full-screen cards already carry a headline; a caption on top is two competing texts.
# full-frame cards carry their own words; a caption on top is two texts at once
SUPPRESS = [B.POOL, B.BEFORE, B.TODAY, B.TRIAL, B.PRICE, B.SOLVED, B.CTA]
# left-panel beats: captions shift RIGHT into Dan's column (the app screens ARE the demo)
PANELS   = [B.BEATS[n] for n in sorted(B.PANEL)]
LOWERS   = [B.BEATS[n] for n in sorted(B.OVERLAY)]
MV_BASE, MV_LIFT = 96, 300
ML_PANEL = 1000          # clear of the 980 px panel (MarginL shifts the centred cue into Dan's column)

# Whisper mishears measured on THIS roll. "gross science" for bro-science and
# "Sixpackabs" for "six-pack abs" both occur; the first 30 s is proofed by hand.
# Whisper mishears measured on THIS roll's word list.
# Whisper mishears measured on THIS roll's word list; the first 30 s is proofed by hand.
CORRECT = {r"\bCancer with two taps\b": "Cancel with two taps", r"\bcancer with\b": "cancel with",
           r"\bsix pack\b": "six-pack", r"\bsix-pack abs\b": "six-pack abs",
           r"\bapps by AI\b": "Abs by AI", r"\bABS by AI\b": "Abs by AI",
           r"\bcharged this\b": "charged just", r"\bworkout histories\b": "workout history"}

def transcribe():
    if os.path.exists(TX): return
    wav = f"{HERE}/_final.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", VIN, "-map", "0:a", "-ac", "1",
                    "-ar", "16000", "-c:a", "pcm_s16le", wav], check=True)
    import whisper
    m = whisper.load_model("small.en")
    json.dump(m.transcribe(wav, word_timestamps=True, language="en"), open(TX, "w"))

def overlaps(a, b, spans, slack=0.12):
    return any(not (b <= s - slack or a >= e + slack) for s, e in spans)

def clip_out(a, b, spans):
    """Largest sub-span of [a,b] outside every suppression window.

    Dropping a cue that merely TOUCHES a card's edge loses real words: "Listen, I've
    spent thousands" vanished because it ended 0.08 s inside a clip beat, and the next
    caption then opened mid-sentence on "of dollars on personal". Clipping keeps the
    words and still guarantees no caption is ever drawn over a card, which is what QC
    asserts."""
    segs = [(a, b)]
    for s, e in spans:
        nxt = []
        for x, y in segs:
            if y <= s or x >= e: nxt.append((x, y)); continue
            if x < s: nxt.append((x, min(y, s)))
            if y > e: nxt.append((max(x, e), y))
        segs = nxt
    segs = [(x, y) for x, y in segs if y - x >= 0.25]
    return max(segs, key=lambda p: p[1] - p[0]) if segs else None

def build():
    # SOURCE OF WORDS: the tight cut's own word list, not a fresh pass on the mix.
    # Measured on this ad: a small.en pass over the finished mix agrees with the tight
    # list to +22 ms median (no systematic offset -- the audio stage does no retiming,
    # it is a -c:v copy mux), but it DROPS PUNCTUATION and mishears ("personal trainer"
    # for "trainers", "gonna" for "going to"). Punctuation is exactly what tells the
    # chunker where a sentence ends, so captioning off the mix pass split cues straight
    # across sentence boundaries ("...personal trainer AI has"). The final-mix pass stays
    # as QC (qc3.py check 5), which is what it is actually good for.
    tc = json.load(open(f"{HERE}/tight_cuts.json"))
    raw = [{"word": w["w"], "start": w["t"], "end": w["e"]} for w in tc["words"]]
    ws = []
    for w in raw:                       # merge punctuation-leading tokens
        t = w["word"]
        if ws and re.match(r"^\s*[.,!?%]", t):
            ws[-1]["word"] = ws[-1]["word"].rstrip() + t.strip(); ws[-1]["end"] = w["end"]
        else:
            ws.append({"word": t, "start": w["start"], "end": w["end"]})

    chunks, cur = [], []
    def flush():
        nonlocal cur
        if cur: chunks.append(cur); cur = []
    for w in ws:
        if cur and (w["start"] - cur[-1]["end"] > 0.65 or len(cur) >= 6): flush()
        cur.append(w)
        t = w["word"].strip()
        # a sentence end ALWAYS breaks the cue -- never carry the next sentence's first
        # words into the same caption
        if re.search(r"[.?!…]$", t) or (t.endswith(",") and len(cur) >= 2): flush()
    flush()

    def t2ass(t):
        h, m = int(t // 3600), int(t % 3600 // 60)
        s, cs = int(t % 60), min(99, round(t % 1 * 100))
        return "%d:%02d:%02d.%02d" % (h, m, s, cs)

    events, dropped = [], 0
    for i, c in enumerate(chunks):
        a = c[0]["start"]
        b = c[-1]["end"] + 0.15
        if i + 1 < len(chunks): b = min(b, chunks[i + 1][0]["start"])
        if b - a < 0.3: b = a + 0.3
        sub = clip_out(a, b, SUPPRESS)
        if sub is None: dropped += 1; continue
        a, b = sub
        txt = " ".join(w["word"].strip() for w in c)
        txt = re.sub(r"\s+([.,!?%])", r"\1", txt)
        txt = re.sub(r"\s{2,}", " ", txt).strip()
        for k, v in CORRECT.items():
            txt = re.sub(k, v, txt, flags=re.I)
        txt = re.sub(r"\babs\b", "abs", txt, flags=re.I)   # Dan: "abs" is ALWAYS lowercase
        txt = re.sub(r"\bai\b", "AI", txt, flags=re.I)
        txt = re.sub(r"\babs by AI\b", "Abs by AI", txt)     # ...except inside the brand name
        ml = ML_PANEL if overlaps(a, b, PANELS) else 0
        mv = MV_LIFT if overlaps(a, b, LOWERS) else 0
        events.append(f"Dialogue: 0,{t2ass(a)},{t2ass(b)},Cap,,{ml},0,{mv},,{txt}")

    style = ("Style: Cap,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,"
             f"100,100,0,0,1,4,2,2,120,120,{MV_BASE},1")
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n"
            "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, "
            "Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,"
            " Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
            " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"{style}\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL,"
            " MarginR, MarginV, Effect, Text\n")
    open(f"{HERE}/cap.ass", "w").write(head + "\n".join(events) + "\n")
    print(f"{len(events)} cues written, {dropped} suppressed over full-screen cards")

def burn():
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", VIN,
                    "-vf", f"ass={HERE}/cap.ass", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", VOUT],
                   check=True)
    print(VOUT, "done")

if __name__ == "__main__":
    steps = sys.argv[1:] or ["build", "burn"]
    if "tx" in steps: transcribe()
    if "build" in steps: build()
    if "burn" in steps: burn()
