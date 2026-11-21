#!/usr/bin/env python3
"""Teleprompter documents and a Filming Document from a "Filming Scripts" Google Doc (first run 2026-11-12).

    python3 tp_from_filming_scripts_doc.py read_doc.json OUT_DIR "Next Green Screen Shoot" [--first TESLA] [--check-clips]

Source format (the Doc built by the next-shoot scripts job): Heading 1 per group, Heading 2 per script
("A15 · Title"), then an italic "Filming script. N spoken words, about ..." line, cue paragraphs that start
with [ and end with ], and spoken paragraphs. The source is only read.

Writes into OUT_DIR:
  "<prefix> - Teleprompter N - <group>.html"   words only, script titles as headings, no blank lines
  "<prefix> - Filming Document.html"           what to bring, reaction clips with links, then every script with cues
  built_seq.json                               every line of every document, for the download check
SETS below says which groups go in which teleprompter document.
"""
import html, json, os, re, sys, urllib.request, urllib.parse

SETS = [("Long Videos", ["Long videos"]),
        ("Shorts and Reaction Shorts", ["Shorts", "Reaction Shorts"]),
        ("Long Reactions", ["Long reactions"])]
P = 'style="color:#000000;font-weight:normal;font-style:normal"'
CUE = 'style="color:#1f5fd0;font-weight:bold"'


def load(path):
    d = json.load(open(path)); d = d.get("content", d)
    groups, g, s = [], None, None
    for el in d["tabs"][0]["documentTab"]["body"]["content"]:
        if "paragraph" not in el: continue
        runs = el["paragraph"]["elements"]
        if any((r.get("textRun") or {}).get("suggestedInsertionIds") or (r.get("textRun") or {}).get("suggestedDeletionIds") for r in runs):
            raise SystemExit("the source has pending suggestions: rule on them first")
        t = "".join((r.get("textRun") or {}).get("content", "") for r in runs).replace("\x0b", " ").strip()
        st = el["paragraph"]["paragraphStyle"].get("namedStyleType")
        if st == "HEADING_1":
            g = {"name": t, "scripts": []}; groups.append(g); s = None
        elif st == "HEADING_2" and g is not None:
            sid, _, title = t.partition(" · ")
            s = {"id": sid.strip(), "title": title.strip(), "paras": []}; g["scripts"].append(s)
        elif s is not None and t:
            kind = "head" if t.startswith("Filming script.") else "cue" if t.startswith("[") and t.endswith("]") else "spoken"
            if kind == "spoken" and "[" in t: raise SystemExit("bracket inside a spoken line in %s: %s" % (s["id"], t[:80]))
            s["paras"].append((kind, t))
    return [g for g in groups if g["scripts"]]


def words(s): return len([x for x in re.split(r"\s+", s) if re.search(r"[A-Za-z0-9]", x)])
def dollar_trap(t): return bool(re.search(r"\$\S[^$]*\S\$", t))
def esc(t): return html.escape(t, quote=False)
def page(title, body): return ('<html><head><meta charset="utf-8"><title>%s</title></head><body style="font-family:Arial;font-size:11pt">%s</body></html>' % (esc(title), "\n".join(body)))


def clips(script):
    out = []
    for kind, t in script["paras"]:
        if kind != "cue": continue
        for m in re.finditer(r"(?<![A-Za-z0-9_-])([A-Za-z0-9_-]{11}),\s*(\d+):(\d\d)", t):
            vid = m.group(1)
            if not (re.search(r"[a-z]", vid) and re.search(r"[A-Z0-9_-]", vid)): continue
            sec = int(m.group(2)) * 60 + int(m.group(3))
            label = t.strip("[]")
            label = re.sub(r"^(COLD )?OPEN ON THE CLIP[^:]*:\s*|^PLAY CLIP \d+[^:]*:\s*|^PLAY CLIP \d+, PLAYING[^:]*:\s*", "", label)
            out.append((vid, sec, label))
    return out


