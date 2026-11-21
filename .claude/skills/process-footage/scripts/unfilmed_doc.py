#!/usr/bin/env python3
"""Build the "Unfilmed Content And Ads" document: every approved script not filmed on this shoot and the shoot
before, with a summary at the top split by format (long ads, short ads, long-form content, short-form content),
then the full scripts by source. Dan approved this layout on 2026-11-14.

    unfilmed_doc.py export --out DIR DOCID [DOCID ...]   # export Google Docs as text (rclone, gdrive: remote)
    unfilmed_doc.py build spec.json --out unfilmed.html  # assemble the HTML (upload it as a Google Doc)

spec.json:
{
  "title": "Unfilmed Content And Ads",
  "intro": "Every script from the 11/13 ... shoot that has not been filmed yet ...",
  "sources": {"ads": {"file": "DIR/Great Again T Ad Outlines (23 ads).txt", "header": "^[LS]\\\\d+\\\\. "},
              "nsf": {"file": "DIR/Next Shoot Filming Scripts.txt", "header": "^([A-D]\\\\d+|TESLA) · "}},
  "parts": [
    {"heading": "Part 1: Ads (Great Again T)", "note": "S16, S23 and S29 are struck through and left out.",
     "groups": [{"heading": "", "items": [
        {"source": "ads", "start": "^L03\\\\. ", "format": "ad-long", "label": "Great Again T",
         "note": "Only the opening line was filmed on 11/13 (roll C1910). Film the whole script."}]}]}
  ]
}
Item fields: source, start (regex of its title line), optional end (regex; default: the source's next header
line), optional title (default: the start line), format (ad-long | ad-short | long | short), label (summary
sub-list name, e.g. "Shorts, from the 11/13 scripts"), note (italic line under the title).
Lines starting "* " become bullets (indent = nesting); every other non-blank line is its own paragraph, so
[BRACKETED CAPS] editor cues and spoken lines keep their order. Check the result has 0 em dashes in text we add.
"""
import argparse, html, json, os, re, subprocess, sys

E = html.escape
FORMATS = [("ad-long", "Ads, long format"), ("ad-short", "Ads, short format"),
           ("long", "Long-form content"), ("short", "Short-form content")]


def export(a):
    os.makedirs(a.out, exist_ok=True)
    for d in a.ids:
        r = subprocess.run([os.path.expanduser("~/bin/rclone"), "backend", "copyid", "gdrive:", d, a.out + "/",
                            "--drive-export-formats", "txt"], capture_output=True, text=True)
        print(d, "ok" if r.returncode == 0 else r.stderr[-300:])
    for f in sorted(os.listdir(a.out)):
        print("  ", f)


def body(out, lines):
    depth = 0
    for ln in lines:
        if not ln.strip():
            continue
        m = re.match(r"^(\s*)\* (.*)$", ln)
        if m:
            lvl = 1 + len(m.group(1).replace("\t", "   ")) // 3
            while depth < lvl:
                out.append("<ul>"); depth += 1
            while depth > lvl:
                out.append("</ul>"); depth -= 1
            out.append(f"<li>{E(m.group(2))}</li>")
        else:
            while depth:
                out.append("</ul>"); depth -= 1
            out.append(f"<p>{E(ln.strip())}</p>")
    while depth:
        out.append("</ul>"); depth -= 1


def build(a):
    spec = json.load(open(a.spec))
    src = {k: {"lines": open(v["file"], encoding="utf-8-sig").read().split("\n"), "header": re.compile(v["header"])}
           for k, v in spec["sources"].items()}

    def extract(it):
        s = src[it["source"]]
        L = s["lines"]
        st = next((i for i, x in enumerate(L) if re.search(it["start"], x)), None)
        if st is None:
            sys.exit(f"start not found: {it['start']} in {it['source']}")
        endre = re.compile(it["end"]) if it.get("end") else s["header"]
        en = next((i for i in range(st + 1, len(L)) if endre.search(L[i])), len(L))
        skip = set(spec.get("skip_lines", []))
        return (it.get("title") or L[st].strip()), [x for x in L[st + 1:en] if x.strip() not in skip]

    summary = {f: {} for f, _ in FORMATS}
    parts = []
    for p in spec["parts"]:
        groups = []
        for g in p["groups"]:
            items = []
            for it in g["items"]:
                title, lines = extract(it)
                items.append((title, lines, it))
                summary[it["format"]].setdefault(it.get("label", ""), []).append(
                    title + (f" ({it['summary_note']})" if it.get("summary_note") else ""))
            groups.append((g.get("heading", ""), items))
        parts.append((p, groups))
    out = [f"<h1>{E(spec['title'])}</h1>", f"<p>{E(spec['intro'])}</p>"]
    out.append("<h2>Summary: what's in this document</h2>")
    for f, name in FORMATS:
        out.append(f"<h3>{E(name)}</h3>")
        if not summary[f]:
            out.append(f"<ul><li>{E(spec.get('empty', {}).get(f, 'None left.'))}</li></ul>")
            continue
        for label, titles in summary[f].items():
            if label:
                out.append(f"<p><b>{E(label)}:</b></p>")
            out.append("<ul>" + "".join(f"<li>{E(t)}</li>" for t in titles) + "</ul>")
    out.append(f"<p>Full scripts follow, by source, in Parts 1 to {len(parts)}.</p>")
    for p, groups in parts:
        out.append(f"<h2>{E(p['heading'])}</h2>")
        if p.get("note"):
            out.append(f"<p>{E(p['note'])}</p>")
        for gh, items in groups:
            if gh:
                out.append(f"<h3>{E(gh)}</h3>")
            for title, lines, it in items:
                out.append(f"<h4>{E(title)}</h4>")
                if it.get("note"):
                    out.append(f"<p><i>{E(it['note'])}</i></p>")
                body(out, lines)
    doc = f"<html><head><meta charset=\"utf-8\"><title>{E(spec['title'])}</title></head><body>" + "\n".join(out) + "</body></html>"
    open(a.out, "w").write(doc)
    added = " ".join([spec["intro"]] + [p.get("note", "") for p, _ in parts])
    print(f"wrote {a.out}: {doc.count('<h4>')} scripts; em dashes in text we added: {added.count(chr(8212))}")
    for f, name in FORMATS:
        print(f"  {name}: {sum(len(v) for v in summary[f].values())}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    e = sp.add_parser("export"); e.add_argument("--out", required=True); e.add_argument("ids", nargs="+")
    b = sp.add_parser("build"); b.add_argument("spec"); b.add_argument("--out", required=True)
    a = ap.parse_args()
    (export if a.cmd == "export" else build)(a)
