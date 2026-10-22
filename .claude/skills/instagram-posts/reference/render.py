#!/usr/bin/env python3
"""Render @danrosefit image posts from content JSON: 1080 x 1350 JPEGs, a contact sheet, and a QA report.

    python3 .claude/skills/instagram-posts/reference/render.py CONTENT.json [CONTENT2.json ...] [--out DIR] [--sheet NAME]

Each content file names its format ("the-fix", "receipts", "steal-my-workout", "cheat-sheet"); the matching
template in templates/ lays it out. Image paths in a content file are relative to the project root (or absolute).
Output: <out>/<id>/<id>-01.jpg ... plus <out>/<id>/contact.jpg; with several files also <out>/<sheet>.jpg.
Default out: "Short-form video content/instagram-danrosefit/posts" (git-ignored: it holds shirtless photos).

The page auto-fits text: an element with data-fit="max,min" inside a data-fit-col box shrinks (largest first) until
the box no longer overflows. QA then checks every slide at phone size and FAILS the post (exit 1) on: overflow,
text in the outer 17 css px (34 px posted, the 3:4 grid crop), any text under 16 css px (32 px posted), headlines
under 35 css px (70 px posted), long dashes, or a slide image without its AI/real label (slide 1 exempt).
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, ChainableUndefined
from markupsafe import Markup
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEFAULT_OUT = ROOT / "Short-form video content" / "instagram-danrosefit" / "posts"
DEFAULT_AVATAR = "Short-form video content/instagram-danrosefit/template-r1-mockups/source/avatar.jpg"
TAGS = {"y": '<span class="y">', "r": '<span class="r">', "hl": '<span class="hl">', "em": '<span class="em">',
        "b": '<b>'}


def mk(text):
    """Escape, then allow [y] yellow, [r] red, [hl] highlighter, [em] yellow bold, [b] bold; newline = line break."""
    if text is None:
        return Markup("")
    s = html.escape(str(text), quote=False)
    for t, open_ in TAGS.items():
        close = "</b>" if t == "b" else "</span>"
        s = s.replace(f"[{t}]", open_).replace(f"[/{t}]", close)
    return Markup(s.replace("\n", "<br>"))


def resolve(p):
    q = Path(p)
    return q if q.is_absolute() else ROOT / q


def uri(p):
    return resolve(p).as_uri()


FIT_JS = r"""
() => {
  const over = el => el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
  for (const col of document.querySelectorAll('[data-fit-col]')) {
    const kids = [...col.querySelectorAll('[data-fit]')].map(el => {
      const [mx, mn] = el.dataset.fit.split(',').map(Number); return {el, mx, mn, cur: mx};
    });
    kids.forEach(k => k.el.style.fontSize = k.mx + 'px');
    let guard = 400;
    while (over(col) && guard-- > 0) {
      // shrink the element with the most room above its minimum, relative to its size
      let best = null;
      for (const k of kids) if (k.cur > k.mn && (!best || (k.cur - k.mn) / k.mx > (best.cur - best.mn) / best.mx)) best = k;
      if (!best) break;
      best.cur = Math.max(best.mn, best.cur - 1);
      best.el.style.fontSize = best.cur + 'px';
    }
  }
}
"""

QA_JS = r"""
() => {
  const out = [];
  const slides = [...document.querySelectorAll('.slide')];
  slides.forEach((sl, i) => {
    const R = sl.getBoundingClientRect(), n = i + 1, M = 17;
    const prob = msg => out.push({slide: n, problem: msg});
    for (const col of sl.querySelectorAll('[data-fit-col]'))
      if (col.scrollHeight > col.clientHeight + 1) prob('text overflows its box: "' + col.innerText.slice(0, 60) + '"');
    const walker = document.createTreeWalker(sl, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      const t = node.textContent.trim();
      if (!t) continue;
      const el = node.parentElement, cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      const fs = parseFloat(cs.fontSize);
      if (fs < 15.99) prob('text under 32 px posted (' + (fs * 2).toFixed(0) + ' px): "' + t.slice(0, 40) + '"');
      if (/[—–]/.test(t)) prob('long dash: "' + t.slice(0, 40) + '"');
      const rg = document.createRange(); rg.selectNodeContents(node);
      for (const r of rg.getClientRects()) {
        if (r.width < 1) continue;
        if (r.left < R.left + M - 0.5 || r.right > R.right - M + 0.5 || r.top < R.top + M - 0.5 || r.bottom > R.bottom - M + 0.5) {
          prob('text inside the outer 34 px: "' + t.slice(0, 40) + '"'); break;
        }
      }
    }
    // text over text is always a collision
    const boxes = [];
    const w2 = document.createTreeWalker(sl, NodeFilter.SHOW_TEXT);
    let tn;
    while ((tn = w2.nextNode())) {
      if (!tn.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(tn);
      const pe = tn.parentElement, pcs = getComputedStyle(pe), fs = parseFloat(pcs.fontSize);
      // glyph band, not the font's content box: Anton caps sit in about 0.72 em, Manrope text in about 0.9 em
      const half = (pcs.fontFamily.includes('Anton') ? 0.36 : 0.45) * fs;
      for (const q of rg.getClientRects()) if (q.width > 1) {
        const mid = (q.top + q.bottom) / 2;
        boxes.push({el: pe, r: {left: q.left, right: q.right, top: mid - half, bottom: mid + half, height: 2 * half}, t: tn.textContent.trim()});
      }
    }
    outer: for (let a = 0; a < boxes.length; a++) for (let b = a + 1; b < boxes.length; b++) {
      const A = boxes[a], B = boxes[b];
      if (A.el === B.el || A.el.contains(B.el) || B.el.contains(A.el)) continue;
      const ix = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left);
      const iy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
      if (ix > 2 && iy > 2) { prob('text overlaps text: "' + A.t.slice(0, 30) + '" / "' + B.t.slice(0, 30) + '"'); break outer; }
    }
    for (const h of sl.querySelectorAll('h1.hd, h2.hd'))
      if (parseFloat(getComputedStyle(h).fontSize) < 34.99) prob('headline under 70 px posted: "' + h.innerText.slice(0, 40) + '"');
    if (n > 1) {
      const imgs = [...sl.querySelectorAll('img')].filter(im => !im.alt.startsWith('Dan Rose') && !im.dataset.nolabel);
      if (imgs.length && !sl.querySelector('.lbl, [data-label]')) prob('image without a real/AI label');
    }
    for (const im of sl.querySelectorAll('img')) if (!im.complete || !im.naturalWidth) prob('image failed to load: ' + im.src.slice(-60));
  });
  return out;
}
"""


def render(content_path: Path, out_root: Path, page):
    post = json.load(open(content_path))
    post.setdefault("avatar", DEFAULT_AVATAR)
    env = Environment(loader=FileSystemLoader(HERE / "templates"), undefined=ChainableUndefined, autoescape=True)
    env.filters["mk"] = mk
    env.filters["uri"] = uri
    html_text = env.get_template(f"{post['format']}.html.j2").render(post=post)
    out = out_root / post["id"]
    out.mkdir(parents=True, exist_ok=True)
    page_file = out / f"{post['id']}.html"
    page_file.write_text(html_text)
    page.goto(page_file.as_uri())
    page.wait_for_load_state("networkidle")
    # Google Fonts can land after networkidle; measuring before Anton and Manrope are in gives false overlaps
    page.wait_for_function("document.fonts.status === 'loaded' && document.fonts.check('40px Anton') && document.fonts.check('700 20px Manrope')", timeout=20000)
    page.wait_for_function("[...document.images].every(i => i.complete)", timeout=20000)
    page.evaluate(FIT_JS)
    problems = page.evaluate(QA_JS)
    files = []
    for i, el in enumerate(page.query_selector_all(".slide"), 1):
        png = out / f"_s{i}.png"
        el.screenshot(path=str(png))
        im = Image.open(png).convert("RGB")
        assert im.size == (1080, 1350), f"{post['id']} slide {i} is {im.size}"
        name = f"{post['id']}-{i:02d}.jpg" if post["format"] != "cheat-sheet" else f"{post['id']}.jpg"
        im.save(out / name, quality=92, optimize=True, progressive=True)
        png.unlink()
        files.append(out / name)
    sheet(files, out / "contact.jpg")
    report = {"id": post["id"], "format": post["format"], "slides": [os.path.relpath(f, ROOT) for f in files],
              "problems": problems}
    json.dump(report, open(out / "qa.json", "w"), indent=1)
    return report, files


def sheet(files, dest, w=270, gap=10, label=None):
    """One row of slides at phone-feed size (270 px wide)."""
    h = int(w * 1350 / 1080)
    im = Image.new("RGB", (gap + len(files) * (w + gap), h + 2 * gap), (207, 203, 196))
    for i, f in enumerate(files):
        im.paste(Image.open(f).resize((w, h), Image.LANCZOS), (gap + i * (w + gap), gap))
    im.save(dest, quality=88)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content", nargs="+")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--sheet", default=None, help="also write <out>/<sheet>.jpg with every post as one row")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    out_root = Path(a.out)
    rows, bad = [], 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        page = b.new_page(viewport={"width": 3200, "height": 800}, device_scale_factor=2)
        for c in a.content:
            rep, files = render(Path(c), out_root, page)
            rows.append(files)
            status = "OK" if not rep["problems"] else f"{len(rep['problems'])} PROBLEMS"
            print(f"{rep['id']}: {len(files)} slides, {status}")
            for pr in rep["problems"]:
                print(f"   slide {pr['slide']}: {pr['problem']}")
            bad += bool(rep["problems"])
        b.close()
    if a.sheet and rows:
        w, gap = 270, 10
        h = int(w * 1350 / 1080)
        width = gap + max(len(r) for r in rows) * (w + gap)
        big = Image.new("RGB", (width, gap + len(rows) * (h + gap)), (207, 203, 196))
        for j, r in enumerate(rows):
            for i, f in enumerate(r):
                big.paste(Image.open(f).resize((w, h), Image.LANCZOS), (gap + i * (w + gap), gap + j * (h + gap)))
        big.save(out_root / f"{a.sheet}.jpg", quality=85)
        print("sheet:", out_root / f"{a.sheet}.jpg")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
