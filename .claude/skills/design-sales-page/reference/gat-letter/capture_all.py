#!/usr/bin/env python3
"""Re-captures every screenshot the review page uses, from the built pages in this folder. Run after `python3 gen.py`."""
import os, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = pathlib.Path(__file__).resolve().parent
CAP = H.parent / 'tools/cap.sh'
P, T, D = dict(W='390', VH='844'), dict(W='768', VH='1024', SC='1'), dict(W='1440', VH='900', SC='1')
L3 = '[data-sec="L3"]'
jobs = [('caps', 'p-after', '3-after-offer.html', 60000, dict(P, SCROLL=f'#studies|{L3}')),
        ('caps', 'p-before', '2-before-offer.html', 3000, P),
        ('caps', 'p-bottom', '3b-after-offer-bottom-bar.html', 3000, dict(P, SCROLL=L3)),
        ('caps', 't-after', '3-after-offer.html', 60000, dict(T, SCROLL='#offer|#letter')),
        ('caps', 'd-after', '3-after-offer.html', 3000, dict(D, SCROLL='#offer|#studies|#letter')),
        ('caps', 'd-before', '2-before-offer.html', 3000, D),
        ('caps', 'd-bottom', '3b-after-offer-bottom-bar.html', 3000, dict(D, SCROLL=L3)),
        ('caps', 'p-checkout', '4-checkout.html', 30000, P), ('caps', 't-checkout', '4-checkout.html', 30000, T),
        ('caps', 'd-checkout', '4-checkout.html', 30000, D), ('caps', 'p-quiz', '1-quiz.html', 3000, P)]
for f in ['questions', 'how-it-works', 'ingredients', 'shipping-returns', 'contact', 'about', 'privacy', 'terms', 'disclaimer']:
    for pre, env in (('p', P), ('t', T), ('d', D)):
        jobs.append(('caps/info', f'{pre}-{f}', f'p-{f}.html', 40000, env))
only = sys.argv[1:]
def run(j):
    d, name, page, maxh, env = j
    (H / d).mkdir(parents=True, exist_ok=True)
    for old in (H / d).glob(f'{name}-full-*.jpg'):
        old.unlink()
    r = subprocess.run(['zsh', str(CAP), name, f'file://{H}/{page}', str(maxh)], cwd=H / d, env=dict(os.environ, **env), capture_output=True, text=True)
    return name, r.returncode, r.stdout.strip()
with ThreadPoolExecutor(6) as ex:
    for name, rc, out in ex.map(run, [j for j in jobs if not only or any(o in j[1] for o in only)]):
        if rc:
            print('FAILED', name, out)
print('captured')
