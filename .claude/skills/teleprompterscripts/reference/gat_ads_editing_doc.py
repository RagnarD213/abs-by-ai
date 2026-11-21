#!/usr/bin/env python3
"""Build the Great Again T ads editing document (19 final ad scripts).

Spoken words and Dan's existing directions come straight from the source export.
New directions are inserted by anchor inside one named script.
"""
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src2" / "ads.md"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
TITLE = "Great Again T - Editing Document 3 - Ads"
EXPECT = "L01 L02 L03 L04 L05 L07 L17 L20 L22 L23 L30 S01 S02 S03 S04 S05 S11 S13 S21".split()


def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))


def clean(line):
    line = re.sub(r'(?<!\\)\[([^\]]+)\]\(https?://[^)]+\)', r'\1', line)
    line = line.replace("**", "")
    line = re.sub(r'\\(.)', r'\1', line)
    return line.strip()


def is_cue(t):
    return t.startswith("[") and t.endswith("]")


# ---------------------------------------------------------------- parse
raw_lines = SRC.read_text().split("\n")
doc, cur, in_final, skipping = [], None, False, True
scripts = {}
for raw in raw_lines:
    t = clean(raw)
    if not t:
        continue
    if raw.startswith("# "):
        cur, in_final, skipping = None, False, True
        name = t.lstrip("# ").strip()
        if name.startswith("LONG ADS"):
            doc.append({"kind": "h1", "text": "LONG ADS"})
        elif name.startswith("SHORT ADS"):
            doc.append({"kind": "h1", "text": "SHORT ADS (VERTICAL, 59 SECONDS OR LESS)"})
        continue
    if raw.startswith("## "):
        name = t.lstrip("# ").strip()
        in_final = False
        if "~~" in name or not re.match(r"[LS]\d\d\. ", name):
            cur, skipping = None, True
            continue
        cur = name[:3]
        skipping = False
        scripts[cur] = {"head": [], "body": [], "has_final": False, "title": name}
        continue
    if cur is None or skipping:
        continue
    s = scripts[cur]
    if raw.startswith("### "):
        name = t.lstrip("# ").strip()
        if name == "Final script":
            s["has_final"] = in_final = True
        elif in_final:
            s["body"].append({"kind": "h3", "text": name})
        continue
    if not in_final:
        if t.startswith("On camera:"):
            s["head"].append({"kind": "ref", "text": t})
        elif t.startswith("AD SETUP:"):
            s["head"].append({"kind": "setup", "text": t})
        continue
    s["body"].append({"kind": "cue" if is_cue(t) else "spoken", "text": t})

final = [k for k, v in scripts.items() if v["has_final"]]
assert final == EXPECT, final
spoken_before = {k: [p["text"] for p in scripts[k]["body"] if p["kind"] == "spoken"] for k in final}
cues_before = sum(1 for k in final for p in scripts[k]["body"] if p["kind"] == "cue")

# ---------------------------------------------------------------- pending suggestions in L17 (directions only)
# At 22:23:57Z the doc gained tracked suggestions that add clip sources to L17's clips direction and move the wipe
# after the presenter's last line. They touch no spoken word of Dan's. Built as if accepted; the inserted wording is
# read from the .docx export's <w:ins> runs, never retyped.
DOCX_XML = HERE.parent / "src4" / "doc.xml"
if DOCX_XML.exists():
    x = DOCX_XML.read_text()
    ins = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", s))
           for s in re.findall(r"<w:ins [^>]*>(.*?)</w:ins>", x, flags=re.S)]
    ins = [html.unescape(s) for s in ins]
    src_ins = next(s for s in ins if s.startswith("SOURCES, BOTH ON THE SIXPACKABS.COM YOUTUBE CHANNEL"))
    wipe_ins = next(s for s in ins if s.startswith("[SHE TURNS AND GESTURES OFF SCREEN.") and s.endswith("STOOD]"))
    b = scripts["L17"]["body"]
    i = next(i for i, p in enumerate(b) if p["kind"] == "cue" and p["text"].startswith("[SHE TURNS AND GESTURES OFF SCREEN."))
    keep = "SHOW CLIP OF DAN ALONE, THEN TWO CLIPS OF DAN INTERACTING WITH 40+ SIXPACKABS.COM TALENT. "
    assert keep in b[i]["text"]
    b[i] = {"kind": "cue", "text": "[" + keep + src_ins}
    assert is_cue(b[i]["text"])
    j = next(j for j, p in enumerate(b) if p["kind"] == "spoken" and p["text"].startswith("Now, you’re going to hear directly"))
    b.insert(j + 1, {"kind": "cue", "text": wipe_ins})
    cues_before += 1

