#!/usr/bin/env python3
"""THE GRAPHIC-LOCK REVIEW PAGE FOR A SHEET BUILD'S VERTICAL (PRE-RENDER-APPROVAL.md "The review page"): the first
minute on top, "Your decisions", "What I decided", then every graphic and clip of the film at 9:16 in timeline order,
three per row, each a still on its real frame with a "Play it moving, in context" button feeding ONE player, then the
checks and one reply box. Nothing here is a full film.

  python3 sbl_page.py --build B --sheet SHEET.json --out REVIEW_DIR --extra page_extra.json [--media] [--clips-only]

--clips-only (a later round): only the clips and photos, each with its fill / square / whole verdict, the reason, and
the proof sheet of the three crops (clip_fit.py). page_extra.json may then carry "minutes": [{"title", "src",
"poster", "caption"}] (several first-minute players side by side, e.g. before and after) and "extra_html".

--media renders what the page shows: the first-minute draft (1080 + 540p), one context clip per item (3 s of speech
either side, 540p) and its still. page_extra.json: {"title", "intro", "locked", "decisions": [..], "decided": [..],
"checks": [..], "reply", "first_minute_end", "options": [{"title", "img", "caption"}]}.
"""
import argparse, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000 / 1001
E = html.escape
KIND = {"lower-third": "Lower third", "before-card": "Fact card", "side-list": "3A list card", "cycle": "Cycle diagram",
        "softblue:title_card": "Title card", "softblue:recap": "Recap card", "cta": "CTA button", "tally": "Running total", "clip": "Clip", "photo": "Photo", "phone": "App demo"}


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True); ap.add_argument("--sheet", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--extra", required=True); ap.add_argument("--media", action="store_true")
    ap.add_argument("--clips-only", action="store_true")
    a = ap.parse_args()
    B = os.path.abspath(a.build); out = os.path.abspath(a.out)
    for d in ("context", "stills", "first-minute"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    S = json.load(open(a.sheet)); X = json.load(open(a.extra))
    rp_ = os.path.join(B, "sheet_report.json")
    rep = json.load(open(rp_)) if os.path.exists(rp_) else dict(pictures=[])     # a master build redrawn by master_to_sbl.py has none
    J = json.load(open(os.path.join(B, "beats.json")))
    W = S["words"]["list"]
    say = lambda x, y: " ".join(w["w"] for w in W if x <= w["t0"] < y)
    mode = {p["id"]: p for p in rep["pictures"]}
    items = []
    for g in ([] if a.clips_only else S["graphics"]):
        items.append(dict(id=g["id"], kind=g["template"], t0=g["t0"], t1=g["t1"], copy=g["text"], beats=g.get("driven_by", []), still_at=g["t1"] - 0.6))
    for b in J["beats"]:
        if b["kind"] in ("card", "bleed") and not b.get("pid"):
            # a master build: the picture is the recovered library file (assets.py), its label the recovered kind
            sys.path.insert(0, B)
            from assets import MEDIA
            m = MEDIA[b["media"]]
            np_ = sum(1 for r in items if r.get("pic")) + 1
            lab = b.get("label") or {"ai": "AI-GENERATED", "real": "Real picture of me - not AI-generated"}.get(b.get("label_kind"))
            items.append(dict(id=f"P{np_:02d}", pic=True, kind="phone" if b.get("phone") else ("photo" if m[0] == "img" else "clip"), t0=b["t0"], t1=b["t1"],
                              still_at=(b["t0"] + b["t1"]) / 2, copy=[x for x in [lab] if x], src=os.path.basename(m[1]),
                              note="The whole picture in a card (never cropped shorter)." if b["kind"] == "card" else "Fills the frame."))
        elif b["kind"] in ("card", "bleed"):
            p = next(x for x in S["pictures"] if x["id"] == b["pid"])
            m = mode[b["media"]]
            fit = m.get("fit") or {}
            shape = m.get("shape") or ("fill" if m["mode"] == "bleed" else "whole")
            proof = None
            if fit.get("sheet") and os.path.exists(fit["sheet"]):
                os.makedirs(os.path.join(out, "proof"), exist_ok=True)
                proof = "proof/" + b["media"] + ".jpg"
                import shutil
                shutil.copy(fit["sheet"], os.path.join(out, proof))
            items.append(dict(id=b["media"], kind=p["kind"], t0=b["t0"], t1=b["t1"], still_at=(b["t0"] + b["t1"]) / 2,
                              copy=[x for x in [p.get("label")] if x], note=m["why"][0].upper() + m["why"][1:], shape=shape, proof=proof,
                              by=fit.get("overridden_by"), src=m["source"]))
    items.sort(key=lambda r: r["t0"])
    items += X.get("extra_items", [])                 # ready-made samples (a template the film itself does not use)
    fm_end = X["first_minute_end"]
    fm = os.path.join(out, "first-minute", "DRAFT - first minute 9x16.mp4")
    if a.media:
        run = lambda c: subprocess.run(c, check=True)
        pv = [sys.executable, os.path.join(HERE, "sbl_preview.py"), "--build", B]
        if not os.path.exists(fm) and not X.get("minutes"):
            run(pv + ["--range", "0", str(fm_end), "--exact", "--out", fm])
            run([FF, "-v", "error", "-y", "-i", fm, "-vf", "scale=540:-2", "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "copy",
                 "-movflags", "+faststart", fm.replace(".mp4", " - REVIEW 540p.mp4")])
            run([FF, "-v", "error", "-y", "-ss", "9", "-i", fm, "-frames:v", "1", "-vf", "scale=540:-2", fm.replace(".mp4", ".jpg")])
        for r in items:
            if r.get("premade"):
                continue
            clip = os.path.join(out, "context", f"{r['id']}-context - REVIEW 540p.mp4")
            a0, b0 = max(0.0, r["t0"] - 3.0), min(S["video"]["duration"] - 0.05, r["t1"] + 3.0)
            if not os.path.exists(clip):
                run(pv + ["--range", f"{a0:.3f}", f"{b0:.3f}", "--exact", "--size", "540", "--out", clip])
            st = os.path.join(out, "stills", r["id"] + ".jpg")
            if not os.path.exists(st):
                run([FF, "-v", "error", "-y", "-ss", f"{max(0.0, r['still_at'] - a0):.3f}", "-i", clip, "-frames:v", "1", "-q:v", "3", st])
            print(r["id"], "media ok", flush=True)
    cards = []
    for r in items:
        lines = [E(s) for s in r["copy"]]
        body = "<br>".join(lines)
        SH = {"fill": "FILLS THE FRAME", "square": "CENTRE SQUARE", "whole": "WHOLE CLIP", "phone": "PHONE, WHOLE"}
        if r.get("shape"):
            body = f'<span class="shape {r["shape"]}">{SH.get(r["shape"], r["shape"])}</span>' + (" (your call)" if r.get("by") == "Dan" else "") + ("<br>" + body if body else "")
        if r.get("src"):
            body += ("<br>" if body else "") + "<b>source</b>: " + E(r["src"])
        if r.get("note"):
            body += "<br><i>" + E(r["note"]) + "</i>"
        beat = ""
        if r.get("beats"):
            beat = "<details><summary>Beat sheet (every move on a word)</summary><table>" + "".join(
                f"<tr><td>{mmss(b['t'])}</td><td>{E(b['phrase'])}</td><td>{E(b['part'])}</td></tr>" for b in r["beats"]) + "</table></details>"
        cards.append(f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(r['t1'])}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a><button onclick="play('context/{r['id']}-context - REVIEW 540p.mp4','{r['id']}')">Play it moving, in context</button>
<div class="copy">{body}</div>{beat}
""" + (f"""<details open><summary>The three crops: whole (yellow = fill, blue = square), square, fill</summary><a href="{r['proof']}"><img loading="lazy" src="{r['proof']}"></a></details>""" if r.get("proof") else "") + ("" if r.get("premade") else f"""<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(say(r['t0'] - 5, r['t0']))}<br><b>during</b>: {E(say(r['t0'], r['t1']))}<br><b>after</b>: {E(say(r['t1'], r['t1'] + 5))}</p></details>""") + "</article>")
    if X.get("minutes"):
        minute = '<div class="grid">' + "".join(
            f"""<article><h3>{E(m['title'])}</h3><video controls preload="none" playsinline poster="{m['poster']}" src="{m['src']}"></video><div class="copy">{m['caption']}</div></article>"""
            for m in X["minutes"]) + "</div>" + f"<p class=\"small\">{X.get('first_minute_note', '')}</p>"
    else:
        minute = f"""<video controls preload="none" playsinline poster="first-minute/DRAFT - first minute 9x16.jpg" src="first-minute/DRAFT - first minute 9x16 - REVIEW 540p.mp4"></video>
<p class="small"><a href="first-minute/DRAFT - first minute 9x16.mp4">1080 x 1920 file</a> · {X.get('first_minute_note', '')}</p>"""
    opts = "".join(f"""<article><h3>{E(o['title'])}</h3><a href="{o['img']}"><img loading="lazy" src="{o['img']}"></a><div class="copy">{o['caption']}</div></article>""" for o in X.get("options", []))
    page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(X['title'])}</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.wide{{grid-template-columns:repeat(2,minmax(0,1fr))}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.shape{{display:inline-block;font-weight:800;font-size:13px;letter-spacing:.5px;padding:3px 9px;border-radius:7px;background:#1d5f8f;color:white}}.shape.fill{{background:#167a52}}.shape.whole{{background:#8a5a12}}.shape.phone{{background:#4a4f66}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:230px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table{{font-size:13px;color:#cfe0f0;border-collapse:collapse}}td{{padding:2px 8px 2px 0;vertical-align:top}}#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px;text-align:center}}#dock video{{max-height:60vh;width:auto;max-width:100%}}#minute video{{max-height:80vh;width:auto;max-width:100%;display:block;margin:auto}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>{E(X['title'])}</h1><p>{X['intro']}</p>
<p class="notice"><b>Already locked, reused as is:</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{''.join('<li>' + d + '</li>' for d in X['decisions'])}</ol>
<div class="grid wide">{opts}</div></section>
<section id="minute"><h2>{E(X.get('minute_title') or f'The first minute at 9:16 (0:00 to {mmss(fm_end)})')}</h2>{minute}</section>{X.get('extra_html', '')}
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in X['decided'])}</ul></section>
<section id="all"><h2>All {len(items)} {'clips' if a.clips_only else 'graphics and clips'} at 9:16, in order</h2><p class="small">Each is a still on its real frame at its real time, after every part has landed. "Play it moving" loads that item with 3 seconds of your speech either side into the one player below.</p>
<div id="dock"><div class="small" id="nowp">Pick an item below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div><div class="grid">{''.join(cards)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id+' in context';v.play();document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
    open(os.path.join(out, "index.html"), "w").write(page)
    json.dump(items, open(os.path.join(out, "items.json"), "w"), indent=1)
    print("page ok:", len(items), "items ->", os.path.join(out, "index.html"))


if __name__ == "__main__":
    main()
