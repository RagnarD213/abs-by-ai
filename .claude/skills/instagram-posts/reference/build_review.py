#!/usr/bin/env python3
"""Build Dan's pick page for a batch of rendered posts: one swipeable row per carousel, ranked, with a tick box
per post and a "Copy my picks" button. Slides are downsized to 720 x 900 so 30+ carousels fit one Artifact.

    python3 .claude/skills/instagram-posts/reference/build_review.py SPEC.json OUT_DIR

SPEC: {"title", "lede", "sections": [{"heading", "intro", "ranking": "ranking-x.md", "ids": [...]}],
       "singles": [{"id", "note"}], "decisions": [{"key", "question", "detail_html", "options": [[value, label]],
       "default", "images": [paths]}], "shootlist": ["shootlist-x.md"], "decided": ["..."], "unticked": [ids],
       "notes": {id: "extra line"}}
Publish OUT_DIR/index.html with the Artifact tool, passing every slides/* file in `files`.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
POSTS = ROOT / "Short-form video content" / "instagram-danrosefit" / "posts"


def plain(s):
    return re.sub(r"\[/?\w+\]", "", s or "").replace("\n", " ").strip()


def ranking(md):
    """id -> (rank, why, placeholder) from a ranking table."""
    out = {}
    for line in (HERE / md).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].isdigit():
            out[cells[1].strip("`")] = (int(cells[0]), cells[2], cells[3] if len(cells) > 3 else "")
    return out


def headline(c):
    f = c["format"]
    if f == "cheat-sheet":
        return plain(c["title"])
    return plain(c["cover"]["headline"])


def slides(pid, dest):
    qa = json.load(open(POSTS / pid / "qa.json"))
    assert not qa["problems"], f"{pid} has QA problems: {qa['problems']}"
    out = []
    for rel in qa["slides"]:
        src = ROOT / rel
        name = f"slides/{src.stem}.jpg"
        im = Image.open(src).convert("RGB").resize((720, 900), Image.LANCZOS)
        im.save(dest / name, quality=82, optimize=True, progressive=True)
        out.append(name)
    return out


def md_list(md):
    items = []
    for line in (HERE / md).read_text().splitlines():
        if re.match(r"^\s*(-|\d+\.)\s", line):
            items.append(re.sub(r"^\s*(-|\d+\.)\s+", "", line))
    return items


def inline_md(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"`(.+?)`", r"\1", s)


def main(spec_path, out_dir):
    spec = json.load(open(spec_path))
    dest = Path(out_dir)
    (dest / "slides").mkdir(parents=True, exist_ok=True)
    unticked = set(spec.get("unticked", []))
    notes = spec.get("notes", {})
    body = []
    total = 0

    for d in spec.get("decisions", []):
        imgs = "".join(f'<img src="{s}" alt="" loading="lazy">' for p in d.get("images", []) for s in slides(p, dest))
        opts = "".join(
            f'<label class="opt"><input type="radio" name="{d["key"]}" id="{d["key"]}-{v}" value="{v}"'
            f'{" checked" if v == d["default"] else ""}> <span>{html.escape(lbl)}</span></label>'
            for v, lbl in d["options"])
        body.append(f'<article class="decision"><h3>{html.escape(d["question"])}</h3>{d["detail_html"]}'
                    f'{"<div class=strip tabindex=0>" + imgs + "</div>" if imgs else ""}'
                    f'<div class="opts" data-key="{d["key"]}">{opts}</div></article>')

    for s in spec.get("singles", []):
        c = json.load(open(HERE / "content" / f"{s['id']}.json"))
        im = slides(s["id"], dest)[0]
        body.append(f'<article class="decision single"><img src="{im}" alt="{html.escape(headline(c))}" loading="lazy">'
                    f'<div>{s["note"]}</div></article>')

    secs = []
    for sec in spec["sections"]:
        rk = ranking(sec["ranking"])
        rows = []
        for pid in sorted(sec["ids"], key=lambda i: rk.get(i, (99,))[0]):
            c = json.load(open(HERE / "content" / f"{pid}.json"))
            r, why, ph = rk.get(pid, (0, "", ""))
            imgs = "".join(f'<img src="{s}" alt="Slide {k + 1} of {pid}" loading="lazy">'
                           for k, s in enumerate(slides(pid, dest)))
            phb = (f'<span class="flag">Needs filming: {html.escape(ph)}</span>'
                   if ph and ph.lower() not in ("no", "none", "") else "")
            extra = f'<p class="why note">{notes[pid]}</p>' if pid in notes else ""
            rows.append(
                f'<article class="post"><div class="post-head">'
                f'<label class="pick"><input type="checkbox" id="pick-{pid}" data-id="{pid}"'
                f'{"" if pid in unticked else " checked"}> Queue it</label>'
                f'<span class="rank">#{r}</span><h3>{html.escape(headline(c))}</h3>{phb}'
                f'<span class="count">{imgs.count("<img")} slides · {pid}</span></div>'
                f'<p class="why">{inline_md(why)}</p>{extra}<div class="strip" tabindex="0">{imgs}</div></article>')
            total += 1
        secs.append(f'<section><h2>{html.escape(sec["heading"])}</h2><p class="lede">{sec["intro"]}</p>{"".join(rows)}</section>')

    shoot = "".join(f"<li>{inline_md(i)}</li>" for f in spec.get("shootlist", []) for i in md_list(f))
    decided = "".join(f"<li>{i}</li>" for i in spec.get("decided", []))
    page = TEMPLATE.format(title=html.escape(spec["title"]), lede=spec["lede"], total=total,
                           decisions="".join(body), sections="".join(secs), shoot=shoot, decided=decided)
    (dest / "index.html").write_text(page)
    print("wrote", dest / "index.html", "with", total, "carousels and", len(list((dest / "slides").glob("*.jpg"))), "images")


TEMPLATE = """<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@500;600;700;800&display=swap">
<style>
/* Layout: one column of ranked post rows; carousels swipe sideways like the Instagram app; picks travel back by copy. */
:root {{
  --bg: #F2EEE6; --surface: #FFFFFF; --fg: #0E1013; --muted: #555B64; --line: rgba(14,16,19,.14);
  --accent: #D33A2C; --hi: #FFD23F; --hi-fg: #0E1013;
  --display: 'Anton', Impact, 'Arial Narrow', sans-serif;
  --body: 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{ --bg: #121417; --surface: #1B1E23; --fg: #F2EEE6; --muted: #A4ABB4; --line: rgba(242,238,230,.14); --accent: #E5584A; color-scheme: dark; }}
}}
:root[data-theme="dark"] {{ --bg: #121417; --surface: #1B1E23; --fg: #F2EEE6; --muted: #A4ABB4; --line: rgba(242,238,230,.14); --accent: #E5584A; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 16px; line-height: 1.5; }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding-inline: 20px; padding-block: 32px 120px; display: flex; flex-direction: column; gap: 48px; }}
h1, h2, h3 {{ margin: 0; text-wrap: balance; }}
h1 {{ font-family: var(--display); font-weight: 400; text-transform: uppercase; font-size: clamp(36px, 6vw, 64px); line-height: .98; }}
h2 {{ font-family: var(--display); font-weight: 400; text-transform: uppercase; font-size: clamp(28px, 4vw, 40px); line-height: 1; }}
h3 {{ font-size: 19px; font-weight: 800; }}
p {{ margin: 0; max-width: 72ch; }}
.lede {{ font-size: 17px; color: var(--muted); font-weight: 600; }}
.eyebrow {{ font-size: 13px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); display: flex; align-items: center; gap: 8px; }}
.eyebrow::before {{ content: ""; width: 9px; height: 9px; background: var(--accent); display: block; }}
section {{ display: flex; flex-direction: column; gap: 24px; }}
.post {{ display: flex; flex-direction: column; gap: 10px; padding-top: 18px; border-top: 1px solid var(--line); }}
.post-head {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; }}
.rank {{ font-family: var(--display); font-size: 26px; color: var(--accent); font-variant-numeric: tabular-nums; }}
.count {{ font-size: 13px; font-weight: 700; color: var(--muted); }}
.flag {{ font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; background: var(--accent); color: #fff; padding: 3px 8px; border-radius: 4px; }}
.why {{ color: var(--muted); font-weight: 600; }}
.note {{ color: var(--fg); }}
.pick {{ display: inline-flex; align-items: center; gap: 8px; font-weight: 800; font-size: 14px; background: var(--hi); color: var(--hi-fg); padding: 6px 12px; border-radius: 6px; cursor: pointer; }}
.pick input {{ width: 18px; height: 18px; accent-color: #0E1013; }}
.post:has(.pick input:not(:checked)) .strip {{ opacity: .55; }}
.post:has(.pick input:not(:checked)) .pick {{ background: var(--surface); color: var(--muted); border: 1px solid var(--line); }}
.strip {{ display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 10px; }}
.strip img {{ flex: none; width: min(280px, 70vw); aspect-ratio: 4 / 5; height: auto; scroll-snap-align: start; border-radius: 6px; background: var(--surface); }}
.decision {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 20px 22px; display: flex; flex-direction: column; gap: 12px; }}
.decision.single {{ flex-direction: row; flex-wrap: wrap; align-items: flex-start; gap: 20px; }}
.decision.single img {{ width: min(340px, 100%); border-radius: 6px; }}
.decision.single > div {{ flex: 1 1 280px; min-width: 0; display: flex; flex-direction: column; gap: 10px; }}
.opts {{ display: flex; flex-direction: column; gap: 8px; }}
.opt {{ display: flex; gap: 10px; align-items: flex-start; font-weight: 700; cursor: pointer; }}
.opt input {{ margin-top: 5px; width: 18px; height: 18px; flex: none; }}
ol, ul {{ margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 8px; max-width: 80ch; }}
li {{ font-weight: 600; }}
.bar {{ position: fixed; left: 0; right: 0; bottom: 0; padding: 12px 20px calc(12px + env(safe-area-inset-bottom, 0px)); background: var(--fg); color: var(--bg); display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; justify-content: center; z-index: 5; }}
.bar b {{ font-variant-numeric: tabular-nums; }}
.bar button {{ font: 800 16px var(--body); background: var(--hi); color: var(--hi-fg); border: 0; border-radius: 6px; padding: 10px 18px; cursor: pointer; }}
#out {{ width: 100%; max-width: 900px; font: 600 13px/1.4 ui-monospace, Menlo, monospace; display: none; }}
a {{ color: var(--accent); }}
:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
</style>

<div class="wrap">
  <header style="display:flex;flex-direction:column;gap:12px">
    <div class="eyebrow">@danrosefit · Carousels batch 1</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </header>
  <section><h2>Two quick calls</h2>{decisions}</section>
  {sections}
  <section><h2>Film at the next shoot</h2><p class="lede">Each line is one marked placeholder slide. Until it is filmed, that post stays off the queue.</p><ul>{shoot}</ul></section>
  <section><h2>What I decided</h2><ul>{decided}</ul></section>
</div>
<div class="bar" role="region" aria-label="Your picks">
  <span><b id="n">0</b> of {total} carousels ticked</span>
  <button type="button" id="copy">Copy my picks</button>
  <textarea id="out" rows="4" readonly aria-label="Your picks as text"></textarea>
</div>
<script>
(function () {{
  const boxes = [...document.querySelectorAll('.pick input')];
  const KEY = 'ig-batch1-picks';
  try {{ const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved) {{ boxes.forEach(b => {{ if (b.dataset.id in saved.p) b.checked = saved.p[b.dataset.id]; }});
      Object.entries(saved.r || {{}}).forEach(([k, v]) => {{ const el = document.getElementById(k + '-' + v); if (el) el.checked = true; }}); }}
  }} catch (e) {{}}
  const radios = () => Object.fromEntries([...document.querySelectorAll('.opts')].map(o => [o.dataset.key, (o.querySelector('input:checked') || {{}}).value]));
  function update() {{
    document.getElementById('n').textContent = boxes.filter(b => b.checked).length;
    try {{ localStorage.setItem(KEY, JSON.stringify({{p: Object.fromEntries(boxes.map(b => [b.dataset.id, b.checked])), r: radios()}})); }} catch (e) {{}}
  }}
  document.addEventListener('change', update); update();
  document.getElementById('copy').addEventListener('click', () => {{
    const r = radios();
    const text = 'Carousel picks: ' + boxes.filter(b => b.checked).map(b => b.dataset.id).join(', ') +
      '. Not these: ' + (boxes.filter(b => !b.checked).map(b => b.dataset.id).join(', ') || 'none') + '. ' +
      Object.entries(r).map(([k, v]) => k + ': ' + v).join('. ') + '.';
    const out = document.getElementById('out'); out.value = text; out.style.display = 'block';
    const btn = document.getElementById('copy');
    const done = ok => {{ btn.textContent = ok ? 'Copied. Paste it in chat' : 'Select the text below and copy it'; if (!ok) {{ out.focus(); out.select(); }} }};
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(() => done(true), () => done(false)); else done(false);
  }});
}})();
</script>
"""

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
