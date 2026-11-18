#!/usr/bin/env python3
"""One-time patch for round 8 (Dan, 2026-11-18). Already applied: kept as the record of what changed.
- the three top food swaps use the film graphics again, without his head
- one labelled graphic for the protein shake and protein bar
- a restaurant-style baked potato
- a small grey "Buy just one bottle - $97" button under the last two buy buttons only"""
import pathlib

R = pathlib.Path(__file__).resolve().parent.parent


def sub(path, old, new, count=1):
    p = R / path
    s = p.read_text()
    assert s.count(old) == count, (path, s.count(old), old[:60])
    p.write_text(s.replace(old, new))


# ---- letterdoc.py: pictures
p = R / 'letterdoc.py'
s = p.read_text()
a = s.index("    if 'egg whites' in t:")
b = s.index("    if 'tongkat' in t:")
new = '''    # Round 8 (Dan, 2026-11-18): back to the film graphics for the three top swaps, without his head (r8/nohead.py)
    if 'egg whites' in t:
        return swapimg('swap-eggs-nohead.jpg', 'Less: egg whites. More: whole eggs.')
    if 'butter' in t:
        return swapimg('swap-oil-nohead.jpg', 'More: olive oil. Less: butter.')
    if 'chicken breast' in t:
        s = swapimg('swap-steak-nohead.jpg', 'More: steak. Less: chicken breast.')
        if '5x' in d:
            s += '<p class="statline"><b>5x</b> the zinc in sirloin steak, ounce for ounce</p>'
        return s
    if 'protein shake' in t:      # one graphic with both, labelled (r8/shakebar.py)
        return swapimg('swap-shake-bar.jpg', 'Less: protein shake and protein bar', 'solo')
    if 'baked potato' in t:
        return tagimg(['potato-restaurant.jpg'], 'more', 'Big baked potato with butter, sour cream and chives')
'''
p.write_text(s[:a] + new + s[b:])

# ---- gen.py: swapimg class, the one-bottle button, its check
sub('gen.py', '''def swapimg(name, alt):
    return f'<figure class="swapimg"><img src="{A}{name}" alt="{alt}"></figure>\'''', '''def swapimg(name, alt, cls=''):
    return f'<figure class="swapimg {cls}"><img src="{A}{name}" alt="{alt}"></figure>'

ONE_BOTTLE = 'Buy just one bottle - $97'      # Dan, 2026-11-18: small grey second button under the last two buy buttons only

def one_bottle_buttons(letter_html):
    """Adds the small one-bottle button after the last two buy buttons of the letter."""
    marks = [m.end() for m in re.finditer(r'<div class="cta-wrap [^"]*"><a class="cta" .*?</a>(?:<ul class="cta-notes">.*?</ul>)?', letter_html, flags=re.S)]
    assert len(marks) >= 2, len(marks)
    link = f'<a class="cta2" href="{LINKS["order"]}?option=single">{ONE_BOTTLE}</a>'
    for at in sorted(marks[-2:], reverse=True):
        letter_html = letter_html[:at] + link + letter_html[at:]
    return letter_html''')
sub('gen.py', '''def letter():
    return render_letter()''', '''def letter():
    return one_bottle_buttons(render_letter())''')
sub('gen.py', "    n_btn = letter_html.count('<a class=\"cta\" ')\n",
    "    n_btn = letter_html.count('<a class=\"cta\" ')\n"
    "    assert pg.count('class=\"cta2\"') == 2 and letter_html.count(ONE_BOTTLE) == 2, 'one-bottle button under the last two buy buttons only'\n"
    "    ltext = ltext.replace(ONE_BOTTLE, ' ')\n")

# ---- page.css
p = R / 'page.css'
p.write_text(p.read_text() + '''
/* ---------- round 8 (Dan, 2026-11-18) ---------- */
/* film graphics are back for the food swaps (no head): edge to edge on a phone, rounded from tablet up */
.letter .swapimg{margin:12px -20px 0;border-top:1px solid #000;border-bottom:1px solid #000;background:#3a2412}
.letter .swapimg.solo{margin:14px -20px 18px}
.letter .swapimg img{width:100%;height:auto;display:block}
@media (min-width:768px){.letter .swapimg,.letter .swapimg.solo{margin-left:0;margin-right:0;border:0;border-radius:8px;overflow:hidden}}
/* the small one-bottle button: grey and quiet on purpose */
.cta2{display:block;width:fit-content;margin:14px auto 0;padding:8px 16px;border:1px solid #d3d8d3;border-radius:6px;background:#f1f2ef;
  color:#7b837e;font-size:13.5px;font-weight:600;line-height:1.3;text-decoration:none;text-align:center}
.cta2:hover{color:#59615c;border-color:#bfc6c0}
.cream .cta2,.offer .cta2{background:#f3eee0;border-color:#ddd2b6}
''')

# ---- live/gat.js: the small button reports its clicks too
sub('live/gat.js', "  $$('a.cta').forEach(function (a) {", "  $$('a.cta, a.cta2').forEach(function (a) {")
sub('live/gat.js', "      track('gat_button_click', { position: pos, revealed: body.classList.contains('revealed') });",
    "      track('gat_button_click', { position: pos, option: a.classList.contains('cta2') ? 'single' : 'trial', revealed: body.classList.contains('revealed') });")
print('round 8 patch applied')