def main():
    src, out_dir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    groups = load(src); by = {g["name"]: g for g in groups}; seq = {}; report = []
    if "--first" in sys.argv:   # film this script first: moved to the top of its group (Dan, 2026-11-13: the Tesla video)
        want = sys.argv[sys.argv.index("--first") + 1]
        for g in groups:
            hit = [s for s in g["scripts"] if s["id"] == want]
            if hit: g["scripts"].remove(hit[0]); g["scripts"].insert(0, hit[0])
        assert any(g["scripts"][0]["id"] == want for g in groups), "no script " + want
    # teleprompter documents
    for n, (label, names) in enumerate(SETS, 1):
        name = "%s - Teleprompter %d - %s" % (prefix, n, label); body = []; lines = []; total = 0
        for gname in names:
            for s in by[gname]["scripts"]:
                head = "%s (%s)" % (s["title"], s["id"])
                body.append("<h2>%s</h2>" % esc(head)); lines.append(head)
                for kind, t in s["paras"]:
                    if kind == "spoken":
                        body.append("<p %s>%s</p>" % (P, esc(t))); lines.append(t); total += words(t)
        text = "\n".join(lines)
        assert "[" not in text and "]" not in text and "Filming script." not in text, name
        open(os.path.join(out_dir, name + ".html"), "w").write(page(name, body)); seq[name] = lines
        report.append((name, sum(len(by[g]["scripts"]) for g in names), total))
    # filming document
    name = "%s - Filming Document" % prefix; body = []; lines = []
    def add(tag, t, style=""):
        body.append("<%s%s>%s</%s>" % (tag, (" " + style) if style else "", t if tag in ("ul",) else esc(t), tag)); lines.append(t)
    add("h1", name)
    add("p", "Every script for this shoot with its filming and editing directions. Blue lines in [BRACKETED CAPS] are directions and are not read aloud. The teleprompter documents hold the same spoken words with the directions removed. All green screen. Change wording here, then the teleprompter documents get rebuilt from this.")
    add("h1", "What to bring")
    for g in groups:
        for s in g["scripts"]:
            for kind, t in s["paras"]:
                if kind == "cue" and "HOLDS UP" in t:
                    body.append("<ul><li>%s: <b>%s</b></li></ul>" % (esc(s["title"]), esc(t.strip("[]")))); lines.append("%s: %s" % (s["title"], t.strip("[]")))
    body.append("<ul><li>A laptop, visible on the desk in every reaction video.</li></ul>"); lines.append("A laptop, visible on the desk in every reaction video.")
    add("h1", "Reaction clips, in filming order")
    add("p", "Each link opens at the second the clip starts.")
    allclips = []
    for g in groups:
        for s in g["scripts"]:
            cl = clips(s)
            if not cl: continue
            add("h3", "%s (%s)" % (s["title"], s["id"]))
            for vid, sec, label in cl:
                url = "https://www.youtube.com/watch?v=%s&t=%ds" % (vid, sec); allclips.append((s["id"], vid))
                body.append('<ul><li><a href="%s">Opens at %d:%02d</a>: %s</li></ul>' % (url, sec // 60, sec % 60, esc(label)))
                lines.append("Opens at %d:%02d: %s" % (sec // 60, sec % 60, label))
    traps = []
    for g in groups:
        add("h1", g["name"])
        for s in g["scripts"]:
            add("h2", "%s · %s" % (s["id"], s["title"]))
            n = sum(words(t) for k, t in s["paras"] if k == "spoken")
            for kind, t in s["paras"]:
                if dollar_trap(t): traps.append((s["id"], t[:90]))
                if kind == "head":
                    t = re.sub(r"Filming script\. [\d,]+ spoken words", "Filming script. %s spoken words" % format(n, ","), t)
                    add("p", t, 'style="font-style:italic"')
                elif kind == "cue": add("p", t, CUE)
                else: add("p", t, P)
    open(os.path.join(out_dir, name + ".html"), "w").write(page(name, body)); seq[name] = lines
    json.dump(seq, open(os.path.join(out_dir, "built_seq.json"), "w"), ensure_ascii=False, indent=0)
    for r in report: print("%-70s %2d scripts %6d words" % r)
    print("%-70s %2d scripts %6d words" % (name, sum(len(g["scripts"]) for g in groups), words(" ".join(lines))))
    print("reaction clips:", len(allclips), "| dollar-sign traps:", traps or "none")
    if "--check-clips" in sys.argv:
        bad = []
        for sid, vid in sorted(set(allclips)):
            u = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote("https://www.youtube.com/watch?v=" + vid, safe="")
            try: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read()
            except Exception as e: bad.append((sid, vid, str(e)[:40]))
        print("clip ids that did not answer:", bad or "none")


if __name__ == "__main__":
    main()