# ---------------------------------------------------------------- new directions
OPS = [
    ("L01", "after", "So let's start with what's probably already happening to you.",
     '[B-ROLL OVER THE NEXT THREE PARAGRAPHS WHILE DAN KEEPS TALKING: A MAN OVER 40 WITH A GROWING BELLY, WIPED OUT IN THE AFTERNOON, TOO TIRED AT THE END OF THE DAY. USE THE SAME CLIPS AS THIS SECTION OF THE VSL. BACK TO DAN FOR "AND HERE\'S WHAT MOST GUYS NEVER FIGURE OUT"]'),
    ("L17", "before", "Wait, wait, wait. Stop. Stop the tape.",
     '[FROM HERE TO THE WIPE, THE VOICE IS THE AI PRESENTER, NOT DAN. HER LINES ARE NOT IN DAN\'S TELEPROMPTER SCRIPT AND HE DOES NOT FILM THEM]'),
    ("L17", "after", "WIPE TO DAN ON GREEN SCREEN, IN THE SAME STUDIO BACKGROUND, STANDING WHERE SHE STOOD",
     '[EVERYTHING ABOVE THIS POINT IS THE PRESENTER\'S VOICE. EVERYTHING BELOW IS DAN ON CAMERA]'),
    ("L22", "after", "So let's run that morning one more time.",
     '[THE REPLAY IS A NEW AI CLIP SET, NOT THE FIRST SCENE REVERSED OR RECUT. SAME MAN, SAME KITCHEN, SAME CAMERA ANGLES, SO THE ONLY THING THAT CHANGES IS THE BREAKFAST AND HOW HE LOOKS]'),
]
added = 0
for sid, mode, anchor, text in OPS:
    body = scripts[sid]["body"]
    hits = [i for i, p in enumerate(body) if p["kind"] in ("spoken", "cue") and not p.get("new")
            and norm(anchor) in norm(p["text"])]
    if len(hits) != 1:
        sys.exit(f"{sid}: anchor matched {len(hits)}: {anchor!r}")
    assert is_cue(text) and "—" not in text
    new = {"kind": "cue", "text": text, "new": True}
    body.insert(hits[0] + (1 if mode == "after" else 0), new)
    added += 1

# every short with an alternate hook: say what to deliver
alt = 0
for sid in final:
    body = scripts[sid]["body"]
    for i, p in enumerate(body):
        if p["kind"] == "cue" and p["text"].startswith("[ALTERNATE HOOK"):
            body.insert(i + 1, {"kind": "cue", "new": True, "text":
                "[DELIVER THIS AD AS TWO VERSIONS: A OPENS ON THE SCRIPTED HOOK, B OPENS ON THE ALTERNATE HOOK. EVERYTHING AFTER THE HOOK IS IDENTICAL]"})
            alt += 1
            break
assert alt == 7, alt
for k in final:
    assert [p["text"] for p in scripts[k]["body"] if p["kind"] == "spoken"] == spoken_before[k]

# ---------------------------------------------------------------- assemble
seq = []
h1_iter = iter([d for d in doc if d["kind"] == "h1"])
long_h1, short_h1 = next(h1_iter), next(h1_iter)
seq.append(long_h1)
for k in final:
    if k == "S01":
        seq.append(short_h1)
    s = scripts[k]
    seq.append({"kind": "h2", "text": s["title"]})
    seq += s["head"] + s["body"]

MATH = re.compile(r"\$(?=\S)[^$]*(?<=\S)\$")
for p in seq:
    if MATH.search(p["text"]):
        print("MATH-RISK", p["kind"], p["text"][:140])
        assert p["kind"] not in ("cue", "ref", "setup")


def li(items):
    return "<ul>" + "".join(f"<li>{html.escape(x, quote=False)}</li>" for x in items) + "</ul>"


