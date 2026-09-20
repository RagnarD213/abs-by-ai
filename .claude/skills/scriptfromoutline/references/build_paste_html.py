import re, html, sys, subprocess
files = ['s1_glycine.txt', 's2_90days.txt', 's3_foods.txt', 's4_maketime.txt']
BASE = "color:#000000;font-family:Arial;text-align:left;"
SPAN = "color:#000000;text-decoration:none;vertical-align:baseline;font-family:Arial;"
out = []
for f in files:
    t = open(f).read().strip()
    assert '—' not in t and '–' not in t, f
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    title = lines[0].lstrip('# ').strip()
    spoken = ' '.join(l for l in lines[1:] if not l.startswith('['))
    n = len(spoken.split())
    secs = round(n / 2.4)
    note = f"~{n} spoken words ≈ {secs//60}:{secs%60:02d} at normal pace."
    out.append(f'<p style="{BASE}margin-top:24pt;margin-bottom:4pt;line-height:1.15"><span style="{SPAN}font-weight:700;font-style:normal;font-size:16pt">{html.escape(title)}</span></p>')
    out.append(f'<p style="{BASE}margin-top:0pt;margin-bottom:14pt;line-height:1.15"><span style="{SPAN}color:#666666;font-weight:400;font-style:italic;font-size:10pt">{html.escape(note)}</span></p>')
    for l in lines[1:]:
        if l.startswith('['):
            out.append(f'<p style="{BASE}margin-top:14pt;margin-bottom:8pt;line-height:1.15;background-color:#fff2a8"><span style="{SPAN}font-weight:700;font-style:normal;font-size:10pt;background-color:#fff2a8">{html.escape(l)}</span></p>')
        else:
            out.append(f'<p style="{BASE}margin-top:0pt;margin-bottom:10pt;line-height:1.5"><span style="{SPAN}font-weight:400;font-style:normal;font-size:11pt">{html.escape(l)}</span></p>')
    print(f, n, note, file=sys.stderr)
doc = '<meta charset="utf-8">' + ''.join(out)
open('scripts.html', 'w').write(doc)
plain = '\n'.join(re.sub('<[^>]+>', '', p) for p in out)
open('scripts_plain.txt', 'w').write(plain)