INTRO = (
    "<p><b>For the AI editors.</b> These are the 19 finished Great Again T ad scripts, word for word as Dan films them "
    "from the teleprompter, with the directions for what is on screen. They are ads: each one runs as an unlisted "
    "YouTube upload behind Google Ads and is never posted organically.</p>"
    "<p><b>How to read it</b></p>"
    + li([
        "Regular text is what is said on camera. Do not change, trim or reorder it.",
        "[BOLD CAPS IN BRACKETS] is a direction: what is on screen, or what Dan is doing. Most were written with the script. A direction placed before a line sets up that line; one placed after a line belongs to the line just above it.",
        "The italic line under each title says who is on camera and the length to hit. The bold AD SETUP line says where the ad sends the viewer and which button wording goes on screen.",
        "Text in quotation marks inside a direction is the exact wording to put on screen.",
    ])
    + "<p><b>Rules that matter most on these ads</b></p>"
    + li([
        "Read .claude/skills/_shared/VIDEO-RULES.md in full before starting, and edit with /ad-edit. Graphics are Soft Blue Light with HyperFrames motion. Dan is on green screen in every ad: use the house key, and put the background the direction names behind him (kitchen, stove, plain dark, studio).",
        "The first two seconds decide each ad. Open on the hook line and its picture. No logo, title card or lead-in before Dan's first word.",
        "If the script does not name it, the screen does not show it. Several ads tease something they never reveal (the \"diet\" food, roots 2 and 3, the mineral, the other two foods, the meat and the oil in some ads). Covers stay on, names stay blurred, and no B-roll gives the answer away.",
        "The button on screen must match the AD SETUP line: \"WATCH NOW\" for ads that go to the video, \"TAKE QUIZ\" for the quiz ads, a plain arrow to the button for ads that go to the four questions. The quiz ads do not run until the quiz returns a plan; build them anyway.",
        "Where a direction says props are \"on a table, or added in the edit\": use the real props if Dan filmed them. Add food pictures in the edit only for what is missing.",
        "Study cards show the real abstract with the result line highlighted. Every number on screen must match the script exactly. Sources: Handoffs/great-again-t-20261105/contest2/CLAIMS-PACK.md, plus the three newer studies named in the ads (Derouiche 2013, Whittaker and Wu 2021, Hayes 2010).",
        "Dan's before photos and after photos never share a screen. Each is full screen on its own line.",
        "L17 and L22 open on AI-generated scenes. Dan sees each clip's START and END frame pair before any clip is generated. The AI people are never presented as real customers.",
        "Build these once and reuse them in every ad, the VSL and the upsells, identical each time: the lower third (\"DANIEL ROSE. FOUNDER, SIXPACKABS.COM. HELPED OVER 4.4 MILLION MEN\"), the channel clips with the counts circled, the before and after photo screens, the cortisol and testosterone seesaw, the \"1% EVERY YEAR\" line, the study card layout, the \"35% MORE LIKELY TO DIE\" abstract, the phone showing the first quiz question, and the three arrow-and-button end cards.",
        "Long ads: cut the 16:9 master first. The vertical, square and one-minute versions come from the approved master with /shortad-from-longform. Short ads are vertical from the start.",
        "Not in this document: L18 (the older spokesman ad) is still an outline with no spokesman hired, and S16, S23 and S29 were struck from the list.",
    ])
)

P = 'style="margin:0 0 10pt 0;color:#000000;font-weight:normal;font-style:normal"'
h = ['<html><head><meta charset="utf-8"></head><body style="font-family:Arial;font-size:11pt;color:#000000">',
     f"<h1>{html.escape(TITLE)}</h1>", INTRO]
for p in seq:
    t = html.escape(p["text"], quote=False)
    k = p["kind"]
    if k in ("h1", "h2", "h3"):
        h.append(f"<{k}>{t}</{k}>")
    elif k == "ref":
        h.append(f'<p style="margin:0 0 10pt 0;color:#000000"><i>{t}</i></p>')
    elif k in ("cue", "setup"):
        h.append(f'<p style="margin:0 0 10pt 0;color:#000000"><b>{t}</b></p>')
    else:
        h.append(f"<p {P}>{t}</p>")
h.append("</body></html>")
(OUT / f"{TITLE}.html").write_text("\n".join(h))
(OUT / f"{TITLE}.seq.json").write_text(json.dumps([p["text"] for p in seq], ensure_ascii=False, indent=1))

# teleprompter cross-check sequence (what Dan reads), for verifying the helper's document
tp = []
for k in final:
    s = scripts[k]
    tp.append(s["title"])
    body = s["body"]
    if k == "L17":
        i = next(i for i, p in enumerate(body) if p["kind"] == "h3" and p["text"] == "The quiz")
        body = body[i:]
    hook = None
    for p in body:
        if p["kind"] == "spoken":
            tp.append(p["text"])
        elif p["kind"] == "cue" and p["text"].startswith("[ALTERNATE HOOK"):
            hook = re.search(r"“(.+)”\]$", p["text"]).group(1)
    if hook:
        tp.append(hook)
(OUT / "ads.teleprompter.expected.json").write_text(json.dumps(tp, ensure_ascii=False, indent=1))

words = sum(len(x.split()) for x in tp)
print("scripts", len(final), "| spoken paragraphs", sum(len(v) for v in spoken_before.values()),
      "| existing directions", cues_before, "| added", added + alt,
      "| teleprompter lines", len(tp), "words", words)
print("em dashes in directions:", sum(p["text"].count("—") for p in seq if p["kind"] != "spoken"))
